"""Aggregate Toronto 2024 issued permit volume by permit type.

This is market-structure research only. It streams the City of Toronto Active and
Cleared building-permit CSV resources, keeps only a minimal permit key/type/date
projection in memory, deduplicates by permit number + revision, and emits only
aggregate counts. No addresses, applicant names, or other row-level data are
written to output.
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


def _stream_source(url: str, source_name: str, target_year: int) -> tuple[int, dict[tuple[str, str], str], dict]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ProjectPermit public-market-research/1.0"},
    )
    source_rows = 0
    selected: dict[tuple[str, str], str] = {}

    with urllib.request.urlopen(request, timeout=180) as response:
        reader = csv.DictReader(io.TextIOWrapper(response, encoding="utf-8-sig", newline=""))
        if not reader.fieldnames:
            raise RuntimeError(f"{source_name}: CSV has no header")
        fieldnames = list(reader.fieldnames)
        permit_col = _find_column(fieldnames, ("PERMIT_NUM", "PERMIT NUMBER", "PERMITNUM"))
        revision_col = _find_column(fieldnames, ("REVISION_NUM", "REVISION NUMBER", "REVISIONNUM"))
        type_col = _find_column(fieldnames, ("PERMIT_TYPE", "PERMIT TYPE", "PERMITTYPE"))
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
            selected[(permit, revision)] = permit_type

    schema = {
        "permit_column": permit_col,
        "revision_column": revision_col,
        "permit_type_column": type_col,
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

    counts = Counter(combined.values())
    ordered_counts = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

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
            for permit_type, count in counts.items()
            if any(token in permit_type.lower() for token in tokens)
        )

    result = {
        "source": "City of Toronto Open Data — Building Permits Active + Cleared",
        "reference_year": args.year,
        "evidence_boundary": (
            "City-level issued-permit workload only. This does not identify contractor accounts, "
            "does not measure ProjectPermit preflight incidence, and is not E3/E4/E5 evidence."
        ),
        "privacy_boundary": (
            "Only permit number/revision/type/issued-date are read for deduplication and aggregation; "
            "no address/applicant/contractor fields are emitted."
        ),
        "source_rows": {"active": active_rows, "cleared": cleared_rows},
        "schema": {"active": active_schema, "cleared": cleared_schema},
        "issued_records_before_cross_source_dedup": {
            "active": len(active),
            "cleared": len(cleared),
        },
        "cross_source_overlap_records": len(overlap),
        "unique_issued_permit_revisions": len(combined),
        "permit_type_counts": ordered_counts,
        "trade_focus_counts": focus_counts,
    }

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
