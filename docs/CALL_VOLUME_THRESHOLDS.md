# ProjectPermit Monthly API Call Thresholds

Updated: 2026-08-27

The core business question is not how many municipalities can be coded. It is whether ProjectPermit can reach enough **repeated paid API calls** through a small number of distribution partners.

This document uses transparent scenario math. Unless explicitly sourced, values are assumptions for decision-making, not forecasts.

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

For a low-cost solo product, **10k monthly calls is the first commercially meaningful checkpoint**, while **100k monthly calls** would validate the category much more strongly. These are internal decision thresholds, not promises of profitability; Railway, support, compliance and rule-maintenance costs still need to be subtracted.

## What 10k calls/month actually requires

Equivalent distribution shapes:

| Distribution shape | Calls/customer/month | Customers/integrations needed | Total calls/month |
|---|---:|---:|---:|
| High-volume contractor accounts | 80 | 125 | 10,000 |
| Medium contractor accounts | 25 | 400 | 10,000 |
| Property portfolios | 20 | 500 | 10,000 |
| Strong SaaS integrations | 2,000 | 5 | 10,000 |
| Mid-sized integrations | 500 | 20 | 10,000 |
| One platform channel | 10,000 | 1 | 10,000 |

The `80 calls/customer/month` row is intentionally comparable to the public iPermit testimonial from a contractor sending **80+ permit jobs/month**. It does **not** assume 125 such contractors currently exist in ProjectPermit's reachable market; it shows the order of magnitude required.

Source for the 80+ example: https://marketplace.servicetitan.com/partner/ipermit

## What 100k calls/month requires

| Distribution shape | Calls/customer/month | Customers/integrations needed | Total calls/month |
|---|---:|---:|---:|
| High-volume contractors | 80 | 1,250 | 100,000 |
| Property portfolios | 50 | 2,000 | 100,000 |
| Strong SaaS integrations | 5,000 | 20 | 100,000 |
| Large platform integration | 100,000 | 1 | 100,000 |

This is why the preferred strategy is **platform/integration distribution**, not acquiring hundreds or thousands of contractors one by one.

## ServiceTitan scale scenario

Public ServiceTitan partner material says the platform serves **12,000+ businesses** and completes **40M+ jobs annually**.

Source: https://help.servicetitan.com/docs/servicetitan-overview-for-app-marketplace-partners

The following scenarios answer only: _if a share of jobs creates a permit-decision event, how large could the call surface be?_ They are not forecasts.

| Assumed permit-decision share | Candidate calls/year | Candidate calls/month |
|---:|---:|---:|
| 2% | 800,000 | ~66,667 |
| 5% | 2,000,000 | ~166,667 |
| 10% | 4,000,000 | ~333,333 |
| 20% | 8,000,000 | ~666,667 |

At the conservative **5% decision-share** scenario, ProjectPermit would need only about **6% of that candidate call surface** to reach 10k calls/month. But this remains theoretical until an integration exists, and the current seven Canadian jurisdictions cannot serve most U.S. ServiceTitan volume.

### Geographic reality

A major hidden constraint is coverage overlap:

- ServiceTitan's largest volume surface is U.S.-heavy.
- ProjectPermit is currently Canada-only.
- Therefore ServiceTitan is a **distribution proof target**, but it cannot produce the theoretical platform call volume until U.S. jurisdiction coverage is justified by a partner.

Do not add U.S. cities speculatively. If a ServiceTitan design partner says, for example, that Los Angeles, Phoenix and Dallas represent 70% of its permit-sensitive jobs, those requested jurisdictions become much higher-priority than generic expansion.

## AppFolio scale scenario

AppFolio reported **22,096 property-management customers** and **9.4M units under management** at 2025 year-end.

Source: https://www.sec.gov/Archives/edgar/data/1433195/000143319526000011/appf-20251231.htm

AppFolio does not publish a universal maintenance-work-order rate, so use a scenario range instead of inventing one.

### Scenario A — low activity

Assume:

- 1 maintenance/capex decision per unit/year;
- 2% are permit-sensitive.

That gives:

- 9.4M × 1 × 2% = **188,000 candidate permit decisions/year**;
- about **15,667/month** across the entire AppFolio footprint.

A 10% capture of that hypothetical surface would be only ~1,567 calls/month.

### Scenario B — higher activity

Assume:

- 3 maintenance/capex decisions per unit/year;
- 5% are permit-sensitive.

That gives:

- 9.4M × 3 × 5% = **1.41M candidate decisions/year**;
- about **117,500/month**.

A 10% capture would be ~11,750 calls/month.

The two scenarios differ by 7.5×. This uncertainty is exactly why the next step is to ask Property Meld, Lula, AppWork, HappyCo and property managers for actual work-order distributions instead of treating unit count as call volume.

