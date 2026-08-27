"""Audit which de-identified property facts actually affect jurisdiction rules.

This static audit distinguishes address/GIS adapter capability from rule-engine
consumption. A municipality can have a rich address adapter while its current
permit-applicability rules never read the derived property fields.

Internal technical/commercial-structure evidence only; not E2/E3/E4/E5.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "gatineau_qc": (ROOT / "src/projectpermit/engine.py", "_evaluate_gatineau"),
    "ottawa_on": (ROOT / "src/projectpermit/engine.py", "_evaluate_ottawa"),
    "toronto_on": (ROOT / "src/projectpermit/expansion_rules.py", "evaluate_toronto"),
    "mississauga_on": (ROOT / "src/projectpermit/expansion_rules.py", "evaluate_mississauga"),
    "laval_qc": (ROOT / "src/projectpermit/quebec_expansion_rules.py", "evaluate_laval"),
    "longueuil_qc": (ROOT / "src/projectpermit/quebec_expansion_rules.py", "evaluate_longueuil"),
    "vancouver_bc": (ROOT / "src/projectpermit/vancouver_rules.py", "evaluate_vancouver"),
}

ADDRESS_ADAPTER_JURISDICTIONS = {
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "vancouver_bc",
}


def _find_function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError(f"function not found: {name}")


def _property_aliases(fn: ast.FunctionDef) -> set[str]:
    aliases: set[str] = set()
    for node in ast.walk(fn):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        value = node.value
        if not isinstance(target, ast.Name):
            continue
        if not isinstance(value, ast.Call) or not isinstance(value.func, ast.Attribute):
            continue
        if value.func.attr != "get" or not isinstance(value.func.value, ast.Name):
            continue
        if value.func.value.id != "facts" or not value.args:
            continue
        first = value.args[0]
        if isinstance(first, ast.Constant) and first.value == "property":
            aliases.add(target.id)
    return aliases


def _consumed_keys(fn: ast.FunctionDef, aliases: set[str]) -> set[str]:
    keys: set[str] = set()
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "get" or not isinstance(node.func.value, ast.Name):
            continue
        if node.func.value.id not in aliases or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            keys.add(first.value)
    return keys


def run() -> dict:
    jurisdictions = {}
    consuming = 0
    address_adapter_consuming = 0

    for jurisdiction, (path, function_name) in TARGETS.items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        fn = _find_function(tree, function_name)
        aliases = _property_aliases(fn)
        keys = sorted(_consumed_keys(fn, aliases))
        has_adapter = jurisdiction in ADDRESS_ADAPTER_JURISDICTIONS
        if keys:
            consuming += 1
            if has_adapter:
                address_adapter_consuming += 1
        jurisdictions[jurisdiction] = {
            "rule_file": str(path.relative_to(ROOT)),
            "function": function_name,
            "has_address_adapter": has_adapter,
            "property_aliases": sorted(aliases),
            "consumed_property_keys": keys,
            "consumes_property_facts": bool(keys),
        }

    adapter_count = len(ADDRESS_ADAPTER_JURISDICTIONS)
    return {
        "evidence_boundary": (
            "Static source audit only. It measures property fields referenced by current deterministic "
            "jurisdiction evaluators; it does not measure how often those fields occur in real projects, "
            "whether adapters resolve them successfully, or willingness to pay for address-aware calls."
        ),
        "jurisdiction_count": len(TARGETS),
        "jurisdictions_consuming_property_facts": consuming,
        "jurisdictions_with_address_adapters": adapter_count,
        "address_adapter_jurisdictions_consuming_property_facts": address_adapter_consuming,
        "address_adapter_consumption_share_pct": round(
            address_adapter_consuming / adapter_count * 100, 2
        ) if adapter_count else None,
        "jurisdictions": jurisdictions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("property_fact_consumption_audit.json")
    )
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
