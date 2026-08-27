#!/usr/bin/env python3
"""Export a privacy-preserving aggregate from an existing E3 benchmark CSV.

This tool intentionally does NOT implement a second evidence standard. It imports
and reuses scripts/summarize_historical_benchmark.py, then removes partner/source
names, case IDs, scope text, structured case facts, notes, and row-level errors.

The evaluated CSV never leaves the operator's machine unless they choose to share
it. The output is suitable for sharing as aggregate benchmark evidence, but an
aggregate file alone does not prove representative sampling or partner identity.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_SCRIPT = ROOT / "scripts" / "summarize_historical_benchmark.py"
_spec = importlib.util.spec_from_file_location("e3_summary", SUMMARY_SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load {SUMMARY_SCRIPT}")
_e3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_e3)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _is_yes(value: Any) -> bool:
    return _text(value).lower() in {"1", "true", "yes", "y"}


def _load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV must contain a header")
        return list(reader)


def _float_values(rows: list[dict[str, str]], field: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        raw = _text(row.get(field))
        if not raw:
            continue
        try:
            values.append(float(raw))
        except ValueError:
            continue
    return values


def _count(rows: list[dict[str, str]], field: str, *, upper: bool = False) -> dict[str, int]:
    values = Counter()
    for row in rows:
        value = _text(row.get(field))
        if not value:
            continue
        if upper:
            value = value.upper()
        values[value] += 1
    return dict(sorted(values.items()))


def build_private_summary(path: Path) -> dict[str, Any]:
    rows = _load_rows(path)
    full_summary = _e3.summarize(rows)
    benchmarks = full_summary["partner_benchmarks"]
    if len(benchmarks) != 1:
        raise ValueError(
            "Private aggregate files must contain exactly one partner/source benchmark; "
            f"found {len(benchmarks)}"
        )

    benchmark = benchmarks[0]
    usable_rows = [row for row in rows if _is_yes(row.get("usable_case"))]

    error_counts: Counter[str] = Counter()
    for invalid in benchmark["invalid_cases"]:
        for error in invalid.get("errors", []):
            error_counts[str(error)] += 1

    research_minutes = _float_values(usable_rows, "manual_research_minutes")

    payload: dict[str, Any] = {
        "report": "ProjectPermit_private_E3_aggregate",
        "report_version": 1,
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "privacy_boundary": (
            "Aggregate only: no partner/source name, case ID, scope summary, address, "
            "project/property facts, notes, or row-level error record is included."
        ),
        "evidence_boundary": (
            "This report reuses the canonical E3 validator. It is not sufficient by itself "
            "to prove partner identity or representative sampling; E3 requires an external "
            "attestation of the sample window and non-hand-picked sampling method."
        ),
        "rows_recorded": benchmark["rows_recorded"],
        "usable_cases": benchmark["usable_cases"],
        "comparable_cases": benchmark["comparable_cases"],
        "agreement_rate": benchmark["agreement_rate"],
        "disagreements": benchmark["disagreements"],
        "material_disagreements": benchmark["material_disagreements"],
        "false_likely_not_required": benchmark["false_likely_not_required"],
        "municipal_confirmation_outputs": benchmark["municipal_confirmation_outputs"],
        "out_of_scope_outputs": benchmark["out_of_scope_outputs"],
        "sampling_methods": benchmark["sampling_methods"],
        "sample_windows": benchmark["sample_windows"],
        "duplicate_case_id_count": len(benchmark["duplicate_case_ids"]),
        "invalid_case_count": len(benchmark["invalid_cases"]),
        "invalid_error_counts": dict(sorted(error_counts.items())),
        "canonical_e3_validator_qualified": benchmark["e3_qualified"],
        "jurisdiction_counts": _count(usable_rows, "jurisdiction"),
        "project_family_counts": _count(usable_rows, "project_family"),
        "historical_determination_counts": _count(
            usable_rows, "historical_determination", upper=True
        ),
        "projectpermit_determination_counts": _count(
            usable_rows, "projectpermit_determination", upper=True
        ),
        "address_aware_cases": sum(
            1 for row in usable_rows if _is_yes(row.get("address_resolution_needed"))
        ),
        "workflow_changed_yes": sum(
            1 for row in usable_rows if _is_yes(row.get("workflow_changed"))
        ),
        "manual_research_minutes": {
            "reported_cases": len(research_minutes),
            "mean": round(statistics.mean(research_minutes), 2) if research_minutes else None,
            "median": round(statistics.median(research_minutes), 2) if research_minutes else None,
        },
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Locally evaluated historical benchmark CSV")
    parser.add_argument("--output", "-o", help="Optional aggregate JSON output path")
    args = parser.parse_args()

    input_path = Path(args.csv_path)
    payload = build_private_summary(input_path)
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
