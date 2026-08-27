# Trade permit workload evidence

Updated: 2026-08-27

Purpose: separate **single-contractor cadence**, **city/platform trade-permit volume**, and **work that can be plausibly related to ProjectPermit's current eight project families** when evaluating the path to repeated API calls.

This is market-structure evidence only. It is not E3, E4 or E5 validation and it does not measure ProjectPermit preflight incidence.

## Vancouver 2024 — named building-contractor workload

Source: City of Vancouver Open Data `issued-building-permits`.

The analysis intentionally requests only permit number, year/month, work type, permit category and building-contractor fields. Contractor strings are used only in runner memory for frequency counts; output contains no contractor names or hashes.

For corporate-like contractor tokens in the 2024 issued-building-permit dataset:

- all building permits: maximum **47 permits/year**; maximum any single month **8**;
- Addition / Alteration: maximum **35/year**; maximum any single month **8**;
- residential renovation: maximum **20/year**; maximum any single month **5**;
- all building permits: **39** contractor tokens had at least 12 permits/year, **16** had at least 20/year, **4** had at least 40/year, and **0** had at least 60/year.

Interpretation: the earlier `80 calls/account/month` direct-contractor scenario should not be treated as a typical building/renovation-contractor shape. A high-volume direct account would need either substantially more upstream candidate jobs than issued building permits, a sub-trade workflow not represented by this dataset, or multi-jurisdiction/multi-branch volume.

### Vancouver aggregate-label diagnostic

The same 2024 City extract contains **4,907 issued building-permit records**. Aggregate City labels were:

| City label | 2024 issued records |
|---|---:|
| `Addition / Alteration` | **2,544** |
| `New Building` | 1,103 |
| `Demolition / Deconstruction` | 631 |
| `Salvage and Abatement` | 583 |
| `Temporary Building / Structure` | 37 |
| `Outdoor Uses (No Buildings Proposed)` | 9 |

Permit-category labels include:

| Permit category | 2024 issued records |
|---|---:|
| `Renovation - Commercial/ Mixed Use - Lower Complexity` | 1,070 |
| `Renovation - Residential - Lower Complexity` | **888** |
| `New Build - Low Density Housing` | 598 |
| `New Build - Standalone Laneway` | 296 |
| blank | 2,055 |

All **888** residential-renovation records pair with `Addition / Alteration`, or **74/month**.

This is useful as a **residential-renovation diagnostic**, but the City labels are not granular enough to map those 888 records safely into a specific ProjectPermit family. `Addition / Alteration` can encompass interior renovation, exterior alteration, windows/doors, additions and other work. Therefore:

> **Vancouver contributes 74 residential-renovation issued events/month as a diagnostic only; it contributes zero to the conservative current-family mapped floor until a more granular first-party field/source is available.**

Do not force the 888 records into `interior_renovation` merely because the category contains the word `Renovation`.

The City FOI release 2024-671 includes building and sub-trade permits (mechanical, electrical, plumbing, HVAC, etc.), but its XLSX currently returns HTTP 403 to automated GitHub runner downloads even with browser-style headers. The aggregate building-permit job succeeds independently; the companion FOI probe remains blocked. Do not treat the missing workbook as evidence either way.

## Toronto 2023–2025 — stable city-level trade permit flow

Source: City of Toronto Open Data, `Building Permits - Active Permits` + `Building Permits - Cleared Permits`.

A reproducible market-research script streams both official CSV resources, reads only permit number/revision/type/work/issued-date, filters to the selected issue year, and deduplicates across Active/Cleared by permit number + revision. It does not emit addresses, project descriptions, applicants, contractors or row-level records.

### Three-year trade-flow stability

| Year | Unique issued permit revisions | Mechanical | Plumbing | Drain & Site Service | Three trade categories combined | Avg combined / month | Combined share |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 37,752 | 7,442 | 8,365 | 4,278 | **20,085** | **1,673.8** | **53.20%** |
| 2024 | 37,451 | 7,435 | 7,939 | 4,639 | **20,013** | **1,667.8** | **53.44%** |
| 2025 | 38,304 | 7,323 | 8,646 | 4,764 | **20,733** | **1,727.8** | **54.13%** |

The combined Mechanical + Plumbing + Drain/Site flow remains tightly clustered around **20k–20.7k issued permit revisions/year**, or roughly **1.67k–1.73k/month**, across all three years.

This is evidence that a Toronto trade-permit workflow has persistent city/platform-level density. It is **not evidence that ProjectPermit's current eight families can serve 1.7k events/month**.

### Why the 1.7k/month number is not current-product SAM

The City `WORK` field exposes the key limitation. In 2024, the largest work labels were:

