"""City of Vancouver open-data address, zoning and heritage adapter.

Uses only first-party Vancouver Open Data Explore API endpoints. The adapter first
resolves an exact civic-number/street match, then queries the zoning polygon at that
point and checks the heritage register by civic address. No paid map/property API is
required.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Dict
from urllib.parse import urlencode

JsonFetcher = Callable[[str], Dict[str, Any]]


API_ROOT = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets"


_ABBREVIATIONS = {
    "AVENUE": "AV",
    "AVE": "AV",
    "STREET": "ST",
    "ROAD": "RD",
    "DRIVE": "DR",
    "BOULEVARD": "BLVD",
    "PLACE": "PL",
    "LANE": "LANE",
    "COURT": "CT",
    "CRESCENT": "CR",
    "TERRACE": "TERR",
    "WEST": "W",
    "EAST": "E",
    "NORTH": "N",
    "SOUTH": "S",
}


def _normalize_street(value: str) -> str:
    text = value.upper().replace(".", " ").replace(",", " ")
    tokens = [token for token in re.split(r"\s+", text.strip()) if token]
    normalized = [_ABBREVIATIONS.get(token, token) for token in tokens]
    return " ".join(normalized)


def _split_civic_address(address: str) -> tuple[str, str]:
    text = address.strip()
    # Drop a conventional unit prefix such as #201-453 or 201-453 when present.
    text = re.sub(r"^#?\w+\s*-\s*(?=\d)", "", text)
    match = re.match(r"^(\d+[A-Za-z]?)\s+(.+)$", text)
    if not match:
        raise ValueError("Vancouver address must start with a civic number")
    civic = match.group(1).upper()
    street_part = match.group(2).split(",", 1)[0].strip()
    return civic, _normalize_street(street_part)


def _records_url(dataset: str, *, where: str, limit: int = 100) -> str:
    params = {"where": where, "limit": str(limit)}
    return f"{API_ROOT}/{dataset}/records?{urlencode(params)}"


def _point_from_record(record: dict[str, Any]) -> tuple[float, float]:
    point = record.get("geo_point_2d") or {}
    if point.get("lon") is not None and point.get("lat") is not None:
        return float(point["lon"]), float(point["lat"])
    geom = record.get("geom") or {}
    geometry = geom.get("geometry") if geom.get("type") == "Feature" else geom
    coords = (geometry or {}).get("coordinates") or []
    if len(coords) >= 2:
        return float(coords[0]), float(coords[1])
    raise ValueError("Vancouver address record did not contain coordinates")


class VancouverAddressAdapter:
    ADDRESS_DATASET = "property-addresses"
    ZONING_DATASET = "zoning-districts-and-labels"
    HERITAGE_DATASET = "heritage-sites"

    ADDRESS_SOURCE = f"https://opendata.vancouver.ca/explore/dataset/{ADDRESS_DATASET}/"
    ZONING_SOURCE = f"https://opendata.vancouver.ca/explore/dataset/{ZONING_DATASET}/"
    HERITAGE_SOURCE = f"https://opendata.vancouver.ca/explore/dataset/{HERITAGE_DATASET}/"

    def __init__(self, fetch_json: JsonFetcher):
        self.fetch_json = fetch_json

    def resolve(self, address: str) -> dict[str, Any]:
        civic, input_street = _split_civic_address(address)

        address_url = _records_url(
            self.ADDRESS_DATASET,
            where=f"civic_number='{civic}'",
            limit=100,
        )
        records = self.fetch_json(address_url).get("results") or []
        matches = [
            record
            for record in records
            if _normalize_street(str(record.get("std_street") or "")) == input_street
        ]
        if not matches:
            raise ValueError("No exact Vancouver property-address match returned by City open data")

        # Multiple records can legitimately share a displayed address. They should
        # resolve to the same or adjacent parcel point; use the first exact street match.
        matched = matches[0]
        lon, lat = _point_from_record(matched)
        matched_address = f"{civic} {matched.get('std_street') or input_street}".strip()

        point_literal = f"GEOM'POINT({lon} {lat})'"
        zoning_url = _records_url(
            self.ZONING_DATASET,
            where=f"within_distance(geom, {point_literal}, 1 m)",
            limit=20,
        )
        zoning_records = self.fetch_json(zoning_url).get("results") or []

        heritage_url = _records_url(
            self.HERITAGE_DATASET,
            where=f"streetnumber='{civic}'",
            limit=100,
        )
        heritage_records = self.fetch_json(heritage_url).get("results") or []
        heritage_matches = [
            record
            for record in heritage_records
            if _normalize_street(str(record.get("streetname") or "")) == input_street
            and str(record.get("status") or "").strip().lower() != "inactive"
        ]

        zoning_codes = [
            str(record.get("zoning_district"))
            for record in zoning_records
            if record.get("zoning_district")
        ]

        return {
            "jurisdiction": "vancouver_bc",
            "address_resolution": {
                "matched_address": matched_address,
                "score": 100.0,
                "longitude": lon,
                "latitude": lat,
                "source": self.ADDRESS_SOURCE,
                "site_id": matched.get("site_id"),
                "parcel_id": matched.get("p_parcel_id"),
            },
            "property": {
                "heritage": bool(heritage_matches),
                "zoning_code": zoning_codes[0] if zoning_codes else None,
                "zoning_features": zoning_records,
                "heritage_features": heritage_matches,
                "geo_local_area": matched.get("geo_local_area"),
            },
            "evidence_sources": [
                self.ADDRESS_SOURCE,
                self.ZONING_SOURCE,
                self.HERITAGE_SOURCE,
            ],
        }
