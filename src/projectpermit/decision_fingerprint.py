from __future__ import annotations

import hashlib
import json
from typing import Any


DECISION_FINGERPRINT_VERSION = 1
DECISION_FINGERPRINT_PREFIX = "ppdf-v1:"


def _json_safe(value: Any) -> Any:
    """Convert decision material into a deterministic JSON-compatible structure."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, set):
        normalized = [_json_safe(item) for item in value]
        return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return str(value)


def _requirement_material(requirement: dict[str, Any]) -> dict[str, Any]:
    evidence = []
    for item in requirement.get("evidence") or []:
        evidence.append(
            {
                "source_id": str(item.get("source_id") or ""),
                "url": str(item.get("url") or ""),
            }
        )
    evidence.sort(key=lambda item: (item["source_id"], item["url"]))

    return {
        "type": str(requirement.get("type") or ""),
        "status": str(requirement.get("status") or ""),
        "rule_id": str(requirement.get("rule_id") or ""),
        "rule_version": str(requirement.get("rule_version") or ""),
        "source_verified_at": str(requirement.get("source_verified_at") or ""),
        "evidence": evidence,
    }


def build_decision_material(facts: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Return the non-PII material that defines one ProjectPermit decision.

    Deliberately excluded:
    - raw civic address
    - address-resolution metadata/coordinates/property identifiers
    - context/client_tag/transport metadata
    - telemetry/request ids

    Address-derived property facts are included because they can change the actual
    determination. This makes the fingerprint useful for cache/audit/replay without
    turning the raw address into a stable identifier.
    """
    requirements = [
        _requirement_material(requirement)
        for requirement in (result.get("requirements") or [])
        if isinstance(requirement, dict)
    ]
    requirements.sort(
        key=lambda item: (
            item["rule_id"],
            item["type"],
            item["status"],
            item["rule_version"],
            item["source_verified_at"],
            json.dumps(item["evidence"], sort_keys=True, separators=(",", ":")),
        )
    )

    required_property_facts = sorted(
        str(item) for item in (result.get("required_property_facts") or [])
    )

    material = {
        "fingerprint_version": DECISION_FINGERPRINT_VERSION,
        "jurisdiction": str(facts.get("jurisdiction") or ""),
        "project": _json_safe(facts.get("project") or {}),
        "property": _json_safe(facts.get("property") or {}),
        "decision": {
            "determination": str(result.get("determination") or ""),
            "confidence": str(result.get("confidence") or ""),
            "engine_version": str(result.get("engine_version") or ""),
            "property_context_status": result.get("property_context_status"),
            "required_property_facts": required_property_facts,
            "requirements": requirements,
        },
    }
    return _json_safe(material)


def compute_decision_fingerprint(facts: dict[str, Any], result: dict[str, Any]) -> str:
    material = build_decision_material(facts, result)
    encoded = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return DECISION_FINGERPRINT_PREFIX + digest
