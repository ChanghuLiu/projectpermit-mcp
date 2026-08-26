# Phase 0 Release Readiness

Updated: 2026-08-26

ProjectPermit Phase 0 is intended to prove three things before municipality expansion or mainnet monetization:

1. deterministic permit preflight can be delivered with official evidence,
2. an external agent can call it through MCP,
3. a paid MCP call can settle through x402 without putting payment logic inside BuildRequirements.

## Gate matrix

| Gate | Status | Evidence / note |
|---|---|---|
| Gatineau + Ottawa rule engine | PASS | Deterministic rules, stable rule ids, conservative outcomes |
| 8 Phase 0 project families | PASS | Covered by taxonomy/golden corpus |
| Official-source evidence | PASS | Rule results carry authority/source metadata |
| Rule versioning / overlays | PASS | Version-aware data model; unknown overlays preserved as unknown |
| Python 3.11 | PASS | GitHub Actions |
| Python 3.13 | PASS | GitHub Actions |
| Public JSON schema contracts | PASS | CI contract checks |
| Source-change watchdog | PASS | Manifest/watch tooling present |
| Docker build | PASS | GitHub Actions |
| Container health | PASS | Live `/health` check in CI |
| Public HTTP API | PASS | Railway deployment |
| Public standard MCP v2 | PASS | Remote MCP initialize/list/call smoke |
| x402 unpaid challenge | PASS | Remote paid-MCP challenge returns v2 payment requirements |
| Paid HTTP x402 E2E | PASS | Real Base Sepolia buyer call + server verification/settlement |
| Paid MCP x402 E2E | PASS | Real Base Sepolia MCP buyer call + deterministic tool result |
| Server-side x402 `/verify` | PASS | Railway logs confirmed facilitator HTTP 200 |
| Server-side x402 `/settle` | PASS | Railway logs confirmed facilitator HTTP 200 |
| MCP v2 settlement receipt compatibility | PASS | Compatibility shim + regression smoke |
| Bazaar-capable facilitator canary | PASS | GoPlausible supports Base Sepolia exact v2 + discovery listing; paid MCP service boots and challenges correctly |
| ProjectPermit pre-index Bazaar snapshot | PASS | Read-only catalog lookup reports absent before first canary settlement |
| ProjectPermit indexed in Bazaar | PENDING | Requires exactly one paid MCP settlement through current GoPlausible canary, then read-only lookup |
| Gatineau stable PIIA/heritage machine endpoint | OPEN / NON-BLOCKING | Unknown remains unknown; no unsafe false default |
| Mainnet payments | INTENTIONALLY BLOCKED | Do not enable before product-value validation |

## Current live endpoints

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The paid MCP tool is `check_project_requirements`; `projectpermit_info` remains free.

## Current payment canary

- Network: Base Sepolia — `eip155:84532`
- Asset: Circle test USDC
- Price: `$0.01`
- Facilitator: `https://facilitator.goplausible.xyz`
- Payment recipient: configured as a public EVM address in Railway; payer secrets never belong in the repository or server environment.

## Release decision rule

Phase 0 can be marked **release-ready for testnet discovery/market validation** when the final Bazaar-indexing gate passes.

Passing Phase 0 does **not** authorize mainnet, expanded legal claims, or presentation as an official municipality service. Those remain separate product decisions.

## Final remaining procedure

1. Make one and only one paid MCP test call through the current canary.
2. Confirm facilitator `/verify` and `/settle` return success in Railway logs.
3. Run the read-only ProjectPermit Bazaar lookup.
4. Inspect the catalog row for the paid MCP discovery metadata and settlement count.
5. If present, mark the Bazaar gate PASS and tag the Phase 0 testnet release.
