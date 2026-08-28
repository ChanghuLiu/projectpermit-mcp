# ProjectPermit Monthly Call Thresholds

Updated: 2026-08-28

The core business question is not how many municipalities can be coded. It is whether ProjectPermit can reach enough **repeated external workflow calls**, and then monetize enough of the higher-value address-aware calls, through a small number of distribution partners.

This document intentionally separates three quantities:

1. **external successful preflights** — proof that ProjectPermit occupies a repeated workflow;
2. **address-aware preflights** — calls that require civic-address / municipal property / GIS context;
3. **paid calls** — calls for which a buyer actually accepts a commercial price.

These quantities are not interchangeable. Unless explicitly sourced, percentages below are sensitivity variables, not forecasts.

See also:

- `docs/COVERED_MARKET_CALL_SENSITIVITY.md` for the covered-city issuance floor and paid-share analysis;
- `docs/REACHABLE_CONTRACTOR_DENOMINATOR.md` for the seven-city business-location floor;
- `docs/TRADE_WORKLOAD_EVIDENCE.md` for direct-contractor, broad trade-flow and current-family-like workflow evidence;
- `docs/COMPETITIVE_LANDSCAPE.md` for the competitor matrix and differentiation gate that must be satisfied in addition to call-volume gates.

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
| High-volume direct contractor accounts | 80 | 125 | 10,000 | **Arithmetic only; unsupported as a repeatable current-family residential-builder cadence** |
| Medium direct contractor accounts | 25 | 400 | 10,000 | **Arithmetic only; current direct-account evidence does not support assuming this cadence** |
| Property portfolios | 20 | 500 | 10,000 | Unproven until permit-sensitive work-order incidence is measured |
| Strong SaaS / multi-account integrations | 2,000 | 5 | 10,000 | **Primary arithmetic path, but current-family fit remains unproven** |
| Mid-sized integrations / multi-account partners | 500 | 20 | 10,000 | **Primary arithmetic path, but current-family fit remains unproven** |
| One platform workflow | 10,000 | 1 | 10,000 | High leverage only if bounded covered-geography **current-family** volume exists |

### Why the direct-account 25/month and 80/month shapes are downgraded

- Vancouver 2024 public building-permit data shows corporate-like contractor tokens maxing at 47 permits/year across all building permits, 35/year for Addition/Alteration, and 20/year for residential renovation; the maximum observed single month was 8.
- Buildertrend's 2026 Modern Builder Playbook reports that **67% of surveyed builders manage more than six projects per year**. The survey covers established Buildertrend users with more than $1M annual revenue, and its concrete scaled design-build example, Cardinal Crest Homes, completes **15–20 custom homes/year**. This does **not** provide a Canadian average, and a completed project is not the same thing as a ProjectPermit call, but it provides a useful cadence sanity check: the public first-party evidence is framed in projects/year, not tens of current-family projects/month per ordinary builder account. Source: `https://buildertrend.com/ebooks/modern-builder-playbook-2026/`.
- A public iPermit Marketplace testimonial does show one HVAC contractor sending roughly 80+ jobs/month to a permit-management vendor, proving that high-volume trade-service outliers exist. That workflow is not evidence for ordinary residential builder/remodeler current-family cadence.
- One project could theoretically trigger more than one preflight decision. That multiplier is currently **unmeasured**. Do not turn projects/year into calls/month by assuming repeated calls per project; require an E2 bounded workflow claim or E4 observed usage first.

Therefore both `400 × 25/month` and `125 × 80/month` remain arithmetic sensitivity only. Direct builders/remodelers remain valuable for E3 accuracy benchmarks and early E4 pilots, but they are **not the base commercial scale engine** unless a real partner demonstrates materially higher repeated current-family call cadence.

## Toronto: broad workflow density vs current-family fit

Toronto Open Data gives strong evidence that permit workflows can be dense at city/platform level, but the broad trade series must **not** be treated as current ProjectPermit addressable volume.

Using Active + Cleared permit records, deduplicated by permit number + revision, Mechanical + Plumbing + Drain/Site Service issued revisions were:

