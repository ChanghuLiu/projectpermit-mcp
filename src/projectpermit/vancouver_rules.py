"""Phase 1C Vancouver permit-preflight rules.

Rules are limited to current City of Vancouver guidance and the 2025 Vancouver
Building By-law. Where a common project (for example same-size window replacement)
is not resolved clearly by the public permit tables, ProjectPermit returns municipal
confirmation instead of borrowing an exemption from another municipality.
"""
from __future__ import annotations

from typing import Any

RULE_VERSION = "2026-08-26.1"
SOURCE_VERIFIED_AT = "2026-08-26"
ENGINE_VERSION = "phase1c-0.4.0"

STATUS_RANK = {
    "OUT_OF_SCOPE": 0,
    "LIKELY_NOT_REQUIRED": 1,
    "MUNICIPAL_CONFIRMATION_REQUIRED": 2,
    "ADDITIONAL_REVIEW_REQUIRED": 3,
    "LIKELY_REQUIRED": 4,
    "REQUIRED": 5,
}

SOURCES: dict[str, dict[str, str]] = {
    "VAN_WHEN": {
        "authority": "City of Vancouver",
        "title": "When you need a permit",
        "url": "https://vancouver.ca/home-property-development/when-you-need-a-permit.aspx",
    },
    "VAN_RENO": {
        "authority": "City of Vancouver",
        "title": "Renovate a home",
        "url": "https://vancouver.ca/home-property-development/renovate-home.aspx",
    },
    "VAN_SUITE": {
        "authority": "City of Vancouver",
        "title": "Create or legalize a secondary suite",
        "url": "https://vancouver.ca/home-property-development/creating-a-secondary-suite.aspx",
    },
    "VAN_VBBL_2025": {
        "authority": "City of Vancouver",
        "title": "Vancouver Building By-law 2025 - Book I - Volume 1",
        "url": "https://vancouver.ca/files/cov/vbbl-2025-volume-1-v2-01.pdf",
    },
}


def _req(req_type: str, status: str, reason: str, source_ids: list[str], rule_id: str) -> dict[str, Any]:
    return {
        "type": req_type,
        "status": status,
        "reason": reason,
        "rule_id": rule_id,
        "rule_version": RULE_VERSION,
        "source_verified_at": SOURCE_VERIFIED_AT,
        "evidence": [dict(SOURCES[source_id], source_id=source_id) for source_id in source_ids],
    }


def _overall(requirements: list[dict[str, Any]]) -> str:
    if not requirements:
        return "MUNICIPAL_CONFIRMATION_REQUIRED"
    return max((item["status"] for item in requirements), key=lambda status: STATUS_RANK[status])


