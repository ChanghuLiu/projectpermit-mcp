import json
import unittest
from pathlib import Path

from projectpermit import evaluate_project


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "public_permit_positive_vancouver.json"


class VancouverPublicPermitPositiveBacktest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = cls.payload["cases"]

    def test_fixture_is_explicitly_not_market_e3(self):
        self.assertIn("not market-validation E3", self.payload["purpose"])
        self.assertGreaterEqual(len(self.cases), 10)

    def test_known_permit_positive_cases_never_return_likely_not_required(self):
        false_negatives = []
        for case in self.cases:
            result = evaluate_project(case["facts"])
            if result["determination"] == "LIKELY_NOT_REQUIRED":
                false_negatives.append(
                    {
                        "case_id": case["case_id"],
                        "permit_number": case["permit_number"],
                        "determination": result["determination"],
                    }
                )

        self.assertEqual([], false_negatives)

    def test_current_structured_mapping_resolves_most_cases_as_required(self):
        determinations = [evaluate_project(case["facts"])["determination"] for case in self.cases]
        required_count = sum(value == "REQUIRED" for value in determinations)

        # Eight cases have explicit structured triggers (walls, suite/addition,
        # garage or deck). The two intentionally sparse public descriptions are
        # allowed to remain OUT_OF_SCOPE/confirmation rather than being guessed.
        self.assertGreaterEqual(required_count, 8)

    def test_sparse_public_descriptions_fail_safe(self):
        sparse_ids = {"van-public-009", "van-public-010"}
        for case in self.cases:
            if case["case_id"] not in sparse_ids:
                continue
            result = evaluate_project(case["facts"])
            self.assertNotEqual("LIKELY_NOT_REQUIRED", result["determination"])


if __name__ == "__main__":
    unittest.main()
