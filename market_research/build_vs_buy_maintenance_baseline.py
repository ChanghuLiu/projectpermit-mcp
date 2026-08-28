"""Measure the maintained surface behind ProjectPermit's permit-specific capability.

This audit is intentionally a repository-maintenance proxy, not an estimate of
engineering hours, dollars, willingness to pay, or competitive moat.  It separates
permit-rule/source/test maintenance from unrelated distribution, payment, MCP and
FSM-adapter code so build-vs-buy discussions do not overstate the product surface.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

JURISDICTIONS = {
    "GAT": "gatineau_qc",
    "OTT": "ottawa_on",
    "TOR": "toronto_on",
    "MIS": "mississauga_on",
    "LAV": "laval_qc",
    "LON": "longueuil_qc",
    "VAN": "vancouver_bc",
}

RULE_FILES = [
    "src/projectpermit/engine.py",
    "src/projectpermit/expansion_rules.py",
    "src/projectpermit/quebec_expansion_rules.py",
    "src/projectpermit/vancouver_rules.py",
    "src/projectpermit/overlay_safety.py",
    "src/projectpermit/jurisdiction_router.py",
]

PROPERTY_CONTEXT_FILES = [
    "src/projectpermit/address.py",
    "src/projectpermit/mississauga_address.py",
    "src/projectpermit/vancouver_address.py",
    "src/projectpermit/overlay_safety.py",
]

SOURCE_MAINTENANCE_FILES = [
    "src/projectpermit/source_watch.py",
    "market_research/property_fact_consumption_audit.py",
    "market_research/property_overlay_flip_matrix.py",
    "market_research/property_overlay_unknown_safety_audit.py",
    ".github/workflows/property-fact-consumption-audit.yml",
]

CONTRACT_FILES = [
    "schemas/request.schema.json",
    "schemas/response.schema.json",
    "src/projectpermit/api.py",
    "src/projectpermit/preflight_service.py",
]

CORE_TEST_FILES = [
    "tests/test_address.py",
    "tests/test_api.py",
    "tests/test_expansion_rules.py",
    "tests/test_overlay_safety.py",
    "tests/test_preflight_service.py",
    "tests/test_public_permit_positive_backtest.py",
    "tests/test_quebec_expansion_rules.py",
    "tests/test_schema_contract.py",
    "tests/test_source_manifest.py",
    "tests/test_source_watch.py",
    "tests/test_vancouver_rules.py",
]

EXPLICITLY_EXCLUDED_FROM_CORE_CLONE = [
    "Jobber / ServiceM8 adapters and clients",
    "MCP servers and registry/distribution packaging",
    "x402/payment configuration and paid smoke tests",
    "telemetry/usage analytics",
    "market-size/permit-volume research scripts",
    "outreach and partner-validation documents",
]

RULE_ID_RE = re.compile(
    r"\b(?P<prefix>GAT|OTT|TOR|MIS|LAV|LON|VAN)-[A-Z0-9]+(?:-[A-Z0-9]+)+\b"
)


def _path(path: str) -> Path:
    result = ROOT / path
    if not result.exists():
        raise FileNotFoundError(path)
    return result


def _file_metrics(paths: Iterable[str]) -> dict:
    unique = list(dict.fromkeys(paths))
    physical = 0
    nonblank = 0
    byte_count = 0
    per_file = []
    for rel in unique:
        p = _path(rel)
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        row = {
            "path": rel,
            "bytes": p.stat().st_size,
            "physical_lines": len(lines),
            "nonblank_lines": sum(1 for line in lines if line.strip()),
        }
        per_file.append(row)
        physical += row["physical_lines"]
        nonblank += row["nonblank_lines"]
        byte_count += row["bytes"]
    return {
        "file_count": len(unique),
        "bytes": byte_count,
        "physical_lines": physical,
        "nonblank_lines": nonblank,
        "files": per_file,
    }


def _rule_ids() -> dict:
    by_jurisdiction = {jurisdiction: set() for jurisdiction in JURISDICTIONS.values()}
    all_ids: set[str] = set()
    for rel in RULE_FILES:
        text = _path(rel).read_text(encoding="utf-8")
        for match in RULE_ID_RE.finditer(text):
            rule_id = match.group(0)
            jurisdiction = JURISDICTIONS[match.group("prefix")]
            all_ids.add(rule_id)
            by_jurisdiction[jurisdiction].add(rule_id)
    return {
        "unique_rule_id_count": len(all_ids),
        "by_jurisdiction": {
            jurisdiction: {
                "count": len(ids),
                "rule_ids": sorted(ids),
            }
            for jurisdiction, ids in by_jurisdiction.items()
        },
    }


def _sources() -> dict:
    manifest = json.loads(_path("data/source_manifest.json").read_text(encoding="utf-8"))
    by_jurisdiction = {jurisdiction: [] for jurisdiction in JURISDICTIONS.values()}
    unknown_prefixes: list[str] = []
    for source in manifest["sources"]:
        source_id = source["source_id"]
        prefix = source_id.split("_", 1)[0]
        jurisdiction = JURISDICTIONS.get(prefix)
        if jurisdiction is None:
            unknown_prefixes.append(source_id)
            continue
        by_jurisdiction[jurisdiction].append(source)
    return {
        "manifest_version": manifest.get("manifest_version"),
        "verified_at": manifest.get("verified_at"),
        "official_source_count": len(manifest["sources"]),
        "by_jurisdiction": {
            jurisdiction: {
                "count": len(items),
                "critical_count": sum(1 for item in items if item.get("criticality") == "critical"),
                "source_ids": [item["source_id"] for item in items],
            }
            for jurisdiction, items in by_jurisdiction.items()
        },
        "unknown_prefix_source_ids": unknown_prefixes,
    }


def run() -> dict:
    sources = _sources()
    rules = _rule_ids()
    rule_surface = _file_metrics(RULE_FILES)
    property_surface = _file_metrics(PROPERTY_CONTEXT_FILES)
    maintenance_surface = _file_metrics(SOURCE_MAINTENANCE_FILES)
    contract_surface = _file_metrics(CONTRACT_FILES)
    test_surface = _file_metrics(CORE_TEST_FILES)

    shared_safe_paths = list(
        dict.fromkeys(
            RULE_FILES
            + PROPERTY_CONTEXT_FILES
            + SOURCE_MAINTENANCE_FILES
            + CONTRACT_FILES
            + CORE_TEST_FILES
            + ["data/source_manifest.json"]
        )
    )
    shared_safe_surface = _file_metrics(shared_safe_paths)

    one_city_proxy = {}
    for jurisdiction in JURISDICTIONS.values():
        one_city_proxy[jurisdiction] = {
            "rule_id_count": rules["by_jurisdiction"][jurisdiction]["count"],
            "official_source_count": sources["by_jurisdiction"][jurisdiction]["count"],
            "critical_source_count": sources["by_jurisdiction"][jurisdiction]["critical_count"],
            "note": (
                "A one-city LOC figure is intentionally not reported because several Python modules "
                "share helpers and multiple jurisdictions. Rule/source counts are the safer city-level proxy."
            ),
        }

    result = {
        "evidence_boundary": (
            "Repository maintenance-surface proxy only. LOC, file counts, rule IDs and official-source counts "
            "do not equal engineering hours, cost, accuracy, willingness to pay, or moat."
        ),
        "jurisdiction_count": len(JURISDICTIONS),
        "official_sources": sources,
        "deterministic_rules": rules,
        "layers": {
            "one_city_proxy": one_city_proxy,
            "multi_city_deterministic_rule_surface": rule_surface,
            "property_context_and_overlay_surface": property_surface,
            "source_and_overlay_maintenance_surface": maintenance_surface,
            "machine_contract_surface": contract_surface,
            "core_correctness_test_surface": test_surface,
            "safe_shared_api_union_surface": shared_safe_surface,
        },
        "explicitly_excluded_from_core_clone": EXPLICITLY_EXCLUDED_FROM_CORE_CLONE,
        "interpretation_rules": [
            "A small one-city rule/source count supports the hypothesis that a narrow local checker can be cheap to internalize.",
            "A larger cross-city source/rule/test surface supports only a maintenance-burden hypothesis; buyer preference must still be observed.",
            "Do not count FSM adapters, MCP, x402, distribution or market-research code as permit-domain moat.",
            "Do not convert LOC to hours or dollars without external evidence.",
        ],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")

    print("=== ProjectPermit build-vs-buy maintenance baseline ===")
    print(f"jurisdictions={result['jurisdiction_count']}")
    print(f"official_sources={result['official_sources']['official_source_count']}")
    print(f"unique_rule_ids={result['deterministic_rules']['unique_rule_id_count']}")
    for jurisdiction, row in result["layers"]["one_city_proxy"].items():
        print(
            f"city={jurisdiction} rule_ids={row['rule_id_count']} "
            f"sources={row['official_source_count']} critical_sources={row['critical_source_count']}"
        )
    for name in (
        "multi_city_deterministic_rule_surface",
        "property_context_and_overlay_surface",
        "source_and_overlay_maintenance_surface",
        "machine_contract_surface",
        "core_correctness_test_surface",
        "safe_shared_api_union_surface",
    ):
        row = result["layers"][name]
        print(
            f"layer={name} files={row['file_count']} physical_lines={row['physical_lines']} "
            f"nonblank_lines={row['nonblank_lines']} bytes={row['bytes']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
