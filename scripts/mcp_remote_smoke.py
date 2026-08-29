"""End-to-end smoke test for the public ProjectPermit MCP endpoint."""
from __future__ import annotations

import asyncio
import json
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = os.getenv(
    "PROJECTPERMIT_MCP_URL",
    "https://projectpermit-mcp-production.up.railway.app/mcp",
)
INTERNAL_CONTEXT = {"client_tag": "projectpermit-ci"}

EXPECTED_JURISDICTIONS = {
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "laval_qc",
    "longueuil_qc",
    "vancouver_bc",
}
EXPECTED_PROJECT_FAMILIES = {
    "window_door",
    "interior_renovation",
    "basement",
    "dwelling_change",
    "deck_porch",
    "accessory_structure",
    "addition",
    "kitchen_bath_plumbing",
}

CASES = [
    ("ottawa_on", {"family": "window_door", "action": "replace_same_size"}, {"heritage": False}, "LIKELY_NOT_REQUIRED"),
    ("gatineau_qc", {"family": "addition", "floor_area_increase": True}, {}, "REQUIRED"),
    (
        "toronto_on",
        {
            "family": "window_door",
            "action": "replace_same_size",
            "single_dwelling_house": True,
            "structural_change": False,
            "new_exit": False,
        },
        {},
        "LIKELY_NOT_REQUIRED",
    ),
    ("mississauga_on", {"family": "window_door", "action": "replace_same_size"}, {}, "LIKELY_NOT_REQUIRED"),
    ("laval_qc", {"family": "window_door", "action": "replace_same_size"}, {"piia": False}, "LIKELY_NOT_REQUIRED"),
    ("longueuil_qc", {"family": "window_door", "action": "enlarge_existing_opening"}, {}, "REQUIRED"),
    ("vancouver_bc", {"family": "interior_renovation", "action": "painting"}, {}, "LIKELY_NOT_REQUIRED"),
]


def _structured_or_text(result):
    structured = getattr(result, "structured_content", None)
    if structured:
        return structured
    rendered = "\n".join(getattr(block, "text", "") for block in result.content)
    try:
        return json.loads(rendered)
    except json.JSONDecodeError:
        return {"_rendered": rendered}


def _assert_identity(bundle: dict) -> dict:
    identity = bundle.get("identity") or {}
    required = (
        "bundle_id",
        "input_fingerprint",
        "decision_fingerprint",
        "routing_fingerprint",
        "ruleset_fingerprint",
        "evidence_fingerprint",
        "idempotency_key",
    )
    missing = [field for field in required if not identity.get(field)]
    if missing:
        raise SystemExit(f"Decision identity missing fields {missing}: {identity}")
    if not str(identity["bundle_id"]).startswith("ppb_"):
        raise SystemExit(f"Unexpected bundle id format: {identity}")
    if not str(identity["idempotency_key"]).startswith("ppidem_"):
        raise SystemExit(f"Unexpected idempotency key format: {identity}")
    change = bundle.get("change") or {}
    if change.get("classification") not in {
        "FIRST_OBSERVATION",
        "UNCHANGED",
        "DECISION_CHANGED",
        "ROUTE_CHANGED",
        "INPUT_CHANGED",
        "RULESET_CHANGED",
        "EVIDENCE_REFRESHED",
        "IDENTITY_VERSION_CHANGED",
    }:
        raise SystemExit(f"Unexpected identity change classification: {change}")
    return identity


def _assert_gate(bundle: dict) -> dict:
    gate = bundle.get("mutation_gate") or {}
    if gate.get("state") not in {
        "READY_FOR_EXPLICIT_WRITE",
        "NOOP_UNCHANGED",
        "BLOCKED",
    }:
        raise SystemExit(f"Safe-writeback mutation gate missing/invalid: {gate}")
    if gate.get("execution_requires_explicit_request") is not True:
        raise SystemExit(f"Mutation gate must require explicit execution: {gate}")
    idempotency = gate.get("idempotency") or {}
    if idempotency.get("mode") != "ATOMIC_UPSERT":
        raise SystemExit(f"Mutation gate must require atomic upsert: {gate}")
    if idempotency.get("unconditional_create_allowed") is not False:
        raise SystemExit(f"Mutation gate must forbid unconditional creates: {gate}")
    return gate


