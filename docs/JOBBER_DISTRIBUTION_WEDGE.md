# Jobber Distribution Wedge

Updated: 2026-08-27

## Why Jobber is the top current distribution experiment

Jobber's Request / Quote / Job workflow can contain the three inputs a permit preflight needs before work is committed:

1. property address;
2. title / line-item scope;
3. a repeated decision point around request, quote or job creation.

Current official Jobber docs expose a GraphQL API, OAuth 2.0, developer test accounts, webhooks, custom fields and an App Marketplace. The Developer Center says Jobber serves 300,000+ Home Service Pros; treat that as a distribution indicator, not an independent-business TAM denominator.

## Preferred product wedge

`Jobber Request/Quote -> property + title/line items -> structured ProjectPermit facts -> permit preflight -> proposed routing metadata`

Quote-time remains the preferred first surface because permit uncertainty can affect price, schedule, fee assumptions and escalation before the customer accepts the work.

ProjectPermit must not automatically block work. It should return deterministic evidence plus explicit uncertainty.

## Integration feasibility verified from official docs

Verified 2026-08-27:

- GraphQL endpoint: `https://api.getjobber.com/api/graphql`
- OAuth 2.0 Bearer authorization
- required `X-JOBBER-GRAPHQL-VERSION` header
- latest active public GraphQL version: `2025-04-16`
- 90-day developer testing account path
- Draft app / GraphiQL testing-token path
- custom integrations can remain Draft for up to 5 paying Jobber accounts; more than 5 requires approval
- Request / Quote / Job expose property + scope-related fields in the public object overview
- custom fields can be app-configured when the relevant scopes are approved
- webhooks are supported; Marketplace apps must handle disconnects
- query-cost rate limiting makes shallow paginated queries preferable

## Important customer-testing constraint

Jobber's current **Testing Your Application** guidance says that, for an app intended for Marketplace publication, developers should **not engage existing Jobber customers to test the application before first coordinating with a Jobber developer representative**.

Therefore:

- do **not** connect the prepared Canadian operator cohort to ProjectPermit yet;
- do **not** treat the `up to 5 paying accounts in Draft` rule as permission to skip Jobber's Marketplace-testing coordination guidance;
- internal Developer Center / test-account work continues now without waiting for support;
- the API-support email already sent remains useful for customer-pilot and Marketplace coordination, but is **not** a sandbox-development gate.

See `docs/JOBBER_DEVELOPER_BOOTSTRAP.md`.

## What is already implemented

- `src/projectpermit/jobber_adapter.py`
  - extracts only source id, property civic address and scope-relevant title/line-item text;
  - excludes client/contact, billing, payment and assignee data;
  - requires a caller/agent to supply the structured ProjectPermit `project.family` + facts;
  - produces a proposed custom-field write-back payload without mutation.

- `src/projectpermit/jobber_client.py`
  - minimal GraphQL transport;
  - current active API version default `2025-04-16`;
  - locally rejects `mutation` and `subscription` operations;
  - avoids echoing bearer tokens or raw HTTP error bodies.

- `scripts/jobber_readonly_probe.py`
  - accepts `JOBBER_ACCESS_TOKEN` via environment variable;
  - runs Jobber's documented `account { id name }` sanity query;
  - prints no token or raw response body.

- `data/historical_benchmark_template.csv`
  - E3 real historical benchmark structure.

## Validation sequence

### J0 — Internal Jobber sandbox

No support reply required.

1. create Jobber developer testing account;
2. create Developer Center Draft app;
3. enable the smallest required read scopes;
4. use GraphiQL to verify the current schema;
5. obtain a testing token;
6. run `scripts/jobber_readonly_probe.py`.

### J1 — Read-only work-object integration

After GraphiQL confirms the exact current fields, add shallow paginated queries for Request / Quote / Job that fetch only:

- object id;
- property civic address;
- title;
- line-item name/description fields needed for scope normalization.

Do not query customer contact, billing or payment data.

### J2 — Synthetic/de-identified integration benchmark

Use 20+ representative sandbox work objects to test:

`Jobber GraphQL -> extract_jobber_work_object -> caller normalization -> build_preflight_facts -> ProjectPermit -> proposed write-back`

This proves the integration pipeline but is **not market E3**.

### J3 — Real E3 historical benchmark

Only after the Jobber customer-testing route is coordinated appropriately, obtain representative anonymized historical cases from independent Canadian operators. Samples must be chronological/reproducible, not hand-picked permit-problem cases.

True E3 asks whether permit applicability actually required research/escalation and whether the result changed quote, schedule, fee or routing behavior.

### J4 — E4 repeat-use pilot

With proper authorization, measure real external successful preflight usage:

- first signal: 20+ calls from one workflow/account;
- next: 100+ aggregate pilot calls;
- meaningful small channel: 500+ candidate calls/month;
- strong integration: 2,000+ candidate calls/month.

### J5 — Marketplace investment only after evidence

Do not spend meaningful effort on listing/certification merely because the API works. Marketplace work should follow E3/E4 evidence and a credible repeated-volume path.

## Call-volume model

Do not infer call volume from Jobber's published user/pro count. Use observed integration volumes.

| Connected contractor businesses | Candidate preflights/business/month | Monthly calls |
|---:|---:|---:|
| 50 | 20 | 1,000 |
| 100 | 20 | 2,000 |
| 250 | 20 | 5,000 |
| 500 | 20 | 10,000 |
| 125 | 80 | 10,000 |

These are scenarios, not forecasts. `20/month` and `80/month` must be replaced with observed E2–E4 evidence.

## Main business risk

The biggest unresolved risk is not API feasibility. It is whether experienced home-service contractors already know permit applicability essentially for free at quote time.

If representative historical samples show that manual permit research/escalation is rare, Jobber may be a very large platform with a weak paid ProjectPermit wedge.

That question must be answered by E3/E4 evidence, not friendly replies.

## Official sources

- Developer Center: https://developer.getjobber.com/docs/
- Getting Started: https://developer.getjobber.com/docs/getting_started/
- Custom integrations: https://developer.getjobber.com/docs/custom_integrations/
- Testing your app: https://developer.getjobber.com/docs/building_your_app/testing_your_app/
- API queries / mutations: https://developer.getjobber.com/docs/using_jobbers_api/api_queries_and_mutations/
- API versioning: https://developer.getjobber.com/docs/using_jobbers_api/api_versioning/
- API rate limits: https://developer.getjobber.com/docs/using_jobbers_api/api_rate_limits/
- Custom fields: https://developer.getjobber.com/docs/using_jobbers_api/custom_fields/
- Webhooks: https://developer.getjobber.com/docs/using_jobbers_api/setting_up_webhooks/
- API support: `api-support@getjobber.com`
