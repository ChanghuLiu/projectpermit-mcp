# ProjectPermit Outreach Batch 02

Updated: 2026-08-27

Status: **prepared, not sent**

Batch B is designed to test six distinct distribution positions without repeating the exact same hypothesis from Batch A. Messages are intentionally shorter than Batch A and should read as workflow-validation outreach, not sales copy.

## Batch B targets

### 1. Lula — property maintenance / Partner API

Current public route: Lula Partnerships page / Partner API page / sales phone `913-513-4480`.

Why: Lula has a Partner API for platforms that send maintenance work orders into its contractor network. This is a direct repeated-work-order surface.

Subject: `Permit-risk routing before maintenance dispatch`

Draft:

Hi Lula team — I’m validating ProjectPermit, a deterministic API/MCP that turns municipality + work scope + optional address into an evidence-linked permit preflight.

Lula’s Partner API is the kind of workflow I’m studying: before a work order is dispatched to a Pro, does someone repeatedly need to determine whether the scope triggers building/plumbing/structural permitting?

I’m not building dispatch or permit submission. The intended use is one upstream routing call inside an existing maintenance flow.

If that decision happens often enough to matter, I’d like to test 20 anonymized work-order scopes and estimate the monthly call volume.

Best,
ProjectPermit
Independent developer

### 2. ServiceChannel — facilities work orders / ServiceTitan integration

Current public route: ServiceChannel `Contact Sales` / `Integration Services` / integration specialist form. ServiceTitan’s current marketplace listing confirms work-order data flows from ServiceChannel into ServiceTitan, including location, trade/category and booking-summary context.

Why: multi-location facilities work orders create a strong jurisdiction + scope routing hypothesis.

Subject: `Permit preflight for incoming facilities work orders`

Draft:

Hi ServiceChannel team — I’m testing a deterministic municipal permit-preflight API for multi-location facilities workflows.

Because ServiceChannel work orders already carry location, trade/category and problem-summary context into downstream systems such as ServiceTitan, I want to validate one narrow step: can relevant work orders be automatically preflighted for permit risk before acceptance, scheduling or quote finalization?

ProjectPermit returns an official-source-backed `required / likely not required / confirm` result. It does not submit permits.

If this decision is repeated in your provider workflows, I’d like to test a small anonymized sample and estimate calls/month.

Best,
ProjectPermit
Independent developer

### 3. Calance — construction / real-estate integration consultancy

Current public route: `connect@calance.com` for general and partnership inquiries.

Why: Calance builds custom integrations across construction/real-estate systems, making it a possible multiplier rather than a single end customer.

Subject: `Reusable permit-preflight component for construction integrations`

Draft:

Hi Calance team — I’m validating ProjectPermit, a deterministic municipal permit-requirements API/MCP intended to plug into existing construction and property workflows.

The question is whether permit-research logic recurs often enough across custom integrations to justify a reusable component instead of rebuilding city-by-city logic for each client.

ProjectPermit currently normalizes project scope across seven Canadian jurisdictions, returns official-source evidence, and preserves uncertainty instead of guessing.

If your clients repeatedly hit this gap, I’d like to test a few anonymized examples and understand the likely monthly call volume before expanding coverage.

Best,
ProjectPermit
Independent developer

### 4. Outbuild — Procore scheduling / roadblocks

Current public route: `sales@outbuild.com` on the current Procore Marketplace listing. The listing currently shows 2,777 installs; Outbuild’s own site says 400+ customers and $50B+ in active projects.

Why: permit dependencies are natural schedule roadblocks. This tests whether the preflight belongs early enough to affect planning.

Subject: `Permit risk as an early project roadblock`

Draft:

Hi Outbuild team — I’m validating a small deterministic permit-preflight API for construction workflows.

Outbuild already turns RFIs and other dependencies into schedule roadblocks. I’m testing whether municipal permit applicability is another early dependency worth detecting automatically at project/scope creation.

The service takes municipality + structured scope + optional address and returns an evidence-linked `required / likely not required / confirm` result. It does not manage submissions.

Would this signal be useful before schedule commitments are made, or is permit applicability already known by then? A few anonymized examples would be enough to test the fit.

Best,
ProjectPermit
Independent developer

### 5. PermitFlow — full permitting platform / competitor learning

Current public route: `sales@permitflow.com` on the current Procore Marketplace listing.

Why: PermitFlow explicitly covers permit requirements, preparation, submission, tracking and management. This is a deliberate wedge test: does a cheaper upstream filter add anything, or is the first-pass decision already effectively free inside a full platform?

Subject: `Would an upstream permit-preflight layer add value?`

Draft:

Hi PermitFlow team — I’m building ProjectPermit as a narrow deterministic preflight layer, not a permit-management platform.

The hypothesis is simple: a contractor/property system calls a low-cost permit-requirements check on every incoming scope, then sends only positive or uncertain cases into a full permitting workflow.

Because PermitFlow already handles end-to-end research and submission, you are a useful reality check: does that upstream routing layer remove real work, or does it duplicate a decision your platform already makes cheaply?

I’d value a short product/technical answer, even if the conclusion is that this layer is unnecessary.

Best,
ProjectPermit
Independent developer

### 6. Pulley — full permitting platform / multi-site commercial

Current public route: `hello@withpulley.com`. Pulley currently positions itself as an end-to-end permitting partner across large commercial and multi-site projects and states coverage across 20,000+ jurisdictions.

Why: this tests whether the wedge survives against a scaled commercial permitting workflow, especially repeated multi-site programs.

Subject: `Preflight before opening a full permitting workflow`

Draft:

Hi Pulley team — I’m validating ProjectPermit, a deterministic municipal permit-preflight API that sits upstream of full permit management.

The workflow hypothesis is: call a cheap municipality/scope/address preflight on every incoming project, then open a deeper permitting workflow only when the result is required or uncertain.

Pulley already operates at multi-site commercial scale, so I’m trying to learn whether that separation removes meaningful work or simply duplicates a step your team already performs efficiently.

If useful, I can share the live developer preview or test a handful of anonymized scopes.

Best,
ProjectPermit
Independent developer

## Recommended send order

Do not send all six simultaneously. Recommended order after Batch A has had time to breathe:

1. Calance
2. Lula
3. ServiceChannel
4. Outbuild
5. PermitFlow
6. Pulley

This order favors integration/distribution partners before direct permit-platform competitors.

## Evidence used to re-verify routes

- Lula Partner API / Partnerships: https://lula.life/partner-api and https://lula.life/partnerships
- ServiceChannel contact / integration services: https://servicechannel.com/contact/ and https://servicechannel.com/tools/provider-support-contact-us/
- ServiceTitan ServiceChannel listing: https://marketplace.servicetitan.com/partner/servicechannel
- Calance contact: https://www.calanceus.com/contact-us
- Outbuild Procore listing: https://marketplace.procore.com/apps/outbuild
- PermitFlow Procore listing: https://marketplace.procore.com/apps/permitflow
- Pulley: https://www.withpulley.com/ and https://marketplace.procore.com/apps/pulley

No message in Batch B has been sent.