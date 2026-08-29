"""Read-only ServiceM8 work-object helpers.

The adapter deliberately performs no ServiceM8 network calls and no mutations.
It copies only the minimum work context needed for ProjectPermit:

    ServiceM8 Job -> address + scope text -> structured ProjectPermit facts
    ProjectPermit result/action bundle -> proposed ServiceM8 routing/tasks

Natural-language scope normalization remains the caller/agent's responsibility.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ServiceM8AdapterError(ValueError):
    message: str

    def __str__(self) -> str:
        return self.message


def _text(value: Any) -> str:
    return str(value or "").strip()


def _material_scope_text(material: Mapping[str, Any]) -> str:
    """Return scope-relevant material text while excluding cost/price fields."""
    pieces: list[str] = []
    for key in ("name", "item_description", "description"):
        value = _text(material.get(key))
        if value and value not in pieces:
            pieces.append(value)
    return " — ".join(pieces)


def extract_servicem8_work_object(
    payload: Mapping[str, Any],
    *,
    job_materials: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Extract the minimum ServiceM8 Job context required for preflight."""
    if not isinstance(payload, Mapping):
        raise ServiceM8AdapterError("ServiceM8 Job must be a mapping")

    source_id = _text(payload.get("uuid"))
    if not source_id:
        raise ServiceM8AdapterError("ServiceM8 Job uuid is required")

    status = _text(payload.get("status"))
    valid_statuses = {"Quote", "Work Order", "Unsuccessful", "Completed"}
    if status and status not in valid_statuses:
        raise ServiceM8AdapterError(f"Unsupported ServiceM8 Job status: {status}")

    address = _text(payload.get("job_address"))
    if not address:
        street = " ".join(
            part
            for part in (_text(payload.get("geo_number")), _text(payload.get("geo_street")))
            if part
        )
        locality = ", ".join(
            part
            for part in (_text(payload.get("geo_city")), _text(payload.get("geo_state")))
            if part
        )
        tail = " ".join(
            part
            for part in (_text(payload.get("geo_postcode")), _text(payload.get("geo_country")))
            if part
        )
        address = ", ".join(part for part in (street, locality, tail) if part)

    if not address:
        raise ServiceM8AdapterError("ServiceM8 job_address is required for permit preflight")

    scope_parts: list[str] = []
    description = _text(payload.get("job_description"))
    if description:
        scope_parts.append(description)

    material_count = 0
    for material in job_materials or ():
        if not isinstance(material, Mapping):
            continue
        material_job_id = _text(material.get("job_uuid"))
        if material_job_id and material_job_id != source_id:
            continue
        material_count += 1
        text = _material_scope_text(material)
        if text and text not in scope_parts:
            scope_parts.append(text)

    scope_text = "\n".join(scope_parts).strip()
    if not scope_text:
        raise ServiceM8AdapterError("ServiceM8 Job needs job_description or scope-relevant JobMaterial text")

    return {
        "source_platform": "servicem8",
        "source_object_type": "job",
        "source_object_id": source_id,
        "source_status": status,
        "address": address,
        "scope_text": scope_text,
        "job_material_count": material_count,
        "project_family_normalization_required": True,
    }


