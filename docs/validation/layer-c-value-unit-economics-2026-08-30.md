# Layer C value-unit economics gate — 2026-08-30

## Purpose

Resolve a commercial tension exposed by the existing call-volume, commercial-scale and vendor build-vs-buy models:

> Can the current `$0.20/call` model ever produce attractive economics for a deeper maintained regulatory-obligation product, and if not, what exactly must future buyer validation prove before pricing/product scope changes?

This is arithmetic and product-strategy framing only. It is **not** willingness-to-pay evidence, E5, or authorization to change production pricing.

Related existing models:

- `docs/REGULATORY_DEPTH_CALL_VOLUME_MODEL_20260830.md`
- `docs/CALL_VOLUME_THRESHOLDS.md`
- `docs/COMMERCIAL_SCALE_GATE_20260828.md`
- `docs/VENDOR_BUILD_VS_BUY_ECONOMICS_20260828.md`
- `docs/PLATFORM_LEAD_VALUE_BREAKEVEN_20260828.md`

## 1. Current `$0.20` revenue reality

At the current production launch price:

| Paid calls / month | Gross monthly revenue @ $0.20 |
|---:|---:|
| 500 | $100 |
| 1,000 | $200 |
| 2,000 | $400 |
| 5,000 | $1,000 |
| 10,000 | $2,000 |
| 25,000 | $5,000 |
| 50,000 | $10,000 |
| 100,000 | $20,000 |

Therefore:

- `500 calls/month` remains a useful **pilot qualification** threshold, not a business-scale threshold;
- even `10,000 paid calls/month` is only `$2K gross/month`;
- `$5K gross/month` requires **25K paid calls/month**;
- `$10K gross/month` requires **50K paid calls/month**.

This is before hosting, maintenance, partner discounts, payment costs, licensing or support.

## 2. Capture-rate stress test against the Layer-C base model

The existing Layer-C model estimates:

- current seven-city base proxy: **4,466 eligible calls/month**;
- Canada-wide base scenario: **26,750 eligible calls/month**.

Those are modelled eligible workflow calls, not observed paid calls.

### Current seven-city base proxy

| Capture of modelled eligible calls | Paid calls/month | Gross @ $0.20 |
|---:|---:|---:|
| 1% | 45 | ~$9 |
| 5% | 223 | ~$45 |
| 10% | 447 | ~$89 |
| 25% | 1,117 | ~$223 |
| 50% | 2,233 | ~$447 |
| 100% | 4,466 | **~$893** |

Even impossible 100% capture does not reach `$1K/month` at the current price.

This makes one conclusion hard to avoid:

> **`$0.20 + current seven-city Layer-C volume` cannot be an attractive terminal business model.**

The seven cities remain useful for validation, not for proving terminal revenue scale.

### Canada-wide base scenario

| Capture of modelled eligible calls | Paid calls/month | Gross @ $0.20 |
|---:|---:|---:|
| 1% | 268 | ~$54 |
| 5% | 1,338 | ~$268 |
| 10% | 2,675 | ~$535 |
| 25% | 6,688 | ~$1,338 |
| 50% | 13,375 | ~$2,675 |
| 100% | 26,750 | **$5,350** |

At the current price, the Canada-wide base model requires essentially **full theoretical eligible-call capture** to reach about `$5.35K/month` gross.

That is not a credible planning assumption.

## 3. Required effective value per paid workflow

Instead of choosing a higher price because the spreadsheet needs one, calculate what effective revenue per paid workflow would be required to reach an illustrative `$5K/month` gross target.

### Current seven-city base proxy

| Capture | Paid workflows/month | Effective revenue/workflow required for $5K/month |
|---:|---:|---:|
| 10% | 447 | **~$11.20** |
| 25% | 1,117 | **~$4.48** |
| 50% | 2,233 | **~$2.24** |
| 100% | 4,466 | **~$1.12** |

### Canada-wide base scenario

| Capture | Paid workflows/month | Effective revenue/workflow required for $5K/month |
|---:|---:|---:|
| 5% | 1,338 | **~$3.74** |
| 10% | 2,675 | **~$1.87** |
| 25% | 6,688 | **~$0.75** |
| 50% | 13,375 | **~$0.37** |
| 100% | 26,750 | **~$0.19** |

These are not price recommendations. They expose the minimum value density the commercial model would need under different capture assumptions.

## 4. Why `just raise per-call price` is not the answer

The existing vendor build-vs-buy model creates the opposite constraint.

