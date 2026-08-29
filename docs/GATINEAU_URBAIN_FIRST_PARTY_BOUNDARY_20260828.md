# Gatineau URBAIN First-Party Permit-Applicability Boundary — 2026-08-28

## Why this matters

Gatineau now operates a first-party municipal digital assistant, **URBAIN**, whose public purpose overlaps closely with ProjectPermit's consumer-facing applicability question.

The City describes URBAIN as an online urban-planning assistant intended to give residents a rapid, reliable, situation-specific answer to:

> `ai-je besoin d'un permis?`

Current official documentation says URBAIN:

- starts from the property location (address, matricule or lot, with map selection available);
- asks a structured sequence of project-specific questions;
- considers the regulations that apply to the selected property/location;
- tells the user when a permit is required;
- tells the user when no permit is required and provides applicable regulatory information;
- routes complex or unusual cases to municipal staff instead of forcing a false yes/no;
- exposes regulations, grids, maps, constraints and related urban-planning information;
- can save results for later continuation;
- currently covers common residential development/construction work including renovations, additions, accessory structures and some exterior work.

Official sources:

- https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal/permis_certificats_autorisation_urbanisme/urbain_assistant_virtuel_urbanisme
- https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal/permis_certificats_autorisation_urbanisme/demande_information/faq
- https://www.gatineau.ca/portail/default.aspx?id=-1977031900&p=nouvelles_annonces/communiques/communique_2015

## Functional overlap

URBAIN's public interaction shape is close to the ProjectPermit consumer question:

`property/location + project type + structured facts -> permit required / no permit / special review + applicable rules`

This is stronger evidence than a static FAQ or generic permit page. It shows a municipality itself considers structured permit-applicability triage useful enough to productize as a digital service.

It also means ProjectPermit must **not** treat a Gatineau homeowner-facing `Do I need a permit?` experience as open commercial whitespace.

## Pain / demand corroboration

Gatineau's historical public service data also shows that urban-planning information demand can be materially larger than permit issuance alone.

The City reported approximately **20,000 urban-planning information requests in 2017**. This is not a ProjectPermit call-volume denominator: the category is broader than permit applicability and the data is old. It is nevertheless evidence that pre-application regulatory information has historically generated substantial service demand.

Official source:

- https://www.gatineau.ca/portail/default.aspx?id=252027633&p=nouvelles_annonces/communiques/communique

Do not convert the 20,000 figure into current-family API calls or current annual demand.

## Development/procurement provenance is unverified

Current public material reviewed on 2026-08-28 and re-checked on 2026-08-29 does **not** establish whether URBAIN was:

- developed wholly by Gatineau staff;
- built with a contractor/vendor;
- assembled on a configurable third-party rules/workflow platform; or
- built through another mixed delivery model.

The City's launch release describes what URBAIN does but does not name a supplier or state that it was built entirely in-house. No vendor attribution, public developer API, white-label offer or reusable municipal product contract was verified.

Therefore ProjectPermit must not claim that URBAIN proves a municipality can build the whole system internally at a known cost. What it proves is narrower: a single municipality can deliver a high-overlap first-party applicability experience, regardless of the hidden build/procurement path.

## Score impact

**No additional score reduction.**

URBAIN materially strengthens evidence already counted in the canonical scorecard:

- focused municipality-specific applicability logic can be delivered cheaply enough to appear as a free user-facing feature;
- single-city rule ownership is not a durable moat;
- free/bundled/first-party alternatives can occupy local consumer demand.

Those facts are already fully reflected in the current canonical commercial state:

- competitive headroom = **0/10**;
- defensibility = **0/10** after the later CivCheck/Clariti Guide deductions;
- the earlier 58 -> 57 local-replication reduction;
- the later build-vs-buy and cross-jurisdiction regulatory-platform deductions.

Reducing the score again for URBAIN would double-count the same underlying commercial fact. URBAIN is strengthening evidence for the current **48/100 (raw 47.5)** pause/re-scope state, not a new independent penalty.

## What URBAIN does change

The remaining geographic-rescue argument must be stated more carefully.

It remains true that ProjectPermit's seven-city footprint is not identical to LandLogic/Parcella's current publicly verified Ontario footprint. But **geographic non-overlap is not itself a moat**. Gatineau shows that a municipality can independently occupy its local consumer permit-applicability surface with a free first-party tool.

The surviving thesis is therefore narrower:

> Can an external buyer justify paying for one maintained cross-city machine contract — with evidence/versioning, safe unknown states and low integration friction — instead of using municipal first-party tools, broader platforms, or internally maintained local logic?

That buyer preference still has no E2/E3/E4/E5 support.

## Future score-moving conditions

URBAIN becomes independently score-moving only if new evidence shows one of the following:

1. the underlying technology is a reusable third-party platform/API already sold across municipalities at economics that directly substitute for ProjectPermit;
2. multiple municipalities expose equivalent machine-readable applicability services through ordinary external APIs;
3. representative software buyers say they prefer querying/replicating municipal first-party tools instead of buying a maintained cross-city layer;
4. current usage statistics show the local first-party tool absorbs essentially all relevant preflight demand that ProjectPermit hoped to monetize.

Until then, URBAIN is strong corroboration of an already-counted weakness, not a separate new score penalty.