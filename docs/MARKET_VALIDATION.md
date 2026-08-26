# ProjectPermit Market Validation

Updated: 2026-08-26

## Executive decision

**Continue ProjectPermit, but do not treat Gatineau + Ottawa as the commercial market.**

Phase 0 proved the deterministic rules engine, public MCP/x402 transports, paid settlement, and Bazaar discovery. The business thesis now depends on becoming a **cross-jurisdiction permit-requirements intelligence layer for software agents and contractor/property platforms**, not another homeowner-facing `Do I need a permit?` wizard.

The near-term objective is therefore:

> normalized project + address -> permit/authority requirements + trigger rules + overlays + official evidence + uncertainty

The server should remain deterministic and evidence-linked. The calling Agent can perform natural-language scope extraction.

## Why the positioning changed

Gatineau now operates **URBAIN**, its own address-aware virtual urban-planning assistant. URBAIN explicitly answers whether a permit is needed, uses a structured questionnaire, takes location into account, points users to documents/fees/application channels, and keeps unusual cases with municipal staff. This validates the problem, but also means a single-city consumer wizard is not a defensible product.

Ottawa remains more fragmented: it has strong permit pages and digital application workflows, but the City still exposes permit requirements mainly through project pages and staff/service channels rather than one generalized cross-project assistant.

The durable differentiation is therefore **normalization across municipalities**. A contractor/property-management/design Agent should not need a different workflow for every city.

## Market evidence

### Canada

- Statistics Canada reported **C$149.7B** in total building-permit value in 2025 and **308,600 residential dwelling units authorized**, a record number of units.
- The Building Permits Survey covers about **2,400 municipalities representing roughly 95% of Canada's population**.
- Canada had **159,514 construction employer establishments** and **255,892 non-employer/indeterminate establishments** in 2025. The narrower `Construction of buildings` category had 49,546 employers and 94,658 non-employer/indeterminate establishments.
- Ottawa received **6,258 construction applications and issued 5,657 permits in the first three quarters of 2024**. Annualizing the permit count gives about **7,543 permits/year** as a model input, not an official annual total.
- Gatineau recorded **3,230 building permits in 2025** according to APCHQ's Statistics Canada-based municipal table.
- Ottawa's year-end 2025 population estimate is **1,116,170**; Gatineau states a population of about **298,000**.

These two local observations imply roughly **6.8 to 10.8 permit records per 1,000 residents per year**. Applying that range to Canada's April 1, 2026 population of 41.417M produces a rough **280k-450k annual permit-record model**. This is an inference, not an official national permit-count statistic.

### United States upside

- The U.S. Census Bureau reported **1,431,616 new privately owned housing units authorized by building permits in 2025**, with a valuation of about US$379B. This covers new residential units only, not the full renovation/commercial permit universe.
- Harvard JCHS projected owner-occupied home improvement and repair spending at **US$509B in 2025**; its July 2026 outlook projects about **US$519B through mid-2027**.
- PermitStack advertises **82M+ historical U.S. permit records across 8,000+ cities** and exposes an MCP/API with tiers up to 100k requests/day. This is adjacent rather than direct competition: it searches historical/issued permits, whereas ProjectPermit answers prospective requirements.

The U.S. is therefore the path to a much larger call market, but only after the Canadian cross-jurisdiction engine proves repeatable maintenance economics.

## Call-volume model

The central business metric is **monthly paid API/MCP calls**, not number of permit applications alone.

### Two-city Phase 0 ceiling

Ottawa annualized permit input + Gatineau actual 2025 permits is about **10,773 permit events/year**.

Assumption: prospective preflight demand is **2-4x issued permit events**, because some projects are scoped before application, abandoned, changed, or determined not to need a permit.

That gives only about **1,800-3,600 preflight events/month** across the two cities even at 100% market capture.

Revenue ceiling from those calls:

| Price/call | Approx. monthly revenue at full two-city preflight volume |
|---:|---:|
| $0.01 | $18-$36 |
| $0.10 | $180-$359 |
| $0.25 | $449-$898 |
| $0.50 | $898-$1,795 |

**Conclusion: $0.01 is a test/discovery price, not a viable commercial price. Gatineau + Ottawa are a technical proving ground, not a standalone business.**

### Canada event-based TAM model

Inputs:

- modeled permit records: **280k-450k/year**
- preflight-event multiplier: **2-4x**
- paid calls per preflight workflow: **1-1.5** (basic rule result plus optional address/overlay/bundle call)

This produces an estimated full-market technical call opportunity of roughly **47k-224k paid calls/month**.

| Canada share | Monthly paid calls | Revenue @ $0.25 | Revenue @ $0.50 |
|---:|---:|---:|---:|
| 5% | 2.3k-11.2k | $0.6k-$2.8k | $1.2k-$5.6k |
| 10% | 4.7k-22.4k | $1.2k-$5.6k | $2.3k-$11.2k |
| 30% | 14.0k-67.3k | $3.5k-$16.8k | $7.0k-$33.7k |

