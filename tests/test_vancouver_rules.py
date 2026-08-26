import unittest

from projectpermit import evaluate_project


class VancouverRulesTest(unittest.TestCase):
    def test_addition_required(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "addition", "floor_area_increase": True},
        })
        self.assertEqual("REQUIRED", result["determination"])

    def test_cosmetic_interior_no_permit(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "interior_renovation", "action": "painting"},
        })
        self.assertEqual("LIKELY_NOT_REQUIRED", result["determination"])
        self.assertEqual("VAN-INT-001", result["requirements"][0]["rule_id"])

    def test_secondary_suite_requires_building_and_development(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "dwelling_change", "action": "add_secondary_suite"},
        })
        self.assertEqual("REQUIRED", result["determination"])
        types = {item["type"] for item in result["requirements"]}
        self.assertIn("building_permit", types)
        self.assertIn("development_permit", types)

    def test_same_size_window_stays_conservative(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "window_door", "action": "replace_same_size"},
        })
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", result["determination"])

    def test_shed_required(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "accessory_structure", "accessory_structure_kind": "shed"},
        })
        self.assertEqual("REQUIRED", result["determination"])

    def test_narrow_outdoor_patio_exception(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {
                "family": "deck_porch",
                "action": "outdoor_patio",
                "deck_height_mm": 600,
                "deck_area_m2": 25,
                "deck_attached": False,
            },
        })
        self.assertEqual("LIKELY_NOT_REQUIRED", result["determination"])
        self.assertEqual("VAN-PATIO-002", result["requirements"][0]["rule_id"])

    def test_normal_deck_required(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {
                "family": "deck_porch",
                "action": "build_deck",
                "deck_height_mm": 300,
                "deck_area_m2": 8,
                "deck_attached": True,
            },
        })
        self.assertEqual("REQUIRED", result["determination"])

    def test_roofing_no_permit_without_structural_scope(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "interior_renovation", "roof_replacement": True},
        })
        self.assertEqual("LIKELY_NOT_REQUIRED", result["determination"])

    def test_every_requirement_has_city_evidence(self):
        result = evaluate_project({
            "jurisdiction": "vancouver_bc",
            "project": {"family": "basement", "action": "finish_basement"},
        })
        for requirement in result["requirements"]:
            self.assertTrue(requirement["evidence"])
            self.assertTrue(requirement["evidence"][0]["url"].startswith("https://vancouver.ca/"))


if __name__ == "__main__":
    unittest.main()
