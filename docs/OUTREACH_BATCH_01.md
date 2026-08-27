# ProjectPermit Outreach Batch 01

Updated: 2026-08-27

Status: **prepared, not sent**

This batch is intentionally optimized for learning and repeated-call validation, not broad sales. No message should be sent until the owner approves external outreach and the sender identity/contact details to use.

## What we are validating

A good conversation should answer four questions:

1. Where in the existing workflow does a human currently stop to research municipal permit requirements?
2. How many times per month could that decision occur?
3. Is a deterministic `REQUIRED / LIKELY_NOT_REQUIRED / CONFIRM` result with official-source evidence useful enough to automate the first routing decision?
4. Would roughly `$0.20-$0.50` per address-aware result be acceptable at the expected call volume?

Do not pitch ProjectPermit as permit submission, guaranteed approval, legal advice, engineering review, or a replacement for the partner's core product.

## Batch order

### 1. iPermit — ServiceTitan / permitting

Public route: `STSupport@iPermitUSA.com`

Why first: direct permitting workflow, ServiceTitan integration, and public evidence of a contractor sending roughly 80+ jobs/month. This is the cleanest test of whether a cheap upstream preflight can save full-workflow effort.

Subject: `Upstream permit preflight before an iPermit order?`

Draft:

Hi iPermit team — I'm validating ProjectPermit, a small deterministic API/MCP that takes municipality + project scope + optional address and returns an evidence-linked permit preflight. It does not submit permits or replace expediting.

Your ServiceTitan workflow is exactly the kind of downstream system I'm trying not to rebuild. The question is whether a low-cost first-pass decision is useful before a contractor opens a full permitting workflow: `job scope -> preflight -> only route positive/uncertain cases into iPermit`.

The current developer preview covers seven Canadian jurisdictions and five first-party municipal address/GIS adapters. I'm looking for a design partner willing to test a few anonymized scopes and tell me whether this decision happens often enough to matter.

The key number I'm trying to learn is simple: for a contractor sending you N jobs/month, how many require manual research merely to decide whether permitting is needed before the full permit process starts?

### 2. Property Meld — AppFolio / property maintenance

Public route: `support@propertymeld.com` or public demo path

Subject: `Permit preflight inside property-maintenance work orders`

Draft:

Hi Property Meld team — I'm testing a deterministic permit-requirements API for property-maintenance workflows. Given a municipality, work scope and optionally an address, it returns a permit preflight with the triggering rule, official-source evidence and explicit uncertainty.

I noticed Property Meld already coordinates the maintenance workflow from request through vendor work and invoice sync. I'm trying to validate whether a permit decision belongs upstream of dispatch/approval for a subset of Melds, especially structural, plumbing, window/door, deck and renovation work.

I am not proposing another maintenance UI or managed permit service. The intended integration is one machine call that decides whether a work order should be routed into a deeper permit workflow.

Would your team be open to testing a small anonymized set of work orders and estimating how often this research occurs per month?

### 3. Lula — AppFolio / maintenance contractor network

Public route: partnerships page / `913-513-4480`

Subject: `Permit-risk routing before dispatching a maintenance job`

Draft:

Hi Lula team — I'm validating ProjectPermit, a deterministic API/MCP for municipal permit preflight. It takes a work scope plus municipality/address and returns an evidence-linked `required / likely not required / confirm` result.

Lula's work-order routing and Partner API make it a strong fit for the workflow question I'm studying: before a job is dispatched to a Pro, is there a repeated need to determine whether the work itself triggers municipal permitting or property-specific review?

The product is deliberately upstream of contractor dispatch and permit submission. I would like to test a few anonymized work-order categories and learn whether this could remove manual research without adding workflow friction.

The commercial hypothesis is usage-based API pricing, roughly $0.20-$0.50 per address-aware preflight if the volume supports it.

### 4. Provizual — Procore / AHJ inspection workflow

Public route: `sales@provizual.com`

Subject: `Upstream permit-requirements signal for AHJ inspection workflows`

Draft:

Hi Provizual team — your Procore integration already connects AHJ/city inspection activity into project QA/QC. I'm validating a complementary upstream capability: a deterministic municipal permit preflight before permit/inspection tracking begins.

ProjectPermit converts municipality + structured scope + optional address into an evidence-linked permit determination and preserves uncertainty rather than inventing an answer. It currently covers seven Canadian jurisdictions.

The integration hypothesis is: `new project/scope -> ProjectPermit preflight -> if required/uncertain, create or enrich the downstream permit/inspection workflow`.

Would that upstream signal be useful in the workflows you see, or is permit applicability already known by the time Provizual enters the process? A few anonymized project examples would be enough to test the fit.

### 5. AppWork — AppFolio / maintenance operations

Public route: `sales@appworkco.com`

Subject: `Permit preflight at work-order / estimate approval time`

Draft:

Hi AppWork team — I'm testing a small deterministic permit-preflight API for maintenance operations. It takes the proposed work, municipality and optional address and returns an official-source-backed requirement result.

AppWork already has structured work orders, inspections and technician workflows, which creates a natural decision point before scheduling or estimate approval. I'm trying to learn whether teams repeatedly stop there to research whether a repair/renovation needs a building/plumbing/structural permit.

