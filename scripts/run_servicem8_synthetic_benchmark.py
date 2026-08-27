#!/usr/bin/env python3
"""Run the deterministic ServiceM8 synthetic integration benchmark.

No ServiceM8 network calls and no municipal GIS calls are made. This is an
integration regression harness, not E3 market evidence.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from projectpermit import evaluate_project
from projectpermit.servicem8_adapter import (
    build_preflight_facts,
    build_servicem8_routing_summary,
    extract_servicem8_work_object,
)


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "servicem8_synthetic_integration_benchmark.json"


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cases = payload["cases"]
    counts: Counter[str] = Counter()
    mismatches: list[dict[str, str]] = []

    for case in cases:
        extracted = extract_servicem8_work_object(
            case["payload"],
            job_materials=case.get("materials"),
        )
        facts = build_preflight_facts(
            extracted,
            jurisdiction=case["jurisdiction"],
            project=case["project"],
            resolve_address=False,
            client_tag="servicem8-synthetic-benchmark",
        )
        result = evaluate_project(facts)
        routing = build_servicem8_routing_summary(result)
        actual = result["determination"]
        expected = case["expected_determination"]
        counts[actual] += 1

        if actual != expected or routing["projectpermit_preflight"] != actual:
            mismatches.append({"id": case["id"], "expected": expected, "actual": actual})

    print(
        json.dumps(
            {
                "benchmark": payload["benchmark"],
                "evidence_level": "integration_regression_not_E3",
                "network_calls": 0,
                "cases": len(cases),
                "families": sorted({case["project"]["family"] for case in cases}),
                "determinations": dict(sorted(counts.items())),
                "mismatches": mismatches,
                "status": "PASS" if not mismatches else "FAIL",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
