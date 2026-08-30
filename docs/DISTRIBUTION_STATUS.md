# ProjectPermit Distribution Status

Last verified: 2026-08-30 UTC.

This document separates **publicly visible distribution** from pending submissions, crawler/liveness traffic, historical testnet catalog entries, and real external successful preflight usage. It is intentionally conservative: a channel is not marked live until a public read-back confirms it.

## Publicly visible MCP distribution

| Channel | Status | Verified evidence |
| --- | --- | --- |
| Official MCP Registry | **LIVE** | `io.github.ChanghuLiu/projectpermit` v0.4.1, remote `https://projectpermit-mcp-production.up.railway.app/mcp` |
| Glama | **LIVE** | Public search/index result for ProjectPermit with the expected evidence-linked municipal permit-preflight description |
| agent-tools.cloud MCP index | **LIVE / HEALTHY** | Public API search returns ProjectPermit, `health_status=ok`, `agent_can_self_serve=true`, free production MCP endpoint |

The free MCP endpoint is the current zero-friction acquisition surface. Its health/liveness probes do **not** count as external product validation unless a real ProjectPermit preflight tool is executed successfully.

## x402 / paid HTTP distribution

| Channel | Status | Notes |
| --- | --- | --- |
| Production OpenAPI x402 discovery | **LIVE** | Paid single and batch resources expose x402 metadata; runtime HTTP 402 remains authoritative |
| `/.well-known/x402-service.json` | **LIVE** | Provider-authoritative seller manifest |
| `/.well-known/agent.json` | **LIVE** | Provider-authoritative agent/payment manifest |
| `/.well-known/x402` | **LIVE** | x402scan-compatible fallback containing canonical paid resource URLs |
| agent-tools.cloud x402 index | **NOT PUBLIC YET** | Current public search returns no ProjectPermit x402 match |
| Open 402 registry | **NOT PUBLIC YET** | Production domain is not yet present in `registry/domains.txt` |
| 402 Index | **NOT PUBLIC YET** | A prior submission ID exists, but public search does not show ProjectPermit and the public detail endpoint currently returns 404 |
| x402scan registration | **NOT REGISTERED** | Discovery surface is ready, but registry registration requires an explicit public-listing action; do not claim registration before read-back |

## Bazaar clarification

A public Bazaar lookup currently finds historical ProjectPermit records from **2026-08-26 on Base Sepolia** (`eip155:84532`) with a successful historical settlement. Those records are useful proof that the payment/discovery plumbing worked, but they are **not** the current commercial Base-mainnet listing.

Current production commercial configuration is Base mainnet (`eip155:8453`), USDC, with a launch price of **$0.05 per single preflight** and **$2.00 per HTTP batch of up to 50 items**. Do not treat the old Sepolia Bazaar entry as evidence that the current mainnet offer has been cataloged.

A fresh Bazaar catalog entry is settlement-driven. Do not spend USDC merely to refresh a directory without an explicit commercial reason and approval.

## External validation counters

As of the timestamp above:

- **E4 real external successful preflight calls: 0**
- MCP health checks, handshake traffic, crawler GETs, `tools/list`, and CI smoke calls are excluded.
- Internal ProjectPermit smoke traffic is tagged `internal_traffic=true` and excluded.
- A real external successful preflight must result in a ProjectPermit usage event attributable to non-internal traffic.

## Continuous checks

`External Directory Audit` runs read-only and must never:

- submit a listing;
- send contact information;
- send credentials;
- send payment headers;
- spend USDC.

Its purpose is only to detect when public directory visibility changes. Real external usage remains a separate validation signal.
