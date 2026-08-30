# Regulatory Depth Call-Volume Model — 2026-08-30

## Purpose

Estimate whether the Layer-C hypothesis could plausibly support meaningful repeated API volume before any deeper regulatory-content engineering or licensing spend.

Layer C hypothesis:

> `project / estimate facts -> current project-specific regulatory obligation bundle + official evidence + freshness/change identity`

This is **market sizing**, not buyer evidence. None of the calculations below are E2, E3, E4 or E5.

The goal is to answer a narrower question:

> If buyers eventually confirm the workflow, is the underlying quote/project activity large enough to support thousands or tens of thousands of calls per month, or is this inherently a tiny niche?

## 1. External denominator anchors

### Canada residential-construction firms

Statistics Canada's 2026 study of NAICS 236110 residential building construction reports **29,722 firms with employees in 2023**.

Source:
https://www150.statcan.gc.ca/n1/pub/36-28-0001/2026002/article/00003-eng.htm

Important scope limitations:

- firms without employees are excluded;
- specialty trade contractors are excluded;
- the study is deliberately narrower than all firms participating in residential construction;
- this is a firm denominator, not a count of estimates or projects.

This makes 29,722 a useful conservative core-builder denominator rather than a complete construction TAM.

### Current Canadian project activity

CMHC reports **259,028 housing starts across Canada in 2025**.

Source:
https://www.cmhc-schl.gc.ca/media-newsroom/news-releases/2026/housing-starts-december-2025

CMHC's July 2026 data show:

- 247,377-unit six-month housing-start trend (SAAR);
- 141,480 units in centres of 50,000+ with approved permits but not yet started;
- 373,091 units under construction.

Source:
https://www.cmhc-schl.gc.ca/media-newsroom/news-releases/2026/housing-starts-construction-data-july-2026

These are housing units, not API-call units. Multi-unit buildings mean one regulatory workflow can correspond to many units, so housing starts must **not** be used one-for-one as Layer-C calls.

Statistics Canada reports June 2026 building permits worth **$14.9B** and residential building-construction investment of about **$16.1B** for the month.

Sources:
https://www.statcan.gc.ca/en/subjects-start/construction
https://www150.statcan.gc.ca/n1/daily-quotidien/260819/dq260819a-eng.htm

Again, these values establish economic activity, not call counts.

### Renovation activity

CMHC's 2026 Mortgage Consumer Survey reports **63% of mortgage consumers are planning renovations**; its 2025 survey found 55% renovated within the prior three years.

Sources:
https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-research/surveys/mortgage-consumer-surveys/2026-mortgage-consumer-survey
https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-research/surveys/mortgage-consumer-surveys/2025-mortgage-consumer-survey

This supports a large recurring renovation pool but does not establish the fraction requiring regulatory lookup.

## 2. Software-workflow scale anchors

These are useful because ProjectPermit is trying to sell a machine-consumable capability, not a consumer legal-information website.

### Buildertrend

Current public claims:

- **20,000+ construction companies** rely on Buildertrend;
- **2M+ projects** have been completed on the platform;
- the product covers lead -> estimating/financials -> project execution.

Sources:
https://buildertrend.com/
https://buildertrend.com/about/

### Jobber

Current public claims:

- **100K+ businesses** use Jobber;
- **400K+ service professionals**;
- **92M+ jobs completed**;
- 50+ service industries;
- workflow runs from first quote to final payment.

Source:
https://www.getjobber.com/

Jobber's 2026 Home Service Trends Report also says 69% of surveyed service businesses close more than half their quotes, confirming quoting is a central recurring workflow. The survey includes HVAC, plumbing, roofing, electrical, general contracting and other trades, but it also includes low-regulatory categories such as cleaning and lawn care.

Source:
https://www.getjobber.com/home-service-trends-report/

Therefore Jobber's full customer/job count must **not** be treated as regulatory-sensitive TAM.

### Buildxact

