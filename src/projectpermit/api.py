from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .jurisdiction_router import SUPPORTED_JURISDICTIONS
from .preflight_service import SUPPORTED_ADDRESS_JURISDICTIONS, run_preflight
from .x402_config import configure_x402

app = FastAPI(title="ProjectPermit", version="0.4.0")


class PreflightRequest(BaseModel):
    jurisdiction: str
    project: Dict[str, Any]
    address: Optional[str] = None
    property: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    resolve_address: bool = False


@app.get("/health")
def health():
    return {"ok": True, "engine_version": "phase1c-0.4.0"}


@app.get("/v1/capabilities")
def capabilities():
    """Free machine-readable discovery; no permit determination is performed."""
    address_resolvers = set(SUPPORTED_ADDRESS_JURISDICTIONS)
    return {
        "service": "ProjectPermit",
        "engine_version": "phase1c-0.4.0",
        "jurisdictions": [
            {
                "id": jurisdiction,
                "rule_preflight": True,
                "address_resolution": jurisdiction in address_resolvers,
            }
            for jurisdiction in SUPPORTED_JURISDICTIONS
        ],
        "project_families": [
            "window_door",
            "interior_renovation",
            "basement",
            "dwelling_change",
            "deck_porch",
            "accessory_structure",
            "addition",
            "kitchen_bath_plumbing",
        ],
        "paid_resource": "/v1/check-project-requirements",
        "disclaimer": "Preflight information only; not municipal authorization or legal advice.",
    }


@app.post("/v1/check-project-requirements")
def check_project_requirements(req: PreflightRequest):
    try:
        return run_preflight(req.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"municipal address resolution failed: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"municipal GIS resolution failed: {exc}") from exc


configure_x402(app)
