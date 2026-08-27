# ProjectPermit Status

Updated: 2026-08-27

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

**Phase 1A Toronto + Mississauga expansion: PASS.** Both cities have deterministic rule coverage plus first-party municipal address/zoning/heritage adapters.

**Phase 1B Laval + Longueuil six-city expansion: PASS.** Conservative deterministic rule coverage is publicly verified.

**Phase 1C Vancouver seven-city expansion: PASS.** Vancouver rules plus first-party City address/zoning/heritage resolution are deployed and verified against the public MCP service.

**Distribution validation: ACTIVE.** External outreach has started. Replies are lead signals only; E3 historical benchmarks, E4 repeated external usage and E5 economic behavior are the decision gates.

ProjectPermit is an evidence-linked deterministic municipal permit-preflight engine across seven jurisdictions. The calling Agent normalizes project scope; the server applies municipal rules and returns official-source evidence. The rules engine does not call an LLM and payment remains outside BuildRequirements.

## Jurisdiction coverage

- `gatineau_qc` — deterministic rules + municipal address geocoder; PIIA/heritage machine overlays still unresolved
- `ottawa_on` — deterministic rules + address/zoning/heritage GIS
- `toronto_on` — deterministic rules + City address/zoning/heritage GIS
- `mississauga_on` — deterministic rules + City address/zoning/heritage/property GIS
- `laval_qc` — conservative deterministic rules; address/GIS adapter pending
- `longueuil_qc` — conservative deterministic rules; address/GIS adapter pending
- `vancouver_bc` — deterministic rules + City Open Data property-address/zoning/heritage adapter

All transports call the same `preflight_service` before the jurisdiction router. For supported address jurisdictions, `resolve_address=true` enriches the request with first-party municipal property context. Laval and Longueuil currently use `resolve_address=false`.

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP developer-validation preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Current **testnet discovery price**: **$0.01 USDC per paid tool/API call** on Base Sepolia. This is not the intended commercial price.

Real buyer-side HTTP and MCP x402 settlement have already been proven. Do not spend additional test USDC merely to re-prove plumbing.

## Completed infrastructure

- seven-jurisdiction deterministic rule router across 8 normalized project families
- five first-party municipal/open-data address resolver jurisdictions
- shared address-aware preflight service for HTTP/free MCP/paid MCP
- official evidence and stable rule ids
- public FastAPI, standard MCP v2 and x402-native paid MCP
- Base Sepolia x402 payment profile and real buyer-side settlement verification
- GoPlausible Bazaar canonical HTTPS indexing
- Docker + GitHub Actions CI
- privacy-minimal structured usage telemetry
- internal CI/owner traffic tagging so it cannot be mistaken for demand
- municipal request-URL logging suppression to avoid leaking address/query details
- no server-side LLM dependency
- no paid map/property-data dependency
- read-only Jobber Request/Quote/Job adapter + tests
- read-only Jobber GraphQL transport + tests
- Jobber no-mutation account probe
- Jobber developer/test-account bootstrap instructions
- **20-case synthetic/de-identified Jobber integration benchmark across all 8 project families**
- runnable Jobber synthetic benchmark summary command
- Jobber E3 historical benchmark template
- Vancouver 10-case public permit-positive false-negative backtest
- Gatineau URBAIN first-party competitive-boundary analysis

Latest CI on `main` after these additions: **PASS**.

## Outreach state

Direct emails sent on 2026-08-27:

**Batch A**
- iPermit
- Provizual
- AppWork
- SyncEzy

**Batch B**
- Calance
- Outbuild
- PermitFlow
- Pulley

**Platform technical validation**
- Jobber API support — Marketplace/API eligibility question sent to `api-support@getjobber.com`

Prepared but not submitted because the current route is interactive/form-based:
- Lula
- ServiceChannel

Sender identity is now ProjectPermit. No further product work is blocked on replies.

## Validation evidence standard

See `docs/VALIDATION_EVIDENCE_STANDARD.md`.

