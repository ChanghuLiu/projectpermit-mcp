# Soumissions Maison → ProjectPermit Schema Fit — 2026-08-28

## Purpose

The Oolong / Soumissions Maison rescue route now has a plausible current upstream insertion point:

`renovation intake -> team sorting / matching -> contractor delivery`

The next question is not whether the forms look detailed. It is:

> **does the data already captured before contractor delivery contain the permit-critical facts required by ProjectPermit's current Quebec rules, without adding another homeowner questionnaire or manual research step?**

This note compares current public Soumissions Maison intake surfaces against the existing deterministic rules for:

- Gatineau;
- Laval;
- Longueuil.

Machine-readable companion:

- `data/soumissionsmaison_schema_fit_20260828.csv`

This is a **public schema-compatibility audit only**. It is not a representative historical sample and therefore is not E2/E3/E4/E5.

---

## 1. Current public intake is materially richer than a generic quote form

### Common multi-service / renovation-style form

Current Soumissions Maison pages publicly expose a reusable form pattern with fields including:

- unique request ID;
- residential vs commercial work;
- property type;
- ownership status;
- requested service;
- timing;
- broad work nature;
- full civic address;
- city;
- postal code;
- required project details / description.

One current form exposes the service choices directly, including:

- `Agrandissement/ajout d’étage`;
- `Construction cabanon/garage`;
- `Finition de sous-sol`;
- `Patio, balcon et terrasse`;
- `Portes et fenêtres`;
- `Rénovation de cuisine`;
- `Salle de bain`;
- `Peinture`;
- `Entrepreneur général`;
- `Autres travaux`.

Sources:

- `https://www.soumissionsmaison.com/renovation-et-travaux/`
- `https://www.soumissionsmaison.com/construction-patio-tableau-materiaux-prix/`
- `https://www.soumissionsmaison.com/renovation-cuisine-armoires-refacing/`

This is important because most ProjectPermit **family routing** can plausibly be normalized from an existing structured service value rather than inferred from arbitrary free text.

### Broad `Nature des travaux` is not a permit fact

The same public form exposes broad nature values such as:

- improvement / embellishment;
- non-urgent repair;
- urgent repair.

These are useful lead-routing attributes but they do **not** safely establish ProjectPermit facts such as:

- `structural_change=false`;
- `modifies_walls=false`;
- `replace_same_size_opening=true`;
- `room_count_change=false`;
- `accessory_permanent=true/false`.

Do not translate a generic `repair` selection into a permit exemption fact.

### Financing amount is not project cost

Some current Soumissions Maison forms ask whether the homeowner wants financing and may ask for an estimated financing amount.

That is **not** equivalent to ProjectPermit's `estimated_cost_cad`.

The amount financed may be lower/higher than the complete labour+materials project value. It must not be used to satisfy Gatineau's current cost-based renovation rule without external validation that the field represents total project cost.

---

## 2. Public form schemas are not perfectly uniform across funnels

The operator has a strong shared-form pattern, but current public pages do not expose one identical schema everywhere.

Examples:

### Generic renovation / kitchen / multi-service flows

Current forms expose a relatively rich combination of:

- full address;
- municipality/region;
- property type;
- service category;
- work nature;
- description.

### Dedicated addition page

The current dedicated home-enlargement page visibly asks for:

- unique ID;
- contact information;
- postal code;
- timing;
- required description.

It does not publicly expose the same full-address/property/service structure on that page.

Source:

- `https://www.soumissionsmaison.com/agrandissement-maison-et-ajout-etage/`

### Dedicated doors/windows page

The current doors/windows page visibly exposes:

- unique ID;
- postal code;
- timing;
- required project description.

A full civic address or a structured same-size-vs-new-opening field is not visible in the current public crawl.

Source:

- `https://www.soumissionsmaison.com/portes-et-fenetres/`

### Specialized plumbing page

The current plumbing page has a useful structured plumbing-work taxonomy, including examples such as:

- fixture/tap installation or repair;
- toilet installation;
- plumbing renovation;
- new-house plumbing;
- bath/shower connection;
- water-entry replacement;
- other plumbing services.

But that page visibly uses city + postal code rather than a full civic address, and the project description is optional.

Source:

- `https://www.soumissionsmaison.com/plombier-tuyauterie-services-travaux-prix/`

Interpretation:

> even if the operator ultimately has one central triage/backend, a ProjectPermit pilot should expect **funnel-specific field mapping** rather than assume one universal intake schema.

