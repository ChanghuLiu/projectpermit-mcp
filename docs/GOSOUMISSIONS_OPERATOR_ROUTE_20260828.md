# GoSoumissions Operator Rescue Route — 2026-08-28

## Purpose

ProjectPermit needs more than one upstream marketplace/operator validation path. Oolong / Soumissions Maison is currently the strongest multi-funnel Quebec route, but relying on a single operator creates a validation single point of failure.

This note evaluates **GoSoumissions** as an independent upstream renovation/referral operator that can test the same commercial questions with a different workflow and intake design.

This is public structural evidence only. It is not E2/E3/E4/E5.

---

## 1. Why GoSoumissions is materially relevant

GoSoumissions publicly operates as an intermediary between homeowners and renovation/construction contractors.

Current terms say that users select requested services and submit contact/project information, after which GoSoumissions sends those details to the service providers most relevant to the request. The stated selection criteria principally include:

- contractor availability;
- requested service type;
- the user's region.

Source:

- `https://gosoumissions.com/termes-et-conditions`

The current homepage says a homeowner describes a renovation project, is contacted by about three verified companies on average, and selects a contractor.

Source:

- `https://gosoumissions.com/`

This is an upstream pre-contract workflow rather than a downstream permit-filing workflow.

---

## 2. Direct pre-routing internal analysis is publicly documented

The current contractor/partner page is unusually useful because it describes the internal routing boundary directly.

It states that each request sent to a contractor matches the contractor's:

- service territory / customer neighborhood;
- expertise requested by the customer;
- current availability to receive the request.

More importantly, it states:

> **all quote requests are analyzed by the internal team before they are routed.**

The page also says six additional questions were added to the intake to provide more information and help assess the seriousness of customers, allowing further filtering before contractor delivery.

Source:

- `https://gosoumissions.com/entrepreneurs`

This establishes a genuine operator-controlled decision point:

`homeowner intake -> internal analysis/filtering -> contractor invitation`

That is the relevant ProjectPermit insertion location. A permit-applicability signal would only be commercially useful if it changes something in that existing analysis/filtering/routing stage.

---

## 3. Commercial denominator concept is built into the contractor offer

GoSoumissions' partner pricing is not publicly presented simply as an unlimited generic subscription.

The current partner FAQ says the annual flat price varies according to:

- territories served;
- number of requested services;
- the **number of annual invitations promised** that the contractor wants to receive.

Source:

- `https://gosoumissions.com/entrepreneurs`

This is useful because it proves that the business already reasons operationally in terms of contractor **invitation volume**.

Important evidence boundary:

- annual invitations are downstream contractor deliveries;
- one unique homeowner project may be sent to multiple contractors;
- therefore promised annual invitations are **not** a unique upstream project denominator;
- GoSoumissions says the goal is for homeowners to compare about three bids and that a contractor competes with about two others on average, reinforcing the need to de-duplicate upstream requests before estimating ProjectPermit calls.

Do not multiply contractor invitation commitments and call the result candidate preflights.

The rescue denominator remains:

> **unique upstream project requests that would actually receive one ProjectPermit preflight before routing.**

---

## 4. Current-family coverage is strong and geographically relevant

Current public residential services include multiple ProjectPermit families or close mappings:

- `Agrandissement / extension` -> `addition`;
- `Construction de garage` -> accessory/addition-like work requiring precise normalization;
- `Construction patio, balcon ou terrasse` -> `deck_porch`;
- `Finition de sous-sol` -> `basement`;
- `Portes et fenêtres` -> `window_door`;
- `Rénovation de cuisine` -> `kitchen_bath_plumbing`;
- `Rénovation de salle de bain` -> `kitchen_bath_plumbing`;
- `Entrepreneur général` / other renovation can contain `interior_renovation` and mixed-family work.

Current cities served include:

- Laval;
- Longueuil;
- Ottawa;
- Gatineau;
- plus Quebec City, Lévis, Montreal, Trois-Rivières, Shawinigan, Drummondville and surrounding areas.

Sources:

- `https://gosoumissions.com/`
- `https://gosoumissions.com/entrepreneurs`

This gives GoSoumissions direct overlap with **four current ProjectPermit jurisdictions**: Laval, Longueuil, Ottawa and Gatineau.

That does not mean every request lies inside supported municipal boundaries; the actual geographic distribution still needs bounded partner data.

---

## 5. Intake fact surface is richer than several previously reviewed marketplaces

The current GoSoumissions request form captures before routing:

### Step 1

- name / contact information;
- **address**;
- postal code;
- planned timing;
- broad type of work.

### Step 2

The user selects one or more service categories. For each displayed service section, the current form includes:

- **required project description**;
- `Quel est votre budget?`;
- optional **project documentation** upload.

Source:

- `https://gosoumissions.com/app`

This is materially stronger than a simple postal-code + generic-description intake.

### Examples show the form is intended to capture permit-relevant details

Public examples include:

- garage: construction of a single/double garage and example budget;
- basement: segmentation of the basement into office/game/cinema/exercise/cellar uses;
- patio/deck: enlargement or new terrace construction;
- doors/windows: replace windows, **enlarge a basement window**, or replace a window+door with a sliding patio door;
- kitchen: complete rearrangement including plumbing/fixtures and budget;
- bathroom: full rearrangement including shower/taps/toilet/floor and budget.

Source:

- `https://gosoumissions.com/app`

These examples make `TEXT_DERIVABLE` permit facts plausible in real descriptions, but examples are not representative historical records.

---