- **E0:** no usable evidence / routing / auto-reply
- **E1:** opinion only
- **E2:** bounded workflow claim with denominator + timeframe + workflow location
- **E3:** representative anonymized historical cases benchmarked against ProjectPermit
- **E4:** observed repeated external usage
- **E5:** economic behavior / paid or resource-committed integration

A positive reply is not market validation. Major coverage, product-boundary, mainnet and pricing decisions should not be made from E0/E1.

Synthetic/de-identified integration benchmarks and public municipal permit-positive backtests are technical evidence only. They do **not** count as E3/E4.

## External usage baseline

Initial post-telemetry baseline before outreach:

- successful external/non-owner preflight calls: **0**
- successful internal CI/smoke events observed at initial capture: **32**
- external integrations/client tags: **0**

Post-outreach Railway audit on 2026-08-27:

- standard/free MCP successful usage events observed: internal CI/owner-smoke only
- paid x402 MCP successful usage events: **0**
- paid HTTP/API-v2 successful usage events: **0**
- API-v2 has received unpaid `402 Payment Required` probes; these do **not** count as E4
- countable E4 external successful preflight calls remains **0**

Do not count CI, owner smoke, demos, synthetic loads, unpaid 402 probes, discovery/crawler traffic or replies as E4.

## Market decision

The commercial thesis remains a **cross-jurisdiction B2B/Agent permit-requirements intelligence layer**, not a homeowner-only wizard and not a managed permit-submission service.

The seven-city footprint is enough to validate distribution. Municipality expansion remains paused until representative E3 cases plus a credible repeated E4 call path justify maintenance.

Working commercial hypothesis: roughly **$0.20-$0.50 per address-aware evidence-linked preflight** or an equivalent platform volume plan, subject to E5 validation.

The first commercially meaningful internal checkpoint remains roughly **10,000 external preflight calls/month**. Example proof shapes:

- 5 integrations × ~2,000 calls/month
- 20 integrations × ~500 calls/month
- one platform workflow × ~10,000 calls/month

At 10k monthly calls, gross revenue would be about $2,500 at $0.25/call or $5,000 at $0.50/call before infrastructure, support and municipal-rule maintenance.

## First-party municipal assistant risk: Gatineau URBAIN

Ville de Gatineau now operates **URBAIN**, a first-party address-aware/project-aware urban-planning assistant. The City says it uses structured questions, applies regulations according to project location, indicates whether a permit is required, provides applicable standards and routes complex cases to municipal staff. Further modules are planned through 2027.

This is a direct substitution risk for a **single-city homeowner permit checker** and a strong reason not to move ProjectPermit toward that product shape.

It does **not** currently establish a public machine-to-machine developer API. The correct finding is only that no public developer/API surface was identified in the official material reviewed so far; do not claim one does not exist.

ProjectPermit differentiation must remain:

- cross-jurisdiction normalization;
- embedded contractor/platform workflow;
- API/MCP delivery;
- common evidence/rule schema;
- repeat portfolio volume;
- fail-safe uncertainty rather than municipal-authority claims.

See `docs/GATINEAU_URBAIN_COMPETITIVE_BOUNDARY.md`.

## Objective activity baseline

First-party 2024 counts already established for four supported cities:

- Toronto: **36,887** building permits issued (~3,074/month)
- Ottawa: **7,688** (~641/month)
- Mississauga: **4,458** (~372/month)
- Laval: **1,415** construction + improvement permits (~118/month), including **1,111 improvement permits**

Combined clean observed issuance flow: **50,448/year**, about **4,204/month**.

Vancouver's first-party issued-building-permits dataset contains 51k+ records since 2017, with roughly half currently categorized as Addition / Alteration. Gatineau annual cumulative extraction and Longueuil distinct-permit extraction remain pending.

This is an activity floor, not ProjectPermit call volume. It reinforces that a 10k-calls/month business cannot rely on `one call only after a permit is already known to be required`; the intended wedge must preflight a broader stream of candidate quotes/work orders/scopes.

