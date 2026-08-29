# ProjectPermit Go / No-Go Scorecard

Updated: 2026-08-28

Decision status:

> **PAUSE / RE-SCOPE — NO FURTHER PRODUCT INVESTMENT; RESCUE / FALSIFICATION ONLY**

This is not a product-quality score. It is a commercial evidence score for whether ProjectPermit deserves more independent-developer time/cash.

## Current score: 49 / 100

Raw weighted score: **48.5 / 100**. The displayed score rounds to 49. The project remains below the formal pause / re-scope boundary and is limited to rescue / falsification work.

| Dimension | Weight | Current rating | Weighted points | Why |
|---|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 12.0 | Permit research/filing is repeatedly described as costly/manual; downstream services charge meaningful money to remove the burden. |
| Willingness to pay / monetization fit | 15 | 4/10 | 6.0 | Filing/permit-ops buyers pay, but ProjectPermit's narrower `$0.20-$0.50` preflight hypothesis has **no E5 evidence**. More importantly, only 2/5 address-adapter jurisdictions currently consume property facts, so the assumed premium `address-aware` unit has a narrower present value base than previously believed. |
| Addressable call volume | 15 | 6/10 | 9.0 | Contractor/platform denominators are material, but Toronto broad MEP flow cannot be mapped safely to the current eight families. Toronto + Mississauga's strongest reproducible current-family-like public issued signal is only ~618-639/month, and even that is not upstream candidate volume. |
| Repeat frequency | 10 | 5/10 | 5.0 | Ordinary contractor building-permit cadence appears modest; aggregated workflow can be larger. **E4 remains 0.** |
| Distribution fit | 10 | 5/10 | 5.0 | Real quote-first workflows exist, but no production integration partner exists. Registry/Bazaar/x402 payment plumbing proves discoverability and settlement capability, not buyer demand; a 2026 population-scale study also cautions that raw x402 settlement counts are heavily concentrated and often internal/fictitious. ProjectPermit itself still has E4=0 despite being discoverable. |
| Competitive headroom | 10 | 0/10 | 0.0 | LandLogic/Parcella now combines a delivered permit/approval product, 80+ Ontario-municipality maintained intelligence, a white-label AI Property Lead Engine for builders and proptech/platforms, configurable APIs with automatic updates, and One Ontario's free first-phase permitting experience. The remaining ProjectPermit differences are contract-shape/auditability/pricing differences, not demonstrated commercial whitespace. PlanEdge separately claims an even closer Canadian requirement engine but remains delivery/API-unverified. |
| Defensibility | 10 | 1/10 | 1.0 | Local/few-city rule ownership is already easy to replicate, and CivCheck/Clariti now independently demonstrates that a commercial platform can maintain and calibrate regulatory/code logic across multiple jurisdictions, achieve useful city-benchmarked accuracy, and distribute through established govtech channels. The remaining defensibility is only the exact upstream deterministic/evidence-versioned/fail-safe machine contract and low-cost developer-native delivery; buyer value for that narrower contract is unproven. |
| Cash-cost fit | 5 | 9/10 | 4.5 | Deterministic rules + first-party/open municipal data; no paid LLM/property-data/human-review dependency required by default. |
| Technical feasibility | 5 | 9/10 | 4.5 | Seven jurisdictions, address adapters, HTTP/MCP/x402, tests and production services already work. |
| Evidence maturity | 5 | 3/10 | 1.5 | No independent representative E3 completed; E4 = 0; E5 = 0. |
| **Total** | **100** |  | **48.5 -> 49 displayed** |  |

## Why the score moved 61 -> 59 -> 58 -> 57 -> 56 -> 53 -> 52 -> 51 -> 50 -> 49

### 61 -> 59: current-family volume correction

Toronto's broad Mechanical + Plumbing + Drain/Site permit flow (~1.7k issued revisions/month) was too broad to count toward the current product. City `WORK` labels show most of that volume as generic building-permit-related work that cannot be mapped safely into the existing eight families.

