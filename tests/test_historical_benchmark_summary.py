from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "summarize_historical_benchmark.py"
spec = importlib.util.spec_from_file_location("summarize_historical_benchmark", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def make_row(case_id: str, **overrides: str) -> dict[str, str]:
    row = {
        "case_id": case_id,
        "partner": "Pilot A",
        "source_platform": "jobber",
        "sample_window_start": "2026-07-01",
        "sample_window_end": "2026-07-31",
        "sampling_method": "chronological",
        "jurisdiction": "ottawa_on",
        "project_family": "deck_porch",
        "scope_summary": "Build a residential rear deck 700 mm above grade",
        "project_facts_json": json.dumps({"family": "deck_porch", "deck_height_mm": 700}),
        "property_facts_json": "{}",
        "usable_case": "yes",
        "address_resolution_needed": "no",
        "historical_determination": "REQUIRED",
        "historical_decision_source": "municipal_research",
        "manual_research_minutes": "12",
        "workflow_changed": "yes",
        "projectpermit_determination": "REQUIRED",
        "projectpermit_confidence": "HIGH",
        "agreement": "yes",
        "material_disagreement": "no",
        "false_likely_not_required": "no",
        "confirm_appropriate": "",
        "unsupported_family": "no",
        "unsupported_jurisdiction": "no",
        "notes": "",
    }
    row.update(overrides)
    return row


class HistoricalBenchmarkSummaryTest(unittest.TestCase):
    def test_five_complete_chronological_cases_qualify_as_e3(self):
        summary = module.summarize([make_row(f"A-{index}") for index in range(5)])
        benchmark = summary["partner_benchmarks"][0]
        self.assertTrue(benchmark["e3_qualified"])
        self.assertEqual(5, benchmark["usable_cases"])
        self.assertEqual(1.0, benchmark["agreement_rate"])
        self.assertEqual(1, summary["qualified_partner_benchmarks"])

    def test_four_cases_do_not_reach_e3_minimum(self):
        summary = module.summarize([make_row(f"A-{index}") for index in range(4)])
        self.assertFalse(summary["partner_benchmarks"][0]["e3_qualified"])

    def test_handpicked_sample_is_rejected(self):
        rows = [make_row(f"A-{index}", sampling_method="hand-picked") for index in range(5)]
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertFalse(benchmark["e3_qualified"])
        self.assertIn("biased_sampling_method", benchmark["invalid_cases"][0]["errors"])

    def test_missing_structured_project_facts_is_rejected(self):
        rows = [make_row(f"A-{index}") for index in range(5)]
        rows[2]["project_facts_json"] = ""
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertFalse(benchmark["e3_qualified"])
        self.assertIn("invalid_or_missing:project_facts_json", benchmark["invalid_cases"][0]["errors"])

    def test_address_aware_case_requires_deidentified_property_facts(self):
        rows = [make_row(f"A-{index}") for index in range(5)]
        rows[1]["address_resolution_needed"] = "yes"
        rows[1]["property_facts_json"] = ""
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertFalse(benchmark["e3_qualified"])
        self.assertIn("address_aware_case_missing:property_facts_json", benchmark["invalid_cases"][0]["errors"])

    def test_false_likely_not_required_is_counted_from_determinations(self):
        rows = [make_row(f"A-{index}") for index in range(5)]
        rows[4]["projectpermit_determination"] = "LIKELY_NOT_REQUIRED"
        rows[4]["agreement"] = "no"
        rows[4]["material_disagreement"] = "yes"
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertTrue(benchmark["e3_qualified"])
        self.assertEqual(1, benchmark["false_likely_not_required"])
        self.assertEqual(1, benchmark["material_disagreements"])
        self.assertEqual(0.8, benchmark["agreement_rate"])

    def test_out_of_scope_case_remains_in_representative_sample(self):
        rows = [make_row(f"A-{index}") for index in range(5)]
        rows[3]["projectpermit_determination"] = "OUT_OF_SCOPE"
        rows[3]["agreement"] = "no"
        rows[3]["material_disagreement"] = "yes"
        rows[3]["unsupported_family"] = "yes"
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertTrue(benchmark["e3_qualified"])
        self.assertEqual(1, benchmark["out_of_scope_outputs"])
        self.assertEqual(1, benchmark["material_disagreements"])
        self.assertEqual(0.8, benchmark["agreement_rate"])

    def test_duplicate_case_ids_prevent_qualification(self):
        rows = [make_row(f"A-{index}") for index in range(5)]
        rows[4]["case_id"] = "A-0"
        summary = module.summarize(rows)
        benchmark = summary["partner_benchmarks"][0]
        self.assertFalse(benchmark["e3_qualified"])
        self.assertEqual(["A-0"], benchmark["duplicate_case_ids"])


if __name__ == "__main__":
    unittest.main()
