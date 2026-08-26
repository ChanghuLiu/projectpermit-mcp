"""Phase 1A jurisdiction rules for ProjectPermit.

These rules intentionally cover only statements that can be mapped directly to
current official municipal guidance. Ambiguous boundaries return municipal
confirmation rather than guessing. Natural-language interpretation remains the
client Agent's job.
"""
from __future__ import annotations

from typing import Any

RULE_VERSION = "2026-08-26.1"
SOURCE_VERIFIED_AT = "2026-08-26"
ENGINE_VERSION = "phase1a-0.2.0"

STATUS_RANK = {
    "OUT_OF_SCOPE": 0,
    "LIKELY_NOT_REQUIRED": 1,
    "MUNICIPAL_CONFIRMATION_REQUIRED": 2,
    "ADDITIONAL_REVIEW_REQUIRED": 3,
    "LIKELY_REQUIRED": 4,
    "REQUIRED": 5,
}

SOURCES: dict[str, dict[str, str]] = {
    "TOR_GENERAL": {
        "authority": "City of Toronto",
        "title": "When Do I Need a Building Permit?",
        "url": "https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/",
    },
    "MIS_GENERAL": {
        "authority": "City of Mississauga",
        "title": "When a building permit is required",
        "url": "https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/",
    },
}


def _req(req_type: str, status: str, reason: str, source_id: str, rule_id: str) -> dict[str, Any]:
    return {
        "type": req_type,
        "status": status,
        "reason": reason,
        "rule_id": rule_id,
        "rule_version": RULE_VERSION,
        "source_verified_at": SOURCE_VERIFIED_AT,
        "evidence": [dict(SOURCES[source_id], source_id=source_id)],
    }


def _overall(requirements: list[dict[str, Any]]) -> str:
    if not requirements:
        return "MUNICIPAL_CONFIRMATION_REQUIRED"
    return max((r["status"] for r in requirements), key=lambda s: STATUS_RANK[s])


def _result(municipality: str, requirements: list[dict[str, Any]]) -> dict[str, Any]:
    determination = _overall(requirements)
    return {
        "jurisdiction": {"country": "CA", "province": "ON", "municipality": municipality},
        "determination": determination,
        "requirements": requirements,
        "confidence": "HIGH" if determination in {"REQUIRED", "LIKELY_NOT_REQUIRED"} else "MEDIUM",
        "disclaimer": (
            "Preflight information only; not municipal authorization or legal advice. "
            "Verify final requirements with the competent authority before work begins."
        ),
        "engine_version": ENGINE_VERSION,
    }


