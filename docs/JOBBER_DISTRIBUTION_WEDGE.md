# Jobber Distribution Wedge

Updated: 2026-08-27

## Why Jobber moved to the top tier

Jobber is a stronger distribution surface for ProjectPermit than many generic construction platforms because its core workflow already contains the three things a permit preflight needs:

1. a **property address**;
2. a **request / quote / job scope**;
3. a repeated decision point before work is scheduled or committed.

It also has a public GraphQL API, OAuth 2.0, webhooks, custom fields, a developer test-account path, and an App Marketplace review process.

Current official Jobber material says more than 400,000 home-service professionals use the product across 50+ industries. The Developer Center currently describes 300,000+ Home Service Pros/customers as the distribution audience for Marketplace apps. These numbers are user/pro distribution indicators, not a count of independent businesses, so they must not be used directly as TAM accounts.

## Relevant official API objects

The current Developer Center exposes:

- `Request`: title, line items, property, status, source;
- `Quote`: title, line items, property, custom fields, status;
- `Job`: title, line items, property, custom fields, linked request/quote;
- `Property`: structured address, client, requests, quotes, jobs;
- `Account`: country code and industry.

This is enough data in principle to construct a ProjectPermit input without asking the contractor to retype the address or project scope.

Jobber also supports app-configured custom fields on properties, quotes, jobs and other objects. A plausible integration could write back fields such as:

- `Permit preflight`: `REQUIRED / LIKELY_NOT_REQUIRED / CONFIRM`;
- `Permit confidence`;
- `Permit evidence URL` or compact evidence reference;
- `Last checked at`;
- `ProjectPermit rule version`.

## Candidate workflow

Preferred wedge:

`Jobber Request/Quote -> extract address + line items/title -> ProjectPermit -> write preflight result to Quote/Job custom fields -> contractor decides whether to escalate into a full permit workflow`

Potential trigger points:

1. **Request created** — earliest lead/intake check;
2. **Quote created or edited** — probably best first product surface because scope is more structured and money is about to be committed;
3. **Job created** — useful fallback when quote data is absent;
4. **Webhook event** — asynchronous re-check when a relevant work object changes.

The initial connector should avoid automatically blocking work. It should add deterministic routing metadata and explicit uncertainty.

## Why quote-time is probably the best wedge

Jobber's 2026 home-service report says quoting is one of the most time-consuming daily tasks reported by service businesses. Permit-sensitive trades such as plumbing, roofing, electrical, HVAC and general contracting are represented in Jobber's customer base. This does **not** prove permit research itself is a major Jobber pain point, but it identifies the workflow stage where a fast permit signal could matter.

A quote-time result is also commercially attractive because it can affect:

- price and scope assumptions;
- schedule promises;
- whether permit fees/lead time need to be included;
- whether a contractor should escalate to a permit service before customer approval.

## Integration feasibility already supported by public docs

Verified from current official Jobber docs on 2026-08-27:

- GraphQL API over HTTPS;
- OAuth 2.0 authorization;
- developer testing accounts with a 90-day test window;
- Marketplace app publication and review;
- custom integrations can connect to up to 5 paying accounts while still in Draft state; more than 5 requires approval;
- webhooks are available and Marketplace apps must handle app disconnect events;
- app-configured custom fields can be created through the API when scopes are approved;
- Request/Quote/Job objects expose property and structured scope-related fields.

This means a real 1–5-account design-partner pilot can be tested before a full Marketplace launch, assuming Jobber approves the required scopes and the participating accounts authorize the app.

## Call-volume model

Do not infer call volume directly from 400,000+ professionals. The account denominator and permit-sensitive work share are unknown.

Use integration-level scenarios instead:

| Connected contractor businesses | Candidate preflights/business/month | Monthly calls |
|---:|---:|---:|
| 50 | 20 | 1,000 |
| 100 | 20 | 2,000 |
| 250 | 20 | 5,000 |
| 500 | 20 | 10,000 |
| 125 | 80 | 10,000 |
| 1,000 | 20 | 20,000 |

These are scenarios, not forecasts. The `20/month` and `80/month` assumptions must be replaced with observed Jobber partner/account data before using them commercially.

The important implication is that ProjectPermit does **not** need a large percentage of Jobber's published user footprint to cross the first 10,000-calls/month checkpoint.

## Validation plan

### Stage 1 — API eligibility

Ask Jobber API support to confirm the intended Marketplace pattern and required scopes:

- read Request/Quote/Job + Property address/line items;
- configure/write ProjectPermit custom fields on Quote/Job;
- react to relevant webhook changes;
- call an external deterministic rules API from the integration backend.

A support answer is technical evidence only and should be checked against the live GraphQL schema/test account.

### Stage 2 — developer prototype

Create a Jobber developer test account and implement a thin adapter that:

1. accepts a Jobber object ID;
2. queries property address + title/line items;
3. maps scope into ProjectPermit's existing project-family input;
4. calls the existing `run_preflight` service;
5. returns a write-back payload without mutating Jobber by default.

No new permit rules are required for this step.

### Stage 3 — historical benchmark

Find 1–5 Canadian Jobber contractor accounts in permit-sensitive trades and obtain 20+ anonymized historical quotes/jobs. Compare ProjectPermit to their prior permit decisions.

This is E3 evidence under `VALIDATION_EVIDENCE_STANDARD.md`.

### Stage 4 — repeat-use pilot

With explicit account authorization, run the connector on live or recent work objects and measure observed external calls. The first meaningful signal is 20+ calls from one account/workflow, then 100+ aggregate external pilot calls.

### Stage 5 — Marketplace only after evidence

Do not invest in Marketplace submission work merely because the integration is technically possible. Submit when E3/E4 evidence shows repeated permit-sensitive volume and at least one credible path toward 500+ monthly calls.

## Key risk

The strongest unresolved question is not API feasibility. It is whether Jobber contractors already know permit applicability without material research at quote time. If historical samples show the answer is usually obvious from trade experience, Jobber may be a large distribution surface with a weak paid wedge.

That question must be answered with historical cases and observed behavior, not positive outreach replies.

## Current official sources

- Jobber Developer Center: https://developer.getjobber.com/docs/
- Jobber custom fields: https://developer.getjobber.com/docs/using_jobbers_api/custom_fields/
- Jobber webhooks: https://developer.getjobber.com/docs/using_jobbers_api/setting_up_webhooks/
- Jobber custom integrations: https://developer.getjobber.com/docs/custom_integrations/
- Jobber App Marketplace listing docs: https://developer.getjobber.com/docs/publishing_your_app/app_listing_details/
- Jobber 2026 Home Service Trends Report: https://www.getjobber.com/home-service-trends-report/
- Jobber feature/customer footprint page: https://www.getjobber.com/features/
- API support: api-support@getjobber.com