A deliberately conservative/non-exclusive Toronto current-family-like diagnostic is:

- 2023: **6,695/year = 557.9/month**;
- 2024: **6,690/year = 557.5/month**;
- 2025: **7,038/year = 586.5/month**.

Mississauga adds a cleaner `dwelling_change` signal from `SECOND UNIT` + `ADDITIONAL RESIDENTIAL UNITS`:

- 2023: **721/year = 60.1/month**;
- 2024: **775/year = 64.6/month**;
- 2025: **632/year = 52.7/month**.

Combined Toronto + Mississauga visible current-family-like issued signal is only about **618-639/month**. Vancouver's 888 residential-renovation records/year remain diagnostic only because the City label is merely `Addition / Alteration` and cannot be assigned safely to one current family.

Even the 618-639/month subtotal is not SAM: it is downstream permit-positive activity and does not measure upstream unresolved applicability.

### 59 -> 58: bundled Ontario checker competition

Build Smart Ontario places a free Permit Requirement Checker inside the same planning/estimating/quote funnel as its estimator and contractor lead flow. Its public guidance already covers many practical triggers also modeled by ProjectPermit, including like-for-like openings, deck height, plumbing relocation, structural changes, secondary suites and accessory-structure thresholds.

This reduced **competitive headroom from 5/10 to 4/10**. Generic `permit checker` functionality is already easy to bundle at zero visible marginal price.

### 58 -> 57: municipality-specific rule replication is also cheap

A further 2026 scan found independent Toronto/GTA contractor-side permit checkers such as Craft & Key and Installix. Installix exposes municipality/project-type decisions across 10 GTA municipalities with official links and conditions such as heritage/fire separation.

No public API/developer/white-label interface was found, so these tools do not occupy ProjectPermit's intended embedded B2B layer. But they show that a focused local contractor can reproduce municipality-specific + official-link logic as a free lead-generation feature.

That reduced **defensibility from 4/10 to 3/10**.

### 57 -> 56: current address-aware premium is narrower than assumed

A static audit now distinguishes address-adapter capability from actual rule-engine use of property facts.

ProjectPermit has address adapters for five cities:

- Gatineau
- Ottawa
- Toronto
- Mississauga
- Vancouver

But current deterministic rules consume adapter-relevant property facts in only:

- **Gatineau**: `heritage`, `piia`
- **Ottawa**: `heritage`

Toronto, Mississauga and Vancouver currently consume **no property facts** in permit-applicability decisions.

Therefore:

> **2 / 5 address-adapter jurisdictions = 40% currently have a permit decision path that can depend on adapter-derived property context.**

Laval and Longueuil rules read `piia`, but neither has a current address adapter.

See `docs/ADDRESS_AWARE_VALUE_AUDIT.md`.

This is not external willingness-to-pay evidence, but it removes an unsupported assumption behind the proposed paid unit. It is not defensible to treat every address lookup as premium value when three of five adapter cities currently produce the same permit determination regardless of adapter-derived property metadata.

Accordingly, **willingness-to-pay / monetization fit falls from 5/10 to 4/10**. A future increase requires E5 or representative evidence that municipality/property specificity materially changes enough real workflow decisions to support pricing.

### 56 -> 53: direct platform competition + embedded build-vs-buy threat

Two separate competitive findings materially narrowed the standalone API thesis.

**Ontario platform/API threat:** LandLogic publicly showed an Ontario-wide property/planning/permit intelligence position spanning 80+ municipalities, partner APIs, white-label/embed capability and One Ontario permitting modernization. Parcella directly entered permit/approval questions. At this stage the public delivery model still looked sufficiently engagement-led that one point of narrow headroom remained for a self-serve permit-specific developer contract.

See `docs/LANDLOGIC_THREAT_ADDENDUM_20260828.md`.

