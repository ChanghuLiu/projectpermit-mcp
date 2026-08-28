# Oolong Integration Boundary — 2026-08-28

## Purpose

`docs/OOLONG_OPERATOR_AGGREGATION_ROUTE_20260828.md` established that Oolong Media controls or centrally handles multiple Quebec quote funnels, including current-family-relevant funnels such as Soumissions Cuisine and Soumissions Plomberie.

This addendum asks a narrower question:

> does public evidence support a low-friction **technical** operator-level integration, or only a centralized commercial/data operator that would still need custom internal integration work?

This remains public structural evidence only. It is not E2/E3/E4/E5.

---

## 1. Current public partner-delivery model is email-first

Oolong's current partner page says:

- **1,000,000+ requests processed since 2015**;
- **40+ niches** served across Quebec;
- partners can define territory, lead quantity and lead type;
- Oolong handles advertising, collection, selection and delivery;
- leads are delivered **directly into the partner's email inbox**.

Sources:

- `https://oolongmedia.ca/devenir-partenaire/`
- `https://oolongmedia.ca/foire-aux-questions-oolong-media/`

The current FAQ likewise describes a performance model where partners receive qualified quote requests directly by email and pay for delivered prospects rather than clicks/impressions.

Interpretation:

> Oolong clearly has centralized operational control over lead collection/qualification/distribution, but the public partner-facing delivery surface is not presented as an API, webhook or developer platform.

A targeted current public scan did not find Oolong partner API/webhook documentation or a public developer portal.

Absence of public documentation does not prove an internal/private integration does not exist.

---

## 2. A real pre-delivery qualification / triage stage is publicly documented

A current Soumissions Maison partner page states that **each quote request is analyzed and sorted by the team before it is sent to a partner**. It also states that an inappropriate request can be credited and redirected to another collaborator.

A separate current Soumissions Maison page gives an even clearer process description:

1. the consumer completes the online form;
2. the request is automatically routed to a **sorting/triage centre (`centre de tri`)**;
3. team members carefully analyze it;
4. the request is transferred to the best-qualified partners according to criteria those partners set.

Sources:

- `https://www.soumissionsmaison.com/inscription-comme-partenaire/`
- `https://www.soumissionsmaison.com/obtenez-de-nouveaux-clients/`

This is stronger insertion-point evidence than generic claims about lead generation.

It establishes that at least this public Soumissions Maison workflow has a real operator-controlled decision stage **after intake and before partner delivery**.

That stage is conceptually where a ProjectPermit result could matter, for example by influencing:

- which partner category receives the request;
- whether a request needs more human validation;
- whether it is held, redirected or considered unsuitable;
- whether additional project information is required before delivery.

However, public evidence still does **not** establish that:

- Soumissions Cuisine and Soumissions Plomberie use exactly this same triage centre/process;
- all Oolong-controlled renovation funnels converge into one shared lead record;
- permit applicability is currently considered during triage;
- permit information would materially change any triage decision;
- current-family permit uncertainty occurs frequently enough to matter.

Therefore this finding strengthens the **insertion-point hypothesis**, not the denominator, fact-sufficiency, material-effect or buy-preference evidence.

---

## 3. Historical technical evidence supports reusable cross-site form infrastructure

An Oolong frontend-developer recruiting page published in 2021 described work on high-traffic Oolong sites and explicitly required developers to:

- build WordPress themes/plugins shareable across multiple applications/sites;
- work with a backend developer;
- recreate/modernize Oolong sites;
- **reuse Gravity Forms as the one WordPress extension that had to remain**.

Source:

- `https://oolongmedia.ca/poste-a-combler-developpeur-frontend/`

The same page repeats Oolong's public description of 50+ online quote comparators generating thousands of request forms per month.

This is useful historical evidence that Oolong deliberately used reusable cross-site web/form infrastructure.

But it is not proof that, in 2026:

- all relevant funnels still use Gravity Forms;
- all forms share one database or CRM;
- one webhook can be configured once for every funnel;
- historical WordPress architecture remains unchanged.

Do not convert a 2021 implementation detail into a current integration contract.

---

## 4. Current form surfaces remain compatible with a centralized enrichment concept

Current public forms reviewed on 2026-08-28 include structured hidden/visible request identifiers and project fields.

### Soumissions Plomberie

Current public form exposes:

- a unique/request ID field;
- city;
- full civic address;
- postal code;
- planned date;
- nature of work;
- required service type;
- property type;
- owner status;
- required detailed work description.

Source:

- `https://www.soumissionsplomberie.com/`

### Soumissions Cuisine

Current public form exposes:

- submission ID;
- region/postal code;
- planned date;
- owner status;
- work type;
- detailed project description.

Source:

- `https://soumissionscuisine.ca/`

