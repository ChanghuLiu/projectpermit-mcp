import json
import unittest
from pathlib import Path

from projectpermit import evaluate_project
from projectpermit.servicem8_adapter import (
    build_preflight_facts,
    build_servicem8_routing_summary,
    extract_servicem8_work_object,
)


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "servicem8_synthetic_integration_benchmark.json"
EXPECTED_FAMILIES = {
    "window_door",
    "interior_renovation",
    "basement",
    "dwelling_change",
    "deck_porch",
    "accessory_structure",
    "addition",
    "kitchen_bath_plumbing",
}


class ServiceM8SyntheticIntegrationBenchmarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = cls.payload["cases"]

    def test_benchmark_is_explicitly_not_market_e3(self):
        self.assertIn("not E3 market validation", self.payload["purpose"])
        self.assertEqual(12, len(self.cases))

    def test_all_current_project_families_are_exercised(self):
        families = {case["project"]["family"] for case in self.cases}
        self.assertEqual(EXPECTED_FAMILIES, families)

    def test_end_to_end_adapter_engine_routing_matches_expected(self):
        mismatches = []

        for case in self.cases:
            extracted = extract_servicem8_work_object(
                case["payload"],
                job_materials=case.get("materials"),
            )
            self.assertEqual("servicem8", extracted["source_platform"])
            self.assertTrue(extracted["address"])
            self.assertTrue(extracted["scope_text"])

            facts = build_preflight_facts(
                extracted,
                jurisdiction=case["jurisdiction"],
                project=case["project"],
                resolve_address=False,
                client_tag="servicem8-synthetic-benchmark",
            )
            result = evaluate_project(facts)
            routing = build_servicem8_routing_summary(result)

            if result["determination"] != case["expected_determination"]:
                mismatches.append(
                    {
                        "id": case["id"],
                        "expected": case["expected_determination"],
                        "actual": result["determination"],
                    }
                )

            self.assertEqual(result["determination"], routing["projectpermit_preflight"])
            self.assertTrue(routing["projectpermit_rule_version"])
            self.assertTrue(routing["projectpermit_evidence_url"])
            self.assertEqual("servicem8_adapter", facts["context"]["_transport"])

        self.assertEqual([], mismatches)

    def test_fixture_contains_no_customer_contact_or_billing_fields(self):
        serialized = json.dumps(self.payload).lower()
        for forbidden in (
            '"company_uuid"',
            '"billing_address"',
            '"email"',
            '"phone"',
            '"payment_',
            '"price"',
            '"cost"',
        ):
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
