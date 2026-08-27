"""Standard MCP transport for ProjectPermit.

Payment is deliberately not embedded here. HTTP, standard MCP and paid MCP all
call the same shared address-aware preflight service.
"""
from __future__ import annotations

import os
from typing import Any

from .capabilities import PROJECT_FAMILIES
from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight


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
            "Municipal construction permit preflight. Start with projectpermit_info "
            "to discover supported jurisdictions, project families and an example. "
            "Normalize the proposed construction scope into structured facts before "
            "calling check_project_requirements. Results are evidence-linked preflight "
            "information, not municipal authorization. For repeated validation, "
            "context.client_tag may be a stable non-sensitive integration label; it is "
            "hashed before telemetry. This public endpoint is a developer-validation preview."
        ),
    )

    @server.tool()
    def projectpermit_info() -> dict[str, Any]:
        """Return free ProjectPermit capabilities and a valid starter example."""
        return {
            "service": "ProjectPermit",
            "tool": "check_project_requirements",
            "jurisdictions": list(SUPPORTED_JURISDICTIONS),
            "address_resolution_jurisdictions": list(SUPPORTED_ADDRESS_JURISDICTIONS),
            "project_families": list(PROJECT_FAMILIES),
            "example": {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "resolve_address": False,
            },
            "validation_hint": (
                "For repeat pilot usage, context.client_tag may be a stable "
                "non-sensitive integration label; it is hashed before telemetry."
            ),
            "disclaimer": (
                "Preflight information only; not municipal authorization or legal advice."
            ),
        }

    @server.tool()
    def check_project_requirements(
        jurisdiction: str,
        project: dict[str, Any],
        address: str | None = None,
        property: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        resolve_address: bool = False,
    ) -> dict[str, Any]:
        """Return evidence-linked permit/planning preflight requirements."""
        return run_preflight(
            {
                "jurisdiction": jurisdiction,
                "project": project,
                "address": address,
                "property": property or {},
                "context": {**(context or {}), "_transport": "standard_mcp"},
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
