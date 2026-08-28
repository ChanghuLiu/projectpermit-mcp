# PlanEdge Canada Threat Addendum — 2026-08-28

## Why this is materially closer than prior downstream permit software

A current public scan found PlanEdge Permits, an Ontario-based Canadian permit-management product whose public site goes beyond filing/status/document management and explicitly claims automated permit-requirement determination from project context.

Public claims include:

- Canada-wide support across 444+ municipalities;
- project intake followed by requirements research for the exact permit type, fees, schedules and supplementary requirements for the municipality;
- an automated workflow where a newly added project automatically determines what permits are needed;
- an intelligent intake questionnaire that determines all required permits;
- smart checklists auto-populated from project type, municipality and scope;
- homeowner assessment that identifies every required permit before the customer commits;
- municipal requirements/bylaw interpretation knowledge across jurisdictions;
- an Open API for custom ERP / enterprise-system connections.

Source:

- `https://www.planedgepermits.com/`

This is substantially closer to ProjectPermit's remaining thesis than permit-record APIs, permit-status tools, document-completeness checkers or downstream plan review.

## Exact overlap

ProjectPermit's current narrow contract is approximately:

`project scope + municipality/address + decisive facts`

→ `permit required / likely not required / confirm`

PlanEdge publicly describes a workflow of:

`project type + municipality + scope / intake answers`

→ `determine all required permits + build municipal submission checklist`

That is an exact product-function overlap at the requirement-identification layer, even though the visible output vocabulary and safety contract differ.

PlanEdge also bundles the result into preparation, submission, tracking, revisions and inspections. This means it competes not only as a checker but as a broader permit-operations service.

## Important API boundary still unresolved

PlanEdge separately advertises a RESTful Open API for custom ERP and enterprise integrations.

The public page does **not** clearly state whether third-party software can call the requirement engine directly (for example, submit project type/municipality/scope and receive required permits/checklists) or whether the API is limited to permit records/status/documents/workflow synchronization.

That distinction matters:

- if the Open API exposes the requirement engine, PlanEdge is very close to the explicit ProjectPermit stop condition: an already-available cross-jurisdiction permit-specific machine interface;
- if the API only synchronizes downstream permit data and requirement identification remains tied to PlanEdge's managed service, ProjectPermit's narrow self-serve API delivery contract still differs materially.

## Delivery / credibility caveat

The current public evidence is strong product-positioning evidence but weak independent delivery evidence.

PlanEdge's site claims:

- founded in Toronto in 2022;
- 444+ municipality coverage;
- national contractor/homebuilder customers;
- thousands of permit applications in its analytics dataset;
- active relationships across Canada.

However, the current independent public footprint found in this review is much smaller:

- PlanEdge's LinkedIn page indexed with only a few followers;
- no independently named customer case study was found in the current search;
- a search-engine snapshot from roughly five months earlier shows a much simpler site under the same domain;
- the rich current website appears to have expanded substantially in 2026.

Sources:

- `https://www.linkedin.com/company/planedge-permits/` (public search footprint)
- historical search-engine snapshot for `planedgepermits.com`

Therefore the 444+ municipality / customer / performance claims must remain **vendor-asserted and unverified** until there is independent evidence or a direct product response.

This is important because ProjectPermit should not enter No-Go solely because an uncorroborated website claims broad delivery.

## Why this still changes the competitive picture

Even with delivery-scale uncertainty, the public site demonstrates a product architecture and commercial positioning that directly attacks the last remaining ProjectPermit whitespace:

- cross-municipality maintenance;
- permit-requirement identification from scope/location;
- contractor/homeowner preconstruction insertion;
- enterprise integration;
- human permit specialists for uncertain cases;
- full downstream permit operations.

GoBuild already showed that permit-needs prediction can be embedded inside contractor software. PlanEdge now shows that a Canadian cross-jurisdiction permitting vendor is publicly positioning the same requirement-identification step as part of a national service.

The remaining ProjectPermit differentiation is narrower still:

> self-serve, deterministic, evidence/version-linked, low-cost per-call API output without a managed permit specialist or full filing engagement.

## Falsification questions

The two highest-value questions for PlanEdge are:

1. **Does the Open API expose permit-requirement determination?**
   Can external software submit project type + municipality/address + scope and receive the required permit types/checklist without a human-managed PlanEdge project?

2. **How automated is 444+ municipality coverage?**
   Is requirement determination primarily rule/data driven and reusable across customers, or is the result produced through permit-specialist research per project?

A third useful commercial question is pricing for requirement-only/API use versus full permit-management service.

## Score implication

### Immediate result: hold the canonical score at 51/100 pending delivery/API verification

This evidence is stronger than ordinary adjacent competition, but the current public record has two unresolved weaknesses:

- independent delivery/adoption evidence is thin;
- public documentation does not prove that the Open API exposes the requirement-identification engine.

Therefore this review does **not yet** reduce competitive headroom from 1/10 to 0/10.

### Automatic downgrade trigger

Reduce competitive headroom to 0/10 and recalculate the canonical score immediately if credible evidence confirms either:

- PlanEdge's Open API exposes project-context permit-requirement output across multiple Canadian municipalities at practical external-software economics; or
- an independent customer/integration confirms repeated production use of PlanEdge's automated cross-municipality requirement engine at meaningful scale.

At the current scorecard arithmetic, a one-point reduction in competitive headroom would move weighted total from 50.5 to 49.5 (display score about 50), placing ProjectPermit at the explicit stop boundary and requiring a formal pause/re-scope review rather than ordinary validation-only continuation.

## Bottom line

PlanEdge is now one of the highest-priority competitive falsification targets because it publicly claims the exact upstream function ProjectPermit still considered relatively open: **scope/location → required permits** across Canada.

The only reason not to downgrade immediately is evidence quality, not product overlap.

The next action is verification, not more ProjectPermit engineering.