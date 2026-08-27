#!/usr/bin/env python3
"""Validate and summarize partner historical benchmarks against the E3 standard.

This tool does not run the permit engine. It audits the evidence record produced
*after* anonymized partner cases have been normalized and evaluated. Its purpose
is to prevent incomplete, hand-picked, or non-reproducible samples from being
counted as E3 market evidence.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping


YES = {"1", "true", "yes", "y"}
NO = {"0", "false", "no", "n"}
BIASED_SAMPLING = {
    "curated",
    "hand-picked",
    "handpicked",
    "selected",
    "selected_successes",
    "success_examples",
}
VALID_DETERMINATIONS = {
    "REQUIRED",
    "LIKELY_NOT_REQUIRED",
    "MUNICIPAL_CONFIRMATION_REQUIRED",
}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _lower(value: Any) -> str:
    return _text(value).lower()


def _bool(value: Any) -> bool | None:
    normalized = _lower(value)
    if normalized in YES:
        return True
    if normalized in NO:
        return False
    return None


def _json_mapping(value: Any) -> Mapping[str, Any] | None:
    text = _text(value)
    if not text:
        return None
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError:
        return None
    return decoded if isinstance(decoded, Mapping) else None


def _usable(row: Mapping[str, Any]) -> bool:
    return _bool(row.get("usable_case")) is True


def _group_key(row: Mapping[str, Any]) -> tuple[str, str]:
    return (_text(row.get("partner")) or "<missing-partner>", _text(row.get("source_platform")) or "<missing-platform>")


def _case_errors(row: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    required_text = (
        "case_id",
        "partner",
        "source_platform",
        "sample_window_start",
        "sample_window_end",
        "sampling_method",
        "jurisdiction",
        "project_family",
        "scope_summary",
        "historical_determination",
        "historical_decision_source",
        "projectpermit_determination",
        "projectpermit_confidence",
        "agreement",
        "material_disagreement",
        "address_resolution_needed",
    )
    for field in required_text:
        if not _text(row.get(field)):
            errors.append(f"missing:{field}")

    project_facts = _json_mapping(row.get("project_facts_json"))
    if project_facts is None:
        errors.append("invalid_or_missing:project_facts_json")
    elif _text(project_facts.get("family")) != _text(row.get("project_family")):
        errors.append("project_family_mismatch")

    address_needed = _bool(row.get("address_resolution_needed"))
    if address_needed is None:
        errors.append("invalid:address_resolution_needed")
    elif address_needed and _json_mapping(row.get("property_facts_json")) is None:
        errors.append("address_aware_case_missing:property_facts_json")

    historical = _text(row.get("historical_determination")).upper()
    projectpermit = _text(row.get("projectpermit_determination")).upper()
    if historical and historical not in VALID_DETERMINATIONS:
        errors.append("invalid:historical_determination")
    if projectpermit and projectpermit not in VALID_DETERMINATIONS:
        errors.append("invalid:projectpermit_determination")

    if _bool(row.get("agreement")) is None:
        errors.append("invalid:agreement")
    if _bool(row.get("material_disagreement")) is None:
        errors.append("invalid:material_disagreement")

    sampling = _lower(row.get("sampling_method")).replace(" ", "_")
    if sampling in {value.replace("-", "_") for value in BIASED_SAMPLING}:
        errors.append("biased_sampling_method")

    return errors


def summarize(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    materialized = [dict(row) for row in rows]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in materialized:
        grouped[_group_key(row)].append(row)

    partner_benchmarks: list[dict[str, Any]] = []
    qualified_count = 0

    for (partner, platform), group_rows in sorted(grouped.items()):
        usable_rows = [row for row in group_rows if _usable(row)]
        ids = [_text(row.get("case_id")) for row in usable_rows if _text(row.get("case_id"))]
        duplicate_case_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})

        invalid_cases: list[dict[str, Any]] = []
        agreement_count = 0
        disagreement_count = 0
        material_disagreements = 0
        false_likely_not_required = 0
        confirm_outputs = 0

        for row in usable_rows:
            errors = _case_errors(row)
            if errors:
                invalid_cases.append({"case_id": _text(row.get("case_id")), "errors": errors})

            agreement = _bool(row.get("agreement"))
            if agreement is True:
                agreement_count += 1
            elif agreement is False:
                disagreement_count += 1

            if _bool(row.get("material_disagreement")) is True:
                material_disagreements += 1

            historical = _text(row.get("historical_determination")).upper()
            projectpermit = _text(row.get("projectpermit_determination")).upper()
            if historical == "REQUIRED" and projectpermit == "LIKELY_NOT_REQUIRED":
                false_likely_not_required += 1
            if projectpermit == "MUNICIPAL_CONFIRMATION_REQUIRED":
                confirm_outputs += 1

        sampling_methods = sorted({_text(row.get("sampling_method")) for row in usable_rows if _text(row.get("sampling_method"))})
        sample_windows = sorted(
            {
                (_text(row.get("sample_window_start")), _text(row.get("sample_window_end")))
                for row in usable_rows
                if _text(row.get("sample_window_start")) or _text(row.get("sample_window_end"))
            }
        )

        e3_qualified = (
            len(usable_rows) >= 5
            and not invalid_cases
            and not duplicate_case_ids
            and len(sampling_methods) == 1
            and len(sample_windows) == 1
        )
        if e3_qualified:
            qualified_count += 1

        comparable = agreement_count + disagreement_count
        partner_benchmarks.append(
            {
                "partner": partner,
                "source_platform": platform,
                "rows_recorded": len(group_rows),
                "usable_cases": len(usable_rows),
                "comparable_cases": comparable,
                "agreement_rate": round(agreement_count / comparable, 4) if comparable else None,
                "disagreements": disagreement_count,
                "material_disagreements": material_disagreements,
                "false_likely_not_required": false_likely_not_required,
                "municipal_confirmation_outputs": confirm_outputs,
                "sampling_methods": sampling_methods,
                "sample_windows": [list(window) for window in sample_windows],
                "duplicate_case_ids": duplicate_case_ids,
                "invalid_cases": invalid_cases,
                "e3_qualified": e3_qualified,
            }
        )

    return {
        "evidence_standard": "E3_historical_case_benchmark",
        "rows_recorded": len(materialized),
        "partner_benchmarks": partner_benchmarks,
        "qualified_partner_benchmarks": qualified_count,
        "note": "E3 qualification here audits sample reproducibility/representativeness only; it does not imply E4 usage or E5 economic evidence.",
    }


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?", default="data/historical_benchmark_template.csv")
    args = parser.parse_args()

    summary = summarize(load_rows(Path(args.csv_path)))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
