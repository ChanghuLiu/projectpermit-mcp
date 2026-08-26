# ProjectPermit Partner Outreach Playbook

Updated: 2026-08-26

## Principle

Do **not** pay marketplace/program fees or spend weeks on certification before proving that a real workflow wants ProjectPermit.

The immediate objective is to find design partners and integration developers who already serve contractors/property managers/construction teams. Use ProjectPermit's live HTTP/MCP surfaces to demonstrate workflow value first. Formal marketplace applications follow when customer demand or a partner makes the integration credible.

## Priority 1 — ServiceTitan ecosystem

### Why

ServiceTitan's current App Marketplace material reports 12,000+ businesses served and 40M+ jobs completed annually. Its V2 APIs expose Jobs, Projects, Invoices, Pricebook and other workflow objects, making job-intake or project-creation time a plausible preflight trigger.

### Official paths

- Partner overview: https://help.servicetitan.com/docs/servicetitan-overview-for-app-marketplace-partners
- App Marketplace Program Guide: https://www.servicetitan.com/legal/app-marketplace-program-guide
- V2 developer onboarding: https://help.servicetitan.com/docs/get-started-with-api-dev-portal-v2
- Partner ecosystem: https://www.servicetitan.com/partners

### Important constraint

The Marketplace program is application-based and may involve program fees, onboarding, sandbox access and certification. Do not enter the paid/certification path solely to test an idea.

The program guidance explicitly says Marketplace apps should solve a specific painful problem and complement rather than replace ServiceTitan core functionality. ProjectPermit fits best as a permit-decision enrichment step, not a new job-management UI.

### Design-partner workflow

`ServiceTitan job/project scope -> normalize work type/address -> ProjectPermit preflight -> attach permit flag/evidence -> estimator/dispatcher decides next step`

Best initial trades:
- HVAC replacement/new installation
- plumbing replacement vs relocation/new plumbing
- roofing/window/deck/structural alteration where supported

### First outreach target

Independent ServiceTitan integration developers/consultancies and existing contractors that already use custom APIs. Ask them to validate the decision point before pursuing Marketplace certification.

## Priority 2 — AppFolio Stack

### Why

AppFolio reported 22,096 property-management customers and 9.4M units under management at 2025 year-end. Stack explicitly supports third-party integrations, including Maintenance and Construction Management categories.

### Official paths

- Partner program: https://www.appfolio.com/stack/become-a-partner
- Partner application: https://www.appfolio.com/stack/partner-application
- Stack marketplace: https://www.appfolio.com/stack/marketplace

### Program path

AppFolio publishes a clear sequence:

1. application / initial review
2. security-compliance review and agreements
3. development/testing
4. final review and marketplace publication

This is more approachable than an invitation-only enterprise program, but still should follow workflow validation rather than precede it.

### Design-partner workflow

`maintenance work order / capex project -> scope classification -> address-aware ProjectPermit check -> route to approval/contractor/permit workflow`

Do not assume an annual permit rate per managed unit. Ask property managers for their actual work-order distribution and permit-research frequency.

## Priority 3 — Procore ecosystem

### Why

Procore reported 17,850 customers at 2025 year-end. Its platform explicitly provides APIs and an App Marketplace, and its core customers are owners, general contractors and specialty contractors.

### Official paths

- Developer platform: https://developers.procore.com/
- Marketplace: https://marketplace.procore.com/
- Partner program: https://developers.procore.com/partner
- Marketplace FAQ: https://marketplace.procore.com/faqs

### Important constraint

Procore's current partner page describes its formal Technology Partner Program as invitation/customer-demand driven, even though developers can build apps and custom integrations through the Developer Platform. Therefore the near-term goal is **not** to obtain partner status.

First demonstrate a customer/custom integration that uses ProjectPermit, then use that demand as evidence for Marketplace/partner onboarding.

### Design-partner workflow

`estimate/project creation/change scope -> ProjectPermit preflight -> permit requirement/evidence field -> deeper permit workflow when required`

## Priority 4 — Autodesk Construction ecosystem

### Why

Autodesk Construction states its platform is trusted by builders on 2M+ projects and provides public API/custom-integration paths plus an AECO/Construction Integration Partner program.

### Official paths

- Construction platform: https://construction.autodesk.com/
- Construction Integration Partner application: https://construction.autodesk.com/partner-signup/
- AECO Technology Partner application: https://www.autodesk.com/partner-signup
- Autodesk Platform Services developer programs: https://aps.autodesk.com/autodesk-developer-programs

