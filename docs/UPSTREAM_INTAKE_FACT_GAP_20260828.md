# Upstream intake fact-gap analysis — 2026-08-28

## Question

Can ProjectPermit run as a low-friction preflight directly from the information that Canadian quote/lead platforms already collect, or would it require substantial extra intake?

This matters because a large upstream funnel is not useful if deterministic permit applicability requires too many additional questions before every call.

## ProjectPermit's current normalized fact surface

The request schema supports project-family-specific facts such as:

- structural/material alteration;
- wall/opening changes;
- new or moved plumbing;
- dwelling-unit changes;
- deck height, area, attachment and covered/access status;
- accessory-structure area, type, storeys, plumbing/heating, permanence, use, yard and lot-line distance;
- like-for-like window/door replacement vs a new/enlarged opening;
- property overlays such as heritage/PIIA/zoning where available.

Source: `schemas/request.schema.json`.

## HomeStars public intake

Public HomeStars workflow:

1. homeowner selects/describes a job;
2. pictures and project information can be attached;
3. HomeStars matches the lead to relevant pros;
4. pros respond and quote before the homeowner selects whom to contact.

Current public lead examples include permit-sensitive scopes such as:

- a large new skylight/opening in a flat roof;
- complete bathroom renovation with fixture/plumbing work;
- moving/re-roofing an existing shed with dimensions and easement context;
- larger general renovation/interior projects.

However, the publicly visible lead layer does not consistently expose all facts needed for a deterministic municipal decision. Examples of potentially missing facts include load-bearing status, exact plumbing relocation, deck height/attachment, shed use/permanence/lot-line distance, and same-size-vs-enlarged opening status.

**Interpretation:** HomeStars appears to offer strong upstream volume potential, but raw public lead data is not proven to be a one-call deterministic input. A pilot may need a very small clarification step or extraction from free text/photos.

Do not assume private HomeStars fields are absent; this observation is limited to the public intake/lead surface.

## QuoteXbert public intake

QuoteXbert's general AI estimate flow publicly asks for:

- project photos;
- free-text project description;
- project type;
- optional postal code.

Its project-specific calculators collect somewhat richer facts. For example, the deck calculator asks deck size, material, city, stairs and pergola/shade structure.

But the same public deck calculator does **not** visibly collect two facts that can be decisive for municipal applicability: deck height and attachment/connection to the building. Instead it publishes a simplified rule that attached decks or decks over 24 inches need a permit.

The basement calculator asks size, scope and city, but then publishes the broader statement that basement finishing requires permits in all Ontario municipalities. That bypasses municipality-specific exception logic rather than collecting all facts needed to resolve it.

**Interpretation:** QuoteXbert is technically close to an ideal ProjectPermit integration point because it already has structured project intake before quote/marketplace routing. But its current public UX suggests a preference for broad heuristic guidance instead of detailed deterministic fact collection. This makes its build-vs-buy reply especially important.

## RealCraft public intake

RealCraft's Smart Quote Wizard publicly says its questionnaires adapt by service type and collect service type, location, timing, photos and project notes. It separately offers a Permit Navigator with municipality-specific guides.

The public Permit Navigator currently exposes guide-style applicability and city guidance, while the quote wizard and permit guidance are presented as distinct tools.

**Interpretation:** RealCraft proves that permit guidance belongs in the pre-hire funnel, but public evidence does not yet prove that its quote wizard captures enough permit-critical facts to make a deterministic decision automatically.

## Integration-friction verdict

### Positive

The upstream platforms already collect several facts ProjectPermit needs:

- project family/type;
- location/postal code;
- free-text scope;
- photos;
- often dimensions or budget/timing.

This means ProjectPermit would usually start from a partially populated scope, not a blank form.

### Negative

Several municipal decisions depend on a small number of facts that marketplace intake may not collect because those facts are irrelevant to contractor matching or rough pricing.

The likely product boundary is therefore not simply:

`lead -> ProjectPermit API`

but potentially:

`lead -> normalize existing facts -> identify missing decisive facts -> ask 0-3 targeted clarifying questions -> deterministic ProjectPermit decision`

That is a hypothesis only. **Do not build a clarification-question product yet.**

## Validation gate created by this analysis

For the first serious upstream platform/pilot, measure:

1. percentage of relevant leads resolvable from existing intake with **0** follow-up questions;
2. percentage resolvable with **1-3** follow-up questions;
3. percentage still unresolved due to property overlays/site-specific facts;
4. median extra user/agent interaction time;
5. whether the platform considers that friction acceptable before quote routing.

A useful pilot threshold would be that a large majority of covered jobs can be resolved from existing data or at most a few targeted facts. The exact threshold should be set from partner workflow evidence rather than invented now.

## Decision implication

This does **not** lower the current Go/No-Go score. It identifies the next technical-commercial falsification question.

Do not expand municipalities or project families in response. First determine whether the existing seven-city/eight-family engine can fit an upstream intake with acceptably low clarification friction.

## Public sources reviewed

- https://www.homestars.com/how-it-works
- https://www.homestars.com/pro/register/general-contractor
- https://www.homestars.com/pro/register/window-contractor
- https://www.homestars.com/pro/register/interior-designer
- https://www.quotexbert.com/
- https://www.quotexbert.com/deck-calculator
- https://www.quotexbert.com/basement-renovation-calculator
- https://realcraft.ca/for-clients/
- https://realcraft.ca/how-it-works/
- https://realcraft.ca/permits/
