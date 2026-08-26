import unittest
from projectpermit.address import ArcGISUrlBuilder, OttawaAddressAdapter, GatineauAddressAdapter


class AddressAdapterTest(unittest.TestCase):
    def test_url_builder(self):
        url = ArcGISUrlBuilder.geocode("https://example.test/GeocodeServer", "110 Laurier Ave W")
        self.assertIn("findAddressCandidates", url)
        self.assertIn("110+Laurier+Ave+W", url)

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


if __name__ == "__main__":
    unittest.main()
