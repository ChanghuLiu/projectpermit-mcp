#!/usr/bin/env python3
"""Probe Ottawa's official 2026 permit ArcGIS item without emitting permit rows.

The purpose is source discovery for an address-premium prevalence audit. The
script prints only item/service/resource metadata; it never downloads or emits
permit records, civic addresses, applicant names, contractors or other row data.
"""
from __future__ import annotations

import json
from urllib.request import Request, urlopen


ITEM_ID = "429ea52d2ff040c799afde2b40b90f68"
BASE = f"https://www.arcgis.com/sharing/rest/content/items/{ITEM_ID}"


def fetch_json(url: str) -> object:
    req = Request(url, headers={"User-Agent": "ProjectPermit-research/1.0"})
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    item = fetch_json(f"{BASE}?f=json")
    resources = fetch_json(f"{BASE}/resources?f=json&num=100")

    if not isinstance(item, dict):
        raise SystemExit("unexpected ArcGIS item metadata shape")
    if not isinstance(resources, dict):
        raise SystemExit("unexpected ArcGIS resource listing shape")

    safe_item_keys = (
        "id",
        "title",
        "type",
        "typeKeywords",
        "size",
        "url",
        "access",
        "modified",
        "ownerFolder",
    )
    safe_item = {key: item.get(key) for key in safe_item_keys}

    safe_resources = []
    for resource in resources.get("resources") or []:
        if not isinstance(resource, dict):
            continue
        safe_resources.append(
            {
                "resource": resource.get("resource"),
                "size": resource.get("size"),
                "created": resource.get("created"),
            }
        )

    output = {
        "source": "City of Ottawa / ArcGIS Online public item",
        "item": safe_item,
        "resource_count": len(safe_resources),
        "resources": safe_resources,
        "notes": [
            "No permit rows were downloaded or emitted.",
            "If item.url is a FeatureServer/MapServer, the next audit can query schema/counts only before selecting a deterministic sample.",
            "If the item is file/resource based, a later audit must avoid bulk downloading unless a bounded monthly resource can be selected safely.",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
