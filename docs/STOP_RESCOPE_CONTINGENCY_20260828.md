# Stop / Re-Scope Contingency — 2026-08-28

## Purpose

ProjectPermit is currently at **50/100**. The project is no longer in normal build mode; it is in validation/falsification mode.

This document defines what happens if the next materially negative qualified signal moves the thesis below the stop line. The goal is to avoid sunk-cost reactions such as adding municipalities, features or integrations merely to preserve the original idea.

## Trigger

Enter **STOP / RE-SCOPE** when a qualified signal shows one of the following:

- a Canadian supplier already offers the target pre-application applicability capability through an acceptable API/batch/white-label path;
- representative software buyers say local permit logic is cheap/easy enough to maintain internally and an external deterministic API adds little value;
- representative E3 cases show no material practical advantage from municipality-specific deterministic rules/source freshness;
- a relevant high-volume upstream platform reports that permit applicability is already resolved on almost all candidate jobs;
- no >=500/month unresolved current-family workflow can be established after qualified platform conversations;
- E5 remains zero after real E3/E4 buyer engagement.

A generic competitor page, an automated email or an unbounded opinion does not by itself trigger the stop.

## What stops immediately

If the trigger fires, freeze these activities:

1. new municipality coverage;
2. new project families;
3. zoning/grant/fee/property-feasibility expansion;
4. permit filing/document review/inspection workflow;
5. additional field-service adapters;
6. paid marketplace certification/listing work;
7. x402 commercialization work beyond preserving the already-working plumbing;
8. source-monitoring infrastructure expansion unless needed to preserve a reusable asset;
9. broad outbound campaigns for the unchanged standalone API thesis.

No `one more feature` exception.

## Assets worth preserving

A No-Go on the standalone API thesis does **not** mean the existing work has zero value.

Preserve:

- normalized 8-family project-fact schema;
- 7-jurisdiction rule corpus;
- 155 stable rule IDs;
- official-source manifest and source-version metadata;
- conservative unknown / overlay handling;
- deterministic engine and regression tests;
- address/GIS adapters already built;
- source-change detector;
- E3 benchmark tooling and de-identified case templates;
- read-only Jobber and ServiceM8 normalization experience;
- REST/MCP contract and proven payment plumbing as reusable infrastructure.

These are reusable technical assets, not evidence that ProjectPermit itself should continue.

## Re-scope paths — ranked by evidence required

### A. Embedded internal component for an existing buyer

Use the deterministic engine as a private component inside a contractor/quote/marketplace product **only if a buyer explicitly asks for it**.

Why this survives:

- avoids needing a standalone category/brand;
- buyer supplies distribution;
- municipality coverage can be narrowed to the buyer's real footprint;
- pricing can be bundled into a larger workflow rather than justified per preflight call.

Required evidence before work:

- named buyer;
- real workflow point;
- expected monthly candidate volume;
- requested output/accuracy boundary;
- willingness to run E3/E4 pilot.

Do not build this speculatively.

### B. Regulatory-source freshness / rule QA service

Potentially preserve source manifest, versioning, rule IDs and change review as a narrower infrastructure capability.

This path is valid only if a software or regulatory-data buyer says stale/conflicting official guidance is a material maintenance problem.

Current Mississauga current-page vs older-official-PDF conflict proves the technical failure mode exists. It does **not** prove a market for a standalone freshness service.

Required evidence:

- buyer currently maintains multiple municipalities;
- source drift causes measurable manual work/error risk;
- buyer prefers external monitoring/QA rather than owning it;
- recurring maintenance value supports payment.

### C. Deterministic benchmark / QA layer for AI permit products

PermitSnapshot-style broad AI feasibility products may need an external benchmark for ordinary scope applicability and stale-source regressions.

This is only a plausible re-scope if an AI permit vendor, marketplace or insurer asks for independent deterministic validation.

Required evidence:

- vendor willing to supply representative historical outputs/cases;
- measurable false-positive/false-negative or source-freshness problem;
- paid QA/benchmark need.

Do not assume competitors want to buy from a potential competitor.

### D. Open/reference corpus

If no commercial buyer emerges but the technical work remains useful, the rule/evidence corpus can be preserved as a reference/open-source asset rather than receiving further commercial investment.

This is a terminal preservation path, not a growth thesis.

## Paths explicitly rejected without new evidence

Do not pivot automatically into:

- homeowner permit app;
- broad property feasibility report competing with PermitSnapshot/LandLogic;
- permit-history API competing with established data vendors;
- municipal application portal;
- U.S. permit filing platform competing with PermitFlow/Permitio;
- generic contractor CRM/estimating software;
- legal/compliance advisory service requiring human experts.

Those are new businesses and require fresh opportunity evaluation rather than being called a ProjectPermit pivot.

## Re-scope decision matrix

| New evidence | Action |
|---|---|
| Exact Canadian API supplier already solves it cheaply | Stop standalone API; evaluate only buyer-specific embedded/QA reuse |
| Buyers prefer internal local rules | Stop standalone API; test source-freshness/QA only if they identify maintenance pain |
| E3 accuracy advantage is material | Keep engine asset; pursue E4 pilot before any expansion |
| >=500/mo unresolved workflow + buyer wants pilot | Continue narrow ProjectPermit; build only buyer-required integration |
| E4 succeeds but E5 fails | Re-evaluate pricing/bundling; do not expand coverage |
| No E2/E3/E4 traction | Archive commercial thesis; preserve code/data assets |

## Decision discipline

At the stop line, the correct objective is not to save ProjectPermit.

The objective is to determine whether the existing assets have a **buyer-backed narrower use**. If no such use appears, archive the commercial thesis and move attention to a better opportunity.