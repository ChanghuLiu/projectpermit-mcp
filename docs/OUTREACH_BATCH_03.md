# ProjectPermit Outreach Batch 03

Updated: 2026-08-27

Status: **prepared, not sent/submitted**

## Goal

Batch C shifts toward platforms whose workflow already contains structured job/request/work-order data and whose scale can plausibly support repeated API calls. A reply is not validation; every message asks for bounded historical workflow evidence or anonymized cases under `docs/VALIDATION_EVIDENCE_STANDARD.md`.

## 1. Jobber — home-service operating system / strongest current distribution candidate

Official evidence:
- Jobber's current Developer Center says 300,000+ Home Service Pros have served 12M+ households in 47+ countries.
- Jobber provides a GraphQL API, App Marketplace, and private custom integrations.
- Jobber requests are the starting point for jobs and can collect job details, photos, measurements and property information before quote/job creation.

Why this matters:
A permit-preflight call could sit at `request -> quote/job` when scope + property address are available. The scale is attractive, and Jobber is especially relevant because ProjectPermit already covers major Canadian municipalities.

Official route:
- Developer Center / API support
- Partner/application route
- Do not apply to the public marketplace until workflow evidence exists.

Evidence-first message:

Subject: `Permit applicability at Jobber request / quote time`

Hi Jobber team — I’m validating ProjectPermit, a deterministic municipal permit-preflight API for home-service workflows.

Jobber already captures property address plus structured request/job context before quote and job creation, so I’m testing one narrow question: in real contractor workflows, how often does someone stop at this stage to determine whether the proposed work needs a municipal permit?

I’m not looking for a general “sounds useful” opinion. The useful evidence would be a bounded recent denominator (for example, jobs/requests in the last 30 days and how many required permit-applicability research) or 5–20 anonymized historical examples that can be benchmarked against our current engine.

ProjectPermit currently covers seven Canadian jurisdictions and returns evidence-linked `required / likely not required / confirm` results. It does not submit permits.

Best,
ProjectPermit
Independent developer

## 2. Buildxact — residential estimating / quoting / project management

Official evidence:
- Buildxact Canada positions the product from takeoff through estimating, quoting, scheduling and job tracking.
- Buildxact reports 988,783 quotes produced and publishes a Canada-specific product site.
- It has a formal partner program and works with Canadian industry groups including the Canadian Home Builders' Association and Ontario Home Builders' Association.

Why this matters:
Permit applicability can affect estimate assumptions, schedule dependencies and whether a renovation scope can proceed as quoted. This tests ProjectPermit earlier than project execution, close to scope/estimate creation.

Official route:
- Canada Contact Us / Book a Demo / partner application.

Evidence-first message:

Subject: `Permit preflight before a residential estimate becomes a job`

Hi Buildxact team — I’m validating ProjectPermit, a deterministic municipal permit-preflight API for residential building/remodeling workflows.

Buildxact already has scope, estimate and project context before work is scheduled. I want to measure whether builders repeatedly need to research permit applicability at estimate/quote time, and whether that decision changes the quote, schedule or next workflow step.

Rather than asking whether the idea sounds useful, I’m looking for a recent denominator/timeframe or 5–20 anonymized historical renovation/build scopes that can be compared with the current manual result.

ProjectPermit currently covers seven Canadian jurisdictions and returns official-source-backed `required / likely not required / confirm` results. It is not a permit-submission service.

Best,
ProjectPermit
Independent developer

## 3. MaintainX — high-volume maintenance work orders

Official evidence:
- MaintainX work orders contain asset/location, responsibility, timing and task detail.
- MaintainX supports standardized and repeating work orders, making it a high-frequency workflow surface.

Why this matters:
This is a deliberate test of whether permit-sensitive maintenance/CapEx work appears often enough inside a general maintenance platform. If the share is tiny, this channel should be downgraded despite large work-order volume.

Official route:
- Contact Sales / official product contact flow.

Evidence-first message:

Subject: `How often do maintenance work orders need permit research?`

Hi MaintainX team — I’m testing a deterministic permit-preflight API for maintenance work-order systems.

Your work orders already carry location and task context, so the measurable question is whether a meaningful subset of real work orders require someone to determine municipal permit applicability before approval or execution.

I’m specifically trying to avoid extrapolating from total work-order volume. If this occurs, the useful evidence is a recent work-order denominator plus the permit-research subset, or 5–20 anonymized historical examples that can be benchmarked.

ProjectPermit returns an evidence-linked municipal requirement result and explicit uncertainty; it does not submit permits.

Best,
ProjectPermit
Independent developer

## 4. Fiix — CMMS / asset and maintenance workflow

Why this matters:
Fiix is a CMMS/work-order platform with Canadian roots and a workflow adjacent to MaintainX. The purpose is not to assume the same demand; it is to test whether permit applicability occurs in facilities/asset maintenance often enough to justify a reusable preflight connector.

Official route:
- Fiix / Rockwell Automation official sales-contact flow.

Evidence-first message:

Subject: `Permit applicability inside CMMS work-order approval`

Hi Fiix team — I’m validating ProjectPermit, a deterministic municipal permit-preflight API that can sit inside an existing maintenance workflow.

The specific question is whether facilities/maintenance teams repeatedly need to determine permit applicability for structural, plumbing, window/door, deck, renovation or similar work before approving or scheduling a work order.

A general opinion is not enough for our decision. If the workflow exists, I’m looking for a bounded recent count or 5–20 anonymized historical cases so we can compare ProjectPermit with the existing process and measure disagreement.

Best,
ProjectPermit
Independent developer

## Ranking

1. **Jobber — highest priority.** Large home-service surface, structured address + work context, API/App Marketplace, strong Canada relevance.
2. **Buildxact — high priority.** Residential renovation/build scope is close to ProjectPermit's current project families and permit decision point.
3. **MaintainX — medium/high experimental priority.** Very repeatable work orders, but unknown permit-sensitive share must be measured rather than assumed.
4. **Fiix — medium experimental priority.** Similar CMMS hypothesis; useful as a cross-check against MaintainX rather than additive TAM.

## Decision rule

Do not count platform customer totals or total work orders as ProjectPermit TAM. For each platform require:

`recent total workflow events -> permit-applicability decision share -> candidate preflight calls/month -> observed pilot/repeat calls -> economic behavior`

No municipality expansion, paid marketplace application, or pricing decision should be triggered by E0/E1 responses.

## Current public evidence

- Jobber Developer Center: https://developer.getjobber.com/docs/
- Jobber requests workflow: https://help.getjobber.com/en/articles/request-basics/
- Jobber partners: https://www.getjobber.com/partners/
- Buildxact Canada: https://www.buildxact.com/ca/
- Buildxact partners: https://www.buildxact.com/ca/our-customers/partners/
- MaintainX work orders: https://help.getmaintainx.com/about-work-orders
