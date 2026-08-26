"""Read-only lookup of ProjectPermit in GoPlausible Bazaar.

No wallet, payment, or secret is used. Exit 0 when found; exit 2 when absent.
"""
from __future__ import annotations

import json
import os
from typing import Any

import httpx

FACILITATOR = os.getenv("PROJECTPERMIT_BAZAAR_URL", "https://facilitator.goplausible.xyz").rstrip("/")
PAY_TO = os.getenv("PROJECTPERMIT_X402_PAY_TO", "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A")
DOMAIN = "projectpermit-x402-mcp-production.up.railway.app"
TOOL_NAME = "check_project_requirements"


def _haystack(item: dict[str, Any]) -> str:
    return json.dumps(item, sort_keys=True).lower()


def main() -> None:
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        response = client.get(
            f"{FACILITATOR}/discovery/resources",
            params={"includeTestnets": "true", "limit": "1000"},
        )
        response.raise_for_status()
        data = response.json()

    items = data.get("items", []) if isinstance(data, dict) else []
    if not isinstance(items, list):
        items = []

    needles = [DOMAIN.lower(), TOOL_NAME.lower(), PAY_TO.lower()]
    matches = [
        item
        for item in items
        if isinstance(item, dict) and any(needle in _haystack(item) for needle in needles)
    ]

    print(f"facilitator={FACILITATOR}")
    print(f"catalog_total={(data.get('pagination') or {}).get('total', len(items)) if isinstance(data, dict) else len(items)}")
    print(f"catalog_returned={len(items)}")
    print(f"projectpermit_matches={len(matches)}")
    for item in matches[:5]:
        print("match=" + json.dumps(item, sort_keys=True))

    if not matches:
        print("projectpermit_bazaar=ABSENT")
        raise SystemExit(2)
    print("projectpermit_bazaar=FOUND")


if __name__ == "__main__":
    main()
