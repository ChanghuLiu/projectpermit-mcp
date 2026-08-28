# SoumissionRénovation Public Denominator Reconciliation — 2026-08-28

## Purpose

SoumissionRénovation is currently the strongest visible Quebec-wide aggregation candidate for ProjectPermit rescue validation.

Its public scale is large, but two current public statements use different figures and wording. This note prevents either number from being silently converted into ProjectPermit SAM.

Machine-readable sensitivity table:

- `data/soumissionrenovation_denominator_sensitivity_20260828.csv`

---

## 1. Two public scale statements

### A. Contractor signup page: 100,000 projects submitted per year

The current public contractor-registration page states:

> `100 000 projets soumis par année`

and markets those projects as pre-qualified real projects sent to contractors.

Source:

- `https://soumissionrenovation.ca/fr/formulaire/formulaire-entrepreneur`

This wording is more directly aligned with **platform submissions** than the broader 155k statement below.

But it remains a rounded vendor marketing claim, not an independently measured E2 denominator.

### B. 2025/2026 market report: 155,000 projects in 2025

SoumissionRénovation's 2026 market report says its analysis draws on more than 155,000 projects in 2025 and a large contractor network.

Source:

- `https://soumissionrenovation.ca/fr/blogue/devoilement-des-tendances-et-comportements-qui-faconneront-lindustrie-de-la-renovation-au-quebec-en-2026`

Earlier ProjectPermit review found the page mixes wording such as projects submitted / projects realized / platform activity, making the exact metric definition unsuitable as a clean upstream opportunity denominator.

Therefore:

- use **100k/year** as a clearer public *submission-scale sensitivity*;
- use **155k/year** only as an upper activity sensitivity;
- use **neither** as E2, SAM or qualifying ProjectPermit call volume.

---

## 2. 100k/year sensitivity

100,000 submissions/year is approximately:

> **8,333 submissions/month**

If every platform submission were eligible, reaching the Quebec rescue gates would require:

- 500 qualifying calls/month = about **6%** of all submissions;
- 2,000 qualifying calls/month = about **24%** of all submissions.

But every submission is not eligible. ProjectPermit currently covers only a bounded residential-family subset.

### If 25% of submissions map to current families

Relevant activity would be about **2,083/month**.

Required unresolved permit-applicability share within that subset:

- for 500 calls: **24%**;
- for 2,000 calls: **96%**.

### If 50% map to current families

Relevant activity would be about **4,167/month**.

Required unresolved share:

- for 500 calls: **12%**;
- for 2,000 calls: **48%**.

### If 75% map to current families

Relevant activity would be about **6,250/month**.

Required unresolved share:

- for 500 calls: **8%**;
- for 2,000 calls: **32%**.

Interpretation:

> the minimum 500-call rescue gate is mathematically plausible on a platform of this size, but only if a meaningful share of submissions both map to current families **and** still have unresolved permit applicability before contractor routing.

The stronger 2,000-call case is much harder unless current-family share and unresolved incidence are both unusually high.

---

## 3. 155k/year upper sensitivity

155,000/year is approximately **12,917/month**.

Because the metric is less clean, use this only to ask whether the rescue is even plausible under a generous activity base.

### 25% current-family share

Relevant activity: about **3,229/month**.

- 500 calls requires about **15.5%** unresolved;
- 2,000 calls requires about **61.9%** unresolved.

### 50% current-family share

Relevant activity: about **6,458/month**.

- 500 calls requires about **7.7%** unresolved;
- 2,000 calls requires about **31.0%** unresolved.

### 75% current-family share

Relevant activity: about **9,688/month**.

- 500 calls requires about **5.2%** unresolved;
- 2,000 calls requires about **20.6%** unresolved.

Again, these are sensitivity values only.

---

## 4. Why public taxonomy matters but does not solve the denominator

A separate fact-compatibility audit found SoumissionRénovation's public taxonomy already contains permit-relevant distinctions such as:

- new door/window opening;
- interior renovation without plumbing/electrical/structure;
- kitchen/bath/basement with versus without plumbing/electrical;
- patio subtypes;
- additions;
- sheds.

See:

- `docs/SOUMISSIONRENOVATION_FACT_COMPATIBILITY_20260828.md`
- `data/soumissionrenovation_taxonomy_fact_mapping.csv`

This is mildly favorable to integration feasibility.

But it does **not** tell us:

- how many annual submissions fall into those labels;
- how many are in Gatineau/Laval/Longueuil versus uncovered Quebec municipalities;
- how many permit decisions are already known;
- how many existing records are fact-sufficient;
- whether SoumissionRénovation exposes those labels through an API/partner feed;
- whether it would buy an external permit capability.

Therefore taxonomy cannot be used to convert 100k or 155k into ProjectPermit call volume.

---

## 5. Public integration boundary

The current public review did not find ordinary developer API, webhook or CRM-feed documentation for SoumissionRénovation.

The platform clearly has internal routing and contractor-matching infrastructure, but the public delivery model is:

`homeowner form -> SoumissionRénovation routing -> selected contractors`

Its privacy policy also explicitly notes that matched contractors may contact clients to ask for additional information about the work.

Source:

- `https://soumissionrenovation.ca/fr/politique-de-vie-privee`

This supports a cautious interpretation:

> some project facts may be collected or clarified after matching rather than being guaranteed complete at the pre-routing insertion point.

It does not prove the absence of a private integration API.

Do not send repetitive outreach merely because no public API documentation was found. If the current contact responds, ask the integration/feed question as a follow-up.

---

## 6. What would convert this from sensitivity to E2

A useful human/operator answer needs a bounded recent period and denominator, for example:

> In July 2026 we received 4,000 Quebec residential renovation requests; 1,100 mapped to the specified current families; 180 still required permit-applicability research before contractor routing.

Even approximate ranges are acceptable if they identify:

1. timeframe;
2. total/relevant denominator;
3. unresolved permit subset;
4. workflow stage.

Without that structure, `100,000/year` remains E0 public context.

---

## 7. Commercial implication

This reconciliation neither rescues nor kills ProjectPermit.

It does show why a province-wide aggregator is necessary:

- single contractors are unlikely to generate enough repeated current-family calls;
- a large marketplace can plausibly cross 500/month if unresolved incidence is material;
- the 2,000/month case remains demanding even with a very large upstream platform.

This is exactly why ProjectPermit must obtain a real platform denominator before adding more Quebec municipalities merely to inflate apparent coverage.

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

The public 100k/year statement improves the clarity of the activity sensitivity, but it is still vendor-provided context rather than E2 evidence.

The next score-moving evidence remains:

- a bounded upstream denominator;
- representative decision-fact sufficiency;
- build-vs-buy preference;
- repeat external calls or economic commitment.
