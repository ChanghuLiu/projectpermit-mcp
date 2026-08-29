# ProjectPermit / BuildRequirements

ProjectPermit is an evidence-linked municipal permit preflight engine for construction and renovation projects. **BuildRequirements** is the deterministic rules engine inside it.

## Try free in 30 seconds

No account, API key, wallet, MCP client, or platform integration is required for the current structured-facts validation preview.

- Free HTTP preview: `POST https://projectpermit-api-v2-production.up.railway.app/v1/preview-project-requirements`
- Free capability discovery: `GET https://projectpermit-api-v2-production.up.railway.app/v1/capabilities`
- Free standard MCP preview: `https://projectpermit-mcp-production.up.railway.app/mcp`

See [`TRY_PROJECTPERMIT.md`](TRY_PROJECTPERMIT.md) for a copy-paste `curl` example and the preview privacy boundary. The anonymous HTTP preview intentionally excludes civic-address/GIS resolution; use the standard MCP developer preview for a bounded address-aware validation workflow.

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

## Agent workflow differentiation

Every successful preflight now includes an additive deterministic `workflow` object so a contractor, property or field-service agent can use the result inside a real operating workflow instead of merely displaying a permit answer.

Stable routing signals include:

- `ADD_PERMIT_TASK`
- `CONTINUE_WITH_EVIDENCE`
- `COLLECT_MISSING_FACTS`
- `ROUTE_SPECIAL_REVIEW`
- `MUNICIPAL_CONFIRMATION`
- `MANUAL_SCOPE_REVIEW`

The workflow package also includes a quote-handling signal, a deliberately narrow `automation_safe` flag, and up to three high-value follow-up questions when another deterministic call can resolve missing context. Workflow guidance never changes the underlying permit determination and never represents municipal authorization.

See [`docs/AGENT_WORKFLOW_GUIDANCE.md`](docs/AGENT_WORKFLOW_GUIDANCE.md).

## Live endpoints and commercial x402 pricing

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free HTTP developer-validation preview: `POST https://projectpermit-api-v2-production.up.railway.app/v1/preview-project-requirements`
- Standard MCP developer-validation preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The HTTP API exposes free machine-readable capability discovery at `GET /v1/capabilities`.

Commercial x402 resources are configured on **Base mainnet** (`eip155:8453`) with USDC payment:

- single paid HTTP preflight: **$0.20 USDC**
- single paid MCP preflight: **$0.20 USDC**
- paid HTTP batch, up to 50 normalized projects: **$5.00 USDC**

The production facilitator is `https://facilitator.payai.network`.

The paid MCP exposes a free `projectpermit_info` tool and the x402-paid `check_project_requirements` tool. The paid HTTP routes return an x402 `402 Payment Required` challenge when no valid payment is supplied.

The result is a preflight information package, **not municipal authorization, legal advice, engineering certification, or building-code design approval**.

## Market thesis

The business target is not a homeowner-only `Do I need a permit?` wizard and not a managed permit-submission service. ProjectPermit is intended to become a **cross-jurisdiction permit-requirements intelligence layer** embedded in contractor, property-management, construction/design, permitting, and real-estate software/Agent workflows.

Market validation remains active in parallel with product development. Differentiated product work and commercial distribution no longer wait for outreach replies. Geography expansion remains evidence-led because every additional municipality adds ongoing rule/source maintenance cost; priority goes to requested geographies or workflows with credible repeated volume.

The first commercially meaningful internal checkpoint is roughly **10,000 monthly external preflight calls**. A preferred proof shape is approximately **5 integrations × 2,000 calls/month**, or one platform workflow capable of the same volume. This is a validation target, not a forecast.

Read:

- `docs/MARKET_VALIDATION.md` — market background, pricing thesis and original call-volume model
- `docs/DISTRIBUTION_VALIDATION.md` — 2026 platform evidence, competition and validation plan
- `docs/CALL_VOLUME_THRESHOLDS.md` — bottom-up monthly-call and revenue thresholds
- `docs/PAIN_EVIDENCE.md` — observed field/community pain evidence separated from assumptions
- `docs/TARGET_ACCOUNT_RANKING.md` — ranked design-partner targets by pain and distribution leverage
- `docs/OUTREACH_BATCH_01.md` — tailored first outreach batch
- `docs/DESIGN_PARTNER_TRIAL.md` — low-friction 20-case pilot protocol
- `docs/EXTERNAL_USAGE_BASELINE.md` — clean external-usage starting baseline
- `docs/INTEGRATION_QUICKSTART.md` — copy-paste developer integration examples