**Embedded vertical-software threat:** BuilderAI's municipal urbanism tool is marked delivered and appears directly in a Quebec estimate/quote workflow. ConstructAI Toronto separately claims `permit requirements` plus an AI permit/regulation checker inside tender estimating, although its current evidence is beta/waitlist-level and delivery quality remains unverified.

See:

- `docs/BUILDERAI_QUEBEC_THREAT_ADDENDUM_20260828.md`
- `docs/CONSTRUCTAI_TORONTO_BETA_THREAT_20260828.md`
- `docs/EMBEDDED_BUILD_VS_BUY_SCAN_20260828.md`

A repository build-vs-buy audit then made the negative case more concrete. Across seven jurisdictions ProjectPermit has 155 deterministic rule IDs, but only 28 rule/guidance sources are needed for the scope-only shared ruleset; 14 additional sources are GIS/open-data context. At the single-city level, current Toronto and Mississauga scope-only logic each rests on **one primary rule/guidance source**, despite having 26-27 rule IDs.

See `docs/BUILD_VS_BUY_MAINTENANCE_BASELINE_20260828.md`.

Interpretation:

- a one-city/few-city embedded checker can be cheap enough to internalize;
- `we have deterministic municipal rules` is not a moat;
- ProjectPermit's remaining buy case is cross-city normalization + source drift + evidence/versioning + unknown-state safety + regression reliability + low-friction delivery;
- buyer preference for that external shared capability is still unproven.

Accordingly:

- **competitive headroom falls from 4/10 to 2/10**;
- **defensibility falls from 3/10 to 2/10**;
- total commercial score falls **56 -> 53**.

### 53 -> 52: x402 discovery/payment is not validated long-tail distribution

ProjectPermit already has working paid MCP/x402 plumbing, Registry/Bazaar discovery metadata and repeated external unpaid 402 probes, but **E4 remains 0**.

A July 2026 population-scale arXiv study of x402 activity on Base reported very high settlement counts while also finding extreme concentration and large internal/fictitious components; the authors explicitly caution that raw settlement count cannot be read directly as independent agent adoption.

See `docs/X402_DISTRIBUTION_REALITY_CHECK_20260828.md`.

This matters because build-vs-buy economics make high-volume vertical SaaS buyers more likely to consider internalizing a local checker. A natural fallback thesis would be that Registry/Bazaar/agent marketplaces aggregate lower-volume variable-geography buyers. That remains technically plausible, but there is currently no ProjectPermit E4 evidence and no reliable basis for assuming passive marketplace discovery will create meaningful independent paid volume.

Accordingly **distribution fit falls from 6/10 to 5/10**. x402 remains useful payment infrastructure; it should not be counted as validated distribution.

### 52 -> 51: GoBuild independently embeds near-exact permit intelligence

A targeted Canadian contractor-software scan found GoBuild publicly advertising an `AI permit & zoning intelligence` feature that:

- predicts the permits and drawings a job needs;
- checks current local code;
- provides cited sources;
- is embedded in the same contractor platform as estimates, proposals and job management;
- publicly shows a `Building permit — likely required (City of Toronto)` example;
- is included in the product's all-features subscription rather than presented as a separate metered permit API.

See `docs/EMBEDDED_BUILD_VS_BUY_SCAN_20260828.md`.

This is independent of BuilderAI and materially closer to ProjectPermit's intended output than permit search, permit-document storage or downstream filing tools. GoBuild does not publicly prove comparable accuracy, broad Canadian municipality coverage or a third-party permit API, but it demonstrates that `job/scope -> likely permits + current local code + cited sources` can already be an embedded contractor-software feature.

Accordingly **competitive headroom falls from 2/10 to 1/10**. Remaining whitespace is no longer the feature itself; it is only the narrower shared/self-serve/cross-city external capability contract and whether buyers prefer that over their embedded implementation.

### 51 -> 50: Parcella / One Ontario closes the remaining external cross-city whitespace

A later review of LandLogic's current 2026 product surfaces produced stronger delivery evidence than the earlier API-boundary review.