def _result(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    determination = _overall(requirements)
    return {
        "jurisdiction": {"country": "CA", "province": "BC", "municipality": "Vancouver"},
        "determination": determination,
        "requirements": requirements,
        "confidence": "HIGH" if determination in {"REQUIRED", "LIKELY_NOT_REQUIRED"} else "MEDIUM",
        "disclaimer": (
            "Preflight information only; not municipal authorization or legal advice. "
            "Verify final requirements with the competent authority before work begins."
        ),
        "engine_version": ENGINE_VERSION,
    }


def evaluate_vancouver(facts: dict[str, Any]) -> dict[str, Any]:
    p = facts.get("project", {})
    family = p.get("family")
    action = p.get("action")
    requirements: list[dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Vancouver requires a permit for new construction and renovations that create new area; home additions are also listed as permit-required renovations.",
            ["VAN_WHEN", "VAN_RENO"], "VAN-ADD-001",
        ))

    if p.get("structural_change") is True or p.get("structural_repair") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Structural repairs or structural changes require a building permit in Vancouver.",
            ["VAN_WHEN", "VAN_RENO"], "VAN-STR-001",
        ))

    if p.get("modifies_walls") is True or p.get("moves_interior_walls") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Moving interior walls or partitions is listed as permit-required renovation work.",
            ["VAN_WHEN", "VAN_RENO"], "VAN-WALL-001",
        ))

    if p.get("plumbing_change") is True and p.get("replace_existing_plumbing_fixture_only") is not True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Moving existing or installing new plumbing lines is listed as permit-required renovation work; separate trade permits may also apply.",
            ["VAN_WHEN", "VAN_RENO"], "VAN-PLUMB-001",
        ))

    if p.get("dwelling_unit_change") is True or family == "dwelling_change" or action in {"add_secondary_suite", "legalize_secondary_suite"}:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Creating or legalizing a secondary suite requires a Development and Building Permit in Vancouver.",
            ["VAN_SUITE", "VAN_WHEN"], "VAN-SUITE-BLD-001",
        ))
        requirements.append(_req(
            "development_permit", "REQUIRED",
            "Vancouver's secondary-suite process requires development approval together with the building permit before upgrading work and formal use change.",
            ["VAN_SUITE"], "VAN-SUITE-DEV-001",
        ))

    if not requirements and family == "window_door":
        if action in {"new_opening", "enlarge_existing_opening", "relocate_opening"} or p.get("structural_change") is True:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "A new, enlarged or relocated opening normally involves structural/material alteration; Vancouver requires permits for structural changes.",
                ["VAN_RENO"], "VAN-WIN-001",
            ))
        elif action == "replace_same_size":
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "The current City permit summary does not expressly list same-size window/door replacement among its general no-permit examples. ProjectPermit does not infer an exemption from another city.",
                ["VAN_WHEN", "VAN_RENO"], "VAN-WIN-000",
            ))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing"}:
        if p.get("replace_existing_plumbing_fixture_only") is True:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Replacing fixtures without moving or installing service lines is within Vancouver's published small-project no-permit examples; trade-specific requirements should still be checked.",
                ["VAN_WHEN", "VAN_RENO"], "VAN-PLUMB-002",
            ))
        elif action in {"replace_cabinets_same_plumbing", "cabinetry", "flooring", "painting", "paint"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Vancouver lists replacing fixtures, cabinets or flooring and interior painting among projects that do not require a building permit.",
                ["VAN_WHEN", "VAN_RENO"], "VAN-INT-001",
            ))

    if not requirements and family == "basement":
        if action == "finish_basement":
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Vancouver's renovation table lists creating new spaces, including basements, as requiring permits. A secondary suite or new service work can add further approvals.",
                ["VAN_RENO"], "VAN-BASE-001",
            ))
        elif action in {"painting", "flooring"} and p.get("structural_change") is False:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Painting and flooring are listed as no-permit work when no separate structural or service-line trigger applies.",
                ["VAN_WHEN", "VAN_RENO"], "VAN-BASE-002",
            ))

    if not requirements and family == "deck_porch":
        height = p.get("deck_height_mm")
        area = p.get("deck_area_m2")
        outdoor_patio = action == "outdoor_patio" or p.get("outdoor_patio") is True
        connected = p.get("deck_attached") is True or p.get("connected_to_building") is True
        if outdoor_patio and height is not None and area is not None and float(height) <= 600 and float(area) <= 25 and not connected:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "The 2025 Vancouver Building By-law provides a specific building-permit exception for an outdoor patio not over 25 m² with a deck not over 0.6 m high, subject to the by-law's conditions for any lightweight demountable elements.",
                ["VAN_VBBL_2025"], "VAN-PATIO-002",
            ))
        else:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Vancouver's public permit guidance lists building or altering a deck as work that generally requires a permit; the narrow outdoor-patio exception applies only when all stated conditions are met.",
                ["VAN_WHEN", "VAN_VBBL_2025"], "VAN-DECK-001",
            ))

    if not requirements and family == "accessory_structure":
        kind = p.get("accessory_structure_kind")
        if kind in {"shed", "garage"}:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Vancouver's current permit summary lists building or altering a garage or shed as permit-required work.",
                ["VAN_WHEN"], "VAN-ACC-001",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "The supplied accessory-structure type is not resolved by this Phase 1C rule subset; Vancouver's project-specific zoning/building requirements should be confirmed.",
                ["VAN_WHEN"], "VAN-ACC-000",
            ))

    if not requirements and p.get("roof_replacement") is True:
        requirements.append(_req(
            "building_permit", "LIKELY_NOT_REQUIRED",
            "Installing roofing, gutters or drain-pipes is listed among Vancouver projects that do not require a building permit, provided no separate structural scope is present.",
            ["VAN_WHEN"], "VAN-ROOF-001",
        ))

    if not requirements:
        requirements.append(_req(
            "building_permit", "OUT_OF_SCOPE",
            "The Phase 1C Vancouver ruleset does not yet contain a deterministic rule for the supplied project facts.",
            ["VAN_WHEN"], "VAN-FALLBACK-001",
        ))

    return _result(requirements)


def evaluate_vancouver_project(facts: dict[str, Any]) -> dict[str, Any] | None:
    if facts.get("jurisdiction") == "vancouver_bc":
        return evaluate_vancouver(facts)
    return None
