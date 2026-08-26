"""Jurisdiction dispatcher for the growing ProjectPermit ruleset."""
from __future__ import annotations

from typing import Any

from .engine import evaluate_project as evaluate_phase0_project
from .expansion_rules import evaluate_expansion_project

SUPPORTED_JURISDICTIONS = (
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
)


def evaluate_project(facts: dict[str, Any]) -> dict[str, Any]:
    expanded = evaluate_expansion_project(facts)
    if expanded is not None:
        return expanded
    return evaluate_phase0_project(facts)
