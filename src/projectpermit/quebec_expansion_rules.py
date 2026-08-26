"""Phase 1B Quebec jurisdiction rules for ProjectPermit.

Only current first-party municipal guidance is promoted to deterministic rules.
Where Longueuil's simplified sheets describe a permit workflow without an explicit
universal exemption table, results stay conservative (`LIKELY_REQUIRED` or
`MUNICIPAL_CONFIRMATION_REQUIRED`) rather than inventing an exemption.
"""
from __future__ import annotations

from typing import Any

RULE_VERSION = "2026-08-26.1"
SOURCE_VERIFIED_AT = "2026-08-26"
ENGINE_VERSION = "phase1b-0.3.0"

STATUS_RANK = {
    "OUT_OF_SCOPE": 0,
    "LIKELY_NOT_REQUIRED": 1,
    "MUNICIPAL_CONFIRMATION_REQUIRED": 2,
    "ADDITIONAL_REVIEW_REQUIRED": 3,
    "LIKELY_REQUIRED": 4,
    "REQUIRED": 5,
}

SOURCES: dict[str, dict[str, str]] = {
    "LAV_EXT": {
        "authority": "Ville de Laval",
        "title": "Rénovation ou réparation résidentielle extérieure",
        "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/renovation-residentielle-exterieure/",
    },
    "LAV_INT": {
        "authority": "Ville de Laval",
        "title": "Rénovation ou réparation résidentielle intérieure",
        "url": "https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx",
    },
    "LAV_SHED": {
        "authority": "Ville de Laval",
        "title": "Remise (cabanon)",
        "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/remise/",
    },
    "LAV_BALCON": {
        "authority": "Ville de Laval",
        "title": "Balcon et galerie",
        "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/balcon-galerie/",
    },
    "LAV_ADD": {
        "authority": "Ville de Laval",
        "title": "Agrandissement d’une habitation de 1 logement (unifamiliale)",
        "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/agrandissement-unifamiliale/",
    },
    "LON_RENO": {
        "authority": "Ville de Longueuil",
        "title": "Rénovation résidentielle intérieure et/ou extérieure — fiche simplifiée (juillet 2025)",
        "url": "https://cms.longueuil.quebec/sites/default/files/medias/documents/2025-07/R%C3%A9novation%20int%C3%A9rieure%20et%20ou%20ext%C3%A9rieure%20r%C3%A9sidentielle%20juillet%202025.pdf",
    },
    "LON_WINDOWS": {
        "authority": "Ville de Longueuil",
        "title": "Ajout, modification ou retrait de porte(s) et/ou fenêtre(s) — fiche simplifiée (juillet 2025)",
        "url": "https://cms.longueuil.quebec/sites/default/files/medias/documents/2025-07/Ajout%2C%20modification%20ou%20retrait%20de%20porte%28s%29%20et_ou%20fen%C3%AAtre%28s%29%20juillet%202025.pdf",
    },
    "LON_PERMITS": {
        "authority": "Ville de Longueuil",
        "title": "Demande de permis en ligne",
        "url": "https://www.longueuil.quebec/fr/services/amenagement-urbanisme/demande-de-permis-en-ligne",
    },
    "LON_URBANISM": {
        "authority": "Ville de Longueuil",
        "title": "Aménagement et urbanisme",
        "url": "https://longueuil.quebec/fr/services/amenagement-urbanisme",
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
        "evidence": [dict(SOURCES[s], source_id=s) for s in source_ids],
    }


def _overall(requirements: list[dict[str, Any]]) -> str:
    if not requirements:
        return "MUNICIPAL_CONFIRMATION_REQUIRED"
    return max((r["status"] for r in requirements), key=lambda status: STATUS_RANK[status])


def _result(municipality: str, requirements: list[dict[str, Any]]) -> dict[str, Any]:
    determination = _overall(requirements)
    return {
        "jurisdiction": {"country": "CA", "province": "QC", "municipality": municipality},
        "determination": determination,
        "requirements": requirements,
        "confidence": "HIGH" if determination in {"REQUIRED", "LIKELY_NOT_REQUIRED"} else "MEDIUM",
        "disclaimer": (
            "Preflight information only; not municipal authorization or legal advice. "
            "Verify final requirements with the competent authority before work begins."
        ),
        "engine_version": ENGINE_VERSION,
    }


def evaluate_laval(facts: dict[str, Any]) -> dict[str, Any]:
    p = facts.get("project", {})
    prop = facts.get("property", {})
    family = p.get("family")
    action = p.get("action")
    requirements: list[dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval states that a permit is mandatory before enlarging a single-family dwelling, including a second storey, attached garage, permanent attached carport, solarium or veranda.",
            ["LAV_ADD"], "LAV-ADD-001",
        ))

    if p.get("structural_change") is True or p.get("modifies_walls") is True or p.get("room_dimensions_change") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval requires a permit for interior work that changes room dimensions, the number of rooms or the structure of the dwelling.",
            ["LAV_INT"], "LAV-STR-001",
        ))

    if p.get("dwelling_unit_change") is True or family == "dwelling_change":
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval lists adding a dwelling unit as permit-required work.",
            ["LAV_INT"], "LAV-DWELL-001",
        ))

    if p.get("new_bedroom") is True:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval lists adding a bedroom as permit-required work.",
            ["LAV_INT"], "LAV-BED-001",
        ))

    if family == "window_door" and action in {"new_opening", "add_opening", "enlarge_existing_opening", "resize_opening"}:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval's exterior-renovation table requires a permit for adding doors/windows or replacing them while changing opening dimensions.",
            ["LAV_EXT"], "LAV-WIN-001",
        ))

    if family == "window_door" and p.get("distance_to_lot_line_m") is not None and float(p["distance_to_lot_line_m"]) < 1.5:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Laval requires a permit when replacing a door or window located less than 1.5 m from the property line.",
            ["LAV_EXT"], "LAV-WIN-LOT-001",
        ))

    if not requirements and family == "window_door" and action == "replace_same_size":
        requirements.append(_req(
            "building_permit", "LIKELY_NOT_REQUIRED",
            "Laval lists replacement of doors/windows while keeping the same dimensions as not requiring a permit, subject to other applicable rules.",
            ["LAV_EXT"], "LAV-WIN-002",
        ))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing"}:
        if action in {"painting", "paint"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Painting is listed by Laval as work not requiring a permit.",
                ["LAV_INT"], "LAV-INT-PAINT-001",
            ))
        elif action in {"renovate_existing_bathroom", "bathroom_renovation"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Renovating an existing bathroom is listed as not requiring a permit.",
                ["LAV_INT"], "LAV-INT-BATH-001",
            ))
        elif action in {"renovate_kitchen", "kitchen_renovation", "replace_cabinets_same_plumbing"}:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Kitchen renovation is listed as not requiring a permit when no separate permit trigger is supplied.",
                ["LAV_INT"], "LAV-INT-KITCHEN-001",
            ))
        elif action in {"add_bathroom", "new_bathroom"}:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Adding a bathroom is listed by Laval as permit-required work.",
                ["LAV_INT"], "LAV-INT-BATH-002",
            ))
        elif p.get("plumbing_change") is True:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Laval's residential interior-renovation table lists replacement or renovation of the plumbing system as not requiring a municipal permit; other code/trade requirements can still apply.",
                ["LAV_INT"], "LAV-PLUMB-001",
            ))

    if not requirements and family == "basement":
        if p.get("room_count_change") is True or p.get("structural_change") is True:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Laval states that basement renovation requires a permit when the number of rooms or the structure is modified.",
                ["LAV_INT"], "LAV-BASE-001",
            ))
        elif action == "finish_basement" and p.get("room_count_change") is False and p.get("structural_change") is False:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Laval's table makes basement-renovation permitting conditional on changing the number of rooms or the structure; with both explicitly unchanged, a building permit is likely not required.",
                ["LAV_INT"], "LAV-BASE-002",
            ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "For basement renovation, Laval's published rule depends on whether room count or structure changes; those facts are not fully supplied.",
                ["LAV_INT"], "LAV-BASE-000",
            ))

    if not requirements and family == "accessory_structure" and p.get("accessory_structure_kind") == "shed":
        area = p.get("accessory_area_m2")
        if area is None:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Laval's shed permit threshold depends on ground footprint; accessory_area_m2 is required.",
                ["LAV_SHED"], "LAV-SHED-000",
            ))
        elif float(area) >= 18:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Laval requires a permit for an accessory structure with a ground footprint of 18 m² or more.",
                ["LAV_SHED"], "LAV-SHED-001",
            ))
        elif prop.get("piia") is True:
            requirements.append(_req(
                "planning_or_design_review", "ADDITIONAL_REVIEW_REQUIRED",
                "A shed below 18 m² is normally permit-exempt, but Laval states that a permit may be required where a PIIA applies.",
                ["LAV_SHED"], "LAV-SHED-PIIA-001",
            ))
        else:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Laval states that a shed below 18 m² does not require a permit, although zoning rules still apply and a PIIA can change the path.",
                ["LAV_SHED"], "LAV-SHED-002",
            ))

    if not requirements and family == "deck_porch":
        yard = p.get("yard")
        if yard in {"front", "side", "secondary_front", "street_facing"}:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Laval requires a permit to repair, modify or build a balcony, stoop, porch or gallery in a front, side or street-facing yard.",
                ["LAV_BALCON"], "LAV-DECK-001",
            ))
        elif yard == "rear":
            if prop.get("piia") is True:
                requirements.append(_req(
                    "planning_or_design_review", "ADDITIONAL_REVIEW_REQUIRED",
                    "Rear-yard balcony/gallery work is generally permit-exempt, but Laval requires additional review where a PIIA applies.",
                    ["LAV_BALCON"], "LAV-DECK-PIIA-001",
                ))
            else:
                requirements.append(_req(
                    "building_permit", "LIKELY_NOT_REQUIRED",
                    "Laval states that rear-yard balcony/gallery maintenance or repair generally does not require a permit; zoning and construction standards still apply.",
                    ["LAV_BALCON"], "LAV-DECK-002",
                ))
        else:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Laval's balcony/gallery permit rule depends on which yard the work occupies; provide project.yard.",
                ["LAV_BALCON"], "LAV-DECK-000",
            ))

    if not requirements and p.get("roof_replacement") is True:
        if p.get("same_roof_material") is True:
            requirements.append(_req(
                "building_permit", "LIKELY_NOT_REQUIRED",
                "Replacing roof covering with the same material is listed as not requiring a permit.",
                ["LAV_EXT"], "LAV-ROOF-002",
            ))
        elif p.get("same_roof_material") is False:
            requirements.append(_req(
                "building_permit", "REQUIRED",
                "Replacing roof covering with a new material is listed as permit-required work.",
                ["LAV_EXT"], "LAV-ROOF-001",
            ))

    if not requirements:
        requirements.append(_req(
            "building_permit", "OUT_OF_SCOPE",
            "The Phase 1B Laval ruleset does not yet contain a deterministic rule for the supplied project facts.",
            ["LAV_INT", "LAV_EXT"], "LAV-FALLBACK-001",
        ))

    return _result("Laval", requirements)


