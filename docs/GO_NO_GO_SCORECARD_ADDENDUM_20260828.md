# Go / No-Go Scorecard Addendum — 2026-08-28

> **Historical transition record.** This file documents the evidence that moved the commercial score from 56 to 53 on 2026-08-28. The current canonical score and decision rules now live in `docs/GO_NO_GO_SCORECARD.md`; do not treat this addendum as a second current scorecard.

This addendum updates the 2026-08-27 commercial scorecard with competitive evidence discovered on 2026-08-28.

It does not change the current decision status:

> **CONTINUE VALIDATION — DO NOT EXPAND PRODUCT SCOPE YET**

## Revised score: 53 / 100

Previous canonical score: **56 / 100**.

| Dimension | Weight | Previous | Revised | Weighted points | Reason for change |
|---|---:|---:|---:|---:|---|
| Pain intensity | 15 | 8/10 | 8/10 | 12.0 | No change. Regulatory research/approval pain remains real. |
| Willingness to pay / monetization fit | 15 | 4/10 | 4/10 | 6.0 | No E5 evidence. |
| Addressable call volume | 15 | 6/10 | 6/10 | 9.0 | No new bounded covered-market upstream denominator. |
| Repeat frequency | 10 | 5/10 | 5/10 | 5.0 | No E4 evidence. |
| Distribution fit | 10 | 6/10 | 6/10 | 6.0 | SoumissionRénovation and Elper improve candidate shape, but neither has validated monthly permit-call volume or integration commitment. |
| **Competitive headroom** | **10** | **4/10** | **2/10** | **2.0** | LandLogic now publicly occupies a broad Ontario platform/API/white-label property-intelligence and permitting-adjacent layer across 80+ municipalities; BuilderAI ships embedded municipal urbanism inside Quebec quote workflows. |
| **Defensibility** | **10** | **3/10** | **2/10** | **2.0** | BuilderAI demonstrates that a vertical SaaS can internalize municipal urbanism/RAG; public municipal rules remain replicable. A moat now requires externally proven deterministic/evidence/maintenance/distribution advantages. |
| Cash-cost fit | 5 | 9/10 | 9/10 | 4.5 | No change. |
| Technical feasibility | 5 | 9/10 | 9/10 | 4.5 | No change; unknown-overlay false-negative path was also corrected on 2026-08-28. |
| Evidence maturity | 5 | 3/10 | 3/10 | 1.5 | No independent representative E3; E4=0; E5=0. |
| **Total** | **100** | **56** |  | **52.5 -> 53** |  |

## 56 -> 54: LandLogic materially closes Ontario platform/API headroom

Current first-party LandLogic evidence shows:

- AI Property Lead Engine across **80+ Ontario municipalities**;
- builders/developers and proptech/platforms as explicit customer categories;
- own-brand embedding;
- machine-ready zoning/planning/property intelligence;
- Data API and Reports API;
- conversational AI integration;
- automatic updates;
- existing integrations such as Teranet/GeoWarehouse;
- LandLogic powering One Ontario's development-approval modernization layer;
- Parcella positioned around property feasibility and permitting.

Sources:

- `https://www.landlogic.ai/ai-property-lead-engine`
- `https://www.landlogic.ai/integration`
- `https://www.landlogic.ai/latest-updates/powering-one-ontario`
- `https://www.landlogic.ai/latest-updates/what-we-learned-from-the-google-for-startups-accelerator`

Important boundary:

> the current public review still does not prove that LandLogic sells the exact narrow ProjectPermit contract `structured residential scope + municipality/address -> deterministic permit applicability + rule/evidence IDs` as a self-serve API.

That remaining difference is no longer enough to justify `competitive headroom = 4/10`.

LandLogic has already demonstrated that standardized cross-municipality regulatory/property intelligence, APIs, white-label distribution and permitting infrastructure can be combined in Ontario.

Therefore competitive headroom falls **4/10 -> 2/10**.

## 54 -> 53: BuilderAI demonstrates vertical internalization in Quebec

BuilderAI creates a different threat from LandLogic.

Its public product and roadmap show:

- Quebec contractor estimating/quote workflow;
- plans/photos -> structured estimate -> quote/client signature;
- municipal `rapport urbanisme` before quote delivery;
- public Laval demo concluding no permit required for the shown existing-bathroom renovation;
- public roadmap marking `Règlements d'urbanisme municipaux (outil Bob)` as **Livré**;
- current public scale signal of only 74 processed estimates, so distribution remains small/unproven.

Sources:

- `https://www.builder-ai.ca/fr`
- `https://www.builder-ai.ca/demo`
- `https://www.builder-ai.ca/roadmap`
- `https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx`

The threat is not scale. It is substitution economics:

> a vertical contractor SaaS can choose to build municipal urbanism/RAG directly into its own quote workflow instead of buying a standalone ProjectPermit API.

That weakens the defensibility of `municipality-specific rules + API wrapper` as a standalone asset.

Defensibility therefore falls **3/10 -> 2/10**.

## Revised differentiation requirement

A buyer saying `permit/urbanism guidance before quote would be useful` is no longer sufficient differentiation evidence.

It proves workflow demand only.

ProjectPermit now needs buyer evidence that an **external shared capability** is preferable to municipal self-service or internal vertical RAG because of one or more of:

1. cross-municipality maintenance burden;
2. deterministic/reproducible rule logic;
3. official evidence and source-version traceability;
4. conservative unknown/property-overlay handling;
5. broader municipality/scope coverage;
6. lower total maintenance cost;
7. reuse across REST/MCP/agent workflows;
8. externally benchmarked accuracy or operational switching cost.

## Why 53 is still above the stop line

The project is not a No-Go yet because:

- municipality-specific rules demonstrably differ;
- deterministic/evidence-linked outputs may still be materially safer or easier to govern than generic RAG;
- Quebec still has no publicly verified LandLogic-equivalent broad third-party API in this review;
- the technical/cash-cost profile remains unusually favorable for a solo developer;
- SoumissionRénovation and Elper create plausible high-leverage buyer tests;
- ProjectPermit's 2026-08-28 unknown-overlay guard improves safety for staged address-light integrations.

But none of these prove a business.

## New stop pressure

The score should move **below 50** without further product expansion if buyer evidence shows any combination of:

- LandLogic already provides the target permit-applicability contract with low-friction procurement;
- Quebec SaaS buyers prefer to build/own narrow municipal RAG internally;
- SoumissionRénovation/Elper report permit applicability is normally resolved before their quote/intake stage;
- no platform exposes >=500 covered current-family candidate events/month with unresolved applicability;
- buyers value municipal deep links/checklists enough that deterministic evidence is not worth paying for;
- E3 requires human expert review on a large share of ordinary cases;
- E5 remains zero after qualified platform/integrator conversations.

## Engineering implication remains unchanged

Do not add an eighth municipality or new scope family because of competitive anxiety.

Allowed work remains:

- correctness and false-negative prevention;
- validation-friction reduction;
- E2/E3/E4/E5 evidence tooling;
- buyer-required integration work;
- corrections to market/competition/economic assumptions.

The next major score movement should come from **external evidence**, not more rules.
