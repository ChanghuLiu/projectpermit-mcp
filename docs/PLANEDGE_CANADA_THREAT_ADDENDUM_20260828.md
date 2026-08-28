# PlanEdge Canada Threat Addendum — live re-verification 2026-08-28

## Why this remains one of the closest Canadian overlaps

A fresh 2026-08-28 re-verification of PlanEdge Permits' current public site confirms that the product still goes beyond filing/status/document management and explicitly claims automated permit-requirement determination from project context.

Current public claims include:

- Canada-wide support across **444+ municipalities/jurisdictions**;
- project intake followed by requirements research for the exact permit type, fees, schedules and supplementary requirements for the municipality;
- a Workflow Automation flow where a newly added project **automatically determines what permits are needed**;
- an **intelligent intake questionnaire determines all required permits**;
- Smart Checklists where permit requirements are auto-populated from **project type, municipality and scope**;
- homeowner assessment that identifies every required permit before the customer commits;
- municipal requirements/bylaw interpretation knowledge across jurisdictions;
- an Open API / RESTful API for custom ERP / enterprise-system connections.

Current source:

- `https://www.planedgepermits.com/`

These statements were re-observed in the current indexed site on 2026-08-28 rather than carried forward only from an older snapshot.

## Exact functional overlap is now re-verified as current

ProjectPermit's narrow contract is approximately:

`project scope + municipality/address + decisive facts`

→ `permit required / likely not required / confirm`

PlanEdge's current Workflow Automation copy describes:

`new project + project type + municipality + scope / intake answers`

→ `automatically determine required permits + build municipal submission checklist`

Its current Property Owners page separately says PlanEdge assesses a project, identifies every required permit and offers a free permit assessment before the customer commits.

Therefore the **functional requirement-identification overlap is current and real at the public-product-claim level**.

PlanEdge also bundles that result into preparation, submission, tracking, revisions and inspections. It competes as a broader permit-operations service rather than only as a lightweight checker.

## Critical Open API boundary remains unresolved

PlanEdge's current Integrations page continues to advertise an Open API:

> RESTful API lets your dev team connect PlanEdge to any internal system or ERP platform.

However, the surrounding current integration examples are framed around **permit data synchronization**:

- approved/rejected permit information flowing into project-management tools;
- permit status, documents and inspection dates syncing into Procore;
- drawings/feedback syncing through Autodesk Construction Cloud;
- generic custom ERP connectivity.

The public site still does **not** document an endpoint/schema equivalent to:

`project type + municipality/address + scope`

→ `required permits / requirement checklist`

for external third-party software without opening a managed PlanEdge project.

No public developer portal, endpoint documentation, OpenAPI schema or requirement-engine request/response example was found in this re-verification.

That distinction remains decisive:

- if the Open API exposes the requirement engine as an ordinary external machine contract, PlanEdge would closely match the explicit remaining ProjectPermit contract;
- if the API primarily synchronizes downstream permit/project data while requirement identification stays inside PlanEdge's own managed workflow, ProjectPermit's self-serve deterministic API contract remains narrower.

**Do not infer requirement-engine API access merely from the words `Open API`.**

## Current delivery evidence is still weaker than the product claims

The current site continues to claim:

- founded in Toronto in 2022;
- first Ontario clients in late 2022;
- platform launched in 2023;
- expanded coast-to-coast / 444+ municipalities by 2024;
- national contractor/homebuilder customers;
- analytics based on thousands of permit applications;
- current trusted use by contractors, developers, architects and property owners.

But independent production evidence remains thin in the public record reviewed here.

### Anonymous customer evidence

Current testimonials still use names/roles such as:

- Jennifer K., COO — National HVAC Contractor;
- Carlos M., CEO — National General Contractor;
- David L., Director of Construction — Regional Homebuilder, Ontario.

The customer companies are not named, so these cannot independently establish production scale or repeated usage.

### Several interfaces remain marked `Interactive Demo Coming Soon`

The current site marks multiple product/interface areas as forthcoming interactive demos, including Workflow Automation, Integration Hub and several role-specific dashboard views.

This does **not** prove the underlying capabilities are undelivered. But it materially limits what can be independently verified from the public interface and means marketing copy should not be treated as equivalent to a usable external product surface.

### Managed-service delivery remains explicit

Current contact/enterprise copy says a **dedicated permit specialist is assigned from day one**. The homeowner page says a **real permit specialist handles the file**.

