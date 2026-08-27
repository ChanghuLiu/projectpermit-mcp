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

## Toronto 2024 — city-level trade permit flow

Source: City of Toronto Open Data, `Building Permits - Active Permits` + `Building Permits - Cleared Permits`.

A reproducible market-research script streams both official CSV resources, reads only permit number/revision/type/issued-date, filters to 2024 issued records, and deduplicates across Active/Cleared by permit number + revision.

Observed 2024 unique issued permit revisions: **37,451**.

| Permit type | 2024 issued revisions | Avg/month |
|---|---:|---:|
| Plumbing (PS) | **7,939** | **661.6** |
| Mechanical (MS) | **7,435** | **619.6** |
| Drain and Site Service | **4,639** | **386.6** |
| **Three trade categories combined** | **20,013** | **1,667.8** |
| Building Additions/Alterations | 4,686 | 390.5 |
| Small Residential Projects | 7,529 | 627.4 |
| New Houses | 2,063 | 171.9 |

The three trade categories alone represent about **53.4%** of Toronto's 2024 unique issued permit revisions in this combined dataset.

Toronto Open Data documentation also notes that multiple Mechanical and Plumbing permits can be issued with other permit types for the same broader construction project. Therefore permit revisions are workflow events, not unique projects or unique customers.

Interpretation: Toronto provides strong evidence that trade-permit workflow volume is large at the **city/platform level**, even though Vancouver building-permit data suggests ordinary direct contractor cadence is much lower than 80/month.

## External high-volume example

ServiceTitan Marketplace's iPermit listing includes a testimonial from ACTION Air Conditioning / Heating / Solar stating that it sends about **80 or more jobs per month** to iPermit. iPermit also states that it has pulled more than 1 million permits over its history.

This proves that high-volume permit-operations customers exist, but it is one U.S. testimonial and must not be generalized into a Canadian contractor distribution without representative evidence.

## Commercial implication

The evidence now supports three different customer shapes:

1. **Ordinary direct building/renovation contractor** — likely low-to-moderate permit cadence; useful for E3/E4 learning but weak as the primary 10k-call distribution engine.
2. **High-volume HVAC/plumbing/mechanical or multi-branch contractor** — plausible, but requires explicit cadence evidence before assuming 80+/month.
3. **Platform / permit-operations / multi-account integration** — currently the most credible path to 500, 2,000 and 10,000+ repeated monthly calls because it aggregates many contractor workflows.

Accordingly:

- keep `125 × 80/month` only as an **aggressive direct-account scenario**, not a base case;
- keep `20 integrations × 500/month`, `5 × 2,000/month`, and a platform workflow as primary distribution shapes;
- prioritize E2/E3/E4 evidence from integrations, permit-operations vendors, consultants, and high-volume HVAC/plumbing operators over ordinary one-city general contractors;
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
