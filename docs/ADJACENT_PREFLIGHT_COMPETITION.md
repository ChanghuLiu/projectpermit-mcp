# Adjacent preflight competition boundary

Updated: 2026-08-27

Purpose: keep ProjectPermit focused on the narrow capability that is not already being served well by zoning/buildability or downstream permit-package products.

This document is a product-scope guardrail, not a claim that every adjacent product is a direct substitute.

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

ProjectPermit should **not** become a general zoning/development-feasibility product or a drawing/package review product unless external integration evidence makes that expansion necessary.

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
- multi-layer GIS aggregation as a general product;
- permitted-use analysis unrelated to permit applicability;
- nearby-development discovery;
- development-charge calculator.

A potentially complementary integration would consume or share derived property facts, then let ProjectPermit answer the narrower scope-specific permit-applicability question.

The public site exposes an `Email me` CTA but current search results do not reveal the underlying address. Do not guess an email address merely to send outreach.

## LotMore

Current public positioning is more overlapping in the Toronto homeowner/developer funnel:

- Toronto address-first property analysis;
- zoning rules and buildable envelope;
- project paths for additions, garden/laneway suites, multiplexes and major-street development;
- project-level feasibility verdicts and likely approval-route hints;
- source-linked rules and nearby approval evidence;
- paid property/project reports;
- downstream architectural drawings, permit support and construction services.

LotMore publicly frames its flow as:

`address -> property/project feasibility -> approval route -> drawings/permit support -> construction`

This is a stronger overlap with ProjectPermit's project-family surface than a pure zoning lookup, especially for additions and secondary-unit projects.

Boundary implication:

- do not compete with LotMore as a Toronto homeowner destination report;
- do not build consumer $49/$99 feasibility reports, 3D massing, architect calls, drawings or construction hand-off merely to match its funnel;
- ProjectPermit must win **earlier and invisibly inside B2B software**, where a Request/Estimate/Quote still needs a permit-applicability routing signal;
- Toronto consumer-facing feasibility should be considered a relatively crowded segment.

LotMore can still be a future integration/benchmark target if a public or permissioned contact path yields a bounded upstream project-check denominator. Do not infer its volume from the number of public address pages.

## PermitCheck.ca

Current public positioning is **downstream** of ProjectPermit:

- automated pre-submission permit-package validation;
- uploads drawings/forms/reports and checks completeness, formats, annotations and common rejection causes;
- current beta check flow includes Toronto, Ottawa and several Ontario municipalities/permit types, with other municipalities rolling out;
- Toronto product initially emphasizes decks/porches and is expanding into basements, interior alterations and additions;
- separately exposes zoning checks for selected cities;
- has an optional human reviewer network for uncertain package-review cases.

Its core question is:

> Is the permit package complete and submission-ready?

ProjectPermit's core question is earlier:

> Does this normalized project scope require a municipal permit in the first place, and what evidence supports that routing decision?

Boundary implication:

Do **not** expand into:

- PDF/drawing ingestion;
- missing-document detection;
- drawing annotation/completeness QA;
- Ontario Building Code plan review;
- human reviewer networks;
- submission-package certification.

PermitCheck demonstrates that downstream application QA is becoming its own product category. That strengthens the need for ProjectPermit to remain the upstream applicability layer rather than stretch across the whole permit lifecycle.

## BuildBlox

Current public positioning is much broader housing-delivery intelligence:

- parcel/zoning/servicing intelligence;
- standardized design matching;
- feasibility/pre-development packages;
- BOM/cost/procurement and modular/offsite workflows;
- active work across several Canadian provinces.

Its Ontario emphasis is not currently a clean match to ProjectPermit's covered GTA/municipal workflow, so it is not a priority E2 target merely because it is Canadian. It is another reason not to turn ProjectPermit into a full housing-development operating system.

## Why this boundary matters

The adjacent market is already becoming crowded across two layers:

**Upstream feasibility**

`address -> parcel -> zoning -> setbacks -> development potential -> approval route`

**Downstream submission QA**

`known permit-positive project -> drawings/forms -> completeness/code/package checks -> submission`

ProjectPermit's defensible gap sits between them and earlier in the commercial workflow:

`Request/Estimate/Quote scope -> permit applicability -> official evidence -> workflow routing`

That boundary also keeps operating cost low: ProjectPermit can use first-party municipal/open-data property facts as supporting context without having to build a full development-feasibility engine or a staffed expert-review operation for every city.

## Product-scope stop list

Do not build the following merely because an adjacent product has them:

- graphical buildable envelopes;
- site plans or massing;
- development pro formas;
- unit-yield optimization;
- general-purpose zoning search;
- citywide development opportunity maps;
- consumer feasibility-report funnel;
- homeowner lead generation;
- permit drawings;
- permit submission/expediting;
- PDF/document completeness QA;
- full architectural/OBC/code-plan review;
- human reviewer marketplace/network.

Any item above requires new external evidence showing that it is necessary to win or retain a high-volume workflow.

## Distribution implication

Adjacent products may be more valuable as **distribution partners** than as competitors.

Priority partner test:

1. Does the adjacent product already receive a normalized project type plus address before construction/permit certainty?
2. Does it process >=500 bounded candidate events/month in a ProjectPermit-covered geography?
3. Is `permit required?` still a distinct unresolved next-step question after its current output?
4. Can 5–20 representative de-identified historical cases be benchmarked?
5. If E3 passes, can repeated external ProjectPermit calls be observed without requiring a staffed manual workflow?

If yes, pursue integration/E3 before adding new zoning or submission features.

## Current conclusion

Current public evidence does **not** show that the adjacent products provide the same deterministic municipal permit-applicability layer across ProjectPermit's seven Canadian jurisdictions.

It does show that both zoning/buildability intelligence and downstream package QA are increasingly mature. Toronto in particular is already crowded as a consumer/developer destination-product market.

ProjectPermit should therefore protect a clean B2B/API differentiation:

> **Permit applicability is the product. Zoning/property intelligence is supporting context. Submission-package review is downstream.**
