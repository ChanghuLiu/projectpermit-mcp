# Build vs Buy Maintenance Baseline — 2026-08-28

## Decision summary

Current evidence supports a **split conclusion**:

> **A narrow one-municipality permit checker is plausibly cheap for a vertical SaaS to internalize.**

> **A reusable multi-municipality deterministic capability carries a materially larger source/rule/test/safety maintenance surface, but buyer willingness to outsource that burden remains unproven.**

This baseline therefore does **not** increase ProjectPermit's commercial score and does **not** justify expansion. The current score remains **53/100**.

## Evidence boundary

This audit measures repository maintenance surface only.

It does **not** estimate:

- engineering hours;
- salary or contractor cost;
- development calendar time;
- accuracy;
- willingness to pay;
- switching cost;
- competitive moat.

LOC, file counts, rule IDs and official-source counts are proxies for the amount of material that must remain consistent over time. They must not be converted directly into money or time.

The reproducible audit is:

- `market_research/build_vs_buy_maintenance_baseline.py`
- `.github/workflows/build-vs-buy-maintenance-baseline.yml`

The 2026-08-28 PR run completed successfully and emitted the figures below.

## Current maintained permit surface

Across the seven currently supported jurisdictions:

- **7 jurisdictions**;
- **155 unique deterministic rule IDs**;
- **42 official municipal / GIS / by-law sources**;
- **6 core deterministic rule/router files**;
- **1,589 physical lines** in the deterministic multi-city rule surface;
- **771 physical lines** in property-context / overlay handling;
- **605 physical lines** in source / property-overlay maintenance audits;
- **306 physical lines** in the machine request/response + API/preflight contract;
- **989 physical lines** in selected core correctness tests.

After deduplicating files shared by layers and adding the source manifest, the deliberately bounded `safe_shared_api_union_surface` is:

> **30 files / 4,146 physical lines / 3,618 nonblank lines / 189,751 bytes**

This union intentionally excludes software-distribution and monetization machinery.

## Jurisdiction-level proxy

Because several Python modules share helpers across municipalities, the audit deliberately avoids pretending that LOC can be allocated cleanly per city. The safer city-level proxy is unique rule IDs plus official sources.

| Jurisdiction | Rule IDs | Official sources | Critical sources |
|---|---:|---:|---:|
| Gatineau | 22 | 7 | 1 |
| Ottawa | 27 | 12 | 6 |
| Toronto | 26 | 5 | 3 |
| Mississauga | 27 | 5 | 3 |
| Laval | 27 | 5 | 2 |
| Longueuil | 8 | 4 | 2 |
| Vancouver | 18 | 4 | 3 |
| **Total** | **155** | **42** |  |

Average across the current seven cities is about **22 rule IDs and 6 official sources per city**, but the spread matters more than the average.

## What this says against ProjectPermit

The negative evidence is important.

A vertical SaaS does **not** need to reproduce the 4,146-line shared capability if it only wants a narrow embedded feature for one local market.

The current city proxies show that a useful local checker can be bounded by roughly:

- **8–27 current rule IDs**;
- **4–12 official sources**;
- no external developer API if the feature is internal;
- no cross-platform adapter layer;
- potentially no property lookup if the product accepts conservative confirmation or serves scopes where parcel context rarely changes the result.

That is consistent with observed market behavior:

- BuilderAI has delivered municipal urbanism inside a Quebec estimating workflow;
- ConstructAI publicly claims a Toronto permit/regulation checker in beta;
- local contractor/checker sites already reproduce municipality-specific permit logic with official links.

Therefore:

> **`We have deterministic rules` is not a moat.**

> **`A contractor SaaS could never build this itself` is contradicted by current evidence.**

If a buyer primarily serves one or two municipalities, internal implementation may be economically rational.

## What may still support buying an external capability

The multi-city burden is qualitatively different from the one-city burden.

ProjectPermit's current shared surface includes:

### 1. Cross-city rule normalization

155 rule IDs must map different municipal wording and thresholds into one machine contract.

### 2. Source maintenance

42 current first-party sources include ordinary guidance, PDFs, GIS layers, zoning/by-law transitions and permit portals.

The hard part is not storing a URL. It is detecting when a source moves or its meaning changes and determining whether that change invalidates a prior rule.

### 3. Property-context safety

The address/property layer is **771 lines** even though previous audits showed that derived property facts currently change permit routing in only a minority of address-adapter jurisdictions.

This is both:

