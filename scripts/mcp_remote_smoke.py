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
            print("remote_mcp_info=PASS")

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
            batch_items = batch.get("results") or []
            if len(batch_items) != 2:
                raise SystemExit(f"Unexpected bulk MCP result count: {batch}")
            good, bad = batch_items
            if good.get("client_ref") != "smoke-good" or good.get("ok") is not True:
                raise SystemExit(f"Bulk MCP good-item correlation failed: {good}")
            if (good.get("result") or {}).get("determination") != "LIKELY_NOT_REQUIRED":
                raise SystemExit(f"Bulk MCP good-item determination failed: {good}")
            if bad.get("client_ref") != "smoke-bad" or bad.get("ok") is not False:
                raise SystemExit(f"Bulk MCP bad-item isolation failed: {bad}")
            if (bad.get("error") or {}).get("type") != "validation_error":
                raise SystemExit(f"Bulk MCP bad-item error type failed: {bad}")
            audit = batch.get("audit") or {}
            if int(audit.get("unique_rule_ids") or 0) < 1 or int(audit.get("evidence_links") or 0) < 1:
                raise SystemExit(f"Bulk MCP audit incomplete: {audit}")
            print("remote_bulk_mcp_smoke=PASS")

            for jurisdiction, project, property_facts, expected in CASES:
                result = await session.call_tool(
                    "check_project_requirements",
                    {
                        "jurisdiction": jurisdiction,
                        "project": project,
                        "property": property_facts,
                        "context": INTERNAL_CONTEXT,
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
