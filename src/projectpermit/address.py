"""Address/overlay adapters for ProjectPermit.

ProjectPermit deliberately prefers municipal GIS/open-data services over paid map
APIs. Network calls are dependency-injected so production can use httpx while
unit tests remain deterministic.
"""
from __future__ import annotations

import re
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
    def point_query(
        layer_url: str,
        x: float,
        y: float,
        in_sr: int = 4326,
        out_fields: str = "*",
    ) -> str:
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

    @staticmethod
    def where_query(
        layer_url: str,
        where: str,
        out_fields: str = "*",
        return_geometry: bool = False,
        out_sr: int = 4326,
        result_record_count: int = 10,
    ) -> str:
        params = {
            "where": where,
            "outFields": out_fields,
            "returnGeometry": str(return_geometry).lower(),
            "outSR": out_sr,
            "resultRecordCount": result_record_count,
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


def _sql_quote(value: str) -> str:
    return value.replace("'", "''")


def _normalize_toronto_address(address: str) -> str:
    """Normalize common civic-address suffixes without pretending to geocode.

    Toronto's official Address Point layer exposes ADDRESS_FULL. We remove only
    locality/province/postal decorations supplied after a comma and normalize
    whitespace/case; the City dataset remains the authority for the match.
    """
    civic = address.split(",", 1)[0].strip().upper()
    civic = re.sub(r"\s+", " ", civic)
    return civic


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


class TorontoAddressAdapter:
    """Toronto civic-address + zoning/heritage adapter using first-party GIS layers.

    Toronto publishes an authorized Address Point layer with ADDRESS_FULL and WGS84
    longitude/latitude fields, plus a Zoning Property Summary polygon layer, Heritage
    District polygons and Heritage Register points. No paid geocoder is needed.

    Matching is deliberately exact after conservative locality/whitespace normalization.
    We fail closed instead of fuzzy-matching the wrong property.
    """

    ADDRESS_POINTS = "https://gis.toronto.ca/arcgis/rest/services/cot_geospatial27/FeatureServer/101"
    ZONING_PROPERTY = "https://gis.toronto.ca/arcgis/rest/services/cot_geospatial11/MapServer/18"
    HERITAGE_DISTRICT = "https://gis.toronto.ca/arcgis/rest/services/cot_geospatial11/MapServer/40"
    HERITAGE_REGISTER = "https://gis.toronto.ca/arcgis/rest/services/cot_geospatial11/MapServer/56"

    def __init__(self, fetch_json: JsonFetcher):
        self.fetch_json = fetch_json

    def resolve(self, address: str) -> Dict[str, Any]:
        normalized = _normalize_toronto_address(address)
        if not normalized or not re.match(r"^\d", normalized):
            raise ValueError("Toronto address must begin with a civic number")

        where = f"UPPER(ADDRESS_FULL) = '{_sql_quote(normalized)}'"
        address_url = ArcGISUrlBuilder.where_query(
            self.ADDRESS_POINTS,
            where,
            out_fields=(
                "ADDRESS_FULL,LONGITUDE,LATITUDE,GENERAL_USE,WARD,WARD_NAME,"
                "ADDRESS_POINT_ID,ADDRESS_STATUS"
            ),
            return_geometry=True,
            out_sr=4326,
            result_record_count=5,
        )
        address_features = self.fetch_json(address_url).get("features") or []
        if not address_features:
            raise ValueError(
                "No exact authorized Toronto Address Point match; use the City's canonical civic-address spelling"
            )
        if len(address_features) > 1:
            raise ValueError("Toronto civic address is ambiguous in the municipal Address Point layer")

        feature = address_features[0]
        attrs = feature.get("attributes") or {}
        geometry = feature.get("geometry") or {}
        longitude = attrs.get("LONGITUDE", geometry.get("x"))
        latitude = attrs.get("LATITUDE", geometry.get("y"))
        if longitude is None or latitude is None:
            raise ValueError("Toronto Address Point match did not include usable coordinates")
        longitude = float(longitude)
        latitude = float(latitude)

        def point_features(layer_url: str, out_fields: str = "*") -> list[dict[str, Any]]:
            payload = self.fetch_json(
                ArcGISUrlBuilder.point_query(
                    layer_url,
                    longitude,
                    latitude,
                    in_sr=4326,
                    out_fields=out_fields,
                )
            )
            return payload.get("features") or []

        zoning = point_features(
            self.ZONING_PROPERTY,
            "ADDRESS_F,ZN_STRING,HT_STRING,PA_STRING,RMH_STRING,CNV_STRING,GEO_ID",
        )
        heritage_district = point_features(self.HERITAGE_DISTRICT, "DISTRICT_NAME")

        heritage_where = f"UPPER(ADDRESS) = '{_sql_quote(normalized)}'"
        heritage_register = (
            self.fetch_json(
                ArcGISUrlBuilder.where_query(
                    self.HERITAGE_REGISTER,
                    heritage_where,
                    out_fields="ADDRESS,STATUS,STATUSCODE,BYLAW,DETAILS",
                    return_geometry=False,
                    result_record_count=10,
                )
            ).get("features")
            or []
        )

        def attrs_only(features: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [f.get("attributes") or {} for f in features]

        zoning_attrs = attrs_only(zoning)
        heritage_attrs = attrs_only(heritage_register)
        district_attrs = attrs_only(heritage_district)
        heritage = bool(heritage_attrs or district_attrs)

        return {
            "jurisdiction": "toronto_on",
            "address_resolution": {
                "matched_address": attrs.get("ADDRESS_FULL") or normalized,
                "score": 100.0,
                "longitude": longitude,
                "latitude": latitude,
                "ward": attrs.get("WARD"),
                "ward_name": attrs.get("WARD_NAME"),
                "general_use": attrs.get("GENERAL_USE"),
                "address_point_id": attrs.get("ADDRESS_POINT_ID"),
                "source": self.ADDRESS_POINTS,
            },
            "property": {
                "heritage": heritage,
                "zoning_code": zoning_attrs[0].get("ZN_STRING") if len(zoning_attrs) == 1 else None,
                "zoning_features": zoning_attrs,
                "heritage_register_features": heritage_attrs,
                "heritage_district_features": district_attrs,
            },
            "evidence_sources": [
                self.ADDRESS_POINTS,
                self.ZONING_PROPERTY,
                self.HERITAGE_DISTRICT,
                self.HERITAGE_REGISTER,
            ],
        }
