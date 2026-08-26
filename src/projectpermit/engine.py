"""ProjectPermit Phase 0 deterministic rules engine.

This prototype intentionally does not call an LLM. The client/agent is expected to
normalize natural-language project scope into structured facts. The engine then
applies jurisdiction rules and returns evidence-linked preflight results.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any, Dict, List

RULESET_VERSION = "2026-08-26.1"
SOURCE_VERIFIED_AT = "2026-08-26"

STATUS_RANK = {
    "OUT_OF_SCOPE": 0,
    "LIKELY_NOT_REQUIRED": 1,
    "MUNICIPAL_CONFIRMATION_REQUIRED": 2,
    "ADDITIONAL_REVIEW_REQUIRED": 3,
    "LIKELY_REQUIRED": 4,
    "REQUIRED": 5,
}

SOURCES: Dict[str, Dict[str, str]] = {
    "GAT_GENERAL": {
        "authority": "Ville de Gatineau",
        "title": "Ai-je besoin d'un permis de construire ou d'un certificat d'autorisation?",
        "url": "https://www.gatineau.ca/portail/default.aspx?c=fr-CA&p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fai_je_besoin_permis_construire_ou_certificat_autorisation",
    },
    "GAT_FAQ": {
        "authority": "Ville de Gatineau",
        "title": "Foire aux questions (FAQ) - permis et urbanisme",
        "url": "https://www.gatineau.ca/portail/default.aspx?c=fr-CA&p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fdemande_information%2Ffaq",
    },
    "GAT_PRINCIPAL": {
        "authority": "Ville de Gatineau",
        "title": "Bâtiment principal à usage résidentiel",
        "url": "https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fpermis_construire%2Fconstruction_batiment_principal",
    },
    "GAT_ACCESSORY": {
        "authority": "Ville de Gatineau",
        "title": "Bâtiments accessoires détachés de l'habitation",
        "url": "https://www.gatineau.ca/portail/default.aspx?c=fr-CA&p=guichet_municipal%2Freglements_municipaux%2Fbatiments_accessoires_detaches_habitation",
    },
    "GAT_GIS": {
        "authority": "Ville de Gatineau",
        "title": "Carte interactive (Géoportail urbanisme)",
        "url": "https://www.gatineau.ca/portail/default.aspx?p=publications_cartes_statistiques_donnees_ouvertes%2Fcartes%2Fcarte_interactive_geoportail_urbanisme",
    },
    "GAT_ZONING_DATA": {
        "authority": "Ville de Gatineau",
        "title": "Zonage normé v1 (CC BY 4.0)",
        "url": "https://www.gatineau.ca/portail/default.aspx?id=1022937247&p=publications_cartes_statistiques_donnees_ouvertes%2Fdonnees_ouvertes%2Fjeux_donnees%2Fdetails",
    },
    "OTT_GENERAL": {
        "authority": "City of Ottawa",
        "title": "Building permit projects",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/building-permit-projects",
    },
    "OTT_EXEMPT": {
        "authority": "City of Ottawa",
        "title": "Projects not requiring Building Permits",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits",
    },
    "OTT_DECK": {
        "authority": "City of Ottawa",
        "title": "Decks - Do I need a building permit?",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/decks",
    },
    "OTT_ACCESSORY": {
        "authority": "City of Ottawa",
        "title": "Permit exemptions for residential accessory structures (2025 A-001)",
        "url": "https://documents.ottawa.ca/sites/default/files/permit_except_acc_structure_advisory_en.pdf",
    },
    "OTT_ADDITION": {
        "authority": "City of Ottawa",
        "title": "Addition - Do I need a building permit?",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/addition",
    },
    "OTT_ADU": {
        "authority": "City of Ottawa",
        "title": "Adding an apartment (additional dwelling units)",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/adding-apartment-additional-dwelling-units",
    },
    "OTT_BASEMENT": {
        "authority": "City of Ottawa",
        "title": "Finishing a basement",
        "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/finishing-basement",
    },
    "OTT_ZONING_2026": {
        "authority": "City of Ottawa",
        "title": "Zoning By-law (By-law No. 2026-50)",
        "url": "https://ottawa.ca/en/living-ottawa/laws-licences-and-permits/laws/laws-z/zoning-law-law-no-2026-50",
    },
    "OTT_ZONING_APPEALS": {
        "authority": "City of Ottawa",
        "title": "Update on status of appeals of new Zoning By-law (July 7, 2026)",
        "url": "https://ottawa.ca/en/node/3046321",
    },
    "OTT_GIS_2026": {
        "authority": "City of Ottawa",
        "title": "Zoning_Bylaw_2026_50 MapServer",
        "url": "https://maps.ottawa.ca/arcgis/rest/services/Zoning_Bylaw_2026_50/MapServer",
    },
    "OTT_GIS_2008": {
        "authority": "City of Ottawa",
        "title": "Zoning_Bylaw_2008_250 MapServer",
        "url": "https://maps.ottawa.ca/arcgis/rest/services/Zoning_Bylaw_2008_250/MapServer",
    },
}


def _req(req_type: str, status: str, reason: str, source_ids: List[str], rule_id: str) -> Dict[str, Any]:
    return {
        "type": req_type,
        "status": status,
        "reason": reason,
        "rule_id": rule_id,
        "rule_version": RULESET_VERSION,
        "source_verified_at": SOURCE_VERIFIED_AT,
        "evidence": [dict(SOURCES[s], source_id=s) for s in source_ids],
    }


def _overall(requirements: List[Dict[str, Any]]) -> str:
    if not requirements:
        return "MUNICIPAL_CONFIRMATION_REQUIRED"
    return max((r["status"] for r in requirements), key=lambda s: STATUS_RANK[s])


def _overlay_review_gatineau(facts: Dict[str, Any], requirements: List[Dict[str, Any]]) -> None:
    prop = facts.get("property", {})
    if prop.get("piia") is True or prop.get("heritage") is True:
        requirements.append(_req(
            "planning_or_heritage_review",
            "ADDITIONAL_REVIEW_REQUIRED",
            "Gatineau's permit exemptions do not apply automatically to work subject to a PIIA or a heritage citation regulation.",
            ["GAT_GENERAL", "GAT_GIS"],
            "GAT-OVERLAY-001",
        ))


def _evaluate_gatineau(facts: Dict[str, Any]) -> Dict[str, Any]:
    p = facts.get("project", {})
    prop = facts.get("property", {})
    family = p.get("family")
    action = p.get("action")
    cost = p.get("estimated_cost_cad")
    requirements: List[Dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Construction/expansion or an increase in existing floor area requires a building permit.", ["GAT_GENERAL"], "GAT-BLD-001"))
    if p.get("foundation_work") is True or p.get("structural_change") is True or p.get("modifies_walls") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Work affecting the foundation, structure, or interior walls requires a permit regardless of project cost.", ["GAT_GENERAL"], "GAT-BLD-002"))
    if p.get("new_opening") is True or p.get("closes_opening") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Adding or closing an opening is listed as work requiring a permit regardless of project cost.", ["GAT_GENERAL", "GAT_PRINCIPAL"], "GAT-BLD-003"))
    if p.get("fire_safety_system_change") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Changes to fire separations or fire-protection/detection systems are always-permit triggers.", ["GAT_GENERAL"], "GAT-BLD-004"))
    if p.get("exterior_wall_cladding_change") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Replacement or modification of exterior wall cladding is listed as requiring a permit.", ["GAT_GENERAL"], "GAT-BLD-005"))
    if p.get("roof_replacement") is True and p.get("roof_slope_percent") is not None and p.get("roof_slope_percent") < 17:
        requirements.append(_req("building_permit", "REQUIRED", "Replacement of a flat/low-slope roof covering below 17% slope requires a permit.", ["GAT_GENERAL"], "GAT-BLD-006"))
    if p.get("dwelling_unit_change") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Adding or removing a dwelling in a family-type residence is listed among work requiring a permit.", ["GAT_FAQ"], "GAT-DWELL-001"))

    if family == "accessory_structure":
        if p.get("accessory_permanent") is True:
            requirements.append(_req("building_permit", "REQUIRED", "A permanent detached residential accessory building/construction requires a building permit.", ["GAT_ACCESSORY", "GAT_GENERAL"], "GAT-ACC-001"))
        elif p.get("accessory_permanent") is False:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "A detached movable accessory building/construction does not require a permit, but zoning standards still apply.", ["GAT_ACCESSORY"], "GAT-ACC-002"))
        else:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "Whether the accessory structure is permanent or movable is required to determine the permit path.", ["GAT_ACCESSORY"], "GAT-ACC-003"))

    if family == "deck_porch" and not requirements:
        if prop.get("piia") is True or prop.get("heritage") is True:
            requirements.append(_req("planning_or_heritage_review", "ADDITIONAL_REVIEW_REQUIRED", "Porches, balconies, galleries, terraces, exterior stairs, ramps, awnings and canopies are permit-exempt only when not subject to PIIA/heritage approval.", ["GAT_GENERAL"], "GAT-DECK-002"))
        else:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "The City's summary lists these residential exterior structures as not requiring a permit when not subject to PIIA or heritage citation approval; zoning standards still apply.", ["GAT_GENERAL"], "GAT-DECK-001"))

    if not requirements and family in {"window_door", "interior_renovation", "basement", "kitchen_bath_plumbing"}:
        if action == "enlarge_existing_opening" and not (p.get("structural_change") or p.get("modifies_walls")):
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "The official summary clearly covers adding/removing openings but does not expressly resolve an enlargement when structural/wall impact is not specified.", ["GAT_GENERAL", "GAT_PRINCIPAL"], "GAT-WIN-AMB-001"))
        elif cost is None:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "Gatineau's general exemption for existing-building renovation depends on total labour and materials cost, so an estimated cost is required.", ["GAT_GENERAL"], "GAT-COST-000"))
        elif cost < 26000:
            if family == "window_door" and action not in {"replace_same_size", "repair"}:
                requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "This window/door action is not within the clearly stated same-opening replacement exemption and lacks an always-required trigger in the supplied facts.", ["GAT_GENERAL"], "GAT-COST-004"))
            elif prop.get("piia") is True or prop.get("heritage") is True:
                requirements.append(_req("planning_or_heritage_review", "ADDITIONAL_REVIEW_REQUIRED", "The under-$26,000 exemption is conditional on the work not being subject to PIIA or heritage citation approval.", ["GAT_GENERAL", "GAT_GIS"], "GAT-COST-003"))
            else:
                requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "For an existing principal building, listed non-structural renovation categories under $26,000 before tax are permit-exempt, subject to PIIA/heritage exceptions and other applicable standards.", ["GAT_GENERAL"], "GAT-COST-001"))
        elif cost > 26000:
            requirements.append(_req("building_permit", "REQUIRED", "Repair/renovation over $26,000 on an existing principal building is listed as requiring a permit.", ["GAT_GENERAL"], "GAT-COST-002"))
        else:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "The City's public summary states 'less than $26,000' for the exemption and 'more than $26,000' for required renovation; the exact $26,000 boundary should be confirmed with the municipality.", ["GAT_GENERAL"], "GAT-COST-26000"))

    if not requirements:
        requirements.append(_req("building_permit", "OUT_OF_SCOPE", "This Phase 0 ruleset does not yet contain a deterministic rule for the supplied Gatineau project facts.", ["GAT_GENERAL"], "GAT-FALLBACK-001"))

    if requirements and _overall(requirements) in {"REQUIRED", "LIKELY_REQUIRED"}:
        _overlay_review_gatineau(facts, requirements)

    return {
        "jurisdiction": {"country": "CA", "province": "QC", "municipality": "Gatineau"},
        "determination": _overall(requirements),
        "requirements": requirements,
        "confidence": "HIGH" if _overall(requirements) in {"REQUIRED", "LIKELY_NOT_REQUIRED"} else "MEDIUM",
    }


def _evaluate_ottawa(facts: Dict[str, Any]) -> Dict[str, Any]:
    p = facts.get("project", {})
    prop = facts.get("property", {})
    family = p.get("family")
    action = p.get("action")
    requirements: List[Dict[str, Any]] = []

    if family == "addition" or p.get("floor_area_increase") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Additions such as sunrooms, solariums, attached garages and porches require a building permit.", ["OTT_ADDITION"], "OTT-ADD-001"))
    if p.get("structural_change") is True or p.get("modifies_walls") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Interior/exterior structural alterations, including adding or removing walls, require a building permit.", ["OTT_GENERAL"], "OTT-STR-001"))
    if family == "window_door" and action in {"new_opening", "enlarge_existing_opening", "relocate_opening"}:
        requirements.append(_req("building_permit", "REQUIRED", "New windows and enlarging or relocating a window or door are listed as structural alterations requiring a building permit.", ["OTT_GENERAL"], "OTT-WIN-001"))
    if p.get("dwelling_unit_change") is True:
        requirements.append(_req("building_permit", "REQUIRED", "Adding an additional dwelling unit requires building-permit review, including change-of-use review even where little physical work is proposed.", ["OTT_ADU"], "OTT-ADU-001"))
    if p.get("plumbing_change") is True and p.get("replace_existing_plumbing_fixture_only") is not True:
        requirements.append(_req("building_permit", "REQUIRED", "Alterations, additions or extensions to a plumbing system require a building permit; replacing existing fixtures is the stated exception.", ["OTT_GENERAL"], "OTT-PLUMB-001"))

    if not requirements and family == "window_door" and action == "replace_same_size":
        if prop.get("heritage") is True:
            requirements.append(_req("heritage_review", "ADDITIONAL_REVIEW_REQUIRED", "Designated heritage buildings or properties within a Heritage District Overlay are not subject to the normal permit exemptions and require City review.", ["OTT_EXEMPT"], "OTT-HER-001"))
        else:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "Replacing a door or window in the same-size opening is listed as exempt from a building permit; other applicable law still applies.", ["OTT_EXEMPT"], "OTT-WIN-002"))

    if not requirements and family in {"interior_renovation", "kitchen_bath_plumbing"}:
        if p.get("replace_existing_plumbing_fixture_only") is True:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "Replacing existing plumbing fixtures without altering/extending the plumbing system falls within the stated plumbing exception.", ["OTT_GENERAL", "OTT_EXEMPT"], "OTT-PLUMB-002"))
        elif action in {"replace_cabinets_same_plumbing", "flooring", "painting"}:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "The City lists same-location cabinet replacement, flooring, painting and decorating among projects exempt from a building permit.", ["OTT_EXEMPT"], "OTT-INT-001"))

    if not requirements and family == "basement":
        if action == "finish_basement":
            requirements.append(_req("building_permit", "LIKELY_REQUIRED", "Ottawa treats finishing a basement as a building-permit project; the exact need depends on whether the work constitutes a material alteration/repair and on the submitted scope.", ["OTT_BASEMENT", "OTT_GENERAL"], "OTT-BASE-001"))
        elif action in {"flooring", "painting"}:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "Flooring, painting and decorating are listed as permit-exempt projects.", ["OTT_EXEMPT"], "OTT-BASE-002"))

    if not requirements and family == "deck_porch":
        h = p.get("deck_height_mm")
        area = p.get("deck_area_m2")
        attached = p.get("deck_attached")
        principal = p.get("principal_access") is True
        if h is None or area is None or attached is None:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "Deck height, area, and whether it is attached/adjacent to the house are required for Ottawa's permit thresholds.", ["OTT_DECK"], "OTT-DECK-000"))
        elif principal and h > 0:
            requirements.append(_req("building_permit", "REQUIRED", "An elevated deck providing principal access to a building requires a permit regardless of walking surface area.", ["OTT_DECK"], "OTT-DECK-001"))
        elif attached and h > 600:
            requirements.append(_req("building_permit", "REQUIRED", "A deck adjacent to or attached to the house with walking surface more than 600 mm above grade requires a permit regardless of area.", ["OTT_DECK"], "OTT-DECK-002"))
        elif (not attached) and area > 10 and h > 600:
            requirements.append(_req("building_permit", "REQUIRED", "An independent deck over 10 m² and more than 600 mm above grade requires a permit.", ["OTT_DECK"], "OTT-DECK-003"))
        elif h <= 600 and not principal:
            requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "A low deck below the permit height threshold is generally exempt, except where it provides the main entrance; zoning and other law still apply.", ["OTT_DECK", "OTT_EXEMPT"], "OTT-DECK-004"))
        else:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "The supplied deck facts do not fit a Phase 0 explicit Ottawa threshold rule; municipal confirmation is recommended.", ["OTT_DECK"], "OTT-DECK-005"))

    if not requirements and family == "accessory_structure":
        area = p.get("accessory_area_m2")
        if area is None:
            requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "Gross area is required to apply Ottawa's small residential accessory-structure permit exemption.", ["OTT_ACCESSORY"], "OTT-ACC-000"))
        else:
            qualifies = (
                area <= 15
                and p.get("accessory_detached") is True
                and (p.get("accessory_storeys") or 1) <= 1
                and p.get("accessory_plumbing") is False
                and p.get("accessory_heated") is False
                and p.get("accessory_personal_ancillary_use") is True
                and p.get("accessory_structure_kind") in {"shed", "gazebo", "pergola", "similar"}
            )
            if qualifies:
                requirements.append(_req("building_permit", "LIKELY_NOT_REQUIRED", "Ottawa Building Code Services extends the small-structure exemption to qualifying low-rise residential sheds, gazebos, pergolas and similar independent structures up to 15 m², with no plumbing or heating and personal ancillary use only; zoning still applies.", ["OTT_ACCESSORY"], "OTT-ACC-001"))
            elif area > 15:
                requirements.append(_req("building_permit", "REQUIRED", "The Ottawa small residential accessory-structure exemption is limited to structures not more than 15 m²; this project exceeds that threshold.", ["OTT_ACCESSORY"], "OTT-ACC-002"))
            elif area > 10:
                requirements.append(_req("building_permit", "LIKELY_REQUIRED", "The structure is between 10 m² and 15 m² but fails at least one restriction of Ottawa's expanded accessory-structure exemption; permit review is likely required.", ["OTT_ACCESSORY"], "OTT-ACC-003"))
            else:
                requirements.append(_req("building_permit", "MUNICIPAL_CONFIRMATION_REQUIRED", "The structure is small but fails one or more conditions of Ottawa's advisory exemption; the advisory reserves case-by-case assessment.", ["OTT_ACCESSORY"], "OTT-ACC-004"))

    if not requirements:
        requirements.append(_req("building_permit", "OUT_OF_SCOPE", "This Phase 0 ruleset does not yet contain a deterministic rule for the supplied Ottawa project facts.", ["OTT_GENERAL"], "OTT-FALLBACK-001"))

    if prop.get("heritage") is True and _overall(requirements) in {"LIKELY_NOT_REQUIRED", "MUNICIPAL_CONFIRMATION_REQUIRED"}:
        requirements.append(_req("heritage_review", "ADDITIONAL_REVIEW_REQUIRED", "Designated heritage buildings / Heritage District Overlay properties are not subject to normal permit exemptions and require City review.", ["OTT_EXEMPT"], "OTT-HER-002"))

    app_date = facts.get("context", {}).get("permit_application_complete_date")
    if app_date:
        try:
            d = date.fromisoformat(app_date)
        except ValueError:
            requirements.append(_req("zoning_review", "MUNICIPAL_CONFIRMATION_REQUIRED", "permit_application_complete_date must be ISO YYYY-MM-DD to apply Ottawa zoning-transition rules.", ["OTT_ZONING_2026"], "OTT-ZONE-000"))
        else:
            if d >= date(2026, 3, 11):
                requirements.append(_req("zoning_review", "ADDITIONAL_REVIEW_REQUIRED", "Applications deemed complete on/after March 11, 2026 must be checked against both Zoning By-law 2008-250 and 2026-50, applying the most restrictive provisions; some 2026-50 provisions remain under appeal.", ["OTT_ZONING_2026", "OTT_ZONING_APPEALS", "OTT_GIS_2026", "OTT_GIS_2008"], "OTT-ZONE-2026-TRANSITION"))

    return {
        "jurisdiction": {"country": "CA", "province": "ON", "municipality": "Ottawa"},
        "determination": _overall(requirements),
        "requirements": requirements,
        "confidence": "HIGH" if _overall(requirements) in {"REQUIRED", "LIKELY_NOT_REQUIRED"} else "MEDIUM",
    }


def evaluate_project(facts: Dict[str, Any]) -> Dict[str, Any]:
    jurisdiction = facts.get("jurisdiction")
    if jurisdiction == "gatineau_qc":
        out = _evaluate_gatineau(deepcopy(facts))
    elif jurisdiction == "ottawa_on":
        out = _evaluate_ottawa(deepcopy(facts))
    else:
        return {
            "jurisdiction": {"input": jurisdiction},
            "determination": "OUT_OF_SCOPE",
            "requirements": [],
            "confidence": "HIGH",
            "disclaimer": "Preflight information only; not municipal authorization or legal advice.",
            "engine_version": "phase0-0.1.0",
        }
    out["disclaimer"] = "Preflight information only; not municipal authorization or legal advice. Verify final requirements with the competent authority before work begins."
    out["engine_version"] = "phase0-0.1.0"
    return out
