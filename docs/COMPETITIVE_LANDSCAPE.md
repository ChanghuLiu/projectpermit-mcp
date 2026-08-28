# ProjectPermit Competitive Landscape

Updated: 2026-08-28

## Purpose

ProjectPermit is no longer evaluating an empty market. Current public evidence shows multiple products that already automate some or most of the path from `address + project scope` to permit requirements.

This document separates **functional overlap** from the narrower commercial wedge ProjectPermit still needs to prove.

The current ProjectPermit hypothesis is **not**:

> a generic homeowner permit guide, municipal portal, plan-review system, permit filing service, or broad land-intelligence platform.

The surviving hypothesis is narrower:

> **A low-cost, developer-accessible, evidence-linked building-permit-applicability API/MCP for third-party software and agents, callable before an estimate, quote, work order, or capital-project decision, across multiple Canadian municipalities without requiring each municipality to procure and configure the product.**

This remains a hypothesis, not a validated moat.

## Competitive matrix

`Public API` means a developer-facing programmatic surface was publicly described. `Self-serve API` is stricter: a developer can obtain access without a sales/implementation engagement. `Not found` means the 2026-08-28 public review did not find one; it does not prove a private interface does not exist.

| Product | Primary buyer / workflow | Permit applicability overlap | Geography observed | Evidence / citations | API / integration access | Public pricing / access | Threat to current wedge |
|---|---|---|---|---|---|---|---|
| **One Ontario + LandLogic / Parcella** | Ontario applicants, municipalities, developers, industry; idea -> requirements -> application -> approval | **High**. One Ontario says users can describe a project in plain language and the platform identifies requirements, explains what is possible, checks compliance, prepares applications, and guides approval. | Ontario; designed as province-wide shared infrastructure. Long-term expansion beyond Ontario is stated. | One Ontario owners/developers: `https://www.oneontario.ca/owners-and-developers`; AI for Housing: `https://www.oneontario.ca/ai-for-housing`; LandLogic partner announcement: `https://www.oneontario.ca/latest-updates/landlogic-joins-ai-for-housing` | **Yes, but engagement-led.** LandLogic publicly offers configurable data/report APIs and pilot conversational-AI integrations. One Ontario says the platform will support direct integrations. No self-serve permit-determination API/key flow was found. | First phase of One Ontario / Parcella can be tried free. LandLogic API pricing is not public in the reviewed pages; integrations begin with demo/configuration. | **Very high in Ontario.** This invalidates any moat based only on Canada, cross-jurisdiction data, conversational UI, or API-accessible land intelligence. |
| **Clariti Guide** | Local governments; pre-application customer self-service | **High**. Guide asks project/address questions, uses GIS and work planned to determine applicable rules, helps users apply for the right permit, and can filter people who do not need a permit. | North American municipal deployments; strong U.S. Guide case evidence. Clariti itself is Canada-based and other Clariti products are used in Canada. | Guide: `https://www.claritisoftware.com/products/guide`; Santa Clarita case: `https://www.claritisoftware.com/resources/case-studies/santa-clarita-ca`; Camino/Clariti overview: `https://camino.ai/` | Guide can integrate with any permitting software. Clariti Enterprise exposes flexible APIs. Public evidence does **not** show a universal self-serve third-party Guide API spanning municipalities without municipal configuration. | Population-based municipal pricing; demo/implementation engagement. | **Very high functionally**, lower on the exact third-party SaaS distribution model. Do not position ProjectPermit as a municipal homeowner permit guide. |
| **QwikScope Greenlight** | Developers / feasibility teams / AEC; project/site feasibility before submittal | **Very high**. Input project + scope; resolves jurisdiction; returns required / likely / conditional permits, issuing agency, dependencies, fees, timelines and risk. | Public platform coverage is stated as 3,000+ **U.S. counties** on the shared property stack. No Canadian Greenlight coverage was found in this review. | Greenlight: `https://qwikscope.com/greenlight/`; platform/API engagement: `https://qwikscope.com/` | **Yes, engagement-led.** Greenlight explicitly says `API access (on engagement)`; broader QwikScope offers API-key integrations, widgets and white-label engagements. | Greenlight is self-serve, but a public Greenlight per-run/API price was not found. API is engagement-based. | **Very high product-shape threat**, currently reduced by observed U.S.-only coverage and non-self-serve API access. |
| **Permitech** | Residential contractors and homeowners; permit intelligence through filing/closeout | **Very high**. Exact-address local code/GIS research says whether a permit is needed and preserves official evidence. | 7,000+ jurisdictions mapped, but company states primary operating region is **Illinois / Wisconsin / Indiana** and not every mapped jurisdiction is fully researched. No Canadian coverage found. | Main: `https://www.permitech.io/`; about: `https://www.permitech.io/about`; story: `https://www.permitech.io/our-story`; pricing: `https://www.permitech.io/pricing` | No public developer API/self-serve API was found in the reviewed site. Product combines structured data, AI, automation and **human permit-technician judgment**. | Free permit check; DIY package $60/project; Done For You from $199/project; custom/monthly contractor operations for volume. | **Very high contractor-workflow threat in its U.S. region**, reduced for ProjectPermit by geography, human-service cost structure, and lack of a public developer API. |
| **PermitMint** | Homeowners, contractors, realtors; fast building-permit lookup | **High** for the core `do I need a permit?` question. | U.S. only. Methodology reports 1,835 cities/counties and 171,221 researched permit rules; current data center tracks 1,842 U.S. jurisdictions. | About: `https://permitmint.com/about.php`; methodology: `https://permitmint.com/methodology`; data center: `https://permitmint.com/data/`; lookup: `https://permitmint.com/lookup.php` | **No public API.** PermitMint says research/journalist API access is case-by-case and no public API is published. | Permit lookup is free/no account. Lookup page showed `306 lookups this week` during the 2026-08-28 review. | **Strong proof that structured cited permit-applicability rules are not unique.** Current threat to Canadian B2B/API wedge is lower because U.S.-only + no public product API. |
| **BC Building Permit Hub** | B.C. homeowners, contractors, architects and participating local governments; standardized permit application workflow | **Medium–high**, mainly after a user starts the permit workflow. Shows jurisdiction-specific requirements, building bylaws/zoning and additional permits/reports; provides code-compliance tools. | B.C.; launched with 12 local governments + 2 First Nations, with government reporting work with ~40 communities and province-wide intent. | Current hub: `https://www2.gov.bc.ca/gov/content/housing-tenancy/building-or-renovating/permits/building-permit-hub`; launch roadmap: `https://news.gov.bc.ca/releases/2024HOUS0028-000817`; digital tools: `https://www2.gov.bc.ca/gov/content/industry/construction-industry/building-codes-standards/innovation` | Public B.C. API infrastructure exists generally, but no public third-party Building Permit Hub permit-applicability API was found in this review. | Government service; applicant BCeID workflow. | **High strategic pressure in B.C.** Cross-jurisdiction provincial infrastructure is not a ProjectPermit moat, even if the exact pre-quote API surface remains different. |
| **SiteWire** | Canadian proptech / developers / sales intelligence; issued permit and pre-permit data | **Low direct overlap.** It is permit-history / contractor / lead intelligence, not `permit required?` determination. | 31 Canadian cities. | Developer API: `https://sitewire.ca/developers` | **Yes, self-serve REST API/key.** | Public pricing exists on SiteWire; not used here as applicability competitor evidence. | **Adjacent proof** that Canadian permit data can be productized as a developer API, but it does not answer the core applicability question. |
| **PermitBird** | Software/agents that need environmental permit determinations | **Low on building permits, high on product pattern.** | U.S. environmental permitting domains. | `https://permitbird.com/` | Public REST API + MCP / sandbox observed in prior review. | Public developer access pattern. | **Category proof** that a permit-determination layer can be agent/API-native; not a direct residential building-permit competitor. |
| **ProjectPermit (current)** | Hypothesis: third-party contractor/property/construction software and agents before quote/work-order approval | Current 8 deterministic residential project families; official evidence + rule version; address-aware adapters where available | Small set of Canadian municipalities across ON/QC/BC | Repository rules/tests and municipal first-party sources | Local API/MCP architecture exists; no externally proven distribution yet | Working hypothesis ~$0.20–$0.50/address-aware call; **no E5 evidence** | **Unproven.** Has no validated moat until external buyers demonstrate why this surface is materially better than existing alternatives. |

