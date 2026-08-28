# Embedded Permit Build-vs-Buy Scan — 2026-08-28

## Purpose

BuilderAI materially weakened the assumption that contractor software must buy a separate ProjectPermit-style API. Its delivered urbanism capability shows that a vertical estimating SaaS can embed municipal regulatory reasoning directly in its quote workflow.

This scan tests whether BuilderAI is already part of a broader Canadian pattern or remains an isolated exact substitute.

Current conclusion:

> **BuilderAI is the only exact publicly observed pre-quote municipal permit/urbanism embedded case found in this targeted scan. Adjacent Canadian contractor products internalize regional compliance or downstream permit information, but they do not yet establish a second exact `scope + municipality -> permit applicability before quote` substitute.**

This means the build-vs-buy risk is real, but the current evidence does **not** justify treating vertical internalization as an already ubiquitous industry pattern.

## Exact case: BuilderAI

BuilderAI is the current exact embedded substitute because it publicly shows:

- project/plan analysis;
- estimating and quotation;
- municipal `rapport urbanisme` before quote delivery;
- a Laval example concluding no permit is required for the shown interior bathroom renovation;
- municipal urbanism regulation tooling listed as `Livré` on its public roadmap.

Sources:

- `https://www.builder-ai.ca/fr`
- `https://www.builder-ai.ca/demo`
- `https://www.builder-ai.ca/roadmap`

See also `docs/BUILDERAI_QUEBEC_THREAT_ADDENDUM_20260828.md`.

## Adjacent case: Contrax — permit-set interpretation, not permit applicability

Contrax is an Ontario AI-native estimating/contractor platform used for renovations and trades including:

- kitchens;
- bathrooms;
- basements;
- decks;
- additions;
- plumbing/electrical/HVAC;
- general contracting.

Its workflow turns phone walkthroughs and plans into structured estimates.

Contrax also states that when a job arrives with drawings or a permit set, its AI reads the documents, extracts dimensions/scope, and identifies obligations contained in the permit documents.

Examples on the public product page include identifying an item that a permit calls for but that is missing from the contractor's scope.

Sources:

- `https://getcontrax.net/`
- `https://getcontrax.net/contractor-estimating-system`

Important boundary:

> this is **downstream permit-document interpretation**. The permit/drawing set already exists. It is not public evidence that Contrax independently determines whether a permit is required before the permit process starts.

Therefore Contrax must not be counted as a second exact BuilderAI-like competitor.

### Why Contrax is still a high-value falsification target

Contrax already owns:

- structured scope extraction;
- project address/business context;
- AI reasoning inside estimate generation;
- permit-document interpretation;
- the exact renovation families ProjectPermit targets.

That makes it a strong build-vs-buy buyer test.

A 2026-08-28 email to the public founder contact `cameron@getcontrax.net` asked one narrow question:

> If pre-quote municipal permit applicability became a repeated need across Ontario municipalities, would Contrax build that municipal logic/RAG internally or buy an external API that maintains rules, official sources and version history — and why?

No customer data was requested.

A response favoring internal implementation would be direct negative evidence against ProjectPermit's standalone-API differentiation thesis.

A response favoring external maintenance because of cross-municipality source complexity, evidence requirements, reliability or economics would be materially positive build-vs-buy evidence.

## Adjacent case: Chronly — permit storage after quote approval

Chronly is a Canadian contractor workflow product that explicitly shows:

1. create quote;
2. customer approves;
3. create job from approved quote;
4. job holds permit, drawings, photos and notes;
5. schedule/invoice/payment.

Source:

- `https://chronly.ca/use-cases/contractors`

This proves permits are a first-class downstream project artifact in contractor software.

It does **not** show that Chronly determines permit applicability before quote approval.

Therefore Chronly is workflow-adjacency evidence only, not a second embedded permit-intelligence competitor.

## Adjacent case: TradeDesk — Ontario compliance internalized, but not municipal permit applicability

TradeDesk explicitly differentiates itself by building Ontario-specific legal/compliance logic into the product rather than treating it as an add-on.

Its public features include:

- WSIB premium tracking;
- HST handling;
- WSIB clearance certificate alerts;
- Skilled Trades Ontario apprenticeship tracking;
- AI quote generation;
- custom integrations for enterprise customers.

Source:

- `https://www.mytradedesk.ca/`

This is important substitution evidence at the architectural level:

> a vertical SaaS can choose to own local regulatory logic because local compliance is part of its product differentiation.

But the current public scan found no municipal `permit required / not required` decision feature.

So TradeDesk is **build-in-house propensity evidence**, not exact permit-applicability competition.

No outreach was sent because the current public review did not identify a verified public email address; no address was guessed.

## Adjacent case: Markup — trade permit fee/compliance inside quote, not municipal applicability

Markup's Canadian HVAC quoting product shows Ontario-specific trade/compliance context inside quotes, including TSSA contractor licence information and a permit/inspection fee line item in a sample installation quote.

Source:

- `https://getmarkup.ca/for/hvac`

This again demonstrates that vertical contractor software can internalize regulatory/trade context.

It does not establish a municipal building-permit applicability engine for residential renovation scope.

## Current interpretation

The scan supports four distinct categories that must not be conflated:

1. **Exact pre-quote permit/urbanism determination** — BuilderAI is the one current exact public case identified here.
2. **Downstream permit-document interpretation** — Contrax.
3. **Permit/project artifact management after quote approval** — Chronly.
4. **Regional/trade compliance embedded in vertical SaaS** — TradeDesk, Markup.

Only category 1 directly substitutes for ProjectPermit's core output.

Categories 2-4 matter because they show vertical SaaS vendors have the technical and product incentive to internalize adjacent regulatory functions.

## Score implication

This scan does **not** justify another automatic score reduction below the current 53/100.

Why:

- BuilderAI confirms one real exact internalization path;
- no second exact public Canadian pre-quote municipal permit-applicability case was found in this targeted scan;
- LandLogic's third-party API is broad property/zoning intelligence, while the exact narrow permit-applicability API contract remains publicly unverified;
- external buyers have not yet answered whether maintaining municipal permit rules internally is cheaper/preferable to buying a shared service.

Therefore the next score movement should come from **build-vs-buy buyer evidence**, not inference from adjacent features.

## Kill / upgrade conditions

### Strong negative / kill pressure

Downgrade ProjectPermit materially if Contrax, Elper, BuilderAI or another credible software buyer says:

- municipal permit applicability is straightforward enough to build with their existing AI/RAG stack;
- they prefer owning the data/rules/product experience internally;
- external API cost/latency/dependency outweighs maintenance savings;
- deterministic rule IDs/source versioning do not matter to their workflow;
- the pre-quote question is too rare to justify either build or buy.

### Positive differentiation evidence

Upgrade only if software buyers independently say an external capability is preferable because:

- municipality-by-municipality maintenance is expensive or distracting;
- regulatory source changes are hard to track reliably;
- reproducibility/evidence/version history matters;
- they need conservative unresolved-property handling;
- they want the same capability across many cities/products/workflows;
- external per-call economics beat internal maintenance;
- they would allocate integration resources or pay for a real pilot.

## Bottom line

BuilderAI makes `we can put permit guidance in the quote workflow` non-differentiating.

The remaining ProjectPermit question is now narrower and more valuable:

> **Will vertical software vendors buy a shared, maintained, deterministic municipal permit capability instead of building a narrower RAG feature themselves?**

The Contrax outreach is designed to answer exactly that question.
