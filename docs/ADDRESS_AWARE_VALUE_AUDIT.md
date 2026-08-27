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

A static AST audit was added at:

- `market_research/property_fact_consumption_audit.py`
- `.github/workflows/property-fact-consumption-audit.yml`

The audit inspects each jurisdiction evaluator and lists the `property` keys currently read by deterministic rules.

## Result

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

It means the proposed `$0.20-$0.50` premium unit has a narrower current value base than previously assumed. Any future score increase must come from external evidence that either:

- municipality-specific scope logic itself is valuable enough to pay for without address context; or
- property/address context changes a meaningful share of real workflow decisions.

Do not add GIS/property features speculatively to recover the narrative.

## Next audit

Run a property-overlay flip diagnostic using representative exemption-like scopes:

- baseline property facts;
- `heritage=true` and/or `piia=true` where supported;
- compare determination and routing changes.

This can measure **technical decision sensitivity** in Gatineau/Ottawa and confirm zero current decision sensitivity in Toronto/Mississauga/Vancouver.

That diagnostic still will not establish real-world incidence; external historical cases must supply that denominator.