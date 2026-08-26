# ProjectPermit Distribution Validation Plan

Updated: 2026-08-26

## Decision

**Stop expanding municipalities mechanically after the current seven-jurisdiction footprint. Validate distribution and repeated call volume first.**

ProjectPermit now has enough technical breadth to test the commercial thesis: seven municipal rule jurisdictions, five address-aware first-party GIS adapters, HTTP + MCP + x402 transports, and proven payment/discovery plumbing. The next unknown is not whether another city can be implemented; it is whether permit preflight becomes a repeated software workflow with enough paid calls.

The commercial target remains a small upstream decision primitive:

> address + normalized project scope -> likely permit/authority requirements + property overlays + official evidence + explicit uncertainty

ProjectPermit should be embedded before quoting, scheduling, design finalization, work-order approval, or full permit submission. It should **not** become a managed permit-submission company.

## 2026 distribution evidence

These figures are distribution-surface indicators, not additive TAM; the customer bases overlap and no source states that every user needs permit preflight.

| Distribution surface | Current scale signal | Why it matters |
|---|---:|---|
| U.S. construction employers | **814,557 establishments** in 2023 County Business Patterns | Very large fragmented contractor base; official Census benchmark |
| Canadian construction industry | **159,514 employer + 255,892 non-employer/indeterminate establishments** in 2025 | More than 415k establishments; strongest immediate rules geography |
| ServiceTitan | **12,000+ businesses served; 40M+ jobs completed annually** | High-frequency HVAC/plumbing/electrical/roofing/service workflows; direct App Marketplace path |
| Procore | **17,850 customers** at 2025 year-end | Owners, GCs and specialty contractors; APIs and App Marketplace are core platform capabilities |
| AppFolio | **22,096 property-management customers; 9.4M units under management** at 2025 year-end | Large recurring maintenance/capex/work-order surface; Stack marketplace uses APIs |
| Autodesk Construction | Trusted by builders on **2M+ projects** | Large project workflow surface and existing construction integration ecosystem |

### Sources

- U.S. Census Bureau, 2023 County Business Patterns, NAICS 23 Construction: https://data.census.gov/table/CBP2023.CB2300CBP?codeset=naics~23&g=010XX00US
- ISED Canadian Industry Statistics, Construction NAICS 23 (2025): https://ised-isde.canada.ca/app/ixb/cis/businesses-entreprises/23?lang=eng
- ServiceTitan overview for App Marketplace partners, updated 2026-07-11: https://help.servicetitan.com/docs/servicetitan-overview-for-app-marketplace-partners
- ServiceTitan partner ecosystem: https://www.servicetitan.com/partners
- Procore 2025 Form 10-K: https://www.sec.gov/Archives/edgar/data/1611052/000162828026011055/pcor-20251231.htm
- AppFolio 2025 Form 10-K: https://www.sec.gov/Archives/edgar/data/1433195/000143319526000011/appf-20251231.htm
- AppFolio Stack marketplace: https://www.appfolio.com/stack
- Autodesk Construction: https://construction.autodesk.com/

## Call-volume model: workflow first, permit counts second

Raw municipal permit filings are a lower-frequency lagging measure. The more useful model is how often a contractor/property platform reaches a **decision point before work begins**.

ServiceTitan provides the cleanest current public workflow denominator: **40M+ jobs annually**. The following is an illustrative scenario only; ServiceTitan does not publish the percentage of jobs that are permit-sensitive, and ProjectPermit has no ServiceTitan integration today.

### ServiceTitan theoretical workflow opportunity

Assume one preflight call for a permit-sensitive job:

| Assumed permit-sensitive share of 40M jobs | Candidate preflights/year | Candidate preflights/month |
|---:|---:|---:|
| 5% | 2.0M | ~167k |
| 10% | 4.0M | ~333k |
| 20% | 8.0M | ~667k |

The 10% row is a useful middle scenario, not a forecast. Apply adoption/capture to it:

| Share of the 10% scenario actually reaching ProjectPermit | Calls/month | Revenue @ $0.25 | Revenue @ $0.50 |
|---:|---:|---:|---:|
| 1% | ~3,333 | ~$833 | ~$1,667 |
| 5% | ~16,667 | ~$4,167 | ~$8,333 |
| 10% | ~33,333 | ~$8,333 | ~$16,667 |

