"""x402-native paid MCP transport for ProjectPermit.

This server uses MCP Python SDK v2 plus the transport-agnostic x402 MCP payment
wrapper. BuildRequirements remains payment-agnostic; payment is enforced only at
the MCP tool boundary. HTTP, free MCP and paid MCP share the same preflight service.
"""
from __future__ import annotations

import json
import os
from typing import Any

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import CallToolResult, TextContent

from x402.extensions.bazaar import (
    DeclareMcpDiscoveryConfig,
    declare_mcp_discovery_extension,
)
from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mcp import (
    MCPToolResult,
    ResourceInfo,
    SyncPaymentWrapperConfig,
    create_payment_wrapper_sync,
)
from x402.schemas import ResourceConfig
from x402.server import x402ResourceServerSync

from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight


TOOL_NAME = "check_project_requirements"

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "jurisdiction": {
            "type": "string",
            "enum": list(SUPPORTED_JURISDICTIONS),
            "description": "Supported municipality identifier.",
        },
        "project": {
            "type": "object",
            "description": "Normalized project facts such as family, action, structural_change and estimated_cost_cad.",
        },
        "address": {
            "type": ["string", "null"],
            "description": "Optional civic address for address-aware preflight where a resolver is available.",
        },
        "property": {
            "type": "object",
            "description": "Known property overlays/facts such as heritage or PIIA status.",
        },
        "context": {
            "type": "object",
            "description": "Optional rule-version or workflow context.",
        },
        "resolve_address": {
            "type": "boolean",
            "description": "When true, enrich the request from first-party municipal address/GIS data before rule evaluation where supported.",
            "default": False,
        },
    },
    "required": ["jurisdiction", "project"],
    "additionalProperties": False,
}

EXAMPLE = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
    "resolve_address": False,
}


def _settings() -> dict[str, str]:
    return {
        "pay_to": os.getenv("PROJECTPERMIT_X402_PAY_TO", "").strip(),
        "network": os.getenv("PROJECTPERMIT_X402_NETWORK", "eip155:84532").strip(),
        "price": os.getenv("PROJECTPERMIT_X402_PRICE_USD", "$0.01").strip(),
        "facilitator_url": os.getenv(
            "PROJECTPERMIT_X402_FACILITATOR_URL", "https://x402.org/facilitator"
        ).strip(),
    }


def _to_call_tool_result(result: MCPToolResult) -> CallToolResult:
    """Bridge x402's transport-neutral MCP result into MCP SDK v2 types."""
    content = []
    for item in result.content:
        if item.get("type") == "text":
            content.append(TextContent(type="text", text=str(item.get("text", ""))))
        else:
            content.append(TextContent(type="text", text=json.dumps(item, ensure_ascii=False)))

    return CallToolResult(
        content=content,
        is_error=result.is_error,
        structured_content=result.structured_content,
        _meta=result.meta or None,
    )


def build_paid_server() -> MCPServer:
    settings = _settings()
    if not settings["pay_to"]:
        raise RuntimeError("PROJECTPERMIT_X402_PAY_TO is required for paid MCP")
    if not settings["network"].startswith("eip155:"):
        raise RuntimeError("ProjectPermit paid MCP supports EVM eip155:* networks only")

    server = MCPServer(
        "ProjectPermit x402",
        instructions=(
            "Paid evidence-linked municipal construction permit preflight. "
            "The check_project_requirements tool uses x402 USDC payment. "
            "Results are preflight information, not municipal authorization."
        ),
    )

    facilitator = HTTPFacilitatorClientSync(
        FacilitatorConfig(url=settings["facilitator_url"])
    )
    resource_server = x402ResourceServerSync(facilitator)
    resource_server.register(settings["network"], ExactEvmServerScheme())
    resource_server.initialize()

    accepts = resource_server.build_payment_requirements(
        ResourceConfig(
            scheme="exact",
            network=settings["network"],
            pay_to=settings["pay_to"],
            price=settings["price"],
            extra={"name": "USDC", "version": "2"},
        )
    )

    extensions = declare_mcp_discovery_extension(
        DeclareMcpDiscoveryConfig(
            tool_name=TOOL_NAME,
            description=(
                "Evidence-linked municipal construction permit/planning preflight for "
                "Gatineau, Ottawa, Toronto, Mississauga, Laval and Longueuil. Returns "
                "deterministic requirements and official-source evidence."
            ),
            transport="streamable-http",
            input_schema=INPUT_SCHEMA,
            example=EXAMPLE,
        )
    )

    wrapper = create_payment_wrapper_sync(
        resource_server,
        SyncPaymentWrapperConfig(
            accepts=accepts,
            resource=ResourceInfo(
                url=f"mcp://tool/{TOOL_NAME}",
                description=(
                    "Evidence-linked Canadian municipal permit preflight. Not municipal "
                    "authorization, legal advice, or engineering certification."
                ),
                service_name="ProjectPermit",
                tags=[
                    "building-permit",
                    "construction",
                    "renovation",
                    "ontario",
                    "quebec",
                    "canada",
                ],
            ),
            extensions=extensions,
        ),
    )

    def execute(args: dict[str, Any], _: Any) -> MCPToolResult:
        result = run_preflight(
            {
                "jurisdiction": args["jurisdiction"],
                "project": args["project"],
                "address": args.get("address"),
                "property": args.get("property") or {},
                "context": args.get("context") or {},
                "resolve_address": bool(args.get("resolve_address", False)),
            }
        )
        return MCPToolResult(
            content=[{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
            structured_content=result,
        )

    paid_tool = wrapper(execute)

    @server.tool()
    def projectpermit_info() -> dict[str, Any]:
        """Free discovery/status tool; does not perform a permit determination."""
        return {
            "service": "ProjectPermit",
            "paid_tool": TOOL_NAME,
            "price": settings["price"],
            "network": settings["network"],
            "jurisdictions": list(SUPPORTED_JURISDICTIONS),
            "address_resolution_jurisdictions": list(SUPPORTED_ADDRESS_JURISDICTIONS),
            "disclaimer": "Preflight information only; not municipal authorization.",
        }

    @server.tool()
    def check_project_requirements(
        jurisdiction: str,
        project: dict[str, Any],
        ctx: Context,
        address: str | None = None,
        property: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        resolve_address: bool = False,
    ) -> CallToolResult:
        """Paid evidence-linked permit preflight. Requires x402 USDC payment."""
        request_meta = dict(ctx.request_context.meta or {})
        result = paid_tool(
            {
                "jurisdiction": jurisdiction,
                "project": project,
                "address": address,
                "property": property or {},
                "context": context or {},
                "resolve_address": resolve_address,
            },
            {"_meta": request_meta, "toolName": TOOL_NAME},
        )
        return _to_call_tool_result(result)

    return server


def main() -> None:
    railway_port = os.getenv("PORT")
    host = os.getenv(
        "PROJECTPERMIT_PAID_MCP_HOST",
        "0.0.0.0" if railway_port else "127.0.0.1",
    )
    port = int(os.getenv("PROJECTPERMIT_PAID_MCP_PORT") or railway_port or "4022")
    build_paid_server().run(
        transport="streamable-http",
        host=host,
        port=port,
        json_response=True,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
