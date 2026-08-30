"""Human- and agent-readable public discovery pages for the hosted API origin."""
from __future__ import annotations

from html import escape

from .openapi_discovery import discovery_settings


API_ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
FREE_MCP_URL = "https://projectpermit-mcp-production.up.railway.app/mcp"
PAID_MCP_URL = "https://projectpermit-x402-mcp-production.up.railway.app/mcp"
REPOSITORY_URL = "https://github.com/ChanghuLiu/projectpermit-mcp"
JURISDICTIONS = (
    "Gatineau",
    "Ottawa",
    "Toronto",
    "Mississauga",
    "Laval",
    "Longueuil",
    "Vancouver",
)
CITY_INTENT_PAGES = {
    "gatineau-qc": {"name": "Gatineau", "jurisdiction": "gatineau_qc", "region": "Quebec"},
    "ottawa-on": {"name": "Ottawa", "jurisdiction": "ottawa_on", "region": "Ontario"},
    "toronto-on": {"name": "Toronto", "jurisdiction": "toronto_on", "region": "Ontario"},
    "mississauga-on": {"name": "Mississauga", "jurisdiction": "mississauga_on", "region": "Ontario"},
    "laval-qc": {"name": "Laval", "jurisdiction": "laval_qc", "region": "Quebec"},
    "longueuil-qc": {"name": "Longueuil", "jurisdiction": "longueuil_qc", "region": "Quebec"},
    "vancouver-bc": {"name": "Vancouver", "jurisdiction": "vancouver_bc", "region": "British Columbia"},
}
CITY_INTENT_PATHS = tuple(f"/permit-requirements/{slug}" for slug in CITY_INTENT_PAGES)


def _single_price() -> str:
    return discovery_settings()["single_amount"]


def _city_links() -> str:
    return ", ".join(
        f'<a href="/permit-requirements/{slug}">{escape(str(page["name"]))}</a>'
        for slug, page in CITY_INTENT_PAGES.items()
    )


def landing_html() -> str:
    price = escape(_single_price())
    city_links = _city_links()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ProjectPermit — Building Permit Requirements API & MCP</title>
  <meta name="description" content="Building permit requirements API and MCP for contractors and AI agents. Check renovation and construction permit requirements across 7 Canadian municipalities with official-source evidence.">
  <meta name="keywords" content="building permit API, renovation permit check, municipal permit requirements, contractor permit preflight, construction permit API, building permit MCP, AI agent tools, Toronto building permit, Ottawa renovation permit, Vancouver building permit">
</head>
<body>
  <main>
    <h1>ProjectPermit</h1>
    <p><strong>Building permit requirements API &amp; MCP for contractors and AI agents.</strong></p>
    <p>Check proposed renovation and construction scope against deterministic municipal rules with official-source evidence, workflow routing, evidence freshness, and an automation-ready action bundle.</p>
    <h2>Coverage</h2>
    <p>{city_links}. Eight normalized project families are supported. Address/GIS resolution is available in Gatineau, Ottawa, Toronto, Mississauga, and Vancouver.</p>
    <h2>Try free</h2>
    <ul>
      <li><a href="/docs">Interactive API docs</a></li>
      <li><code>POST /v1/preview-project-requirements</code> — free, no account, API key, or wallet</li>
      <li><a href="{FREE_MCP_URL}">Free MCP developer preview</a></li>
      <li><a href="/v1/capabilities">Machine-readable capabilities</a></li>
      <li><a href="/openapi.json">OpenAPI discovery</a></li>
    </ul>
    <h2>Commercial x402</h2>
    <p>Full ProjectPermit preflight: <strong>${price} USDC / call</strong> on Base mainnet via x402.</p>
    <ul>
      <li><code>POST /v1/check-project-requirements</code></li>
      <li><a href="{PAID_MCP_URL}">Paid x402 MCP</a></li>
    </ul>
    <p><a href="{REPOSITORY_URL}">GitHub / integration documentation</a></p>
    <p><small>Preflight information only; not municipal authorization, legal advice, engineering certification, or building-code design approval.</small></p>
  </main>