This is why one credible platform integration can matter more than adding dozens of municipalities with no distribution.

### What not to do with these numbers

- Do not call the 40M ServiceTitan jobs ProjectPermit's TAM; most are not permit-sensitive.
- Do not add Procore customers + AppFolio customers + ServiceTitan businesses as if they were unique buyers.
- Do not assume Canadian rules can serve U.S. volume today.
- Do not assume $0.25-$0.50 is accepted pricing until buyers say so.

The purpose of the model is to define the **order of magnitude required from a successful integration** and a concrete test for whether the market can produce 10k-100k monthly calls.

## Competitive reality in 2026

The market is not empty. The product must stay narrow enough that existing full-workflow vendors validate rather than erase the opportunity.

### PermitFlow

PermitFlow now operates a full permitting workflow with AI agents. Its Research Agent identifies requirements, fees and timelines; subsequent agents prepare and submit permit applications. It also positions integrations with construction/trade software. This makes PermitFlow a serious full-workflow competitor, not just a permit runner.

Source: https://www.permitflow.com/

### Symbium

Symbium lets contractors/owner-builders enter an address and project scope, checks jurisdiction-specific compliance using official property data, and in supported jurisdictions can generate approval documents, submit packages, or create/issue permits through municipal systems. It is a direct warning against building another consumer-facing city wizard.

Sources:
- https://help.symbium.com/hc/en-us/articles/47592280623508-How-do-I-use-Symbium-to-check-compliance-and-submit-a-permit
- https://help.symbium.com/hc/en-us/articles/47317399207060-How-does-Symbium-process-my-permit-application

### GreenLite

GreenLite combines AI requirements mapping, expert code-compliance review, submission/AHJ coordination and full permit management. Its labor/expert-heavy service model is intentionally different from ProjectPermit's low-cost deterministic decision layer.

Source: https://greenlite.com/permit-management/

## Defensible wedge

ProjectPermit should not compete on managed submission, permit expediting, plan review, or human AHJ coordination. The wedge is:

1. **Deterministic and evidence-linked** — every rule result should point to official authority/source and preserve uncertainty rather than hallucinating an approval.
2. **Agent/API native** — HTTP, MCP and x402 are the product surfaces, not an end-user permit portal.
3. **Cheap upstream decision** — a platform can ask before quoting/scheduling/designing whether work is likely to trigger permitting and which authority/overlay matters.
4. **Cross-jurisdiction normalization** — one project schema across municipalities rather than one bespoke city questionnaire per workflow.
5. **Low marginal data cost** — prefer municipal/open-government GIS and rules; avoid expensive property datasets until a buyer justifies them.

The product can therefore sit **upstream of PermitFlow/GreenLite/Symbium or a municipal portal**, routing only the cases that need deeper permit work.

## Distribution priority

### P0 — ServiceTitan / field-service ecosystem

Why first:
- 40M+ annual jobs gives a real repeated-workflow denominator.
- HVAC, plumbing, electrical, roofing and replacement/construction jobs frequently create permit decision points.
- ServiceTitan has an explicit App Marketplace/partner path.
- A preflight answer can be requested automatically after job scope classification and before scheduling/quote finalization.

Validation demo workflows:
- HVAC equipment replacement / new installation
- plumbing fixture replacement vs relocation/new plumbing
- electrical/service work once an electrical permit rules module is supported
- roofing/deck/window/structural alteration routing where current municipality scope supports it

### P1 — AppFolio / property-management ecosystem

Why:
- 22,096 property-management customers and 9.4M managed units create a large recurring maintenance/capex surface.
- Stack is explicitly an integration marketplace and already has maintenance and construction-management categories.
- Best workflow: work order or capex project -> normalize scope -> preflight permit/overlay -> route to contractor/approval process.

Do not invent a per-unit permit-event rate until an external property manager provides one.

### P1 — Procore / Autodesk construction ecosystem

Why:
- Procore has 17,850 customers and explicit APIs/App Marketplace.
- Autodesk Construction is used on 2M+ projects.
- Permit preflight fits before project setup, estimating, design lock or submission workflow.

