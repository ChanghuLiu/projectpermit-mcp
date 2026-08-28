# Build-vs-Buy Buyer Geographic Breadth — 2026-08-28

## Why geographic breadth matters now

The build-vs-buy maintenance baseline changed the buyer-selection logic.

ProjectPermit currently supports seven jurisdictions and maintains 155 deterministic rule IDs, but a narrow scope-only local checker can require only 1–9 core rule/guidance sources in the current cities. Toronto and Mississauga each currently have one primary scope rule/guidance source in the maintained source manifest.

Therefore:

> **single-city / few-city software is a strong test of whether local permit logic is cheap enough to build internally.**

> **multi-municipality / multi-region software is the stronger test of whether shared cross-city maintenance is worth buying.**

Do not ask both buyer types the same generic `would permit checking be useful?` question.

## Buyer class A — cross-municipality / cross-region buy candidates

### Elper — strongest current Quebec cross-municipality buyer test

Public evidence:

- Elper states that its customers grow with the product `partout au Québec`;
- its current free-trial page states **600+ satisfied companies**;
- it covers the workflow from quotation to invoicing, with electronic quote approval and accepted-quote-to-project conversion;
- it serves general contractors and multiple construction trades;
- its public product remains Quebec-focused rather than a single-city product.

Sources:

- `https://elper.pro/`
- `https://elper.pro/essai-gratuit/`
- `https://elper.pro/application-gestion-suivi-chantiers/`

Interpretation:

Elper is now more valuable as a build-vs-buy falsification target than a generic single contractor because its customer base plausibly spans many Quebec municipalities.

The useful question is **not** whether one local contractor wants permit help. It is:

> Across Elper's Quebec contractor base, does municipality-by-municipality permit maintenance create enough repeated pre-quote burden that Elper would rather consume a maintained shared capability than build local rules internally?

Still missing:

- monthly quote/project denominator;
- current-family share;
- covered-municipality share;
- unresolved permit-incidence before quote approval;
- API/partnership route;
- willingness to pay.

`600+ companies` is not a ProjectPermit call denominator.

### Buildxact — strongest current broad-platform build-vs-buy test

Public evidence:

- Buildxact has a dedicated Canadian product and Canadian pricing site;
- it is designed for residential builders/remodelers from takeoff/estimating through quote and project management;
- its public company page currently reports **988,783 quotes produced**;
- its customer messaging says the product is trusted by residential builders worldwide.

Sources:

- `https://www.buildxact.com/ca/`
- `https://www.buildxact.com/ca/pricing/`
- `https://www.buildxact.com/ca/company/about/`
- `https://www.buildxact.com/ca/our-customers/builders-remodelers/`

Existing direct-contact evidence from 2026-08-27:

- Buildxact Support confirmed a REST API path for programmatic tenant-data access;
- Support redirected broader commercial/data questions to Sales;
- ProjectPermit already asked for a recent-month aggregate validation point and has not received a bounded answer.

Interpretation:

Buildxact is useful because a broad residential-construction platform is more exposed to jurisdiction fragmentation than a city-local SaaS.

The next useful Buildxact evidence is not another API-access question. It is one of:

1. a bounded Canada/Ontario current-family quote denominator;
2. an explicit build-vs-buy view on municipality-specific permit maintenance;
3. a concrete reason LandLogic/municipal tools/internal AI do or do not fit.

Important boundary:

> **988,783 quotes is a public aggregate/global cumulative product metric, not Canadian monthly volume and not permit-preflight volume.**

Do not use it in SAM or call forecasts.

## Buyer class B — local-build comparator

### Contrax — strongest current internal-build falsification target

Public evidence:

- Contrax is built in Oshawa, Ontario by a renovation contractor;
- it targets Canadian small renovation/trade businesses, especially roughly 2–15 person crews;
- its workflow is site walkthrough/video -> AI-written scope -> priced estimate -> project;
- it covers kitchens, baths, basements, decks, additions and multiple trades;
- it explicitly embeds Canadian/Ontario concerns such as CAD/HST rather than treating them as external integrations.

Sources:

- `https://getcontrax.net/`
- `https://getcontrax.net/estimating-software-for-contractors`
- `https://getcontrax.net/estimating-software-for-contractors.html`

Interpretation:

Contrax is **not currently supported by public evidence as a large cross-municipality distribution buyer**. Its value is the opposite:

> if a small Ontario-focused AI-native contractor SaaS says it would simply build the relevant municipal permit logic itself, that is strong negative build-vs-buy evidence for ProjectPermit.

ProjectPermit already sent the founder the direct build-vs-buy question on 2026-08-28.

Do not reinterpret a future `we would build it ourselves` answer as merely `small customer` feedback. It is exactly the local internalization hypothesis this target is meant to test.

## Revised interpretation matrix

| Target | Current role | Geographic-breadth evidence | Highest-value answer |
|---|---|---|---|
| Elper | Cross-municipality Quebec buy candidate | 600+ companies; customers across Quebec | `We do/do not want to maintain municipality-specific permit rules across our customer footprint, because...` |
| Buildxact | Broad platform buy candidate | Dedicated Canada product + global builder footprint | Bounded Canada/Ontario denominator + build-vs-buy reason |
| Contrax | Local-build comparator | Canada positioning but strongly anchored in Oshawa/Ontario small renovation | `We would build locally` vs `we would buy shared maintenance`, with reason |

## What this changes

This changes **target interpretation**, not the ProjectPermit score.

Current score remains **53/100** because:

- no cross-municipality software buyer has said the shared-maintenance burden is worth paying to outsource;
- no bounded current-family monthly denominator has been supplied;
- Contrax has not yet answered the local-build question;
- Elper has only sent an automatic receipt;
- Buildxact has confirmed an integration surface but not market incidence or purchase intent.

## Next evidence rule

Do not count a positive feature-interest reply equally across these targets.

For **Elper / Buildxact** a useful positive answer must explain why owning regulatory logic across regions is undesirable or uneconomic.

For **Contrax** a useful negative answer can be just as valuable: if a representative local vertical SaaS can cheaply internalize its relevant municipality set, ProjectPermit's standalone buy case weakens.

No new city or feature should be built to influence these answers.
