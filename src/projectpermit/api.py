from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .batch_service import MAX_BATCH_ITEMS, run_batch_preflight
from .capabilities import PROJECT_FAMILIES
from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight
from .x402_config import configure_x402

app = FastAPI(title="ProjectPermit", version="0.5.0")


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


class BatchPreviewRequest(BaseModel):
    """Free bulk preview; item validation is intentionally isolated per project."""

    model_config = ConfigDict(extra="forbid")
    items: list[Any]


@app.get("/health")
def health():
    return {"ok": True, "engine_version": "phase1c-0.5.0"}


@app.get("/v1/capabilities")
def capabilities():
    """Free machine-readable discovery; no permit determination is performed."""
    address_resolvers = set(SUPPORTED_ADDRESS_JURISDICTIONS)
    return {
        "service": "ProjectPermit",
        "engine_version": "phase1c-0.5.0",
        "jurisdictions": [
            {
                "id": jurisdiction,
                "rule_preflight": True,
                "address_resolution": jurisdiction in address_resolvers,
            }
            for jurisdiction in SUPPORTED_JURISDICTIONS
        ],
        "project_families": list(PROJECT_FAMILIES),
        "free_preview_resource": "/v1/preview-project-requirements",
        "free_batch_preview_resource": "/v1/preview-project-requirements-batch",
        "bulk_max_items": MAX_BATCH_ITEMS,
        "free_preview_address_resolution": False,
        "paid_resource": "/v1/check-project-requirements",
        "disclaimer": "Preflight information only; not municipal authorization or legal advice.",
    }


@app.post("/v1/preview-project-requirements")
def preview_project_requirements(req: PreviewRequest):
    """Free structured-facts preview; never performs civic-address/GIS resolution."""
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
def preview_project_requirements_batch(req: BatchPreviewRequest):
    """Free 1-50 item bulk preview with per-item error isolation and audit summary."""
    try:
        return run_batch_preflight(
            req.items,
            allow_address=False,
            transport="http_preview_batch",
        )
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


configure_x402(app)
