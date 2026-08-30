# PCC-like Vancouver license-light representative E3 slice — 2026-08-30

## Purpose

Define the **smallest representative Layer-C E3 case** that could be built quickly if a PCC-like Vancouver buyer crosses the E2 gate.

This is a readiness specification only. It does **not** authorize implementation, licensing spend, outreach expansion, or an E-level increase.

The objective is to prove a deeper result than `permit required?` without ingesting or reproducing protected National / Building Code technical text.

## Representative buyer/work-record scenario

Use a Vancouver residential bathroom or kitchen renovation with facts like:

- jurisdiction: `vancouver_bc`;
- existing residential dwelling;
- bathroom or kitchen update;
- existing plumbing line(s) will be moved or new plumbing line(s) installed;
- no structural alteration;
- no addition / new floor area;
- project value under CAD 250,000;
- no secondary-suite creation/legalization;
- no work-without-permit enforcement case;
- no parking/tree-retention condition identified;
- final property-specific exceptions remain explicitly unresolved unless supplied by the buyer.

This is intentionally close to Pacific Coast Contracting's publicly described renovation work and to ProjectPermit's current `kitchen_bath_plumbing` family.

## First-party City of Vancouver basis

### 1. Moving or installing plumbing lines triggers permit work

The City of Vancouver's current `Renovate a home` page states that moving existing plumbing/electrical/gas lines or installing new lines requires permits, while replacing fixtures/cabinets/flooring does not by itself require a building permit.

Official source:
- https://vancouver.ca/home-property-development/renovate-home.aspx

The separate plumbing-permit page states that a plumbing permit is required to install/change/upgrade plumbing, while replacing a fixture in the same location is an exception.

Official source:
- https://vancouver.ca/home-property-development/plumbing-permit.aspx

### 2. Simple bathroom/kitchen renovations may qualify for Residential Renovation Fast Track

The City's renovation page currently describes Residential Renovation Fast Track (RRFT) for simple residential renovation projects under CAD 250,000 and expressly lists:

- bathroom and kitchen updates; and
- plumbing/electrical updates

as eligible project types, subject to the City's stated exclusions/conditions.

The same page says RRFT is not available for examples including:

- additions;
- structural alterations;
- secondary-suite addition/legalization;
- work-without-permit / similar enforcement cases;
- projects over CAD 250,000;
- projects needing parking or tree-retention review.

Official source:
- https://vancouver.ca/home-property-development/renovate-home.aspx

RRFT eligibility must therefore be represented as **conditional**, not guaranteed.

### 3. Application requires forms plus a project-specific drawing/document package

The City's renovation process directs applicants to gather the required drawings/documents using the Addition/Renovation submission checklist, complete the Development/Building Permit Application Form, and submit the complete package.

Official sources:
- https://vancouver.ca/home-property-development/renovate-home.aspx
- https://vancouver.ca/home-property-development/application-forms-and-checklists.aspx

The public forms/checklists directory maintains project-specific checklist categories including single-detached/duplex addition/renovation, field-review minor renovation, building-envelope repair, decks and other project types.

For ProjectPermit E3, **link to the current official checklist/form; do not ingest or reproduce protected checklist/code content as a required product dependency.**

### 4. Permit fees are a workflow prerequisite

The renovation page states that after application intake the City notifies the applicant to pay permit application fees/deposits.

The plumbing-permit page states that plumbing-permit fees are payable at permit submission.

Official sources:
- https://vancouver.ca/home-property-development/renovate-home.aspx
- https://vancouver.ca/home-property-development/plumbing-permit.aspx

The E3 result does not need to calculate the exact fee unless a reliable current fee source is separately validated. It can safely return a `FEE_PAYMENT_REQUIRED` workflow obligation with the official fee link/state.

### 5. Separate plumbing trade permit is a distinct work item

The City's renovation page says most house renovations require separate trade permits and identifies plumbing, electrical, fire-sprinkler and gas permits as examples typically submitted by the relevant trade contractor.

For the representative scenario, moved/new plumbing lines provide a concrete reason to include a plumbing-trade-permit obligation.

Official sources:
- https://vancouver.ca/home-property-development/renovate-home.aspx
- https://vancouver.ca/home-property-development/plumbing-permit.aspx

