# Trade permit workload evidence

Updated: 2026-08-27

Purpose: separate **single-contractor cadence** from **city/platform trade-permit volume** when evaluating ProjectPermit's path to repeated API calls.

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

The City FOI release 2024-671 includes building and sub-trade permits (mechanical, electrical, plumbing, HVAC, etc.), but its XLSX currently returns HTTP 403 to automated GitHub runner downloads even with browser-style headers. Do not treat the missing workbook as evidence either way.

## Toronto 2023–2025 — stable city-level trade permit flow

Source: City of Toronto Open Data, `Building Permits - Active Permits` + `Building Permits - Cleared Permits`.

A reproducible market-research script streams both official CSV resources, reads only permit number/revision/type/issued-date, filters to the selected issue year, and deduplicates across Active/Cleared by permit number + revision.

### Three-year stability

| Year | Unique issued permit revisions | Mechanical | Plumbing | Drain & Site Service | Three trade categories combined | Avg combined / month | Combined share |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 37,752 | 7,442 | 8,365 | 4,278 | **20,085** | **1,673.8** | **53.20%** |
| 2024 | 37,451 | 7,435 | 7,939 | 4,639 | **20,013** | **1,667.8** | **53.44%** |
| 2025 | 38,304 | 7,323 | 8,646 | 4,764 | **20,733** | **1,727.8** | **54.13%** |

The combined Mechanical + Plumbing + Drain/Site flow remains tightly clustered around **20k–20.7k issued permit revisions/year**, or roughly **1.67k–1.73k/month**, across all three years.

This makes the 2024 observation a structural workflow-volume signal rather than a one-year spike.

### 2024 detail

| Permit type | 2024 issued revisions | Avg/month |
|---|---:|---:|
| Plumbing (PS) | **7,939** | **661.6** |
| Mechanical (MS) | **7,435** | **619.6** |
| Drain and Site Service | **4,639** | **386.6** |
| **Three trade categories combined** | **20,013** | **1,667.8** |
| Building Additions/Alterations | 4,686 | 390.5 |
| Small Residential Projects | 7,529 | 627.4 |
| New Houses | 2,063 | 171.9 |

Toronto Open Data documentation notes that multiple Mechanical and Plumbing permits can be issued with other permit types for the same broader construction project. Therefore permit revisions are workflow events, not unique projects or unique customers.

Interpretation: Toronto provides strong evidence that trade-permit workflow volume is large and persistent at the **city/platform level**, even though Vancouver building-permit data suggests ordinary direct contractor cadence is much lower than 80/month.

## Mississauga 2023–2025 — visible sub-trade floor

Source: City of Mississauga official `Issued_Building_Permits` ArcGIS FeatureServer. The research script uses server-side grouped statistics on `APP_DETAIL` and `ISSUE_DATE`; it does not request row-level addresses, descriptions, applicant or contractor fields.

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

Important limitation: most Mississauga records have blank `APP_DETAIL`, and some trade work can be embedded in broader building permits. Therefore 41–59/month is a **visible application-type floor**, not a complete Mississauga mechanical/plumbing universe.

Even with that limitation, the comparison reinforces that the cleanest measured high-density trade-event pool is Toronto rather than an even distribution across covered Ontario municipalities.

## External high-volume example

ServiceTitan Marketplace's iPermit listing includes a testimonial from ACTION Air Conditioning / Heating / Solar stating that it sends about **80 or more jobs per month** to iPermit. iPermit also states that it has pulled more than 1 million permits over its history.

This proves that high-volume permit-operations customers exist, but it is one U.S. testimonial and must not be generalized into a Canadian contractor distribution without representative evidence.

## Commercial implication

The evidence now supports three different customer shapes:

1. **Ordinary direct building/renovation contractor** — likely low-to-moderate permit cadence; useful for E3/E4 learning but weak as the primary 10k-call distribution engine.
2. **High-volume HVAC/plumbing/mechanical or multi-branch contractor** — plausible, and the iPermit example proves such outliers exist, but explicit Canadian cadence evidence is still required before assuming 80+/month.
3. **Platform / permit-operations / multi-account integration** — currently the most credible path to 500, 2,000 and 10,000+ repeated monthly calls because it aggregates many contractor workflows. Toronto alone shows roughly 1.7k monthly trade-permit workflow events after issuance; an upstream platform sees a broader candidate pool than issued permits, but that multiplier remains unmeasured.

Accordingly:

- keep `125 × 80/month` only as an **aggressive direct-account scenario**, not a base case;
- keep `20 integrations × 500/month`, `5 × 2,000/month`, and a platform workflow as primary distribution shapes;
- prioritize E2/E3/E4 evidence from integrations, permit-operations vendors, consultants, and high-volume HVAC/plumbing operators over ordinary one-city general contractors;
- make **Toronto/GTA estimate/quote workflows** the first bounded-volume validation target; Toronto's measured issued trade-event density is much higher than the visible Mississauga sub-trade floor;
- do not fabricate an Ottawa trade denominator: its public construction/demolition/pool dataset is not equivalent to Toronto's Mechanical/Plumbing permit-type series;
- do not expand municipalities merely to increase denominator size until a partner/workflow identifies the missing geography.

## Next measurement

The key unresolved metric is still:

`candidate permit-applicability decisions / issued permit`

For a partner benchmark, measure:

- candidate Requests/Quotes/Jobs per month;
- how many trigger permit-applicability research before a permit is known to be required;
- how many become issued permits;
- address-aware share;
- repeated calls per account/integration;
- realized willingness to pay.

A partner exposing **500+ bounded candidate events/month** in covered geographies now matters more than collecting additional broad market-size estimates.