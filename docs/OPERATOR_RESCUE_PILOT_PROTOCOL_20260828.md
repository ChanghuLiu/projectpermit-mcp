# Operator Rescue Pilot Protocol — 2026-08-28

## Purpose

ProjectPermit is at **50/100, PAUSE / RE-SCOPE**. Engineering expansion remains frozen.

The operator-level route identified through Oolong / Soumissions Maison creates a better validation opportunity than another generic outreach round:

> one operator may see many narrow renovation funnels before contractor routing, potentially allowing one integration to aggregate enough unresolved permit-applicability decisions to matter.

The next step is **not** to build an integration.

The next step is to obtain one bounded, reproducible evidence package that can answer in a single cycle:

1. is the upstream volume real?
2. is permit applicability actually unresolved there?
3. are existing intake facts sufficient?
4. does the answer materially change the operator workflow?
5. is one operator-level integration technically/commercially preferable to separate site work?
6. would the operator buy rather than build?

This protocol applies to Oolong and any comparable multi-funnel marketplace/operator.

---

## 1. Evidence target

A useful pilot should build one chain:

`recent unique operator requests -> unresolved permit subset -> representative historical cases -> ProjectPermit replay -> measurable workflow effect -> shadow external calls -> economic commitment`

Map this to the existing evidence standard:

- **E2** — bounded complete-month operator workflow claim;
- **E3** — representative chronological historical sample;
- **E4** — real repeat external calls in shadow/production-like workflow;
- **E5** — price/resource/integration commitment.

A friendly reply is still E1.

---

## 2. Phase A — bounded operator denominator (E2)

Ask for the **most recent complete month**.

The denominator must be **unique homeowner/project requests**, not copies sent to multiple contractor partners.

### Required aggregate fields

For each current-family funnel/category available to the operator, request:

- unique project requests in the month;
- number whose municipality was within current ProjectPermit coverage;
- number where permit applicability was already known before routing;
- number where permit applicability was unresolved before routing;
- number where permit applicability was simply not checked / irrelevant to routing;
- number that required a human to ask another project question or research a municipality;
- if known, number where permit uncertainty changed routing, qualification, price/tier, manual work, rejection/refund or another measurable outcome.

Current-family groups:

- `window_door`;
- `interior_renovation`;
- `basement`;
- `dwelling_change`;
- `deck_porch`;
- `accessory_structure`;
- `addition`;
- `kitchen_bath_plumbing`.

### Duplicate-delivery control

If the operator sells one homeowner request to three contractors, that is:

- **1 unique upstream project request**;
- **3 partner-delivered lead copies**.

Do not use `3` as ProjectPermit call volume unless the product would actually be called separately at all three downstream copies.

Record both if available:

- `unique_requests`;
- `partner_deliveries`;
- `delivery_multiplier = partner_deliveries / unique_requests`.

The commercial preflight hypothesis is primarily about **unique upstream requests**.

### Existing commercial checkpoint

ProjectPermit's existing evidence standard defines **500+ candidate calls/month from a specific workflow** as the first commercially relevant small-channel checkpoint.

Therefore:

- an operator route does **not** clear the existing single-channel rescue gate unless the measured workflow can plausibly produce >=500 candidate calls/month;
- below 500/month can still be an aggregation component, but it does not justify resuming jurisdiction/product engineering on its own;
- do not inflate the number with partner-delivered duplicates.

No new lower threshold is invented in this protocol.

---

## 3. Phase B — representative historical lead sample (E3)

### Preferred sample

Request **50–100 chronological recent unique requests** from current-family funnels.

If that is too burdensome:

- 20 recent chronological cases is the preferred minimum for a first operator replay;
- the existing E3 standard allows smaller representative case sets, but a tiny sample should not be used for market-rate claims.

Do not ask the partner to hand-pick interesting permit cases.

Preferred sampling instruction:

> take the first N qualifying unique current-family requests received after a fixed date/time, regardless of whether a permit issue occurred.

That preserves negative cases.

### Privacy / PII rule

ProjectPermit does not need names, phone numbers or email addresses for this validation.

Never request:

- homeowner name;
- email;
- phone;
- unrelated free-text identifiers.

For addresses:

- record `address_available=yes/no`;
- do not require the operator to transmit raw civic addresses in ordinary email;
- a scope-only replay can use municipality plus sanitized project facts;
- where an address/property fact is necessary, prefer an operator-local/shadow call or another explicitly authorized secure path rather than copying PII into research files.

