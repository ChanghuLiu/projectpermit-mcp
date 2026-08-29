"""Target-bound external execution plans for ProjectPermit writeback.

Layer 6 deliberately stops one boundary before real OAuth/network execution. It
converts a Layer 5 mutation gate into a concrete, auditable platform mutation plan
only after the caller supplies the raw target identifier and that identifier hashes
to the same scope fingerprint used by the permit decision.

No function in this module sends an HTTP request or stores OAuth credentials.
"""
from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Any, Mapping

from .decision_identity import build_scope_fingerprint


EXECUTION_PLAN_VERSION = "2026-08-29.1"

READY_TO_EXECUTE = "READY_TO_EXECUTE"
BINDING_REQUIRED = "BINDING_REQUIRED"
NOOP = "NOOP"
BLOCKED = "BLOCKED"

_SERVICEM8_NAMESPACE = uuid.UUID("b41bb286-49d6-5d70-912a-b3ce7e316d3c")

JOBBER_COMPACT_FIELDS = (
    {
        "key": "status",
        "name": "ProjectPermit Status",
        "value_type": "TEXT",
        "read_only": True,
    },
    {
        "key": "route",
        "name": "ProjectPermit Route",
        "value_type": "TEXT",
        "read_only": True,
    },
    {
        "key": "evidence",
        "name": "ProjectPermit Evidence",
        "value_type": "LINK",
        "read_only": True,
    },
    {
        "key": "freshness",
        "name": "ProjectPermit Freshness",
        "value_type": "TEXT",
        "read_only": True,
    },
    {
        "key": "identity",
        "name": "ProjectPermit Identity",
        "value_type": "TEXT",
        "read_only": True,
    },
)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _bundle(result: Mapping[str, Any]) -> Mapping[str, Any]:
    bundle = result.get("action_bundle")
    if not isinstance(bundle, Mapping):
        raise ValueError("ProjectPermit result.action_bundle is required")
    return bundle


