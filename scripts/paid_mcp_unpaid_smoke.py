"""Verify the public x402-native MCP server without spending funds."""
from __future__ import annotations

import asyncio
import json
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = os.getenv(
    "PROJECTPERMIT_PAID_MCP_URL",
    "https://projectpermit-x402-mcp-production.up.railway.app/mcp",
)
EXPECTED_NETWORK = os.getenv("PROJECTPERMIT_SMOKE_X402_NETWORK", "eip155:8453")
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
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            print(f"tools={names}")
            assert "projectpermit_info" in names
            assert "check_project_requirements" in names

            paid_tool = next(tool for tool in tools.tools if tool.name == "check_project_requirements")
            schema = getattr(paid_tool, "input_schema", None) or {}
            properties = schema.get("properties") or {}
            if "resolve_address" not in properties:
                raise SystemExit("Paid MCP input schema missing resolve_address")

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
            workflow = info_payload.get("workflow_guidance") or {}
            if workflow.get("field") != "workflow":
                raise SystemExit(f"Paid MCP info missing workflow guidance: {workflow}")
            print(f"free_info_jurisdictions={sorted(jurisdictions)}")
            print("free_info=PASS")

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
            if not any(item.get("network") == EXPECTED_NETWORK for item in accepts):
                raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")
            print("paid_mcp_seven_jurisdictions=PASS")
            print("paid_mcp_unpaid_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
