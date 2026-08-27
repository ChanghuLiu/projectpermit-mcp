# E2 bounded platform-volume request

Updated: 2026-08-27

Purpose: obtain a decision-useful workflow denominator from a platform, consultant, permit-operations vendor or multi-account operator **before** asking for integration work or a large historical data export.

This request is intentionally short. Positive opinions, demos, API documentation and general market-size claims do not satisfy it.

## Fast threshold question

For one recent complete month:

> In the stated covered geography, did your workflow contain at least **500 candidate Requests / Estimates / Quotes / Jobs** that could plausibly require a municipal permit-applicability decision before work was scheduled or accepted?

A simple `yes` / `no` is usable **only if the response also states**:

- the month or bounded date range;
- the geography;
- the workflow object being counted (Request, Estimate, Quote, Job, work order, permit intake, etc.);
- whether the count is aggregate across multiple customer accounts or one account.

Do not ask for customer names, exact addresses, phone/email, payment data or account identifiers.

## Preferred numeric response

If the partner can provide aggregate counts, request:

```text
month/date range:
geography:
workflow object:
total candidate workflow events:
distinct customer accounts represented (optional but preferred):
HVAC/mechanical events (if available):
plumbing/drain events (if available):
residential renovation/build events (if available):
events that triggered manual permit research (if available):
events where property/zoning/heritage context was checked (if available):
```

The first four fields are the minimum useful denominator.

## Evidence classification

### E0

- auto-reply;
- routing to sales/support;
- generic API documentation;
- invitation to book a demo;
- no denominator/timeframe/geography.

### E1

- person says permit research is common/useful;
- person says customers ask about permits;
- no bounded count.

### E2

A bounded workflow claim with:

- denominator or threshold;
- timeframe;
- geography;
- workflow location/object.

Example:

> In July 2026, customers in Toronto generated 820 residential estimates before conversion to jobs.

That is E2 even if no ProjectPermit call has occurred.

## Threshold interpretation

### <100 candidate events/month

Useful only as an E3/E4 learning partner unless price per decision is much higher than the current per-call hypothesis.

### 100–499/month

Potential validation partner. Do not expand product scope solely for this volume.

### >=500/month

Meaningful distribution candidate. Move to E3 historical benchmark if representative scopes can be supplied.

### >=2,000/month

High-priority integration candidate if the events occur upstream of permit certainty and a material share falls in supported project families/geographies.

### >=10,000/month

Potential single-channel path to the distribution checkpoint; verify scope mix, address-aware share, integration access and economics before expanding jurisdictions.

## E3 follow-up after E2 passes

Ask for **5–20 representative de-identified historical scopes**, selected from a bounded recent window rather than hand-picked successes.

Use:

```bash
python scripts/run_partner_e3_cases.py partner.csv
python scripts/summarize_historical_benchmark.py partner.evaluated.csv
```

Historical sample must retain unsupported/out-of-scope cases and must not include exact customer identity/contact/payment data.

## Why 500/month is now the preferred first gate

Public market-structure work found:

- a seven-city broad renovation-trade floor of **14,077 employer business locations**;
- Toronto Mechanical + Plumbing + Drain/Site issued permit revisions of roughly **1.67k–1.73k/month** in each of 2023, 2024 and 2025;
- Vancouver ordinary building/renovation contractor permit cadence far below 80/month.

Therefore the strongest current hypothesis is not hundreds of individually acquired ordinary contractors. It is an aggregation layer — software platform, permit operator, consultant or multi-account workflow — that can expose hundreds or thousands of candidate decisions per month.

## Current outreach wording

Use this when a contact has already received the product explanation:

> Before discussing an integration, I only need one aggregate validation point. For one recent complete month, did customers in [covered geography] collectively create at least **500 [Requests / Estimates / Quotes / Jobs]** in the workflow where permit applicability could still affect the next action? A yes/no is enough if you can state the month, geography and workflow object. No customer-level data is needed.

This wording is deliberately designed to make a useful response easier than a generic sales conversation.