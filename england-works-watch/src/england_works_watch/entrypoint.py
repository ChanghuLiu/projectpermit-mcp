"""Production entrypoint with machine-discovery catalog routes and telemetry.

The deterministic decision server remains in ``server.py``. This module adds
catalog surfaces, benchmark-driven MCP selection metadata, and privacy-minimal
HTTP discovery observability. It does not change regulatory rules, prices,
payment semantics, or tool execution.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
import os
import sys
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount

from . import server
from .analytics import record_discovery
from .selection_metadata import apply_selection_metadata

# The server module has already registered every tool by import time. Override
# only advertised discovery metadata/schemas; deterministic execution stays in
# server.py and policy.py.
apply_selection_metadata(server.mcp)

OWNER_DISCOVERY_HEADER = b"x-mcp-commercial-actor"
_OWNER_MARKERS = {"owned", "owned_ci", "owner", "test", "smoke"}
_DISCOVERY_PATHS = {
    "/",
    "/robots.txt",
    "/sitemap.xml",
    "/llms.txt",
    "/openapi.json",
    "/.well-known/x402",
    "/.well-known/mcp.json",
    "/.well-known/mcp/server-card.json",
    "/.well-known/agent-card.json",
    "/.well-known/agent.json",
    "/.well-known/glama.json",
    "/.well-known/ai-catalog.json",
    "/.well-known/api-catalog",
    "/mcp",
}


def _owned_probe(scope: dict[str, Any]) -> bool:
    """Check the one allow-listed owner marker without persisting headers."""
    for item in scope.get("headers") or []:
        try:
            key, value = item
        except Exception:
            continue
        if key.lower() != OWNER_DISCOVERY_HEADER:
            continue
        marker = value.decode("latin1", errors="ignore").strip().lower()
        return marker in _OWNER_MARKERS
    return False


class DiscoveryObservabilityASGI:
    """Record privacy-minimal hits to public machine discovery surfaces.

    Only the normalized route and timestamp are ultimately persisted by
    analytics.record_discovery(). No IP, user-agent, query, arbitrary headers,
    cookies, MCP payload, or payment material is retained. POST /mcp is not
    counted here because it may be a real business tool call rather than
    discovery; MCP tool telemetry remains the source for that layer.
    """

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope.get("type") == "http":
            path = str(scope.get("path") or "")
            method = str(scope.get("method") or "GET").upper()
            if (
                path in _DISCOVERY_PATHS
                and not _owned_probe(scope)
                and (path != "/mcp" or method in {"GET", "HEAD"})
            ):
                record_discovery(path)
        await self.app(scope, receive, send)


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


def _run_http() -> None:
    server.ensure_runtime_seeded()
    server.start_background_source_monitor()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    mcp_app = server.mcp.streamable_http_app(
        host=host,
        json_response=True,
        stateless_http=True,
    )

    @asynccontextmanager
    async def lifespan(_app):
        async with server.mcp.session_manager.run():
            yield

    app = Starlette(routes=[Mount("/", app=mcp_app)], lifespan=lifespan)
    app = DiscoveryObservabilityASGI(app)
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    # Preserve the existing CLI contract used by Railway and release smokes.
    if "--http" in sys.argv[1:]:
        _run_http()
    else:
        server.main()


if __name__ == "__main__":
    main()
