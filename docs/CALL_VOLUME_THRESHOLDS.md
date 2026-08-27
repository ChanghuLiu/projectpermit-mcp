# ProjectPermit Monthly Call Thresholds

Updated: 2026-08-27

The core business question is not how many municipalities can be coded. It is whether ProjectPermit can reach enough **repeated external workflow calls**, and then monetize enough of the higher-value address-aware calls, through a small number of distribution partners.

This document intentionally separates three quantities:

1. **external successful preflights** — proof that ProjectPermit occupies a repeated workflow;
2. **address-aware preflights** — calls that require civic-address / municipal property / GIS context;
3. **paid calls** — calls for which a buyer actually accepts a commercial price.

These quantities are not interchangeable. Unless explicitly sourced, percentages below are sensitivity variables, not forecasts.

See also `docs/COVERED_MARKET_CALL_SENSITIVITY.md` for the currently covered-city issuance floor and paid-share analysis.

## Two different commercial checkpoints

### Distribution checkpoint

A first meaningful distribution target remains:

> **10,000 external successful preflights/month**

This would show that the product is being used repeatedly rather than as a one-off lookup.

It does **not** by itself imply $2,500-$5,000/month of revenue.

### Monetization checkpoint

The current working price hypothesis is approximately **$0.20-$0.50 per address-aware evidence-linked preflight**, subject to E5 validation.

A stronger economic checkpoint is therefore:

> **10,000 paid address-aware calls/month**, or a lower paid volume whose realized revenue clearly justifies infrastructure + rule-maintenance cost.

At $0.25-$0.50/call, 10,000 paid calls would produce $2,500-$5,000 gross/month before infrastructure, support and municipal-rule maintenance.

## Revenue sensitivity by monthly paid calls

| Monthly paid calls | Revenue @ $0.10 | Revenue @ $0.25 | Revenue @ $0.50 |
|---:|---:|---:|---:|
| 1,000 | $100 | $250 | $500 |
| 5,000 | $500 | $1,250 | $2,500 |
| 10,000 | $1,000 | $2,500 | $5,000 |
| 25,000 | $2,500 | $6,250 | $12,500 |
| 50,000 | $5,000 | $12,500 | $25,000 |
| 100,000 | $10,000 | $25,000 | $50,000 |
| 1,000,000 | $100,000 | $250,000 | $500,000 |

These are gross-revenue sensitivities, not profitability forecasts.

## Paid-share sensitivity

At exactly 10,000 total external successful preflights/month:

| Paid/address-aware share | Paid calls/month | Gross @ $0.25 | Gross @ $0.50 |
|---:|---:|---:|---:|
| 30% | 3,000 | $750 | $1,500 |
| 50% | 5,000 | $1,250 | $2,500 |
| 70% | 7,000 | $1,750 | $3,500 |
| 100% | 10,000 | $2,500 | $5,000 |

Conversely, total external preflights required to produce 10,000 paid calls are:

| Paid share | Total external preflights required |
|---:|---:|
| 30% | ~33,333/month |
| 50% | 20,000/month |
| 70% | ~14,286/month |
| 100% | 10,000/month |

The next external partner benchmarks therefore need to measure `address-aware share` and willingness to pay, not merely total workflow volume.

## What 10k external calls/month could look like

Equivalent distribution shapes:

| Distribution shape | Calls/customer/month | Customers/integrations needed | Total external calls/month |
|---|---:|---:|---:|
| High-volume contractor accounts | 80 | 125 | 10,000 |
| Medium contractor accounts | 25 | 400 | 10,000 |
| Property portfolios | 20 | 500 | 10,000 |
| Strong SaaS integrations | 2,000 | 5 | 10,000 |
| Mid-sized integrations | 500 | 20 | 10,000 |
| One platform workflow | 10,000 | 1 | 10,000 |

The `80 calls/customer/month` row is comparable to a public iPermit Marketplace testimonial from a contractor reporting roughly 80+ permit jobs/month. It does not imply 125 such reachable contractors exist, nor that all of those jobs require a ProjectPermit preflight.

Source: https://marketplace.servicetitan.com/partner/ipermit

## Covered-city activity floor