Parcella is now publicly described as a delivered property-owner product launched in late May 2026, starting with **build feasibility, permits and approvals**. LandLogic's consumer-first permitting materials explicitly frame the problem around owners asking what permits are required before committing to garages, basement apartments, pools, additions, garden suites and similar projects.

More importantly, the current `parcella.ai` route leads to LandLogic's **AI Property Lead Engine**, which is explicitly packaged for third-party embedding:

- builders & developers and proptech/platforms are named target partners;
- partners can embed the assistant under their own brand/workflow;
- property owners enter an address and receive instant answers;
- the maintained foundation covers **80+ Ontario municipalities**;
- LandLogic states there is no maintenance burden on the embedding partner;
- the product can go live in days.

LandLogic separately exposes configurable APIs, Reports API, automatic updates and conversational-AI integration pilots for organizations powering their own products. One Ontario simultaneously presents Parcella as the first phase of a province-wide permitting platform where users can describe projects, discuss requirements and request permits through one conversational experience.

See `docs/ONE_ONTARIO_PARCELLA_DELIVERY_UPDATE_20260828.md`.

This still does **not** prove a public metered endpoint matching ProjectPermit's exact deterministic schema. But the remaining differences are now contract-shape differences—deterministic rule IDs, source/version history, fail-safe unknown states, self-serve MCP/x402 and proposed low per-call pricing—rather than clear commercial whitespace.

None of those narrower differences has E2/E3/E4/E5 buyer validation.

Accordingly:

- **competitive headroom falls from 1/10 to 0/10**;
- weighted score falls **50.5 -> 49.5**;
- displayed score becomes **50/100**;
- decision changes from ordinary validation-only continuation to **pause / re-scope with rescue/falsification work only**.

### 50 -> 49: CivCheck / Clariti productizes cross-jurisdiction regulatory maintenance

A separate 2026 review found a new evidence class that was not included in the LandLogic/Parcella competition deduction.

Toronto launched an official CivCheck-hosted Building Permit Application Pre-Check pilot on August 27, 2026. The current Toronto workflow is downstream of permit-type selection and therefore is **not** an exact substitute for ProjectPermit's upstream `does this scope require a permit?` contract. It nevertheless demonstrates live Canadian municipal deployment of a third-party regulatory/code checking engine.

More importantly, Seattle independently tested CivCheck against real residential permit applications and City-staff review. Seattle reported **87% accuracy for application-completeness checks** and **92% accuracy for design-compliance checks**, with accuracy improving through calibration, and recommended moving to a production pilot.

CivCheck publicly operates as a multi-jurisdiction product, works with city partners to maintain changing regulations, and after its 2025 acquisition by Clariti has access to an established govtech permitting-software distribution channel. Clariti/CivCheck material shows a product model intended to be configured across local governments rather than rebuilt as a one-off single-city checker.

See `docs/CIVCHECK_CLARITI_CROSS_CITY_MAINTENANCE_THREAT_20260828.md`.

This does **not** reduce competitive headroom again: CivCheck's public workflow remains primarily application/document compliance after the applicant already knows the permit path.

It does independently weaken the remaining defensibility rationale. Cross-jurisdiction regulatory maintenance, calibration/accuracy history and embedded govtech distribution can no longer be treated as largely unproductized capabilities.

Accordingly:

- **defensibility falls from 2/10 to 1/10**;
- raw weighted score falls **49.5 -> 48.5**;
- displayed score falls **50 -> 49**;
- decision remains **PAUSE / RE-SCOPE — rescue / falsification only**.

The remaining 1/10 is narrow: ProjectPermit's exact upstream deterministic/evidence-versioned/fail-safe machine contract and very low-cost developer-native delivery are still different in contract shape, but no buyer has validated that difference as commercially valuable.

## Municipality-specific technical value still exists

A separate synthetic discrimination audit should not be confused with this commercial downgrade.