## Procore / construction platform scenario

Procore reported **17,850 customers** at 2025 year-end. Marketplace examples show integrations can achieve thousands of installs: Outbuild currently shows **2,777 installs**, and SyncEzy's SharePoint integration shows more than a thousand installs on the public Marketplace.

Sources:

- Procore 2025 Form 10-K: https://www.sec.gov/Archives/edgar/data/1611052/000162828026011055/pcor-20251231.htm
- Outbuild: https://marketplace.procore.com/apps/outbuild
- Procore Marketplace: https://marketplace.procore.com/

Project count per customer and permit-decision frequency are not public enough for a reliable denominator. Use partner-level thresholds instead:

| Active integration accounts | Calls/account/month | Monthly calls |
|---:|---:|---:|
| 100 | 10 | 1,000 |
| 250 | 20 | 5,000 |
| 500 | 20 | 10,000 |
| 1,000 | 25 | 25,000 |
| 2,000 | 25 | 50,000 |

This makes an integration partner with hundreds or thousands of active accounts materially more valuable than direct one-off contractor sales.

## Partner-by-partner call-volume questions

### iPermit / PermitFlow / Pulley

Ask:

- How many new permit workflows enter the system each month?
- How many upstream jobs are rejected or determined not to require a permit?
- Is permit applicability already known before the platform is invoked?

If full permit vendors only see cases already known to require a permit, ProjectPermit adds little value there. If they receive a broad job stream and perform triage first, the upstream API wedge becomes much stronger.

### Property Meld / Lula / AppWork / HappyCo

Ask:

- work orders/month;
- percentage involving structural/plumbing/window/door/deck/addition/renovation scopes;
- percentage that causes permit research;
- how many municipalities per portfolio;
- whether the decision is made before vendor dispatch, estimate approval or capital authorization.

A useful target is one design partner with **2,000+ candidate preflights/month**. Five such partners would meet the 10k gate.

### ServiceTitan integration consultants

Ask them to identify the top three contractor workflows by monthly job count where permit applicability is still manually researched. A consultant serving multiple contractors may be a better first distribution partner than a single contractor.

### Procore / Autodesk integrators

Ask for the number of projects/clients where permit requirements are maintained in spreadsheets, custom fields or email. The goal is to attach one preflight call to project creation or scope change, not to replace project management.

## Pricing × call-density decision matrix

| Calls/month | $0.10/call | $0.25/call | $0.50/call | Interpretation |
|---:|---:|---:|---:|---|
| <1k | <$100 | <$250 | <$500 | Too small unless strategic design partner |
| 1k-10k | $100-$1k | $250-$2.5k | $500-$5k | Validation stage |
| 10k-100k | $1k-$10k | $2.5k-$25k | $5k-$50k | Attractive solo-business scale if costs stay low |
| 100k+ | $10k+ | $25k+ | $50k+ | Strong product-market/distribution signal |

## Operational cost constraint

The preferred capability remains one where marginal cost is close to zero:

- deterministic local rule evaluation;
- first-party municipal/open-data GIS;
- no server-side LLM requirement;
- no paid property-data API by default;
- no human permit runner/reviewer required for each call.

That means a $0.20-$0.50 price can support healthy gross margins **if** municipal source maintenance remains manageable. The real scaling risk is not compute; it is keeping jurisdiction rules current and defensible.

Track the maintenance metric explicitly:

> engineering/source-review hours per supported municipality per month, and per 1,000 external calls.

A city generating 20 calls/month but requiring several hours of recurring maintenance should be removed or deprioritized. A city generating 20k calls/month can justify much deeper maintenance.

## Go / no-go gates

### Continue ProjectPermit aggressively when any two are true

- 10k+ external calls/month or a signed/credible path to it;
- 3+ repeated integrations;
- one partner generates 2k+ calls/month;
- one buyer accepts $0.20-$0.50 address-aware pricing;
- requested unsupported jurisdictions collectively imply 10k+ monthly calls;
- maintenance cost remains low relative to call revenue.

### Pause expansion / reconsider the capability when

- after 20 qualified conversations nobody can identify a repeated preflight decision;
- external testers use it only as a one-off lookup;
- partners require human permit research on nearly every call;
- buyers only want full submission/expediting;
- the address-aware result is not trusted enough to automate routing;
- required data becomes dominated by expensive licensed sources.

## Bottom line

ProjectPermit does **not** need millions of customers. It needs a small number of integrations that each generate hundreds or thousands of repeated calls.

The near-term target is therefore not `city #8`. It is:

> **5 integrations × ~2,000 calls/month = 10,000 monthly calls**

or one platform workflow capable of the same volume.

That is the minimum distribution shape worth proving before substantial geographic expansion.