Buildxact currently reports **988,783 quotes produced** on its platform and is explicitly focused on residential builders/remodelers and estimating/project management.

Source:
https://www.buildxact.com/company/about/

This is a cumulative workflow-scale signal, not a monthly denominator.

## 3. Core Canadian builder call model

Use only the 29,722 employee residential-construction firms as the starting population.

Formula:

`monthly calls = firms × estimate/project workflows per firm/month × Layer-C-sensitive share × calls per sensitive workflow`

The last three variables are explicit assumptions. They are **not** observed buyer facts yet.

| Scenario | Workflows / firm / month | Layer-C-sensitive share | Calls / sensitive workflow | Canada calls / month |
|---|---:|---:|---:|---:|
| Low | 1 | 10% | 1.0 | **2,972** |
| Base | 3 | 25% | 1.2 | **26,750** |
| High | 8 | 40% | 1.5 | **142,666** |

Annualized:

- Low: **35.7K calls/year**
- Base: **321K calls/year**
- High: **1.71M calls/year**

### Interpretation

The important result is not the exact base number. It is that the market does not require heroic assumptions to cross the project's 500-calls/month relevance threshold **nationally**.

Even the low scenario is ~3K calls/month.

However, this is full-Canada core-builder TAM. ProjectPermit does not currently serve all of Canada.

## 4. Current seven-city geographic SAM proxy

Current municipalities:

- Toronto
- Ottawa
- Mississauga
- Vancouver
- Laval
- Gatineau
- Longueuil

Statistics Canada 2021 Census populations:

- Toronto: 2,794,356
- Ottawa: 1,017,449
- Mississauga: 717,961
- Vancouver: 662,248
- Laval: 438,366
- Gatineau: 291,041
- Longueuil: 254,483

Combined: **6,175,904**.

Canada 2021 Census population: **36,991,981**.

Population-share proxy: **16.7%**.

Sources:
https://www12.statcan.gc.ca/census-recensement/2021/as-sa/98-200-x/2021001/98-200-x2021001-eng.cfm
https://www.statcan.gc.ca/en/hp/estima

This is only a geographic proxy. Construction activity, project mix and software adoption are not uniform by population.

Applying 16.7% mechanically to the Canadian core-builder scenarios gives:

| Scenario | Current 7-city proxy calls / month | Calls / year |
|---|---:|---:|
| Low | **496** | 5,955 |
| Base | **4,466** | 53,591 |
| High | **23,818** | 285,821 |

### 500-calls/month threshold sensitivity

To reach 500 monthly calls within the current 7-city proxy:

- Low scenario: essentially **100%** of modelled eligible workflow volume;
- Base scenario: about **11.2%**;
- High scenario: about **2.1%**.

This is strategically important.

> Current seven-city coverage is large enough to test repeated use, but it is not automatically a large commercial SAM at low per-call pricing.

Do **not** respond by adding cities now. First prove the workflow and distribution conversion.

## 5. Price sensitivity — not a pricing recommendation

The current ProjectPermit permit-preflight launch price is **$0.20/call**. Layer C would be a materially deeper product and has unresolved licensing/maintenance costs, so it must not automatically inherit that price.

For perspective only, at 100% modelled call capture:

### Canada base scenario: 26,750 calls/month

- $0.20/call -> **$5.35K/month**
- $1.00/call -> **$26.75K/month**
- $2.50/call -> **$66.88K/month**

### Current 7-city base proxy: 4,466 calls/month

- $0.20/call -> **$893/month**
- $1.00/call -> **$4.47K/month**
- $2.50/call -> **$11.16K/month**

These are theoretical gross revenue sensitivities at impossible 100% capture and before partner discounts, licences, maintenance or payment costs.

The conclusion is directional:

> `$0.20 + seven cities` is not an attractive end-state for a deeper maintained regulatory product.

If Layer C is proven, its economics likely require some combination of:

