# Quebec Upstream Intake Fact Sufficiency — 2026-08-28

## Purpose

The Quebec rescue hypothesis now depends on upstream quote/intake platforms rather than downstream permit-filing vendors.

A second question follows immediately:

> even if an upstream platform has enough project volume, does it already possess enough structured facts to call ProjectPermit and obtain a useful determination without adding a long questionnaire or manual review?

This note compares current Quebec rule inputs against the publicly observable intake surfaces of two newly contacted upstream networks:

- Québec Rénovation;
- Besoindunentrepreneur.com / Optilog.

This is a **technical/distribution-friction audit**, not E2/E3/E4/E5 evidence.

Machine-readable companion:

- `data/quebec_upstream_fact_sufficiency.csv`

---

## 1. Important distinction: schema-valid is not decision-sufficient

ProjectPermit's request schema formally requires only:

- `jurisdiction`;
- `project.family`.

Source:

- `schemas/request.schema.json`

But many current deterministic rules require additional facts to reach a useful `REQUIRED` or `LIKELY_NOT_REQUIRED` branch rather than `MUNICIPAL_CONFIRMATION_REQUIRED` / `OUT_OF_SCOPE`.

Examples from current Quebec rules:

### Gatineau

For common existing-building renovation families such as:

- window/door;
- interior renovation;
- basement;
- kitchen/bath/plumbing;

Gatineau's general renovation path frequently depends on `estimated_cost_cad`, while structural/wall/foundation/opening facts can create independent permit triggers.

Gatineau property overlays can also change exemption-like outcomes through `heritage` / `piia`.

Source:

- `src/projectpermit/engine.py`

### Laval

Current examples include:

- basement: conclusive no-permit branch requires both `room_count_change=false` and `structural_change=false`;
- deck/porch: the rule depends on `yard`; a rear-yard result can change when `property.piia=true`;
- shed: threshold depends on `accessory_area_m2`, with PIIA able to change the sub-18 m² path;
- window/door: action matters, and a same-size replacement can still have a permit trigger when `distance_to_lot_line_m < 1.5`;
- interior/kitchen/bath: action plus structural/wall/room facts determine important branches.

Source:

- `src/projectpermit/quebec_expansion_rules.py`

### Longueuil

Longueuil's current rules are coarser. Several families can produce `LIKELY_REQUIRED` from the family alone, but this comes with less exemption precision. Some cases remain confirmation-oriented or out-of-scope.

Source:

- `src/projectpermit/quebec_expansion_rules.py`

Interpretation:

> the commercial integration question is not `can the platform send JSON?`; it is `how often can its existing intake produce enough facts for a useful deterministic answer without another user interaction?`

---

## 2. Québec Rénovation — publicly verified intake is relatively thin

Current public request form / workflow:

- `https://quebecrenovation.com/demande/`
- `https://quebecrenovation.com/`

The visible public form currently verifies:

- postal code;
- selected professional/service category;
- contact information;
- project-needs description / project details;
- dynamic service-specific questions exist, but the crawler does not expose a reliable complete field set for each renovation category.

The homepage explicitly says the user selects a service and shares `quelques détails sur votre projet` before receiving contractor estimates.

Important boundary:

> do **not** assume the platform collects every permit-relevant fact merely because the form is dynamic.

The current public crawl does not prove structured fields for facts such as:

- room-count change;
- structural change;
- deck yard/location;
- deck height/area;
- accessory footprint/permanence;
- opening-size change;
- distance to lot line;
- plumbing relocation;
- full civic address.

### What can likely be normalized with low friction

From a selected service + project description, a software integration could plausibly infer:

- family;
- broad action;
- obvious positive triggers explicitly stated in text, such as `add a room`, `new opening`, `build an addition`, or `new bathroom`.

But this is an inference/NLP layer, not a fact currently proven as structured upstream data.

### Full-address issue

The visible Québec Rénovation request surface verifies **postal code**, not a full civic address.

That matters because ProjectPermit's Gatineau address adapter can resolve decision-changing `heritage` / `piia` context only from usable address/property resolution. Laval and Longueuil currently have no address adapters at all.

See:

- `docs/ADDRESS_AWARE_VALUE_AUDIT.md`

Therefore postal-code-only intake is not equivalent to address-aware permit preflight.

---

## 3. Besoindunentrepreneur.com — richer possible data, but completeness is unproven

Public privacy policy:

- `https://besoindunentrepreneur.com/politique-de-confidentialite/`

The company says project/property information it may collect can include:

- address;
- project type;
- budget;
- region;
- property type;
- number of storeys;
- property value;
- lot dimensions;
- land area;
- construction date;
- renovation/maintenance history;
- building plans/images;
- similar property characteristics.

This is materially richer than Québec Rénovation's currently visible generic request form and suggests that a low-friction ProjectPermit call is technically more plausible in some workflows.