def _assert_action_bundle(payload: dict, *, expected_route: str | None = None) -> dict:
    bundle = payload.get("action_bundle") or {}
    if not bundle:
        raise SystemExit(f"action_bundle missing from preflight result: {payload}")
    if bundle.get("bundle_version") != "2026-08-29.2":
        raise SystemExit(f"Unexpected action bundle version: {bundle}")
    routing = bundle.get("routing") or {}
    if expected_route and routing.get("recommended_route") != expected_route:
        raise SystemExit(f"Unexpected action bundle route: {bundle}")
    audit = bundle.get("audit") or {}
    if audit.get("generated_from") != "deterministic_preflight":
        raise SystemExit(f"Action bundle audit missing deterministic origin: {bundle}")
    _assert_identity(bundle)
    _assert_gate(bundle)
    return bundle


def _scoped_context(jurisdiction: str) -> dict:
    return {
        **INTERNAL_CONTEXT,
        "source_platform": "projectpermit_ci",
        "source_object_type": "mcp_record",
        "source_object_id": f"mcp-smoke-{jurisdiction}",
    }


async def main() -> None:
    print(f"mcp_url={URL}")
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            print(f"tools={names}")
            for required_tool in (
                "projectpermit_info",
                "check_project_requirements",
                "check_project_requirements_batch",
            ):
                if required_tool not in names:
                    raise SystemExit(f"Required ProjectPermit tool not found: {required_tool}")

            info_result = await session.call_tool("projectpermit_info", {})
            if info_result.is_error:
                raise SystemExit(f"ProjectPermit info tool returned error: {info_result}")
            info = _structured_or_text(info_result)
            jurisdictions = set(info.get("jurisdictions") or [])
            families = set(info.get("project_families") or [])
            example = info.get("example") or {}
            if jurisdictions != EXPECTED_JURISDICTIONS:
                raise SystemExit(f"Unexpected info jurisdictions: {sorted(jurisdictions)}")
            if families != EXPECTED_PROJECT_FAMILIES:
                raise SystemExit(f"Unexpected info project families: {sorted(families)}")
            if example.get("jurisdiction") != "ottawa_on":
                raise SystemExit(f"Starter example missing/invalid: {example}")
            if info.get("bulk_tool") != "check_project_requirements_batch":
                raise SystemExit(f"Bulk tool missing from info: {info}")
            if info.get("bulk_max_items") != 50:
                raise SystemExit(f"Unexpected bulk_max_items: {info.get('bulk_max_items')}")
            bundle_info = info.get("action_bundle") or {}
            includes = set(bundle_info.get("includes") or [])
            if bundle_info.get("field") != "action_bundle" or not {"identity", "change", "tasks", "mutation_gate"}.issubset(includes):
                raise SystemExit(f"Identity/action bundle contract missing from free MCP info: {bundle_info}")
            identity_info = info.get("decision_identity") or {}
            if identity_info.get("repeat_check_input") != "context.prior_decision_identity":
                raise SystemExit(f"Decision identity repeat contract missing from info: {identity_info}")
            gate_info = info.get("mutation_gate") or {}
            if set(gate_info.get("states") or []) != {
                "READY_FOR_EXPLICIT_WRITE",
                "NOOP_UNCHANGED",
                "BLOCKED",
            }:
                raise SystemExit(f"Mutation gate discovery missing states: {gate_info}")
            if gate_info.get("external_mutation_performed_by_projectpermit") is not False:
                raise SystemExit(f"Free MCP must advertise no external mutation execution: {gate_info}")
            print("remote_mcp_info_safe_writeback=PASS")
            print("remote_mcp_info_identity=PASS")

            batch_result = await session.call_tool(
                "check_project_requirements_batch",
                {
                    "items": [
                        {
                            "client_ref": "smoke-good",
                            "jurisdiction": "ottawa_on",
                            "project": {"family": "window_door", "action": "replace_same_size"},
                            "property": {"heritage": False},
                            "context": INTERNAL_CONTEXT,
                        },
                        {
                            "client_ref": "smoke-bad",
                            "jurisdiction": "ottawa_on",
                            "context": INTERNAL_CONTEXT,
                        },
                    ]
                },
            )
            if batch_result.is_error:
                raise SystemExit(f"Bulk MCP tool returned top-level error: {batch_result}")
            batch = _structured_or_text(batch_result)
            if batch.get("batch_size") != 2 or batch.get("succeeded") != 1 or batch.get("failed") != 1:
                raise SystemExit(f"Unexpected bulk MCP counts: {batch}")
            good, bad = batch.get("results") or [None, None]
            if not good or good.get("client_ref") != "smoke-good" or good.get("ok") is not True:
                raise SystemExit(f"Bulk MCP good-item correlation failed: {good}")
            good_result = good.get("result") or {}
            good_bundle = _assert_action_bundle(good_result, expected_route="CONTINUE_WITH_EVIDENCE")
            if (good_bundle.get("mutation_gate") or {}).get("state") != "BLOCKED":
                raise SystemExit(f"Unscoped batch item should remain writeback-blocked: {good_bundle}")
            if not bad or bad.get("client_ref") != "smoke-bad" or bad.get("ok") is not False:
                raise SystemExit(f"Bulk MCP bad-item isolation failed: {bad}")
            print("remote_bulk_mcp_identity=PASS")

            first_ottawa_identity = None
            first_ottawa_key = None
            for jurisdiction, project, property_facts, expected in CASES:
                result = await session.call_tool(
                    "check_project_requirements",
                    {
                        "jurisdiction": jurisdiction,
                        "project": project,
                        "property": property_facts,
                        "context": _scoped_context(jurisdiction),
                    },
                )
                if result.is_error:
                    raise SystemExit(f"MCP tool returned error for {jurisdiction}: {result}")
                payload = _structured_or_text(result)
                actual = payload.get("determination")
                municipality = (payload.get("jurisdiction") or {}).get("municipality")
                print(f"case={jurisdiction} municipality={municipality} determination={actual}")
                if actual != expected:
                    raise SystemExit(
                        f"Unexpected determination for {jurisdiction}: expected {expected}, got {actual}: {payload}"
                    )
                bundle = _assert_action_bundle(payload)
                gate = bundle.get("mutation_gate") or {}
                if jurisdiction == "ottawa_on":
                    if gate.get("state") != "READY_FOR_EXPLICIT_WRITE":
                        raise SystemExit(f"Scoped safe Ottawa result should be READY: {gate}")
                    first_ottawa_identity = bundle["identity"]
                    first_ottawa_key = first_ottawa_identity["idempotency_key"]

            repeat = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "ottawa_on",
                    "project": {"family": "window_door", "action": "replace_same_size"},
                    "property": {"heritage": False},
                    "context": {
                        **_scoped_context("ottawa_on"),
                        "prior_decision_identity": first_ottawa_identity,
                    },
                },
            )
            if repeat.is_error:
                raise SystemExit(f"Repeat identity MCP call failed: {repeat}")
            repeat_payload = _structured_or_text(repeat)
            repeat_bundle = _assert_action_bundle(repeat_payload, expected_route="CONTINUE_WITH_EVIDENCE")
            if (repeat_bundle.get("change") or {}).get("classification") != "UNCHANGED":
                raise SystemExit(f"Repeat check did not classify UNCHANGED: {repeat_bundle}")
            if (repeat_bundle.get("identity") or {}).get("idempotency_key") != first_ottawa_key:
                raise SystemExit(f"Repeat check changed idempotency key: {repeat_bundle}")
            repeat_gate = repeat_bundle.get("mutation_gate") or {}
            if repeat_gate.get("state") != "NOOP_UNCHANGED":
                raise SystemExit(f"Repeat scoped safe MCP check did not suppress duplicate: {repeat_gate}")
            if repeat_gate.get("recommended_operation") != "NOOP":
                raise SystemExit(f"Repeat scoped safe MCP check must recommend NOOP: {repeat_gate}")
            print("remote_mcp_safe_writeback_ready_then_noop=PASS")
            print("remote_mcp_repeat_idempotency=PASS")

            address_result = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "vancouver_bc",
                    "address": "453 W 12TH AVE, Vancouver, BC",
                    "resolve_address": True,
                    "project": {"family": "interior_renovation", "action": "painting"},
                    "context": INTERNAL_CONTEXT,
                },
            )
            if address_result.is_error:
                raise SystemExit(f"Vancouver address-aware MCP call failed: {address_result}")
            address_payload = _structured_or_text(address_result)
            address_bundle = _assert_action_bundle(address_payload)
            if (address_bundle.get("mutation_gate") or {}).get("state") != "BLOCKED":
                raise SystemExit(f"Unscoped address query must remain writeback-blocked: {address_bundle}")
            resolution = ((address_payload.get("address_context") or {}).get("address_resolution") or {})
            matched = str(resolution.get("matched_address") or "")
            zoning = ((address_payload.get("address_context") or {}).get("property") or {}).get("zoning_code")
            if not matched.startswith("453 ") or not zoning:
                raise SystemExit(f"Unexpected Vancouver address resolution: {address_payload}")
            print("vancouver_address_aware_preflight=PASS")

            print("remote_mcp_identity=PASS")
            print("remote_mcp_seven_jurisdictions=PASS")
            print("remote_mcp_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
