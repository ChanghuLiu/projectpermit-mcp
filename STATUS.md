# ProjectPermit Status

Updated: 2026-08-26

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

**Phase 1A Toronto + Mississauga expansion: PASS.** Both cities have deterministic rule coverage plus first-party municipal address/zoning/heritage adapters.

**Phase 1B Laval + Longueuil six-city expansion: PASS.** Conservative deterministic rule coverage is publicly verified.

**Phase 1C Vancouver seven-city expansion: PASS.** Vancouver rules plus first-party City address/zoning/heritage resolution are deployed and verified against the public MCP service.

ProjectPermit is now an evidence-linked deterministic municipal permit preflight engine across seven jurisdictions. The calling Agent normalizes project scope; the server applies municipal rules and returns official-source evidence. The rules engine does not call an LLM and payment remains outside BuildRequirements.

## Jurisdiction coverage

- `gatineau_qc` — deterministic rules + municipal address geocoder; PIIA/heritage machine overlays still unresolved
- `ottawa_on` — deterministic rules + address/zoning/heritage GIS
- `toronto_on` — deterministic rules + City address/zoning/heritage GIS
- `mississauga_on` — deterministic rules + City address/zoning/heritage/property GIS
- `laval_qc` — conservative deterministic rules; address/GIS adapter pending
- `longueuil_qc` — conservative deterministic rules; address/GIS adapter pending
- `vancouver_bc` — deterministic rules + City Open Data property-address/zoning/heritage adapter

All transports call the same `preflight_service` before the jurisdiction router. For supported address jurisdictions, `resolve_address=true` enriches the request with first-party municipal property context. Laval and Longueuil currently use `resolve_address=false`.

## Production verification

GitHub Actions run 130 (`33022280741`) completed **8/8 jobs successfully**:

- Python 3.11 core
- Python 3.13 core
- optional MCP/x402 integrations
- Docker/container health
- remote seven-jurisdiction free MCP
- remote paid-MCP unpaid challenge
- remote HTTP Bazaar unpaid challenge
- facilitator/Bazaar capability state

The remote MCP test also performed a real address-aware Vancouver call using the public civic address `453 W 12TH AVE, Vancouver, BC` and the live City of Vancouver open-data APIs. It resolved:

- matched address: `453 W 12TH AV`
- zoning: `CD-1 (46)`
- result: `vancouver_address_aware_preflight=PASS`

No paid smoke transaction was required for this expansion verification.

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP developer-validation preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Latest seven-city production deployments are successful for all three active services.

Paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid permit preflight

Current **testnet discovery price**: **$0.01 USDC per paid tool/API call** on Base Sepolia. This is not the intended commercial price.

## Completed infrastructure

- seven-jurisdiction deterministic rule router across 8 normalized project families
- five first-party municipal/open-data address resolver jurisdictions
- shared address-aware preflight service for HTTP/free MCP/paid MCP
- official evidence and stable rule ids
- public FastAPI, standard MCP v2 and x402-native paid MCP
- Base Sepolia x402 payment profile
- real buyer-side paid HTTP + paid MCP verification/settlement
- GoPlausible Bazaar canonical HTTPS indexing
- Docker + GitHub Actions CI
- no server-side LLM dependency
- no paid map/property-data dependency

## Verification policy

Real buyer-side x402 plumbing is already proven. **Do not spend additional test USDC for routine expansion smoke tests.** Expansion verification should use free discovery or unpaid 402 challenges.

Final canonical-HTTPS Phase 0 HTTP settlement transaction:

`0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`

## Market decision

The commercial thesis is a **cross-jurisdiction B2B/Agent permit-requirements intelligence layer**, not a homeowner-only wizard and not a managed permit-submission service.

The current seven-city footprint is enough to validate distribution. Municipality expansion is now intentionally paused until repeated external usage or a design-partner request justifies more maintenance.

The working commercial hypothesis remains roughly **$0.20-$0.50 per address-aware evidence-linked preflight** or an equivalent platform volume plan, subject to external willingness-to-pay validation.

Two market documents now separate the questions:

- `docs/MARKET_VALIDATION.md` — market background, pricing thesis and original call-volume model
- `docs/DISTRIBUTION_VALIDATION.md` — 2026 platform evidence, competition, ServiceTitan workflow scenario and 30-day GTM test

## Distribution evidence now driving the next phase

Current public platform signals include:

- U.S. construction: 814,557 employer establishments in 2023 County Business Patterns
- Canada construction: 159,514 employer + 255,892 non-employer/indeterminate establishments in 2025
- ServiceTitan: 12,000+ businesses and 40M+ jobs completed annually
- Procore: 17,850 customers at 2025 year-end
- AppFolio: 22,096 property-management customers and 9.4M units under management at 2025 year-end
- Autodesk Construction: used by builders on 2M+ projects

These numbers are distribution-surface indicators, not additive TAM. The strongest immediate experiment is to insert ProjectPermit into a repeated field-service/property/construction workflow rather than acquiring homeowners one by one.

## Known unresolved items

1. **Laval/Longueuil property adapters:** rule coverage exists; stable no-cost address/zoning/overlay resolution still needs evaluation only if usage justifies it.
2. **Gatineau PIIA/heritage:** public mapping confirms the concepts/layers but a stable unauthenticated machine endpoint is not yet locked. Unknown must never become false.
3. **Longueuil exemptions:** current simplified material describes permit workflows more clearly than universal exemptions, so conservative outcomes remain intentional.
4. **Mainnet:** intentionally disabled until external demand and willingness-to-pay validation pass.
5. **External Bazaar stale row:** historical `http://` discovery row remains alongside canonical HTTPS; non-blocking.
6. **Free MCP bypass:** the standard public MCP currently exposes full determinations without payment and should be treated as a temporary developer-validation preview, not permanent commercial packaging.

## Next gates

1. Add privacy-minimal usage telemetry that excludes internal CI/smoke calls and never logs raw civic addresses.
2. Publish copy-paste HTTP, standard MCP and x402 MCP integration quickstarts plus developer-preview policy.
3. Target at least 20 developer/partner conversations across ServiceTitan, AppFolio, Procore/Autodesk, permit-automation and contractor/property Agent ecosystems.
4. Seek at least 3 external integrations, 100 non-owner external calls, one repeated integration with 20+ calls, and one buyer conversation accepting the commercial price range.
5. Do not expand mechanically to 20+ municipalities until there is 1,000 external calls/month, a credible platform path to 10k+ calls/month, or a paying/design partner requesting jurisdictions.