### 6. Plumbing-permit applicant eligibility is machine-actionable

The plumbing-permit page currently states that a plumbing-permit applicant generally needs either:

- a valid City of Vancouver business licence; or
- an inter-municipal business licence,

with specific homeowner/outside-service exceptions described by the City.

Official source:
- https://vancouver.ca/home-property-development/plumbing-permit.aspx

For contractor workflows this can be represented as a bounded precondition rather than inferred from company identity.

### 7. Inspections are part of the permit lifecycle

The renovation page states that work is inspected at various construction stages and that the project is considered complete after approval of the final inspection.

The plumbing-permit page states that all plumbing work must be inspected for the plumbing permit to be finalized.

Official sources:
- https://vancouver.ca/home-property-development/renovate-home.aspx
- https://vancouver.ca/home-property-development/plumbing-permit.aspx

The E3 slice should therefore include inspection/milestone obligations, but it should not invent exact inspection stages beyond what the official page currently establishes unless those stages are separately sourced.

### 8. Approved permit and drawings must be available at the jobsite

The renovation page states that the City-approved permit and one paper set of City-approved drawings must be available at the jobsite for inspectors; missing accepted/stamped drawings can cause inspection rescheduling and possible re-inspection fees.

Official source:
- https://vancouver.ca/home-property-development/renovate-home.aspx

This is a useful `DOCUMENT_AT_JOBSITE` operational obligation because it is both deterministic and directly relevant to field workflow.

## Candidate `obligations[]` for this representative E3

These are **ProjectPermit product-model proposals derived from the official process**, not City of Vancouver field names.

### OBL-1 — Building / renovation permit path

- category: `PERMIT_OR_APPROVAL`
- applicability: `REQUIRED` for moved/new plumbing-line renovation under the current published City table
- action: include building/renovation permit process before regulated work starts
- blocking_before: `WORK_START`
- evidence: City `Renovate a home`

### OBL-2 — RRFT eligibility check

- category: `SPECIAL_REVIEW` or `PERMIT_ROUTE`
- applicability: `CONDITIONAL`
- action: evaluate published RRFT eligibility/exclusions
- blocking_before: `PERMIT_SUBMISSION`
- quote impact: `SCHEDULE_RISK` / faster-route possibility, not guaranteed turnaround
- evidence: City `Renovate a home`

Do **not** promise RRFT approval or issuance timing merely because the high-level facts appear eligible.

### OBL-3 — Required application package

- category: `REQUIRED_DOCUMENT`
- applicability: `REQUIRED`
- action: prepare current project-specific official checklist package + application form
- blocking_before: `PERMIT_SUBMISSION`
- evidence: renovation page + official forms/checklists directory

### OBL-4 — Permit-fee payment

- category: `PRECONDITION`
- applicability: `REQUIRED`
- action: permit fees/deposits become payable at the City's stated intake/submission stage
- blocking_before: `PERMIT_PROGRESS`
- quote impact: `ALLOWANCE` if the contractor prices permit/admin cost
- evidence: renovation/plumbing permit pages

Do not hard-code a dollar amount until a separate current-fee fact is validated.

### OBL-5 — Plumbing trade permit

- category: `PERMIT_OR_APPROVAL`
- applicability: `REQUIRED` for the representative moved/new plumbing-line scope
- action: obtain plumbing trade permit
- blocking_before: `TRADE_WORK_START`
- evidence: renovation page + plumbing permit page

### OBL-6 — Plumbing applicant licence precondition

- category: `PRECONDITION`
- applicability: `REQUIRED_OR_EXCEPTION`
- action: confirm valid Vancouver/inter-municipal business licence or an applicable City-stated exception
- blocking_before: `PLUMBING_PERMIT_SUBMISSION`
- required_fact: `plumbing_permit_applicant_eligibility`
- evidence: plumbing permit page

### OBL-7 — Inspection milestones

- category: `INSPECTION_OR_STAGE`
- applicability: `REQUIRED`
- action: book/complete required inspections; final approval required to finalize the permitted work/permit
- blocking_before: `PROJECT_COMPLETE`
- quote impact: `SCHEDULE_RISK`
- evidence: renovation + plumbing-permit pages

