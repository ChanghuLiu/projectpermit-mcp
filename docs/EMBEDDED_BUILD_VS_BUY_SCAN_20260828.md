# Embedded Permit Build-vs-Buy Scan — 2026-08-28

## Purpose

BuilderAI materially weakened the assumption that contractor software must buy a separate ProjectPermit-style API. Its delivered urbanism capability shows that a vertical estimating SaaS can embed municipal regulatory reasoning directly in its quote workflow.

A later targeted scan found **GoBuild** as a second, even closer publicly documented embedded case. The conclusion is therefore stronger than the original scan:

> **At least two independent Canadian contractor-software products now publicly embed pre-quote / in-job permit intelligence rather than exposing permit logic as a separate purchased ProjectPermit-style API dependency.**

This does not prove those products maintain every rule internally, and it does not establish their accuracy or adoption. It does prove that `permit applicability/intelligence inside the contractor OS` is no longer an isolated product pattern.

## Exact case 1: BuilderAI

BuilderAI is an exact embedded substitute because it publicly shows:

- project/plan analysis;
- estimating and quotation;
- municipal `rapport urbanisme` before quote delivery;
- a Laval example concluding no permit is required for the shown interior bathroom renovation;
- municipal urbanism regulation tooling listed as delivered on its public roadmap.

Sources:

- `https://www.builder-ai.ca/fr`
- `https://www.builder-ai.ca/demo`
- `https://www.builder-ai.ca/roadmap`

The Laval bathroom demo was independently checked against current City of Laval guidance and the shown `no permit` conclusion is consistent with Laval's published rule for renovation of an existing bathroom when the relevant trigger conditions are absent. This is a concrete example where the embedded vertical product is not merely displaying generic Ontario/Quebec text.

See also `docs/BUILDERAI_QUEBEC_THREAT_ADDENDUM_20260828.md`.

## Exact case 2: GoBuild — permit prediction + cited current local code inside contractor OS

GoBuild is a broader construction-management product for GCs, home builders, remodelers and specialty trades. Its public product pages explicitly advertise:

- inline estimates and proposals;
- an `AI permit & zoning intelligence` feature;
- prediction of **the permits and drawings a job needs**;
- zoning checking against **current local code**;
- **cited sources**;
- an inspections tracker;
- job-command-center permit status embedded with the rest of project operations.

A public command-center example shows:

`Building permit — likely required (City of Toronto)`

Sources:

- `https://www.gobuild.ca/features`
- `https://www.gobuild.ca/`
- `https://www.gobuild.ca/pricing`

GoBuild's pricing page says every feature is included in one plan and specifically lists `Permits & compliance tracker`; the permit/zoning intelligence is not presented as a separately metered external API purchase by the contractor.

Important limits:

- GoBuild does not publicly disclose the internal data/provider architecture behind the permit feature;
- no representative accuracy benchmark was found;
- no public customer/adoption denominator for the permit feature was found;
- no public third-party permit-intelligence API/white-label contract was found in the current scan.

Even with those limits, GoBuild is materially closer to ProjectPermit's intended output than a permit-document repository or simple search tool because it explicitly predicts required permits using local code and cited sources inside the contractor workflow.

## Adjacent case: Jobtract — multi-city permit search/compliance inside quote software

Jobtract is a Canadian AI-first field-service / contractor platform. Its current public product advertises:

- AI quoting;
- `Permits Search` with AI-assisted permit search and form filling;
- `Permit search · 30+ cities`;
- a four-agent quote society in which intake, materials, pricing and **compliance** specialists build a quote before QA;
- a public MCP server exposing its own business tool catalog.

Source:

- `https://jobtract.ca/`

The current public text does **not** clearly prove that Jobtract produces a deterministic `required / not required` municipal building-permit decision before quote, so it is not counted as a third exact ProjectPermit substitute.

It is nevertheless strong architectural evidence that Canadian contractor software vendors are willing to internalize multi-city permit-related functionality rather than leave it entirely to a separate permit system.

