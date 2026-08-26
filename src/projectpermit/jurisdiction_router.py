"""Jurisdiction dispatcher for the growing ProjectPermit ruleset."""
from __future__ import annotations

from typing import Any

from .engine import evaluate_project as evaluate_phase0_project
from .expansion_rules import evaluate_expansion_project
from .quebec_expansion_rules import evaluate_quebec_expansion_project
from .vancouver_rules import evaluate_vancouver_project

SUPPORTED_JURISDICTIONS = (
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "laval_qc",
    "longueuil_qc",
    "vancouver_bc",
)


def evaluate_project(facts: dict[str, Any]) -> dict[str, Any]:
    expanded = evaluate_expansion_project(facts)
    if expanded is not None:
        return expanded
    expanded_qc = evaluate_quebec_expansion_project(facts)
    if expanded_qc is not None:
        return expanded_qc
    expanded_bc = evaluate_vancouver_project(facts)
    if expanded_bc is not None:
        return expanded_bc
    return evaluate_phase0_project(facts)
