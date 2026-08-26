"""Verify ProjectPermit's public paid HTTP discovery twin without paying."""
from __future__ import annotations

import os

import httpx
from x402.http import decode_payment_required_header

URL = os.getenv(
    "PROJECTPERMIT_PAID_HTTP_URL",
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements",
)

PAYLOAD = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
    "resolve_address": False,
}

EXPECTED_JURISDICTIONS = {
    "gatineau_qc",
    "ottawa_on",
    "toronto_on",
    "mississauga_on",
    "laval_qc",
    "longueuil_qc",
}


def main() -> None:
    print(f"paid_http_url={URL}")
    response = httpx.post(URL, json=PAYLOAD, timeout=30.0, follow_redirects=True)
    print(f"status={response.status_code}")
    if response.status_code != 402:
        raise SystemExit(f"Expected HTTP 402, got {response.status_code}: {response.text[:500]}")

    header = response.headers.get("payment-required")
    if not header:
        raise SystemExit("Missing PAYMENT-REQUIRED header")

    challenge = decode_payment_required_header(header).model_dump(by_alias=True, exclude_none=True)
    resource = challenge.get("resource") or {}
    if resource.get("url") != URL:
        raise SystemExit(f"Unexpected x402 resource URL: {resource}")
    description = str(resource.get("description") or "")
    for city in ("Gatineau", "Ottawa", "Toronto", "Mississauga", "Laval", "Longueuil"):
        if city not in description:
            raise SystemExit(f"Jurisdiction missing from x402 resource description: {city}: {description}")

    accepts = challenge.get("accepts") or []
    if not any(item.get("network") == "eip155:84532" for item in accepts):
        raise SystemExit("Base Sepolia payment option missing")

    bazaar = (challenge.get("extensions") or {}).get("bazaar")
    if not bazaar:
        raise SystemExit("Bazaar discovery extension missing")

    info = bazaar.get("info") or {}
    input_info = info.get("input") or {}
    if input_info.get("type") != "http":
        raise SystemExit(f"Unexpected Bazaar resource type: {input_info}")
    if input_info.get("method") != "POST":
        raise SystemExit(f"Bazaar HTTP method was not enriched: {input_info}")
    if input_info.get("bodyType") != "json":
        raise SystemExit(f"Unexpected Bazaar body type: {input_info}")

    body = input_info.get("body") or {}
    if body.get("jurisdiction") != "ottawa_on":
        raise SystemExit(f"Unexpected Bazaar input example: {body}")

    input_schema = input_info.get("schema") or input_info.get("inputSchema") or {}
    jurisdiction_schema = ((input_schema.get("properties") or {}).get("jurisdiction") or {})
    if jurisdiction_schema:
        enum = set(jurisdiction_schema.get("enum") or [])
        if not EXPECTED_JURISDICTIONS.issubset(enum):
            raise SystemExit(f"Jurisdiction enum missing from Bazaar schema: {enum}")

    output = info.get("output") or {}
    if (output.get("example") or {}).get("engine_version") != "phase0-0.1.0":
        raise SystemExit(f"Unexpected Bazaar output example: {output}")

    print("http_bazaar_six_jurisdictions=PASS")
    print("http_bazaar_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
