"""Audit that unresolved parcel overlays never masquerade as resolved exemptions.

This is a synthetic correctness invariant, not real-world market evidence.  For each
known overlay-sensitive rule shape we compare three states while holding project
scope constant:

- overlay explicitly absent (False)
- overlay unknown (None)
- overlay explicitly present (True)

If the resolved False and True states produce different permit determinations, the
unknown state must not remain ``LIKELY_NOT_REQUIRED``.  That would create a false-
negative path for postal-code / municipality-only preflights.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from projectpermit import evaluate_project

CASES = (
    {
        "case_id": "gatineau_low_cost_interior",
        "jurisdiction": "gatineau_qc",
        "project": {
            "family": "interior_renovation",
            "estimated_cost_cad": 10000,
            "structural_change": False,
            "modifies_walls": False,
        },
        "resolved_false": {"piia": False, "heritage": False},
        "unknown": {"piia": None, "heritage": None},
        "resolved_true": {"piia": True, "heritage": True},
    },
    {
        "case_id": "gatineau_deck",
        "jurisdiction": "gatineau_qc",
        "project": {"family": "deck_porch"},
        "resolved_false": {"piia": False, "heritage": False},
        "unknown": {"piia": None, "heritage": None},
        "resolved_true": {"piia": True, "heritage": True},
    },
    {
        "case_id": "ottawa_low_deck",
        "jurisdiction": "ottawa_on",
        "project": {
            "family": "deck_porch",
            "deck_height_mm": 500,
            "deck_area_m2": 9,
            "deck_attached": False,
            "principal_access": False,
        },
        "resolved_false": {"heritage": False},
        "unknown": {"heritage": None},
        "resolved_true": {"heritage": True},
    },
    {
        "case_id": "laval_small_shed",
        "jurisdiction": "laval_qc",
        "project": {
            "family": "accessory_structure",
            "accessory_structure_kind": "shed",
            "accessory_area_m2": 10,
        },
        "resolved_false": {"piia": False},
        "unknown": {"piia": None},
        "resolved_true": {"piia": True},
    },
    {
        "case_id": "laval_rear_deck",
        "jurisdiction": "laval_qc",
        "project": {"family": "deck_porch", "yard": "rear"},
        "resolved_false": {"piia": False},
        "unknown": {"piia": None},
        "resolved_true": {"piia": True},
    },
)


def _run_case(case: dict) -> dict:
    def evaluate(property_facts: dict) -> dict:
        return evaluate_project(
            {
                "jurisdiction": case["jurisdiction"],
                "project": case["project"],
                "property": property_facts,
            }
        )

    resolved_false = evaluate(case["resolved_false"])
    unknown = evaluate(case["unknown"])
    resolved_true = evaluate(case["resolved_true"])

    false_det = resolved_false["determination"]
    unknown_det = unknown["determination"]
    true_det = resolved_true["determination"]
    overlay_changes_result = false_det != true_det
    unsafe_unknown_exemption = (
        overlay_changes_result
        and false_det == "LIKELY_NOT_REQUIRED"
        and unknown_det == "LIKELY_NOT_REQUIRED"
    )

    return {
        "case_id": case["case_id"],
        "jurisdiction": case["jurisdiction"],
        "resolved_false_determination": false_det,
        "unknown_determination": unknown_det,
        "resolved_true_determination": true_det,
        "overlay_changes_result": overlay_changes_result,
        "unsafe_unknown_exemption": unsafe_unknown_exemption,
        "unknown_required_property_facts": unknown.get("required_property_facts", []),
    }


def run() -> dict:
    rows = [_run_case(case) for case in CASES]
    unsafe = [row for row in rows if row["unsafe_unknown_exemption"]]
    return {
        "evidence_boundary": (
            "Synthetic unknown-overlay correctness audit only; not real-world overlay "
            "incidence, address-adapter accuracy, E2/E3/E4/E5 or demand evidence."
        ),
        "case_count": len(rows),
        "unsafe_unknown_exemption_count": len(unsafe),
        "pass": not unsafe,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("property_overlay_unknown_safety_audit.json"),
    )
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