Constraint: enterprise construction integrations are likely slower to close than field-service developer pilots, so do not make them the first proof of demand.

### P2 — open Agent distribution

Keep x402/Bazaar as the low-friction long-tail channel. It is useful for discovery and machine payment, but it should not be assumed to create demand by itself.

Enterprise/platform customers may prefer API keys, invoicing, committed-use tiers or marketplace billing. x402 is a distribution/payment option, not a requirement for every eventual buyer.

## Pricing validation

Keep the current `$0.01` Base Sepolia price strictly as testnet plumbing.

Test these commercial hypotheses with buyers:

- simple jurisdiction-only rule check: **$0.05-$0.10/call**
- address-aware evidence-linked preflight: **$0.20-$0.50/call**
- richer project bundle with all relevant permits/authorities/documents/fees where reliably supported: **$1-$3/project**
- platform volume plan: equivalent unit economics with monthly minimum/commit and support/SLA

Do not optimize price until at least one external integration repeats usage. First prove that the call belongs in the workflow.

## 30-day validation execution

### Week 1 — integration-ready surface

- Freeze municipality expansion at seven jurisdictions.
- Keep `/v1/capabilities` free.
- Publish three copy-paste integration examples: HTTP, standard MCP, paid x402 MCP.
- Clearly mark the standard free MCP as a **temporary developer-validation preview** so it is not mistaken for permanent production pricing.
- Add privacy-minimal usage telemetry: transport, jurisdiction, project family, address-resolution flag, result class and a generated request id; never log raw civic address.
- Tag internal CI/smoke traffic so it can be excluded from external-call counts.

### Week 2 — targeted partner outreach

Target at least **20 developer/partner conversations**, prioritized:

1. ServiceTitan App Marketplace / integration developers
2. property-management integration developers around AppFolio Stack
3. Procore App Marketplace / construction workflow developers
4. permit-automation vendors that could consume ProjectPermit as an upstream router
5. independent AI Agent builders serving contractors/property managers

The ask is not “buy our API.” The ask is: **where in your workflow do you currently decide whether proposed work needs a permit, and would a deterministic evidence-linked API remove manual research?**

### Week 3 — usage test

Offer a limited developer preview and measure:

- external unique integrations
- total external preflight calls
- calls per integration
- repeated calls on different addresses/jurisdictions
- percentage requesting address-aware resolution
- project-family distribution
- how often results are `MUNICIPAL_CONFIRMATION_REQUIRED`
- buyer-requested missing jurisdictions/families

### Week 4 — decision gate

Continue municipality expansion only if at least one of these is true:

- **100+ non-owner external calls** and at least one integration makes 20+ calls;
- **3+ external developers** integrate or actively test;
- one credible platform partner shows a path to **10k+ calls/month**;
- a design partner accepts roughly **$0.20-$0.50 address-aware unit economics** or an equivalent monthly plan;
- a paying/design partner requests specific new municipalities.

If none occurs, do not add another ten cities. Re-evaluate the capability against other MCP/x402 markets with stronger repeated-call density.

## Metrics that matter

Primary:
- external paid/qualified calls per month
- calls per active integration
- repeat rate
- address-aware share
- gross revenue/call and infrastructure/data cost/call
- municipality maintenance hours per 1,000 calls

Secondary:
- number of supported municipalities
- Bazaar listing/discovery impressions
- GitHub stars

A 50-city engine with no repeated integrations is weaker than a 7-city engine producing 10k calls/month.

## Immediate build order

1. Lock seven-city production verification, including Vancouver address-aware first-party GIS. **Done.**
2. Add privacy-minimal external-call telemetry and internal-smoke exclusion.
3. Add integration quickstarts and a developer-preview policy.
4. Start targeted developer/partner validation.
5. Only then decide whether Calgary/Montréal or U.S. jurisdictions deserve implementation.

## Bottom line

The stronger 2026 evidence shifts the opportunity assessment upward from a small municipal-permit lookup API to a potentially useful **high-frequency workflow primitive distributed through vertical SaaS platforms**. The market can plausibly support tens of thousands of monthly calls if one integration inserts the check into recurring contractor/property workflows.

The remaining risk is execution/distribution, not x402 plumbing and not the ability to code another municipality.