A clean same-year first-party 2024 floor is currently established for Toronto, Ottawa, Mississauga, Laval and Vancouver:

- Toronto: 36,887 permits
- Ottawa: 7,688 permits
- Mississauga: 4,458 permits
- Laval: 1,415 construction/improvement permits
- Vancouver: 3,705 building-permit subtotal

Combined: **54,153 issued permits/year = 4,512.75/month**.

Vancouver source: https://vancouver.ca/files/cov/statement-of-building-permits-issued-dec-2025.pdf

Gatineau and Longueuil remain excluded from this exact cumulative floor rather than being guessed.

If upstream candidate-preflight volume were:

| Candidate preflights per observed issued permit | Implied external preflights/month |
|---:|---:|
| 1.0x | 4,513 |
| 1.5x | 6,769 |
| 2.0x | 9,026 |
| 2.22x | ~10,019 |
| 3.0x | 13,538 |
| 5.0x | 22,564 |

Thus the current geographic footprint does not need a huge top-of-funnel multiplier merely to reach the **10k external-call distribution checkpoint**. Roughly 2.22 candidate preflights per observed issued permit would be enough on this sensitivity model.

But candidate/issued multiplier is not yet externally measured. It must not be treated as observed demand.

## ServiceTitan scale sensitivity — corrected

Current official ServiceTitan App Marketplace partner material states:

- **12,000+ businesses served**;
- **40M+ jobs completed annually**.

Source: https://help.servicetitan.com/docs/servicetitan-overview-for-app-marketplace-partners

40M jobs/year is roughly 3.33M jobs/month. The relevant question is not whether total volume is large; it is what tiny fraction of those jobs creates an upstream permit-applicability decision that ProjectPermit can serve.

Because no credible public permit-decision incidence has been established, use a broad low-incidence sensitivity range rather than calling any value conservative:

| Assumed permit-decision share | Candidate calls/year | Candidate calls/month |
|---:|---:|---:|
| 0.10% | 40,000 | ~3,333 |
| 0.30% | 120,000 | ~10,000 |
| 0.50% | 200,000 | ~16,667 |
| 1.00% | 400,000 | ~33,333 |
| 2.00% | 800,000 | ~66,667 |

A whole-platform incidence of only about **0.30%** would theoretically expose 10k candidate calls/month.

This does **not** mean ProjectPermit can currently capture them:

- ServiceTitan volume is predominantly U.S.-oriented while ProjectPermit currently covers seven Canadian municipalities;
- many jobs are in trades/scopes that may never require municipal permit research;
- applicability may already be known before the relevant workflow point;
- not every candidate call needs address/GIS data;
- not every address-aware call will be paid.

Therefore ServiceTitan is evidence that a sufficiently dense platform could support the call target, not evidence of current SAM.

Do not add U.S. municipalities speculatively. If a real partner identifies a bounded high-volume geography/workflow, that evidence should determine expansion priority.

## Jobber scale interpretation

Jobber remains the strongest current commercial wedge because of Canadian relevance and the Request/Quote/Job + Property workflow.

Platform-wide account/professional counts are useful only as a distribution ceiling. They are not candidate-call counts because Jobber spans many low/no-permit categories.

For Jobber, the measurements that matter are:

- number of candidate Requests/Quotes/Jobs in covered municipalities;
- trade mix;
- fraction requiring permit-applicability research;
- fraction where address/property context changes the answer;
- next workflow step changed by the result;
- willingness to pay.

Do not infer demand from total Jobber accounts.

## Property-management sensitivity

Large property-management platforms can provide very large unit denominators, but maintenance-work-order and permit-sensitive shares are usually not public enough to support reliable TAM claims.

Use the generic model:

`units x maintenance/capex events per unit x permit-decision share x covered-geography share x address-aware share`

Every multiplier after `units` must be observed or explicitly labeled as a scenario.

A platform with millions of units can still be a poor ProjectPermit market if only a tiny fraction of work orders have relevant construction scope or if applicability is already handled by vendors before the platform sees it.

## Procore / construction-platform sensitivity

Construction platforms provide potentially high-value project context and thousands of integration installs, but project count/customer and upstream permit-decision frequency are not public enough for a reliable denominator.

