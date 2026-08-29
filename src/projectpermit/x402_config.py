"""Optional x402 v2 transport configuration.

BuildRequirements remains payment-agnostic. This module is imported by the FastAPI
transport and is a no-op unless PROJECTPERMIT_X402_ENABLED=true.

The single-item HTTP route declares Bazaar discovery metadata. The paid bulk route
uses the same x402 network/facilitator/pay-to settings with an independently
configurable batch price, but intentionally does not publish Bazaar metadata yet.
"""
from __future__ import annotations

import os
from typing import Any

from .jurisdiction_router import SUPPORTED_JURISDICTIONS


HTTP_PUBLIC_RESOURCE_URL = (
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements"
)
HTTP_BATCH_PUBLIC_RESOURCE_URL = (
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements-batch"
)

HTTP_DISCOVERY_INPUT: dict[str, Any] = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
    "resolve_address": False,
}

HTTP_DISCOVERY_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "jurisdiction": {
            "type": "string",
            "enum": list(SUPPORTED_JURISDICTIONS),
            "description": "Supported municipality identifier.",
        },
        "project": {
            "type": "object",
            "description": "Normalized project facts such as family, action, structural_change and estimated_cost_cad.",
        },
        "address": {
            "type": ["string", "null"],
            "description": "Optional civic address for address-aware preflight where a resolver is available.",
        },
        "property": {
            "type": "object",
            "description": "Known property overlays/facts such as heritage or PIIA status.",
        },
        "context": {
            "type": "object",
            "description": "Optional rule-version or workflow context.",
        },
        "resolve_address": {
            "type": "boolean",
            "description": "Resolve the civic address against a supported municipal geocoder/GIS adapter. Not every rules jurisdiction has an address adapter yet.",
        },
    },
    "required": ["jurisdiction", "project"],
}

HTTP_DISCOVERY_OUTPUT_EXAMPLE: dict[str, Any] = {
    "jurisdiction": {"country": "CA", "province": "ON", "municipality": "Ottawa"},
    "determination": "LIKELY_NOT_REQUIRED",
    "requirements": [
        {
            "type": "building_permit",
            "status": "LIKELY_NOT_REQUIRED",
            "rule_id": "OTT-WIN-002",
        }
    ],
    "confidence": "HIGH",
    "workflow": {
        "mode": "NO_PERMIT_SIGNAL",
        "recommended_route": "CONTINUE_WITH_EVIDENCE",
        "quote_handling": "NO_PERMIT_ALLOWANCE_SIGNAL",
        "automation_safe": True,
        "summary": "No permit requirement was identified by the supplied facts; retain the official evidence with the job record.",
        "follow_up_questions": [],
    },
    "engine_version": "phase0-0.1.0",
}

HTTP_DISCOVERY_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "jurisdiction": {"type": "object"},
        "determination": {
            "type": "string",
            "enum": [
                "REQUIRED",
                "LIKELY_REQUIRED",
                "LIKELY_NOT_REQUIRED",
                "ADDITIONAL_REVIEW_REQUIRED",
                "MUNICIPAL_CONFIRMATION_REQUIRED",
                "OUT_OF_SCOPE",
            ],
        },
        "requirements": {"type": "array"},
        "confidence": {"type": "string"},
        "workflow": {
            "type": "object",
            "properties": {
                "mode": {"type": "string"},
                "recommended_route": {"type": "string"},
                "quote_handling": {"type": "string"},
                "automation_safe": {"type": "boolean"},
                "summary": {"type": "string"},
                "follow_up_questions": {"type": "array"},
            },
            "required": [
                "mode",
                "recommended_route",
                "quote_handling",
                "automation_safe",
                "summary",
                "follow_up_questions",
            ],
        },
        "disclaimer": {"type": "string"},
        "engine_version": {"type": "string"},
        "address_context": {"type": "object"},
    },
    "required": [
        "jurisdiction",
        "determination",
        "requirements",
        "confidence",
        "workflow",
        "engine_version",
    ],
}


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def load_x402_settings() -> dict[str, Any]:
    price = os.getenv("PROJECTPERMIT_X402_PRICE_USD", "").strip()
    return {
        "enabled": _truthy(os.getenv("PROJECTPERMIT_X402_ENABLED")),
        "price": price,
        "batch_price": os.getenv("PROJECTPERMIT_X402_BATCH_PRICE_USD", price).strip(),
        "network": os.getenv("PROJECTPERMIT_X402_NETWORK", "").strip(),
        "pay_to": os.getenv("PROJECTPERMIT_X402_PAY_TO", "").strip(),
        "facilitator_url": os.getenv("PROJECTPERMIT_X402_FACILITATOR_URL", "").strip(),
    }


