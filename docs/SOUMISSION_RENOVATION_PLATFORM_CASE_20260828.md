# SoumissionRénovation Platform Validation Case — 2026-08-28

## Why this platform matters

SoumissionRénovation.ca is currently the strongest publicly observed Quebec platform candidate for ProjectPermit because it combines:

- very large recurring renovation-project platform activity;
- a Quebec-focused contractor network;
- project details collected before contractor matching;
- explicit current-family service categories;
- a public workflow that still directs users to municipalities to determine permit requirements rather than exposing an observed automated permit-applicability step.

This creates a plausible place to test **distribution + differentiation together**.

## Public scale evidence

SoumissionRénovation's 2026 market report states that the platform had **155,000+ projects in 2025** and a network of **17,500 certified contractors**. The same report says the platform has handled 889,000 projects since creation.

Source:

- `https://soumissionrenovation.ca/fr/blogue/devoilement-des-tendances-et-comportements-qui-faconneront-lindustrie-de-la-renovation-au-quebec-en-2026`

### Metric-definition caveat

The source is internally ambiguous about the exact event definition:

- the narrative says `155 000 projets réalisés en 2025`;
- a nearby chart section is titled `Nombre total de projets soumis sur la plateforme et leur valeur`;
- the later summary again says `+ de 155 000 projets réalisés en 2025`.

Therefore **do not treat 155,000 as a clean observed intake-request count** until SoumissionRénovation confirms the definition. It is evidence of very large platform project activity, but the public page does not cleanly distinguish submitted projects, matched projects, completed/realized projects, or a shared internal `project` metric.

155,000 annual projects corresponds to roughly **12,900 platform project events/month** only as a simple annual-average sensitivity.

This is **not** current ProjectPermit SAM because:

- the event definition is not cleanly confirmed as intake;
- the public figure is Quebec-wide / platform-wide;
- it includes project types outside ProjectPermit's current families;
- it includes municipalities outside current ProjectPermit coverage.

### Current threshold sensitivity

If the 155k figure is comparable to the project events available at or before contractor matching, then at roughly 12,900 total project events/month:

- 500 current-family candidate events/month would require roughly **3.9%** of total project flow;
- 2,000 current-family candidate events/month would require roughly **15.5%** of total project flow.

These percentages are only sensitivity thresholds. They are **not observed current-family shares**, and they should not be used if the 155k metric is later confirmed to represent only downstream/completed projects that are not available at the pre-quote decision point.

## Workflow placement evidence

Current SoumissionRénovation service pages describe a simple intake sequence:

1. client describes the project and submits an online form in under five minutes;
2. SoumissionRénovation matches the project with qualified contractors, generally within 48 hours;
3. the client compares contractor quotes.

Sources:

- `https://www.soumissionrenovation.ca/fr/service/entrepreneurs-renovation`
- `https://www.soumissionrenovation.ca/fr/comment-ca-fonctionne?contractor=true`

This is upstream enough for a permit-applicability preflight if the project form contains adequate municipality/address + scope information.

## Current-family overlap is visibly present, but share is not public

SoumissionRénovation has dedicated project/intake surfaces for current ProjectPermit families including:

- basement renovation;
- home additions;
- doors and windows;
- general/home renovation;
- construction;
- structural/interior-system work.

Sources:

- `https://soumissionrenovation.ca/fr/service/renovation-sous-sol`
- `https://soumissionrenovation.ca/fr/service/agrandissement-de-maison`
- `https://soumissionrenovation.ca/fr/service/portes-et-fenetres`
- `https://soumissionrenovation.ca/fr/service/renovation-de-maison`
- `https://soumissionrenovation.ca/fr/service/construction-entrepreneurs`
- `https://soumissionrenovation.ca/fr/service/systeme-interieur-soumission`

The contractor/service taxonomy visible in covered-city directories also includes addition, balconies/patios, accessory sheds/garages, creation of door/window openings, basement, kitchen, bathroom and general renovation scopes.

Example covered-city evidence:

- `https://soumissionrenovation.ca/fr/repertoire/qc/gatineau/renovation`
- `https://soumissionrenovation.ca/fr/repertoire/QC/gatineau/construction`
- `https://soumissionrenovation.ca/fr/repertoire/qc/gatineau/entrepreneur-general`
- `https://soumissionrenovation.ca/fr/repertoire/qc/laval/plancher`
- `https://soumissionrenovation.ca/fr/repertoire/qc/longueuil/entrepreneur-general`

Do **not** infer project-demand share from contractor/service listings. These pages prove workflow/category/geography presence only.

## Public permit workflow still appears manual / externalized

SoumissionRénovation's current contractor-selection guidance explicitly tells clients to contact/check their municipality before work to determine whether a special building permit is needed, with municipal calling suggested when in doubt.

