# Municipal Permit Activity Baseline

Updated: 2026-08-27

Purpose: establish an objective activity floor for ProjectPermit's currently supported geography without relying on partner replies, platform TAM claims, or subjective pain estimates.

This is **not** an API-call forecast. Issued permits measure completed permit activity; ProjectPermit is intended to run earlier on a broader set of candidate jobs, including jobs that ultimately do not need a permit. The relationship between `issued permits` and `candidate preflight calls` must be measured from real workflows.

## Confirmed municipal activity

| Jurisdiction | Objective activity signal | Period | Approx monthly equivalent | Source quality |
|---|---:|---|---:|---|
| Toronto | **36,887 building permits issued** | 2024 actual | **3,074/mo** | City of Toronto 2026 Operating Budget Notes |
| Ottawa | **7,688 building permits issued** | 2024 actual | **641/mo** | City of Ottawa 2024 Annual Report |
| Mississauga | **4,458 building permits issued** | 2024 | **372/mo** | Open Data Mississauga building-permit dataset summary |
| Vancouver | **51,068 issued-building-permit records since 2017** | 2017–2026 dataset stock | not converted to annual rate here | City of Vancouver Open Data |

For the three jurisdictions with a clean 2024 annual count, the combined observed issuance volume is:

- **49,033 permits/year**
- **~4,086 permits/month**

This is an activity floor, not addressable ProjectPermit calls.

## Vancouver scope signal

Vancouver's current issued-building-permits dataset contains roughly 51,068 records since 2017. The portal exposes a `PermitCategory` specifically intended to group higher-volume/lower-complexity project scopes, which is unusually relevant to ProjectPermit's wedge.

The current table shows **25,130 Addition / Alteration records**, about **49.2%** of the dataset. This is evidence that a large share of real permitting activity is not just ground-up construction. The dataset also contains project descriptions, property use, specific-use category, contractor and issue dates, making it a strong source for future historical benchmark construction.

Do not interpret 25,130 as 25,130 ProjectPermit-compatible cases. The current eight project families cover only a subset, and one project may require multiple permits.

## Important implication for the 10,000-calls/month target

The currently confirmed 2024 issuance flow for Toronto + Ottawa + Mississauga is only about **4,086 issued permits/month**. Therefore a commercial path to 10,000 monthly API calls cannot be based on the simplistic model:

`one ProjectPermit call only when a permit is already known to be required`.

The intended product must instead prove an earlier, broader workflow such as:

`every relevant quote/work order/project scope -> preflight -> only required/uncertain cases escalate`.

That is exactly why Jobber/property-maintenance/field-service distribution matters. The preflight call surface can be larger than issued-permit volume if businesses need to screen many candidate jobs, including jobs that do not require permits.

But that multiplier is currently **unknown**. It must come from E2/E3/E4 workflow evidence rather than assumption.

## What would falsify the current business model

If real contractor/operator samples show that:

- permit applicability is obvious from trade knowledge for nearly every candidate job;
- only jobs already known to require permits are ever researched;
- ambiguous cases are rare;
- and one permit decision often covers many downstream work objects,

then the candidate-preflight multiplier may be near 1x or below issued-permit activity. In that case the current Canadian-only footprint is unlikely to support large API-call volume without major geographic expansion or a different workflow layer.

## What would strengthen it

The model becomes stronger if historical work-order/quote data shows, for example, that businesses screen several relevant candidate jobs for each ultimately issued permit, and that the screening decision changes quoting, scheduling, dispatch, or escalation.

The key empirical metric is therefore:

`candidate permit-decision work objects / ultimately permit-positive work objects`

Measure this per trade, platform and municipality. Do not assume one universal multiplier.

## Next objective-data work

1. Build annual/monthly permit-issuance series for Vancouver from its first-party API.
2. Extract project-family-compatible scope counts from Vancouver's `PermitCategory`, `TypeOfWork` and `ProjectDescription` fields.
3. Obtain Ottawa monthly Construction/Demolition/Pool data and deduplicate by permit number because one permit may appear at multiple addresses.
4. Find comparable first-party annual/scope data for Gatineau, Laval and Longueuil.
5. Compare observed municipal permit activity against E3/E4 contractor workflow data to estimate the candidate-preflight multiplier.

## Sources reviewed 2026-08-27

- Toronto 2026 Operating Budget Notes — 2024 actual building permits issued: https://www.toronto.ca/legdocs/mmis/2026/bu/bgrd/backgroundfile-261720.pdf
- Toronto Open Data — active/cleared permit datasets and daily refresh context: https://open.toronto.ca/dataset/building-permits-active-permits/ and https://open.toronto.ca/dataset/building-permits-cleared-permits/
- Ottawa 2024 Annual Report — 7,688 building permits issued: https://documents.ottawa.ca/sites/default/files/EN%20-%202024%20Annual%20Report.pdf
- Ottawa Construction/Demolition/Pool permit dataset description: https://www.arcgis.com/home/item.html?id=429ea52d2ff040c799afde2b40b90f68
- Mississauga Building Permits summary: https://opendatamississauga.ca/building-permits
- Vancouver Issued Building Permits: https://opendata.vancouver.ca/explore/dataset/issued-building-permits/
