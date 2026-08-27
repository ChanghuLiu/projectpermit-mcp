# Embedded Field-Service Platform Distribution Scorecard

Updated: 2026-08-27

## Why two rankings are required

ProjectPermit must not confuse **easy API access** with **large commercial distribution**.

For an independent developer with low cash cost tolerance, the best platform to prototype next may not be the platform with the largest eventual API-call surface.

Therefore maintain two separate rankings:

1. **Commercial distribution priority** — credible platform scale, workflow frequency, permit-sensitive trade fit and geography.
2. **Immediate technical validation priority** — cost, sandbox/API access, account friction and ability to prove a read-only integration now.

Neither ranking is market validation. E3/E4 still controls major product decisions.

## Current official scale signals

| Platform | Current official scale signal reviewed 2026-08-27 | Call-density signal | Canada relevance | Access friction |
|---|---|---|---|---|
| Jobber | 400,000+ service pros across 50+ industries; current Jobber material also reports 100K+ businesses | strong repeated Request/Quote/Job workflow; official material reports 92M+ jobs completed by Jobber-powered businesses, but do not assume a time period unless the source states one | **High** — Canadian company/footprint and explicit Canadian operators | Medium: developer test path exists, but existing-customer Marketplace testing should be coordinated with Jobber first |
| ServiceTitan | **12,000+ businesses** | **40M+ jobs completed annually** | Low for current Canada-only rules; strongest footprint is U.S. trades | Medium-high: third-party developer access request; standard-data integration environment after access |
| Housecall Pro | **200,000+ pros**; About page reports **45,000+ businesses** | official site reports **100M+ pro jobs completed** (cumulative context not converted to annual flow) | primarily U.S.; Canadian path weaker than Jobber | Medium-high for low-cost prototype: customer API access tied to higher-tier plan/partner path |
| Workiz | **120,000+ home service pros in US and Canada** | core lead/job/estimate/dispatch workflow; exact annual job count not established in current review | **Medium-high stated geography** because official site explicitly says US and Canada | Medium: public REST docs/token path, but account/add-on access still needs validation |
| ServiceM8 | no defensible current business/pro account denominator found | strong Job/Quote/Work Order object fit; global site reports large job-value totals, not an account denominator | **Confirmed presence, unknown scale** — Canada site, Canadian partner and community users exist | **Low**: private own-account API key documented; Free plan exists; read-only API-key type documented |

Do not add these platform denominators together. They overlap heavily in target trades and represent different units (pros, businesses, jobs).

## Commercial distribution ranking

### #1 Jobber

Why:

- strongest combination of Canadian relevance + home-service focus + Quote/Job workflow;
- address + structured scope at the right decision point;
- large current platform signal;
- ProjectPermit read-only adapter already exists.

Main uncertainty remains **paid pain**, not technical fit: contractors may already know permit applicability from experience.

### #2 ServiceTitan — conditional on U.S. geography evidence

ServiceTitan's 40M+ annual jobs is the strongest current **annual workflow-volume signal** among platforms reviewed.

Simple arithmetic for context only:

- 40M jobs/year ≈ 3.33M jobs/month across the platform.
- If only 1% of jobs were relevant permit-decision candidates, that would be ≈33k candidate objects/month platform-wide.
- At 5%, ≈167k/month.

These are **sensitivity scenarios, not estimates**. The actual permit-sensitive share is unknown and must be measured.

Current problem: ProjectPermit is Canada-only while ServiceTitan is U.S.-heavy. Do not add U.S. municipalities speculatively. ServiceTitan becomes #2 executable commercial priority only when a partner/workflow attaches credible volume to specific cities.

### #3 Workiz / Housecall Pro — needs access + geography validation

**Workiz** has an attractive explicit `US and Canada` 120k+ pro signal and public API docs. It may move above ServiceTitan for near-term Canadian distribution if we verify:

- account/API access cost;
- exact Job/Estimate/address fields;
- Canadian operator density inside supported cities.

**Housecall Pro** has the stronger business denominator (45k+ businesses / 200k+ pros), but current API/customer access is less attractive for a near-zero-cash prototype and the footprint is strongly U.S.-oriented.

### ServiceM8 — commercial rank intentionally unproven

ServiceM8 should **not** be assigned a high commercial rank yet because no reliable Canadian business/account denominator was found.

Its value right now is speed of falsification: we can cheaply learn whether the generic `field-service Job -> permit preflight` integration pattern works on a second independent product model.

If later Canadian operator evidence shows meaningful density, ServiceM8 can be upgraded.

## Immediate technical validation ranking

### #1 Jobber

Already implemented locally:

- adapter;
- no-mutation GraphQL client;
- 20-case integration benchmark;
- account probe.

Manual remaining gate: Developer Center test account/Draft app/testing token/live schema.

### #2 ServiceM8

Already implemented locally:

- read-only adapter;
- GET-only API-key client;
- 12-case all-family synthetic benchmark;
- safe own-account connectivity probe;
- bootstrap instructions.

Manual remaining gate: verify a Free account exposes `Settings -> API Keys`, create a **Read Only** key, then run the live probe.

### #3 Workiz

Next research target if both Jobber and ServiceM8 live-account paths become blocked or weak.

Before coding, verify:

- current API-token availability by plan;
- Job/Estimate property address + scope fields;
- read-only credential possibility;
- Canada-supported-city operator evidence.

### #4 ServiceTitan

High strategic value but not the fastest independent prototype because developer access is requested/approved before use of the standard-data integration environment.

### #5 Housecall Pro

High commercial scale but currently a weaker low-cash own-account validation path than ServiceM8.

## Monthly API-call reasoning

The target remains a **repeated preflight workflow**, not one API call per final permit.

For any platform, measure:

`candidate permit-decision work objects/month`

not:

`all platform jobs/month`

and not:

`permits issued/month`.

A credible partner should eventually let us estimate:

`accounts × relevant jobs/account/month × preflight trigger share × repeat usage rate`.

Examples of equivalent 10k monthly call shapes:

- 500 businesses × 20 candidate preflights/month;
- 125 businesses × 80/month;
- 20 integrations × 500/month;
- 5 integrations × 2,000/month;
- one large platform/workflow × 10,000/month.

## Decision rule

Do not spend months integrating every field-service product.

A second platform prototype is useful only to test whether the ProjectPermit contract generalizes beyond Jobber. After Jobber + ServiceM8, additional platform adapters require one of:

- credible E2+ workflow evidence;
- specific E3 historical data access;
- a partner request;
- a clear 500+/month candidate call path;
- unusually low-cost access that tests a materially different workflow.

Otherwise stop adapter proliferation and return effort to external E3/E4 validation.

## Official sources reviewed 2026-08-27

### Jobber
- https://www.getjobber.com/llm-info/
- https://www.getjobber.com/features/

### ServiceTitan
- https://help.servicetitan.com/docs/servicetitan-overview-for-app-marketplace-partners

### Housecall Pro
- https://www.housecallpro.com/about/
- https://www.housecallpro.com/
- https://www.housecallpro.com/llm-info/

### Workiz
- https://www.workiz.com/

### ServiceM8
- https://developer.servicem8.com/docs/authentication
- https://www.servicem8.com/pricing
- https://www.servicem8.com/
