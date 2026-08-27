# ProjectPermit Status

Updated: 2026-08-27

## Current state

**Seven-jurisdiction deterministic permit-preflight engine: LIVE.**

**Distribution validation: ACTIVE.** Replies are lead signals only. E3 representative historical benchmarks, E4 repeated external usage and E5 economic behavior remain the decision gates.

ProjectPermit is an evidence-linked cross-jurisdiction B2B/Agent permit-preflight layer. It is **not** a homeowner-only wizard, municipal application portal, managed permit-expediting service, legal opinion or municipal authorization.

The calling agent normalizes project scope into structured facts. The ProjectPermit rules engine does not call an LLM.

## Current jurisdiction coverage

- `gatineau_qc` — deterministic rules + municipal address geocoder
- `ottawa_on` — deterministic rules + address/zoning/heritage GIS
- `toronto_on` — deterministic rules + City address/zoning/heritage GIS
- `mississauga_on` — deterministic rules + City address/zoning/heritage/property GIS
- `laval_qc` — conservative deterministic rules; address/GIS adapter pending
- `longueuil_qc` — conservative deterministic rules; address/GIS adapter pending
- `vancouver_bc` — deterministic rules + City Open Data property-address/zoning/heritage adapter

Municipality expansion is paused until external workflow evidence justifies maintenance.

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP developer-validation preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Current Base Sepolia discovery price is `$0.01 USDC/call`; this is not the intended commercial price.

Real buyer-side HTTP and MCP x402 settlement have already been proven. Do not spend test USDC merely to re-prove payment plumbing.

## Core infrastructure completed

- 7-jurisdiction deterministic router across 8 normalized project families
- 5 first-party municipal/open-data address resolver jurisdictions
- shared address-aware preflight service for HTTP/free MCP/paid MCP
- official evidence + stable rule ids
- FastAPI + MCP v2 + x402-native MCP
- privacy-minimal structured usage telemetry
- CI/owner traffic tagging
- municipal request URL logging suppression to reduce address/query leakage
- Docker + GitHub Actions CI
- no paid municipal/property data dependency
- no server-side LLM dependency

## Validation evidence standard

See `docs/VALIDATION_EVIDENCE_STANDARD.md`.

- **E0** — no usable evidence / routing / auto-reply
- **E1** — opinion only
- **E2** — bounded workflow claim with denominator + timeframe + workflow location
- **E3** — representative anonymized historical cases benchmarked against ProjectPermit
- **E4** — observed repeated external usage
- **E5** — economic behavior / paid or resource-committed integration

Synthetic/de-identified platform benchmarks and public municipal permit-positive backtests are technical evidence only. They do **not** count as E3/E4.

## External usage baseline

Initial post-telemetry baseline:

- external/non-owner successful preflight calls: **0**
- internal CI/smoke successful events at initial capture: **32**
- external integrations/client tags: **0**

Post-outreach Railway audit on 2026-08-27:

- free/standard MCP successful usage: internal CI/owner smoke only
- paid x402 MCP successful external usage: **0**
- paid HTTP/API-v2 successful external usage: **0**
- unpaid `402 Payment Required` probes are present but do **not** count as E4
- countable E4 external successful preflights remains **0**

Do not count replies, crawlers, synthetic benchmarks, CI, owner smoke, demos or unpaid 402 probes as demand.

## Outreach state

Sent on 2026-08-27:

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
- Jobber API support / Marketplace-testing eligibility question sent to `api-support@getjobber.com`

Prepared, not submitted because the route is interactive/form-based:
- Lula
- ServiceChannel

Latest Gmail check found no reply or delivery-failure message from the current outreach set. Work continues without waiting.

## Platform strategy — keep scale separate from ease of integration

See `docs/PLATFORM_DISTRIBUTION_SCORECARD.md`.

### Commercial distribution priority

**#1 Jobber** remains the strongest current fit because of Canadian relevance, home-service workflow, address + Request/Quote/Job scope, and large platform footprint.

**ServiceTitan** has the strongest annual workflow-density signal reviewed so far — 12,000+ businesses and 40M+ jobs/year — but ProjectPermit is Canada-only while ServiceTitan is U.S.-heavy. Do not add U.S. cities without partner-linked volume.

