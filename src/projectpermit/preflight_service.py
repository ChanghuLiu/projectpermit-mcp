"""Shared address-aware ProjectPermit preflight service.

HTTP, standard MCP and x402-paid MCP all call this module so municipal address/
overlay resolution and property merging cannot drift between transports.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict

from .address import GatineauAddressAdapter, OttawaAddressAdapter, TorontoAddressAdapter
from .http_fetch import fetch_json
from .jurisdiction_router import evaluate_project
from .mississauga_address import MississaugaAddressAdapter
from .telemetry import emit_preflight_event
from .vancouver_address import VancouverAddressAdapter
from .workflow_advice import build_workflow_guidance

JsonFetcher = Callable[[str], Dict[str, Any]]

SUPPORTED_ADDRESS_JURISDICTIONS = (
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "vancouver_bc",
)


def _resolve_address(jurisdiction: str, address: str, fetcher: JsonFetcher) -> dict[str, Any]:
    if jurisdiction == "ottawa_on":
        return OttawaAddressAdapter(fetcher).resolve(address)
    if jurisdiction == "gatineau_qc":
        return GatineauAddressAdapter(fetcher).geocode(address)
    if jurisdiction == "toronto_on":
        return TorontoAddressAdapter(fetcher).resolve(address)
    if jurisdiction == "mississauga_on":
        return MississaugaAddressAdapter(fetcher).resolve(address)
    if jurisdiction == "vancouver_bc":
        return VancouverAddressAdapter(fetcher).resolve(address)
    raise ValueError(f"address resolver not available for jurisdiction: {jurisdiction}")


def run_preflight(facts: dict[str, Any], fetcher: JsonFetcher = fetch_json) -> dict[str, Any]:
    """Resolve optional municipal address context, then run deterministic rules.

    `resolve_address` is opt-in because municipal GIS calls add latency and can fail
    independently of the rules engine. Resolved non-null municipal property fields
    override caller-supplied values; unknown (`None`) overlays never overwrite a
    caller's explicit value.

    A deterministic workflow-guidance layer is attached after rule evaluation. It
    never changes the permit determination; it only tells calling agents how to
    route the result and which missing facts are worth collecting next.

    A privacy-minimal usage event is emitted after successful evaluation. The event
    never contains the civic address, coordinates or raw property identifiers.
    """
    prepared = deepcopy(facts)
    address_context: dict[str, Any] | None = None

    if bool(prepared.get("resolve_address")):
        address = str(prepared.get("address") or "").strip()
        if not address:
            raise ValueError("address is required when resolve_address=true")

        jurisdiction = str(prepared.get("jurisdiction") or "")
        address_context = _resolve_address(jurisdiction, address, fetcher)
        resolved_property = {
            key: value
            for key, value in (address_context.get("property") or {}).items()
            if value is not None
        }
        prepared["property"] = {
            **(prepared.get("property") or {}),
            **resolved_property,
        }

    result = evaluate_project(prepared)
    if address_context is not None:
        result["address_context"] = address_context
    result["workflow"] = build_workflow_guidance(prepared, result)
    emit_preflight_event(prepared, result)
    return result
