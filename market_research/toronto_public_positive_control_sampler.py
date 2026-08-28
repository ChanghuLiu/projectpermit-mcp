"""Build a privacy-minimized Toronto permit-positive candidate sample.

This is technical safety-benchmark tooling only. It streams City of Toronto Active
and Cleared building-permit CSV resources, keeps issued 2026 residential records
that map textually to a current ProjectPermit family, deduplicates permit revisions,
and emits a deterministic chronological candidate sample.

The output is NOT market-validation E3 evidence. It is only a source from which
clearly mappable, already-permit-positive cases may be replayed to detect dangerous
`LIKELY_NOT_REQUIRED` false negatives.

Privacy boundary:
- civic address, postal code, applicant, owner, contractor and contact fields are
  never emitted;
- exact street number/name tokens are removed from scope text if they appear there;
- email/phone-like strings are redacted;
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

RESIDENTIAL_TOKENS = (
    "residential",
    "single family",
    "single-family",
    "single detached",
    "detached dwelling",
    "semi-detached",
    "semi detached",
    "townhouse",
    "row house",
    "dwelling",
    "house",
    "secondary suite",
    "laneway suite",
    "garden suite",
)

NONRESIDENTIAL_TOKENS = (
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


def _residential_basis(structure: str, current_use: str, proposed_use: str) -> list[str]:
    fields = {
        "structure_type": structure,
        "current_use": current_use,
        "proposed_use": proposed_use,
    }
    combined = " | ".join(fields.values()).lower()
    if _contains_token(combined, NONRESIDENTIAL_TOKENS):
        return []
    return [
        label
        for label, value in fields.items()
        if _contains_token(value, RESIDENTIAL_TOKENS)
    ]


def _family_matches(work: str, description: str) -> dict[str, list[str]]:
    text = f"{work} | {description}".lower()
    matches: dict[str, list[str]] = {}
    for family, tokens in FAMILY_TOKENS.items():
        hits = sorted({token for token in tokens if token in text})
        if hits:
            matches[family] = hits
    return matches


def _sanitize_scope_text(
    text: str,
    *,
    street_num: str,
    street_name: str,
    postal: str,
) -> str:
    value = EMAIL_RE.sub("[redacted-email]", text or "")
    value = PHONE_RE.sub("[redacted-phone]", value)

    # Remove exact address tokens from the row if they appear in the free-text scope.
    # Do not globally remove numbers because dimensions/counts are decision-useful.
    for token in (postal.strip(), street_name.strip(), street_num.strip()):
        if not token or len(token) < 2:
            continue
        value = re.sub(re.escape(token), "[redacted-address]", value, flags=re.I)

    return WHITESPACE_RE.sub(" ", value).strip()


def _stream_source(
    url: str,
    source_name: str,
    *,
    start_date: date,
    end_date: date,
) -> tuple[int, dict[tuple[str, str], dict]]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ProjectPermit public-positive-control/1.0"},
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
            if not permit:
                continue

            structure = _value(row, structure_col).strip()
            current_use = _value(row, current_use_col).strip()
            proposed_use = _value(row, proposed_use_col).strip()
            residential_basis = _residential_basis(structure, current_use, proposed_use)
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

    # Prefer the current Active row when the same permit revision is visible in both
    # sources, but preserve source overlap in aggregate metadata.
    overlap = set(active) & set(cleared)
    combined = dict(cleared)
    combined.update(active)

    ordered = sorted(
        combined.values(),
        key=lambda item: (
            item["issued_date"],
            item["permit_number"],
            item["revision_number"],
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
            "Technical permit-positive false-negative candidate sample only; "
            "not market-validation E3, not an incidence denominator, and not SAM."
        ),
        "selection_rule": (
            "Issued record in fixed date window + explicit residential structure/use token + "
            "at least one current-family token in City WORK/DESCRIPTION; deduplicate by "
            "permit number/revision; deterministic ascending issue-date/permit/revision order; "
            "take first N eligible records."
        ),
        "privacy_boundary": (
            "No civic address/postal/applicant/owner/contractor/contact columns emitted; exact row "
            "street number/name/postal tokens and email/phone-like strings are redacted from scope text."
        ),
        "source_rows_scanned": {"active": active_rows, "cleared": cleared_rows},
        "eligible_unique_permit_revisions": len(combined),
        "cross_source_overlap": len(overlap),
        "sample_limit": args.limit,
        "sample_count": len(sample),
        "cases": sample,
    }

    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "eligible_unique_permit_revisions": len(combined),
                "sample_count": len(sample),
                "cross_source_overlap": len(overlap),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