**Workiz / Housecall Pro** remain credible large-platform candidates. Workiz currently states 120k+ home-service pros in the US and Canada; Housecall Pro states 200k+ pros / 45k+ businesses. Access/geography evidence is not yet strong enough to justify another adapter now.

**ServiceM8 commercial scale is intentionally unproven.** Its Canadian account denominator is unknown, so do not promote it merely because its API is easy to use.

### Immediate low-cost technical validation priority

1. **Jobber** — adapter/client/benchmark done; manual Developer Center token/live-schema gate remains.
2. **ServiceM8** — adapter/client/benchmark done; manual own-account Read Only API-key gate remains.
3. **Workiz** — only if the first two paths become blocked/weak or new evidence justifies it.
4. **ServiceTitan** — high leverage, but developer-access approval required.
5. **Housecall Pro** — high scale, but less attractive low-cash API-access path.

Stop adapter proliferation after Jobber + ServiceM8 unless a new platform brings credible E2+/E3 access or a 500+/month candidate-call path.

## Jobber — #1 current commercial wedge

Preferred flow:

`Jobber Quote/Job -> property address + title/line items -> structured ProjectPermit facts -> preflight -> proposed routing/write-back metadata`

Completed:

- read-only Jobber adapter
- no-mutation GraphQL client
- token-safe error handling
- account probe
- developer bootstrap docs
- **20-case synthetic/de-identified integration benchmark across all 8 project families**
- runnable synthetic benchmark command
- E3 historical benchmark template

Important testing rule: Jobber's current Marketplace-oriented testing guidance says not to engage existing Jobber customers to test before coordinating with a Jobber developer representative. The prepared Canadian operator cohort therefore remains research/future-E3 only.

Next Jobber technical gate requires interactive account work:

1. create/use Jobber developer testing account;
2. create Developer Center Draft app;
3. obtain GraphiQL testing token;
4. run `scripts/jobber_readonly_probe.py`;
5. verify exact live Request/Quote/Job/Property/line-item fields;
6. bind those verified fields without enabling mutations.

See:
- `docs/JOBBER_DEVELOPER_BOOTSTRAP.md`
- `docs/JOBBER_DISTRIBUTION_WEDGE.md`
- `docs/JOBBER_OPERATOR_VALIDATION.md`

## ServiceM8 — #2 immediate technical wedge

ServiceM8 provides a materially different and lower-friction live-account test path.

Official current docs establish:

- Private Applications may connect to the developer's own account / one specific customer via API key;
- a Developer account is not required for that private path;
- API key uses `X-API-Key`;
- ServiceM8 explicitly supports a **Read Only** API-key type;
- public apps later use OAuth 2.0;
- Free plan is `$0/month`, 1 user, up to 30 jobs/month;
- Job records expose `uuid`, `status`, `job_address`, `job_description`;
- documented status values include `Quote`, `Work Order`, `Unsuccessful`, `Completed`.

Completed on `main`:

- `src/projectpermit/servicem8_adapter.py`
- `src/projectpermit/servicem8_client.py` — GET-only, no POST/DELETE methods
- token/body-safe error handling
- `scripts/servicem8_readonly_probe.py`
- `docs/SERVICEM8_DEVELOPER_BOOTSTRAP.md`
- `docs/SERVICEM8_DISTRIBUTION_WEDGE.md`
- **12-case synthetic/de-identified benchmark across all 8 project families**
- runnable ServiceM8 benchmark command
- tests enforcing exclusion of customer UUID, billing, contact, payment, price and cost data

Full CI after the ServiceM8 adapter/client/benchmark addition: **PASS** on Python 3.11/3.13, container, remote MCP, paid challenge, HTTP Bazaar challenge and optional integrations.

Next ServiceM8 live gate:

1. create/sign in to a ServiceM8 account;
2. verify whether the Free-plan UI shows `Account -> Settings -> API Keys`;
3. if available, create **Read Only** key named `ProjectPermit Read Only Validation`;
4. do not upgrade/pay if the Free plan hides API keys;
5. store key locally only as `SERVICEM8_API_KEY`;
6. create several obviously synthetic Quote/Work Order jobs;
7. run `python scripts/servicem8_readonly_probe.py`.

