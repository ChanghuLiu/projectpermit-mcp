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
            "Municipal construction permit preflight for supported Canadian cities. "
            "Use it when proposed renovation/building work needs an evidence-linked "
            "permit-applicability check before quoting, scheduling or design lock. "
            "Start with projectpermit_info to discover supported jurisdiction ids, "
            "project families and a valid example. Normalize the proposed scope into "
            "structured facts before calling check_project_requirements. Preserve "
            "unknown facts rather than guessing them; the engine can return review or "
            "municipal-confirmation states when the facts do not support a safe yes/no. "
            "Do not use ProjectPermit as municipal authorization, legal advice, engineering "
            "review, plan/code review, permit filing or inspection approval. For repeated "
            "validation, context.client_tag may be a stable non-sensitive integration "
            "label; it is hashed before telemetry. This public endpoint is a "
            "developer-validation preview."
        ),
    )

    @server.tool()
    def projectpermit_info() -> dict[str, Any]:
        """Use first to get supported Canadian cities/families and a valid starter example. This is capability discovery only; it does not decide whether a project needs a permit."""
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
        """Use for a proposed renovation/building scope in a supported city when an agent needs permit applicability before quoting, scheduling or design lock. Supply normalized scope facts; use address resolution where supported when property overlays matter. Returns a deterministic determination (REQUIRED, LIKELY_REQUIRED, LIKELY_NOT_REQUIRED, ADDITIONAL_REVIEW_REQUIRED, MUNICIPAL_CONFIRMATION_REQUIRED or OUT_OF_SCOPE), confidence, stable rule/version metadata and official-source evidence. Do not use for final municipal authorization, legal/engineering advice, plan review, permit filing or inspection approval; preserve missing facts instead of guessing."""
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