| Year | Combined broad trade permit revisions | Avg/month | Share of all issued revisions |
|---:|---:|---:|---:|
| 2023 | 20,085 | **1,673.8** | 53.20% |
| 2024 | 20,013 | **1,667.8** | 53.44% |
| 2025 | 20,733 | **1,727.8** | 54.13% |

This is a persistent three-year band, but the City `WORK` labels show why it is not current-product SAM. In 2024, most of the Mechanical/Plumbing/Drain volume sits in broad labels such as `Building Permit Related(PS)`, `Building Permit Related(MS)` and `Building Permit Related (DR)`. Those labels do not expose enough scope detail to map safely into the current eight project families.

ProjectPermit currently has no dedicated general HVAC/electrical/mechanical-service family, and `kitchen_bath_plumbing` cannot be equated with all Plumbing/Drain permits.

Therefore:

> **~1.7k broad trade permit revisions/month proves workflow density, not current serviceable demand.**

### Current-family-like diagnostic

A conservative/diagnostic match against City `WORK` labels that visibly resemble current ProjectPermit families produced:

| Year | Non-exclusive current-family-like issued-workflow signal | Avg/month |
|---:|---:|---:|
| 2023 | **6,695** | **557.9** |
| 2024 | **6,690** | **557.5** |
| 2025 | **7,038** | **586.5** |

The 2024 signal is heavily dominated by `Interior Alterations` (~4.8k/year). It also has major limitations:

- it is non-exclusive label matching, not unique projects or SAM;
- `Interior Alterations` is broader than a guaranteed ProjectPermit candidate;
- ambiguous MEP records remain unmapped rather than being forced into `kitchen_bath_plumbing`;
- `kitchen_bath_plumbing = 0` in the label matcher reflects weak label visibility, not zero market;
- every observed item is a downstream issued/permit-positive workflow event, not an upstream Request/Quote with unresolved applicability;
- candidate/issued multiplier, address-aware share and willingness to pay remain unknown.

The most defensible current reading is:

> Toronto visibly contains roughly **560–587 current-family-like issued workflow events/month**, but even that is only a diagnostic signal — not a callable preflight denominator.

A partner must expose the upstream subset where:

1. the scope maps to a current family;
2. permit applicability is still unresolved;
3. the event occurs before quote/job routing;
4. ProjectPermit can be called repeatedly.

Until that exists, Toronto's broad MEP flow must not be used to support the 10k-call target.

## Covered-city activity floor — broad activity, not serviceable SAM

A clean same-year first-party 2024 floor previously established for Toronto, Ottawa, Mississauga, Laval and Vancouver is:

- Toronto: 36,887 permits in the earlier city issuance series;
- Ottawa: 7,688 permits;
- Mississauga: 4,458 permits;
- Laval: 1,415 construction/improvement permits;
- Vancouver: 3,705 building-permit subtotal.

Combined: **54,153 issued permits/year = 4,512.75/month**.

This number is useful as evidence that municipal permit activity is substantial across covered cities. It is **not ProjectPermit serviceable SAM** because:

- permit universes include project types outside the current eight families;
- some records are downstream sub-permits/revisions rather than one candidate project;
- permit-positive issuance says nothing about whether applicability was uncertain upstream;
- the city series use different permit definitions.

Do not silently merge this earlier issuance series with the Toronto Active+Cleared `permit revision` series; they answer different questions.

Gatineau and Longueuil remain excluded from this exact cumulative floor rather than being guessed.

The old candidate/issued sensitivity remains arithmetic only:

| Candidate preflights per broad observed issued permit | Implied external preflights/month |
|---:|---:|
| 1.0x | 4,513 |
| 1.5x | 6,769 |
| 2.0x | 9,026 |
| 2.22x | ~10,019 |
| 3.0x | 13,538 |
| 5.0x | 22,564 |

Because the denominator itself is broader than current-family serviceable work, **do not use 2.22× as evidence that the present product can reach 10k calls/month**. The candidate/issued multiplier and current-family share are both externally unmeasured.

## Reachable contractor denominator

Statistics Canada June 2026 CSD employer-location data gives a seven-city broad renovation-trade floor of **14,077 employer business locations** for NAICS 2361 + 2381 + 2382 + 2383.

