"""PII-minimal deterministic identity for ProjectPermit decisions.

These fingerprints support duplicate suppression and change detection in downstream
contractor/field-service agents. They are product identity hashes, not signatures,
legal attestations, authentication tokens, or proof of municipal authorization.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


IDENTITY_VERSION = "2026-08-29.1"

# These keys can contain caller/platform correlation or personal data and therefore
# never participate in the reusable permit-decision input fingerprint. Project and
# property facts remain included because they materially drive deterministic rules.
_EXCLUDED_FACT_KEYS = {
    "address",
    "context",
    "client_ref",
    "source_object_id",
    "source_object_type",
    "source_platform",
}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _canonical(value: Any) -> Any:
    """Return a JSON-stable representation with mapping keys sorted by serialization."""
    if isinstance(value, Mapping):
        return {
            str(key): _canonical(item)
            for key, item in value.items()
            if str(key) not in _EXCLUDED_FACT_KEYS
        }
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _digest(prefix: str, payload: Any) -> str:
    rendered = json.dumps(
        _canonical(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(rendered).hexdigest()[:32]}"


def _scope_fingerprint(facts: Mapping[str, Any]) -> str | None:
    """Hash optional work-record scope without exposing raw platform identifiers."""
    context = facts.get("context")
    if not isinstance(context, Mapping):
        return None

    explicit_scope = _text(context.get("idempotency_scope"))
    if explicit_scope:
        return _digest("pps", {"scope": explicit_scope})

    platform = _text(context.get("source_platform"))
    object_type = _text(context.get("source_object_type"))
    object_id = _text(context.get("source_object_id"))
    if not object_id:
        return None
    return _digest(
        "pps",
        {
            "platform": platform,
            "object_type": object_type,
            "object_id": object_id,
        },
    )


def build_decision_identity(
    facts: Mapping[str, Any],
    result: Mapping[str, Any],
    *,
    evidence: list[dict[str, Any]],
    audit: Mapping[str, Any],
) -> dict[str, Any]:
    """Build stable component fingerprints and an integration idempotency key.

    Decision fingerprints exclude raw address and caller/platform context. The
    idempotency key may be scoped to a work record using a one-way hash of the
    caller's source object id (or explicit context.idempotency_scope), preventing
    identical permit scopes on different jobs from colliding without returning the
    raw identifier.
    """
    workflow = result.get("workflow")
    if not isinstance(workflow, Mapping):
        raise ValueError("ProjectPermit result.workflow is required for decision identity")

    reusable_input = {
        "jurisdiction": facts.get("jurisdiction"),
        "project": facts.get("project") if isinstance(facts.get("project"), Mapping) else {},
        "property": facts.get("property") if isinstance(facts.get("property"), Mapping) else {},
    }
    input_fingerprint = _digest("ppi", reusable_input)

    decision_fingerprint = _digest(
        "ppd",
        {
            "determination": _text(result.get("determination")),
            "confidence": _text(result.get("confidence")),
        },
    )
    routing_fingerprint = _digest(
        "ppr",
        {
            "recommended_route": _text(workflow.get("recommended_route")),
            "quote_handling": _text(workflow.get("quote_handling")),
            "automation_safe": bool(workflow.get("automation_safe", False)),
            "freshness_status": _text(
                (workflow.get("evidence_freshness") or {}).get("status")
                if isinstance(workflow.get("evidence_freshness"), Mapping)
                else ""
            ),
        },
    )
    ruleset_fingerprint = _digest(
        "pprules",
        {
            "engine_version": _text(audit.get("engine_version")),
            "rule_ids": audit.get("rule_ids") or [],
            "rule_versions": audit.get("rule_versions") or [],
        },
    )
    evidence_fingerprint = _digest(
        "ppe",
        [
            {
                "source_id": _text(item.get("source_id")),
                "url": _text(item.get("url")),
                "rule_ids": item.get("rule_ids") or [],
                "source_verified_at": item.get("source_verified_at"),
            }
            for item in evidence
            if isinstance(item, Mapping)
        ],
    )

    scope_fingerprint = _scope_fingerprint(facts)
    idempotency_key = _digest(
        "ppidem",
        {
            "identity_version": IDENTITY_VERSION,
            "scope_fingerprint": scope_fingerprint,
            "input_fingerprint": input_fingerprint,
            "decision_fingerprint": decision_fingerprint,
            "routing_fingerprint": routing_fingerprint,
            "ruleset_fingerprint": ruleset_fingerprint,
            "evidence_fingerprint": evidence_fingerprint,
        },
    )
    bundle_id = _digest(
        "ppb",
        {
            "identity_version": IDENTITY_VERSION,
            "input_fingerprint": input_fingerprint,
            "decision_fingerprint": decision_fingerprint,
            "routing_fingerprint": routing_fingerprint,
            "ruleset_fingerprint": ruleset_fingerprint,
            "evidence_fingerprint": evidence_fingerprint,
        },
    )

    return {
        "identity_version": IDENTITY_VERSION,
        "bundle_id": bundle_id,
        "input_fingerprint": input_fingerprint,
        "decision_fingerprint": decision_fingerprint,
        "routing_fingerprint": routing_fingerprint,
        "ruleset_fingerprint": ruleset_fingerprint,
        "evidence_fingerprint": evidence_fingerprint,
        "scope_fingerprint": scope_fingerprint,
        "idempotency_key": idempotency_key,
    }


def classify_identity_change(
    previous: Mapping[str, Any] | None,
    current: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare a prior public identity object with the current one.

    The primary classification is impact-prioritized while `reasons` preserves all
    changed components so integrations can choose their own policy.
    """
    if not isinstance(previous, Mapping) or not _text(previous.get("bundle_id")):
        return {
            "classification": "FIRST_OBSERVATION",
            "material_change": True,
            "reasons": ["NO_PRIOR_IDENTITY"],
            "prior_bundle_id": None,
        }

    previous_bundle_id = _text(previous.get("bundle_id"))
    if previous_bundle_id == _text(current.get("bundle_id")):
        return {
            "classification": "UNCHANGED",
            "material_change": False,
            "reasons": [],
            "prior_bundle_id": previous_bundle_id,
        }

    components = (
        ("decision_fingerprint", "DECISION_CHANGED"),
        ("routing_fingerprint", "ROUTE_CHANGED"),
        ("input_fingerprint", "INPUT_CHANGED"),
        ("ruleset_fingerprint", "RULESET_CHANGED"),
        ("evidence_fingerprint", "EVIDENCE_REFRESHED"),
    )
    reasons = [
        reason
        for field, reason in components
        if _text(previous.get(field)) != _text(current.get(field))
    ]

    classification = reasons[0] if reasons else "IDENTITY_VERSION_CHANGED"
    return {
        "classification": classification,
        "material_change": True,
        "reasons": reasons or ["IDENTITY_VERSION_CHANGED"],
        "prior_bundle_id": previous_bundle_id,
    }
