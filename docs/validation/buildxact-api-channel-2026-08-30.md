# Buildxact API channel evidence — 2026-08-30

## Purpose

Correct the prior assumption that Buildxact is only a vendor-partnership target and evaluate it as a potential ProjectPermit distribution/buyer channel.

This is distribution/readiness evidence only. It does **not** justify contacting Buildxact, registering an application or implementing an adapter before the Layer-C buyer gate crosses E2.

## 1. Buildxact now has a public developer API surface

Buildxact's April 30, 2026 help documentation points developers to a dedicated public developer portal.

Official sources:

- https://help.buildxact.com/en/articles/4510284-buildxact-application-programming-interface-api
- https://developer.buildxact.com/
- https://developer.buildxact.com/getting-started

The current API catalogue includes:

- Accounts;
- Catalogues;
- Clients;
- Contacts;
- Estimates;
- Jobs;
- Leads;
- Metadata.

Official source:

- https://developer.buildxact.com/apis

This materially lowers ProjectPermit's integration-risk estimate because Buildxact is no longer a closed/no-API platform.

## 2. Third-party SaaS integrations are explicitly supported

Buildxact documents two auth modes:

1. first-party customer access;
2. third-party SaaS access where Buildxact users connect their accounts to another platform.

For a third-party app, the developer must first contact Buildxact support and request registration. Buildxact then issues a client id/secret and supports delegated OAuth consent.

Applications registered after 2026-07-14 use stricter OAuth 2.1-style security with mandatory PKCE and restricted grants/scopes.

Official source:

- https://developer.buildxact.com/authorization

Interpretation:

- there is still a vendor approval dependency;
- but the technical/distribution route is formal, documented and designed for third-party SaaS;
- ProjectPermit would not need to reverse-engineer Buildxact or ask contractors to share permanent credentials.

## 3. Staging and operational API infrastructure exist

Buildxact documents:

- a staging/UAT developer environment;
- separate staging subscription keys;
- a staging Buildxact UI for development;
- OData filtering/sorting/paging;
- an API rate limit of 100 requests per 30 seconds;
- webhooks.

Official source:

- https://developer.buildxact.com/getting-started

This is sufficient platform infrastructure for a normal small SaaS integration if commercial/buyer evidence later justifies one.

## 4. Estimate workflow is unusually well matched to Layer C

Buildxact's customer/product positioning is specifically builders/remodelers and preconstruction/estimating.

Public claims include:

- builders and remodelers as core customers;
- digital takeoffs;
- estimating/quoting;
- preconstruction RFQs;
- estimate -> project management/schedule/cost tracking;
- quotes produced much faster than manual workflows.

Official sources:

- https://www.buildxact.com/ca/our-customers/builders-remodelers/
- https://www.buildxact.com/ca/features/builder-remodeler/preconstruction/
- https://www.buildxact.com/ca/features/builder-remodeler/

This aligns more directly with ProjectPermit's current normalized families than a broad field-service platform dominated by recurring maintenance/repair work.

Current ProjectPermit families are concentrated around renovation/construction activities such as:

- window/door work;
- interior renovation;
- basements;
- dwelling changes;
- decks/porches;
- accessory structures;
- additions;
- kitchen/bath plumbing.

Therefore Buildxact is a high-fit **quote-stage** platform, not merely a large generic contractor denominator.

## 5. Estimate data is commercially meaningful

Buildxact publicly documents detailed Estimate and Estimate Item data including quote totals, costs, markup and tax-calculated values.

Official source:

- https://developer.buildxact.com/estimate-data

Existing public company statistics separately report nearly one million historical quotes and very high cumulative quoted value.

This supports a useful workflow hypothesis:

> a regulatory result inserted before quote lock can affect an already-monetized estimate/cost structure rather than producing a disconnected compliance memo.

This remains a hypothesis until a real Buildxact/builder buyer confirms the consequence.

## 6. Webhook path exists, but should not be the first pilot mode

Buildxact documents standard webhooks including `Estimate Accepted`, Lead events and other tenant events.

Official source:

- https://developer.buildxact.com/webhooks

ProjectPermit should **not** start with an automatic webhook-based compliance engine.

For a first representative pilot, an explicit user-triggered check is safer because:

- requirement decisions may need missing facts;
- running only after estimate acceptance may be too late to change the quote;
- automatic events create noisy calls before denominator/value is proven;
- human confirmation fits ProjectPermit's current conservative workflow architecture.

If later usage shows repeated pre-quote checks, webhook/automation can be added around known lifecycle events.

## 7. Remaining technical unknowns

The public pages inspected establish API coverage for Estimates/Jobs/Clients and estimate-item data, but this pass did not yet confirm from a static endpoint schema exactly where every ProjectPermit input is located, especially:

- project/site civic address;
- free-text scope fields;
- all estimate item descriptions/categories;
- user-defined project metadata.

This is an adapter-level unknown, not a strategic blocker. It should be resolved only after E2 before implementation.

## 8. Revised platform ranking

### High-fit / executable after E2

**Jobber**

- explicit General Contractor + Remodeling segments;
- large business denominator;
- private/draft small-account integration route;
- current ProjectPermit adapter already exists.

**Buildxact**

- strongest direct builder/remodeler/preconstruction fit among the newly researched platforms;
- official Estimates/Jobs/Leads/Clients API;
- third-party OAuth is supported;
- staging/webhooks exist;
- requires Buildxact registration/approval before third-party OAuth use.

### Low-friction secondary validation channel

**ServiceM8**

- easiest embedded Job Action pattern;
- private install before public Store approval;
- recurring billing infrastructure;
- current adapter exists;
- but public Canadian customer denominator is not disclosed and many users/jobs are field-service/maintenance rather than current ProjectPermit family fit.

### Higher-friction strategic vendor route

**Buildertrend**

- very strong builder/remodeler workflow fit;
- marketplace/integration precedent;
- no comparable self-serve public developer portal confirmed in current official search.

## 9. Build gate

Do not contact Buildxact to register ProjectPermit yet.

A vendor integration approval request should follow, not precede, evidence that:

1. builders/remodelers repeatedly need the current regulatory result during estimating/preconstruction;
2. the result materially changes quote scope/cost/schedule/professional/document/inspection handling;
3. maintained jurisdiction data is preferred over internal/manual research;
4. expected bounded usage justifies integration/support work.

## Evidence impact

No E-level increase.

What changed:

- Buildxact integration feasibility: **materially stronger**;
- Buildxact current-family workflow fit: **high**;
- Buildxact buyer demand for ProjectPermit: **unproven**;
- vendor approval remains a dependency;
- E4 = 0;
- E5 = 0.
