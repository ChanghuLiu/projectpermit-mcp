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
    if "action" not in description.lower() or "evidence" not in description.lower():
        raise SystemExit(f"x402 resource description missing action/evidence bundle positioning: {description}")

    accepts = challenge.get("accepts") or []
    if not any(item.get("network") == EXPECTED_NETWORK for item in accepts):
        raise SystemExit(f"Expected payment network missing: {EXPECTED_NETWORK}: {accepts}")

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

    # x402 v2 puts the JSON Schema for `info` at extensions.bazaar.schema.
    # The request-body schema lives under schema.properties.input.properties.body;
    # it is not serialized as info.input.schema.
    extension_schema = bazaar.get("schema") or {}
    schema_properties = extension_schema.get("properties") or {}
    input_schema = (((schema_properties.get("input") or {}).get("properties") or {}).get("body") or {})
    jurisdiction_schema = ((input_schema.get("properties") or {}).get("jurisdiction") or {})
    enum = set(jurisdiction_schema.get("enum") or [])
    if not EXPECTED_JURISDICTIONS.issubset(enum):
        raise SystemExit(f"Jurisdiction enum missing from Bazaar extension schema: {enum}")

    output = info.get("output") or {}
    example = output.get("example") or {}
    if example.get("engine_version") != "phase0-0.1.0":
        raise SystemExit(f"Unexpected Bazaar output example: {output}")
    workflow = example.get("workflow") or {}
    if workflow.get("recommended_route") != "CONTINUE_WITH_EVIDENCE":
        raise SystemExit(f"Bazaar output example missing workflow routing: {workflow}")
    bundle = example.get("action_bundle") or {}
    if not bundle:
        raise SystemExit(f"Bazaar output example missing action_bundle: {example}")
    if (bundle.get("routing") or {}).get("recommended_route") != "CONTINUE_WITH_EVIDENCE":
        raise SystemExit(f"Bazaar action bundle missing routing: {bundle}")
    tasks = bundle.get("tasks") or []
    if not tasks or tasks[0].get("task_type") != "ATTACH_EVIDENCE":
        raise SystemExit(f"Bazaar action bundle missing proposed task: {bundle}")

    # OutputConfig.schema is folded into the schema for info.output.example by the
    # current x402 Python SDK. `info.output` itself only contains type/format/example.
    output_example_schema = (
        ((((schema_properties.get("output") or {}).get("properties") or {}).get("example") or {}))
    )
    if "action_bundle" not in (output_example_schema.get("properties") or {}):
        raise SystemExit(
            f"Bazaar extension schema missing action_bundle output contract: {output_example_schema}"
        )

    print("http_bazaar_action_bundle=PASS")
    print("http_bazaar_seven_jurisdictions=PASS")
    print("http_bazaar_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