This live own-account test is technical evidence only, not E3/E4.

## Municipal first-party substitution

See:
- `docs/MUNICIPAL_SELF_SERVICE_COMPETITION.md`
- `docs/GATINEAU_URBAIN_COMPETITIVE_BOUNDARY.md`

Current pattern:

- **Gatineau URBAIN:** Level-4-style direct address/project-aware permit eligibility assistant; strongest homeowner substitution risk.
- **Toronto:** AI Building Permit Application Pre-Check for eligible residential application documents; downstream application-review competition rather than initial eligibility routing.
- **Longueuil:** meaningful online application/selected automated issuance workflow.
- **Ottawa / Mississauga / Laval / Vancouver:** strong digital guidance/property/application tooling; no equivalent integrated URBAIN-style eligibility assistant was identified in the official material reviewed on 2026-08-27.

Strategic boundary:

- no homeowner destination app as priority;
- no municipal application portal clone;
- no full drawing/document code review without independent B2B evidence;
- keep differentiation in cross-jurisdiction schema, embedded contractor workflow, API/MCP delivery and normalized first-party evidence.

Before adding/deepening any city, check for first-party eligibility assistants, automated issuance and AI/document pre-checks.

## Technical correctness guards

### Vancouver permit-positive backtest

A 10-case first-party public permit-positive fixture is committed with residential addresses/contact details intentionally omitted.

Regression requirement: known permit-positive scopes must never be classified `LIKELY_NOT_REQUIRED` by the mapped structured facts.

This is a technical false-negative guard, not market E3.

### Platform benchmarks

- Jobber: 20 synthetic/de-identified cases, all 8 project families
- ServiceM8: 12 synthetic/de-identified cases, all 8 project families

Both verify adapter -> structured facts -> engine -> proposed routing metadata without platform mutation or market-evidence inflation.

## Objective municipal activity baseline

Clean first-party 2024 counts established:

- Toronto: **36,887** building permits issued (~3,074/month)
- Ottawa: **7,688** (~641/month)
- Mississauga: **4,458** (~372/month)
- Laval: **1,415** construction + improvement permits (~118/month), including **1,111 improvement permits**

Combined clean observed issuance floor: **50,448/year**, ~**4,204/month**.

Vancouver's first-party dataset contains 51k+ issued-building-permit records since 2017, roughly half categorized Addition / Alteration. Exact Gatineau annual cumulative extraction and Longueuil distinct-permit extraction remain pending; do not invent counts merely to fill the table.

This reinforces that a 10k-calls/month product cannot rely on `one call only after a permit is already known to be required`. The commercial wedge must prove a broader `candidate quote/work order -> preflight` multiplier through E3/E4.

## Commercial checkpoint

Working price hypothesis remains roughly **$0.20-$0.50 per address-aware evidence-linked preflight**, subject to E5.

First meaningful internal scale checkpoint: **~10,000 external successful preflights/month**.

Equivalent shapes include:

- 500 contractor businesses × 20 candidate calls/month
- 125 × 80/month
- 20 integrations × 500/month
- 5 integrations × 2,000/month
- one platform workflow × 10,000/month

At $0.25/call this is $2,500 gross/month; at $0.50/call $5,000 gross/month, before infrastructure, support and municipal-rule maintenance.

## Next gates

### Technical

- live Jobber developer-account/token/schema probe
- live ServiceM8 Free-account Read Only API-key probe
- do not build a third field-service adapter without new evidence

### Market

- 2 independent representative E3 historical benchmarks
- 1 repeated external workflow with 20+ successful calls
- 3 external integrations + 100+ non-owner successful calls
- one credible workflow with 500+ candidate calls/month
- one partner/integration with 2,000+ candidate calls/month
- one credible path to 10,000+ calls/month
- one E5 price/resource commitment around the working unit economics

### Geography

- add/deepen municipalities only when requested geography is tied to credible repeated volume and passes the municipal-self-service substitution check

GitHub issue #1, `Validate external distribution before expanding municipalities`, remains the canonical validation checklist.