- `Building Permit Related(PS)`: **7,547**
- `Building Permit Related(MS)`: **7,214**
- `Interior Alterations`: **4,834**
- `Multiple Projects`: **2,844**
- `Building Permit Related (DR)`: **2,468**
- `New Building`: **2,235**
- `Back Water Valve (Sewer only)`: **1,885**

The overwhelming majority of Mechanical/Plumbing/Drain volume is therefore represented by broad `Building Permit Related(...)` labels that do **not** expose enough scope detail to map safely into ProjectPermit's existing families.

ProjectPermit currently has no dedicated general HVAC/electrical/mechanical-service family. `kitchen_bath_plumbing` also must not be treated as equivalent to the entire Toronto Plumbing or Drain permit universe.

Therefore:

> **~1.7k trade revisions/month = workflow-density evidence only, not current addressable call volume.**

Do not use the 20k/year trade series as current ProjectPermit SAM, a paid-call denominator, or evidence supporting an HVAC/electrical expansion.

### Current-family-like WORK-label diagnostic

For a diagnostic only, the research script matches City `WORK` labels that visibly resemble the current project families and leaves ambiguous labels unmapped.

| Year | Non-exclusive current-family-like matched WORK events | Avg/month |
|---:|---:|---:|
| 2023 | **6,695** | **557.9** |
| 2024 | **6,690** | **557.5** |
| 2025 | **7,038** | **586.5** |

2024 diagnostic components were:

| Current family signal | Matched issued revisions |
|---|---:|
| interior_renovation | **4,876** |
| accessory_structure | **542** |
| addition | **523** |
| dwelling_change | **377** |
| deck_porch | **335** |
| basement | **34** |
| window_door | **3** |
| kitchen_bath_plumbing | **0** |

Important limitations:

- the matched count is **non-exclusive diagnostic signal**, not SAM or unique projects;
- `Interior Alterations` dominates the total and is itself much broader than a guaranteed ProjectPermit candidate event;
- keyword/work-label matching can both over-map and under-map edge cases;
- `kitchen_bath_plumbing = 0` only means the City `WORK` labels do not expose kitchen/bath wording in this series; it does **not** prove zero market for that family;
- current-family-like issued events are downstream permit-positive outcomes, not upstream Requests/Quotes where applicability is still uncertain;
- the result gives no candidate/issued multiplier, no address-aware share and no willingness-to-pay evidence.

The most defensible interpretation is therefore:

> Toronto has a stable **~560–587/month issued-workflow diagnostic** visibly resembling current ProjectPermit families, but even this number is not yet a callable preflight denominator.

This is materially smaller than the ~1.7k/month broad MEP trade pool and should be used whenever discussing **current-product fit**.

### 2024 permit-type detail

| Permit type | 2024 issued revisions | Avg/month |
|---|---:|---:|
| Plumbing (PS) | **7,939** | **661.6** |
| Mechanical (MS) | **7,435** | **619.6** |
| Drain and Site Service | **4,639** | **386.6** |
| **Three trade categories combined** | **20,013** | **1,667.8** |
| Building Additions/Alterations | 4,686 | 390.5 |
| Small Residential Projects | 7,529 | 627.4 |
| New Houses | 2,063 | 171.9 |

Toronto Open Data documentation notes that multiple Mechanical and Plumbing permits can be issued with other permit types for the same broader construction project. Permit revisions are therefore workflow events, not unique projects or unique customers.

## Mississauga 2023–2025 — visible sub-trade and dwelling-change signals

Source: City of Mississauga official `Issued_Building_Permits` ArcGIS FeatureServer. The research script uses server-side grouped statistics on `APP_DETAIL` and `ISSUE_DATE`; it does not request row-level addresses, descriptions, applicant or contractor fields.

### Visible trade-focus floor

Focus categories are Plumbing Only + Heating Only + Mechanical Only + Drain Only + Site Servicing.

| Year | Total issued records | Visible trade-focus records | Avg/month | Share of all issued records |
|---:|---:|---:|---:|---:|
| 2023 | 4,333 | **496** | **41.3** | 11.45% |
| 2024 | 4,409 | **709** | **59.1** | 16.08% |
| 2025 | 4,225 | **612** | **51.0** | 14.49% |

2024 focus detail:

- Plumbing Only: **633**
- Site Servicing: **67**
- Heating Only: **7**
- Drain Only: **2**
- Mechanical Only: **0**

Important limitation: most Mississauga records have blank `APP_DETAIL`, and some trade work can be embedded in broader building permits. Therefore 41–59/month is a **visible application-type floor**, not a complete Mississauga mechanical/plumbing universe and not current ProjectPermit SAM.

Do **not** map `PLUMBING ONLY` wholesale into `kitchen_bath_plumbing`: the current family is not equivalent to general plumbing-only permit work.

### Conservative `dwelling_change` signal

Two Mississauga `APP_DETAIL` labels are specific enough to map conservatively to the existing `dwelling_change` family:

