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


async def main() -> None:
    print(f"paid_mcp_url={URL}")
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            print(f"tools={names}")
            assert "projectpermit_info" in names
            assert "check_project_requirements" in names

            info = await session.call_tool("projectpermit_info", {})
            assert not info.is_error, info
            print("free_info=PASS")

            result = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "ottawa_on",
                    "project": {
                        "family": "window_door",
                        "action": "replace_same_size",
                    },
                    "property": {"heritage": False},
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
            if not any(item.get("network") == "eip155:84532" for item in accepts):
                raise SystemExit("Base Sepolia payment option missing")
            print("paid_mcp_unpaid_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