I am not building maintenance coordination or permit submission. The goal is one low-latency API call that adds a permit flag, evidence and explicit uncertainty to the existing workflow.

Would you be open to testing a handful of anonymized work-order scopes and telling me the rough monthly frequency of this decision?

### 6. ServiceChannel — ServiceTitan / facilities work orders

Public route: ServiceTitan Marketplace `Get Started`

Subject: `Municipal permit preflight for incoming facilities work orders`

Draft:

Hi ServiceChannel team — I'm validating a deterministic municipal permit-preflight API for multi-location field-service workflows.

Because ServiceChannel work orders can flow into ServiceTitan with location, trade/category and booking-summary context, I want to test whether permit research could be automated before acceptance/scheduling for relevant scopes.

The service returns a machine-readable permit decision with official evidence and explicit uncertainty. It does not submit permits or replace ServiceChannel/ServiceTitan workflows.

The question I want to validate is whether multi-location providers see enough repeated permit-research friction for this to become a standard routing step. If yes, I'd like to test a small anonymized sample and estimate monthly call volume.

### 7. PermitFlow — Procore / full permitting

Public route: `sales@permitflow.com`

Type: competitor/partnership learning; do not position as a head-on replacement.

Subject: `Low-cost permit preflight as an upstream routing layer`

Draft:

Hi PermitFlow team — I'm building ProjectPermit, a narrow deterministic preflight layer rather than a permit-management/submission platform.

The intended use is upstream of a full permitting workflow: call a low-cost municipality/scope/address rules service on every incoming project, then route only positive or uncertain cases into deeper permit research, filing and tracking.

I'm trying to validate whether that separation is useful to a platform already doing end-to-end permitting, or whether your own workflow makes the first-pass decision essentially free.

The current preview covers seven Canadian jurisdictions and returns official-source evidence with each determination. I'd value a technical/product conversation about where this kind of routing signal would or would not add value.

### 8. Pulley — Procore / full permitting

Public route: `hello@withpulley.com`

Type: competitor/partnership learning.

Subject: `Preflight signal before opening a permitting project`

Draft:

Hi Pulley team — I'm validating a narrow permit-requirements API that sits before full permit management. ProjectPermit takes municipality + scope + optional address and returns a deterministic, evidence-linked requirement result.

Pulley's Procore workflow already handles documents, checklists, submission and status. The hypothesis I'm testing is whether an upstream preflight could cheaply answer `does this scope belong in a permitting workflow at all, and why?` before a Pulley project is created.

I'm not trying to duplicate submission/tracking. I'm looking for feedback on whether this routing layer removes real work or simply duplicates a decision your customers already know.

### 9. SyncEzy — Procore integration specialist

Public route: `support@syncezy.com`

Subject: `Reusable permit-preflight component for Procore integrations`

Draft:

Hi SyncEzy team — I'm validating ProjectPermit, a deterministic permit-requirements API/MCP intended to be embedded inside existing contractor/construction workflows rather than sold as another project-management UI.

You already build and operate Procore integrations for many customers, so I'm particularly interested in whether permit research appears as a recurring custom-integration gap. The service can enrich a project/work scope with an official-source-backed permit flag and explicit uncertainty.

Would this be useful as a reusable connector/API component in customer-specific workflows? If you have one or two anonymized examples where teams manually research municipality requirements, I can test them against the live developer preview.

### 10. Calance — cross-platform construction/real-estate integrator

Public route: public consultation form

Subject: `Permit-requirements API as a reusable construction integration component`

Draft:

Hi Calance team — I saw that you connect Procore, Autodesk, AppFolio, Northspyre and other construction/real-estate systems, including custom point solutions where core platforms have workflow gaps.

I'm validating one such reusable component: ProjectPermit, a deterministic municipal permit-preflight API/MCP. Given municipality + project scope + optional address, it returns an evidence-linked requirement decision without attempting submission or legal/design review.

I'm trying to learn whether permit-research gaps recur across enough client integrations to justify treating this as a reusable capability rather than building bespoke logic each time.

If you have anonymized examples of that workflow, I can test the current seven-jurisdiction preview and compare the result to the manual process.

## Response classification

Record every reply as one of:

- `A — integration interest`: willing to test live endpoint or provide real scopes
- `B — workflow confirmed`: pain is real and repeated, but no integration yet
- `C — weak pain`: occasional research, no repeated-call path
- `D — wrong layer`: permit applicability already known / full workflow starts earlier
- `E — coverage blocker`: need unsupported municipalities before testing
- `F — procurement/security blocker`

## Success gate for Batch 01

Do not judge success by reply count alone. The batch passes only if it produces at least one of:

- one external integration calling the endpoint 20+ times;
- two or more organizations providing anonymized real scopes;
- one credible workflow with 1,000+ monthly potential calls;
- one buyer/partner who says `$0.20-$0.50` per address-aware result is acceptable.

If all positive replies require full permit submission, guaranteed approvals, or human expediting, ProjectPermit's current product boundary is wrong and should be reconsidered before more city expansion.
