import json
import unittest
from pathlib import Path

from projectpermit import evaluate_project
from projectpermit.jobber_adapter import (
    build_jobber_writeback,
    build_preflight_facts,
    extract_jobber_work_object,
)


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "jobber_synthetic_integration_benchmark.json"
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


class JobberSyntheticIntegrationBenchmarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = cls.payload["cases"]

    def test_benchmark_is_explicitly_not_market_e3(self):
        self.assertIn("not E3 market validation", self.payload["purpose"])
        self.assertEqual(20, len(self.cases))

    def test_all_current_project_families_are_exercised(self):
        families = {case["project"]["family"] for case in self.cases}
        self.assertEqual(EXPECTED_FAMILIES, families)

    def test_end_to_end_adapter_engine_writeback_matches_expected(self):
        mismatches = []

        for case in self.cases:
            extracted = extract_jobber_work_object(case["payload"])
            self.assertEqual("jobber", extracted["source_platform"])
            self.assertTrue(extracted["address"])
            self.assertTrue(extracted["scope_text"])

            # Deliberately do not resolve the synthetic addresses against live
            # municipal GIS in CI. Address extraction is still exercised above.
            facts = build_preflight_facts(
                extracted,
                jurisdiction=case["jurisdiction"],
                project=case["project"],
                resolve_address=False,
                client_tag="jobber-synthetic-benchmark",
            )
            result = evaluate_project(facts)
            writeback = build_jobber_writeback(result)

            if result["determination"] != case["expected_determination"]:
                mismatches.append(
                    {
                        "id": case["id"],
                        "expected": case["expected_determination"],
                        "actual": result["determination"],
                    }
                )

            self.assertEqual(result["determination"], writeback["projectpermit_preflight"])
            self.assertTrue(writeback["projectpermit_rule_version"])
            self.assertTrue(writeback["projectpermit_evidence_url"])
            self.assertEqual("jobber_adapter", facts["context"]["_transport"])
            self.assertEqual("jobber-synthetic-benchmark", facts["context"]["client_tag"])

        self.assertEqual([], mismatches)

    def test_fixture_contains_no_real_customer_contact_or_billing_fields(self):
        serialized = json.dumps(self.payload).lower()
        forbidden = [
            '"client"',
            '"email"',
            '"phone"',
            '"total"',
            '"unitprice"',
            '"invoice"',
            '"payment"',
        ]
        for token in forbidden:
            self.assertNotIn(token, serialized)


if __name__ == "__main__":
    unittest.main()
