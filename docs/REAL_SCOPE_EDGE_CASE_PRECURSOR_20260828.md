# Real-scope edge-case / clarification-friction precursor — 2026-08-28

## Purpose

Use ordinary public HomeStars renovation scopes — searched by project family, **not by `permit` problem keywords** — to test a narrow product question:

> Does a real upstream project description usually contain enough decisive facts for ProjectPermit immediately, or would a useful integration commonly need a small number of targeted clarification questions?

This is a **structured convenience sample**, not a representative benchmark. Search ranking, public-review availability and review wording create strong selection bias. There is no independently verified historical permit outcome for most rows.

Therefore this does **not** count as E2, E3, E4 or demand evidence.

## Method

Searches focused on ordinary 2025 HomeStars scopes in supported Ontario municipalities and current ProjectPermit families: basement, bathroom/kitchen, addition, windows and decks.

For each visible scope, classify only the **input completeness** needed to reach a safe permit-applicability decision under current first-party municipal guidance:

- `0` = public scope itself contains a decisive permit trigger / clear enough fact pattern for the basic applicability decision;
- `1-3` = family is known, but one to three decisive facts are missing;
- `>3/CONFIRM` = likely requires broader site/property/expert context.

This does not assert that the public review reproduces the original lead form exactly.

## Convenience sample

| # | City | Public scope | Family | Likely extra decisive facts | Why |
|---|---|---|---|---:|---|
| 1 | Toronto | Renovate existing basement, ~1000+ sq ft | basement | 1-3 | Need to know material/structural alteration, new plumbing, additional dwelling unit. Toronto has a narrower exemption boundary than a generic `all basement finishing needs permit` rule. |
| 2 | Toronto | Basement transformed with guest bedroom, bathroom and wet bar | basement | 1-3 | Bathroom/wet bar strongly suggest plumbing, but the public text does not establish whether plumbing is new/relocated or already present; dwelling-unit status also matters. |
| 3 | Toronto | Basement renovated into a **legal rental suite** | dwelling_change / basement | 0 | Additional dwelling-unit / second-suite fact is explicit and is a direct permit trigger. |
| 4 | Toronto | Main-floor renovation + 3-bed/2-bath **second-storey addition** | addition | 0 | Addition is explicit. |
| 5 | Toronto | Complete bathroom renovation, 50-100 sq ft | kitchen_bath_plumbing | 1-3 | Need to know whether plumbing fixtures are merely replaced in place or added/relocated, plus structural/material changes. |
| 6 | Toronto / East York | `New installation; 3 windows` | window_door | 1-3 | `New installation` does not establish whether openings are new/enlarged/relocated vs replacement in existing same-size openings. |
| 7 | Toronto | Replacement deck, under 100 sq ft | deck_porch | 1-3 | Area alone is insufficient; height/attachment/main-access/structural scope may decide applicability. |
| 8 | Mississauga | Complete renovation of two bathrooms; bathroom stays same size | kitchen_bath_plumbing | 1-3 | Same room size does not answer whether sinks/tub/toilet/shower are added, removed or relocated. Mississauga distinguishes same-location fixture replacement from plumbing changes. |
| 9 | Mississauga | Renovate an existing basement, 500-1000 sq ft | basement | 0* | Mississauga explicitly lists finishing a basement to create rooms/living space as permit-required. `0*` assumes the HomeStars category means substantive basement finishing rather than purely cosmetic repair. |
| 10 | Mississauga | Replacement of 13 windows | window_door | 1 | Need confirmation that openings stay the same size; same-size replacement is exempt, new/enlarged openings are not. |
| 11 | Mississauga | Replacement deck, 200-300 sq ft | deck_porch | 1-3 | Mississauga uses a height threshold; public review does not state deck height. |
| 12 | Mississauga | Kitchen renovation from an `empty canvas` | kitchen_bath_plumbing / interior_renovation | 1-3 | Need wall/structural and plumbing-relocation facts. |
| 13 | Ottawa | Complete bathroom renovation, 50-100 sq ft | kitchen_bath_plumbing | 1-3 | Need whether plumbing is altered/extended vs existing fixtures simply replaced; structural changes also matter. |
| 14 | Ottawa | 1960s bathroom full renovation with **reworked plumbing** and electrical upgrades | kitchen_bath_plumbing | 0 | Ottawa explicitly requires a permit for plumbing alterations/additions/extensions except replacement of existing fixtures. |
| 15 | Ottawa | Laundry-room renovation | interior_renovation / kitchen_bath_plumbing | 1-3 | Need wall/structural and plumbing change facts. |
| 16 | Ottawa / Gloucester | Replacement deck, under 100 sq ft | deck_porch | 1-3 | Ottawa's exemption depends on height and main-entrance status, not area alone. |

