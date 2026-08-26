import unittest

from projectpermit import evaluate_project


class QuebecExpansionRulesTest(unittest.TestCase):
    def test_laval_same_size_window_no_permit(self):
        result = evaluate_project({
            "jurisdiction": "laval_qc",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {"piia": False},
        })
        self.assertEqual("LIKELY_NOT_REQUIRED", result["determination"])
        self.assertEqual("LAV-WIN-002", result["requirements"][0]["rule_id"])

    def test_laval_resized_window_requires_permit(self):
        result = evaluate_project({
            "jurisdiction": "laval_qc",
            "project": {"family": "window_door", "action": "enlarge_existing_opening"},
        })
        self.assertEqual("REQUIRED", result["determination"])

    def test_laval_shed_threshold(self):
        small = evaluate_project({
            "jurisdiction": "laval_qc",
            "project": {
                "family": "accessory_structure",
                "accessory_structure_kind": "shed",
                "accessory_area_m2": 17.9,
            },
            "property": {"piia": False},
        })
        large = evaluate_project({
            "jurisdiction": "laval_qc",
            "project": {
                "family": "accessory_structure",
                "accessory_structure_kind": "shed",
                "accessory_area_m2": 18,
            },
        })
        self.assertEqual("LIKELY_NOT_REQUIRED", small["determination"])
        self.assertEqual("REQUIRED", large["determination"])

    def test_laval_basement_requires_room_structure_facts(self):
        result = evaluate_project({
            "jurisdiction": "laval_qc",
            "project": {"family": "basement", "action": "finish_basement"},
        })
        self.assertEqual("MUNICIPAL_CONFIRMATION_REQUIRED", result["determination"])

    def test_longueuil_window_modification_required(self):
        result = evaluate_project({
            "jurisdiction": "longueuil_qc",
            "project": {"family": "window_door", "action": "enlarge_existing_opening"},
        })
        self.assertEqual("REQUIRED", result["determination"])
        self.assertEqual("LON-WIN-001", result["requirements"][0]["rule_id"])

    def test_longueuil_interior_renovation_stays_conservative(self):
        result = evaluate_project({
            "jurisdiction": "longueuil_qc",
            "project": {"family": "interior_renovation", "action": "renovate"},
        })
        self.assertEqual("LIKELY_REQUIRED", result["determination"])

    def test_longueuil_piia_elevates_review(self):
        result = evaluate_project({
            "jurisdiction": "longueuil_qc",
            "project": {"family": "interior_renovation", "action": "renovate"},
            "property": {"piia": True},
        })
        self.assertEqual("LIKELY_REQUIRED", result["determination"])
        self.assertTrue(any(r["type"] == "planning_or_design_review" for r in result["requirements"]))

    def test_every_new_rule_has_official_evidence(self):
        samples = [
            {"jurisdiction": "laval_qc", "project": {"family": "addition", "floor_area_increase": True}},
            {"jurisdiction": "longueuil_qc", "project": {"family": "deck_porch", "action": "repair"}},
        ]
        for sample in samples:
            result = evaluate_project(sample)
            for requirement in result["requirements"]:
                self.assertTrue(requirement["evidence"])
                self.assertTrue(requirement["evidence"][0]["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
