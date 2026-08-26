"""Privacy-minimal structured usage telemetry for market validation.

The event intentionally excludes civic address, coordinates, property identifiers,
raw project text, payment credentials and IP/user-agent data. A caller-provided
`context.client_tag` is hashed before logging so repeated integrations can be grouped
without persisting the tag itself.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


INTERNAL_TAGS = {
    "projectpermit-ci",
    "projectpermit-owner-smoke",
}


def _hash_client_tag(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def emit_preflight_event(facts: dict[str, Any], result: dict[str, Any]) -> None:
    """Write one machine-readable, non-PII usage event to stdout."""
    context = facts.get("context") or {}
    client_tag = str(context.get("client_tag") or "").strip()
    transport = str(context.get("_transport") or "unknown").strip() or "unknown"
    project = facts.get("project") or {}

    event = {
        "event": "projectpermit_preflight",
        "event_version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid4()),
        "transport": transport,
        "jurisdiction": str(facts.get("jurisdiction") or ""),
        "project_family": str(project.get("family") or ""),
        "resolve_address": bool(facts.get("resolve_address")),
        "determination": str(result.get("determination") or ""),
        "confidence": str(result.get("confidence") or ""),
        "requirements_count": len(result.get("requirements") or []),
        "client_tag_hash": _hash_client_tag(client_tag),
        "internal_traffic": client_tag in INTERNAL_TAGS,
    }
    print("PROJECTPERMIT_USAGE " + json.dumps(event, sort_keys=True), flush=True)
