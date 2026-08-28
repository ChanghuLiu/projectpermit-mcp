# Competitor Guidance Accuracy Spot Check — Expanded Addendum — 2026-08-28

This addendum extends `docs/COMPETITOR_GUIDANCE_ACCURACY_SPOTCHECK_20260828.md` with additional public QuoteXbert/Toronto comparisons.

## Expanded result

The broader public spot check does **not** support claiming that competitor permit guidance is broadly inaccurate.

Observed pattern:

| Scope boundary | Public guidance vs Toronto current rule | Result |
|---|---|---|
| Clean basement finish | QuoteXbert says basement finishing requires permits across Ontario; Toronto has a three-condition exemption | Material specificity gap |
| Qualifying detached storage shed 10–<15 m² | QuoteXbert Toronto guide uses a >10 m² shed threshold; Toronto has a qualifying shed exemption below 15 m² | Material subtype/threshold gap |
| Deck around 600 mm | QuoteXbert uses >24 in / attachment logic; Toronto uses a <=60 cm exemption subject to conditions | Broadly aligned |
| Bathroom same-location fixtures vs moved plumbing | QuoteXbert distinguishes cosmetic/same-location work from moved/new plumbing | Broadly aligned |
| Kitchen cosmetic work vs structural/plumbing changes | QuoteXbert distinguishes ordinary finish/layout work from structural/plumbing changes | Broadly aligned |
| Same-size window vs changed opening | QuoteXbert distinguishes like-for-like replacement from new/enlarged opening work | Broadly aligned |
| RealCraft Toronto basement summary | `habitable space` wording is coarser than Toronto's three-condition exemption | Less precise / needs facts |

## Sources

Toronto current first-party baseline:

- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

QuoteXbert public material:

- https://www.quotexbert.com/basement-renovation-calculator
- https://www.quotexbert.com/do-i-need-permits-to-finish-my-basement-ontario
- https://www.quotexbert.com/blog/toronto-home-addition-permits-guide
- https://www.quotexbert.com/deck-calculator
- https://www.quotexbert.com/bathroom-renovation-permits-ontario
- https://www.quotexbert.com/ontario-renovation-cost-guide
- https://www.quotexbert.com/kitchen-renovation-calculator

RealCraft:

- https://realcraft.ca/permits/ontario/toronto/

## Revised interpretation

Reject the strong claim:

> Generic/AI permit guidance is broadly inaccurate, therefore ProjectPermit has a large accuracy moat.

The public evidence does not support it.

The narrower hypothesis remains plausible:

> Simplified guidance gets many common boundaries right, while municipality-specific exceptions, subtype thresholds and conjunctive conditions can still be flattened and create edge-case routing errors.

Therefore ProjectPermit's potential differentiator is not generic permit knowledge. It is:

- normalized project facts;
- municipality-specific exceptions/subtypes;
- deterministic reproducibility;
- stable evidence/rule IDs;
- source-change maintenance;
- conservative unknown handling.

## Commercial implication

This remains **unproven defensibility**.

A buyer can rationally decide that simplified guidance is `good enough`, that false positives are cheap to confirm manually, or that internal maintenance costs less than another API.

Representative E3 must establish that the municipality-specific edge conditions:

1. occur often enough in real work;
2. change workflow decisions often enough;
3. matter economically enough;
4. are handled materially better by ProjectPermit.

Until then:

- no Go/No-Go score increase;
- no E3 upgrade;
- no claim of broad competitor-accuracy superiority.