# Phase 0 Release Readiness

Updated: 2026-08-26

ProjectPermit Phase 0 is intended to prove three things before municipality expansion or mainnet monetization:

1. deterministic permit preflight can be delivered with official evidence,
2. an external agent can call it through MCP,
3. a paid MCP/API call can settle through x402 without putting payment logic inside BuildRequirements.

## Release decision

**PASS — Phase 0 is release-ready for testnet discovery / market validation.**

This does **not** authorize mainnet payments, expanded legal claims, or presentation as an official municipality service.

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
| Server-side x402 `/verify` | PASS | Railway logs confirmed facilitator HTTP 200 in paid runs |
| Server-side x402 `/settle` | PASS | Railway logs confirmed facilitator HTTP 200 in paid runs |
| MCP v2 settlement receipt compatibility | PASS | Compatibility shim + regression smoke |
| Bazaar-capable facilitator canary | PASS | GoPlausible supports Base Sepolia exact v2 + discovery listing |
| ProjectPermit Bazaar indexing | PASS | Catalog grew and ProjectPermit appeared after settlement |
| Canonical HTTPS Bazaar resource | PASS | `FOUND_CANONICAL_HTTPS`; exact public HTTPS POST URL present |
| Gatineau stable PIIA/heritage machine endpoint | OPEN / NON-BLOCKING | Unknown remains unknown; no unsafe false default |
| Mainnet payments | INTENTIONALLY BLOCKED | Do not enable before product-value validation |

## Current live endpoints

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The paid MCP tool is `check_project_requirements`; `projectpermit_info` remains free.

## Current test payment profile

- Network: Base Sepolia — `eip155:84532`
- Asset: Circle test USDC
- Price: `$0.01`
- Facilitator used for Bazaar validation: `https://facilitator.goplausible.xyz`
- Payment recipient: configured as a public EVM address in Railway; payer secrets never belong in the repository or server environment.

## Final Bazaar evidence

After the canonical HTTPS fix and one final real paid HTTP call:

- Railway independently recorded `POST` 402 followed by `POST` 200.
- Buyer received `settlement_success=True`.
- Settlement transaction: `0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`.
- GoPlausible catalog total reached **1682**.
- ProjectPermit catalog matches: **2**.
- Canonical HTTPS matches: **1**.
- Canonical resource URL: `https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`.
- Canonical row method: `POST`.
- Canonical row network: `eip155:84532`.
- Canonical row price: `10000` USDC atomic units.
- Canonical row scheme: `exact`.
- Canonical row `settleCount`: **1**.
- Lookup status: **`projectpermit_bazaar=FOUND_CANONICAL_HTTPS`**.

The external catalog still contains one stale pre-fix `http://` row. Because the canonical HTTPS row is separately present and validated, this is not a Phase 0 blocker.

## Phase 0 conclusion

The product now has evidence for the full testnet path:

**external buyer / agent -> discovery -> x402 challenge -> payment authorization -> facilitator verification -> deterministic ProjectPermit execution -> settlement -> structured result -> Bazaar listing**

Phase 0 payment plumbing should now be treated as complete. Further paid smoke calls are discouraged unless a specific regression requires them.

## Next gate: market validation

The next decision is no longer technical transport readiness. It is whether the capability can generate enough repeat paid calls to justify expansion.

Required next-phase evidence:

1. external-agent discovery and selection behavior,
2. paid call frequency per customer/workflow,
3. realistic target-agent / target-enterprise count,
4. jurisdiction and project-family expansion demand,
5. TAM / SAM / SOM and potential monthly API/MCP calls,
6. willingness to pay at realistic mainnet prices.

Mainnet remains intentionally blocked until that evidence is strong enough.