def evaluate_longueuil(facts: dict[str, Any]) -> dict[str, Any]:
    p = facts.get("project", {})
    prop = facts.get("property", {})
    family = p.get("family")
    action = p.get("action")
    requirements: list[dict[str, Any]] = []

    if family == "window_door" and action in {
        "new_opening", "add_opening", "enlarge_existing_opening", "resize_opening",
        "relocate_opening", "remove_opening",
    }:
        requirements.append(_req(
            "building_permit", "REQUIRED",
            "Longueuil's July 2025 simplified sheet defines a permit application specifically for adding, modifying or removing doors/windows and requires plans and supporting documents for that permit.",
            ["LON_WINDOWS"], "LON-WIN-001",
        ))

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req(
            "building_permit", "LIKELY_REQUIRED",
            "Longueuil's current permit portal treats enlargement of a principal building as a construction/renovation permit workflow; final applicability can depend on the borough and project details.",
            ["LON_PERMITS", "LON_URBANISM"], "LON-ADD-001",
        ))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing", "basement"}:
        if action in {"painting", "decorating"} and p.get("structural_change") is False:
            requirements.append(_req(
                "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
                "Longueuil's current simplified renovation sheet describes the permit workflow but does not provide a complete exemption table for purely cosmetic work; municipal confirmation avoids inventing an exemption.",
                ["LON_RENO"], "LON-INT-COSMETIC-000",
            ))
        else:
            requirements.append(_req(
                "building_permit", "LIKELY_REQUIRED",
                "Longueuil publishes a dedicated residential interior/exterior renovation permit workflow requiring architectural plans for affected floors; exact exemptions should be confirmed against the current borough rules.",
                ["LON_RENO", "LON_URBANISM"], "LON-RENO-001",
            ))

    if not requirements and family == "deck_porch":
        requirements.append(_req(
            "building_permit", "LIKELY_REQUIRED",
            "Longueuil lists balcony work among residential permit types that can be processed online; the exact borough/location conditions should be confirmed before work.",
            ["LON_PERMITS"], "LON-DECK-001",
        ))

    if not requirements and family == "accessory_structure":
        requirements.append(_req(
            "building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED",
            "Longueuil's current rules vary by accessory-structure type and borough. This Phase 1B ruleset does not yet claim a universal accessory-structure threshold.",
            ["LON_PERMITS", "LON_URBANISM"], "LON-ACC-000",
        ))

    if prop.get("piia") is True:
        requirements.append(_req(
            "planning_or_design_review", "ADDITIONAL_REVIEW_REQUIRED",
            "Longueuil states that some zones are subject to a PIIA before permits/certificates can be issued; the applicable borough regulation must be checked.",
            ["LON_RENO", "LON_URBANISM"], "LON-PIIA-001",
        ))

    if not requirements:
        requirements.append(_req(
            "building_permit", "OUT_OF_SCOPE",
            "The Phase 1B Longueuil ruleset does not yet contain a deterministic rule for the supplied project facts.",
            ["LON_URBANISM"], "LON-FALLBACK-001",
        ))

    return _result("Longueuil", requirements)


def evaluate_quebec_expansion_project(facts: dict[str, Any]) -> dict[str, Any] | None:
    jurisdiction = facts.get("jurisdiction")
    if jurisdiction == "laval_qc":
        return evaluate_laval(facts)
    if jurisdiction == "longueuil_qc":
        return evaluate_longueuil(facts)
    return None