- broader geographic coverage after validation;
- a higher-value B2B/API price;
- account/subscription/volume contracts;
- platform distribution with meaningful repeated calls;
- a broader set of regulatory-sensitive builder/trade workflows.

## 6. Platform-distribution threshold math

Public platform scale shows why distribution can matter more than adding one municipality.

### Buildertrend-like channel

Buildertrend has 20,000+ construction companies.

Pure sensitivity examples:

- **1%** adoption × **3** Layer-C checks/month = **600 calls/month**
- **5%** adoption × **5** checks/month = **5,000 calls/month**

These are assumptions, not observed Buildertrend demand. They simply show that one construction-software channel can cross the 500/month threshold with low penetration if the workflow is real.

### Jobber-like channel

Jobber has 100K+ businesses, but many are not regulatory-sensitive trades.

Pure sensitivity examples across the full customer base:

- **0.5%** of accounts × **2** checks/month = **1,000 calls/month**
- **2%** of accounts × **5** checks/month = **10,000 calls/month**

Again, this is not a claim that Jobber would adopt ProjectPermit or that all Jobber accounts are eligible. It demonstrates channel leverage.

### Distribution implication

A platform/API partner with a few hundred genuinely eligible active accounts is more strategically valuable than many passive registry listings.

This reinforces the current priority:

> **regulatory depth validation -> software/platform distribution -> E4 -> E5**

not:

> more MCP directories -> more crawler traffic.

## 7. Practical SOM targets

These are execution targets, not forecast claims.

A useful first real-workflow milestone could be:

| Active external accounts | Checks/account/month | Calls/month |
|---:|---:|---:|
| 100 | 3 | 300 |
| 200 | 3 | **600** |
| 500 | 5 | **2,500** |

The 200-account / 3-check case crosses 500 calls/month without requiring mass-market adoption.

A single software partner may make 200 active end-accounts much more achievable than direct contractor acquisition one business at a time.

## 8. What this model proves and does not prove

### It supports

- There is enough underlying construction/quote activity for Layer C to become a meaningful API-call market.
- The national core-builder opportunity plausibly reaches tens of thousands of monthly calls under moderate assumptions.
- Platform distribution has high leverage: tiny adoption fractions of a 20K-100K account platform can cross 500 calls/month.
- Current seven-city coverage is enough for validation but not obviously enough for a large low-price end-state.

### It does not support

- that 25% of estimates are actually Layer-C sensitive;
- that builders will externalize the work;
- that a $1 or $2.50 call price is acceptable;
- that Buildertrend, Jobber or Buildxact will integrate;
- that current 7-city population share equals construction-workflow share;
- that code-content licensing economics will work;
- any E2/E3/E4/E5 score increase.

Those remain buyer/usage questions.

## 9. Decision from the model

**Do not kill Layer C for market-size reasons.** The plausible call-volume ceiling is large enough to continue validation.

But also **do not build Layer C yet**.

The model exposes the two real bottlenecks:

1. **eligible-workflow fraction** — how often deeper regulatory obligations materially affect an estimate/project;
2. **distribution/externalization** — whether software buyers prefer an external maintained API enough to integrate and send repeated calls.

The active buyer probes with SubmitX, Contrax, Join and BuildPass are aimed directly at bottleneck #1. The next decisive evidence is a bounded monthly denominator and a concrete workflow consequence.

## Bottom line

Current evidence now says:

- **maintenance feasibility:** viable with source-specific Tier A/B/C monitoring;
- **market-size feasibility:** plausible; not inherently niche;
- **licensing/cash feasibility:** unresolved for deeper code content;
- **buyer volume:** still unproven;
- **real external usage:** E4 = 0;
- **payment:** E5 = 0.

Therefore the correct sequence remains:

> **prove Layer-C denominator/consequence -> prove platform workflow -> clarify/licence only the data actually needed -> build the smallest representative Layer-C slice -> E4 -> E5**
