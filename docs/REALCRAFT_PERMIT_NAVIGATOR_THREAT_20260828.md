# RealCraft Permit Navigator Threat — 2026-08-28

## Why this matters

RealCraft is the clearest Canadian example found so far of a contractor marketplace independently placing permit guidance directly beside the homeowner/project-to-quote workflow.

It is not currently verified as an exact ProjectPermit API substitute, and its marketplace is still in Beta / founding-member mode. But it materially weakens the assumption that a quote/lead platform would naturally buy permit guidance rather than build a lightweight version internally.

## Current public product evidence

RealCraft's client page currently advertises:

- a **Smart Quote Wizard** where users describe a project in plain language;
- verified-pro matching and quote comparison;
- a **Free Ontario Permit Navigator** positioned as `Know your permits before you build`;
- municipality-specific permit guidance for Ottawa, Toronto, Mississauga, Hamilton and London;
- free use without signup.

The same page states users can `find out which permits your project needs before you hire`.

Source:

- https://realcraft.ca/for-clients/

The public permit directory currently lists:

- Ottawa;
- Toronto;
- Gatineau;
- Mississauga;
- London;
- Hamilton.

Source:

- https://realcraft.ca/permits/

This creates direct city overlap with ProjectPermit in **Ottawa, Toronto, Gatineau and Mississauga**.

## Important boundary: current navigator appears guide-driven, not a verified deterministic API

The current public `Open the Permit Advisor` link routes to RealCraft's municipality guide directory rather than exposing a verified structured `scope facts -> deterministic permit applicability result` API or decision engine.

The city guides contain categorized `permit usually required` / `permit typically not required` guidance, process steps, fees, timelines and additional approval notes.

Current review did **not** find public evidence of:

- an API for permit applicability;
- stable rule IDs;
- machine-readable official-source evidence per determination;
- address/GIS enrichment;
- a reproducible structured fact contract comparable to ProjectPermit;
- a public deterministic response schema;
- external platform integrations for the permit navigator.

Do not turn this absence into a claim that no private/internal implementation exists.

## RealCraft is still pre-scale

RealCraft's current client page identifies the product as **Beta** and says:

- it is building toward a later-2026 launch;
- professionals on the preview are placeholders;
- local names ship at launch / founding members receive early access.

Source:

- https://realcraft.ca/for-clients/

Therefore RealCraft is not evidence of proven Canadian permit-guidance transaction volume.

It is evidence of **independent product convergence**.

## Accuracy / specificity differentiation remains testable

RealCraft's Toronto permit guide says a permit is usually required for `Finishing a basement — When it adds habitable space`.

Source:

- https://realcraft.ca/permits/ontario/toronto/

Toronto's current first-party guidance is more conditional. The City explicitly says a house-basement finish does **not** require a building permit when:

- there are no structural or material alterations;
- no additional dwelling unit is created; and
- no new plumbing is installed.

Source:

- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

This is exactly the type of nuance ProjectPermit's structured-fact rules are intended to preserve.

It does not prove ProjectPermit is more accurate overall. It provides one concrete case where a generic city-level guide can be less precise than a deterministic scope-specific rule.

## Strategic interpretation

RealCraft creates two opposing signals.

### Negative signal

A Canadian marketplace can build permit guidance itself and give it away as a free acquisition/decision-support feature.

That weakens the thesis:

> `permit guidance exists, therefore platforms will pay ProjectPermit for it`.

Guidance can be bundled into lead generation and monetized indirectly through contractor memberships/marketplace activity.

### Positive / differentiation signal

The current public RealCraft implementation appears guide-driven and simplified rather than a verified deterministic evidence contract.

That preserves a narrower B2B thesis:

> platforms may still buy a maintained, reproducible, evidence-linked machine capability if internal guidance becomes inaccurate, costly to maintain, hard to audit, or difficult to scale across municipalities.

This must be proven through build-vs-buy evidence, not assumed.

## Direct build-vs-buy outreach

On 2026-08-28, ProjectPermit emailed `support@realcraft.ca` and asked only two directional product-infrastructure questions:

1. whether RealCraft's municipal permit guidance is maintained internally or uses a third-party permit-data provider;
2. whether RealCraft would consider an external deterministic API with official evidence/stable rule IDs as municipality coverage expands.

No customer data or confidential metrics were requested.

Evidence state: **no qualifying reply yet**.

## Go / No-Go implication

Recommended score change:

- competitive headroom: **1/10 -> 0/10**;
- overall score: **52 -> 51 / 100** (50.5 rounded to 51);
- defensibility remains **2/10** pending evidence on maintained-rule accuracy, buyer preference and representative E3 benchmarking.

Rationale:

- LandLogic proves broad Ontario regulatory/property APIs;
- BuilderAI proves a Quebec quote platform can internalize municipal urbanism guidance;
- PermitFlow proves permit research/data/API can scale massively in the U.S.;
- RealCraft independently proves a Canadian quote marketplace can bundle permit guidance directly into the homeowner pre-hire funnel.

There is now effectively **no conceptual competitive headroom**. Remaining opportunity is execution quality, Canadian maintenance, deterministic evidence and embedded distribution.

## Stop pressure

At **51/100**, one additional materially negative validated signal can cross the project's <50 stop threshold.

Examples that should trigger a stop/re-scope review:

- RealCraft or another Canadian platform says its internal permit guidance is cheap/easy enough that an external maintained API has no value;
- representative E3 shows deterministic accuracy is not meaningfully better than simpler guide/RAG approaches;
- a high-volume platform reports permit applicability is already known in >90% of relevant quote-stage events;
- no >=500/month current-family upstream denominator can be established after qualified platform outreach;
- E5 remains zero after actual product/platform decision-maker conversations.

## Engineering consequence

Do not respond by adding Hamilton, London, or more municipalities.

RealCraft's existence makes speculative geography expansion less rational, not more.

Continue only work that tests:

- external historical accuracy (E3);
- upstream event density (E2);
- non-owner repeated calls (E4);
- build-vs-buy preference;
- price/resource commitment (E5).