"""Verify the public free HTTP preview without consuming paid x402 resources."""
from __future__ import annotations

import os

import httpx

BASE = os.getenv(
    "PROJECTPERMIT_HTTP_BASE",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
PREVIEW = f"{BASE}/v1/preview-project-requirements"


def _preview(
    jurisdiction: str,
    project: dict,
    property_facts: dict | None = None,
    *,
    context: dict | None = None,
) -> dict:
    response = httpx.post(
        PREVIEW,
        json={
            "jurisdiction": jurisdiction,
            "project": project,
            "property": property_facts or {},
            "context": {"client_tag": "projectpermit-ci", **(context or {})},
        },
        timeout=30.0,
    )
    print(f"preview_status[{jurisdiction}]={response.status_code}")
    if response.status_code != 200:
        raise SystemExit(
            f"Expected preview HTTP 200 for {jurisdiction}: {response.text[:500]}"
        )
    return response.json()


def _first_rule_id(payload: dict) -> str | None:
    requirements = payload.get("requirements") or []
    if not requirements:
        return None
    return requirements[0].get("rule_id")


def _identity(payload: dict) -> dict:
    bundle = payload.get("action_bundle") or {}
    if bundle.get("bundle_version") != "2026-08-29.2":
        raise SystemExit(f"HTTP preview missing Layer 4 action bundle: {bundle}")
    identity = bundle.get("identity") or {}
    if not identity.get("bundle_id") or not identity.get("idempotency_key"):
        raise SystemExit(f"HTTP preview missing decision identity: {bundle}")
    if not str(identity["bundle_id"]).startswith("ppb_"):
        raise SystemExit(f"Unexpected HTTP bundle id: {identity}")
    return identity


def main() -> None:
    capabilities = httpx.get(f"{BASE}/v1/capabilities", timeout=30.0)
    capabilities.raise_for_status()
    info = capabilities.json()
    if info.get("free_preview_resource") != "/v1/preview-project-requirements":
        raise SystemExit(f"Free preview missing from capabilities: {info}")
    if info.get("free_preview_address_resolution") is not False:
        raise SystemExit(f"Free preview must advertise address resolution disabled: {info}")
    bundle_info = info.get("action_bundle") or {}
    includes = set(bundle_info.get("includes") or [])
    if not {"identity", "change"}.issubset(includes):
        raise SystemExit(f"HTTP capabilities missing decision identity/change: {bundle_info}")
    identity_capabilities = set(bundle_info.get("identity_capabilities") or [])
    if "work_record_scoped_idempotency" not in identity_capabilities:
        raise SystemExit(f"HTTP capabilities missing scoped idempotency: {bundle_info}")

    project = {"family": "window_door", "action": "replace_same_size"}
    property_facts = {"heritage": False}
    payload = _preview("ottawa_on", project, property_facts)
    if payload.get("determination") != "LIKELY_NOT_REQUIRED":
        raise SystemExit(f"Unexpected preview result: {payload}")
    first_identity = _identity(payload)
    first_bundle = payload.get("action_bundle") or {}
    if (first_bundle.get("change") or {}).get("classification") != "FIRST_OBSERVATION":
        raise SystemExit(f"Initial HTTP preview did not classify FIRST_OBSERVATION: {first_bundle}")

    repeat = _preview(
        "ottawa_on",
        project,
        property_facts,
        context={"prior_decision_identity": first_identity},
    )
    repeat_identity = _identity(repeat)
    repeat_bundle = repeat.get("action_bundle") or {}
    if (repeat_bundle.get("change") or {}).get("classification") != "UNCHANGED":
        raise SystemExit(f"Repeated HTTP preview did not classify UNCHANGED: {repeat_bundle}")
    if repeat_identity.get("idempotency_key") != first_identity.get("idempotency_key"):
        raise SystemExit(f"Repeated HTTP preview changed idempotency key: {repeat_bundle}")
    print("http_preview_identity_repeat=PASS")

    clean_basement = {
        "family": "basement",
        "action": "finish_basement",
        "structural_change": False,
        "material_alteration": False,
        "dwelling_unit_change": False,
        "new_plumbing": False,
    }
    divergence_expectations = {
        "toronto_on": ("LIKELY_NOT_REQUIRED", "TOR-BASE-001"),
        "mississauga_on": ("REQUIRED", "MIS-BASE-001"),
        "ottawa_on": ("LIKELY_REQUIRED", "OTT-BASE-001"),
    }
    observed: dict[str, str] = {}
    for jurisdiction, (expected_determination, expected_rule_id) in divergence_expectations.items():
        result = _preview(jurisdiction, clean_basement)
        _identity(result)
        determination = result.get("determination")
        rule_id = _first_rule_id(result)
        observed[jurisdiction] = str(determination)
        print(f"divergence[{jurisdiction}]={determination} rule_id={rule_id}")
        if determination != expected_determination or rule_id != expected_rule_id:
            raise SystemExit(
                f"Municipal divergence regression for {jurisdiction}: "
                f"expected {expected_determination}/{expected_rule_id}, "
                f"got {determination}/{rule_id}: {result}"
            )

    if len(set(observed.values())) != 3:
        raise SystemExit(f"Expected three distinct live basement outcomes, got {observed}")
    print("municipal_divergence_live=PASS")

    rejected = httpx.post(
        PREVIEW,
        json={
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "address": "123 Example St",
            "resolve_address": True,
        },
        timeout=30.0,
    )
    print(f"address_rejection_status={rejected.status_code}")
    if rejected.status_code != 422:
        raise SystemExit(
            f"Free preview must reject address/address-resolution fields: "
            f"{rejected.status_code} {rejected.text[:500]}"
        )

    print("http_preview_no_address_boundary=PASS")
    print("http_preview_remote_smoke=PASS")


if __name__ == "__main__":
    main()
