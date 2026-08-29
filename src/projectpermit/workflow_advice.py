"""Deterministic workflow guidance for ProjectPermit results.

The permit rules engine decides permit applicability. This module translates that
result into machine-readable workflow hints for contractor/field-service agents:
what to do next, whether an automated workflow may continue, and which missing
facts are worth collecting before another preflight call.

It never changes the permit determination and never claims municipal approval.
"""
from __future__ import annotations

from typing import Any


Question = tuple[str, str, str]

PROPERTY_QUESTIONS: dict[str, Question] = {
    "heritage": (
        "property.heritage",
        "Is the property designated heritage or within a heritage overlay/district?",
        "A heritage constraint can change an otherwise available permit exemption.",
    ),
    "piia": (
        "property.piia",
        "Is the property/project subject to a PIIA/SPAIP-style planning overlay?",
        "A planning overlay can require additional review even when the base work is permit-exempt.",
    ),
    "zoning_code": (
        "property.zoning_code",
        "What municipal zoning code applies to the property?",
        "Some permit and planning paths depend on parcel-specific zoning context.",
    ),
    "zoning_under_appeal": (
        "property.zoning_under_appeal",
        "Is the applicable zoning provision currently under appeal or transition?",
        "A zoning transition can require municipal confirmation before relying on a normal path.",
    ),
}

FAMILY_QUESTIONS: dict[str, list[Question]] = {
    "window_door": [
        (
            "project.action",
            "Is this a same-size replacement, an enlarged opening, a new opening, or a closed opening?",
            "Opening changes are treated differently from like-for-like replacement in several jurisdictions.",
        ),
        (
            "project.structural_change",
            "Will the work alter structural framing or a load-bearing element?",
            "Structural impact is a strong permit trigger across the supported rulesets.",
        ),
    ],
    "interior_renovation": [
        (
            "project.structural_change",
            "Will the renovation alter structural or load-bearing elements?",
            "Structural work can move the project directly onto a permit path.",
        ),
        (
            "project.modifies_walls",
            "Will interior walls be added, removed, relocated, or materially modified?",
            "Wall changes are permit-relevant in multiple supported cities.",
        ),
    ],
    "basement": [
        (
            "project.new_bedroom",
            "Will the basement work create a new bedroom or sleeping room?",
            "A new sleeping room can introduce egress and building-permit requirements.",
        ),
        (
            "project.structural_change",
            "Will the basement work alter structural or load-bearing elements?",
            "Structural changes are a strong permit trigger.",
        ),
        (
            "project.plumbing_change",
            "Will plumbing be added, moved, or materially changed?",
            "Plumbing changes can create a separate permit/review path.",
        ),
    ],
    "dwelling_change": [
        (
            "project.dwelling_unit_change",
            "Will the work add, remove, or reconfigure a dwelling unit?",
            "Dwelling-unit changes commonly require a permit and additional planning review.",
        ),
    ],
    "deck_porch": [
        (
            "project.deck_height_mm",
            "What is the deck/porch height above grade in millimetres?",
            "Permit exemptions often depend on height thresholds.",
        ),
        (
            "project.deck_area_m2",
            "What is the deck/porch area in square metres?",
            "Area thresholds can change the permit path.",
        ),
        (
            "project.deck_attached",
            "Will the deck/porch be attached to the building?",
            "Attached and detached structures can follow different permit rules.",
        ),
    ],
    "accessory_structure": [
        (
            "project.accessory_area_m2",
            "What is the accessory structure area in square metres?",
            "Permit exemptions often depend on structure size.",
        ),
        (
            "project.accessory_structure_kind",
            "What kind of accessory structure is proposed (shed, garage, gazebo, pergola, or other)?",
            "Different accessory structures can have different permit thresholds.",
        ),
        (
            "project.accessory_permanent",
            "Is the accessory structure permanent/fixed rather than movable?",
            "Permanence is a permit trigger in some supported jurisdictions.",
        ),
    ],
    "addition": [
        (
            "project.floor_area_increase",
            "Will the project increase the building's floor area?",
            "An increase in floor area is a direct building-permit trigger in supported jurisdictions.",
        ),
    ],
    "kitchen_bath_plumbing": [
        (
            "project.plumbing_change",
            "Will plumbing be added, moved, or materially changed?",
            "Plumbing changes can create a permit or trade-review requirement.",
        ),
        (
            "project.structural_change",
            "Will the work alter structural or load-bearing elements?",
            "Structural work is a strong building-permit trigger.",
        ),
    ],
}

