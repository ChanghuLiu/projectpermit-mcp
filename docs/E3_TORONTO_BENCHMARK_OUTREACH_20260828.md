# Toronto E3 Historical Benchmark Outreach — 2026-08-28

Purpose: add a second-city contractor cohort to the Ottawa historical-case requests so ProjectPermit can test real permit outcomes across municipalities rather than relying on synthetic rule divergence.

## Benchmark request

Each contractor was asked for only:

- 5-10 recent Toronto renovation project types / short scopes;
- actual municipal building-permit outcome: `yes / no / conditional`.

Even 3 cases are accepted as a starter set.

Not requested:

- client names;
- addresses;
- prices;
- drawings;
- permit documents.

The benchmark will compare contractor-reported actual outcome against ProjectPermit's deterministic output and current first-party municipal guidance.

## Targets sent

### Oriel Renovations

Recipient: `info@orielrenovations.com`

RenoMark-verified Toronto renovator/custom home builder. Public scope includes basements, bathrooms, exterior, additions, kitchens and whole-home renovation, with long experience in older Toronto homes.

Public evidence:

- https://renomark.ca/renovator/oriel-renovations/
- https://orielrenovations.com/contact-us

Evidence state: request sent; no qualifying cases received yet.

### Sunnylea Homes

Recipient: `renovate@sunnyleahomes.ca`

RenoMark-listed Toronto/GTA renovator. Public scope includes basement, bathroom, additions, kitchens and whole-home renovation.

Public evidence:

- https://renomark.ca/renovator/sunnylea-homes-ltd/
- https://sunnyleahomes.ca/contact/

Evidence state: request sent; no qualifying cases received yet.

### All Angles Renovations Ltd.

Recipient: `allangles@sympatico.ca`

RenoMark-verified Toronto/GTA renovator. Public scope includes basement, bathroom, exterior, additions and kitchens; company materials describe residential work in older Toronto homes.

Public evidence:

- https://renomark.ca/renovator/all-angles-renovations-ltd/
- https://www.allanglesrenovations.ca/

Evidence state: request sent; no qualifying cases received yet.

## Why Toronto + Ottawa matters

Current first-party guidance already contains a clear municipal differentiation anchor for a basic basement finish:

- Toronto says a house-basement finish can be permit-exempt when there are no structural/material alterations, no new dwelling unit and no new plumbing;
- Ottawa publishes a dedicated basement-finishing permit workflow.

See `docs/MUNICIPAL_RULE_DIFFERENTIATION.md`.

Historical cases can test whether such differences are actually material in representative contractor work rather than merely possible in synthetic examples.

## E3 acceptance rule

Do not call a sample E3 merely because it came from a real contractor.

A useful benchmark set must still be:

- recent enough to reflect current workflow/rules;
- representative rather than intentionally selected edge cases;
- sufficiently described to map to normalized facts without guessing;
- free of duplicates;
- independently checkable against first-party municipal guidance where practical.

Use the existing historical benchmark tooling/runbook to classify disagreements and false-negative risk.

## Evidence state

As of sending on 2026-08-28:

- Toronto contractor targets contacted: **3**;
- historical cases received: **0**;
- countable E3 benchmarks from this cohort: **0**.

No score upgrade is justified until actual cases arrive and pass the benchmark acceptance rules.