# ProjectPermit Status

Updated: 2026-08-27

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

**Phase 1A Toronto + Mississauga expansion: PASS.** Both cities have deterministic rule coverage plus first-party municipal address/zoning/heritage adapters.

**Phase 1B Laval + Longueuil six-city expansion: PASS.** Conservative deterministic rule coverage is publicly verified.

**Phase 1C Vancouver seven-city expansion: PASS.** Vancouver rules plus first-party City address/zoning/heritage resolution are deployed and verified against the public MCP service.

**Distribution-validation instrumentation and partner pilot package: READY.** External outreach is the next real gate; messages are prepared but remain unsent pending explicit approval of sender identity/contact details and outreach.

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

The seven-city public MCP test performs deterministic rule checks for all supported jurisdictions and a real address-aware Vancouver call against City open data. The Vancouver production verification resolved:

- matched address: `453 W 12TH AV`
- zoning: `CD-1 (46)`
- result: `vancouver_address_aware_preflight=PASS`

No paid smoke transaction is required for routine expansion verification. Real buyer-side HTTP and MCP x402 settlement were already proven earlier.

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
- privacy-minimal structured usage telemetry
- internal CI/owner traffic tagging so it cannot be mistaken for demand
- municipal `httpx/httpcore` request URL logging suppressed to avoid leaking address/query details
- no server-side LLM dependency
- no paid map/property-data dependency

## Verification policy

Real buyer-side x402 plumbing is already proven. **Do not spend additional test USDC for routine expansion smoke tests.** Expansion verification should use free discovery or unpaid 402 challenges.

Final canonical-HTTPS Phase 0 HTTP settlement transaction:

`0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`

## External usage baseline

A clean post-telemetry baseline was captured before outreach:

- successful external/non-owner preflight calls: **0**
- successful internal CI/smoke preflight events observed: **32**
- external integrations/client tags: **0**

The zero-external baseline is expected because targeted outreach has not been sent. Internal events are explicitly marked `internal_traffic=true` and are excluded from market validation.

See `docs/EXTERNAL_USAGE_BASELINE.md` and `scripts/summarize_usage_logs.py`.

## Market decision

The commercial thesis is a **cross-jurisdiction B2B/Agent permit-requirements intelligence layer**, not a homeowner-only wizard and not a managed permit-submission service.

The current seven-city footprint is enough to validate distribution. Municipality expansion is intentionally paused until repeated external usage or a design-partner request justifies more maintenance.

The working commercial hypothesis remains roughly **$0.20-$0.50 per address-aware evidence-linked preflight** or an equivalent platform volume plan, subject to external willingness-to-pay validation.

The first commercially meaningful internal checkpoint is roughly **10,000 external preflight calls/month**. Preferred proof shapes include:

- 5 integrations × ~2,000 calls/month;
- 20 integrations × ~500 calls/month;
- one platform workflow × ~10,000 calls/month.

This is a validation threshold, not a revenue forecast. At 10k monthly calls, gross revenue would be about $2,500 at $0.25/call or $5,000 at $0.50/call before infrastructure, support and municipal-rule maintenance.

## Distribution evidence now driving the next phase

Current public platform signals include:

- U.S. construction: 814,557 employer establishments in 2023 County Business Patterns
- Canada construction: 159,514 employer + 255,892 non-employer/indeterminate establishments in 2025
- ServiceTitan: 12,000+ businesses and 40M+ jobs completed annually
- Procore: 17,850 customers at 2025 year-end
- AppFolio: 22,096 property-management customers and 9.4M units under management at 2025 year-end
- Autodesk Construction: used by builders on 2M+ projects

These numbers are distribution-surface indicators, not additive TAM.

Observed workflow evidence also shows permit work can be repeated and operationally costly. One public iPermit/ServiceTitan contractor testimonial reports roughly **80+ permit jobs/month**. Community reports show multi-jurisdiction contractors dealing with different replacement/new-install permit rules and construction teams maintaining permit tracking outside core systems. These anecdotes justify validation conversations but are not converted into market-size claims.

