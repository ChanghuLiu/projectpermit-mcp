"""Verify the public x402-native MCP server without spending funds."""
from __future__ import annotations

import asyncio
import json
import os
from decimal import Decimal

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = os.getenv(
    "PROJECTPERMIT_PAID_MCP_URL",
    "https://projectpermit-x402-mcp-production.up.railway.app/mcp",
)
EXPECTED_NETWORK = os.getenv("PROJECTPERMIT_SMOKE_X402_NETWORK", "eip155:8453")
EXPECTED_PRICE_USD = os.getenv("PROJECTPERMIT_SMOKE_X402_SINGLE_AMOUNT", "0.20")
EXPECTED_WIRE_AMOUNT = str(int(Decimal(EXPECTED_PRICE_USD) * Decimal("1000000")))
EXPECTED_JURISDICTIONS = {
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "laval_qc",
    "longueuil_qc",
    "vancouver_bc",
}


def _json_from_result(result):
    structured = getattr(result, "structured_content", None)
    if structured:
        return structured
    rendered = "\n".join(getattr(block, "text", "") for block in result.content)
    return json.loads(rendered)


async def main() -> None:
    print(f"paid_mcp_url={URL}")
    print(f"expected_network={EXPECTED_NETWORK}")
    print(f"expected_price_usd={EXPECTED_PRICE_USD}")
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            print(f"tools={names}")
            assert "projectpermit_info" in names
            assert "check_project_requirements" in names

            # MCP SDK tools/list generates this schema from the Python function
            # signature. Plain dict parameters retain presence/type but not the
            # richer INPUT_SCHEMA description used by x402 discovery metadata.
            paid_tool = next(tool for tool in tools.tools if tool.name == "check_project_requirements")
            schema = getattr(paid_tool, "input_schema", None) or {}
            properties = schema.get("properties") or {}
            if "resolve_address" not in properties or "context" not in properties:
                raise SystemExit("Paid MCP input schema missing resolve_address/context")

            info = await session.call_tool("projectpermit_info", {})
            assert not info.is_error, info
            info_payload = _json_from_result(info)
            jurisdictions = set(info_payload.get("jurisdictions") or [])
            if not EXPECTED_JURISDICTIONS.issubset(jurisdictions):
                raise SystemExit(f"Paid MCP info missing jurisdictions: {jurisdictions}")
            if info_payload.get("network") != EXPECTED_NETWORK:
                raise SystemExit(
                    f"Paid MCP info network mismatch: {info_payload.get('network')} != {EXPECTED_NETWORK}"
                )
            bundle = info_payload.get("action_bundle") or {}
            includes = set(bundle.get("includes") or [])
            if bundle.get("field") != "action_bundle" or not {"identity", "change", "tasks", "evidence", "mutation_gate"}.issubset(includes):
                raise SystemExit(f"Paid MCP action bundle missing identity/change/mutation gate contract: {bundle}")
            integrations = set(bundle.get("integration_proposals") or [])
            if not {"jobber", "servicem8"}.issubset(integrations):
                raise SystemExit(f"Paid MCP action bundle missing integration proposals: {bundle}")
            identity = info_payload.get("decision_identity") or {}
            if identity.get("repeat_check_input") != "context.prior_decision_identity":
                raise SystemExit(f"Paid MCP decision identity contract missing: {identity}")
            if identity.get("idempotency_field") != "action_bundle.identity.idempotency_key":
                raise SystemExit(f"Paid MCP idempotency contract missing: {identity}")
            gate = info_payload.get("mutation_gate") or {}
            if set(gate.get("states") or []) != {
                "READY_FOR_EXPLICIT_WRITE",
                "NOOP_UNCHANGED",
                "BLOCKED",
            }:
                raise SystemExit(f"Paid MCP mutation gate states missing: {gate}")
            if gate.get("write_contract") != "explicit_authorized_atomic_upsert_by_idempotency_key":
                raise SystemExit(f"Paid MCP safe-writeback contract missing: {gate}")
            if gate.get("unconditional_create_allowed") is not False:
                raise SystemExit(f"Paid MCP must forbid unconditional creates: {gate}")
            if gate.get("external_mutation_performed_by_projectpermit") is not False:
                raise SystemExit(f"Paid MCP must advertise no external mutation execution: {gate}")
            writeback = info_payload.get("safe_writeback_proposals") or {}
            if writeback.get("jobber") != "mutation_gate_supported" or writeback.get("servicem8") != "mutation_gate_supported":
                raise SystemExit(f"Paid MCP safe writeback proposals missing: {writeback}")
            print("free_info_safe_writeback=PASS")
            print("free_info_identity=PASS")

            result = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "vancouver_bc",
                    "project": {"family": "interior_renovation", "action": "painting"},
                },
            )
            print(f"paid_without_payment_is_error={result.is_error}")
            print(f"challenge={json.dumps(result.structured_content, default=str)}")
            if not result.is_error:
                raise SystemExit("Paid MCP tool unexpectedly executed without payment")
            challenge = result.structured_content or {}
            if not challenge.get("accepts"):
                raise SystemExit("x402 payment challenge did not include accepts")
            accepts = challenge["accepts"]
            matching = [item for item in accepts if item.get("network") == EXPECTED_NETWORK]
            if not matching:
                raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")
            if not any(
                str(item.get("amount")) == EXPECTED_WIRE_AMOUNT
                and ((item.get("extra") or {}).get("name") == "USDC")
                for item in matching
            ):
                raise SystemExit(
                    f"Paid MCP runtime price mismatch: expected ${EXPECTED_PRICE_USD} USDC "
                    f"({EXPECTED_WIRE_AMOUNT} base units): {matching}"
                )
            print("paid_mcp_runtime_price=PASS")
            print("paid_mcp_safe_writeback_discovery=PASS")
            print("paid_mcp_identity_discovery=PASS")
            print("paid_mcp_seven_jurisdictions=PASS")
            print("paid_mcp_unpaid_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
