# Pilot city × buyer fit × source-maintenance matrix — 2026-08-30

## Purpose

Prevent two opposite mistakes when choosing a representative Layer-C E3 pilot:

1. choosing the contractor that looks most attractive while ignoring the cost of maintaining its official-source layer; or
2. choosing the municipality with the easiest crawler merely because its sources are machine-friendly, even though no buyer has validated the workflow.

The correct order is:

> **direct buyer evidence first; source-maintenance cost breaks ties and shapes the operating model.**

A Tier-C municipality is not disqualified from a small representative pilot if the buyer evidence is strong. Conversely, a Tier-A municipality is not a reason to build without buyer evidence.

## Current source-observability baseline

From the official-source observability audit:

| Municipality | Canonical sources | Direct machine fetch | Validators | Monitoring mode |
|---|---:|---:|---:|---|
| Toronto | 5 | 5/5 | 3 | Tier A |
| Mississauga | 5 | 5/5 | 4 | Tier A |
| Ottawa | 12 | 4/12 | 1 | split Tier A/B |
| Vancouver | 4 | 0/4 | 0 | Tier C |
| Gatineau | 7 | 7/7 | 0 | Tier A/hash |
| Laval | 5 | 0/5 | 0 | Tier C |
| Longueuil | 4 | 4/4 | 4 | Tier A |

A follow-up probe of eight plausible first-party Laval/Vancouver alternate surfaces also produced 0/8 successes from the same commodity runner environment.

Source:
- `docs/REGULATORY_SOURCE_MONITORING_POLICY.md`

## Current buyer/workflow specimens

### Vancouver — PCC-like remodel/general contractor

Strengths:

- current supported municipality;
- very high overlap with existing families;
- public Jobber/ClickUp workflow;
- public evidence of permit/regulation/timeline handling;
- public statement of weekly zoning/bylaw monitoring;
- exact license-light representative bathroom/kitchen renovation E3 slice is now documented;
- no city expansion or new vertical needed.

Weakness:

- Vancouver canonical source monitoring is Tier C from commodity CI;
- no direct buyer denominator/externalization/payment evidence yet.

### Toronto — Summit-like residential remodeler, Toronto records only

Strengths:

- very high overlap with current renovation families;
- Jobber customer evidence;
- company publicly handles permits and maintains permit/building/fire-code knowledge;
- Toronto official sources are currently the cleanest high-value Tier-A set: 5/5 direct, 3 validators.

Weaknesses:

- company is based primarily in unsupported Richmond Hill/York Region;
- only representative Toronto records are valid for a no-expansion pilot;
- no direct `last 20 estimates` evidence;
- no exact Toronto obligation E3 slice is currently documented at the same level as Vancouver.

### Ottawa — Ottawa Plumbing & Heating-like Jobber workflow

Strengths:

- current supported municipality;
- public operational evidence of Jobber + ESA/Hydro/City inspection/document workflow + job costing;
- directly demonstrates regulatory process work living next to the field-service work record.

Weaknesses:

- current ProjectPermit family overlap is narrower than PCC/Summit;
- much business activity is service/HVAC/electrical rather than today's residential-renovation wedge;
- Ottawa source monitoring is mixed: only 4/12 canonical sources directly pass the runner audit.

### Mississauga / Gatineau / Longueuil

Strength:

- source observability is good (5/5, 7/7, 4/4 respectively).

Weakness:

- no equally strong current public Jobber/Buildxact buyer specimen has yet been established in the current validation work.

Do not manufacture a pilot solely because the source layer is easy to monitor.

### Laval

Current state:

- no strong current buyer specimen;
- source observability is Tier C / 0-of-5 direct.

No reason to prioritize Laval for representative E3 at this stage.

## Decision matrix

