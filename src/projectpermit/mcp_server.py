"""Standard MCP transport for ProjectPermit.

Payment is deliberately not embedded here in Phase 0. The same engine is exposed by
FastAPI so x402 payment enforcement can wrap the paid HTTP resource independently.
"""
from __future__ import annotations

import os
from typing import Any

from .engine import evaluate_project


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

        Supported Phase 0 jurisdictions are `gatineau_qc` and `ottawa_on`.
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
    host = os.getenv("PROJECTPERMIT_MCP_HOST", "127.0.0.1")
    port = int(os.getenv("PROJECTPERMIT_MCP_PORT", "8001"))
    build_server().run(
        transport="streamable-http",
        host=host,
        port=port,
        json_response=True,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
