#!/usr/bin/env python3
"""Run the deterministic 20-case Jobber synthetic integration benchmark.

This command performs no Jobber network calls and no municipal GIS calls.  It is
an integration regression harness, not E3 market evidence.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from projectpermit import evaluate_project
from projectpermit.jobber_adapter import (
    build_jobber_writeback,
    build_preflight_facts,
    extract_jobber_work_object,
)


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "jobber_synthetic_integration_benchmark.json"


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cases = payload["cases"]
    counts: Counter[str] = Counter()
    mismatches: list[dict[str, str]] = []

    for case in cases:
        extracted = extract_jobber_work_object(case["payload"])
        facts = build_preflight_facts(
            extracted,
            jurisdiction=case["jurisdiction"],
            project=case["project"],
            resolve_address=False,
            client_tag="jobber-synthetic-benchmark",
        )
        result = evaluate_project(facts)
        writeback = build_jobber_writeback(result)
        actual = result["determination"]
        expected = case["expected_determination"]
        counts[actual] += 1

        if actual != expected or writeback["projectpermit_preflight"] != actual:
            mismatches.append(
                {
                    "id": case["id"],
                    "expected": expected,
                    "actual": actual,
                }
            )

    families = sorted({case["project"]["family"] for case in cases})
    summary = {
        "benchmark": payload["benchmark"],
        "evidence_level": "integration_regression_not_E3",
        "network_calls": 0,
        "cases": len(cases),
        "families": families,
        "determinations": dict(sorted(counts.items())),
        "mismatches": mismatches,
        "status": "PASS" if not mismatches else "FAIL",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
