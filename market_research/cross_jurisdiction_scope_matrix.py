"""Measure how often identical normalized scopes produce different permit outcomes.

This is internal technical/market-structure evidence only. It is not E2/E3/E4/E5.
The fixtures are synthetic and intentionally address-free; property overlays are set
explicitly false so the audit measures municipal rule differences rather than GIS.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from projectpermit.jurisdiction_router import SUPPORTED_JURISDICTIONS, evaluate_project

POSITIVE = {"REQUIRED", "LIKELY_REQUIRED"}
NEGATIVE = {"LIKELY_NOT_REQUIRED"}
REVIEW = {"MUNICIPAL_CONFIRMATION_REQUIRED", "ADDITIONAL_REVIEW_REQUIRED", "OUT_OF_SCOPE"}

BASE_PROPERTY = {"heritage": False, "piia": False}

CASES = [
    {
        "id": "same_size_window_house",
        "project": {
            "family": "window_door",
            "action": "replace_same_size",
            "estimated_cost_cad": 5000,
            "structural_change": False,
            "modifies_walls": False,
            "new_exit": False,
            "single_dwelling_house": True,
        },
    },
    {
        "id": "enlarge_window_structural",
        "project": {
            "family": "window_door",
            "action": "enlarge_existing_opening",
            "estimated_cost_cad": 8000,
            "structural_change": True,
            "modifies_walls": True,
        },
    },
    {
        "id": "cosmetic_interior_painting",
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
        "id": "remove_structural_wall",
        "project": {
            "family": "interior_renovation",
            "action": "remove_wall",
            "estimated_cost_cad": 12000,
            "structural_change": True,
            "modifies_walls": True,
        },
    },
    {
        "id": "clean_basement_finish",
        "project": {
            "family": "basement",
            "action": "finish_basement",
            "estimated_cost_cad": 15000,
            "structural_change": False,
            "material_alteration": False,
            "dwelling_unit_change": False,
            "new_plumbing": False,
            "plumbing_change": False,
        },
    },
    {
        "id": "basement_finish_new_plumbing",
        "project": {
            "family": "basement",
            "action": "finish_basement",
            "estimated_cost_cad": 18000,
            "structural_change": False,
            "material_alteration": False,
            "dwelling_unit_change": False,
            "new_plumbing": True,
            "plumbing_change": True,
            "replace_existing_plumbing_fixture_only": False,
        },
    },
    {
        "id": "add_dwelling_unit",
        "project": {
            "family": "dwelling_change",
            "action": "add_dwelling",
            "dwelling_unit_change": True,
        },
    },
    {
        "id": "low_detached_deck_500mm_9m2",
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
        "id": "attached_deck_700mm_12m2",
        "project": {
            "family": "deck_porch",
            "action": "build_deck",
            "deck_height_mm": 700,
            "deck_area_m2": 12,
            "deck_attached": True,
            "principal_access": False,
            "required_exit": False,
        },
    },
    {
        "id": "detached_storage_shed_9m2",
        "project": {
            "family": "accessory_structure",
            "action": "build_shed",
            "accessory_structure_kind": "shed",
            "accessory_area_m2": 9,
            "accessory_detached": True,
            "accessory_storeys": 1,
            "accessory_plumbing": False,
            "accessory_heated": False,
            "accessory_personal_ancillary_use": True,
            "accessory_storage_only": True,
            "accessory_permanent": True,
        },
    },
    {
        "id": "detached_storage_shed_14m2",
        "project": {
            "family": "accessory_structure",
            "action": "build_shed",
            "accessory_structure_kind": "shed",
            "accessory_area_m2": 14,
            "accessory_detached": True,
            "accessory_storeys": 1,
            "accessory_plumbing": False,
            "accessory_heated": False,
            "accessory_personal_ancillary_use": True,
            "accessory_storage_only": True,
            "accessory_permanent": True,
        },
    },
    {
        "id": "room_addition",
        "project": {
            "family": "addition",
            "action": "build_addition",
            "floor_area_increase": True,
        },
    },
    {
        "id": "replace_existing_plumbing_fixture",
        "project": {
            "family": "kitchen_bath_plumbing",
            "action": "fixture_refresh",
            "estimated_cost_cad": 5000,
            "structural_change": False,
            "plumbing_change": False,
            "replace_existing_plumbing_fixture_only": True,
        },
    },
    {
        "id": "relocate_plumbing_fixture",
        "project": {
            "family": "kitchen_bath_plumbing",
            "action": "move_sink",
            "estimated_cost_cad": 8000,
            "structural_change": False,
            "plumbing_change": True,
            "replace_existing_plumbing_fixture_only": False,
        },
    },
    {
        "id": "replace_cabinets_same_plumbing",
        "project": {
            "family": "kitchen_bath_plumbing",
            "action": "replace_cabinets_same_plumbing",
            "estimated_cost_cad": 10000,
            "structural_change": False,
            "plumbing_change": False,
        },
    },
]


def bucket(status: str) -> str:
    if status in POSITIVE:
        return "permit_positive"
    if status in NEGATIVE:
        return "permit_negative"
    if status in REVIEW:
        return "review_or_out_of_scope"
    return "unknown"


def run() -> dict:
    rows = []
    polarity_divergence = 0
    all_same_bucket = 0
    review_present = 0

    for case in CASES:
        outcomes = {}
        buckets = set()
        for jurisdiction in SUPPORTED_JURISDICTIONS:
            facts = {
                "jurisdiction": jurisdiction,
                "project": deepcopy(case["project"]),
                "property": deepcopy(BASE_PROPERTY),
            }
            result = evaluate_project(facts)
            status = result["determination"]
            outcomes[jurisdiction] = status
            buckets.add(bucket(status))

        has_positive = "permit_positive" in buckets
        has_negative = "permit_negative" in buckets
        polarity = has_positive and has_negative
        if polarity:
            polarity_divergence += 1
        if len(buckets) == 1:
            all_same_bucket += 1
        if "review_or_out_of_scope" in buckets:
            review_present += 1

        rows.append(
            {
                "case_id": case["id"],
                "family": case["project"]["family"],
                "polarity_divergence": polarity,
                "bucket_count": len(buckets),
                "outcomes": outcomes,
            }
        )

    return {
        "evidence_boundary": (
            "Synthetic address-free cross-jurisdiction diagnostic only; not E2/E3/E4/E5 and not a demand estimate. "
            "A polarity divergence means at least one supported city returned permit-positive while another returned permit-negative for identical normalized facts."
        ),
        "case_count": len(CASES),
        "jurisdiction_count": len(SUPPORTED_JURISDICTIONS),
        "polarity_divergence_cases": polarity_divergence,
        "polarity_divergence_share_pct": round(polarity_divergence / len(CASES) * 100, 2),
        "all_same_bucket_cases": all_same_bucket,
        "all_same_bucket_share_pct": round(all_same_bucket / len(CASES) * 100, 2),
        "cases_with_review_or_out_of_scope": review_present,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cross_jurisdiction_scope_matrix.json"),
    )
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
