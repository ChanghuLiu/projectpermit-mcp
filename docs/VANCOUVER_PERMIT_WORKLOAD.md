# Vancouver anonymous permit-workload evidence

Updated: 2026-08-27

Purpose: test whether ProjectPermit's direct-account call-volume scenarios resemble observed municipal permit workload, without collecting or publishing contractor identities.

## Source and privacy boundary

Source: City of Vancouver Open Data, `issued-building-permits`.

Dataset:
https://opendata.vancouver.ca/explore/dataset/issued-building-permits/

Reproducible aggregate runner:

```bash
python market_research/vancouver_contractor_permit_workload.py
```

The runner requests only:

- permit number;
- year-month;
- type of work;
- permit category;
- building-contractor field.

It does **not** request applicant, civic address, applicant address or contractor address. Contractor strings exist only in runner memory. Output contains no contractor names, row-level records, addresses or hashes.

Reference year: **2024**, using the City's static prior-year extract.

## Permit-universe clarification

The City publishes multiple permit-count universes.

The official December 2025 construction-activity statement reports for 2024:

- building-permit **SUB TOTAL: 3,705**;
- after demolition plus salvage/abatement, **TOTAL: 4,919**.

The Open Data `issued-building-permits` 2024 extract contains **4,907 records**, which is close to the broader official total rather than the 3,705 construction subtotal.

Therefore the earlier 3,705 figure was not a broken count; it represented the narrower construction subtotal. Do not mix it with the broader Open Data record universe without labeling the scope.

## Anonymous 2024 workload — all issued-building-permit records

Observed records: **4,907**.

For contractor strings that look corporate/business-like after conservative normalization:

- permits with usable corporate-like contractor token: **2,840**;
- anonymous corporate-like contractor tokens: **944**;
- median: **1 permit/year**;
- p90: **6/year**;
- p95: **10/year**;
- p99: **25/year**;
- maximum: **47/year**;
- maximum observed for any one contractor token in a single month: **8**.

Annual corporate-like contractor counts at thresholds:

| Annual issued permits | Contractors at or above |
|---:|---:|
| 5 | 145 |
| 10 | 48 |
| 12 | 39 |
| 20 | 16 |
| 24 | 10 |
| 40 | 4 |
| 60 | 0 |
| 80 | 0 |
| 120 | 0 |

Permit concentration among corporate-like tokens:

- top 1: **1.65%** of contractor-attributed permits;
- top 5: **7.50%**;
- top 10: **12.61%**;
- top 25: **22.71%**;
- top 50: **33.35%**.

This is not an ultra-concentrated market where a tiny handful of general building contractors each pull hundreds of City building permits per year.

## Addition / Alteration workload

The Open Data dataset contains **2,544** 2024 `Addition / Alteration` records.

Corporate-like contractor cohort:

- contractor-attributed permits: **928**;
- anonymous contractor tokens: **468**;
- median: **1/year**;
- p90: **4/year**;
- p95: **6/year**;
- p99: **14/year**;
- maximum: **35/year**;
- maximum in any one month: **8**.

Annual thresholds:

| Addition/alteration permits/year | Contractors at or above |
|---:|---:|
| 5 | 37 |
| 10 | 10 |
| 12 | 8 |
| 20 | 4 |
| 24 | 1 |
| 40 | 0 |

## Residential renovation workload

The `PermitCategory` residential-renovation scope contains **888** 2024 records.

Corporate-like contractor cohort:

- contractor-attributed permits: **303**;
- anonymous contractor tokens: **204**;
- median: **1/year**;
- p90: **2/year**;
- p95: **3/year**;
- p99: **8/year**;
- maximum: **20/year**;
- maximum in any one month: **5**.

Only:

- 8 corporate-like tokens reached 5+ residential-renovation permits/year;
- 2 reached 10+;
- 1 reached 12+;
- 1 reached 20+.

## Commercial implication

This is meaningful **negative evidence** against treating:

> `125 direct contractors × 80 preflights/month`

as a routine direct-customer shape for general building/renovation contractors inside one municipality.

Within Vancouver City building permits, even the busiest anonymous corporate-like token observed only **47 issued permits in the full year**, and the busiest addition/alteration token had **35**.

However, an issued permit is downstream of ProjectPermit's target decision. This analysis does **not** establish the ratio:

`candidate jobs requiring permit research / issued permits`.

A direct contractor could have many more quotes/work orders than issued permits. Also, a contractor may work across multiple municipalities.

Therefore the evidence changes the model as follows:

- **125 × 80/month direct accounts:** aggressive; must be proven rather than used as a default shape.
- **400 × 25/month direct accounts:** still requires strong upstream candidate-job multiplier evidence.
- **platform / multi-account / multi-jurisdiction integrations:** remain the preferred path to 10k external preflights/month.

## Important sub-trade limitation

The `issued-building-permits` dataset is not sufficient to evaluate the highest-frequency HVAC, plumbing, electrical and mechanical permit workflows.

The City separately released FOI records covering **building and sub-trade permits (mechanical, electrical, plumbing, HVAC, etc.)**. That source is the next workload test because the public 80+ permits/month evidence in the broader market comes primarily from high-frequency field-service trades rather than general renovation building permits.

Do not generalize the Vancouver building-permit distribution to HVAC/plumbing/electrical until the sub-trade source is analyzed.

## Evidence boundary

This is public, aggregate technical market evidence only.

It is **not**:

- E2 workflow-frequency evidence from a partner;
- E3 representative historical ProjectPermit accuracy evidence;
- E4 external ProjectPermit usage;
- E5 willingness to pay.

E4 remains **0**.