def evaluate_toronto(facts: dict[str, Any]) -> dict[str, Any]:
    p = facts.get("project", {})
    family = p.get("family")
    action = p.get("action")
    requirements: list[dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Toronto lists additions to existing buildings, including attached garages, sunrooms, porches and decks, as requiring a building permit.",
            "TOR_GENERAL", "TOR-ADD-001",
        ))

    if p.get("structural_change") is True or p.get("modifies_walls") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Structural or material alterations, including adding or removing walls, require a building permit.",
            "TOR_GENERAL", "TOR-STR-001",
        ))

    if family == "window_door" and action in {"new_opening", "enlarge_existing_opening", "relocate_opening"}:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "New, enlarged or relocated windows or doors are listed as structural/material alterations requiring a building permit.",
            "TOR_GENERAL", "TOR-WIN-001",
        ))

    if p.get("dwelling_unit_change") is True or family == "dwelling_change":
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "A change of use, including changing a single dwelling to a multi-dwelling building, requires a building permit even where no construction is proposed.",
            "TOR_GENERAL", "TOR-DWELL-001",
        ))

    if p.get("plumbing_change") is True and p.get("replace_existing_plumbing_fixture_only") is not True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Installing or modifying plumbing systems is listed as permit-required work.",
            "TOR_GENERAL", "TOR-PLUMB-001",
        ))

    if not requirements and family == "window_door" and action == "replace_same_size":
        house_ok = p.get("single_dwelling_house") is True
        unchanged = p.get("structural_change") is False and p.get("new_exit") is not True
        if house_ok and unchanged:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Toronto exempts same-location, same-size window/door replacement in a detached, semi-detached or row house containing a single dwelling unit when structural support is unaffected and no new exit is created.",
                "TOR_GENERAL", "TOR-WIN-002",
            ))
        elif p.get("single_dwelling_house") is False:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Toronto specifically lists replacement windows/doors in buildings other than qualifying single-dwelling detached, semi-detached or row houses as permit-required work.",
                "TOR_GENERAL", "TOR-WIN-003",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Toronto's same-size replacement exemption depends on building form/use and structural/exit conditions; provide single_dwelling_house and structural facts.",
                "TOR_GENERAL", "TOR-WIN-000",
            ))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing"}:
        if p.get("replace_existing_plumbing_fixture_only") is True:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Repairing or replacing existing plumbing fixtures without altering the plumbing system is listed as permit-exempt.",
                "TOR_GENERAL", "TOR-PLUMB-002",
            ))
        elif action in {"replace_cabinets_same_plumbing", "cabinetry", "millwork"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Installation of cabinetry and millwork is listed as not requiring a building permit.",
                "TOR_GENERAL", "TOR-INT-001",
            ))

    if not requirements and family == "basement":
        if action == "finish_basement":
            explicit_safe = (
                p.get("structural_change") is False
                and p.get("material_alteration") is False
                and p.get("dwelling_unit_change") is False
                and p.get("new_plumbing") is False
            )
            unsafe = any(
                p.get(k) is True
                for k in ("structural_change", "material_alteration", "dwelling_unit_change", "new_plumbing")
            )
            if explicit_safe:
                requirements.append(_req(
                    "building_permit", "LIKELY_NOT_REQUIRED",
                    "Toronto lists finishing a house basement as permit-exempt when there are no structural/material alterations, no additional dwelling unit and no new plumbing.",
                    "TOR_GENERAL", "TOR-BASE-001",
                ))
            elif unsafe:
                requirements.append(_req(
                    "building_permit", "REQUIRED",
                    "Toronto requires a permit for basement finishing when the scope includes structural/material alterations, new plumbing, foundation work, a basement entrance or an additional dwelling unit.",
                    "TOR_GENERAL", "TOR-BASE-002",
                ))
            else:
                requirements.append(_req(
                    "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                    "Basement-finishing permit status depends on structural/material alteration, dwelling-unit and plumbing facts that were not fully supplied.",
                    "TOR_GENERAL", "TOR-BASE-000",
                ))
        elif action == "waterproofing_repair":
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Waterproofing repairs to a basement are listed as not requiring a building permit.",
                "TOR_GENERAL", "TOR-BASE-003",
            ))

    if not requirements and family == "deck_porch":
        height = p.get("deck_height_mm")
        required_exit = p.get("required_exit") is True or p.get("principal_access") is True
        if height is None:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Deck height and whether it forms part of a required exit are needed to apply Toronto's 600 mm threshold.",
                "TOR_GENERAL", "TOR-DECK-000",
            ))
        elif height > 600:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Toronto lists decks more than 60 cm (600 mm) above ground as requiring a building permit.",
                "TOR_GENERAL", "TOR-DECK-001",
            ))
        elif not required_exit:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "An uncovered platform not more than 600 mm above adjacent grade and not forming part of a required exit is listed as permit-exempt; zoning still applies.",
                "TOR_GENERAL", "TOR-DECK-002",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "The low-deck exemption does not safely apply when the platform forms part of a required exit/access path.",
                "TOR_GENERAL", "TOR-DECK-003",
            ))

    if not requirements and family == "accessory_structure":
        kind = p.get("accessory_structure_kind")
        area = p.get("accessory_area_m2")
        attached = p.get("accessory_detached") is False
        plumbing = p.get("accessory_plumbing") is True
        if attached or plumbing:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Toronto states that an accessory structure attached to an existing building or containing plumbing requires a permit regardless of size.",
                "TOR_GENERAL", "TOR-ACC-001",
            ))
        elif area is None:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Accessory-structure gross area is required to apply Toronto's 10 m² general and 15 m² shed thresholds.",
                "TOR_GENERAL", "TOR-ACC-000",
            ))
        elif kind == "shed":
            if area < 15 and (p.get("accessory_storeys") in {None, 1}) and p.get("accessory_storage_only") is True:
                requirements.append(_req(
                    "building_permit", "LIKELY_NOT_REQUIRED",
                    "A qualifying detached one-storey storage-only shed below 15 m² with no plumbing is permit-exempt under Toronto's published guidance.",
                    "TOR_GENERAL", "TOR-ACC-002",
                ))
            elif area > 15:
                requirements.append(_req(
                    "building_permit", "REQUIRED",
                    "Toronto lists sheds above the small-shed exemption threshold as requiring a building permit.",
                    "TOR_GENERAL", "TOR-ACC-003",
                ))
            else:
                requirements.append(_req(
                    "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                    "Toronto's page describes sheds of 15 m² or more as requiring a permit while also describing sheds not more than 15 m² as exempt; the exact 15 m² boundary is conservatively sent for confirmation.",
                    "TOR_GENERAL", "TOR-ACC-015",
                ))
        elif area > 10:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Toronto lists residential accessory structures larger than 10 m², other than the specific shed exemption, as requiring a building permit.",
                "TOR_GENERAL", "TOR-ACC-004",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "The supplied small accessory structure is below Toronto's general 10 m² threshold but is not a fully matched published exemption; zoning and structure-specific rules must be checked.",
                "TOR_GENERAL", "TOR-ACC-005",
            ))

    if not requirements:
        requirements.append(_req(
            "building_permit", "OUT_OF_SCOPE",
            "The Phase 1A Toronto ruleset does not yet contain a deterministic rule for the supplied project facts.",
            "TOR_GENERAL", "TOR-FALLBACK-001",
        ))

    return _result("Toronto", requirements)


