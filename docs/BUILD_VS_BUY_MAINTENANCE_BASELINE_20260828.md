# Build vs Buy Maintenance Baseline — 2026-08-28

## Decision summary

Current evidence supports a **split conclusion**:

> **A narrow one-municipality scope-only permit checker is plausibly cheap for a vertical SaaS to internalize.**

> **A reusable multi-municipality deterministic capability carries a materially larger source/rule/test/safety maintenance surface, but buyer willingness to outsource that burden remains unproven.**

This baseline therefore does **not** increase ProjectPermit's commercial score and does **not** justify expansion. The current score remains **53/100**.

## Evidence boundary

This audit measures repository maintenance surface only. It does **not** estimate engineering hours, salary/contractor cost, calendar time, accuracy, willingness to pay, switching cost or moat.

LOC, file counts, rule IDs and official-source counts are proxies for the amount of material that must remain internally consistent. They must not be converted directly into money or time.

The reproducible audit is:

- `market_research/build_vs_buy_maintenance_baseline.py`
- `.github/workflows/build-vs-buy-maintenance-baseline.yml`

The 2026-08-28 PR workflow ran successfully and emitted the figures below.

## Current maintained permit surface

Across the seven supported jurisdictions:

- **7 jurisdictions**;
- **155 unique deterministic rule IDs**;
- **42 total official municipal / GIS / by-law sources**;
- of those, **28 are rule/guidance/by-law/permit-portal sources**;
- **14 are GIS/open-data context endpoints**;
- **1,589 physical lines** in the deterministic multi-city rule/router surface;
- **771 physical lines** in property-context / overlay handling;
- **605 physical lines** in source / property-overlay maintenance audits;
- **306 physical lines** in the machine request/response + API/preflight contract;
- **989 physical lines** in selected core correctness tests.

After deduplicating files shared by layers and adding the source manifest, the deliberately bounded `safe_shared_api_union_surface` is:

> **30 files / 4,146 physical lines / 3,618 nonblank lines / 189,751 bytes**

This union intentionally excludes software-distribution and monetization machinery.

## Why the source split matters

Using all 42 official sources as the minimum clone burden would overstate the case for ProjectPermit.

A vertical SaaS that wants only a **scope-based permit checker** may not need address, parcel, zoning-layer or heritage GIS endpoints at all. For that narrower build-vs-buy question, the more defensible source proxy is the **28 rule/guidance sources**, not all 42 sources.

The 14 GIS/open-data sources matter only when the product chooses to own address/property-aware context as well.

This distinction is especially important because previous ProjectPermit audits showed that derived property facts currently change permit routing in only a minority of address-adapter jurisdictions.

## Jurisdiction-level proxy

Because several Python modules share helpers across municipalities, the audit deliberately avoids pretending that LOC can be allocated cleanly per city. The safer city-level proxy is unique rule IDs plus source counts.

| Jurisdiction | Rule IDs | Rule/guidance sources | Context/GIS sources | Total sources |
|---|---:|---:|---:|---:|
| Gatineau | 22 | 4 | 3 | 7 |
| Ottawa | 27 | 9 | 3 | 12 |
| Toronto | 26 | 1 | 4 | 5 |
| Mississauga | 27 | 1 | 4 | 5 |
| Laval | 27 | 5 | 0 | 5 |
| Longueuil | 8 | 4 | 0 | 4 |
| Vancouver | 18 | 4 | 0 | 4 |
| **Total** | **155** | **28** | **14** | **42** |

The most commercially important rows are Toronto and Mississauga: a scope-only embedded checker can currently ground its core permit logic in **one primary rule/guidance source per city**, even though ProjectPermit also maintains four context/GIS endpoints for each.

That is strong negative evidence against any claim that a Toronto-only or Mississauga-only SaaS must buy an external permit API because municipal source maintenance is inherently too large.

## What this says against ProjectPermit

A vertical SaaS does **not** need to reproduce the 4,146-line shared capability if it only wants a narrow embedded feature for one local market.

The current city proxies show a local checker can be bounded by roughly:

- **8–27 current rule IDs**;
- **1–9 core rule/guidance sources** for a scope-only implementation;
- no external developer API if the feature is internal;
- no cross-platform adapter layer;
- no GIS/property layer if the product accepts conservative confirmation or chooses not to make parcel-specific claims.

That is consistent with observed market behavior:

- BuilderAI has delivered municipal urbanism inside a Quebec estimating workflow;
- ConstructAI publicly claims a Toronto permit/regulation checker in beta;
- local contractor/checker sites already reproduce municipality-specific permit logic with official links.

Therefore:

> **`We have deterministic rules` is not a moat.**

> **`Municipal rules are too difficult for a vertical SaaS to build itself` is contradicted by current evidence for narrow local coverage.**

If a buyer primarily serves one or two municipalities, internal implementation may be economically rational.

## What may still support buying an external capability

The multi-city burden is qualitatively different from the one-city burden.

