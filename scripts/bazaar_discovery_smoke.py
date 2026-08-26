"""Check whether ProjectPermit is discoverable through the x402 facilitator Bazaar.

This is a read-only check. It performs no payment and uses no wallet key.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any

import httpx

FACILITATOR = os.getenv(
    "PROJECTPERMIT_X402_FACILITATOR_URL", "https://x402.org/facilitator"
).rstrip("/")
PAY_TO = os.getenv(
    "PROJECTPERMIT_X402_PAY_TO", "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A"
)
EXPECTED_TOOL = "check_project_requirements"


def _matches(item: dict[str, Any]) -> bool:
    haystack = json.dumps(item, sort_keys=True).lower()
    return (
        "projectpermit" in haystack
        or EXPECTED_TOOL.lower() in haystack
        or PAY_TO.lower() in haystack
    )


def main() -> None:
    candidates: list[dict[str, Any]] = []
    attempts: list[tuple[str, int]] = []
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        search = client.get(
            f"{FACILITATOR}/discovery/search",
            params={"query": "ProjectPermit building permit", "type": "mcp", "limit": "20"},
        )
        attempts.append(("search", search.status_code))
        if search.status_code == 200:
            data = search.json()
            candidates.extend(data.get("resources", []) or [])

        listing = client.get(
            f"{FACILITATOR}/discovery/resources",
            params={"type": "mcp", "payTo": PAY_TO, "limit": "100"},
        )
        attempts.append(("list", listing.status_code))
        if listing.status_code == 200:
            data = listing.json()
            candidates.extend(data.get("items", []) or [])

    unique: dict[str, dict[str, Any]] = {}
    for item in candidates:
        key = str(item.get("resource") or json.dumps(item, sort_keys=True))
        unique[key] = item

    matches = [item for item in unique.values() if _matches(item)]
    print(f"facilitator={FACILITATOR}")
    print(f"attempts={attempts}")
    print(f"candidate_count={len(unique)}")
    print(f"projectpermit_matches={len(matches)}")
    for item in matches[:5]:
        print("match=" + json.dumps(item, sort_keys=True))

    if not matches:
        print("bazaar_projectpermit_discovery=NOT_FOUND")
        raise SystemExit(2)

    print("bazaar_projectpermit_discovery=PASS")


if __name__ == "__main__":
    main()
