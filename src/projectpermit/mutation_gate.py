"""Deterministic safety gate for downstream field-service writeback.

ProjectPermit itself does not execute Jobber/ServiceM8 mutations here. The gate
classifies an action bundle so an authorized integration can decide whether to
perform an explicit idempotent upsert, suppress a duplicate, or block writeback.

This is a product automation policy, not municipal authorization or legal advice.
"""
from __future__ import annotations

from typing import Any, Mapping


MUTATION_GATE_VERSION = "2026-08-29.1"

READY_FOR_EXPLICIT_WRITE = "READY_FOR_EXPLICIT_WRITE"
NOOP_UNCHANGED = "NOOP_UNCHANGED"
BLOCKED = "BLOCKED"


def _text(value: Any) -> str:
    return str(value or "").strip()


def build_mutation_gate(
    bundle: Mapping[str, Any],
    *,
    prior_identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify whether an action bundle is safe for an explicit downstream write.

    The gate never performs a mutation. Callers must still explicitly request and
    authorize any write. When READY, the required integration behavior is an atomic
    idempotent upsert keyed by `idempotency_key`, never an unconditional create.
    """
    identity = bundle.get("identity")
    if not isinstance(identity, Mapping):
        identity = {}
    change = bundle.get("change")
    if not isinstance(change, Mapping):
        change = {}
    routing = bundle.get("routing")
    if not isinstance(routing, Mapping):
        routing = {}
    freshness = routing.get("evidence_freshness")
    if not isinstance(freshness, Mapping):
        freshness = {}
    required_inputs = bundle.get("required_inputs")
    if not isinstance(required_inputs, list):
        required_inputs = []

    idempotency_key = _text(identity.get("idempotency_key"))
    scope_fingerprint = _text(identity.get("scope_fingerprint"))
    classification = _text(change.get("classification")) or "UNKNOWN"
    prior_idempotency_key = (
        _text(prior_identity.get("idempotency_key"))
        if isinstance(prior_identity, Mapping)
        else ""
    )
    same_idempotency_key = bool(
        idempotency_key
        and prior_idempotency_key
        and idempotency_key == prior_idempotency_key
    )

    blockers: list[str] = []
    if not idempotency_key:
        blockers.append("MISSING_IDEMPOTENCY_KEY")
    if not scope_fingerprint:
        blockers.append("MISSING_WORK_RECORD_SCOPE")
    if not bool(routing.get("automation_safe", False)):
        blockers.append("AUTOMATION_NOT_SAFE")
    if _text(freshness.get("status")) != "CURRENT":
        blockers.append("EVIDENCE_NOT_CURRENT")
    if required_inputs:
        blockers.append("REQUIRED_INPUTS_PENDING")

    if classification == "UNCHANGED" and not blockers:
        state = NOOP_UNCHANGED
        mutation_allowed = False
        recommended_operation = "NOOP"
        reason_codes = ["DUPLICATE_SUPPRESSED"]
    elif blockers:
        state = BLOCKED
        mutation_allowed = False
        recommended_operation = "NONE"
        reason_codes = blockers
    else:
        state = READY_FOR_EXPLICIT_WRITE
        mutation_allowed = True
        if same_idempotency_key and classification in {
            "RULESET_CHANGED",
            "EVIDENCE_REFRESHED",
        }:
            recommended_operation = "UPSERT_METADATA"
            reason_codes = ["SAME_OPERATIONAL_ROUTE_METADATA_REFRESH"]
        else:
            recommended_operation = "UPSERT_OPERATIONAL_ROUTE"
            reason_codes = ["SAFETY_GUARDS_PASSED"]

    return {
        "gate_version": MUTATION_GATE_VERSION,
        "state": state,
        "mutation_allowed": mutation_allowed,
        "execution_requires_explicit_request": True,
        "recommended_operation": recommended_operation,
        "reason_codes": reason_codes,
        "idempotency": {
            "mode": "ATOMIC_UPSERT",
            "idempotency_key": idempotency_key or None,
            "scope_fingerprint": scope_fingerprint or None,
            "prior_same_key": same_idempotency_key,
            "unconditional_create_allowed": False,
        },
        "safeguards": {
            "automation_safe": bool(routing.get("automation_safe", False)),
            "evidence_freshness": _text(freshness.get("status")) or "UNKNOWN",
            "required_inputs_pending": bool(required_inputs),
            "change_classification": classification,
        },
        "execution_note": (
            "ProjectPermit has not performed a mutation. An authorized integration may "
            "execute only when state=READY_FOR_EXPLICIT_WRITE and must upsert atomically "
            "by idempotency_key."
        ),
    }
