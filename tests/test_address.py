import unittest
from projectpermit.address import (
    ArcGISUrlBuilder,
    OttawaAddressAdapter,
    GatineauAddressAdapter,
    TorontoAddressAdapter,
)


class AddressAdapterTest(unittest.TestCase):
    def test_url_builder(self):
        url = ArcGISUrlBuilder.geocode("https://example.test/GeocodeServer", "110 Laurier Ave W")
        self.assertIn("findAddressCandidates", url)
        self.assertIn("110+Laurier+Ave+W", url)

        where_url = ArcGISUrlBuilder.where_query(
            "https://example.test/FeatureServer/0",
            "UPPER(ADDRESS_FULL) = '100 QUEEN ST W'",
            return_geometry=True,
        )
        self.assertIn("where=", where_url)
        self.assertIn("returnGeometry=true", where_url)

    def test_ottawa_adapter_parses_layers(self):
        calls = []

        def fake(url):
            calls.append(url)
            if "findAddressCandidates" in url:
                return {"candidates": [{"address": "110 LAURIER AVE W", "score": 99, "location": {"x": -75.69, "y": 45.42}}]}
            if "/MapServer/1/query" in url and "Zoning_Bylaw_2026_50" in url:
                return {"features": []}
            if "/MapServer/7/query" in url:
                return {"features": [{"attributes": {"ZONE_CODE": "*_N4"}}]}
            if "/Zoning/MapServer/1/query" in url:
                return {"features": [{"attributes": {"NAME_EN": "Heritage"}}]}
            if "/Zoning/MapServer/3/query" in url:
                return {"features": [{"attributes": {"ZONE_CODE": "R4"}}]}
            if "/Zoning_Bylaw_2026_50/MapServer/0/query" in url:
                return {"features": [{"attributes": {"ZONE_CODE": "N4"}}]}
            return {"features": []}

        out = OttawaAddressAdapter(fake).resolve("110 Laurier Ave W")
        self.assertEqual("ottawa_on", out["jurisdiction"])
        self.assertTrue(out["property"]["heritage"])
        self.assertTrue(out["property"]["zoning_under_appeal"])
        self.assertFalse(out["property"]["floodplain"])
        self.assertGreaterEqual(len(calls), 6)

    def test_gatineau_geocoder_keeps_unknown_overlays_unknown(self):
        def fake(url):
            return {"candidates": [{"address": "25 RUE LAURIER", "score": 96, "location": {"x": -75.72, "y": 45.43}}]}

        out = GatineauAddressAdapter(fake).geocode("25 rue Laurier")
        self.assertEqual("gatineau_qc", out["jurisdiction"])
        self.assertIsNone(out["property"]["piia"])
        self.assertIsNone(out["property"]["heritage"])
        self.assertEqual(96, out["address_resolution"]["score"])

    def test_toronto_adapter_uses_official_address_zoning_and_heritage_layers(self):
        calls = []

        def fake(url):
            calls.append(url)
            if "cot_geospatial27/FeatureServer/101/query" in url:
                return {
                    "features": [{
                        "attributes": {
                            "ADDRESS_FULL": "100 QUEEN ST W",
                            "LONGITUDE": -79.3832,
                            "LATITUDE": 43.6532,
                            "GENERAL_USE": "Civic",
                            "WARD": "10",
                            "WARD_NAME": "Spadina-Fort York",
                            "ADDRESS_POINT_ID": 123,
                        },
                        "geometry": {"x": -79.3832, "y": 43.6532},
                    }]
                }
            if "cot_geospatial11/MapServer/18/query" in url:
                return {"features": [{"attributes": {"ADDRESS_F": "100 QUEEN ST W", "ZN_STRING": "CR 6.0"}}]}
            if "cot_geospatial11/MapServer/40/query" in url:
                return {"features": []}
            if "cot_geospatial11/MapServer/56/query" in url:
                return {"features": [{"attributes": {"ADDRESS": "100 QUEEN ST W", "STATUS": "Part IV"}}]}
            return {"features": []}

        out = TorontoAddressAdapter(fake).resolve("100 Queen St W, Toronto, ON")
        self.assertEqual("toronto_on", out["jurisdiction"])
        self.assertEqual("100 QUEEN ST W", out["address_resolution"]["matched_address"])
        self.assertEqual(100.0, out["address_resolution"]["score"])
        self.assertEqual("CR 6.0", out["property"]["zoning_code"])
        self.assertTrue(out["property"]["heritage"])
        self.assertEqual(4, len(calls))
        self.assertTrue(any("UPPER%28ADDRESS_FULL%29" in url for url in calls))

    def test_toronto_adapter_fails_closed_on_no_exact_address(self):
        def fake(url):
            return {"features": []}

        with self.assertRaises(ValueError):
            TorontoAddressAdapter(fake).resolve("100 Imaginary St, Toronto, ON")


if __name__ == "__main__":
    unittest.main()