This makes `CENTRAL_WITH_SITE_MAPPING` a more plausible future topology than `CENTRAL_SINGLE_INTEGRATION`, but neither is proven publicly.

---

## 3. Family routing is mostly easy; permit-critical distinctions are not

The public form has enough structured service taxonomy to identify many current families directly:

| ProjectPermit family | Current structured service signal? | Family-routing friction |
|---|---|---|
| `addition` | `Agrandissement/ajout d’étage` | Low |
| `window_door` | `Portes et fenêtres` | Low |
| `basement` | `Finition de sous-sol` | Low |
| `deck_porch` | `Patio, balcon et terrasse` | Low |
| `accessory_structure` | `Construction cabanon/garage` | Medium — two materially different kinds are conflated |
| `kitchen_bath_plumbing` | `Rénovation de cuisine`, `Salle de bain`; separate plumbing taxonomy | Low family routing, medium/high action routing |
| `interior_renovation` | `Entrepreneur général`, `Peinture`, `Autres travaux` | Medium — no exact one-to-one family label |
| `dwelling_change` | no dedicated current option verified | High |

The commercial integration problem therefore moves one level deeper:

> the missing facts are usually **not `what broad type of renovation is this?`**; they are the facts that distinguish a permit-required branch from an exemption/confirmation branch *inside* that family.

---

## 4. Family-by-family decision fit

### A. `addition` — only clear cross-Quebec one-shot family

Public structured signal:

- exact service option `Agrandissement/ajout d’étage`;
- separate dedicated enlargement funnel also exists.

Current rule fit:

- Gatineau: `family=addition` alone triggers `REQUIRED`;
- Laval: `family=addition` alone triggers `REQUIRED`;
- Longueuil: `family=addition` alone triggers `LIKELY_REQUIRED`.

Therefore:

> **once the structured service is normalized to `family=addition`, the current core permit-positive routing does not require another project question in any of the three Quebec jurisdictions.**

Gatineau address-derived heritage/PIIA can add review context, but it does not remove the core required permit route.

Classification:

- **`DIRECT_STRUCTURED`**.

Commercial caveat:

- low technical friction does not imply high willingness to pay;
- `addition -> permit required/likely required` may be easy enough for the operator to know internally.

---

### B. `window_door` — direct family, missing the valuable action distinction

Public structured signal:

- exact service option `Portes et fenêtres`;
- dedicated doors/windows funnel exists.

Missing permit-critical facts:

- same-size replacement vs new/enlarged/relocated opening;
- structural/wall impact;
- Gatineau total project cost for non-always-required paths;
- Laval lot-line distance for the special same-size replacement trigger.

Current rule consequences:

- Gatineau: a clearly new/closed opening is permit-required, but ordinary non-trigger renovation can fall back to the C$26k cost rule;
- Laval: new/changed opening is required, whereas same-size replacement can be likely exempt unless the lot-line condition triggers;
- Longueuil: add/modify/remove opening is required, but same-size/no-action does not hit the same conclusive branch.

Therefore the structured family selection is insufficient for the economically interesting answer.

A description that explicitly says `create a new window` or `enlarge the opening` can be conservatively normalized without another homeowner question. A generic `replace windows` description cannot.

Default classification:

- **`FOLLOWUP_REQUIRED`**;
- conditional **`TEXT_DERIVABLE`** for explicit changed/new/removed opening cases.

---

### C. `interior_renovation` — broad form fields do not establish negative facts

Public signals can route generic interior work, painting, design or general-contractor requests.

Missing permit-critical facts include:

- structural change;
- wall modification;
- room dimensions / room-count change;
- Gatineau total project cost;
- precise Laval action.

A generic work-nature selection like `improvement` or `repair` does not establish those facts as false.

Consequences:

- Gatineau: the general renovation exemption path still needs total cost unless an independent positive structural/wall/foundation/opening trigger is explicit;
- Laval: useful exemption/required distinctions depend on action + structural/wall/room facts;
- Longueuil: family-level routing is broader and often `LIKELY_REQUIRED`, but the rules intentionally do not invent a cosmetic exemption.

Default classification:

- **`FOLLOWUP_REQUIRED`**.

Conditional positive case:

- if existing description explicitly states a structural change / wall removal, that trigger can be **`TEXT_DERIVABLE`**.

---

### D. `basement` — family is structured, exemption facts are absent

Public structured signal:

- exact service option `Finition de sous-sol`;
- dedicated basement funnel exists.

Missing facts:

- Gatineau: cost plus structure/wall/foundation facts for the non-trigger route;
- Laval: `room_count_change` and `structural_change` are both important for the explicit likely-no-permit branch.

Longueuil can broadly route a normalized basement family to `LIKELY_REQUIRED`, but that does not repair Gatineau/Laval fact gaps.

Default classification:

- **`FOLLOWUP_REQUIRED`**.

Conditional positive case:

- explicit description of wall/foundation/structural work can create an independent positive trigger without another question.

---

### E. `deck_porch` — full address helps Gatineau, but Laval needs an uncollected location fact

Public structured signal:

- exact service option `Patio, balcon et terrasse`;
- dedicated patio/terrace workflow exists;
- common form has full civic address.

Current rule fit:

- Gatineau: family route is generally likely-not-required unless PIIA/heritage applies; full address is useful because the existing Gatineau adapter can resolve those property overlays;
- Laval: the deterministic branch requires `yard` (`front/side/street-facing` vs `rear`), and Laval has no current address adapter supplying PIIA;
- Longueuil: family alone can produce a broad `LIKELY_REQUIRED` result.

The public form does **not** expose `yard` as a dedicated structured field.

Default cross-Quebec classification:

- **`FOLLOWUP_REQUIRED`**.

This is an important example where `address available=yes` is not the same as `all property/location facts available=yes`.

---

### F. `accessory_structure` — structured option is too coarse

Public structured signal:

- exact service option `Construction cabanon/garage`.

The option itself merges at least two materially different concepts.

Current rule gaps:

- Gatineau: needs `accessory_permanent` to select required vs likely-not-required;
- Laval: the current deterministic path is specifically for `kind=shed` and then needs `accessory_area_m2`; PIIA can also change the below-18m² route;
- Longueuil: current rules stay at `MUNICIPAL_CONFIRMATION_REQUIRED` for generic accessory structures.

Therefore a `cabanon/garage` selection cannot safely be converted into either:

- `kind=shed`;
- `family=addition` for an attached garage;
- or a permanent accessory structure,

without additional evidence.

Default classification:

- **`FOLLOWUP_REQUIRED`**;
- **`INSUFFICIENT_FOR_CONCLUSIVE_CURRENT_RULES`** in Longueuil for the generic accessory path.

---

### G. `kitchen_bath_plumbing` — better taxonomy, still missing permit action

Public family signals:

- `Rénovation de cuisine`;
- `Salle de bain`;
- separate plumbing form with specific plumbing-service types.

The plumbing taxonomy is genuinely useful for routing, but it still does not universally establish the exact permit fact:

- new bathroom vs renovation of an existing bathroom;
- fixture replacement vs plumbing-system relocation/extension;
- wall/structural changes;
- Gatineau total project cost.

Examples:

- `Pose d'une toilette` does not by itself say whether existing plumbing is reused or extended;
- `Rénovation plomberie` is too broad to map automatically to ProjectPermit's `plumbing_change=true` in every case;
- a common `Salle de bain` service selection does not distinguish `renovate_existing_bathroom` from `add_bathroom`.

Current rule consequences:

- Gatineau: non-independent-trigger paths still depend on cost;
- Laval: `new bathroom` is required while an existing bathroom renovation can be likely exempt, and structural/wall facts can override;
- Longueuil: family-level routing is broadly likely-required.

Default classification:

- **`FOLLOWUP_REQUIRED`**;
- conditional **`TEXT_DERIVABLE`** when the existing description explicitly states `add a new bathroom`, wall/structural change, new opening, etc.

---

### H. `dwelling_change` — weakest current schema/rule fit

No dedicated current common-form service option for adding/removing a dwelling unit was verified.

A qualifying project may appear inside:

- an addition;
- basement work;
- general renovation;
- free text.

But `addition` is not semantically equivalent to `dwelling_unit_change=true`.

Current rule consequences:

- Gatineau requires the semantic fact `dwelling_unit_change=true` for the dedicated trigger;
- Laval can route a normalized `dwelling_change` family to required;
- Longueuil does not currently have a dedicated `dwelling_change` branch and can fall through without another covered trigger.

Default classification:

- **`FOLLOWUP_REQUIRED` / `TEXT_DERIVABLE` only when description is explicit**;
- **partly `INSUFFICIENT_FOR_CURRENT_RULES`** across Quebec because current Longueuil coverage is incomplete.

---

## 5. Cross-Quebec result: family taxonomy is strong, decision-fact sufficiency is still narrow

