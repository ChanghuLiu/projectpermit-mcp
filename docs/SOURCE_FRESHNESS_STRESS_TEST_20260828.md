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

## ProjectPermit self-audit

The current ProjectPermit implementation was checked against this exact Mississauga conflict rather than assuming its own source handling is correct.

Current repository state:

- `data/source_manifest.json` has `manifest_version: 1` and `verified_at: 2026-08-26`;
- `MIS_GENERAL` points to the current City of Mississauga `When a building permit is required` webpage, **not** the older residential guide PDF;
- `src/projectpermit/expansion_rules.py` identifies the ruleset as `RULE_VERSION = 2026-08-26.1` and `SOURCE_VERIFIED_AT = 2026-08-26`;
- Mississauga rule `MIS-BASE-001` deterministically returns `REQUIRED` for `finish_basement`, with the reason that Mississauga explicitly lists finishing a basement to create rooms/living space as permit-required work;
- the older 10 m² / basement-finishing guidance is not the cited source for that current rule.

So the demonstrated stale-source failure mode is **not currently present in ProjectPermit's Mississauga basement rule**.

## Existing source-change detector

`src/projectpermit/source_watch.py` already implements a low-cost source-change detector:

1. fetch each URL in the source manifest;
2. normalize HTML/text whitespace while retaining PDF bytes;
3. compute SHA-256 content digests;
4. compare them with the prior stored source state;
5. emit `CONTENT_CHANGED` when a known source hash changes;
6. emit `FETCH_FAILED` when an official source can no longer be fetched.

The module intentionally does **not** auto-edit legal/regulatory rules. A source change creates a review signal; a human/developer must decide whether the rule or its golden cases actually need revision.

That is the correct safety model for a deterministic regulatory ruleset.

## Operationalization gap

The current repository audit also found an important limitation:

- no committed `data/source_state.json` baseline is currently visible;
- no scheduled GitHub Actions workflow for `source_watch.py` is currently visible.

Therefore the accurate claim today is:

> **ProjectPermit has a source-change detection mechanism, but continuous/scheduled source monitoring is not yet operationalized.**

Do **not** describe the project as already continuously monitoring municipal changes.

This distinction matters because the commercial differentiation thesis depends on maintained freshness, not merely having code capable of detecting changes when someone runs it.

## ProjectPermit differentiation hypothesis strengthened technically

The surviving technical hypothesis is now narrower:

> A maintained rule layer with explicit current source selection, source-version tracking, stable rule IDs and deterministic inputs can avoid stale-but-official guidance errors that broad web/RAG systems are exposed to.

The current Mississauga self-audit shows the architecture can encode the correct present source boundary. It does **not** yet prove that buyers value this enough to pay for it or that the monitoring process will remain operationally cheap at scale.

This should be tested explicitly in E3.

## E3 stress-test requirement

For representative historical cases, record not only agreement/disagreement but also:

1. which municipal source/version supports the historical outcome;
2. whether a stale official source would have changed a generic/RAG answer;
3. whether ProjectPermit's current rule/source manifest selects the current authoritative boundary;
4. whether this difference mattered operationally (quote, scope, delay, research time, inspection, change order).

Cases involving changed thresholds or changed municipal guidance are especially valuable, but the sample must remain representative rather than cherry-picked.

## Do not operationalize monitoring merely to stay busy

At the current Go/No-Go score, adding a scheduled source-watch workflow would be easy engineering but weak commercial learning.

Do **not** build it merely to make the product look more complete.

Operationalize scheduled monitoring only if one of these becomes true:

- an E2+/E3 partner explicitly values maintained/source-versioned rules;
- a real E4 pilot needs source-freshness assurance;
- source-update burden becomes a measured part of build-vs-buy economics;
- ProjectPermit continues past the current stop/re-scope gate.

## Score effect

**No score increase.**

Reason:

- this supports technical differentiation;
- it does not establish buyer willingness to pay for source freshness;
- it does not establish frequency of stale-source failures in real workflows;
- continuous monitoring is not yet operationalized;
- it is not an independent representative benchmark.

Go/No-Go remains **50/100 — validation/falsification only**.