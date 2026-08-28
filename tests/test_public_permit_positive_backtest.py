import json
import unittest
from pathlib import Path

from projectpermit import evaluate_project


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIXTURES = {
    "vancouver": DATA_DIR / "public_permit_positive_vancouver.json",
    "mississauga": DATA_DIR / "public_permit_positive_mississauga.json",
    "toronto": DATA_DIR / "public_permit_positive_toronto.json",
}


class PublicPermitPositiveBacktest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payloads = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in FIXTURES.items()
        }

    def test_fixtures_are_explicitly_not_market_e3(self):
        minimum_cases = {"vancouver": 10, "mississauga": 6, "toronto": 20}
        for name, payload in self.payloads.items():
            with self.subTest(fixture=name):
                self.assertIn("not market-validation E3", payload["purpose"])
                self.assertGreaterEqual(len(payload["cases"]), minimum_cases[name])

    def test_known_permit_positive_cases_never_return_likely_not_required(self):
        false_negatives = []
        for fixture_name, payload in self.payloads.items():
            for case in payload["cases"]:
                result = evaluate_project(case["facts"])
                if result["determination"] == "LIKELY_NOT_REQUIRED":
                    false_negatives.append(
                        {
                            "fixture": fixture_name,
                            "case_id": case["case_id"],
                            "permit_number": case["permit_number"],
                            "determination": result["determination"],
                        }
                    )

        self.assertEqual([], false_negatives)

    def test_current_structured_mapping_resolves_expected_cases_as_required(self):
        expected_required_floor = {"vancouver": 8, "mississauga": 4, "toronto": 16}
        for name, payload in self.payloads.items():
            determinations = [
                evaluate_project(case["facts"])["determination"]
                for case in payload["cases"]
            ]
            required_count = sum(value == "REQUIRED" for value in determinations)
            with self.subTest(fixture=name):
                self.assertGreaterEqual(required_count, expected_required_floor[name])

    def test_toronto_direct_mappings_are_all_required(self):
        payload = self.payloads["toronto"]
        cases_by_id = {case["case_id"]: case for case in payload["cases"]}
        expected_ids = set(payload["direct_required_case_ids"])
        self.assertEqual(16, len(expected_ids))

        failures = []
        for case_id in sorted(expected_ids):
            case = cases_by_id[case_id]
            result = evaluate_project(case["facts"])
            if result["determination"] != "REQUIRED":
                failures.append(
                    {
                        "case_id": case_id,
                        "permit_number": case["permit_number"],
                        "determination": result["determination"],
                    }
                )
        self.assertEqual([], failures)

    def test_sparse_public_descriptions_fail_safe(self):
        sparse_ids = {
            "van-public-009",
            "van-public-010",
            "mis-public-005",
            "mis-public-006",
            "tor-public-003",
            "tor-public-012",
            "tor-public-013",
            "tor-public-020",
        }
        for payload in self.payloads.values():
            for case in payload["cases"]:
                if case["case_id"] not in sparse_ids:
                    continue
                result = evaluate_project(case["facts"])
                self.assertNotEqual("LIKELY_NOT_REQUIRED", result["determination"])

    def test_toronto_fixture_ids_and_groups_are_consistent(self):
        payload = self.payloads["toronto"]
        case_ids = [case["case_id"] for case in payload["cases"]]
        self.assertEqual(20, len(case_ids))
        self.assertEqual(20, len(set(case_ids)))

        direct = set(payload["direct_required_case_ids"])
        sparse = set(payload["sparse_fail_safe_case_ids"])
        self.assertFalse(direct & sparse)
        self.assertEqual(set(case_ids), direct | sparse)


if __name__ == "__main__":
    unittest.main()
