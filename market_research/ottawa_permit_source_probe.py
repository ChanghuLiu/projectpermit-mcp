#!/usr/bin/env python3
"""Probe Ottawa's official 2026 permit ArcGIS item without emitting permit rows.

The purpose is source discovery for an address-premium prevalence audit. The
script prints only item/service/resource metadata or ArcGIS public error codes;
it never downloads or emits permit records, civic addresses, applicant names,
contractors or other row data.
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


def safe_error(payload: dict) -> dict | None:
    error = payload.get("error")
    if not isinstance(error, dict):
        return None
    return {
        "code": error.get("code"),
        "message": error.get("message"),
        "details": error.get("details"),
    }


def main() -> None:
    item_json = fetch_json(f"{BASE}?f=json")
    item_pjson = fetch_json(f"{BASE}?f=pjson")
    resources = fetch_json(f"{BASE}/resources?f=json&num=100")

    for label, payload in (("item_json", item_json), ("item_pjson", item_pjson), ("resources", resources)):
        if not isinstance(payload, dict):
            raise SystemExit(f"unexpected ArcGIS {label} shape")

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
    safe_item = {key: item_json.get(key) for key in safe_item_keys}

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
        "item_json_error": safe_error(item_json),
        "item_pjson_error": safe_error(item_pjson),
        "resources_error": safe_error(resources),
        "resource_count": len(safe_resources),
        "resources": safe_resources,
        "notes": [
            "No permit rows were downloaded or emitted.",
            "ArcGIS public error code/message is retained when metadata lookup fails; this is source-discovery evidence, not permit data.",
            "If item.url is a FeatureServer/MapServer, the next audit can query schema/counts only before selecting a deterministic sample.",
            "If the item is file/resource based, a later audit must avoid bulk downloading unless a bounded monthly resource can be selected safely.",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