def evaluate_mississauga(facts: dict[str, Any]) -> dict[str, Any]:
    p = facts.get("project", {})
    family = p.get("family")
    action = p.get("action")
    requirements: list[dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Mississauga lists additions to existing buildings as permit-required work.",
            "MIS_GENERAL", "MIS-ADD-001",
        ))

    if p.get("structural_change") is True or p.get("modifies_walls") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Interior alterations and structural changes are within Mississauga's listed permit-required work.",
            "MIS_GENERAL", "MIS-STR-001",
        ))

    if family == "window_door" and action in {"new_opening", "enlarge_existing_opening"}:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Mississauga requires a permit for a new window/door or increasing the size of an existing opening.",
            "MIS_GENERAL", "MIS-WIN-001",
        ))

    if p.get("dwelling_unit_change") is True or family == "dwelling_change":
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "A basement apartment/second unit or other change of building use is listed as permit-required work.",
            "MIS_GENERAL", "MIS-DWELL-001",
        ))

    if p.get("plumbing_change") is True and p.get("replace_existing_plumbing_fixture_only") is not True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Adding, removing or relocating plumbing fixtures or installing/replacing/repairing plumbing drainage is listed as permit-required work.",
            "MIS_GENERAL", "MIS-PLUMB-001",
        ))

    if not requirements and family == "window_door" and action == "replace_same_size":
        requirements.append(_req(
            "building_permit", "LIKELY_NOT_REQUIRED",
            "Mississauga lists replacing an existing window or door with the same size as work that does not need a building permit; zoning and other approvals may still apply.",
            "MIS_GENERAL", "MIS-WIN-002",
        ))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing"}:
        if p.get("replace_existing_plumbing_fixture_only") is True:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Replacing a plumbing fixture in the same location is listed as not requiring a building permit.",
                "MIS_GENERAL", "MIS-PLUMB-002",
            ))
        elif action in {"replace_cabinets_same_plumbing", "cabinetry", "painting", "decorations"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Cabinetry/cupboards, painting and decorations are listed as projects that do not need a building permit.",
                "MIS_GENERAL", "MIS-INT-001",
            ))
        elif p.get("recladding") is True:
            if p.get("same_cladding_material") is True:
                requirements.append(_req(
                    "building_permit", "LIKELY_NOT_REQUIRED",
                    "Re-cladding with the same material is listed as not requiring a building permit.",
                    "MIS_GENERAL", "MIS-CLAD-002",
                ))
            else:
                requirements.append(_req(
                    "building_permit", "REQUIRED",
                    "Re-cladding a building with a new material is listed as permit-required work.",
                    "MIS_GENERAL", "MIS-CLAD-001",
                ))

    if not requirements and family == "basement":
        if action == "finish_basement":
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Mississauga explicitly lists finishing a basement to create rooms or living space as requiring a building permit.",
                "MIS_GENERAL", "MIS-BASE-001",
            ))
        elif action == "damp_proof":
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Damp-proofing a basement is listed as work that does not need a building permit.",
                "MIS_GENERAL", "MIS-BASE-002",
            ))

    if not requirements and family == "deck_porch":
        height = p.get("deck_height_mm")
        covered = p.get("covered") is True or action == "covered_porch"
        if covered:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Mississauga lists a covered porch as permit-required work.",
                "MIS_GENERAL", "MIS-DECK-003",
            ))
        elif height is None:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Deck height is required to apply Mississauga's published height thresholds.",
                "MIS_GENERAL", "MIS-DECK-000",
            ))
        elif height > 610:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Mississauga lists decks greater than 0.61 m (610 mm) high as requiring a building permit.",
                "MIS_GENERAL", "MIS-DECK-001",
            ))
        elif height < 600:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Mississauga lists decks less than 600 mm high as not needing a building permit.",
                "MIS_GENERAL", "MIS-DECK-002",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "The City's public page leaves a narrow 600-610 mm gap between its no-permit and permit-required deck thresholds; municipal confirmation is safer.",
                "MIS_GENERAL", "MIS-DECK-610",
            ))

    if not requirements and family == "accessory_structure":
        kind = p.get("accessory_structure_kind")
        area = p.get("accessory_area_m2")
        plumbing = p.get("accessory_plumbing") is True
        if plumbing:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Mississauga requires a permit for a building/structure of any size that contains plumbing.",
                "MIS_GENERAL", "MIS-ACC-001",
            ))
        elif area is None:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Accessory-structure area is required to apply Mississauga's 10 m² general and 15 m² shed thresholds.",
                "MIS_GENERAL", "MIS-ACC-000",
            ))
        elif kind == "shed":
            qualifies = (
                area < 15
                and p.get("accessory_detached") is True
                and (p.get("accessory_storeys") in {None, 1})
                and p.get("accessory_storage_only") is True
            )
            if qualifies:
                requirements.append(_req(
                    "building_permit", "LIKELY_NOT_REQUIRED",
                    "A detached one-storey storage-only shed below 15 m² with no plumbing is listed as permit-exempt.",
                    "MIS_GENERAL", "MIS-ACC-002",
                ))
            elif area > 15:
                requirements.append(_req(
                    "building_permit", "REQUIRED",
                    "Mississauga lists sheds greater than 15 m² as requiring a building permit.",
                    "MIS_GENERAL", "MIS-ACC-003",
                ))
            else:
                requirements.append(_req(
                    "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                    "The public page states greater than 15 m² requires a permit and less than 15 m² can be exempt, leaving exactly 15 m² unresolved in the summary guidance.",
                    "MIS_GENERAL", "MIS-ACC-015",
                ))
        elif kind == "gazebo":
            status = "REQUIRED" if area > 10 else "LIKELY_NOT_REQUIRED"
            reason = (
                "Mississauga lists gazebos greater than 10 m² as permit-required."
                if area > 10
                else "Mississauga lists gazebos 10 m² or less as not requiring a building permit."
            )
            requirements.append(_req("building_permit", status, reason, "MIS_GENERAL", "MIS-GAZ-001" if area > 10 else "MIS-GAZ-002"))
        elif area > 10:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "A building or structure other than a shed greater than 10 m² is listed as permit-required work.",
                "MIS_GENERAL", "MIS-ACC-004",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "This small accessory structure is below the general 10 m² threshold but does not match a named published exemption; structure-specific and zoning rules should be confirmed.",
                "MIS_GENERAL", "MIS-ACC-005",
            ))

    if not requirements:
        requirements.append(_req(
            "building_permit", "OUT_OF_SCOPE",
            "The Phase 1A Mississauga ruleset does not yet contain a deterministic rule for the supplied project facts.",
            "MIS_GENERAL", "MIS-FALLBACK-001",
        ))

    return _result("Mississauga", requirements)


def evaluate_expansion_project(facts: dict[str, Any]) -> dict[str, Any] | None:
    jurisdiction = facts.get("jurisdiction")
    if jurisdiction == "toronto_on":
        return evaluate_toronto(facts)
    if jurisdiction == "mississauga_on":
        return evaluate_mississauga(facts)
    return None
