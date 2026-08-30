# Layer C buyer-archetype ranking — 2026-08-30

## Purpose

Use the accumulated public frequency, workflow, staffing and platform evidence to narrow **who ProjectPermit should validate first**.

This avoids two common errors:

1. chasing the buyer with the highest theoretical permit volume even when ProjectPermit's current project families do not fit;
2. chasing the easiest integration platform even when its users mostly perform low-regulatory service/maintenance work.

This is a targeting hypothesis, not buyer evidence. It does not cross E2.

## Decision dimensions

Each archetype is assessed on:

- **current-family fit** — overlap with ProjectPermit's current renovation/construction families;
- **frequency potential** — plausible repeated requirement checks;
- **material consequence** — likelihood the answer changes quote/scope/schedule/professional/document/inspection handling;
- **replacement budget** — existing staff/consultant effort that can plausibly be reduced;
- **externalization fit** — whether maintained jurisdiction knowledge is reasonably non-core;
- **build-vs-buy risk** — whether the buyer is large/technical enough to internalize the logic;
- **distribution friction** — cost to reach/test the buyer.

## 1. Rank #1 — multi-municipality residential remodel/design-build contractor

### Typical work

- kitchens/bathrooms with layout or trade changes;
- basement finishing/legal suites;
- structural interior renovation;
- additions;
- decks/porches;
- accessory structures;
- window/door changes;
- plumbing-related renovation.

### Why this is the best current buyer archetype

**Current-family fit: very high.**

This is almost exactly ProjectPermit's current eight-family wedge.

**Frequency: medium to high.**

Public contractor evidence includes:

- permits on all remodeling projects;
- permit costs/engineering/sign-offs factored into every quote by permit-heavy Canadian contractors;
- contractors operating in multiple municipalities with different fee/process requirements.

**Consequence: high.**

Permit/professional/document requirements directly affect:

- whether scope can be quoted as proposed;
- engineering/designer allowance;
- permit fees;
- schedule assumptions;
- inspection sequence;
- client exclusions/allowances.

**Replacement budget: plausible.**

The research is often performed by the owner, estimator, project coordinator, designer or permit consultant before the quote is locked.

**Externalization fit: good.**

A remodel contractor's core competency is selling/building renovations, not maintaining normalized municipal requirements across cities.

**Build-vs-buy risk: moderate.**

A 5–50 person contractor is less likely than a software platform to build/maintain a rules engine, especially across municipalities.

### Best distribution surfaces

1. Jobber — General Contractor / Remodeling segments + low-account draft/private integration;
2. Buildxact — strongest preconstruction/estimating fit, formal third-party API but app registration required;
3. direct API/private pilot if buyer does not use either platform.

### E2 question

> In your last 20 renovation estimates, how many required you to verify a permit, code, engineer/designer, drawing/document, inspection or other municipality-specific requirement before pricing? In how many did the answer change the quote or schedule?

This is the highest-priority archetype.

---

## 2. Rank #2 — permit-heavy specialty contractor across multiple jurisdictions

### Examples

- HVAC;
- plumbing;
- electrical;
- structural alteration specialist;
- basement/ADU specialist;
- window/door contractor where local permit thresholds vary.

### Why attractive

**Frequency: potentially very high.**

Public contractor evidence includes a company reporting **hundreds of permits/year**, with 2–3 people using a shared jurisdiction-specific permit knowledge base.

This is unusually strong evidence of a real maintenance burden.

**Replacement budget: high once volume is high.**

Repeated city-specific rules, forms, quirks and process knowledge can consume dedicated staff time.

### Why not rank #1 today

**Current-family fit is uneven.**

ProjectPermit currently covers only some relevant specialty-trade scenarios. A broad HVAC/electrical permitting product would require new normalized project families and possibly new regulatory/code content.

Do not expand product families merely to chase this volume before the current wedge validates.

### Commercial model

Likely stronger fit for:

- monthly account licence;
- multi-jurisdiction package;
- later API integration into field-service software.

High volume also raises internal-build pressure, so maintained freshness/breadth is essential.

---

## 3. Rank #3 — small/mid-sized permit consultant / designer serving contractors

### Why attractive

Permit/design firms already externalize jurisdiction/process expertise and manage applications professionally.

They may have repeated workflows across many clients and strong knowledge of where municipal research is costly.

### Why lower priority

They are both potential buyer **and competitor/substitute**.

A permit consultant may view current regulatory research as core intellectual capital and therefore prefer internal tools rather than buying an external decision layer.

They may still buy:

- source change monitoring;
- cross-jurisdiction normalized data;
- pre-screening automation;
- evidence/version infrastructure.

But build-vs-buy risk is higher than for a remodel contractor.

---

## 4. Rank #4 — construction software platform vendor

### Examples

- Jobber;
- Buildxact;
- Buildertrend;
- ServiceTitan;
- ServiceM8.

