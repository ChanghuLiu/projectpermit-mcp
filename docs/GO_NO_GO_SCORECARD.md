# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-28

Decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 51 / 100

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay / monetization fit | 15 | 4/10 | 6.0 | Filing/permit-ops buyers pay, but ProjectPermit's narrower `$0.20-$0.50` preflight hypothesis has **no E5 evidence**. More importantly, only 2/5 address-adapter jurisdictions currently consume property facts, so the assumed premium `address-aware` unit has a narrower present value base than previously believed. |
| Addressable call volume | 15 | 6/10 | 9.0 | Contractor/platform denominators are material, but Toronto broad MEP flow cannot be mapped safely to the current eight families. Toronto + Mississauga's strongest reproducible current-family-like public issued signal is only ~618-639/month, and even that is not upstream candidate volume. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated workflow can be larger. **E4 remains 0.** |
| Distribution fit | 10 | 5/10 | 5.0 | Real quote-first workflows exist, but no production integration partner exists. Registry/Bazaar/x402 payment plumbing proves discoverability and settlement capability, not buyer demand; a 2026 population-scale study also cautions that raw x402 settlement counts are heavily concentrated and often internal/fictitious. ProjectPermit itself still has E4=0 despite being discoverable. |
| Competitive headroom | 10 | 1/10 | 1.0 | GoBuild now independently embeds permit-needs prediction, current-local-code checks and cited sources inside contractor software; BuilderAI already embeds municipal urbanism in Quebec estimates; LandLogic/Parcella covers broad Ontario property/permit intelligence + partner APIs. Remaining whitespace for a standalone self-serve permit-specific API is extremely narrow and unvalidated. |
| Defensibility | 10 | 2/10 | 2.0 | Local rule replication is demonstrably cheap enough for focused checkers/vertical SaaS, and the build-vs-buy audit shows Toronto/Mississauga scope-only logic can currently be grounded in one primary rule/guidance source per city. Defensibility must come from externally valued cross-city maintenance, evidence/versioning, safety, accuracy history or embedded distribution—not rule ownership itself. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **50.5 -> 51** |  |

## Why the score moved 61 -> 59 -> 58 -> 57 -> 56 -> 53 -> 52 -> 51

### 61 -> 59: current-family volume correction

Toronto's broad Mechanical + Plumbing + Drain/Site permit flow (~1.7k issued revisions/month) was too broad to count toward the current product. City `WORK` labels show most of that volume as generic building-permit-related work that cannot be mapped safely into the existing eight families.

A deliberately conservative/non-exclusive Toronto current-family-like diagnostic is:

- 2023: **6,695/year = 557.9/month**;
- 2024: **6,690/year = 557.5/month**;
- 2025: **7,038/year = 586.5/month**.

Mississauga adds a cleaner `dwelling_change` signal from `SECOND UNIT` + `ADDITIONAL RESIDENTIAL UNITS`:

- 2023: **721/year = 60.1/month**;
- 2024: **775/year = 64.6/month**;
- 2025: **632/year = 52.7/month**.

Combined Toronto + Mississauga visible current-family-like issued signal is only about **618-639/month**. Vancouver's 888 residential-renovation records/year remain diagnostic only because the City label is merely `Addition / Alteration` and cannot be assigned safely to one current family.

Even the 618-639/month subtotal is not SAM: it is downstream permit-positive activity and does not measure upstream unresolved applicability.

### 59 -> 58: bundled Ontario checker competition

Build Smart Ontario places a free Permit Requirement Checker inside the same planning/estimating/quote funnel as its estimator and contractor lead flow. Its public guidance already covers many practical triggers also modeled by ProjectPermit, including like-for-like openings, deck height, plumbing relocation, structural changes, secondary suites and accessory-structure thresholds.

This reduced **competitive headroom from 5/10 to 4/10**. Generic `permit checker` functionality is already easy to bundle at zero visible marginal price.

### 58 -> 57: municipality-specific rule replication is also cheap

