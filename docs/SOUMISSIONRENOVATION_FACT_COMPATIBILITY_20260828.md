# SoumissionRénovation Fact Compatibility Addendum — 2026-08-28

## Purpose

The initial upstream fact-sufficiency audit found that a lightweight quote form can lack several decision-changing facts required by ProjectPermit's Quebec rules.

SoumissionRénovation is important because its public service taxonomy is materially more granular than a generic `describe your renovation` intake.

This addendum asks a narrow question:

> does the platform's existing public taxonomy show that at least some ProjectPermit facts could already be encoded before contractor routing, reducing integration friction?

The answer is **yes, partially**.

This is still public technical compatibility evidence, not E2/E3 evidence about real lead records or usage.

Machine-readable mapping:

- `data/soumissionrenovation_taxonomy_fact_mapping.csv`

---

## Public evidence

SoumissionRénovation operates project-specific service pages for categories such as:

- terrace/patio;
- doors/windows;
- bathroom renovation;
- kitchen renovation.

The pages say the homeowner describes the project in a form taking under five minutes and is then matched with up to three certified contractors.

Sources:

- `https://soumissionrenovation.ca/fr/service/terrasse`
- `https://soumissionrenovation.ca/fr/service/portes-et-fenetres`
- `https://soumissionrenovation.ca/fr/service/renovation-salle-bain-D`
- `https://soumissionrenovation.ca/fr/service/cuisine-renovation`

More importantly, public contractor/service listings expose a granular routing taxonomy including labels such as:

- `Rénovations - Cuisine (avec électricité / plomberie)`;
- `Rénovations - Cuisine (sans électricité / plomberie)`;
- `Rénovations - Salle de bain (avec électricité / plomberie)`;
- `Rénovations - Salle de bain (sans électricité / plomberie)`;
- `Rénovations - Sous-sol (avec électricité / plomberie)`;
- `Rénovations - Sous-sol (sans électricité / plomberie)`;
- `Rénovations intérieures - Sans Plomberie/ Électricité/Structure`;
- `Création ouverture de portes et/ou de fenêtres`;
- `Sciage de béton et ajout de fenêtre`;
- `Patio - Au sol`;
- `Patio - Sur un toît`;
- `Agrandissement de maison`;
- `Cabanon`.

Representative public pages:

- `https://soumissionrenovation.ca/fr/entrepreneur/9378-2472_quebec_inc`
- `https://soumissionrenovation.ca/fr/entrepreneur/9442-2425-quebec-inc`
- `https://soumissionrenovation.ca/fr/entrepreneur/renovation-sr`
- public directory pages for doors/windows and renovation categories.

---

## Why this is meaningful for ProjectPermit

Several labels are already close to deterministic normalization facts.

### Strong compatibility examples

#### `Agrandissement de maison`

This maps directly to `family=addition`, which already produces a permit-positive route in Gatineau, Laval and Longueuil.

This is a low-fact-friction case.

#### `Création ouverture de portes et/ou de fenêtres`

This strongly signals a new/changed opening rather than a same-size replacement.

That is materially more useful to ProjectPermit than a generic `portes et fenêtres` category because changed/new openings are explicit permit triggers in current Quebec rules.

#### `Sciage de béton et ajout de fenêtre`

This also strongly identifies an added opening and is far more decision-compatible than generic window replacement.

#### `Rénovations intérieures - Sans Plomberie/ Électricité/Structure`

This is unusually useful because the taxonomy itself contains negative scope facts: no plumbing, electrical or structural work.

It does not fully solve Gatineau's cost threshold or all Laval action details, but it can eliminate several otherwise-required follow-up facts.

#### `Cabanon`

This gives ProjectPermit a strong accessory-structure kind signal (`shed`), though Gatineau still needs permanence and Laval still needs area/PIIA for the useful threshold branch.

### Partial compatibility examples

Kitchen, bathroom and basement categories distinguish `avec` versus `sans électricité / plomberie`.

That is useful but should not be over-normalized.

For example:

> `avec plomberie` does **not** necessarily mean `plumbing_change=true` in ProjectPermit's semantic sense.

It may include fixture replacement, reconnection or other plumbing work that does not match a relocation/new-plumbing trigger.

Therefore these labels reduce ambiguity but do not by themselves justify every rule fact.

Similarly, `Patio - Au sol` identifies a subtype but does not supply Laval's `yard` fact or property-overlay status.

---

## Critical evidence boundary

The public taxonomy proves that **structured routing concepts exist inside the SoumissionRénovation ecosystem**.

It does **not** prove any of the following:

- every inbound homeowner lead is tagged with the same taxonomy before contractor routing;
- all labels are exposed in an API or partner feed;
- the platform stores the necessary numeric/boolean details for each current ProjectPermit rule;
- a lead contains a full civic address;
- a lead contains Gatineau's estimated project cost in the exact rule-compatible sense;
- Laval yard, lot-line distance, accessory area or PIIA are already available;
- ProjectPermit could execute without any NLP/follow-up step;
- the platform wants an external permit API.

This is why the existing direct outreach asking for a bounded workflow denominator remains more important than public taxonomy analysis.

---

## Revised fact-sufficiency interpretation

The public Quebec upstream market is not uniformly `thin form -> impossible automation`.

A better working model is:

### Lightweight lead networks

Some public forms visibly expose only service/postal code/project description. They may require NLP and follow-up for many current rule branches.

### Mature category-driven marketplaces

SoumissionRénovation demonstrates that a large platform can already maintain a detailed project/trade taxonomy containing several permit-relevant distinctions.

For those platforms, the decisive metric is not whether structured facts exist at all. It is:

> **what fraction of real current-family leads already contain enough trustworthy facts for a useful ProjectPermit determination without adding new customer questions?**

That is still the `decision-fact sufficiency rate` defined in the parent audit.

---

## Rescue impact

This finding is mildly favorable to the Quebec rescue because it weakens the strongest version of the integration-friction objection.

It shows at least one high-scale target may already possess useful normalization signals such as:

- addition;
- new opening;
- no-structure interior work;
- plumbing/electrical involvement;
- shed/accessory subtype;
- patio subtype.

But it does **not** raise the commercial score because:

- no bounded current-family lead count is known;
- no unresolved permit share is known;
- no representative record sample is available;
- no decision-fact sufficiency rate is measured;
- no build-vs-buy preference or price acceptance exists.

ProjectPermit therefore remains **50/100, PAUSE / RE-SCOPE**.

## Next evidence request if SoumissionRénovation replies

Do not send a second same-day message merely because this taxonomy was discovered.

If the current outreach receives a human response, the highest-value follow-up is:

1. Are those granular service labels attached to inbound project records before contractor routing?
2. Can they provide 5–20 anonymized recent records containing only service/taxonomy + project description + municipality/region + whatever scope fields already exist?
3. For those records, was permit applicability already known or researched before contractor matching?

That single sample could simultaneously test:

- E2 incidence;
- E3 accuracy;
- decision-fact sufficiency;
- actual normalization friction.