But the evidence boundary is critical:

> a privacy policy describes categories of information the company **may collect**; it does not prove that every relevant homeowner lead contains those fields, that they are structured, or that they are present before contractor routing.

It also does not prove capture of several permit-specific booleans/numerics such as:

- structural change;
- room-count change;
- new vs same-size opening;
- plumbing relocation;
- deck yard;
- accessory permanence;
- PIIA/heritage status.

Those may be derivable from free text/plans or require follow-up.

---

## 4. Family-by-family integration friction

### Lowest-friction current family: addition

Across Gatineau, Laval and Longueuil, a clearly normalized `addition` family already routes to a permit-positive result in the current rules.

This is the strongest candidate for a one-shot upstream call from a basic service-selection workflow.

The commercial problem is that `addition -> permit likely/required` may also be easy for the platform or contractor to know internally, so low fact friction does **not** imply high willingness to pay.

### Highest-friction families

#### Basement

Laval needs room-count/structural facts for the most useful exemption branch; Gatineau's general path needs cost plus structural context.

A generic `basement renovation` lead is not enough to reproduce those distinctions safely.

#### Window / door

The high-value distinction is often not `windows` but:

- same-size replacement vs changed/new opening;
- structural impact;
- location/property constraints;
- in Laval, potential lot-line distance condition.

These are not publicly verified as ordinary upstream form fields.

#### Deck / porch

Laval currently needs `yard`; Gatineau can be affected by property overlays. Neither is proven from Québec Rénovation's visible request fields.

#### Accessory structure

Gatineau needs permanence/movability; Laval's deterministic shed threshold needs structure kind + area and can be affected by PIIA. Again, generic category selection is insufficient.

### Medium-friction families

Kitchen/bath/plumbing and generic interior renovation may be inferable from a sufficiently detailed description, but current Gatineau/Laval rules still depend on cost/action/structural/plumbing facts in meaningful branches.

---

## 5. New metric: decision-fact sufficiency rate

The Quebec rescue should add a new measurement alongside volume and uncertainty:

> **decision-fact sufficiency rate = upstream candidate cases where existing captured data is sufficient for a useful ProjectPermit determination without manual research / all upstream candidate cases.**

Do not substitute `address available` or `project description available` for this metric.

Recommended classification for representative E3 cases:

- `DIRECT_STRUCTURED` — existing structured fields are enough;
- `TEXT_DERIVABLE` — enough detail exists in existing description and can be normalized conservatively;
- `FOLLOWUP_REQUIRED` — one or more decision-changing facts must be asked;
- `EXTERNAL_PROPERTY_LOOKUP_REQUIRED` — address/property resolution is needed;
- `INSUFFICIENT_FOR_CURRENT_RULES` — current rule coverage itself cannot produce a useful result.

### Rescue interpretation

A platform with 1,000 relevant requests/month is **not** a 1,000-call low-friction opportunity if most calls require several new questions or manual plan review.

A future E2/E3 partner should therefore provide or allow us to sample both:

1. how many relevant projects occur;
2. what facts are already present at the insertion point.

---

## 6. Distribution / product implication

There are two possible outcomes, and they should not be conflated.

### A. Existing intake is usually sufficient

This would support the original external preflight API model:

`existing quote/intake record -> normalize -> ProjectPermit -> decision`

No new questionnaire would be needed.

### B. Existing intake is often insufficient

Then ProjectPermit is not really a passive one-call enrichment product. It would need one of:

- an interactive follow-up-question layer;
- platform-specific structured-field mapping;
- reliable conservative NLP extraction;
- external property/GIS enrichment;
- or frequent `CONFIRMATION_REQUIRED` output.

Each option adds friction, integration work or lowers decision value.

**Do not build any of these now.**

First verify which case is true from representative upstream records.

---

## 7. Score impact

**No immediate score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

Reason:

- the public Québec Rénovation surface demonstrates a credible fact-gap risk;
- Besoindunentrepreneur demonstrates that richer upstream data can exist;
- neither proves representative fact completeness or insufficiency.

A future distribution-fit downgrade would be justified if representative E2/E3 evidence shows that the majority of otherwise-qualifying upstream cases cannot reach a useful determination without new user questions/manual research.

Conversely, a high decision-fact sufficiency rate would remove one major integration objection but would still not prove willingness to pay.

## Bottom line

The Quebec rescue now has **three independent gates**, not two:

1. **volume:** enough relevant upstream projects exist;
2. **uncertainty:** permit applicability is genuinely unresolved at that stage;
3. **fact sufficiency:** the existing record contains enough decision facts to automate the answer with low friction.

Only after those three gates should build-vs-buy/economics and E4/E5 determine whether ProjectPermit deserves renewed engineering.
