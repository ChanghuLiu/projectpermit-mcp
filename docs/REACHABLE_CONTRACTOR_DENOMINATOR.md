# Reachable contractor denominator

Updated: 2026-08-27

Purpose: estimate a defensible **covered-geography business denominator** for ProjectPermit without using nationwide contractor counts or platform user totals as if they were directly reachable customers.

## Primary source

Statistics Canada:

**Table 33-10-1176-01 — Canadian Business Counts, with employees, census metropolitan areas and census subdivisions, June 2026**

Release date: 2026-08-14.

Source page:
https://www150.statcan.gc.ca/n1/en/type/data?freq=11&geoname=S0503%2CA0005

Reproducible extractor:

```bash
python scripts/statcan_reachable_contractor_denominator.py
```

The dedicated GitHub Actions workflow downloads the current official StatCan CSV ZIP and fails closed if geography, employment-size or NAICS parsing becomes ambiguous.

## Geography rule and verification

ProjectPermit rules are municipal, so the denominator uses **census subdivision (CSD)**, not the full census metropolitan area (CMA).

The StatCan CSV can contain the same `GEO` label for a municipality and its CMA. For example, `Toronto` appears with both:

- `2021A00053520005` — Toronto CSD;
- `2021S0503535` — Toronto CMA.

The extractor therefore selects the administrative-area CSD DGUID schema `A0005` plus the expected province UID rather than relying on name matching alone.

No Ottawa-Gatineau, Toronto, Montreal or Vancouver CMA total is substituted for a supported municipality.

## Observed June 2026 employer-location denominator

These are **employer business locations**, not platform users and not estimates.

Industry layers:

- **A — residential building:** NAICS `2361`, Residential building construction.
- **B core — permit-sensitive building trades:** `2361 + 2381 + 2382` (residential building + foundation/structure/exterior + building equipment contractors).
- **B broad — renovation-trade working pool:** B core + `2383` Building finishing contractors.
- **C — all construction ceiling:** NAICS `23`; never use this as the main SAM.

| Supported municipality | A residential | B core | B broad | C all construction |
|---|---:|---:|---:|---:|
| Toronto | 1,944 | 4,239 | 5,443 | 6,906 |
| Ottawa | 756 | 1,821 | 2,389 | 2,970 |
| Mississauga | 567 | 1,524 | 2,025 | 2,539 |
| Vancouver | 729 | 1,253 | 1,643 | 2,185 |
| Laval | 493 | 1,131 | 1,378 | 1,791 |
| Gatineau | 222 | 475 | 605 | 771 |
| Longueuil | 213 | 445 | 594 | 715 |
| **Seven-city total** | **4,924** | **10,888** | **14,077** | **17,877** |

The corresponding CSD DGUIDs are:

- Toronto `2021A00053520005`
- Ottawa `2021A00053506008`
- Mississauga `2021A00053521005`
- Vancouver `2021A00055915022`
- Laval `2021A00052465005`
- Gatineau `2021A00052481017`
- Longueuil `2021A00052458227`

## What the 10k-call account shapes now imply

Using the observed seven-city employer-location pools:

| Account target | A residential penetration | B core penetration | B broad penetration | Calls/account/month needed for 10k external calls |
|---:|---:|---:|---:|---:|
| 125 | 2.539% | 1.148% | **0.888%** | 80 |
| 400 | 8.123% | 3.674% | **2.842%** | 25 |
| 500 | 10.154% | 4.592% | **3.552%** | 20 |

This is a materially better result than an ungrounded national-platform denominator: **125 high-volume accounts would be less than 1% of the observed broad employer-location pool**.

But the difficult variable is still cadence. The table does not say that 125 of those locations each have 80 unresolved permit decisions per month. That must be established through E2/E4 workflow evidence.

## Geographic concentration

The broad employer pool is not evenly distributed:

- Toronto + Ottawa + Mississauga: **9,857 / 14,077 ≈ 70.0%**
- Vancouver: **1,643 / 14,077 ≈ 11.7%**
- Laval + Gatineau + Longueuil: **2,577 / 14,077 ≈ 18.3%**

