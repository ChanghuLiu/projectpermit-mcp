import json
import unittest

from projectpermit.decision_identity import (
    build_decision_identity,
    classify_identity_change,
)
from projectpermit.preflight_service import run_preflight


def fixture_result(
    *,
    determination: str = "REQUIRED",
    route: str = "ADD_PERMIT_TASK",
    quote_handling: str = "INCLUDE_PERMIT_ALLOWANCE",
    automation_safe: bool = True,
    freshness_status: str = "CURRENT",
) -> dict:
    return {
        "determination": determination,
        "confidence": "HIGH",
        "workflow": {
            "recommended_route": route,
            "quote_handling": quote_handling,
            "automation_safe": automation_safe,
            "evidence_freshness": {"status": freshness_status},
        },
    }


def fixture_evidence(verified_at: str = "2026-08-26") -> list[dict]:
    return [
        {
            "source_id": "OTT_GENERAL",
            "url": "https://ottawa.example/permit",
            "rule_ids": ["OTT-BLD-001"],
            "source_verified_at": verified_at,
        }
    ]


def fixture_audit(rule_version: str = "2026-08-26.1") -> dict:
    return {
        "engine_version": "phase0-0.1.0",
        "rule_ids": ["OTT-BLD-001"],
        "rule_versions": [rule_version],
    }


class DecisionIdentityTest(unittest.TestCase):
    def test_mapping_order_does_not_change_identity(self):
        facts_a = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "structural_change": False, "action": "replace_same_size"},
            "property": {"heritage": False, "zoning_code": "R1"},
        }
        facts_b = {
            "property": {"zoning_code": "R1", "heritage": False},
            "project": {"action": "replace_same_size", "family": "window_door", "structural_change": False},
            "jurisdiction": "ottawa_on",
        }
        first = build_decision_identity(
            facts_a,
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        second = build_decision_identity(
            facts_b,
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        self.assertEqual(first["bundle_id"], second["bundle_id"])
        self.assertEqual(first["input_fingerprint"], second["input_fingerprint"])
        self.assertEqual(first["idempotency_key"], second["idempotency_key"])

    def test_raw_address_and_platform_id_do_not_change_reusable_bundle_identity(self):
        base = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "addition", "floor_area_increase": True},
            "property": {"heritage": False},
        }
        first = build_decision_identity(
            {
                **base,
                "address": "111 Private Street, Ottawa, ON",
                "context": {
                    "source_platform": "jobber",
                    "source_object_type": "job",
                    "source_object_id": "job-secret-111",
                },
            },
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        second = build_decision_identity(
            {
                **base,
                "address": "999 Different Private Street, Ottawa, ON",
                "context": {
                    "source_platform": "jobber",
                    "source_object_type": "job",
                    "source_object_id": "job-secret-999",
                },
            },
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        self.assertEqual(first["bundle_id"], second["bundle_id"])
        self.assertEqual(first["input_fingerprint"], second["input_fingerprint"])
        self.assertNotEqual(first["scope_fingerprint"], second["scope_fingerprint"])
        self.assertNotEqual(first["idempotency_key"], second["idempotency_key"])
        rendered = json.dumps([first, second])
        self.assertNotIn("Private Street", rendered)
        self.assertNotIn("job-secret-111", rendered)
        self.assertNotIn("job-secret-999", rendered)

    def test_evidence_refresh_changes_bundle_but_not_task_idempotency(self):
        facts = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "addition"},
            "property": {},
            "context": {"source_platform": "jobber", "source_object_type": "job", "source_object_id": "J-1"},
        }
        first = build_decision_identity(
            facts,
            fixture_result(),
            evidence=fixture_evidence("2026-08-01"),
            audit=fixture_audit(),
        )
        second = build_decision_identity(
            facts,
            fixture_result(),
            evidence=fixture_evidence("2026-08-29"),
            audit=fixture_audit(),
        )
        self.assertNotEqual(first["bundle_id"], second["bundle_id"])
        self.assertNotEqual(first["evidence_fingerprint"], second["evidence_fingerprint"])
        self.assertEqual(first["idempotency_key"], second["idempotency_key"])
        change = classify_identity_change(first, second)
        self.assertEqual("EVIDENCE_REFRESHED", change["classification"])
        self.assertEqual(["EVIDENCE_REFRESHED"], change["reasons"])

    def test_ruleset_refresh_changes_bundle_but_not_task_idempotency(self):
        facts = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "addition"},
            "context": {"source_platform": "jobber", "source_object_type": "job", "source_object_id": "J-1"},
        }
        first = build_decision_identity(
            facts,
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit("2026-08-26.1"),
        )
        second = build_decision_identity(
            facts,
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit("2026-08-29.1"),
        )
        self.assertNotEqual(first["ruleset_fingerprint"], second["ruleset_fingerprint"])
        self.assertEqual(first["idempotency_key"], second["idempotency_key"])
        self.assertEqual("RULESET_CHANGED", classify_identity_change(first, second)["classification"])

    def test_route_change_changes_task_idempotency(self):
        facts = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door"},
            "context": {"idempotency_scope": "jobber:quote:Q-1"},
        }
        first = build_decision_identity(
            facts,
            fixture_result(
                determination="LIKELY_NOT_REQUIRED",
                route="CONTINUE_WITH_EVIDENCE",
                quote_handling="NO_PERMIT_ALLOWANCE_SIGNAL",
            ),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        second = build_decision_identity(
            facts,
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        self.assertNotEqual(first["idempotency_key"], second["idempotency_key"])
        change = classify_identity_change(first, second)
        self.assertEqual("DECISION_CHANGED", change["classification"])
        self.assertIn("ROUTE_CHANGED", change["reasons"])

    def test_input_change_is_classified_when_decision_and_route_stay_same(self):
        first = build_decision_identity(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition", "floor_area_increase": True}},
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        second = build_decision_identity(
            {"jurisdiction": "ottawa_on", "project": {"family": "addition", "floor_area_increase": True, "structural_change": True}},
            fixture_result(),
            evidence=fixture_evidence(),
            audit=fixture_audit(),
        )
        self.assertEqual("INPUT_CHANGED", classify_identity_change(first, second)["classification"])

    def test_shared_preflight_can_classify_repeat_as_unchanged(self):
        facts = {
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {"heritage": False},
            "context": {
                "source_platform": "jobber",
                "source_object_type": "quote",
                "source_object_id": "Q-42",
            },
            "resolve_address": False,
        }
        first = run_preflight(facts)
        self.assertEqual("FIRST_OBSERVATION", first["action_bundle"]["change"]["classification"])
        identity = first["action_bundle"]["identity"]

        second_facts = dict(facts)
        second_facts["context"] = {
            **facts["context"],
            "prior_decision_identity": identity,
        }
        second = run_preflight(second_facts)
        self.assertEqual("UNCHANGED", second["action_bundle"]["change"]["classification"])
        self.assertFalse(second["action_bundle"]["change"]["material_change"])
        self.assertEqual(
            first["action_bundle"]["identity"]["idempotency_key"],
            second["action_bundle"]["identity"]["idempotency_key"],
        )


if __name__ == "__main__":
    unittest.main()
