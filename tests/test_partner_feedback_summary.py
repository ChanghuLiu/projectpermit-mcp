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
    def test_opinion_only_reply_cannot_create_volume_or_price_evidence(self):
        rows = [
            {
                "company": "Opinion Only",
                "contact_status": "replied",
                "response_class": "A",
                "candidate_preflights_per_month": "50000",
                "pilot_calls": "25",
                "observed_external_calls": "25",
                "integration_status": "testing",
                "price_reaction_025": "acceptable",
                "price_reaction_050": "",
                "monthly_call_band": "10,000+/month",
                "historical_samples_provided": "20",
                "evidence_level": "E1",
            }
        ]

        summary = module.summarize(rows)
        self.assertEqual(1, summary["conversations"])
        self.assertEqual(1, summary["positive_A_or_B"])
        self.assertEqual(0, summary["bounded_workflow_claims_E2_plus"])
        self.assertEqual(0, summary["known_candidate_preflights_per_month"])
        self.assertEqual(0, summary["observed_external_calls"])
        self.assertEqual(0, summary["price_025_accepts"])
        self.assertFalse(summary["gates"]["one_2000_month_partner"])
        self.assertFalse(summary["gates"]["one_20_call_repeat"])
        self.assertFalse(summary["gates"]["price_acceptance_with_bounded_volume"])

    def test_bounded_and_observed_evidence_drive_the_right_gates(self):
        rows = [
            {
                "company": "Pilot A",
                "contact_status": "replied",
                "response_class": "A",
                "candidate_preflights_per_month": "2000",
                "pilot_calls": "25",
                "observed_external_calls": "25",
                "integration_status": "testing",
                "price_reaction_025": "acceptable",
                "price_reaction_050": "",
                "monthly_call_band": "2,000-10,000/month",
                "historical_samples_provided": "20",
                "evidence_level": "E4",
            },
            {
                "company": "Pilot B",
                "contact_status": "replied",
                "response_class": "B",
                "candidate_preflights_per_month": "unknown",
                "pilot_calls": "",
                "observed_external_calls": "",
                "integration_status": "",
                "price_reaction_025": "",
                "price_reaction_050": "too_high",
                "monthly_call_band": "",
                "historical_samples_provided": "",
                "evidence_level": "E2",
            },
        ]

        summary = module.summarize(rows)
        self.assertEqual(2, summary["conversations"])
        self.assertEqual(2, summary["bounded_workflow_claims_E2_plus"])
        self.assertEqual(1, summary["historical_benchmarks_E3_plus"])
        self.assertEqual(1, summary["observed_usage_partners_E4_plus"])
        self.assertEqual(25, summary["observed_external_calls"])
        self.assertEqual(2000, summary["known_candidate_preflights_per_month"])
        self.assertTrue(summary["gates"]["one_E3_historical_benchmark"])
        self.assertTrue(summary["gates"]["one_20_call_repeat"])
        self.assertTrue(summary["gates"]["one_2000_month_partner"])
        self.assertTrue(summary["gates"]["price_acceptance_with_bounded_volume"])
        self.assertFalse(summary["gates"]["credible_10000_month_path"])
        self.assertFalse(summary["gates"]["one_E5_economic_signal"])

    def test_e5_is_counted_as_economic_signal(self):
        rows = [{"company": "Paid", "evidence_level": "E5"}]
        summary = module.summarize(rows)
        self.assertEqual(1, summary["economic_signals_E5"])
        self.assertTrue(summary["gates"]["one_E5_economic_signal"])

    def test_empty_tracker_has_zero_evidence_and_no_passed_gates(self):
        summary = module.summarize([])
        self.assertEqual(0, summary["targets_recorded"])
        self.assertEqual(0, summary["conversations"])
        self.assertEqual(0, summary["known_candidate_preflights_per_month"])
        self.assertFalse(any(summary["gates"].values()))


if __name__ == "__main__":
    unittest.main()
