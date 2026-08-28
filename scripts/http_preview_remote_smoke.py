"""Verify the public free HTTP preview without consuming paid x402 resources."""
from __future__ import annotations

import os

import httpx

BASE = os.getenv(
    "PROJECTPERMIT_HTTP_BASE",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
PREVIEW = f"{BASE}/v1/preview-project-requirements"


def _preview(jurisdiction: str, project: dict, property_facts: dict | None = None) -> dict:
    response = httpx.post(
        PREVIEW,
        json={
            "jurisdiction": jurisdiction,
            "project": project,
            "property": property_facts or {},
            "context": {"client_tag": "projectpermit-ci"},
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


def main() -> None:
    capabilities = httpx.get(f"{BASE}/v1/capabilities", timeout=30.0)
    capabilities.raise_for_status()
    info = capabilities.json()
    if info.get("free_preview_resource") != "/v1/preview-project-requirements":
        raise SystemExit(f"Free preview missing from capabilities: {info}")
    if info.get("free_preview_address_resolution") is not False:
        raise SystemExit(f"Free preview must advertise address resolution disabled: {info}")

    payload = _preview(
        "ottawa_on",
        {"family": "window_door", "action": "replace_same_size"},
        {"heritage": False},
    )
    if payload.get("determination") != "LIKELY_NOT_REQUIRED":
        raise SystemExit(f"Unexpected preview result: {payload}")

    # Live regression for a commercially important municipality-specific divergence.
    # The same clean basement scope must not collapse into one generic Ontario answer:
    # Toronto publishes an explicit exemption, Mississauga publishes a requirement,
    # and Ottawa treats finishing a basement as a permit project with scope-dependent need.
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
        determination = result.get("determination")
        rule_id = _first_rule_id(result)
        observed[jurisdiction] = str(determination)
        print(
            f"divergence[{jurisdiction}]={determination} "
            f"rule_id={rule_id}"
        )
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
