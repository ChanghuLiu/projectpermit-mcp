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

from .capabilities import PROJECT_FAMILIES
from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .mcp_input_models import (
    CivicAddress,
    JurisdictionId,
    ProjectFacts,
    PropertyFactsInput,
    ResolveAddress,
    WorkflowContextInput,
    model_or_mapping,
    paid_mcp_input_schema,
)
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight


TOOL_NAME = "check_project_requirements"
INPUT_SCHEMA: dict[str, Any] = paid_mcp_input_schema()

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
            "Paid evidence-linked municipal construction permit preflight for contractor "
            "and field-service agents. Start with projectpermit_info for capabilities. "
            "The check_project_requirements tool uses x402 USDC payment and returns the "
            "permit determination, workflow guidance, evidence freshness and a platform-neutral "
            "action bundle with proposed tasks, official evidence, audit metadata, deterministic "
            "identity, idempotency key, change classification and a safe-writeback mutation gate. "
            "Start project facts with family + action and supply only known facts; unknown "
            "municipal-specific facts remain accepted for forward compatibility. Pass a prior "
            "identity in context.prior_decision_identity for repeated checks. The gate can classify "
            "READY_FOR_EXPLICIT_WRITE, NOOP_UNCHANGED or BLOCKED, but ProjectPermit does not itself "
            "execute external mutations. Results are preflight information, not municipal authorization."
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
                "Gatineau, Ottawa, Toronto, Mississauga, Laval, Longueuil and Vancouver. "
                "Returns deterministic requirements, official-source evidence, freshness-guarded "
                "workflow routing, action/evidence bundle, deterministic decision fingerprints, "
                "idempotency key, repeat-check change classification and safe-writeback mutation "
                "gate for contractor/field-service Agents."
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
                    "Evidence-linked Canadian municipal permit preflight with freshness-guarded "
                    "workflow routing, action/evidence bundle, duplicate-suppression identity and "
                    "safe-writeback gate. Not municipal authorization, legal advice, or engineering "
                    "certification."
                ),
                service_name="ProjectPermit",
                tags=[
                    "building-permit",
                    "construction",
                    "renovation",
                    "contractor-workflow",
                    "field-service",
                    "agent-routing",
                    "evidence-bundle",
                    "action-bundle",
                    "idempotency",
                    "change-detection",
                    "safe-writeback",
                    "mutation-gate",
                    "ontario",
                    "quebec",
                    "british-columbia",
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
            "project_families": list(PROJECT_FAMILIES),
            "workflow_guidance": {
                "field": "workflow",
                "includes": [
                    "recommended_route",
                    "quote_handling",
                    "automation_safe",
                    "follow_up_questions",
                    "evidence_freshness",
                ],
            },
            "action_bundle": {
                "field": "action_bundle",
                "includes": [
                    "identity",
                    "change",
                    "decision",
                    "routing",
                    "required_inputs",
                    "tasks",
                    "evidence",
                    "audit",
                    "writeback_hints",
                    "mutation_gate",
                ],
                "integration_proposals": ["jobber", "servicem8"],
            },
            "decision_identity": {
                "field": "action_bundle.identity",
                "repeat_check_input": "context.prior_decision_identity",
                "idempotency_field": "action_bundle.identity.idempotency_key",
                "change_field": "action_bundle.change",
                "purpose": "Suppress duplicate downstream work and distinguish operational change from rules/evidence refresh.",
            },
            "mutation_gate": {
                "field": "action_bundle.mutation_gate",
                "states": [
                    "READY_FOR_EXPLICIT_WRITE",
                    "NOOP_UNCHANGED",
                    "BLOCKED",
                ],
                "write_contract": "explicit_authorized_atomic_upsert_by_idempotency_key",
                "unconditional_create_allowed": False,
                "external_mutation_performed_by_projectpermit": False,
            },
            "safe_writeback_proposals": {
                "jobber": "mutation_gate_supported",
                "servicem8": "mutation_gate_supported",
                "execution": "not_enabled_in_projectpermit",
            },
            "example": EXAMPLE,
            "disclaimer": "Preflight information only; not municipal authorization.",
        }

    @server.tool()
    def check_project_requirements(
        jurisdiction: JurisdictionId,
        project: ProjectFacts,
        ctx: Context,
        address: CivicAddress = None,
        property: PropertyFactsInput = None,
        context: WorkflowContextInput = None,
        resolve_address: ResolveAddress = False,
    ) -> CallToolResult:
        """Paid evidence-linked permit preflight. Start project with family + action and add only known facts. Returns workflow/action bundle, identity, idempotency, change classification and safe-writeback mutation gate. Requires x402 USDC payment."""
        request_meta = dict(ctx.request_context.meta or {})
        project_facts = model_or_mapping(project)
        property_facts = model_or_mapping(property)
        context_facts = model_or_mapping(context)
        tool_context = {**context_facts, "_transport": "paid_mcp"}
        result = paid_tool(
            {
                "jurisdiction": jurisdiction,
                "project": project_facts,
                "address": address,
                "property": property_facts,
                "context": tool_context,
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
