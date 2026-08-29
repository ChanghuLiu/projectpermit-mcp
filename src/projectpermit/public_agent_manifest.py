"""Provider-authoritative agent.json manifest for Open 402 style discovery."""
from __future__ import annotations

from typing import Any

from .openapi_discovery import discovery_settings
from .public_x402_manifest import API_ORIGIN, x402_service_manifest


BASE_USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


def agent_manifest() -> dict[str, Any]:
    """Return a Tier-2 agent.json manifest derived from current x402 settings."""
    seller = x402_service_manifest()
    payment = seller["payment"]
    pricing = discovery_settings()

    if payment["chain"] != "base" or payment["network"] != "eip155:8453":
        raise RuntimeError("agent.json is pinned to ProjectPermit's Base mainnet commercial rail")

    x402_network = {
        "network": "base",
        "asset": "USDC",
        "contract": BASE_USDC_CONTRACT,
        "facilitator": payment["facilitator"],
    }

    return {
        "version": "1.3",
        "origin": API_ORIGIN.removeprefix("https://"),
        "display_name": "ProjectPermit",
        "description": seller["description"],
        "payout_address": payment["address"],
        "payments": {
            "x402": {
                "networks": [x402_network],
                "recipient": payment["address"],
            }
        },
        "intents": [
            {
                "name": "check_building_permit_requirements",
                "description": (
                    "Check proposed construction or renovation scope against deterministic "
                    "municipal building-permit rules and return official-source evidence, "
                    "workflow routing, freshness and decision identity metadata."
                ),
                "endpoint": "/v1/check-project-requirements",
                "method": "POST",
                "parameters": {
                    "jurisdiction": {
                        "type": "string",
                        "required": True,
                        "description": "Supported ProjectPermit municipality identifier.",
                    },
                    "project": {
                        "type": "object",
                        "required": True,
                        "description": "Normalized proposed project facts.",
                    },
                    "address": {
                        "type": "string",
                        "required": False,
                        "description": "Optional civic address when address-aware resolution is desired.",
                    },
                    "property": {
                        "type": "object",
                        "required": False,
                        "description": "Known property overlays such as heritage status.",
                    },
                    "resolve_address": {
                        "type": "boolean",
                        "required": False,
                        "description": "Resolve supported civic addresses through municipal GIS/geocoders.",
                    },
                },
                "returns": {
                    "type": "object",
                    "description": (
                        "Permit determination with requirements, official evidence, workflow guidance, "
                        "action bundle, decision fingerprints and safe-writeback gate."
                    ),
                },
                "price": {
                    "amount": float(pricing["single_amount"]),
                    "currency": "USDC",
                    "model": "per_call",
                    "network": ["base"],
                },
            },
            {
                "name": "check_building_permit_requirements_batch",
                "description": (
                    "Run 1-50 normalized permit-preflight checks in one paid request with "
                    "per-item error isolation and batch audit metadata."
                ),
                "endpoint": "/v1/check-project-requirements-batch",
                "method": "POST",
                "parameters": {
                    "items": {
                        "type": "array",
                        "required": True,
                        "description": "One to fifty ProjectPermit preflight request objects.",
                    }
                },
                "returns": {
                    "type": "object",
                    "description": "Batch preflight results with per-item success/error isolation.",
                },
                "price": {
                    "amount": float(pricing["batch_amount"]),
                    "currency": "USDC",
                    "model": "per_call",
                    "network": ["base"],
                },
            },
        ],
        "extensions": {
            "projectpermit": {
                "openapi": seller["openapi"],
                "free_preview": seller["free_preview"],
                "x402_manifest": f"{API_ORIGIN}/.well-known/x402-service.json",
                "jurisdictions": 7,
                "disclaimer": "Preflight information only; not municipal authorization or legal advice.",
            }
        },
    }