## Architecture

All transports call the same shared address-aware preflight pipeline:

`HTTP / standard MCP / x402 paid MCP -> preflight_service -> municipal address/GIS adapters -> jurisdiction router -> deterministic rules -> workflow guidance`

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

For no-wallet validation, use the free structured-facts route:

`POST /v1/preview-project-requirements`

For the x402-paid HTTP contract, use:

`POST /v1/check-project-requirements`

Both use the same normalized project shape; the anonymous free preview intentionally rejects address/GIS resolution. Example project facts:

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

A successful preflight response also contains `workflow`, for example:

```json
{
  "workflow": {
    "mode": "NO_PERMIT_SIGNAL",
    "recommended_route": "CONTINUE_WITH_EVIDENCE",
    "quote_handling": "NO_PERMIT_ALLOWANCE_SIGNAL",
    "automation_safe": true,
    "follow_up_questions": []
  }
}
```

For an address-aware jurisdiction, set `resolve_address=true` and supply `address` through the standard MCP preview or paid route; the anonymous HTTP preview deliberately does not accept address resolution.

## Developer-validation workflow

The standard MCP endpoint remains free so a design partner can test workflow fit without a wallet or billing setup. A recommended pilot uses **20 anonymized real scopes**, a stable non-PII `context.client_tag`, and measures whether the result actually changes the next workflow step.

Partner evidence is tracked in:

- `data/partner_targets.csv` — 20 candidate design-partner accounts
- `data/partner_feedback.csv` — structured conversation/pilot/call-volume outcomes
- `data/design_partner_scope_template.csv` — anonymized pilot-case template

Summarize validation evidence with:

```bash
python scripts/summarize_partner_feedback.py
```

Unknown interview values remain unknown rather than being silently converted to zero. Commercial decisions therefore depend on recorded external evidence, not optimistic inference, while engineering/distribution work continues in parallel.

## Repository map

- `src/projectpermit/engine.py` — original Gatineau/Ottawa deterministic rules
- `src/projectpermit/expansion_rules.py` — Toronto/Mississauga rules
- `src/projectpermit/quebec_expansion_rules.py` — Laval/Longueuil rules
- `src/projectpermit/vancouver_rules.py` — Vancouver rules
- `src/projectpermit/jurisdiction_router.py` — public jurisdiction dispatcher
- `src/projectpermit/preflight_service.py` — shared address-aware preflight pipeline
- `src/projectpermit/workflow_advice.py` — deterministic agent routing and missing-fact guidance
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
- `scripts/paid_mcp_buyer_smoke.py` — historical buyer-side paid smoke tooling; do not spend merely to re-prove plumbing
- `scripts/facilitator_capability_probe.py` — no-cost facilitator capability matrix
- `scripts/projectpermit_bazaar_lookup.py` — read-only Bazaar catalog lookup
- `scripts/summarize_usage_logs.py` — external/internal usage-log summarizer
- `scripts/summarize_partner_feedback.py` — partner conversation/call-volume gate summarizer
- `docs/AGENT_WORKFLOW_GUIDANCE.md` — workflow-routing response contract and integration pattern
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

Historical buyer-side paid HTTP and paid MCP settlement were verified end-to-end on testnet. The commercial production services are now configured for Base mainnet and can be verified without spending funds by checking their x402 `402 Payment Required` challenges. A real mainnet payment should only be made when there is a reason to verify actual settlement or a genuine buyer call.

## x402 / discovery status

Canonical paid HTTP resources:

- `https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`
- `https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements-batch`

Canonical paid MCP resource:

- `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Commercial network: `eip155:8453` (Base mainnet)

Production facilitator: `https://facilitator.payai.network`

The single HTTP resource publishes Bazaar discovery metadata; paid MCP publishes MCP x402 discovery metadata. Both advertise the Agent workflow-routing differentiation.

## CI / verification

Current CI covers:

- Python 3.11 + 3.13
- deterministic jurisdiction-rule and schema tests
- workflow-guidance routing tests
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
- public paid-bulk HTTP unpaid challenge
- facilitator capability checks

See `STATUS.md` for the broader engineering/validation state and the distribution documents above for market evidence.

## Safety boundary

Determinations intentionally use preflight language such as `REQUIRED`, `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, and `MUNICIPAL_CONFIRMATION_REQUIRED` where uncertainty exists. Ambiguous official thresholds are conservatively routed to confirmation instead of being silently resolved.

The engine should not be presented as a municipality, permit issuer, lawyer, architect, or engineer.
