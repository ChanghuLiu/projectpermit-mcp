# Source Freshness Stress Test — 2026-08-28

## Purpose

Test whether ProjectPermit's source-versioning / maintained-rule thesis solves a real technical problem rather than merely duplicating public municipal guidance.

This is **not** E2/E3/E4/E5 demand evidence. It is a technical falsification precursor for the remaining differentiation claim.

## Mississauga: current page vs older official PDF

A particularly useful conflict exists inside the City of Mississauga's own currently accessible public materials.

### Current City webpage

The current `When a building permit is required` page lists, among other examples:

- finishing a basement to create rooms or living space — permit required;
- plumbing fixtures added, removed or relocated — permit required;
- same-location plumbing fixture replacement — no permit;
- shed greater than 15 m², or any size with plumbing — permit required;
- qualifying shed less than 15 m² — no permit;
- same-size replacement windows/doors — no permit;
- new/enlarged window or door opening — permit required.

Source:

- https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/

### Older City residential permit guide still online

An older City PDF still accessible publicly contains materially different guidance, including:

- non-load-bearing basement wall / basement finishing with no plumbing or HVAC listed under work not requiring a building permit;
- detached accessory structure exemption described using a 10 m² threshold rather than the newer qualifying-shed 15 m² threshold.

Source:

- https://www.mississauga.ca/file/COM/Residential_Building_Permit_Guide_PDF.pdf

## Why this matters

This is direct evidence that **first-party sources themselves can be stale and contradictory across versions**.

A generic web-search/RAG implementation can retrieve an official City document and still produce the wrong current answer if it does not distinguish source currency and supersession.

This is especially relevant to PermitSnapshot-style broad AI approaches because PermitSnapshot's own disclaimer says reports may rely on general Ontario regulatory context, may not reflect the most current municipal by-law, and may contain outdated information.

This does **not** prove PermitSnapshot's paid reports are wrong. It demonstrates the technical failure mode ProjectPermit is trying to control.

## ProjectPermit differentiation hypothesis strengthened technically

The surviving technical hypothesis is now narrower:

> A maintained rule layer with explicit current source selection, source-version tracking, stable rule IDs and deterministic inputs can avoid stale-but-official guidance errors that broad web/RAG systems are exposed to.

This should be tested explicitly in E3.

## E3 stress-test requirement

For representative historical cases, record not only agreement/disagreement but also:

1. which municipal source/version supports the historical outcome;
2. whether a stale official source would have changed a generic/RAG answer;
3. whether ProjectPermit's current rule/source manifest selects the current authoritative boundary;
4. whether this difference mattered operationally (quote, scope, delay, research time, inspection, change order).

Cases involving changed thresholds or changed municipal guidance are especially valuable, but the sample must remain representative rather than cherry-picked.

## Score effect

**No score increase.**

Reason:

- this supports technical differentiation;
- it does not establish buyer willingness to pay for source freshness;
- it does not establish frequency of stale-source failures in real workflows;
- it is not an independent representative benchmark.

Go/No-Go remains **50/100 — validation/falsification only**.