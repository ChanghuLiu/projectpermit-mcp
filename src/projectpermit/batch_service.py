from __future__ import annotations

from collections import Counter
from typing import Any

from .preflight_service import run_preflight


MAX_BATCH_ITEMS = 50

_ALLOWED_ITEM_FIELDS = {
    "client_ref",
    "jurisdiction",
    "project",
    "address",
    "property",
    "context",
    "resolve_address",
}


def _normalize_item(item: Any, *, allow_address: bool, transport: str) -> tuple[str | None, dict[str, Any]]:
    if not isinstance(item, dict):
        raise ValueError("batch item must be an object")

    unknown = sorted(set(item) - _ALLOWED_ITEM_FIELDS)
    if unknown:
        raise ValueError("unsupported batch item fields: " + ", ".join(unknown))

    client_ref = item.get("client_ref")
    if client_ref is not None:
        client_ref = str(client_ref)
        if len(client_ref) > 200:
            raise ValueError("client_ref must be at most 200 characters")

    jurisdiction = str(item.get("jurisdiction") or "").strip()
    if not jurisdiction:
        raise ValueError("jurisdiction is required")

    project = item.get("project")
    if not isinstance(project, dict) or not project:
        raise ValueError("project must be a non-empty object")

    property_facts = item.get("property") or {}
    if not isinstance(property_facts, dict):
        raise ValueError("property must be an object")

    context = item.get("context") or {}
    if not isinstance(context, dict):
        raise ValueError("context must be an object")

    if not allow_address and ("address" in item or "resolve_address" in item):
        raise ValueError("anonymous batch preview does not accept address or resolve_address")

    facts = {
        "jurisdiction": jurisdiction,
        "project": project,
        "address": item.get("address") if allow_address else None,
        "property": property_facts,
        "context": {**context, "_transport": transport},
        "resolve_address": bool(item.get("resolve_address", False)) if allow_address else False,
    }
    return client_ref, facts


def _build_audit(successful_results: list[dict[str, Any]]) -> dict[str, Any]:
    engine_versions: set[str] = set()
    rule_ids: set[str] = set()
    verified_dates: list[str] = []
    evidence_links = 0

    for result in successful_results:
        engine_version = str(result.get("engine_version") or "").strip()
        if engine_version:
            engine_versions.add(engine_version)
        for requirement in result.get("requirements") or []:
            rule_id = str(requirement.get("rule_id") or "").strip()
            if rule_id:
                rule_ids.add(rule_id)
            source_verified_at = str(requirement.get("source_verified_at") or "").strip()
            if source_verified_at:
                verified_dates.append(source_verified_at)
            evidence_links += len(requirement.get("evidence") or [])

    return {
        "engine_versions": sorted(engine_versions),
        "unique_rule_ids": len(rule_ids),
        "source_verified_at_oldest": min(verified_dates) if verified_dates else None,
        "source_verified_at_newest": max(verified_dates) if verified_dates else None,
        "evidence_links": evidence_links,
    }


def run_batch_preflight(
    items: list[Any],
    *,
    allow_address: bool,
    transport: str,
    max_items: int = MAX_BATCH_ITEMS,
) -> dict[str, Any]:
    if not isinstance(items, list):
        raise ValueError("items must be an array")
    if not items:
        raise ValueError("items must contain at least one project")
    if len(items) > max_items:
        raise ValueError(f"items must contain at most {max_items} projects")

    results: list[dict[str, Any]] = []
    successful_results: list[dict[str, Any]] = []
    determination_counts: Counter[str] = Counter()

    for index, raw_item in enumerate(items):
        client_ref = raw_item.get("client_ref") if isinstance(raw_item, dict) else None
        try:
            client_ref, facts = _normalize_item(
                raw_item,
                allow_address=allow_address,
                transport=transport,
            )
            result = run_preflight(facts)
            successful_results.append(result)
            determination_counts[str(result.get("determination") or "UNKNOWN")] += 1
            results.append(
                {
                    "index": index,
                    "client_ref": client_ref,
                    "ok": True,
                    "result": result,
                }
            )
        except ValueError as exc:
            results.append(
                {
                    "index": index,
                    "client_ref": client_ref,
                    "ok": False,
                    "error": {"type": "validation_error", "message": str(exc)},
                }
            )
        except Exception:
            results.append(
                {
                    "index": index,
                    "client_ref": client_ref,
                    "ok": False,
                    "error": {
                        "type": "evaluation_error",
                        "message": "preflight evaluation failed",
                    },
                }
            )

    succeeded = len(successful_results)
    failed = len(results) - succeeded
    return {
        "batch_size": len(items),
        "succeeded": succeeded,
        "failed": failed,
        "determination_counts": dict(sorted(determination_counts.items())),
        "audit": _build_audit(successful_results),
        "results": results,
    }
