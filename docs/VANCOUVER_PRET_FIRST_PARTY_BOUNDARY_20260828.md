# Vancouver PRET First-Party Requirements Boundary — 2026-08-28

## Why this matters

The City of Vancouver operates a live **Project Requirements Exploration Tool (PRET)** that materially overlaps ProjectPermit's pre-application requirements-discovery surface.

Current City pages route applicants to PRET on the City's ServiceNow domain (`cov.service-now.com`). The tool is currently available for several low-density housing project types and is being expanded.

The City says PRET can help an applicant:

- explore whether a project is allowed on a property;
- understand regulations and requirements associated with the site;
- identify the permits needed before applying;
- assess feasibility before pursuing an application;
- receive tailored required-document information;
- create a project, check eligibility and set up permits.

Current official sources:

- https://vancouver.ca/home-property-development/build-a-multiplex-dwelling.aspx
- https://vancouver.ca/home-property-development/permitting-and-licensing-is-getting-easier.aspx
- https://vancouver.ca/news-calendar/permitting-improvements-ease-laneway-builds-and-residential-renovations.aspx
- https://vancouver.ca/news-calendar/city-to-launch-project-requirements-exploration-and-ecomply-digital-permitting-tools.aspx

## The original municipal problem statement is unusually close to ProjectPermit

The City's 2022 Call for Innovation `PS20220333 — Digital Regulatory & Business Rules Ecosystem` described a pre-existing problem in which regulations and supporting guidance were largely available as PDFs but were not easily linked to:

- a type of project;
- an address;
- a building;
- a parcel.

The City said this made it difficult for residents, customers and staff to understand which rules apply under what conditions for which property-development projects, creating rework and inconsistent interpretation.

The CFI explicitly sought solutions that would let any user understand how regulations, policies and business rules apply to a proposed situation or project through an intuitive, accessible, data-driven digital platform. Evaluation criteria specifically called out digital rules, decision-engine services and DMN experience.

Official sources:

- https://bids.vancouver.ca/bidopp/EOI/CFI-PS20220333.htm
- https://vancouver.ca/files/cov/2024-315-release.pdf

This is strong independent evidence that the underlying applicability/requirements problem is real and can justify municipal investment.

## Current delivery is real, not roadmap-only

PRET launched in 2023 for laneway-house applicants. The City reported that frequent applicants tested the tool and valued its eligibility check and tailored required-document list.

Current 2026 City pages say the project-exploration tool is available for:

- laneway houses;
- single detached houses;
- duplexes;
- some multiplex configurations;

with more application types planned.

The PRET entry points currently resolve to the City's ServiceNow domain, which establishes that the live first-party experience is backed by the City's ServiceNow-based application environment.

## Procurement / implementation boundary

The proactive FOI release for `2024-315` requires careful interpretation.

The FOI request itself characterizes PRET as having been built on ServiceNow and asks for the CFI plus the awarded contract. The release contains:

- the broad Digital Regulatory & Business Rules Ecosystem CFI;
- multiple vendor proposals/agreements under the same innovation program;
- a 2022 Solvera Solutions ServiceNow contract;
- later Deloitte advisory material;
- Archistar/eComply material.

However, the **actual Solvera contract scope visible in the released documents is a new-business-licence digital workflow**, not a PRET-specific laneway/permit-requirements implementation. It uses the City's ServiceNow environment, dynamic rules and APIs, but it should not be cited as proof that Solvera built PRET.

Similarly, the City explicitly identifies **Archistar as the developer/technology partner for eComply**, a separate design/zoning-compliance tool. The official launch announcement discusses PRET and eComply as two distinct tools. Therefore ProjectPermit must not attribute PRET to Archistar merely because both appear in the same permitting-modernization program.

What is safe to say today:

- PRET is a live City product;
- current PRET links run on the City's ServiceNow domain;
- Vancouver deliberately pursued a broader digital-regulatory/business-rules architecture;
- the City can use enterprise workflow/rules infrastructure plus internal/external delivery resources to create first-party requirements exploration;
- the exact PRET production-build vendor, implementation cost and reusable external product contract are not established by the reviewed public records.

## Digital-rules horizon

Vancouver's Housing Accelerator Fund action plan separately lists a **Digital Rules Framework and Platform** milestone due September 30, 2026 and currently marked `On Track`. It also lists PRET for low-density housing as completed and additional automated zoning/building-code initiatives.

This is a meaningful future defensibility threat, but the Digital Rules Framework and Platform is not yet evidence of a delivered reusable external rules API.

Source:

- CMHC Vancouver Housing Accelerator Fund Action Plan Summary

## Scope mismatch that still matters

PRET's current live coverage is predominantly low-density housing feasibility / new-build-style project setup. ProjectPermit's present normalized families include renovation and alteration cases such as windows/doors, decks, plumbing changes, basement/secondary-suite work and accessory structures.

Vancouver still publishes separate static renovation guidance and fast-track renovation streams. The current public evidence does not show PRET broadly resolving ProjectPermit's full renovation applicability contract.

Therefore PRET is a strong functional analogue and first-party substitute for some workflows, but not a demonstrated replacement for every current ProjectPermit family.

## Score impact

**No additional score reduction today.**

PRET is stronger corroboration than a static FAQ and, together with Gatineau URBAIN, shows that first-party municipalities can occupy a local `property/project -> requirements` surface.

But the canonical scorecard already removed the value of single-city rule ownership:

- competitive headroom is already **0/10**;
- defensibility is already **2/10** because local/few-city logic can be internalized and focused local checkers already exist;
- the remaining two defensibility points are explicitly tied to externally valued **cross-city maintenance, evidence/versioning, safe unknown-state handling, accuracy history and embedded distribution**, not to ownership of one city's rules.

PRET does not yet prove that those remaining cross-city/external-machine-contract functions are cheaply commoditized.

A second penalty would therefore double-count the already-recognized local-internalization weakness.

## What this does change

The scorecard's geographic-rescue language must not imply that Quebec/Vancouver/Ottawa coverage itself creates a moat.

The accurate statement is:

> ProjectPermit's geography is not identical to LandLogic/Parcella's currently verified Ontario footprint, but local geographic coverage can be displaced by first-party municipal tools. The surviving commercial question is whether buyers value one maintained cross-city machine contract enough to pay for it instead of combining municipal tools, broader platforms and internal local logic.

That buyer preference still has no E2/E3/E4/E5 support.

## Future score-moving triggers

PRET should trigger a new score review if future evidence establishes any of the following:

1. Vancouver exposes PRET/project-requirements results as an ordinary external API or machine-readable service;
2. the underlying ServiceNow/digital-rules implementation becomes a reusable packaged product adopted across municipalities at low marginal implementation cost;
3. the 2026 Digital Rules Framework and Platform becomes a production rules service that substantially commoditizes deterministic municipal-rule maintenance;
4. several municipalities independently expose comparable machine contracts, making cross-city aggregation primarily an orchestration problem rather than a maintained-knowledge problem;
5. representative software buyers state that municipal first-party requirement tools are already good enough and they would not pay for an external cross-city layer.

Until one of those occurs, Vancouver PRET is a high-value corroborator of a weakness already counted in the score, not an independent new penalty.