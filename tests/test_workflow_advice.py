import unittest
from datetime import date

from projectpermit.workflow_advice import build_workflow_guidance


AS_OF = date(2026, 8, 29)


def requirement(verified_at: str) -> dict:
    return {
        "type": "building_permit",
        "status": "LIKELY_NOT_REQUIRED",
        "reason": "test",
        "rule_id": "TEST-001",
        "rule_version": "test",
        "source_verified_at": verified_at,
        "evidence": [],
    }


class WorkflowAdviceTest(unittest.TestCase):
    def test_required_routes_to_permit_task(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition"}},
            {
                "determination": "REQUIRED",
                "confidence": "HIGH",
                "requirements": [requirement("2026-08-26")],
            },
            as_of=AS_OF,
        )

        self.assertEqual("PERMIT_PATH", guidance["mode"])
        self.assertEqual("ADD_PERMIT_TASK", guidance["recommended_route"])
        self.assertEqual("INCLUDE_PERMIT_ALLOWANCE", guidance["quote_handling"])
        self.assertTrue(guidance["automation_safe"])
        self.assertEqual([], guidance["follow_up_questions"])
        self.assertEqual("CURRENT", guidance["evidence_freshness"]["status"])
        self.assertEqual(3, guidance["evidence_freshness"]["oldest_age_days"])

    def test_high_confidence_exemption_can_continue_with_fresh_evidence(self):
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
                "requirements": [requirement("2026-08-26")],
            },
            as_of=AS_OF,
        )

        self.assertEqual("NO_PERMIT_SIGNAL", guidance["mode"])
        self.assertEqual("CONTINUE_WITH_EVIDENCE", guidance["recommended_route"])
        self.assertTrue(guidance["automation_safe"])
        self.assertEqual([], guidance["follow_up_questions"])
        self.assertFalse(guidance["evidence_freshness"]["automation_blocked"])

    def test_review_due_evidence_blocks_unattended_automation_without_changing_route(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "window_door"}},
            {
                "determination": "LIKELY_NOT_REQUIRED",
                "confidence": "HIGH",
                "requirements": [requirement("2026-05-01")],
            },
            as_of=AS_OF,
        )

        self.assertEqual("CONTINUE_WITH_EVIDENCE", guidance["recommended_route"])
        self.assertFalse(guidance["automation_safe"])
        self.assertEqual("REVIEW_DUE", guidance["evidence_freshness"]["status"])
        self.assertTrue(guidance["evidence_freshness"]["automation_blocked"])

    def test_stale_evidence_blocks_unattended_automation_without_changing_determination_route(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition"}},
            {
                "determination": "REQUIRED",
                "confidence": "HIGH",
                "requirements": [requirement("2026-01-01")],
            },
            as_of=AS_OF,
        )

        self.assertEqual("ADD_PERMIT_TASK", guidance["recommended_route"])
        self.assertFalse(guidance["automation_safe"])
        self.assertEqual("STALE", guidance["evidence_freshness"]["status"])
        self.assertTrue(guidance["evidence_freshness"]["automation_blocked"])

    def test_missing_verification_date_is_unknown_and_blocks_automation(self):
        guidance = build_workflow_guidance(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition"}},
            {"determination": "REQUIRED", "confidence": "HIGH", "requirements": []},
            as_of=AS_OF,
        )

        self.assertEqual("UNKNOWN", guidance["evidence_freshness"]["status"])
        self.assertTrue(guidance["evidence_freshness"]["automation_blocked"])
        self.assertFalse(guidance["automation_safe"])

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
            as_of=AS_OF,
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
            as_of=AS_OF,
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
            as_of=AS_OF,
        )

        self.assertEqual("UNSUPPORTED_SCOPE", guidance["mode"])
        self.assertEqual("MANUAL_SCOPE_REVIEW", guidance["recommended_route"])
        self.assertFalse(guidance["automation_safe"])


if __name__ == "__main__":
    unittest.main()