| Candidate | Buyer archetype fit | Current family fit | Current platform/work-record fit | Direct buyer evidence | Source maintenance | E3 readiness | Current decision |
|---|---|---|---|---|---|---|---|
| **Vancouver / PCC-like** | Very high | Very high | Very high (Jobber) | Pending | Higher manual burden / Tier C | **Exact slice ready** | **P0 if E2 crosses** |
| **Toronto / Summit-like Toronto records** | High | Very high | High (Jobber) | None | **Low / Tier A** | medium; slice not yet frozen | P1 backup / tie-break winner on maintenance |
| Ottawa / OPH-like | medium | medium-low | **Very high (Jobber + inspections/docs)** | none | mixed A/B | medium | workflow contrast / secondary pilot |
| Mississauga | unknown | potentially high | unknown | none | **low / Tier A** | rules exist, buyer missing | do not build for source convenience |
| Gatineau | unknown | potentially high | unknown | none | **low / Tier A** | rules exist, buyer missing | do not build for source convenience |
| Longueuil | unknown | potentially high | unknown | none | **low / Tier A** | rules exist, buyer missing | do not build for source convenience |
| Laval | unknown | unknown | unknown | none | higher manual burden / Tier C | no representative buyer slice | deprioritize |

## Key tradeoff: PCC buyer fit versus Vancouver maintenance cost

PCC currently wins on **validation fit**, not on maintenance economics.

That distinction matters.

If PCC or an equivalent Vancouver remodeler directly reports something like:

- `8+ of last 20 estimates` need current regulatory research;
- the result changes price/scope/schedule/documents/inspections;
- research/currentness is a repeated burden;
- buyer prefers an external maintained source-of-truth layer;

then **use Vancouver for the representative E3**, even though source monitoring is Tier C.

Why:

- the E3 question is whether the workflow value exists;
- the documented license-light slice is small enough for bounded manual source verification;
- changing to Toronto merely to get nicer automation would introduce a different buyer/workflow variable.

Do not optimize the crawler before validating the buyer.

## When source-maintenance cost should change the decision

Maintenance becomes decisive in three situations.

### Case 1 — two buyers produce similarly strong E2

If a Vancouver buyer and a Toronto buyer produce similarly strong denominator/consequence/externalization evidence, prefer **Toronto** for the first scalable production slice because its official source layer is materially cheaper to observe automatically.

### Case 2 — buyer demand is weak/moderate

If a Vancouver buyer reports only marginal value (`0–2/20` or low consequence), do not accept Tier-C maintenance cost to rescue a weak market signal.

### Case 3 — after representative E3 succeeds

If a Vancouver E3 succeeds and moves toward recurring production, calculate explicit ongoing Tier-C maintenance cost:

- official push subscriptions available;
- manual verification cadence;
- minutes per review;
- frequency of actual material changes;
- expected customer/account revenue.

Only then decide whether Vancouver Tier-C maintenance is economically acceptable at scale.

## Do not confuse E3 validation cost with terminal maintenance cost

For a single representative pilot:

- manually re-verifying a handful of Vancouver first-party process pages is acceptable;
- no need to build brittle browser scraping;
- no need to abandon the strongest buyer merely because CI receives 403.

For hundreds/thousands of accounts:

- manual maintenance must be priced into the account/licence economics;
- Tier-A jurisdictions become structurally more attractive;
- a future official machine-readable/push source could promote a Vancouver source later.

## Exact pilot selection rule

Use this order:

1. `recent direct buyer denominator`;
2. `material workflow consequence`;
3. `externalization preference`;
4. `current family + municipality overlap`;
5. `representative E3 simplicity`;
6. `source-maintenance cost`;
7. only then platform scale / broader TAM.

This prevents source engineering from driving the market thesis.

## Current recommendation

**Do not switch away from PCC/Vancouver just because Vancouver is Tier C.**

PCC remains the P0 supported-city validation target because it is currently the cleanest intersection of:

`current city + current family + Jobber + explicit maintained-regulatory workflow`

But keep Toronto as the highest-quality operational fallback because:

- Toronto source observability is 5/5;
- the family fit is strong;
- Summit-like Toronto work records can supply a representative buyer type without new geography.

## Evidence score

No E-level change.

This is a **pilot economics / operating-cost decision framework**, not customer evidence.