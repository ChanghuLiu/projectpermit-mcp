import unittest

from fastapi.testclient import TestClient

from projectpermit.api import app
from projectpermit.preflight_service import run_preflight


class ActionBundleIntegrationTest(unittest.TestCase):
    def test_shared_preflight_attaches_bundle_matching_workflow(self):
        result = run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "resolve_address": False,
            }
        )

        self.assertIn("workflow", result)
        self.assertIn("action_bundle", result)
        bundle = result["action_bundle"]
        self.assertEqual(
            result["workflow"]["recommended_route"],
            bundle["routing"]["recommended_route"],
        )
        self.assertEqual(
            result["workflow"]["automation_safe"],
            bundle["routing"]["automation_safe"],
        )
        self.assertEqual("window_door", bundle["decision"]["project_family"])
        self.assertGreaterEqual(bundle["audit"]["evidence_source_count"], 1)
        self.assertGreaterEqual(len(bundle["audit"]["rule_ids"]), 1)
        self.assertEqual("deterministic_preflight", bundle["audit"]["generated_from"])
        self.assertEqual("ATTACH_EVIDENCE", bundle["tasks"][0]["task_type"])
        self.assertIn("mutation_gate", bundle)
        self.assertEqual("BLOCKED", bundle["mutation_gate"]["state"])
        self.assertIn(
            "MISSING_WORK_RECORD_SCOPE",
            bundle["mutation_gate"]["reason_codes"],
        )

    def test_http_capabilities_advertise_action_bundle_and_read_only_integrations(self):
        client = TestClient(app)
        response = client.get("/v1/capabilities")
        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("action_bundle", payload["action_bundle"]["field"])
        self.assertIn("tasks", payload["action_bundle"]["includes"])
        self.assertIn("evidence", payload["action_bundle"]["includes"])
        self.assertIn("mutation_gate", payload["action_bundle"]["includes"])
        self.assertEqual(
            "read_only_proposal_supported",
            payload["integration_proposals"]["jobber"],
        )
        self.assertEqual(
            "read_only_proposal_supported",
            payload["integration_proposals"]["servicem8"],
        )
        self.assertEqual(
            "action_bundle.mutation_gate",
            payload["mutation_gate"]["field"],
        )
        self.assertEqual(
            {"READY_FOR_EXPLICIT_WRITE", "NOOP_UNCHANGED", "BLOCKED"},
            set(payload["mutation_gate"]["states"]),
        )
        self.assertFalse(payload["mutation_gate"]["unconditional_create_allowed"])
        self.assertFalse(
            payload["mutation_gate"]["external_mutation_performed_by_projectpermit"]
        )
        self.assertEqual(
            "mutation_gate_supported",
            payload["safe_writeback_proposals"]["jobber"],
        )
        self.assertEqual(
            "mutation_gate_supported",
            payload["safe_writeback_proposals"]["servicem8"],
        )

    def test_batch_items_receive_action_bundle_without_changing_batch_audit(self):
        client = TestClient(app)
        response = client.post(
            "/v1/preview-project-requirements-batch",
            json={
                "items": [
                    {
                        "client_ref": "bundle-1",
                        "jurisdiction": "vancouver_bc",
                        "project": {"family": "interior_renovation", "action": "painting"},
                    }
                ]
            },
        )
        self.assertEqual(200, response.status_code)
        payload = response.json()
        result = payload["results"][0]["result"]
        self.assertIn("action_bundle", result)
        self.assertIn("mutation_gate", result["action_bundle"])
        self.assertEqual("bundle-1", payload["results"][0]["client_ref"])
        self.assertGreaterEqual(payload["audit"]["unique_rule_ids"], 1)


if __name__ == "__main__":
    unittest.main()
