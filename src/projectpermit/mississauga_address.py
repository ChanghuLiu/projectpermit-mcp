"""Mississauga address/property adapter using first-party City ArcGIS services."""
from __future__ import annotations

import re
from typing import Any, Dict

from .address import ArcGISUrlBuilder, JsonFetcher


def _sql_quote(value: str) -> str:
    return value.replace("'", "''")


def _normalize_address(address: str) -> str:
    civic = address.split(",", 1)[0].strip().upper()
    return re.sub(r"\s+", " ", civic)


class MississaugaAddressAdapter:
    """Resolve a Mississauga civic address and public zoning/heritage overlays.

    The City publishes an Address FeatureServer with FULLNAME, CITY_PIN, ward and
    WGS84 latitude/longitude, a citywide Zoning By-law polygon layer, and a City
    Heritage Properties layer. Matching is exact after locality/whitespace
    normalization; ambiguous or absent matches fail closed.
    """

    ADDRESS = "https://services6.arcgis.com/hM5ymMLbxIyWTjn2/ArcGIS/rest/services/Address/FeatureServer/0"
    ZONING = "https://services6.arcgis.com/hM5ymMLbxIyWTjn2/ArcGIS/rest/services/Mississauga_Zoning_Bylaw/FeatureServer/0"
    HERITAGE = "https://services6.arcgis.com/hM5ymMLbxIyWTjn2/ArcGIS/rest/services/City_Heritage_Properties/FeatureServer/5"
    PROPERTY = "https://services6.arcgis.com/hM5ymMLbxIyWTjn2/ArcGIS/rest/services/Property_Search/FeatureServer/0"

    def __init__(self, fetch_json: JsonFetcher):
        self.fetch_json = fetch_json

    def resolve(self, address: str) -> Dict[str, Any]:
        normalized = _normalize_address(address)
        if not normalized or not re.match(r"^\d", normalized):
            raise ValueError("Mississauga address must begin with a civic number")

        where = f"UPPER(FULLNAME) = '{_sql_quote(normalized)}'"
        address_url = ArcGISUrlBuilder.where_query(
            self.ADDRESS,
            where,
            out_fields="ADDR_ID,STNO,UNIT_NO,STNAME,SUFFIX,DIRECTION,FULLNAME,CITY_PIN,WARD,LATITUDE,LONGITUDE",
            return_geometry=True,
            out_sr=4326,
            result_record_count=5,
        )
        matches = self.fetch_json(address_url).get("features") or []
        if not matches:
            raise ValueError(
                "No exact Mississauga municipal Address match; use the City's canonical civic-address spelling"
            )
        if len(matches) > 1:
            # Unit-level duplicates can share a civic FULLNAME. Without an explicit unit,
            # selecting one would silently attach the wrong property context.
            raise ValueError("Mississauga civic address is ambiguous in the municipal Address layer")

        feature = matches[0]
        attrs = feature.get("attributes") or {}
        geometry = feature.get("geometry") or {}
        longitude = attrs.get("LONGITUDE", geometry.get("x"))
        latitude = attrs.get("LATITUDE", geometry.get("y"))
        if longitude is None or latitude is None:
            raise ValueError("Mississauga Address match did not include usable coordinates")
        longitude = float(longitude)
        latitude = float(latitude)

        def point_features(layer: str, out_fields: str = "*") -> list[dict[str, Any]]:
            response = self.fetch_json(
                ArcGISUrlBuilder.point_query(
                    layer,
                    longitude,
                    latitude,
                    in_sr=4326,
                    out_fields=out_fields,
                )
            )
            return response.get("features") or []

        zoning = point_features(
            self.ZONING,
            "ZONE_CODE,ZONE_DESCRIPTION,ZONE_CATEGORY,GREENLANDS_OVERLAY,BYLAW,ZAREA,BASE_ZONE_DESIGNATION,EXCEPTION_ZONE_NUMBER,EXCEPTION_ZONE_DESIGNATION,HOLDING_PROVISION,SUB_ZONING_DESIGNATION",
        )
        heritage = point_features(self.HERITAGE, "*")

        city_pin = attrs.get("CITY_PIN")
        parcel_features: list[dict[str, Any]] = []
        if city_pin is not None:
            parcel_where = f"CITY_PIN = {int(city_pin)}"
            parcel_features = (
                self.fetch_json(
                    ArcGISUrlBuilder.where_query(
                        self.PROPERTY,
                        parcel_where,
                        out_fields="CITY_PIN,ROLL_NO,TERA_PIN",
                        return_geometry=False,
                        result_record_count=5,
                    )
                ).get("features")
                or []
            )

        def attrs_only(features: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [f.get("attributes") or {} for f in features]

        zoning_attrs = attrs_only(zoning)
        heritage_attrs = attrs_only(heritage)
        parcel_attrs = attrs_only(parcel_features)

        # More than one zoning polygon can legitimately intersect a parcel boundary.
        # Only emit one zoning_code when the result is unambiguous.
        zone_codes = {
            str(item.get("ZONE_CODE"))
            for item in zoning_attrs
            if item.get("ZONE_CODE") not in (None, "")
        }

        return {
            "jurisdiction": "mississauga_on",
            "address_resolution": {
                "matched_address": attrs.get("FULLNAME") or normalized,
                "score": 100.0,
                "longitude": longitude,
                "latitude": latitude,
                "city_pin": city_pin,
                "ward": attrs.get("WARD"),
                "address_id": attrs.get("ADDR_ID"),
                "source": self.ADDRESS,
            },
            "property": {
                "heritage": bool(heritage_attrs),
                "zoning_code": next(iter(zone_codes)) if len(zone_codes) == 1 else None,
                "zoning_features": zoning_attrs,
                "heritage_features": heritage_attrs,
                "parcel_features": parcel_attrs,
            },
            "evidence_sources": [self.ADDRESS, self.ZONING, self.HERITAGE, self.PROPERTY],
        }
