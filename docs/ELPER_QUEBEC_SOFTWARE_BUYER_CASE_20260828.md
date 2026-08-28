# Elper Quebec Software-Buyer Validation Case — 2026-08-28

## Why Elper matters

Elper is a Quebec-focused construction-management SaaS whose public workflow spans quotation approval, project creation, invoicing, employee/project management and cost tracking.

That makes Elper a materially better ProjectPermit falsification target than a single contractor: one product can expose whether permit applicability is a repeated cross-customer workflow problem before quote approval.

Current classification:

> **HIGH-VALUE QUEBEC SOFTWARE-BUYER FALSIFICATION TARGET — SCALE UNVALIDATED**

## Public workflow evidence

Elper's current homepage states that it serves **hundreds of clients across Quebec** and supports construction businesses from very small teams to large organizations.

It explicitly positions the product around:

- quotation to invoicing;
- electronic quote approval;
- project management;
- project budgets and cost tracking;
- employee/time management.

Sources:

- `https://elper.pro/`
- `https://elper.pro/forfaits-elper/`

Elper's support documentation gives the quote-stage transition explicitly:

1. a quote is sent to the client;
2. the client accepts or rejects it;
3. an accepted quote becomes `Gagnée`;
4. a project is then created from the accepted quote;
5. project financials and invoicing continue downstream.

Source:

- `https://elper.pro/support/creer-un-projet-et-facturer-a-partir-dune-soumission/`

**Implication:** if permit applicability is unresolved inside this workflow, the clean insertion point is before quote acceptance / `Gagnée`, not after project creation.

## Scale boundary

`Hundreds of clients` is **not** a monthly permit-call denominator.

Do not infer:

- projects/month per Elper client;
- current-family project share;
- covered-municipality share;
- unresolved permit-applicability incidence;
- 500+ ProjectPermit calls/month.

A 500/month distribution gate can only be supported by a bounded observed denominator such as:

> active contractor accounts × recent monthly current-family quotes × fraction where permit applicability is unresolved before approval.

Until such data exists, Elper is a distribution-shape and differentiation target, not scale evidence.

## Integration boundary

The current public Elper pages reviewed on 2026-08-28 show accounting integrations with Sage, Acomba and QuickBooks, but the current public homepage/support/package pages reviewed did not expose a documented third-party developer API, webhook product or general external integration marketplace.

Sources:

- `https://elper.pro/forfaits-elper/`
- `https://elper.pro/support/`

This is only a public-market observation.

> Absence of public API documentation does **not** establish absence of private APIs, partner integrations or custom integration routes.

Elper must answer this directly.

## SoumissionRénovation adjacency

SoumissionRénovation has publicly announced a partnership with Elper. That matters because SoumissionRénovation is currently ProjectPermit's strongest observed Quebec high-volume renovation-platform candidate.

The partnership shows that Elper is not isolated from Quebec renovation lead/project ecosystems and that software partnership is a plausible operating model.

It does **not** prove that project intake data flows automatically between the products or that either side exposes an API.

## Why the current two-stage ProjectPermit contract fits

ProjectPermit now fails safe when a permit exemption depends on unresolved parcel overlays.

A software workflow can therefore be staged as:

1. municipality / postal code + structured project scope;
2. municipal-level permit preflight;
3. if the response contains `property_context_status=UNRESOLVED_FOR_EXEMPTION`, collect or resolve the property facts listed in `required_property_facts`;
4. run the address/property-aware second stage before relying on the exemption.

This reduces quote-form friction without treating unknown heritage/PIIA status as false.

The integration hypothesis for Elper is therefore not `send every quote to a full address lookup`.

It is:

> selectively call ProjectPermit for current-family quotes, and request parcel context only when the deterministic result requires it.

## Outreach sent

A short falsification email was sent on 2026-08-28 to Elper's publicly documented support address `aide@elper.pro`.

The questions were deliberately narrow:

1. across contractor clients, does `permit required or not?` recur before a quote is approved, or is it normally resolved elsewhere?
2. does Elper have an API, integration or partnership route through which an external service could read municipality + project category and return a structured permit preflight?

The message explicitly said that `this is not a problem we would automate` is a useful answer and requested no customer-specific data.

Public contact source:

- `https://elper.pro/wp-content/uploads/2025/02/Guide-de-demarrage.pdf`

## Upgrade conditions

Upgrade Elper only if a response or other bounded evidence establishes both:

1. **workflow incidence:** permit applicability is a repeated unresolved pre-quote decision across multiple contractor customers; and
2. **delivery path:** a realistic external API / integration / partnership route exists.

For a distribution-scale upgrade, additionally require a bounded monthly denominator showing enough current-family quote events in covered or explicitly expandable Quebec municipalities.

## Negative conditions

Downgrade or close this route if Elper reports that:

- contractors normally know permit applicability before creating/sending the quote;
- permit research is handled later without meaningful quote-stage friction;
- the question is too infrequent to justify automation;
- municipal assistants/manual research are adequate;
- there is no realistic external integration route;
- the value per call cannot support municipal rule maintenance.

## Strategic interpretation

Elper is useful because it tests a more important question than `can ProjectPermit integrate with construction software?`

The decisive question is:

> **Does a Quebec construction-software vendor with hundreds of contractor customers observe enough repeated pre-quote permit uncertainty that a deterministic external machine service is worth integrating?**

If the answer is no, Quebec's remaining `unified developer API` thesis weakens materially even if the technical integration is easy.