The purpose is to measure **whether address context is needed and available**, not to collect a homeowner dataset.

---

## 4. Historical-case fields

Use `data/operator_rescue_pilot_sample_template.csv`.

Each row should represent one **unique upstream project request**.

Key field groups:

### Provenance

- opaque `sample_id`;
- source funnel/category;
- received date (day granularity is enough);
- municipality;
- current-family mapping.

### Existing intake facts

Record what was already present before any ProjectPermit-specific follow-up:

- structured service/category fields;
- sanitized project description;
- address available yes/no;
- relevant ProjectPermit facts when directly present.

Do not backfill missing fields using hindsight before classifying fact sufficiency.

### Permit state at insertion point

Use one of:

- `KNOWN_REQUIRED`;
- `KNOWN_NOT_REQUIRED`;
- `UNRESOLVED`;
- `NOT_CHECKED`;
- `UNKNOWN`.

If the operator did not track this historically, use `UNKNOWN`; do not infer `UNRESOLVED` from silence.

### Existing human/operator action

Examples:

- no permit action;
- asked homeowner another question;
- contractor determined it later;
- operator researched municipality;
- routed to a different partner type;
- rejected/held the lead;
- permit question had no routing effect.

### Historical outcome

If known, record:

- actual permit was required;
- actual permit was not required;
- municipality confirmed special review;
- outcome unknown.

Historical outcome is optional; absence does not make the case useless for fact-sufficiency measurement.

---

## 5. Fact-sufficiency classification

Before running ProjectPermit, classify the case using the existing categories:

- `DIRECT_STRUCTURED` — existing structured fields are sufficient;
- `TEXT_DERIVABLE` — existing description contains enough detail for conservative normalization;
- `FOLLOWUP_REQUIRED` — a decision-changing project fact must be asked;
- `EXTERNAL_PROPERTY_LOOKUP_REQUIRED` — address/property lookup is needed;
- `INSUFFICIENT_FOR_CURRENT_RULES` — the current ruleset cannot give a useful result even if upstream facts are complete.

Important distinction:

`address_available` is not the same as `address_required`.

### Primary metric

`decision_fact_sufficiency_rate = (DIRECT_STRUCTURED + TEXT_DERIVABLE cases that current rules can evaluate usefully) / qualifying sampled cases`

Report property-lookup-dependent cases separately.

Do not create a new questionnaire or NLP extractor merely to improve this metric during the rescue phase.

---

## 6. Offline ProjectPermit replay

Run only:

- current supported jurisdictions;
- current supported project families;
- current rules and source versions.

Do **not** add a municipality or rule because a pilot case falls outside coverage.

For each replay, record:

- ProjectPermit input facts;
- determination;
- confidence;
- requirement types;
- rule/source version;
- whether the result required address/property context;
- agreement/disagreement with historical human/outcome when available;
- whether disagreement is material.

### Safety metric

Track separately:

- cases where ProjectPermit is more conservative than the historical path;
- cases where ProjectPermit is less conservative than a known permit-required/special-review outcome.

A less-conservative disagreement against a known required outcome is a higher-severity error and must not be averaged away by easy cases.

---

## 7. Material workflow-effect test

A technically correct permit result has weak commercial value if it changes nothing.

For every sampled `UNRESOLVED` case, ask or reconstruct whether a reliable preflight would have changed one of:

- partner routing;
- lead qualification;
- lead tier/price;
- manual validation/research time;
- need to contact homeowner again;
- lead hold/rejection;
- refund/complaint risk;
- contractor response quality;
- another operator-defined measurable outcome.

Classify:

- `MATERIAL_EFFECT_CONFIRMED`;
- `POSSIBLE_EFFECT_NOT_MEASURED`;
- `NO_MATERIAL_EFFECT`;
- `UNKNOWN`.

### Material-hit rate

`material_hit_rate = MATERIAL_EFFECT_CONFIRMED / all candidate preflight cases`

Use the break-even framework in:

- `docs/PLATFORM_LEAD_VALUE_BREAKEVEN_20260828.md`

Do not assign a dollar value to a material hit unless the operator supplies or accepts one.

---

## 8. Operator integration test

Before any custom integration work, answer these questions explicitly:

1. Are relevant funnels stored/routed through one CRM/data workflow?
2. Can one operator-level integration see multiple funnels?
3. Are the fields normalized centrally or site-specific?
4. Would a ProjectPermit result be written back centrally?
5. Would each site require separate engineering/security/legal work?
6. Can a shadow call run without changing customer-visible behavior?

