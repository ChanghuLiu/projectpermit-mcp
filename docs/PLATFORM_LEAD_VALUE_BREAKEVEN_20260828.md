# Platform Lead-Value Break-Even — 2026-08-28

## Purpose

ProjectPermit already has a separate vendor build-vs-buy sensitivity in `docs/VENDOR_BUILD_VS_BUY_ECONOMICS_20260828.md`.

That model asks:

> when does a software vendor generate enough calls that maintaining permit logic internally may be cheaper than paying ProjectPermit per call?

This note asks a different question for **marketplaces / lead-routing platforms**:

> how much bad routing, duplicate research, low-quality lead value, or avoidable operational loss must one ProjectPermit preflight prevent for a metered call to pay for itself?

This is a **unit-economics sensitivity only**. It is not E5, observed willingness to pay, measured routing loss, or proof that permit uncertainty causes marketplace waste.

### Currency boundary

The lead values below are Canadian-dollar values. For arithmetic comparability, the hypothetical ProjectPermit prices are treated as **CAD-equivalent call prices** in the sensitivity tables.

If production billing is actually denominated in USD/USDC through x402, the realized bill must first be converted to CAD at the applicable transaction/exchange rate before using these ratios. This note therefore does not claim FX-invariant pricing or a final billing currency.

---

## 1. Public lead-value context

Current/public Quebec renovation lead economics do not support using one universal lead value.

### SoumissionRénovation historical official monetization signal

An older official SoumissionRénovation article states that the platform did not charge a percentage of a contractor's signed job and instead charged a small amount when connecting a contractor with a customer, described as approximately **C$5–C$50 per connection**.

Reproducible official sources:

- `https://soumissionrenovation.ca/fr/blogue/comment-eviter-arnaque-renovation`
- `https://soumissionrenovation.ca/fr/blogue/pourquoi-soumission-renovation-plus-facile`

The current contractor signup surface advertises:

- **100,000 projects submitted/year**;
- **no membership fee**;
- no credit card required at signup.

Source:

- `https://soumissionrenovation.ca/fr/formulaire/formulaire-entrepreneur`

A current public per-connection SoumissionRénovation tariff was **not** found in the latest review.

Therefore:

- C$5–C$50 is useful as a **historical official range**;
- it must not be presented as the platform's current tariff;
- `no membership fee` must not be converted into `free leads`.

### Current independent lead-market signal

A current Canadian home-improvement lead provider, CHISA Home Leads, publicly lists a flexible **C$45/lead** option alongside subscription plans.

Source:

- `https://chisa.ca/forcontractors`

CHISA is not SoumissionRénovation and its GTA-oriented pricing is not a Quebec market average. It is only a current proof that a renovation/home-improvement lead can be sold at a price in the tens of Canadian dollars.

For a deliberately broad sensitivity, this note therefore uses three anchors:

- **C$5** — low-value / low-priced connection anchor grounded in SoumissionRénovation's historical official range;
- **C$25** — deliberately constructed midpoint sensitivity, not an observed tariff;
- **C$50** — upper historical SoumissionRénovation connection anchor and broadly comparable to a current C$45 public lead listing.

The anchors are not TAM inputs and are not ProjectPermit willingness-to-pay evidence.

---

## 2. Basic break-even equation

Let:

- `P` = ProjectPermit CAD-equivalent price per candidate preflight call;
- `L` = economic value / avoidable loss associated with one lead or routing event;
- `r` = minimum fraction of `L` that ProjectPermit must preserve or avoid losing for the call to break even, ignoring integration cost.

Then:

`r = P / L`

### Required value preservation by lead-value band

| Lead / routing value | C$0.10-equivalent call | C$0.25-equivalent call | C$0.50-equivalent call |
|---:|---:|---:|---:|
| C$5 | 2.0% | 5.0% | 10.0% |
| C$25 | 0.4% | 1.0% | 2.0% |
| C$50 | 0.2% | 0.5% | 1.0% |

Interpretation:

- at C$50/lead, a C$0.25-equivalent call appears arithmetically easy to absorb **if** the preflight reliably creates at least 0.5% of lead value;
- at C$5/connection, the same call requires a much more material **5%** value effect;
- a C$0.50-equivalent call is especially demanding in low-value lead channels.

This is why ProjectPermit should not justify pricing by citing a single high lead-price example.

---

## 3. More useful metric: material-hit rate

The previous table assumes every preflight creates a small amount of value. A more realistic marketplace question is often:

> only what fraction of candidate leads does the permit signal materially change?

Let:

- `h` = fraction of called leads where ProjectPermit materially improves routing, avoids meaningful manual research, prevents a bad handoff, or otherwise creates measurable value;
- `V` = minimum value required on each materially improved lead to recover call spend across all calls.

Then:

