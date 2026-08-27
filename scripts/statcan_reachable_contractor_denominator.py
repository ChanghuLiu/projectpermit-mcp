"""Fetch and summarize Statistics Canada employer-business counts for ProjectPermit cities.

Source table: Statistics Canada 33-10-1176-01, June 2026.
This script intentionally uses employer locations only because the June 2026
census-subdivision table is the clean municipal-level denominator currently
available. It does not convert CMA or provincial counts into city estimates.

Layers:
- A: residential building construction [2361]
- B core: A + foundation/structure/exterior [2381] + building equipment [2382]
- B broad: B core + building finishing [2383]
- C: all construction [23] (ceiling only)

The hierarchy rows are read directly; B layers sum mutually exclusive industry
groups and do not sum parents with children.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

TABLE_ID = "33101176"
SOURCE_URL = f"https://www150.statcan.gc.ca/n1/en/tbl/csv/{TABLE_ID}-eng.zip"

TARGETS = {
    "toronto_on": ("Toronto", "Ontario"),
    "ottawa_on": ("Ottawa", "Ontario"),
    "mississauga_on": ("Mississauga", "Ontario"),
    "vancouver_bc": ("Vancouver", "British Columbia"),
    "gatineau_qc": ("Gatineau", "Quebec"),
    "laval_qc": ("Laval", "Quebec"),
    "longueuil_qc": ("Longueuil", "Quebec"),
}

LAYER_CODES = {
    "A_residential_building": ["2361"],
    "B_core_permit_sensitive": ["2361", "2381", "2382"],
    "B_broad_renovation_trades": ["2361", "2381", "2382", "2383"],
    "C_all_construction_ceiling": ["23"],
}


def _find_column(fieldnames: list[str], needle: str) -> str:
    matches = [name for name in fieldnames if needle.lower() in name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one column matching {needle!r}; got {matches}")
    return matches[0]


def _extract_code(label: str) -> str | None:
    match = re.search(r"\[([0-9A-Za-z-]+)\]\s*$", label or "")
    return match.group(1) if match else None


def _is_target_geo(geo: str, city: str, province: str) -> bool:
    text = (geo or "").strip().lower()
    return text.startswith(city.lower()) and province.lower() in text


def _download_rows() -> tuple[list[dict[str, str]], list[str]]:
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "ProjectPermit market-denominator research/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        candidates = [
            name for name in zf.namelist()
            if name.lower().endswith(".csv") and "metadata" not in name.lower()
        ]
        if not candidates:
            raise RuntimeError("StatCan ZIP contained no data CSV")
        data_name = max(candidates, key=lambda name: zf.getinfo(name).file_size)
        raw = zf.read(data_name).decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        raise RuntimeError("StatCan CSV has no header")
    return list(reader), list(reader.fieldnames)


def summarize() -> dict:
    rows, fieldnames = _download_rows()
    geo_col = _find_column(fieldnames, "GEO")
    naics_col = _find_column(fieldnames, "North American Industry Classification System")
    employment_col = _find_column(fieldnames, "Employment size")
    value_col = "VALUE" if "VALUE" in fieldnames else _find_column(fieldnames, "VALUE")

    employment_values = sorted({(row.get(employment_col) or "").strip() for row in rows})
    total_employment_values = [
        value for value in employment_values
        if "total" in value.lower() and ("employment" in value.lower() or "size" in value.lower())
    ]
    if len(total_employment_values) != 1:
        raise RuntimeError(
            "Could not uniquely identify total-employment row; candidates="
            + repr(total_employment_values)
            + "; actual_values="
            + repr(employment_values[:100])
        )
    total_employment = total_employment_values[0]

    results: dict[str, dict] = {}
    diagnostics: dict[str, list[str]] = {}

    for jurisdiction, (city, province) in TARGETS.items():
        geo_candidates = sorted({
            (row.get(geo_col) or "").strip()
            for row in rows
            if _is_target_geo(row.get(geo_col) or "", city, province)
        })
        diagnostics[jurisdiction] = geo_candidates
        if not geo_candidates:
            raise RuntimeError(f"No StatCan geography matched {city}, {province}")

        if len(geo_candidates) == 1:
            chosen_geo = geo_candidates[0]
        else:
            csd = [g for g in geo_candidates if "census subdivision" in g.lower()]
            if len(csd) == 1:
                chosen_geo = csd[0]
            else:
                exactish = [g for g in geo_candidates if g.lower() in {
                    f"{city}, {province}".lower(),
                    f"{city} (city), {province}".lower(),
                }]
                if len(exactish) == 1:
                    chosen_geo = exactish[0]
                else:
                    raise RuntimeError(
                        f"Ambiguous geography for {jurisdiction}: {geo_candidates}"
                    )

        by_code: dict[str, float] = {}
        labels: dict[str, str] = {}
        for row in rows:
            if (row.get(geo_col) or "").strip() != chosen_geo:
                continue
            if (row.get(employment_col) or "").strip() != total_employment:
                continue
            label = (row.get(naics_col) or "").strip()
            code = _extract_code(label)
            if not code:
                continue
            raw_value = (row.get(value_col) or "").strip()
            if raw_value in {"", "..", "...", "x", "F"}:
                continue
            try:
                value = float(raw_value.replace(",", ""))
            except ValueError:
                continue
            by_code[code] = value
            labels[code] = label

        missing_codes = sorted({code for codes in LAYER_CODES.values() for code in codes} - set(by_code))
        if missing_codes:
            raise RuntimeError(
                f"{jurisdiction}: missing required NAICS codes {missing_codes}; "
                f"available nearby={[c for c in sorted(by_code) if c.startswith(('23','236','238'))][:80]}"
            )

        layers = {
            name: int(sum(by_code[code] for code in codes))
            for name, codes in LAYER_CODES.items()
        }
        results[jurisdiction] = {
            "geo": chosen_geo,
            "layers": layers,
            "component_naics": {
                code: {"label": labels[code], "employer_locations": int(by_code[code])}
                for code in sorted({code for codes in LAYER_CODES.values() for code in codes})
            },
        }

    totals = {
        layer: sum(item["layers"][layer] for item in results.values())
        for layer in LAYER_CODES
    }

    penetration = {}
    for layer, denominator in totals.items():
        penetration[layer] = {
            "125_accounts_pct": round(125 / denominator * 100, 3) if denominator else None,
            "400_accounts_pct": round(400 / denominator * 100, 3) if denominator else None,
            "500_accounts_pct": round(500 / denominator * 100, 3) if denominator else None,
        }

    return {
        "source_table": "33-10-1176-01",
        "source_url": SOURCE_URL,
        "reference_period": "June 2026",
        "unit": "employer business locations",
        "important_boundary": (
            "Municipal census-subdivision employer locations only. Non-employer/indeterminate businesses "
            "are excluded; CMA and provincial counts are not substituted."
        ),
        "employment_size_filter": total_employment,
        "layer_definitions": LAYER_CODES,
        "cities": results,
        "totals": totals,
        "penetration_required": penetration,
        "geo_match_diagnostics": diagnostics,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("reachable_contractor_denominator.json"))
    args = parser.parse_args()
    result = summarize()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