A further 2026 scan found independent Toronto/GTA contractor-side permit checkers such as Craft & Key and Installix. Installix exposes municipality/project-type decisions across 10 GTA municipalities with official links and conditions such as heritage/fire separation.

No public API/developer/white-label interface was found, so these tools do not occupy ProjectPermit's intended embedded B2B layer. But they show that a focused local contractor can reproduce municipality-specific + official-link logic as a free lead-generation feature.

That reduced **defensibility from 4/10 to 3/10**.

### 57 -> 56: current address-aware premium is narrower than assumed

A static audit now distinguishes address-adapter capability from actual rule-engine use of property facts.

ProjectPermit has address adapters for five cities:

- Gatineau
- Ottawa
- Toronto
- Mississauga
- Vancouver

But current deterministic rules consume adapter-relevant property facts in only:

- **Gatineau**: `heritage`, `piia`
- **Ottawa**: `heritage`

Toronto, Mississauga and Vancouver currently consume **no property facts** in permit-applicability decisions.

Therefore:

> **2 / 5 address-adapter jurisdictions = 40% currently have a permit decision path that can depend on adapter-derived property context.**

Laval and Longueuil rules read `piia`, but neither has a current address adapter.

See `docs/ADDRESS_AWARE_VALUE_AUDIT.md`.

This is not external willingness-to-pay evidence, but it removes an unsupported assumption behind the proposed paid unit. It is not defensible to treat every address lookup as premium value when three of five adapter cities currently produce the same permit determination regardless of adapter-derived property metadata.

Accordingly, **willingness-to-pay / monetization fit falls from 5/10 to 4/10**. A future increase requires E5 or representative evidence that municipality/property specificity materially changes enough real workflow decisions to support pricing.

### 56 -> 53: direct platform competition + embedded build-vs-buy threat

Two separate competitive findings materially narrowed the standalone API thesis.

**Ontario platform/API threat:** LandLogic now publicly shows an Ontario-wide property/planning/permit intelligence position spanning 80+ municipalities, partner APIs, white-label/embed capability and One Ontario permitting modernization. Parcella also directly enters `Do I need a permit?` / likely-permit questions. Public delivery is still assisted/tailored rather than a clearly self-serve permit-specific developer product, so the exact ProjectPermit contract is not proven redundant—but broad API access, external software buyers, cross-city maintenance and permit intelligence can no longer be treated as whitespace.

See `docs/LANDLOGIC_THREAT_ADDENDUM_20260828.md`.

**Embedded vertical-software threat:** BuilderAI's municipal urbanism tool is marked delivered and appears directly in a Quebec estimate/quote workflow. ConstructAI Toronto separately claims `permit requirements` plus an AI permit/regulation checker inside tender estimating, although its current evidence is beta/waitlist-level and delivery quality remains unverified.

See:

- `docs/BUILDERAI_QUEBEC_THREAT_ADDENDUM_20260828.md`
- `docs/CONSTRUCTAI_TORONTO_BETA_THREAT_20260828.md`
- `docs/EMBEDDED_BUILD_VS_BUY_SCAN_20260828.md`

A repository build-vs-buy audit then made the negative case more concrete. Across seven jurisdictions ProjectPermit has 155 deterministic rule IDs, but only 28 rule/guidance sources are needed for the scope-only shared ruleset; 14 additional sources are GIS/open-data context. At the single-city level, current Toronto and Mississauga scope-only logic each rests on **one primary rule/guidance source**, despite having 26-27 rule IDs.

See `docs/BUILD_VS_BUY_MAINTENANCE_BASELINE_20260828.md`.

Interpretation:

- a one-city/few-city embedded checker can be cheap enough to internalize;
- `we have deterministic municipal rules` is not a moat;
- ProjectPermit's remaining buy case is cross-city normalization + source drift + evidence/versioning + unknown-state safety + regression reliability + low-friction delivery;
- buyer preference for that external shared capability is still unproven.

Accordingly:

- **competitive headroom falls from 4/10 to 2/10**;
- **defensibility falls from 3/10 to 2/10**;
- total commercial score falls **56 -> 53**.