### Strategy

Autodesk is attractive for project/design workflows, but partner/certification effort is higher. Treat it as a second-wave channel after a field-service/property workflow proves repeat calls.

## Priority 5 — permit workflow vendors

PermitFlow, Symbium and GreenLite are competitors at the full-workflow level, but they also validate the need for requirements research and jurisdiction routing.

The pitch is not to replace their submission/expediting systems. The potential relationship is:

`ProjectPermit low-cost deterministic preflight/routing -> full permit research/submission workflow only for positive/uncertain cases`

This is especially useful where a full managed permit workflow is too expensive to invoke for every incoming job.

## Outreach message A — integration developer

Subject: deterministic permit-preflight API for contractor/property workflows

Hi — I'm validating a small API/MCP capability for construction workflows. Given a municipality, project scope and optionally an address, ProjectPermit returns a deterministic permit preflight with the triggering rule, official-source evidence and explicit uncertainty.

I'm not building permit submission or another contractor CRM. The intended use is one upstream decision inside an existing job/work-order/project flow: should this scope be routed into a permit workflow, and why?

The current developer preview covers Gatineau, Ottawa, Toronto, Mississauga, Laval, Longueuil and Vancouver; five have first-party municipal address/GIS resolution. I can share a live MCP endpoint or simple HTTP request.

I'm trying to validate one question: does permit research create enough repeated friction in the workflows you build that a machine-readable preflight would be useful? If yes, I'd like to test a few real anonymized scopes and understand expected call volume before building more city coverage.

## Outreach message B — contractor/property platform user

Subject: where does your team decide whether a job needs a permit?

I'm testing a deterministic permit-requirements service for contractor/property software. It takes the proposed work plus municipality/address and returns a preflight result with official evidence; it does not submit the permit or claim municipal approval.

I'm looking for the exact point in real operations where somebody currently stops to research: “does this job need a permit, which approval applies, and is there a property/zoning/heritage issue?”

If your team sees this repeatedly, I'd like to test the live developer preview against a small set of anonymized jobs/work orders. The goal is to measure whether this belongs in the workflow before expanding to more jurisdictions.

## Discovery questions

Ask these before discussing pricing:

1. How many jobs/work orders/projects does the workflow process per month?
2. Roughly what fraction require someone to research permit or jurisdiction requirements?
3. Who performs that research today and how long does it take?
4. At what workflow step would an automated preflight be called?
5. Is a `REQUIRED / LIKELY_NOT_REQUIRED / CONFIRM` result with official evidence enough, or must it also return documents/fees/timelines?
6. Which municipalities represent most of the volume?
7. Would the system call once per job, or multiple times as scope changes?
8. Would `$0.20-$0.50` per address-aware result be trivial, material, or unacceptable at expected volume?
9. Does the buyer prefer per-call usage, monthly commitment, marketplace billing or API-key invoicing?
10. What would prevent production adoption: accuracy, coverage, liability, latency, procurement, integration work, or price?

## Qualification score

Prioritize a lead when most are true:

- repeated monthly job/work-order volume, not one-off homeowner usage
- permit research is currently manual or fragmented
- multiple municipalities are involved
- API/integration capability already exists
- buyer can provide anonymized scope examples
- there is a clear workflow location for the call
- 1,000+ potential calls/month or strategic platform distribution
- buyer values evidence/provenance rather than only a generic AI answer

Deprioritize leads that want full permit expediting, plan review, guaranteed approval, human permit runners, or one-off consumer guidance.

## 20-conversation target mix

For the first validation batch:

- 6 ServiceTitan ecosystem developers/contractors
- 5 property-management/AppFolio ecosystem developers/operators
- 4 Procore/Autodesk construction integration developers
- 3 permit-tech vendors/consultants who can assess upstream routing value
- 2 independent contractor/property AI-Agent builders

The goal is not 20 sales. The goal is to discover whether at least three external developers will actually call the endpoint and whether one workflow can credibly reach 10k+ calls/month.

## Marketplace application gate

Only start a formal marketplace/certification application when at least one is true:

- an existing customer/design partner asks for the native integration;
- the platform team confirms the use case and requests an application;
- a prototype integration already demonstrates repeated calls;
- projected usage and willingness-to-pay justify program/security/certification effort and fees.

Until then, ProjectPermit's public HTTP/MCP developer preview is the faster validation vehicle.