Use partner-level thresholds instead:

| Active integration accounts | External calls/account/month | Monthly external calls |
|---:|---:|---:|
| 100 | 10 | 1,000 |
| 250 | 20 | 5,000 |
| 500 | 20 | 10,000 |
| 1,000 | 25 | 25,000 |
| 2,000 | 25 | 50,000 |

The key question is whether a permit decision exists **before** a full permit workflow begins.

## Partner-by-partner evidence questions

### Permit-management vendors

Ask:

- How many new workflows enter the system each month?
- How many upstream candidate jobs were reviewed before it was known a permit was required?
- How many are rejected/not-required/out-of-scope?
- Is applicability already known before their service is invoked?

If they only receive known permit-positive jobs, the ProjectPermit upstream wedge is weak.

### Field-service / contractor software

Ask:

- candidate Requests/Quotes/Jobs per month in covered municipalities;
- permit-sensitive trade and project-family mix;
- fraction that triggers manual permit research;
- fraction needing property/zoning/heritage context;
- manual research minutes;
- whether the result changes quote, scheduling, dispatch or job creation.

### Property-management / CMMS

Ask:

- work orders/month;
- fraction involving structural/plumbing/window/door/deck/addition/renovation scopes;
- fraction that triggers permit research;
- municipality mix;
- decision point before vendor dispatch / approval / capital authorization;
- address-aware share.

### Integration consultants

A consultant serving several contractor accounts may be more valuable than one contractor because they can provide a bounded cross-customer denominator and identify which workflows repeat.

## Pricing x paid-call-density matrix

| Paid calls/month | $0.10/call | $0.25/call | $0.50/call | Interpretation |
|---:|---:|---:|---:|---|
| <1k | <$100 | <$250 | <$500 | Too small unless strategic evidence partner |
| 1k-10k | $100-$1k | $250-$2.5k | $500-$5k | Monetization validation stage |
| 10k-100k | $1k-$10k | $2.5k-$25k | $5k-$50k | Attractive solo-business scale if maintenance stays low |
| 100k+ | $10k+ | $25k+ | $50k+ | Strong distribution + monetization signal |

## Operational cost constraint

The preferred capability remains one where marginal compute cost is near zero:

- deterministic local rule evaluation;
- first-party municipal/open-data GIS;
- no server-side LLM requirement;
- no paid property-data API by default;
- no human permit runner/reviewer required for every call.

The major scaling cost is keeping jurisdiction rules, official sources and address adapters current and defensible.

Track:

> engineering/source-review hours per municipality per month, per 1,000 external calls, and per 1,000 paid calls.

A city generating little paid usage but requiring several maintenance hours/month should be removed or deprioritized.

## Revised go / no-go gates

### Distribution proof

- 2 independent representative E3 historical benchmarks;
- 1 repeated external workflow with 20+ successful calls;
- 3 external integrations + 100+ non-owner successful calls;
- 1 workflow with 500+ candidate calls/month;
- 1 partner/integration with 2,000+ candidate calls/month;
- credible path to 10,000+ **external successful preflights/month**.

### Monetization proof

Separately require evidence for:

- address-aware share;
- realized price / willingness to pay;
- paid-call volume;
- maintenance cost relative to revenue.

A strong checkpoint is 10,000 paid address-aware calls/month, but lower volume can still be commercially sufficient if realized price is higher and maintenance remains low.

### Reconsider or pause when

- after 20 qualified conversations nobody identifies a repeated upstream applicability decision;
- external testers use ProjectPermit only as a one-off lookup;
- candidate/issued multiplier is too low to support distribution;
- address-aware share or willingness to pay is too low to support monetization;
- partners mainly want full submission/expediting rather than preflight;
- nearly every call requires manual expert research;
- required data becomes dominated by expensive licensed sources.

## Bottom line

ProjectPermit does not need millions of customers. It needs a small number of integrations that generate repeated calls **and** a sufficiently large monetizable address-aware subset.

The near-term model is therefore two-dimensional:

> **distribution:** external successful preflights/month

and

> **economics:** paid address-aware calls/month x realized price - maintenance/infra cost

Do not collapse those two metrics into one.