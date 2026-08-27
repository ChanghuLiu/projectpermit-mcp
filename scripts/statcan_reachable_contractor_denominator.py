"""Fetch and summarize Statistics Canada contractor business-count evidence.

Primary municipal source: 33-10-1176-01, June 2026, with employees, CMA/CSD.
Provincial sensitivity sources: 33-10-1174-01 (with employees) and
33-10-1175-01 (without employees), June 2026.

Municipal counts are observed CSD employer-location counts. Provincial
without/with-employee ratios are reported only as missing-pool sensitivity and
must never be converted into observed city counts.
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

MUNICIPAL_TABLE_ID = "33101176"
PROV_EMPLOYER_TABLE_ID = "33101174"
PROV_NONEMPLOYER_TABLE_ID = "33101175"

TARGETS = {
    "toronto_on": ("Toronto", "35"),
    "ottawa_on": ("Ottawa", "35"),
    "mississauga_on": ("Mississauga", "35"),
    "vancouver_bc": ("Vancouver", "59"),
    "gatineau_qc": ("Gatineau", "24"),
    "laval_qc": ("Laval", "24"),
    "longueuil_qc": ("Longueuil", "24"),
}

PROVINCES = ("Ontario", "Quebec", "British Columbia")

LAYER_CODES = {
    "A_residential_building": ["2361"],
    "B_core_permit_sensitive": ["2361", "2381", "2382"],
    "B_broad_renovation_trades": ["2361", "2381", "2382", "2383"],
    "C_all_construction_ceiling": ["23"],
}
REQUIRED_CODES = sorted({code for codes in LAYER_CODES.values() for code in codes})


def _table_url(table_id: str) -> str:
    return f"https://www150.statcan.gc.ca/n1/en/tbl/csv/{table_id}-eng.zip"


def _find_column(fieldnames: list[str], needle: str) -> str:
    matches = [name for name in fieldnames if needle.lower() in name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one column matching {needle!r}; got {matches}")
    return matches[0]


def _extract_code(label: str) -> str | None:
    match = re.search(r"\[([0-9A-Za-z-]+)\]\s*$", label or "")
    return match.group(1) if match else None


def _is_csd_dguid(dguid: str, province_uid: str) -> bool:
    # DGUID structure: reference-year + geographic-area type/schema + UID.
    # A0005 is the Census subdivision administrative-area schema. The CSD UID
    # starts with the 2-digit province/territory UID.
    return bool(re.fullmatch(rf"\d{{4}}A0005{re.escape(province_uid)}\d{{5}}", dguid or ""))


def _download_rows(table_id: str) -> tuple[list[dict[str, str]], list[str]]:
    req = urllib.request.Request(
        _table_url(table_id),
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
            raise RuntimeError(f"StatCan table {table_id} ZIP contained no data CSV")
        data_name = max(candidates, key=lambda name: zf.getinfo(name).file_size)
        raw = zf.read(data_name).decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        raise RuntimeError(f"StatCan table {table_id} CSV has no header")
    return list(reader), list(reader.fieldnames)


def _numeric_value(row: dict[str, str], value_col: str) -> float | None:
    raw = (row.get(value_col) or "").strip()
    if raw in {"", "..", "...", "x", "F"}:
        return None
    try:
        return float(raw.replace(",", ""))
    except ValueError:
        return None


def _layer_totals(by_code: dict[str, float]) -> dict[str, int]:
    missing = sorted(set(REQUIRED_CODES) - set(by_code))
    if missing:
        raise RuntimeError(f"Missing required NAICS codes {missing}; available={sorted(by_code)[:100]}")
    return {
        name: int(sum(by_code[code] for code in codes))
        for name, codes in LAYER_CODES.items()
    }


def _municipal_employer_counts() -> dict:
    rows, fieldnames = _download_rows(MUNICIPAL_TABLE_ID)
    geo_col = _find_column(fieldnames, "GEO")
    naics_col = _find_column(fieldnames, "North American Industry Classification System")
    employment_col = _find_column(fieldnames, "Employment size")
    value_col = "VALUE" if "VALUE" in fieldnames else _find_column(fieldnames, "VALUE")
    dguid_col = "DGUID" if "DGUID" in fieldnames else _find_column(fieldnames, "DGUID")

    employment_values = sorted({(row.get(employment_col) or "").strip() for row in rows})
    total_employment_values = [
        value for value in employment_values
        if value.strip().lower() == "total, with employees"
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
    diagnostics: dict[str, list[dict[str, str]]] = {}

    for jurisdiction, (city, province_uid) in TARGETS.items():
        city_rows = {
            ((row.get(geo_col) or "").strip(), (row.get(dguid_col) or "").strip())
            for row in rows
            if (row.get(geo_col) or "").strip().lower() == city.lower()
        }
        diagnostics[jurisdiction] = [
            {"geo": geo, "dguid": dguid} for geo, dguid in sorted(city_rows)
        ]
        csd_candidates = [
            (geo, dguid) for geo, dguid in sorted(city_rows)
            if _is_csd_dguid(dguid, province_uid)
        ]
        if len(csd_candidates) != 1:
            raise RuntimeError(
                f"Could not uniquely identify CSD for {jurisdiction}; "
                f"city_rows={sorted(city_rows)}; csd_candidates={csd_candidates}"
            )
        chosen_geo, chosen_dguid = csd_candidates[0]

        by_code: dict[str, float] = {}
        labels: dict[str, str] = {}
        for row in rows:
            if (row.get(dguid_col) or "").strip() != chosen_dguid:
                continue
            if (row.get(employment_col) or "").strip() != total_employment:
                continue
            label = (row.get(naics_col) or "").strip()
            code = _extract_code(label)
            value = _numeric_value(row, value_col)
            if code and value is not None:
                by_code[code] = value
                labels[code] = label

        try:
            layers = _layer_totals(by_code)
        except RuntimeError as exc:
            nearby_labels = sorted({
                (row.get(naics_col) or "").strip()
                for row in rows
                if (row.get(dguid_col) or "").strip() == chosen_dguid
                and (row.get(employment_col) or "").strip() == total_employment
                and any(token in (row.get(naics_col) or "").lower() for token in (
                    "construction", "residential", "building equipment", "foundation"
                ))
            })
            raise RuntimeError(
                f"{jurisdiction}: {exc}; raw_nearby_labels={nearby_labels[:80]}"
            ) from exc

        results[jurisdiction] = {
            "geo": chosen_geo,
            "dguid": chosen_dguid,
            "layers": layers,
            "component_naics": {
                code: {"label": labels[code], "employer_locations": int(by_code[code])}
                for code in REQUIRED_CODES
            },
        }

    totals = {
        layer: sum(item["layers"][layer] for item in results.values())
        for layer in LAYER_CODES
    }
    penetration = {
        layer: {
            "125_accounts_pct": round(125 / denominator * 100, 3) if denominator else None,
            "400_accounts_pct": round(400 / denominator * 100, 3) if denominator else None,
            "500_accounts_pct": round(500 / denominator * 100, 3) if denominator else None,
        }
        for layer, denominator in totals.items()
    }
    return {
        "source_table": "33-10-1176-01",
        "source_url": _table_url(MUNICIPAL_TABLE_ID),
        "employment_size_filter": total_employment,
        "cities": results,
        "totals": totals,
        "penetration_required": penetration,
        "geo_match_diagnostics": diagnostics,
    }


def _province_code_counts(
    table_id: str,
    province: str,
    require_total_employment: bool,
) -> dict[str, float]:
    rows, fieldnames = _download_rows(table_id)
    geo_col = _find_column(fieldnames, "GEO")
    naics_col = _find_column(fieldnames, "North American Industry Classification System")
    value_col = "VALUE" if "VALUE" in fieldnames else _find_column(fieldnames, "VALUE")
    employment_col = _find_column(fieldnames, "Employment size") if require_total_employment else None

    matches: dict[str, list[float]] = {code: [] for code in REQUIRED_CODES}
    for row in rows:
        if (row.get(geo_col) or "").strip().lower() != province.lower():
            continue
        if employment_col and (row.get(employment_col) or "").strip().lower() != "total, with employees":
            continue
        code = _extract_code((row.get(naics_col) or "").strip())
        if code not in matches:
            continue
        value = _numeric_value(row, value_col)
        if value is not None:
            matches[code].append(value)

    ambiguous = {code: values for code, values in matches.items() if len(values) != 1}
    if ambiguous:
        raise RuntimeError(
            f"Table {table_id}, province {province}: expected one value per required NAICS code; "
            f"got {ambiguous}; fieldnames={fieldnames}"
        )
    return {code: values[0] for code, values in matches.items()}


def _provincial_nonemployer_sensitivity() -> dict:
    result: dict[str, dict] = {}
    for province in PROVINCES:
        with_emp = _province_code_counts(PROV_EMPLOYER_TABLE_ID, province, True)
        without_emp = _province_code_counts(PROV_NONEMPLOYER_TABLE_ID, province, False)
        with_layers = _layer_totals(with_emp)
        without_layers = _layer_totals(without_emp)

        layers: dict[str, dict] = {}
        for layer in LAYER_CODES:
            employer = with_layers[layer]
            nonemployer = without_layers[layer]
            combined = employer + nonemployer
            layers[layer] = {
                "with_employee_locations": employer,
                "without_employee_locations": nonemployer,
                "without_to_with_ratio": round(nonemployer / employer, 3) if employer else None,
                "without_share_of_combined_pct": round(nonemployer / combined * 100, 2) if combined else None,
            }
        result[province] = {"layers": layers}
    return {
        "with_employees_source_table": "33-10-1174-01",
        "without_employees_source_table": "33-10-1175-01",
        "important_boundary": (
            "Province-level sensitivity only. Do not multiply municipal CSD employer counts by these ratios "
            "and present the result as an observed municipal count."
        ),
        "provinces": result,
    }


def summarize() -> dict:
    municipal = _municipal_employer_counts()
    return {
        "reference_period": "June 2026",
        "unit": "statistical business locations",
        "layer_definitions": LAYER_CODES,
        "municipal_employer_lower_bound": municipal,
        "provincial_nonemployer_sensitivity": _provincial_nonemployer_sensitivity(),
        "important_boundary": (
            "Municipal counts are observed CSD locations with employees. Province-level without-employee "
            "ratios quantify the missing-pool scale only and are not municipal SAM estimates."
        ),
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
