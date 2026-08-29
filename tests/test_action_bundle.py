import unittest

from projectpermit.action_bundle import build_action_bundle


class ActionBundleTest(unittest.TestCase):
    def test_required_result_builds_blocking_permit_task_and_deduped_evidence(self):
        result = {
            "jurisdiction": {"country": "CA", "province": "ON", "municipality": "Ottawa"},
            "determination": "REQUIRED",
            "confidence": "HIGH",
            "engine_version": "phase0-0.1.0",
            "disclaimer": "Preflight only.",
            "requirements": [
                {
                    "status": "REQUIRED",
                    "rule_id": "OTT-BLD-001",
                    "rule_version": "2026-08-26.1",
                    "source_verified_at": "2026-08-26",
                    "evidence": [
                        {
                            "source_id": "OTT_GENERAL",
                            "authority": "City of Ottawa",
                            "title": "Building permit projects",
                            "url": "https://ottawa.example/permit",
                        }
                    ],
                },
                {
                    "status": "ADDITIONAL_REVIEW_REQUIRED",
                    "rule_id": "OTT-ZONE-001",
                    "rule_version": "2026-08-26.1",
                    "source_verified_at": "2026-08-26",
                    "evidence": [
                        {
                            "source_id": "OTT_GENERAL",
                            "authority": "City of Ottawa",
                            "title": "Building permit projects",
                            "url": "https://ottawa.example/permit",
                        }
                    ],
                },
            ],
            "workflow": {
                "recommended_route": "ADD_PERMIT_TASK",
                "quote_handling": "INCLUDE_PERMIT_ALLOWANCE",
                "automation_safe": True,
                "follow_up_questions": [],
                "evidence_freshness": {"status": "CURRENT", "automation_blocked": False},
            },
        }

        bundle = build_action_bundle(
            {"project": {"family": "addition"}},
            result,
        )

        self.assertEqual("2026-08-29.3", bundle["bundle_version"])
        self.assertEqual("REQUIRED", bundle["decision"]["determination"])
        self.assertEqual("addition", bundle["decision"]["project_family"])
        self.assertEqual("ADD_PERMIT_TASK", bundle["routing"]["recommended_route"])
        self.assertTrue(bundle["routing"]["automation_safe"])
        self.assertEqual("PERMIT_PROCESS", bundle["tasks"][0]["task_type"])
        self.assertTrue(bundle["tasks"][0]["blocking"])
        self.assertEqual("ATTACH_EVIDENCE", bundle["tasks"][1]["task_type"])
        self.assertEqual(1, len(bundle["evidence"]))
        self.assertEqual(
            ["OTT-BLD-001", "OTT-ZONE-001"],
            bundle["evidence"][0]["rule_ids"],
        )
        self.assertEqual(2, len(bundle["audit"]["rule_ids"]))
        self.assertEqual("deterministic_preflight", bundle["audit"]["generated_from"])
        self.assertEqual("BLOCKED", bundle["mutation_gate"]["state"])
        self.assertIn("MISSING_WORK_RECORD_SCOPE", bundle["mutation_gate"]["reason_codes"])

    def test_missing_facts_are_preserved_as_required_inputs(self):
        question = {
            "fact_path": "property.heritage",
            "question": "Is the property heritage designated?",
            "why_it_matters": "It can change the permit path.",
        }
        result = {
            "jurisdiction": {"country": "CA", "province": "ON", "municipality": "Toronto"},
            "determination": "MUNICIPAL_CONFIRMATION_REQUIRED",
            "confidence": "MEDIUM",
            "engine_version": "phase0-0.1.0",
            "disclaimer": "Preflight only.",
            "requirements": [],
            "workflow": {
                "recommended_route": "COLLECT_MISSING_FACTS",
                "quote_handling": "HOLD_AUTOMATED_FINALIZATION",
                "automation_safe": False,
                "follow_up_questions": [question],
                "evidence_freshness": {"status": "UNKNOWN", "automation_blocked": True},
            },
        }

        bundle = build_action_bundle(
            {"project": {"family": "window_door"}},
            result,
        )

        self.assertEqual([question], bundle["required_inputs"])
        self.assertEqual("COLLECT_MISSING_FACTS", bundle["tasks"][0]["task_type"])
        self.assertTrue(bundle["tasks"][0]["blocking"])
        self.assertEqual("UNKNOWN", bundle["routing"]["evidence_freshness"]["status"])
        self.assertEqual("COLLECT_MISSING_FACTS", bundle["writeback_hints"]["recommended_route"])
        self.assertEqual("BLOCKED", bundle["mutation_gate"]["state"])
        self.assertIn("AUTOMATION_NOT_SAFE", bundle["mutation_gate"]["reason_codes"])
        self.assertIn("REQUIRED_INPUTS_PENDING", bundle["mutation_gate"]["reason_codes"])

    def test_continue_with_evidence_has_nonblocking_task_and_writeback_hints(self):
        result = {
            "jurisdiction": {"country": "CA", "province": "BC", "municipality": "Vancouver"},
            "determination": "LIKELY_NOT_REQUIRED",
            "confidence": "HIGH",
            "engine_version": "phase0-0.1.0",
            "disclaimer": "Preflight only.",
            "requirements": [
                {
                    "status": "LIKELY_NOT_REQUIRED",
                    "rule_id": "VAN-001",
                    "rule_version": "2026-08-26.1",
                    "source_verified_at": "2026-08-26",
                    "evidence": [
                        {
                            "source_id": "VAN_WHEN",
                            "authority": "City of Vancouver",
                            "title": "When you need a permit",
                            "url": "https://vancouver.example/permit",
                        }
                    ],
                }
            ],
            "workflow": {
                "recommended_route": "CONTINUE_WITH_EVIDENCE",
                "quote_handling": "NO_PERMIT_ALLOWANCE_SIGNAL",
                "automation_safe": True,
                "follow_up_questions": [],
                "evidence_freshness": {"status": "CURRENT", "automation_blocked": False},
            },
        }

        bundle = build_action_bundle(
            {
                "project": {"family": "interior_renovation"},
                "context": {
                    "source_platform": "jobber",
                    "source_object_type": "quote",
                    "source_object_id": "opaque-direct-builder-test",
                },
            },
            result,
        )

        self.assertEqual(1, len(bundle["tasks"]))
        self.assertEqual("ATTACH_EVIDENCE", bundle["tasks"][0]["task_type"])
        self.assertFalse(bundle["tasks"][0]["blocking"])
        self.assertEqual("https://vancouver.example/permit", bundle["writeback_hints"]["evidence_url"])
        self.assertEqual("2026-08-26.1", bundle["writeback_hints"]["rule_version"])
        self.assertEqual("CURRENT", bundle["writeback_hints"]["freshness_status"])
        self.assertEqual("READY_FOR_EXPLICIT_WRITE", bundle["mutation_gate"]["state"])
        self.assertEqual("UPSERT_OPERATIONAL_ROUTE", bundle["mutation_gate"]["recommended_operation"])
        self.assertTrue(bundle["mutation_gate"]["mutation_allowed"])

    def test_workflow_is_required(self):
        with self.assertRaisesRegex(ValueError, "result.workflow"):
            build_action_bundle(
                {"project": {"family": "addition"}},
                {"determination": "REQUIRED", "requirements": []},
            )


if __name__ == "__main__":
    unittest.main()
