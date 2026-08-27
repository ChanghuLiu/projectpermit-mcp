"""Read-only ServiceM8 work-object helpers.

The adapter deliberately performs no ServiceM8 network calls and no mutations.
It copies only the minimum work context needed for ProjectPermit:

    ServiceM8 Job -> address + scope text -> structured ProjectPermit facts

Natural-language scope normalization remains the caller/agent's responsibility.
"""
from __future__ import annotations

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
    """Extract the minimum ServiceM8 Job context required for preflight.

    `payload` should be one decoded ServiceM8 Job record. Optional JobMaterial
    objects may be supplied when description text alone is insufficient. Customer,
    billing, payment, staff and price fields are intentionally ignored.
    """
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
        # Some API responses expose already-geocoded components. Reconstructing a
        # civic address from those fields is safe and avoids requiring client data.
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
        # If a material carries a job_uuid, reject material rows belonging to some
        # other job rather than silently blending scopes.
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
) -> dict[str, Any]:
    """Build ProjectPermit's existing fact shape after explicit scope normalization."""
    if _text(extracted.get("source_platform")).lower() != "servicem8":
        raise ServiceM8AdapterError("extracted object is not a ServiceM8 work object")
    if not _text(jurisdiction):
        raise ServiceM8AdapterError("jurisdiction is required")
    if not isinstance(project, Mapping) or not _text(project.get("family")):
        raise ServiceM8AdapterError("structured project.family is required before preflight")

    address = _text(extracted.get("address"))
    if resolve_address and not address:
        raise ServiceM8AdapterError("address is required when resolve_address=true")

    return {
        "jurisdiction": jurisdiction.strip(),
        "project": dict(project),
        "address": address or None,
        "property": {},
        "context": {
            "client_tag": client_tag,
            "_transport": "servicem8_adapter",
            "source_platform": "servicem8",
            "source_object_type": "job",
            "source_object_id": _text(extracted.get("source_object_id")),
            "source_status": _text(extracted.get("source_status")),
        },
        "resolve_address": bool(resolve_address),
    }


def build_servicem8_routing_summary(result: Mapping[str, Any]) -> dict[str, str]:
    """Create proposed compact routing metadata without mutating ServiceM8."""
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

    return {
        "projectpermit_preflight": determination,
        "projectpermit_confidence": confidence,
        "projectpermit_rule_version": rule_version,
        "projectpermit_evidence_url": evidence_url,
    }