Across 15 identical address-free normalized scopes run through all seven supported jurisdictions:

- broad permit-positive vs permit-negative divergence: **9/15 = 60.0%**;
- strict `REQUIRED` vs `LIKELY_NOT_REQUIRED` divergence: **7/15 = 46.67%**;
- only one case was decisively unanimous across all seven cities.

Several major strict divergences were independently spot-checked against current first-party municipal guidance.

See `docs/MUNICIPAL_RULE_DIFFERENTIATION.md`.

Interpretation:

- municipality-specific rule logic has real **technical** value;
- property/address-specific value is currently much narrower in the implemented rules;
- neither synthetic result proves real workflow incidence, repeated usage or willingness to pay;
- technical non-uniformity does not prove buyers prefer ProjectPermit's external API contract over LandLogic/Parcella, a bundled vertical checker or a narrow internal implementation.

The score therefore does not rise because the synthetic municipal matrix is favorable.

## Why this is a pause / re-scope boundary, not yet an irreversible kill

The project still has assets worth validating before deletion or abandonment:

- the deterministic engine works;
- municipality-specific routing can genuinely diverge;
- operating cash cost is low;
- ProjectPermit's seven-city footprint is not identical to LandLogic/Parcella's currently verified Ontario footprint, but Gatineau URBAIN and Vancouver PRET show that local geographic coverage itself is **not** a moat; the unresolved value is one maintained cross-city machine contract;
- ProjectPermit's exact upstream deterministic evidence/version/safety contract is narrower than the broader public conversational/compliance alternatives;
- no representative software buyer has yet said whether that narrower contract is worth paying for;
- no independent representative E3 benchmark has been completed;
- E4 and E5 remain zero.

See:

- `docs/GATINEAU_URBAIN_FIRST_PARTY_BOUNDARY_20260828.md`
- `docs/VANCOUVER_PRET_FIRST_PARTY_BOUNDARY_20260828.md`

But these facts no longer justify building more product.

At this boundary, the burden of proof reverses:

> **ProjectPermit must now be rescued by external evidence. Engineering cannot be used to manufacture more reasons to continue.**

Only work that could directly produce a kill, hold or rescue decision is allowed.

## Why this is not a Go-to-scale

The critical commercial facts remain missing:

1. How often is `permit required?` unresolved when a Request/assessment/estimate/quote is created?
2. How many of those events map to a current family?
3. Will software buyers pay for a separate deterministic/auditable API instead of using LandLogic/Parcella, PlanEdge, embedded products like GoBuild/BuilderAI, municipal first-party tools, or their own local automation?
4. What exact reliability/auditability/economics/cross-province blocker makes those alternatives insufficient?
5. How often does municipality-specific logic change a generic answer in representative real projects?
6. How often does derived address/property context materially change safe routing?
7. Will anyone pay the proposed price or commit integration resources?
8. Can accuracy stay high without a staffed expert operation?
9. Can variable-geography agent/long-tail channels produce meaningful independent repeated usage rather than merely discovery/probes?

## What could rescue the score above 70

Two or three strong independent signals would be required, not marginal improvements:

- one genuine E2 workflow with **>=500 current-family candidate events/month** in covered geography plus a clear reason LandLogic/Parcella/other alternatives do not fit;
- one representative independent E3 benchmark with no dangerous false `LIKELY_NOT_REQUIRED` pattern;
- representative evidence that municipality-specific logic changes a material share of safe routing decisions;
- representative evidence that derived property/address context changes a material share of decisions;
- one repeated external workflow with **20+ successful preflight calls**;
- three external integrations / 100+ non-owner successful calls;
- one partner showing **>=2,000 current-family candidate events/month** or equivalent proven aggregation;
- one E5 willingness-to-pay/resource commitment at a commercially useful price;
- representative software buyers explicitly preferring ProjectPermit's external deterministic/evidence-linked maintenance over LandLogic/Parcella/internal RAG/municipal first-party alternatives for a concrete cost/reliability/auditability reason;
- repeat paid usage from multiple unrelated agent/API buyers discovered without direct sales.