These field surfaces support the idea that ProjectPermit could be inserted after form capture without creating a completely new consumer questionnaire for every case.

They do not reveal the server-side form processor or prove one shared technical endpoint.

---

## 5. Stronger current operator-centralization evidence

The current operator model is more important than the exact WordPress plugin:

- Oolong lets partners choose the **type**, **territory** and **quantity** of leads;
- Soumissions Maison publicly documents a **pre-delivery team triage stage**;
- requests can be redirected when unsuitable for a particular partner;
- Oolong publicly frames the business as lead-to-deal performance marketing rather than independent site hosting.

That means a permit-applicability signal could theoretically become an input to an existing qualification/routing decision rather than create an entirely new workflow.

The key question is no longer simply:

> `Do all sites use the same WordPress plugin?`

It is:

> `Do the relevant Oolong-controlled renovation funnels converge into one operator-side lead/triage record where a permit signal can be evaluated before partner delivery?`

Only Oolong can confirm that boundary.

---

## 6. Integration classification today

Public evidence supports:

- `CENTRAL_OPERATOR_CONTROL = YES`
- `PRE_DELIVERY_TRIAGE_STAGE = YES_FOR_PUBLIC_SOUMISSIONS_MAISON_WORKFLOW`
- `MULTI_FUNNEL_DATA_COLLECTION = YES`
- `PUBLIC_PARTNER_DELIVERY = EMAIL_FIRST`
- `HISTORICAL_SHARED_FORM_INFRASTRUCTURE = YES`
- `CURRENT_SHARED_CRM_OR_DATABASE = UNVERIFIED`
- `CURRENT_FAMILY_FUNNELS_SHARE_DOCUMENTED_TRIAGE_STAGE = UNVERIFIED`
- `PUBLIC_PARTNER_API_OR_WEBHOOK = NOT_FOUND`
- `ONE_INTEGRATION_ACROSS_CURRENT_FAMILY_FUNNELS = UNVERIFIED`

Therefore the correct current ProjectPermit integration classification remains:

> **UNKNOWN — a real pre-delivery operator triage point is documented, but a shared current-family technical insertion point is not externally demonstrated.**

Do not mark Oolong as `CENTRAL_SINGLE_INTEGRATION` or `CENTRAL_WITH_SITE_MAPPING` until a human/operator or direct technical artifact confirms it.

---

## 7. Economic consequence

This boundary cuts both ways.

### Positive

A centralized operator already has a qualification/routing stage, so ProjectPermit may not need to invent a new operational step.

If one internal enrichment point reaches several relevant funnels, integration cost `I` can be amortized across a larger `N`.

### Negative

Because the public partner product is email-first rather than an exposed API ecosystem, a ProjectPermit pilot likely requires **Oolong's internal engineering/operations cooperation**.

That cooperation is itself valuable evidence:

- committing staff to map fields, configure a webhook/shadow process or export chronological cases is resource commitment;
- refusing custom integration because existing triage/email delivery is sufficient is negative evidence;
- saying the team would add permit logic directly to its own shared WordPress/backend/triage stack is strong build-vs-buy negative evidence.

Therefore an integration discussion should be treated as part of E5/resource validation, not as a free implementation assumption.

---

## 8. Highest-value human questions

If Oolong responds, ask only after the bounded denominator/workflow questions:

1. Do Soumissions Cuisine, Soumissions Plomberie and the other relevant renovation funnels pass through the same pre-delivery triage/routing process described publicly by Soumissions Maison?
2. Do those funnels converge into one internal lead record/CRM/routing process before partner email delivery?
3. What decisions does the triage team currently make, and would knowing `permit required / likely not / municipal confirmation needed` change any of them?
4. Can one enrichment step see leads from multiple funnels, or would each site need separate work?
5. Could a shadow permit-preflight result be attached before partner routing without changing homeowner-facing behavior?
6. Would Oolong rather call an externally maintained service or implement municipal permit logic inside its existing shared stack?

Do not build a Gravity Forms plugin or webhook before these answers exist.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

This review now proves more than generic centralization: a real public pre-delivery triage stage exists in the Soumissions Maison workflow.

But it still does not establish:

- current-family candidate volume;
- unresolved permit incidence;
- shared current-family triage/CRM topology;
- material effect of permit information;
- external buy/resource commitment.

That makes Oolong a better **validation target**, not a validated integration.

## Bottom line

The operator route should now be stated precisely:

> Oolong/Soumissions Maison publicly documents an operator-controlled triage step between form intake and partner delivery, while Oolong historically used reusable WordPress/Gravity Forms infrastructure. ProjectPermit therefore has a plausible existing insertion point, but no current public API/webhook or confirmed shared current-family CRM/triage integration has been found.

The next proof must come from Oolong's workflow/technical response, not more speculative engineering.
