# PlanEdge Permit-Requirement / Open-API Boundary — 2026-08-28

## Purpose

The canonical Go/No-Go scorecard already treats PlanEdge Permits as a serious kill-path competitor. The exact kill condition is stronger than simple feature overlap:

> PlanEdge must independently verify an externally callable cross-municipality permit-requirement engine at meaningful production scale/economics.

This review tightens what is now publicly proven and what is still missing. It does **not** lower the score merely because adjacent public claims can be combined into a plausible story.

## Publicly proven product overlap is now strong

PlanEdge's current public product surface describes a Canada-wide permit platform covering residential, commercial and industrial work.

The workflow states that PlanEdge performs requirements research before application preparation and identifies the exact permit type, fees, schedules and supplementary requirements for the relevant municipality.

The Workflow Automation surface is more specific: when a new project is added, PlanEdge says it **automatically determines what permits are needed**, builds the submission checklist, routes documents and proceeds through the permit workflow.

Its Smart Checklists are described as auto-populating permit requirements based on:

- project type;
- municipality;
- scope.

That is near-exact functional overlap with ProjectPermit's core input boundary even though PlanEdge continues into full permit preparation/submission/management.

Source:

- https://www.planedgepermits.com/

## Public Open API is also real

PlanEdge's Integration Hub currently advertises:

- Procore integration;
- Autodesk Construction Cloud integration;
- Bluebeam integration;
- **Open API for custom ERP and enterprise system connections**.

The Open API description states that a RESTful API lets a customer's development team connect PlanEdge to an internal system or ERP platform.

Source:

- https://www.planedgepermits.com/

Therefore the previous question is no longer whether PlanEdge has any external integration surface. It does.

## Scale / delivery claims are materially stronger than a roadmap-only competitor

PlanEdge currently claims:

- 444+ municipalities across Canada;
- 2022 company founding;
- first clients onboarded in late 2022;
- platform launched in 2023 with coverage expanded to 200+ municipalities;
- coast-to-coast expansion and 444+ municipality coverage in 2024;
- active relationships in 444+ municipalities;
- analytics learned from thousands of permit applications across Canadian municipalities;
- current contractor/developer/homebuilder/property-owner use;
- project-based pricing plus monthly-retainer enterprise accounts.

Source:

- https://www.planedgepermits.com/

These are vendor claims, not independent production telemetry. They are nonetheless materially stronger delivery evidence than a waitlist/beta-only competitor.

## The one remaining API semantic boundary

The public site does **not** currently expose API endpoint documentation, Swagger/OpenAPI schema, sample request/response, or another public machine contract showing that an external client can do the following directly:

`project type + municipality + scope -> required permits / requirement checklist`

The integrations page's concrete examples emphasize synchronization of:

- permit status;
- documents;
- inspection dates;
- drawings/review feedback.

The site separately proves that the internal workflow engine can determine required permits.

It is therefore tempting—but not evidence-safe—to infer:

`internal requirement engine + Open API = requirement engine is externally callable`.

ProjectPermit must **not** make that inference without direct API documentation, a working endpoint, or a substantive PlanEdge confirmation.

## Exact verification question

Only one yes/no-style boundary remains worth asking PlanEdge:

> Can a third-party system use the current PlanEdge Open API to create/send a project scope and programmatically receive the required-permits / municipal checklist output, before engaging the managed permit-submission workflow?

A useful positive answer should clarify that the result is available programmatically and reusable across PlanEdge's multi-municipality coverage.

A useful negative answer would be that the Open API is limited to project/status/document/inspection synchronization while permit-requirement identification remains a managed-service or human-assisted internal step.

No internal customer counts, revenue, proprietary rules or confidential endpoint details are needed to answer this boundary.

## Contact-route constraint

Current public crawling exposes a demo/contact form but no independently verifiable general product email address. Search of ProjectPermit's Gmail found no prior PlanEdge thread.

Do **not** guess an address or misuse a privacy/legal mailbox for product-validation outreach.

The next legitimate outreach route is the published demo/contact form or a future clearly published business contact.

## Decision rule

### Strong negative / kill signal

Trigger a mandatory Go/No-Go score review if PlanEdge confirms, documents or demonstrates that:

1. third-party software can create/send scope/project data through the Open API;
2. the API exposes or triggers the required-permits / municipality-specific checklist result programmatically;
3. that capability applies across meaningful Canadian multi-municipality coverage;
4. production use/economics are credible enough that the external machine contract is not merely a bespoke demo.

This is the serious kill condition already named in `docs/GO_NO_GO_SCORECARD.md`.

### Hold / unresolved

Keep the score unchanged if:

- requirement identification is only internal/managed-service;
- Open API only synchronizes downstream project/status/document/inspection data;
- API access is bespoke but requirement output is not externally reusable;
- 444+ coverage is mainly human specialist research per project rather than a reusable machine requirement layer;
- public evidence remains ambiguous.

### Possible rescue evidence

PlanEdge would indirectly strengthen ProjectPermit's narrow wedge only if the requirement layer is materially human/sales-gated and independent software buyers specifically prefer a low-cost self-serve deterministic evidence/version-linked API instead.

PlanEdge alone cannot provide that buyer-preference evidence.

## Current decision impact

**No score change today.**

Canonical state remains:

> **50/100 — PAUSE / RE-SCOPE; rescue / falsification only.**

What changed is confidence in the competitor's delivered functional overlap, not proof of the final external machine-contract semantic.

The remaining uncertainty is now narrow enough that one substantive yes/no answer or public API document can resolve it. No additional broad PlanEdge feature research is useful.