## What is already commoditized

The competitor review invalidates several previously tempting differentiators.

ProjectPermit must **not** claim uniqueness merely because it offers:

- `address + project scope -> permit requirements`;
- jurisdiction resolution;
- GIS/property context;
- local-rule normalization;
- official-source citations;
- a plain-language permit answer;
- cross-jurisdiction property intelligence;
- an API integration;
- an AI/conversational interface;
- a pre-application permit guide.

All of those capabilities exist somewhere in the current market.

## The narrower wedge that remains to be tested

No reviewed competitor was publicly observed offering **all** of the following together:

1. **Canadian multi-province building-permit applicability**, not only U.S. coverage or one government-configured jurisdiction;
2. **third-party SaaS / agent as the buyer**, rather than municipal procurement or a homeowner portal;
3. **developer self-service**, rather than `book a demo`, implementation consulting, or `API on engagement`;
4. **permit-specific machine contract**, such as a deterministic `REQUIRED / LIKELY_NOT_REQUIRED / CONFIRMATION_REQUIRED` result with rule version and official evidence;
5. **low marginal cost / no mandatory human reviewer per call**;
6. **lightweight per-call economics** suitable for a quote, estimate, work-order, or agent workflow;
7. **MCP / agent-native invocation** in addition to ordinary REST/API use.