### 53 -> 52: x402 discovery/payment is not validated long-tail distribution

ProjectPermit already has working paid MCP/x402 plumbing, Registry/Bazaar discovery metadata and repeated external unpaid 402 probes, but **E4 remains 0**.

A July 2026 population-scale arXiv study of x402 activity on Base reported very high settlement counts while also finding extreme concentration and large internal/fictitious components; the authors explicitly caution that raw settlement count cannot be read directly as independent agent adoption.

See `docs/X402_DISTRIBUTION_REALITY_CHECK_20260828.md`.

This matters because build-vs-buy economics make high-volume vertical SaaS buyers more likely to consider internalizing a local checker. A natural fallback thesis would be that Registry/Bazaar/agent marketplaces aggregate lower-volume variable-geography buyers. That remains technically plausible, but there is currently no ProjectPermit E4 evidence and no reliable basis for assuming passive marketplace discovery will create meaningful independent paid volume.

Accordingly **distribution fit falls from 6/10 to 5/10**. x402 remains useful payment infrastructure; it should not be counted as validated distribution.

### 52 -> 51: GoBuild independently embeds near-exact permit intelligence

A targeted Canadian contractor-software scan found GoBuild publicly advertising an `AI permit & zoning intelligence` feature that:

- predicts the permits and drawings a job needs;
- checks current local code;
- provides cited sources;
- is embedded in the same contractor platform as estimates, proposals and job management;
- publicly shows a `Building permit — likely required (City of Toronto)` example;
- is included in the product's all-features subscription rather than presented as a separate metered permit API.

See `docs/EMBEDDED_BUILD_VS_BUY_SCAN_20260828.md`.

This is independent of BuilderAI and materially closer to ProjectPermit's intended output than permit search, permit-document storage or downstream filing tools. GoBuild does not publicly prove comparable accuracy, broad Canadian municipality coverage or a third-party permit API, but it demonstrates that `job/scope -> likely permits + current local code + cited sources` can already be an embedded contractor-software feature.

Accordingly **competitive headroom falls from 2/10 to 1/10**. Remaining whitespace is no longer the feature itself; it is only the narrower shared/self-serve/cross-city external capability contract and whether buyers prefer that over their embedded implementation.

## Municipality-specific technical value still exists

A separate synthetic discrimination audit should not be confused with this monetization/competition downgrade.

Across 15 identical address-free normalized scopes run through all seven supported jurisdictions:

- broad permit-positive vs permit-negative divergence: **9/15 = 60.0%**;
- strict `REQUIRED` vs `LIKELY_NOT_REQUIRED` divergence: **7/15 = 46.67%**;
- only one case was decisively unanimous across all seven cities.

Several major strict divergences were independently spot-checked against current first-party municipal guidance.

See `docs/MUNICIPAL_RULE_DIFFERENTIATION.md`.

Interpretation:

- municipality-specific rule logic has real **technical** value;
- property/address-specific value is currently much narrower in the implemented rules;
- neither synthetic result proves real workflow incidence, repeated usage or willingness to pay;
- technical non-uniformity does not prove buyers prefer an external API over a narrow internal checker.

The score therefore does not rise because the synthetic municipal matrix is favorable.

## Why this is not yet a No-Go

At 51/100 the project is now only one weighted point above the explicit stop zone. The remaining reason to continue is narrow:

- the product works technically;
- municipality-specific routing really can diverge;
- current operation remains cheap;
- no representative software buyer has yet answered the build-vs-buy question;
- no direct competitor has yet publicly demonstrated the exact combination of self-serve cross-city deterministic permit API + official rule/version contract + low-friction metered developer access across ProjectPermit's target geographies;
- the external validation stop clock is only 2/20 qualified human conversations.

This justifies **continued validation only**. It does not justify more product investment.

## Why this is not a Go-to-scale

The critical commercial facts remain missing:

