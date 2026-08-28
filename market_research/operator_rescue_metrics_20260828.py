from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path


NUMERIC_FIELDS = (
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
)


@dataclass(frozen=True)
class AggregateMetrics:
    unique_requests: int
    supported_requests: int
    candidate_preflights: int
    unresolved: int
    followup_or_research: int
    material_effect_known: int
    partner_deliveries: int

    @property
    def unresolved_share(self) -> float | None:
        return None if self.candidate_preflights == 0 else self.unresolved / self.candidate_preflights

    @property
    def followup_share(self) -> float | None:
        return None if self.candidate_preflights == 0 else self.followup_or_research / self.candidate_preflights

    @property
    def candidate_share_of_unique(self) -> float | None:
        return None if self.unique_requests == 0 else self.candidate_preflights / self.unique_requests

    @property
    def delivery_multiplier(self) -> float | None:
        return None if self.unique_requests == 0 else self.partner_deliveries / self.unique_requests


def _to_int(value: str | None, field: str, row_number: int) -> int:
    text = (value or "").strip()
    if text == "":
        return 0
    try:
        parsed = int(text)
    except ValueError as exc:
        raise ValueError(f"row {row_number}: {field} must be an integer, got {text!r}") from exc
    if parsed < 0:
        raise ValueError(f"row {row_number}: {field} must be >= 0")
    return parsed


def load_monthly_aggregate(path: Path) -> AggregateMetrics:
    totals = {field: 0 for field in NUMERIC_FIELDS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"operator", "complete_month", "current_family", *NUMERIC_FIELDS}
        missing = sorted(required - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"missing aggregate columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("monthly aggregate has no rows")

    months = {row.get("complete_month", "").strip() for row in rows if row.get("complete_month", "").strip()}
    operators = {row.get("operator", "").strip() for row in rows if row.get("operator", "").strip()}
    if len(months) > 1:
        raise ValueError(f"aggregate must represent one complete month, got {sorted(months)}")
    if len(operators) > 1:
        raise ValueError(f"aggregate must represent one operator, got {sorted(operators)}")

    for index, row in enumerate(rows, start=2):
        values = {field: _to_int(row.get(field), field, index) for field in NUMERIC_FIELDS}
        unique = values["unique_requests"]
        supported = values["within_supported_jurisdictions"]
        candidate = values["candidate_preflight_requests"]

        if supported > unique:
            raise ValueError(f"row {index}: within_supported_jurisdictions exceeds unique_requests")
        if candidate > supported:
            raise ValueError(f"row {index}: candidate_preflight_requests exceeds within_supported_jurisdictions")
        if values["unresolved"] > candidate:
            raise ValueError(f"row {index}: unresolved exceeds candidate_preflight_requests")
        if values["required_followup_or_research"] > candidate:
            raise ValueError(f"row {index}: required_followup_or_research exceeds candidate_preflight_requests")
        if values["material_effect_known_count"] > candidate:
            raise ValueError(f"row {index}: material_effect_known_count exceeds candidate_preflight_requests")

        permit_state_sum = sum(values[field] for field in ("known_required", "known_not_required", "unresolved", "not_checked", "unknown_permit_state"))
        if permit_state_sum > candidate:
            raise ValueError(f"row {index}: permit-state buckets sum to {permit_state_sum}, exceeding candidate_preflight_requests={candidate}")

        for field, value in values.items():
            totals[field] += value

    return AggregateMetrics(
        unique_requests=totals["unique_requests"],
        supported_requests=totals["within_supported_jurisdictions"],
        candidate_preflights=totals["candidate_preflight_requests"],
        unresolved=totals["unresolved"],
        followup_or_research=totals["required_followup_or_research"],
        material_effect_known=totals["material_effect_known_count"],
        partner_deliveries=totals["partner_deliveries"],
    )


def load_case_sample(path: Path) -> dict[str, int | float | None]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"case_id", "chronological_index", "current_family", "jurisdiction", "facts_sufficient_without_followup", "material_workflow_effect"}
        missing = sorted(required - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"missing sample columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        return {"sample_size": 0, "fact_sufficient_count": 0, "fact_sufficiency_rate": None, "material_hit_count": 0, "material_hit_rate": None}

    indexes: list[int] = []
    sufficient = 0
    material = 0
    truthy = {"1", "true", "yes", "y"}
    for row_number, row in enumerate(rows, start=2):
        try:
            index = int((row.get("chronological_index") or "").strip())
        except ValueError as exc:
            raise ValueError(f"row {row_number}: chronological_index must be an integer") from exc
        indexes.append(index)
        if (row.get("facts_sufficient_without_followup") or "").strip().lower() in truthy:
            sufficient += 1
        if (row.get("material_workflow_effect") or "").strip().lower() in truthy:
            material += 1

    if indexes != sorted(indexes) or len(indexes) != len(set(indexes)):
        raise ValueError("sample chronological_index values must be unique and ascending")

    n = len(rows)
    return {"sample_size": n, "fact_sufficient_count": sufficient, "fact_sufficiency_rate": sufficient / n, "material_hit_count": material, "material_hit_rate": material / n}


def build_summary(aggregate: AggregateMetrics, sample: dict[str, int | float | None]) -> dict[str, object]:
    return {
        "aggregate": {
            "unique_requests": aggregate.unique_requests,
            "supported_requests": aggregate.supported_requests,
            "candidate_preflights": aggregate.candidate_preflights,
            "candidate_share_of_unique": aggregate.candidate_share_of_unique,
            "unresolved": aggregate.unresolved,
            "unresolved_share_of_candidates": aggregate.unresolved_share,
            "followup_or_research": aggregate.followup_or_research,
            "followup_share_of_candidates": aggregate.followup_share,
            "partner_deliveries": aggregate.partner_deliveries,
            "delivery_multiplier": aggregate.delivery_multiplier,
        },
        "sample": sample,
        "gates": {
            "candidate_preflight_500_monthly": aggregate.candidate_preflights >= 500,
            "representative_sample_50": int(sample["sample_size"] or 0) >= 50,
            "representative_sample_100": int(sample["sample_size"] or 0) >= 100,
        },
        "boundary": "These metrics support rescue/falsification only. They do not constitute E4 usage or E5 willingness to pay.",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: operator_rescue_metrics_20260828.py MONTHLY_AGGREGATE.csv CASE_SAMPLE.csv", file=sys.stderr)
        return 2
    try:
        aggregate = load_monthly_aggregate(Path(argv[1]))
        sample = load_case_sample(Path(argv[2]))
        print(json.dumps(build_summary(aggregate, sample), indent=2, sort_keys=True))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
