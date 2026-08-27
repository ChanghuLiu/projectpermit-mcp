# Jobber Developer Bootstrap — Read-Only ProjectPermit Validation

Verified against Jobber's public developer documentation on 2026-08-27.

## Decision

A reply from Jobber API support is **not** required to begin internal sandbox development.

Jobber's official Getting Started path allows a developer to:

1. create a 90-day Jobber developer testing account;
2. create a Developer Center account;
3. create a Draft app;
4. use GraphiQL / a testing token before implementing the full OAuth callback flow;
5. call the GraphQL API at `https://api.getjobber.com/api/graphql`.

The latest active GraphQL version shown in Jobber's public changelog at verification time is `2025-04-16`.

## Important testing constraint

For an app intended for eventual Jobber App Marketplace publication, Jobber's testing guide says not to engage existing Jobber customers to test the app before first coordinating with a Jobber developer representative.

Therefore:

- the current supported-city Jobber operator list remains a research/design-partner candidate list;
- **do not connect those existing customer accounts to ProjectPermit yet**;
- internal Developer Center / test-account work can continue now;
- the already-sent API-support message remains useful for future customer-pilot / Marketplace coordination, but it is not an internal-development blocker.

Jobber also documents that a Draft custom integration can remain private and connect to up to 5 paying Jobber accounts; connecting to more than 5 paying accounts requires Jobber approval. This does not override the Marketplace-testing coordination rule above.

## Phase J0 — Create the sandbox manually

These steps require an interactive Jobber account login and therefore are intentionally not automated by this repository.

1. Create a Jobber **developer testing account** using the official developer testing signup flow.
2. Create/sign in to the **Jobber Developer Center**.
3. Create a new Draft app:
   - App name: `ProjectPermit`
   - Developer name: use the ProjectPermit developer identity
   - Description: evidence-linked municipal permit preflight for contractor quote/job workflows
4. Enable only the **minimum read scopes** needed to inspect Requests / Quotes / Jobs and their Properties / line items. Do not enable write scopes merely for convenience.
5. In GraphiQL, run Jobber's documented account query first:

```graphql
query GetAccount {
  account {
    id
    name
  }
}
```

6. Use the Developer Center testing token only as a local environment variable. Never commit it.

## Phase J1 — Run the repository probe

```bash
export JOBBER_ACCESS_TOKEN='...'
python scripts/jobber_readonly_probe.py
```

Expected shape:

```json
{
  "account": {"id": "...", "name": "..."},
  "api_version": "2025-04-16",
  "jobber_probe": "PASS",
  "read_only": true
}
```

The probe uses `src/projectpermit/jobber_client.py`, which locally rejects GraphQL mutations and subscriptions before any network request.

## Phase J2 — Validate exact live schema in GraphiQL

The public Jobber docs explicitly warn that object field names can change and that GraphiQL is the authoritative current schema explorer.

Before hard-coding a production query, confirm the exact live fields for:

- Request: `id`, `title`, `property`, `lineItems`
- Quote: `id`, `title`, `property`, `lineItems`
- Job: `id`, `title`, `property`, `lineItems`
- Property address subfields
- line-item name / description fields
- collection pagination (`first`, `after`, `pageInfo`)

Do not guess field names that are absent from the live schema.

## Phase J3 — Minimal read-only query strategy

Use shallow paginated collection queries. Jobber's API uses query-cost rate limits and recommends explicit pagination; omitting `first`/`last` can make the query cost assume up to 100 nodes.

ProjectPermit only needs enough Jobber data to form:

```text
source object id
+ property civic address
+ title / line-item scope text
```

Do **not** query client emails, phone numbers, billing data, invoice/payment data, assignees or other fields that are irrelevant to permit preflight.

Feed one decoded work object into:

```python
extract_jobber_work_object(...)
```

Then a caller/agent must convert `scope_text` to ProjectPermit's structured `project.family` + facts before:

```python
build_preflight_facts(...)
```

The ProjectPermit server does not add an LLM classifier here.

## Phase J4 — Historical internal benchmark

Once the test account contains representative synthetic quotes/jobs:

1. create at least 20 non-cherry-picked synthetic or de-identified test work objects across ProjectPermit's supported families;
2. fetch them read-only through Jobber GraphQL;
3. normalize their scope to ProjectPermit facts;
4. run ProjectPermit;
5. verify the adapter, address handling, evidence links and fail-safe behavior.

This is an integration test, **not market E3**.

True E3 still requires representative historical real-world cases from an independent operator/organization after the Jobber customer-testing route is authorized.

## Phase J5 — Write-back remains disabled

`build_jobber_writeback()` currently returns proposed custom-field values only. It does not call Jobber.

Do not enable Jobber mutations until:

- internal read-only sandbox is stable;
- the correct write scopes/custom-field API shape are verified in GraphiQL;
- customer testing is coordinated with Jobber where required;
- at least one real E3 benchmark justifies the integration;
- the write-back can be reversed/disabled safely.

## Official references

- Jobber Developer Center / API overview: `https://developer.getjobber.com/docs/`
- Getting Started: `https://developer.getjobber.com/docs/getting_started/`
- Custom integrations: `https://developer.getjobber.com/docs/custom_integrations/`
- Testing your app: `https://developer.getjobber.com/docs/building_your_app/testing_your_app/`
- API queries and mutations: `https://developer.getjobber.com/docs/using_jobbers_api/api_queries_and_mutations/`
- API versioning: `https://developer.getjobber.com/docs/using_jobbers_api/api_versioning/`
- API rate limits: `https://developer.getjobber.com/docs/using_jobbers_api/api_rate_limits/`
