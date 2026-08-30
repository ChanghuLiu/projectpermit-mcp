# Platform denominator + payer gate — 2026-08-30

## Purpose

Turn public construction-software scale and integration mechanics into a stricter distribution/commercial test for ProjectPermit Layer C.

This note answers three separate questions:

1. Can one software channel plausibly generate 500 / 2K / 10K monthly calls without mass-market adoption?
2. Who can actually pay — AI agent, contractor account, or software platform?
3. Which channels have enough integration/payment infrastructure to test without first winning an enterprise platform deal?

This is **market/distribution modeling, not buyer evidence**. It does not change E2/E3/E4/E5.

## 1. Public platform scale anchors

### Jobber

Current public claims:

- 100K+ businesses use Jobber;
- 400K+ service pros;
- 92M+ jobs completed;
- construction/contracting, electrical, HVAC, plumbing and roofing are explicitly served industries;
- Jobber runs from first quote through job and payment.

Official sources:

- https://www.getjobber.com/
- https://www.getjobber.com/about/

Jobber's 2026 Home Service Trends Report says quoting is a major recurring workflow and more than half of AI adopters use AI for estimates/quotes/contracts. The same report also includes lower-regulatory industries, so the entire Jobber base must **not** be treated as Layer-C eligible.

Official source:

- https://www.getjobber.com/home-service-trends-report/

Developer/distribution route:

- public GraphQL/OAuth Developer Center;
- App Marketplace apps can serve many Jobber accounts;
- draft/custom integrations are restricted once they exceed 5 paying accounts unless approved.

Official sources:

- https://developer.getjobber.com/docs/
- https://developer.getjobber.com/docs/custom_integrations/

### Buildertrend

Current public claims:

- 20,000+ builders use Buildertrend;
- the product explicitly spans lead -> proposal/estimate -> job costing -> project execution;
- 2M+ projects have historically been completed on the platform.

Official sources:

- https://buildertrend.com/
- https://buildertrend.com/about/

Buildertrend has a Marketplace and public evidence that integrations are API-based, but this research pass did not find a general self-serve public developer onboarding path equivalent to Jobber or ServiceM8.

Official sources:

- https://buildertrend.com/help-article/buildertrend-marketplace/
- https://buildertrend.com/blog/marketplace-crm-integrations/

### ServiceTitan

As of January 31, 2026, ServiceTitan reported approximately **10,800 Active Customers** and FY2026 gross transaction volume of **$82.1B**.

Official sources:

- https://investors.servicetitan.com/static-files/84e016f3-9a75-4199-ad42-b3babe1bb3dd
- https://investors.servicetitan.com/news-releases/news-release-details/servicetitan-announces-fiscal-fourth-quarter-and-full-fiscal

Developer/distribution route:

- third-party software organizations can request an integration environment;
- public apps can pursue App Marketplace certification;
- OAuth/API integration is a supported product surface.

Official sources:

- https://developer.servicetitan.io/request-access/
- https://developer.servicetitan.io/docs/faqs/developers

### Buildxact

Buildxact publicly reports:

- 988,783 quotes produced;
- $134B quoted;
- $18B of projects delivered;
- explicit focus on residential builders/remodelers, estimating and project management.

Official source:

- https://www.buildxact.com/ca/company/about/

The cumulative quote statistics imply an average historical quote value of roughly **$135K** (`$134B / 988,783`). This is not a current monthly volume or a customer count. It does show that Buildxact sits on high-value estimate workflows where a regulatory requirement can plausibly change scope, professional involvement, schedule or price.

A general public third-party developer route was not confirmed in this pass.

### ServiceM8

ServiceM8 serves trade/service businesses through quote -> job -> invoice/payment workflows and says businesses around the world have managed more than tens of billions of dollars of jobs through the platform.

Official sources:

- https://www.servicem8.com/
- https://www.servicem8.com/ca/

Its current plans also expose a useful per-account workflow denominator:

- Free: 30 new jobs/month;
- Starter: 50;
- Growing: 150;
- Premium: 500;
- Premium Plus: 1500+.

Official source:

- https://www.servicem8.com/ca/pricing

Developer/distribution route:

- public REST API;
- public Add-on Store;
- add-ons can be promoted to thousands of ServiceM8 businesses;
- ServiceM8 can bill a monthly add-on fee directly on the customer's ServiceM8 bill;
- developer receives 90% and ServiceM8 keeps 10% for billing;
- both upfront/ongoing billing models are supported.

