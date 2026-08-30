# Agent402 external discovery audit — 2026-08-30

## Purpose

Record the first independently observed x402 crawler interaction with ProjectPermit's current production discovery surfaces and classify what it does and does not prove.

This note is about distribution observability. It is **not** buyer usage evidence.

## 1. Production observation

Railway production logs for `projectpermit-api-v2` show one external source at approximately 2026-08-30 14:29:39 UTC using the Agent402 crawler identity:

- `GET /.well-known/x402` -> 200
- `GET /openapi.json` -> 200
- `GET /v1/capabilities` -> 200
- `POST /v1/preview-project-requirements` -> 422
- `POST /v1/preview-project-requirements-batch` -> 422

The first two requests used:

`Mozilla/5.0 (compatible; Agent402/1.0; +https://github.com/MikeyPetrillo/Agent402)`

The capability/preview probes came from the same source IP with a Node client user-agent.

No city-intent-page visit or successful city-demo free-preview call was observed in the same production log window.

## 2. Important correction: the 422s are not failed user invocations

Inspection of the current public Agent402 crawler source shows that its live-quote discovery logic deliberately sends an empty JSON object (`{}`) when probing POST operations. A schema-valid application request is not its goal; the crawler is trying to discover whether an endpoint exposes a payment quote/challenge.

Source:

- https://github.com/MikeyPetrillo/Agent402/blob/main/src/x402-index.js

Therefore:

> the 422 preview responses are expected discovery-probe behavior and must **not** be interpreted as a ProjectPermit user/agent workflow that tried and failed to invoke the product.

## 3. Why Agent402 probed free preview routes

Agent402's current OpenAPI normalizer recognizes `x-payment-info` as an explicit payment signal.

ProjectPermit currently decorates only:

- `POST /v1/check-project-requirements`
- `POST /v1/check-project-requirements-batch`

with `x-payment-info` and x402 payment metadata.

The free preview operations remain unannotated and are therefore normalized as `paid:false` in an OpenAPI document that contains payment annotations.

However, Agent402's current **live-quote enrichment** candidate filter is based mainly on missing price/network data and safe probe methods; it does not exclude `paid:false` rows. As a result, an unpriced free POST operation can still receive an empty-body discovery probe.

This explains the observed 422s without requiring a ProjectPermit metadata change.

## 4. Paid-route paywall probe is separate

Agent402's paywall-health function is stricter than its live-quote enrichment path. It selects only tool rows where:

`Number(t.price) > 0`

and expects exactly HTTP 402 from an unpaid call to a paid route.

ProjectPermit's paid single and batch operations already declare price through `x-payment-info`, so they qualify for a future paywall-health probe.

Agent402 rate-limits/rotates those probes rather than touching every seller each crawl. The absence of a paid-route POST in this one observed crawl therefore does **not** demonstrate a paywall failure.

## 5. ProjectPermit discovery metadata audit

### `/.well-known/x402`

ProjectPermit currently advertises only the two canonical paid resource URLs.

### OpenAPI

Only paid routes receive:

- `x-payment-info`
- ProjectPermit x402 metadata
- documented 402 response

Free previews are not marked paid.

### `/.well-known/x402-service.json`

The service manifest separately identifies:

- the paid endpoint;
- pricing/payment information;
- OpenAPI;
- the free-preview URL.

No evidence was found in this audit that the free preview is falsely advertised as a paid x402 resource.

## 6. Current Agent402 marketplace state

A fresh public Agent402 marketplace view on 2026-08-30 reported approximately:

- 2,827 sellers listed;
- 3,482 endpoints indexed;
- 88,796 advertised tool listings;
- 1,734 sellers on Base.

A text search of the accessible marketplace snapshot did **not** find ProjectPermit or the Railway API hostname.

Therefore the correct statement is:

> **Agent402 has independently discovered/crawled ProjectPermit, but current evidence does not yet prove that ProjectPermit is publicly listed, routable, paywall-health-verified or used by an external buyer.**

## 7. Evidence classification

This is a useful distribution signal because the crawler was not an owner smoke test and independently reached the machine-readable surfaces.

But it is **not E4**.

Why:

- the traffic is automated discovery/probing;
- no real project facts were sent;
- no valid result was consumed;
- no repeated end-user/platform workflow exists;
- no payment occurred.

Current state remains:

- independent discovery: **observed**;
- Agent402 listing/routability: **not yet verified**;
- city-page -> free-preview conversion: **0 observed**;
- E4: **0**;
- E5: **0**.

## 8. Decision consequence

**Do not change production discovery or request schemas based on the observed 422s.**

The current metadata already gives Agent402 the payment distinction it recognizes. A compatibility change is justified only if a later external paywall probe shows that the paid route itself fails to return a valid 402 or if Agent402 publishes a concrete indexing error attributable to our manifest/OpenAPI shape.

For now, preserve the clean distribution experiment and continue observing:

1. independent crawler rediscovery;
2. public listing/routability;
3. successful external free-preview calls;
4. real repeated workflow calls;
5. paid settlement.

Only items 3–5 move the product meaningfully toward E4/E5; automated crawling alone does not.