- `SECOND UNIT`
- `ADDITIONAL RESIDENTIAL UNITS`

| Year | SECOND UNIT | ADDITIONAL RESIDENTIAL UNITS | Conservative dwelling_change signal | Avg/month |
|---:|---:|---:|---:|---:|
| 2023 | 587 | 134 | **721** | **60.1** |
| 2024 | 6 | 769 | **775** | **64.6** |
| 2025 | 0 | 632 | **632** | **52.7** |

This is still downstream issued-permit activity, not an upstream applicability-decision count. It is simply a cleaner current-family mapping than the broad trade categories.

## Toronto + Mississauga conservative current-family-like signal

Combining only Toronto's existing current-family-like diagnostic with Mississauga's clearly mapped `dwelling_change` labels gives:

| Year | Toronto signal | Mississauga clear dwelling_change | Combined visible signal | Avg/month |
|---:|---:|---:|---:|---:|
| 2023 | 6,695 | 721 | **7,416** | **618.0** |
| 2024 | 6,690 | 775 | **7,465** | **622.1** |
| 2025 | 7,038 | 632 | **7,670** | **639.2** |

This is intentionally **not** extended to Vancouver's 888 residential-renovation records because Vancouver's public labels are too broad for a specific family mapping. Ottawa, Laval, Gatineau and Longueuil are also excluded from this mapped subtotal unless an equivalent clean first-party classification is available.

Interpretation:

> The strongest reproducible current-family-like public signal currently visible across Toronto + Mississauga is only about **618–639 issued workflow events/month**.

That is useful negative discipline for the 10k thesis. It does **not** mean the total seven-city market is only 618–639/month, because public classifications omit/blur many relevant cases and four covered cities are not included. But it does mean we cannot credibly point at broad permit totals and claim the current product already has a 10k/month denominator.

To reach 10k monthly calls with the current family set, ProjectPermit still needs a combination of:

- a materially larger **upstream candidate/issued multiplier** than public issuance counts show;
- aggregation across multiple covered cities/accounts/platforms;
- repeated preflight calls before permit necessity is already known;
- and/or partner evidence that public classification fields substantially undercount current-family candidate work.

None of those multipliers is currently proven.

## External high-volume example

ServiceTitan Marketplace's iPermit listing includes a testimonial from ACTION Air Conditioning / Heating / Solar stating that it sends about **80 or more jobs per month** to iPermit. iPermit also states that it has pulled more than 1 million permits over its history.

This proves that high-volume permit-operations customers exist, but it is one U.S. testimonial and must not be generalized into a Canadian contractor distribution without representative evidence. It also concerns a high-frequency trade mix that ProjectPermit's current project families do not fully cover.

## Commercial implication

The evidence supports three different customer shapes, but current-family coverage must be kept separate from broad trade volume:

1. **Ordinary direct building/renovation contractor** — likely low-to-moderate permit cadence; useful for E3/E4 learning but weak as the primary 10k-call distribution engine.
2. **High-volume HVAC/plumbing/mechanical or multi-branch contractor** — such operators exist, but much of that trade volume is outside or ambiguous relative to ProjectPermit's current eight families. Do not count it as serviceable without explicit partner demand and scope expansion evidence.
3. **Platform / multi-account integration** — still the most credible path to aggregation, but a platform's total trade volume is irrelevant unless a bounded subset maps to current families **and** reaches the workflow before permit necessity is already known.

Accordingly:

- keep `125 × 80/month` only as an **aggressive direct-account scenario**, not a base case;
- keep `20 integrations × 500/month`, `5 × 2,000/month`, and a platform workflow as arithmetic distribution shapes, but require family-fit evidence before calling them reachable;
- prioritize E2/E3/E4 evidence from upstream Request/on-site-assessment/Estimate/Quote workflows rather than downstream permit-filing intake;
- make **Toronto/GTA current-family estimate/quote workflows** the first bounded-volume validation target;
- do not fabricate an Ottawa trade denominator: its public construction/demolition/pool dataset is not equivalent to Toronto's Mechanical/Plumbing permit-type series;
- do not add HVAC/electrical/mechanical families merely because broad trade volume is high;
- do not expand municipalities merely to increase denominator size until a partner/workflow identifies the missing geography.

## Next measurement

The key unresolved metric is now more specific:

`current-family candidate Requests/Assessments/Quotes with unresolved permit applicability / month`

For a partner benchmark, measure:

- candidate Requests/Assessments/Quotes/Jobs per month;
- how many map to one of the current eight project families;
- how many still require permit-applicability research before permit necessity is known;
- how many later become issued permits;
- address-aware share;
- repeated calls per account/integration;
- realized willingness to pay.

A partner exposing **500+ bounded current-family candidate events/month** in covered geographies would be materially stronger evidence than another broad trade-volume estimate.