This absence is only a **public-market gap observation**. It is not evidence that customers value the combination or that a competitor cannot add it quickly.

## Canada-specific competitive pressure

### Ontario

Ontario is the highest-threat province.

- One Ontario explicitly aims to unify permitting across all 444 municipalities.
- LandLogic already standardizes Ontario zoning/planning/property data across jurisdictions and sells configurable APIs to third parties.
- Parcella / One Ontario already lets users discuss project requirements and move toward permit requests.
- LandLogic is actively piloting conversational-AI integrations and says One Ontario will support direct integrations.

**Implication:** ProjectPermit should not expand Ontario coverage merely to build a broader rules database. An Ontario integration must prove a buyer-specific advantage that One Ontario/LandLogic does not already satisfy.

### British Columbia

B.C. has already built shared multi-jurisdiction government infrastructure through the Building Permit Hub and continues expanding it.

**Implication:** `works across multiple B.C. municipalities` is not enough. The only defensible B.C. reason to continue is a third-party pre-quote/API workflow that the Hub does not serve.

### Quebec

The current review found no comparable province-wide Quebec permit-intelligence/API platform. Quebec's own guidance emphasizes municipality-specific permit/certificate rules, and municipal assistants exist individually. LandLogic's current Terms explicitly state that its services are not available in Quebec.

**Implication:** Quebec appears to have more public whitespace than Ontario/B.C., but this must not be mistaken for commercial demand. French-language maintenance, municipality-by-municipality rule variance, and a smaller reachable software-channel denominator may make the whitespace uneconomic.

## Competitor evidence that raises the bar

The market category itself is real:

- Clariti Guide has municipality case studies showing 1,000+ users in Santa Clarita's first four months and that no-permit users were successfully filtered before visiting the counter.
- PermitMint's public lookup showed 306 lookups in a week and has built more than 170k structured U.S. permit rules.
- Permitech was born from a permit technician handling up to 200 permit lookups/week and now sells contractor permit operations.
- QwikScope has productized permit determination as a dedicated module with API access on engagement.
- One Ontario / LandLogic and B.C. are investing in shared government permitting infrastructure.

