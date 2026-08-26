import unittest

from projectpermit.preflight_service import run_preflight


class SharedPreflightServiceTest(unittest.TestCase):
    def test_gatineau_address_context_is_shared_into_rule_evaluation(self):
        calls = []

        def fake_fetch(url):
            calls.append(url)
            return {
                "candidates": [
                    {
                        "address": "25 RUE LAURIER",
                        "score": 97,
                        "location": {"x": -75.72, "y": 45.43},
                    }
                ]
            }

        result = run_preflight(
            {
                "jurisdiction": "gatineau_qc",
                "address": "25 rue Laurier, Gatineau, QC",
                "resolve_address": True,
                "project": {
                    "family": "interior_renovation",
                    "estimated_cost_cad": 10000,
                    "structural_change": False,
                },
                "property": {"heritage": False, "piia": False},
            },
            fetcher=fake_fetch,
        )

        self.assertEqual("LIKELY_NOT_REQUIRED", result["determination"])
        self.assertEqual("gatineau_qc", result["address_context"]["jurisdiction"])
        self.assertEqual(97, result["address_context"]["address_resolution"]["score"])
        self.assertEqual(1, len(calls))

    def test_missing_address_fails_before_rule_evaluation(self):
        with self.assertRaisesRegex(ValueError, "address is required"):
            run_preflight(
                {
                    "jurisdiction": "ottawa_on",
                    "resolve_address": True,
                    "project": {"family": "window_door", "action": "replace_same_size"},
                },
                fetcher=lambda _: {},
            )

    def test_unsupported_address_resolver_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "address resolver not available"):
            run_preflight(
                {
                    "jurisdiction": "unknown_city",
                    "address": "1 Main St",
                    "resolve_address": True,
                    "project": {"family": "window_door", "action": "replace_same_size"},
                },
                fetcher=lambda _: {},
            )


if __name__ == "__main__":
    unittest.main()