</body>
</html>"""


def city_intent_html(city_slug: str) -> str:
    page = CITY_INTENT_PAGES.get(city_slug)
    if page is None:
        raise KeyError(city_slug)

    city = escape(str(page["name"]))
    region = escape(str(page["region"]))
    jurisdiction = escape(str(page["jurisdiction"]))
    canonical = f"{API_ORIGIN}/permit-requirements/{escape(city_slug)}"
    price = escape(_single_price())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{city} Building Permit Requirements API &amp; MCP — ProjectPermit</title>
  <meta name="description" content="Check proposed renovation and construction permit requirements in {city}, {region} with deterministic ProjectPermit rules, official-source evidence, freshness metadata, API and MCP access.">
  <meta name="keywords" content="{city} building permit requirements, {city} renovation permit, {city} building permit API, {city} contractor permit preflight, {city} permit MCP">
  <link rel="canonical" href="{canonical}">
</head>
<body>
  <main>
    <p><a href="/">ProjectPermit</a> / {city}</p>
    <h1>{city} building permit requirements API &amp; MCP</h1>
    <p>ProjectPermit provides a deterministic preflight for proposed renovation and construction scope in <strong>{city}, {region}</strong>, using the existing jurisdiction-specific ruleset and official-source evidence.</p>
    <p>Normalized project inputs cover common renovation and construction families such as window/door work, interior renovation, basements, dwelling changes, decks/porches, accessory structures, additions, and kitchen/bath plumbing.</p>
    <h2>Try the current {city} rules free</h2>
    <p>Use jurisdiction id <code>{jurisdiction}</code> with <code>POST /v1/preview-project-requirements</code>. The preview requires no account, API key, or wallet and does not perform civic-address/GIS resolution.</p>
    <ul>
      <li><a href="/docs">Interactive API docs</a></li>
      <li><a href="/v1/capabilities">Machine-readable coverage and capabilities</a></li>
      <li><a href="/openapi.json">OpenAPI specification</a></li>
      <li><a href="{FREE_MCP_URL}">Free MCP developer preview</a></li>
    </ul>
    <h2>Commercial workflow</h2>
    <p>The full preflight is currently <strong>${price} USDC / call</strong> on Base mainnet via x402 and can return official-source evidence, freshness, workflow routing, decision identity/change metadata, and an automation-ready action bundle.</p>
    <p><small>This page describes ProjectPermit's current software coverage. It does not claim complete coverage of every bylaw, code, approval or site condition and is not municipal authorization, legal advice, engineering certification, or building-code design approval. Confirm project-critical requirements with the applicable authority and professionals.</small></p>
  </main>
</body>
</html>"""


def llms_text() -> str:
    price = _single_price()
    cities = ", ".join(JURISDICTIONS)
    city_pages = "\n".join(
        f"- {page['name']}: {API_ORIGIN}/permit-requirements/{slug}"
        for slug, page in CITY_INTENT_PAGES.items()
    )
    return f"""# ProjectPermit

> Building permit requirements API & MCP for contractors and AI agents.

ProjectPermit checks proposed renovation and construction scope against deterministic municipal rules and returns official-source evidence, workflow routing, evidence freshness, decision identity/change metadata, and an automation-ready action bundle.

## Coverage

Jurisdictions: {cities}.
Project families: 8 normalized construction/renovation families.
Address/GIS resolution: Gatineau, Ottawa, Toronto, Mississauga, Vancouver.

Jurisdiction discovery pages:
{city_pages}

## Free discovery and validation

- Capabilities: {API_ORIGIN}/v1/capabilities
- OpenAPI: {API_ORIGIN}/openapi.json
- API docs: {API_ORIGIN}/docs
- Free HTTP preview: POST {API_ORIGIN}/v1/preview-project-requirements
- Free MCP: {FREE_MCP_URL}

The free HTTP preview requires no account, API key, or wallet and intentionally excludes civic-address/GIS resolution.

## Commercial x402

- Full paid HTTP preflight: POST {API_ORIGIN}/v1/check-project-requirements
- Launch price: ${price} USDC per full preflight
- Network: Base mainnet (eip155:8453)
- Payment protocol: x402 v2, exact scheme
- Paid MCP: {PAID_MCP_URL}

Runtime HTTP 402 payment requirements are authoritative.

## Search intents

building permit API; renovation permit check; municipal permit requirements; contractor permit preflight; construction permit API; building permit MCP; permit requirements MCP; Toronto building permit; Ottawa renovation permit; Vancouver building permit; AI agent permit tool.

## Source and integration docs

- Repository: {REPOSITORY_URL}
- Official MCP Registry name: io.github.ChanghuLiu/projectpermit

ProjectPermit is a preflight information service, not a municipality, permit issuer, lawyer, architect, or engineer.
"""
