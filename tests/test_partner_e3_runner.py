from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_partner_e3_cases.py"
spec = importlib.util.spec_from_file_location("run_partner_e3_cases", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def row(**overrides: str) -> dict[str, str]:
    base = {
        "case_id": "E3-001",
        "partner": "Pilot",
        "source_platform": "manual",
        "sample_window_start": "2026-07-01",
        "sample_window_end": "2026-07-31",
        "sampling_method": "chronological",
        "jurisdiction": "gatineau_qc",
        "project_family": "window_door",
        "scope_summary": "Replace same-size exterior window in existing opening",
        "project_facts_json": json.dumps(
            {
                "family": "window_door",
                "action": "replace_same_size",
                "estimated_cost_cad": 1800,
                "structural_change": False,
            }
        ),
        # These tests exercise agreement/disagreement accounting, not unresolved
        # property-overlay behavior. Make the no-overlay state explicit so the
        # expected exemption is based on resolved facts rather than omission.
        "property_facts_json": json.dumps({"piia": False, "heritage": False}),
        "usable_case": "yes",
        "address_resolution_needed": "no",
        "historical_determination": "LIKELY_NOT_REQUIRED",
        "historical_decision_source": "municipal_research",
        "material_disagreement": "",
    }
    base.update(overrides)
    return base


class PartnerE3RunnerTest(unittest.TestCase):
    def test_engine_result_and_agreement_are_written(self):
        result = module.evaluate_rows([row()])[0]
        self.assertEqual("LIKELY_NOT_REQUIRED", result["projectpermit_determination"])
        self.assertEqual("yes", result["agreement"])
        self.assertEqual("no", result["material_disagreement"])
        self.assertEqual("no", result["false_likely_not_required"])
        self.assertEqual("no", result["unsupported_jurisdiction"])
        self.assertEqual("no", result["unsupported_family"])

    def test_disagreement_requires_fresh_human_materiality_review(self):
        result = module.evaluate_rows(
            [row(historical_determination="REQUIRED", material_disagreement="no")]
        )[0]
        self.assertEqual("LIKELY_NOT_REQUIRED", result["projectpermit_determination"])
        self.assertEqual("no", result["agreement"])
        self.assertEqual("", result["material_disagreement"])
        self.assertEqual("yes", result["false_likely_not_required"])

    def test_out_of_scope_is_kept_as_negative_evidence(self):
        result = module.evaluate_rows(
            [
                row(
                    jurisdiction="unknown_city",
                    historical_determination="REQUIRED",
                )
            ]
        )[0]
        self.assertEqual("OUT_OF_SCOPE", result["projectpermit_determination"])
        self.assertEqual("no", result["agreement"])
        self.assertEqual("", result["material_disagreement"])
        self.assertEqual("yes", result["unsupported_jurisdiction"])
        self.assertEqual("no", result["false_likely_not_required"])

    def test_address_aware_case_requires_deidentified_property_facts(self):
        with self.assertRaisesRegex(ValueError, "property_facts_json is required"):
            module.evaluate_rows([row(address_resolution_needed="yes", property_facts_json="")])

    def test_project_family_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "must match project_family"):
            module.evaluate_rows([row(project_family="deck_porch")])

    def test_unusable_case_is_left_unevaluated(self):
        original = row(usable_case="no", project_facts_json="")
        result = module.evaluate_rows([original])[0]
        self.assertNotIn("projectpermit_determination", result)


if __name__ == "__main__":
    unittest.main()