These are scenario calculations, not revenue forecasts. They show that **Canada alone can plausibly support a small profitable bootstrapped API if distribution and city coverage are strong**, but the narrow preflight product is unlikely to be a large venture-scale market without U.S. expansion or higher-value workflow bundles.

### Platform-distribution model

Selling one contractor at a time is not the preferred route. A platform can concentrate demand.

Example:

- 10,000 active contractor/property users inside one software integration
- 2-4 permit-preflight workflows/user/month
- 1-1.5 paid calls/workflow

= **20k-60k calls/month from one successful platform integration**.

Five integrations of that size = **100k-300k calls/month**. At $0.25/call this is $25k-$75k/month gross; at $0.50/call it is $50k-$150k/month gross.

This is why the primary buyer should be a software/Agent platform, while contractors/property managers are the end users.

## Pricing thesis

Do not commercialize the current testnet price.

Recommended eventual structure, only after external demand is demonstrated:

- **Free**: capability discovery, supported jurisdictions, source freshness/status
- **$0.05-$0.10**: simple jurisdiction-level requirement check without property-specific overlays
- **$0.20-$0.50**: address-aware evidence-linked permit preflight; this should be the core paid SKU
- **$1-$3**: project bundle only when reliably supported: all likely permits/authorities, fees, required documents, overlays, and source provenance

Adjacent pricing supports room above pennies. SiteWire sells Canadian permit-data API capacity at $49/month for 10k calls, $199 for 100k, and $699 for 1M, while its broader Pro product is C$799/month. PermitStack's U.S. permit-search API advertises Business capacity of 100k requests/day for $149/month. Those vendors sell permit-history/data access rather than prospective rule intelligence, so their prices are references, not direct comparables.

## Buyer priority

1. **Contractor / home-service software and Agents** - repeated jobs, repeated municipalities, clear workflow fit.
2. **Property-management / maintenance platforms** - many properties and recurring alterations/repairs.
3. **Construction PM / estimating / design software** - permit preflight before quoting and design finalization.
4. **Permit automation vendors** - ProjectPermit can be an upstream routing/requirements component rather than competing on submission operations.
5. **PropTech / real-estate due diligence / lender / insurer workflows** - useful when planned or past work affects a property decision.
6. **Municipal software vendors** - later; sales cycles and procurement are slower.

Avoid making direct homeowners the acquisition engine. Their per-user frequency is too low.

## Competitor map

### Direct local workflow competitor

**Gatineau URBAIN** is the clearest warning. It already performs address-aware permit orientation for common projects and explicitly frames results as informational, not as the permit itself. ProjectPermit should not try to win by cloning URBAIN for each city.

### Adjacent data/API competitors

- **PermitStack**: U.S. permit-history/search MCP/API; 82M+ records, 8,000+ cities.
- **SiteWire**: Canadian permit/project data and REST API across 31 cities and growing.
- Other permit-data providers can answer `what permits were issued?`; ProjectPermit should focus on `what requirements apply to this proposed work?`.

### Full permitting workflow competitors

Permit-automation platforms focus on preparation, submission, tracking, and managed workflows. ProjectPermit should remain the small upstream deterministic rules layer rather than entering document/BIM review or managed permit submission too early.

## Expansion-city scorecard

Scores are directional (5 = favorable). `Competition` scores how favorable the competitive gap is, so 5 means little direct official assistant competition.

| City | Demand/volume | Competition | Rule clarity | Machine/open-data leverage | Maintenance/reuse | Priority |
|---|---:|---:|---:|---:|---:|---:|
| Toronto | 5 | 4 | 5 | 3 | 5 | **1** |
| Mississauga | 3 | 4 | 5 | 4 | 5 | **2** |
| Laval | 3 | 4 | 5 | 3 | 4 | **3** |
| Longueuil | 3 | 4 | 4 | 5 | 4 | **4** |
| Vancouver | 4 | 4 | 4 | 5 | 3 | **5** |
| Calgary | 5 | 2 | 4 | 5 | 3 | **6** |
| Montréal | 5 | 2 | 3 | 3 | 1 | **7** |

Rationale:

- Toronto has a large market and a very explicit official `required/not required` rule page. Ontario reuse from Ottawa lowers implementation cost.
- Mississauga also publishes a clear project list and benefits from Ontario rule-model reuse.
- Laval has unusually machine-friendly deterministic permit pages; for example, same-size window/door replacement is explicitly distinguished from dimension changes.
- Longueuil exposes online permit workflows plus ArcGIS permit layers, making property/data adapters attractive.
- Vancouver has excellent open permit data and substantial alteration volume, but introduces a new provincial rule family.
- Calgary has very high housing/building activity and open data, but the City already provides interactive questionnaires for some project types, reducing the simple-preflight gap.
- Montréal has the biggest Quebec demand but borough fragmentation creates high maintenance cost; Saint-Laurent already offers an `Assistant-permis`. Fragmentation can become a moat later, but it is inefficient for the next increment.

