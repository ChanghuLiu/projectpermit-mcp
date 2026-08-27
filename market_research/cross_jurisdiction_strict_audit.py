"""Apply a stricter decisiveness test to the synthetic scope matrix.

Strict divergence requires at least one jurisdiction returning REQUIRED and at least
one returning LIKELY_NOT_REQUIRED for the exact same normalized facts. This avoids
counting LIKELY_REQUIRED, confirmation, additional-review, or OUT_OF_SCOPE states as
proof of opposite municipal outcomes.

Internal technical/market-structure evidence only; not E2/E3/E4/E5.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from projectpermit.jurisdiction_router import SUPPORTED_JURISDICTIONS, evaluate_project
from cross_jurisdiction_scope_matrix import BASE_PROPERTY, CASES


def run() -> dict:
    rows = []
    strict_cases = []
    unanimous_decisive_cases = []

    for case in CASES:
        outcomes = {}
        for jurisdiction in SUPPORTED_JURISDICTIONS:
            result = evaluate_project(
                {
                    "jurisdiction": jurisdiction,
                    "project": deepcopy(case["project"]),
                    "property": deepcopy(BASE_PROPERTY),
                }
            )
            outcomes[jurisdiction] = result["determination"]

        statuses = set(outcomes.values())
        strict = "REQUIRED" in statuses and "LIKELY_NOT_REQUIRED" in statuses
        if strict:
            strict_cases.append(case["id"])

        decisive = {s for s in statuses if s in {"REQUIRED", "LIKELY_NOT_REQUIRED"}}
        unanimous_decisive = len(decisive) == 1 and all(
            status in {"REQUIRED", "LIKELY_NOT_REQUIRED"} for status in outcomes.values()
        )
        if unanimous_decisive:
            unanimous_decisive_cases.append(case["id"])

        rows.append(
            {
                "case_id": case["id"],
                "family": case["project"]["family"],
                "strict_required_vs_not_required_divergence": strict,
                "outcomes": outcomes,
            }
        )

    total = len(CASES)
    return {
        "evidence_boundary": (
            "Synthetic address-free strict diagnostic only; not E2/E3/E4/E5 and not demand evidence. "
            "Strict divergence requires REQUIRED in at least one supported jurisdiction and "
            "LIKELY_NOT_REQUIRED in at least one other jurisdiction for identical normalized facts."
        ),
        "case_count": total,
        "jurisdiction_count": len(SUPPORTED_JURISDICTIONS),
        "strict_divergence_cases": len(strict_cases),
        "strict_divergence_share_pct": round(len(strict_cases) / total * 100, 2),
        "strict_divergence_case_ids": strict_cases,
        "unanimous_decisive_cases": len(unanimous_decisive_cases),
        "unanimous_decisive_case_ids": unanimous_decisive_cases,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("cross_jurisdiction_strict_audit.json")
    )
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
