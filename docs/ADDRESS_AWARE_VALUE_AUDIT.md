# Address-aware value audit

Updated: 2026-08-27

Purpose: separate **address/GIS resolution capability** from **decision-changing address/property value** in ProjectPermit's current product and pricing hypothesis.

This is an internal technical/commercial-structure audit only. It is not E2, E3, E4, E5, usage-frequency evidence, or willingness-to-pay evidence.

## Current architecture

ProjectPermit currently has municipal address/property adapters for five jurisdictions:

- Gatineau
- Ottawa
- Toronto
- Mississauga
- Vancouver

Those adapters can resolve address/property context from first-party municipal sources. However, an adapter is commercially useful for permit preflight only when the deterministic jurisdiction rules actually **consume** a derived property fact that can change or qualify the result.

Reproducible audits:

- `market_research/property_fact_consumption_audit.py`
- `market_research/property_overlay_flip_matrix.py`
- `.github/workflows/property-fact-consumption-audit.yml`

## Static consumption result

> **Only 2 of 5 address-adapter jurisdictions currently consume any property facts in permit-applicability rules = 40%.**

| Jurisdiction | Address adapter | Property facts consumed by current rules | Current determination can depend on adapter-derived property context? |
|---|---|---|---|
| Gatineau | Yes | `heritage`, `piia` | **Yes** |
| Ottawa | Yes | `heritage` | **Yes** |
| Toronto | Yes | none | **No, under current rule code** |
| Mississauga | Yes | none | **No, under current rule code** |
| Vancouver | Yes | none | **No, under current rule code** |
| Laval | No | `piia` | Property context can matter, but no current address adapter supplies it |
| Longueuil | No | `piia` | Property context can matter, but no current address adapter supplies it |

Across all seven jurisdictions, four rule evaluators consume some property fact, but two of those four — Laval and Longueuil — do not have an address adapter.

## Synthetic outcome-flip result

A second audit holds project scope constant and changes only property facts from:

`heritage=false, piia=false`

to:

`heritage=true, piia=true`

It uses four common exemption-like scopes across all five address-adapter jurisdictions:

1. same-size window replacement;
2. cosmetic interior painting;
3. low detached deck;
4. same-location plumbing fixture replacement.

Result:

- jurisdiction × scope pairs: **20**
- determination flips: **8 / 20 = 40%**
- requirement-set changes: **8 / 20 = 40%**

By jurisdiction:

| Jurisdiction | Determination flips | Flip rate | Requirement-set changes |
|---|---:|---:|---:|
| Gatineau | **4/4** | **100%** | 4/4 |
| Ottawa | **4/4** | **100%** | 4/4 |
| Toronto | **0/4** | **0%** | 0/4 |
| Mississauga | **0/4** | **0%** | 0/4 |
| Vancouver | **0/4** | **0%** | 0/4 |

In the selected Gatineau/Ottawa exemption-like cases, property overlays changed `LIKELY_NOT_REQUIRED` into `ADDITIONAL_REVIEW_REQUIRED`. In Toronto, Mississauga and Vancouver, toggling those same property fields produced no determination or requirement-set change because the current jurisdiction evaluators do not consume them.

This outcome audit independently matches the static source audit: current address/property decision value is concentrated in **2 of the 5 adapter jurisdictions**.

## Commercial interpretation

This removes an important unsupported assumption from the current monetization thesis.

The previous working hypothesis treated an **address-aware evidence-linked preflight** as the higher-value paid unit, roughly `$0.20-$0.50/call` subject to E5.

The current implementation does **not** justify treating every address-aware lookup as a higher-value determination:

- in Toronto, Mississauga and Vancouver, resolving an address can add municipal property/GIS metadata, but the current permit-applicability evaluator does not read that metadata at all;
- therefore the permit determination for those three cities is currently the same whether those adapter-derived property facts exist or not;
- charging a premium merely because an address lookup occurred would confuse **technical work performed** with **decision value created**.

The most defensible present statement is:

> ProjectPermit has five address adapters, but only Gatineau and Ottawa currently have a deterministic permit-applicability path where adapter-derived property context can affect the decision.

## What this does not mean

It does not prove that Toronto, Mississauga or Vancouver property context is irrelevant in the real permit workflow.

It only proves that **the current ruleset does not yet use it**.

There may be official zoning, heritage, floodplain, overlay, building-form or other property-specific conditions that could become relevant. But those should not be added merely to justify existing adapters or pricing. They should be promoted into deterministic rules only when:

1. a current first-party source supports the rule clearly;
2. the condition materially changes permit applicability or required routing; and
3. external E2/E3 evidence shows that this property-specific decision occurs often enough to matter commercially.

Engineering freeze remains in force.

## Pricing implication

Until representative external evidence exists, replace the old mental model:

`address lookup happened -> premium paid call`

with:

`address/property context materially changes or qualifies the routing decision -> potentially higher-value call`

The commercial metric to measure is therefore not `address-aware share` alone.

It is:

`representative preflight cases where derived property context materially changes safe routing / all representative current-family preflight cases`

A useful E3 benchmark should distinguish:

- address was available;
- address resolution was technically possible;
- property facts were actually needed;
- property facts changed the safe outcome.

Only the last two support an address-aware monetization premium.

## Go / No-Go implication

This audit is negative evidence against the current monetization assumption, even though it is not external willingness-to-pay evidence.

It means the proposed `$0.20-$0.50` premium unit has a narrower current value base than previously assumed. The scorecard now reflects this by reducing willingness-to-pay / monetization fit from 5/10 to 4/10.

Any future score increase must come from external evidence that either:

- municipality-specific scope logic itself is valuable enough to pay for without address context; or
- property/address context changes a meaningful share of real workflow decisions.

Do not add GIS/property features speculatively to recover the narrative.

## Next external measurement

The synthetic flip matrix establishes technical sensitivity only. It does not establish how often a real address is heritage/PIIA or otherwise decision-relevant.

The next representative historical benchmark should optionally record:

`address_property_context_changed_outcome=yes/no`

The target commercial metric is:

`representative cases where derived address/property context materially changes safe routing / all representative current-family cases`

This optional diagnostic must not affect E3 qualification. Its purpose is to test whether the address-aware premium has real incidence, not to make the benchmark easier to pass.