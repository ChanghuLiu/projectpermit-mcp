# ProjectPermit × Jobber Integration Feasibility

Updated: 2026-08-27

Status: **technical feasibility documented; no marketplace application submitted**

## Why Jobber is the strongest current platform hypothesis

Jobber's current Developer Center states that 300,000+ Home Service Pros have served 12M+ households across 47+ countries. The platform exposes a GraphQL API, real-time webhooks, a public App Marketplace path, and custom integrations for a limited number of paying accounts before broader approval is required.

This is relevant to ProjectPermit because the Jobber workflow already has the two inputs our preflight needs:

1. **property/location context**;
2. **structured work/request/quote/job context**.

The commercial question remains unproven: what share of Jobber requests/jobs actually need a permit-applicability decision? Total Jobber scale must not be converted into ProjectPermit TAM without measuring that share.

## Candidate workflow

Preferred insertion point:

`new Request -> fetch Request + Property -> normalize scope -> ProjectPermit preflight -> attach routing signal -> quote/job decision`

Alternative later insertion point:

`Quote created/updated -> ProjectPermit preflight -> permit flag/evidence before quote acceptance or job creation`

The request stage is preferable because it can avoid downstream rework earlier.

## Relevant Jobber API objects

### Account

The API exposes `countryCode` including `CA`/`US`. This can be used as an early eligibility gate before any municipal lookup.

### Request

Current Jobber API documentation shows Request fields including:
- `id`
- `createdAt`
- `lineItems`
- `notes`
- `property`
- `quotes`
- `jobs`
- `requestStatus`
- `source`
- `title`

These fields are enough to form a first-pass scope summary in many workflows without requesting unnecessary personal data.

### Property

Request, Quote and Assessment objects are linked to a Property. ProjectPermit should use only the minimum address/location fields required for municipal resolution and should not persist customer identity fields.

### Quote

Quote includes:
- `lineItems`
- `notes`
- `property`
- `request`
- `title`
- quote state/timestamps

This is a viable fallback if request data is too sparse.

### Webhooks

Jobber supports real-time webhooks configured per app. A production integration could call ProjectPermit only when a relevant request/quote event occurs rather than polling.

## Privacy/minimum-data design

ProjectPermit should not ingest or store Jobber customer names, emails, phone numbers or billing information.

Minimum desired payload after normalization:

```json
{
  "jurisdiction": "ottawa_on",
  "project_family": "window_door",
  "scope": "replace exterior window, same opening",
  "civic_address": "<used transiently only when address-aware resolution is needed>",
  "context": {
    "client_tag": "jobber:<non-PII-account-or-integration-tag>"
  }
}
```

Persist only anonymized telemetry already supported by ProjectPermit. Do not log raw Jobber request text or civic address.

## Technical feasibility result

**PASS at architecture level.** Jobber exposes the required workflow objects, property relationships, GraphQL API and webhook mechanism for a ProjectPermit integration.

This does **not** prove demand.

## Evidence required before building a marketplace app

Do not spend time on full Jobber App Marketplace review until at least one of these is true:

- one Jobber service provider supplies 20+ anonymized historical requests for E3 benchmarking;
- one approved custom integration/account produces 20+ repeat real preflight calls (E4);
- a Jobber-facing integration partner identifies a bounded workflow with >=500 candidate calls/month and provides representative cases.

Preferred commercial trigger for broader Jobber-specific engineering: a credible path to >=2,000 candidate preflights/month from specific accounts/workflows.

## Pilot design

A Jobber pilot should begin without marketplace publication:

1. export or manually provide 20 anonymized historical requests;
2. retain property city/municipality and only the address detail required for address-aware cases;
3. compare historical permit decision vs ProjectPermit result;
4. mark material disagreements;
5. estimate the recent denominator: total requests/jobs and permit-research subset;
6. only then decide whether to build OAuth/webhook integration.

## Key risk

The largest risk is not API access. It is that permit-sensitive work may represent too small a share of Jobber's total service volume. Landscaping, cleaning, lawn care and many routine service categories could generate high Jobber volume but near-zero ProjectPermit demand.

Therefore measure **permit-sensitive share by trade and workflow**, not total Jobber customers/jobs.

## Official sources

- Jobber Developer Center: https://developer.getjobber.com/docs/
- Jobber Getting Started: https://developer.getjobber.com/docs/getting_started/
- Jobber Custom Integrations: https://developer.getjobber.com/docs/custom_integrations/
- Jobber request workflow: https://help.getjobber.com/en/articles/request-basics/