Official sources:

- https://developer.servicem8.com/
- https://developer.servicem8.com/docs/servicem8-add-on-store

This is the clearest current evidence that the **human business customer can pay for an embedded regulatory capability without knowing anything about x402 or USDC**.

## 2. Platform call-threshold sensitivity

Use a deliberately simple distribution sensitivity:

`monthly calls = active connected accounts × checks/account/month`

This does not assume every platform account is Canadian or regulatory-sensitive. It only measures how many connected eligible accounts are required once the workflow is real.

### At 3 checks per active connected account per month

| Platform anchor | Public account base | Accounts for 500 calls | % of full base | Accounts for 2K calls | % of full base | Accounts for 10K calls | % of full base |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jobber | 100,000+ businesses | 167 | 0.17% | 667 | 0.67% | 3,334 | 3.33% |
| Buildertrend | 20,000+ builders | 167 | 0.84% | 667 | 3.34% | 3,334 | 16.67% |
| ServiceTitan | 10,800 active customers | 167 | 1.55% | 667 | 6.18% | 3,334 | 30.87% |

### Important eligibility penalty

The percentages above are **not realistic adoption forecasts** because ProjectPermit currently covers Canada and only some project/job types are Layer-C sensitive.

If only 10% of a platform's full account base were both geographically addressable and genuinely relevant, the same 500-call threshold at 3 checks/account/month would require roughly:

- Jobber: 167 / 10,000 eligible = **1.67%** of the eligible slice;
- Buildertrend: 167 / 2,000 = **8.35%**;
- ServiceTitan: 167 / 1,080 = **15.46%**.

This is why Jobber-like broad channels can create large volume with tiny penetration, while smaller high-fit platforms may need materially higher eligible-account conversion.

The 10% eligible slice is only a sensitivity assumption, not a measured fact.

## 3. ServiceM8 per-account denominator is especially useful

Because ServiceM8 publishes monthly job allowances, its user-level economics can be stress-tested without pretending all jobs need regulation checks.

Illustrative sensitivity only:

| ServiceM8 plan | Jobs/month | If 5% need a regulatory check | If 10% need a regulatory check |
|---|---:|---:|---:|
| Starter | 50 | 2.5 | 5 |
| Growing | 150 | 7.5 | 15 |
| Premium | 500 | 25 | 50 |
| Premium Plus | 1500+ | 75+ | 150+ |

A single trade business therefore does not need hundreds of regulatory events per month to be commercially useful. If an add-on saves repeated research or prevents quote/scope mistakes, a fixed monthly fee can monetize the capability even when only a handful of jobs trigger it.

## 4. Payer model — who actually pays?

### Model A — contractor/business add-on subscription

Natural payer: the contractor/service business using Jobber/ServiceM8/etc.

Best evidence: ServiceM8 explicitly allows a developer to set a monthly fee and lets ServiceM8 collect it on the customer's bill.

Advantages:

- no crypto knowledge required;
- no enterprise platform procurement required for every customer;
- revenue does not collapse when per-account call count is modest;
- user understands the purchase as software/compliance/estimating value, not `API calls`.

### Model B — software-platform licence / minimum commitment

Natural payer: Jobber/Buildertrend/ServiceTitan/Buildxact or another software vendor embedding the capability for its customer base.

Likely commercial shape if Layer C is validated:

- fixed annual/monthly licence;
- implementation fee or integration work;
- jurisdiction/content scope tier;
- bounded usage or high/unlimited checks;
- potentially licensed-content pass-through economics.

This aligns better with the existing ICC Code Connect / licensed maintained-content precedent than high marginal pricing for every deterministic lookup.

### Model C — x402 per-call

Natural payer: an autonomous agent, developer, integration service or long-tail buyer with a funded wallet.

Best role:

- no-account experimentation;
- agent-native discovery and settlement;
- low-friction long-tail calls;
- cross-service machine payment;
- metered fallback for users who do not want a subscription.

Do **not** require the end contractor to understand or adopt x402 for the main B2B business to work.

## 5. Build-vs-buy / channel ranking

### Tier 1A — ServiceM8 add-on route

Why it is attractive for validation:

- exact quote/job workflow;
- public API and public third-party add-on model;
- built-in monthly billing and payout;
- distribution to thousands of businesses;
- existing ProjectPermit ServiceM8 adapter already models job -> proposal flow;
- no need to persuade ServiceM8 to buy an enterprise licence before testing end-user demand.