For a technically capable platform, metered spend rises directly with volume. At sufficiently high recurring volume, the buyer can rationally compare ProjectPermit spend with the internal cost of maintaining a narrower checker.

Existing sensitivity examples:

- at `$0.25/call`, a vendor with only `$500/month` of internal maintenance economics reaches cost parity around **2,000 calls/month**;
- at `$0.25/call`, `$1,000/month` internal maintenance reaches parity around **4,000 calls/month**;
- at `$0.50/call`, those thresholds fall to roughly **1,000** and **2,000 calls/month** respectively.

Therefore a pure strategy of moving from `$0.20` to `$1-$2.50` for the same commodity determination would make the high-volume platform build-vs-buy problem materially worse.

The commercial thesis survives only if the external service is buying more than raw rules — for example maintained cross-jurisdiction breadth, evidence/versioning, change monitoring, hard property overlays, conservative unknown-state handling, workflow consequence, support/SLA or other non-core maintenance/risk reduction.

## 5. Value unit should follow workflow consequence

The Layer-C buyer test is already asking whether the result materially changes:

- quote scope;
- price / allowance;
- schedule;
- required professional involvement;
- approval/document handoff;
- inspection/stage sequencing.

If buyers confirm that consequence, the economically meaningful unit is unlikely to be `one lookup`.

Candidate future commercial units to test — **only after E4/E5 evidence** — include:

1. **Regulatory obligation bundle**
   - one project-specific maintained result with evidence/freshness and unresolved-condition handling.
2. **Quote-impact / preconstruction decision bundle**
   - the obligation bundle plus explicit scope/cost/schedule/professional/milestone consequences.
3. **Platform minimum / monthly licence**
   - fixed or committed spend in exchange for bounded usage and maintained multi-jurisdiction coverage.
4. **Hybrid pricing**
   - inexpensive/simple deterministic checks plus premium hard/property-aware/maintained obligation results.
5. **Maintained rule/change subscription**
   - the buyer pays for not having to own source drift/version maintenance rather than paying a high marginal price for every repeated deterministic call.

These are hypotheses, not features to implement now.

## 6. New commercial evidence gate

A future buyer that qualifies Layer C should be able to answer **both** the workflow and commercial questions.

### Workflow gate

1. recent bounded monthly candidate estimates/preconstruction records;
2. fraction needing current local regulatory research;
3. fraction where result materially changes scope/price/schedule/professional involvement/handoff;
4. likely repeated calls per work record/account.

### Commercial-structure gate

If volume grew to roughly 2K / 10K / 50K checks/month:

- would the buyer prefer metered API, fixed platform licence/minimum commitment, or internal maintenance?
- what external-service value makes buying rational instead of building?
- what monthly spend would trigger an internal build decision?
- is the buyer paying for the decision result, for maintained breadth/freshness, for workflow integration, or for a downstream compliance artifact?

A high-volume denominator with `we would build internally once this matters` is **not** a strong commercial lead.

A modest-volume buyer that says a high-consequence obligation bundle avoids expensive repeated research/risk may be commercially more attractive than a high-volume commodity checker.

## 7. Current decision

### Keep production price unchanged

Do **not** change the existing `$0.20/call` launch price now.

Reasons:

- no E5 price acceptance exists;
- the existing product is still primarily permit preflight, not a validated Layer-C obligation bundle;
- changing price now would mix a pricing experiment with the newly launched distribution/conversion experiments;
- PermitBird and other adjacent products show that low-cost commodity API calls exist, so a higher price needs outcome-value evidence.

### Freeze the new commercial hypothesis

For Layer C, stop treating `$0.20/call` as the likely terminal monetization unit.

The new hypothesis is:

> **If deeper regulatory obligations materially change a buyer's quote/scope/schedule workflow, monetize the maintained decision/workflow value rather than simply charging more for the same lookup.**

### Evidence score

No E1/E2/E3/E4/E5 change.

This note is arithmetic derived from existing market-size assumptions and build-vs-buy sensitivity. It does not demonstrate buyer demand, willingness to pay, usage or payment.

## Bottom line

The current numbers expose a structural pricing problem early enough to fix the validation question:

> **Low per-call pricing needs unrealistically large paid volume; high per-call pricing encourages capable high-volume platforms to internalize narrow rule logic.**

Therefore the strongest future ProjectPermit business is unlikely to be a commodity `permit yes/no @ $0.20` API.

The Layer-C thesis only becomes commercially stronger if buyers prove that the maintained obligation result changes a high-value workflow and that they prefer buying the maintained cross-jurisdiction/risk layer rather than owning it internally.
