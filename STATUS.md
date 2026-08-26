# ProjectPermit Phase 0 Status

Updated: 2026-08-26

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

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
- GoPlausible Bazaar indexing proven end to end
- canonical HTTPS Bazaar resource URL proven after settlement

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP: Railway service `projectpermit-mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid permit preflight

Current test price: **$0.01 USDC per paid tool/API call** on Base Sepolia.

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
- public HTTP Bazaar unpaid challenge
- facilitator capability matrix
- read-only Bazaar catalog state, including canonical HTTPS listing

Real buyer-side x402 calls have completed successfully through the public Railway services. Server logs independently confirmed the expected `402 -> 200` HTTP flow and successful facilitator verification/settlement. The deterministic engine returned the expected Ottawa preflight result.

Final canonical-HTTPS HTTP settlement transaction:

`0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`

## Bazaar result

The x402.org public testnet facilitator remains a known-good Base Sepolia payment facilitator, but its public endpoint does not expose the Bazaar listing endpoints used by this canary.

For Bazaar discovery, ProjectPermit uses:

`https://facilitator.goplausible.xyz`

The final read-only catalog verification reports:

- catalog total: **1682**
- ProjectPermit matches: **2**
- canonical HTTPS matches: **1**
- canonical resource: `https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`
- method: `POST`
- price: `10000` USDC atomic units = **$0.01 test USDC**
- network: `eip155:84532`
- scheme: `exact`
- canonical listing `settleCount`: **1**
- status: **`FOUND_CANONICAL_HTTPS`**

A stale pre-fix `http://` catalog row also remains in the external facilitator catalog. It is not the canonical ProjectPermit resource and is retained by the facilitator as historical discovery state; the canonical HTTPS row is present and is the release gate.

## Known unresolved items

1. **Gatineau PIIA/heritage:** public municipal mapping confirms the concept/layers, but a stable unauthenticated machine endpoint has not yet been locked. Unknown overlay state must never be mapped to `false`.
2. **Mainnet:** intentionally disabled until testnet discovery and product-value validation produce enough demand evidence.
3. **External Bazaar stale row:** the pre-fix `http://` discovery row remains alongside the canonical HTTPS row. This is external catalog hygiene, not a blocker for Phase 0.

## Next phase

Phase 0 is complete for **testnet discovery / market validation**. The next work should focus on demand and market size rather than more payment plumbing:

1. validate that external agents can discover and choose the capability from Bazaar,
2. measure discovery impressions / calls / paid-call conversion where observable,
3. expand the highest-value jurisdiction/project families only after demand evidence,
4. estimate realistic monthly paid API/MCP calls and TAM/SAM/SOM before mainnet pricing,
5. keep mainnet payments blocked until product-value validation passes.

No additional paid calls should be made merely for smoke testing unless a regression specifically requires them.
