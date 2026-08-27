"""Aggregate Toronto issued permit volume by permit type and work type.

This is market-structure research only. It streams the City of Toronto Active and
Cleared building-permit CSV resources, keeps only a minimal permit key/type/work/date
projection in memory, deduplicates by permit number + revision, and emits only
aggregate counts. No addresses, descriptions, applicant names, or other row-level
data are written to output.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

ACTIVE_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/"
    "6d0229af-bc54-46de-9c2b-26759b01dd05"
)
CLEARED_URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/"
    "a96c0ba4-3026-402b-b09d-5b1268b8f810"
)


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def _find_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str:
    by_norm = {_norm(name): name for name in fieldnames}
    for candidate in candidates:
        key = _norm(candidate)
        if key in by_norm:
            return by_norm[key]
    raise RuntimeError(
        f"Could not find any of {candidates!r}; available={fieldnames!r}"
    )


def _year(value: str) -> int | None:
    text = (value or "").strip()
    if not text:
        return None
    match = re.match(r"^(\d{4})", text)
    if match:
        return int(match.group(1))
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text[:10], fmt).year
        except ValueError:
            pass
    return None


def _stream_source(
    url: str,
    source_name: str,
    target_year: int,
) -> tuple[int, dict[tuple[str, str], tuple[str, str]], dict]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ProjectPermit public-market-research/1.0"},
    )
    source_rows = 0
    selected: dict[tuple[str, str], tuple[str, str]] = {}

    with urllib.request.urlopen(request, timeout=180) as response:
        reader = csv.DictReader(io.TextIOWrapper(response, encoding="utf-8-sig", newline=""))
        if not reader.fieldnames:
            raise RuntimeError(f"{source_name}: CSV has no header")
        fieldnames = list(reader.fieldnames)
        permit_col = _find_column(fieldnames, ("PERMIT_NUM", "PERMIT NUMBER", "PERMITNUM"))
        revision_col = _find_column(fieldnames, ("REVISION_NUM", "REVISION NUMBER", "REVISIONNUM"))
        type_col = _find_column(fieldnames, ("PERMIT_TYPE", "PERMIT TYPE", "PERMITTYPE"))
        work_col = _find_column(fieldnames, ("WORK", "WORK TYPE", "WORKTYPE"))
        issued_col = _find_column(fieldnames, ("ISSUED_DATE", "ISSUED DATE", "ISSUEDDATE"))

        for row in reader:
            source_rows += 1
            if _year(row.get(issued_col, "")) != target_year:
                continue
            permit = (row.get(permit_col) or "").strip()
            revision = (row.get(revision_col) or "").strip()
            if not permit:
                continue
            permit_type = (row.get(type_col) or "").strip() or "(blank)"
            work_type = (row.get(work_col) or "").strip() or "(blank)"
            selected[(permit, revision)] = (permit_type, work_type)

    schema = {
        "permit_column": permit_col,
        "revision_column": revision_col,
        "permit_type_column": type_col,
        "work_column": work_col,
        "issued_date_column": issued_col,
    }
    return source_rows, selected, schema


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--output", type=Path, default=Path("toronto_trade_permit_volume.json"))
    args = parser.parse_args()

    active_rows, active, active_schema = _stream_source(ACTIVE_URL, "active", args.year)
    cleared_rows, cleared, cleared_schema = _stream_source(CLEARED_URL, "cleared", args.year)

    combined = dict(cleared)
    overlap = set(active) & set(cleared)
    combined.update(active)

    permit_type_counts = Counter(permit_type for permit_type, _ in combined.values())
    work_type_counts = Counter(work_type for _, work_type in combined.values())
    pair_counts = Counter(combined.values())

    ordered_permit_counts = dict(
        sorted(permit_type_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    ordered_work_counts = dict(
        sorted(work_type_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    ordered_pair_counts = [
        {"permit_type": permit_type, "work": work_type, "count": count}
        for (permit_type, work_type), count in sorted(
            pair_counts.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
        )
    ]

    focus_tokens = {
        "mechanical": ("mechanical",),
        "plumbing": ("plumbing",),
        "drain_site_service": ("drain", "site service", "site-service"),
        "electrical": ("electrical",),
        "heating_hvac": ("heating", "hvac"),
    }
    focus_counts = {}
    for label, tokens in focus_tokens.items():
        focus_counts[label] = sum(
            count
            for permit_type, count in permit_type_counts.items()
            if any(token in permit_type.lower() for token in tokens)
        )

    # Conservative current-family signals based only on City-provided WORK labels.
    # These are not claimed to be complete mappings: ambiguous labels stay unmapped.
    family_work_tokens = {
        "addition": ("addition",),
        "interior_renovation": ("interior", "alteration", "renovation"),
        "basement": ("basement",),
        "deck_porch": ("deck", "porch"),
        "accessory_structure": ("garage", "shed", "accessory"),
        "window_door": ("window", "door"),
        "dwelling_change": ("conversion", "convert", "second suite", "secondary suite", "additional residential"),
        "kitchen_bath_plumbing": ("plumbing", "kitchen", "bathroom", "washroom"),
    }
    current_family_work_signal = {}
    matched_work_types: set[str] = set()
    for family, tokens in family_work_tokens.items():
        matched = {
            work_type: count
            for work_type, count in work_type_counts.items()
            if any(token in work_type.lower() for token in tokens)
        }
        current_family_work_signal[family] = {
            "count": sum(matched.values()),
            "work_types": dict(sorted(matched.items(), key=lambda item: (-item[1], item[0]))),
        }
        matched_work_types.update(matched)

    unmapped_work_count = sum(
        count for work_type, count in work_type_counts.items() if work_type not in matched_work_types
    )

    result = {
        "source": "City of Toronto Open Data — Building Permits Active + Cleared",
        "reference_year": args.year,
        "evidence_boundary": (
            "City-level issued-permit workload only. This does not identify contractor accounts, "
            "does not measure ProjectPermit preflight incidence, and is not E3/E4/E5 evidence. "
            "Current-family work-label matching is a conservative/diagnostic signal, not SAM."
        ),
        "privacy_boundary": (
            "Only permit number/revision/type/work/issued-date are read for deduplication and aggregate counts; "
            "no addresses, descriptions, applicants, contractors, or row-level records are emitted."
        ),
        "source_rows": {"active": active_rows, "cleared": cleared_rows},
        "schema": {"active": active_schema, "cleared": cleared_schema},
        "issued_records_before_cross_source_dedup": {
            "active": len(active),
            "cleared": len(cleared),
        },
        "cross_source_overlap_records": len(overlap),
        "unique_issued_permit_revisions": len(combined),
        "permit_type_counts": ordered_permit_counts,
        "work_type_counts": ordered_work_counts,
        "permit_type_work_counts": ordered_pair_counts,
        "trade_focus_counts": focus_counts,
        "current_family_work_signal": current_family_work_signal,
        "current_family_matched_work_count_nonexclusive": sum(
            item["count"] for item in current_family_work_signal.values()
        ),
        "unmapped_unique_work_labels_count": sum(
            1 for work_type in work_type_counts if work_type not in matched_work_types
        ),
        "unmapped_work_count": unmapped_work_count,
    }

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