See `docs/PAIN_EVIDENCE.md`.

## External-validation assets completed

- `data/partner_targets.csv` — 20 contact-ready target accounts
- `docs/TARGET_ACCOUNT_RANKING.md` — ranking by pain proximity, repeat density, integration readiness and distribution leverage
- `docs/OUTREACH_BATCH_01.md` — tailored first 10 outreach drafts, **prepared but not sent**
- `docs/PARTNER_OUTREACH.md` — discovery questions and response qualification
- `docs/DESIGN_PARTNER_TRIAL.md` — 20-case, no-wallet developer pilot
- `data/design_partner_scope_template.csv` — anonymized pilot scope template
- `data/partner_feedback.csv` — structured conversation/call-volume/price feedback tracker
- `scripts/summarize_partner_feedback.py` — evidence/gate summarizer
- `docs/CALL_VOLUME_THRESHOLDS.md` — bottom-up monthly call model
- `docs/EXTERNAL_USAGE_BASELINE.md` — zero-external starting baseline
- `docs/INTEGRATION_QUICKSTART.md` — HTTP/MCP/x402 developer instructions

GitHub issue #1, `Validate external distribution before expanding municipalities`, is the canonical validation checklist.

## Recommended first conversations

The first wave intentionally tests different workflow layers rather than only direct permit competitors:

1. iPermit — full downstream permit workflow
2. ServiceChannel — facilities work-order intake
3. Property Meld — property maintenance coordination
4. Lula — maintenance contractor network / Partner API
5. HappyCo or AppWork — multifamily maintenance/inspection workflow
6. Provizual — AHJ/inspection workflow inside Procore
7. PermitFlow — full permitting platform / upstream-routing hypothesis
8. SyncEzy or Calance — integration consultancy with multi-customer leverage

External messages should not be sent until sender identity/contact details and outreach are explicitly approved.

## Known unresolved items

1. **Laval/Longueuil property adapters:** rule coverage exists; stable no-cost address/zoning/overlay resolution should be evaluated only if usage justifies it.
2. **Gatineau PIIA/heritage:** public mapping confirms the concepts/layers but a stable unauthenticated machine endpoint is not yet locked. Unknown must never become false.
3. **Longueuil exemptions:** current simplified material describes permit workflows more clearly than universal exemptions, so conservative outcomes remain intentional.
4. **Mainnet:** intentionally disabled until external demand and willingness-to-pay validation pass.
5. **External Bazaar stale row:** historical `http://` discovery row remains alongside canonical HTTPS; non-blocking.
6. **Free MCP bypass:** the standard public MCP currently exposes full determinations without payment and should be treated as a temporary developer-validation preview, not permanent commercial packaging.
7. **Geographic overlap:** the strongest ServiceTitan distribution surface is U.S.-heavy while current rules are Canada-only. U.S. jurisdictions should be added only when a partner attaches credible repeated call volume to specific cities.

## Next gates

Completed before outreach:

- privacy-minimal telemetry and internal-smoke exclusion — **DONE**
- municipal request-log privacy guard — **DONE**
- developer integration quickstart — **DONE**
- 20-account target list and ranking — **DONE**
- first 10 tailored outreach drafts — **DONE**
- 20-case design-partner pilot package — **DONE**
- call-volume/pricing threshold model — **DONE**
- external usage baseline — **DONE**

The next actual market gates are:

1. obtain explicit approval for sender identity/contact details and external outreach;
2. run the first 8-10 workflow-diverse conversations;
3. obtain at least 2 organizations willing to provide anonymized real scopes or one integration with 20+ calls;
4. reach 3 external integrations and 100+ non-owner successful preflight calls;
5. identify one partner/integration with 2,000+ candidate calls/month;
6. validate one credible path to 10,000+ calls/month;
7. get at least one buyer/partner reaction that `$0.20-$0.50` address-aware unit economics are acceptable;
8. add new jurisdictions only when partner-requested volume justifies the maintenance burden.
