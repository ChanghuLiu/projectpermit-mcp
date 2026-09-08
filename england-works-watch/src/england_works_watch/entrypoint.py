"""Production entrypoint with machine-discovery catalog routes.

The deterministic decision server remains in ``server.py``. This module adds
catalog surfaces and benchmark-driven MCP selection metadata, then delegates
to the canonical server entrypoint.
"""
from __future__ import annotations

from starlette.responses import JSONResponse

from . import server
from .selection_metadata import apply_selection_metadata

# The server module has already registered every tool by import time. Override
# only advertised discovery metadata/schemas; deterministic execution stays in
# server.py and policy.py.
apply_selection_metadata(server.mcp)


@server.mcp.custom_route("/.well-known/ai-catalog.json", methods=["GET"])
async def ai_catalog(_request):
    """Machine-readable catalog advertising both MCP and OpenAPI interfaces."""
    return JSONResponse(
        {
            "name": "England Works Watch",
            "version": server.SERVICE_VERSION,
            "description": "UK sponsor compliance/change intelligence for Skilled Worker sponsor duties.",
            "interfaces": [
                {
                    "type": "mcp",
                    "transport": "streamable-http",
                    "url": server.PUBLIC_MCP_URL,
                },
                {
                    "type": "openapi",
                    "url": f"{server.PUBLIC_ORIGIN}/openapi.json",
                },
            ],
            "discovery": {
                "mcp_manifest": f"{server.PUBLIC_ORIGIN}/.well-known/mcp.json",
                "mcp_server_card": f"{server.PUBLIC_ORIGIN}/.well-known/mcp/server-card.json",
                "agent_card": f"{server.PUBLIC_ORIGIN}/.well-known/agent-card.json",
                "llms": f"{server.PUBLIC_ORIGIN}/llms.txt",
                "x402": f"{server.PUBLIC_ORIGIN}/.well-known/x402",
            },
            "scope": "Skilled Worker sponsor duties only",
            "payment": server._payment_info(),
            "evidence_policy": "Official GOV.UK sources are fingerprint-monitored; changed or stale evidence fails closed.",
        }
    )


@server.mcp.custom_route("/.well-known/api-catalog", methods=["GET"])
async def api_catalog(_request):
    """RFC-style linkset for crawlers that discover machine APIs by relation."""
    payload = {
        "linkset": [
            {
                "anchor": server.PUBLIC_ORIGIN,
                "service-desc": [
                    {
                        "href": f"{server.PUBLIC_ORIGIN}/openapi.json",
                        "type": "application/openapi+json",
                    },
                    {
                        "href": f"{server.PUBLIC_ORIGIN}/.well-known/mcp.json",
                        "type": "application/json",
                    },
                    {
                        "href": server.PUBLIC_MCP_URL,
                        "type": "application/json",
                    },
                ],
                "describedby": [
                    {
                        "href": f"{server.PUBLIC_ORIGIN}/llms.txt",
                        "type": "text/plain",
                    },
                    {
                        "href": f"{server.PUBLIC_ORIGIN}/.well-known/x402",
                        "type": "application/json",
                    },
                ],
            }
        ]
    }
    return JSONResponse(payload, media_type="application/linkset+json")


def main() -> None:
    server.main()


if __name__ == "__main__":
    main()
