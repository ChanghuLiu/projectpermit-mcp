# Municipal Permit Self-Service Competition

Updated: 2026-08-27

Purpose: identify where ProjectPermit risks duplicating first-party municipal self-service and where the product still has a differentiated machine-to-machine role.

This is competitive-context research, not E3/E4 market validation.

## Classification

- **Level 1 — static guidance only:** pages/lists explain permit requirements.
- **Level 2 — static guidance + property/online service tooling:** permit guidance remains mostly page-based, but the city provides property lookup, zoning, application or status tooling.
- **Level 3 — workflow automation:** structured online workflow materially automates application/pre-check/issuance, but does not clearly provide an integrated address-aware `do I need a permit?` determination.
- **Level 4 — address-aware permit eligibility assistant:** user enters project + property and the first-party system explicitly helps determine whether a permit is required.

The levels describe substitution risk for ProjectPermit's homeowner-facing use case, not quality or legal authority.

## Current seven-city matrix

| Jurisdiction | Current first-party self-service | Level | ProjectPermit substitution risk | Practical implication |
|---|---|---:|---|---|
| Gatineau | **URBAIN** asks structured project questions, requires address/matricule/lot or map selection, applies regulations according to the project location, and tells the user whether an urbanism permit is required | **4** | **Very high** for a Gatineau homeowner checker | Do not build a Gatineau-specific homeowner front end; keep Gatineau only for cross-jurisdiction API normalization |
| Toronto | Static `When Do I Need a Building Permit?` guidance plus a new **AI Building Permit Application Pre-Check** hosted on CivCheck for eligible residential permit applications; the AI reviews uploaded application documents and selected zoning/OBC issues | **3** | **High** for downstream application completeness/review, lower for initial permit-applicability routing | ProjectPermit should stay upstream at quote/intake routing and should not expand into plan/document review without strong evidence |
| Longueuil | Structured online permit portal supports all permit/certificate applications and can issue some common permits online under stated conditions | **3** | **Moderate-high** for simple application/issuance workflows | Avoid duplicating application submission; focus on cross-city preflight before a user commits to the municipal workflow |
| Laval | Detailed project-specific permit pages plus address-based `Info-règlements` / PIIA lookup and online application/account workflow | **2** | **Moderate** | Existing deterministic rules still add cross-city value, but deeper Laval-only UI work has low priority |
| Ottawa | Detailed `Do I need a building permit?` project pages plus My ServiceOttawa Building/Planning/Land Development portal with address/parcel selection for applications | **2** | **Moderate** | Keep ProjectPermit upstream; do not duplicate the application portal |
| Mississauga | Static common-project permit-required/not-required list, separate property-information/zoning tools, ePlans and permit-status services | **2** | **Moderate** | Cross-jurisdiction preflight remains differentiated; homeowner-only value is limited |
| Vancouver | Project-based permit guidance, permit/application search by address, online permit management and application workflows | **2** | **Moderate** | Keep machine-readable cross-city routing; avoid becoming another Vancouver permit-navigation site |

## Key finding: Gatineau is the clearest direct substitute

Ville de Gatineau's URBAIN is already very close to the homeowner-facing version of ProjectPermit:

- structured question flow;
- project-specific routing;
- address / property context;
- current regulation applied according to location;
- explicit `permit required / not required` guidance;
- links to the appropriate online application;
- rules, zoning/grid and mapping context;
- escalation to municipal staff for special/complex cases.

The City explicitly says the user must enter the address, or may use a matricule, lot number or map selection so that location-specific rules can be considered.

This makes a single-city Gatineau permit checker strategically unattractive even if ProjectPermit's deterministic rule engine works well.

## Toronto: different but important competitive movement

Toronto now has an official **Building Permit Application Pre-Check** pilot using AI through CivCheck.

Important boundary:

- it is **not primarily a `do I need a permit?` eligibility assistant**;
- it begins after the applicant already has an eligible permit project and application documents;
- it can review document/format issues and some Ontario Building Code / zoning applicable-law issues for eligible low-rise residential projects;
- users supply property address, permit type, expected submission date and PDF application documents;
- it does not replace the City's formal review or approve a permit.

This matters because it shows municipalities are also moving into **AI-assisted permit review**, not just digitized application forms.

ProjectPermit should therefore avoid drifting into full drawing/document code review unless there is a very strong independent B2B wedge. That problem is more complex, higher-liability and increasingly served by first-party or city-contracted tools.

## Longueuil: application automation is already meaningful

