# Adjacent preflight competition boundary

Updated: 2026-08-28

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

## Permitio

Permitio is the strongest current evidence that permit applicability can be bundled directly into field-service workflows.

Current public positioning:

- U.S.-only HVAC/mechanical, electrical and plumbing/gas permit service;
- direct integrations with ServiceTitan, Jobber and Housecall Pro;
- pulls job address, equipment and scope from the field-service record;
- identifies jurisdiction and permit requirements, files applications, handles corrections and inspections;
- explicitly advertises **automatic permit detection** from job type/equipment/scope;
- human-assisted filing remains part of the service model;
- public pricing is roughly `$25-$100 per permit` with pay-as-you-go positioning.

Public adoption evidence is still early rather than mature:

- vendor site shows several contractor testimonials;
- public LinkedIn company page shows a 2-10 employee company and only a small public following at the time of review;
- no representative independent customer-volume evidence was found.

Boundary implication:

Permitio means ProjectPermit cannot claim the conceptual idea `job details -> permit requirement` is novel.

Current differentiation remains:

- Canada vs. Permitio's U.S. focus;
- deterministic rule engine + stable rule IDs + official-source evidence;
- API/MCP capability layer rather than a staffed permit-filing service;
- broad renovation/building project families rather than only high-frequency MEP/service permits.

A bounded E2 question was sent to Permitio asking whether Jobber-originated jobs generally arrive already known to require a permit or whether `permit required?` is still unresolved at intake. This is a high-value boundary measurement regardless of the answer.

Do not respond to this competitor by adding filing/inspection operations or U.S. municipalities without partner-linked evidence.

## QwikScope Greenlight

QwikScope Greenlight is the closest currently observed **conceptual product analogue**.

Current public positioning:

- project + scope + address -> jurisdiction resolution;
- required / likely / conditional permit determination;
- issuing agency and jurisdiction-specific triggers;
- building, grading, floodplain, zoning, telecom and utility permits;
- dependency-ordered permitting plan, critical path, fees and risk flags;
- self-serve product plus API access on engagement;
- QwikScope's public property layer states U.S.-nationwide coverage across 3,000+ counties and U.S. federal/state/local sources.

This is materially closer to ProjectPermit than a zoning lookup or filing service.

Boundary implication:

- the category already exists outside Canada;
- ProjectPermit must not claim `scope -> permit determination -> API` as a unique architecture;
- current geographic separation matters: no comparable seven-city Canadian deterministic/evidence-linked API product was found in this scan;
- QwikScope makes future U.S. expansion less attractive unless a real partner supplies large bounded demand in a geography QwikScope does not already serve well.

No credible independent usage/customer-scale evidence was found in the current public scan, so QwikScope is a **replication/competition risk**, not evidence that this market is already mature or saturated.

## Ampr

Ampr is a narrow but important Canadian embedded-workflow example.

Current public positioning:

- electrician-specific quoting/invoicing/job app;
- used in Ontario plus selected U.S. states;
- automatically detects permit-triggering electrical tasks during quote creation;
- Ontario examples add an ESA permit line item for panel/service/EV/hot-tub/generator and related tasks;
- permit cost is included before the quote is sent;
- quote workflow is exactly where ProjectPermit hopes to provide a routing signal in broader contractor software.

Adoption evidence remains early:

- live iOS product exists;
- App Store currently does not have enough ratings to show an overview;
- limited community mentions exist, but no representative volume evidence was found.

Boundary implication:

Ampr proves the **embedded-before-quote permit trigger** is not hypothetical, including in Ontario.

However, ProjectPermit's current eight project families do not include a dedicated electrical/HVAC family. Therefore Ampr is not a one-for-one substitute for the current product.

Do **not** add electrical/HVAC/mechanical project families simply because Toronto issued-permit volume is high. Add them only if an E2+/E3 partner exposes a bounded >=500/month candidate-preflight path and requests that coverage.

## PermitBird

PermitBird uses a very similar capability-layer architecture for environmental permits:

- deterministic/cited permit determination;
- REST API + hosted MCP;
- agent-callable output with rule text attached.

Its current domain is wetland/stormwater/environmental coverage rather than municipal residential building permits, so it is not a direct ProjectPermit substitute.

It does show that `cited permit-determination engine -> API/MCP` is becoming a recognizable product pattern. ProjectPermit's moat therefore cannot be the protocol wrapper or generic decision-engine concept.

## BuildBlox

Current public positioning is much broader housing-delivery intelligence:

- parcel/zoning/servicing intelligence;
- standardized design matching;
- feasibility/pre-development packages;
- BOM/cost/procurement and modular/offsite workflows;
- active work across several Canadian provinces.

Its Ontario emphasis is not currently a clean match to ProjectPermit's covered GTA/municipal workflow, so it is not a priority E2 target merely because it is Canadian. It is another reason not to turn ProjectPermit into a full housing-development operating system.

## Neighbourly / Homicity — permit-history API, not applicability

A 2026 API-level search found Neighbourly/Homicity exposing a Canadian Building Permits API across roughly 20 cities. It normalizes permit records into a shared schema and supports address/coordinate/viewport queries, filtering by permit type, status, cost and date.

Public source:

- https://homicity.com/data/permits

