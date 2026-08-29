"""Safe writeback proposal wrappers for existing read-only field-service adapters.

These helpers do not call external APIs. They combine the existing Jobber/ServiceM8
proposal mappers with ProjectPermit's mutation gate so an authorized caller can see
whether the proposal is ready for an explicit idempotent upsert, is a duplicate no-op,
or must remain blocked.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .jobber_adapter import build_jobber_action_proposal
from .mutation_gate import READY_FOR_EXPLICIT_WRITE
from .servicem8_adapter import build_servicem8_action_proposal


def _gate(result: Mapping[str, Any]) -> dict[str, Any]:
    bundle = result.get("action_bundle")
    if not isinstance(bundle, Mapping):
        raise ValueError("ProjectPermit result.action_bundle is required")
    gate = bundle.get("mutation_gate")
    if not isinstance(gate, Mapping):
        raise ValueError("ProjectPermit action_bundle.mutation_gate is required")
    return deepcopy(dict(gate))


def _decorate(proposal: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    proposal["mutation_gate"] = gate
    proposal["writeback_ready"] = gate.get("state") == READY_FOR_EXPLICIT_WRITE
    proposal["proposed_operation"] = str(gate.get("recommended_operation") or "NONE")
    proposal["mutation_performed"] = False
    return proposal


def build_jobber_safe_writeback_proposal(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a Jobber proposal plus the platform-neutral safe mutation gate."""
    return _decorate(build_jobber_action_proposal(result), _gate(result))


def build_servicem8_safe_writeback_proposal(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a ServiceM8 proposal plus the platform-neutral safe mutation gate."""
    return _decorate(build_servicem8_action_proposal(result), _gate(result))
