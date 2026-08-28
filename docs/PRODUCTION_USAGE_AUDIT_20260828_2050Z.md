# Production Usage Audit — 2026-08-28 20:50Z

## Purpose

Extend `docs/PRODUCTION_USAGE_AUDIT_20260828_1620Z.md` through 20:50Z and determine whether the substantial new discovery/probe traffic converted into countable external ProjectPermit usage.

This is an incremental audit. It does not reclassify protocol handshakes, registry probes, unpaid 402 requests or internal CI/owner previews as product usage.

## Incremental audit window

Reviewed Railway production traffic and application telemetry for approximately:

- start: `2026-08-28T16:20:00Z`
- end: `2026-08-28T20:50:00Z`

Production surfaces checked:

1. `projectpermit-api-v2`
2. `projectpermit-mcp`
3. `projectpermit-x402-mcp`
4. legacy `projectpermit-api` deployment status

## 1. API v2 — discovery increased, paid conversion remained zero

The API-v2 endpoint continued to receive internal remote-smoke traffic plus some independent external discovery.

Notable external/non-CI observations included:

- a Node client at `94.72.106.160` repeatedly posting to `/v1/check-project-requirements`; every attempt returned **402 Payment Required**;
- a browser-style client at `79.177.157.243` fetching `/openapi.json` successfully;
- later generic icon/favicon probing from another external address.

These are discovery/evaluation signals only.

### Application-level telemetry is decisive

For the entire 16:20Z–20:50Z increment, every visible `PROJECTPERMIT_USAGE` preflight event was explicitly tagged:

- `internal_traffic: true`
- `client_tag_hash: e75759cae03f5b65`
- `transport: http_preview`

The repeated jurisdiction/family pattern also matched the known remote smoke matrix, including Ottawa window/door and Ottawa/Toronto/Mississauga basement cases.

No `PROJECTPERMIT_USAGE` event with `internal_traffic: false` was observed.

### Paid result

All visible `/v1/check-project-requirements` attempts in the incremental window remained **402**. No 2xx paid determination or external payment-success marker was observed.

Therefore:

- external successful API preflights: **0**
- external paid API success: **0**

## 2. Free MCP — meaningful ecosystem discovery, still no tool-use evidence

The public MCP endpoint was independently reached by a broader set of MCP ecosystem services during the incremental window.

Identifiable examples included:

- `SentinelOracle/0.1` — explicitly says `liveness-only, never invokes tools`;
- `mcpbeat/0.1` — liveness checks;
- `402explorer/0.1`;
- `VerifyMCP-OwnersBot/1.0`;
- `ProofBench/0.1` — MCP registry health probe;
- `mcplookup.com-probe/0.1`;
- `AIVE-MCP-EndpointProbe/1.0` — reachability-only probe;
- `agent-tools.cloud-crawler/0.1`;
- `mcpscan/1.0` — MCP index crawler;
- `utopian-foundry-probe/1.0`;
- long-lived `GET /mcp` connections from a Bun client.

This is stronger evidence that the public endpoint is visible across multiple independent MCP directories/indexers.

It is **not E4**.

### One ambiguous standalone MCP request was checked

A single `python-httpx/0.28.1` POST from `188.122.20.85` at roughly 17:05Z did not match the obvious named crawler UAs or the larger Azure CI burst pattern.

The application deploy log for that event showed only:

- `POST /mcp` → 200;
- `Terminating session: None` immediately afterward.

There was no tool invocation/session evidence and no ProjectPermit preflight telemetry associated with it.

It is therefore classified as a compatibility/probe request, not E4 usage.

### Internal remote-smoke pattern

Separate `python-httpx2/2.12.0` bursts from changing Microsoft/Azure IPs repeatedly followed the known multi-request remote-smoke shape after repository merges. Those are infrastructure validation, not external users.

Therefore:

- independent MCP discovery: **yes, multiple sources**
- countable external successful preflight invocation: **0**

## 3. Paid x402 MCP — protocol traffic but no completed economic behavior

The x402 MCP endpoint received many short bursts of `POST /mcp`, generally from rotating Microsoft/Azure addresses with `python-httpx2/2.12.0`.

The bursts were highly regular and aligned with ProjectPermit's own remote paid/MCP smoke behavior after main-branch changes. MCP 200/202 responses in these sequences are protocol/session success, not payment or a completed permit determination.

No external payment-success marker, settlement success, or countable external paid preflight was observed.

Therefore:

- external paid x402 successful preflight: **0**
- external economic commitment: **0**

## 4. Legacy API

The legacy `projectpermit-api` service's latest deployment was in a failed state and had no HTTP traffic in the reviewed window.

It contributes no external usage evidence.

## Consolidated evidence through 20:50Z

| Production surface | Independent discovery/probes | External successful preflights | External paid success |
|---|---:|---:|---:|
| API v2 | Yes | **0** | **0** |
| Free MCP | Yes — multiple independent registries/indexers | **0** | n/a |
| x402 MCP | Yes / protocol probes + internal smoke | **0** | **0** |
| Legacy API | No current traffic | **0** | **0** |

Current evidence state remains:

- **E4 = 0**
- non-owner successful preflight calls = **0**
- external paid success = **0**
- **E5 = 0**

## What this increment changes

The distribution signal is now stronger than it was at 16:20Z:

> ProjectPermit is not merely published; multiple independent MCP ecosystem crawlers, registry-health systems and discovery services are actively finding the endpoint.

But the conversion evidence remains absent:

`discovery / indexing -> tool invocation -> repeated operational workflow -> payment/resource commitment`

ProjectPermit is still stopping at the first stage.

This is important because it weakens any argument that E4=0 is simply caused by the service being undiscoverable. Public discoverability now has direct production-log evidence, yet no countable external preflight use has followed in this audit window.

The observation is still short-duration and must **not** be converted into a permanent No-Go claim. It is a stronger distribution falsification datapoint, not proof that organic MCP distribution can never work.

## Decision impact

**No Go/No-Go score change.**

Canonical status remains:

> **50/100 — PAUSE / RE-SCOPE; rescue / falsification only.**

The correct interpretation is stricter than `no traffic`:

> **There is real discovery traffic, but no verified conversion into E4/E5 behavior yet.**

No new MCP/x402 feature work is justified by these logs. A future upgrade requires a real non-owner successful preflight, repeated external workflow, or payment/resource commitment—not more probes or indexer traffic.