`V = P / h`

### Required value per materially improved lead

| Material hit rate | C$0.10-eq/call | C$0.25-eq/call | C$0.50-eq/call |
|---:|---:|---:|---:|
| 1% | C$10.00 | C$25.00 | C$50.00 |
| 2% | C$5.00 | C$12.50 | C$25.00 |
| 5% | C$2.00 | C$5.00 | C$10.00 |
| 10% | C$1.00 | C$2.50 | C$5.00 |
| 20% | C$0.50 | C$1.25 | C$2.50 |

This table is strategically more useful than `API price as a percent of lead value`.

Example:

- if only **1%** of candidate leads materially benefit, a C$0.25-equivalent call needs to create/avoid about **C$25 of value on each hit** merely to cover API spend;
- if **10%** materially benefit, the required value per hit falls to **C$2.50**.

Therefore even a cheap call is unattractive if permit applicability almost never changes anything at the insertion point.

This links the economic model directly to the upstream validation requirement:

`candidate volume × unresolved incidence × fact sufficiency × material workflow effect`

not merely `platform lead volume`.

---

## 4. Integration cost must be added, not hand-waved away

Let:

- `I` = integration / security / mapping / ongoing partner-specific cost allocated to the measurement period;
- `N` = candidate calls in the same period.

Then effective cost per call is:

`effective_call_cost = P + I / N`

No integration-cost dollar amount is assumed here.

That omission is deliberate. Public website/API research cannot establish a partner's actual internal integration cost.

Consequences:

- low-volume pilots can look uneconomic even when the raw metered call is cheap because `I/N` is large;
- high-volume platforms amortize integration better, but high volume also strengthens the incentive to internalize logic, as shown in `VENDOR_BUILD_VS_BUY_ECONOMICS_20260828.md`;
- a commercially attractive partner must therefore clear **both** the value-at-risk test and the build-vs-buy test.

---

## 5. Marketplace rescue gate

For a marketplace / lead router, a credible ProjectPermit rescue path now requires evidence for all of the following:

1. **Volume** — enough current-family candidate projects occur at the upstream insertion point.
2. **Uncertainty** — permit applicability is genuinely unresolved there.
3. **Fact sufficiency** — the existing intake contains enough facts for a useful low-friction result.
4. **Material effect** — the result changes routing, avoids meaningful research, improves lead qualification, or prevents another measurable loss often enough to matter.
5. **Economics** — measured/accepted value exceeds API spend plus amortized integration cost.
6. **Build-vs-buy preference** — the platform still prefers buying/partnering rather than reproducing the relevant municipal logic internally.

A public statement such as `100,000 projects/year` clears none of gates 2–6 by itself.

---

## 6. What would count as strong economic evidence

### Still not E5

These remain sensitivity/context only:

- public lead prices;
- public contractor acquisition costs;
- platform subscription prices;
- theoretical savings percentages;
- an operator saying the concept sounds useful;
- a platform saying permit questions happen sometimes.

### E5-like behavior

Strong evidence requires economic commitment, for example:

- accepting a concrete per-call price tied to expected volume;
- accepting a fixed platform licence / paid pilot;
- committing engineering/security/procurement effort for a real integration;
- continuing real external usage after free pilot limits end;
- demonstrating measured routing/research savings and agreeing that the commercial term is below those savings.

The exact pricing model should follow evidence rather than be built in advance.

---

## 7. Pricing implication

The current `$0.20–$0.50/call` idea should remain a hypothesis, not a product promise. If billed in USD/USDC, compare the converted CAD-equivalent cost against partner economics rather than using the nominal number directly.

This sensitivity makes several possibilities plausible **only if E4/E5 appears**:

- cheaper scope-only calls;
- premium pricing only when municipality/property context materially changes safe routing;
- volume tiers;
- fixed platform licence / capped usage;
- hybrid maintained-rule licence for high-volume partners.

Do not implement these pricing variants now.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

The arithmetic shows that a low metered price can fit inside some renovation-lead economics, but it also shows that low-value connections and low material-hit rates can make even nominal `$0.25–$0.50` pricing unattractive.

No current evidence establishes:

- the real value of permit-related routing errors;
- the material-hit rate;
- current SoumissionRénovation per-lead economics;
- partner integration cost;
- price acceptance.

Therefore this model narrows the next experiment; it does not rescue monetization fit.

## Bottom line

The economically meaningful question for a marketplace is not:

> `Is $0.25 cheap compared with a renovation project?`

It is:

> `Across every lead we pay to check, does the permit signal prevent enough real routing/research/lead-quality loss — after FX and integration cost — to beat the metered spend, and do we still prefer buying rather than building?`

Until a real partner answers that with observed workflow behavior or money/resource commitment, willingness-to-pay remains unvalidated.
