from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "market_research" / "operator_rescue_metrics_20260828.py"
SPEC = importlib.util.spec_from_file_location("operator_rescue_metrics_20260828", MODULE_PATH)
assert SPEC and SPEC.loader
metrics = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = metrics
SPEC.loader.exec_module(metrics)


AGGREGATE_FIELDS = [
    "operator",
    "complete_month",
    "current_family",
    "unique_requests",
    "within_supported_jurisdictions",
    "candidate_preflight_requests",
    "known_required",
    "known_not_required",
    "unresolved",
    "not_checked",
    "unknown_permit_state",
    "required_followup_or_research",
    "material_effect_known_count",
    "partner_deliveries",
    "delivery_multiplier",
    "integration_topology",
    "notes",
]

SAMPLE_FIELDS = [
    "case_id",
    "chronological_index",
    "submitted_at",
    "current_family",
    "jurisdiction",
    "raw_scope",
    "facts_sufficient_without_followup",
    "material_workflow_effect",
]


class OperatorRescueMetricsTests(unittest.TestCase):
    def write_csv(self, path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_aggregate_and_sample(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            aggregate_path = root / "aggregate.csv"
            sample_path = root / "sample.csv"
            self.write_csv(
                aggregate_path,
                AGGREGATE_FIELDS,
                [
                    {
                        "operator": "Example",
                        "complete_month": "2026-07",
                        "current_family": "kitchen_bath_plumbing",
                        "unique_requests": 400,
                        "within_supported_jurisdictions": 350,
                        "candidate_preflight_requests": 300,
                        "known_required": 80,
                        "known_not_required": 70,
                        "unresolved": 100,
                        "not_checked": 30,
                        "unknown_permit_state": 20,
                        "required_followup_or_research": 90,
                        "material_effect_known_count": 40,
                        "partner_deliveries": 800,
                    },
                    {
                        "operator": "Example",
                        "complete_month": "2026-07",
                        "current_family": "window_door",
                        "unique_requests": 300,
                        "within_supported_jurisdictions": 260,
                        "candidate_preflight_requests": 220,
                        "known_required": 50,
                        "known_not_required": 60,
                        "unresolved": 70,
                        "not_checked": 20,
                        "unknown_permit_state": 20,
                        "required_followup_or_research": 60,
                        "material_effect_known_count": 35,
                        "partner_deliveries": 500,
                    },
                ],
            )
            self.write_csv(
                sample_path,
                SAMPLE_FIELDS,
                [
                    {
                        "case_id": "a",
                        "chronological_index": 1,
                        "current_family": "kitchen_bath_plumbing",
                        "jurisdiction": "gatineau",
                        "facts_sufficient_without_followup": "yes",
                        "material_workflow_effect": "true",
                    },
                    {
                        "case_id": "b",
                        "chronological_index": 2,
                        "current_family": "window_door",
                        "jurisdiction": "ottawa",
                        "facts_sufficient_without_followup": "no",
                        "material_workflow_effect": "false",
                    },
                ],
            )

            aggregate = metrics.load_monthly_aggregate(aggregate_path)
            sample = metrics.load_case_sample(sample_path)
            summary = metrics.build_summary(aggregate, sample)

            self.assertEqual(aggregate.unique_requests, 700)
            self.assertEqual(aggregate.candidate_preflights, 520)
            self.assertEqual(aggregate.unresolved, 170)
            self.assertAlmostEqual(summary["aggregate"]["unresolved_share_of_candidates"], 170 / 520)
            self.assertAlmostEqual(summary["sample"]["fact_sufficiency_rate"], 0.5)
            self.assertAlmostEqual(summary["sample"]["material_hit_rate"], 0.5)
            self.assertTrue(summary["gates"]["candidate_preflight_500_monthly"])

    def test_rejects_candidate_count_above_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aggregate.csv"
            self.write_csv(
                path,
                AGGREGATE_FIELDS,
                [{
                    "operator": "Example",
                    "complete_month": "2026-07",
                    "current_family": "window_door",
                    "unique_requests": 10,
                    "within_supported_jurisdictions": 8,
                    "candidate_preflight_requests": 9,
                }],
            )
            with self.assertRaisesRegex(ValueError, "candidate_preflight_requests exceeds"):
                metrics.load_monthly_aggregate(path)

    def test_rejects_partner_delivery_duplicates_as_candidate_volume(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aggregate.csv"
            self.write_csv(
                path,
                AGGREGATE_FIELDS,
                [{
                    "operator": "Example",
                    "complete_month": "2026-07",
                    "current_family": "window_door",
                    "unique_requests": 100,
                    "within_supported_jurisdictions": 80,
                    "candidate_preflight_requests": 60,
                    "partner_deliveries": 500,
                }],
            )
            aggregate = metrics.load_monthly_aggregate(path)
            summary = metrics.build_summary(aggregate, {"sample_size": 0, "fact_sufficient_count": 0, "fact_sufficiency_rate": None, "material_hit_count": 0, "material_hit_rate": None})
            self.assertEqual(aggregate.partner_deliveries, 500)
            self.assertEqual(aggregate.candidate_preflights, 60)
            self.assertFalse(summary["gates"]["candidate_preflight_500_monthly"])

    def test_rejects_non_chronological_sample(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            self.write_csv(
                path,
                SAMPLE_FIELDS,
                [
                    {"case_id": "b", "chronological_index": 2, "current_family": "window_door", "jurisdiction": "ottawa"},
                    {"case_id": "a", "chronological_index": 1, "current_family": "window_door", "jurisdiction": "ottawa"},
                ],
            )
            with self.assertRaisesRegex(ValueError, "unique and ascending"):
                metrics.load_case_sample(path)


if __name__ == "__main__":
    unittest.main()