## Product boundary for the next phase

Keep ProjectPermit narrow:

**Input**
- jurisdiction/address
- normalized project family/action
- structural/use/plumbing/mechanical facts
- known property facts

**Output**
- likely permit requirement(s)
- competent authority
- trigger rule(s)
- relevant property/zoning/heritage overlays when machine-verifiable
- required documents/fees only where authoritative and maintainable
- official evidence URLs and rule/source versions
- explicit uncertainty / municipal confirmation state

Do not expand now into:

- plan/BIM code-compliance review
- permit application submission on behalf of users
- legal approval guarantees
- paid third-party property datasets unless demand justifies them
- server-side LLM interpretation

## 30-day validation gates

### Build gate

Add **Toronto + Mississauga + Laval + Longueuil + Vancouver** before broad marketing. This turns the product from a two-city demo into a visibly cross-jurisdiction engine while preserving low cash cost.

### Demand gate

After 5-city expansion, pursue external usage rather than more plumbing. Target:

- at least **3 external Agent/platform developers** using the endpoint/MCP
- at least **100 non-owner external calls** that are not generated by our own smoke scripts
- at least **one repeated user/integration** making 20+ calls
- at least **one buyer conversation where $0.20-$0.50/call or an equivalent monthly plan is acceptable**

### Scale gate

Do not expand to 20+ Canadian municipalities until at least one of these occurs:

- 1,000 external calls/month,
- a platform integration with a credible path to 10k+ calls/month,
- or a paying design partner requests specific new municipalities.

If external demand remains near zero after multi-city coverage + targeted outreach, pause expansion and compare the same x402/MCP infrastructure against the Heavy Haul opportunity instead of accumulating rules indefinitely.

## Sources / research snapshot

- Statistics Canada, Building permits, December 2025 / annual review: https://www150.statcan.gc.ca/n1/daily-quotidien/260211/dq260211a-eng.htm
- Statistics Canada, population estimates Q1 2026: https://www150.statcan.gc.ca/n1/daily-quotidien/260617/dq260617a-eng.htm
- ISED Canadian Industry Statistics, Construction (NAICS 23): https://ised-isde.canada.ca/app/ixb/cis/businesses-entreprises/23?lang=eng
- ISED Canadian Industry Statistics, Construction of buildings (NAICS 236): https://www.ised-isde.canada.ca/app/ixb/cis/businesses-entreprises/236
- City of Ottawa Draft Budget 2025 (Q1-Q3 2024 construction activity): https://documents.ottawa.ca/sites/default/files/Draft%20Budget%202025%20Magazine.pdf
- City of Ottawa year-end 2025 population: https://ottawa.ca/en/living-ottawa/statistics-and-demographics/current-population-and-household-estimates/sub-area-year-end-2025
- APCHQ, 2025 building permits bulletin: https://media.apchq.com/QNt4vKT4SLm-Vr62aZcTVQ/26126-com-bulletin_permis_batir_2026_v02c.pdf
- Gatineau URBAIN: https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Furbain_assistant_virtuel_urbanisme
- Toronto permit-required guidance: https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
- Mississauga permit-required guidance: https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
- Laval renovation permit guidance: https://www.laval.ca/reglements-permis/trouver-mon-permis/renovation-residentielle-exterieure/
- Longueuil online permits: https://www.longueuil.quebec/fr/services/amenagement-urbanisme/demande-de-permis-en-ligne
- Vancouver issued building-permit open data: https://opendata.vancouver.ca/explore/dataset/issued-building-permits/
- Calgary deck permit questionnaire: https://www.calgary.ca/development/home-building/deck-questionnaire.html
- Montréal / Saint-Laurent Assistant-permis: https://montreal.ca/articles/soumettre-une-demande-de-permis-saint-laurent-5197
- U.S. Census, 2025 Annual Building Permits: https://www.census.gov/construction/bps/pdf/annual_highlights.pdf
- Harvard JCHS remodeling outlook: https://www.jchs.harvard.edu/benchmark-update-lifts-remodeling-market-size-projections
- PermitStack MCP: https://github.com/PermitStack/permitstack-mcp
- SiteWire developers/API pricing: https://sitewire.ca/developers

## Bottom line

**GO, with a narrower business thesis and a wider jurisdiction footprint.**

The engine/payment plumbing is no longer the main risk. The main risks are now:

1. distribution into high-frequency B2B Agent workflows,
2. whether address-aware preflight is worth at least roughly $0.20 per result,
3. whether city-rule maintenance scales faster than revenue.

The next code investment should therefore be reusable jurisdiction tooling plus the first five expansion cities, while every additional city must be justified by a call-volume or design-partner signal.
