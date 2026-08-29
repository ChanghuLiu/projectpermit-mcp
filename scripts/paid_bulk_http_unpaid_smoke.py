"""Verify ProjectPermit's public paid bulk HTTP resource without paying."""
from __future__ import annotations

import os

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
    if "bulk" not in description.lower() or "1-50" not in description:
        raise SystemExit(f"Paid-bulk resource description is incomplete: {description}")

    accepts = challenge.get("accepts") or []
    if not any(item.get("network") == EXPECTED_NETWORK for item in accepts):
        raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")

    print("paid_bulk_http_402_challenge=PASS")
    print("paid_bulk_http_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
