# ProjectPermit / BuildRequirements

ProjectPermit is an evidence-linked municipal permit preflight engine for construction and renovation projects. **BuildRequirements** is the deterministic rules engine inside it.

## Current jurisdiction coverage

Current deterministic rule footprint:

- `gatineau_qc`
- `ottawa_on`
- `toronto_on`
- `mississauga_on`
- `laval_qc`
- `longueuil_qc`
- `vancouver_bc`

The engine covers 8 normalized project families, preserves uncertainty instead of guessing, attaches official-source evidence to rule results, and exposes the same jurisdiction router through HTTP, standard MCP, and x402-paid MCP.

First-party municipal/open-data address resolution is available for Gatineau, Ottawa, Toronto, Mississauga and Vancouver. Laval and Longueuil currently support rule preflight with `resolve_address=false`.

The engine deliberately does **not** call an LLM. A calling agent normalizes natural-language scope into structured facts; BuildRequirements applies deterministic municipal rules.

## Live endpoints

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Standard MCP developer-validation preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The HTTP API exposes free machine-readable capability discovery at `GET /v1/capabilities`.

The paid MCP exposes a free `projectpermit_info` tool and the x402-paid `check_project_requirements` tool. The current **testnet discovery price** is **$0.01 USDC** on Base Sepolia (`eip155:84532`); it is not the intended commercial price.

The result is a preflight information package, **not municipal authorization, legal advice, engineering certification, or building-code design approval**.

## Market thesis

The business target is not a homeowner-only `Do I need a permit?` wizard and not a managed permit-submission service. ProjectPermit is intended to become a **cross-jurisdiction permit-requirements intelligence layer** embedded in contractor, property-management, construction/design, permitting, and real-estate software/Agent workflows.

Seven jurisdictions are now enough to validate distribution. Additional city expansion is intentionally paused until repeated external usage, a credible high-volume integration, or a design partner requests more coverage with measurable call volume.

The first commercially meaningful internal checkpoint is roughly **10,000 monthly external preflight calls**. A preferred proof shape is approximately **5 integrations × 2,000 calls/month**, or one platform workflow capable of the same volume. This is a validation target, not a forecast.

Read:

- `docs/MARKET_VALIDATION.md` — market background, pricing thesis and original call-volume model
- `docs/DISTRIBUTION_VALIDATION.md` — 2026 platform evidence, competition and 30-day validation plan
- `docs/CALL_VOLUME_THRESHOLDS.md` — bottom-up monthly-call and revenue thresholds
- `docs/PAIN_EVIDENCE.md` — observed field/community pain evidence separated from assumptions
- `docs/TARGET_ACCOUNT_RANKING.md` — ranked design-partner targets by pain and distribution leverage
- `docs/OUTREACH_BATCH_01.md` — tailored first outreach batch, prepared but not sent
- `docs/DESIGN_PARTNER_TRIAL.md` — low-friction 20-case pilot protocol
- `docs/EXTERNAL_USAGE_BASELINE.md` — clean external-usage starting baseline
- `docs/INTEGRATION_QUICKSTART.md` — copy-paste developer integration examples

## Architecture

All transports call the same shared address-aware preflight pipeline:

`HTTP / standard MCP / x402 paid MCP -> preflight_service -> municipal address/GIS adapters -> jurisdiction router -> deterministic rules`

Resolved non-null municipal property facts can enrich a request before rule evaluation. Unknown overlays remain unknown and never silently overwrite an explicit caller value.

