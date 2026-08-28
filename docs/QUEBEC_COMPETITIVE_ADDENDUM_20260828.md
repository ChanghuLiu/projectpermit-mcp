# Quebec Competitive Addendum — 2026-08-28

This addendum corrects an overly broad interpretation of Quebec as competitive whitespace.

The current public evidence shows that Quebec municipalities and private homeowner tools already solve a substantial part of the `do I need a permit?` information problem.

The remaining ProjectPermit hypothesis in Quebec is therefore **not** superior permit guidance for homeowners. It is a unified third-party developer/API delivery model across municipalities, if software buyers actually value that surface.

## Gatineau — direct homeowner permit-applicability assistant already exists

Gatineau's current **URBAIN : assistant virtuel en urbanisme** explicitly exists to answer:

> `ai-je besoin d'un permis?`

URBAIN:

- uses a structured question/answer path adapted to the project;
- analyzes the declared situation using current regulations and project location;
- directs users to the correct permit application when a permit is required;
- tells users when no permit is required and provides applicable norms;
- escalates complex/regulatory cases to the urban-planning service;
- exposes supporting information such as standards, maps and regulatory text.

Sources:

- `https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Furbain_assistant_virtuel_urbanisme&requete=urbain`
- `https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fdemande_information%2Ffaq`

**Implication:** Gatineau invalidates any ProjectPermit value claim based merely on giving residents a clear permit-required / no-permit / confirmation-style answer.

The current public review did not find a documented third-party developer API for URBAIN.

## Laval — permit/no-permit rules are already highly structured online

Laval's current `Trouver mon permis` pages explicitly encode common residential decisions as `Permis requis` vs `Aucun permis` and then add address-specific overlays such as PIIA checks.

Examples in current ProjectPermit families include:

- same-size replacement doors/windows -> no permit;
- changing door/window dimensions -> permit;
- renovating an existing bathroom -> no permit;
- adding a bathroom -> permit;
- ordinary kitchen renovation -> no permit;
- interior renovation -> permit where room dimensions, room count or structure changes;
- accessory structures and gazebos/pergolas use explicit size thresholds;
- project pages instruct users to enter an address into Laval's regulatory map to detect additional site-specific constraints.

Sources:

- `https://www.laval.ca/reglements-permis/trouver-mon-permis/renovation-residentielle-exterieure/`
- `https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx`
- `https://www.laval.ca/reglements-permis/trouver-mon-permis/pergola-pavillon-jardin/`
- `https://www.laval.ca/reglements-permis/trouver-mon-permis/garage-abri-auto-permanent-detache/`

**Implication:** much of the normalized rule logic is already publicly productized for humans. ProjectPermit cannot claim the rule classification itself as a moat.

The current review did not find a published external permit-applicability API for these Laval decision pages.

## Longueuil — mature digital permit workflow + public machine-readable permit records

Longueuil's current online permit service lets citizens:

- submit all permit/certificate request types online;
- pay fees;
- track status;
- receive some permits fully online for categories such as balcony, interior renovation, exterior repair and accessory equipment.

Source:

- `https://www.longueuil.quebec/fr/services/amenagement-urbanisme/demande-de-permis-en-ligne`

Longueuil also exposes a public ArcGIS FeatureServer for permit records. It supports machine-readable query formats including JSON, GeoJSON and PBF.

Sources:

- `https://gociteweb.longueuil.quebec/arcgis/rest/services/CarteInteractive/Permis_En_Ligne/FeatureServer`
- `https://gociteweb.longueuil.quebec/arcgis/rest/services/CarteInteractive/Permis_En_Ligne/FeatureServer/0`

Important boundary:

> the ArcGIS service is a permit-record / geospatial data API, **not** a discovered `address + scope -> permit applicability` API.

Do not confuse public machine-readable permit records with a third-party permit-decision interface.

## Private Quebec-wide homeowner tool — Assistant Rénovation QC

`Assistant Rénovation QC` currently states that it tracks **69 municipalities** and helps Quebec property owners:

- identify permits that may be necessary before work;
- estimate renovation subsidies;
- prepare supporting documents;
- maintain a project/owner record.

It explicitly says it does not replace the municipality's official decision.

Source:

- `https://assistantrenovationquebec.ca/`

The 2026-08-28 public search did **not** find a published developer API, white-label integration, or B2B SaaS integration product for Assistant Rénovation QC.

That absence is a public-market observation only; it does not prove private APIs or partnerships do not exist.

## Revised Quebec classification

Quebec should now be classified as:

> **LOWER PLATFORM/API COMPETITION THAN ONTARIO, BUT NOT PERMIT-LOGIC WHITESPACE**

Existing municipal/private tools already demonstrate:

- permit-required / no-permit determination;
- address/project-specific guidance;
- structured residential rules;
- regulatory-source guidance;
- multi-municipality homeowner coverage;
- online application workflows;
- public geospatial/permit APIs in some cities.

Therefore ProjectPermit's remaining plausible Quebec differentiation is only the combination of:

1. one standardized third-party software contract across several municipalities;
2. developer self-service rather than resident web pages or municipal portals;
3. machine-readable permit applicability with official evidence/rule versions;
4. low-cost per-call use before quote/work-order/estimate decisions;
5. French/English developer-facing normalization;
6. REST/MCP/agent invocation without a municipality-specific implementation project.

Every one of these is still an **unvalidated buyer preference**, not a moat.

## Quebec-specific falsification gate

Before materially expanding ProjectPermit in Quebec, require evidence from a real software/integration buyer that answers all of the following:

1. Why can the workflow not simply link users to Gatineau URBAIN, Laval's permit finder, Longueuil's permit portal, or another municipal assistant?
2. Why is a unified API materially better than municipality-specific UI/manual research for this buyer?
3. How many recent monthly project events would actually call the API?
4. Does the buyer need a deterministic/evidence-linked machine output, rather than just a deep link or human-readable guidance?
5. Would the buyer pay enough per call or pilot to justify French municipal rule maintenance?

Pause Quebec expansion if the answer is merely `one API is more convenient` without bounded recurring volume and willingness to pay.

## Strategic consequence

As of 2026-08-28:

> Ontario is the highest competitive threat because LandLogic / One Ontario already combine broad regulatory intelligence, third-party integrations and a rapidly expanding permitting layer.

> Quebec has less observed third-party API competition, but municipalities already solve much of the homeowner permit-applicability problem themselves.

> Quebec is therefore a **developer-distribution experiment**, not an uncontested permit-information market.

No new Quebec municipality should be added solely because Ontario is crowded. Expansion must be pulled by a real multi-city software workflow that passes distribution, differentiation and economics gates.
