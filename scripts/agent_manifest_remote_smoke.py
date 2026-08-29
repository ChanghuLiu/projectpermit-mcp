"""Validate the live provider-authoritative agent.json without making a paid request."""
from __future__ import annotations

import json
import urllib.request


ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
URL = f"{ORIGIN}/.well-known/agent.json"
EXPECTED_PAYOUT = "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A"
EXPECTED_USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
EXPECTED_FACILITATOR = "https://facilitator.payai.network"


def main() -> None:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "projectpermit-agent-manifest-smoke/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"agent manifest returned HTTP {response.status}")
        content_type = response.headers.get_content_type()
        if content_type != "application/json":
            raise RuntimeError(f"unexpected content-type: {content_type}")
        payload = json.load(response)

    if payload.get("version") != "1.3":
        raise RuntimeError(f"unexpected agent.json version: {payload.get('version')!r}")
    if payload.get("origin") != "projectpermit-api-v2-production.up.railway.app":
        raise RuntimeError(f"unexpected origin: {payload.get('origin')!r}")
    if payload.get("payout_address") != EXPECTED_PAYOUT:
        raise RuntimeError("unexpected payout address")

    x402 = (payload.get("payments") or {}).get("x402") or {}
    if x402.get("recipient") != EXPECTED_PAYOUT:
        raise RuntimeError("x402 recipient drifted from the public payout address")
    networks = x402.get("networks") or []
    if len(networks) != 1:
        raise RuntimeError(f"expected one commercial x402 network, got {len(networks)}")
    network = networks[0]
    expected_network = {
        "network": "base",
        "asset": "USDC",
        "contract": EXPECTED_USDC,
        "facilitator": EXPECTED_FACILITATOR,
    }
    if network != expected_network:
        raise RuntimeError(f"unexpected Base/USDC payment metadata: {network!r}")

    intents = {item.get("name"): item for item in payload.get("intents") or []}
    single = intents.get("check_building_permit_requirements")
    batch = intents.get("check_building_permit_requirements_batch")
    if not single or not batch:
        raise RuntimeError("agent.json is missing the single or batch paid intent")

    if single.get("method") != "POST" or single.get("endpoint") != "/v1/check-project-requirements":
        raise RuntimeError(f"unexpected single intent routing: {single!r}")
    if (single.get("price") or {}).get("amount") != 0.05:
        raise RuntimeError(f"unexpected single intent price: {single.get('price')!r}")
    if (single.get("price") or {}).get("currency") != "USDC":
        raise RuntimeError(f"unexpected single currency: {single.get('price')!r}")

    if batch.get("method") != "POST" or batch.get("endpoint") != "/v1/check-project-requirements-batch":
        raise RuntimeError(f"unexpected batch intent routing: {batch!r}")
    if (batch.get("price") or {}).get("amount") != 2.0:
        raise RuntimeError(f"unexpected batch intent price: {batch.get('price')!r}")
    if (batch.get("price") or {}).get("currency") != "USDC":
        raise RuntimeError(f"unexpected batch currency: {batch.get('price')!r}")

    extensions = (payload.get("extensions") or {}).get("projectpermit") or {}
    if extensions.get("openapi") != f"{ORIGIN}/openapi.json":
        raise RuntimeError("agent.json OpenAPI discovery link drifted")
    if extensions.get("x402_manifest") != f"{ORIGIN}/.well-known/x402-service.json":
        raise RuntimeError("agent.json x402 manifest link drifted")

    print("agent_manifest_remote_smoke=PASS")
    print("agent_manifest_http=200")
    print("agent_manifest_version=1.3")
    print("agent_manifest_network=base")
    print("agent_manifest_asset=USDC")
    print("agent_manifest_single_method=POST")
    print("agent_manifest_single_price=0.05")
    print("agent_manifest_batch_method=POST")
    print("agent_manifest_batch_price=2.0")


if __name__ == "__main__":
    main()
