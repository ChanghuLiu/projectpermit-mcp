# ProjectPermit Phase 0 Status

Updated: 2026-08-26

## Completed

- Product boundary and conservative determination vocabulary locked
- Gatineau + Ottawa Phase 0 rules implemented
- deterministic rules engine with official evidence and stable rule ids
- Ottawa official geocoder/GIS adapter
- Gatineau official municipal geocoder adapter
- FastAPI endpoint
- MCP Python SDK v2 server source
- official source manifest and source-change detector
- public request/response JSON schemas
- x402 v2 FastAPI transport adapter
- Base Sepolia public test profile configured for `eip155:84532`
- no server-side LLM dependency
- no paid map/property-data dependency
- Dockerfile and GitHub Actions CI

## Verification

The full development artifact contains a 97-case golden corpus and 20 passing local automated tests. The public repository additionally runs API, GIS-adapter, x402-config, source-manifest/source-watch, MCP-wiring and JSON-schema contract tests on Python 3.11 and 3.13, plus an optional MCP/x402 dependency smoke job.

## Known unresolved items

1. Gatineau PIIA/heritage: public Geoportal confirms the layers, but a stable unauthenticated machine endpoint has not yet been locked. Unknown overlay state must never be mapped to `false`.
2. A live internet deployment is still required for end-to-end Ottawa/Gatineau GIS calls.
3. Base Sepolia x402 settlement still needs a live public deployment and a buyer-side test payment.
4. Mainnet payment is intentionally blocked until testnet and product-value validation pass.

## Next gate

- obtain a public deployment URL
- live-test `/health`
- live-test Ottawa and Gatineau municipal GIS resolution
- verify unpaid request returns HTTP 402 when x402 is enabled
- complete a Base Sepolia paid retry and validate settlement response
- only then consider Bazaar discovery and additional municipalities
