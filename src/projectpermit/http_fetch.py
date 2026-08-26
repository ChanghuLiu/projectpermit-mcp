from __future__ import annotations

import logging

import httpx

# Municipal geocoder/GIS URLs can contain civic numbers or coordinates in query
# parameters. Keep transport diagnostics below INFO so production logs do not
# persist those request URLs. Application telemetry is emitted separately from
# projectpermit.telemetry and deliberately excludes raw location data.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def fetch_json(url: str):
    with httpx.Client(timeout=15.0, headers={"User-Agent": "ProjectPermit/0.4"}) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(f"Municipal GIS error: {data['error']}")
        return data