Source:

- `https://soumissionrenovation.ca/fr/blogue/guide-pratique-choisir-entrepreneur`

This is a materially stronger differentiation signal than a generic marketplace gap because the platform already has project intake and matching, while permit applicability is publicly described as a separate municipal-research step.

Important boundary:

> this does **not** prove SoumissionRénovation internally lacks automation or partner tooling that is not visible publicly.

The platform itself must confirm the actual operational workflow.

## Covered-geography correction

ProjectPermit's current Quebec coverage is limited to existing supported municipalities such as:

- Gatineau;
- Laval;
- Longueuil.

The Quebec-wide 155k/year platform figure **cannot** satisfy the current 500+/month gate by itself.

The required scale observation is:

> one recent complete month's current-family project intake in Gatineau + Laval + Longueuil (or another explicitly covered ProjectPermit geography), with permit applicability still unresolved at intake/quote routing.

If only Quebec-wide volume is available, it is an **expansion signal**, not current covered-market distribution proof.

## Public covered-city denominator path exhausted

A targeted 2026-08-28 public review looked specifically for project-volume breakdowns for **Gatineau / Outaouais, Laval and Longueuil / Montérégie**.

What is publicly reproducible:

- the Quebec-wide 2025 platform signal of 155,000+ projects and 17,500 certified contractors;
- active contractor/service directory coverage in Gatineau, Laval and Longueuil;
- visible overlap between those local service taxonomies and current ProjectPermit families.

What was **not** found in the current public material:

- project events/month by Gatineau, Laval or Longueuil;
- Outaouais/Laval/Montérégie regional project-volume breakdowns in the annual report;
- current-family share by covered city;
- pre-quote unresolved permit-applicability incidence by city or region.

Therefore the public denominator route is now classified as:

> **EXHAUSTED FOR CURRENT COVERED-CITY SCALE — INTERNAL/PARTNER DATA REQUIRED**

Do not substitute any of the following:

- Quebec population share;
- city population share;
- number of listed contractors;
- directory service counts;
- the 155k Quebec-wide annual project figure;
- generic renovation-market statistics.

Those proxies cannot establish the required observation:

`covered-city current-family upstream events × unresolved permit-applicability incidence`.

This is not negative product evidence. It is a **measurement boundary**: scale validation for SoumissionRénovation now requires the platform, an integration partner, or another bounded first-party workflow dataset.

## Outreach sent

Email sent to `pro@soumissionrenovation.ca` on 2026-08-28 requesting:

1. one recent-complete-month aggregate range for projects matching the current 8-family scope set;
2. whether permit applicability is already resolved before contractor matching or still checked by client/advisor/contractor against municipalities;
3. whether a machine result such as `permit required / likely not required / municipal confirmation required + official source` would materially improve the workflow versus current tools/municipal assistants;
4. a follow-up clarification requesting a combined Gatineau + Laval + Longueuil monthly range so Quebec-wide scale is not misrepresented as covered-market volume.

No customer-identifying information was requested.

## Upgrade conditions

SoumissionRénovation becomes a meaningful scale/differentiation validation win only if it provides evidence such as:

- **500+ recent monthly current-family project events in currently covered municipalities** with permit applicability unresolved upstream; or
- a smaller covered-city denominator plus a credible expansion denominator, coupled with concrete platform interest in a multi-city API; and
- a specific reason municipality assistants/manual research do not fit the platform workflow; ideally
- willingness to test an external machine-readable preflight in real intake/matching flow.

## Negative / pause conditions

Downgrade this route if:

- the 155k metric is not comparable to an upstream project/intake event and no upstream denominator can be obtained;
- covered-city current-family volume is below the 500/month threshold and there is no credible multi-city expansion pull;
- permit applicability is normally already known before project matching;
- contractors reliably handle permit decisions downstream without meaningful friction;
- the platform already uses an internal/partner solution that solves the decision well enough;
- the platform only values resident education content or deep links rather than a machine API;
- willingness to pay is too low to support Quebec rule maintenance.

## Current classification

As of 2026-08-28:

> **HIGH-PRIORITY QUEBEC SCALE + DIFFERENTIATION CANDIDATE — PUBLIC COVERED-CITY DENOMINATOR UNAVAILABLE / EXTERNAL VALIDATION REQUIRED**

SoumissionRénovation has the strongest observed public project-activity shape in Quebec, but the decisive observations remain unknown and are no longer expected to be recoverable from public proxies:

1. the exact operational definition of the public 155k project metric;
2. covered-city current-family project events/month at the pre-quote/intake stage;
3. unresolved permit-applicability incidence before contractor matching.
