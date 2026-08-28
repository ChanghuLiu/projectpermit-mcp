# Municipality-Specific Divergence Benchmark

Updated: 2026-08-28

Purpose: test whether ProjectPermit has a real information advantage over generic Ontario permit checkers. This is **technical/product-boundary evidence only**. It is not E2/E3/E4/E5 market validation.

## Hypothesis

A generic Ontario-level permit checker is easy to reproduce and is already available in adjacent products. ProjectPermit is only worth maintaining as a separate capability if municipality-specific rules can materially change the routing result for otherwise similar renovation scopes.

The benchmark therefore looks for cases where the same normalized project description should produce different preflight outcomes by municipality, or where a province-wide heuristic is too coarse to make a safe deterministic decision.

## Public generic-checker baseline

### Build Smart Ontario

Public 2026 positioning includes a free Permit Requirement Checker inside a broader contractor/planning funnel. Its Ontario permit guide summarizes common projects with broad heuristics such as:

- basements (finishing): usually permit-required;
- decks above about 24 in / 600 mm, attached decks, or decks with guards: usually permit-required;
- same-opening windows/doors without structural changes: typically exempt;
- plumbing relocation/new fixtures: usually permit-required.

Sources:

- https://buildsmartontario.com/guides/permits
- https://buildsmartontario.com/tools
- https://buildsmartontario.com/services/basement
- https://buildsmartontario.com/services/decks

This is a useful Ontario-wide summary, but the site itself says municipal thresholds/exemptions vary and users should confirm with the municipality.

### RealCraft Permit Advisor

RealCraft publicly advertises a free Ontario Permit Navigator in the same upstream flow as project description and quote acquisition. It explicitly says it has municipality-specific guides for Ottawa, Toronto, Mississauga, Hamilton and London.

Source:

- https://realcraft.ca/for-clients/

This is materially closer to ProjectPermit's target workflow than a generic homeowner guide. No public developer/API surface, stable rule-id contract, address-aware municipal-data contract, or auditable deterministic evidence interface was found in the current scan. An external build-vs-buy question has already been sent; do not count the lack of reply as validation.

### PermitSnapshot

PermitSnapshot sells AI-generated Ontario permit/feasibility reports for builders, realtors and investors at a public price of C$49 + HST per report and advertises all 414 Ontario municipalities. Its builder use case explicitly includes running a report before quoting to identify permit and zoning risk.

Sources:

- https://permitsnapshot.ca/
- https://permitsnapshot.ca/disclaimers

Its own disclaimer says reports are AI-generated, use general Ontario regulatory context, may not reflect the current municipality-specific zoning by-law or supplementary requirements, and require independent municipal verification. This is willingness-to-pay/competition context, not evidence that ProjectPermit's narrower per-call API price is validated.

## Case A — clean finished basement

Normalized scope:

```json
{
  "family": "basement",
  "action": "finish_basement",
  "structural_change": false,
  "material_alteration": false,
  "dwelling_unit_change": false,
  "new_plumbing": false
}
```

### Toronto

City of Toronto's current page explicitly lists finishing a basement of a house as not requiring a building permit when there are no structural/material alterations, no additional dwelling unit and no new plumbing.

Expected ProjectPermit routing: `LIKELY_NOT_REQUIRED`.

Official source:

- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

### Mississauga

City of Mississauga currently lists finishing a basement to create rooms or living space among projects requiring a building permit.

Expected ProjectPermit routing: `REQUIRED`.

Official source:

- https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/

### Ottawa

Ottawa maintains a dedicated finished-basement permit application path and its current FAQ states a permit may be required when basement renovation includes installation, erection, extension, material alteration or repair. Ottawa also publishes specific finished-basement submission requirements.

Expected ProjectPermit behavior should remain tied to Ottawa's published rule set rather than inheriting Toronto's explicit exemption.

Official sources:

- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/finishing-basement
- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/frequently-asked-questions/building-permits

