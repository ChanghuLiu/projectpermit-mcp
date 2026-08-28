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

### Renovation itself is inside an operator-handled workflow

A current Soumissions Maison renovation page is directly relevant to ProjectPermit's existing families. It includes renovation work such as:

- doors/windows;
- bathroom work;
- additions/house extensions;
- garage work;
- other interior/exterior renovation.

Its live form captures fields including:

- unique request ID;
- full civic address;
- city and postal code;
- property type;
- type/nature of work;
- owner status;
- planned date;
- required detailed work description.

The page says the **Soumissions Maison team identifies the renovation contractors that best match the consumer's criteria and needs**, and its service description says submitted information is handled by the team and sent to three regional renovation contractors.

Source:

- `https://www.soumissionsmaison.com/renovation-et-travaux/`

This removes a material ambiguity from the earlier review: team handling is not documented only for real-estate/professional-service leads; there is a directly current-family-adjacent **renovation intake -> team matching -> contractor delivery** workflow.

It also makes this renovation funnel one of the strongest public fact-sufficiency candidates found so far because the intake already includes address plus structured work attributes and free text.

### Ownership / technical identity boundary still matters

The current Soumissions Maison terms describe Soumissions Maison itself as collecting/managing/transmitting submitted data. They do **not** directly name Oolong Media Inc. as the current legal owner/data controller of `soumissionsmaison.com`.

At the same time, current Soumissions Maison pages:

- credit site creation to Oolong Media;
- contain partner testimonials describing business with Oolong Media;
- include author/team biographies stating Oolong Media staff participate in management of companies partnered with Soumissions Maison.

Sources:

- `https://www.soumissionsmaison.com/conditions-utilisation/`
- `https://www.soumissionsmaison.com/annoncez-avec-nous/`
- `https://www.soumissionsmaison.com/obtenez-de-nouveaux-clients/`

These are strong operational-link signals, but they are **not substituted for a direct current legal-ownership statement**.

Keep two evidence chains separate:

1. **Soumissions Maison renovation triage / team handling** — directly evidenced on current Soumissions Maison pages;
2. **Oolong ownership/data control of Soumissions Cuisine and Soumissions Plomberie** — independently evidenced in those sites' terms.

The unresolved commercial/technical question is whether those chains converge into the same current internal lead record/CRM/triage infrastructure.

Therefore this finding strengthens the **insertion-point and fact-sufficiency hypotheses**, not the denominator, shared-topology, material-effect or buy-preference evidence.

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

### Soumissions Maison renovation

Current renovation intake exposes a particularly strong operator-side candidate surface:

- unique ID;
- full address, city and postal code;
- property type;
- type and nature of work;
- ownership;
- timing;
- detailed description.

Source:

- `https://www.soumissionsmaison.com/renovation-et-travaux/`

These field surfaces support the idea that ProjectPermit could be evaluated **after existing form capture** rather than require a wholly new consumer questionnaire for every case.

They do not reveal the server-side processor or prove one shared technical endpoint.

---

## 5. Stronger current operator-centralization evidence

The current operator model is more important than the exact WordPress plugin:

- Oolong lets partners choose the **type**, **territory** and **quantity** of leads;
- Soumissions Maison publicly documents a **pre-delivery team triage stage**;
- the Soumissions Maison renovation funnel itself uses team matching and already captures address/scope facts;
- requests can be redirected when unsuitable for a particular partner;
- Oolong publicly frames the business as lead-to-deal performance marketing rather than independent site hosting.

That means a permit-applicability signal could theoretically become an input to an existing qualification/routing decision rather than create an entirely new workflow.

The key question is no longer simply:

> `Do all sites use the same WordPress plugin?`

It is:

> `Do the relevant Oolong-controlled renovation funnels converge into the same operator-side lead/triage record evidenced by the Soumissions Maison renovation workflow, where a permit signal can be evaluated before partner delivery?`

Only Oolong/Soumissions Maison can confirm that boundary.

---

## 6. Integration classification today

Public evidence supports:

