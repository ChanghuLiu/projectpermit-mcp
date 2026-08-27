# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-27

Decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 56 / 100

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay / monetization fit | 15 | 4/10 | 6.0 | Filing/permit-ops buyers pay, but ProjectPermit's narrower `$0.20-$0.50` preflight hypothesis has **no E5 evidence**. More importantly, only 2/5 address-adapter jurisdictions currently consume property facts, so the assumed premium `address-aware` unit has a narrower present value base than previously believed. |
| Addressable call volume | 15 | 6/10 | 9.0 | Contractor/platform denominators are material, but Toronto broad MEP flow cannot be mapped safely to the current eight families. Toronto + Mississauga's strongest reproducible current-family-like public issued signal is only ~618-639/month, and even that is not upstream candidate volume. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated workflow can be larger. **E4 remains 0.** |
| Distribution fit | 10 | 6/10 | 6.0 | Real quote-first contractor workflows exist, but permit-first workflows also exist. No production integration partner yet. |
| Competitive headroom | 10 | 4/10 | 4.0 | QwikScope, Permitio, Ampr and Ontario contractor-side permit checkers prove the category is already forming. The B2B API/evidence gap is narrower than initially assumed. |
| Defensibility | 10 | 3/10 | 3.0 | Idea/protocol/basic rule novelty is not a moat, and local contractors can already reproduce municipality-specific checkers with official links. Only externally benchmarked accuracy, meaningful property context, rule-change history and embedded distribution could become defensible assets. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **55.5 -> 56** |  |

## Why the score moved 61 -> 59 -> 58 -> 57 -> 56

### 61 -> 59: current-family volume correction

Toronto's broad Mechanical + Plumbing + Drain/Site permit flow (~1.7k issued revisions/month) was too broad to count toward the current product. City `WORK` labels show most of that volume as generic building-permit-related work that cannot be mapped safely to the existing eight families.

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

## Municipality-specific technical value still exists

A separate synthetic discrimination audit should not be confused with this monetization downgrade.

Across 15 identical address-free normalized scopes run through all seven supported jurisdictions:

- broad permit-positive vs permit-negative divergence: **9/15 = 60.0%**;
- strict `REQUIRED` vs `LIKELY_NOT_REQUIRED` divergence: **7/15 = 46.67%**;
- only one case was decisively unanimous across all seven cities.

Several major strict divergences were independently spot-checked against current first-party municipal guidance.

See `docs/MUNICIPAL_RULE_DIFFERENTIATION.md`.

Interpretation:

- municipality-specific rule logic has real **technical** value;
- property/address-specific value is currently much narrower in the implemented rules;
- neither synthetic result proves real workflow incidence, repeated usage or willingness to pay.

The score therefore does not rise because the synthetic municipal matrix is favorable.

## Workflow timing: quote-first exists, but is not universal

Public contractor processes show at least two real patterns.

Quote-first examples:

- TopDown Renovations: estimate -> written quote -> design -> permits;
- Nexon Build: discovery -> scope/fixed-price estimate -> design & permits;
- Crown Structural: detailed quotation including engineering/permit costs -> engineering -> permit submission.

Permit-first counterexample:

- WeRenovate.com requires permit-approved drawings before processing a construction estimate.

See `docs/QUOTE_STAGE_WORKFLOW_TIMING_EVIDENCE.md`.

Implication: ProjectPermit's intended quote-stage insertion point is real, but not universal. A platform's total quote count is not a call denominator until we know how many quotes still have unresolved permit applicability at that point.

## Why this is not a No-Go

ProjectPermit still has several unusually good solo-developer properties:

- very low marginal compute cost;
- no mandatory paid data license;
- no mandatory human reviewer/permit runner;
- real regulatory pain;
- a concrete quote/job integration point in some contractor workflows;
- municipality-specific rules genuinely can produce opposite safe routing outcomes;
- no dominant public Canadian B2B evidence-linked permit-applicability API/MCP has yet been identified.

## Why this is not a Go-to-scale

The critical commercial facts remain missing:

