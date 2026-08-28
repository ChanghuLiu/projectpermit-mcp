# Vendor Build-vs-Buy Economics — 2026-08-28

Purpose: quantify when a multi-account software vendor has a rational economic incentive to **build/maintain permit logic internally** instead of paying ProjectPermit per call.

This is a sensitivity model, not observed willingness-to-pay evidence. It intentionally does **not** convert repository LOC, rule IDs, or source counts into engineering dollars. The only assumed variables are the vendor's own monthly internal maintenance budget and ProjectPermit's hypothetical per-call price.

See also:

- `docs/BUILD_VS_BUY_MAINTENANCE_BASELINE_20260828.md`
- `docs/GO_NO_GO_SCORECARD.md`

## Core equation

Let:

- `P` = ProjectPermit price per call
- `C` = monthly ProjectPermit calls
- `M` = vendor's monthly all-in incremental cost to own/maintain the equivalent internal checker

Then:

`buy_cost = P × C`

The external API becomes more expensive than internal ownership when:

`C > M / P`

This simple threshold is the key commercial constraint for a high-volume software buyer.

## Break-even calls/month by internal maintenance budget

| Vendor internal maintenance budget / month | Break-even @ $0.10/call | Break-even @ $0.25/call | Break-even @ $0.50/call |
|---:|---:|---:|---:|
| C$250 | 2,500 | 1,000 | 500 |
| C$500 | 5,000 | 2,000 | 1,000 |
| C$1,000 | 10,000 | 4,000 | 2,000 |
| C$2,500 | 25,000 | 10,000 | 5,000 |
| C$5,000 | 50,000 | 20,000 | 10,000 |
| C$10,000 | 100,000 | 40,000 | 20,000 |

Interpretation:

- if a focused software vendor can maintain its own relevant cities for **C$500/month**, then at `$0.25/call` ProjectPermit loses pure cost advantage above **2,000 calls/month**;
- even if internal maintenance costs **C$1,000/month**, `$0.25/call` reaches parity at only **4,000 calls/month**;
- at the current strategic scale checkpoint of **10,000 calls/month**, `$0.25/call` costs C$2,500/month and `$0.50/call` costs C$5,000/month.

This does not prove a vendor can actually maintain the logic for those budgets. It shows exactly what must be true for the API to remain cheaper.

## Direct conflict with the 10k-call scale target

ProjectPermit has used **10,000 external successful preflights/month** as a first meaningful distribution checkpoint.

At that volume:

| Price | API spend/month | API spend/year |
|---:|---:|---:|
| $0.10 | C$1,000 | C$12,000 |
| $0.25 | C$2,500 | C$30,000 |
| $0.50 | C$5,000 | C$60,000 |

For a technically capable vendor serving only one/few municipalities, that annual spend can be large enough to fund meaningful internal maintenance.

Therefore the 10k-call target creates a paradox:

> the exact software buyer capable of generating attractive call volume may also be the buyer with the strongest economic incentive to internalize a narrow local checker.

The external API thesis only survives if ProjectPermit saves the buyer more than the raw rule implementation cost through one or more of:

- broad cross-municipality/cross-province coverage;
- source-change monitoring;
- official evidence/versioning;
- conservative unknown-state safety;
- property/overlay handling that materially changes decisions;
- externally benchmarked accuracy and false-negative controls;
- lower integration/maintenance risk than internal ownership;
- contractual/SLA value;
- enough geography breadth that internal maintenance cost rises faster than API spend.

All of those still require buyer evidence.

## BuilderAI SaaS margin stress test

BuilderAI is a useful public Quebec vertical-SaaS example because it bundles an urbanism report into the quote workflow and publishes transparent pricing.

Current public pricing reviewed 2026-08-28:

- Solo: **C$59/month** or **C$47/month annual billing equivalent**;
- Solo includes **20 estimates/month**;
- Pro: C$119/month, unlimited estimates;
- Team: C$229/month, unlimited estimates;
- the quote workflow explicitly includes an urbanism report.

Source: `https://www.builder-ai.ca/`

If every Solo estimate generated one ProjectPermit call and the customer used all 20 included estimates:

