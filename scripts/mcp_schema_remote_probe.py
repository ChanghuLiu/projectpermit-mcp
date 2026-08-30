"""Read-only probe for the public ProjectPermit MCP tools/list schema.

This script performs only MCP initialize + tools/list. It never calls a ProjectPermit
business tool, sends payment, or submits data. The purpose is to observe whether external
agents receive sufficiently structured input schemas for first-call success.
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


URL = os.getenv(
    "PROJECTPERMIT_MCP_URL",
    "https://projectpermit-mcp-production.up.railway.app/mcp",
)
TARGET_TOOLS = (
    "projectpermit_info",
    "check_project_requirements",
    "check_project_requirements_batch",
)


def _tool_dump(tool: Any) -> dict[str, Any]:
    if hasattr(tool, "model_dump"):
        return tool.model_dump(by_alias=True, exclude_none=True)
    result: dict[str, Any] = {}
    for name in ("name", "description", "inputSchema", "input_schema"):
        value = getattr(tool, name, None)
        if value is not None:
            result[name] = value
    return result


def _schema(data: dict[str, Any]) -> dict[str, Any]:
    value = data.get("inputSchema") or data.get("input_schema") or {}
    return value if isinstance(value, dict) else {}


def _schema_quality(name: str, schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    result: dict[str, Any] = {
        "top_level_property_names": sorted(properties),
        "top_level_required": schema.get("required") or [],
    }
    if name == "check_project_requirements":
        project = properties.get("project") if isinstance(properties.get("project"), dict) else {}
        project_properties = (
            project.get("properties") if isinstance(project.get("properties"), dict) else {}
        )
        result.update(
            {
                "project_type": project.get("type"),
                "project_has_nested_properties": bool(project_properties),
                "project_nested_property_names": sorted(project_properties),
                "project_allows_additional_properties": project.get("additionalProperties"),
            }
        )
    elif name == "check_project_requirements_batch":
        items = properties.get("items") if isinstance(properties.get("items"), dict) else {}
        item_schema = items.get("items") if isinstance(items.get("items"), dict) else {}
        item_properties = (
            item_schema.get("properties")
            if isinstance(item_schema.get("properties"), dict)
            else {}
        )
        result.update(
            {
                "batch_items_type": items.get("type"),
                "batch_item_has_nested_properties": bool(item_properties),
                "batch_item_nested_property_names": sorted(item_properties),
                "batch_item_allows_additional_properties": item_schema.get("additionalProperties"),
            }
        )
    return result


async def main() -> None:
    report: dict[str, Any] = {
        "mcp_url": URL,
        "operation": "initialize_plus_tools_list_only",
        "business_tool_called": False,
        "payment_sent": False,
        "tools": {},
    }
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            report["server"] = init.server_info.name
            listed = await session.list_tools()
            by_name = {tool.name: tool for tool in listed.tools}
            missing = [name for name in TARGET_TOOLS if name not in by_name]
            if missing:
                raise SystemExit(f"missing public tools: {missing}")

            for name in TARGET_TOOLS:
                data = _tool_dump(by_name[name])
                schema = _schema(data)
                report["tools"][name] = {
                    "description": data.get("description"),
                    "input_schema": schema,
                    "quality": _schema_quality(name, schema),
                }

    single_quality = report["tools"]["check_project_requirements"]["quality"]
    batch_quality = report["tools"]["check_project_requirements_batch"]["quality"]
    report["summary"] = {
        "single_project_schema": (
            "STRUCTURED" if single_quality.get("project_has_nested_properties") else "GENERIC_OBJECT"
        ),
        "batch_item_schema": (
            "STRUCTURED" if batch_quality.get("batch_item_has_nested_properties") else "GENERIC_OBJECT"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
