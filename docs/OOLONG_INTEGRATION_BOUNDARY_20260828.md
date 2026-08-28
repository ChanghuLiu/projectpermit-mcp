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

## 2. Historical technical evidence supports reusable cross-site form infrastructure

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

## 3. Current form surfaces remain compatible with a centralized enrichment concept

Current public forms reviewed on 2026-08-28 include structured hidden/visible request identifiers and project fields.

Examples:

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

## 4. Stronger current operator-centralization evidence

The current Oolong partner model is more important than the exact WordPress plugin:

- Oolong lets partners choose the **type**, **territory** and **quantity** of leads;
- Oolong describes itself as performing collection and a selection/qualification process before delivery;
- Oolong publicly frames the business as lead-to-deal performance marketing rather than independent site hosting.

That means a permit-applicability signal could theoretically be inserted in a central operator qualification/routing step even if the underlying consumer sites use different forms.

The relevant integration question is therefore not merely:

> `Do all sites use the same WordPress plugin?`

It is:

> `Is there one operator-side lead record / routing stage where multiple funnels can be enriched before partner delivery?`

Only Oolong can confirm that.

---

## 5. Integration classification today

Public evidence supports:

- `CENTRAL_OPERATOR_CONTROL = YES`
- `MULTI_FUNNEL_DATA_COLLECTION = YES`
- `PUBLIC_PARTNER_DELIVERY = EMAIL_FIRST`
- `HISTORICAL_SHARED_FORM_INFRASTRUCTURE = YES`
- `CURRENT_SHARED_CRM_OR_DATABASE = UNVERIFIED`
- `PUBLIC_PARTNER_API_OR_WEBHOOK = NOT_FOUND`
- `ONE_INTEGRATION_ACROSS_CURRENT_FAMILY_FUNNELS = UNVERIFIED`

Therefore the correct current ProjectPermit integration classification remains:

> **UNKNOWN — central operator integration plausible, but not externally demonstrated.**

Do not mark Oolong as `CENTRAL_SINGLE_INTEGRATION` or `CENTRAL_WITH_SITE_MAPPING` until a human/operator or direct technical artifact confirms it.

---

## 6. Economic consequence

This boundary cuts both ways.

### Positive

A centralized operator may already own the collection/qualification step, so ProjectPermit would not necessarily need a separate business relationship with every niche site.

If one internal operator integration reaches several relevant funnels, integration cost `I` can be amortized across a larger `N`.

### Negative

Because the public partner product is email-first rather than an exposed API ecosystem, a ProjectPermit pilot likely requires **Oolong's internal engineering/operations cooperation**.

That cooperation is itself valuable evidence:

- committing staff to map fields, configure a webhook/shadow process or export chronological cases is resource commitment;
- refusing custom integration because email delivery is sufficient is negative evidence;
- saying the team would add the permit logic directly to its own shared WordPress/backend stack is strong build-vs-buy negative evidence.

Therefore an integration discussion should be treated as part of E5/resource validation, not as a free implementation assumption.

---

## 7. Highest-value human questions

If Oolong responds, ask only after the bounded denominator/workflow questions:

1. Do the relevant renovation funnels converge into one internal lead record/CRM/routing process before partner email delivery?
2. Can one enrichment step see leads from multiple funnels, or would each site need separate work?
3. Are the relevant forms still based on a shared Gravity Forms/WordPress pipeline, or has the architecture changed?
4. Could a shadow permit-preflight result be attached to the internal lead before partner routing without changing homeowner-facing behavior?
5. Would Oolong rather call an externally maintained service or implement municipal permit logic inside its existing shared stack?

Do not build a Gravity Forms plugin or webhook before these answers exist.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

This review strengthens the claim that Oolong is a genuine centralized lead operator and weakens the assumption that an off-the-shelf public API already exists.

That makes Oolong a better **validation target**, but not an easier validated integration.

## Bottom line

The operator route remains credible, but the integration thesis should now be stated precisely:

> Oolong appears to centralize lead collection, qualification and email delivery across many niches, and historically used reusable WordPress/Gravity Forms infrastructure. A single internal enrichment point is plausible, but no current public partner API/webhook or confirmed shared CRM insertion point has been found.

The next proof must come from Oolong's workflow/technical response, not more speculative engineering.