## 6. Budget is promising but must not be silently mapped to Gatineau project cost

GoSoumissions asks `Quel est votre budget?` inside each service section.

This is closer to ProjectPermit's Gatineau `estimated_cost_cad` input than the unrelated financing-amount field seen on some other marketplaces.

However, public wording still does **not** prove that the field represents:

- total labour + materials before tax;
- the final expected project value;
- or the same cost definition used by Gatineau's current C$26,000 renovation threshold.

A homeowner budget can be a spending target rather than an estimate of total actual labour/material cost.

Therefore classify the current public relationship as:

> `budget_available = YES; safe_mapping_to_estimated_cost_cad = UNVERIFIED`.

A representative historical sample or operator field-definition answer is required before using it as Gatineau rule input.

---

## 7. Documents add potential fact richness, not automatic fact sufficiency

The form allows optional project documentation uploads for the displayed service sections.

That can plausibly include plans/photos or other scope evidence.

But this does not prove:

- documents are present on most relevant requests;
- they are reviewed before routing;
- ProjectPermit should parse them;
- the needed decision facts are reliably extractable;
- a document-analysis layer is economically justified.

Do not build plan/image ingestion for this route under the engineering freeze.

For a pilot, simply record whether relevant facts already exist in structured fields/description and whether documents were necessary for the operator's current human judgment.

---

## 8. Comparison with Oolong / Soumissions Maison

These two routes should remain independent rather than be blended into one Quebec marketplace thesis.

### Oolong / Soumissions Maison strengths

- multi-funnel operator structure;
- very large public historical network scale;
- current public pre-delivery sorting/team-matching evidence;
- verified Oolong ownership/data control for multiple current-family niche funnels;
- potential aggregation across many funnels.

### Oolong / Soumissions Maison uncertainties

- current partner delivery is email-first;
- schemas vary across funnels;
- convergence into one current Oolong/Soumissions Maison backend/CRM remains unverified;
- most current families still lack one or more publicly structured permit-critical facts.

### GoSoumissions strengths

- one clear platform/legal intermediary rather than a portfolio whose backend convergence is uncertain;
- explicit internal analysis before routing;
- contractor matching based on geography + expertise + availability;
- annual invitation commitments are part of contractor commercial terms;
- unified current intake exposes address + service + required description + budget + optional documents;
- four current ProjectPermit cities are explicitly served.

### GoSoumissions uncertainties

- no public unique monthly request denominator;
- promised invitations are downstream copies, not unique projects;
- no public evidence that permit applicability is considered in internal analysis;
- no public API/webhook/integration contract established in this review;
- budget semantics vs Gatineau cost definition are unverified;
- representative decision-fact sufficiency remains unknown.

Interpretation:

> GoSoumissions is valuable precisely because it is an **independent structural test** of the upstream-triage thesis, not because public evidence already proves it is a customer.

---

## 9. Outreach sent

On 2026-08-28 ProjectPermit sent `info@gosoumissions.com` a bounded aggregate question asking for the most recent complete month:

1. the approximate number of **unique** requests across current-family-like categories (addition, garage, patio/deck, basement, windows/doors, kitchen, bathroom);
2. among those, how many still required a person to determine whether a municipal permit was required before contractor routing.

Requested answer bands:

- `<100`;
- `100–249`;
- `250–499`;
- `500–999`;
- `1,000+`.

The question explicitly said that `permit is almost always already known`, `permit is not checked at this stage`, or `current fields generally cannot answer it` are equally useful responses.

Gmail message id:

- `1a049f903bc56462`

No immediate delivery failure was observed in the first post-send check.

Until a human reply arrives, outreach evidence remains **E0**.

---

## 10. Rescue gate for GoSoumissions

A credible rescue contribution requires more than a friendly reply.

### E2 / denominator

For a recent complete month:

- unique current-family requests;
- within supported municipalities;
- candidate preflight requests;
- unresolved permit-applicability subset.

Do not use contractor invitation copies as the upstream denominator.

### Fact sufficiency

For a chronological sample, measure whether existing address + service + budget + required description are:

- `DIRECT_STRUCTURED`;
- `TEXT_DERIVABLE`;
- `FOLLOWUP_REQUIRED`;
- `EXTERNAL_PROPERTY_LOOKUP_REQUIRED`;
- `INSUFFICIENT_FOR_CURRENT_RULES`.

Especially validate whether `budget` can safely map to Gatineau total project cost.

### Material workflow effect

The permit signal must change an actual internal-analysis outcome, such as:

- contractor category/routing;
- request filtering;
- human follow-up/research;
- lead quality / rejection;
- another measurable pre-delivery decision.

### Integration / build vs buy

A real operator must still prefer an external maintained municipal decision service over simply adding permit logic to its own internal analysis stack.

Resource commitment to a shadow export/integration is itself meaningful evidence.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

GoSoumissions materially diversifies the rescue evidence path and has a stronger publicly visible intake/triage structure than several prior targets.

But public evidence still does not establish:

- the unique candidate-call denominator;
- unresolved permit incidence;
- representative fact sufficiency;
- material workflow effect;
- external buy preference or payment/resource commitment.

## Bottom line

GoSoumissions is now one of the highest-quality independent Quebec upstream validation targets because it combines:

> **current-family coverage + four supported cities + required descriptions/budget/docs + explicit internal pre-routing analysis + a commercial model that already measures contractor invitation volume.**

The decisive question remains external and measurable:

> **how many unique relevant requests actually reach that internal analysis each month with permit applicability still unresolved, and would a permit result change what the team does before routing?**
