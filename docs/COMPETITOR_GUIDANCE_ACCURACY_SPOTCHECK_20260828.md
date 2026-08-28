# Competitor Permit-Guidance Accuracy Spot Check — 2026-08-28

## Purpose

Test the narrower differentiation hypothesis that Canadian renovation/quote platforms can easily publish useful permit guidance, but may lose municipality-specific exceptions when they compress rules into generic guides, calculators or AI-estimate assumptions.

This is a **small public-source diagnostic**, not a representative E3 benchmark and not proof that any competitor is broadly inaccurate.

The current spot check compares selected public QuoteXbert / RealCraft statements against the City of Toronto's current first-party permit guidance.

## Current first-party baseline

Toronto's current `When Do I Need a Building Permit?` page was modified July 21, 2026.

Source:

- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

Relevant current Toronto rules include:

- a house basement finish is permit-exempt when there are no structural/material alterations, no additional dwelling unit and no new plumbing;
- a shed is permit-exempt when it is no more than 15 m², one storey, detached, storage-only and without plumbing;
- a low uncovered platform/deck can be permit-exempt when its finished level is not more than 60 cm above adjacent grade, subject to the rest of the stated conditions;
- enlarging/relocating a window or door opening is permit-required, while the City's guidance distinguishes replacement work in small residential buildings from new/enlarged openings.

## Case 1 — clean basement finish

### QuoteXbert public guidance

QuoteXbert's current basement calculator states:

> `Basement finishing requires permits in all Ontario municipalities.`

Its 2026 Ontario basement-permit guide similarly says basement work with framing/insulation generally requires a permit and describes only purely cosmetic paint/flooring as the exception.

Sources:

- https://www.quotexbert.com/basement-renovation-calculator
- https://www.quotexbert.com/do-i-need-permits-to-finish-my-basement-ontario

### Toronto current rule

Toronto explicitly exempts finishing a house basement when all three conditions are satisfied:

- no structural/material alteration;
- no additional dwelling unit;
- no new plumbing.

### Diagnostic result

**Material overgeneralization / potential false-positive routing.**

A normalized Toronto project such as:

`existing single-dwelling house + basement finish + no structural/material alterations + no added unit + no new plumbing`

can be `LIKELY_NOT_REQUIRED` / permit-exempt under Toronto's current guidance even though a generic Ontario statement says basement finishing always needs a permit.

This is a strong example of why province-wide text should not overwrite municipality-specific exemptions.

## Case 2 — detached storage shed between 10 and 15 m²

### QuoteXbert public Toronto guide

QuoteXbert's current Toronto addition/permit guide says permits are required for new structures such as a detached garage or **shed over 10 m²**, and lists `sheds under 10 m²` among generally permit-exempt work.

Source:

- https://www.quotexbert.com/blog/toronto-home-addition-permits-guide

### Toronto current rule

Toronto's current first-party page separately distinguishes:

- **shed:** permit required at 15 m² or more; under 15 m² can be exempt when one storey, detached, storage-only and no plumbing;
- other accessory structures such as detached garages/workshops/carports/pool houses: the page uses a 10 m² threshold.

### Diagnostic result

**Material category-collapse / overconservative threshold for a qualifying shed.**

A 12 m² one-storey detached storage-only shed with no plumbing can fall inside Toronto's explicit shed exemption even though a simplified `shed >10 m²` rule would route it permit-positive.

This is exactly the type of project-family/subtype distinction a deterministic fact model can preserve.

## Case 3 — deck height around 600 mm

### QuoteXbert public guidance

QuoteXbert's current Ontario deck calculator says decks attached to the house or over 24 inches high need a permit.

Source:

- https://www.quotexbert.com/deck-calculator

### Toronto current rule

Toronto's current public page gives a permit exemption for an uncovered platform when its finished level is not more than 60 cm (24 inches) above adjacent finished grade, subject to the stated conditions.

### Diagnostic result

**Broadly aligned at the height threshold.**

This is important because the spot check should not be interpreted as `competitor guidance is generally wrong`. Some common thresholds are captured reasonably well in simplified guidance.

## Case 4 — RealCraft Toronto basement summary

### RealCraft public guidance

RealCraft's Toronto permit guide currently summarizes basement finishing as usually permit-required when it adds habitable space.

Source:

- https://realcraft.ca/permits/ontario/toronto/

### Toronto current rule

Toronto's current first-party exemption is conditional on structural/material alterations, additional dwelling unit and new plumbing rather than merely whether the basement becomes habitable finished space.

### Diagnostic result

**Less precise than the current municipality-specific condition set.**

This does not establish an outright wrong answer for every RealCraft basement scenario. It shows that `habitable space` alone is a coarser decision feature than Toronto's currently published exemption conditions.

## What this spot check supports

The public evidence supports a narrower technical thesis:

> A platform can cheaply create helpful permit content, but accurate routing can require municipality-specific subtype thresholds and conjunctive exceptions that are easy to flatten in generic prose, calculators or RAG summaries.

Potential ProjectPermit value is therefore not `we know permits exist`.

It is:

1. normalized facts instead of broad project labels;
2. municipality-specific exceptions and thresholds;
3. deterministic/reproducible routing;
4. stable evidence/rule identifiers;
5. source-change maintenance;
6. conservative unknown handling rather than blanket yes/no statements.

## What this does NOT prove

This diagnostic does not prove:

- ProjectPermit is more accurate on a representative project distribution;
- QuoteXbert or RealCraft produce these exact statements inside every live estimate;
- the public pages reflect private/internal decision logic;
- contractors/platforms care enough about these differences to pay;
- overconservative permit-positive routing causes material economic harm;
- ProjectPermit's current rules contain no errors.

Therefore it does **not** upgrade E3, E4, E5 or the Go/No-Go score.

## Commercial falsification test

The next buyer-side question is now more specific:

> When a platform already has project type, city, scope and sometimes photos, is avoiding municipality-specific false positives/false negatives important enough to buy a maintained deterministic capability instead of publishing a simplified guide or maintaining rules internally?

The 2026-08-28 QuoteXbert outreach asks precisely this build-vs-buy question and also requests a bounded Toronto + Mississauga recent-month current-family denominator.

## E3 requirement

A real upgrade requires representative external cases, not cherry-picked competitor pages.

For each independent historical case record:

- normalized scope facts;
- municipality;
- actual permit outcome;
- ProjectPermit output;
- first-party rule/source;
- false-positive / false-negative / confirmation classification;
- whether a generic guide would have routed differently;
- whether that difference mattered operationally.

Only then can `deterministic precision` move from a plausible differentiator to externally validated defensibility.