"""Standard MCP transport for ProjectPermit.

Payment is deliberately not embedded here. The same deterministic jurisdiction
router is exposed by FastAPI and the paid MCP transport.
"""
from __future__ import annotations

import os
from typing import Any

from .jurisdiction_router import SUPPORTED_JURISDICTIONS, evaluate_project


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
    ) -> dict[str, Any]:
        """Return evidence-linked permit/planning preflight requirements.

        Supported jurisdictions include Gatineau, Ottawa, Toronto and Mississauga.
        The tool is deterministic and does not perform natural-language scope extraction.
        """
        return evaluate_project(
            {
                "jurisdiction": jurisdiction,
                "project": project,
                "address": address,
                "property": property or {},
                "context": context or {},
            }
        )

    return server


def main() -> None:
    # Railway injects PORT. Local development keeps the safer loopback default.
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
