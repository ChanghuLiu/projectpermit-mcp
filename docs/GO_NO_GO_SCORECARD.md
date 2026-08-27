# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-27

Decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 57 / 100

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay | 15 | 5/10 | 7.5 | Filing/permit-ops buyers pay, but ProjectPermit's narrower `$0.20-$0.50` per-call hypothesis has **no E5 evidence** yet. |
| Addressable call volume | 15 | 6/10 | 9.0 | Contractor/platform denominators are material, but Toronto broad MEP flow cannot be mapped safely to the current eight families. Toronto + Mississauga's strongest reproducible current-family-like public issued signal is only ~618-639/month, and even that is not upstream candidate volume. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated workflow can be larger. **E4 remains 0.** |
| Distribution fit | 10 | 6/10 | 6.0 | Real quote-first contractor workflows exist, but permit-first workflows also exist. No production integration partner yet. |
| Competitive headroom | 10 | 4/10 | 4.0 | QwikScope, Permitio, Ampr and Ontario contractor-side permit checkers prove the category is already forming. The B2B API/evidence gap is narrower than initially assumed. |
| Defensibility | 10 | 3/10 | 3.0 | Idea/protocol/basic rule novelty is not a moat, and local contractors can already reproduce municipality-specific checkers with official links. Only externally benchmarked accuracy, address adapters, rule-change history and embedded distribution could become defensible assets. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **57.0 -> 57** |  |

## Why the score moved 61 -> 59 -> 58 -> 57

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

Municipality-specific differentiation can still matter. For example, broad Ontario basement guidance is often conservative, while Toronto's current official guidance exempts a house basement finish when there are no structural/material alterations, no additional dwelling unit and no new plumbing.

### 58 -> 57: municipality-specific rule replication is also cheap

A further 2026 scan found two independent Toronto/GTA contractor-side permit checkers:

- **Craft & Key**: a free Toronto permit checker using four scope questions and Toronto-specific thresholds before the homeowner starts planning;
- **Installix Windows & Doors**: an instant GTA window/door permit checker covering 10 municipalities, with project-type choices, heritage/fire-separation conditions and official municipal links.

No public API/developer/white-label interface was found for these tools, so they do not occupy ProjectPermit's intended embedded B2B distribution layer.

However, Installix demonstrates that a focused local contractor can reproduce **municipality-specific + official-link decision logic** across many cities as a free lead-generation feature. Therefore the maintained rule corpus itself should no longer be treated as a meaningful moat.

That reduces **defensibility from 4/10 to 3/10**.

Future defensibility must come from cumulative external assets that a new entrant cannot instantly copy:

1. independently benchmarked historical accuracy and false-negative history;
2. maintained source/rule change history over time;
3. address/property adapters tied to first-party municipal data;
4. partner-specific normalization/routing embedded into real operations;
5. repeated production usage and distribution agreements;
6. evidence that those differentiated outputs materially change workflow decisions.

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
- municipality-specific differences can materially change outcomes;
- no dominant public Canadian B2B evidence-linked permit-applicability API/MCP has yet been identified.

## Why this is not a Go-to-scale

The critical commercial facts remain missing:

1. How often is `permit required?` unresolved when a Request/assessment/estimate/quote is created?
2. How many of those events map to a current family?
3. Will a workflow call a separate API instead of using a free bundled checker or human checklist?
4. How often does municipality/address-specific context change the generic answer?
5. Will anyone pay the proposed price or commit integration resources?
6. Can accuracy stay high without a staffed expert operation?

Until those are answered, expanding cities/features only increases maintenance burden.

## What would move the score above 70

Any two or three of the following would materially upgrade the project:

- one genuine E2 workflow with **>=500 current-family candidate events/month** in covered geography;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 current-family candidate events/month** or equivalent proven aggregation;
- one E5 willingness-to-pay/resource commitment at a commercially useful price;
- evidence that municipality/address-aware results materially change quote/schedule/routing often enough to beat generic bundled checkers.

## What would move the score below 50

Serious stop signals include:

- 20 qualified conversations with no bounded repeated upstream applicability workflow;
- current-family upstream candidate volume remains too small when aggregated;
- representative E3 cases show material false-negative risk requiring expert review on most calls;
- permit necessity is usually known before the workflow reaches our insertion point;
- external users treat the tool as one-off research instead of infrastructure;
- free/general bundled checkers are considered sufficient;
- municipality/address specificity rarely changes the answer;
- address-aware share is too small to monetize;
- rule maintenance costs several hours/month per low-volume jurisdiction;
- buyers only value full filing/expediting and will not pay for preflight.

## Engineering freeze

Until external evidence pushes the score above 70:

**Do not:**

- add an eighth municipality;
- add U.S. coverage;
- add electrical/HVAC/mechanical families based only on public permit volume;
- build a third FSM adapter;
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
- corrections that prevent SAM/competition overclaim;
- changes explicitly required by an E2+/E3 partner.

## Current highest-value experiments

### A. Bounded estimator / quote denominator

For one recent complete month or fixed recent sample:

- relevant Requests/Assessments/Estimates/Quotes;
- current-family share;
- fraction where `permit required?` is still unresolved at first quote;
- who/what resolved the rest before quote.

### B. Generic checker vs. municipality/evidence value

For representative historical cases, record whether a safe answer required any of:

- municipality-specific exemption/threshold;
- property/zoning/heritage context;
- official-source evidence beyond a generic Ontario checklist;
- conservative `MUNICIPAL_CONFIRMATION_REQUIRED` rather than a broad yes/no.

If most cases are safely answerable by a free generic/local checklist, ProjectPermit's incremental value is weak even if its raw accuracy is good.

### C. Platform threshold

Measure one recent month of covered-geography **current-family** candidate events. First threshold: **>=500/month**; then look for >=2,000/month aggregation and a credible path to 10,000 external preflights/month.

### D. E3 -> E4 -> E5 chain

Keep the evidence order strict:

`E2 bounded workflow -> E3 representative historical benchmark -> E4 repeated external usage -> E5 economic behavior`

No directory listing, polite reply, internal CI call, synthetic benchmark or public permit count substitutes for that chain.

## Defensibility checkpoint

Do not score defensibility above 6/10 until at least one of these exists:

- repeated integration with real switching cost;
- externally benchmarked accuracy corpus;
- meaningful rule/source-change history;
- partner-specific normalization/routing embedded into operations;
- enough observed production outcomes to prioritize and maintain rules better than a new entrant.

Basic permit trigger lists, municipality-specific educational checkers, API/MCP wrappers and idea novelty do **not** qualify as moat assets.

## Bottom line

ProjectPermit remains worth validating because the cost structure is excellent and the embedded Canadian B2B evidence layer is not yet clearly dominated.

But the current commercial status is now:

> **promising low-cost capability, unproven current-family volume, unproven distribution, easily reproducible checker logic, low current defensibility**

The next dollar/hour should buy **external workflow evidence and proof that municipality/evidence/address specificity changes decisions**, not more code.