| ProjectPermit price | Cost per Solo account/month | % of C$59 monthly subscription | % of C$47 annual-plan monthly equivalent |
|---:|---:|---:|---:|
| $0.10 | C$2 | 3.39% | 4.26% |
| $0.25 | C$5 | 8.47% | 10.64% |
| $0.50 | C$10 | 16.95% | 21.28% |

This is before BuilderAI pays for its own AI inference, hosting, material-price lookups, support, payment fees, and other product costs.

Therefore `$0.50/call` looks especially difficult for a low-ARPU vertical SaaS if permit checks are frequent. `$0.25/call` is not impossible, but ~8.5-10.6% of subscription revenue for one embedded sub-feature is already material at maximum Solo usage.

This is a **margin sensitivity**, not proof that BuilderAI would buy ProjectPermit or that all 20 estimates require a permit check.

## Multi-account scaling example

For a vendor whose customers each generate 20 permit-preflight calls/month:

| Customer accounts | Calls/month | Cost @ $0.10 | Cost @ $0.25 | Cost @ $0.50 |
|---:|---:|---:|---:|---:|
| 100 | 2,000 | C$200 | C$500 | C$1,000 |
| 500 | 10,000 | C$1,000 | C$2,500 | C$5,000 |
| 1,000 | 20,000 | C$2,000 | C$5,000 | C$10,000 |
| 5,000 | 100,000 | C$10,000 | C$25,000 | C$50,000 |

Again, this is arithmetic only. Real permit-sensitive share may be far below 100%.

But it exposes the structural problem: **large distribution partners create both the best volume and the strongest build incentive**.

## Customer-segment implication

### Weakest target: one/few-city vertical SaaS with engineering staff

Why:

- narrow local rule set may be cheap to internalize;
- high call volume quickly makes per-call API spend visible;
- BuilderAI and other observed products already demonstrate internal permit/urbanism features.

ProjectPermit should not assume this buyer is attractive merely because integration volume is high.

### Better target: software serving many municipalities but lacking regulatory engineering appetite

Potential buy case:

- many municipalities/provinces;
- permit logic is non-core but repeatedly required;
- buyer wants one stable contract;
- rule/source drift is operationally painful;
- enough revenue per workflow to absorb API cost.

This buyer profile is still hypothetical until external conversations confirm it.

### Possible target: agent/API consumers with variable geography and no persistent local rule team

An agent marketplace, property workflow, or long-tail integration may prefer metered external calls because it cannot predict geography or justify building local rules.

This is closer to the original x402 capability thesis, but current E4 is zero and no paid demand exists.

## Pricing implication

The current `$0.20-$0.50/call` hypothesis should not be treated as one universal price.

The economics suggest a likely need for one of these if E5 ever appears:

1. **volume tiers** where effective per-call price falls materially for high-volume software partners;
2. **monthly platform licensing / capped usage** to remove runaway variable-cost anxiety;
3. **premium only for address/property-aware or hard municipal cases**, with cheaper scope-only calls;
4. **hybrid cache/license model** for high-volume deterministic calls while ProjectPermit charges for maintained rule/version updates.

Do not build billing complexity now. These are only pricing hypotheses to test after E4/E5.

## New buyer falsification question

For any software/platform respondent, ask the economic version directly:

> If this workflow reached 2k / 10k / 50k checks per month, would you prefer a metered external API, a fixed platform license, or maintaining the relevant municipal rules internally? What makes that choice rational for you?

A repeated answer of `we would build it internally once volume is material` is strong negative evidence against per-call B2B SaaS distribution.

A repeated answer of `we would still buy because cross-city maintenance/risk is non-core` supports the shared-capability thesis, but still needs E5 pricing evidence.

## Decision consequence

**No automatic score change yet. Current score remains 53/100.**

This sensitivity does not tell us the vendor's actual internal maintenance cost or preference. It does, however, make the next evidence requirement much stricter:

> a high-volume partner is not commercially attractive unless it also demonstrates a reason **not to internalize** the capability at the resulting API spend.

Therefore future E2 volume claims should be paired with a build-vs-buy answer before they are interpreted as a credible 10k-call commercial path.