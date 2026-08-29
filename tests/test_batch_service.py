import unittest

from projectpermit.batch_service import MAX_BATCH_ITEMS, run_batch_preflight


class BatchPreflightServiceTest(unittest.TestCase):
    def test_bulk_success_preserves_client_ref_and_builds_audit_summary(self):
        payload = run_batch_preflight(
            [
                {
                    "client_ref": "lead-001",
                    "jurisdiction": "ottawa_on",
                    "project": {"family": "window_door", "action": "replace_same_size"},
                    "property": {"heritage": False},
                },
                {
                    "client_ref": "lead-002",
                    "jurisdiction": "toronto_on",
                    "project": {
                        "family": "window_door",
                        "action": "enlarge_existing_opening",
                    },
                },
            ],
            allow_address=False,
            transport="unit_test_batch",
        )

        self.assertEqual(2, payload["batch_size"])
        self.assertEqual(2, payload["succeeded"])
        self.assertEqual(0, payload["failed"])
        self.assertEqual("lead-001", payload["results"][0]["client_ref"])
        self.assertEqual("LIKELY_NOT_REQUIRED", payload["results"][0]["result"]["determination"])
        self.assertTrue(payload["results"][1]["ok"])
        self.assertGreaterEqual(payload["audit"]["unique_rule_ids"], 2)
        self.assertGreaterEqual(payload["audit"]["evidence_links"], 2)
        self.assertTrue(payload["audit"]["engine_versions"])
        self.assertIsNotNone(payload["audit"]["source_verified_at_oldest"])
        self.assertIsNotNone(payload["audit"]["source_verified_at_newest"])

    def test_bad_item_is_isolated(self):
        payload = run_batch_preflight(
            [
                {
                    "client_ref": "good",
                    "jurisdiction": "ottawa_on",
                    "project": {"family": "window_door", "action": "replace_same_size"},
                    "property": {"heritage": False},
                },
                {
                    "client_ref": "bad",
                    "jurisdiction": "ottawa_on",
                },
            ],
            allow_address=False,
            transport="unit_test_batch",
        )

        self.assertEqual(1, payload["succeeded"])
        self.assertEqual(1, payload["failed"])
        self.assertTrue(payload["results"][0]["ok"])
        self.assertFalse(payload["results"][1]["ok"])
        self.assertEqual("validation_error", payload["results"][1]["error"]["type"])
        self.assertEqual("bad", payload["results"][1]["client_ref"])

    def test_anonymous_batch_rejects_address_per_item_without_failing_batch(self):
        payload = run_batch_preflight(
            [
                {
                    "client_ref": "addressed",
                    "jurisdiction": "ottawa_on",
                    "project": {"family": "window_door", "action": "replace_same_size"},
                    "address": "123 Example St",
                }
            ],
            allow_address=False,
            transport="unit_test_batch",
        )

        self.assertEqual(0, payload["succeeded"])
        self.assertEqual(1, payload["failed"])
        self.assertIn("does not accept address", payload["results"][0]["error"]["message"])

    def test_empty_and_oversized_batches_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            run_batch_preflight([], allow_address=False, transport="unit_test_batch")

        with self.assertRaisesRegex(ValueError, f"at most {MAX_BATCH_ITEMS}"):
            run_batch_preflight(
                [
                    {
                        "jurisdiction": "ottawa_on",
                        "project": {"family": "window_door", "action": "replace_same_size"},
                    }
                ]
                * (MAX_BATCH_ITEMS + 1),
                allow_address=False,
                transport="unit_test_batch",
            )

    def test_client_ref_length_is_bounded(self):
        payload = run_batch_preflight(
            [
                {
                    "client_ref": "x" * 201,
                    "jurisdiction": "ottawa_on",
                    "project": {"family": "window_door", "action": "replace_same_size"},
                }
            ],
            allow_address=False,
            transport="unit_test_batch",
        )
        self.assertFalse(payload["results"][0]["ok"])
        self.assertIn("client_ref", payload["results"][0]["error"]["message"])


if __name__ == "__main__":
    unittest.main()
