from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from .jurisdiction_router import evaluate_project
from .address import OttawaAddressAdapter, GatineauAddressAdapter
from .http_fetch import fetch_json
from .x402_config import configure_x402

app = FastAPI(title="ProjectPermit Phase 0", version="0.1.0")

class PreflightRequest(BaseModel):
    jurisdiction: str
    project: Dict[str, Any]
    address: Optional[str] = None
    property: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    resolve_address: bool = False

@app.get("/health")
def health():
    return {"ok": True, "engine_version": "phase0-0.1.0"}

@app.post("/v1/check-project-requirements")
def check_project_requirements(req: PreflightRequest):
    facts = req.model_dump()
    address_context = None
    if req.resolve_address:
        if not req.address:
            raise HTTPException(status_code=422, detail="address is required when resolve_address=true")
        try:
            if req.jurisdiction == "ottawa_on":
                address_context = OttawaAddressAdapter(fetch_json).resolve(req.address)
            elif req.jurisdiction == "gatineau_qc":
                address_context = GatineauAddressAdapter(fetch_json).geocode(req.address)
            else:
                raise HTTPException(status_code=422, detail="address resolver not available for jurisdiction")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"municipal GIS resolution failed: {exc}") from exc
        resolved_property = {k: v for k, v in address_context.get("property", {}).items() if v is not None}
        facts["property"] = {**req.property, **resolved_property}
    result = evaluate_project(facts)
    if address_context:
        result["address_context"] = address_context
    return result

configure_x402(app)
