from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "market_research" / "operator_rescue_metrics.py"
_spec = importlib.util.spec_from_file_location("operator_rescue_metrics", SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
metrics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(metrics)


MONTHLY_FIELDS = [
    "operator",
    "complete_month",
    "current_family",
    "unique_requests",
    "candidate_preflight_requests",
    "within_supported_jurisdictions",
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
    "sample_id",
    "source_operator",
    "source_funnel",
    "received_date",
    "municipality",
    "current_family",
    "within_supported_jurisdiction",
    "candidate_preflight",
    "address_available",
    "structured_service_category",
    "structured_scope_fields_present",
    "sanitized_project_description",
    "permit_state_at_intake",
    "existing_human_action",
    "historical_permit_outcome",
    "historical_outcome_source",
    "partner_deliveries_for_request",
    "fact_sufficiency_class",
    "missing_decision_facts",
    "property_lookup_required",
    "normalized_project_facts_json",
    "projectpermit_determination",
    "projectpermit_confidence",
    "projectpermit_rule_ids",
    "projectpermit_rule_version",
    "projectpermit_source_verified_at",
    "address_context_changed_outcome",
    "agreement_with_historical",
    "disagreement_material",
    "safety_direction",
    "material_effect_class",
    "material_effect_type",
    "operator_override",
    "notes",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class OperatorRescueMetricsTests(unittest.TestCase):
    def test_exact_500_candidate_gate_and_sample_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            monthly = root / "monthly.csv"
            sample = root / "sample.csv"
            write_csv(
                monthly,
                MONTHLY_FIELDS,
                [
                    {
                        "operator": "Operator A",
                        "complete_month": "2026-07",
                        "current_family": "kitchen_bath_plumbing",
                        "unique_requests": 600,
                        "candidate_preflight_requests": 500,
                        "within_supported_jurisdictions": 550,
                        "known_required": 100,
                        "known_not_required": 150,
                        "unresolved": 200,
                        "not_checked": 100,
                        "unknown_permit_state": 50,
                        "required_followup_or_research": 120,
                        "material_effect_known_count": 80,
                        "partner_deliveries": 1200,
                        "delivery_multiplier": 2.0,
                        "integration_topology": "CENTRAL_WITH_SITE_MAPPING",
                    }
                ],
            )
            write_csv(
                sample,
                SAMPLE_FIELDS,
                [
                    {
                        "sample_id": "A-1",
                        "current_family": "kitchen_bath_plumbing",
                        "within_supported_jurisdiction": "YES",
                        "candidate_preflight": "YES",
                        "permit_state_at_intake": "UNRESOLVED",
                        "fact_sufficiency_class": "DIRECT_STRUCTURED",
                        "material_effect_class": "MATERIAL_EFFECT_CONFIRMED",
                    },
                    {
                        "sample_id": "A-2",
                        "current_family": "kitchen_bath_plumbing",
                        "within_supported_jurisdiction": "YES",
                        "candidate_preflight": "YES",
                        "permit_state_at_intake": "UNRESOLVED",
                        "fact_sufficiency_class": "TEXT_DERIVABLE",
                        "material_effect_class": "NO_MATERIAL_EFFECT",
                    },
                    {
                        "sample_id": "A-3",
                        "current_family": "kitchen_bath_plumbing",
                        "within_supported_jurisdiction": "YES",
                        "candidate_preflight": "YES",
                        "permit_state_at_intake": "KNOWN_REQUIRED",
                        "fact_sufficiency_class": "FOLLOWUP_REQUIRED",
                        "material_effect_class": "UNKNOWN",
                    },
                    {
                        "sample_id": "A-4",
                        "current_family": "kitchen_bath_plumbing",
                        "within_supported_jurisdiction": "NO",
                        "candidate_preflight": "NO",
                        "permit_state_at_intake": "UNKNOWN",
                        "fact_sufficiency_class": "INSUFFICIENT_FOR_CURRENT_RULES",
                        "material_effect_class": "UNKNOWN",
                    },
                ],
            )

            summary = metrics.build_summary(monthly, sample)
            self.assertTrue(summary["monthly"]["commercial_500_call_gate"])
            self.assertEqual(summary["monthly"]["totals"]["unique_requests"], 600)
            self.assertEqual(summary["monthly"]["totals"]["candidate_preflight_requests"], 500)
            self.assertEqual(summary["monthly"]["unresolved_share_of_candidate_pct"], 40.0)
            self.assertEqual(summary["monthly"]["delivery_multiplier"], 2.0)
            self.assertEqual(summary["sample"]["candidate_cases"], 3)
            self.assertEqual(summary["sample"]["decision_fact_sufficiency_rate_pct"], 66.67)
            self.assertEqual(summary["sample"]["material_hit_rate_pct"], 33.33)
            self.assertTrue(summary["advance_to_e4_mechanical_screen"])
            self.assertFalse(summary["renew_engineering"])

    def test_499_candidates_does_not_clear_gate(self) -> None:
        rows = [
            {
                "operator": "Operator A",
                "complete_month": "2026-07",
                "current_family": "window_door",
                "unique_requests": "700",
                "candidate_preflight_requests": "499",
                "within_supported_jurisdictions": "600",
                "unresolved": "200",
                "partner_deliveries": "700",
                "integration_topology": "CENTRAL_SINGLE_INTEGRATION",
            }
        ]
        summary = metrics.summarize_monthly(rows)
        self.assertFalse(summary["commercial_500_call_gate"])

    def test_rejects_unresolved_above_candidate(self) -> None:
        rows = [
            {
                "operator": "Operator A",
                "complete_month": "2026-07",
                "current_family": "basement",
                "unique_requests": "100",
                "candidate_preflight_requests": "20",
                "within_supported_jurisdictions": "80",
                "unresolved": "21",
            }
        ]
        with self.assertRaisesRegex(ValueError, "unresolved cannot exceed candidate_preflight_requests"):
            metrics.summarize_monthly(rows)

    def test_rejects_candidate_above_supported(self) -> None:
        rows = [
            {
                "operator": "Operator A",
                "complete_month": "2026-07",
                "current_family": "addition",
                "unique_requests": "100",
                "candidate_preflight_requests": "90",
                "within_supported_jurisdictions": "80",
            }
        ]
        with self.assertRaisesRegex(ValueError, "candidate_preflight_requests cannot exceed"):
            metrics.summarize_monthly(rows)

    def test_rejects_state_sum_above_unique(self) -> None:
        rows = [
            {
                "operator": "Operator A",
                "complete_month": "2026-07",
                "current_family": "deck_porch",
                "unique_requests": "100",
                "candidate_preflight_requests": "50",
                "within_supported_jurisdictions": "80",
                "known_required": "30",
                "known_not_required": "30",
                "unresolved": "20",
                "not_checked": "20",
                "unknown_permit_state": "10",
            }
        ]
        with self.assertRaisesRegex(ValueError, "permit-state counts sum"):
            metrics.summarize_monthly(rows)

    def test_rejects_delivery_multiplier_mismatch(self) -> None:
        rows = [
            {
                "operator": "Operator A",
                "complete_month": "2026-07",
                "current_family": "window_door",
                "unique_requests": "100",
                "candidate_preflight_requests": "50",
                "within_supported_jurisdictions": "80",
                "partner_deliveries": "200",
                "delivery_multiplier": "3.0",
            }
        ]
        with self.assertRaisesRegex(ValueError, "delivery_multiplier"):
            metrics.summarize_monthly(rows)

    def test_rejects_candidate_sample_outside_supported_jurisdiction(self) -> None:
        rows = [
            {
                "sample_id": "A-1",
                "current_family": "basement",
                "within_supported_jurisdiction": "NO",
                "candidate_preflight": "YES",
            }
        ]
        with self.assertRaisesRegex(ValueError, "candidate_preflight=yes"):
            metrics.summarize_sample(rows)

    def test_rejects_duplicate_sample_ids(self) -> None:
        rows = [
            {"sample_id": "A-1", "current_family": "basement"},
            {"sample_id": "A-1", "current_family": "basement"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate sample_id"):
            metrics.summarize_sample(rows)

    def test_material_less_conservative_disagreement_blocks_mechanical_screen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            monthly = root / "monthly.csv"
            sample = root / "sample.csv"
            write_csv(
                monthly,
                MONTHLY_FIELDS,
                [
                    {
                        "operator": "Operator A",
                        "complete_month": "2026-07",
                        "current_family": "basement",
                        "unique_requests": 600,
                        "candidate_preflight_requests": 500,
                        "within_supported_jurisdictions": 550,
                        "unresolved": 100,
                        "integration_topology": "CENTRAL_SINGLE_INTEGRATION",
                    }
                ],
            )
            write_csv(
                sample,
                SAMPLE_FIELDS,
                [
                    {
                        "sample_id": "A-1",
                        "current_family": "basement",
                        "within_supported_jurisdiction": "YES",
                        "candidate_preflight": "YES",
                        "fact_sufficiency_class": "DIRECT_STRUCTURED",
                        "material_effect_class": "MATERIAL_EFFECT_CONFIRMED",
                        "disagreement_material": "YES",
                        "safety_direction": "LESS_CONSERVATIVE",
                    }
                ],
            )
            summary = metrics.build_summary(monthly, sample)
            self.assertEqual(summary["sample"]["safety_material_disagreements"], 1)
            self.assertFalse(summary["advance_to_e4_mechanical_screen"])


if __name__ == "__main__":
    unittest.main()
