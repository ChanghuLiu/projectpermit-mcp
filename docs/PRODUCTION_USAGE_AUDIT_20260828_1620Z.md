# Production Usage Audit — 2026-08-28 16:20Z

## Purpose

Re-check all live ProjectPermit production surfaces for countable external usage after the latest validation/outreach work.

This audit deliberately separates:

- internal/CI smoke traffic;
- MCP registry/indexing/liveness discovery;
- unpaid payment probes;
- actual external preflight tool usage;
- actual external paid usage.

Only successful non-owner/non-CI preflight invocations can count toward E4. Discovery, handshakes, tool listing, health probes and unpaid payment attempts do not count.

## Audit window

Reviewed Railway production logs for approximately:

- start: `2026-08-28T12:00:00Z`
- end: `2026-08-28T16:20:00Z`

Production services checked:

1. `projectpermit-api-v2`
2. `projectpermit-mcp` (free / standard MCP)
3. `projectpermit-x402-mcp` (paid MCP)

## 1. API v2

### Successful preflights

Every visible `PROJECTPERMIT_USAGE` success event in the audit window was explicitly tagged:

- `internal_traffic: true`
- known internal client-tag hash

These included ordinary CI/owner preview checks.

### Paid endpoint probes

`POST /v1/check-project-requirements` received multiple `402 Payment Required` responses.

A 402 request is evidence that something reached the payment boundary, not evidence of payment, tool completion or economic behavior.

No external successful paid preflight was observed.

### Other external traffic

A `GET /robots.txt` crawler request returned 404.

This is discovery traffic only.

### API-v2 E4 result

**0 countable external successful preflights.**

## 2. Free / standard MCP

The public MCP endpoint received substantial external request traffic.

Observed identifiable discovery/indexing/liveness clients included examples such as:

- `mcpbeat` — liveness checks;
- `SentinelOracle` — explicitly liveness-only;
- `AgentIndexBot` — MCP/agent indexing crawler;
- `402explorer` — discovery/probing;
- `MCP-Stats-Prober`;
- `mcpscan` — MCP index crawler;
- `ProofBench` — registry health probe;
- `agent-world-probe` — MCP census/research;
- `mcp-rugpull-research`;
- other requests for `robots.txt`, `/.well-known/x402`, `/.well-known/agent-card.json`, `/openapi.json`, and `/.well-known/glama.json`.

There were also long-lived `GET /mcp` connections and MCP `POST /mcp` 200/202 handshakes from external IPs/clients.

### Critical interpretation

MCP HTTP 200/202 responses are **not** sufficient to prove a ProjectPermit tool was invoked. They can represent protocol initialization, session traffic, tool discovery, health checks or indexer probes.

The authoritative application-level telemetry is `PROJECTPERMIT_USAGE`.

All visible actual preflight usage telemetry in this window was still:

- `internal_traffic: true`.

No external preflight invocation event was observed.

### Free-MCP E4 result

**0 countable external successful preflights.**

### Distribution signal

The endpoint is now being independently discovered by multiple MCP indexers/probers.

Classify this strictly as:

> **E0 — external distribution/discovery signal, not product usage.**

It is useful because it confirms the public endpoint is visible to parts of the MCP ecosystem. It does not show that an agent/user found the tool valuable enough to call its permit-preflight capability.

## 3. Paid x402 MCP

The x402 MCP endpoint received repeated MCP protocol POST traffic, primarily patterned `python-httpx2` requests consistent with automated/infrastructure probing and internal validation sequences.

During the audit window there was:

- no visible `PROJECTPERMIT_USAGE` event demonstrating an external paid preflight;
- no external settlement/payment-success marker;
- no evidence that an external actor completed the paid tool flow;
- a crawler-style `robots.txt` request only outside the protocol sequences.

MCP handshakes returning HTTP 200/202 are not payment success.

### x402 E4/E5 result

- external paid successful preflight: **0**
- external payment/economic signal: **0**

## Consolidated result

| Production surface | External discovery/probes | External successful preflights | External paid success |
|---|---:|---:|---:|
| API v2 | Yes | **0** | **0** |
| Free MCP | Yes — multiple independent MCP crawlers/indexers | **0** | n/a |
| x402 MCP | Yes / protocol probes | **0** | **0** |

Current evidence state remains:

- **E4 = 0**
- non-owner successful preflight calls = **0**
- external paid x402 success = **0**
- **E5 = 0**

## What changed since earlier usage audits

The meaningful change is not usage but **discoverability**:

> Multiple independent MCP ecosystem crawlers/indexers are now reaching the public endpoint.

This is a real distribution-layer observation but must not be upgraded into demand evidence.

The missing conversion is still:

`external discovery -> actual permit-preflight tool invocation -> repeated workflow -> economic commitment`

ProjectPermit currently stops at the first stage.

## Decision impact

**No Go/No-Go score change.**

Discovery traffic is encouraging operationally but is E0 and therefore cannot offset the current weak E2-E5 evidence.

ProjectPermit remains:

> **50/100 — VALIDATION / FALSIFICATION ONLY; NO PRODUCT EXPANSION.**

The next meaningful product signal must still come from one of:

- a bounded upstream E2 workflow denominator;
- representative E3 historical cases;
- a real external E4 pilot/use pattern;
- E5 payment/resource commitment;
- a qualified negative build-vs-buy/API response that triggers STOP / RE-SCOPE.
