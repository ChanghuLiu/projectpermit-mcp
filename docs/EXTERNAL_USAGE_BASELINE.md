# ProjectPermit External Usage Baseline

Captured: 2026-08-27 around 13:14 UTC

This is the starting point for distribution validation after privacy-minimal production telemetry was deployed.

## Observed production telemetry since the privacy deployment

Across the three active Railway services:

- standard free MCP: **32 successful preflight events observed**
- paid HTTP API: **0 successful preflight events observed in this window**
- paid x402 MCP: **0 successful preflight events observed in this window**
- external/non-owner events: **0**
- internal events: **32**

All 32 standard MCP events were tagged `internal_traffic=true` by CI/remote smoke tests. They consist of repeated seven-jurisdiction verification plus Vancouver address-aware smoke calls and therefore **must not be counted as market validation**.

This zero-external baseline is expected: targeted outreach has been prepared but not sent.

## Why record a zero baseline

Without an explicit baseline it is easy to accidentally count CI traffic, owner smoke tests or deployment verification as demand. From this point forward the relevant number is:

> `events_external`, not total requests.

For integrations that voluntarily provide a stable `context.client_tag`, telemetry stores only a short SHA-256-derived hash, allowing repeated use to be grouped without persisting the raw tag.

Raw civic addresses, coordinates, property identifiers, request bodies, payment credentials, IP addresses and user-agent strings are intentionally excluded from `PROJECTPERMIT_USAGE` events.

## Measurement checkpoints

| Gate | Current | Target |
|---|---:|---:|
| External preflight calls | 0 | 100+ initial validation |
| External integrations/client tags | 0 | 3+ |
| Largest integration repeat count | 0 | 20+ initial; 2,000+/month strong signal |
| Address-aware external calls | 0 | measure, no arbitrary target yet |
| Credible monthly call path | none | 10,000+ |
| Buyer pricing validation | none | one buyer accepts ~$0.20-$0.50/call equivalent |

## Re-check procedure

Use Railway runtime logs from all active services, filter for `PROJECTPERMIT_USAGE`, then pipe/export them into:

```bash
python scripts/summarize_usage_logs.py
```

The summarizer reports:

- total events;
- external vs internal events;
- unique hashed external client tags;
- external calls by transport;
- external calls by jurisdiction;
- external calls by project family;
- external determinations.

Do not use raw proxy request counts as the external-demand metric because health checks, MCP session setup and unpaid x402 challenges are not successful permit-preflight usage.