### Crude input-completeness count

Under the assumptions above:

- immediate/basic decision from public text: **4 / 16 (~25%)**;
- likely resolvable after **1-3 targeted clarifications: 12 / 16 (~75%)**;
- clearly `>3/CONFIRM` from the visible scope alone: **0 / 16**, although address/property overlays could still introduce confirmation requirements later.

These percentages are **pilot-design heuristics only**. They must not be reused as market incidence, platform-wide intake completeness, model accuracy or TAM/call-volume evidence.

## Municipality-specific edge visible in ordinary scope

The most useful structural contrast is basement work:

- **Toronto:** current official guidance allows work without a building permit only when the project remains within published exemption conditions; structural/material alterations, additional dwelling units, new plumbing and related triggers matter.
- **Mississauga:** current official guidance explicitly lists basement finishing to create rooms/living space as permit-required.

Thus a generic national/provincial `basement renovation` label is not sufficient. The same family can need different municipality logic and/or different follow-up facts.

Likewise, window and bathroom scopes repeatedly show why a few binary facts matter:

- existing same-size opening vs new/enlarged/relocated opening;
- replace fixture in same location vs add/remove/relocate plumbing fixture;
- deck height/attachment/access status rather than `deck` alone.

## Product implication

The data shape supports a narrower integration hypothesis:

`existing marketplace scope + location`

→ normalize obvious facts

→ return only the **missing decisive questions** (often 1-3)

→ deterministic permit preflight

This is more realistic than assuming every marketplace lead can be sent directly to a deterministic rules engine with no clarification.

### Do not build this yet

The convenience sample is insufficient to justify a new clarification-question subsystem. A real partner/pilot should first measure:

1. 0-question resolution rate;
2. 1-3-question resolution rate;
3. residual `CONFIRM` rate;
4. median extra interaction time;
5. whether the platform/operator tolerates the friction;
6. whether the extra specificity changes enough real decisions versus a simpler guide/RAG answer.

If representative E3/E4 shows most jobs need many questions or that simple city guidance performs equally well, the thesis should be reduced/re-scoped rather than adding product complexity.

## Score implication

**No score change. Go/No-Go remains 51/100.**

This is readiness/falsification evidence, not external validation.

## HomeStars public sources sampled

- https://www.homestars.com/profile/2886365-onlybasements/reviews
- https://www.homestars.com/profile/2939367-strategic-homes-group-inc/reviews
- https://www.homestars.com/profile/3003610-david-s-quality-renovations/reviews
- https://www.homestars.com/profile/2910687-panes-window-manufacturing/reviews?page=1
- https://www.homestars.com/profile/208817-griffin-construction/reviews
- https://www.homestars.com/profile/215155-majesty-renovations/reviews
- https://www.homestars.com/profile/2946590-heptagon-for-general-contracting/reviews
- https://www.homestars.com/profile/2891018-everest-windows-and-doors-inc/reviews?page=1
- https://www.homestars.com/profile/2973074-maty-construction-inc/reviews
- https://www.homestars.com/profile/2937271-paramount-kitchen-and-bath/reviews
- https://www.homestars.com/profile/2969781-castellanos-reno-repair/reviews
- https://www.homestars.com/profile/2988091-bull-renovation/reviews
- https://www.homestars.com/profile/2987497-ottawa-general-renovation/reviews
- https://www.homestars.com/profile/yunus-construction-global-ltd/reviews?page=2

## First-party rule sources used for the input-completeness check

- Toronto: https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/
- Mississauga: https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
- Ottawa permit projects: https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/building-permit-projects
- Ottawa no-permit projects: https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits
