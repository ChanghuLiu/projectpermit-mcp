# Covered-market call sensitivity

Updated: 2026-08-27

Purpose: keep three different quantities separate when evaluating ProjectPermit:

1. **Issued permits** — downstream observed municipal activity.
2. **External preflight calls** — upstream candidate jobs/scopes evaluated by ProjectPermit.
3. **Paid address-aware calls** — the subset that reaches the monetizable address/GIS path under the current working pricing hypothesis.

These are not interchangeable.

## Same-year observed permit floor

Previously established first-party 2024 issuance counts:

- Toronto: 36,887
- Ottawa: 7,688
- Mississauga: 4,458
- Laval: 1,415 construction/improvement permits

Subtotal: **50,448/year**.

City of Vancouver's December 2025 construction-activity statement reports, in the comparison column for **2024**, a building-permit subtotal of **3,705** permits (excluding demolition and salvage/abatement rows).

Source: https://vancouver.ca/files/cov/statement-of-building-permits-issued-dec-2025.pdf

Adding Vancouver gives a clean same-year observed floor of:

- **54,153 issued permits/year**
- **4,512.75 issued permits/month**

This still excludes Gatineau and Longueuil from the exact cumulative floor rather than guessing their counts.

The current Vancouver run rate is not materially larger: the City's July 2026 statement reports **1,991 building permits YTD through July 2026**, or about **284/month** for the first seven months.

Source: https://vancouver.ca/files/cov/statement-of-building-permits-issued-jul-2026.pdf

## Candidate-preflight multiplier needed for 10k total calls

Let `M` be candidate preflights per observed issued permit.

Using the 4,512.75/month observed issuance floor:

| Candidate / issued multiplier | Implied external preflights/month |
|---:|---:|
| 1.0x | 4,513 |
| 1.5x | 6,769 |
| 2.0x | 9,026 |
| 2.22x | ~10,019 |
| 3.0x | 13,538 |
| 5.0x | 22,564 |

Therefore the current seven-city footprint does **not** require an implausibly huge top-of-funnel multiplier merely to reach 10,000 total preflights/month. A multiplier of roughly **2.22x** over the clean observed issuance floor would be enough.

However, this is only a sensitivity calculation. We do not yet have an external measurement of how many candidate quotes/work orders are checked before a permit is known to be required.

## Total external calls are not paid calls

The current working commercial hypothesis is approximately **$0.20-$0.50 per address-aware evidence-linked preflight**. The free structured/no-address validation path exists specifically to reduce evaluation friction.

Therefore `10,000 external preflights/month` must not be converted directly into revenue unless the paid/address-aware share is known.

At exactly 10,000 total external preflights/month:

| Paid address-aware share | Paid calls/month | Gross @ $0.25 | Gross @ $0.50 |
|---:|---:|---:|---:|
| 30% | 3,000 | $750 | $1,500 |
| 50% | 5,000 | $1,250 | $2,500 |
| 70% | 7,000 | $1,750 | $3,500 |
| 100% | 10,000 | $2,500 | $5,000 |

So the old shortcut `10k external calls -> $2.5k-$5k/month` is valid only if essentially all 10k calls are monetized at the address-aware price.

## Total calls required for 10k paid calls

| Paid share | Total external calls required for 10k paid | Candidate / issued multiplier vs 4,512.75 monthly floor |
|---:|---:|---:|
| 30% | ~33,333 | ~7.39x |
| 50% | 20,000 | ~4.43x |
| 70% | ~14,286 | ~3.17x |
| 100% | 10,000 | ~2.22x |

This is the more useful commercial sensitivity table.

## Revised validation gates

Track both metrics independently:

### Distribution gate

- **10,000 external successful preflights/month** remains a useful first proof that ProjectPermit can occupy a repeated workflow.

### Monetization gate

- Separately measure `paid_address_aware_share`.
- Do not call the business economically validated merely because total external calls reach 10k.
- A stronger commercial checkpoint is either:
  - **10,000 paid address-aware calls/month**, or
  - a lower paid-call volume with demonstrated pricing/revenue sufficient to justify rule-maintenance cost.

The target should eventually be expressed as:

`external preflights x paid share x realized price - maintenance/infra cost`

rather than raw call count alone.

## What evidence is still missing

The next partner evidence should explicitly measure:

- candidate jobs/scopes per month;
- fraction for which permit applicability is not already known;
- fraction needing address/property/GIS context;
- fraction where the result changes routing, quote, scheduling or submission behavior;
- willingness to pay for the address-aware result;
- municipality mix.

Until those are observed, 2.22x, 3x, 5x and the paid-share percentages above are scenario variables, not forecasts.
