from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from projectpermit.api import app
from projectpermit.public_discovery import API_ORIGIN, CITY_INTENT_PAGES, CITY_INTENT_PATHS, city_intent_html


class CityIntentDiscoveryTests(unittest.TestCase):
    def test_all_supported_city_pages_render_existing_coverage_only(self) -> None:
        self.assertEqual(len(CITY_INTENT_PAGES), 7)
        self.assertEqual(len(CITY_INTENT_PATHS), 7)
        for slug, page in CITY_INTENT_PAGES.items():
            html = city_intent_html(slug)
            city = str(page["name"])
            jurisdiction = str(page["jurisdiction"])
            self.assertIn(f"{city} building permit requirements API &amp; MCP", html)
            self.assertIn(jurisdiction, html)
            self.assertIn("/v1/preview-project-requirements", html)
            self.assertIn("official-source evidence", html)
            self.assertIn("does not claim complete coverage", html)
            self.assertIn(f'<link rel="canonical" href="{API_ORIGIN}/permit-requirements/{slug}">', html)

    def test_unknown_city_slug_is_not_a_discovery_page(self) -> None:
        with self.assertRaises(KeyError):
            city_intent_html("not-a-supported-city")

    def test_http_city_pages_are_public_and_unknown_slug_is_404(self) -> None:
        client = TestClient(app)
        response = client.get("/permit-requirements/ottawa-on")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ottawa building permit requirements API", response.text)

        missing = client.get("/permit-requirements/not-supported")
        self.assertEqual(missing.status_code, 404)

    def test_city_pages_are_in_public_sitemap(self) -> None:
        client = TestClient(app)
        sitemap = client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        for path in CITY_INTENT_PATHS:
            self.assertIn(f"<loc>{API_ORIGIN}{path}</loc>", sitemap.text)


if __name__ == "__main__":
    unittest.main()
