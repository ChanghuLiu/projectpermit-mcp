"""Measure whether derived property overlays change current permit outcomes.

This synthetic diagnostic toggles heritage/PIIA facts while holding project scope
constant. It intentionally does not perform address lookup. The goal is to measure
current rule-engine sensitivity to address-derived property facts, not adapter
reliability or real-world incidence.

Internal technical/commercial-structure evidence only; not E2/E3/E4/E5.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from projectpermit.jurisdiction_router import evaluate_project

ADAPTER_JURISDICTIONS = (
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "vancouver_bc",
)

CASES = (
    {
        "id": "same_size_window",
        "project": {
            "family": "window_door",
            "action": "replace_same_size",
            "estimated_cost_cad": 5000,
            "structural_change": False,
            "modifies_walls": False,
            "single_dwelling_house": True,
            "new_exit": False,
        },
    },
    {
        "id": "cosmetic_painting",
        "project": {
            "family": "interior_renovation",
            "action": "painting",
            "estimated_cost_cad": 5000,
            "structural_change": False,
            "modifies_walls": False,
            "plumbing_change": False,
        },
    },
    {
        "id": "low_detached_deck",
        "project": {
            "family": "deck_porch",
            "action": "build_deck",
            "deck_height_mm": 500,
            "deck_area_m2": 9,
            "deck_attached": False,
            "principal_access": False,
            "required_exit": False,
        },
    },
    {
        "id": "same_location_fixture_replacement",
        "project": {
            "family": "kitchen_bath_plumbing",
            "action": "fixture_refresh",
            "estimated_cost_cad": 5000,
            "structural_change": False,
            "plumbing_change": False,
            "replace_existing_plumbing_fixture_only": True,
        },
    },
)

BASELINE_PROPERTY = {"heritage": False, "piia": False}
OVERLAY_PROPERTY = {"heritage": True, "piia": True}


def _evaluate(jurisdiction: str, project: dict, property_facts: dict) -> dict:
    return evaluate_project(
        {
            "jurisdiction": jurisdiction,
            "project": deepcopy(project),
            "property": deepcopy(property_facts),
        }
    )


def run() -> dict:
    rows = []
    by_jurisdiction = {
        jurisdiction: {"cases": 0, "determination_flips": 0, "requirement_set_changes": 0}
        for jurisdiction in ADAPTER_JURISDICTIONS
    }

    for case in CASES:
        for jurisdiction in ADAPTER_JURISDICTIONS:
            baseline = _evaluate(jurisdiction, case["project"], BASELINE_PROPERTY)
            overlay = _evaluate(jurisdiction, case["project"], OVERLAY_PROPERTY)
            baseline_rules = sorted(
                requirement.get("rule_id", "") for requirement in baseline.get("requirements", [])
            )
            overlay_rules = sorted(
                requirement.get("rule_id", "") for requirement in overlay.get("requirements", [])
            )
            determination_flip = baseline["determination"] != overlay["determination"]
            requirement_change = baseline_rules != overlay_rules

            stats = by_jurisdiction[jurisdiction]
            stats["cases"] += 1
            if determination_flip:
                stats["determination_flips"] += 1
            if requirement_change:
                stats["requirement_set_changes"] += 1

            rows.append(
                {
                    "case_id": case["id"],
                    "jurisdiction": jurisdiction,
                    "baseline_determination": baseline["determination"],
                    "overlay_determination": overlay["determination"],
                    "determination_flip": determination_flip,
                    "baseline_rule_ids": baseline_rules,
                    "overlay_rule_ids": overlay_rules,
                    "requirement_set_changed": requirement_change,
                }
            )

    total_pairs = len(rows)
    total_flips = sum(row["determination_flip"] for row in rows)
    total_requirement_changes = sum(row["requirement_set_changed"] for row in rows)

    for stats in by_jurisdiction.values():
        stats["determination_flip_rate_pct"] = round(
            stats["determination_flips"] / stats["cases"] * 100, 2
        ) if stats["cases"] else None
        stats["requirement_change_rate_pct"] = round(
            stats["requirement_set_changes"] / stats["cases"] * 100, 2
        ) if stats["cases"] else None

    return {
        "evidence_boundary": (
            "Synthetic property-overlay sensitivity only; not real-world overlay incidence, "
            "not address-adapter accuracy, not E2/E3/E4/E5 and not willingness-to-pay evidence."
        ),
        "adapter_jurisdiction_count": len(ADAPTER_JURISDICTIONS),
        "scope_case_count": len(CASES),
        "jurisdiction_scope_pairs": total_pairs,
        "determination_flip_pairs": total_flips,
        "determination_flip_share_pct": round(total_flips / total_pairs * 100, 2),
        "requirement_set_change_pairs": total_requirement_changes,
        "requirement_set_change_share_pct": round(
            total_requirement_changes / total_pairs * 100, 2
        ),
        "by_jurisdiction": by_jurisdiction,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("property_overlay_flip_matrix.json")
    )
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
