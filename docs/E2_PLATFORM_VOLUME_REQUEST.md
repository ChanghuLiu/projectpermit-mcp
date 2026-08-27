# E2 bounded workflow request

Updated: 2026-08-27

Purpose: obtain a decision-useful **bounded workflow claim** before asking for integration work, customer data or a large historical export.

Positive opinions, demos, API documentation and general market-size claims do not satisfy E2.

## Principle: ask the smallest question that can falsify the thesis

Do **not** default to asking a contractor, consultant or competitor for its internal monthly volume. That can trigger unnecessary competitive/privacy resistance and is often not needed.

Prefer one of three patterns, in this order.

## Pattern A — public denominator already known

When the company's own public site already states a bounded workload/capacity, use that number and ask only for the unresolved-permit subset.

Example:

> Your site says you take on 4 projects per month. Looking at those 4 in a typical/recent month, about how many need someone to check `do we need a permit?` before the fixed quote is finalized: 0, 1, 2, 3, or 4?

Useful because:

- no internal total is requested;
- the denominator is already public;
- the answer directly measures incidence at the insertion point.

To count as E2, retain the source/date for the public denominator and the respondent's bounded workflow statement.

## Pattern B — fixed recent sample

When monthly volume is sensitive or unknown, ask about a fixed recent sequence instead of company scale.

Example:

> Think about your last 10 residential renovation estimates. For how many was permit applicability still unresolved when you first priced the job: 0, 1–2, 3–5, 6–8, or 9–10?

Then ask one optional routing question:

> For the rest, was it already resolved by the homeowner, architect/designer, permit consultant, internal checklist/software, or municipality?

A bounded `last 10` sample with workflow location can qualify as E2 if the respondent confirms it is consecutive/representative rather than hand-picked.

## Pattern C — platform / multi-account threshold

Use the >=500/month question only for a platform, multi-account operator or implementation consultant where aggregate scale is the commercial thesis.

For one recent complete month:

> In the stated covered geography, did your workflow contain at least **500 current-family candidate Requests / Assessments / Estimates / Quotes / Jobs** where permit applicability was still unresolved at that point?

A simple yes/no is useful only if the response also states:

- month or bounded date range;
- geography;
- workflow object;
- whether the count aggregates multiple customer accounts.

Do not ask for customer names, exact addresses, phone/email, payment data or account identifiers.

## The critical denominator

The quantity we need is not total projects, quotes or permits.

It is:

`current-family workflow events where permit applicability is still unresolved at the intended insertion point / total relevant events in the bounded sample`

Public workflow research shows both patterns exist:

- **quote-first**: estimate/quote before design/permit;
- **permit-first**: permit-approved drawings before construction estimate.

See `docs/QUOTE_STAGE_WORKFLOW_TIMING_EVIDENCE.md`.

Therefore a quote count is not a call denominator until permit certainty timing is measured.

## Preferred follow-up fields

If the respondent is willing to give aggregate detail:

```text
month/date range or fixed recent sample:
geography:
workflow object:
total relevant events:
events mapping to current ProjectPermit families:
events where permit applicability was unresolved at this point:
who/what resolved the remainder before this point:
events where municipality-specific rules changed a generic answer:
events where property/zoning/heritage context was needed:
```

The first six fields are the strongest E2 shape.

## Evidence classification

### E0

- auto-reply;
- routing to sales/support;
- generic API documentation;
- invitation to book a demo;
- bounced/invalid contact;
- no bounded workflow claim.

### E1

- person says permit research is common/useful;
- person says all/most jobs need permits but gives no bounded sample/timeframe;
- workflow-boundary opinion with no denominator.

### E2

A bounded workflow claim with:

- denominator or fixed sample/threshold;
- timeframe or recent-sequence boundary;
- workflow location/object;
- enough context to know what is being counted.

Examples:

> In our last 10 basement estimates, 3 needed a permit check before we could finalize pricing.

or

> In July 2026, Toronto customers generated 820 relevant estimates and about 210 still needed permit-applicability research before quote approval.

Neither requires a ProjectPermit call to have occurred.

## Threshold interpretation

### Direct account / small contractor

A 4–10 project/month contractor is useful for E3/E4 learning but cannot be the primary path to 10k calls/month unless economics are much higher than the current per-call hypothesis.

### <100 aggregated candidate events/month

Useful learning partner; weak distribution engine.

### 100–499/month

Potential validation partner. Do not expand scope solely for this volume.

### >=500/month

Meaningful distribution candidate **only if the events are current-family and applicability is still unresolved**.

### >=2,000/month

High-priority integration candidate if geography/family fit and access are real.

### >=10,000/month

Potential single-channel path to the distribution checkpoint; verify address-aware share, accuracy and economics before expansion.

## E3 follow-up after E2 passes

Ask for **5–20 representative de-identified historical scopes** from the same bounded workflow.

Offer three intake paths:

1. human-readable de-identified scope intake;
2. hosted free HTTP benchmark;
3. fully private local aggregate benchmark.

Do not require a non-technical partner to hand-write `project_facts_json`.

## Current outreach wording

### Contractor with public monthly number

> I saw your site already says you take on about [N] projects per month, so I am not asking for internal volume. Of those [N], roughly how many need someone to check whether a permit is required before the first fixed quote is finalized? A number or simple range is enough.

### Estimator / consultant

> Looking only at your last 10 consecutive residential renovation estimates, about how many still needed a `permit required?` check when you first priced them: 0, 1–2, 3–5, 6–8, or 9–10? No client names or project details needed.

### Platform / multi-account operator

> For one recent complete month, did covered-geography customers collectively create at least 500 current-family Requests/Assessments/Estimates/Quotes where permit applicability was still unresolved? A yes/no is enough if you can state the month, geography and workflow object.

The goal is not to maximize replies. It is to obtain a bounded answer that can kill or strengthen the commercial thesis.