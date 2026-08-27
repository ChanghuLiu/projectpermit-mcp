"""Aggregate Mississauga issued building permits by application type.

Source: City of Mississauga official ArcGIS FeatureServer. The script uses
server-side grouped statistics by APP_DETAIL and ISSUE_DATE. It never requests
addresses, descriptions, applicant/contractor data, or row-level records.
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

LAYER_URL = (
    "https://services6.arcgis.com/hM5ymMLbxIyWTjn2/arcgis/rest/services/"
    "Issued_Building_Permits/FeatureServer/0/query"
)

FOCUS_TYPES = (
    "PLUMBING ONLY",
    "HEATING ONLY",
    "MECHANICAL ONLY",
    "DRAIN ONLY",
    "SITE SERVICING",
)


def _query(year: int) -> list[dict]:
    params = {
        "where": (
            f"ISSUE_DATE >= DATE '{year}-01-01' AND "
            f"ISSUE_DATE < DATE '{year + 1}-01-01'"
        ),
        "outStatistics": json.dumps(
            [
                {
                    "statisticType": "count",
                    "onStatisticField": "OBJECTID",
                    "outStatisticFieldName": "permit_count",
                }
            ],
            separators=(",", ":"),
        ),
        "groupByFieldsForStatistics": "APP_DETAIL",
        "orderByFields": "permit_count DESC",
        "returnGeometry": "false",
        "f": "json",
    }
    request = urllib.request.Request(
        LAYER_URL + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "ProjectPermit public-market-research/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.load(response)
    if "error" in payload:
        raise RuntimeError(f"ArcGIS query failed: {payload['error']}")
    return payload.get("features", [])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument(
        "--output", type=Path, default=Path("mississauga_trade_permit_volume.json")
    )
    args = parser.parse_args()

    features = _query(args.year)
    counts: dict[str, int] = {}
    for feature in features:
        attributes = feature.get("attributes", {})
        label = (attributes.get("APP_DETAIL") or "(blank)").strip()
        counts[label] = int(attributes.get("permit_count") or 0)

    total = sum(counts.values())
    focus = {name: counts.get(name, 0) for name in FOCUS_TYPES}
    focus_total = sum(focus.values())

    result = {
        "source": "City of Mississauga — Issued Building Permits FeatureServer",
        "reference_year": args.year,
        "evidence_boundary": (
            "City-level issued-permit workflow events only; not unique customers, "
            "not ProjectPermit preflight incidence, and not E3/E4/E5 evidence."
        ),
        "privacy_boundary": (
            "Server-side grouped statistics only on APP_DETAIL and ISSUE_DATE; "
            "no row-level address, description, applicant, or contractor fields requested."
        ),
        "total_issued_records": total,
        "application_type_counts": dict(
            sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ),
        "trade_focus_counts": focus,
        "trade_focus_total": focus_total,
        "trade_focus_avg_month": round(focus_total / 12, 2),
        "trade_focus_share_pct": round(focus_total / total * 100, 2) if total else None,
    }

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