Using a conservative requirement that the same existing intake pattern should support a useful current answer across Gatineau + Laval + Longueuil:

- **1 / 8 families = `DIRECT_STRUCTURED` by default**: `addition`;
- **6 / 8 families = `FOLLOWUP_REQUIRED` by default**: `window_door`, `interior_renovation`, `basement`, `deck_porch`, `accessory_structure`, `kitchen_bath_plumbing`;
- **1 / 8 families = follow-up/text-derived plus partial current-rule coverage gap**: `dwelling_change`.

This does **not** mean only 12.5% of real Soumissions Maison leads are usable.

Why not:

- family mix is unknown;
- required descriptions may already state the missing facts in many cases;
- some workflows expose richer dynamic subfields than the public crawler shows;
- a target may accept broad permit-positive routing rather than demand exemption precision;
- individual jurisdictions, especially Longueuil's coarse positive routing, can need fewer facts than the cross-Quebec standard.

Therefore public schema cannot substitute for the protocol's representative metric:

> `decision-fact sufficiency rate = sampled candidate cases where the existing record is enough without a new question / sampled candidate cases`.

---

## 6. The strongest public pilot starting point is not necessarily the biggest family

If an operator agreed to a shadow pilot, the public schema suggests two different starting strategies.

### Strategy A — lowest-friction plumbing/renovation record surface

A rich common renovation record can already provide:

- full address;
- municipality;
- property type;
- family/service;
- free-text details.

This maximizes the chance of observing whether missing facts are already present in descriptions.

### Strategy B — addition as a schema-control group

`addition` is useful as a control because the existing structured service category is enough for the current permit-positive branch across all three Quebec jurisdictions.

If even addition records cannot be reliably normalized from operator data, the integration/data-contract thesis is weaker than the public form suggests.

If addition works but other families fail, the problem is not transport/API plumbing; it is **decision-fact completeness**.

That is a useful diagnostic distinction.

---

## 7. What a future E3 sample must measure

Do not ask the operator merely whether these fields exist in its database.

For 50–100 chronological/anonymized recent candidate records, classify each as:

- `DIRECT_STRUCTURED`;
- `TEXT_DERIVABLE`;
- `FOLLOWUP_REQUIRED`;
- `EXTERNAL_PROPERTY_LOOKUP_REQUIRED`;
- `INSUFFICIENT_FOR_CURRENT_RULES`.

The sample should separately record:

- structured service value;
- full address available yes/no;
- existing description;
- missing decision facts;
- whether address/property resolution was actually required;
- whether ProjectPermit changed a triage/routing/manual-validation decision.

Templates and validation tooling already exist in:

- `docs/OPERATOR_RESCUE_PILOT_PROTOCOL_20260828.md`;
- `data/operator_rescue_pilot_sample_template.csv`;
- `market_research/operator_rescue_metrics.py`.

---

## 8. Integration implication

The public evidence now supports a more nuanced integration hypothesis:

`multiple funnel schemas -> funnel-specific mapping -> common normalized ProjectPermit facts -> preflight -> existing triage`

rather than:

`one identical form everywhere -> one zero-effort API call`.

This is still compatible with a commercially good operator integration **if**:

- the relevant funnels converge centrally;
- mapping cost is modest;
- descriptions already contain missing facts often enough;
- the permit signal materially changes triage/value;
- the operator prefers external maintenance over adding the rules internally.

But the public form review alone does not prove any of those rates/preferences.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

The finding is mixed:

Positive:

- current public taxonomy makes broad family normalization much easier than a generic free-text lead flow;
- full address is present on important common renovation flows;
- `addition` is a genuine one-shot cross-Quebec schema match;
- existing descriptions may resolve some positive triggers without new homeowner interaction.

Negative:

- most families still lack one or more permit-critical structured distinctions;
- public schemas vary by funnel;
- Gatineau's cost dependency remains a major recurring gap;
- Laval often needs specific negative/location/geometry facts not exposed by the common form;
- Longueuil still lacks conclusive current coverage for some families.

Only representative chronological records can tell whether the required free text already closes these gaps often enough to preserve a low-friction API thesis.

## Bottom line

The Soumissions Maison opportunity is **not blocked by broad project taxonomy**.

It is blocked by a narrower empirical question:

> **after the operator already knows the project family, how often does the existing record contain the exact decision-changing facts needed by the municipal rule without asking the homeowner anything else?**

Public schema suggests `addition` should work immediately; most other families remain description-dependent or follow-up-dependent.

That makes representative record replay, not more form scraping or product development, the next proof.