Classify integration topology:

- `CENTRAL_SINGLE_INTEGRATION`;
- `CENTRAL_WITH_SITE_MAPPING`;
- `SEPARATE_SITE_INTEGRATIONS`;
- `MANUAL_EXPORT_ONLY`;
- `UNKNOWN`.

The operator aggregation thesis is materially weakened if the answer is `SEPARATE_SITE_INTEGRATIONS`.

---

## 9. Phase C — shadow external usage (E4)

Only after Phase A/B shows a credible workflow should ProjectPermit run on real incoming cases.

Shadow-mode properties:

- no automated homeowner/contractor decision at first;
- operator continues existing process;
- ProjectPermit result is logged alongside existing workflow;
- no synthetic/internal calls count as E4.

Existing evidence thresholds still apply:

- **20+ real external calls** — repeat-use evidence;
- **100+ aggregate external pilot calls** — stronger workflow evidence;
- **500+ candidate calls/month** — commercially relevant small-channel path.

Track:

- call count;
- supported-family/jurisdiction rate;
- decision-fact sufficiency;
- determination mix;
- material-hit rate;
- manual follow-up avoided/created;
- operator overrides;
- known safety disagreements.

---

## 10. Phase D — economic / build-vs-buy test (E5)

Do not ask a generic willingness-to-pay question before the operator has seen replay/shadow results.

After observed behavior, ask for one concrete commitment tied to actual expected volume, for example:

- accepted per-call price;
- fixed paid pilot;
- fixed monthly operator licence;
- engineering/security time committed to integration;
- production continuation after free pilot;
- explicit decision to buy/partner instead of internalizing the rules.

Record the actual term, expected monthly volume and integration obligations.

A statement such as `this is useful` remains E1.

---

## 11. Stop / proceed logic

### Do not resume product engineering when any of these is true

- no bounded unique-request denominator;
- the workflow cannot plausibly reach the existing 500 candidate-call/month checkpoint without double-counting partner deliveries;
- permit applicability is normally already known before this insertion point;
- the operator does not check/care about permit applicability and no measurable workflow effect exists;
- representative leads usually lack required decision facts and the operator does not want additional enrichment/follow-up;
- one integration cannot cover enough funnels to make integration economics credible;
- the operator says it can/preferably will internalize municipality logic itself;
- no safe path exists to handle address/property context where needed.

### Evidence that justifies advancing to shadow E4

Advance only when the combined evidence shows:

- recent unique volume is bounded;
- a non-trivial unresolved subset exists at the target insertion point;
- representative sample is available;
- current rules can evaluate a useful share without speculative engineering;
- at least one measurable material workflow effect is identified;
- an operator-level integration path is plausible.

This protocol intentionally avoids inventing a new arbitrary percentage gate. Report the measured rates; apply the existing 500-call commercial checkpoint and the evidence-level standard.

### Evidence that justifies renewed engineering

New jurisdiction/product engineering should still require:

- representative E3 evidence;
- credible E4 workflow volume, preferably >=500 calls/month for the geography/channel;
- and preferably E5 resource/economic commitment.

Do not restart engineering merely because operator aggregation makes TAM arithmetic look larger.

---

## 12. Oolong-specific first response path

Oolong is currently E0. The existing 2026-08-28 email to `info@oolongmedia.ca` was sent as a forwarding route for the Québec Rénovation bounded question after both published Québec Rénovation addresses returned 550.

Do not immediately send a second near-duplicate email.

If a human replies, the preferred next message should ask whether the responder can answer at the **operator/network level** and request:

1. recent complete-month unique current-family request counts across Oolong-controlled funnels;
2. unresolved permit-applicability count before partner routing;
3. whether relevant funnels are in one CRM/data workflow;
4. permission to evaluate a chronological anonymized 20–100 case sample;
5. what measurable routing/validation outcome a permit signal could change.

That single reply path can move Oolong from E0 toward E2/E3 without another generic sales conversation.

---

## Bottom line

The operator rescue pilot is designed to answer one question:

> **Is there a real, low-friction, high-enough-volume upstream decision point where an operator gains measurable value from buying maintained municipal permit applicability rather than building or ignoring it?**

If the answer is no, stop the rescue rather than adding more municipalities.

If the answer is yes, the evidence chain itself determines what — if anything — should be engineered next.
