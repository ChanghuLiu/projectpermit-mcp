"""x402scan-compatible well-known fallback discovery document."""
from __future__ import annotations

from typing import Any


API_ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
PAID_SINGLE_RESOURCE = f"{API_ORIGIN}/v1/check-project-requirements"
PAID_BATCH_RESOURCE = f"{API_ORIGIN}/v1/check-project-requirements-batch"


def x402_well_known() -> dict[str, Any]:
    """Return the minimal x402scan compatibility document.

    OpenAPI remains ProjectPermit's primary discovery contract. This fallback deliberately
    contains only canonical paid resource URLs; runtime HTTP 402 responses remain authoritative
    for payment requirements, pricing and settlement details.
    """
    return {
        "version": 1,
        "resources": [
            PAID_SINGLE_RESOURCE,
            PAID_BATCH_RESOURCE,
        ],
    }
