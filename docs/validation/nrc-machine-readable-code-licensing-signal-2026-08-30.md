# NRC machine-readable code licensing signal — 2026-08-30

## Purpose

Record a new official Canadian source-rights/product-infrastructure signal relevant to ProjectPermit Layer C.

This note is **not legal advice, not a licence, and not authorization to ingest or commercially redistribute NRC code content**.

## Official 2026 NRC / ISED signal

In the 2026 Innovative Solutions Canada challenge for deterministic AI-assisted building-permit compliance checking, NRC describes an active construction-code digitalization program.

Official source:

- https://ised-isde.canada.ca/site/innovative-solutions-canada/en/deterministic-artificial-intelligence-assisted-compliance-checking-building-permit-applications

The challenge requires or encourages compatibility with machine-readable construction-code formats including:

- XML / DITA;
- JSON / JSON-LD;
- RDF / TTL / knowledge-graph forms;
- RASE and other semantic/logical annotations;
- mappings to BIM / IFC information structures.

The FAQ further says NRC is working with DITA/XML for managing code changes and creating multiple output formats including the existing PDF plus new HTML, JSON, RDF/TTL and JSON-LD outputs.

NRC also says funded projects may receive one or more machine-readable formats of the National Codes and associated schemas/API information for prototype integration.

## Commercial-use answer

The most important current official statement is NRC's answer to questions about using National Building Code content in future commercial products.

NRC states that:

> the licensing and distribution model for new digitalized Code format(s) is under development.

In a related answer NRC states that it is updating the licensing and distribution approach for commercial use of machine-readable codes.

This is materially different from assuming that the only future commercial route is ad-hoc permission to reproduce a free PDF.

## What this does prove

The official signal supports the following conclusions:

1. NRC is actively converting National Code content into machine-oriented formats, not merely publishing PDFs.
2. NRC expects software systems to query/use digitalized code content in deterministic compliance workflows.
3. NRC explicitly contemplates APIs/data pipelines between code databases and software systems.
4. NRC explicitly recognizes **commercial use of machine-readable codes** as a licensing/distribution problem it is currently updating.
5. Therefore a future official machine-readable commercial distribution/licensing channel is a credible possibility.

## What this does NOT prove

It does **not** establish:

- that ProjectPermit currently has any commercial reuse right;
- that the future licence will be cheap;
- that licences will be available to every software vendor;
- that commercial redistribution of code text, rules or derived facts will be unrestricted;
- that there will be a public API;
- that licence terms will support x402/per-call resale;
- any publication date for final commercial licensing terms.

Until actual terms are obtained, NRC technical-code content remains behind a rights gate.

## Layer C licensing classification change

Previous shorthand:

`NRC National Codes = protected content / written consent required`

More precise current model:

`NRC National Codes = protected content today + official machine-readable commercial licensing/distribution pathway under development`

This is a **risk-profile improvement**, not clearance.

## Product architecture implication

If Layer C later crosses E2/E3, ProjectPermit should be able to ingest an authoritative licensed machine-readable feed rather than relying on scraped PDFs.

The existing conceptual architecture already aligns unusually well with NRC's stated direction:

- deterministic result categories;
- explicit missing/uncertain states;
- provision/source traceability;
- evidence freshness/versioning;
- change identity;
- open API/workflow integration;
- human-in-the-loop gating.

That architectural alignment is strategic evidence only. It is not buyer demand.

## Cash discipline

No spending change:

- spend $0 on NRC/code-content licences while Layer C remains E1-only;
- do not build a protected-code corpus from PDFs merely because digital formats are coming;
- first prove buyer denominator + material workflow consequence;
- if buyer evidence crosses the gate, request the then-current NRC commercial machine-readable licensing/distribution terms;
- model licence/minimum/implementation cost against real addressable workflows before committing.

## Evidence score

No E-level increase.

This is **licensing feasibility / infrastructure-direction evidence**, not buyer usage, integration commitment or payment.

## Current decision

Continue Layer C validation with the following updated licensing gate:

> buyer denominator -> material quote/scope/schedule consequence -> representative low-risk E3 if justified -> obtain current NRC machine-readable commercial licensing terms -> licence economics -> protected-code integration only if economically viable.
