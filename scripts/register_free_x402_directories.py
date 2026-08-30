"""Register ProjectPermit with zero-cost x402 directories after validating production discovery.

This script never sends payment credentials and treats HTTP 402 from a directory as a hard
failure. Registration is opt-in via --execute; the default mode validates production only.
Transient directory outages and rate limits are recorded but do not block later directories.
After Agent402 registration, read-only discovery checks verify both seller indexing and
representative cross-seller task routing; propagation lag is observational and never fails
registration.
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
EXPECTED_PRICE = os.getenv("PROJECTPERMIT_EXPECTED_SINGLE_PRICE", "0.20")
EXPECTED_NETWORK = "eip155:8453"
EXPECTED_FACILITATOR = "https://facilitator.payai.network"
AGENT402_FIND_BASE_URL = "https://agent402.tools/api/find"
AGENT402_ROUTE_URL = "https://agent402.tools/api/route"
AGENT402_TASK_QUERIES = (
    "building permit",
    "renovation permit",
)

PROBE_BODY = json.dumps(
    {
        "jurisdiction": "ottawa_on",
        "project": {"family": "window_door", "action": "replace_same_size"},
        "property": {"heritage": False},
        "resolve_address": False,
    },
    separators=(",", ":"),
)

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
    (
        "402index",
        "https://402index.io/api/v1/register",
        {
            "url": CANONICAL_PAID_ENDPOINT,
            "name": "ProjectPermit Building Permit Preflight",
            "protocol": "x402",
            "http_method": "POST",
            "probe_body": PROBE_BODY,
            "description": (
                "Building permit requirements API for contractors and AI agents across 7 "
                "Canadian municipalities with deterministic rules and official-source evidence."
            ),
            "price_usd": float(EXPECTED_PRICE),
            "payment_asset": "USDC",
            "payment_network": "Base",
            "provider": "ProjectPermit",
        },
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
    return text[:1500]


def _register(client: httpx.Client, name: str, url: str, body: dict[str, Any]) -> str:
    try:
        response = client.post(url, json=body)
    except httpx.RequestError as exc:
        print(f"directory[{name}]=TRANSIENT_NETWORK_FAILURE error={type(exc).__name__}")
        return "transient_failure"

    print(f"directory[{name}] status={response.status_code} body={_safe_body(response)}")
    if response.status_code == 402:
        raise RuntimeError(f"{name} unexpectedly requested payment; refusing to continue")
    if 200 <= response.status_code < 300:
        print(f"directory[{name}]=REGISTERED_OR_ACCEPTED")
        return "accepted"
    if response.status_code == 409:
        print(f"directory[{name}]=ALREADY_REGISTERED")
        return "accepted"
    if response.status_code == 429:
        print(f"directory[{name}]=TRANSIENT_RATE_LIMIT")
        return "transient_failure"
    if 500 <= response.status_code < 600:
        print(f"directory[{name}]=TRANSIENT_PROVIDER_FAILURE")
        return "transient_failure"
    raise RuntimeError(f"{name} registration failed with HTTP {response.status_code}")


def _payload_mentions_projectpermit(payload: Any) -> bool:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False).lower()
    return ORIGIN.lower() in serialized or "projectpermit" in serialized


def _observe_agent402_public_find(client: httpx.Client, query: str = "ProjectPermit") -> bool | None:
    """Observe Agent402's local find surface for seller-index recognition hints."""
    try:
        response = client.get(AGENT402_FIND_BASE_URL, params={"q": query})
    except httpx.RequestError as exc:
        print(
            "directory[agent402_tools]_public_find="
            f"TRANSIENT_NETWORK_FAILURE query={query!r} error={type(exc).__name__}"
        )
        return None

    print(
        "directory[agent402_tools]_public_find "
        f"query={query!r} status={response.status_code} body={_safe_body(response)}"
    )
    if response.status_code == 402:
        raise RuntimeError("Agent402 public find unexpectedly requested payment; refusing to continue")
    if response.status_code != 200:
        print(f"directory[agent402_tools]_public_find=UNAVAILABLE query={query!r}")
        return None

    try:
        payload = response.json()
    except ValueError:
        print(f"directory[agent402_tools]_public_find=INVALID_JSON query={query!r}")
        return None

    visible = _payload_mentions_projectpermit(payload)
    print(
        "directory[agent402_tools]_public_find="
        + ("VISIBLE" if visible else "NOT_VISIBLE_YET")
        + f" query={query!r}"
    )
    return visible


def _observe_agent402_external_route(client: httpx.Client, query: str) -> bool | None:
    """Observe the free Smart Order Router across external sellers for a real task query."""
    body = {"query": query, "top": 10, "include": "external"}
    try:
        response = client.post(AGENT402_ROUTE_URL, json=body)
    except httpx.RequestError as exc:
        print(
            "directory[agent402_tools]_external_route="
            f"TRANSIENT_NETWORK_FAILURE query={query!r} error={type(exc).__name__}"
        )
        return None

    print(
        "directory[agent402_tools]_external_route "
        f"query={query!r} status={response.status_code} body={_safe_body(response)}"
    )
    if response.status_code == 402:
        raise RuntimeError("Agent402 external route unexpectedly requested payment; refusing to continue")
    if response.status_code != 200:
        print(f"directory[agent402_tools]_external_route=UNAVAILABLE query={query!r}")
        return None

    try:
        payload = response.json()
    except ValueError:
        print(f"directory[agent402_tools]_external_route=INVALID_JSON query={query!r}")
        return None

    visible = _payload_mentions_projectpermit(payload)
    print(
        "directory[agent402_tools]_external_route="
        + ("ROUTED" if visible else "NOT_ROUTED")
        + f" query={query!r}"
    )
    return visible


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Submit the origin/endpoints to free directories after production validation.",
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

        transient_failures: list[str] = []
        agent402_accepted = False
        for name, url, body in DIRECTORIES:
            outcome = _register(client, name, url, body)
            if name == "agent402_tools" and outcome == "accepted":
                agent402_accepted = True
            if outcome == "transient_failure":
                transient_failures.append(name)

        if agent402_accepted:
            _observe_agent402_public_find(client)
            for query in AGENT402_TASK_QUERIES:
                _observe_agent402_external_route(client, query)

    if transient_failures:
        print("directory_transient_failures=" + ",".join(transient_failures))
    print("free_x402_directory_registration=PASS")


if __name__ == "__main__":
    main()