Longueuil's `Permis en ligne` portal allows online submission for all permit/certificate types and says selected common cases may be issued online under defined conditions, including examples such as:

- pools;
- balconies;
- interior renovations;
- exterior repairs;
- accessory equipment.

The current public portal also exposes a structured catalog of work types across residential, commercial and industrial use.

No integrated address-aware `do I need a permit?` diagnostic comparable to Gatineau URBAIN was identified in the official material reviewed on 2026-08-27. Do not strengthen this into a claim that none exists.

## Ottawa / Mississauga / Laval / Vancouver

The current official material reviewed shows increasingly strong digital application/property tooling but not a first-party integrated eligibility assistant comparable to URBAIN:

### Ottawa

- detailed permit-required / permit-exempt project pages;
- online Building, Planning and Land Development customer portal;
- application workflow includes address/parcel selection.

### Mississauga

- explicit static list of common projects that do/do not require permits;
- property information by address/roll number;
- zoning information map;
- ePlans / permit application and status services.

### Laval

- highly structured permit pages by project family;
- some pages explicitly tabulate `permit required / no permit` outcomes;
- `Info-règlements` property lookup by lot/address to identify PIIA and location-specific conditions;
- online permit application/account workflow.

### Vancouver

- project-based `when you need a permit` guidance;
- online permit/application management;
- permit/application lookup by address;
- project-specific renovation/building pages.

## Strategic conclusion

The municipal software trend strengthens one part of ProjectPermit's thesis and weakens another.

### Weaker thesis

> Build a better homeowner permit checker for each municipality.

This becomes less defensible as cities deploy their own structured, address-aware, AI-assisted or immediate-issuance experiences.

### Stronger thesis

> Provide one deterministic machine contract across many municipalities inside a contractor/platform workflow before the user enters any city's portal.

The durable differentiation must be:

1. **cross-jurisdiction schema** — one input/output contract across municipalities;
2. **workflow position** — quote/request/job/intake before permit submission;
3. **machine-to-machine delivery** — API/MCP rather than another destination website;
4. **evidence normalization** — stable rule ids, determination, confidence and first-party sources in a common response;
5. **portfolio volume** — repeated work across many addresses/cities;
6. **fail-safe unknown handling** — explicit confirmation/escalation rather than pretending to be the AHJ;
7. **low workflow friction** — contractor does not have to manually visit a different municipal website for every candidate job.

## New municipality-admission rule

Before adding any city, answer these questions first:

1. Does the municipality already provide an address-aware permit eligibility assistant?
2. Does it provide automated/instant permit issuance for common scopes?
3. Does it provide an AI/document pre-check?
4. Is there a documented public API/data surface ProjectPermit could reuse rather than duplicate?
5. What independent external workflow will generate repeated calls in that municipality?

If the city already has Level 3–4 self-service and there is no external B2B call path, **do not add or deepen coverage merely for homeowner utility**.

## Product-boundary decision

- Do not build a standalone homeowner UI as a priority.
- Do not compete with municipal application portals.
- Do not move into full plan/code-document review merely because Toronto has validated that workflow category; that is a different, higher-cost product.
- Keep ProjectPermit upstream and cross-jurisdiction.
- Municipality-specific engineering work must be justified by E3/E4-backed external workflow volume.

## Official sources reviewed 2026-08-27

### Gatineau
- https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Furbain_assistant_virtuel_urbanisme
- https://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme

### Toronto
- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/building-permit-application-pre-check/
- https://www.toronto.ca/services-payments/building-construction/building-permit/before-you-apply-for-a-building-permit/when-do-i-need-a-building-permit/

### Ottawa
- https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/building-permit-projects
- https://myservice.ottawa.ca/help?cat-id=2235126&help-file=3033791&lang=en

### Mississauga
- https://www.mississauga.ca/services-and-programs/building-and-renovating/building-permits/when-a-building-permit-is-required/
- https://www.mississauga.ca/services-and-programs/building-and-renovating/find-property-information/

### Laval
- https://www.laval.ca/reglements-permis/trouver-mon-permis/renovation-residentielle-exterieure/
- https://www.laval.ca/Pages/Fr/Citoyens/renovation-ou-reparation.aspx

### Longueuil
- https://www.longueuil.quebec/fr/services/amenagement-urbanisme/demande-de-permis-en-ligne
- https://permisenligne.longueuil.quebec/

### Vancouver
- https://vancouver.ca/home-property-development/when-you-need-a-permit.aspx
- https://vancouver.ca/home-property-development/apply-for-and-manage-your-permit.aspx