See `docs/MUNICIPAL_ACTIVITY_BASELINE.md`.

## Highest-priority wedge: Jobber

Jobber is currently the top distribution experiment because Request/Quote/Job objects can expose property address plus structured scope before a job is committed.

Preferred workflow:

`Jobber Quote/Job -> address + title/line items -> structured ProjectPermit facts -> preflight -> proposed custom-field writeback`

### Current Jobber state

- API/Marketplace eligibility question — **SENT; not a sandbox blocker**
- read-only adapter + unit tests — **DONE**
- read-only GraphQL client that rejects mutation/subscription — **DONE**
- one-command account probe — **DONE**
- developer/test-account bootstrap path — **DOCUMENTED**
- 20-case synthetic/de-identified integration benchmark — **DONE; all 8 project families**
- external existing-customer Jobber testing — **ON HOLD until coordinated with a Jobber developer representative**

Jobber's current testing guidance says that an app intended for Marketplace publication should not engage existing Jobber customers for testing before coordinating with a Jobber developer representative. The separate rule allowing a Draft custom integration to connect to up to five paying accounts does not override that testing guidance.

### Current sequence

1. create/use a Jobber developer testing account + Developer Center Draft app + GraphiQL testing token — **CURRENT MANUAL SANDBOX STEP**
2. run the read-only account probe and verify exact live Request/Quote/Job/Property/line-item fields — **NEXT TECHNICAL GATE**
3. bind the verified live schema into the query layer and rerun the existing 20-case integration contract — **NEXT AFTER SCHEMA**
4. after Jobber customer-testing coordination, obtain 20+ representative historical Canadian cases from independent operators — **E3 GATE**
5. only then run an authorized repeat-use pilot — **E4 GATE**
6. Marketplace investment only after E3/E4 shows repeated permit-sensitive volume

Keep mutation disabled until the read-only mapping is benchmarked and external testing is authorized appropriately.

See `docs/JOBBER_DEVELOPER_BOOTSTRAP.md`, `docs/JOBBER_DISTRIBUTION_WEDGE.md`, and `docs/JOBBER_OPERATOR_VALIDATION.md`.

## Known unresolved items

1. **Laval/Longueuil property adapters:** evaluate only if usage justifies them.
2. **Gatineau PIIA/heritage:** stable unauthenticated machine overlay endpoint is not yet locked; unknown must never become false. URBAIN increases the case for not investing here before external API volume exists.
3. **Longueuil exemptions:** conservative outcomes remain intentional where simplified official material does not establish universal exemptions.
4. **Mainnet:** intentionally disabled until external demand and willingness-to-pay validation pass.
5. **External Bazaar stale row:** historical `http://` discovery row remains alongside canonical HTTPS; non-blocking.
6. **Free MCP bypass:** full determinations are temporarily free for developer validation; this is not permanent commercial packaging.
7. **Geographic overlap:** strong U.S. platform distribution does not justify U.S. city expansion without E3/E4-backed volume.
8. **Municipal first-party substitution:** check each new city for an official address-aware permit assistant before adding homeowner-oriented product work.

## Next gates

- complete the Jobber internal developer/test-account account + live-schema probe
- bind verified live Jobber Request/Quote/Job fields without enabling mutations
- obtain **2 independent representative E3 historical benchmarks** after the relevant platform/customer-testing route is cleared
- reach **1 repeated external workflow with 20+ successful calls**
- reach **3 external integrations and 100+ non-owner successful calls**
- identify **one workflow with 500+ candidate calls/month**
- identify **one partner/integration with 2,000+ candidate calls/month**
- validate **one credible platform path toward 10,000+ calls/month**
- obtain an **E5 economic signal** around the $0.20-$0.50 address-aware unit economics or equivalent resource commitment
- add new jurisdictions only when requested geography is tied to credible volume and preferably E3/E4 evidence

GitHub issue #1, `Validate external distribution before expanding municipalities`, is the canonical validation checklist.