def build_preflight_facts(
    extracted: Mapping[str, Any],
    *,
    jurisdiction: str,
    project: Mapping[str, Any],
    resolve_address: bool = True,
    client_tag: str = "servicem8-integration",
    prior_decision_identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build ProjectPermit facts after explicit scope normalization.

    A prior public `action_bundle.identity` may be supplied for deterministic change
    classification. Raw ServiceM8 UUIDs remain request context only; only one-way
    scope/idempotency fingerprints are returned.
    """
    if _text(extracted.get("source_platform")).lower() != "servicem8":
        raise ServiceM8AdapterError("extracted object is not a ServiceM8 work object")
    if not _text(jurisdiction):
        raise ServiceM8AdapterError("jurisdiction is required")
    if not isinstance(project, Mapping) or not _text(project.get("family")):
        raise ServiceM8AdapterError("structured project.family is required before preflight")

    address = _text(extracted.get("address"))
    if resolve_address and not address:
        raise ServiceM8AdapterError("address is required when resolve_address=true")

    context: dict[str, Any] = {
        "client_tag": client_tag,
        "_transport": "servicem8_adapter",
        "source_platform": "servicem8",
        "source_object_type": "job",
        "source_object_id": _text(extracted.get("source_object_id")),
        "source_status": _text(extracted.get("source_status")),
    }
    if isinstance(prior_decision_identity, Mapping):
        context["prior_decision_identity"] = dict(prior_decision_identity)

    return {
        "jurisdiction": jurisdiction.strip(),
        "project": dict(project),
        "address": address or None,
        "property": {},
        "context": context,
        "resolve_address": bool(resolve_address),
    }


def _legacy_result_hints(result: Mapping[str, Any]) -> dict[str, Any]:
    determination = _text(result.get("determination"))
    if not determination:
        raise ServiceM8AdapterError("ProjectPermit result.determination is required")

    confidence = _text(result.get("confidence"))
    rule_version = ""
    evidence_url = ""
    requirements = result.get("requirements")
    if isinstance(requirements, list):
        for requirement in requirements:
            if not isinstance(requirement, Mapping):
                continue
            if not rule_version:
                rule_version = _text(requirement.get("rule_version"))
            evidence = requirement.get("evidence")
            if isinstance(evidence, list):
                for source in evidence:
                    if isinstance(source, Mapping) and _text(source.get("url")):
                        evidence_url = _text(source.get("url"))
                        break
            if rule_version and evidence_url:
                break

    workflow = result.get("workflow")
    if not isinstance(workflow, Mapping):
        workflow = {}
    freshness = workflow.get("evidence_freshness")
    if not isinstance(freshness, Mapping):
        freshness = {}

    return {
        "permit_status": determination,
        "confidence": confidence,
        "recommended_route": _text(workflow.get("recommended_route")),
        "quote_handling": _text(workflow.get("quote_handling")),
        "automation_safe": bool(workflow.get("automation_safe", False)),
        "rule_version": rule_version,
        "evidence_url": evidence_url,
        "freshness_status": _text(freshness.get("status")),
        "bundle_id": "",
        "idempotency_key": "",
        "change_classification": "",
    }


def _writeback_hints(result: Mapping[str, Any]) -> dict[str, Any]:
    bundle = result.get("action_bundle")
    if isinstance(bundle, Mapping) and isinstance(bundle.get("writeback_hints"), Mapping):
        return dict(bundle["writeback_hints"])
    return _legacy_result_hints(result)


def build_servicem8_routing_summary(result: Mapping[str, Any]) -> dict[str, str]:
    """Create proposed compact routing metadata without mutating ServiceM8."""
    hints = _writeback_hints(result)
    return {
        "projectpermit_preflight": _text(hints.get("permit_status")),
        "projectpermit_confidence": _text(hints.get("confidence")),
        "projectpermit_rule_version": _text(hints.get("rule_version")),
        "projectpermit_evidence_url": _text(hints.get("evidence_url")),
        "projectpermit_route": _text(hints.get("recommended_route")),
        "projectpermit_quote_handling": _text(hints.get("quote_handling")),
        "projectpermit_automation_safe": "true" if bool(hints.get("automation_safe")) else "false",
        "projectpermit_freshness": _text(hints.get("freshness_status")),
        "projectpermit_bundle_id": _text(hints.get("bundle_id")),
        "projectpermit_idempotency_key": _text(hints.get("idempotency_key")),
        "projectpermit_change": _text(hints.get("change_classification")),
    }


def build_servicem8_action_proposal(result: Mapping[str, Any]) -> dict[str, Any]:
    """Map the action bundle into a read-only ServiceM8 integration proposal.

    The idempotency key may be stored as a duplicate-suppression marker for the same
    ServiceM8 work-record scope/result. No ServiceM8 API mutation is performed.
    """
    bundle = result.get("action_bundle")
    if not isinstance(bundle, Mapping):
        raise ServiceM8AdapterError("ProjectPermit result.action_bundle is required")

    tasks = bundle.get("tasks") if isinstance(bundle.get("tasks"), list) else []
    required_inputs = (
        bundle.get("required_inputs") if isinstance(bundle.get("required_inputs"), list) else []
    )
    evidence = bundle.get("evidence") if isinstance(bundle.get("evidence"), list) else []
    audit = bundle.get("audit") if isinstance(bundle.get("audit"), Mapping) else {}
    identity = bundle.get("identity") if isinstance(bundle.get("identity"), Mapping) else {}
    change = bundle.get("change") if isinstance(bundle.get("change"), Mapping) else {}

    return {
        "source_platform": "servicem8",
        "mutation_performed": False,
        "idempotency_key": _text(identity.get("idempotency_key")),
        "change": deepcopy(dict(change)),
        "proposed_routing_fields": build_servicem8_routing_summary(result),
        "proposed_tasks": deepcopy(tasks),
        "required_inputs": deepcopy(required_inputs),
        "evidence": deepcopy(evidence),
        "audit": deepcopy(dict(audit)),
    }
