# ProjectPermit Monthly Call Thresholds

Updated: 2026-08-27

The core business question is not how many municipalities can be coded. It is whether ProjectPermit can reach enough **repeated external workflow calls**, and then monetize enough of the higher-value address-aware calls, through a small number of distribution partners.

This document intentionally separates three quantities:

1. **external successful preflights** — proof that ProjectPermit occupies a repeated workflow;
2. **address-aware preflights** — calls that require civic-address / municipal property / GIS context;
3. **paid calls** — calls for which a buyer actually accepts a commercial price.

These quantities are not interchangeable. Unless explicitly sourced, percentages below are sensitivity variables, not forecasts.

See also:

- `docs/COVERED_MARKET_CALL_SENSITIVITY.md` for the covered-city issuance floor and paid-share analysis;
- `docs/REACHABLE_CONTRACTOR_DENOMINATOR.md` for the seven-city business-location floor;
- `docs/TRADE_WORKLOAD_EVIDENCE.md` for direct-contractor versus platform-level cadence evidence.

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

## Evidence-weighted shapes for 10k external calls/month

The arithmetic shapes are still useful, but they no longer have equal evidentiary weight.

| Distribution shape | Calls/customer/month | Customers/integrations needed | Total external calls/month | Current evidence weight |
|---|---:|---:|---:|---|
| High-volume direct contractor accounts | 80 | 125 | 10,000 | **Aggressive / unproven as a repeatable Canadian distribution shape** |
| Medium direct contractor accounts | 25 | 400 | 10,000 | Possible, but requires broad acquisition and cadence proof |
| Property portfolios | 20 | 500 | 10,000 | Unproven until permit-sensitive work-order incidence is measured |
| Strong SaaS / permit-ops integrations | 2,000 | 5 | 10,000 | **Primary commercial path** |
| Mid-sized integrations / multi-account partners | 500 | 20 | 10,000 | **Primary commercial path** |
| One platform workflow | 10,000 | 1 | 10,000 | **High-leverage path if bounded covered-geography volume exists** |

Why the direct 80/month shape was downgraded:

- Vancouver 2024 public building-permit data shows corporate-like contractor tokens maxing at 47 permits/year across all building permits, 35/year for Addition/Alteration, and 20/year for residential renovation; the maximum observed single month was 8.
- A public iPermit Marketplace testimonial does show one HVAC contractor sending roughly 80+ jobs/month to a permit-management vendor, proving that high-volume outliers exist.
- One outlier does not establish that 125 similar reachable Canadian contractor accounts exist or that all 80 jobs/month would require a ProjectPermit applicability preflight.

Therefore `125 × 80/month` remains arithmetic sensitivity only. It is not the base distribution plan.

## Stable Toronto trade-workflow volume

Toronto Open Data provides a much stronger signal for **aggregated workflow volume** than for individual-account cadence.

Using Active + Cleared permit records, deduplicated by permit number + revision, Mechanical + Plumbing + Drain/Site Service issued revisions were:

| Year | Combined trade permit revisions | Avg/month | Share of all issued revisions |
|---:|---:|---:|---:|
| 2023 | 20,085 | **1,673.8** | 53.20% |
| 2024 | 20,013 | **1,667.8** | 53.44% |
| 2025 | 20,733 | **1,727.8** | 54.13% |

This is a persistent three-year band, not a one-year spike.

Important boundary: permit revisions are workflow events, not unique projects or unique customers. Multiple Mechanical or Plumbing permits can be associated with a broader project. This evidence therefore supports the **platform/integration flow thesis**, not a 1:1 contractor-account model.

A partner that aggregates a meaningful portion of Toronto's trade workflow could plausibly expose 500+ monthly candidate events. Whether those events occur early enough for ProjectPermit, and what fraction require applicability research, remains an external validation question.

## Covered-city activity floor

A clean same-year first-party 2024 floor previously established for Toronto, Ottawa, Mississauga, Laval and Vancouver is:

- Toronto: 36,887 permits in the earlier city issuance series;
- Ottawa: 7,688 permits;
- Mississauga: 4,458 permits;
- Laval: 1,415 construction/improvement permits;
- Vancouver: 3,705 building-permit subtotal.

Combined: **54,153 issued permits/year = 4,512.75/month**.

Do not silently merge that earlier issuance series with the Toronto Active+Cleared `permit revision` series above; they are useful for different questions and have different definitions.

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

The candidate/issued multiplier is not externally measured. It must not be treated as observed demand.

## Reachable contractor denominator

Statistics Canada June 2026 CSD employer-location data gives a seven-city broad renovation-trade floor of **14,077 employer business locations** for NAICS 2361 + 2381 + 2382 + 2383.

Toronto + Ottawa + Mississauga account for about 70% of that observed broad employer-location floor. Province-level companion data also shows substantial without-employee contractor populations, especially in Ontario and British Columbia, but those provincial ratios must not be multiplied into city counts and presented as observed municipal SAM.

This evidence says the business-account pool itself is not obviously too small. The harder variable is still **candidate permit-applicability events per account/integration per month**.

## ServiceTitan scale sensitivity

Public ServiceTitan partner material has reported platform scale in the tens of millions of jobs annually. The relevant question is not total platform volume; it is what fraction of jobs creates an upstream permit-applicability decision in ProjectPermit's covered geographies.

Use platform-wide incidence only as sensitivity, never as current SAM. The platform is predominantly U.S.-oriented while ProjectPermit currently covers seven Canadian municipalities, many jobs are low/no-permit, applicability may already be known, and not every address-aware call will be paid.

Do not add U.S. municipalities speculatively. If a real partner identifies a bounded high-volume geography/workflow, that evidence should determine expansion priority.

## Jobber scale interpretation

Jobber remains the strongest current Canadian commercial wedge because of its Request/Quote/Job + Property workflow.

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

`units × maintenance/capex events per unit × permit-decision share × covered-geography share × address-aware share`

Every multiplier after `units` must be observed or explicitly labeled as a scenario.

A platform with millions of units can still be a poor ProjectPermit market if only a tiny fraction of work orders have relevant construction scope or if applicability is already handled by vendors before the platform sees it.

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

The next search priority is explicitly a partner or integration capable of exposing **500+ bounded candidate events/month** in covered geographies, not another broad directory listing or another speculative adapter.

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

Current public evidence now favors aggregation over direct-account volume:

> **ordinary direct contractor:** useful for validation, weak as the main scale engine

> **high-volume trade/permit operator:** plausible but must be specifically proven

> **platform / multi-account integration:** current primary path to 10k monthly external calls

The near-term model remains two-dimensional:

> **distribution:** external successful preflights/month

and

> **economics:** paid address-aware calls/month × realized price − maintenance/infra cost

Do not collapse those two metrics into one.