Successful preflight calls also emit privacy-minimal structured usage telemetry for market validation. The telemetry excludes civic address, coordinates, property identifiers, payment credentials, IP/user-agent data and raw client tags. Internal CI/owner smoke traffic is explicitly tagged so it can be excluded from external call counts. Municipal HTTP request URL logging is suppressed so address/query details are not leaked indirectly through `httpx` INFO logs.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn projectpermit.api:app --host 127.0.0.1 --port 8000
```

For standard MCP support:

```bash
pip install -e '.[mcp]'
projectpermit-mcp
```

`projectpermit-mcp` uses MCP Python SDK v2 Streamable HTTP, JSON responses, and stateless HTTP. It listens on `127.0.0.1:8001` by default. Override with `PROJECTPERMIT_MCP_HOST` and `PROJECTPERMIT_MCP_PORT`.

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## API

`POST /v1/check-project-requirements`

Example:

```json
{
  "jurisdiction": "toronto_on",
  "resolve_address": false,
  "project": {
    "family": "window_door",
    "action": "replace_same_size",
    "single_dwelling_house": true,
    "structural_change": false,
    "new_exit": false
  }
}
```

For an address-aware jurisdiction, set `resolve_address=true` and supply `address`; the same behavior is available through standard MCP and paid MCP.

## Developer-validation workflow

The standard MCP endpoint is temporarily free so a design partner can test workflow fit without a wallet or billing setup. A recommended pilot uses **20 anonymized real scopes**, a stable non-PII `context.client_tag`, and measures whether the result actually changes the next workflow step.

Partner evidence is tracked in:

- `data/partner_targets.csv` — 20 candidate design-partner accounts
- `data/partner_feedback.csv` — structured conversation/pilot/call-volume outcomes
- `data/design_partner_scope_template.csv` — anonymized pilot-case template

Summarize validation evidence with:

```bash
python scripts/summarize_partner_feedback.py
```

Unknown interview values remain unknown rather than being silently converted to zero. The commercial gates therefore depend on recorded external evidence, not optimistic inference.

## Repository map

- `src/projectpermit/engine.py` — original Gatineau/Ottawa deterministic rules
- `src/projectpermit/expansion_rules.py` — Toronto/Mississauga rules
- `src/projectpermit/quebec_expansion_rules.py` — Laval/Longueuil rules
- `src/projectpermit/vancouver_rules.py` — Vancouver rules
- `src/projectpermit/jurisdiction_router.py` — public jurisdiction dispatcher
- `src/projectpermit/preflight_service.py` — shared address-aware preflight pipeline
- `src/projectpermit/address.py` — Gatineau/Ottawa/Toronto address/GIS adapters
- `src/projectpermit/mississauga_address.py` — Mississauga address/property adapter
- `src/projectpermit/vancouver_address.py` — Vancouver first-party open-data adapter
- `src/projectpermit/telemetry.py` — privacy-minimal usage events
- `src/projectpermit/http_fetch.py` — municipal HTTP fetch with request-URL log suppression
- `src/projectpermit/api.py` — HTTP API
- `src/projectpermit/mcp_server.py` — standard MCP v2 developer preview
- `src/projectpermit/paid_mcp_server.py` — x402-native paid MCP v2 server
- `src/projectpermit/mcp_v2_x402_compat.py` — MCP SDK v2 / x402 result compatibility shim
- `data/source_manifest.json` — official source registry/freshness metadata
- `data/partner_targets.csv` — first 20 design-partner targets
- `data/partner_feedback.csv` — structured external-validation tracker
- `data/design_partner_scope_template.csv` — anonymized 20-case pilot template
- `schemas/` — public request/response schemas
- `scripts/mcp_remote_smoke.py` — seven-city + Vancouver address-aware public MCP smoke
- `scripts/paid_mcp_unpaid_smoke.py` — no-cost remote payment-challenge test
- `scripts/paid_mcp_buyer_smoke.py` — real buyer-side testnet paid MCP call
- `scripts/facilitator_capability_probe.py` — no-cost facilitator capability matrix
- `scripts/projectpermit_bazaar_lookup.py` — read-only Bazaar catalog lookup
- `scripts/summarize_usage_logs.py` — external/internal usage-log summarizer
- `scripts/summarize_partner_feedback.py` — partner conversation/call-volume gate summarizer
- `docs/PHASE0_SPEC.md` — original product/engineering scope
- `docs/PHASE0_RELEASE_READINESS.md` — completed Phase 0 release gate
- `docs/MARKET_VALIDATION.md` — market background and original business gates
- `docs/DISTRIBUTION_VALIDATION.md` — platform distribution validation plan
- `docs/CALL_VOLUME_THRESHOLDS.md` — monthly API-call economics and go/no-go thresholds
- `docs/PAIN_EVIDENCE.md` — observed workflow pain evidence
- `docs/TARGET_ACCOUNT_RANKING.md` — account prioritization model
- `docs/PARTNER_OUTREACH.md` — outreach/discovery playbook
- `docs/OUTREACH_BATCH_01.md` — first tailored outreach batch
- `docs/DESIGN_PARTNER_TRIAL.md` — design-partner pilot package
- `docs/EXTERNAL_USAGE_BASELINE.md` — telemetry baseline before outreach
- `docs/INTEGRATION_QUICKSTART.md` — developer quickstart
- `docs/X402_ARCHITECTURE.md` — payment/discovery design

## Production verification

The seven-city public MCP footprint and Vancouver address-aware resolution have been verified from GitHub Actions against Railway production. The Vancouver production smoke resolved the City Hall civic address `453 W 12TH AV` and City zoning `CD-1 (46)` through Vancouver first-party open data.

Real buyer-side paid HTTP and paid MCP flows were already verified end-to-end earlier. No additional paid smoke calls should be made merely to prove plumbing that has already passed.

## x402 / Bazaar status

The canonical paid HTTP resource is:

`https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`

It is indexed by the current Bazaar-capable facilitator canary with canonical HTTPS discovery metadata.

Current facilitator canary:

`https://facilitator.goplausible.xyz`

## CI / verification

Current CI covers:

- Python 3.11 + 3.13
- deterministic jurisdiction-rule and schema tests
- address-adapter and shared-preflight regressions
- telemetry privacy contract
- municipal request-log privacy guard
- partner-validation metric summarizer tests
- official source-manifest contracts
- MCP v2 integration
- x402 wire behavior
- MCP v2 settlement-receipt compatibility
- Docker build + live `/health`
- public seven-jurisdiction MCP tool invocation
- public Vancouver address-aware MCP invocation
- public paid-MCP unpaid challenge
- public HTTP Bazaar unpaid challenge
- facilitator capability checks
- canonical HTTPS Bazaar catalog state

See `STATUS.md` for the current engineering state and the distribution documents above for the commercial gates.

## Safety boundary

Determinations intentionally use preflight language such as `REQUIRED`, `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, and `MUNICIPAL_CONFIRMATION_REQUIRED` where uncertainty exists. Ambiguous official thresholds are conservatively routed to confirmation instead of being silently resolved.

The engine should not be presented as a municipality, permit issuer, lawyer, architect, or engineer.
