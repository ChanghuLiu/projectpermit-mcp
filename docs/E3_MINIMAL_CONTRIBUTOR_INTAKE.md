# Minimal E3 contributor intake

This is the low-friction intake format for an external builder, remodeler, contractor, permit professional or integration consultant who is willing to provide anonymized historical cases for a ProjectPermit accuracy benchmark.

The contributor should **not** fill out `data/historical_benchmark_template.csv`. That larger file is ProjectPermit's internal analysis record after the submitted cases have been normalized and benchmarked.

## What to send

A useful batch contains **5–20+ recent, representative cases**. Prefer one of:

- consecutive projects from a stated recent period;
- a random sample from a stated recent period; or
- every relevant project from one recent complete month.

Please do not select only unusual cases, only permit-required cases, or cases chosen because the expected answer is obvious.

For the batch, provide once:

- approximate sample window, for example `2026-07-01 to 2026-07-31`;
- sampling method: `consecutive`, `random`, or `all relevant cases in period`;
- source workflow/platform if useful, for example `Buildertrend`, `JobTread`, `Jobber`, `Property Meld`, or `manual estimating`.

For each case, only five fields are needed:

| Field | Example | Notes |
|---|---|---|
| `case_id` | `CASE-001` | Contributor-created anonymous identifier. |
| `municipality` | `Toronto` | City only; no street address. |
| `scope_summary` | `Rear two-storey addition` | Enough scope detail to reproduce the permit decision. |
| `final_permit_outcome` | `required` | Use `required`, `not_required`, or `confirmation_only`. |
| `outcome_source` | `permit_issued` | Examples: `permit_issued`, `municipal_confirmation`, `historical_project_record`, `other`. |

A ready-to-copy CSV is in `data/e3_minimal_contributor_template.csv`.

## Privacy boundary

Do **not** send:

- customer/client names;
- exact civic addresses or unit numbers;
- emails or phone numbers;
- invoice/contract values;
- permit drawings or private project documents;
- internal account IDs or other identifiers that could be tied back to a customer.

If property-specific context materially changed the historical answer, describe only the derived non-identifying fact, for example `heritage-designated`, `corner lot`, or `secondary suite already existed`. Do not provide the address.

## Scope detail examples

Good scope summaries include the fact that drove the decision, for example:

- `Finish basement; no new plumbing; no second unit; no structural changes`
- `Convert basement to second dwelling unit and add kitchen plumbing`
- `Remove load-bearing wall between kitchen and dining room`
- `Build rear deck 900 mm above grade`
- `Replace existing window same size with no structural change`
- `Enlarge existing window opening`
- `Detached 18 m² storage shed with no plumbing`
- `Move kitchen sink and add new drain/vent connection`

Avoid descriptions that are too vague to reproduce, such as `renovation`, `repair`, or `kitchen job` without the decision-driving details.

## What ProjectPermit does with the batch

ProjectPermit will:

1. normalize each anonymous scope into the existing structured project facts;
2. run the deterministic ruleset for the stated municipality;
3. compare the ProjectPermit determination with the historical outcome;
4. identify agreement, material disagreement, false `LIKELY_NOT_REQUIRED` outcomes and cases where more information should have been requested;
5. report only aggregate benchmark results unless the contributor explicitly wants case-level feedback.

A contributor reply or positive opinion is not treated as demand evidence. A batch counts toward E3 only when the cases are sufficiently representative and reproducible under `docs/VALIDATION_EVIDENCE_STANDARD.md`.
