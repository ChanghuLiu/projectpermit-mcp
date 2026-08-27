from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "summarize_partner_feedback.py"
spec = importlib.util.spec_from_file_location("summarize_partner_feedback", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class PartnerFeedbackSummaryTest(unittest.TestCase):
    def test_unknown_values_are_not_silently_counted_as_zero_evidence(self):
        rows = [
            {
                "company": "Pilot A",
                "contact_status": "replied",
                "response_class": "A",
                "candidate_preflights_per_month": "2000",
                "pilot_calls": "25",
                "integration_status": "testing",
                "price_reaction_025": "acceptable",
                "price_reaction_050": "",
                "monthly_call_band": "2,000-10,000/month",
            },
            {
                "company": "Pilot B",
                "contact_status": "replied",
                "response_class": "B",
                "candidate_preflights_per_month": "unknown",
                "pilot_calls": "",
                "integration_status": "",
                "price_reaction_025": "",
                "price_reaction_050": "too_high",
                "monthly_call_band": "",
            },
        ]

        summary = module.summarize(rows)
        self.assertEqual(2, summary["conversations"])
        self.assertEqual(2, summary["positive_A_or_B"])
        self.assertEqual(1, summary["integrations_testing_or_better"])
        self.assertEqual(25, summary["pilot_calls_recorded"])
        self.assertEqual(2000, summary["known_candidate_preflights_per_month"])
        self.assertTrue(summary["gates"]["one_20_call_repeat"])
        self.assertTrue(summary["gates"]["one_2000_month_partner"])
        self.assertTrue(summary["gates"]["price_acceptance"])
        self.assertFalse(summary["gates"]["credible_10000_month_path"])

    def test_empty_tracker_has_zero_evidence_and_no_passed_gates(self):
        summary = module.summarize([])
        self.assertEqual(0, summary["targets_recorded"])
        self.assertEqual(0, summary["conversations"])
        self.assertEqual(0, summary["known_candidate_preflights_per_month"])
        self.assertFalse(any(summary["gates"].values()))


if __name__ == "__main__":
    unittest.main()
