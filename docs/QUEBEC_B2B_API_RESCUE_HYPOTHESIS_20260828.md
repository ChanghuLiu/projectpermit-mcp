# Quebec B2B/API Rescue Hypothesis — 2026-08-28

## Purpose

ProjectPermit is now at the 50/100 pause / re-scope boundary. The broad Canada thesis no longer justifies product investment because Ontario's remaining external cross-city whitespace is substantially occupied by LandLogic / Parcella / One Ontario, while B.C. is increasingly standardized through public infrastructure.

One geographic re-scope remains worth falsifying before a final No-Go decision:

> **Quebec-only, French-first, cross-municipality B2B permit-applicability API with deterministic/auditable output.**

This is a rescue hypothesis, not a recommendation to build more Quebec coverage.

## Why Quebec is structurally different from Ontario

LandLogic's current public Terms state that its services are not available in Quebec.

Source:

- `https://www.landlogic.ai/terms`

That removes the strongest delivered Ontario external competitor from the immediate Quebec market.

However, this does **not** mean Quebec is empty. It means the competitive shape is different.

## Consumer / municipal permit-checking is already crowded

### Assistant Rénovation QC

Assistant Rénovation QC publicly says it helps Quebec homeowners identify permits and tracks **69 municipalities**. It combines permit guidance, renovation subsidies, documents and a homeowner report.

Source:

- `https://assistantrenovationquebec.ca/`

Its public product is homeowner-facing. The current review did not find public developer API documentation, partner API pricing, enterprise embedding, webhook/MCP delivery or a third-party software integration program.

Absence from public search is not proof that no private API exists.

### Ville de Québec Assistant-permis

Ville de Québec operates an address/property-specific Assistant-permis that validates whether a permit or certificate is required for planned work.

Its public flow takes:

- address / postal code / lot;
- permit category;
- nature of work;
- property-specific context.

Source:

- `https://www.ville.quebec.qc.ca/services/assistant-permis/index.aspx`

The City's public result model is conceptually close to ProjectPermit's safety-oriented triage: work can be permit-required, permit-not-required, or require contacting the City for verification.

This is strong evidence that `permit required?` itself is not a product innovation in Quebec.

### Other municipal/self-service tools

Current reviewed Quebec cities also expose substantial direct guidance or assistants:

- Gatineau: URBAIN virtual urbanism assistant;
- Laval: detailed permit-required / no-permit renovation tables plus property-specific overlays;
- Longueuil: machine-readable permit/GIS and municipal regulatory surfaces;
- Québec City: address-aware Assistant-permis.

Therefore a Quebec rescue must **not** be positioned as a better homeowner checker.

## Builder-software competition also exists

BuilderAI is Quebec-native contractor software and publicly embeds urbanism/permit reasoning in the estimate workflow. Its Laval demonstration was previously checked against Laval's official renovation guidance.

Source:

- `https://www.builder-ai.ca/`

This proves that a Quebec vertical SaaS can internalize municipal guidance rather than buying a separate permit API.

## What public search still did not find

The current focused scan did **not** find a publicly documented Quebec-wide product that combines all of the following:

1. third-party B2B/developer delivery;
2. cross-municipality Quebec coverage;
3. project-scope/address input;
4. permit-applicability output before application;
5. deterministic/auditable source-linked contract;
6. ordinary API / webhook / MCP-style reuse across many customers.

This is the only plausible remaining whitespace.

It must be treated as **unproven public-market whitespace**, not proof of demand or absence of private/internal competitors.

## Public API infrastructure is not the same thing

The Régie du bâtiment du Québec (RBQ) currently exposes an API Developer Portal with account signup and API-product discovery.

Source:

- `https://portail-prd.api.rbq.gouv.qc.ca/`

The currently visible public portal does not establish a municipal residential permit-applicability API; the reviewed public product content includes example/developer infrastructure rather than a cross-municipality `permit required?` service.

This matters because Quebec is technically capable of public API delivery, but the existence of an API portal should not be misclassified as competitive evidence for ProjectPermit's exact layer.

## Buyer-pool signal is large enough to justify one rescue test

The APCHQ currently represents **more than 28,000 businesses** in Quebec residential construction and renovation across 13 regional associations.

Sources:

- `https://www.apchq.com/a-propos/reseau-de-l-apchq/`
- `https://www.apchq.com/`

APCHQ's February 2026 forecast also expects residential renovation spending to grow about **8% in 2026** after a strong 2025 rebound.

Source:

- `https://www.apchq.com/actualites/previsions-2026-2027-apchq/`

A separate April 2026 APCHQ survey found **64%** of Quebec homeowners in its target sample planned at least C$5,000 of renovation/maintenance within three years.

Source:

- `https://www.apchq.com/actualites/renovation-au-quebec-malgre-lincertitude-economique-64-percent-des-proprietaires/`

These are market-size signals only. They do not measure permit-preflight calls.

## Platform-scale sensitivity — the key rescue arithmetic

SoumissionRénovation has publicly reported Quebec-wide project activity around **155,000 projects in 2025** and a contractor network around **17,500**.

Important evidence boundary:

- the exact 155k metric has already been found ambiguous between `projects completed` and `projects submitted/platform activity` in ProjectPermit's earlier research;
- it is not a clean upstream opportunity denominator;
- it includes many projects outside ProjectPermit's current families;
- it does not measure permit uncertainty.