## What would turn pause / re-scope into No-Go

Serious kill signals include:

- 20 qualified conversations with no bounded repeated upstream applicability workflow;
- current-family upstream candidate volume remains too small when aggregated;
- representative E3 cases show material false-negative risk requiring expert review on most calls;
- permit necessity is usually known before the workflow reaches our insertion point;
- external users treat the tool as one-off research instead of infrastructure;
- free/general bundled or municipal first-party checkers are considered sufficient;
- municipality specificity rarely changes the answer in representative work;
- property/address context rarely changes the answer;
- buyers will not pay for scope-only municipal preflight and the address-aware premium proves too rare;
- multiple representative software buyers say they would simply build/maintain the relevant one-city/few-city checker internally;
- buyers say LandLogic/Parcella/One Ontario or another existing external platform is already good enough;
- PlanEdge independently verifies an externally callable cross-municipality permit-requirement engine at meaningful production scale/economics;
- LandLogic exposes permit-requirement output as an ordinary external machine contract at economics that remove the remaining deterministic-contract wedge;
- CivCheck/Clariti or another multi-jurisdiction platform exposes direct pre-application permit-type/applicability output through an ordinary external machine contract;
- multiple municipal first-party applicability systems become externally queryable/reusable enough that cross-city aggregation is mainly orchestration rather than maintained regulatory knowledge;
- agent/x402 discovery continues to produce only probes/one-off use rather than repeat independent workflows after credible exposure;
- rule maintenance costs several hours/month per low-volume jurisdiction;
- buyers only value full filing/expediting and will not pay for preflight.

## Engineering freeze

Unless external rescue evidence materially changes the decision:

**Do not:** add an eighth municipality; add U.S. coverage; add electrical/HVAC/mechanical families from public volume; build a third FSM adapter; add speculative property/GIS rules; add drawing/document QA; add filing/status/inspection operations; add human reviewer network; pay marketplace/listing fees; build consumer permit/zoning tools; add speculative MCP/x402 features.

**Allowed:** bugs; security/privacy correctness; keeping the existing service operational at negligible cost; benchmark tooling; corrections that prevent overclaim; validation-friction reduction; changes explicitly required by a credible E2+/E3 partner; instrumentation needed to measure real E4/E5 use.

## Current highest-value rescue / falsification experiments

1. **Buyer vs LandLogic/Parcella/municipal-first-party test** — ask software buyers exactly why delivered external/first-party alternatives are insufficient and whether they would pay for deterministic evidence/versioning instead.
2. **Representative CHBA/RMI-style pre-contract incidence** — measure how often `permit required?` is genuinely unresolved before contract rather than merely how long approvals take.
3. **PlanEdge / external-machine-contract verification** — verify whether PlanEdge, LandLogic or another current platform actually exposes the requirement/applicability engine to ordinary third-party software at meaningful multi-municipality scale/economics.
4. **Representative E3 divergence-sensitive cases** — especially basement/window/deck/accessory/plumbing/overlay boundaries.
5. **External E4 / E5** — repeated operational use and actual willingness to pay/resource commitment.

## Bottom line

ProjectPermit is now a **49/100 pause / re-scope project** with a raw weighted score of **48.5**.

The feature/category is real and the technical engine works, but the last clear commercial whitespace has been substantially occupied by delivered external alternatives, municipal first-party tools, and reusable cross-jurisdiction regulatory-automation platforms. The surviving thesis is narrower:

> **some buyers may pay specifically for an upstream deterministic, evidence/version-linked, fail-safe and very low-cost permit-applicability machine contract even when broader maintained cross-city permitting/property intelligence and regulatory-compliance platforms already exist.**

That thesis has no E2/E3/E4/E5 support yet.

The next evidence must come from buyers, representative cases or real usage. **No more speculative product construction.**