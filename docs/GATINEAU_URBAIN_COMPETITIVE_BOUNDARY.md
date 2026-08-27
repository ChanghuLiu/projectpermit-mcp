# Gatineau URBAIN — Competitive Boundary

Updated: 2026-08-27

## Finding

Ville de Gatineau now operates **URBAIN**, a first-party virtual urban-planning / permit assistant.

This materially changes how ProjectPermit should think about the Gatineau wedge. It does **not** invalidate the cross-jurisdiction API thesis, but it makes a standalone single-city homeowner permit checker a poor product direction.

## What Gatineau says URBAIN does

Current official City material says URBAIN:

- uses a structured sequence of questions adapted to the project;
- analyzes the user's declared situation against current regulations and their application to the project location;
- accepts address / property identification inputs;
- gives short targeted answers and routes the user appropriately;
- tells the user whether an urbanism permit is required for the described work;
- when a permit is required, guides the user to the online permit request with preparation information;
- when a permit is not required, provides relevant standards;
- for complex or special regulatory situations, tells the user to contact the urban-planning service;
- can expose the zoning grid, constraint map and no-permit work list for the selected address.

The City announced URBAIN on 2025-12-09 and said it would launch in early 2026. The current Gatineau permit pages now link to it as a live tool.

The City's current roadmap says additional modules are planned by the end of 2027 for:

- subdivision / lotissement;
- demolition;
- business permits;
- subsidy programs.

## Official sources

- URBAIN product page: https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Furbain_assistant_virtuel_urbanisme
- URBAIN announcement (2025-12-09): https://www.gatineau.ca/portail/default.aspx?id=-1977031900&p=nouvelles_annonces%2Fcommuniques%2Fcommunique_2015
- Gatineau permit/urbanism portal: https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme
- Gatineau URBAIN FAQ: https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fdemande_information%2Ffaq

## What is **not** established

Current public official material reviewed on 2026-08-27 does **not establish** a public developer/API product for URBAIN.

Do not convert that into a stronger claim such as “URBAIN has no API.” The correct status is:

> **No public developer/API surface has been identified in the official material reviewed so far.**

Likewise, do not assume ProjectPermit can or should call undocumented URBAIN internals.

## Strategic implication

### Direction to avoid

Do **not** position ProjectPermit as:

> “A Gatineau homeowner enters an address and project and we tell them whether they need a permit.”

The municipality itself already provides a first-party version of that experience, with stronger authority and deeper property/regulatory context.

### Direction to preserve

ProjectPermit should stay focused on a different workflow:

`multi-jurisdiction work intake / quote / job -> normalized scope + property -> deterministic preflight -> official evidence -> machine-readable routing`

The differentiators must be:

1. **cross-jurisdiction normalization** — one schema across municipalities;
2. **embedded B2B workflow** — quote/job/intake systems such as Jobber rather than a homeowner destination site;
3. **API / MCP delivery** — machine-to-machine use rather than a human-only municipal portal;
4. **evidence normalization** — stable rule ids + first-party source links in a common response shape;
5. **portfolio/volume workflow** — repeat decisions across many properties and municipalities;
6. **explicit uncertainty/fail-safe behavior** — route unknowns rather than pretending to be municipal authorization.

## Interpretation for market validation

URBAIN is both a **substitution risk** and a **problem-validation signal**:

- substitution risk: cities can increasingly automate their own resident-facing permit guidance;
- problem-validation signal: Gatineau invested in a dedicated personalized permit-guidance experience because self-service rule discovery was important enough to improve;
- ProjectPermit still needs independent evidence that contractors/platforms will pay for cross-city embedded preflight rather than simply use municipal tools manually.

Do not count Gatineau's investment as E3/E4 demand for ProjectPermit. It is market-context evidence only.

## Product rule going forward

When evaluating a new municipality, add one competitive check:

> **Does the municipality already provide an address-aware project/permit assistant or structured permit wizard?**

If yes:

- lower the value of a homeowner-facing ProjectPermit experience in that city;
- increase attention to B2B workflow/API differentiation;
- do not duplicate the city's front end;
- consider whether the municipality's official assistant provides a documented reusable data/API surface before maintaining duplicate rules;
- keep the ProjectPermit rule only when it contributes to cross-jurisdiction machine workflow and can be maintained from authoritative sources.

## Current decision

- Keep Gatineau in the seven-city ruleset because cross-jurisdiction callers still benefit from a common API contract.
- Do not expand ProjectPermit into a Gatineau-specific homeowner UI.
- Do not invest heavily in reverse-engineering URBAIN.
- Keep unresolved Gatineau PIIA/heritage machine-overlay work behind actual external-volume evidence.
- Prioritize Jobber/embedded-workflow validation over deeper Gatineau feature parity with URBAIN.