This is important because it confirms that human-assisted permit operations remain part of PlanEdge's visible delivery model even while workflow automation is advertised.

Therefore the current public evidence supports:

> `automated requirement-identification capability is claimed`

but does not yet establish:

> `fully unattended, externally callable requirement engine at 444+ municipality production scale`.

## Why this still matters despite LandLogic / Parcella already closing competitive headroom

The canonical scorecard has already moved to **50/100, PAUSE / RE-SCOPE**, with competitive headroom at **0/10**, after the stronger Parcella / One Ontario delivery review.

Therefore PlanEdge no longer controls a simple `51 → 50` score transition.

Its role is now different:

- **functional overlap re-verification** strengthens the conclusion that requirement identification itself is not unique;
- confirmation of an externally callable requirement API would further weaken the surviving `deterministic/self-serve machine contract` wedge;
- independent production evidence would strengthen the case for No-Go / deeper re-scope rather than merely change competitive-headroom arithmetic that is already at zero.

Do not double-count the same competitive dimension by subtracting another point from a 0/10 category.

## Current remaining ProjectPermit wedge versus PlanEdge

The remaining public difference is narrower than the function itself:

### ProjectPermit

- self-serve machine-first contract;
- deterministic rule IDs;
- explicit source/evidence/version history;
- fail-safe `CONFIRM` / unknown-state behavior;
- proposed very low per-call economics;
- no required permit-specialist engagement per ordinary call.

### PlanEdge current public model

- broader end-to-end permit management;
- current requirement-identification automation claims;
- project preparation/submission/tracking/inspection operations;
- dedicated permit-specialist support;
- generic Open API / enterprise integration;
- no public requirement-engine endpoint/schema/pricing contract found.

None of ProjectPermit's narrower differences has buyer E2/E4/E5 validation.

## Highest-value falsification questions

The highest-value questions remain:

1. **Does the Open API expose permit-requirement determination?**
   Can external software submit project type + municipality/address + scope and receive required permit types/checklists without a human-managed PlanEdge project?

2. **How automated is 444+ municipality coverage in production?**
   Is requirement determination primarily reusable rule/data/software logic, or does a permit specialist research/verify most projects?

3. **Can a customer buy requirement-only/API use?**
   Is there a standalone machine/API commercial model, or only broader project/retainer permit-management pricing?

4. **Can any named customer/integration independently confirm repeated production use?**

These are direct falsification questions. More ProjectPermit engineering does not answer them.

## Current evidence classification

| Claim | Current status |
|---|---|
| Scope/location → required-permit functionality | **Current vendor claim re-verified** |
| 444+ municipality coverage | **Current vendor claim, independently unverified** |
| Automated intake / Smart Checklist | **Current vendor claim re-verified** |
| Open REST API exists | **Current vendor claim re-verified** |
| Open API exposes requirement engine | **Unverified** |
| Named independent production customer | **Not found** |
| Requirement-only API pricing | **Not found** |
| Fully unattended requirement determination | **Unverified; visible specialist model remains** |

See also:

- `data/planedge_public_claims_20260828.csv`
- `docs/GO_NO_GO_SCORECARD.md`

## Score implication

**No immediate score change. Canonical status remains 50/100, PAUSE / RE-SCOPE.**

Why:

- competitive headroom is already 0/10 after Parcella / One Ontario;
- the live re-check confirms PlanEdge functional overlap but does not independently verify production scale or the exact external requirement-engine API contract;
- public API copy remains too generic to assume the requirement engine is externally callable;
- external buyer preference, real usage and willingness to pay for ProjectPermit's narrower contract remain unvalidated.

### Stronger No-Go / re-scope trigger

Treat PlanEdge as materially stronger falsification evidence if credible evidence confirms either:

- its Open API exposes project-context permit-requirement output across multiple Canadian municipalities at practical external-software economics; or
- a named independent customer/integration confirms repeated production use of the automated cross-municipality requirement engine at meaningful scale.

That evidence should trigger a formal canonical decision review. It should **not** be represented as another automatic competitive-headroom point because that category is already at zero.

## Bottom line

PlanEdge's closest-overlap claims survive current re-verification:

> **new project / municipality / scope → automatically determine required permits**

is still publicly advertised in Canada.

But the exact machine-contract threat remains unproven:

> **external software → Open API → requirement engine output**

is not documented publicly.

Therefore PlanEdge remains a high-priority falsification target, not verified proof that ProjectPermit's exact external contract is already commoditized.
