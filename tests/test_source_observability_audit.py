import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "source_observability_audit.py"
SPEC = importlib.util.spec_from_file_location("source_observability_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class SourceObservabilityAuditTests(unittest.TestCase):
    def test_summary_reports_fetch_and_validator_coverage(self) -> None:
        rows = [
            {
                "source_id": "A",
                "authority": "City A",
                "criticality": "critical",
                "ok": True,
                "has_http_validator": True,
            },
            {
                "source_id": "B",
                "authority": "City A",
                "criticality": "high",
                "ok": True,
                "has_http_validator": False,
            },
            {
                "source_id": "C",
                "authority": "City B",
                "criticality": "critical",
                "ok": False,
                "error_type": "HTTPStatusError",
            },
        ]
        summary = MODULE.summarize(rows)
        self.assertEqual(summary["total_sources"], 3)
        self.assertEqual(summary["fetch_ok"], 2)
        self.assertEqual(summary["fetch_failed"], 1)
        self.assertEqual(summary["fetch_success_pct"], 66.7)
        self.assertEqual(summary["http_validator_count"], 1)
        self.assertEqual(summary["http_validator_pct_of_ok"], 50.0)
        self.assertEqual(summary["critical_failures"], ["C"])
        self.assertFalse(summary["interpretation"]["continuous_monitoring_enabled"])
        self.assertFalse(summary["interpretation"]["source_state_written"])
        self.assertFalse(summary["interpretation"]["rules_modified"])


if __name__ == "__main__":
    unittest.main()
