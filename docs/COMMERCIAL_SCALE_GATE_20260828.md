# Commercial Scale Gate — 2026-08-28

## Why this gate exists

ProjectPermit's existing `>=500 candidate calls/month` gate is useful for deciding whether a workflow is worth piloting.

It is **not** enough to establish an attractive standalone API business.

The current working E5 price hypothesis is approximately **$0.20-$0.50 per paid/address-aware preflight**. At that price, a successful pilot can still be commercially too small.

## Gross revenue sensitivity

| Paid calls/month | $0.20/call | $0.25/call | $0.50/call |
|---:|---:|---:|---:|
| 500 | $100 | $125 | $250 |
| 2,000 | $400 | $500 | $1,000 |
| 10,000 | $2,000 | $2,500 | $5,000 |
| 20,000 | $4,000 | $5,000 | $10,000 |
| 40,000 | $8,000 | $10,000 | $20,000 |
| 50,000 | $10,000 | $12,500 | $25,000 |
| 100,000 | $20,000 | $25,000 | $50,000 |

These are gross-revenue sensitivities, not forecasts or profit estimates.

## Paid-share problem

External successful preflights are not automatically paid calls.

If only 50% of a workflow becomes paid/address-aware usage, total external calls required are twice the paid-call figures above.

For example:

- $5k gross/month at $0.25 requires **20k paid calls/month**, or ~40k total calls at a 50% paid share;
- $10k gross/month at $0.25 requires **40k paid calls/month**, or ~80k total calls at a 50% paid share;
- $10k gross/month at $0.50 requires **20k paid calls/month**, or ~40k total calls at a 50% paid share.

Therefore `10k external calls/month` remains a strong distribution proof point but may be only a modest revenue business.

## Revised interpretation of workflow gates

### 500+ candidate calls/month

Purpose: **pilot qualification**.

A workflow at this level can justify E3/E4 integration learning if permit applicability is genuinely unresolved often enough.

It does not establish standalone commercial scale.

### 2,000+ candidate calls/month

Purpose: **meaningful partner leverage**.

One such partner reduces the number of integrations required, but even 2,000 paid calls at the full $0.50 hypothesis is only $1,000 gross/month.

It still needs either multiple partners, much higher realized price, or a bundled commercial model.

### 10,000+ external calls/month

Purpose: **repeated distribution proof**.

This demonstrates that ProjectPermit can occupy a real workflow. It does not by itself prove attractive MRR because paid share and realized price remain unknown.

### 20,000-50,000+ paid calls/month

Purpose: **credible standalone API economics at the current price hypothesis**.

This is the scale band where `$0.20-$0.50/call` begins producing roughly `$4k-$25k gross/month`.

The exact attractiveness threshold is a business choice; the important point is that it is materially above the 500-call pilot gate.

## What E2 outreach should now learn

When a platform gives a useful bounded denominator, record enough information to estimate the next scale step rather than stopping at `>=500`:

1. recent monthly candidate events in covered geographies/families;
2. unresolved permit-applicability share;
3. likely number of ProjectPermit calls per candidate event;
4. address-aware / evidence-linked share;
5. whether the platform could deploy across more accounts/geographies without a separate integration each time;
6. realistic paid-call share;
7. whether per-call pricing or bundled platform pricing is preferred.

Do not ask every target for all seven questions in the first email. Use them after a target qualifies.

## Pricing implication

Do **not** lock ProjectPermit into `$0.20-$0.50/call` before E5.

If a buyer has only 500-2,000 relevant calls/month but the preflight changes a high-value quote/workflow, a platform subscription, minimum monthly commitment or bundled pricing may be more rational than pure usage pricing.

Conversely, do not raise the assumed price in the model simply to make the economics look better. A higher price requires actual buyer behavior.

## Go / No-Go implication

**No score change.**

This is arithmetic clarification, not new external evidence.

However, future `Go` evidence must increasingly explain **both**:

- a real unresolved workflow exists; and
- there is a credible path from pilot-scale use to economically meaningful paid volume or pricing.

A 500+/month pilot with no credible aggregation, pricing or expansion path is useful E4 learning but weak evidence for a standalone business.

Current ProjectPermit status remains:

> **50/100 — validation/falsification only; no product expansion.**