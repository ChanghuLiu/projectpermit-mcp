# Adjacent preflight competition boundary

Updated: 2026-08-27

Purpose: keep ProjectPermit focused on the narrow capability that is not already being served well by zoning/buildability products.

This document is a product-scope guardrail, not a claim that adjacent products are direct substitutes.

## ProjectPermit's intended boundary

ProjectPermit should answer:

> Given a normalized renovation/build scope and municipal/property context, is a municipal permit **required / likely not required / needs confirmation**, and what official source/rule supports that decision?

Core differentiators:

- deterministic scope-to-rule evaluation;
- evidence-linked official sources;
- stable rule IDs;
- explicit required / likely-not-required / confirm outcomes;
- address-aware property context where it materially changes applicability;
- multi-jurisdiction Canadian coverage;
- API/MCP insertion into an upstream Request / Estimate / Quote / Job workflow.

ProjectPermit should **not** become a general zoning/development-feasibility product unless external integration evidence makes that expansion necessary.

## FutureLot

Current public positioning:

- U.S. nationwide lot-specific zoning/buildability intelligence;
- single-family homes, additions, ADUs/backyard cottages, pools and similar project feasibility;
- setbacks, lot coverage, buildable area and site-plan style outputs;
- appears in Buildxact's partner directory as a lot-by-lot zoning-intelligence partner.

Boundary implication:

- validates that lot-specific feasibility can be valuable inside a builder workflow;
- not a current Canadian substitute for ProjectPermit's seven-city coverage;
- do not use FutureLot as a reason to expand speculatively into U.S. municipalities;
- do not clone its buildable-envelope/site-plan scope.

## Zoned.ca

Current public positioning:

- Canadian address-first zoning/buildability checks;
- live Ottawa and beta Toronto/Mississauga;
- parcel/zoning/setbacks/envelope/project-fit workflow for additions, basement units, accessory structures, pools, sheds, rebuilds and related projects;
- explicitly describes itself as a **pre-check, not a permit** and not a permit-approval service;
- partner proof-of-concept access is offered case-by-case while pricing is still being developed.

Boundary implication:

Zoned is adjacent rather than identical:

`address -> zoning/buildability/project fit`

ProjectPermit should remain:

`normalized scope + property facts -> permit applicability -> evidence-linked decision`

Potential relationship:

- upstream data/context partner;
- complementary decision step after zoning-fit;
- potential E2/E3 distribution partner if its project-check volume is meaningful.

An E2 threshold request was sent to `hello@zoned.ca` asking whether one recent complete month across Ottawa + Toronto + Mississauga contained at least 500 address/project checks with a selected project type. No reply should be counted above E0/E1 unless it includes timeframe, geography and workflow denominator.

## Toronto Zoning

Current public positioning:

- Toronto-only zoning/development-feasibility product;
- REST API with address lookup and batch lookup (up to 50 addresses/call);
- effective zoning standards, development potential, parcel/GIS layers, heritage/natural-hazard constraints;
- permitted-use analysis;
- nearby permit / Committee of Adjustment / rezoning activity;
- development-charge estimation;
- public-data-backed and explicitly not legal advice.

Its public API demonstrates that property-context intelligence is already becoming API-native.

Boundary implication:

Do **not** duplicate:

- full zoning profile;
- theoretical maximum GFA;
- buildable envelope;
- 19-layer GIS aggregation as a general product;
- permitted-use analysis unrelated to permit applicability;
- nearby-development discovery;
- development-charge calculator.

A potentially complementary integration would consume or share derived property facts, then let ProjectPermit answer the narrower scope-specific permit-applicability question.

The public site exposes an `Email me` CTA but current search results do not reveal the underlying address. Do not guess an email address merely to send outreach.

## Why this boundary matters

The adjacent market is becoming crowded around:

`address -> parcel -> zoning -> setbacks -> development potential`

ProjectPermit's defensible wedge should therefore become **narrower, not broader**:

`scope -> permit applicability -> official evidence -> workflow routing`

That boundary also keeps operating cost low: ProjectPermit can reuse first-party municipal/open-data property facts without having to build a full development-feasibility engine for every city.

## Product-scope stop list

Do not build the following merely because an adjacent product has them:

- graphical buildable envelopes;
- site plans or massing;
- development pro formas;
- unit-yield optimization;
- general-purpose zoning search;
- citywide development opportunity maps;
- homeowner lead generation;
- permit submission/expediting;
- full architectural/code-plan review.

Any item above requires new external evidence showing that it is necessary to win or retain a high-volume workflow.

## Distribution implication

Adjacent products may be more valuable as **distribution partners** than as competitors.

Priority partner test:

1. Does the adjacent product already receive a normalized project type plus address before construction/permit certainty?
2. Does it process >=500 bounded candidate events/month in a ProjectPermit-covered geography?
3. Is `permit required?` still a distinct unresolved next-step question after its current output?
4. Can 5–20 representative de-identified historical cases be benchmarked?
5. If E3 passes, can repeated external ProjectPermit calls be observed without requiring a staffed manual workflow?

If yes, pursue integration/E3 before adding new zoning features.

## Current conclusion

Current public evidence does **not** show that FutureLot, Zoned or Toronto Zoning already provides the same deterministic municipal permit-applicability layer across ProjectPermit's Canadian coverage.

It does show that zoning/buildability intelligence is increasingly mature. ProjectPermit should therefore protect a clean differentiation:

> **Permit applicability is the product. Zoning/property intelligence is supporting context, not the product.**
