"""Probe x402 facilitator capabilities without spending or using wallet keys."""
from __future__ import annotations

import json
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


def _catalog_summary(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        return {"catalog_shape": type(data).__name__}
    items = data.get("items", []) or data.get("resources", []) or []
    if not isinstance(items, list):
        items = []
    types = sorted(
        {str(item.get("type")) for item in items if isinstance(item, dict) and item.get("type")}
    )
    sample = items[0] if items and isinstance(items[0], dict) else None
    return {
        "catalog_total": (data.get("pagination") or {}).get("total", len(items))
        if isinstance(data.get("pagination"), dict)
        else len(items),
        "catalog_returned": len(items),
        "catalog_types": types,
        "catalog_sample_keys": sorted(sample.keys()) if sample else [],
    }


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
                row["base_sepolia_exact_v2"] = any(
                    _kind_matches(k) for k in kinds if isinstance(k, dict)
                )
                row["extensions"] = (
                    supported_json.get("extensions", []) if isinstance(supported_json, dict) else []
                )
            except Exception as exc:
                row["supported_error"] = f"{type(exc).__name__}: {exc}"
                row["base_sepolia_exact_v2"] = False

            try:
                resources = client.get(f"{base}/discovery/resources?type=mcp&limit=20")
                row["discovery_resources_status"] = resources.status_code
                if resources.status_code == 200:
                    row.update(_catalog_summary(resources.json()))
            except Exception as exc:
                row["discovery_resources_status"] = f"{type(exc).__name__}: {exc}"

            try:
                search = client.get(
                    f"{base}/discovery/search?query=building%20permit&type=mcp&limit=1"
                )
                row["discovery_search_status"] = search.status_code
            except Exception as exc:
                row["discovery_search_status"] = f"{type(exc).__name__}: {exc}"

            # Listing is the normative Bazaar capability needed to make MCP tools discoverable.
            # Natural-language /discovery/search is useful but not required for the canary.
            row["bazaar_listing"] = row.get("discovery_resources_status") == 200
            row["bazaar_search"] = row.get("discovery_search_status") == 200
            results.append(row)
            print(json.dumps(row, sort_keys=True))

    current = next(r for r in results if r["name"] == "x402.org")
    candidate = next(r for r in results if r["name"] == "goplausible")

    if not current.get("base_sepolia_exact_v2"):
        raise SystemExit("x402.org unexpectedly lost Base Sepolia exact v2 support")

    if candidate.get("base_sepolia_exact_v2") and candidate.get("bazaar_listing"):
        print("goplausible_bazaar_canary=COMPATIBLE_FOR_LISTING")
        if not candidate.get("bazaar_search"):
            print("goplausible_bazaar_search=UNAVAILABLE_NON_BLOCKING")
    else:
        print("goplausible_bazaar_canary=NOT_COMPATIBLE")
        raise SystemExit(3)


if __name__ == "__main__":
    main()
