"""Machine-readable x402 discovery metadata for ProjectPermit HTTP resources.

FastAPI already exposes `/openapi.json`. This module decorates that canonical
contract with the payment metadata expected by current x402 discovery/indexing
systems while keeping the runtime 402 challenge as the final payment truth.
"""
from __future__ import annotations

import os
from copy import deepcopy
from typing import Any, Mapping

from fastapi.openapi.utils import get_openapi


SINGLE_PATH = "/v1/check-project-requirements"
BATCH_PATH = "/v1/check-project-requirements-batch"
DEFAULT_SINGLE_PRICE = "$0.05"
DEFAULT_BATCH_PRICE = "$2.00"
DEFAULT_NETWORK = "eip155:8453"


def _amount(value: str | None, fallback: str) -> str:
    rendered = str(value or fallback).strip()
    if rendered.startswith("$"):
        rendered = rendered[1:]
    return rendered or fallback.lstrip("$")


def discovery_settings() -> dict[str, str]:
    """Return public pricing/network metadata, using commercial defaults locally."""
    single = os.getenv("PROJECTPERMIT_X402_PRICE_USD", DEFAULT_SINGLE_PRICE)
    batch = os.getenv("PROJECTPERMIT_X402_BATCH_PRICE_USD", DEFAULT_BATCH_PRICE)
    network = os.getenv("PROJECTPERMIT_X402_NETWORK", DEFAULT_NETWORK).strip() or DEFAULT_NETWORK
    return {
        "single_amount": _amount(single, DEFAULT_SINGLE_PRICE),
        "batch_amount": _amount(batch, DEFAULT_BATCH_PRICE),
        "network": network,
    }


def _payment_info(amount: str) -> dict[str, Any]:
    # x402scan's current canonical discovery contract requires `price` plus a
    # protocol object. Runtime chain/asset details remain authoritative in the 402.
    return {
        "price": {
            "mode": "fixed",
            "currency": "USD",
            "amount": amount,
        },
        "protocols": [{"x402": {}}],
    }


def decorate_openapi_schema(
    schema: Mapping[str, Any],
    *,
    single_amount: str,
    batch_amount: str,
    network: str,
) -> dict[str, Any]:
    """Return a copy of an OpenAPI schema with ProjectPermit x402 discovery fields."""
    output = deepcopy(dict(schema))
    info = output.setdefault("info", {})
    info["x-guidance"] = (
        "Use free preview routes to test normalized permit facts without payment. "
        "Use x402-paid routes for commercial preflight calls. Paid responses return "
        "deterministic permit requirements, official-source evidence, workflow routing, "
        "action-bundle identity/change metadata and safe-writeback gating. Runtime 402 "
        "payment requirements are authoritative."
    )
    info["x-projectpermit"] = {
        "commercialNetwork": network,
        "paymentProtocol": "x402-v2",
        "currency": "USDC",
        "paidMcp": "https://projectpermit-x402-mcp-production.up.railway.app/mcp",
        "freeMcp": "https://projectpermit-mcp-production.up.railway.app/mcp",
    }

    paid = {
        SINGLE_PATH: single_amount,
        BATCH_PATH: batch_amount,
    }
    paths = output.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("OpenAPI schema.paths is required")

    for path, amount in paid.items():
        path_item = paths.get(path)
        if not isinstance(path_item, dict):
            raise ValueError(f"OpenAPI paid path missing: {path}")
        operation = path_item.get("post")
        if not isinstance(operation, dict):
            raise ValueError(f"OpenAPI POST operation missing: {path}")
        operation["x-payment-info"] = _payment_info(amount)
        operation["x-projectpermit-payment"] = {
            "network": network,
            "scheme": "exact",
            "asset": "USDC",
            "runtimeChallengeAuthoritative": True,
        }
        responses = operation.setdefault("responses", {})
        responses.setdefault(
            "402",
            {
                "description": (
                    "Payment Required. Inspect the runtime x402 v2 challenge for the "
                    "authoritative network, asset, amount and payment requirements."
                )
            },
        )
    return output


def install_openapi_discovery(app: Any) -> None:
    """Install a lazy custom OpenAPI generator on a fully-defined FastAPI app."""
    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        base = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        settings = discovery_settings()
        app.openapi_schema = decorate_openapi_schema(
            base,
            single_amount=settings["single_amount"],
            batch_amount=settings["batch_amount"],
            network=settings["network"],
        )
        return app.openapi_schema

    app.openapi = custom_openapi