Toronto + Ottawa + Mississauga account for about 70% of that observed broad employer-location floor. Province-level companion data also shows substantial without-employee contractor populations, especially in Ontario and British Columbia, but those provincial ratios must not be multiplied into city counts and presented as observed municipal SAM.

This evidence says the business-account pool itself is not obviously too small. The harder variables are still:

- relevant current-family candidate events per account/integration;
- whether permit applicability is unresolved at Request/assessment/quote time;
- address-aware share;
- willingness to pay.

### Direct residential builder cadence sanity check

The 14,077-location employer floor answers `how many businesses exist`, not `how many ProjectPermit calls each business can generate`.

Buildertrend's April 2026 first-party report provides a useful but limited cadence check:

- 67% of surveyed builders manage more than six projects/year;
- the survey population is not Canada-only and consists of established Buildertrend users generating more than $1M in annual revenue;
- one highlighted scaled design-build company completes 15–20 custom homes/year;
- Buildertrend states that more than 20,000 construction companies use the platform.

Do not convert these values directly into ProjectPermit calls. Projects, estimates, quotes and preflight decisions are different event types. The correct inference is narrower:

> **ordinary direct-account project cadence does not currently justify assuming 25–80 current-family calls/account/month.**

If a builder project contains several meaningful permit-applicability decision events, that repeated-call multiplier must be measured in a real workflow. Until then, the scale strategy should favor platform/multi-account aggregation over hundreds of one-by-one contractor integrations.

## ServiceTitan scale sensitivity

Public ServiceTitan partner material has reported platform scale in the tens of millions of jobs annually. The relevant question is not total platform volume; it is what fraction of jobs creates an upstream permit-applicability decision in ProjectPermit's **current families and covered Canadian geographies**.

Use platform-wide incidence only as sensitivity, never as current SAM. The platform is predominantly U.S.-oriented, many jobs are low/no-permit, much high-frequency MEP work is not covered by the current family set, applicability may already be known, and not every address-aware call will be paid.

Do not add U.S. municipalities or HVAC/electrical families speculatively. If a real partner identifies a bounded high-volume workflow, that evidence should determine expansion priority.

## Jobber scale interpretation

Jobber remains the strongest current Canadian commercial wedge because of its Request/Quote/Job + Property workflow.

Platform-wide account/professional counts are useful only as a distribution ceiling. They are not candidate-call counts because Jobber spans many low/no-permit categories.

For Jobber, the measurements that matter are:

- number of candidate Requests/Assessments/Quotes/Jobs in covered municipalities;
- fraction mapping to a current ProjectPermit family;
- fraction still requiring permit-applicability research before the Quote/Job is finalized;
- fraction where address/property context changes the answer;
- next workflow step changed by the result;
- willingness to pay.

Do not infer demand from total Jobber accounts.

## Property-management sensitivity

Large property-management platforms can provide very large unit denominators, but maintenance-work-order and permit-sensitive shares are usually not public enough to support reliable TAM claims.

Use the generic model:

`units × maintenance/capex events per unit × current-family share × unresolved permit-decision share × covered-geography share × address-aware share`

Every multiplier after `units` must be observed or explicitly labeled as a scenario.

A platform with millions of units can still be a poor ProjectPermit market if only a tiny fraction of work orders map to current project families or if applicability is already handled by vendors before the platform sees it.

## Partner-by-partner evidence questions

### Permit-management vendors

Ask:

- How many new workflows enter the system each month?
- Are jobs already known permit-positive before intake?
- If not, how many still require a `permit required?` decision?

Current external boundary evidence from Permitio points toward downstream permit-filing intake already being permit-positive. That reply is E1, not E2, because no bounded recent denominator was provided. Do not overgeneralize it to all permit vendors, but prioritize upstream workflows instead of filing intake.

### Field-service / contractor software

Ask:

- candidate Requests/Assessments/Quotes/Jobs per month in covered municipalities;
- current-family project mix;
- fraction that triggers manual permit-applicability research;
- fraction needing property/zoning/heritage context;
- manual research minutes;
- whether the result changes quote, scheduling, dispatch or job creation.

### Property-management / CMMS

Ask:

- work orders/month;
- current-family share;
- fraction that triggers permit research before vendor dispatch / approval / capital authorization;
- municipality mix;
- address-aware share.

