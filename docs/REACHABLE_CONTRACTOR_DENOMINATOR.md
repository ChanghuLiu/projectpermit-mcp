# Reachable contractor denominator

Updated: 2026-08-27

Purpose: estimate a defensible **covered-geography business denominator** for ProjectPermit without using nationwide contractor counts or platform user totals as if they were directly reachable customers.

## Primary source

Use Statistics Canada's latest current table:

**Table 33-10-1176-01 — Canadian Business Counts, with employees, census metropolitan areas and census subdivisions, June 2026**

Release date: 2026-08-14.

Source page:
https://www150.statcan.gc.ca/n1/en/type/data?freq=11&geoname=S0503%2CA0005

Statistics Canada documents that the Business Counts table provides location counts with employees by employment-size range, NAICS and both census metropolitan area (CMA) and census subdivision (CSD).

## Geography rule

ProjectPermit rules are municipal, so the primary denominator must use **census subdivision**, not the full CMA.

Use CSD rows corresponding as closely as possible to the seven currently supported municipalities:

- Gatineau, Quebec
- Ottawa, Ontario
- Toronto, Ontario
- Mississauga, Ontario
- Laval, Quebec
- Longueuil, Quebec
- Vancouver, British Columbia

Do not use the Ottawa-Gatineau, Toronto, Montreal or Vancouver CMA totals as the primary covered denominator because those geographies contain municipalities ProjectPermit does not currently support.

CMA totals may be retained as an expansion ceiling only.

## Industry scope

Do not use all NAICS 23 Construction businesses as the main SAM denominator. That would include many civil/infrastructure/commercial activities unrelated to the current residential/light-building rule families.

Build three nested denominators instead.

### A. Narrow residential-builder floor

Start with:

- NAICS 23611 — Residential building construction

This is a conservative account pool with strong scope overlap but misses specialty contractors who independently create permit-sensitive jobs.

### B. Permit-sensitive trade pool

Add specialty-trade classes where ProjectPermit's existing families plausibly appear, such as:

- structural/foundation/framing contractors;
- electrical contractors;
- plumbing/HVAC contractors;
- glass/window/door contractors;
- other building-equipment / building-envelope trades where municipal permits can be relevant.

Exact 6-digit NAICS membership must be documented before summing; do not silently include all specialty trades.

### C. Broad construction ceiling

Use NAICS 23 only as an upper bound.

The commercial model should report A / B / C separately rather than choosing the largest number.

## Employer-location limitation

Table 33-10-1176-01 is explicitly **with employees**. It therefore misses businesses without employees / many owner-operators.

For ProjectPermit this means:

- the CSD employer-location count is a defensible **floor**, not the full contractor universe;
- do not inflate the CSD count using province-wide non-employer ratios unless the adjustment is clearly labeled as a scenario;
- platform-reported 'pros' counts must not be added to Statistics Canada business locations because the units are different and may overlap.

## Conversion from business denominator to call denominator

Even a clean contractor count is not API call volume.

For each municipality/trade segment, estimate:

`business locations × active-job rate × candidate-scope share × permit-decision share × ProjectPermit adoption × calls per decision`

Then separately estimate monetization:

`external preflights × address-aware share × paid conversion × realized price`

The important unknowns are therefore not only number of contractors, but:

- jobs/month/business;
- share of jobs in ProjectPermit's 8 current families;
- share where permit applicability is not already known;
- share needing address/zoning/heritage/property context;
- adoption/integration penetration;
- realized price.

## Why this matters for the 125 / 400 account scenarios

The existing call-threshold model contains examples such as:

- 125 high-volume accounts × 80 calls/month = 10,000 external calls/month;
- 400 medium accounts × 25 calls/month = 10,000 external calls/month.

The Statistics Canada CSD extraction will let us calculate what fraction of the actual covered employer-location pool those account counts represent.

Examples of the question to answer after extraction:

- If the permit-sensitive employer pool is 20,000 businesses, 125 accounts is only 0.625% penetration.
- If it is 2,000 businesses, 125 accounts is 6.25% penetration and direct acquisition becomes much harder.

These examples are arithmetic illustrations only; the actual denominator still needs to be extracted from the current table.

## Evidence boundary

Business Counts is **market structure evidence**, not E3/E4/E5 validation.

It can improve TAM/SAM discipline, but it does not prove:

- a repeated permit-preflight workflow;
- ProjectPermit accuracy on representative historical cases;
- external usage;
- willingness to pay.

The commercial evidence chain remains:

`covered business denominator -> E2 workflow frequency -> E3 historical benchmark -> E4 repeated usage -> E5 monetization`
