# Layer C source licensing matrix — 2026-08-30

## Purpose

Reduce pre-build cash/licensing risk by separating regulatory source classes before any Layer C implementation.

This is a **product-risk research note, not legal advice**. Public terms can establish clear reproduction permissions/restrictions, but they do not fully answer whether every independently encoded factual abstraction is a copyright-controlled reproduction/adaptation. Written answers from the relevant rights holders remain the final gate for ambiguous uses.

## Current matrix

### GREEN — Ontario statutes and regulations / legal materials

Ontario's King's Printer copyright policy explicitly permits any person to reproduce the text and images contained in Ontario statutes, regulations and judicial decisions without seeking permission and without charge.

Conditions include:

- reproduce accurately;
- acknowledge Crown copyright;
- reproductions that are not official copies must state that they are not official versions.

Commercial reproduction is specifically excluded from the general commercial-licence requirement for Ontario legal materials.

Official source:
- https://www.ontario.ca/page/copyright-information

Practical Layer C implication:

- Ontario statutory/regulatory legal material is the clearest low-cash-cost legal-text source class found so far.
- Prefer provision ids + structured facts + official e-Laws links even where broader reproduction is permitted.
- Preserve source/version/currency metadata and the required non-official-version boundary.

### RED / LICENCE REQUIRED — Ontario Building Code Compendium

Ontario says the digital Building Code Compendium is available for non-commercial use, but commercial reproduction/distribution requires a licence from the Ministry of Municipal Affairs and Housing.

Official sources:
- https://www.ontario.ca/page/request-digital-copy-2012-building-code-compendium
- https://www.ontario.ca/page/ontarios-building-code
- https://www.ontario.ca/page/2024-ontario-building-code

Important 2024-code structure:

- Ontario's 2024 Building Code adopts NBC 2020 except as amended by the Ontario Amendment Document.
- The Compendium consolidates the National Building Code and Ontario amendments.

Practical Layer C implication:

- Do not ingest/reproduce/distribute Compendium content commercially without a written licence.
- Do not assume the permissive Ontario legal-material policy automatically clears the Compendium, because Ontario publishes a separate explicit commercial-licensing rule for it.
- Written inquiry already sent to `buildingtransformation@ontario.ca` asking about a commercial API that exposes structured requirement facts/provision ids/links without republishing code text.

### RED TODAY / COMMERCIAL MACHINE-READABLE PATHWAY UNDER DEVELOPMENT — NRC National Model Codes

The National Building Code of Canada 2025 remains NRC-protected content; free electronic access does **not** create commercial reuse rights. Commercial reproduction still requires appropriate NRC permission/licensing.

Official sources:
- https://nrc.canada.ca/en/certifications-evaluations-standards/codes-canada/codes-canada-publications/national-building-code-canada-2025
- https://ised-isde.canada.ca/site/innovative-solutions-canada/en/deterministic-artificial-intelligence-assisted-compliance-checking-building-permit-applications

New 2026 licensing/digitalization signal:

- NRC is actively working with DITA/XML to manage Code changes;
- NRC says it is creating machine-oriented outputs including HTML, JSON, RDF/TTL and JSON-LD;
- funded compliance-checking projects may receive machine-readable National Code formats plus schema/API information;
- NRC explicitly says the **licensing and distribution model for new digitalized Code formats is under development**;
- NRC separately states it is updating the licensing/distribution approach for **commercial use of machine-readable codes**.

Practical Layer C implication:

- Do not ingest/reproduce National Code content commercially yet; current rights are still gated.
- However, do not model NRC as a permanent PDF-only licensing dead end either.
- A future authoritative machine-readable commercial distribution/licensing channel is now an official, credible possibility.
- If buyer evidence later justifies Layer C, request the then-current machine-readable commercial terms rather than building a scraped-PDF corpus.
- Pricing, eligibility, redistribution scope, API availability and timing remain unknown, so this is **not clearance**.
- Existing written inquiry to Codes Canada remains useful, but the question should now explicitly ask about the developing machine-readable commercial pathway.

