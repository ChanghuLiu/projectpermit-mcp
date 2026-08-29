"""Register ProjectPermit with zero-cost x402 directories after validating production discovery.

This script never sends payment credentials and treats HTTP 402 from a directory as a hard
failure. Registration is opt-in via --execute; the default mode validates production only.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any

import httpx


ORIGIN = os.getenv(
    "PROJECTPERMIT_PUBLIC_ORIGIN",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
MANIFEST_URL = f"{ORIGIN}/.well-known/x402-service.json"
CANONICAL_PAID_ENDPOINT = f"{ORIGIN}/v1/check-project-requirements"
EXPECTED_PRICE = os.getenv("PROJECTPERMIT_EXPECTED_SINGLE_PRICE", "0.05")
EXPECTED_NETWORK = "eip155:8453"
EXPECTED_FACILITATOR = "https://facilitator.payai.network"

DIRECTORIES = (
    (
        "agent402_tools",
        "https://agent402.tools/api/index/register",
        {"origin": ORIGIN},
    ),
    (
        "true402",
        "https://true402.dev/api/v1/services",
        {"url": ORIGIN},
    ),
)


def _validate_manifest(payload: dict[str, Any]) -> None:
    if payload.get("x402") != "1.0":
        raise RuntimeError(f"unexpected manifest version: {payload.get('x402')!r}")
    if payload.get("endpoint") != CANONICAL_PAID_ENDPOINT:
        raise RuntimeError(f"unexpected paid endpoint: {payload.get('endpoint')!r}")

    pricing = payload.get("pricing") or {}
    if pricing != {"currency": "USDC", "base": EXPECTED_PRICE, "unit": "request"}:
        raise RuntimeError(f"unexpected launch pricing: {pricing!r}")

    payment = payload.get("payment") or {}
    if payment.get("chain") != "base" or payment.get("network") != EXPECTED_NETWORK:
        raise RuntimeError(f"unexpected payment network: {payment!r}")
    if payment.get("facilitator") != EXPECTED_FACILITATOR:
        raise RuntimeError(f"unexpected facilitator: {payment!r}")
    if payment.get("scheme") != "exact":
        raise RuntimeError(f"unexpected payment scheme: {payment!r}")
    address = str(payment.get("address") or "")
    if not address.startswith("0x") or len(address) != 42:
        raise RuntimeError("manifest is missing a valid public EVM pay-to address")

    description = str(payload.get("description") or "").lower()
    for term in ("building permit", "contractors", "ai agents"):
        if term not in description:
            raise RuntimeError(f"manifest description missing discovery term {term!r}")


def _safe_body(response: httpx.Response) -> str:
    text = response.text.strip().replace("\n", " ")
    return text[:1000]


def _register(client: httpx.Client, name: str, url: str, body: dict[str, str]) -> None:
    response = client.post(url, json=body)
    print(f"directory[{name}] status={response.status_code} body={_safe_body(response)}")
    if response.status_code == 402:
        raise RuntimeError(f"{name} unexpectedly requested payment; refusing to continue")
    if 200 <= response.status_code < 300:
        print(f"directory[{name}]=REGISTERED_OR_ACCEPTED")
        return
    if response.status_code == 409:
        print(f"directory[{name}]=ALREADY_REGISTERED")
        return
    raise RuntimeError(f"{name} registration failed with HTTP {response.status_code}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Submit the origin to free directories after production validation.",
    )
    args = parser.parse_args()

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        manifest_response = client.get(MANIFEST_URL)
        print(f"manifest_url={MANIFEST_URL}")
        print(f"manifest_status={manifest_response.status_code}")
        manifest_response.raise_for_status()
        manifest = manifest_response.json()
        _validate_manifest(manifest)
        print("production_x402_manifest=PASS")

        if not args.execute:
            print("directory_registration=DRY_RUN")
            return

        for name, url, body in DIRECTORIES:
            _register(client, name, url, body)

    print("free_x402_directory_registration=PASS")


if __name__ == "__main__":
    main()
