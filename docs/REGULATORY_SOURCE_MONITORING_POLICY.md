# Regulatory Source Monitoring Policy

Updated: 2026-08-30

## Purpose

ProjectPermit's official-source moat is useful only if it can be maintained cheaply and conservatively. Source monitoring exists to surface possible regulatory/source changes for review. It must never silently rewrite permit rules or convert a source-fetch anomaly into a legal conclusion.

The first full read-only observability audit fetched each of the 42 current official-source manifest entries exactly once from a standard GitHub-hosted runner. The result was 25 successful fetches and 17 HTTP 403 failures: a 59.5% direct-fetch success rate. Twelve of the 25 successful responses exposed an ETag and/or Last-Modified validator.

All 17 observed failures were HTTP 403. That pattern is treated as access-path friction from the audit environment, not proof that the official source is unavailable, stale or invalid.

A second one-shot probe tested eight first-party alternate monitoring candidates for Laval and Vancouver: regulation/change indexes, a consolidated regulation PDF, Vancouver document-library surfaces and Vancouver City Clerk/council surfaces. All eight also returned HTTP 403 from the same commodity runner environment. This is sufficient evidence that, for the current product, repeatedly searching for a different first-party webpage URL is not a productive route to unattended monitoring for those two authorities.

## First audit by authority

| Authority | Sources | Direct fetch OK | Failed | HTTP validators | Monitoring tier |
| --- | ---: | ---: | ---: | ---: | --- |
| Gatineau | 7 | 7 | 0 | 0 | A — direct hash monitoring |
| Ottawa | 12 | 4 | 8 | 1 | A/B — split by source |
| Toronto | 5 | 5 | 0 | 3 | A — direct validator/hash monitoring |
| Mississauga | 5 | 5 | 0 | 4 | A — direct validator/hash monitoring |
| Laval | 5 | 0 | 5 | 0 | C — official push/manual verification |
| Longueuil | 4 | 4 | 0 | 4 | A — direct validator monitoring |
| Vancouver | 4 | 0 | 4 | 0 | C — official push/manual verification |
| **Total** | **42** | **25** | **17** | **12** | — |

Critical source IDs that failed in the canonical-source audit were:

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

### Tier B — alternate first-party machine signal

Use when a canonical guidance page blocks commodity runners but another first-party machine-readable or machine-stable surface represents the same regulatory change domain.

Useful Tier B surfaces can include:

- official change logs / "what changed" indexes;
- official PDF or consolidated by-law publication endpoints;
- first-party ArcGIS/Open Data feeds;
- official document indexes, feeds or stable publication metadata.

The alternate source is a change detector, not automatically a substitute for the canonical legal/evidence citation. If an alert is raised, review the canonical official source before updating ProjectPermit rules/evidence.

Initial Tier B scope:

- Ottawa guidance pages that returned 403 may be covered by the already-accessible official PDF/ArcGIS surfaces when those surfaces represent the same regulatory change domain.
- Do not promote Laval or Vancouver to Tier B merely because another official webpage exists. The follow-up candidate audit found 0/8 machine-readable successes across the tested first-party alternate surfaces.

### Tier C — official push plus bounded manual verification

Use when no robust first-party unattended signal is available from the standard monitoring environment.

Initial Tier C authorities:

- Laval;
- Vancouver.

For Tier C:

1. prefer official email subscriptions, public notices, change notifications or similar first-party push channels when available;
2. perform bounded manual review of the canonical official pages/documents on a reasonable cadence;
3. trigger an extra review when a customer, partner, municipality or another trustworthy signal suggests a material change;
4. keep the canonical official source as the evidence authority before changing rules.

Search engines, web caches and third-party summaries may help detect that an official page moved or that a new regulation was published. They are discovery/freshness signals only and must not become ProjectPermit's canonical evidence.

Tier C is an intentional operating choice, not an engineering defect. The product does not need 100% unattended crawling coverage to maintain trustworthy multi-jurisdiction evidence.

## Safety invariants

1. **Never auto-edit deterministic rules from a source-observation event.**
2. **Never interpret HTTP 403/429/5xx as a regulatory change.**
3. **Never replace official evidence with a search snippet or third-party summary.**
4. **Never downgrade a current rule only because a runner cannot fetch its source.**
5. A suspected material change must be reviewed against first-party content before rules, evidence fingerprints or effective dates are changed.
6. Preserve old evidence/rule identity so downstream action-bundle change detection can explain what changed.
7. Monitoring remains read-only; no municipal submission, authentication bypass, anti-bot circumvention or browser-impersonation scraping is part of the monitoring design.

## Cost decision from the audits

Selective automated regulatory monitoring is economically viable: 25/42 current canonical sources are directly observable from commodity CI, and 12 of those expose cheap HTTP validators. The correct architecture is **not** a universal crawler. It is a small per-source observation layer with Tier A automation, narrowly justified Tier B alternate first-party signals and Tier C human verification where authorities block commodity runners.

The Laval/Vancouver follow-up is also useful cost evidence: eight plausible first-party alternate surfaces were tested and all eight returned 403. Continuing to search for page-level workarounds would create brittle scraping work without increasing the regulatory moat proportionally.

This supports the ProjectPermit moat thesis because maintaining multi-jurisdiction evidence requires source-specific work, but most recurring machine cost is negligible. The principal ongoing cost is developer review when a source actually changes or when an authority changes its publication/access pattern.

## Operating cadence

Do not enable high-frequency continuous polling across all 42 sources.

Recommended initial operational cadence:

- Tier A: weekly unattended observation unless a source is known to change more frequently;
- Tier B: weekly observation of the justified alternate first-party signal;
- Tier C: bounded manual verification plus official push/event-driven review.

Before turning a recurring Tier A/B monitor on, the implementation should persist only minimal source-state metadata needed to compare observations and should alert on change without mutating rules.

## Promotion / demotion rules

Promote a source to Tier A only after repeated unattended fetch success and a stable change signal. Promote a blocked source to Tier B only when a specific first-party alternate signal is demonstrated to be both materially relevant and machine-stable. Demote a source when repeated 403/429/anti-bot behavior makes automation noisy.

A municipality is never assigned one permanent tier if its sources behave differently. Ottawa is the canonical example: 4/12 canonical sources were directly observable while 8/12 were blocked.

## Evidence status

The observability audits are maintenance-feasibility evidence. They are **not E3, E4 or E5 market evidence** and must not be counted as customer demand.
