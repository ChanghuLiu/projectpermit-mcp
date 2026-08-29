"""Public x402 seller manifest for zero-cost agent directory discovery."""
from __future__ import annotations

import os
from typing import Any

from .openapi_discovery import discovery_settings


API_ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
PAID_ENDPOINT = f"{API_ORIGIN}/v1/check-project-requirements"


def x402_service_manifest() -> dict[str, Any]:
    """Return the public single-resource seller manifest used by x402 directories."""
    network = os.getenv("PROJECTPERMIT_X402_NETWORK", "eip155:8453").strip() or "eip155:8453"
    if network != "eip155:8453":
        raise RuntimeError("Public x402 seller manifest is pinned to Base mainnet (eip155:8453)")

    pay_to = os.getenv("PROJECTPERMIT_X402_PAY_TO", "").strip()
    if not pay_to:
        raise RuntimeError("PROJECTPERMIT_X402_PAY_TO is required for the public x402 seller manifest")

    facilitator = os.getenv(
        "PROJECTPERMIT_X402_FACILITATOR_URL",
        "https://facilitator.payai.network",
    ).strip() or "https://facilitator.payai.network"
    price = discovery_settings()["single_amount"]

    return {
        "x402": "1.0",
        "name": "projectpermit-building-permit-preflight",
        "description": (
            "Building permit requirements API for contractors and AI agents across "
            "7 Canadian municipalities with deterministic rules and official-source evidence."
        ),
        "capabilities": [
            "building-permit-requirements",
            "renovation-permit-check",
            "construction-permit-preflight",
            "contractor-workflow",
            "municipal-rules",
            "official-source-evidence",
        ],
        "pricing": {
            "currency": "USDC",
            "base": price,
            "unit": "request",
        },
        "payment": {
            "address": pay_to,
            "chain": "base",
            "network": network,
            "facilitator": facilitator,
            "scheme": "exact",
        },
        "endpoint": PAID_ENDPOINT,
        "openapi": f"{API_ORIGIN}/openapi.json",
        "free_preview": f"{API_ORIGIN}/v1/preview-project-requirements",
    }
