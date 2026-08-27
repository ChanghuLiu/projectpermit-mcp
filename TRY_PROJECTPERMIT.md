# Try ProjectPermit in 30 seconds

No account, API key, wallet, MCP client, or platform integration is required for the current structured-facts validation preview.

## 1. See supported jurisdictions and project families

```bash
curl -sS https://projectpermit-api-v2-production.up.railway.app/v1/capabilities
```

## 2. Run one free preflight preview

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -X POST \
  https://projectpermit-api-v2-production.up.railway.app/v1/preview-project-requirements \
  -d '{
    "jurisdiction": "ottawa_on",
    "project": {
      "family": "window_door",
      "action": "replace_same_size"
    },
    "property": {
      "heritage": false
    },
    "context": {
      "client_tag": "your-non-pii-pilot-id"
    }
  }'
```

Expected determination for that example: `LIKELY_NOT_REQUIRED`.

Use a stable, non-identifying `context.client_tag` if you are testing multiple cases. ProjectPermit hashes the tag before telemetry is written. Do not put a person/customer name, email, exact civic address, account id, or other identifying data in the tag.

## Free-preview boundary

The free HTTP preview intentionally does **not** accept:

- `address`
- `resolve_address`

Those fields return HTTP `422`. This keeps the low-friction validation surface limited to already-structured, de-identified facts and prevents civic-address/GIS lookups through the anonymous preview.

For current design-partner validation requiring address-aware first-party municipal data, use the standard MCP preview documented in `llms-install.md` or coordinate a bounded pilot.

## What the result is

ProjectPermit returns deterministic, evidence-linked municipal permit/planning preflight information. It is not municipal authorization, legal advice, engineering certification, or a building-code design approval.

Unsupported or ambiguous cases should remain visible as uncertainty / confirmation / out-of-scope results rather than being filtered out.

## Historical batch benchmark

For 5–20 representative anonymized historical cases, use the existing E3 CSV plus:

```bash
python scripts/run_remote_historical_benchmark.py path/to/partner_cases.csv \
  --output path/to/partner_cases.evaluated.csv \
  --client-tag partner-pilot-01
```

See `docs/E3_BENCHMARK_RUNBOOK.md` for the sampling and privacy requirements.
