"""Measure anonymous contractor permit-workload concentration in Vancouver.

Source: City of Vancouver Open Data, `issued-building-permits`.
Reference year: 2024 (static prior-year extract).

Privacy boundary:
- request only permit number, year-month, type of work, permit category, and
  building-contractor fields;
- never request applicant, civic address, or contractor address;
- contractor strings are normalized only in memory;
- output contains only aggregate frequency distributions and never names,
  addresses, hashes, or row-level records.

This is workload evidence, not demand validation. An issued permit is a
lower/downstream event and does not equal an upstream permit-preflight call.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

BASE_URL = (
    "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/"
    "issued-building-permits/records"
)
REFERENCE_YEAR = "2024"
PAGE_SIZE = 100
FIELDS = "permitnumber,yearmonth,typeofwork,permitcategory,buildingcontractor"

GENERIC_CONTRACTOR_TOKENS = {
    "owner",
    "owner builder",
    "owner-builder",
    "owner/ builder",
    "owner/builder",
    "unknown",
    "n/a",
    "na",
    "none",
    "not applicable",
    "tbd",
    "to be determined",
}

CORPORATE_MARKERS = (
    " ltd", " ltd.", " limited", " inc", " inc.", " corp", " corp.",
    " corporation", " construction", " contracting", " contractor",
    " builders", " builder", " developments", " development", " homes",
    " renovations", " renovation", " group", " services", " projects",
    " enterprises", " holdings", " management", " engineering",
)

ANNUAL_THRESHOLDS = (2, 5, 10, 12, 20, 24, 40, 60, 80, 120, 240, 480, 960)
MONTHLY_THRESHOLDS = (2, 5, 10, 20, 40, 80)


def _normalize_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _display_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    text = re.sub(r"\s+", " ", text)
    return text or "(blank)"


def _contractor_token(value: object) -> str | None:
    token = _normalize_text(value)
    if not token or token in GENERIC_CONTRACTOR_TOKENS:
        return None
    return token


def _looks_corporate(token: str) -> bool:
    padded = f" {token} "
    return any(marker in padded for marker in CORPORATE_MARKERS)


def _fetch_records() -> list[dict]:
    rows: list[dict] = []
    offset = 0
    total_count: int | None = None

    while True:
        params = urllib.parse.urlencode(
            {
                "select": FIELDS,
                "where": f'issueyear="{REFERENCE_YEAR}"',
                "limit": PAGE_SIZE,
                "offset": offset,
            }
        )
        request = urllib.request.Request(
            f"{BASE_URL}?{params}",
            headers={"User-Agent": "ProjectPermit public-market-research/1.0"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if total_count is None:
            total_count = int(payload.get("total_count", -1))
            # 2024 is a known static full-year extract; fail closed on a wildly
            # unexpected result rather than analyze the wrong filter/year.
            if not 2500 <= total_count <= 6000:
                raise RuntimeError(f"Unexpected 2024 total_count={total_count}")

        batch = payload.get("results")
        if not isinstance(batch, list):
            raise RuntimeError("Vancouver API response has no results list")
        rows.extend(batch)
        offset += len(batch)
        if not batch or len(rows) >= total_count:
            break
        if offset >= 10000:
            raise RuntimeError("Records pagination reached API 10,000-row limit")

    if total_count is None or len(rows) != total_count:
        raise RuntimeError(f"Expected {total_count} records, fetched {len(rows)}")
    return rows


def _percentile(values: list[int], percentile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(percentile * len(ordered)) - 1))
    return int(ordered[index])


def _scope_rows(rows: Iterable[dict], scope: str) -> list[dict]:
    result = []
    for row in rows:
        work = _normalize_text(row.get("typeofwork"))
        category = _normalize_text(row.get("permitcategory"))
        if scope == "all":
            keep = True
        elif scope == "addition_alteration":
            keep = work == "addition / alteration"
        elif scope == "residential_any":
            keep = "residential" in category
        elif scope == "residential_renovation":
            keep = "residential" in category and "renovation" in category
        else:
            raise ValueError(scope)
        if keep:
            result.append(row)
    return result


def _analyze_cohort(rows: list[dict], corporate_only: bool) -> dict:
    annual = Counter()
    monthly: dict[str, Counter] = defaultdict(Counter)
    rows_with_token = 0

    for row in rows:
        token = _contractor_token(row.get("buildingcontractor"))
        if token is None:
            continue
        if corporate_only and not _looks_corporate(token):
            continue
        rows_with_token += 1
        annual[token] += 1
        month = _normalize_text(row.get("yearmonth")) or "unknown"
        monthly[token][month] += 1

    annual_values = list(annual.values())
    max_month_by_contractor = [max(counts.values()) for counts in monthly.values() if counts]
    sorted_annual = sorted(annual_values, reverse=True)

    def concentration(n: int) -> float | None:
        if not rows_with_token:
            return None
        return round(sum(sorted_annual[:n]) / rows_with_token * 100, 2)

    return {
        "permits_with_contractor_token": rows_with_token,
        "anonymous_contractor_tokens": len(annual),
        "annual_permits_per_contractor": {
            "median": round(statistics.median(annual_values), 2) if annual_values else None,
            "p75": _percentile(annual_values, 0.75),
            "p90": _percentile(annual_values, 0.90),
            "p95": _percentile(annual_values, 0.95),
            "p99": _percentile(annual_values, 0.99),
            "max": max(annual_values) if annual_values else None,
            "contractors_at_or_above": {
                str(threshold): sum(value >= threshold for value in annual_values)
                for threshold in ANNUAL_THRESHOLDS
            },
        },
        "max_monthly_permits_per_contractor": {
            "median": round(statistics.median(max_month_by_contractor), 2)
            if max_month_by_contractor else None,
            "p90": _percentile(max_month_by_contractor, 0.90),
            "p95": _percentile(max_month_by_contractor, 0.95),
            "p99": _percentile(max_month_by_contractor, 0.99),
            "max": max(max_month_by_contractor) if max_month_by_contractor else None,
            "contractors_with_any_month_at_or_above": {
                str(threshold): sum(value >= threshold for value in max_month_by_contractor)
                for threshold in MONTHLY_THRESHOLDS
            },
        },
        "permit_concentration_pct": {
            "top_1": concentration(1),
            "top_5": concentration(5),
            "top_10": concentration(10),
            "top_25": concentration(25),
            "top_50": concentration(50),
        },
    }


def _aggregate_label_counts(rows: list[dict]) -> dict:
    work = Counter(_display_text(row.get("typeofwork")) for row in rows)
    category = Counter(_display_text(row.get("permitcategory")) for row in rows)
    pairs = Counter(
        (_display_text(row.get("typeofwork")), _display_text(row.get("permitcategory")))
        for row in rows
    )
    return {
        "type_of_work_counts": dict(sorted(work.items(), key=lambda item: (-item[1], item[0]))),
        "permit_category_counts": dict(sorted(category.items(), key=lambda item: (-item[1], item[0]))),
        "work_category_counts": [
            {"type_of_work": work_label, "permit_category": category_label, "count": count}
            for (work_label, category_label), count in sorted(
                pairs.items(), key=lambda item: (-item[1], item[0][0], item[0][1])
            )
        ],
    }


def summarize() -> dict:
    rows = _fetch_records()
    scopes = {}
    for scope in ("all", "addition_alteration", "residential_any", "residential_renovation"):
        scoped = _scope_rows(rows, scope)
        scopes[scope] = {
            "issued_permit_records": len(scoped),
            "all_nonempty_nongeneric_contractor_tokens": _analyze_cohort(scoped, False),
            "corporate_like_contractor_tokens": _analyze_cohort(scoped, True),
        }

    return {
        "source": "City of Vancouver Open Data — issued-building-permits",
        "source_dataset": "issued-building-permits",
        "reference_year": int(REFERENCE_YEAR),
        "privacy_boundary": (
            "No applicant/address/contractor-address fields requested. Contractor strings are used only "
            "in runner memory and are not emitted or hashed into output. City type-of-work and permit-category "
            "labels are emitted only as aggregate counts."
        ),
        "evidence_boundary": (
            "Issued-permit workload is downstream technical market evidence, not permit-preflight incidence, "
            "not E3/E4/E5, and not a count of unique companies. Aggregate labels are diagnostic and must not "
            "be mapped to ProjectPermit families unless the City label is unambiguous."
        ),
        "aggregate_labels": _aggregate_label_counts(rows),
        "scopes": scopes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("vancouver_contractor_permit_workload_2024.json"),
    )
    args = parser.parse_args()
    result = summarize()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
