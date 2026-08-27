#!/usr/bin/env python3
"""Evaluate de-identified partner E3 cases through the deterministic rules engine.

Input is the historical benchmark CSV shape. Exact addresses are intentionally not
accepted or required here. Address-aware cases must already contain only the
derived non-PII property facts needed by the rules engine.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from projectpermit import SUPPORTED_JURISDICTIONS, evaluate_project


YES = {"1", "true", "yes", "y"}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _is_yes(value: Any) -> bool:
    return _text(value).lower() in YES


def _json_mapping(value: Any, *, field: str, case_id: str, required: bool) -> dict[str, Any]:
    text = _text(value)
    if not text:
        if required:
            raise ValueError(f"{case_id}: {field} is required")
        return {}
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{case_id}: {field} must be valid JSON") from exc
    if not isinstance(decoded, Mapping):
        raise ValueError(f"{case_id}: {field} must be a JSON object")
    return dict(decoded)


def evaluate_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    evaluated: list[dict[str, str]] = []

    for raw in rows:
        row = {str(key): _text(value) for key, value in raw.items()}
        if not _is_yes(row.get("usable_case")):
            evaluated.append(row)
            continue

        case_id = row.get("case_id") or "<missing-case-id>"
        jurisdiction = row.get("jurisdiction", "")
        project_family = row.get("project_family", "")
        if not jurisdiction:
            raise ValueError(f"{case_id}: jurisdiction is required")
        if not project_family:
            raise ValueError(f"{case_id}: project_family is required")

        project = _json_mapping(
            row.get("project_facts_json"),
            field="project_facts_json",
            case_id=case_id,
            required=True,
        )
        if _text(project.get("family")) != project_family:
            raise ValueError(f"{case_id}: project_facts_json.family must match project_family")

        address_aware = _is_yes(row.get("address_resolution_needed"))
        property_facts = _json_mapping(
            row.get("property_facts_json"),
            field="property_facts_json",
            case_id=case_id,
            required=address_aware,
        )

        facts: dict[str, Any] = {
            "jurisdiction": jurisdiction,
            "project": project,
        }
        if property_facts:
            facts["property"] = property_facts

        result = evaluate_project(facts)
        determination = _text(result.get("determination")).upper()
        confidence = _text(result.get("confidence")).upper()
        if not determination:
            raise ValueError(f"{case_id}: ProjectPermit returned no determination")

        historical = row.get("historical_determination", "").upper()
        agreement = bool(historical and historical == determination)
        row["projectpermit_determination"] = determination
        row["projectpermit_confidence"] = confidence
        row["agreement"] = "yes" if agreement else "no"
        # Exact agreement cannot be a material disagreement. Any disagreement must
        # be reviewed by a human after each run; clear stale/pre-filled values so a
        # re-run cannot accidentally preserve an old materiality judgment.
        row["material_disagreement"] = "no" if agreement else ""
        row["false_likely_not_required"] = (
            "yes" if historical == "REQUIRED" and determination == "LIKELY_NOT_REQUIRED" else "no"
        )
        row["unsupported_jurisdiction"] = "yes" if jurisdiction not in SUPPORTED_JURISDICTIONS else "no"
        row["unsupported_family"] = (
            "yes" if determination == "OUT_OF_SCOPE" and jurisdiction in SUPPORTED_JURISDICTIONS else "no"
        )
        evaluated.append(row)

    return evaluated


def load_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV must contain a header")
        return list(reader), list(reader.fieldnames)


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    required_output_fields = (
        "projectpermit_determination",
        "projectpermit_confidence",
        "agreement",
        "material_disagreement",
        "false_likely_not_required",
        "unsupported_family",
        "unsupported_jurisdiction",
    )
    output_fields = list(fieldnames)
    for field in required_output_fields:
        if field not in output_fields:
            output_fields.append(field)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    input_path = Path(args.csv_path)
    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}.evaluated.csv")
    if output_path.resolve() == input_path.resolve():
        raise SystemExit("Refusing to overwrite the source benchmark CSV; choose a different --output path")

    rows, fieldnames = load_rows(input_path)
    evaluated = evaluate_rows(rows)
    write_rows(output_path, evaluated, fieldnames)
    print(json.dumps({"input": str(input_path), "output": str(output_path), "rows": len(evaluated)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