def validate_x402_settings(settings: dict[str, Any]) -> None:
    if not settings["enabled"]:
        return
    missing = [
        k
        for k in ("price", "batch_price", "network", "pay_to", "facilitator_url")
        if not settings.get(k)
    ]
    if missing:
        raise RuntimeError("x402 enabled but missing settings: " + ", ".join(missing))
    if not str(settings["price"]).startswith("$"):
        raise RuntimeError("PROJECTPERMIT_X402_PRICE_USD must use x402 dollar format, e.g. $0.10")
    if not str(settings["batch_price"]).startswith("$"):
        raise RuntimeError(
            "PROJECTPERMIT_X402_BATCH_PRICE_USD must use x402 dollar format, e.g. $0.50"
        )
    if ":" not in str(settings["network"]):
        raise RuntimeError("PROJECTPERMIT_X402_NETWORK must be a CAIP-2 identifier, e.g. eip155:84532")


def configure_x402(app: Any) -> None:
    settings = load_x402_settings()
    validate_x402_settings(settings)
    if not settings["enabled"]:
        return

    try:
        from x402.extensions.bazaar import (
            OutputConfig,
            bazaar_resource_server_extension,
            declare_discovery_extension,
        )
        from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
        from x402.http.middleware.fastapi import PaymentMiddlewareASGI
        from x402.http.types import RouteConfig
        from x402.mechanisms.evm.exact import ExactEvmServerScheme
        from x402.server import x402ResourceServer
    except ImportError as exc:  # pragma: no cover - optional deployment dependency
        raise RuntimeError(
            'x402 is enabled but the Python x402 FastAPI/EVM extension support is missing. Install: pip install "x402[fastapi,evm]"'
        ) from exc

    facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=settings["facilitator_url"]))
    resource_server = x402ResourceServer(facilitator)

    network = settings["network"]
    if network.startswith("eip155:"):
        resource_server.register(network, ExactEvmServerScheme())
    else:
        raise RuntimeError(
            "ProjectPermit x402 transport currently enables EVM exact scheme only; configure an eip155:* network"
        )

    resource_server.register_extension(bazaar_resource_server_extension)

    discovery_extensions = declare_discovery_extension(
        input=HTTP_DISCOVERY_INPUT,
        input_schema=HTTP_DISCOVERY_INPUT_SCHEMA,
        body_type="json",
        output=OutputConfig(
            example=HTTP_DISCOVERY_OUTPUT_EXAMPLE,
            schema=HTTP_DISCOVERY_OUTPUT_SCHEMA,
        ),
    )

    common_description = (
        "Evidence-linked municipal construction permit/planning preflight for Gatineau, "
        "Ottawa, Toronto, Mississauga, Laval, Longueuil and Vancouver. Returns "
        "deterministic rule results, official-source evidence, and agent-ready workflow "
        "routing with targeted missing-fact questions. Not municipal authorization or "
        "legal advice."
    )

    routes = {
        "POST /v1/check-project-requirements": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=settings["pay_to"],
                    price=settings["price"],
                    network=network,
                )
            ],
            resource=HTTP_PUBLIC_RESOURCE_URL,
            mime_type="application/json",
            description=common_description,
            extensions={**discovery_extensions},
        ),
        "POST /v1/check-project-requirements-batch": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    pay_to=settings["pay_to"],
                    price=settings["batch_price"],
                    network=network,
                )
            ],
            resource=HTTP_BATCH_PUBLIC_RESOURCE_URL,
            mime_type="application/json",
            description=(
                "Paid bulk ProjectPermit preflight for 1-50 normalized projects with "
                "per-item error isolation, workflow routing, and batch audit metadata. "
                + common_description
            ),
        ),
    }
    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=resource_server)