def _gate(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    gate = bundle.get("mutation_gate")
    if not isinstance(gate, Mapping):
        raise ValueError("ProjectPermit action_bundle.mutation_gate is required")
    return gate


def _identity(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    identity = bundle.get("identity")
    if not isinstance(identity, Mapping):
        raise ValueError("ProjectPermit action_bundle.identity is required")
    return identity


def _base_plan(platform: str, bundle: Mapping[str, Any], gate: Mapping[str, Any]) -> dict[str, Any]:
    identity = _identity(bundle)
    return {
        "execution_plan_version": EXECUTION_PLAN_VERSION,
        "platform": platform,
        "mutation_performed": False,
        "requires_explicit_execute_call": True,
        "gate_state": _text(gate.get("state")),
        "idempotency_key": _text(identity.get("idempotency_key")),
        "scope_fingerprint": _text(identity.get("scope_fingerprint")) or None,
        "bundle_id": _text(identity.get("bundle_id")),
        "change_classification": _text((bundle.get("change") or {}).get("classification"))
        if isinstance(bundle.get("change"), Mapping)
        else "",
    }


def _target_scope_matches(
    bundle: Mapping[str, Any],
    *,
    source_platform: str,
    source_object_type: str,
    source_object_id: str,
) -> tuple[bool, str | None]:
    expected = _text(_identity(bundle).get("scope_fingerprint"))
    actual = build_scope_fingerprint(
        source_platform=source_platform,
        source_object_type=source_object_type,
        source_object_id=source_object_id,
    )
    return bool(expected and actual and expected == actual), actual


def _blocked(plan: dict[str, Any], reason: str, **extra: Any) -> dict[str, Any]:
    return {
        **plan,
        "status": BLOCKED,
        "executable": False,
        "reason_codes": [reason],
        "required_oauth_scopes": [],
        "mutation_intents": [],
        **extra,
    }


def _gate_transition(plan: dict[str, Any], gate: Mapping[str, Any]) -> dict[str, Any] | None:
    state = _text(gate.get("state"))
    if state == "NOOP_UNCHANGED":
        return {
            **plan,
            "status": NOOP,
            "executable": False,
            "reason_codes": ["DUPLICATE_SUPPRESSED"],
            "required_oauth_scopes": [],
            "mutation_intents": [],
        }
    if state != "READY_FOR_EXPLICIT_WRITE":
        return _blocked(
            plan,
            "MUTATION_GATE_BLOCKED",
            upstream_reason_codes=list(gate.get("reason_codes") or []),
        )
    return None


def _writeback_hints(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    hints = bundle.get("writeback_hints")
    return hints if isinstance(hints, Mapping) else {}


def _first_task(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    tasks = bundle.get("tasks")
    if isinstance(tasks, list):
        for task in tasks:
            if isinstance(task, Mapping):
                return task
    return {}


def _first_evidence(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    evidence = bundle.get("evidence")
    if isinstance(evidence, list):
        for source in evidence:
            if isinstance(source, Mapping):
                return source
    return {}


def _servicem8_record_uuid(idempotency_key: str, record_kind: str) -> str:
    return str(uuid.uuid5(_SERVICEM8_NAMESPACE, f"{record_kind}:{idempotency_key}"))


def _servicem8_summary(bundle: Mapping[str, Any]) -> str:
    hints = _writeback_hints(bundle)
    evidence = _first_evidence(bundle)
    pieces = [
        f"ProjectPermit: {_text(hints.get('permit_status'))}",
        f"Route: {_text(hints.get('recommended_route'))}",
        f"Confidence: {_text(hints.get('confidence'))}",
        f"Evidence freshness: {_text(hints.get('freshness_status'))}",
        f"Evidence: {_text(evidence.get('url'))}",
        f"Idempotency: {_text(hints.get('idempotency_key'))}",
    ]
    return "\n".join(piece for piece in pieces if not piece.endswith(": "))


def build_servicem8_execution_plan(
    result: Mapping[str, Any],
    *,
    job_uuid: str,
) -> dict[str, Any]:
    """Build a concrete ServiceM8 read-then-create/update plan; perform no request.

    ServiceM8 supports caller-specified UUIDs for both Task and Note creation. We
    derive that UUID from ProjectPermit's idempotency key so retries converge on one
    record. A non-blocking ATTACH_EVIDENCE route uses a job Note; blocking workflow
    routes use a Task.
    """
    bundle = _bundle(result)
    gate = _gate(bundle)
    plan = _base_plan("servicem8", bundle, gate)

    job_uuid = _text(job_uuid)
    if not job_uuid:
        return _blocked(plan, "TARGET_ID_REQUIRED")
    matches, actual_scope = _target_scope_matches(
        bundle,
        source_platform="servicem8",
        source_object_type="job",
        source_object_id=job_uuid,
    )
    if not matches:
        return _blocked(
            plan,
            "TARGET_SCOPE_MISMATCH",
            target_scope_fingerprint=actual_scope,
        )

    transition = _gate_transition(plan, gate)
    if transition is not None:
        return transition

    task = _first_task(bundle)
    task_type = _text(task.get("task_type"))
    is_evidence_only = task_type == "ATTACH_EVIDENCE" and not bool(task.get("blocking", False))
    record_kind = "note" if is_evidence_only else "task"
    record_uuid = _servicem8_record_uuid(plan["idempotency_key"], record_kind)
    details = _servicem8_summary(bundle)

    if record_kind == "note":
        required_scopes = ["read_job_notes", "publish_job_notes"]
        lookup = {
            "method": "GET",
            "path": f"/api_1.0/dbonote/{record_uuid}.json",
            "expected": {"exists": 200, "missing": 404},
        }
        create = {
            "method": "POST",
            "path": "/api_1.0/note.json",
            "body": {
                "uuid": record_uuid,
                "related_object": "job",
                "related_object_uuid": job_uuid,
                "note": details,
                "action_required": "0",
            },
        }
        update = {
            "method": "POST",
            "path": f"/api_1.0/dbonote/{record_uuid}.json",
            "body": {
                "uuid": record_uuid,
                "related_object": "job",
                "related_object_uuid": job_uuid,
                "note": details,
                "action_required": "0",
            },
        }
    else:
        required_scopes = ["read_tasks", "manage_tasks"]
        lookup = {
            "method": "GET",
            "path": f"/api_1.0/task/{record_uuid}.json",
            "expected": {"exists": 200, "missing": 404},
        }
        create = {
            "method": "POST",
            "path": "/api_1.0/task.json",
            "body": {
                "uuid": record_uuid,
                "name": "ProjectPermit permit workflow",
                "task_details": details,
                "related_object": "job",
                "related_object_uuid": job_uuid,
                "task_complete": "0",
            },
        }
        update = {
            "method": "POST",
            "path": f"/api_1.0/task/{record_uuid}.json",
            "body": deepcopy(create["body"]),
        }

    return {
        **plan,
        "status": READY_TO_EXECUTE,
        "executable": True,
        "reason_codes": ["TARGET_SCOPE_VERIFIED", "DETERMINISTIC_RECORD_UUID"],
        "required_oauth_scopes": required_scopes,
        "upsert_strategy": "GET_THEN_CREATE_OR_UPDATE_DETERMINISTIC_UUID",
        "target": {"object_type": "job", "object_id": job_uuid},
        "deterministic_record": {"kind": record_kind, "uuid": record_uuid},
        "mutation_intents": [
            {"step": "LOOKUP", **lookup},
            {"step": "CREATE_IF_MISSING", **create},
            {"step": "UPDATE_IF_EXISTS", **update},
        ],
    }


def _jobber_compact_values(bundle: Mapping[str, Any]) -> dict[str, Any]:
    hints = _writeback_hints(bundle)
    evidence = _first_evidence(bundle)
    evidence_url = _text(evidence.get("url") or hints.get("evidence_url"))
    return {
        "status": _text(hints.get("permit_status")),
        "route": _text(hints.get("recommended_route")),
        "evidence": {
            "text": "ProjectPermit evidence",
            "url": evidence_url,
        },
        "freshness": _text(hints.get("freshness_status")),
        "identity": _text(hints.get("idempotency_key")),
    }


def build_jobber_execution_plan(
    result: Mapping[str, Any],
    *,
    object_type: str,
    object_id: str,
    custom_field_bindings: Mapping[str, str] | None = None,
    graphql_binding: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build a Jobber compact-field execution plan without guessing live schema.

    Current Jobber docs allow app-configured custom fields on Quotes and Jobs and
    limit an app to five configurations per object. ProjectPermit therefore compresses
    writeback to exactly five logical fields. The exact current GraphQL mutation and
    input argument names must be bound from the app's active-version GraphiQL schema
    before this plan becomes executable.
    """
    bundle = _bundle(result)
    gate = _gate(bundle)
    plan = _base_plan("jobber", bundle, gate)

    object_type = _text(object_type).lower()
    object_id = _text(object_id)
    if object_type not in {"job", "quote"}:
        return _blocked(plan, "UNSUPPORTED_JOBBER_WRITE_TARGET")
    if not object_id:
        return _blocked(plan, "TARGET_ID_REQUIRED")

    matches, actual_scope = _target_scope_matches(
        bundle,
        source_platform="jobber",
        source_object_type=object_type,
        source_object_id=object_id,
    )
    if not matches:
        return _blocked(
            plan,
            "TARGET_SCOPE_MISMATCH",
            target_scope_fingerprint=actual_scope,
        )

    transition = _gate_transition(plan, gate)
    if transition is not None:
        return transition

    values = _jobber_compact_values(bundle)
    required_keys = [item["key"] for item in JOBBER_COMPACT_FIELDS]
    bindings = dict(custom_field_bindings or {})
    missing_fields = [key for key in required_keys if not _text(bindings.get(key))]

    graphql = dict(graphql_binding or {})
    required_graphql = ("api_version", "mutation_name", "id_argument", "input_argument")
    missing_graphql = [key for key in required_graphql if not _text(graphql.get(key))]

    if missing_fields or missing_graphql:
        return {
            **plan,
            "status": BINDING_REQUIRED,
            "executable": False,
            "reason_codes": ["JOBBER_SCHEMA_BINDING_REQUIRED"],
            "required_oauth_capabilities": [
                "target_object_read_write",
                "custom_field_configurations_read_write",
            ],
            "target": {"object_type": object_type, "object_id": object_id},
            "compact_field_contract": [dict(item) for item in JOBBER_COMPACT_FIELDS],
            "compact_values": values,
            "missing_custom_field_bindings": missing_fields,
            "missing_graphql_bindings": missing_graphql,
            "mutation_intents": [],
            "schema_note": (
                "Bind mutation_name/id_argument/input_argument from Jobber GraphiQL for the active "
                "X-JOBBER-GRAPHQL-VERSION; ProjectPermit does not guess version-sensitive schema."
            ),
        }

    custom_fields = []
    for field in JOBBER_COMPACT_FIELDS:
        key = field["key"]
        value = values[key]
        entry: dict[str, Any] = {
            "logical_key": key,
            "customFieldConfigurationId": bindings[key],
        }
        if field["value_type"] == "LINK":
            entry["valueLink"] = value
        else:
            entry["valueText"] = value
        custom_fields.append(entry)

    return {
        **plan,
        "status": READY_TO_EXECUTE,
        "executable": True,
        "reason_codes": ["TARGET_SCOPE_VERIFIED", "JOBBER_SCHEMA_BOUND"],
        "required_oauth_capabilities": [
            "target_object_read_write",
            "custom_field_configurations_read_write",
        ],
        "target": {"object_type": object_type, "object_id": object_id},
        "graphql_binding": graphql,
        "compact_field_contract": [dict(item) for item in JOBBER_COMPACT_FIELDS],
        "mutation_intents": [
            {
                "step": "UPSERT_CUSTOM_FIELDS",
                "transport": "GRAPHQL_POST",
                "endpoint": "https://api.getjobber.com/api/graphql",
                "api_version": graphql["api_version"],
                "mutation_name": graphql["mutation_name"],
                "id_argument": graphql["id_argument"],
                "input_argument": graphql["input_argument"],
                "target_id": object_id,
                "custom_fields": custom_fields,
            }
        ],
    }
