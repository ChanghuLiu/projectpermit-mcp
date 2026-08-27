# Municipal rule differentiation diagnostic

Updated: 2026-08-27

Purpose: test whether a generic Ontario/Canada permit checklist is technically sufficient for ProjectPermit's current project families, or whether identical normalized scopes can genuinely produce opposite permit outcomes across supported municipalities.

This is **internal synthetic technical/market-structure evidence only**. It is not E2, E3, E4, E5, demand evidence, willingness-to-pay evidence, or an accuracy benchmark against representative external cases.

## Reproducible audit

Scripts:

- `market_research/cross_jurisdiction_scope_matrix.py`
- `market_research/cross_jurisdiction_strict_audit.py`

GitHub Actions workflow:

- `.github/workflows/cross-jurisdiction-scope-matrix.yml`

The audit runs 15 identical, address-free normalized scopes across all seven supported jurisdictions. Heritage/PIIA property flags are explicitly false so the first pass measures municipal rule differences rather than GIS/address differences.

### Broad bucket result

- cases: **15**
- jurisdictions: **7**
- cases with any permit-positive vs permit-negative bucket divergence: **9/15 = 60.0%**
- cases where all seven jurisdictions land in the same broad bucket: **3/15 = 20.0%**
- cases containing at least one review/confirmation/out-of-scope result: **10/15**

Because the broad measure includes `LIKELY_REQUIRED`, it is intentionally not the preferred headline.

### Strict result

The strict audit counts a case only when the **same normalized facts** produce:

- `REQUIRED` in at least one supported jurisdiction; and
- `LIKELY_NOT_REQUIRED` in at least one other supported jurisdiction.

It does **not** use `LIKELY_REQUIRED`, `MUNICIPAL_CONFIRMATION_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED` or `OUT_OF_SCOPE` to manufacture a polarity difference.

Result:

> **7 / 15 cases = 46.67% strict REQUIRED-vs-LIKELY_NOT_REQUIRED divergence**

Only **1 / 15** cases was decisively unanimous across all seven jurisdictions: structural enlargement of a window/opening was permit-required everywhere in the current rulesets.

Strict-divergence cases:

1. clean basement finish;
2. basement finish with new plumbing;
3. low detached deck at 500 mm / 9 m²;
4. attached deck at 700 mm / 12 m²;
5. permanent detached storage shed at 9 m²;
6. permanent detached storage shed at 14 m²;
7. relocated plumbing fixture.

## Official-source spot checks

The matrix is synthetic, so important divergences were checked against current first-party municipal guidance rather than accepted merely because the rules engine produced them.

### Clean basement finish — Toronto vs Mississauga/Ottawa

Toronto's current `When Do I Need a Building Permit?` page explicitly states that finishing a house basement does not require a building permit when there are no structural/material alterations, no additional dwelling unit, and no new plumbing.

Source:
https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

Mississauga explicitly lists `Finishing a basement to create rooms or living space` among permit-required projects.

Source:
https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/

Ottawa publishes a dedicated finished-basement permit application workflow and says basement finishing may require a permit where the activity includes installation, erection, extension, material alteration or repair.

Sources:
https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/finishing-basement
https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/frequently-asked-questions/building-permits

This is a genuine municipality-specific workflow difference, not a generic Ontario rule.

### Plumbing relocation under the Gatineau cost threshold

Gatineau's current summary lists electrical, plumbing and heating/air-conditioning work under **$26,000** on an existing principal building as permit-exempt when the stated PIIA/heritage exceptions do not apply. Work over $26,000 is listed as permit-required.

Source:
https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fai_je_besoin_permis_construire_ou_certificat_autorisation

Toronto and Mississauga treat installing/modifying/relocating plumbing systems or fixtures as permit-required, while same-location fixture replacement is exempt.

Sources:
https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/

This supports a real Gatineau-vs-Ontario polarity difference for the synthetic sub-$26k plumbing-relocation scope.

### Permanent small shed — Gatineau vs Ontario cities

Gatineau states that a detached movable accessory building does not need a permit, while a **permanent** accessory building requires a building permit.

Sources:
https://www.gatineau.ca/portail/default.aspx?c=fr-CA&p=guichet_municipal%2Freglements_municipaux%2Fbatiments_accessoires_detaches_habitation
https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fpermis_construire%2Fconstruction_batiment_accessoire

Toronto, Mississauga and Ottawa publish small-shed exemptions around the 15 m² threshold subject to conditions such as one storey, detached/storage-only use and no plumbing.

Sources:
https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits

Therefore 9 m² and 14 m² permanent storage sheds can legitimately fall on opposite sides of the permit decision depending on municipality.

### Decks — Gatineau / Ontario / Vancouver

Gatineau's current summary lists residential porches, balconies, galleries, terraces, exterior stairs, ramps, awnings and canopies as permit-exempt when the stated PIIA/heritage condition does not apply.

Source:
https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fai_je_besoin_permis_construire_ou_certificat_autorisation

Toronto and Mississauga use approximately 600 mm deck-height thresholds in their public building-permit guidance. Ottawa also exposes detailed height/area/attachment/access conditions.

Sources:
https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/decks

Vancouver's current `When you need a permit` guidance generally includes building or altering a garage, shed or deck among permit-required work.

Source:
https://vancouver.ca/home-property-development/when-you-need-a-permit.aspx

This makes deck logic a clear example where a generic cross-Canada yes/no checklist is unsafe.

## What this proves

The current supported geography contains real municipality-level decision differences. A generic national/provincial checklist can therefore be technically insufficient for several common current-family scopes.

The most defensible technical statement is:

> Municipality-specific permit applicability is a real problem. In the current synthetic matrix, 46.67% of standard scopes produce a strict `REQUIRED` vs `LIKELY_NOT_REQUIRED` split across supported cities, and multiple major splits are independently visible in current first-party municipal guidance.

## What this does **not** prove

It does not show:

- that 46.67% of real customer projects experience such a split;
- that representative workflow mix resembles these 15 synthetic fixtures;
- that address/property context is needed at a commercially meaningful rate;
- that contractors do not already know the local rule;
- that a free municipality-specific checker is insufficient;
- that anyone will call ProjectPermit repeatedly;
- that anyone will pay $0.20-$0.50 per preflight.

Do not upgrade E3/E4/E5 or the Go/No-Go score merely because this synthetic discrimination test is favorable.

## Next commercial measurement

The next external benchmark should record a new field:

`municipality_specificity_changed_generic_answer`

For each representative historical case, ask whether a generic Ontario/Quebec/BC checklist would have produced the same safe routing result, or whether a city-specific threshold/exemption/property fact was material.

The useful metric is:

`representative cases where municipality/address specificity materially changes safe routing / all representative current-family cases`

If that share is low, ProjectPermit's technical sophistication has weak commercial value even if the rule matrix is correct.

If that share is meaningful **and** it occurs in an upstream repeated workflow, it strengthens the case for an embedded evidence-linked API rather than a generic bundled checker.