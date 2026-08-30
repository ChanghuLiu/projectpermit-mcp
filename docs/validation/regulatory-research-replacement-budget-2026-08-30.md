# Regulatory research replacement-budget stress test — 2026-08-30

## Purpose

Translate a future buyer's bounded regulatory-check frequency into an internal labour-cost floor without inventing a ProjectPermit price.

The key question is:

> If a contractor currently uses an estimator/project coordinator to research municipality-specific permit/regulatory requirements before pricing, what labour budget is being consumed today?

This is a **sensitivity model**, not an observed time study, willingness-to-pay result or pricing recommendation.

## 1. Current wage anchors

Government of Canada Job Bank currently reports Ontario median wages approximately:

- Construction estimator: **$38.46/hour**;
- Construction project coordinator: **$50.61/hour**;
- Toronto construction project coordinator: **$51.28/hour**.

Sources:

- https://www.on.jobbank.gc.ca/marketreport/wages-occupation/3260/ON
- https://www.nt.jobbank.gc.ca/marketreport/wages-occupation/24320/ON
- https://www.jobbank.gc.ca/marketreport/wages-occupation/24320/22437

These wage figures already omit employer overhead and most opportunity-cost effects. Therefore they are useful as a conservative labour-cost floor.

Do not add an invented overhead multiplier until a buyer's actual staffing economics are known.

## 2. Cost per check sensitivity

No reliable representative time-per-check dataset has been established yet.

Therefore use explicit time scenarios rather than claiming a typical duration.

### Wage-only labour cost per check

| Research time / check | Ontario estimator @ $38.46/h | Ontario project coordinator @ $50.61/h |
|---:|---:|---:|
| 10 min | $6.41 | $8.44 |
| 15 min | $9.62 | $12.65 |
| 30 min | $19.23 | $25.31 |
| 45 min | $28.85 | $37.96 |
| 60 min | $38.46 | $50.61 |

Interpretation:

Even a short 15-minute check has a wage-only cost around `$10–$13` if performed by typical estimator/coordinator staff.

That does **not** mean ProjectPermit can charge `$10/check`. A buyer may not save all of that time, the check may be bundled into another task, and some checks are already handled from staff memory.

## 3. Monthly replacement-budget sensitivity

### Using estimator median wage

| Checks/month | 15 min each | 30 min each | 60 min each |
|---:|---:|---:|---:|
| 5 | $48 | $96 | $192 |
| 20 | $192 | $385 | $769 |
| 50 | $481 | $962 | $1,923 |
| 100 | $962 | $1,923 | $3,846 |
| 300 | $2,885 | $5,769 | $11,538 |

### Using project-coordinator median wage

| Checks/month | 15 min each | 30 min each | 60 min each |
|---:|---:|---:|---:|
| 5 | $63 | $127 | $253 |
| 20 | $253 | $506 | $1,012 |
| 50 | $633 | $1,265 | $2,531 |
| 100 | $1,265 | $2,531 | $5,061 |
| 300 | $3,796 | $7,592 | $15,183 |

All values are wage-only sensitivity calculations.

## 4. Why frequency dominates the commercial answer

### Low-frequency contractor

If a contractor needs only 5 checks/month and each check consumes 15 minutes of staff time, wage-only burden is roughly `$48–$63/month`.

A large subscription would be difficult to justify from research-time savings alone.

The product would need another value source:

- avoiding a high-cost mistake;
- professional-risk reduction;
- client trust/quote quality;
- faster close rate;
- downstream execution/referral value.

Those require evidence.

### Medium-frequency remodeler / estimator team

At 20–50 checks/month and 15–30 minutes/check, wage-only burden is already roughly `$192–$1,265/month` depending on role/time assumption.

This is the first region where a normal B2B monthly subscription/minimum can plausibly fit inside the buyer's existing labour budget without requiring heroic avoided-loss claims.

### High-frequency multi-jurisdiction operator

At 100–300 checks/month, even the conservative 15-minute scenario consumes roughly `$962–$3,796/month` of estimator/coordinator wage time.

This is where maintained jurisdiction coverage/freshness could support material recurring economics.

But this is also where **build-vs-buy pressure becomes strongest**. A high-frequency platform/operator will compare external spend with internal rule/data maintenance.

Therefore high frequency alone is insufficient; ProjectPermit must remove a maintenance burden the buyer does not want to own.

## 5. Savings fraction matters

ProjectPermit will almost certainly not eliminate 100% of regulatory research time.

A result may still require:

- confirming missing site facts;
- engineer/designer judgment;
- unusual municipal clarification;
- permit filing;
- client communication.

Therefore a future economic model should apply a **verified saved-time fraction** from pilot observation.

Example only:

If the baseline task is 30 minutes and ProjectPermit reduces it to 10 minutes, the saved fraction is 20/30 = **67%**.

At 50 checks/month using the Ontario estimator wage:

- baseline labour ≈ `$962/month`;
- 67% saved ≈ `$645/month` wage value.

This is still not the product price. It is the maximum direct labour-value pool before buyer surplus, integration/support costs and errors are considered.

## 6. The buyer question should now capture time, not only frequency

Preferred bounded sequence:

1. **Last 20 estimates:** how many required municipality-specific permit/code/professional/document/inspection research before pricing?
2. Of those, how many changed quote/scope/schedule/professional involvement/handoff?
3. **Who does the research today?** Owner, estimator, coordinator, designer/engineer, permit consultant?
4. For a normal one, roughly how much staff time is spent before you have enough confidence to price: `<10 min`, `10–30`, `30–60`, `1–2h`, `>2h`?
5. If the maintained result with official source were available inside the estimate/job, what portion of that step would disappear?
6. Would you prefer a fixed monthly add-on, platform licence, or internal maintenance at your volume?

These answers can populate a buyer-specific replacement budget without guessing.

## 7. Price-testing consequence

Do not choose `$29/$99/$299` merely because those are familiar SaaS tiers.

After E2, derive candidate price from three measured inputs:

`replacement value ≈ checks/month × minutes saved/check × buyer labour cost/minute`

Then apply commercial constraints:

- buyer must retain meaningful surplus;
- error/risk profile may increase or decrease value;
- high volume increases build-vs-buy pressure;
- licensed data/content costs may create a minimum viable contract size;
- x402 per-call and account subscription can coexist.

## 8. Current decision

The stress test reinforces the current build gate:

> **Frequency is now the highest-leverage missing variable.**

Public evidence already demonstrates that regulatory requirements can materially change cost/scope/schedule and that some contractors perform permit work repeatedly. But without one real buyer's bounded check count + time burden, choosing product scope or pricing remains premature.

No E-level increase.
