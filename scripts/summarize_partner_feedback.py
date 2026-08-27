"""Summarize design-partner validation evidence from CSV.

Usage:
    python scripts/summarize_partner_feedback.py
    python scripts/summarize_partner_feedback.py data/partner_feedback.csv

Missing values remain unknown rather than silently becoming zero. Commercial
volume gates only use bounded evidence (E2+) and observed-use gates only use
E4+ rows, so polite replies cannot masquerade as market validation.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path("data/partner_feedback.csv")
POSITIVE_RESPONSE_CLASSES = {"A", "B"}
INTEGRATED_STATUSES = {"testing", "integrated", "production"}
ACCEPT_PRICE_VALUES = {"accept", "accepted", "acceptable", "yes", "trivial"}
EVIDENCE_RANK = {f"e{i}": i for i in range(6)}


def _int_or_none(value: Any) -> int | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def _normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def _evidence_rank(row: dict[str, str]) -> int:
    return EVIDENCE_RANK.get(_normalized(row.get("evidence_level")), 0)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    contacted = [row for row in rows if _normalized(row.get("contact_status")) not in {"", "not_contacted"}]
    conversations = [row for row in rows if str(row.get("response_class") or "").strip()]
    positive = [
        row
        for row in conversations
        if str(row.get("response_class") or "").strip().upper() in POSITIVE_RESPONSE_CLASSES
    ]
    integrations = [
        row
        for row in rows
        if _normalized(row.get("integration_status")) in INTEGRATED_STATUSES
    ]

    bounded_rows = [row for row in rows if _evidence_rank(row) >= 2]
    historical_rows = [row for row in rows if _evidence_rank(row) >= 3]
    observed_rows = [row for row in rows if _evidence_rank(row) >= 4]
    economic_rows = [row for row in rows if _evidence_rank(row) >= 5]

    candidate_values = [
        value
        for row in bounded_rows
        if (value := _int_or_none(row.get("candidate_preflights_per_month"))) is not None
    ]
    pilot_call_values = [
        value
        for row in rows
        if (value := _int_or_none(row.get("pilot_calls"))) is not None
    ]
    observed_call_values = [
        value
        for row in observed_rows
        if (value := _int_or_none(row.get("observed_external_calls"))) is not None
    ]
    historical_sample_values = [
        value
        for row in historical_rows
        if (value := _int_or_none(row.get("historical_samples_provided"))) is not None
    ]

    price_025_accepts = sum(
        _normalized(row.get("price_reaction_025")) in ACCEPT_PRICE_VALUES for row in bounded_rows
    )
    price_050_accepts = sum(
        _normalized(row.get("price_reaction_050")) in ACCEPT_PRICE_VALUES for row in bounded_rows
    )

    response_counts = Counter(
        str(row.get("response_class") or "").strip().upper()
        for row in conversations
    )
    call_band_counts = Counter(
        str(row.get("monthly_call_band") or "").strip()
        for row in bounded_rows
        if str(row.get("monthly_call_band") or "").strip()
    )
    evidence_counts = Counter(
        str(row.get("evidence_level") or "E0").strip().upper() or "E0"
        for row in rows
    )

    known_candidate_total = sum(candidate_values)
    largest_candidate = max(candidate_values, default=0)
    largest_pilot = max(pilot_call_values, default=0)
    observed_external_total = sum(observed_call_values)
    largest_observed_external = max(observed_call_values, default=0)
    historical_samples_total = sum(historical_sample_values)

    gates = {
        "20_conversations": len(conversations) >= 20,
        "3_integrations": len(integrations) >= 3,
        "one_E3_historical_benchmark": bool(historical_rows) and historical_samples_total >= 5,
        "100_external_pilot_calls": observed_external_total >= 100,
        "one_20_call_repeat": largest_observed_external >= 20,
        "one_2000_month_partner": largest_candidate >= 2000,
        "credible_10000_month_path": known_candidate_total >= 10000,
        "price_acceptance_with_bounded_volume": price_025_accepts > 0 or price_050_accepts > 0,
        "one_E5_economic_signal": bool(economic_rows),
    }

    return {
        "targets_recorded": len(rows),
        "contacts_attempted": len(contacted),
        "conversations": len(conversations),
        "positive_A_or_B": len(positive),
        "bounded_workflow_claims_E2_plus": len(bounded_rows),
        "historical_benchmarks_E3_plus": len(historical_rows),
        "observed_usage_partners_E4_plus": len(observed_rows),
        "economic_signals_E5": len(economic_rows),
        "integrations_testing_or_better": len(integrations),
        "pilot_calls_recorded": sum(pilot_call_values),
        "largest_single_pilot_calls": largest_pilot,
        "observed_external_calls": observed_external_total,
        "largest_partner_observed_external_calls": largest_observed_external,
        "historical_samples_provided": historical_samples_total,
        "known_candidate_preflights_per_month": known_candidate_total,
        "largest_partner_candidate_preflights_per_month": largest_candidate,
        "price_025_accepts": price_025_accepts,
        "price_050_accepts": price_050_accepts,
        "response_classes": dict(sorted(response_counts.items())),
        "monthly_call_bands": dict(sorted(call_band_counts.items())),
        "evidence_levels": dict(sorted(evidence_counts.items())),
        "gates": gates,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(DEFAULT_PATH))
    args = parser.parse_args()

    summary = summarize(load_rows(Path(args.path)))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
