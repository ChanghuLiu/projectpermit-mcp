# Municipal Self-Service Expansion Watch — 2026-08-28

## Québec City — do not treat as a low-friction expansion target

A 2026-08-28 first-party scan found that Ville de Québec already operates an `Assistant-permis` experience for residents/businesses planning work.

The city describes the tool as an information/accompaniment service for project preparation. It is property/project-oriented and helps users navigate whether permits/certificates and regulatory requirements apply to renovation, additions, exterior work and other project types.

Official sources:

- https://www.ville.quebec.qc.ca/services/assistant-permis/index.aspx
- https://www.ville.quebec.qc.ca/citoyens/reglements_permis/info-permis.aspx
- https://www.ville.quebec.qc.ca/citoyens/propriete/maison_patrimoniale.aspx

The City also explicitly advises users with heritage properties to consult Assistant-permis to determine whether a permit/certificate or other regulatory requirement applies before beginning work.

## Classification

For expansion-screening purposes, treat Québec City as **high first-party self-service substitution risk**.

Do not assign a precise Level-4 equivalence to Gatineau URBAIN without testing the full current interaction flow. The public evidence is sufficient, however, to reject the assumption that Québec City is merely static permit guidance.

## Product implication

Do **not** add Québec City merely to increase the coverage map.

Admission should require:

- a credible external B2B workflow with repeated candidate calls;
- an explicit reason the municipal Assistant-permis cannot satisfy the machine-to-machine workflow;
- evidence that cross-jurisdiction normalization/evidence maintenance creates value beyond linking to the first-party tool.

## Adjacent Canadian platforms found in the same scan

### Cloudpermit

Cloudpermit is a large Canadian municipal permitting/planning platform with API integration, application/workspace, inspection, GIS/property and fee/data capabilities.

Source:

- https://cloudpermit.ca/products/building-permitting

Current public positioning is primarily municipality/application/inspection workflow, not a contractor quote-stage deterministic `does this scope require a permit?` API. Treat as downstream/infrastructure competition, not an exact ProjectPermit substitute based on current evidence.

### PermitAssure

PermitAssure is a Canada-built API-first digital permitting/building-code compliance platform oriented toward permitting authorities, case/document management, GIS/BIM integration and professional decision support.

Source:

- https://www.permitassure.com/

Current public positioning is downstream digital review/compliance infrastructure rather than ProjectPermit's narrow Request/Estimate/Quote-stage applicability contract.

## Score implication

No additional Go/No-Go reduction is justified from this scan alone.

Why:

- Québec City is not currently in ProjectPermit's seven supported jurisdictions;
- Cloudpermit and PermitAssure are not currently verified exact quote-stage substitutes;
- the existing municipality-admission rule already says Level-3/4 first-party self-service requires a separate external B2B call path.

Record this as an expansion guardrail, not as E2/E3/E4/E5 demand evidence.