Validation outreach should therefore be weighted toward Ontario rather than spread equally across all seven municipalities. Vancouver is the next distinct regional test; the three Quebec municipalities remain a meaningful third cohort.

This is an evidence-acquisition priority, not a claim that Ontario contractors have a higher permit-decision rate.

## Employer-location limitation

Table 33-10-1176-01 is explicitly **with employees**. It misses businesses without employees / many owner-operators.

Statistics Canada's June 2026 companion table for businesses **without employees** is available at Canada/province level, but the current public CSD/CMA table is with-employees only. Therefore:

- the 4,924 / 10,888 / 14,077 counts are a defensible municipal **employer-location floor**;
- do not apply a province-wide non-employer ratio to a city and present it as an observed city count;
- platform-reported `pros` counts must not be added to Statistics Canada business locations because the units are different and may overlap.

Also note that a **business location is not necessarily a unique company/account**. A multi-location company can contribute more than one location, while excluding non-employers moves the denominator in the opposite direction. This dataset is therefore a defensible market-structure proxy, not an exact count of potential paying accounts.

## Provincial non-employer sensitivity — missing-pool scale only

The same reproducible extractor also reads:

- **33-10-1174-01** — businesses with employees, Canada/provinces, June 2026;
- **33-10-1175-01** — businesses without employees, Canada/provinces, June 2026.

These province-level figures answer only: *how large is the contractor population excluded by an employer-only municipal table?* They do **not** provide a city-level uplift factor.

### Broad renovation-trade layer (2361 + 2381 + 2382 + 2383)

| Province | With employees | Without employees | Without / with ratio | Without-employees share of combined |
|---|---:|---:|---:|---:|
| Ontario | 42,308 | 82,601 | **1.952×** | **66.13%** |
| British Columbia | 21,664 | 38,199 | **1.763×** | **63.81%** |
| Quebec | 27,320 | 23,399 | **0.856×** | **46.13%** |

### Core permit-sensitive layer (2361 + 2381 + 2382)

| Province | With employees | Without employees | Without / with ratio | Without-employees share of combined |
|---|---:|---:|---:|---:|
| Ontario | 33,415 | 57,277 | **1.714×** | 63.16% |
| British Columbia | 16,528 | 27,440 | **1.660×** | 62.41% |
| Quebec | 22,036 | 18,155 | **0.824×** | 45.17% |

### Interpretation

The municipal employer-only floor is therefore likely to omit a **material** contractor pool, especially in Ontario and British Columbia. In those provinces, businesses without employees outnumber employer locations by roughly 1.7–2.0× in the relevant broad/core construction layers.

However, ProjectPermit must **not** calculate `city employer locations × provincial ratio` and present the result as an observed municipal SAM. The geographic distribution of non-employer contractors may differ materially from the employer distribution.

The correct statement is:

> The seven-city B-broad **observed employer-location floor is 14,077**. Current provincial evidence shows the omitted without-employees contractor population is large—especially in Ontario and BC—so the actual covered contractor-location universe is plausibly substantially larger, but its exact seven-city count is unknown from the current public StatCan CSD tables.

This strengthens the conclusion that **account count is probably not the main constraint**. The harder commercial unknown remains repeated permit-decision cadence per account.

## Conversion from business denominator to call denominator

Even a clean contractor count is not API call volume.

For each municipality/trade segment, estimate:

`business locations × active-job rate × candidate-scope share × permit-decision share × ProjectPermit adoption × calls per decision`

Then separately estimate monetization:

`external preflights × address-aware share × paid conversion × realized price`

The important unknowns remain:

- jobs/month/business;
- share of jobs in ProjectPermit's 8 current families;
- share where permit applicability is not already known;
- share needing address/zoning/heritage/property context;
- adoption/integration penetration;
- realized price.

## Evidence boundary

Business Counts is **market structure evidence**, not E3/E4/E5 validation.

It improves SAM discipline but does not prove:

- a repeated permit-preflight workflow;
- ProjectPermit accuracy on representative historical cases;
- external usage;
- willingness to pay.

The commercial evidence chain remains:

`covered business denominator -> E2 workflow frequency -> E3 historical benchmark -> E4 repeated usage -> E5 monetization`
