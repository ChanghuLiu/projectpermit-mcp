"""Verify ProjectPermit's public paid HTTP discovery twin without paying."""
from __future__ import annotations

import os

import httpx
from x402.http import decode_payment_required_header

URL = os.getenv(
    "PROJECTPERMIT_PAID_HTTP_URL",
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements",
)
BASE_URL = URL.split("/v1/", 1)[0]
EXPECTED_NETWORK = os.getenv("PROJECTPERMIT_SMOKE_X402_NETWORK", "eip155:8453")
EXPECTED_SINGLE_AMOUNT = os.getenv("PROJECTPERMIT_SMOKE_X402_SINGLE_AMOUNT", "0.20")
EXPECTED_BATCH_AMOUNT = os.getenv("PROJECTPERMIT_SMOKE_X402_BATCH_AMOUNT", "5.00")

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


def _verify_openapi_discovery() -> None:
    response = httpx.get(f"{BASE_URL}/openapi.json", timeout=30.0, follow_redirects=True)
    if response.status_code != 200:
        raise SystemExit(f"OpenAPI discovery unavailable: {response.status_code}: {response.text[:300]}")
    schema = response.json()
    info = schema.get("info") or {}
    if not info.get("x-guidance"):
        raise SystemExit(f"OpenAPI info.x-guidance missing: {info}")
    projectpermit_info = info.get("x-projectpermit") or {}
    if projectpermit_info.get("commercialNetwork") != EXPECTED_NETWORK:
        raise SystemExit(f"OpenAPI commercial network mismatch: {projectpermit_info}")
    if projectpermit_info.get("paymentProtocol") != "x402-v2":
        raise SystemExit(f"OpenAPI x402 protocol metadata missing: {projectpermit_info}")

    expectations = {
        "/v1/check-project-requirements": EXPECTED_SINGLE_AMOUNT,
        "/v1/check-project-requirements-batch": EXPECTED_BATCH_AMOUNT,
    }
    paths = schema.get("paths") or {}
    for path, amount in expectations.items():
        operation = ((paths.get(path) or {}).get("post") or {})
        payment = operation.get("x-payment-info") or {}
        price = payment.get("price") or {}
        if price != {"mode": "fixed", "currency": "USD", "amount": amount}:
            raise SystemExit(f"OpenAPI x-payment-info price mismatch for {path}: {payment}")
        if payment.get("protocols") != [{"x402": {}}]:
            raise SystemExit(f"OpenAPI x402 protocol declaration missing for {path}: {payment}")
        if "402" not in (operation.get("responses") or {}):
            raise SystemExit(f"OpenAPI 402 response missing for {path}: {operation}")
        runtime = operation.get("x-projectpermit-payment") or {}
        if runtime.get("network") != EXPECTED_NETWORK or runtime.get("asset") != "USDC":
            raise SystemExit(f"OpenAPI runtime payment metadata mismatch for {path}: {runtime}")

    preview = ((paths.get("/v1/preview-project-requirements") or {}).get("post") or {})
    if "x-payment-info" in preview:
        raise SystemExit(f"Free preview must not be marked as paid in OpenAPI: {preview}")
    print("http_openapi_x402_discovery=PASS")


def main() -> None:
    print(f"paid_http_url={URL}")
    print(f"expected_network={EXPECTED_NETWORK}")
    _verify_openapi_discovery()

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
    for required_term in ("action", "evidence", "idempotency", "change", "writeback", "mutation"):
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
    if "prior_decision_identity" not in context_description or "writeback" not in context_description.lower():
        raise SystemExit(f"Bazaar input schema missing repeat identity/safe-writeback contract: {context_description}")

    output = info.get("output") or {}
    example = output.get("example") or {}
    if example.get("engine_version") != "phase0-0.1.0":
        raise SystemExit(f"Unexpected Bazaar output example: {output}")
    workflow = example.get("workflow") or {}
    if workflow.get("recommended_route") != "CONTINUE_WITH_EVIDENCE":
        raise SystemExit(f"Bazaar output example missing workflow routing: {workflow}")
    bundle = example.get("action_bundle") or {}
    if bundle.get("bundle_version") != "2026-08-29.3":
        raise SystemExit(f"Bazaar output example missing Layer 5 action bundle version: {bundle}")
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
    gate = bundle.get("mutation_gate") or {}
    if gate.get("state") != "BLOCKED":
        raise SystemExit(f"Unscoped Bazaar example must be writeback-blocked: {gate}")
    if "MISSING_WORK_RECORD_SCOPE" not in (gate.get("reason_codes") or []):
        raise SystemExit(f"Bazaar mutation gate missing unscoped blocker: {gate}")
    if gate.get("execution_requires_explicit_request") is not True:
        raise SystemExit(f"Bazaar mutation gate must require explicit request: {gate}")
    if (gate.get("idempotency") or {}).get("unconditional_create_allowed") is not False:
        raise SystemExit(f"Bazaar mutation gate must forbid unconditional create: {gate}")

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
    if not {"identity", "change", "mutation_gate"}.issubset(bundle_properties):
        raise SystemExit(f"Bazaar output schema missing identity/change/mutation gate: {bundle_schema}")
    gate_schema = bundle_properties.get("mutation_gate") or {}
    gate_properties = gate_schema.get("properties") or {}
    state_enum = set((gate_properties.get("state") or {}).get("enum") or [])
    if state_enum != {"READY_FOR_EXPLICIT_WRITE", "NOOP_UNCHANGED", "BLOCKED"}:
        raise SystemExit(f"Bazaar output schema missing mutation gate states: {gate_schema}")

    print("http_bazaar_safe_writeback_gate=PASS")
    print("http_bazaar_identity=PASS")
    print("http_bazaar_action_bundle=PASS")
    print("http_bazaar_seven_jurisdictions=PASS")
    print("http_bazaar_unpaid_smoke=PASS")


if __name__ == "__main__":
    main()
