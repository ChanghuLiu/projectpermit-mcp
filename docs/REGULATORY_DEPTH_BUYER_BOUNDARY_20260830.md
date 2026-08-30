# Regulatory Depth Buyer Boundary — 2026-08-30

## Decision

Do **not** expand ProjectPermit into a general building-code compliance checker and do **not** add new regulatory-depth product fields yet.

Two independent software-side E1 replies now justify testing a narrower re-scope hypothesis:

> A software buyer may prefer to keep simple `permit required?` logic internally, while buying a maintained external layer that returns current project-specific regulatory requirements with official-source provenance, freshness and change history.

This is a validation hypothesis, not a product pivot.

## Buyer evidence that created this boundary

### Contrax

The buyer-side reply explicitly separated the two layers:

- `do I need a permit?` logic: would build internally because it is a better flow, faster and cheaper;
- API for updated legal requirements / regulations / building code: described as "super useful."

A bounded monthly workflow-volume follow-up is pending.

Evidence class: **E1 only** until a denominator/timeframe is provided.

### SubmitX

SubmitX says it already maintains some light municipal / Québec compliance logic internally, but an external solution with real depth and market coverage could still be interesting if cost and reliability are reasonable. It also noted that resources of this kind are scarce in the Québec market.

A bounded monthly permit-sensitive workflow-volume follow-up is pending.

Evidence class: **E1 only**.

## Current ProjectPermit capability vs the new hypothesis

The current response contract already contains much of the infrastructure needed for a maintained regulatory-data product:

- deterministic `requirements[]`;
- stable `rule_id` and `rule_version`;
- `source_verified_at`;
- official evidence with authority/title/URL/source ID;
- evidence freshness status and automation blocking;
- ruleset and evidence fingerprints;
- change classification including `RULESET_CHANGED` and `EVIDENCE_REFRESHED`;
- audit metadata and source counts;
- downstream routing and safe-writeback gates.

Therefore the missing buyer value is **not primarily provenance/versioning plumbing**.

The important gap is substantive regulatory breadth.

## Four-layer boundary

### Layer A — permit applicability

Question:

> Does this project require a permit / likely require one / require municipal confirmation?

Current ProjectPermit coverage: **strongest existing layer**.

Examples already encoded:

- additions;
- structural changes;
- window/door opening changes;
- plumbing triggers;
- basement work;
- sheds/accessory structures;
- decks/porches;
- dwelling-unit changes;
- selected roof/exterior-renovation thresholds.

Buyer signal so far: simple local versions may be cheap enough to internalize.

### Layer B — approval / permit path

Question:

> Which approval path or additional municipal review is implicated?

Current ProjectPermit coverage: **partial**.

Existing examples include:

- `building_permit`;
- `development_permit` in Vancouver secondary-suite logic;
- planning/design/heritage review in selected Québec rules;
- municipal-confirmation and special-review routing.

This is still mostly organized around deciding the permit path rather than producing a complete obligation inventory.

### Layer C — project-specific regulatory obligation bundle

Question:

> Before an estimate is finalized, what current regulatory obligations are likely relevant to this scope, where do they come from, and what changed since the last evaluation?

Examples of the type of information a future Layer C might contain **only if buyer evidence justifies it**:

- applicable municipal by-law / code provision identifiers;
- project-specific zoning/building/fire/egress/accessibility/energy/trade obligations that can be determined from supplied facts without reviewing drawings;
- required professional documents or plan components when explicitly established by current official sources;
- required related approvals/trade permits;
- effective/version date;
- official source and source freshness;
- whether the obligation changed since the prior project evaluation;
- unresolved facts that block a safe answer.

Current ProjectPermit coverage: **weak / incidental**.

Some current rule reasons mention that zoning standards, trade requirements, fire-safety systems or other standards may apply. Vancouver also uses the 2025 Vancouver Building By-law for a narrow patio exception. But ProjectPermit does **not** currently expose a systematic project-specific catalogue of applicable code/by-law obligations.

This is the exact layer now worth validating.

### Layer D — design / drawing compliance checking

Question:

> Does this drawing/BIM/design comply with detailed code provisions?

Current ProjectPermit coverage: **out of scope by design**.

This includes deterministic review of dimensions, assemblies, structural calculations, fire-resistance design, complete code conformance of permit drawings, BIM/IFC checking and similar downstream work.

