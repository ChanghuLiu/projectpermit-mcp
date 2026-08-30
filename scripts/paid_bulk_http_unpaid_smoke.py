"""Verify ProjectPermit's public paid bulk HTTP resource without paying."""
from __future__ import annotations

import os
from decimal import Decimal

import httpx
from x402.http import decode_payment_required_header

BASE_URL = os.getenv(
    "PROJECTPERMIT_HTTP_BASE_URL",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
URL = os.getenv(
    "PROJECTPERMIT_PAID_BULK_HTTP_URL",
    f"{BASE_URL}/v1/check-project-requirements-batch",
)
EXPECTED_NETWORK = os.getenv("PROJECTPERMIT_SMOKE_X402_NETWORK", "eip155:8453")
EXPECTED_ASSET = os.getenv(
    "PROJECTPERMIT_SMOKE_X402_ASSET",
    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
)
EXPECTED_PRICE_USD = os.getenv("PROJECTPERMIT_SMOKE_X402_BATCH_AMOUNT", "5.00")
EXPECTED_WIRE_AMOUNT = str(int(Decimal(EXPECTED_PRICE_USD) * Decimal("1000000")))

PAYLOAD = {
    "items": [
        {
            "client_ref": "paid-bulk-unpaid-smoke",
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {"heritage": False},
            "context": {"client_tag": "projectpermit-ci"},
        }
    ]
}


def main() -> None:
    print(f"paid_bulk_http_url={URL}")
    print(f"expected_network={EXPECTED_NETWORK}")
    print(f"expected_price_usd={EXPECTED_PRICE_USD}")
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        capabilities_response = client.get(f"{BASE_URL}/v1/capabilities")
        capabilities_response.raise_for_status()
        capabilities = capabilities_response.json()
        if capabilities.get("paid_batch_resource") != "/v1/check-project-requirements-batch":
            raise SystemExit(f"Paid bulk resource missing from capabilities: {capabilities}")
        if capabilities.get("bulk_max_items") != 50:
            raise SystemExit(f"Unexpected bulk_max_items: {capabilities.get('bulk_max_items')}")
        workflow = capabilities.get("workflow_guidance") or {}
        if workflow.get("field") != "workflow":
            raise SystemExit(f"Workflow guidance missing from capabilities: {workflow}")
        gate = capabilities.get("mutation_gate") or {}
        if set(gate.get("states") or []) != {
            "READY_FOR_EXPLICIT_WRITE",
            "NOOP_UNCHANGED",
            "BLOCKED",
        }:
            raise SystemExit(f"Mutation gate missing from paid-bulk capabilities: {gate}")
        if gate.get("unconditional_create_allowed") is not False:
            raise SystemExit(f"Paid-bulk capabilities must forbid unconditional create: {gate}")
        print("paid_bulk_safe_writeback_capabilities=PASS")
        print("paid_bulk_capabilities=PASS")

        response = client.post(URL, json=PAYLOAD)

    print(f"status={response.status_code}")
    if response.status_code != 402:
        raise SystemExit(f"Expected HTTP 402, got {response.status_code}: {response.text[:500]}")

    header = response.headers.get("payment-required")
    if not header:
        raise SystemExit("Missing PAYMENT-REQUIRED header")

    challenge = decode_payment_required_header(header).model_dump(by_alias=True, exclude_none=True)
    if challenge.get("x402Version") != 2:
        raise SystemExit(f"Unexpected x402 version: {challenge}")

    resource = challenge.get("resource") or {}
    if resource.get("url") != URL:
        raise SystemExit(f"Unexpected paid-bulk resource URL: {resource}")
    description = str(resource.get("description") or "")
    lower_description = description.lower()
    if "bulk" not in lower_description or "1-50" not in description:
        raise SystemExit(f"Paid-bulk resource description is incomplete: {description}")
    if "mutation" not in lower_description or "writeback" not in lower_description:
        raise SystemExit(f"Paid-bulk resource description missing Layer 5 positioning: {description}")

    accepts = challenge.get("accepts") or []
    matching = [item for item in accepts if item.get("network") == EXPECTED_NETWORK]
    if not matching:
        raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")
    if not any(
        str(item.get("amount")) == EXPECTED_WIRE_AMOUNT
        and str(item.get("asset") or "").lower() == EXPECTED_ASSET.lower()
        for item in matching
    ):
        raise SystemExit(
            f"Paid bulk runtime price/asset mismatch: expected ${EXPECTED_PRICE_USD} USDC "
            f"({EXPECTED_WIRE_AMOUNT} base units, asset {EXPECTED_ASSET}): {matching}"
        )

    print("paid_bulk_runtime_price=PASS")
    print("paid_bulk_http_402_challenge=PASS")
    print("paid_bulk_http_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