JURISDICTION_FAMILY_QUESTIONS: dict[tuple[str, str], list[Question]] = {
    ("gatineau_qc", "window_door"): [
        (
            "project.estimated_cost_cad",
            "What is the estimated total labour-and-material cost before tax?",
            "Gatineau's general existing-building renovation exemption uses a project-cost threshold.",
        )
    ],
    ("gatineau_qc", "interior_renovation"): [
        (
            "project.estimated_cost_cad",
            "What is the estimated total labour-and-material cost before tax?",
            "Gatineau's general existing-building renovation exemption uses a project-cost threshold.",
        )
    ],
    ("gatineau_qc", "basement"): [
        (
            "project.estimated_cost_cad",
            "What is the estimated total labour-and-material cost before tax?",
            "Gatineau's general existing-building renovation exemption uses a project-cost threshold.",
        )
    ],
    ("gatineau_qc", "kitchen_bath_plumbing"): [
        (
            "project.estimated_cost_cad",
            "What is the estimated total labour-and-material cost before tax?",
            "Gatineau's general existing-building renovation exemption uses a project-cost threshold.",
        )
    ],
}


def _get_path(facts: dict[str, Any], path: str) -> Any:
    value: Any = facts
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _question_payload(question: Question) -> dict[str, str]:
    fact_path, text, why = question
    return {"fact_path": fact_path, "question": text, "why_it_matters": why}


def _follow_up_questions(
    facts: dict[str, Any], result: dict[str, Any], limit: int = 3
) -> list[dict[str, str]]:
    questions: list[Question] = []

    for property_fact in result.get("required_property_facts") or []:
        question = PROPERTY_QUESTIONS.get(str(property_fact))
        if question is not None:
            questions.append(question)

    family = str((facts.get("project") or {}).get("family") or "")
    jurisdiction = str(facts.get("jurisdiction") or "")
    questions.extend(JURISDICTION_FAMILY_QUESTIONS.get((jurisdiction, family), []))
    questions.extend(FAMILY_QUESTIONS.get(family, []))

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for question in questions:
        fact_path = question[0]
        if fact_path in seen or _get_path(facts, fact_path) is not None:
            continue
        seen.add(fact_path)
        out.append(_question_payload(question))
        if len(out) >= limit:
            break
    return out


def build_workflow_guidance(
    facts: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    """Return additive agent-routing guidance without changing the legal determination."""
    determination = str(result.get("determination") or "OUT_OF_SCOPE")
    confidence = str(result.get("confidence") or "LOW")
    follow_ups = _follow_up_questions(facts, result)

    if determination == "REQUIRED":
        route = "ADD_PERMIT_TASK"
        mode = "PERMIT_PATH"
        quote_handling = "INCLUDE_PERMIT_ALLOWANCE"
        automation_safe = confidence == "HIGH"
        summary = "Treat permit work as part of the project workflow before scheduling or design lock."
    elif determination == "LIKELY_REQUIRED":
        route = "ADD_PERMIT_TASK"
        mode = "PERMIT_PATH"
        quote_handling = "INCLUDE_PERMIT_ALLOWANCE"
        automation_safe = False
        summary = "Plan for a permit path, while preserving the result as preflight rather than municipal authorization."
    elif determination == "LIKELY_NOT_REQUIRED":
        route = "CONTINUE_WITH_EVIDENCE"
        mode = "NO_PERMIT_SIGNAL"
        quote_handling = "NO_PERMIT_ALLOWANCE_SIGNAL"
        automation_safe = confidence == "HIGH" and not follow_ups
        summary = "No permit requirement was identified by the supplied facts; retain the official evidence with the job record."
    elif determination == "ADDITIONAL_REVIEW_REQUIRED":
        route = "ROUTE_SPECIAL_REVIEW"
        mode = "NEEDS_REVIEW"
        quote_handling = "HOLD_AUTOMATED_FINALIZATION"
        automation_safe = False
        summary = "Route the project for the indicated planning/heritage/special review before automated finalization."
    elif determination == "MUNICIPAL_CONFIRMATION_REQUIRED":
        if follow_ups:
            route = "COLLECT_MISSING_FACTS"
            mode = "NEEDS_MORE_CONTEXT"
            summary = "Collect the highest-value missing facts and run the deterministic preflight again."
        else:
            route = "MUNICIPAL_CONFIRMATION"
            mode = "NEEDS_REVIEW"
            summary = "The supplied facts do not support a safe deterministic yes/no; obtain municipal confirmation."
        quote_handling = "HOLD_AUTOMATED_FINALIZATION"
        automation_safe = False
    else:
        route = "MANUAL_SCOPE_REVIEW"
        mode = "UNSUPPORTED_SCOPE"
        quote_handling = "HOLD_AUTOMATED_FINALIZATION"
        automation_safe = False
        summary = "The current ruleset does not cover this scope well enough for automated routing."

    return {
        "mode": mode,
        "recommended_route": route,
        "quote_handling": quote_handling,
        "automation_safe": automation_safe,
        "summary": summary,
        "follow_up_questions": follow_ups,
    }
