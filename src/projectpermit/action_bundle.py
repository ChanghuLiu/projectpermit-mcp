"""Platform-neutral evidence/action bundle for ProjectPermit results.

The bundle is designed for contractor, field-service and property workflow agents.
It packages the deterministic permit decision, workflow routing, official evidence,
blocking tasks, missing facts and audit metadata into one stable object.

It never mutates an upstream platform and never represents municipal authorization.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping


BUNDLE_VERSION = "2026-08-29.1"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _dedupe_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _collect_evidence(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Deduplicate official sources while preserving the rules that relied on them."""
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    rule_ids: dict[tuple[str, str], list[str]] = defaultdict(list)
    statuses: dict[tuple[str, str], list[str]] = defaultdict(list)
    verified_dates: dict[tuple[str, str], list[str]] = defaultdict(list)

    requirements = result.get("requirements")
    if not isinstance(requirements, list):
        return []

    for requirement in requirements:
        if not isinstance(requirement, Mapping):
            continue
        rule_id = _text(requirement.get("rule_id"))
        status = _text(requirement.get("status"))
        verified_at = _text(requirement.get("source_verified_at"))
        evidence = requirement.get("evidence")
        if not isinstance(evidence, list):
            continue

        for source in evidence:
            if not isinstance(source, Mapping):
                continue
            source_id = _text(source.get("source_id"))
            url = _text(source.get("url"))
            if not source_id and not url:
                continue
            key = (source_id, url)
            if key not in by_key:
                by_key[key] = {
                    "source_id": source_id,
                    "authority": _text(source.get("authority")),
                    "title": _text(source.get("title")),
                    "url": url,
                }
            if rule_id:
                rule_ids[key].append(rule_id)
            if status:
                statuses[key].append(status)
            if verified_at:
                verified_dates[key].append(verified_at)

    output: list[dict[str, Any]] = []
    for key, source in by_key.items():
        output.append(
            {
                **source,
                "rule_ids": _dedupe_sorted(rule_ids[key]),
                "statuses": _dedupe_sorted(statuses[key]),
                "source_verified_at": (
                    min(verified_dates[key]) if verified_dates[key] else None
                ),
            }
        )

    output.sort(key=lambda item: (item.get("authority") or "", item.get("source_id") or "", item.get("url") or ""))
    return output


def _collect_audit(result: Mapping[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    rule_ids: list[str] = []
    rule_versions: list[str] = []
    verified_dates: list[str] = []

    requirements = result.get("requirements")
    if isinstance(requirements, list):
        for requirement in requirements:
            if not isinstance(requirement, Mapping):
                continue
            rule_ids.append(_text(requirement.get("rule_id")))
            rule_versions.append(_text(requirement.get("rule_version")))
            verified_dates.append(_text(requirement.get("source_verified_at")))

    rule_ids = _dedupe_sorted(rule_ids)
    rule_versions = _dedupe_sorted(rule_versions)
    verified_dates = _dedupe_sorted(verified_dates)

    return {
        "engine_version": _text(result.get("engine_version")),
        "rule_ids": rule_ids,
        "rule_versions": rule_versions,
        "source_verified_at_oldest": min(verified_dates) if verified_dates else None,
        "source_verified_at_newest": max(verified_dates) if verified_dates else None,
        "evidence_source_count": len(evidence),
        "generated_from": "deterministic_preflight",
    }


def _route_task(route: str, workflow: Mapping[str, Any]) -> dict[str, Any] | None:
    if route == "ADD_PERMIT_TASK":
        return {
            "task_type": "PERMIT_PROCESS",
            "blocking": True,
            "action": "Add a permit task/allowance before scheduling or design lock.",
        }
    if route == "CONTINUE_WITH_EVIDENCE":
        return {
            "task_type": "ATTACH_EVIDENCE",
            "blocking": False,
            "action": "Attach the evidence-linked preflight result to the work record before continuing.",
        }
    if route == "COLLECT_MISSING_FACTS":
        return {
            "task_type": "COLLECT_MISSING_FACTS",
            "blocking": True,
            "action": "Collect the listed missing facts and rerun ProjectPermit before automated finalization.",
        }
    if route == "ROUTE_SPECIAL_REVIEW":
        return {
            "task_type": "SPECIAL_REVIEW",
            "blocking": True,
            "action": "Route the work for the indicated planning, heritage, or special review.",
        }
    if route == "MUNICIPAL_CONFIRMATION":
        return {
            "task_type": "MUNICIPAL_CONFIRMATION",
            "blocking": True,
            "action": "Obtain municipal confirmation before automated finalization.",
        }
    if route == "MANUAL_SCOPE_REVIEW":
        return {
            "task_type": "MANUAL_SCOPE_REVIEW",
            "blocking": True,
            "action": "Route the scope for manual review because the current ruleset does not cover it safely.",
        }
    return None


def _build_tasks(workflow: Mapping[str, Any], evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    route = _text(workflow.get("recommended_route"))
    tasks: list[dict[str, Any]] = []
    primary = _route_task(route, workflow)
    if primary is not None:
        tasks.append(primary)

    # Permit/review paths also benefit from an explicit evidence-preservation task.
    if evidence and route not in {"CONTINUE_WITH_EVIDENCE", "COLLECT_MISSING_FACTS"}:
        tasks.append(
            {
                "task_type": "ATTACH_EVIDENCE",
                "blocking": False,
                "action": "Attach the official-source evidence and rule metadata to the work record.",
            }
        )
    return tasks


def build_action_bundle(facts: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    """Build a stable, platform-neutral action package from a completed preflight."""
    workflow = result.get("workflow")
    if not isinstance(workflow, Mapping):
        raise ValueError("ProjectPermit result.workflow is required before action bundle generation")

    evidence = _collect_evidence(result)
    audit = _collect_audit(result, evidence)
    follow_ups = workflow.get("follow_up_questions")
    if not isinstance(follow_ups, list):
        follow_ups = []

    freshness = workflow.get("evidence_freshness")
    if not isinstance(freshness, Mapping):
        freshness = {}

    first_evidence_url = _text(evidence[0].get("url")) if evidence else ""
    first_rule_version = audit["rule_versions"][0] if audit["rule_versions"] else ""

    return {
        "bundle_version": BUNDLE_VERSION,
        "decision": {
            "determination": _text(result.get("determination")),
            "confidence": _text(result.get("confidence")),
            "jurisdiction": result.get("jurisdiction") if isinstance(result.get("jurisdiction"), Mapping) else {},
            "project_family": _text((facts.get("project") or {}).get("family"))
            if isinstance(facts.get("project"), Mapping)
            else "",
        },
        "routing": {
            "recommended_route": _text(workflow.get("recommended_route")),
            "quote_handling": _text(workflow.get("quote_handling")),
            "automation_safe": bool(workflow.get("automation_safe", False)),
            "evidence_freshness": dict(freshness),
        },
        "required_inputs": [dict(item) for item in follow_ups if isinstance(item, Mapping)],
        "tasks": _build_tasks(workflow, evidence),
        "evidence": evidence,
        "audit": audit,
        "writeback_hints": {
            "permit_status": _text(result.get("determination")),
            "confidence": _text(result.get("confidence")),
            "recommended_route": _text(workflow.get("recommended_route")),
            "quote_handling": _text(workflow.get("quote_handling")),
            "automation_safe": bool(workflow.get("automation_safe", False)),
            "rule_version": first_rule_version,
            "evidence_url": first_evidence_url,
            "freshness_status": _text(freshness.get("status")),
        },
        "disclaimer": _text(result.get("disclaimer")),
    }