A build-vs-buy question was sent to Jobtract's verified public support address on 2026-08-28 asking whether its permit layer is maintained internally or relies on an external provider, and whether material-volume economics would favor metered API, fixed license, or in-house logic. Until a human reply arrives, this is E0 outreach only.

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

Therefore Contrax must not be counted as an exact BuilderAI/GoBuild-like competitor.

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

Therefore Chronly is workflow-adjacency evidence only, not an embedded permit-intelligence competitor.

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

## Adjacent case: Markup — trade permit fee/compliance inside quote, not municipal applicability

Markup's Canadian HVAC quoting product shows Ontario-specific trade/compliance context inside quotes, including TSSA contractor licence information and a permit/inspection fee line item in a sample installation quote.

Source:

- `https://getmarkup.ca/for/hvac`

This again demonstrates that vertical contractor software can internalize regulatory/trade context.

It does not establish a municipal building-permit applicability engine for residential renovation scope.

## Revised interpretation

The scan now supports five distinct categories:

1. **Exact/near-exact embedded permit determination/intelligence** — BuilderAI and GoBuild.
2. **Multi-city permit search/compliance internalized in contractor software** — Jobtract.
3. **Downstream permit-document interpretation** — Contrax.
4. **Permit/project artifact management after quote approval** — Chronly.
5. **Regional/trade compliance embedded in vertical SaaS** — TradeDesk, Markup.

Category 1 directly pressures ProjectPermit's core output.

Categories 2-5 matter because they show multiple independent vendors have the technical/product incentive to internalize regulatory functions rather than default to an external specialized API.

## Score implication

The original scan did not justify a score reduction because BuilderAI was the only exact public case.

GoBuild changes that conclusion. It independently demonstrates the same broad product pattern in another contractor OS and adds two details especially close to ProjectPermit:

- permit-needs prediction from job context;
- cited current-local-code sources.

Therefore **competitive headroom should fall from 2/10 to 1/10**.

This is not a claim that GoBuild's output is more accurate, has broad Canadian municipal coverage, or is available as an external API. It is a recognition that the remaining whitespace for a standalone embedded permit capability is now extremely narrow.

No additional defensibility reduction is applied from this evidence alone because defensibility is already 2/10 and buyer preference/build-vs-buy economics still require external confirmation.

## Kill / upgrade conditions

### Strong negative / kill pressure

Downgrade ProjectPermit materially if Contrax, Jobtract, Elper, BuilderAI or another credible software buyer says:

- municipal permit applicability is straightforward enough to build with their existing AI/RAG stack;
- they prefer owning the data/rules/product experience internally;
- external API cost/latency/dependency outweighs maintenance savings;
- deterministic rule IDs/source versioning do not matter to their workflow;
- the pre-quote question is too rare to justify either build or buy.

Also downgrade if GoBuild, LandLogic or another competitor exposes a low-friction third-party permit-specific API with comparable workflow coverage/economics.

### Positive differentiation evidence

Upgrade only if software buyers independently say an external capability is preferable because:

- municipality-by-municipality maintenance is expensive or distracting;
- regulatory source changes are hard to track reliably;
- reproducibility/evidence/version history matters;
- they need conservative unresolved-property handling;
- they want the same capability across many cities/products/workflows;
- external economics beat internal maintenance;
- they would allocate integration resources or pay for a real pilot.

## Bottom line

BuilderAI and GoBuild make `we can put municipality-aware permit intelligence with sources into the contractor workflow` non-differentiating.

The remaining ProjectPermit question is now extremely narrow:

> **Will software/agent buyers pay for a shared, self-serve, maintained, deterministic cross-city permit capability instead of using their own embedded AI/RAG, an assisted platform such as LandLogic, or bundled permit intelligence already inside their operating software?**

Only external build-vs-buy + E3/E4/E5 evidence can rescue that thesis.