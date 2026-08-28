# BuilderAI Laval demo — official-rule spot check (2026-08-28)

## Purpose

Test one public BuilderAI permit/urbanism result against current first-party Ville de Laval guidance. This is a falsification check, not an E3 benchmark: the BuilderAI case is vendor-selected, public, and not an independently sampled historical cohort.

## BuilderAI public demo

BuilderAI publishes a real/anonymized demo for a **10 × 10 ft bathroom renovation in Laval**. The visible scope includes:

- existing bathroom renovation;
- double vanity;
- glass shower;
- heated floor;
- plumbing rough-in / shower and vanity supply work;
- no visible statement that room dimensions, room count, or building structure are being changed.

The demo's urbanism section says it checks Laval zoning before quote delivery and displays:

- `Urbanisme consulté`;
- `Zonage R-1 confirmé — pas de permis requis pour rénovation intérieure`.

It also shows an **indicative excerpt** labelled `Art. 4.2.1` stating, in substance, that interior renovations without modification of footprint or habitable volume do not require a construction permit. BuilderAI explicitly labels the excerpt as indicative and says the in-app urbanism RAG consults the real municipal regulation.

Public source: https://www.builder-ai.ca/demo

## Current Ville de Laval guidance

Ville de Laval's current residential interior renovation/repair page gives a project-type table. It states:

- renovation of an **existing bathroom**: no permit;
- addition of a bathroom: permit required;
- general interior renovation: permit required when **room dimensions, number of rooms, or the structure of the dwelling** are modified;
- basement renovation: permit required when room count or structure changes;
- replacement/renovation of the plumbing system: no permit;
- replacement of an electrical panel: no permit;
- modification of electrical wiring inside walls/ceilings: no permit.

Official source: https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx

The same page notes that plumbing-equipment changes may be part of the required documentation **when a permit application is otherwise required**. That documentation requirement should not be misread as saying every plumbing change independently requires a construction permit.

## Verdict on the demo outcome

### Outcome: plausibly correct

Based on the facts visible in the public demo, BuilderAI's `no permit required` outcome is consistent with Laval's current first-party table **if** this is renovation of an existing bathroom with no change to room dimensions, room count, or building structure.

The visible plumbing rough-in does not, by itself, make the public result incorrect under Laval's current table because replacement/renovation of the plumbing system is explicitly listed as no-permit work.

Therefore ProjectPermit should **not** cite this demo as evidence that BuilderAI gives the wrong permit answer.

## Precision / traceability issue

The public reasoning presentation is coarser than Laval's first-party applicability logic:

- BuilderAI explains the result using an indicative `Art. 4.2.1` excerpt framed around footprint/habitable-volume changes;
- Laval's current public decision table uses a more specific interior-renovation trigger: room dimensions, number of rooms, or structure;
- the exact quoted phrase / article shown in the BuilderAI demo was not located in the current official Laval material during this spot check;
- BuilderAI itself labels that text `extrait indicatif`, so it should not be treated as a verified verbatim municipal citation.

Also, a zoning label such as `R-1` is not by itself what determines whether this ordinary interior bathroom renovation requires a permit; the project-type permit rules matter directly.

This suggests a potential ProjectPermit distinction around **auditable rule provenance and exact decisive facts**, but it does not prove users will pay for that distinction.

## Competitive implication

This check is mildly negative for an `accuracy moat` claim:

- BuilderAI reaches the likely correct answer on a realistic common case;
- a simpler/RAG-style workflow may therefore be good enough for many ordinary jobs;
- ProjectPermit cannot justify itself merely by saying competitor permit guidance is inaccurate.

The remaining thesis must be tested on cases where municipality-specific exceptions, thresholds, property overlays, or missing decisive facts materially change the answer.

## Evidence classification

- BuilderAI public demo: vendor-selected public case, **not E3**.
- Official-rule comparison: technical falsification/competitive evidence only.
- Go/No-Go score: **no change; remains 51/100**.

Competitive headroom is already scored at zero and defensibility remains weak/unproven. A single correctly handled public demo should not be double-counted as a further score penalty.

## Next validation implication

For any representative E3 cohort, track not just raw accuracy but also:

1. whether a simplified city guide/RAG answer would have produced the same result;
2. whether ProjectPermit's extra structured facts changed the answer;
3. whether source-level provenance/rule IDs mattered to the operator;
4. whether any clarification questions were needed to reach the deterministic result.

If ordinary representative cases are overwhelmingly resolved correctly by simpler guidance with little value from deterministic specificity, that should trigger a negative score revision / re-scope review.
