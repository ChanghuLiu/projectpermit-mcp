#!/usr/bin/env python3
"""Validate and summarize ProjectPermit operator-rescue evidence CSVs.

Research/evidence utility only. It keeps unique requests, supported-jurisdiction
requests, candidate preflights, partner-delivered copies, unresolved cases and
material hits as separate denominators.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

CURRENT_FAMILIES = {
    "window_door",
    "interior_renovation",
    "basement",
    "dwelling_change",
    "deck_porch",
    "accessory_structure",
    "addition",
    "kitchen_bath_plumbing",
}
PERMIT_STATES = {"KNOWN_REQUIRED", "KNOWN_NOT_REQUIRED", "UNRESOLVED", "NOT_CHECKED", "UNKNOWN"}
FACT_CLASSES = {
    "DIRECT_STRUCTURED",
    "TEXT_DERIVABLE",
    "FOLLOWUP_REQUIRED",
    "EXTERNAL_PROPERTY_LOOKUP_REQUIRED",
    "INSUFFICIENT_FOR_CURRENT_RULES",
}
MATERIAL_CLASSES = {
    "MATERIAL_EFFECT_CONFIRMED",
    "POSSIBLE_EFFECT_NOT_MEASURED",
    "NO_MATERIAL_EFFECT",
    "UNKNOWN",
}
INTEGRATION_TOPOLOGIES = {
    "CENTRAL_SINGLE_INTEGRATION",
    "CENTRAL_WITH_SITE_MAPPING",
    "SEPARATE_SITE_INTEGRATIONS",
    "MANUAL_EXPORT_ONLY",
    "UNKNOWN",
}
CENTRAL_TOPOLOGIES = {"CENTRAL_SINGLE_INTEGRATION", "CENTRAL_WITH_SITE_MAPPING"}
YES_VALUES = {"1", "true", "yes", "y"}
NO_VALUES = {"0", "false", "no", "n"}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: CSV must contain a header")
        return list(reader)


def _optional_int(row: dict[str, str], field: str, label: str) -> int | None:
    raw = _text(row.get(field))
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{label}: {field} must be an integer, got {raw!r}") from exc
    if value < 0:
        raise ValueError(f"{label}: {field} must be >= 0")
    return value


def _optional_float(row: dict[str, str], field: str, label: str) -> float | None:
    raw = _text(row.get(field))
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{label}: {field} must be numeric, got {raw!r}") from exc
    if value < 0:
        raise ValueError(f"{label}: {field} must be >= 0")
    return value


def _optional_bool(value: Any, *, label: str, field: str) -> bool | None:
    raw = _text(value).lower()
    if not raw:
        return None
    if raw in YES_VALUES:
        return True
    if raw in NO_VALUES:
        return False
    raise ValueError(f"{label}: {field} must be yes/no when populated, got {value!r}")


def _pct(numerator: int, denominator: int) -> float | None:
    return round(numerator * 100.0 / denominator, 2) if denominator > 0 else None


def summarize_monthly(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        raise ValueError("monthly aggregate CSV has no rows")

    operators = {_text(row.get("operator")) for row in rows if _text(row.get("operator"))}
    months = {_text(row.get("complete_month")) for row in rows if _text(row.get("complete_month"))}
    if len(operators) != 1:
        raise ValueError(f"monthly aggregate must contain exactly one operator, found {sorted(operators)}")
    if len(months) != 1:
        raise ValueError(f"monthly aggregate must contain exactly one complete month, found {sorted(months)}")

    count_fields = [
        "unique_requests",
        "candidate_preflight_requests",
        "within_supported_jurisdictions",
        "known_required",
        "known_not_required",
        "unresolved",
        "not_checked",
        "unknown_permit_state",
        "required_followup_or_research",
        "material_effect_known_count",
        "partner_deliveries",
    ]
    totals: Counter[str] = Counter()
    family_rows: list[dict[str, Any]] = []
    topology_values: set[str] = set()

    for index, row in enumerate(rows, start=2):
        family = _text(row.get("current_family"))
        label = f"monthly row {index} ({family or 'missing family'})"
        if family not in CURRENT_FAMILIES:
            raise ValueError(f"{label}: unsupported current_family {family!r}")

        values = {field: _optional_int(row, field, label) for field in count_fields}
        unique = values["unique_requests"]
        candidate = values["candidate_preflight_requests"]
        supported = values["within_supported_jurisdictions"]
        unresolved = values["unresolved"]
        material = values["material_effect_known_count"]

        if unique is not None:
            for field in count_fields:
                if field == "partner_deliveries":
                    continue
                value = values[field]
                if value is not None and value > unique:
                    raise ValueError(f"{label}: {field} cannot exceed unique_requests")
        if candidate is not None and supported is not None and candidate > supported:
            raise ValueError(f"{label}: candidate_preflight_requests cannot exceed within_supported_jurisdictions")
        if unresolved is not None and candidate is not None and unresolved > candidate:
            raise ValueError(f"{label}: unresolved cannot exceed candidate_preflight_requests")
        if material is not None and candidate is not None and material > candidate:
            raise ValueError(f"{label}: material_effect_known_count cannot exceed candidate_preflight_requests")

        state_values = [values[name] for name in (
            "known_required", "known_not_required", "unresolved", "not_checked", "unknown_permit_state"
        )]
        if unique is not None and all(value is not None for value in state_values):
            state_total = sum(value for value in state_values if value is not None)
            if state_total > unique:
                raise ValueError(f"{label}: permit-state counts sum to {state_total}, above unique_requests={unique}")

        partner_deliveries = values["partner_deliveries"]
        reported_multiplier = _optional_float(row, "delivery_multiplier", label)
        computed_multiplier = None
        if unique not in (None, 0) and partner_deliveries is not None:
            computed_multiplier = round(partner_deliveries / unique, 4)
            if reported_multiplier is not None and abs(reported_multiplier - computed_multiplier) > 0.02:
                raise ValueError(
                    f"{label}: delivery_multiplier={reported_multiplier} disagrees with "
                    f"partner_deliveries/unique_requests={computed_multiplier}"
                )

        topology = _text(row.get("integration_topology")).upper()
        if topology:
            if topology not in INTEGRATION_TOPOLOGIES:
                raise ValueError(f"{label}: invalid integration_topology {topology!r}")
            topology_values.add(topology)

        for field, value in values.items():
            if value is not None:
                totals[field] += value
        family_rows.append({
            "current_family": family,
            **values,
            "computed_delivery_multiplier": computed_multiplier,
            "integration_topology": topology or None,
        })

    unique_total = totals["unique_requests"]
    candidate_total = totals["candidate_preflight_requests"]
    unresolved_total = totals["unresolved"]
    partner_delivery_total = totals["partner_deliveries"]
    topology_list = sorted(topology_values)
    central_integration_plausible = bool(topology_values & CENTRAL_TOPOLOGIES) and (
        "SEPARATE_SITE_INTEGRATIONS" not in topology_values
    )

    return {
        "operator": next(iter(operators)),
        "complete_month": next(iter(months)),
        "families_recorded": len(rows),
        "family_rows": family_rows,
        "totals": dict(totals),
        "unresolved_share_of_candidate_pct": _pct(unresolved_total, candidate_total),
        "candidate_share_of_unique_pct": _pct(candidate_total, unique_total),
        "delivery_multiplier": round(partner_delivery_total / unique_total, 4)
        if unique_total > 0 and partner_delivery_total > 0 else None,
        "integration_topologies": topology_list,
        "central_integration_plausible": central_integration_plausible,
        "commercial_500_call_gate": candidate_total >= 500,
    }


def summarize_sample(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        return {
            "sampled_cases": 0,
            "candidate_cases": 0,
            "supported_cases": 0,
            "permit_state_counts": {},
            "fact_sufficiency_counts": {},
            "decision_fact_sufficiency_rate_pct": None,
            "material_effect_counts": {},
            "material_effect_confirmed_candidate_count": 0,
            "material_hit_rate_pct": None,
            "safety_material_disagreements": 0,
        }

    ids = [_text(row.get("sample_id")) for row in rows]
    missing_ids = [index + 2 for index, sample_id in enumerate(ids) if not sample_id]
    if missing_ids:
        raise ValueError(f"sample rows missing sample_id at CSV lines {missing_ids}")
    duplicates = sorted(sample_id for sample_id, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise ValueError(f"sample contains duplicate sample_id values: {duplicates}")

    fact_counts: Counter[str] = Counter()
    material_counts: Counter[str] = Counter()
    permit_state_counts: Counter[str] = Counter()
    supported_cases = candidate_cases = sufficient_candidate_cases = 0
    material_confirmed_candidate = safety_material_disagreements = 0

    for index, row in enumerate(rows, start=2):
        sample_id = _text(row.get("sample_id"))
        label = f"sample row {index} ({sample_id})"
        family = _text(row.get("current_family"))
        if family and family not in CURRENT_FAMILIES:
            raise ValueError(f"{label}: unsupported current_family {family!r}")

        supported = _optional_bool(row.get("within_supported_jurisdiction"), label=label, field="within_supported_jurisdiction")
        candidate = _optional_bool(row.get("candidate_preflight"), label=label, field="candidate_preflight")
        if candidate is True and supported is False:
            raise ValueError(f"{label}: candidate_preflight=yes cannot have within_supported_jurisdiction=no")
        supported_cases += int(supported is True)
        candidate_cases += int(candidate is True)

        permit_state = _text(row.get("permit_state_at_intake")).upper()
        if permit_state:
            if permit_state not in PERMIT_STATES:
                raise ValueError(f"{label}: invalid permit_state_at_intake {permit_state!r}")
            permit_state_counts[permit_state] += 1

        fact_class = _text(row.get("fact_sufficiency_class")).upper()
        if fact_class:
            if fact_class not in FACT_CLASSES:
                raise ValueError(f"{label}: invalid fact_sufficiency_class {fact_class!r}")
            fact_counts[fact_class] += 1
            if candidate is True and fact_class in {"DIRECT_STRUCTURED", "TEXT_DERIVABLE"}:
                sufficient_candidate_cases += 1

        material_class = _text(row.get("material_effect_class")).upper()
        if material_class:
            if material_class not in MATERIAL_CLASSES:
                raise ValueError(f"{label}: invalid material_effect_class {material_class!r}")
            material_counts[material_class] += 1
            if candidate is True and material_class == "MATERIAL_EFFECT_CONFIRMED":
                material_confirmed_candidate += 1

        disagreement_material = _optional_bool(row.get("disagreement_material"), label=label, field="disagreement_material")
        safety_direction = _text(row.get("safety_direction")).upper()
        if disagreement_material is True and safety_direction in {
            "LESS_CONSERVATIVE", "FALSE_LIKELY_NOT_REQUIRED", "UNSAFE_LESS_CONSERVATIVE"
        }:
            safety_material_disagreements += 1

    return {
        "sampled_cases": len(rows),
        "supported_cases": supported_cases,
        "candidate_cases": candidate_cases,
        "permit_state_counts": dict(sorted(permit_state_counts.items())),
        "fact_sufficiency_counts": dict(sorted(fact_counts.items())),
        "decision_fact_sufficiency_rate_pct": _pct(sufficient_candidate_cases, candidate_cases),
        "material_effect_counts": dict(sorted(material_counts.items())),
        "material_effect_confirmed_candidate_count": material_confirmed_candidate,
        "material_hit_rate_pct": _pct(material_confirmed_candidate, candidate_cases),
        "safety_material_disagreements": safety_material_disagreements,
    }


def build_summary(monthly_path: Path, sample_path: Path | None = None) -> dict[str, Any]:
    monthly = summarize_monthly(_read_csv(monthly_path))
    sample = summarize_sample(_read_csv(sample_path)) if sample_path is not None else summarize_sample([])
    advance_to_e4 = (
        monthly["commercial_500_call_gate"]
        and monthly["totals"].get("unresolved", 0) > 0
        and monthly["central_integration_plausible"]
        and sample["candidate_cases"] > 0
        and sample["decision_fact_sufficiency_rate_pct"] not in (None, 0)
        and sample["material_effect_confirmed_candidate_count"] > 0
        and sample["safety_material_disagreements"] == 0
    )
    return {
        "report": "ProjectPermit_operator_rescue_metrics",
        "report_version": 1,
        "evidence_boundary": (
            "Mechanical research screen only. Aggregate values do not become E2/E3/E4/E5 unless "
            "the repository evidence standard's provenance, representativeness, external-use and "
            "commitment requirements are independently satisfied."
        ),
        "monthly": monthly,
        "sample": sample,
        "advance_to_e4_mechanical_screen": advance_to_e4,
        "renew_engineering": False,
    }


def decision_row(summary: dict[str, Any]) -> dict[str, Any]:
    monthly, sample = summary["monthly"], summary["sample"]
    totals = monthly["totals"]
    fact_counts = sample["fact_sufficiency_counts"]
    return {
        "operator": monthly["operator"],
        "complete_month": monthly["complete_month"],
        "evidence_level": "E0",
        "unique_current_family_requests": totals.get("unique_requests", 0),
        "candidate_calls_month": totals.get("candidate_preflight_requests", 0),
        "unresolved_count": totals.get("unresolved", 0),
        "unresolved_share_pct": monthly["unresolved_share_of_candidate_pct"],
        "sampled_cases": sample["sampled_cases"],
        "direct_structured_count": fact_counts.get("DIRECT_STRUCTURED", 0),
        "text_derivable_count": fact_counts.get("TEXT_DERIVABLE", 0),
        "followup_required_count": fact_counts.get("FOLLOWUP_REQUIRED", 0),
        "external_property_lookup_required_count": fact_counts.get("EXTERNAL_PROPERTY_LOOKUP_REQUIRED", 0),
        "insufficient_current_rules_count": fact_counts.get("INSUFFICIENT_FOR_CURRENT_RULES", 0),
        "decision_fact_sufficiency_rate_pct": sample["decision_fact_sufficiency_rate_pct"],
        "material_effect_confirmed_count": sample["material_effect_confirmed_candidate_count"],
        "material_hit_rate_pct": sample["material_hit_rate_pct"],
        "integration_topology": ";".join(monthly["integration_topologies"]),
        "shadow_external_calls": "",
        "accepted_price_or_license": "",
        "operator_resources_committed": "",
        "build_vs_buy_preference": "",
        "safety_material_disagreements": sample["safety_material_disagreements"],
        "commercial_500_call_gate": "YES" if monthly["commercial_500_call_gate"] else "NO",
        "advance_to_e4": "YES" if summary["advance_to_e4_mechanical_screen"] else "NO",
        "renew_engineering": "NO",
        "decision_notes": "Mechanical screen only; evidence level and engineering decision require human evidence review.",
    }


def _write_decision_csv(path: Path, row: dict[str, Any]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("monthly_csv", help="Complete-month operator aggregate CSV")
    parser.add_argument("--sample", help="Optional chronological operator sample CSV")
    parser.add_argument("--json-output", help="Optional JSON summary output path")
    parser.add_argument("--decision-csv", help="Optional one-row decision summary CSV output path")
    args = parser.parse_args()

    summary = build_summary(Path(args.monthly_csv), Path(args.sample) if args.sample else None)
    rendered = json.dumps(summary, indent=2, sort_keys=True)
    if args.json_output:
        Path(args.json_output).write_text(rendered + "\n", encoding="utf-8")
    if args.decision_csv:
        _write_decision_csv(Path(args.decision_csv), decision_row(summary))
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
