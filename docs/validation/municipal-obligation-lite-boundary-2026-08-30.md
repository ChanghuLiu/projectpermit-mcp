# Municipal obligation-lite boundary — 2026-08-30

## Purpose

Test whether ProjectPermit has a meaningful next value layer between:

`permit required? yes/no`

and the deeper licensed-content Layer C:

`full current building-code/regulatory obligations`

The candidate fallback is intentionally narrower:

> **permit-positive project facts -> current municipal submission/process obligation bundle + official evidence + freshness/change identity**

This is a market/product boundary note only. It does **not** authorize implementation.

## 1. Why this boundary matters

Current licensing research shows that deep Ontario technical Building Code content depends on NRC NBC 2020 + the Ontario Amendment Document and cannot safely be assumed to be a free commercial corpus.

However, municipalities publish substantial operational requirements around a permit workflow outside the protected technical code corpus.

If buyers value these operational obligations, ProjectPermit could potentially deepen value before or without reproducing code text.

The product must not label this as `building-code compliance` unless it actually has the rights/data/logic required for that claim.

## 2. Representative Ottawa evidence

### Part 9 residential additions / renovations / accessory structures

Ottawa publicly lists project-specific submission requirements including, depending on the project:

- completed digital permit application;
- scaled/dimensioned construction drawings;
- Schedule 1 identifying BCIN designer / architect / engineer / homeowner exemption;
- septic approval where applicable;
- Energy Efficiency Design Summary where applicable;
- Mechanical Design Report / layouts where applicable;
- truss / engineered joist manufacturer packages;
- professional-engineer excavation/shoring design where applicable;
- engineered guard documentation where applicable;
- testing/BMEC/CCMC reports for alternative materials where applicable.

Official source:

- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/planning-your-project/building-permit-application-submission-requirements-part-9-residential/new-buildings-additions-renovations-and-accessory-structures-submissions

This is already much richer than a binary permit determination because the result can change what the estimator/project team must obtain before application or construction.

### Timelines and inspections

For an additional-dwelling-unit workflow, Ottawa currently publishes:

- an approximate first-review timeline of 15 business days;
- required inspections at key stages;
- a direction to book inspections approximately 48 hours in advance;
- a warning that missed inspections can require work to be exposed or lead to orders.

Official source:

- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/adding-apartment-additional-dwelling-units

This establishes that municipality-published process obligations can affect schedule and execution sequencing, not merely application paperwork.

### Fees

Ottawa's 2026 Building Code Services Fee Schedule contains current permit/revision/reinspection/conditional-permit and other charges.

Official source:

- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/forms-applications-and-fees/comprehensive-building-code-fee-schedule

Example structure includes valuation-based construction permit fees, minimum fees, revision fees, refundable inspection fees and reinspection fees.

The exact amount depends on project type/valuation and must be computed from current official rules rather than hard-coded as one universal number.

## 3. Representative Toronto evidence

Toronto's project-specific Building Permit Application Guides publish operational requirements by project class.

Current examples include:

- application forms and project-specific screening forms;
- drawing/signature/designer-responsibility requirements;
- BCIN / architect / engineer information where applicable;
- application route;
- current permit fee formula/rates;
- project-specific outside approvals or extra forms.

Official examples:

- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/building-permit-application-guides/guides-for-other-buildings/non-residential-building-permit/
- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/building-permit-application-guides/guides-for-other-buildings/interior-alterations-non-residential/
- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/building-permit-fees/

Toronto's 2026 fee material is sufficiently structured to affect quote allowance/cost planning, while project guides can affect required professional/design documentation.

## 4. Candidate obligation bundle

A representative `municipal_process_obligations` object could eventually contain categories such as:

- `submission_documents`
- `professional_or_designer_requirements`
- `related_approvals`
- `permit_fee_basis`
- `estimated_review_timeline`
- `required_inspection_stages`
- `inspection_booking_lead_time`
- `permit_revision_requirements`
- `special_project_screening`
- `official_sources`
- `source_version_or_verified_at`
- `missing_facts`