Risks:

- platform is globally distributed and Canada share is unknown;
- many ServiceM8 jobs are small service/maintenance work with no permit/code consequence;
- no buyer evidence yet that Canadian trade users want ProjectPermit obligations.

Decision: **best product-distribution falsification route after E2, not authorization to build now.**

### Tier 1B — Jobber marketplace route

Why it is attractive:

- 100K+ business denominator;
- Canadian company with strong construction/trade categories;
- quote/job workflow is central;
- public OAuth/GraphQL platform;
- marketplace supports broad account distribution;
- existing ProjectPermit Jobber adapter already models Request/Quote/Job -> proposal flow.

Risks:

- only a subset of Jobber industries/jobs are regulatory-sensitive;
- app review/approval is needed for scale;
- a successful high-volume capability could eventually be internalized by a large platform.

Decision: **highest scale candidate among currently developer-accessible platforms; validate buyer consequence before marketplace product work.**

### Tier 2A — Buildertrend partnership

Why attractive:

- 20K+ builders with much higher preconstruction/regulatory relevance than general field service;
- estimate -> job costing -> project lifecycle is core;
- marketplace/integration precedent exists.

Risk:

- no self-serve general developer channel was confirmed;
- likely requires partnership/business-development path;
- enterprise vendor can build narrow rules internally if the maintained external layer is not sufficiently differentiated.

Decision: **high strategic buyer fit, higher distribution friction.**

### Tier 2B — ServiceTitan marketplace / platform deal

Why attractive:

- 10.8K active customers;
- enormous workflow/GTV scale;
- supported third-party API/app route;
- HVAC/plumbing/electrical/trades have real regulatory touchpoints.

Risks:

- sophisticated and well-funded platform/customer base increases internal-build threat;
- App Marketplace certification and integration are more enterprise-like;
- much of ServiceTitan's workflow is service/repair, not permit-sensitive construction.

Decision: **large potential volume, but external maintained-content differentiation must be strong.**

### Tier 2C — Buildxact vendor route

Why attractive:

- quote-centric residential builder/remodeler workflow;
- nearly 1M historical quotes and very high average quoted project value;
- regulatory consequences can directly affect estimate economics.

Risk:

- no general public third-party developer route confirmed in this pass;
- likely vendor partnership rather than self-serve app distribution.

Decision: **strong buyer archetype; use for validation/partnership, not immediate distribution engineering.**

## 6. Commercial falsification thresholds

The next buyer evidence should answer **both** denominator and externalization.

A lead is stronger if it can establish:

1. at least ~10 real candidate workflows/month for one contractor account **or** a platform cohort large enough to produce 500+ calls/month;
2. the result changes quote scope/price, professional involvement, schedule, document handoff or inspection sequencing;
3. repeated regulatory maintenance is something the buyer prefers not to own internally;
4. the buyer can name a natural payment mechanism: add-on subscription, platform licence/minimum, or per-call;
5. the expected monthly spend remains below the buyer's rational internal-build threshold.

A huge platform that says `we would just build this` is weaker evidence than a smaller channel that says `we will pay monthly because maintaining current jurisdiction rules is non-core`.

## 7. Decision consequence

This research changes the distribution/payment thesis but **not** the build gate.

### Stronger conclusion

ProjectPermit does not depend on a future world where autonomous agents independently decide to purchase regulation checks with crypto.

The commercial stack can be:

`contractor workflow -> embedded add-on/integration -> ProjectPermit capability -> optional x402 settlement internally`

or:

`platform vendor -> fixed/licensed maintained capability -> embedded in product`

The end user may never see x402.

### What remains unproven

- how many Canadian contractor accounts in these platforms are actually Layer-C eligible;
- real monthly checks/account;
- material workflow consequence;
- willingness to pay for maintained obligations;
- whether the platform/user prefers buy vs build;
- E4 real external use;
- E5 payment.

## Current decision

**Do not build a marketplace app yet.**

Use this ranking to make the next evidence gate sharper:

> buyer denominator + consequence -> choose ServiceM8/Jobber-style end-user distribution if users will pay directly, or platform licence if vendor-level buyer emerges -> smallest representative Layer C -> external usage -> payment.

x402 remains strategically useful, but it is now explicitly a **payment rail / agent-native distribution option**, not the assumption that every economic buyer must be an autonomous agent.
