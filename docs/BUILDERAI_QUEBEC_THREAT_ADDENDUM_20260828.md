# BuilderAI Quebec Threat Addendum — 2026-08-28

## Classification

> **DIRECT PRODUCT-THESIS THREAT IN QUEBEC — LOW OBSERVED DISTRIBUTION, HIGH WORKFLOW OVERLAP**

BuilderAI is not currently a demonstrated high-scale distribution competitor. Its public site says the product has been tested on **74 real estimates/projects** since launch.

However, it materially changes ProjectPermit's Quebec differentiation thesis because it publicly embeds municipal `urbanisme` analysis directly inside a Quebec contractor estimating and quotation workflow.

## Public workflow overlap

BuilderAI's current product flow is:

1. contractor describes a real project and can attach plans/photos;
2. AI structures the project, quantities and estimate;
3. BuilderAI runs a `rapport urbanisme` / municipal urbanism check before quote delivery;
4. the contractor finalizes a professional quote;
5. the quote can be shared/signed through a client portal or exported/integrated with accounting software.

Sources:

- `https://www.builder-ai.ca/fr`
- `https://www.builder-ai.ca/demo`

The public product explicitly positions itself as a Quebec platform for estimating, plan analysis, urbanism and project execution from first quote to client signature.

## Laval permit-applicability demo

BuilderAI's public Laval bathroom-renovation demo states that before sending the quote it validates Quebec regulatory items and runs an urbanism check.

The demo shows:

- municipality: Laval;
- residential bathroom renovation;
- zoning/urbanism consulted;
- conclusion: no construction permit required for the interior renovation case shown;
- statement that the in-app urbanism RAG consults the real municipal regulation.

Source:

- `https://www.builder-ai.ca/demo`

This is direct functional overlap with ProjectPermit's `permit applicability before quote` use case.

## Cross-check against official Laval guidance

Laval's current official residential interior-renovation page explicitly states:

- renovation of an existing bathroom -> no permit;
- adding a bathroom -> permit required;
- ordinary kitchen renovation -> no permit;
- interior renovation requires a permit when room dimensions, room count or structure changes;
- basement renovation requires a permit when room count or structure changes.

Source:

- `https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx`

Therefore BuilderAI's public bathroom-demo conclusion is directionally consistent with the City's current permit table.

## Evidence-quality boundary

Do **not** treat the BuilderAI demo as equivalent to ProjectPermit's deterministic/evidence-linked contract yet.

The public demo labels its displayed regulatory excerpt as indicative and says the application uses an urbanism RAG internally.

The current public review did not establish that BuilderAI exposes:

- deterministic rule IDs;
- rule/source versions;
- source-verification timestamps;
- explicit machine states such as `REQUIRED / LIKELY_NOT_REQUIRED / MUNICIPAL_CONFIRMATION_REQUIRED`;
- fail-safe unresolved parcel-overlay handling;
- public third-party developer API;
- broad verified municipality coverage.

These are unresolved competitive questions, not proven differentiators.

## Scale boundary

BuilderAI's public site currently cites **74 estimates processed since launch** by its founder/operator workflow and 10+ project types.

Source:

- `https://www.builder-ai.ca/fr`

This is not enough to establish a high-volume distribution threat.

Do not infer:

- active paid customer count;
- monthly estimate volume across customers;
- municipality coverage;
- current-family permit-check volume;
- 500+ monthly permit decisions.

BuilderAI is presently more important as a **product architecture signal** than a scale signal.

## Why this changes ProjectPermit's differentiation gate

Before this evidence, a buyer statement such as:

> `We would like permit/urbanism guidance before approving a quote.`

could look like strong differentiation evidence for ProjectPermit.

That is no longer sufficient.

BuilderAI demonstrates that a vertical estimating SaaS can embed an urbanism/RAG feature directly inside its own quote workflow.

ProjectPermit must therefore prove that buying an external capability is superior to each SaaS building a narrow internal RAG.

Required differentiation evidence now includes at least one of:

1. **cross-city maintenance advantage** — buyer does not want to maintain municipal sources/rules itself;
2. **deterministic/evidence advantage** — buyer requires reproducible rule IDs, official evidence, source versions and conservative unknown handling rather than a generic RAG summary;
3. **coverage advantage** — one API covers enough municipalities/scopes to outperform a buyer-specific internal implementation;
4. **economics advantage** — external per-call cost is cheaper than building and maintaining the capability internally;
5. **delivery advantage** — REST/MCP/agent access lets multiple products/workflows reuse the capability rather than embedding it into one estimator.

A generic desire for `urbanisme before quote` is now **workflow-demand evidence only**, not ProjectPermit differentiation evidence.

## Outreach sent

A short competitive-falsification email was sent on 2026-08-28 to the official contact listed in BuilderAI's privacy policy: `info@gestion-af.ca`.

Questions:

1. whether the urbanism module already covers multiple Quebec municipalities or is limited/pilot;
2. whether it returns permit applicability plus municipal-source evidence or mainly a RAG zoning/urbanism summary;
3. whether the capability is internal-only or available through API/integration/partnership.

Official contact source:

- `https://www.builder-ai.ca/politique-confidentialite`

No customer data was requested.

## Revised Quebec threat structure

As of 2026-08-28, Quebec competition should be separated into three layers:

### Municipal self-service

Examples: Gatineau URBAIN, Laval permit decision pages, Longueuil digital permitting.

Threat: residents/contractors may not need a separate product for a single municipality.

### Embedded vertical software

Example: BuilderAI.

Threat: contractor software can internalize permit/urbanism checking directly in the quote workflow.

### Cross-municipality third-party API

No broad Quebec equivalent to LandLogic's observed Ontario platform/API position has yet been publicly verified in this review.

This is ProjectPermit's remaining possible Quebec wedge — but only if buyers prefer an external deterministic shared capability to building narrow internal RAG features.

## Pause condition

Pause or materially downgrade Quebec expansion if either of these becomes true:

- BuilderAI or another vertical SaaS demonstrates that broad multi-municipality permit applicability can be cheaply and reliably internalized with ordinary RAG; or
- software buyers say they prefer to own the urbanism feature internally and do not value an external deterministic/evidence-linked API enough to pay for it.

Do not add municipalities merely to stay ahead of embedded competitors. Expand only when external software demand validates the shared-API model.
