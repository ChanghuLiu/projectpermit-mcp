"""Credential-isolated external mutation executor.

Layer 7 is the first ProjectPermit component allowed to perform a third-party write.
It accepts only a previously target-bound Layer 6 execution plan, requires an
explicit execute=True flag, keeps credentials caller-supplied/in-memory, pins the
provider host, validates every planned endpoint before sending credentials, and
returns no credential material.

Only ServiceM8 has a concrete executor in this layer. Jobber remains plan-only until
an active-version GraphQL mutation document is explicitly bound and tested.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

import httpx


EXECUTOR_VERSION = "2026-08-29.1"
SERVICEM8_BASE_URL = "https://api.servicem8.com"

DRY_RUN = "DRY_RUN"
EXECUTED_CREATE = "EXECUTED_CREATE"
EXECUTED_UPDATE = "EXECUTED_UPDATE"
NOOP = "NOOP"
BLOCKED = "BLOCKED"
EXECUTION_FAILED = "EXECUTION_FAILED"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _base_result(plan: Mapping[str, Any]) -> dict[str, Any]:
    record = plan.get("deterministic_record")
    if not isinstance(record, Mapping):
        record = {}
    return {
        "executor_version": EXECUTOR_VERSION,
        "platform": _text(plan.get("platform")),
        "mutation_performed": False,
        "idempotency_key": _text(plan.get("idempotency_key")),
        "bundle_id": _text(plan.get("bundle_id")),
        "record_kind": _text(record.get("kind")) or None,
        "record_uuid": _text(record.get("uuid")) or None,
    }


def _blocked(plan: Mapping[str, Any], reason: str, **extra: Any) -> dict[str, Any]:
    return {
        **_base_result(plan),
        "status": BLOCKED,
        "reason_codes": [reason],
        **extra,
    }


def _intent_by_step(plan: Mapping[str, Any], step: str) -> Mapping[str, Any] | None:
    intents = plan.get("mutation_intents")
    if not isinstance(intents, list):
        return None
    for item in intents:
        if isinstance(item, Mapping) and _text(item.get("step")) == step:
            return item
    return None


def _expected_paths(kind: str, record_uuid: str) -> dict[str, str] | None:
    if kind == "note":
        return {
            "LOOKUP": f"/api_1.0/dbonote/{record_uuid}.json",
            "CREATE_IF_MISSING": "/api_1.0/note.json",
            "UPDATE_IF_EXISTS": f"/api_1.0/dbonote/{record_uuid}.json",
        }
    if kind == "task":
        return {
            "LOOKUP": f"/api_1.0/task/{record_uuid}.json",
            "CREATE_IF_MISSING": "/api_1.0/task.json",
            "UPDATE_IF_EXISTS": f"/api_1.0/task/{record_uuid}.json",
        }
    return None


def _validate_servicem8_plan(plan: Mapping[str, Any]) -> tuple[bool, str | None]:
    if _text(plan.get("platform")) != "servicem8":
        return False, "UNSUPPORTED_PLATFORM"
    if _text(plan.get("status")) != "READY_TO_EXECUTE" or plan.get("executable") is not True:
        return False, "PLAN_NOT_EXECUTABLE"
    if plan.get("requires_explicit_execute_call") is not True:
        return False, "EXPLICIT_EXECUTE_CONTRACT_MISSING"
    if not _text(plan.get("idempotency_key")):
        return False, "IDEMPOTENCY_KEY_REQUIRED"

    record = plan.get("deterministic_record")
    if not isinstance(record, Mapping):
        return False, "DETERMINISTIC_RECORD_REQUIRED"
    kind = _text(record.get("kind"))
    record_uuid = _text(record.get("uuid"))
    expected = _expected_paths(kind, record_uuid)
    if not record_uuid or expected is None:
        return False, "INVALID_DETERMINISTIC_RECORD"

    target = plan.get("target")
    if not isinstance(target, Mapping) or _text(target.get("object_type")) != "job" or not _text(target.get("object_id")):
        return False, "TARGET_JOB_REQUIRED"
    target_id = _text(target.get("object_id"))

    methods = {
        "LOOKUP": "GET",
        "CREATE_IF_MISSING": "POST",
        "UPDATE_IF_EXISTS": "POST",
    }
    for step, method in methods.items():
        intent = _intent_by_step(plan, step)
        if not isinstance(intent, Mapping):
            return False, f"{step}_INTENT_REQUIRED"
        if _text(intent.get("method")).upper() != method:
            return False, f"{step}_METHOD_MISMATCH"
        path = _text(intent.get("path"))
        if path != expected[step] or "://" in path or not path.startswith("/api_1.0/"):
            return False, f"{step}_PATH_MISMATCH"
        if step != "LOOKUP":
            body = intent.get("body")
            if not isinstance(body, Mapping):
                return False, f"{step}_BODY_REQUIRED"
            if _text(body.get("uuid")) != record_uuid:
                return False, f"{step}_UUID_MISMATCH"
            if _text(body.get("related_object")).lower() != "job":
                return False, f"{step}_RELATED_OBJECT_MISMATCH"
            if _text(body.get("related_object_uuid")) != target_id:
                return False, f"{step}_TARGET_MISMATCH"
    return True, None


def _credential_headers(*, access_token: str | None, api_key: str | None) -> tuple[dict[str, str] | None, str | None]:
    token = _text(access_token)
    key = _text(api_key)
    if bool(token) == bool(key):
        return None, None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        return headers, "oauth"
    headers["X-API-Key"] = key
    return headers, "api_key"


def _scope_check(plan: Mapping[str, Any], *, credential_mode: str, granted_scopes: Iterable[str] | None) -> tuple[bool, list[str]]:
    if credential_mode != "oauth":
        return True, []
    required = {_text(item) for item in (plan.get("required_oauth_scopes") or []) if _text(item)}
    granted = {_text(item) for item in (granted_scopes or []) if _text(item)}
    missing = sorted(required - granted)
    return not missing, missing


def execute_servicem8_plan(
    plan: Mapping[str, Any],
    *,
    execute: bool = False,
    access_token: str | None = None,
    api_key: str | None = None,
    granted_scopes: Iterable[str] | None = None,
    client: Any | None = None,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    """Execute one validated ServiceM8 deterministic upsert.

    Safety boundary:
    - execute defaults to False and performs no network call;
    - NOOP/BLOCKED plans never perform a network call;
    - exactly one caller-supplied credential mode is required for real execution;
    - OAuth execution requires the caller to declare granted scopes;
    - only canonical api.servicem8.com paths generated by Layer 6 are accepted;
    - credentials are never included in the returned result.

    The executor performs one lookup followed by exactly one create-or-update request.
    It intentionally does not auto-retry ambiguous provider failures. Because the
    record UUID is deterministic, the caller may safely rebuild/retry the operation.
    """
    if not isinstance(plan, Mapping):
        raise ValueError("execution plan must be a mapping")

    base = _base_result(plan)
    status = _text(plan.get("status"))
    if status == "NOOP":
        return {
            **base,
            "status": NOOP,
            "reason_codes": ["DUPLICATE_SUPPRESSED"],
        }
    if status in {"BLOCKED", "BINDING_REQUIRED"}:
        return _blocked(plan, "UPSTREAM_PLAN_BLOCKED")

    valid, validation_reason = _validate_servicem8_plan(plan)
    if not valid:
        return _blocked(plan, validation_reason or "INVALID_EXECUTION_PLAN")

    if execute is not True:
        return {
            **base,
            "status": DRY_RUN,
            "reason_codes": ["EXPLICIT_EXECUTE_REQUIRED"],
            "would_execute": "GET_THEN_CREATE_OR_UPDATE_DETERMINISTIC_UUID",
        }

    headers, credential_mode = _credential_headers(access_token=access_token, api_key=api_key)
    if headers is None or credential_mode is None:
        return _blocked(plan, "EXACTLY_ONE_CREDENTIAL_MODE_REQUIRED")

    scopes_ok, missing_scopes = _scope_check(
        plan,
        credential_mode=credential_mode,
        granted_scopes=granted_scopes,
    )
    if not scopes_ok:
        return _blocked(
            plan,
            "OAUTH_SCOPE_DECLARATION_INSUFFICIENT",
            missing_scopes=missing_scopes,
        )

    lookup = _intent_by_step(plan, "LOOKUP")
    create = _intent_by_step(plan, "CREATE_IF_MISSING")
    update = _intent_by_step(plan, "UPDATE_IF_EXISTS")
    assert isinstance(lookup, Mapping) and isinstance(create, Mapping) and isinstance(update, Mapping)

    owns_client = client is None
    http_client = client or httpx.Client()
    try:
        try:
            lookup_response = http_client.request(
                "GET",
                SERVICEM8_BASE_URL + _text(lookup.get("path")),
                headers=headers,
                timeout=timeout_seconds,
            )
        except Exception as exc:  # provider/network boundary; do not echo exception text
            return {
                **base,
                "status": EXECUTION_FAILED,
                "reason_codes": ["LOOKUP_REQUEST_FAILED"],
                "error_type": type(exc).__name__,
            }

        if lookup_response.status_code == 200:
            chosen = update
            operation = "update"
            success_status = EXECUTED_UPDATE
        elif lookup_response.status_code == 404:
            chosen = create
            operation = "create"
            success_status = EXECUTED_CREATE
        else:
            return {
                **base,
                "status": EXECUTION_FAILED,
                "reason_codes": ["UNEXPECTED_LOOKUP_STATUS"],
                "provider_status_code": int(lookup_response.status_code),
            }

        try:
            mutation_response = http_client.request(
                "POST",
                SERVICEM8_BASE_URL + _text(chosen.get("path")),
                headers=headers,
                json=dict(chosen.get("body") or {}),
                timeout=timeout_seconds,
            )
        except Exception as exc:  # do not expose headers/token through exception text
            return {
                **base,
                "status": EXECUTION_FAILED,
                "reason_codes": ["MUTATION_REQUEST_FAILED"],
                "operation": operation,
                "error_type": type(exc).__name__,
            }

        provider_status = int(mutation_response.status_code)
        if 200 <= provider_status < 300:
            return {
                **base,
                "status": success_status,
                "mutation_performed": True,
                "operation": operation,
                "provider_status_code": provider_status,
                "credential_mode": credential_mode,
            }
        return {
            **base,
            "status": EXECUTION_FAILED,
            "reason_codes": ["PROVIDER_MUTATION_REJECTED"],
            "operation": operation,
            "provider_status_code": provider_status,
        }
    finally:
        if owns_client:
            http_client.close()
