from projectpermit.workflow_advice import build_workflow_guidance


def test_required_routes_to_permit_task():
    guidance = build_workflow_guidance(
        {"jurisdiction": "ottawa_on", "project": {"family": "addition"}},
        {"determination": "REQUIRED", "confidence": "HIGH", "requirements": []},
    )

    assert guidance["mode"] == "PERMIT_PATH"
    assert guidance["recommended_route"] == "ADD_PERMIT_TASK"
    assert guidance["quote_handling"] == "INCLUDE_PERMIT_ALLOWANCE"
    assert guidance["automation_safe"] is True
    assert guidance["follow_up_questions"] == []


def test_high_confidence_exemption_can_continue_with_evidence():
    guidance = build_workflow_guidance(
        {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size", "structural_change": False},
            "property": {"heritage": False},
        },
        {"determination": "LIKELY_NOT_REQUIRED", "confidence": "HIGH", "requirements": []},
    )

    assert guidance["mode"] == "NO_PERMIT_SIGNAL"
    assert guidance["recommended_route"] == "CONTINUE_WITH_EVIDENCE"
    assert guidance["automation_safe"] is True


def test_property_context_is_asked_first_when_required():
    guidance = build_workflow_guidance(
        {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {},
        },
        {
            "determination": "MUNICIPAL_CONFIRMATION_REQUIRED",
            "confidence": "MEDIUM",
            "requirements": [],
            "required_property_facts": ["heritage"],
        },
    )

    assert guidance["recommended_route"] == "COLLECT_MISSING_FACTS"
    assert guidance["automation_safe"] is False
    assert guidance["follow_up_questions"][0]["fact_path"] == "property.heritage"


def test_gatineau_ambiguous_renovation_prioritizes_cost_question():
    guidance = build_workflow_guidance(
        {
            "jurisdiction": "gatineau_qc",
            "project": {"family": "interior_renovation", "structural_change": False},
            "property": {"heritage": False, "piia": False},
        },
        {
            "determination": "MUNICIPAL_CONFIRMATION_REQUIRED",
            "confidence": "MEDIUM",
            "requirements": [],
        },
    )

    assert guidance["recommended_route"] == "COLLECT_MISSING_FACTS"
    assert guidance["follow_up_questions"][0]["fact_path"] == "project.estimated_cost_cad"


def test_out_of_scope_never_marks_automation_safe():
    guidance = build_workflow_guidance(
        {"jurisdiction": "ottawa_on", "project": {"family": "unknown"}},
        {"determination": "OUT_OF_SCOPE", "confidence": "LOW", "requirements": []},
    )

    assert guidance["mode"] == "UNSUPPORTED_SCOPE"
    assert guidance["recommended_route"] == "MANUAL_SCOPE_REVIEW"
    assert guidance["automation_safe"] is False
