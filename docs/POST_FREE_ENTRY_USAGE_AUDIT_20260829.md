# Post-Free-Entry External Usage Audit — 2026-08-29

## Purpose

PR #60 made the existing free HTTP validation path unambiguous on the first screen of the public README and fixed stale static MCP coverage metadata. This audit checks whether that lower-friction public entry translated into any real external preflight usage.

Observation window begins at approximately **2026-08-28 21:57Z**, immediately after the public-entry change deployed, and runs through the 2026-08-29 morning review.

This is a short observation window. It is useful as a falsification datapoint, not as a statistically mature distribution experiment.

## Structured telemetry result

All successful preflights emit the same privacy-minimal `PROJECTPERMIT_USAGE` event before returning a result. Internal CI/owner smoke traffic is tagged separately.

During the observation window:

- free HTTP preview successful external preflights: **0**;
- standard MCP successful external preflights: **0**;
- paid MCP successful external preflights: **0**;
- successful preflights with `internal_traffic=false`: **0**.

The only successful HTTP-preview and standard-MCP determinations in the reviewed deployment logs were the known post-deploy/internal validation calls.

Therefore:

> **E4 remains 0.**

## HTTP proxy context

The API proxy did receive external/non-CI traffic, but it did not become a successful preflight workflow.

Observed examples include:

- one external `GET /v1/preview-project-requirements` returning **405**;
- search/crawler-style requests such as `robots.txt` and GETs against the paid resource;
- a `node` client repeatedly POSTing to `/v1/check-project-requirements` and receiving **402** payment challenges, plus GETs returning 405.

These events demonstrate discovery/contact with the public surfaces. They do **not** demonstrate a permit determination, repeated workflow, payment, or integration.

The single GET to the free preview path is ambiguous: it could be a human/browser click or another crawler/probe. It must not be upgraded to E4.

## Why this audit matters

Before PR #60 it was plausible that a developer might see the repository and encounter the paid HTTP route before discovering the free preview.

After PR #60:

- the no-account/no-key/no-wallet HTTP preview is visible on the README first screen;
- the standard MCP developer preview is also explicitly free;
- the paid route is clearly separated;
- live MCP descriptions already state the pre-quote permit-applicability use case;
- successful anonymous preview calls are observable as external telemetry.

The continued absence of external successful preflight usage therefore cannot be explained primarily by a hidden free route or broken external-usage instrumentation.

## Decision impact

**No score change today.**

Canonical state remains **48/100 — PAUSE / RE-SCOPE**.

The window is too short to reduce distribution fit again. However, this is a stronger falsification datapoint against passive Registry/Bazaar/GitHub discovery as a meaningful distribution channel.

Future external probes, GETs, 402 challenges, capability checks or MCP initialization requests still do not count as E4. Only successful non-owner permit determinations used in a real or repeated external workflow should advance E4.

No further README/discovery-copy optimization should be used as a substitute for buyer/workflow evidence.