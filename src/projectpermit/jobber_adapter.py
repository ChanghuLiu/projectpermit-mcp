"""Read-only helpers for a future Jobber integration.

The adapter deliberately does not call Jobber, mutate Jobber, or classify natural
language into a ProjectPermit project family. Its job is to isolate platform shape
from the deterministic permit engine:

    Jobber GraphQL object -> minimal work object -> structured ProjectPermit facts
    ProjectPermit result/action bundle -> proposed Jobber fields/tasks

Natural-language scope normalization remains the caller/agent's responsibility,
consistent with ProjectPermit's no-server-side-LLM architecture.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class JobberAdapterError(ValueError):
    """Raised when a Jobber payload does not contain the required work context."""

    message: str

    def __str__(self) -> str:
        return self.message


def _text(value: Any) -> str:
    return str(value or "").strip()


def _nodes(value: Any) -> list[Mapping[str, Any]]:
    """Normalize GraphQL list/connection shapes without depending on Jobber SDKs."""
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if not isinstance(value, Mapping):
        return []

    nodes = value.get("nodes")
    if isinstance(nodes, list):
        return [item for item in nodes if isinstance(item, Mapping)]

    edges = value.get("edges")
    if isinstance(edges, list):
        normalized: list[Mapping[str, Any]] = []
        for edge in edges:
            if isinstance(edge, Mapping) and isinstance(edge.get("node"), Mapping):
                normalized.append(edge["node"])
        return normalized
    return []


def _first_text(mapping: Mapping[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = _text(mapping.get(key))
        if value:
            return value
    return ""


def _format_address(property_payload: Mapping[str, Any]) -> str:
    address = property_payload.get("address")
    if isinstance(address, str):
        return address.strip()
    if not isinstance(address, Mapping):
        return ""

    street1 = _first_text(address, ("street1", "street", "address1", "line1"))
    street2 = _first_text(address, ("street2", "address2", "line2"))
    city = _first_text(address, ("city",))
    province = _first_text(address, ("province", "provinceCode", "state", "stateCode"))
    postal = _first_text(address, ("postalCode", "postal_code", "zip", "zipCode"))
    country = _first_text(address, ("country", "countryCode"))

    street = " ".join(part for part in (street1, street2) if part)
    locality = ", ".join(part for part in (city, province) if part)
    tail = " ".join(part for part in (postal, country) if part)
    return ", ".join(part for part in (street, locality, tail) if part)


def _line_item_text(item: Mapping[str, Any]) -> str:
    # Only scope-relevant fields are copied. Price, client and billing fields are
    # intentionally ignored.
    pieces: list[str] = []
    for key in ("name", "title", "description"):
        value = _text(item.get(key))
        if value and value not in pieces:
            pieces.append(value)
    return " — ".join(pieces)


def extract_jobber_work_object(
    payload: Mapping[str, Any],
    *,
    object_type: str | None = None,
) -> dict[str, Any]:
    """Extract the minimum Jobber Request/Quote/Job context needed for preflight.

    `payload` is expected to be one decoded GraphQL work object, not the entire
    GraphQL response envelope. The output intentionally excludes client/contact,
    pricing, invoice, payment and assignee data.
    """
    if not isinstance(payload, Mapping):
        raise JobberAdapterError("Jobber work object must be a mapping")

    resolved_type = _text(object_type or payload.get("__typename")).lower()
    if resolved_type not in {"request", "quote", "job"}:
        raise JobberAdapterError("Jobber object_type must be request, quote, or job")

    source_id = _text(payload.get("id"))
    if not source_id:
        raise JobberAdapterError("Jobber work object id is required")

    property_payload = payload.get("property")
    if not isinstance(property_payload, Mapping):
        raise JobberAdapterError("Jobber property is required for permit preflight")

    address = _format_address(property_payload)
    if not address:
        raise JobberAdapterError("Jobber property address is required for permit preflight")

    title = _text(payload.get("title"))
    line_items = _nodes(payload.get("lineItems") or payload.get("line_items"))
    scope_parts = [title] if title else []
    scope_parts.extend(text for item in line_items if (text := _line_item_text(item)))
    scope_text = "\n".join(scope_parts).strip()
    if not scope_text:
        raise JobberAdapterError("Jobber work object needs title or line items for scope normalization")

    return {
        "source_platform": "jobber",
        "source_object_type": resolved_type,
        "source_object_id": source_id,
        "address": address,
        "scope_text": scope_text,
        "line_item_count": len(line_items),
        "project_family_normalization_required": True,
    }


def build_preflight_facts(
    extracted: Mapping[str, Any],
    *,
    jurisdiction: str,
    project: Mapping[str, Any],
    resolve_address: bool = True,
    client_tag: str = "jobber-integration",
) -> dict[str, Any]:
    """Build the existing ProjectPermit fact shape after scope normalization.

    The caller must supply a structured `project` object, including `family`.
    This prevents the integration layer from silently guessing permit semantics.
    """
    if _text(extracted.get("source_platform")).lower() != "jobber":
        raise JobberAdapterError("extracted object is not a Jobber work object")
    if not _text(jurisdiction):
        raise JobberAdapterError("jurisdiction is required")
    if not isinstance(project, Mapping) or not _text(project.get("family")):
        raise JobberAdapterError("structured project.family is required before preflight")

    address = _text(extracted.get("address"))
    if resolve_address and not address:
        raise JobberAdapterError("address is required when resolve_address=true")

    return {
        "jurisdiction": jurisdiction.strip(),
        "project": dict(project),
        "address": address or None,
        "property": {},
        "context": {
            "client_tag": client_tag,
            "_transport": "jobber_adapter",
            "source_platform": "jobber",
            "source_object_type": _text(extracted.get("source_object_type")),
            # The source id is useful to the authorized integration for correlation,
            # but telemetry.py does not emit raw context fields other than a hash of
            # client_tag.
            "source_object_id": _text(extracted.get("source_object_id")),
        },
        "resolve_address": bool(resolve_address),
    }


def _legacy_result_hints(result: Mapping[str, Any]) -> dict[str, Any]:
    """Backwards-compatible hints for older stored results without action_bundle."""
    determination = _text(result.get("determination"))
    if not determination:
        raise JobberAdapterError("ProjectPermit result.determination is required")

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
            if evidence_url and rule_version:
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
    }


def _writeback_hints(result: Mapping[str, Any]) -> dict[str, Any]:
    bundle = result.get("action_bundle")
    if isinstance(bundle, Mapping) and isinstance(bundle.get("writeback_hints"), Mapping):
        return dict(bundle["writeback_hints"])
    return _legacy_result_hints(result)


def build_jobber_writeback(result: Mapping[str, Any]) -> dict[str, str]:
    """Return proposed Jobber text custom-field values; this function performs no mutation."""
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
    }


def build_jobber_action_proposal(result: Mapping[str, Any]) -> dict[str, Any]:
    """Map ProjectPermit's action bundle into a read-only Jobber integration proposal.

    The returned object describes what an authorized integration *could* write or
    create. No Jobber API call is performed here.
    """
    bundle = result.get("action_bundle")
    if not isinstance(bundle, Mapping):
        raise JobberAdapterError("ProjectPermit result.action_bundle is required")

    tasks = bundle.get("tasks") if isinstance(bundle.get("tasks"), list) else []
    required_inputs = (
        bundle.get("required_inputs") if isinstance(bundle.get("required_inputs"), list) else []
    )
    evidence = bundle.get("evidence") if isinstance(bundle.get("evidence"), list) else []
    audit = bundle.get("audit") if isinstance(bundle.get("audit"), Mapping) else {}

    return {
        "source_platform": "jobber",
        "mutation_performed": False,
        "proposed_custom_fields": build_jobber_writeback(result),
        "proposed_tasks": deepcopy(tasks),
        "required_inputs": deepcopy(required_inputs),
        "evidence": deepcopy(evidence),
        "audit": deepcopy(dict(audit)),
    }
