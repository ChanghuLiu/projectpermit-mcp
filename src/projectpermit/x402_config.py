"""Optional x402 v2 transport configuration.

BuildRequirements remains payment-agnostic. This module is imported by the FastAPI
transport and is a no-op unless PROJECTPERMIT_X402_ENABLED=true.
"""
from __future__ import annotations

import os
from typing import Any


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def load_x402_settings() -> dict[str, Any]:
    return {
        "enabled": _truthy(os.getenv("PROJECTPERMIT_X402_ENABLED")),
        "price": os.getenv("PROJECTPERMIT_X402_PRICE_USD", "").strip(),
        "network": os.getenv("PROJECTPERMIT_X402_NETWORK", "").strip(),
        "pay_to": os.getenv("PROJECTPERMIT_X402_PAY_TO", "").strip(),
        "facilitator_url": os.getenv("PROJECTPERMIT_X402_FACILITATOR_URL", "").strip(),
    }


def validate_x402_settings(settings: dict[str, Any]) -> None:
    if not settings["enabled"]:
        return
    missing = [k for k in ("price", "network", "pay_to", "facilitator_url") if not settings.get(k)]
    if missing:
        raise RuntimeError("x402 enabled but missing settings: " + ", ".join(missing))
    if not str(settings["price"]).startswith("$"):
        raise RuntimeError("PROJECTPERMIT_X402_PRICE_USD must use x402 dollar format, e.g. $0.10")
    if ":" not in str(settings["network"]):
        raise RuntimeError("PROJECTPERMIT_X402_NETWORK must be a CAIP-2 identifier, e.g. eip155:84532")


def configure_x402(app: Any) -> None:
    settings = load_x402_settings()
    validate_x402_settings(settings)
    if not settings["enabled"]:
        return

    try:
        from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
        from x402.http.middleware.fastapi import PaymentMiddlewareASGI
        from x402.http.types import RouteConfig
        from x402.mechanisms.evm.exact import ExactEvmServerScheme
        from x402.server import x402ResourceServer
    except ImportError as exc:  # pragma: no cover - optional deployment dependency
        raise RuntimeError(
            'x402 is enabled but the Python x402 FastAPI extra is missing. Install: pip install "x402[fastapi,evm]"'
        ) from exc

    facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=settings["facilitator_url"]))
    resource_server = x402ResourceServer(facilitator)

    network = settings["network"]
    if network.startswith("eip155:"):
        resource_server.register(network, ExactEvmServerScheme())
    else:
        raise RuntimeError(
            "Phase 0 x402 transport currently enables EVM exact scheme only; configure an eip155:* network"
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
            mime_type="application/json",
            description=(
                "Evidence-linked municipal construction permit/planning preflight for "
                "Gatineau and Ottawa. Not municipal authorization or legal advice."
            ),
        )
    }
    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=resource_server)