- a maintenance cost that a broad provider may centralize; and
- a warning not to overprice address lookup when it does not change the answer.

### 4. Conservative unknown handling

The recent overlay correction demonstrates a concrete failure mode: missing heritage/PIIA facts can turn a safe-looking exemption into a dangerous false `LIKELY_NOT_REQUIRED` result if unknown is treated like false.

The product therefore maintains explicit unknown-state routing and audits instead of relying only on happy-path rules.

### 5. Regression and evidence contract

The selected core correctness tests alone are **989 physical lines**, about **62% of the physical size of the deterministic rule layer**.

That ratio is not a quality score, but it demonstrates that operational reliability requires a meaningful validation surface beyond the trigger list itself.

## Three build-vs-buy layers

### Layer A — narrow local embedded checker

Likely buyer behavior:

- one or a few municipalities;
- a narrow project mix;
- internal UI/RAG/checklist;
- acceptable manual escalation for ambiguity.

Current evidence suggests this can be relatively cheap to internalize.

**ProjectPermit advantage: weak unless the buyer explicitly rejects owning local rule maintenance.**

### Layer B — multi-city deterministic engine

Current ProjectPermit proxy:

- 7 jurisdictions;
- 155 deterministic rule IDs;
- 42 official sources;
- 1,589 lines in the shared rule/router surface.

This is a more credible maintenance burden, especially where buyers serve multiple municipalities.

**ProjectPermit advantage: plausible, not validated.**

### Layer C — safe shared machine capability

Adds:

- address/property resolution;
- overlay fail-safe behavior;
- source-change monitoring/audits;
- machine schemas/API contract;
- regression/backtest coverage.

Bounded current union:

- 30 files;
- 4,146 physical lines;
- 3,618 nonblank lines.

**ProjectPermit advantage: potentially strongest here, but only if buyers value this reliability enough to buy rather than accept a narrower internal feature.**

## Explicit exclusions

The audit does **not** count the following as permit-domain clone burden or moat:

- Jobber / ServiceM8 adapters and clients;
- MCP server / registry packaging;
- x402/payment infrastructure;
- telemetry;
- market-size / permit-volume research scripts;
- outreach and partner-validation documents.

Those may matter to ProjectPermit's product/distribution economics, but including them would inflate the `permit intelligence` build-vs-buy comparison.

## Implication for current competitors

### BuilderAI

BuilderAI proves that one vertical SaaS can ship its own urbanism capability. This baseline makes that result unsurprising rather than anomalous: one-city/few-city rule scope is much smaller than ProjectPermit's shared surface.

### ConstructAI Toronto

Its beta permit-checker claim is compatible with the same conclusion. Public evidence still does not establish a reliable delivered rule engine, but Toronto-only embedding is not technically implausible.

### LandLogic

LandLogic attacks the opposite side of the spectrum: broad Ontario data/permit intelligence and partner integrations. ProjectPermit's remaining possible distinction is narrower self-serve deterministic permit-specific delivery, not ownership of uniquely difficult rules.

### Contrax / Elper / other software buyers

The highest-value build-vs-buy question is now concrete:

> `Would you rather maintain roughly 4–12 official sources and a few dozen local permit rules for the municipalities you actually serve, or pay an external provider to maintain cross-city rules, evidence, source drift, unknown-state safety and regression tests?`

A buyer saying `we would just build the local version` is meaningful negative evidence.

A buyer saying `we do not want to own cross-city regulatory maintenance` is useful differentiation evidence, but still does not prove price or volume.

## Score consequence

**No score change: remain at 53/100.**

Reason:

- the audit strengthens the negative case that narrow local embedding is feasible;
- it also quantifies a non-trivial cross-city maintenance burden;
- neither side resolves buyer preference, volume or willingness to pay.

A future score change should come from observed build-vs-buy behavior, not LOC.

## Next falsification gates

Increase confidence in the external-API thesis only if software buyers independently say that one or more of these matters enough to avoid internal implementation:

1. cross-municipality source/rule maintenance;
2. deterministic reproducibility;
3. official evidence and source versions;
4. conservative unknown/property-overlay handling;
5. shared use across multiple products/agents;
6. lower total cost than maintaining local RAG/checker logic.

Downgrade the thesis if multiple representative software buyers say they can maintain their relevant cities internally with acceptable accuracy and cost.

Do not add another municipality merely to make the maintenance surface larger. Expansion remains frozen until external evidence justifies it.
