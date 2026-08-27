"""Verify the public free HTTP preview without consuming paid x402 resources."""
from __future__ import annotations

import os

import httpx

BASE = os.getenv(
    "PROJECTPERMIT_HTTP_BASE",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
PREVIEW = f"{BASE}/v1/preview-project-requirements"


def main() -> None:
    capabilities = httpx.get(f"{BASE}/v1/capabilities", timeout=30.0)
    capabilities.raise_for_status()
    info = capabilities.json()
    if info.get("free_preview_resource") != "/v1/preview-project-requirements":
        raise SystemExit(f"Free preview missing from capabilities: {info}")
    if info.get("free_preview_address_resolution") is not False:
        raise SystemExit(f"Free preview must advertise address resolution disabled: {info}")

    response = httpx.post(
        PREVIEW,
        json={
            "jurisdiction": "ottawa_on",
            "project": {"family": "window_door", "action": "replace_same_size"},
            "property": {"heritage": False},
            "context": {"client_tag": "projectpermit-ci"},
        },
        timeout=30.0,
    )
    print(f"preview_status={response.status_code}")
    if response.status_code != 200:
        raise SystemExit(f"Expected preview HTTP 200: {response.text[:500]}")
    payload = response.json()
    if payload.get("determination") != "LIKELY_NOT_REQUIRED":
        raise SystemExit(f"Unexpected preview result: {payload}")

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
