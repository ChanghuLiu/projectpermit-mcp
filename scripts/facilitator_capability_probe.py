"""Probe x402 facilitator capabilities without spending or using wallet keys."""
from __future__ import annotations

import json
import os
from typing import Any

import httpx

FACILITATORS = [
    ("x402.org", "https://x402.org/facilitator"),
    ("goplausible", "https://facilitator.goplausible.xyz"),
]
TARGET_NETWORK = "eip155:84532"


def _kind_matches(kind: dict[str, Any]) -> bool:
    return (
        kind.get("network") == TARGET_NETWORK
        and kind.get("scheme") == "exact"
        and int(kind.get("x402Version", kind.get("x402_version", 0)) or 0) == 2
    )


def main() -> None:
    results: list[dict[str, Any]] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        for name, base in FACILITATORS:
            row: dict[str, Any] = {"name": name, "base": base}
            try:
                supported = client.get(f"{base}/supported")
                row["supported_status"] = supported.status_code
                supported_json = supported.json() if supported.status_code == 200 else {}
                kinds = supported_json.get("kinds", []) if isinstance(supported_json, dict) else []
                extensions = supported_json.get("extensions", []) if isinstance(supported_json, dict) else []
                row["base_sepolia_exact_v2"] = any(
                    _kind_matches(k) for k in kinds if isinstance(k, dict)
                )
                row["extensions"] = extensions
            except Exception as exc:
                row["supported_error"] = f"{type(exc).__name__}: {exc}"
                row["base_sepolia_exact_v2"] = False

            for path, field in [
                ("/discovery/resources?type=mcp&limit=1", "discovery_resources_status"),
                ("/discovery/search?query=building%20permit&type=mcp&limit=1", "discovery_search_status"),
            ]:
                try:
                    response = client.get(base + path)
                    row[field] = response.status_code
                except Exception as exc:
                    row[field] = f"{type(exc).__name__}: {exc}"

            row["bazaar_queryable"] = (
                row.get("discovery_resources_status") == 200
                and row.get("discovery_search_status") == 200
            )
            results.append(row)
            print(json.dumps(row, sort_keys=True))

    current = next(r for r in results if r["name"] == "x402.org")
    candidate = next(r for r in results if r["name"] == "goplausible")

    # x402.org is our known-good testnet payment facilitator; discovery is optional there.
    if not current.get("base_sepolia_exact_v2"):
        raise SystemExit("x402.org unexpectedly lost Base Sepolia exact v2 support")

    # A Bazaar canary is only safe if the alternative has both payment and discovery capability.
    if candidate.get("base_sepolia_exact_v2") and candidate.get("bazaar_queryable"):
        print("goplausible_bazaar_canary=COMPATIBLE")
    else:
        print("goplausible_bazaar_canary=NOT_COMPATIBLE")
        raise SystemExit(3)


if __name__ == "__main__":
    main()
