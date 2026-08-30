"""Crawler-facing discovery documents for the public ProjectPermit API origin."""
from __future__ import annotations

from xml.sax.saxutils import escape

from .public_discovery import CITY_INTENT_PATHS


API_ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
PUBLIC_CRAWL_PATHS = (
    "/",
    "/llms.txt",
    "/docs",
    "/openapi.json",
    "/v1/capabilities",
    "/.well-known/agent.json",
    "/.well-known/x402",
    "/.well-known/x402-service.json",
    *CITY_INTENT_PATHS,
)


def robots_text() -> str:
    """Allow public discovery crawlers and advertise the canonical sitemap."""
    return f"User-agent: *\nAllow: /\nSitemap: {API_ORIGIN}/sitemap.xml\n"


def sitemap_xml() -> str:
    """Return a compact sitemap containing only useful public GET discovery resources."""
    urls = "".join(
        f"<url><loc>{escape(API_ORIGIN + path)}</loc></url>" for path in PUBLIC_CRAWL_PATHS
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}"
        "</urlset>"
    )