This is important **data-layer competition**, but it answers a different question:

`What permits were filed/issued around this address/place?`

rather than:

`Does this proposed normalized scope require a permit under the current municipality's rules?`

Boundary implication:

- do not duplicate normalized historical permit-search APIs;
- historical permit data may become supporting context, but it is not a substitute for applicability rules;
- the existence of a Canada-wide normalized permit-data API further weakens any moat claim based on data normalization alone;
- no current public evidence from this product shows a scope-to-permit-required deterministic endpoint.

## Canadian deterministic compliance-checking initiative — medium-term threat

In August 2026, Innovative Solutions Canada / NRC published a challenge for deterministic AI-assisted compliance checking of building permit applications. The requested capabilities include itemized `Meets / Does not Meet / Information Not Available / Uncertain` outcomes, rule-level checks, possible open APIs, and pipelines to digitalized code/by-law data.

Public source:

- https://ised-isde.canada.ca/site/innovative-solutions-canada/en/deterministic-artificial-intelligence-assisted-compliance-checking-building-permit-applications

This is primarily **downstream application/code-compliance review**, not ProjectPermit's upstream `do I need a permit?` decision. It therefore does not make the current product redundant.

However, it is a medium-term competitive signal:

- Canadian public-sector funding is actively encouraging deterministic regulatory engines and interoperable APIs;
- digitalized code/by-law infrastructure will reduce the cost of building rule-based compliance products over time;
- ProjectPermit must not rely on the claim that deterministic regulatory interpretation will remain technically rare;
- any moat has to come from validated workflow distribution, maintained municipal exceptions, safety/accuracy history and low-cost integration rather than the mere existence of a deterministic rules engine.

Do not lower the commercial score solely for this initiative because its current scope is downstream and no directly substitutable self-serve permit-applicability API is demonstrated.

## Why this boundary matters

The adjacent market is already becoming crowded across three layers:

**Upstream feasibility**

`address -> parcel -> zoning -> setbacks -> development potential -> approval route`

**Permit applicability / permit determination**

`project/job scope -> jurisdiction -> permit required/type -> evidence/routing`

**Downstream submission QA / filing**

`known or detected permit-positive project -> forms/drawings -> filing -> corrections -> inspections`

ProjectPermit is **not alone in the middle layer**. QwikScope, Permitio and Ampr show overlapping implementations in different geographies/trades.

ProjectPermit's current gap is therefore narrower:

`Canadian Request/Estimate/Quote scope -> municipal building-permit applicability -> deterministic official evidence -> workflow routing`

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
- human reviewer marketplace/network;
- inspections/status operations;
- speculative U.S. coverage;
- speculative electrical/HVAC family expansion.

Any item above requires new external evidence showing that it is necessary to win or retain a high-volume workflow.

## Defensibility rule

ProjectPermit should no longer treat **idea novelty** as a moat.

Observed 2026 products already demonstrate:

- scope-aware permit determination;
- permit detection inside quote/job software;
- jurisdiction resolution;
- cited regulatory outputs;
- API access;
- CRM/FSM integration.

The only credible future moat candidates are cumulative operational assets:

1. **maintained Canadian rule corpus** with stable rule IDs and source history;
2. **address/property adapters** tied to first-party municipal datasets;
3. **representative historical accuracy corpus** with false-negative tracking;
4. **embedded distribution agreements/integrations** where switching removes workflow value;
5. **observed production outcomes** that improve coverage prioritization and rule maintenance;
6. low-cost/self-service operations that competitors cannot match without a staffed permit-runner model.

Until items 3-5 exist externally, defensibility should be scored **medium-low**, not high.

## Distribution implication

Adjacent products may be more valuable as **distribution partners** than as competitors.

Priority partner test:

1. Does the adjacent product already receive a normalized project type plus address before construction/permit certainty?
2. Does it process >=500 bounded candidate events/month in a ProjectPermit-covered geography?
3. Is `permit required?` still a distinct unresolved next-step question after its current output?
4. Can 5-20 representative de-identified historical cases be benchmarked?
5. If E3 passes, can repeated external ProjectPermit calls be observed without requiring a staffed manual workflow?

If yes, pursue integration/E3 before adding new zoning, trade, filing or submission features.

## Current conclusion

The 2026 competitive scan changes the conclusion from **no equivalent layer found** to a more cautious one:

- no current public product found with the same **seven-city Canadian municipal-building coverage + deterministic official-evidence API/MCP contract**;
- but the underlying capability category is clearly real and reproducible;
- QwikScope Greenlight is a close U.S. conceptual analogue;
- Permitio bundles automatic permit detection into U.S. field-service permit filing;
- Ampr embeds Ontario electrical permit detection directly at quote creation;
- Canadian permit-history/property APIs and public-sector deterministic compliance initiatives are reducing the technical whitespace around the product;
- these observations do not yet prove a directly substitutable low-friction Canadian applicability API.

Therefore ProjectPermit is still early enough to validate, but **feature novelty is not defensibility**.

ProjectPermit should protect a clean B2B/API differentiation:

> **Canadian permit applicability is the product. Zoning/property intelligence is supporting context. Filing/package review is downstream. The moat, if one develops, must come from maintained evidence + accuracy + distribution.**
