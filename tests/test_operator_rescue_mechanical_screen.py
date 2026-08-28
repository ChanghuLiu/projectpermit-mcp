from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "market_research" / "operator_rescue_metrics.py"
_spec = importlib.util.spec_from_file_location("operator_rescue_metrics_screen", SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
metrics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(metrics)


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _monthly(topology: str) -> dict[str, str]:
    return {
        "operator": "Operator A",
        "complete_month": "2026-07",
        "current_family": "kitchen_bath_plumbing",
        "unique_requests": "600",
        "candidate_preflight_requests": "500",
        "within_supported_jurisdictions": "550",
        "unresolved": "100",
        "integration_topology": topology,
    }


class OperatorRescueMechanicalScreenTests(unittest.TestCase):
    def test_manual_export_does_not_clear_e4_screen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            monthly, sample = root / "monthly.csv", root / "sample.csv"
            _write(monthly, [_monthly("MANUAL_EXPORT_ONLY")])
            _write(sample, [{
                "sample_id": "A-1",
                "current_family": "kitchen_bath_plumbing",
                "within_supported_jurisdiction": "YES",
                "candidate_preflight": "YES",
                "fact_sufficiency_class": "DIRECT_STRUCTURED",
                "material_effect_class": "MATERIAL_EFFECT_CONFIRMED",
            }])
            summary = metrics.build_summary(monthly, sample)
            self.assertFalse(summary["monthly"]["central_integration_plausible"])
            self.assertFalse(summary["advance_to_e4_mechanical_screen"])

    def test_material_hit_on_noncandidate_does_not_clear_e4_screen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            monthly, sample = root / "monthly.csv", root / "sample.csv"
            _write(monthly, [_monthly("CENTRAL_SINGLE_INTEGRATION")])
            _write(sample, [
                {
                    "sample_id": "A-1",
                    "current_family": "kitchen_bath_plumbing",
                    "within_supported_jurisdiction": "YES",
                    "candidate_preflight": "YES",
                    "fact_sufficiency_class": "DIRECT_STRUCTURED",
                    "material_effect_class": "NO_MATERIAL_EFFECT",
                },
                {
                    "sample_id": "A-2",
                    "current_family": "kitchen_bath_plumbing",
                    "within_supported_jurisdiction": "NO",
                    "candidate_preflight": "NO",
                    "fact_sufficiency_class": "INSUFFICIENT_FOR_CURRENT_RULES",
                    "material_effect_class": "MATERIAL_EFFECT_CONFIRMED",
                },
            ])
            summary = metrics.build_summary(monthly, sample)
            self.assertEqual(summary["sample"]["material_effect_counts"]["MATERIAL_EFFECT_CONFIRMED"], 1)
            self.assertEqual(summary["sample"]["material_effect_confirmed_candidate_count"], 0)
            self.assertEqual(summary["sample"]["material_hit_rate_pct"], 0.0)
            self.assertFalse(summary["advance_to_e4_mechanical_screen"])


if __name__ == "__main__":
    unittest.main()
