# Layer C minimal E3 readiness — 2026-08-30

## Purpose

Define the smallest prototype boundary **only if** Layer C crosses the buyer validation gate. This is a readiness note, not authorization to implement.

Current gate remains: obtain independent buyer/workflow denominator plus material workflow consequence before changing production schema/content.

## What already exists

### Platform-neutral action bundle

Current `action_bundle` already carries:

- deterministic decision + confidence
- jurisdiction + project family
- workflow route + quote handling
- automation-safe flag
- evidence freshness
- required/missing inputs
- proposed tasks
- official evidence with rule ids / source verification dates
- audit metadata
- deterministic bundle/idempotency identity
- repeat-check change classification
- safe-writeback mutation gate
- writeback hints

Therefore Layer C does **not** require a new orchestration envelope.

### Jobber adapter

Current Jobber adapter already:

- accepts Request / Quote / Job objects
- extracts stable work-record id, property address and scope text from title/line items
- binds source object scope into deterministic idempotency context
- can carry prior decision identity for repeat/change checks
- converts an action bundle into proposed custom fields, tasks, required inputs, evidence and audit metadata
- performs no mutation by default

### ServiceM8 adapter

Current ServiceM8 adapter already:

- extracts stable Job uuid, status, address and scope from job description/materials
- binds source job scope into deterministic idempotency context
- can carry prior decision identity
- converts an action bundle into proposed routing fields, tasks, required inputs, evidence and audit metadata
- performs no mutation by default

## Minimal Layer C data gap

If buyer evidence crosses the gate, the minimum useful addition is a structured `obligations[]` layer. It should describe only project-specific pre-estimate / preconstruction consequences, not full code text and not drawing compliance.

Candidate obligation categories:

1. `PERMIT_OR_APPROVAL`
   - another permit/approval/review that the scope triggers
2. `PRECONDITION`
   - prerequisite before filing, pricing lock or work start
3. `REQUIRED_DOCUMENT`
   - site plan, drawing, schedule, calculation, form or other submission artifact
4. `PROFESSIONAL_INVOLVEMENT`
   - architect/engineer/designer/trade or other qualified professional involvement where the source clearly requires it
5. `INSPECTION_OR_STAGE`
   - required inspection or regulated construction stage that affects sequence
6. `DEADLINE_OR_VALIDITY`
   - filing/response/expiry/renewal timing that affects schedule
7. `SPECIAL_REVIEW`
   - heritage/planning/zoning/conservation/design or similar routed review

Each obligation should remain evidence-linked and bounded. Minimum candidate fields:

- `obligation_id`
- `category`
- `status` / applicability
- `title`
- `action_required`
- `blocking_before` (`QUOTE_LOCK`, `DESIGN_LOCK`, `WORK_START`, `INSPECTION_STAGE`, etc.)
- `quote_impact` (`NONE`, `ALLOWANCE`, `SCOPE_CHANGE`, `PROFESSIONAL_COST`, `SCHEDULE_RISK`, `UNKNOWN`)
- `required_facts` / unresolved conditions
- `rule_id`
- `rule_version`
- `source_verified_at`
- evidence/source references

Do not add raw reproduced code text as a required field.

## Minimal workflow output gap

Current generic tasks are already sufficient for permit-task / evidence / missing facts / special review / municipal confirmation / manual review.

For an E3 prototype, only two new concepts are likely required:

- `ADD_REGULATORY_ALLOWANCE_OR_SCOPE` — proposal only when an obligation materially changes quoted scope/cost.
- `ADD_REGULATORY_MILESTONE` — proposal only when an obligation creates a sequencing/inspection/deadline dependency.

Both should remain proposed actions behind the existing mutation gate. No unconditional write is needed.

## Minimum integration mapping

### Jobber

Use existing work object and proposal envelope. Candidate output mapping only:

- quote internal note / custom fields: obligation summary + source freshness
- quote line-item/allowance proposal: only for `quote_impact` that changes cost/scope
- task proposal: missing document/professional/permit/inspection prerequisite
- existing source-object idempotency prevents duplicate proposals on rerun

### ServiceM8

Use existing Job object and proposal envelope. Candidate mapping only:

- routing summary: obligation status + quote handling
- job/task proposal: required document/professional/inspection milestone
- material/scope change proposal only when buyer workflow shows that this is wanted
- existing source-job idempotency prevents duplicate proposals

No new platform client or write executor is required for E3.

## What E3 should NOT contain

Even after E2:

- no full National/Provincial building-code ingestion by default
- no design/drawing/BIM compliance certification
- no legal advice
- no permit filing automation unless separately validated
- no broad CRM/estimating replacement
- no unconditional Jobber/ServiceM8 mutation
- no new municipality expansion simply to make the prototype look larger
- no paid code-content licence before licensing economics are known

## E3 success condition

A valid E3 is not `the schema exists`.

It must demonstrate, on a buyer-representative work record:

1. existing request/quote/job facts enter ProjectPermit;
2. one or more evidence-linked obligations are returned;
3. at least one obligation has a buyer-recognized material consequence on scope, price, schedule, professional involvement or handoff;
4. the adapter produces a bounded proposal into an existing work object;
5. repeat evaluation is idempotent / change-classified;
6. buyer says the output replaces or materially reduces a real repeated manual step.

Until the buyer denominator/consequence gate is crossed, **do not implement this file as product scope**.
