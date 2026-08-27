# ProjectPermit Workflow Pain Evidence

Updated: 2026-08-27

This document separates **observed evidence** from assumptions. Community anecdotes are useful for discovering pain and workflow language, but they are not market-size statistics.

## Strongest observed signals

### 0. CHBA Spring 2026 renovator panel: permit processes are a measurable pre-renovation cost

The Canadian Home Builders' Association Spring 2026 Renovation Market Index is based on a panel of renovation-focused member businesses. CHBA explicitly describes **pre-renovation processes and delays as a hard-to-quantify cost to renovators** and reports average building-permit application-to-approval time of about **9 weeks in Ontario** and **18 weeks in British Columbia**. Renovator comments indicated that timelines have gradually lengthened.

Source: https://www.chba.ca/rmi/

Why this matters:

- this is current industry-panel evidence rather than a single anecdote;
- it confirms that municipal permitting/regulatory process is materially present in professional renovation workflows in two of ProjectPermit's key provinces;
- long downstream lead time increases the value of discovering permit/planning obligations early enough to account for them in quoting and scheduling.

Critical boundary:

- the published RMI statistic measures **application-to-approval delay**, not time spent deciding whether a permit is required;
- it does not publish the share of renovation scopes that need a permit, the share where applicability is initially uncertain, or how often a permit decision changes a quote/scope/schedule;
- therefore it supports pain intensity but **must not be converted into ProjectPermit call-volume/TAM or E3/E4 evidence**.

An evidence request was sent to the CHBA RMI team asking whether aggregate data exists for the missing upstream measures.

### 1. ServiceTitan + iPermit: one contractor reports 80+ permit jobs/month

ServiceTitan's public iPermit Marketplace listing includes a contractor testimonial stating that the company sends about **80 or more jobs per month** to iPermit across residential change-outs, light commercial and other work.

Source: https://marketplace.servicetitan.com/partner/ipermit

Why this matters:

- it proves permit work can be a repeated monthly operational stream rather than a rare one-off task;
- 80 jobs/month from one contractor is already enough volume for an automated decision step to matter operationally;
- it does **not** prove every ServiceTitan contractor has this volume or that every job needs a ProjectPermit preflight.

ProjectPermit question to validate:

> Before a job enters iPermit's full expediting/submission process, is there a repeated manual decision about whether the scope needs a permit at all?

### 2. HVAC contractor: jurisdiction differences create permit uncertainty

A public r/HVAC thread describes a contractor operating across municipalities where straight replacements are treated differently. The poster says a customer may require permits for potentially **dozens of installations per week** and worries that the logistics could require a dedicated position.

Source: https://www.reddit.com/r/HVAC/comments/11lm0q9/permits/

Why this matters:

- the pain is not merely permit submission; it begins with inconsistent municipality rules;
- `same-size replacement` versus `new/relocated equipment` is exactly the type of normalized scope distinction ProjectPermit can encode;
- the stated cadence suggests a repeated API decision can be more valuable than a consumer lookup page.

Caution: this is one contractor anecdote, not a frequency benchmark.

### 3. HVAC contractor: multi-department permitting adds weeks

A 2025 r/HVAC thread from Northern California reports permit timelines of several weeks for heat pumps, generators and equipment replacements, with some projects requiring both planning and building review and substantial application packages.

Source: https://www.reddit.com/r/HVAC/comments/1koioki/permits_are_a_nightmare_now/

Why this matters:

- the downstream permit process is expensive enough that early routing has value;
- ProjectPermit should not try to reproduce the 10-15 page submission package or plan review;
- the wedge is to identify which workflow needs deeper permitting/planning work before the expensive process starts.

### 4. Procore users still report permit tracking outside the core workflow

A 2026 r/ConstructionMNGT discussion explicitly asks whether permit tracking inside Procore is adequate and whether teams still rely on spreadsheets/email/calendars. A reply says Procore handles the permit-tracking problem poorly.

Source: https://www.reddit.com/r/ConstructionMNGT/comments/1ttftl8/does_procore_actually_handle_permit_tracking_well/

Another construction-management thread describes manually tracking multiple permit review cycles and missing follow-up dates when cities do not respond on time.

Source: https://www.reddit.com/r/ConstructionManagers/comments/1c6rgfg/issues_managing_multiple_permits_advice_thoughts/

Why this matters:

- it validates that permit workflow remains fragmented even in mature construction software ecosystems;
- however, these comments are mostly about **tracking after a permit process begins**, while ProjectPermit is an **upstream requirements/preflight** service;
- this is evidence for integrations with downstream platforms, not evidence that ProjectPermit should become a permit tracker.

## Product-boundary implication

Observed pain appears at multiple layers:

1. **Do I need a permit / which authority or overlay matters?** — ProjectPermit's target layer.
2. What documents, drawings, fees and calculations are required?
3. Prepare and submit the package.
4. Track reviews, corrections, inspections and approvals.

PermitFlow, Pulley, iPermit and similar systems primarily address layers 2-4. ProjectPermit should remain optimized for layer 1 unless external design partners repeatedly ask for adjacent machine-readable requirements.

## Pain-strength assessment

| Pain signal | Strength | Repeated-call potential | ProjectPermit fit |
|---|---|---|---|
| Municipality-specific replacement/new-install rules | High | High for multi-jurisdiction contractors | Very high |
| Deciding whether a work order should enter permitting | High if frequent | High in field-service/property portfolios | Very high |
| Full permit package preparation | High | Repeated | Low — crowded/human-heavy |
| Permit status tracking/corrections | High | Repeated | Low-medium — strong existing products |
| One-off homeowner permit question | Medium | Low | Low commercial priority |

## What still must be proven externally

The evidence above is sufficient to justify conversations, but not to prove a business. We still need measured answers to:

- permit-decision events per customer/month;
- percentage of work orders/jobs where this decision is not already known;
- municipalities that dominate real volume;
- address-aware preflight share;
- whether official evidence reduces enough risk/time to justify payment;
- whether `$0.20-$0.50` per address-aware call is acceptable;
- whether one integration can realistically produce 1k, 10k or 100k monthly calls.

Until those are measured, industry-panel delay evidence and community anecdotes should not be converted into ProjectPermit TAM claims.
