# Ontario Layer C source-rights boundary — 2026-08-30

## Purpose

Clarify whether Ontario's comparatively permissive e-Laws reproduction policy creates a no-licence path to a meaningful Layer C building-code obligation product.

Conclusion: **not by itself**.

## 1. Current Ontario Building Code legal structure

Ontario Regulation 163/24 is now a very short regulation. The current consolidated regulation states that Ontario's Building Code consists of:

1. the National Building Code of Canada 2020 (NBC 2020), issued by the Canadian Commission on Building and Fire Codes / NRC; and
2. the current `Ontario Amendments to the National Building Code of Canada 2020`, issued by Ontario's Ministry of Municipal Affairs and Housing.

Official e-Laws source:

- https://www.ontario.ca/laws/regulation/r24163

Ontario's own 2024 Building Code guidance explicitly explains the structural change:

- the new Building Code regulation is one page long;
- it adopts NBC 2020 except where amended by the Ontario Amendment Document;
- the full-length Building Code is no longer available on e-Laws;
- the Compendium consolidates NBC 2020 + Ontario Amendments into one document.

Official source:

- https://www.ontario.ca/page/2024-ontario-building-code

## 2. Consequence for open e-Laws reuse

ProjectPermit previously identified Ontario statutes/regulations on e-Laws as comparatively permissive for commercial reproduction subject to conditions.

That remains useful for:

- the Building Code Act;
- O. Reg. 163/24 adoption/transition language;
- amendment history and effective dates;
- other enacted Ontario statutes/regulations that contain substantive obligations directly.

But the main technical Building Code requirements are no longer printed inside O. Reg. 163/24 itself.

Therefore:

> **the permissive e-Laws layer does not contain enough substantive Building Code technical content to support a meaningful quote-stage Layer C obligation engine on its own.**

The crucial technical content sits upstream in NBC 2020 and the Ontario Amendment Document.

## 3. Current authoritative dependency graph

For current Ontario technical Building Code obligations:

`O. Reg. 163/24 -> NBC 2020 + current Ontario Amendment Document`

The Compendium is a consolidated convenience form of those materials rather than an independent open substitute.

Current e-Laws amendment history also matters because O. Reg. 163/24 changes which dated Ontario Amendment Document is legally adopted. As of the 2026 research window, Ontario has repeatedly updated that referenced amendment document through amending regulations.

This means a maintained product must track **both**:

- the regulation/effective-date pointer; and
- the incorporated code/amendment content.

## 4. Compendium commercial-use boundary

Ontario's official digital Building Code Compendium guidance states that the digital Compendium is available for personal/non-commercial reproduction and distribution, but if the material is not provided to the public for free, Ontario treats that as commercial use requiring a ministry licence.

Official example/guidance:

- https://www.ontario.ca/page/request-digital-copy-2012-building-code-compendium
- https://www.ontario.ca/form/get-2012-building-code-compendium-non-commercial-use

The 2024 Building Code guidance likewise links to the 2024 Compendium as a non-commercial-use resource.

Therefore ProjectPermit must **not** treat the free digital Compendium as a commercial source corpus.

## 5. Ontario Amendment Document boundary

Ontario states that the Amendment Document is an official component of the Building Code and instructs users to request a copy by email.

The public pages reviewed in this pass do **not** clearly state a separate commercial-reuse licence for derived structured facts from the Amendment Document itself.

Therefore its commercial API rights remain **unresolved**, not assumed open.

The existing ministry licensing clarification request remains necessary.

## 6. NRC dependency remains unavoidable for deep technical rules

Because Ontario adopts NBC 2020 as the base code, most harmonized technical requirements ultimately depend on NRC content even if Ontario-specific differences are separately available.

Existing ProjectPermit licensing research has already identified NRC's commercial reproduction/consent boundary as a hard gate for protected code content.

Therefore a technically deep Ontario Layer C cannot be classified as a simple zero-cost/open-data build until NRC rights and the Ontario Amendment Document rights are clear.

## 7. What can still be built without protected code ingestion

A no-licence/no-protected-corpus Ontario slice could still use open/official sources for things such as:

- Building Code Act / administrative statutory obligations;
- adoption/effective/transition dates;
- municipal permit applicability and procedural requirements from municipal public sources;
- municipal planning/zoning/heritage/process facts where rights permit;
- change/freshness monitoring and source identity;
- official links and citations without reproducing protected code text.

But that is **not equivalent** to full technical `building-code obligations`.

Do not market it as such.

## 8. Commercial decision consequence

This materially narrows the Layer C build gate:

### Do not assume

`Ontario e-Laws is open -> Ontario Layer C can be built cheaply from open law.`

### Correct model

`open administrative/legal layer + licensed/permissioned technical code layer + maintained amendment/effective-date graph`

This is much closer to the commercial architecture used by ICC Code Connect and independent applications such as Kestrel: authoritative content/licensing is an infrastructure layer distinct from the application/workflow layer.

## 9. Evidence / score impact

No E-level increase.

This is a **cash/licensing feasibility clarification** and, if anything, makes the no-licence Layer C path narrower.

Current consequence:

- do not pay for licence yet;
- do not ingest NBC/Compendium protected content yet;
- continue buyer denominator/material-consequence validation;
- wait for written Ontario/NRC rights clarification;
- if buyer evidence becomes strong, scope the smallest representative licensed-content slice rather than assuming a province-wide corpus is needed on day one.
