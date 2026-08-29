from __future__ import annotations

import json
from urllib.request import Request, urlopen


ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
SINGLE_RESOURCE = f"{ORIGIN}/v1/check-project-requirements"
BATCH_RESOURCE = f"{ORIGIN}/v1/check-project-requirements-batch"


def _get(path: str) -> tuple[str, str]:
    request = Request(
        ORIGIN + path,
        headers={"User-Agent": "ProjectPermit-Remote-Crawler-Smoke/1.0"},
        method="GET",
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"{path} returned HTTP {response.status}")
        content_type = response.headers.get("Content-Type", "")
        return content_type, response.read().decode("utf-8")


def main() -> None:
    robots_type, robots = _get("/robots.txt")
    if not robots_type.startswith("text/plain"):
        raise RuntimeError(f"unexpected robots content type: {robots_type!r}")
    expected_sitemap = f"Sitemap: {ORIGIN}/sitemap.xml"
    for required in ("User-agent: *", "Allow: /", expected_sitemap):
        if required not in robots:
            raise RuntimeError(f"robots.txt missing {required!r}")
    if "Disallow:" in robots:
        raise RuntimeError("robots.txt unexpectedly disallows crawling")

    sitemap_type, sitemap = _get("/sitemap.xml")
    if not sitemap_type.startswith("application/xml"):
        raise RuntimeError(f"unexpected sitemap content type: {sitemap_type!r}")
    required_paths = (
        "/",
        "/llms.txt",
        "/docs",
        "/openapi.json",
        "/v1/capabilities",
        "/.well-known/agent.json",
        "/.well-known/x402",
        "/.well-known/x402-service.json",
    )
    for path in required_paths:
        url = ORIGIN + path
        if f"<loc>{url}</loc>" not in sitemap:
            raise RuntimeError(f"sitemap missing {url}")

    for forbidden in (
        "/v1/check-project-requirements</loc>",
        "/v1/preview-project-requirements</loc>",
        "/health</loc>",
    ):
        if forbidden in sitemap:
            raise RuntimeError(f"sitemap unexpectedly includes {forbidden!r}")

    x402_type, x402_text = _get("/.well-known/x402")
    if not x402_type.startswith("application/json"):
        raise RuntimeError(f"unexpected x402 well-known content type: {x402_type!r}")
    x402_payload = json.loads(x402_text)
    expected_x402 = {
        "version": 1,
        "resources": [SINGLE_RESOURCE, BATCH_RESOURCE],
    }
    if x402_payload != expected_x402:
        raise RuntimeError(f"unexpected x402 well-known payload: {x402_payload!r}")

    print("production_crawler_discovery=PASS")
    print("production_x402_well_known=PASS")


if __name__ == "__main__":
    main()
