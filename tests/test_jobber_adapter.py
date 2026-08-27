from __future__ import annotations

import unittest

from projectpermit.jobber_adapter import (
    JobberAdapterError,
    build_jobber_writeback,
    build_preflight_facts,
    extract_jobber_work_object,
)


class JobberAdapterTest(unittest.TestCase):
    def test_extracts_quote_scope_and_address_without_client_or_price_data(self):
        payload = {
            "__typename": "Quote",
            "id": "quote-123",
            "title": "Replace basement plumbing fixtures",
            "property": {
                "address": {
                    "street1": "100 Queen St",
                    "city": "Ottawa",
                    "province": "ON",
                    "postalCode": "K1P 1J9",
                    "country": "CA",
                },
                "client": {"name": "Private Customer", "email": "person@example.test"},
            },
            "lineItems": {
                "nodes": [
                    {
                        "name": "Bathroom rough-in",
                        "description": "Move drain and water lines",
                        "unitPrice": 3000,
                    },
                    {"name": "Install shower"},
                ]
            },
            "total": 9000,
        }

        extracted = extract_jobber_work_object(payload)
        self.assertEqual("quote", extracted["source_object_type"])
        self.assertEqual("quote-123", extracted["source_object_id"])
        self.assertEqual("100 Queen St, Ottawa, ON, K1P 1J9 CA", extracted["address"])
        self.assertIn("Bathroom rough-in", extracted["scope_text"])
        self.assertIn("Move drain and water lines", extracted["scope_text"])
        self.assertEqual(2, extracted["line_item_count"])
        self.assertTrue(extracted["project_family_normalization_required"])

        serialized = repr(extracted)
        self.assertNotIn("Private Customer", serialized)
        self.assertNotIn("person@example.test", serialized)
        self.assertNotIn("3000", serialized)
        self.assertNotIn("9000", serialized)

    def test_edges_connection_is_supported(self):
        payload = {
            "__typename": "Job",
            "id": "job-1",
            "title": "Rear deck replacement",
            "property": {"address": "453 W 12TH AVE, Vancouver, BC"},
            "lineItems": {
                "edges": [
                    {"node": {"name": "Remove existing deck"}},
                    {"node": {"name": "Build new deck", "description": "Same footprint"}},
                ]
            },
        }
        extracted = extract_jobber_work_object(payload)
        self.assertEqual(2, extracted["line_item_count"])
        self.assertIn("Build new deck — Same footprint", extracted["scope_text"])

    def test_missing_property_address_is_rejected(self):
        with self.assertRaisesRegex(JobberAdapterError, "address is required"):
            extract_jobber_work_object(
                {
                    "__typename": "Request",
                    "id": "request-1",
                    "title": "Window replacement",
                    "property": {"address": {}},
                }
            )

    def test_scope_normalization_must_be_explicit_before_preflight(self):
        extracted = {
            "source_platform": "jobber",
            "source_object_type": "quote",
            "source_object_id": "q1",
            "address": "100 Queen St, Ottawa, ON",
        }
        with self.assertRaisesRegex(JobberAdapterError, "project.family"):
            build_preflight_facts(
                extracted,
                jurisdiction="ottawa_on",
                project={},
            )

    def test_builds_existing_preflight_shape_without_guessing_project_semantics(self):
        extracted = {
            "source_platform": "jobber",
            "source_object_type": "quote",
            "source_object_id": "q1",
            "address": "100 Queen St, Ottawa, ON",
        }
        facts = build_preflight_facts(
            extracted,
            jurisdiction="ottawa_on",
            project={"family": "deck_porch", "height_m": 0.7},
            client_tag="jobber-pilot-a",
        )
        self.assertEqual("ottawa_on", facts["jurisdiction"])
        self.assertEqual("deck_porch", facts["project"]["family"])
        self.assertTrue(facts["resolve_address"])
        self.assertEqual("jobber_adapter", facts["context"]["_transport"])
        self.assertEqual("jobber-pilot-a", facts["context"]["client_tag"])
        self.assertEqual("q1", facts["context"]["source_object_id"])

    def test_writeback_is_compact_and_read_only(self):
        result = {
            "determination": "REQUIRED",
            "confidence": "HIGH",
            "requirements": [
                {
                    "rule_version": "2026-08-26.1",
                    "evidence": [
                        {"url": "https://example.gov/permit-rule", "title": "Official rule"}
                    ],
                }
            ],
        }
        writeback = build_jobber_writeback(result)
        self.assertEqual("REQUIRED", writeback["projectpermit_preflight"])
        self.assertEqual("HIGH", writeback["projectpermit_confidence"])
        self.assertEqual("2026-08-26.1", writeback["projectpermit_rule_version"])
        self.assertEqual(
            "https://example.gov/permit-rule",
            writeback["projectpermit_evidence_url"],
        )


if __name__ == "__main__":
    unittest.main()
