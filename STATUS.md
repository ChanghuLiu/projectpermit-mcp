# ProjectPermit Phase 0 Status

Updated: 2026-08-26

## Current state

**Phase 0 core + x402 paid MCP E2E: PASS.**

ProjectPermit is deployed as an evidence-linked, deterministic municipal permit preflight for Gatineau, Quebec and Ottawa, Ontario. The rules engine does not call an LLM and the payment layer is kept outside BuildRequirements.

## Completed

- Product boundary and conservative determination vocabulary locked
- Gatineau + Ottawa Phase 0 rules implemented
- 8 project families
- deterministic rules engine with official evidence and stable rule ids
- rule-version and property-overlay-aware results
- Ottawa official geocoder/GIS adapter
- Gatineau official municipal geocoder adapter
- FastAPI endpoint deployed publicly
- MCP Python SDK v2 Streamable HTTP server deployed publicly
- x402-native paid MCP tool deployed publicly
- official source manifest and source-change detector
- public request/response JSON schemas
- x402 v2 HTTP transport adapter
- Base Sepolia `eip155:84532` payment profile
- public payee configured without storing payer keys server-side
- no server-side LLM dependency
- no paid map/property-data dependency
- Docker + GitHub Actions CI
- MCP SDK v2 / x402 settlement-metadata compatibility bridge and regression test
- facilitator capability probe and Bazaar catalog lookup scripts

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP: Railway service `projectpermit-mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid permit preflight

Current test price: **$0.01 USDC per paid tool call** on Base Sepolia.

## Verification

The repository contains the deterministic golden corpus and automated tests. Current CI verifies:

- Python 3.11 and 3.13 core tests
- deterministic rule/schema/source contracts
- MCP v2 integration
- x402 wire behavior
- MCP v2 settlement-receipt metadata compatibility
- Docker build and live container `/health`
- public free MCP connection/tool invocation
- public paid MCP unpaid challenge
- facilitator capability matrix
- read-only Bazaar catalog state

A real buyer-side x402 MCP call has completed successfully through the public Railway service. Server logs independently confirmed successful facilitator `/verify` and `/settle` calls and the deterministic tool returned a real Ottawa preflight result.

## Bazaar canary

The x402.org public testnet facilitator remains a known-good Base Sepolia payment facilitator, but its public endpoint does not expose `/discovery/resources` or `/discovery/search`.

For the paid MCP Bazaar canary, `projectpermit-x402-mcp` is currently configured with:

`https://facilitator.goplausible.xyz`

Free capability probes confirmed that this facilitator:

- supports x402 v2 `exact` on Base Sepolia
- exposes `/discovery/resources`
- accepts the same paid MCP challenge shape used by ProjectPermit
- allows the ProjectPermit paid MCP service to initialize and serve its x402 challenge normally

The pre-settlement catalog snapshot reports **ProjectPermit absent**, which is expected before the first ProjectPermit settlement through this Bazaar-capable facilitator.

## Known unresolved items

1. **Bazaar indexing:** one final 0.01 Base Sepolia test-USDC MCP settlement through the current GoPlausible canary is required, followed by a read-only catalog lookup to prove indexing end to end.
2. **Gatineau PIIA/heritage:** public municipal mapping confirms the concept/layers, but a stable unauthenticated machine endpoint has not yet been locked. Unknown overlay state must never be mapped to `false`.
3. **Mainnet:** intentionally disabled until testnet plumbing and product-value validation are complete.

## Next gate

1. Perform exactly one paid MCP call through the current GoPlausible canary.
2. Confirm `/verify` and `/settle` in Railway logs.
3. Confirm ProjectPermit appears in the Bazaar `/discovery/resources` catalog and inspect its discovery metadata.
4. Mark Phase 0 release readiness complete if indexing succeeds.

No additional paid calls should be made merely for smoke testing unless a regression specifically requires them.
