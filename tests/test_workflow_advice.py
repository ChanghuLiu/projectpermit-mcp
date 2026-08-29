import unittest

from projectpermit.workflow_advice import build_workflow_guidance


class WorkflowAdviceTest(unittest.TestCase):
    def test_required_routes_to_permit_task(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition"}},
            {"determination": "REQUIRED", "confidence": "HIGH", "requirements": []},
        )

        self.assertEqual("PERMIT_PATH", guidance["mode"])
        self.assertEqual("ADD_PERMIT_TASK", guidance["recommended_route"])
        self.assertEqual("INCLUDE_PERMIT_ALLOWANCE", guidance["quote_handling"])
        self.assertTrue(guidance["automation_safe"])
        self.assertEqual([], guidance["follow_up_questions"])

    def test_high_confidence_exemption_can_continue_with_evidence(self):
        guidance = build_workflow_guidance(
            {
                "jurisdiction": "ottawa_on",
                "project": {
                    "family": "window_door",
                    "action": "replace_same_size",
                    "structural_change": False,
                },
                "property": {"heritage": False},
            },
            {
                "determination": "LIKELY_NOT_REQUIRED",
                "confidence": "HIGH",
                "requirements": [],
            },
        )

        self.assertEqual("NO_PERMIT_SIGNAL", guidance["mode"])
        self.assertEqual("CONTINUE_WITH_EVIDENCE", guidance["recommended_route"])
        self.assertTrue(guidance["automation_safe"])
        self.assertEqual([], guidance["follow_up_questions"])

    def test_property_context_is_asked_first_when_required(self):
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

        self.assertEqual("COLLECT_MISSING_FACTS", guidance["recommended_route"])
        self.assertFalse(guidance["automation_safe"])
        self.assertEqual(
            "property.heritage",
            guidance["follow_up_questions"][0]["fact_path"],
        )

    def test_gatineau_ambiguous_renovation_prioritizes_cost_question(self):
        guidance = build_workflow_guidance(
            {
                "jurisdiction": "gatineau_qc",
                "project": {
                    "family": "interior_renovation",
                    "structural_change": False,
                },
                "property": {"heritage": False, "piia": False},
            },
            {
                "determination": "MUNICIPAL_CONFIRMATION_REQUIRED",
                "confidence": "MEDIUM",
                "requirements": [],
            },
        )

        self.assertEqual("COLLECT_MISSING_FACTS", guidance["recommended_route"])
        self.assertEqual(
            "project.estimated_cost_cad",
            guidance["follow_up_questions"][0]["fact_path"],
        )

    def test_out_of_scope_never_marks_automation_safe(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "unknown"}},
            {"determination": "OUT_OF_SCOPE", "confidence": "LOW", "requirements": []},
        )

        self.assertEqual("UNSUPPORTED_SCOPE", guidance["mode"])
        self.assertEqual("MANUAL_SCOPE_REVIEW", guidance["recommended_route"])
        self.assertFalse(guidance["automation_safe"])


if __name__ == "__main__":
    unittest.main()