### OBL-8 — Approved documents at jobsite

- category: `REQUIRED_DOCUMENT`
- applicability: `REQUIRED`
- action: keep City-approved permit and accepted/stamped drawing set available for inspectors at the jobsite
- blocking_before: `INSPECTION_STAGE`
- quote impact: `SCHEDULE_RISK` because missing documents may require inspection rescheduling
- evidence: renovation page

## Professional-involvement boundary

Do **not** encode `architect/engineer/designer required` for this generic representative slice based only on the current high-level renovation page.

The City recommends engaging a qualified design professional/contractor depending on project scale, but the public high-level page does not establish a universal mandatory professional for every bathroom/kitchen renovation with moved plumbing.

Therefore:

- `professional_required = UNKNOWN / PROJECT_SPECIFIC` unless a narrower official source establishes a requirement;
- keep structural/professional triggers as unresolved conditions;
- do not turn a recommendation into a legal requirement.

This is exactly the conservative behavior ProjectPermit should preserve.

## Quote/work-record consequence — product inference, not City requirement

The City sources establish process obligations. The following are **ProjectPermit workflow interpretations that must be buyer-validated**:

- permit/trade-permit fees can create a quote allowance;
- application documents can create administrative/design scope;
- permit route/conditions can affect schedule assumptions;
- inspections create project milestones;
- applicant eligibility can change subcontractor/handoff responsibility;
- missing approved documents can create inspection delay/reinspection risk.

These consequences must not be represented as City-mandated pricing rules.

## Why this is a better E3 than same-size window replacement

Current ProjectPermit Vancouver rules deliberately return `MUNICIPAL_CONFIRMATION_REQUIRED` for same-size window/door replacement because the public City summary does not expressly resolve that exemption.

That is safe behavior, but it makes same-size window replacement a poor representative Layer-C demonstration.

The bathroom/kitchen + moved-plumbing scenario is stronger because first-party City pages directly support multiple deterministic workflow obligations:

`permit path -> documents -> fee stage -> trade permit -> applicant eligibility -> inspections -> jobsite documents`

That is enough to test whether a maintained obligation bundle changes a real contractor quote/job workflow **without pretending to perform technical Building Code compliance**.

## Source-rights / licensing classification

For this E3 readiness slice:

- use City public process pages as evidence links;
- store structured independently encoded process facts and verification metadata;
- do not reproduce protected National Building Code / Vancouver Building By-law technical text;
- do not ingest City checklist PDFs as a corpus for the prototype;
- link users to the current official checklist/form;
- keep any future code-derived technical obligation behind the existing licensing gate.

This is a **license-light validation slice**, not a declaration that every City webpage or form is unrestricted for all commercial reuse.

## E3 activation gate

Do not implement this slice merely because the official data exists.

Activate only after a real supported-city buyer (PCC-like or equivalent) establishes:

1. recent bounded denominator (`last 20 estimates`);
2. material quote/scope/schedule consequence;
3. meaningful repeated research/maintenance burden;
4. preference to externalize at least the currentness/evidence layer;
5. a plausible payment path.

If those are present, this slice is deliberately small enough to implement as a representative E3 without purchasing protected-code content or adding municipalities.

## E3 success condition for this slice

A valid representative test would show:

1. a real/sanitized Vancouver Jobber-like renovation work record enters the existing adapter;
2. the structured project facts identify moved/new plumbing scope;
3. ProjectPermit returns the evidence-linked obligation bundle above;
4. at least one obligation changes a buyer-recognized quote allowance, scope item, schedule assumption, handoff or milestone;
5. the action bundle produces a bounded proposal into the existing work-record workflow;
6. rerun behavior remains idempotent/change-classified;
7. the buyer says the result reduces a repeated manual current-regulation/process step.

Until then this file remains readiness documentation only.

## Evidence score

No E2/E3/E4/E5 increase.

This note answers only:

> **If a current-coverage buyer crosses E2, can ProjectPermit demonstrate a materially deeper, license-light obligation bundle immediately without broadening geography or ingesting protected code content?**

For this Vancouver renovation scenario, the answer is **yes**.