"""x402-native paid MCP transport for ProjectPermit.

This server uses the official x402 Python MCP payment wrapper. The deterministic
BuildRequirements engine remains payment-agnostic; payment is applied only at the
MCP tool boundary.
"""
from __future__ import annotations

import json
import os
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import CallToolResult

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
    wrap_fastmcp_tool_sync,
)
from x402.schemas import ResourceConfig
from x402.server import x402ResourceServerSync

from .engine import evaluate_project


TOOL_NAME = "check_project_requirements"

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "jurisdiction": {
            "type": "string",
            "enum": ["gatineau_qc", "ottawa_on"],
            "description": "Phase 0 municipality identifier.",
        },
        "project": {
            "type": "object",
            "description": "Normalized project facts such as family, action, structural_change and estimated_cost_cad.",
        },
        "address": {
            "type": ["string", "null"],
            "description": "Optional civic address for address-aware preflight.",
        },
        "property": {
            "type": "object",
            "description": "Known property overlays/facts such as heritage or PIIA status.",
        },
        "context": {
            "type": "object",
            "description": "Optional rule-version or workflow context.",
        },
    },
    "required": ["jurisdiction", "project"],
    "additionalProperties": False,
}

EXAMPLE = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
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


def build_paid_server() -> FastMCP:
    settings = _settings()
    if not settings["pay_to"]:
        raise RuntimeError("PROJECTPERMIT_X402_PAY_TO is required for paid MCP")
    if not settings["network"].startswith("eip155:"):
        raise RuntimeError("Phase 0 paid MCP supports EVM eip155:* networks only")

    port = int(os.getenv("PORT") or os.getenv("PROJECTPERMIT_PAID_MCP_PORT") or "4022")
    host = os.getenv(
        "PROJECTPERMIT_PAID_MCP_HOST",
        "0.0.0.0" if os.getenv("PORT") else "127.0.0.1",
    )
    server = FastMCP("ProjectPermit x402", host=host, port=port)

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
                "Gatineau, Quebec and Ottawa, Ontario. Returns determination, reasons, "
                "property flags, unresolved questions, and official-source evidence."
            ),
            transport="sse",
            input_schema=INPUT_SCHEMA,
            example=EXAMPLE,
        )
    )

    paid = create_payment_wrapper_sync(
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
                    "ottawa",
                    "gatineau",
                    "canada",
                ],
            ),
            extensions=extensions,
        ),
    )

    def execute(args: dict[str, Any], _: Any) -> MCPToolResult:
        payload = {
            "jurisdiction": args["jurisdiction"],
            "project": args["project"],
            "address": args.get("address"),
            "property": args.get("property") or {},
            "context": args.get("context") or {},
        }
        result = evaluate_project(payload)
        return MCPToolResult(
            content=[{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
            structured_content=result,
        )

    paid_tool = wrap_fastmcp_tool_sync(paid, execute, tool_name=TOOL_NAME)

    @server.tool(name="projectpermit_info")
    def projectpermit_info() -> dict[str, Any]:
        """Free discovery/status tool; does not perform a permit determination."""
        return {
            "service": "ProjectPermit",
            "paid_tool": TOOL_NAME,
            "price": settings["price"],
            "network": settings["network"],
            "jurisdictions": ["gatineau_qc", "ottawa_on"],
            "disclaimer": "Preflight information only; not municipal authorization.",
        }

    @server.tool(name=TOOL_NAME)
    def check_project_requirements(
        jurisdiction: str,
        project: dict[str, Any],
        ctx: Context,
        address: str | None = None,
        property: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> CallToolResult:
        """Paid evidence-linked permit preflight. Requires x402 USDC payment."""
        return paid_tool(
            {
                "jurisdiction": jurisdiction,
                "project": project,
                "address": address,
                "property": property or {},
                "context": context or {},
            },
            ctx,
        )

    return server


def main() -> None:
    server = build_paid_server()
    # Official x402 Python MCP integration currently uses FastMCP's SSE adapter.
    server.run(transport="sse")


if __name__ == "__main__":
    main()