### Integration consultants / estimators

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
- 1 workflow with **500+ current-family candidate events/month** in covered geography;
- 1 partner/integration with **2,000+ current-family candidate events/month**, or equivalent proven aggregation;
- credible path to 10,000+ **external successful current-family preflights/month**.

The next search priority is explicitly a partner or integration capable of exposing bounded **current-family** Request/Assessment/Quote volume, not another broad directory listing, trade-volume statistic or speculative adapter.

### Differentiation proof

Call volume alone is no longer enough. `docs/COMPETITIVE_LANDSCAPE.md` documents direct overlap from One Ontario/LandLogic, Clariti Guide, QwikScope Greenlight, Permitech and PermitMint, plus province-level infrastructure in B.C.

Before materially expanding coverage or building production adapters, require evidence that a real software/integration buyer needs the **specific ProjectPermit delivery model**, not merely permit guidance in general.

A credible differentiation proof should include at least one of:

- **two independent third-party software/integration buyers** explicitly identify why existing municipal portals, One Ontario/LandLogic, Clariti, permit-service vendors, or other permit-intelligence products do not fit their pre-quote / work-order workflow;
- one bounded partner workflow where the existing alternative requires municipality procurement, custom implementation, manual research, or human permit operations, while a lightweight ProjectPermit-style API can be invoked directly;
- one external pilot where the **same integration** uses ProjectPermit across multiple municipalities and would otherwise need separate municipal integrations or manual rule research;
- an E5 buyer accepts a concrete per-call or paid-pilot term specifically for the machine-readable evidence-linked applicability result.

Do **not** treat the following as differentiation by themselves: Canada coverage, address resolution, GIS, citations, conversational AI, cross-jurisdiction data, or having an API. Competitors already demonstrate those capabilities individually.

### Monetization proof

Separately require evidence for:

- address-aware share;
- realized price / willingness to pay;
- paid-call volume;
- maintenance cost relative to revenue.

A strong checkpoint is 10,000 paid address-aware calls/month, but lower volume can still be commercially sufficient if realized price is higher and maintenance remains low.

### Reconsider or pause when

- after 20 qualified conversations nobody identifies a repeated upstream applicability decision;
- current-family upstream candidate volume is too small even when aggregated;
- external testers use ProjectPermit only as a one-off lookup;
- applicability is usually already known before the Request/Quote workflow point;
- address-aware share or willingness to pay is too low to support monetization;
- partners mainly want full submission/expediting rather than preflight;
- nearly every call requires manual expert research;
- required data becomes dominated by expensive licensed sources;
- LandLogic / One Ontario or another provider exposes a self-serve Canadian permit-requirement API that satisfies the same third-party workflow at competitive economics;
- target SaaS/integrators repeatedly report that an existing municipal portal, land-intelligence provider, permit-intelligence vendor, or permit-service partner already solves the decision well enough;
- the only remaining distinction is `cheaper`, without enough E4/E5 paid volume to justify ongoing rule maintenance.

## Bottom line

ProjectPermit does not need millions of customers. It needs a small number of integrations that generate repeated **current-family** calls and a sufficiently large monetizable address-aware subset **that existing alternatives do not already satisfy**.

Current public evidence says:

> **ordinary direct contractor:** useful for E3/E4 validation, weak as the main scale engine; current builder cadence evidence does not support assuming 25–80 current-family calls/account/month

> **broad HVAC/plumbing/mechanical trade flow:** real and high-frequency, but mostly not safely countable as current ProjectPermit demand

> **current-family-like Toronto issued-work signal:** roughly 560–587/month, diagnostic only and heavily dominated by Interior Alterations

> **platform / multi-account integration:** still the most plausible aggregation path, but current-family upstream incidence is unproven

> **generic permit-guide / permit-intelligence capability:** already crowded; a narrower Canadian developer/agent API delivery model is the remaining hypothesis, not a proven moat

The near-term model is now three-dimensional:

> **distribution:** external successful current-family preflights/month

> **differentiation:** why the target buyer cannot or will not use an existing alternative

and

> **economics:** paid address-aware calls/month × realized price − maintenance/infra cost

Do not collapse those metrics, substitute broad permit volume for current-product demand, or pass the scale gate without also passing the differentiation gate.