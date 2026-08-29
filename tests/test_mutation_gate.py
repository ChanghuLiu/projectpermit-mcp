import unittest

from projectpermit.mutation_gate import (
    BLOCKED,
    NOOP_UNCHANGED,
    READY_FOR_EXPLICIT_WRITE,
    build_mutation_gate,
)
from projectpermit.preflight_service import run_preflight


class MutationGateTest(unittest.TestCase):
    def _scoped_facts(self):
        return {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {"heritage": False},
            "context": {
                "source_platform": "jobber",
                "source_object_type": "quote",
                "source_object_id": "opaque-jobber-id-123",
            },
            "resolve_address": False,
        }

    def test_safe_first_observation_is_ready_for_explicit_idempotent_upsert(self):
        result = run_preflight(self._scoped_facts())
        gate = result["action_bundle"]["mutation_gate"]

        self.assertEqual(READY_FOR_EXPLICIT_WRITE, gate["state"])
        self.assertTrue(gate["mutation_allowed"])
        self.assertTrue(gate["execution_requires_explicit_request"])
        self.assertEqual("UPSERT_OPERATIONAL_ROUTE", gate["recommended_operation"])
        self.assertEqual("ATOMIC_UPSERT", gate["idempotency"]["mode"])
        self.assertFalse(gate["idempotency"]["unconditional_create_allowed"])
        self.assertTrue(gate["idempotency"]["scope_fingerprint"].startswith("pps_"))
        self.assertTrue(gate["idempotency"]["idempotency_key"].startswith("ppidem_"))

    def test_repeat_unchanged_is_noop_and_suppresses_duplicate(self):
        facts = self._scoped_facts()
        first = run_preflight(facts)
        prior = first["action_bundle"]["identity"]
        repeated = run_preflight(
            {
                **facts,
                "context": {
                    **facts["context"],
                    "prior_decision_identity": prior,
                },
            }
        )
        gate = repeated["action_bundle"]["mutation_gate"]

        self.assertEqual("UNCHANGED", repeated["action_bundle"]["change"]["classification"])
        self.assertEqual(NOOP_UNCHANGED, gate["state"])
        self.assertFalse(gate["mutation_allowed"])
        self.assertEqual("NOOP", gate["recommended_operation"])
        self.assertEqual(["DUPLICATE_SUPPRESSED"], gate["reason_codes"])
        self.assertTrue(gate["idempotency"]["prior_same_key"])

    def test_safe_decision_without_work_record_scope_is_blocked(self):
        result = run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "resolve_address": False,
            }
        )
        gate = result["action_bundle"]["mutation_gate"]

        self.assertEqual(BLOCKED, gate["state"])
        self.assertFalse(gate["mutation_allowed"])
        self.assertIn("MISSING_WORK_RECORD_SCOPE", gate["reason_codes"])

    def test_non_automation_safe_result_is_blocked(self):
        result = run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door"},
                "property": {},
                "context": {
                    "source_platform": "servicem8",
                    "source_object_type": "job",
                    "source_object_id": "opaque-servicem8-id-123",
                },
                "resolve_address": False,
            }
        )
        gate = result["action_bundle"]["mutation_gate"]

        self.assertEqual(BLOCKED, gate["state"])
        self.assertFalse(gate["mutation_allowed"])
        self.assertIn("AUTOMATION_NOT_SAFE", gate["reason_codes"])

    def test_ruleset_or_evidence_refresh_with_same_key_uses_metadata_upsert(self):
        bundle = {
            "identity": {
                "idempotency_key": "ppidem_current",
                "scope_fingerprint": "pps_scope",
            },
            "change": {"classification": "EVIDENCE_REFRESHED"},
            "routing": {
                "automation_safe": True,
                "evidence_freshness": {"status": "CURRENT"},
            },
            "required_inputs": [],
        }
        gate = build_mutation_gate(
            bundle,
            prior_identity={"idempotency_key": "ppidem_current"},
        )

        self.assertEqual(READY_FOR_EXPLICIT_WRITE, gate["state"])
        self.assertEqual("UPSERT_METADATA", gate["recommended_operation"])
        self.assertEqual(["SAME_OPERATIONAL_ROUTE_METADATA_REFRESH"], gate["reason_codes"])


if __name__ == "__main__":
    unittest.main()
