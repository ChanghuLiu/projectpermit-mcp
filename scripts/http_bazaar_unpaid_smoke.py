"""Verify ProjectPermit's public paid HTTP discovery twin without paying."""
from __future__ import annotations

import os

import httpx
from x402.http import decode_payment_required_header

URL = os.getenv(
    "PROJECTPERMIT_PAID_HTTP_URL",
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements",
)
EXPECTED_NETWORK = os.getenv("PROJECTPERMIT_SMOKE_X402_NETWORK", "eip155:8453")

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
    "vancouver_bc",
}


def main() -> None:
    print(f"paid_http_url={URL}")
    print(f"expected_network={EXPECTED_NETWORK}")
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
    for city in ("Gatineau", "Ottawa", "Toronto", "Mississauga", "Laval", "Longueuil", "Vancouver"):
        if city not in description:
            raise SystemExit(f"Jurisdiction missing from x402 resource description: {city}: {description}")
    lower_description = description.lower()
    for required_term in ("action", "evidence", "idempotency", "change"):
        if required_term not in lower_description:
            raise SystemExit(f"x402 resource description missing {required_term} positioning: {description}")

    accepts = challenge.get("accepts") or []
    if not any(item.get("network") == EXPECTED_NETWORK for item in accepts):
        raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")

    bazaar = (challenge.get("extensions") or {}).get("bazaar")
    if not bazaar:
        raise SystemExit("Bazaar discovery extension missing")

    info = bazaar.get("info") or {}
    input_info = info.get("input") or {}
    if input_info.get("type") != "http" or input_info.get("method") != "POST":
        raise SystemExit(f"Unexpected Bazaar input contract: {input_info}")
    if input_info.get("bodyType") != "json":
        raise SystemExit(f"Unexpected Bazaar body type: {input_info}")
    body = input_info.get("body") or {}
    if body.get("jurisdiction") != "ottawa_on":
        raise SystemExit(f"Unexpected Bazaar input example: {body}")

    extension_schema = bazaar.get("schema") or {}
    schema_properties = extension_schema.get("properties") or {}
    input_schema = (((schema_properties.get("input") or {}).get("properties") or {}).get("body") or {})
    jurisdiction_schema = ((input_schema.get("properties") or {}).get("jurisdiction") or {})
    enum = set(jurisdiction_schema.get("enum") or [])
    if not EXPECTED_JURISDICTIONS.issubset(enum):
        raise SystemExit(f"Jurisdiction enum missing from Bazaar extension schema: {enum}")
    context_description = str(((input_schema.get("properties") or {}).get("context") or {}).get("description") or "")
    if "prior_decision_identity" not in context_description:
        raise SystemExit(f"Bazaar input schema missing repeat identity contract: {context_description}")

    output = info.get("output") or {}
    example = output.get("example") or {}
    if example.get("engine_version") != "phase0-0.1.0":
        raise SystemExit(f"Unexpected Bazaar output example: {output}")
    workflow = example.get("workflow") or {}
    if workflow.get("recommended_route") != "CONTINUE_WITH_EVIDENCE":
        raise SystemExit(f"Bazaar output example missing workflow routing: {workflow}")
    bundle = example.get("action_bundle") or {}
    if bundle.get("bundle_version") != "2026-08-29.2":
        raise SystemExit(f"Bazaar output example missing Layer 4 bundle version: {bundle}")
    identity = bundle.get("identity") or {}
    if not identity.get("bundle_id") or not identity.get("idempotency_key"):
        raise SystemExit(f"Bazaar output example missing decision identity: {bundle}")
    if (bundle.get("change") or {}).get("classification") != "FIRST_OBSERVATION":
        raise SystemExit(f"Bazaar output example missing change classification: {bundle}")
    if (bundle.get("routing") or {}).get("recommended_route") != "CONTINUE_WITH_EVIDENCE":
        raise SystemExit(f"Bazaar action bundle missing routing: {bundle}")
    tasks = bundle.get("tasks") or []
    if not tasks or tasks[0].get("task_type") != "ATTACH_EVIDENCE":
        raise SystemExit(f"Bazaar action bundle missing proposed task: {bundle}")

    output_example_schema = (
        ((((schema_properties.get("output") or {}).get("properties") or {}).get("example") or {}))
    )
    output_properties = output_example_schema.get("properties") or {}
    if "action_bundle" not in output_properties:
        raise SystemExit(
            f"Bazaar extension schema missing action_bundle output contract: {output_example_schema}"
        )
    bundle_schema = output_properties.get("action_bundle") or {}
    bundle_properties = bundle_schema.get("properties") or {}
    if not {"identity", "change"}.issubset(bundle_properties):
        raise SystemExit(f"Bazaar output schema missing identity/change: {bundle_schema}")

    print("http_bazaar_identity=PASS")
    print("http_bazaar_action_bundle=PASS")
    print("http_bazaar_seven_jurisdictions=PASS")
    print("http_bazaar_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
