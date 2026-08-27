# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-27

Decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 61 / 100

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay | 15 | 5/10 | 7.5 | Filing/permit-ops buyers pay, but ProjectPermit's narrower upstream `$0.20-$0.50` per-call hypothesis has **no E5 evidence** yet. |
| Addressable call volume | 15 | 7/10 | 10.5 | Seven-city employer floor is material; Toronto shows ~1.7k mechanical/plumbing/drain permit revisions/month; large FSM platforms have enough aggregate workflow density. Candidate-preflight incidence is still unknown. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated trade/platform workflow can be large. **E4 remains 0.** |
| Distribution fit | 10 | 6/10 | 6.0 | Jobber/Buildxact Request/Estimate/Quote/Job insertion is structurally credible; official MCP Registry is generating downstream machine discovery. No production integration partner yet. |
| Competitive headroom | 10 | 5/10 | 5.0 | Canadian municipal-building API gap still exists, but QwikScope, Permitio, Ampr, zoning tools and municipal automation show the category is forming quickly. |
| Defensibility | 10 | 4/10 | 4.0 | Idea/protocol novelty is not a moat. Rule corpus, accuracy history and distribution could become a moat, but external assets are not built yet. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Uses deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **60.5 -> 61** |  |

## Interpretation

### Why this is not a No-Go

ProjectPermit still has several unusually good properties for a solo developer:

- very low marginal compute cost;
- no mandatory paid data license;
- no mandatory human reviewer/permit runner;
- clear high-value regulatory pain;
- large enough contractor/platform denominators;
- concrete integration point before quote/job creation;
- current Canadian API/MCP competition is still fragmented rather than obviously dominant.

### Why this is not a Go-to-scale

The critical commercial facts are still missing:

1. **How often is `permit required?` actually unresolved before a quote/job?**
2. **Will an external workflow repeatedly call a separate API for that answer?**
3. **What fraction needs address/property context?**
4. **Will anyone pay the proposed per-call price or commit integration resources?**
5. **Can the rule corpus stay accurate enough without a human-expert operation?**

Until those are answered, adding cities/features only increases maintenance burden.

## What would move the score above 70

Any two of the following would materially upgrade the project:

- one genuine E2 workflow with **>=500 candidate events/month** in covered geography;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 candidate events/month**;
- one E5 willingness-to-pay/resource commitment at a commercially useful price;
- evidence that address-aware results materially change quote/schedule/routing often enough to monetize.

Expected score after credible E2 + E3 + first E4: roughly **70-76**, depending on accuracy and volume.

## What would move the score below 50

Any of the following is a serious stop signal:

- 20 qualified conversations with no bounded repeated upstream applicability workflow;
- representative E3 cases show material false-negative risk that requires expert review on most calls;
- partners say permit necessity is almost always known before the workflow reaches them;
- external users treat the tool as one-off research instead of repeated workflow infrastructure;
- address-aware share is too small to support monetization;
- adjacent platforms bundle permit detection at negligible marginal cost before ProjectPermit gains distribution;
- city/rule maintenance consumes several hours/month per low-volume jurisdiction;
- buyers demand full filing/expediting rather than preflight and will not pay for the narrower layer.

## Engineering freeze

Until the score crosses 70 through external evidence:

**Do not:**

- add an eighth municipality;
- add U.S. coverage;
- add electrical/HVAC/mechanical families based only on public permit volume;
- build a third FSM adapter;
- add drawings/document QA;
- add permit filing/status/inspection operations;
- add a human reviewer network;
- pay marketplace/listing fees merely for visibility;
- build consumer zoning/feasibility features.

**Allowed engineering:**

- bugs;
- validation friction reduction;
- privacy/telemetry correctness;
- benchmark tooling;
- changes explicitly required by an E2+/E3 partner.

## Current highest-value experiments

### Experiment A — bounded multi-account estimator denominator

Targets: GTA estimator/consulting firms serving multiple contractors.

Measure for one recent complete month:

- Toronto + Mississauga residential-renovation estimates;
- estimates requiring manual permit-applicability research before quote finalization.

A bucketed answer is sufficient for E2.

### Experiment B — adjacent permit-ops intake boundary

Targets: Permitio / PermitCheck / similar permit workflow products.

Measure:

- jobs arriving already known permit-positive;
- jobs still requiring `permit required?` determination at intake.

If almost all are already permit-positive, downstream permit vendors are not the main distribution channel for ProjectPermit; move upstream toward estimating/FSM platforms.

### Experiment C — platform threshold

Targets: Buildxact / Jobber or their multi-account partners.

Measure one recent month of covered-geography candidate Requests/Estimates/Quotes/Jobs. First threshold: **>=500/month**.

## Defensibility checkpoint

Do not score defensibility above 6/10 until at least one of these exists:

- a repeated integration whose workflow switching cost is real;
- an externally benchmarked accuracy corpus competitors cannot reproduce instantly;
- meaningful rule/source-change history maintained over time;
- a partner-specific normalized schema/routing layer embedded into operations;
- enough observed production outcomes to prioritize/maintain rules better than a new entrant.

## Bottom line

ProjectPermit remains worth validating because the market/pain/cost structure is attractive and the category appears early rather than saturated.

But its current commercial status is:

> **promising capability, unproven distribution, medium-low defensibility**

The next dollar/hour should buy **external evidence**, not more code.