This is **category validation**, not validation of ProjectPermit's business model.

## Revised differentiation gate

Before investing materially in new municipalities, new project families, marketplace certifications, or production-grade adapters, ProjectPermit should obtain evidence for **both** distribution and differentiation.

A credible differentiation proof should include at least one of:

- **two independent third-party software/integration buyers** explicitly state that current municipal portals / One Ontario / LandLogic / Clariti / existing permit services do not fit their pre-quote or work-order use case, and identify why;
- one partner supplies a bounded current-family workflow where an existing alternative would require municipality procurement, manual research, expensive implementation, or human permit operations, while a ProjectPermit-style API can be called directly;
- one external pilot demonstrates that the same integration calls ProjectPermit across **multiple municipalities** and would otherwise need separate rule integrations or manual research;
- one buyer accepts a concrete per-call or paid-pilot term specifically for the machine-readable evidence-linked determination rather than for filing/expediting work.

### Competitor-triggered pause conditions

Pause or materially narrow ProjectPermit if any of the following becomes true before E4/E5:

- LandLogic / One Ontario exposes a self-serve permit-requirement API that satisfies the same third-party Canadian workflow at a competitive cost;
- another provider exposes a Canada-wide or multi-province self-serve `address + scope -> permit applicability` API with adequate citations and maintenance;
- target SaaS/integrators repeatedly say their existing municipal portal, LandLogic, Clariti, QwikScope-like vendor, or permit-service partner already solves the decision well enough;
- the only remaining differentiation is `cheaper`, without evidence of enough paid call volume to support rule maintenance;
- Quebec/other whitespace requires high manual rule-maintenance cost but produces too little bounded partner volume.

## Current strategic reading

As of 2026-08-28:

> **The broad permit-guide idea is crowded and should be considered rejected.**

> **The contractor/property-software permit-intelligence category also has direct U.S. competitors; it is not a greenfield category.**

> **A narrower Canadian developer/agent API wedge remains plausible but unvalidated.**

The next milestone is therefore not another feature or municipality. It is evidence that a real third-party software buyer needs this exact integration shape despite the alternatives above.

## Source notes

High-value first-party sources reviewed on 2026-08-28:

- One Ontario owners/developers: `https://www.oneontario.ca/owners-and-developers`
- One Ontario AI for Housing: `https://www.oneontario.ca/ai-for-housing`
- One Ontario / LandLogic technology partner: `https://www.oneontario.ca/latest-updates/landlogic-joins-ai-for-housing`
- LandLogic API integration: `https://www.landlogic.ai/integration`
- LandLogic platform: `https://www.landlogic.ai/`
- LandLogic Terms: `https://www.landlogic.ai/terms`
- Clariti Guide: `https://www.claritisoftware.com/products/guide`
- Clariti Santa Clarita: `https://www.claritisoftware.com/resources/case-studies/santa-clarita-ca`
- QwikScope Greenlight: `https://qwikscope.com/greenlight/`
- QwikScope platform/API engagement: `https://qwikscope.com/`
- Permitech: `https://www.permitech.io/`
- Permitech story: `https://www.permitech.io/our-story`
- Permitech pricing: `https://www.permitech.io/pricing`
- PermitMint methodology: `https://permitmint.com/methodology`
- PermitMint data/API access note: `https://permitmint.com/data/`
- PermitMint lookup: `https://permitmint.com/lookup.php`
- B.C. Building Permit Hub: `https://www2.gov.bc.ca/gov/content/housing-tenancy/building-or-renovating/permits/building-permit-hub`
- B.C. digital construction tools: `https://www2.gov.bc.ca/gov/content/industry/construction-industry/building-codes-standards/innovation`
- SiteWire developer API: `https://sitewire.ca/developers`
