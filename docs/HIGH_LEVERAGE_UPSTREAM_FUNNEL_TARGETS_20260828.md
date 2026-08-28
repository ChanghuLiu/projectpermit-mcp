# High-Leverage Upstream Funnel Targets — 2026-08-28

## Purpose

Shift market validation away from one-contractor-at-a-time outreach toward Canadian platforms that already receive project scope **before quotes/contractor selection** and can potentially expose hundreds or thousands of candidate preflight events per month.

These targets do not count as demand until a bounded workflow denominator is obtained.

## Priority A — RenoAssistance

### Why it is high leverage

RenoAssistance currently reports:

- **137,000+ completed projects**;
- **2,400+ Verified Contractors**;
- approximately **15 years** operating;
- a workflow where the customer first describes the project, then works with an advisor and receives up to three contractor quotes;
- service in Quebec and Ontario, with current public pages explicitly showing Greater Ottawa, Toronto / Greater Toronto, and Outaouais in relevant service lines.

Current public service content includes ProjectPermit-relevant work such as:

- complete kitchen renovation;
- complete bathroom renovation;
- basement renovation;
- window and door replacement;
- balcony/patio renovation;
- home/garage expansion;
- home conversion;
- home and garage construction.

Sources:

- https://www.renoassistance.ca/en
- https://www.renoassistance.ca/en/residential/lp/general-contractor
- https://www.renoassistance.ca/en/residential/contact
- https://go.renoassistance.ca/en/commercial/faq
- https://www.renoassistance.ca/en/commercial/services/real-estate

### Important denominator rule

`137,000 completed projects / ~15 years` is **not** a valid current monthly denominator. It is only a scale signal justifying direct E2 measurement.

Do not convert the lifetime number into current call volume in TAM/SAM/SOM.

### E2 request sent

Recipient: `info@renoassistance.ca`

Asked for one recent complete month across Greater Ottawa + Greater Toronto + Outaouais:

1. residential renovation intake-project count bucket:
   - `<100`
   - `100-249`
   - `250-499`
   - `500-999`
   - `1,000+`
2. share still requiring someone to determine municipal permit applicability before/during quote preparation:
   - `<10%`
   - `10-24%`
   - `25-49%`
   - `50%+`

No client names, addresses, records or confidential data requested.

Evidence state: **no qualifying reply yet**.

### Why this target can move the score

If RenoAssistance reports `>=500` current-family candidate projects/month with a meaningful unresolved permit share, it would establish a credible path to the first 500+/month integration gate from one upstream workflow.

If it reports permit applicability is almost always resolved before intake/quote, that is strong negative E2 evidence against the target insertion point.

## Priority B — HomeStars

### Why it is high leverage

HomeStars' current workflow is explicitly:

1. homeowner **posts a job** with project details;
2. suitable pros receive/respond to the lead;
3. homeowner shortlists pros and then discusses/collects quotes.

HomeStars currently exposes service coverage in Toronto, Ottawa, Mississauga and Vancouver and lists many ProjectPermit-current-family jobs, including:

- basement renovation;
- decking;
- sheds/outbuildings;
- garages;
- porches;
- kitchens;
- bathrooms;
- windows;
- general contracting and renovation.

Sources:

- https://www.homestars.com/services
- https://www.homestars.com/pro/register
- https://www.homestars.com/blog/become-a-partner

A current public lead sample also visibly contains scope that maps to ProjectPermit families before contractor selection. See `docs/HOMESTARS_UPSTREAM_OBSERVATION_20260828.md`.

### E2 request sent

Recipient: `service@homestars.com` (public professional-contact address)

Asked for one recent complete month across Toronto + Ottawa + Mississauga + Vancouver:

1. number of residential project postings in renovation/building categories where municipal permit applicability could plausibly matter:
   - `<100`
   - `100-499`
   - `500-1,999`
   - `2,000-9,999`
   - `10,000+`
2. share arriving before permit applicability had already been established:
   - `<10%`
   - `10-24%`
   - `25-49%`
   - `50%+`

No homeowner names, addresses, job records or confidential data requested.

Evidence state: **no qualifying reply yet**.

### Why this target can move the score

HomeStars can potentially expose the exact object ProjectPermit wants to enrich: a project description before pros quote.

If a covered current-family monthly posting denominator is large and permit certainty is frequently missing, this is more commercially meaningful than dozens of single-contractor interviews because one integration could supply repeated calls across many contractors.

If permit status is already internally known or current-family candidate volume is small, downgrade the platform hypothesis.

## Secondary watch — TrustedPros

TrustedPros publicly shows a Canadian project-posting / contractor-matching workflow and large cumulative Ontario project signals. Its public pages show homeowners can post projects and let local contractors compete for the job.

Sources:

- https://trustedpros.ca/on/toronto/general-contracting
- https://trustedpros.ca/on/toronto/plumbing

However, the current scan did **not** identify a verified public company email suitable for this research request.

Do not guess an email address. Keep as a future E2 target if a verified business contact route is found.

Also do not treat cumulative `Ontario homeowners helped` or project-value figures as a recent monthly denominator.

## Priority interpretation

These targets are now **higher learning priority** than another generic single contractor because they combine:

- project scope before quote/selection;
- multi-contractor distribution leverage;
- overlap with current supported cities/families;
- potential to hit the `>=500 candidate events/month` gate through one workflow.

They are **not** automatically higher engineering priority because no API/integration request has been validated.

## Build rule

Do not build RenoAssistance or HomeStars adapters/speculative connectors yet.

Engineering begins only if one of these occurs:

- bounded E2 shows >=500 covered candidate events/month and meaningful unresolved applicability;
- a platform explicitly requests a technical pilot;
- representative E3 cases are supplied and benchmark well;
- a platform provides a safe sandbox/export/webhook/API route that can reach E4 without customer-data overcollection.

## Current state

As of 2026-08-28:

- RenoAssistance E2 request: **sent**;
- HomeStars E2 request: **sent**;
- TrustedPros: **watch / no verified email found**;
- qualifying E2 from these upstream funnels: **0**;
- E3: **0 / 2**;
- E4 external repeated workflow: **0**;
- E5: **0**.