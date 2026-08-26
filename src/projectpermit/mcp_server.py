"""Standard MCP transport for ProjectPermit.

Payment is deliberately not embedded here. HTTP, standard MCP and paid MCP all
call the same shared address-aware preflight service.
"""
from __future__ import annotations

import os
from typing import Any

from .preflight_service import run_preflight


def build_server():
    try:
        from mcp.server import MCPServer
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "MCP support is optional. Install with: pip install -e '.[mcp]'"
        ) from exc

    server = MCPServer(
        "ProjectPermit",
        instructions=(
            "Municipal construction permit preflight. Normalize the user's proposed "
            "construction scope into structured facts before calling the tool. Results "
            "are evidence-linked preflight information, not municipal authorization."
        ),
    )

    @server.tool()
    def check_project_requirements(
        jurisdiction: str,
        project: dict[str, Any],
        address: str | None = None,
        property: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        resolve_address: bool = False,
    ) -> dict[str, Any]:
        """Return evidence-linked permit/planning preflight requirements.

        Supported jurisdictions include Gatineau, Ottawa, Toronto and Mississauga.
        Set `resolve_address=true` to enrich the request with first-party municipal
        address/zoning/heritage context before deterministic rule evaluation.
        """
        return run_preflight(
            {
                "jurisdiction": jurisdiction,
                "project": project,
                "address": address,
                "property": property or {},
                "context": context or {},
                "resolve_address": resolve_address,
            }
        )

    return server


def main() -> None:
    railway_port = os.getenv("PORT")
    host = os.getenv(
        "PROJECTPERMIT_MCP_HOST",
        "0.0.0.0" if railway_port else "127.0.0.1",
    )
    port = int(os.getenv("PROJECTPERMIT_MCP_PORT") or railway_port or "8001")
    build_server().run(
        transport="streamable-http",
        host=host,
        port=port,
        json_response=True,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
