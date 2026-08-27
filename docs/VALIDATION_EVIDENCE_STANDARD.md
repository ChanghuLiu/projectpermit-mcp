# ProjectPermit Validation Evidence Standard

Updated: 2026-08-27

## Principle

A reply is not market validation. Positive language such as `interesting`, `useful`, `sounds good`, or `let's talk` is only a lead-qualification signal. Major product, coverage, pricing, or infrastructure decisions must be based on reproducible workflow evidence or observed behavior.

## Evidence levels

### E0 — no evidence

No reply, bounce, auto-reply, support ticket acknowledgement, or generic routing message.

### E1 — opinion only

A real person gives an opinion but no denominator, timeframe, examples, or observed behavior.

Examples:
- "This sounds useful."
- "We have customers who may need this."
- "Permit research is sometimes painful."

E1 is useful for targeting but must not drive a major decision.

### E2 — bounded workflow claim

The partner provides a denominator + timeframe + workflow location, ideally with a recent historical count.

Examples:
- 1,200 maintenance work orders in the last 30 days.
- 85 required a person to determine permit applicability before dispatch.
- The decision occurs at estimate approval and is performed by operations staff.

E2 is stronger than a survey answer but is still self-reported.

### E3 — historical case benchmark

The partner provides 5–20+ anonymized historical scopes or records that can be compared against ProjectPermit.

For every case, record:
- municipality/jurisdiction;
- normalized project family;
- enough scope detail to reproduce the determination;
- historical human/downstream result if available;
- ProjectPermit result;
- agreement/disagreement;
- whether disagreement is material;
- whether address-aware resolution was necessary.

E3 can support engineering prioritization when the cases are representative rather than hand-picked success examples.

### E4 — observed repeat usage

The partner or an external integration actually calls the live service on real workflow cases repeatedly.

Minimum useful thresholds:
- 20+ real calls from one external workflow: repeat-use evidence;
- 100+ aggregate external pilot calls: stronger workflow evidence;
- 500+ candidate calls/month from a specific workflow: commercially relevant small channel;
- 2,000+ candidate calls/month from one credible partner: strong expansion candidate;
- 10,000+ credible monthly path: first meaningful commercial scale checkpoint.

Internal CI, owner smoke tests, demos, and synthetic loads never count as E4.

### E5 — economic behavior

The partner accepts a concrete commercial term or spends real resources to integrate.

Examples:
- accepts $0.25 or $0.50 per address-aware call;
- agrees to a paid pilot;
- signs an integration agreement;
- completes security/procurement work for deployment;
- runs production traffic with a paid or contract-backed path.

E5 is the strongest evidence for pricing and commercialization decisions.

## Decision policy

Do not make the following decisions from E0/E1 alone:
- add a new municipality or country;
- change the product boundary;
- enable mainnet payments;
- invest in a paid marketplace/certification program;
- set final commercial pricing;
- claim TAM/SAM/SOM from partner anecdotes.

Preferred minimum evidence:
- **new jurisdiction engineering**: E3 cases plus a credible E4 call path, preferably 500+ calls/month for that geography;
- **major product-boundary change**: multiple E3/E4 workflows showing the same missing capability;
- **pricing decision**: E5 or repeated explicit price acceptance tied to a quantified volume;
- **commercial scale claim**: observed E4 usage plus platform-scale data, not reply counts.

## Anti-bias rules

1. Always ask for **denominator + timeframe + examples**.
2. Distinguish `estimated candidate calls` from `observed calls`.
3. Do not convert `sometimes`, `often`, or `many` into numbers.
4. Do not count polite replies as positive market validation.
5. Do not count a partner's total customer/job volume as ProjectPermit volume without a measured permit-research share.
6. Prefer random or recent historical samples over hand-picked examples.
7. Record negative evidence. `Permit applicability is always known before our workflow` is a valuable result.
8. Keep unknown values blank/unknown rather than substituting zero.

## Outreach question format

Prefer:

> In the last 30 days, roughly how many jobs/work orders/projects reached this decision point, and how many required someone to determine permit applicability? If possible, can you share 5–20 anonymized historical examples so we can compare our result to the existing process?

Avoid:

> Would this be useful?

## Current validation objective

The next milestone is not a high reply rate. It is at least one reproducible chain:

`real workflow -> bounded recent volume -> anonymized historical cases -> repeat external calls -> economic signal`.
