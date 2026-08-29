from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field

from .batch_service import MAX_BATCH_ITEMS, run_batch_preflight
from .capabilities import PROJECT_FAMILIES
from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .openapi_discovery import install_openapi_discovery
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight
from .public_discovery import landing_html, llms_text
from .public_x402_manifest import x402_service_manifest
from .x402_config import configure_x402

app = FastAPI(title="ProjectPermit", version="0.6.0")


class PreflightRequest(BaseModel):
    jurisdiction: str
    project: Dict[str, Any]
    address: Optional[str] = None
    property: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    resolve_address: bool = False


class PreviewRequest(BaseModel):
    """Free validation preview deliberately excludes raw civic address resolution."""

    model_config = ConfigDict(extra="forbid")
    jurisdiction: str
    project: Dict[str, Any]
    property: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)


class BatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[Any]


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def public_landing():
    """Human-readable entry point for direct visits and search crawlers."""
    return landing_html()


@app.get("/llms.txt", response_class=PlainTextResponse, include_in_schema=False)
def public_llms_text():
    """Compact agent-readable capability, pricing and discovery guide."""
    return llms_text()


@app.get("/.well-known/x402-service.json", include_in_schema=False)
def public_x402_service_manifest():
    """Machine-readable seller manifest for zero-cost x402 directory discovery."""
    return x402_service_manifest()


@app.get("/health")
def health():
    return {"ok": True, "engine_version": "phase1c-0.6.0"}


@app.get("/v1/capabilities")
def capabilities():
    address_resolvers = set(SUPPORTED_ADDRESS_JURISDICTIONS)
    return {
        "service": "ProjectPermit",
        "engine_version": "phase1c-0.6.0",
        "jurisdictions": [
            {
                "id": jurisdiction,
                "rule_preflight": True,
                "address_resolution": jurisdiction in address_resolvers,
            }
            for jurisdiction in SUPPORTED_JURISDICTIONS
        ],
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
            "purpose": "Route permit-preflight results directly inside contractor/field-service agent workflows.",
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
            "identity_capabilities": [
                "decision_fingerprint",
                "work_record_scoped_idempotency",
                "change_classification",
            ],
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
                "Provide one PII-minimal evidence/action package with deterministic "
                "duplicate suppression, change detection and safe-writeback gating for "
                "contractor, property and field-service integrations."
            ),
        },
        "mutation_gate": {
            "field": "action_bundle.mutation_gate",
            "states": [
                "READY_FOR_EXPLICIT_WRITE",
                "NOOP_UNCHANGED",
                "BLOCKED",
            ],
            "ready_requires": [
                "work_record_scope",
                "automation_safe",
                "CURRENT_evidence",
                "no_required_inputs",
            ],
            "write_contract": "explicit_authorized_atomic_upsert_by_idempotency_key",
            "unconditional_create_allowed": False,
            "external_mutation_performed_by_projectpermit": False,
        },
        "integration_proposals": {
            "jobber": "read_only_proposal_supported",
            "servicem8": "read_only_proposal_supported",
        },
        "safe_writeback_proposals": {
            "jobber": "mutation_gate_supported",
            "servicem8": "mutation_gate_supported",
            "execution": "not_enabled_in_projectpermit",
        },
        "free_preview_resource": "/v1/preview-project-requirements",
        "free_batch_preview_resource": "/v1/preview-project-requirements-batch",
        "paid_resource": "/v1/check-project-requirements",
        "paid_batch_resource": "/v1/check-project-requirements-batch",
        "bulk_max_items": MAX_BATCH_ITEMS,
        "free_preview_address_resolution": False,
        "disclaimer": "Preflight information only; not municipal authorization or legal advice.",
    }


@app.post("/v1/preview-project-requirements")
def preview_project_requirements(req: PreviewRequest):
    try:
        facts = req.model_dump()
        facts["address"] = None
        facts["resolve_address"] = False
        facts["context"] = {**facts.get("context", {}), "_transport": "http_preview"}
        return run_preflight(facts)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"preview preflight failed: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="preview evaluation failed") from exc


@app.post("/v1/preview-project-requirements-batch")
def preview_project_requirements_batch(req: BatchRequest):
    try:
        return run_batch_preflight(req.items, allow_address=False, transport="http_preview_batch")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"batch preview failed: {exc}") from exc


@app.post("/v1/check-project-requirements")
def check_project_requirements(req: PreflightRequest):
    try:
        facts = req.model_dump()
        facts["context"] = {**facts.get("context", {}), "_transport": "http_api"}
        return run_preflight(facts)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"municipal address resolution failed: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"municipal GIS resolution failed: {exc}") from exc


@app.post("/v1/check-project-requirements-batch")
def check_project_requirements_batch(req: BatchRequest):
    try:
        return run_batch_preflight(req.items, allow_address=True, transport="http_api_batch")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"batch preflight failed: {exc}") from exc


install_openapi_discovery(app)
configure_x402(app)
