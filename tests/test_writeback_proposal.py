import unittest

from projectpermit.preflight_service import run_preflight
from projectpermit.writeback_proposal import (
    build_jobber_safe_writeback_proposal,
    build_servicem8_safe_writeback_proposal,
)


class WritebackProposalTest(unittest.TestCase):
    def _result(self, platform: str, object_type: str):
        return run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "context": {
                    "source_platform": platform,
                    "source_object_type": object_type,
                    "source_object_id": f"opaque-{platform}-record-1",
                },
                "resolve_address": False,
            }
        )

    def test_jobber_proposal_exposes_ready_gate_but_never_mutates(self):
        proposal = build_jobber_safe_writeback_proposal(self._result("jobber", "quote"))
        self.assertEqual("jobber", proposal["source_platform"])
        self.assertTrue(proposal["writeback_ready"])
        self.assertEqual("UPSERT_OPERATIONAL_ROUTE", proposal["proposed_operation"])
        self.assertFalse(proposal["mutation_performed"])
        self.assertEqual(
            proposal["idempotency_key"],
            proposal["mutation_gate"]["idempotency"]["idempotency_key"],
        )

    def test_servicem8_proposal_exposes_ready_gate_but_never_mutates(self):
        proposal = build_servicem8_safe_writeback_proposal(self._result("servicem8", "job"))
        self.assertEqual("servicem8", proposal["source_platform"])
        self.assertTrue(proposal["writeback_ready"])
        self.assertEqual("UPSERT_OPERATIONAL_ROUTE", proposal["proposed_operation"])
        self.assertFalse(proposal["mutation_performed"])
        self.assertEqual(
            proposal["idempotency_key"],
            proposal["mutation_gate"]["idempotency"]["idempotency_key"],
        )


if __name__ == "__main__":
    unittest.main()
