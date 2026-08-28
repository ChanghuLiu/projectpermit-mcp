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

Current public service content includes ProjectPermit-relevant work such as kitchens, bathrooms, basements, windows/doors, balcony/patio renovation, additions, conversions and garage/home construction.

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

1. residential renovation intake-project count bucket: `<100 / 100-249 / 250-499 / 500-999 / 1,000+`;
2. share still requiring someone to determine municipal permit applicability before/during quote preparation: `<10% / 10-24% / 25-49% / 50%+`.

No client names, addresses, records or confidential data requested.

Evidence state: **no qualifying reply yet**.

## Priority B — HomeStars

### Why it is high leverage

HomeStars' current workflow is explicitly:

1. homeowner **posts a job** with project details;
2. suitable pros receive/respond to the lead;
3. homeowner shortlists pros and then discusses/collects quotes.

HomeStars currently exposes service coverage in Toronto, Ottawa, Mississauga and Vancouver and lists many ProjectPermit-current-family jobs including basements, decking, sheds/outbuildings, garages, porches, kitchens, bathrooms, windows and general renovation.

Sources:

- https://www.homestars.com/services
- https://www.homestars.com/pro/register
- https://www.homestars.com/blog/become-a-partner

A current public lead sample also visibly contains scope that maps to ProjectPermit families before contractor selection. See `docs/HOMESTARS_UPSTREAM_OBSERVATION_20260828.md`.

### E2 request sent

Recipient: `service@homestars.com`

Asked for one recent complete month across Toronto + Ottawa + Mississauga + Vancouver:

1. candidate residential renovation/building posting volume: `<100 / 100-499 / 500-1,999 / 2,000-9,999 / 10,000+`;
2. share arriving before permit applicability had already been established: `<10% / 10-24% / 25-49% / 50%+`.

No homeowner names, addresses, job records or confidential data requested.

Evidence state: **no qualifying reply yet**.

## Priority C — GoQuotes

### Why it is high leverage

GoQuotes' public workflow starts with the homeowner describing a renovation project and then routes the project to an average of approximately three contractors for quotes.

Current public geography includes **Gatineau, Laval, Ottawa and Toronto**, all inside ProjectPermit's current footprint, as well as other Canadian cities.

Public categories overlap strongly with current families, including:

- home additions;
- garage construction;
- patio/balcony/deck work;
- basement renovation;
- doors/windows;
- kitchen/bathroom renovation;
- general contracting.

Sources:

- https://goquotes.ca/

### E2 request sent

Recipient: `info@goquotes.ca`

Asked for one recent complete month across Gatineau + Laval + Ottawa + Toronto:

1. current-family project count bucket: `<100 / 100-249 / 250-499 / 500-999 / 1,000+`;
2. share reaching intake before permit applicability had already been established: `<10% / 10-24% / 25-49% / 50%+`.

Evidence state: **no qualifying reply yet**.

### Why it matters

GoQuotes has unusually clean geography overlap with ProjectPermit's already-built rules. If a current-family unresolved-intake denominator reaches >=500/month, it can test distribution without speculative municipality expansion.

## Priority D — JobDeck

### Why it is diagnostically useful

JobDeck currently exposes two different workflow layers:

1. Ontario homeowners post a renovation job, after which local contractors are notified and typically 2-4 contact the homeowner;
2. contractors can access public municipal building-permit data for prospecting/business intelligence.

This creates a useful product-boundary test:

> Is issued-permit data only downstream intelligence after a permit event already exists, while a separate `does this new posted job require a permit?` question remains unresolved upstream?

Current public site reports **1,100+ renovation projects tracked across Ontario**, but the timeframe and exact definition are not clear enough to count as a monthly E2 denominator.

Source:

- https://jobdeck.ca/

### E2 request sent

Recipient: `jonathan@jobdeck.ca`

Asked for one recent complete month across Toronto + Ottawa + Mississauga:

1. homeowner-posted current-family-like renovation jobs: `<100 / 100-249 / 250-499 / 500+`;
2. share where permit applicability was not already established at posting: `<10% / 10-24% / 25-49% / 50%+`;
3. whether JobDeck's public permit-data feed is mainly downstream/prospecting intelligence or already determines permit applicability for newly posted work.

Evidence state: **no qualifying reply yet**.

## Strategic adjacent target — RealCraft

RealCraft is not being treated as a volume target yet because its public client marketplace is still Beta / founding-member stage.

It matters for **build-vs-buy falsification** instead: RealCraft already bundles a free municipal Permit Navigator/Advisor into the pre-hire quote funnel and independently maintains city permit guidance.

A direct message asked whether RealCraft maintains those rules internally and whether it would consider an external deterministic/evidence-linked permit API as it expands.

See `docs/REALCRAFT_PERMIT_NAVIGATOR_THREAT_20260828.md`.

Evidence state: **no qualifying reply yet**.

## Secondary watch — TrustedPros

TrustedPros publicly shows a Canadian project-posting / contractor-matching workflow and large cumulative Ontario project signals. Its public pages show homeowners can post projects and let local contractors compete for the job.

Sources:

- https://trustedpros.ca/on/toronto/general-contracting
- https://trustedpros.ca/on/toronto/plumbing

However, the current scan did **not** identify a verified public company email suitable for this research request.

Do not guess an email address. Keep as a future E2 target if a verified business contact route is found. Also do not treat cumulative `Ontario homeowners helped` or project-value figures as a recent monthly denominator.

## Priority interpretation

RenoAssistance, HomeStars, GoQuotes and JobDeck are now higher learning priority than another generic single contractor because they combine some or all of:

- project scope before quote/selection;
- multi-contractor distribution leverage;
- overlap with current supported cities/families;
- potential to hit the `>=500 candidate events/month` gate through one workflow.

They are **not** automatically higher engineering priority because no API/integration request has been validated.

## Build rule

Do not build platform-specific adapters/speculative connectors yet.

Engineering begins only if one of these occurs:

- bounded E2 shows >=500 covered candidate events/month and meaningful unresolved applicability;
- a platform explicitly requests a technical pilot;
- representative E3 cases are supplied and benchmark well;
- a platform provides a safe sandbox/export/webhook/API route that can reach E4 without customer-data overcollection.

## Current state

As of 2026-08-28:

- RenoAssistance E2 request: **sent**;
- HomeStars E2 request: **sent**;
- GoQuotes E2 request: **sent**;
- JobDeck E2/boundary request: **sent**;
- RealCraft build-vs-buy request: **sent**;
- TrustedPros: **watch / no verified email found**;
- qualifying E2 from these upstream funnels: **0**;
- E3: **0 / 2**;
- E4 external repeated workflow: **0**;
- E5: **0**.