Therefore use it only for sensitivity arithmetic.

If 155,000 annual platform projects were the upper activity base, that is about **12,917 projects/month**.

To produce ProjectPermit calls at different uncertain-preflight shares:

| Qualifying pre-contract uncertainty share | Approx. calls/month |
|---:|---:|
| 1% | 129 |
| 3.9% | 500 |
| 5% | 646 |
| 10% | 1,292 |
| 15% | 1,938 |
| 15.5% | 2,000 |
| 20% | 2,583 |

Interpretation:

- the original **500 calls/month** gate needs roughly **3.9%** of a Quebec-wide 155k/year activity stream to become genuine qualifying pre-contract permit-applicability calls;
- the stronger **2,000 calls/month** gate needs roughly **15.5%**;
- because only a subset maps to current families and the 155k metric is not a clean intake denominator, the real required unresolved-incidence share would be higher.

This makes direct-contractor acquisition a weak rescue path. The plausible rescue requires **province-wide aggregation** through a platform, software vendor, integrator or industry workflow.

## Why the current three Quebec cities are insufficient evidence

ProjectPermit's current Quebec coverage is Gatineau, Laval and Longueuil.

Earlier public research already closed the path to deriving a defensible SoumissionRénovation denominator for just those covered cities and current families. Public sources confirm Quebec-wide scale and presence in covered cities but do not expose the required city × family × upstream-uncertainty denominator.

See:

- `docs/SOUMISSIONRENOVATION_PUBLIC_DENOMINATOR_CLOSURE_20260828.md` or the corresponding merged public-denominator research if file naming differs in the repository history.

Therefore **do not add Montreal, Quebec City or other municipalities merely to make the denominator look larger**.

Coverage expansion is only justified after a credible Quebec software/platform buyer proves the workflow and asks for the additional geography.

## Rescue gate

The Quebec-only thesis survives only if one credible province-wide or multi-customer buyer supplies all four elements:

### Gate A — bounded repeated incidence

A recent complete-month or similarly bounded denominator showing enough renovation opportunities/quotes where permit applicability is unresolved before contract.

Target:

- **>=500 current-family qualifying events/month** for minimum rescue evidence;
- **>=2,000/month** for a materially stronger platform case.

### Gate B — current-family fit

The denominator must exclude routine repairs and unrelated trades. A meaningful share must map to families ProjectPermit can actually decide safely.

### Gate C — differentiation from existing Quebec tools

The buyer must explain why the workflow is not already adequately solved by:

- municipal assistants/pages;
- Assistant Rénovation QC;
- BuilderAI/internal AI/RAG;
- manual permit specialists;
- municipality-specific customer support.

The missing capability should be specifically reusable B2B/API automation, auditable/reproducible evidence, cross-city maintenance or similar.

### Gate D — build-vs-buy / economics

The buyer must prefer an external maintained layer over internal logic for a concrete reason and accept commercially useful economics or allocate integration resources.

A statement that an API would be "nice to have" is insufficient.

## Highest-value Quebec rescue targets

1. **SoumissionRénovation / RenoQuotes** — strongest visible province-wide project aggregation; public city/current-family denominator is unavailable, so only internal/partner data can clear the gate.
2. **Elper** — Quebec contractor-management SaaS with broad customer footprint; needs explicit repeated pre-quote incidence + build-vs-buy preference.
3. **APCHQ / regional associations** — not a direct API buyer by default, but a strong neutral route for representative incidence or member workflow measurement.
4. **BuilderAI / other Quebec contractor software** — mainly a build-vs-buy comparator; a preference for external cross-city maintenance would be positive evidence, while internalization preference is negative.
5. **Assistant Rénovation QC** — competitive/API-boundary target: public product is multi-municipality consumer-facing; a private partner API would materially weaken the rescue thesis.

## Engineering policy

Until a Quebec rescue gate clears:

**Do not:**

- add Montreal;
- add Quebec City;
- add more Quebec project families;
- build a Quebec-specific consumer app;
- build integrations for Elper/SoumissionRénovation speculatively;
- add paid data sources;
- market the product as Quebec-wide.

**Allowed:**

- buyer/incidence research;
- representative E3 cases from existing Quebec coverage;
- exact competitor/API verification;
- French-language validation material;
- a small adapter/integration change only when a credible partner requires it to run a real trial.

## Score implication

**No score increase. ProjectPermit remains 50/100 pause / re-scope.**

LandLogic's Quebec exclusion creates a plausible geographic rescue hypothesis, but Quebec's consumer/municipal checker layer is already crowded and the B2B/API call-volume denominator is unobserved.

The score should rise only after external evidence clears the rescue gate. Public market size or apparent API whitespace is insufficient.

## Bottom line

Quebec is not a reason to restart development.

It is one last, tightly bounded falsification path:

> **Can a province-wide Quebec software/platform workflow generate enough repeated pre-contract permit-applicability calls, and will that buyer pay specifically for a cross-municipality deterministic/auditable API instead of using municipal/consumer tools or internal logic?**

If the answer is no, the geographic re-scope fails and the remaining ProjectPermit thesis should move toward No-Go rather than further expansion.