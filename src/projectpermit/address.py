"""Address/overlay adapters for ProjectPermit.

Phase 0 deliberately uses municipal GIS/geocoding services instead of paid map APIs.
Network calls are dependency-injected so production can use httpx while tests remain deterministic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict
from urllib.parse import urlencode

JsonFetcher = Callable[[str], Dict[str, Any]]


@dataclass(frozen=True)
class ResolvedAddress:
    matched_address: str
    score: float
    x: float
    y: float
    spatial_reference: int = 4326


class ArcGISUrlBuilder:
    @staticmethod
    def geocode(base: str, address: str, out_sr: int = 4326, max_locations: int = 5) -> str:
        params = {
            "SingleLine": address,
            "f": "json",
            "outSR": out_sr,
            "maxLocations": max_locations,
        }
        return f"{base.rstrip('/')}/findAddressCandidates?{urlencode(params)}"

    @staticmethod
    def point_query(layer_url: str, x: float, y: float, in_sr: int = 4326, out_fields: str = "*") -> str:
        params = {
            "geometry": f"{x},{y}",
            "geometryType": "esriGeometryPoint",
            "inSR": in_sr,
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": out_fields,
            "returnGeometry": "false",
            "f": "json",
        }
        return f"{layer_url.rstrip('/')}/query?{urlencode(params)}"


def _best_candidate(payload: Dict[str, Any], minimum_score: float = 85.0) -> ResolvedAddress:
    candidates = payload.get("candidates") or []
    if not candidates:
        raise ValueError("No address candidate returned by municipal geocoder")
    best = max(candidates, key=lambda c: float(c.get("score", 0)))
    score = float(best.get("score", 0))
    if score < minimum_score:
        raise ValueError(f"Best municipal geocoder score {score} is below {minimum_score}")
    loc = best.get("location") or {}
    return ResolvedAddress(
        matched_address=best.get("address") or best.get("attributes", {}).get("Match_addr") or "",
        score=score,
        x=float(loc["x"]),
        y=float(loc["y"]),
    )


class OttawaAddressAdapter:
    GEOCODER = "https://maps.ottawa.ca/arcgis/rest/services/addressLocator/GeocodeServer"
    ZONING_2026 = "https://maps.ottawa.ca/arcgis/rest/services/Zoning_Bylaw_2026_50/MapServer"
    ZONING_2008 = "https://maps.ottawa.ca/arcgis/rest/services/Zoning/MapServer"

    def __init__(self, fetch_json: JsonFetcher):
        self.fetch_json = fetch_json

    def resolve(self, address: str) -> Dict[str, Any]:
        geocode_url = ArcGISUrlBuilder.geocode(self.GEOCODER, address)
        matched = _best_candidate(self.fetch_json(geocode_url))

        def query(layer_url: str):
            return self.fetch_json(ArcGISUrlBuilder.point_query(layer_url, matched.x, matched.y)).get("features") or []

        zoning_2026 = query(f"{self.ZONING_2026}/0")
        floodplain = query(f"{self.ZONING_2026}/1")
        under_appeal = query(f"{self.ZONING_2026}/7")
        heritage = query(f"{self.ZONING_2008}/1")
        zoning_2008 = query(f"{self.ZONING_2008}/3")

        def attrs(features):
            return [f.get("attributes", {}) for f in features]

        return {
            "jurisdiction": "ottawa_on",
            "address_resolution": {
                "matched_address": matched.matched_address,
                "score": matched.score,
                "longitude": matched.x,
                "latitude": matched.y,
                "source": self.GEOCODER,
            },
            "property": {
                "heritage": bool(heritage),
                "floodplain": bool(floodplain),
                "zoning_under_appeal": bool(under_appeal),
                "zoning_2026_features": attrs(zoning_2026),
                "zoning_2008_features": attrs(zoning_2008),
            },
            "evidence_sources": [self.GEOCODER, self.ZONING_2026, self.ZONING_2008],
        }


class GatineauAddressAdapter:
    """Gatineau municipal-geocoder adapter.

    The public ArcGIS Enterprise portal declares ComposVDG as its first-party geocoder.
    Phase 0 can geocode a civic address at zero paid-API cost. PIIA/heritage overlay
    extraction is kept separate because the public Géoportail exposes those layers, but
    their stable machine endpoints still need to be locked before production.
    """

    GEOCODER = "https://vportailgis.gatineau.ca/arcgis/rest/services/Communs/ComposVDG/GeocodeServer"

    def __init__(self, fetch_json: JsonFetcher):
        self.fetch_json = fetch_json

    def geocode(self, address: str) -> Dict[str, Any]:
        geocode_url = ArcGISUrlBuilder.geocode(self.GEOCODER, address)
        matched = _best_candidate(self.fetch_json(geocode_url))
        return {
            "jurisdiction": "gatineau_qc",
            "address_resolution": {
                "matched_address": matched.matched_address,
                "score": matched.score,
                "longitude": matched.x,
                "latitude": matched.y,
                "source": self.GEOCODER,
            },
            "property": {
                "piia": None,
                "heritage": None,
                "zoning_code": None,
                "overlay_resolution_status": "PENDING_STABLE_PUBLIC_LAYER_ENDPOINTS",
            },
            "evidence_sources": [self.GEOCODER],
        }
