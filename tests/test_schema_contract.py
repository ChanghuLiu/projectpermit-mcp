import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from projectpermit import evaluate_project

ROOT = Path(__file__).resolve().parents[1]


class SchemaContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.req_schema = json.loads((ROOT / "schemas" / "request.schema.json").read_text())
        cls.res_schema = json.loads((ROOT / "schemas" / "response.schema.json").read_text())
        Draft202012Validator.check_schema(cls.req_schema)
        Draft202012Validator.check_schema(cls.res_schema)
        cls.samples = [
            {"jurisdiction": "ottawa_on", "project": {"family": "window_door", "action": "replace_same_size"}, "property": {"heritage": False}},
            {"jurisdiction": "ottawa_on", "project": {"family": "window_door", "action": "enlarge_existing_opening"}},
            {"jurisdiction": "ottawa_on", "project": {"family": "deck_porch", "deck_height_mm": 700, "deck_area_m2": 12, "deck_attached": True, "principal_access": False}},
            {"jurisdiction": "gatineau_qc", "project": {"family": "interior_renovation", "estimated_cost_cad": 10000, "structural_change": False}, "property": {"heritage": False, "piia": False}},
            {"jurisdiction": "gatineau_qc", "project": {"family": "addition", "floor_area_increase": True}},
            {"jurisdiction": "toronto_on", "project": {"family": "window_door", "action": "replace_same_size", "single_dwelling_house": True, "structural_change": False, "new_exit": False}},
            {"jurisdiction": "toronto_on", "project": {"family": "basement", "action": "finish_basement", "structural_change": False, "material_alteration": False, "dwelling_unit_change": False, "new_plumbing": False}},
            {"jurisdiction": "mississauga_on", "project": {"family": "window_door", "action": "replace_same_size"}},
            {"jurisdiction": "mississauga_on", "project": {"family": "deck_porch", "deck_height_mm": 605}},
        ]

    def test_sample_inputs_match_request_schema(self):
        validator = Draft202012Validator(self.req_schema)
        for sample in self.samples:
            self.assertEqual([], list(validator.iter_errors(sample)))

    def test_sample_outputs_match_response_schema(self):
        validator = Draft202012Validator(self.res_schema)
        for sample in self.samples:
            result = evaluate_project(sample)
            self.assertEqual([], list(validator.iter_errors(result)))

    def test_every_returned_requirement_has_official_evidence(self):
        for sample in self.samples:
            result = evaluate_project(sample)
            for req in result["requirements"]:
                self.assertTrue(req.get("evidence"))
                for ev in req["evidence"]:
                    self.assertTrue(ev.get("url"))
                    self.assertTrue(ev.get("authority"))


if __name__ == "__main__":
    unittest.main()
