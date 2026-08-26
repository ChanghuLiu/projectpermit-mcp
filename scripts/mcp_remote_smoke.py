"""End-to-end smoke test for the public ProjectPermit MCP endpoint."""
from __future__ import annotations

import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = os.getenv(
    "PROJECTPERMIT_MCP_URL",
    "https://projectpermit-mcp-production.up.railway.app/mcp",
)


async def main() -> None:
    print(f"mcp_url={URL}")
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            print(f"tools={names}")
            if "check_project_requirements" not in names:
                raise SystemExit("ProjectPermit tool not found")

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
            if result.is_error:
                raise SystemExit(f"MCP tool returned error: {result}")

            rendered = "\n".join(
                getattr(block, "text", "") for block in result.content
            )
            print(rendered)
            if "LIKELY_NOT_REQUIRED" not in rendered:
                structured = getattr(result, "structured_content", None)
                print(f"structured={structured}")
                if not structured or structured.get("determination") != "LIKELY_NOT_REQUIRED":
                    raise SystemExit("Unexpected ProjectPermit determination")

            print("remote_mcp_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
