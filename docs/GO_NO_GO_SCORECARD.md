# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-27

Decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 59 / 100

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay | 15 | 5/10 | 7.5 | Filing/permit-ops buyers pay, but ProjectPermit's narrower upstream `$0.20-$0.50` per-call hypothesis has **no E5 evidence** yet. |
| Addressable call volume | 15 | 6/10 | 9.0 | Contractor/platform denominators are material, but Toronto's ~1.7k/month broad MEP flow cannot be mapped safely to the current eight families. A City-WORK-label diagnostic shows only ~560-587 current-family-like issued events/month, heavily dominated by Interior Alterations, and even that is not upstream candidate volume. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated workflow can be larger. **E4 remains 0.** |
| Distribution fit | 10 | 6/10 | 6.0 | Jobber/Buildxact Request/Assessment/Estimate/Quote insertion is structurally credible; official MCP Registry is generating downstream machine discovery. No production integration partner yet. |
| Competitive headroom | 10 | 5/10 | 5.0 | Canadian municipal-building API gap still exists, but QwikScope, Permitio, Ampr, zoning tools and municipal automation show the category is forming quickly. |
| Defensibility | 10 | 4/10 | 4.0 | Idea/protocol novelty is not a moat. Rule corpus, accuracy history and distribution could become a moat, but external assets are not built yet. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Uses deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **59.0 -> 59** |  |

## Why the score dropped from 61 to 59

The previous 61/100 score gave too much weight to Toronto's broad Mechanical + Plumbing + Drain/Site permit flow (~1.7k issued revisions/month).

A follow-up analysis of the City `WORK` field showed that most of that volume is recorded as broad `Building Permit Related(PS/MS/DR)` work and cannot be mapped safely into ProjectPermit's existing families.

A deliberately conservative/non-exclusive current-family-like label diagnostic shows roughly:

- 2023: **6,695/year = 557.9/month**;
- 2024: **6,690/year = 557.5/month**;
- 2025: **7,038/year = 586.5/month**.

Even this is **not SAM**: it is downstream issued-workflow signal, heavily dominated by `Interior Alterations`, and says nothing about the fraction where permit applicability was unresolved upstream.

Therefore addressable call volume is now scored 6/10 instead of 7/10. The product remains worth validating, but public permit statistics no longer justify an optimistic current-family call-volume assumption.

## Interpretation

### Why this is not a No-Go

ProjectPermit still has several unusually good properties for a solo developer:

- very low marginal compute cost;
- no mandatory paid data license;
- no mandatory human reviewer/permit runner;
- clear high-value regulatory pain;
- material contractor/platform denominators;
- concrete integration point before quote/job creation;
- current Canadian API/MCP competition is still fragmented rather than obviously dominant.

### Why this is not a Go-to-scale

The critical commercial facts are still missing:

1. **How often is `permit required?` actually unresolved before a Request/assessment becomes a quote/job?**
2. **How many of those upstream candidates map to one of the current eight families?**
3. **Will an external workflow repeatedly call a separate API for that answer?**
4. **What fraction needs address/property context?**
5. **Will anyone pay the proposed per-call price or commit integration resources?**
6. **Can the rule corpus stay accurate enough without a human-expert operation?**

Until those are answered, adding cities/features only increases maintenance burden.

## What would move the score above 70

Any two or three of the following would materially upgrade the project:

- one genuine E2 workflow with **>=500 current-family candidate events/month** in covered geography;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 current-family candidate events/month** or equivalent proven aggregation;
- one E5 willingness-to-pay/resource commitment at a commercially useful price;
- evidence that address-aware results materially change quote/schedule/routing often enough to monetize.

Expected score after credible E2 + E3 + first E4: roughly **70-76**, depending on accuracy and volume.

## What would move the score below 50

Any of the following is a serious stop signal:

- 20 qualified conversations with no bounded repeated upstream applicability workflow;
- current-family upstream candidate volume remains too small even when aggregated across platforms/accounts;
- representative E3 cases show material false-negative risk that requires expert review on most calls;
- partners say permit necessity is almost always known before the workflow reaches Request/assessment/quote;
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
- market-research corrections that prevent SAM/call-volume overclaim;
- changes explicitly required by an E2+/E3 partner.

## Current highest-value experiments

### Experiment A — bounded multi-account estimator denominator

Targets: GTA estimator/consulting firms serving multiple contractors.

Measure for one recent complete month:

- Toronto + Mississauga residential-renovation estimates;
- current-family scope mix;
- estimates requiring manual permit-applicability research before quote finalization.

A bucketed answer with timeframe/workflow denominator is sufficient for E2.

### Experiment B — upstream workflow incidence

Targets: Jobber/Buildxact implementation experts, estimators and platform teams.

Measure at Request/on-site-assessment/Estimate/Quote time:

- relevant candidate volume;
- current-family share;
- fraction where `permit required?` remains unresolved.

Permitio's founder provided useful E1 boundary evidence that its downstream filing intake is already permit-positive; Permitio declined to share internal volume and is now closed as an E2 acquisition target. Do not contact it again for internal data.

### Experiment C — platform threshold

Targets: Buildxact / Jobber or their multi-account partners.

Measure one recent month of covered-geography **current-family** candidate Requests/Assessments/Estimates/Quotes/Jobs. First threshold: **>=500/month**.

## Defensibility checkpoint

Do not score defensibility above 6/10 until at least one of these exists:

- a repeated integration whose workflow switching cost is real;
- an externally benchmarked accuracy corpus competitors cannot reproduce instantly;
- meaningful rule/source-change history maintained over time;
- a partner-specific normalized schema/routing layer embedded into operations;
- enough observed production outcomes to prioritize/maintain rules better than a new entrant.

## Bottom line

ProjectPermit remains worth validating because the pain/cost structure is attractive and the category appears early rather than saturated.

But its current commercial status is now more cautiously stated as:

> **promising low-cost capability, unproven current-family volume, unproven distribution, medium-low defensibility**

The next dollar/hour should buy **external current-family workflow evidence**, not more code.