This is a conceptual data contract, not an implementation commitment.

Every item needs conditional applicability, evidence and a safe unknown state. A generic checklist copied from a website is not sufficient.

## 5. Why this can be higher value than permit yes/no

A binary permit signal answers whether the workflow exists.

An operational obligation bundle can answer what must change next in the real work record:

- add an engineer/designer task;
- request a missing drawing/report;
- add a permit/inspection allowance;
- avoid scheduling construction before required approvals;
- add review/inspection lead time;
- flag a related municipal licence/screening process;
- create inspection-stage tasks;
- attach official evidence to the quote/job record.

This aligns well with ProjectPermit's existing `action_bundle`, `tasks`, `required_inputs`, `routing`, `evidence`, `identity/change` and safe-writeback proposal architecture.

## 6. Important difference from full Layer C

### Municipal obligation-lite can cover

- application/process requirements;
- forms/documents;
- current municipal fees;
- published service/review timelines;
- inspection scheduling/process;
- professional/document dependencies explicitly published by the municipality;
- related municipal approvals/licences;
- source freshness/change monitoring.

### It cannot honestly claim to cover

- full technical building-code compliance;
- structural/fire/accessibility/energy design requirements hidden in incorporated code documents;
- complete code-section logic;
- every condition where a professional is legally required if the rule is only discoverable through protected technical code content;
- plan review/compliance certification.

The boundary must remain visible in API naming and marketing.

## 7. Rights/copyright caution

Official public availability is **not the same thing as a blanket commercial-reuse licence**.

Before commercializing a maintained structured corpus from municipal pages, ProjectPermit still needs source-by-source rights/terms review and should minimize reproduction of expressive text.

A safer architecture may often be:

- independently structured factual fields;
- short normalized labels;
- official URLs/citations;
- source/version/freshness metadata;
- no large copied passages;
- explicit source-specific rights classification.

This note does not provide a legal opinion that municipal website content is freely reusable.

## 8. Market-risk boundary

This fallback may be easier to source than deep code obligations, but it could also be less valuable because:

- municipalities already provide project guides and online submission systems;
- a contractor who rarely files permits may not pay for automated checklist normalization;
- downstream permit-management vendors may already handle the process after permit need is known;
- the workflow may be one call/project rather than high-frequency repeated use.

Therefore do not build it merely because the data is available.

The same buyer gate applies:

> Does this bundle materially change quote scope/cost/schedule/handoff often enough that a platform wants it maintained externally?

## 9. Relationship to Contrax E1

Contrax explicitly expressed more interest in updated legal/regulatory/building-code information than in a binary permit-required checker.

Municipal obligation-lite partially moves in that direction but does **not** fully satisfy the stated building-code-content interest.

Therefore it is best treated as:

- a licence-light **fallback/representative E3 slice** if buyers confirm process obligations are valuable; or
- an intermediate layer combined with licensed technical content later.

It is not evidence that Contrax would buy it.

## 10. Build gate

Do not implement this layer yet.

A representative prototype becomes justified only when at least one qualified buyer/platform gives a bounded workflow and identifies one or more of these process obligations as materially useful.

If that happens, the smallest E3 slice should use:

- one project family;
- one or two municipalities;
- only the 3–5 obligation types named by the buyer;
- current official sources;
- explicit freshness/source identity;
- no protected technical code ingestion unless rights are already clear.

This keeps cash cost low and measures the actual workflow consequence before licensing or broad content expansion.

## Bottom line

**There is a real value layer between `permit yes/no` and full licensed building-code compliance.** Ottawa and Toronto already publish enough official operational information to support a richer project-specific permit-process bundle.

But availability is not demand, and public availability is not automatically commercial-reuse permission.

The correct role for this layer is therefore:

> **licence-light fallback / representative validation slice — not speculative product expansion.**
