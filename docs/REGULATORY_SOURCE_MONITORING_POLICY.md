# Regulatory Source Monitoring Policy

Updated: 2026-08-30

## Purpose

ProjectPermit's official-source moat is useful only if it can be maintained cheaply and conservatively. Source monitoring exists to surface possible regulatory/source changes for review. It must never silently rewrite permit rules or convert a source-fetch anomaly into a legal conclusion.

The first full read-only observability audit fetched each of the 42 current official-source manifest entries exactly once from a standard GitHub-hosted runner. The result was 25 successful fetches and 17 HTTP 403 failures: a 59.5% direct-fetch success rate. Twelve of the 25 successful responses exposed an ETag and/or Last-Modified validator.

All 17 observed failures were HTTP 403. That pattern is treated as access-path friction from the audit environment, not proof that the official source is unavailable, stale or invalid.

## First audit by authority

| Authority | Sources | Direct fetch OK | Failed | HTTP validators | Initial monitoring tier |
| --- | ---: | ---: | ---: | ---: | --- |
| Gatineau | 7 | 7 | 0 | 0 | A — direct hash monitoring |
| Ottawa | 12 | 4 | 8 | 1 | A/B — split by source |
| Toronto | 5 | 5 | 0 | 3 | A — direct validator/hash monitoring |
| Mississauga | 5 | 5 | 0 | 4 | A — direct validator/hash monitoring |
| Laval | 5 | 0 | 5 | 0 | B — alternate official access path |
| Longueuil | 4 | 4 | 0 | 4 | A — direct validator monitoring |
| Vancouver | 4 | 0 | 4 | 0 | B — alternate official access path/change index |
| **Total** | **42** | **25** | **17** | **12** | — |

Critical source IDs that failed in the first runner audit were:

- Ottawa: `OTT_GENERAL`, `OTT_EXEMPT`, `OTT_ZONING_2026`, `OTT_ZONING_APPEALS`
- Laval: `LAV_EXT`, `LAV_INT`
- Vancouver: `VAN_WHEN`, `VAN_RENO`, `VAN_VBBL_2025`

A critical-source 403 is a monitoring-path problem. It does not itself degrade or invalidate the currently committed evidence unless the canonical source can no longer be independently verified.

## Monitoring tiers

### Tier A — direct machine observation

Use for official sources that a standard runner can fetch reliably.

Preferred signal order:

1. ETag / Last-Modified when present;
2. normalized content hash;
3. final URL / redirect change;
4. content type or abnormal response-size change as a supporting anomaly only.

A detected change creates a review event. It does not change rules automatically.

Initial Tier A authorities/surfaces:

- Gatineau — direct content-hash observation;
- Toronto — validator plus hash;
- Mississauga — validator plus hash;
- Longueuil — validator plus hash;
- Ottawa — only the individual official/PDF/ArcGIS surfaces that passed the audit; do not treat the authority as wholly Tier A.

### Tier B — alternate official access path

Use when the canonical guidance page blocks commodity runners or is otherwise unsuitable for unattended GETs.

Look first for another first-party surface that represents the same regulatory change domain, such as:

- official change logs / "what changed" indexes;
- official PDF or consolidated by-law publication endpoints;
- first-party ArcGIS/Open Data feeds;
- official document indexes, feeds or stable publication metadata.

The alternate source is a change detector, not automatically a substitute for the canonical legal/evidence citation. If an alert is raised, review the canonical official source before updating ProjectPermit rules/evidence.

Initial Tier B areas:

- Ottawa guidance pages that returned 403 from the GitHub runner;
- Laval guidance pages;
- Vancouver guidance/VBBL surfaces. Vancouver's official change-index/document surfaces should be preferred for unattended monitoring when they cover the same change domain.

### Tier C — manual verification fallback

Use when no robust first-party automated signal exists. Review through an ordinary browser or another legitimate first-party access route on a bounded cadence or when another signal suggests change.

Search engines, web caches and third-party summaries may help detect that an official page moved or that a new regulation was published. They are discovery/freshness signals only and must not become ProjectPermit's canonical evidence.

## Safety invariants

1. **Never auto-edit deterministic rules from a source-observation event.**
2. **Never interpret HTTP 403/429/5xx as a regulatory change.**
3. **Never replace official evidence with a search snippet or third-party summary.**
4. **Never downgrade a current rule only because a runner cannot fetch its source.**
5. A suspected material change must be reviewed against first-party content before rules, evidence fingerprints or effective dates are changed.
6. Preserve old evidence/rule identity so downstream action-bundle change detection can explain what changed.
7. Monitoring remains read-only; no municipal submission, authentication bypass or anti-bot circumvention is part of the monitoring design.

## Cost decision from the first audit

Selective automated regulatory monitoring is economically viable: 25/42 current sources are directly observable from commodity CI, and 12 of those expose cheap HTTP validators. The correct architecture is **not** a universal crawler. It is a small per-source observation layer with Tier A automation and Tier B/C fallbacks.

This supports the ProjectPermit moat thesis because maintaining multi-jurisdiction evidence requires source-specific work, but most of the recurring machine cost is negligible. The main cost is developer review when a source actually changes or when an authority changes its publication/access pattern.

## Operating cadence

Do not enable high-frequency continuous polling across all 42 sources.

Recommended initial operational cadence after the one-shot audit phase:

- Tier A: weekly unattended observation is sufficient for the current preflight product unless a source is known to change more frequently;
- Tier B: weekly alternate-official-source observation where a trustworthy first-party anchor is identified;
- Tier C: bounded manual review, plus event-driven review when customers, partners, municipalities or Tier A/B signals indicate change.

Before turning a recurring monitor on, the implementation should persist only minimal source-state metadata needed to compare observations and should alert on change without mutating rules.

## Promotion / demotion rules

Promote a source to Tier A only after repeated unattended fetch success and a stable change signal. Demote or split a source when repeated 403/429/anti-bot behavior makes automation noisy.

A municipality is never assigned one permanent tier if its sources behave differently. Ottawa's first audit is the canonical example: 4/12 sources were directly observable while 8/12 were blocked.

## Evidence status

The observability audit is maintenance-feasibility evidence. It is **not E3, E4 or E5 market evidence** and must not be counted as customer demand.