Detailed note:
- `docs/validation/nrc-machine-readable-code-licensing-signal-2026-08-30.md`

### RED / PRIOR AUTHORIZATION, POSSIBLE ROYALTIES — Québec LégisQuébec

LégisQuébec's copyright page says prior authorization from Publications du Québec and associated royalties are required to reproduce, download, store, translate, adapt, publish, communicate or publicly represent information from LégisQuébec.

It also expressly says a person wishing to download information from LégisQuébec to process it with an AI tool or feed an AI tool must obtain prior authorization.

The page expressly says no authorization is required simply to reproduce a hyperlink to a law, regulation or LégisQuébec page.

Official source:
- https://www.legisquebec.gouv.qc.ca/fr/contenu/droit_auteur

Practical Layer C implication:

- Do not build a commercial Québec Layer C corpus by downloading/storing/adapting LégisQuébec content before permission is resolved.
- Official hyperlinks are the only use explicitly identified on the public copyright page as not requiring authorization.
- Treat Québec legal-content ingestion as a separate licensed data layer rather than assuming Canadian legal text is uniformly open.
- Written inquiry already sent to the Québec copyright office asking about structured requirement facts + provision ids + official links without republishing legal text.

## YELLOW — factual abstractions / provision ids / official links without reproduced text

This is the most important unresolved category for ProjectPermit.

Proposed commercial output is not a code reader. It would ideally return facts such as:

- required professional involvement;
- required document;
- approval/precondition;
- inspection/stage;
- filing or validity deadline;
- provision/source identifier;
- official link;
- verification/version metadata.

Public copyright pages clearly regulate reproduction/adaptation of protected content but do not fully resolve the legal boundary for every independently encoded factual conclusion derived from reading that content.

Therefore:

- **Do not classify this category as GREEN merely because the API does not quote text.**
- Await written rights-holder clarification for NRC / Ontario Compendium / Québec before making code-derived facts a commercial production dependency.
- In the meantime, keep E3 design capable of using source ids/links and low-risk sources without requiring full protected text ingestion.

## Product architecture consequence

If Layer C crosses E2, keep sources in separate entitlement classes rather than one undifferentiated corpus:

1. `OPEN_LEGAL_MATERIAL`
   - e.g. Ontario statutes/regulations under the King's Printer legal-material permission.
2. `PUBLIC_LINK_ONLY`
   - official source may be linked but content is not ingested/reproduced absent permission.
3. `LICENSE_REQUIRED`
   - NRC / Building Code Compendium / Québec source classes where commercial reuse terms require or may require written licence/authorization.
4. `MACHINE_READABLE_LICENSE_PENDING`
   - authoritative digital source has an official commercial licensing/distribution pathway under development, but current terms are not yet available/cleared.
5. `WRITTEN_CLEARANCE_PENDING`
   - derived factual abstractions whose status has not been confirmed in writing.

Every obligation/evidence record should be capable of carrying a source-rights classification, but **do not implement that schema before buyer validation crosses the gate**.

## Cash discipline

- Spend **$0** on code-content licences while Layer C remains E1-only.
- Do not purchase a licence merely to create a demo.
- Do not spend engineering time converting protected PDFs into a private commercial corpus while an authoritative machine-readable distribution path is actively being developed.
- First prove a repeated buyer workflow and material consequence.
- If E2/E3 emerges, obtain current licence terms and calculate licence cost per addressable workflow/call before committing to a protected source layer.
- If rights costs destroy unit economics, constrain Layer C to legally reusable/public-link source classes instead of subsidizing expensive content.

## Current decision

Licensing risk does **not** kill Layer C. The NRC 2026 signal modestly improves long-run feasibility, but it does not change the immediate build gate.

Safest order now:

> buyer denominator -> workflow consequence -> representative low-risk E3 only if justified -> obtain current NRC/Ontario/Québec commercial machine-readable or structured-data rights terms -> licence economics -> only then protected code-content expansion.

No E-level increase results from this licensing update.
