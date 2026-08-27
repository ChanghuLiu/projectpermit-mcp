import unittest

from projectpermit.servicem8_adapter import (
    ServiceM8AdapterError,
    build_preflight_facts,
    build_servicem8_routing_summary,
    extract_servicem8_work_object,
)


class ServiceM8AdapterTest(unittest.TestCase):
    def test_extracts_only_scope_address_status_and_id(self):
        payload = {
            "uuid": "job-123",
            "status": "Quote",
            "job_address": "100 Queen St, Ottawa, ON K1P 1J9",
            "job_description": "Move basement drain and add shower rough-in",
            "company_uuid": "private-client-id",
            "billing_address": "Private billing address",
            "payment_received": 1,
            "payment_amount": "9000",
            "created_by_staff_uuid": "private-staff-id",
        }
        materials = [
            {
                "job_uuid": "job-123",
                "name": "Bathroom rough-in",
                "item_description": "Move drain and water lines",
                "price": "3000",
                "cost": "1000",
            },
            {
                "job_uuid": "different-job",
                "name": "Do not copy this",
            },
        ]

        extracted = extract_servicem8_work_object(payload, job_materials=materials)
        self.assertEqual("servicem8", extracted["source_platform"])
        self.assertEqual("job-123", extracted["source_object_id"])
        self.assertEqual("Quote", extracted["source_status"])
        self.assertEqual("100 Queen St, Ottawa, ON K1P 1J9", extracted["address"])
        self.assertIn("Move basement drain", extracted["scope_text"])
        self.assertIn("Bathroom rough-in", extracted["scope_text"])
        self.assertIn("Move drain and water lines", extracted["scope_text"])
        self.assertNotIn("Do not copy this", extracted["scope_text"])
        self.assertEqual(1, extracted["job_material_count"])

        serialized = repr(extracted)
        self.assertNotIn("private-client-id", serialized)
        self.assertNotIn("Private billing address", serialized)
        self.assertNotIn("private-staff-id", serialized)
        self.assertNotIn("9000", serialized)
        self.assertNotIn("3000", serialized)
        self.assertNotIn("1000", serialized)

    def test_reconstructs_address_from_geo_fields(self):
        extracted = extract_servicem8_work_object(
            {
                "uuid": "job-geo",
                "status": "Work Order",
                "job_address": "",
                "job_description": "Rear deck replacement",
                "geo_number": "453",
                "geo_street": "W 12TH AV",
                "geo_city": "Vancouver",
                "geo_state": "BC",
                "geo_postcode": "V5Y 1T2",
                "geo_country": "CA",
            }
        )
        self.assertEqual("453 W 12TH AV, Vancouver, BC, V5Y 1T2 CA", extracted["address"])

    def test_missing_scope_is_rejected(self):
        with self.assertRaisesRegex(ServiceM8AdapterError, "job_description or scope-relevant"):
            extract_servicem8_work_object(
                {
                    "uuid": "job-empty",
                    "status": "Quote",
                    "job_address": "100 Queen St, Ottawa, ON",
                }
            )

    def test_unknown_job_status_is_rejected(self):
        with self.assertRaisesRegex(ServiceM8AdapterError, "Unsupported"):
            extract_servicem8_work_object(
                {
                    "uuid": "job-bad-status",
                    "status": "ArchivedCustomState",
                    "job_address": "100 Queen St, Ottawa, ON",
                    "job_description": "Window replacement",
                }
            )

    def test_project_family_must_be_explicit(self):
        extracted = {
            "source_platform": "servicem8",
            "source_object_id": "job-1",
            "source_status": "Quote",
            "address": "100 Queen St, Ottawa, ON",
        }
        with self.assertRaisesRegex(ServiceM8AdapterError, "project.family"):
            build_preflight_facts(extracted, jurisdiction="ottawa_on", project={})

    def test_builds_existing_preflight_contract(self):
        extracted = {
            "source_platform": "servicem8",
            "source_object_id": "job-1",
            "source_status": "Quote",
            "address": "100 Queen St, Ottawa, ON",
        }
        facts = build_preflight_facts(
            extracted,
            jurisdiction="ottawa_on",
            project={"family": "addition", "floor_area_increase": True},
            resolve_address=False,
            client_tag="servicem8-synthetic",
        )
        self.assertEqual("ottawa_on", facts["jurisdiction"])
        self.assertEqual("servicem8_adapter", facts["context"]["_transport"])
        self.assertEqual("Quote", facts["context"]["source_status"])
        self.assertFalse(facts["resolve_address"])

    def test_routing_summary_is_proposed_metadata_only(self):
        summary = build_servicem8_routing_summary(
            {
                "determination": "REQUIRED",
                "confidence": "HIGH",
                "requirements": [
                    {
                        "rule_version": "2026-08-26.1",
                        "evidence": [{"url": "https://example.gov/rule"}],
                    }
                ],
            }
        )
        self.assertEqual("REQUIRED", summary["projectpermit_preflight"])
        self.assertEqual("HIGH", summary["projectpermit_confidence"])
        self.assertEqual("2026-08-26.1", summary["projectpermit_rule_version"])
        self.assertEqual("https://example.gov/rule", summary["projectpermit_evidence_url"])


if __name__ == "__main__":
    unittest.main()