This overlaps the NRC Automated Compliance Checking direction and would materially change the product, data/licensing burden and competitive set.

**Do not enter Layer D from the current E1 evidence.**

## Proposed re-scope hypothesis

The narrow hypothesis to falsify is:

> `scope/address/project facts → current regulatory obligation bundle + official evidence + freshness/change identity`

not:

> `scope/address → permit yes/no only`

and not:

> `drawings/BIM → full building-code compliance review`.

A useful commercial call would occur while the buyer is still preparing an estimate, scope, proposal or job plan — early enough for a requirement to change cost, scope, sequencing, professional involvement or quote handling.

## Why this may have better build-vs-buy economics

The current maintenance audit already shows why simple local permit logic is vulnerable to internalization:

- Toronto and Mississauga scope-only permit logic can currently be grounded in one primary municipal guidance source each;
- a local buyer can accept conservative escalation and avoid ProjectPermit's full cross-city architecture.

Layer C changes the build-vs-buy question. The buyer would no longer be comparing ProjectPermit with a small local trigger table. It would be comparing against maintaining a broader set of current, source-versioned regulatory obligations and amendment effects across jurisdictions.

That could increase externalization value, but **the current evidence does not yet prove that it does**.

## What must be proven before engineering Layer C

### Gate 1 — repeated workflow volume (E2)

At least one credible software/platform buyer provides a bounded timeframe and denominator showing that regulatory-obligation checks occur often enough to automate.

Preferred evidence:

- monthly eligible estimates/projects;
- percentage requiring regulatory requirement lookup;
- or a directly observed workflow count with source/timeframe.

### Gate 2 — operational consequence

At least one buyer explains a concrete way the deeper requirement changes a workflow, such as:

- estimate line item / allowance;
- scope exclusion or addition;
- need for engineer/architect/designer;
- sequence or lead time;
- trade-permit task;
- customer warning/approval;
- hold on quote finalization.

Generic `useful` is not enough.

### Gate 3 — externalization preference

The buyer says that maintaining the deeper rules/sources itself is meaningfully undesirable, not merely that the information would be nice to have.

### Gate 4 — representative real cases (E3)

Run representative buyer-provided historical scopes against a bounded Layer-C prototype or manual research result and measure whether the obligation bundle is correct and materially useful.

### Gate 5 — repeated external use (E4)

A non-owner workflow repeatedly invokes the capability for real work.

## Minimum validation questions

Do not ask prospects broad product-opinion questions. Use bounded questions:

1. `In a normal month, about how many estimates/projects require checking current municipal/code/regulatory requirements before finalization?`
2. `Of those, in roughly how many does the answer change price, scope, sequencing, professional involvement or whether the quote can be finalized?`
3. `Do you currently maintain those requirements internally, search them manually, rely on staff knowledge, or use an external source/API?`
4. `Which part would you least want to maintain internally: simple permit triggers, current by-law/code requirements, source/version tracking, or none of these?`

One or two bounded questions per outreach interaction are enough; do not turn outreach into a survey burden.

## What not to build now

Until the gates above move:

- no new cities;
- no general building-code corpus ingestion;
- no drawing/BIM compliance engine;
- no paid code-data licensing;
- no large `obligations[]` schema redesign;
- no additional field-service adapters;
- no anti-bot scraping stack;
- no continuous high-frequency source crawler.

## Current evidence classification

| Signal | Evidence level | Score effect |
|---|---|---|
| SubmitX deeper-layer interest | E1 | none |
| Contrax updated legal/regulation/code API interest | E1 | none |
| Source observability 25/42 direct canonical fetches | maintenance feasibility | none |
| Laval/Vancouver alternate probe 0/8 | maintenance-cost boundary | none |
| External successful preflight workflows | E4 = 0 | none |
| External payment | E5 = 0 | none |

## Bottom line

ProjectPermit already owns much of the **trust infrastructure** for a deeper regulatory product — source provenance, version identity, freshness, deterministic rules and change detection semantics.

It does **not** yet own the substantive breadth of a project-specific regulatory obligation API, and there is not enough buyer evidence to build that breadth.

The next score-moving work is therefore **buyer-volume and workflow-consequence validation of Layer C**, not more engineering.