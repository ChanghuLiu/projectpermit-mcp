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

            for jurisdiction, project, property_facts, expected in CASES:
                result = await session.call_tool(
                    "check_project_requirements",
                    {"jurisdiction": jurisdiction, "project": project, "property": property_facts},
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

            # Real first-party municipal GIS smoke. Vancouver City Hall is a stable,
            # public civic address present in the City's property-address dataset.
            address_result = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "vancouver_bc",
                    "address": "453 W 12TH AVE, Vancouver, BC",
                    "resolve_address": True,
                    "project": {"family": "interior_renovation", "action": "painting"},
                },
            )
            if address_result.is_error:
                raise SystemExit(f"Vancouver address-aware MCP call failed: {address_result}")
            address_payload = _structured_or_text(address_result)
            address_context = address_payload.get("address_context") or {}
            resolution = address_context.get("address_resolution") or {}
            matched = str(resolution.get("matched_address") or "")
            zoning = (address_context.get("property") or {}).get("zoning_code")
            print(f"vancouver_address_matched={matched} zoning={zoning}")
            if not matched.startswith("453 "):
                raise SystemExit(f"Unexpected Vancouver address resolution: {address_payload}")
            if not zoning:
                raise SystemExit(f"Vancouver zoning was not resolved: {address_payload}")
            print("vancouver_address_aware_preflight=PASS")

            print("remote_mcp_seven_jurisdictions=PASS")
            print("remote_mcp_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
