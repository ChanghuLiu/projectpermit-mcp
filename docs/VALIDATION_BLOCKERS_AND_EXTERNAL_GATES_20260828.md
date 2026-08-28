# Validation Blockers and External Gates — 2026-08-28

## Current decision state

ProjectPermit is at **50/100**.

> **VALIDATION / FALSIFICATION ONLY — NO PRODUCT EXPANSION.**

This document separates questions that can still be answered autonomously from questions that now require real external evidence.

The purpose is to stop low-value research loops and prevent public-web proxies from being mistaken for buyer validation.

## Questions already answerable without a partner

### 1. Do municipal rules differ enough that one generic Ontario/Canada checklist is imperfect?

**Yes.**

Examples already documented include Toronto vs Mississauga basement finishing and municipality-specific accessory-structure thresholds/exceptions.

This proves rule heterogeneity, not willingness to pay.

### 2. Can stale first-party sources create conflicting answers?

**Yes.**

Mississauga currently exposes a newer web page and an older official PDF with materially different basement/accessory-structure guidance.

This proves a source-freshness failure mode, not buyer demand.

### 3. Can ProjectPermit represent current rules deterministically with evidence/version metadata?

**Yes, technically.**

The current Mississauga rules cite the current City page; rule IDs, source metadata, conservative unknown handling and regression infrastructure exist.

### 4. Is a local one-city checker prohibitively difficult for a vertical SaaS to build itself?

**No.**

The current maintenance audit shows Toronto and Mississauga scope-only logic can each rely on one primary rule/guidance source. Narrow local internalization is plausible and already observed in adjacent products.

### 5. Does a Canadian pre-application feasibility competitor exist?

**Yes.**

PermitSnapshot independently converges on address + scope + pre-quote permit feasibility across Ontario.

Its public product does not yet prove the exact high-frequency deterministic API contract, but conceptual headroom is gone.

### 6. Are issued-permit-history APIs already a commodity/adjacent market?

**Yes.**

Multiple Canadian vendors already normalize historical/issued permit data. ProjectPermit should not position generic permit-record normalization as differentiation.

### 7. Is 500 calls/month enough to establish a meaningful standalone business?

**No.**

It is a pilot qualification threshold. At the current price hypothesis, standalone economics require a credible path to materially larger paid volume or higher/bundled pricing.

## Questions that public research can no longer answer reliably

### A. Is permit applicability unresolved often enough in real upstream quote/intake workflows?

Required evidence: **E2**.

Need a bounded recent denominator from a real platform/operator, including workflow point and unresolved share.

Public cumulative jobs, contractor counts, permit issuance and marketplace reviews cannot substitute.

### B. Do buyers prefer buying a shared deterministic capability over maintaining local guidance/RAG themselves?

Required evidence: informed **build-vs-buy buyer/operator response**, ideally followed by E3/E4 behavior.

Public feature pages show what products can build, not what another buyer will purchase.

### C. Does municipality-specific deterministic logic materially outperform simplified guidance on representative real cases?

Required evidence: **E3**.

Need chronological/random or otherwise defensibly representative historical scopes plus actual permit outcome/confirmation.

Search-selected anecdotes and permit-positive municipal records cannot substitute.

### D. Can ProjectPermit occupy a repeated real workflow with low enough clarification friction?

Required evidence: **E4**.

Need 20+ real external successful calls from one repeated workflow while measuring:

- zero-question decisions;
- 1-3 clarification decisions;
- unresolved/escalated cases;
- whether result changes next action.

### E. Will anyone pay the hypothesized price or commit resources?

Required evidence: **E5**.

Need actual payment, paid pilot, minimum commitment, contract/resource commitment or similarly costly behavior.

Competitor list prices are not ProjectPermit E5.

### F. Can the business reach meaningful standalone scale?

Requires combined **E2 + E4 + E5**:

- candidate workflow volume;
- paid/address-aware share;
- repeat-call multiplier;
- platform aggregation path;
- realized price/commercial structure.

No public TAM multiplication can resolve these variables safely.

## Current external gates in priority order

### Gate 1 — build-vs-buy falsification

Highest-value pending targets:

- PermitSnapshot;
- BuilderAI;
- QuoteXbert;
- RealCraft.

A clear informed answer that internal/simple AI maintenance is good enough and an external deterministic layer adds little value is materially negative at the current score.

### Gate 2 — upstream E2 denominator

Highest-value pending targets:

- HomeStars;
- RenoAssistance;
- GoQuotes;
- JobDeck;
- CHBA/RenoMark if it can provide bounded industry workflow evidence.

Need recent bounded volume + unresolved applicability share.

### Gate 3 — independent E3 historical cases

Pending contractor cohorts:

Toronto:

- Oriel Renovations;
- Sunnylea Homes;
- All Angles Renovations.

Ottawa:

- Upland Builds;
- Westend Bath and Kitchen;
- Ottawa General Contractors.

All six outreach addresses currently show no delivery failure. No historical samples have been received yet.

### Gate 4 — E4 pilot

Already prepared:

- 10-20 historical-case intake;
- blind benchmark tooling;
- read-only 20+ real-call pilot structure;
- clarification-friction measurement.

Do not start platform-specific engineering before a partner qualifies.

### Gate 5 — E5 pricing/resource commitment

Only after E3/E4 shows operational value.

Do not prematurely optimize x402 pricing or add commercial infrastructure.

## What not to do while external gates are unresolved

Do not spend time on:

- another municipality;
- another project family;
- another field-service adapter;
- more broad competitor list-building without a new falsification question;
- more permit-volume TAM arithmetic without an upstream denominator;
- polishing source-watch automation before a buyer values freshness;
- paid PermitSnapshot report purchase merely for curiosity;
- repeated follow-up emails on the same day;
- turning anecdotal reviews into incidence percentages.

## Product work allowed before a qualified reply

Only work that either fixes a known correctness/safety defect or directly reduces validation friction is justified.

Examples:

- correcting a proven false-negative path;
- making E3 case import/benchmarking easier;
- improving anonymization/privacy safeguards for a real pilot;
- fixing a broken public endpoint needed by a prospective tester.

Do not build speculative differentiation.

## Decision rule

At **50/100**, the next meaningful movement should come from external evidence.

- Qualified negative signal -> explicit **STOP / RE-SCOPE review**.
- Qualified positive E2 -> do not increase scope; move target toward E3/E4.
- Strong E3 -> pursue a narrow E4 pilot.
- E4 without E5 -> test commercial structure, not municipality expansion.
- E5 + credible scale path -> only then reconsider growth engineering.
