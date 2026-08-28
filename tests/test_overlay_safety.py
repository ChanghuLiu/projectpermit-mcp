import unittest

from projectpermit import evaluate_project
from projectpermit.preflight_service import run_preflight


class UnknownPropertyOverlaySafetyTest(unittest.TestCase):
    def test_gatineau_low_cost_exemption_requires_resolved_piia_and_heritage(self):
        facts = {
            "jurisdiction": "gatineau_qc",
            "project": {
                "family": "interior_renovation",
                "estimated_cost_cad": 10000,
                "structural_change": False,
                "modifies_walls": False,
            },
        }

        unknown = evaluate_project(facts)
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", unknown["determination"])
        self.assertEqual("UNRESOLVED_FOR_EXEMPTION", unknown["property_context_status"])
        self.assertEqual(["heritage", "piia"], unknown["required_property_facts"])
        self.assertIn(
            "GAT-OVERLAY-UNKNOWN-001",
            {req["rule_id"] for req in unknown["requirements"]},
        )

        resolved = evaluate_project(
            {**facts, "property": {"heritage": False, "piia": False}}
        )
        self.assertEqual("LIKELY_NOT_REQUIRED", resolved["determination"])
        self.assertNotIn("required_property_facts", resolved)

    def test_gatineau_address_geocode_does_not_turn_unknown_overlays_false(self):
        def fake_fetch(_url):
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
                    "modifies_walls": False,
                },
            },
            fetcher=fake_fetch,
        )

        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", result["determination"])
        self.assertEqual(["heritage", "piia"], result["required_property_facts"])
        self.assertIsNone(result["address_context"]["property"]["heritage"])
        self.assertIsNone(result["address_context"]["property"]["piia"])

    def test_ottawa_exemption_requires_resolved_heritage_status(self):
        facts = {
            "jurisdiction": "ottawa_on",
            "project": {
                "family": "deck_porch",
                "deck_height_mm": 500,
                "deck_area_m2": 9,
                "deck_attached": False,
                "principal_access": False,
            },
        }

        unknown = evaluate_project(facts)
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", unknown["determination"])
        self.assertEqual(["heritage"], unknown["required_property_facts"])
        self.assertIn(
            "OTT-HER-UNKNOWN-001",
            {req["rule_id"] for req in unknown["requirements"]},
        )

        resolved = evaluate_project({**facts, "property": {"heritage": False}})
        self.assertEqual("LIKELY_NOT_REQUIRED", resolved["determination"])

    def test_laval_piia_sensitive_shed_exemption_fails_safe_when_unknown(self):
        facts = {
            "jurisdiction": "laval_qc",
            "project": {
                "family": "accessory_structure",
                "accessory_structure_kind": "shed",
                "accessory_area_m2": 10,
            },
        }

        unknown = evaluate_project(facts)
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", unknown["determination"])
        self.assertEqual(["piia"], unknown["required_property_facts"])
        self.assertIn(
            "LAV-PIIA-UNKNOWN-001",
            {req["rule_id"] for req in unknown["requirements"]},
        )

        resolved = evaluate_project({**facts, "property": {"piia": False}})
        self.assertEqual("LIKELY_NOT_REQUIRED", resolved["determination"])

    def test_laval_rear_deck_exemption_fails_safe_when_piia_unknown(self):
        facts = {
            "jurisdiction": "laval_qc",
            "project": {
                "family": "deck_porch",
                "yard": "rear",
            },
        }
        result = evaluate_project(facts)
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", result["determination"])
        self.assertEqual(["piia"], result["required_property_facts"])

    def test_required_outcome_is_not_downgraded_by_missing_property_context(self):
        result = evaluate_project(
            {
                "jurisdiction": "gatineau_qc",
                "project": {
                    "family": "addition",
                    "floor_area_increase": True,
                },
            }
        )
        self.assertEqual("REQUIRED", result["determination"])
        self.assertNotIn("required_property_facts", result)


if __name__ == "__main__":
    unittest.main()