### Product implication

A province-wide rule such as `finished basement -> usually permit` is directionally useful but loses a real Toronto exception. A province-wide rule such as `clean basement finish -> exempt` would be unsafe in Mississauga. This is a concrete example where municipality-level routing can change the result.

## Case B — same-size window replacement

Normalized scope:

```json
{
  "family": "window_door",
  "action": "replace_same_size",
  "structural_change": false
}
```

Ottawa and Mississauga both explicitly list same-size window replacement among permit-exempt projects. Toronto's exemption is narrower: same-location/same-size replacement is exempt for a detached, semi-detached or row house containing a single dwelling unit when structural support is unaffected and no new exit is created; replacement windows/doors in other building types are listed as permit-required.

Official sources:

- Ottawa: https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits
- Mississauga: https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
- Toronto: https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

Product implication: the generic statement `same-size window -> no permit` is insufficient for Toronto unless building form/use and exit/structural facts are also normalized.

## Case C — low deck threshold

Ontario-wide tools commonly summarize a ~600 mm / 24 in threshold, but municipal wording still matters.

- Toronto: deck more than 600 mm above ground requires a permit; the low-platform exemption also depends on whether it forms part of a required exit.
- Ottawa: deck less than 24 inches above grade is listed as exempt **except main entrance**.
- Mississauga: current page lists deck greater than 0.61 m / 2 ft as requiring a permit and deck less than 600 mm as not requiring one; the published wording creates a narrow threshold ambiguity that should be handled conservatively rather than guessed.

Official sources:

- Toronto: https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
- Ottawa: https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits
- Mississauga: https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/

Product implication: a single numeric threshold is not enough; access/exit use and publication-boundary ambiguity can change `LIKELY_NOT_REQUIRED` into `MUNICIPAL_CONFIRMATION_REQUIRED`.

## Case D — Quebec vs Ontario rule architecture

Gatineau creates an even stronger cross-province divergence because its existing-building renovation exemption depends on total labour/material cost and PIIA/heritage conditions, while the Ontario cities above primarily publish scope/structure/use thresholds for the same broad renovation families.

This is why a Canada-wide generic classifier is not sufficient to reproduce the current ProjectPermit contract. The value, if any, is in maintained municipal exceptions and property overlays, not in the generic project taxonomy.

## What this benchmark proves

It supports the following product-boundary claim:

> Municipality-specific rules can materially change a permit-preflight result for the same or nearly identical project scope.

It does **not** prove:

- that buyers need a separate API for the difference;
- that RealCraft/other competitors cannot reproduce the same rules;
- that ProjectPermit's implementation is more accurate in representative historical cases;
- that the difference changes a quote/schedule often enough to pay for;
- E2, E3, E4 or E5.

## Falsification criteria

ProjectPermit should be downgraded or stopped if external evidence shows any of the following:

1. Request/Estimate/Quote systems are satisfied by coarse municipality-aware guidance and do not need deterministic rule/evidence detail.
2. Representative E3 cases show that municipality-specific exceptions rarely change workflow routing.
3. A competing platform exposes equivalent municipality-specific deterministic evidence/API functionality at negligible marginal cost and gains distribution first.
4. The address/property-aware share is too small to monetize.
5. Maintaining municipal exceptions costs more than the observable paid-call density justifies.

## Next benchmark requirement

The next independent E3 sample should intentionally include **divergence-sensitive cases**, not only obvious permit-positive projects:

- clean basement finishes;
- same-size vs enlarged windows/doors;
- low decks near the published threshold and entrance/exit cases;
- small accessory structures near 10 m2 / 15 m2 boundaries;
- same-location plumbing fixtures vs relocated/new plumbing;
- heritage/PIIA/property-overlay cases where available.

The safety metric remains false `LIKELY_NOT_REQUIRED` outcomes. A rule corpus is not a moat until representative external cases demonstrate that these municipal distinctions are both accurate and operationally useful.