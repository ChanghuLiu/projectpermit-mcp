from __future__ import annotations
import httpx


def fetch_json(url: str):
    with httpx.Client(timeout=15.0, headers={"User-Agent": "ProjectPermit/phase0"}) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(f"ArcGIS error: {data['error']}")
        return data
