"""Read-only lookup of ProjectPermit in GoPlausible Bazaar.

No wallet, payment, or secret is used. Exit 0 only when the canonical HTTPS HTTP
listing is present. Exit 2 when ProjectPermit is absent; exit 3 when only a stale
non-HTTPS listing is present.
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

import httpx

FACILITATOR = os.getenv("PROJECTPERMIT_BAZAAR_URL", "https://facilitator.goplausible.xyz").rstrip("/")
PAY_TO = os.getenv("PROJECTPERMIT_X402_PAY_TO", "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A")
MCP_DOMAIN = "projectpermit-x402-mcp-production.up.railway.app"
HTTP_DOMAIN = "projectpermit-api-v2-production.up.railway.app"
CANONICAL_HTTP_URL = f"https://{HTTP_DOMAIN}/v1/check-project-requirements"
TOOL_NAME = "check_project_requirements"
PAGE_SIZE = 200
MAX_PAGES = 20


def _haystack(item: dict[str, Any]) -> str:
    return json.dumps(item, sort_keys=True).lower()


def _fetch_page(client: httpx.Client, offset: int) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = client.get(
                f"{FACILITATOR}/discovery/resources",
                params={
                    "includeTestnets": "true",
                    "limit": str(PAGE_SIZE),
                    "offset": str(offset),
                },
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {}
        except (httpx.HTTPError, ValueError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1.0 * (attempt + 1))
    assert last_error is not None
    raise last_error


def main() -> None:
    matches: list[dict[str, Any]] = []
    scanned = 0
    catalog_total: int | None = None

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        for page in range(MAX_PAGES):
            offset = page * PAGE_SIZE
            data = _fetch_page(client, offset)
            items = data.get("items", [])
            if not isinstance(items, list):
                items = []

            pagination = data.get("pagination") or {}
            try:
                catalog_total = int(pagination.get("total"))
            except (TypeError, ValueError):
                pass

            scanned += len(items)
            for item in items:
                if not isinstance(item, dict):
                    continue
                haystack = _haystack(item)
                # Require a ProjectPermit-specific identifier. PAY_TO is printed for
                # verification but is deliberately not sufficient by itself because
                # one merchant can own multiple Bazaar resources.
                if (
                    MCP_DOMAIN.lower() in haystack
                    or HTTP_DOMAIN.lower() in haystack
                    or TOOL_NAME.lower() in haystack
                ):
                    matches.append(item)

            # Do not stop at the first match: an older http:// entry and a newer
            # canonical https:// entry can coexist and may be on different pages.
            if not items:
                break
            if catalog_total is not None and offset + len(items) >= catalog_total:
                break

    canonical_matches = [
        item
        for item in matches
        if str(item.get("resourceUrl") or "").rstrip("/") == CANONICAL_HTTP_URL
    ]

    print(f"facilitator={FACILITATOR}")
    print(f"pay_to={PAY_TO}")
    print(f"catalog_total={catalog_total if catalog_total is not None else 'unknown'}")
    print(f"catalog_scanned={scanned}")
    print(f"projectpermit_matches={len(matches)}")
    print(f"canonical_https_matches={len(canonical_matches)}")
    for item in matches[:10]:
        print("match=" + json.dumps(item, sort_keys=True))

    if not matches:
        print("projectpermit_bazaar=ABSENT")
        raise SystemExit(2)
    if not canonical_matches:
        print("projectpermit_bazaar=FOUND_STALE_NON_HTTPS_ONLY")
        raise SystemExit(3)

    print("projectpermit_bazaar=FOUND_CANONICAL_HTTPS")


if __name__ == "__main__":
    main()