1. How often is `permit required?` unresolved when a Request/assessment/estimate/quote is created?
2. How many of those events map to a current family?
3. Will a workflow call a separate API instead of using a free bundled checker or human checklist?
4. How often does municipality-specific logic change a generic answer in representative real projects?
5. How often does derived address/property context materially change safe routing?
6. Will anyone pay the proposed price or commit integration resources?
7. Can accuracy stay high without a staffed expert operation?

Until those are answered, expanding cities/features only increases maintenance burden.

## What would move the score above 70

Any two or three of the following would materially upgrade the project:

- one genuine E2 workflow with **>=500 current-family candidate events/month** in covered geography;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- representative evidence that municipality-specific logic changes a material share of safe routing decisions;
- representative evidence that derived property/address context changes a material share of decisions;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 current-family candidate events/month** or equivalent proven aggregation;
- one E5 willingness-to-pay/resource commitment at a commercially useful price.

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
- rule maintenance costs several hours/month per low-volume jurisdiction;
- buyers only value full filing/expediting and will not pay for preflight.

## Engineering freeze

Until external evidence pushes the score above 70:

**Do not:**

- add an eighth municipality;
- add U.S. coverage;
- add electrical/HVAC/mechanical families based only on public permit volume;
- build a third FSM adapter;
- add speculative property/GIS rules merely to make existing adapters appear valuable;
- add drawings/document QA;
- add filing/status/inspection operations;
- add a human reviewer network;
- pay marketplace/listing fees merely for visibility;
- build consumer zoning/feasibility or standalone permit-checker features.

**Allowed engineering:**

- bugs;
- validation-friction reduction;
- privacy/telemetry correctness;
- benchmark tooling;
- corrections that prevent SAM/competition/monetization overclaim;
- changes explicitly required by an E2+/E3 partner.

## Current highest-value experiments

### A. Bounded estimator / quote denominator

For one recent complete month or fixed recent sample:

- relevant Requests/Assessments/Estimates/Quotes;
- current-family share;
- fraction where `permit required?` is still unresolved at first quote;
- who/what resolved the rest before quote.

### B. Generic checker vs municipality-specific value

Representative historical cases now have optional benchmark fields to record whether municipality specificity changed the safe answer. This does not affect E3 qualification.

Measure:

`cases where municipality-specific logic materially changed generic routing / representative current-family cases`

### C. Address/property incremental value

Measure separately:

`cases where derived property/address context materially changed safe routing / representative current-family cases`

Do not use `address was available`, `address lookup succeeded`, or `GIS data was returned` as substitutes for this metric.

### D. Platform threshold

Measure one recent month of covered-geography **current-family** candidate events. First threshold: **>=500/month**; then look for >=2,000/month aggregation and a credible path to 10,000 external preflights/month.

### E. E3 -> E4 -> E5 chain

Keep the evidence order strict:

`E2 bounded workflow -> E3 representative historical benchmark -> E4 repeated external usage -> E5 economic behavior`

No directory listing, polite reply, internal CI call, synthetic benchmark, successful address lookup or public permit count substitutes for that chain.

## Defensibility checkpoint

Do not score defensibility above 6/10 until at least one of these exists:

- repeated integration with real switching cost;
- externally benchmarked accuracy corpus;
- meaningful rule/source-change history;
- partner-specific normalization/routing embedded into operations;
- property/address context shown to matter in representative usage;
- enough observed production outcomes to prioritize and maintain rules better than a new entrant.

Basic permit trigger lists, municipality-specific educational checkers, API/MCP wrappers, unused GIS capability and idea novelty do **not** qualify as moat assets.

## Bottom line

ProjectPermit remains worth validating because municipality-specific permit applicability is demonstrably non-uniform and the operating-cost profile is excellent.

But the current commercial status is now:

> **promising low-cost capability, real municipal rule differentiation, unproven workflow volume, unproven distribution, weak current address-aware monetization, low current defensibility**

The next dollar/hour should buy **external workflow incidence, representative municipality-specific value, representative property-context value, and E5**, not more coverage.