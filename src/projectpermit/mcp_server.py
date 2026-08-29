"""Standard MCP transport for ProjectPermit.

Payment is deliberately not embedded here. HTTP, standard MCP and paid MCP all
call the same shared address-aware preflight service.
"""
from __future__ import annotations

import os
from typing import Any

from .batch_service import MAX_BATCH_ITEMS, run_batch_preflight
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
            "project families and valid examples. Normalize the proposed scope into "
            "structured facts before calling check_project_requirements, or use "
            "check_project_requirements_batch for up to 50 normalized projects. Results "
            "include deterministic workflow guidance plus a platform-neutral action_bundle "
            "containing decision/routing, proposed tasks, official evidence, audit metadata, "
            "deterministic decision identity and an idempotency key for duplicate suppression. "
            "For repeated checks of the same work record, pass the prior action_bundle.identity "
            "as context.prior_decision_identity to receive change.classification. Preserve unknown "
            "facts rather than guessing them; the engine can return review or municipal-confirmation "
            "states when the facts do not support a safe yes/no. Do not use ProjectPermit as "
            "municipal authorization, legal advice, engineering review, plan/code review, "
            "permit filing or inspection approval."
        ),
    )

    @server.tool()
    def projectpermit_info() -> dict[str, Any]:
        """Use first to get supported Canadian cities/families, action-bundle identity semantics and starter examples. Capability discovery only; no permit determination is performed."""
        return {
            "service": "ProjectPermit",
            "tool": "check_project_requirements",
            "bulk_tool": "check_project_requirements_batch",
            "bulk_max_items": MAX_BATCH_ITEMS,
            "jurisdictions": list(SUPPORTED_JURISDICTIONS),
            "address_resolution_jurisdictions": list(SUPPORTED_ADDRESS_JURISDICTIONS),
            "project_families": list(PROJECT_FAMILIES),
            "workflow_guidance": {
                "field": "workflow",
                "routes": [
                    "ADD_PERMIT_TASK",
                    "CONTINUE_WITH_EVIDENCE",
                    "COLLECT_MISSING_FACTS",
                    "ROUTE_SPECIAL_REVIEW",
                    "MUNICIPAL_CONFIRMATION",
                    "MANUAL_SCOPE_REVIEW",
                ],
                "description": (
                    "Machine-readable contractor/field-service routing metadata derived "
                    "from the permit result without changing the legal determination."
                ),
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
                ],
                "description": (
                    "Platform-neutral evidence/action package for contractor and field-service "
                    "integrations. Jobber and ServiceM8 read-only proposal mapping is supported."
                ),
            },
            "decision_identity": {
                "field": "action_bundle.identity",
                "includes": [
                    "bundle_id",
                    "input_fingerprint",
                    "decision_fingerprint",
                    "routing_fingerprint",
                    "ruleset_fingerprint",
                    "evidence_fingerprint",
                    "scope_fingerprint",
                    "idempotency_key",
                ],
                "repeat_check_input": "context.prior_decision_identity",
                "change_field": "action_bundle.change",
                "change_classifications": [
                    "FIRST_OBSERVATION",
                    "UNCHANGED",
                    "DECISION_CHANGED",
                    "ROUTE_CHANGED",
                    "INPUT_CHANGED",
                    "RULESET_CHANGED",
                    "EVIDENCE_REFRESHED",
                    "IDENTITY_VERSION_CHANGED",
                ],
                "purpose": (
                    "Suppress duplicate downstream tasks and distinguish operational changes "
                    "from ruleset/evidence refreshes without returning raw platform object ids."
                ),
            },
            "example": {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "resolve_address": False,
            },
            "bulk_example": {
                "items": [
                    {
                        "client_ref": "lead-001",
                        "jurisdiction": "ottawa_on",
                        "project": {"family": "window_door", "action": "replace_same_size"},
                        "property": {"heritage": False},
                    },
                    {
                        "client_ref": "lead-002",
                        "jurisdiction": "toronto_on",
                        "project": {
                            "family": "window_door",
                            "action": "enlarge_existing_opening",
                        },
                    },
                ]
            },
            "validation_hint": (
                "For repeat pilot usage, context.client_tag may be a stable non-sensitive "
                "integration label. For work-record duplicate suppression, integrations may "
                "supply context.source_platform/source_object_type/source_object_id; only a "
                "one-way scope fingerprint is returned in decision identity."
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
        """Use for a proposed renovation/building scope when an agent needs permit applicability before quoting/scheduling. Returns determination, evidence, workflow/action bundle, deterministic identity, idempotency key and change classification when context.prior_decision_identity is supplied."""
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

    @server.tool()
    def check_project_requirements_batch(items: list[dict[str, Any]]) -> dict[str, Any]:
        """Evaluate 1-50 normalized projects in one call. Each item may include prior_decision_identity in context; results include per-item action-bundle identity/change metadata and batch-level audit."""
        return run_batch_preflight(
            items,
            allow_address=True,
            transport="standard_mcp_batch",
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
