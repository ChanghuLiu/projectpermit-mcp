import unittest

from projectpermit.jobber_adapter import build_jobber_action_proposal, build_jobber_writeback
from projectpermit.servicem8_adapter import (
    build_servicem8_action_proposal,
    build_servicem8_routing_summary,
)


def sample_result() -> dict:
    return {
        "determination": "REQUIRED",
        "confidence": "HIGH",
        "requirements": [],
        "action_bundle": {
            "writeback_hints": {
                "permit_status": "REQUIRED",
                "confidence": "HIGH",
                "recommended_route": "ADD_PERMIT_TASK",
                "quote_handling": "INCLUDE_PERMIT_ALLOWANCE",
                "automation_safe": True,
                "rule_version": "2026-08-26.1",
                "evidence_url": "https://example.gov/permit",
                "freshness_status": "CURRENT",
            },
            "tasks": [
                {
                    "task_type": "PERMIT_PROCESS",
                    "blocking": True,
                    "action": "Add a permit task/allowance before scheduling or design lock.",
                }
            ],
            "required_inputs": [],
            "evidence": [
                {
                    "source_id": "TEST",
                    "authority": "Test City",
                    "title": "Permit rule",
                    "url": "https://example.gov/permit",
                    "rule_ids": ["TEST-001"],
                    "statuses": ["REQUIRED"],
                    "source_verified_at": "2026-08-26",
                }
            ],
            "audit": {
                "engine_version": "phase0-0.1.0",
                "rule_ids": ["TEST-001"],
                "rule_versions": ["2026-08-26.1"],
                "source_verified_at_oldest": "2026-08-26",
                "source_verified_at_newest": "2026-08-26",
                "evidence_source_count": 1,
                "generated_from": "deterministic_preflight",
            },
        },
    }


class PlatformActionProposalTest(unittest.TestCase):
    def test_jobber_maps_bundle_to_richer_custom_fields_without_mutation(self):
        result = sample_result()
        fields = build_jobber_writeback(result)
        self.assertEqual("REQUIRED", fields["projectpermit_preflight"])
        self.assertEqual("ADD_PERMIT_TASK", fields["projectpermit_route"])
        self.assertEqual("INCLUDE_PERMIT_ALLOWANCE", fields["projectpermit_quote_handling"])
        self.assertEqual("true", fields["projectpermit_automation_safe"])
        self.assertEqual("CURRENT", fields["projectpermit_freshness"])

        proposal = build_jobber_action_proposal(result)
        self.assertEqual("jobber", proposal["source_platform"])
        self.assertFalse(proposal["mutation_performed"])
        self.assertEqual("PERMIT_PROCESS", proposal["proposed_tasks"][0]["task_type"])
        self.assertEqual("https://example.gov/permit", proposal["evidence"][0]["url"])
        self.assertEqual(["TEST-001"], proposal["audit"]["rule_ids"])

    def test_servicem8_maps_bundle_to_richer_routing_without_mutation(self):
        result = sample_result()
        fields = build_servicem8_routing_summary(result)
        self.assertEqual("REQUIRED", fields["projectpermit_preflight"])
        self.assertEqual("ADD_PERMIT_TASK", fields["projectpermit_route"])
        self.assertEqual("INCLUDE_PERMIT_ALLOWANCE", fields["projectpermit_quote_handling"])
        self.assertEqual("true", fields["projectpermit_automation_safe"])
        self.assertEqual("CURRENT", fields["projectpermit_freshness"])

        proposal = build_servicem8_action_proposal(result)
        self.assertEqual("servicem8", proposal["source_platform"])
        self.assertFalse(proposal["mutation_performed"])
        self.assertEqual("PERMIT_PROCESS", proposal["proposed_tasks"][0]["task_type"])
        self.assertEqual("https://example.gov/permit", proposal["evidence"][0]["url"])

    def test_proposals_do_not_mutate_bundle_objects(self):
        result = sample_result()
        jobber = build_jobber_action_proposal(result)
        service = build_servicem8_action_proposal(result)
        jobber["proposed_tasks"][0]["action"] = "changed"
        service["evidence"][0]["title"] = "changed"

        self.assertNotEqual(
            "changed",
            result["action_bundle"]["tasks"][0]["action"],
        )
        self.assertNotEqual(
            "changed",
            result["action_bundle"]["evidence"][0]["title"],
        )


if __name__ == "__main__":
    unittest.main()