1. How often is `permit required?` unresolved when a Request/assessment/estimate/quote is created?
2. How many of those events map to a current family?
3. Will software buyers call a separate API instead of building a narrow local checker/RAG or using embedded products like GoBuild/BuilderAI?
4. For buyers considering LandLogic/Parcella or internal RAG, what exact blocker makes ProjectPermit's narrower contract preferable?
5. How often does municipality-specific logic change a generic answer in representative real projects?
6. How often does derived address/property context materially change safe routing?
7. Will anyone pay the proposed price or commit integration resources?
8. Can accuracy stay high without a staffed expert operation?
9. If high-volume software buyers prefer internalization, can variable-geography agent/long-tail channels produce meaningful independent repeated usage rather than merely discovery/probes?

## What would move the score above 70

Any two or three of the following would materially upgrade the project:

- one genuine E2 workflow with **>=500 current-family candidate events/month** in covered geography;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- representative evidence that municipality-specific logic changes a material share of safe routing decisions;
- representative evidence that derived property/address context changes a material share of decisions;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 current-family candidate events/month** or equivalent proven aggregation;
- one E5 willingness-to-pay/resource commitment at a commercially useful price;
- representative software buyers explicitly preferring external cross-city deterministic maintenance over internal local RAG/checkers for a concrete cost/reliability reason;
- repeat paid usage from multiple unrelated agent/API buyers discovered without direct sales.

## What would move the score below 50

Serious stop signals include:

- 20 qualified conversations with no bounded repeated upstream applicability workflow;
- current-family upstream candidate volume remains too small when aggregated;
- representative E3 cases show material false-negative risk requiring expert review on most calls;
- permit necessity is usually known before the workflow reaches our insertion point;
- external users treat the tool as one-off research instead of infrastructure;
- free/general bundled checkers are considered sufficient;
- municipality specificity rarely changes the answer in representative work;
- property/address context rarely changes the answer;
- buyers will not pay for scope-only municipal preflight and the address-aware premium proves too rare;
- **multiple representative software buyers say they would simply build/maintain the relevant one-city/few-city checker internally**;
- **LandLogic, GoBuild or another competitor confirms an already-available low-friction/self-serve permit-specific API that adequately covers the target workflow/economics**;
- **agent/x402 discovery continues to produce only probes/one-off use rather than repeat independent workflows after credible exposure**;
- rule maintenance costs several hours/month per low-volume jurisdiction;
- buyers only value full filing/expediting and will not pay for preflight.

## Engineering freeze

Until external evidence pushes the score above 70:

**Do not:** add an eighth municipality; add U.S. coverage; add electrical/HVAC/mechanical families from public volume; build a third FSM adapter; add speculative property/GIS rules; add drawing/document QA; add filing/status/inspection operations; add human reviewer network; pay marketplace/listing fees; build consumer permit/zoning tools.

**Allowed:** bugs; validation-friction reduction; privacy/telemetry correctness; benchmark tooling; corrections that prevent overclaim; changes explicitly required by E2+/E3 partners.

## Current highest-value experiments

1. **Qualified human build-vs-buy responses** — current stop clock 2/20.
2. **Representative E3 divergence-sensitive cases** — especially basement/window/deck/accessory/plumbing/overlay boundaries.
3. **Platform volume + economics together** — a 10k-call partner only matters if it also explains why C$2.5k/month at `$0.25` is preferable to internal maintenance.
4. **External E4** — 20+ repeated operational calls from one real workflow.
5. **Exact competitor API check** — if an existing product exposes comparable self-serve permit-specific machine output at acceptable economics, stop earlier than the 20-conversation clock.

## Bottom line

ProjectPermit is now a **51/100 validation-only project**.

The feature/category is real, but most apparent moats have been falsified. The remaining thesis is only:

> **some buyers may still prefer a shared, self-serve, deterministic, cross-city permit capability over internal embedded AI/RAG because maintenance, evidence, safety and geography breadth are non-core.**

That thesis has no E2/E3/E4/E5 support yet. The next evidence must come from buyers or real usage, not more product work.