- `CENTRAL_OPERATOR_CONTROL = YES_FOR_OOLONG_VERIFIED_FUNNELS`
- `PRE_DELIVERY_TRIAGE_STAGE = YES_FOR_PUBLIC_SOUMISSIONS_MAISON_WORKFLOW`
- `RENOVATION_TEAM_MATCHING_STAGE = YES_FOR_SOUMISSIONS_MAISON_RENOVATION`
- `RENOVATION_STRUCTURED_ADDRESS_SCOPE_INTAKE = YES`
- `PUBLIC_PARTNER_DELIVERY = EMAIL_FIRST`
- `HISTORICAL_SHARED_FORM_INFRASTRUCTURE = YES`
- `CURRENT_SHARED_CRM_OR_DATABASE = UNVERIFIED`
- `OOLONG_VERIFIED_CURRENT_FAMILY_FUNNELS_SHARE_SOUMISSIONS_MAISON_TRIAGE = UNVERIFIED`
- `PUBLIC_PARTNER_API_OR_WEBHOOK = NOT_FOUND`
- `ONE_INTEGRATION_ACROSS_CURRENT_FAMILY_FUNNELS = UNVERIFIED`

Therefore the correct current ProjectPermit integration classification remains:

> **UNKNOWN — a real current renovation pre-delivery team-matching point and strong intake surface are documented, but convergence with Oolong-verified current-family funnels into one technical insertion point is not externally demonstrated.**

Do not mark Oolong as `CENTRAL_SINGLE_INTEGRATION` or `CENTRAL_WITH_SITE_MAPPING` until a human/operator or direct technical artifact confirms it.

---

## 7. Economic consequence

This boundary cuts both ways.

### Positive

A renovation operator workflow already has human/team matching after structured intake, so ProjectPermit may not need to invent a new operational step.

If one internal enrichment point reaches several relevant funnels, integration cost `I` can be amortized across a larger `N`.

### Negative

Because the public partner product is email-first rather than an exposed API ecosystem, a ProjectPermit pilot likely requires **internal engineering/operations cooperation**.

That cooperation is itself valuable evidence:

- committing staff to map fields, configure a webhook/shadow process or export chronological cases is resource commitment;
- refusing custom integration because existing triage/email delivery is sufficient is negative evidence;
- saying the team would add permit logic directly to its own shared WordPress/backend/triage stack is strong build-vs-buy negative evidence.

Therefore an integration discussion should be treated as part of E5/resource validation, not as a free implementation assumption.

---

## 8. Highest-value human questions

If Oolong/Soumissions Maison responds, ask only after the bounded denominator/workflow questions:

1. Does the current Soumissions Maison renovation workflow and Oolong-controlled funnels such as Soumissions Cuisine / Soumissions Plomberie converge into one internal lead record/CRM/triage process before partner email delivery?
2. How many **unique** renovation/current-family requests crossed that process in the most recent complete month, and how many would actually be candidates for permit preflight?
3. At triage, how often is permit applicability unresolved, and what decision would `required / likely-not / municipal-confirmation-needed` actually change?
4. Can one enrichment step see leads from multiple funnels, or would each site need separate work?
5. Could a shadow permit-preflight result be attached before partner routing without changing homeowner-facing behavior?
6. Would the operator rather call an externally maintained service or implement municipal permit logic inside its existing shared stack?

Do not build a Gravity Forms plugin or webhook before these answers exist.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

This review now establishes two commercially useful structural facts:

- a real public pre-delivery triage/team-matching stage exists;
- a current-family-adjacent renovation funnel already captures a strong address + structured-scope input surface before contractor delivery.

But it still does not establish:

- current-family candidate volume;
- unresolved permit incidence;
- convergence of Oolong-verified funnels with the Soumissions Maison renovation triage/backend;
- material effect of permit information;
- external buy/resource commitment.

That makes the route a better **validation target**, not a validated integration.

## Bottom line

The integration thesis should now be stated precisely:

> Soumissions Maison publicly demonstrates a current renovation intake -> team matching/triage -> contractor delivery workflow with strong address/scope facts, while separate terms prove Oolong ownership/data control for current-family funnels such as Soumissions Cuisine and Soumissions Plomberie. The unresolved proof is whether these surfaces converge into one current technical lead/triage layer that can be enriched once.

The next proof must come from operator workflow/technical evidence, not more speculative engineering.