### 1. Cross-city rule normalization

155 rule IDs map different municipal wording and thresholds into one machine contract.

### 2. Rule-source maintenance

The stricter scope-only shared source set still contains **28 first-party rule/guidance sources** across seven municipalities. Ottawa alone currently requires nine such sources because its permit and zoning transition logic is fragmented across multiple official pages/advisories.

The relevant burden is not storing URLs; it is detecting source drift and deciding whether a change invalidates a prior rule.

### 3. Optional property-context breadth

If the provider also promises address/property-aware routing, the source set grows by **14 GIS/open-data context endpoints** and the codebase adds a **771-line** address/property/overlay layer.

This is potentially centralizable maintenance, but it should not be sold as universal value when property context does not materially change the decision.

### 4. Conservative unknown handling

The recent overlay correction demonstrates a concrete failure mode: missing heritage/PIIA facts can turn an apparent exemption into a dangerous false `LIKELY_NOT_REQUIRED` result if unknown is treated like false.

### 5. Regression and evidence contract

The selected core correctness tests are **989 physical lines**, about **62% of the physical size of the deterministic rule layer**.

That ratio is not a quality score. It simply shows that an operational shared capability contains a meaningful validation surface beyond the trigger list itself.

## Three build-vs-buy layers

### Layer A — narrow local embedded checker

Typical shape:

- one or a few municipalities;
- narrow project mix;
- 1–9 core rule/guidance sources per current city;
- internal UI/RAG/checklist;
- manual escalation for ambiguity;
- no need for external API packaging.

**ProjectPermit advantage: weak unless the buyer explicitly rejects owning local rule maintenance.**

### Layer B — multi-city deterministic engine

Current ProjectPermit proxy:

- 7 jurisdictions;
- 155 deterministic rule IDs;
- 28 rule/guidance sources;
- 1,589 lines in the shared rule/router surface.

**ProjectPermit advantage: plausible maintenance centralization, not validated customer value.**

### Layer C — safe property-aware shared machine capability

Adds:

- 14 GIS/open-data context sources;
- address/property resolution;
- overlay fail-safe behavior;
- source-change monitoring/audits;
- machine schemas/API contract;
- regression/backtest coverage.

Bounded current union:

- 30 files;
- 4,146 physical lines;
- 3,618 nonblank lines.

**ProjectPermit advantage: potentially strongest here, but only if buyers value this reliability/property breadth enough to buy rather than accept a narrower internal feature.**

## Explicit exclusions

The audit does **not** count the following as permit-domain clone burden or moat:

- Jobber / ServiceM8 adapters and clients;
- MCP server / registry packaging;
- x402/payment infrastructure;
- telemetry;
- market-size / permit-volume research scripts;
- outreach and partner-validation documents.

Including those would inflate the `permit intelligence` build-vs-buy comparison.

## Implication for current competitors

### BuilderAI

BuilderAI proves that one vertical SaaS can ship its own urbanism capability. The stricter source breakdown makes this less surprising: narrow local coverage can rely on a small number of primary rule sources.

### ConstructAI Toronto

Its beta permit-checker claim is technically plausible from a maintenance perspective. Toronto's current scope-only core rule source count is just **one**, although reliable interpretation, exceptions and production accuracy remain unverified.

### LandLogic

LandLogic attacks the broad end of the spectrum: Ontario-wide property/permit intelligence and assisted partner integrations. ProjectPermit's remaining possible distinction is narrow self-serve deterministic permit delivery and shared maintenance, not uniquely hard raw source collection.

### Contrax / Elper / other software buyers

The highest-value build-vs-buy question is now more concrete:

> `For your actual municipalities, would you rather maintain roughly 1–9 core municipal rule/guidance sources and a few dozen local permit rules yourself, or pay an external provider to maintain cross-city normalization, evidence, source drift, unknown-state safety, optional property context and regression tests?`

A buyer saying `we would just build the local version` is meaningful negative evidence.

A buyer saying `we do not want to own cross-city regulatory maintenance` is useful differentiation evidence, but still does not prove price or call volume.

## Score consequence

**No score change: remain at 53/100.**

The stricter source split actually strengthens the negative case for local internal builds, while the seven-city shared surface still supports a possible maintenance-centralization thesis. Neither resolves buyer preference, volume or willingness to pay.

A future score change should come from observed build-vs-buy behavior, not LOC or source counts.

## Next falsification gates

Increase confidence in the external-API thesis only if software buyers independently say one or more of these matters enough to avoid internal implementation:

1. cross-municipality source/rule maintenance;
2. deterministic reproducibility;
3. official evidence and source versions;
4. conservative unknown/property-overlay handling;
5. shared use across multiple products/agents;
6. lower total cost than maintaining local RAG/checker logic.

Downgrade the thesis if multiple representative software buyers say they can maintain their relevant cities internally with acceptable accuracy and cost.

Do not add another municipality merely to make the maintenance surface larger. Expansion remains frozen until external evidence justifies it.
