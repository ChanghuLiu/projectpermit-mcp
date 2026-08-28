"""Build a privacy-minimized Toronto residential building-permit positive sample.

This is technical safety-benchmark tooling only. It streams City of Toronto Active
and Cleared building-permit CSV resources, keeps issued low-rise residential BLD
records that map textually to a current ProjectPermit family, deduplicates revisions
to one row per base building permit, and emits a deterministic chronological
candidate sample.

The output is NOT market-validation E3 evidence. It is only a source from which
clearly mappable, already-building-permit-positive cases may be replayed to detect
dangerous `LIKELY_NOT_REQUIRED` false negatives.

Privacy boundary:
- civic address, postal code, applicant, owner, contractor and contact fields are
  never emitted;
- if the row's exact `street number + street name` appears inside public scope text,
  that combined address phrase is redacted without deleting standalone numbers;
- postal/email/phone-like strings are redacted;
- only permit id/revision, issue date, non-address classification fields, sanitized
  public work/scope text and deterministic family-token matches are written.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

ACTIVE_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/"
    "6d0229af-bc54-46de-9c2b-26759b01dd05"
)
CLEARED_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/"
    "a96c0ba4-3026-402b-b09d-5b1268b8f810"
)

FAMILY_TOKENS: dict[str, tuple[str, ...]] = {
    "addition": (
        "addition",
        "extension",
        "add storey",
        "add story",
        "rear addition",
        "front addition",
    ),
    "interior_renovation": (
        "interior alteration",
        "interior renovation",
        "renovation",
        "renovate",
        "partition",
        "interior wall",
    ),
    "basement": (
        "basement",
        "cellar",
        "underpin",
    ),
    "deck_porch": (
        "deck",
        "porch",
        "veranda",
        "terrace",
    ),
    "accessory_structure": (
        "garage",
        "shed",
        "carport",
        "accessory structure",
    ),
    "window_door": (
        "window",
        "door",
        "opening",
    ),
    "dwelling_change": (
        "secondary suite",
        "second suite",
        "additional residential unit",
        "additional dwelling unit",
        "laneway suite",
        "garden suite",
        "dwelling unit",
        "convert to residential",
    ),
    "kitchen_bath_plumbing": (
        "kitchen",
        "bathroom",
        "washroom",
        "plumbing",
    ),
}

LOW_RISE_STRUCTURE_TOKENS = (
    "sfd",
    "single family",
    "single-family",
    "single detached",
    "detached dwelling",
    "semi-detached",
    "semi detached",
    "townhouse",
    "row house",
    "laneway",
    "rear yard suite",
    "2 unit",
    "3+ unit",
    "house",
)

EXCLUDED_STRUCTURE_TOKENS = (
    "apartment",
    "group home",
    "multiple use",
    "non residential",
    "non-residential",
    "commercial",
    "industrial",
    "institutional",
    "office",
    "warehouse",
    "other",
)

NONRESIDENTIAL_USE_TOKENS = (
    "industrial",
    "warehouse",
    "office",
    "retail",
    "commercial",
    "institutional",
    "school",
    "hospital",
    "restaurant",
    "factory",
    "automotive",
)

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\d)")
WHITESPACE_RE = re.compile(r"\s+")


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def _find_column(
    fieldnames: list[str], candidates: tuple[str, ...], *, required: bool = True
) -> str | None:
    by_norm = {_norm(name): name for name in fieldnames}
    for candidate in candidates:
        key = _norm(candidate)
        if key in by_norm:
            return by_norm[key]
    if required:
        raise RuntimeError(
            f"Could not find any of {candidates!r}; available={fieldnames!r}"
        )
    return None


def _parse_date(value: str) -> date | None:
    text = (value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text[:19] if "T" in fmt else text[:10], fmt).date()
        except ValueError:
            pass
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)
    if match:
        return date(*(int(part) for part in match.groups()))
    return None


def _value(row: dict[str, str], column: str | None) -> str:
    return (row.get(column, "") if column else "") or ""


def _contains_token(text: str, tokens: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in tokens)


def _is_building_permit_number(permit_number: str) -> bool:
    return bool(re.search(r"\bBLD\b", permit_number or "", flags=re.I))


def _low_rise_residential_basis(
    structure: str,
    current_use: str,
    proposed_use: str,
) -> list[str]:
    structure_lower = structure.lower()
    if _contains_token(structure_lower, EXCLUDED_STRUCTURE_TOKENS):
        return []
    if not _contains_token(structure_lower, LOW_RISE_STRUCTURE_TOKENS):
        return []

    use_combined = f"{current_use} | {proposed_use}".lower()
    if _contains_token(use_combined, NONRESIDENTIAL_USE_TOKENS):
        return []

    basis = ["structure_type"]
    if current_use.strip():
        basis.append("current_use")
    if proposed_use.strip():
        basis.append("proposed_use")
    return basis


def _family_matches(work: str, description: str) -> dict[str, list[str]]:
    text = f"{work} | {description}".lower()
    matches: dict[str, list[str]] = {}
    for family, tokens in FAMILY_TOKENS.items():
        hits = sorted({token for token in tokens if token in text})
        if hits:
            matches[family] = hits
    return matches


def _combined_address_pattern(street_num: str, street_name: str) -> re.Pattern[str] | None:
    num = street_num.strip()
    name = street_name.strip()
    if not num or not name:
        return None
    # Match only the combined civic-number + street-name phrase. Never redact a
    # standalone number because it may be a dimension, count or cost fact.
    escaped_name = re.escape(name).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\w){re.escape(num)}\s+{escaped_name}(?!\w)", re.I)


def _sanitize_scope_text(
    text: str,
    *,
    street_num: str,
    street_name: str,
    postal: str,
) -> str:
    value = EMAIL_RE.sub("[redacted-email]", text or "")
    value = PHONE_RE.sub("[redacted-phone]", value)

    address_pattern = _combined_address_pattern(street_num, street_name)
    if address_pattern:
        value = address_pattern.sub("[redacted-address]", value)

    postal_token = postal.strip()
    if postal_token:
        value = re.sub(re.escape(postal_token), "[redacted-postal]", value, flags=re.I)

    return WHITESPACE_RE.sub(" ", value).strip()


def _revision_sort_key(value: str) -> tuple[int, str]:
    text = (value or "").strip()
    match = re.match(r"^(\d+)", text)
    return (int(match.group(1)) if match else -1, text)


def _stream_source(
    url: str,
    source_name: str,
    *,
    start_date: date,
    end_date: date,
) -> tuple[int, dict[tuple[str, str], dict]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ProjectPermit public-positive-control/1.1"},
    )
    source_rows = 0
    selected: dict[tuple[str, str], dict] = {}

    with urllib.request.urlopen(request, timeout=180) as response:
        reader = csv.DictReader(
            io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        )
        if not reader.fieldnames:
            raise RuntimeError(f"{source_name}: CSV has no header")
        fieldnames = list(reader.fieldnames)

        permit_col = _find_column(fieldnames, ("PERMIT_NUM", "PERMIT NUMBER", "PERMITNUM"))
        revision_col = _find_column(fieldnames, ("REVISION_NUM", "REVISION NUMBER", "REVISIONNUM"))
        issued_col = _find_column(fieldnames, ("ISSUED_DATE", "ISSUED DATE", "ISSUEDDATE"))
        permit_type_col = _find_column(fieldnames, ("PERMIT_TYPE", "PERMIT TYPE", "PERMITTYPE"))
        structure_col = _find_column(fieldnames, ("STRUCTURE_TYPE", "STRUCTURE TYPE", "STRUCTURETYPE"), required=False)
        work_col = _find_column(fieldnames, ("WORK", "WORK TYPE", "WORKTYPE"), required=False)
        description_col = _find_column(
            fieldnames,
            ("DESCRIPTION", "WORK_DESCRIPTION", "WORK DESCRIPTION", "DESC"),
            required=False,
        )
        current_use_col = _find_column(fieldnames, ("CURRENT_USE", "CURRENT USE", "CURRENTUSE"), required=False)
        proposed_use_col = _find_column(fieldnames, ("PROPOSED_USE", "PROPOSED USE", "PROPOSEDUSE"), required=False)
        street_num_col = _find_column(fieldnames, ("STREET_NUM", "STREET NUMBER", "STREETNUM"), required=False)
        street_name_col = _find_column(fieldnames, ("STREET_NAME", "STREET NAME", "STREETNAME"), required=False)
        postal_col = _find_column(fieldnames, ("POSTAL", "POSTAL_CODE", "POSTAL CODE"), required=False)

        if not description_col:
            raise RuntimeError(
                f"{source_name}: description column is required for this safety sampler; "
                f"available={fieldnames!r}"
            )

        for row in reader:
            source_rows += 1
            issued = _parse_date(_value(row, issued_col))
            if issued is None or issued < start_date or issued > end_date:
                continue

            permit = _value(row, permit_col).strip()
            revision = _value(row, revision_col).strip()
            if not permit or not _is_building_permit_number(permit):
                continue

            structure = _value(row, structure_col).strip()
            current_use = _value(row, current_use_col).strip()
            proposed_use = _value(row, proposed_use_col).strip()
            residential_basis = _low_rise_residential_basis(
                structure, current_use, proposed_use
            )
            if not residential_basis:
                continue

            work = _value(row, work_col).strip()
            description_raw = _value(row, description_col).strip()
            family_matches = _family_matches(work, description_raw)
            if not family_matches:
                continue

            description = _sanitize_scope_text(
                description_raw,
                street_num=_value(row, street_num_col),
                street_name=_value(row, street_name_col),
                postal=_value(row, postal_col),
            )

            selected[(permit, revision)] = {
                "permit_number": permit,
                "revision_number": revision,
                "issued_date": issued.isoformat(),
                "permit_type": _value(row, permit_type_col).strip(),
                "structure_type": structure,
                "work": work,
                "current_use": current_use,
                "proposed_use": proposed_use,
                "scope_text_sanitized": description,
                "residential_basis": residential_basis,
                "family_token_matches": family_matches,
                "source_seen_in": source_name,
            }

    return source_rows, selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", default="2026-06-01")
    parser.add_argument("--end-date", default="2026-08-28")
    parser.add_argument("--limit", type=int, default=60)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("toronto_public_positive_control_candidates.json"),
    )
    args = parser.parse_args()

    start_date = date.fromisoformat(args.start_date)
    end_date = date.fromisoformat(args.end_date)
    if end_date < start_date:
        raise SystemExit("--end-date must be on or after --start-date")
    if args.limit <= 0:
        raise SystemExit("--limit must be positive")

    active_rows, active = _stream_source(
        ACTIVE_URL, "active", start_date=start_date, end_date=end_date
    )
    cleared_rows, cleared = _stream_source(
        CLEARED_URL, "cleared", start_date=start_date, end_date=end_date
    )

    overlap = set(active) & set(cleared)
    combined_revisions = dict(cleared)
    combined_revisions.update(active)

    # One project should not gain weight merely because the City dataset contains
    # multiple revisions. Keep the latest issued/revision row for each base BLD permit.
    by_permit: dict[str, dict] = {}
    for candidate in combined_revisions.values():
        permit = candidate["permit_number"]
        existing = by_permit.get(permit)
        candidate_key = (
            candidate["issued_date"],
            _revision_sort_key(candidate["revision_number"]),
        )
        if existing is None:
            by_permit[permit] = candidate
            continue
        existing_key = (
            existing["issued_date"],
            _revision_sort_key(existing["revision_number"]),
        )
        if candidate_key > existing_key:
            by_permit[permit] = candidate

    ordered = sorted(
        by_permit.values(),
        key=lambda item: (
            item["issued_date"],
            item["permit_number"],
            _revision_sort_key(item["revision_number"]),
        ),
    )
    sample = ordered[: args.limit]

    output = {
        "source": "City of Toronto Open Data — Building Permits Active + Cleared",
        "source_urls": [ACTIVE_URL, CLEARED_URL],
        "captured_by": "GitHub Actions public-data research runner",
        "window": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        "purpose": (
            "Technical building-permit-positive false-negative candidate sample only; "
            "not market-validation E3, not an incidence denominator, and not SAM."
        ),
        "selection_rule": (
            "Issued BLD record in fixed date window + low-rise residential structure/use gate + "
            "at least one current-family token in City WORK/DESCRIPTION; merge Active/Cleared; "
            "deduplicate to latest row per base building permit; deterministic ascending "
            "issue-date/permit order; take first N eligible building permits."
        ),
        "privacy_boundary": (
            "No civic address/postal/applicant/owner/contractor/contact columns emitted; only the "
            "combined exact civic-number + street-name phrase, full postal token and email/phone-like "
            "strings are redacted from scope text; standalone numbers are preserved."
        ),
        "source_rows_scanned": {"active": active_rows, "cleared": cleared_rows},
        "eligible_unique_permit_revisions_before_base_dedup": len(combined_revisions),
        "eligible_unique_building_permits": len(by_permit),
        "cross_source_overlap_revisions": len(overlap),
        "sample_limit": args.limit,
        "sample_count": len(sample),
        "cases": sample,
    }

    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "eligible_unique_permit_revisions_before_base_dedup": len(combined_revisions),
                "eligible_unique_building_permits": len(by_permit),
                "sample_count": len(sample),
                "cross_source_overlap_revisions": len(overlap),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
