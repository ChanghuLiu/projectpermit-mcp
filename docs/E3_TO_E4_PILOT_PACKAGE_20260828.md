# ProjectPermit E3 -> E4 pilot package — 2026-08-28

## Goal

Convert a qualified contractor/platform conversation into evidence with minimal partner effort.

The pilot is deliberately split into two stages so a prospect does not need to integrate anything merely to validate whether ProjectPermit is useful.

---

## Stage 1 — historical benchmark (E3 candidate)

### Partner effort

Provide **10–20 recent, de-identified projects** from one supported municipality / workflow.

Preferred sampling method: the most recent chronological qualifying projects, not hand-picked interesting examples.

For each project, only five fields are required:

1. anonymous case ID;
2. municipality;
3. short project scope;
4. actual final permit outcome: `required / not required / conditional-confirm`;
5. source of the historical outcome, for example `permit issued`, `municipal confirmation`, `professional/contractor record`.

Use `data/e3_minimal_contributor_template.csv`.

### Privacy

Do **not** send:

- customer names;
- email/phone;
- exact civic address;
- invoice/contract value;
- private documents unless independently agreed later.

If an address/property overlay was decisive historically, send only the derived non-personal fact when possible (for example `heritage=yes`, `flood_overlay=yes`, `corner_lot=yes`).

### What ProjectPermit does

For every usable case:

- normalize the scope into the current taxonomy;
- run the deterministic municipality rules;
- record the ProjectPermit determination and confidence;
- compare with the actual historical outcome;
- separately record whether a generic city guide/checklist would likely have produced the same answer;
- record whether municipality specificity changed the answer;
- identify missing decisive facts rather than silently guessing.

### Stage-1 output

Return one compact benchmark:

- usable-case count;
- agreement rate;
- material false-negative count (`LIKELY_NOT_REQUIRED` where a permit was actually required);
- confirmation/unknown rate;
- municipality-specificity wins;
- cases where a simpler generic guide would have been equally good;
- median number of missing clarification facts.

### Evidence rule

The cohort is only E3-worthy if the sampling is reasonably representative/chronological and the historical outcome is independently grounded. Cherry-picked examples, synthetic cases, demos and ProjectPermit-owner data do not qualify.

---

## Stage 2 — live repeated workflow (E4 candidate)

Only proceed if Stage 1 is useful enough to justify the operational test.

### Target

Run ProjectPermit on at least **20 real new projects** during the normal request/estimate/quote workflow.

No write-back or workflow mutation is required for the first pilot. A CSV/manual batch or read-only integration is acceptable.

### Measure

For each relevant project record:

1. whether the existing intake was enough for a decision with **0 clarification questions**;
2. whether **1–3 targeted missing facts** were enough;
3. whether the case remained `CONFIRM` because of property/site/unsupported facts;
4. whether the preflight changed the operator's next action;
5. manual municipal research minutes avoided, if observable.

### E4 success condition

At minimum:

- one independent external workflow;
- 20+ successful preflight calls on real new projects;
- calls are not owner/CI/synthetic traffic;
- repeated usage is observed rather than merely promised.

---

## Stage 3 — economic test (E5 candidate)

Only after Stage 2 demonstrates repeated utility.

Test one concrete resource/economic commitment, for example:

- willingness to continue at approximately **$0.20–$0.50 per address-aware preflight**;
- a fixed paid pilot budget;
- engineering/integration time committed by the partner;
- a documented procurement/partnership step that consumes real organizational resources.

A positive email opinion is not E5.

---

## Partner-facing short description

> We can start without an integration. Send 10–20 recent anonymous project scopes from one city plus the actual permit outcome your team used. We will run them blind through ProjectPermit and return the disagreement/confirmation analysis. If the results are useful, the second step is a read-only 20-project live pilot in your existing quote/request workflow. No customer names or exact addresses are needed for the first benchmark.

---

## Stop conditions

Do not proceed to Stage 2 merely because the partner is friendly.

Stop/re-scope if Stage 1 shows that:

- a simple generic municipal guide/RAG answer performs essentially as well on representative ordinary cases;
- deterministic resolution requires expert review or many extra questions on a large share of jobs;
- false negatives are material;
- the partner says the workflow volume is too low to matter;
- the partner explicitly prefers cheap internal rule maintenance and sees little value in a shared maintained API.

## Current evidence state

- independent representative E3 cohorts: **0 / 2**;
- repeated external E4 workflow with 20+ calls: **0**;
- E5: **0**;
- Go/No-Go: **51 / 100**.

This package is readiness work only and does not itself count as validation.