### Why strategically valuable

One integration can create hundreds/thousands of active end accounts and large call volume.

### Why not the first proof target

Contrax already exposed the core risk:

- a software vendor can build narrow permit logic internally;
- it is more likely to buy a **maintained regulations/building-code layer** than a commodity yes/no checker.

Large platforms also require stronger product reliability, jurisdiction breadth, rights clarity, support and integration maturity.

### Role in sequence

Use platform vendors as:

- high-leverage distribution after end-user workflow proof;
- buyer validation for the maintained-data layer;
- eventual licence/minimum-commitment customers.

Do not require an enterprise platform deal to reach E4.

---

## 5. Rank #5 — production homebuilder

### Evidence of real permit headcount

Public career/professional evidence shows dedicated permit roles at production builders such as Minto/Empire, and architecture/municipal-code coordination roles at Mattamy.

Examples surfaced in current research:

- Permit Coordinator at Empire Communities;
- Permit Coordinator -> Architecture & Permits Manager career path at Minto Group;
- Mattamy Architectural Coordinator responsible for consultant deliverables, municipal requirements and Ontario Building Code alignment.

This demonstrates a real fixed-headcount budget once permitting volume is large.

### Why not current target

ProjectPermit's current normalized families are renovation/remodel oriented, not greenfield production-home permitting.

Serving production homebuilders properly would require a materially different product surface:

- new-home/building types;
- subdivision/site/lot context;
- repeated model/lot permitting;
- planning/development overlays;
- potentially much deeper technical-code content.

Do not expand into that merely because the headcount economics look attractive.

This is a future adjacent market after the core wedge proves itself.

---

## 6. Do not target — major infrastructure permit coordinator

Current Toronto job postings show large infrastructure projects paying roughly **$68K–$135K+** for permit coordinator/manager roles, with some VINCI roles around `$100K–$115K`.

Responsibilities can include:

- construction/environmental/operational permits;
- permit trackers;
- regulatory-agency interface;
- review of drawings/contracts;
- work permits/HSE authorization;
- audits and internal safety systems.

This proves that regulatory/permit coordination can support dedicated high-cost headcount at scale.

It does **not** make these companies a ProjectPermit target.

Major infrastructure permitting is outside current scope and includes environmental, safety, utility and project-specific approvals far beyond residential building-permit preflight.

Treat this only as a general `regulatory complexity can justify headcount/software` precedent.

Sources:

- https://jobs.vinci.com/fr/emploi/toronto/permit-coordinator/1440/37037743296
- https://ca.indeed.com/q-permits-coordinator-l-ontario-jobs.html
- https://ca.indeed.com/q-permit-coordinator-l-toronto%2C-on-jobs.html

---

## Buyer ranking table

| Archetype | Current-family fit | Frequency | Consequence | Externalization fit | Build-vs-buy risk | Validation priority |
|---|---|---|---|---|---|---|
| Multi-municipality remodel/design-build contractor | **Very high** | Med–High | **High** | **High** | Low–Med | **#1** |
| Permit-heavy specialty contractor | Med | **Very high** | High | High | Med | **#2** |
| Permit consultant/designer | High | High | High | Low–Med | **High** | #3 |
| Construction software vendor | Variable | **Very high leverage** | High | Med–High for maintained layer | **Very high** | #4 / distribution |
| Production homebuilder | Low for current wedge | Very high | High | High | Med–High | #5 / future adjacent |
| Major infrastructure contractor | **Very low** | Very high | Very high | High | High | **Do not target now** |

## Ideal first design-partner profile

If a buyer appears organically, prioritize one matching most of these characteristics:

- residential renovation/remodel/design-build;
- works in **2+ municipalities**;
- performs at least roughly **10+ estimates/month**;
- projects regularly include basements, additions, structural interiors, decks/porches, kitchens/baths, accessory structures or window/door changes;
- owner/estimator/coordinator currently checks municipality websites/calls staff/consults designer before some quotes;
- has experienced quote/schedule changes due to permit/professional/document/inspection requirements;
- does not have an internal regulatory software/data team;
- uses Jobber or Buildxact if possible, but platform use is not mandatory.

This is a **target profile**, not a claim that such buyers have already validated ProjectPermit.

## Stop rules

Do not let attractive adjacent segments pull the product away from the validated wedge.

Before adding a new project family solely for a new buyer archetype, require either:

- repeated E4 from the existing families showing expansion demand; or
- a strong bounded buyer denominator in the new archetype plus clear economic commitment.

## Current decision

The immediate buyer-validation focus should narrow to:

> **multi-municipality residential remodel/design-build contractors whose estimate workflow already carries permit/engineering/document/inspection assumptions.**

This is where ProjectPermit's current family coverage, public frequency evidence, quote consequence and low build-vs-buy risk overlap best.

No E-level increase.
