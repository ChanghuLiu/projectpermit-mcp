from __future__ import annotations

import unittest

from projectpermit.crawler_discovery import API_ORIGIN, PUBLIC_CRAWL_PATHS, robots_text, sitemap_xml


class CrawlerDiscoveryTests(unittest.TestCase):
    def test_robots_allows_public_crawling_and_points_to_sitemap(self) -> None:
        text = robots_text()
        self.assertIn("User-agent: *", text)
        self.assertIn("Allow: /", text)
        self.assertIn(f"Sitemap: {API_ORIGIN}/sitemap.xml", text)
        self.assertNotIn("Disallow:", text)

    def test_sitemap_contains_only_public_get_discovery_resources(self) -> None:
        xml = sitemap_xml()
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        for path in PUBLIC_CRAWL_PATHS:
            self.assertIn(f"<loc>{API_ORIGIN}{path}</loc>", xml)
        self.assertNotIn("/v1/check-project-requirements</loc>", xml)
        self.assertNotIn("/v1/preview-project-requirements</loc>", xml)
        self.assertNotIn("/health</loc>", xml)

    def test_key_machine_discovery_documents_are_in_sitemap(self) -> None:
        self.assertIn("/.well-known/agent.json", PUBLIC_CRAWL_PATHS)
        self.assertIn("/.well-known/x402-service.json", PUBLIC_CRAWL_PATHS)
        self.assertIn("/openapi.json", PUBLIC_CRAWL_PATHS)
        self.assertIn("/llms.txt", PUBLIC_CRAWL_PATHS)


if __name__ == "__main__":
    unittest.main()
