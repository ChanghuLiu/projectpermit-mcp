# Quote-stage permit workflow timing evidence

Updated: 2026-08-27

Purpose: test whether ProjectPermit's intended `Request / assessment -> permit preflight -> estimate / quote` insertion point exists in real contractor workflows, while avoiding the false assumption that every contractor prices work before permit status is known.

This is public workflow evidence only. It is **not E2/E3/E4/E5**, because the public pages do not provide a bounded recent denominator for how many projects required permit-applicability research.

## Observed quote-first workflows

### TopDown Renovations — Toronto / GTA

Public process:

1. free in-home estimate;
2. written quote with finish allowances;
3. design meeting;
4. apply for City of Toronto building permits where required;
5. construction after permits issue.

Source: https://topdownrenos.com/

Implication: permit work occurs **after an initial estimate/quote**. This is structurally compatible with ProjectPermit as a routing/check step before or while the quote is prepared.

### Nexon Build — Toronto / GTA

Public process:

1. discovery;
2. scope & fixed-price estimate;
3. design & permits;
4. build;
5. handover.

Source: https://nexonbuild.ca/services

Implication: another explicit estimate-before-permit workflow. It does not prove that `permit required?` is unresolved at estimate time, but it confirms the workflow location exists.

### Crown Structural — GTA

Public process:

1. free consultation;
2. detailed quotation including engineering and permit costs;
3. structural engineering;
4. permit preparation/submission;
5. installation and inspection.

Source: https://crownstructural.ca/pricing-and-process

Implication: the quote explicitly includes permit cost **before** engineering drawings and permit submission. A deterministic permit-applicability/cost-routing signal could plausibly fit this workflow, but public material does not reveal how often the permit decision is uncertain.

### Home Reframe — Toronto / GTA

Public positioning combines a free written/itemized estimate with drawings and permits handled by the contractor.

Source: https://www.homereframe.com/

Implication: consistent with quote-first integrated contracting, but the exact ordering of permit determination inside the estimate process is not public enough to count as a stronger workflow claim.

## Observed permit-first workflow

### WeRenovate.com — Toronto / GTA

WeRenovate explicitly requires a **completed permit before processing a construction estimate**. Its public explanation is that permit-approved drawings remove zoning/code uncertainty and make contractor pricing comparable and predictable.

Sources:

- https://www.werenovate.com/archold
- https://www.werenovate.com/architects

Implication: in this workflow, ProjectPermit would be too late if inserted at contractor estimate time. Any permit-applicability decision belongs earlier in the architectural/design intake.

This is important negative evidence against assuming that every contractor estimate is an unresolved permit-preflight opportunity.

## Interpretation

The public evidence supports at least two real workflow shapes:

`A. scope -> estimate/quote -> design/permit -> build`

and

`B. scope -> design/permit -> construction estimate -> build`

Therefore:

- quote-stage insertion is **real**, not merely an architectural hypothesis;
- quote-stage insertion is **not universal**;
- a future partner benchmark must record where permit certainty first becomes known;
- contractor/platform total quote volume must not be treated as ProjectPermit call volume until the unresolved-applicability subset is measured.

## Next bounded measurement

For one recent complete month or fixed recent sample, ask a partner:

1. How many current-family Requests/Assessments/Estimates/Quotes entered the workflow?
2. For how many was `permit required?` still unresolved when the estimate/quote was first prepared?
3. For the rest, who/what had already resolved it — homeowner, architect/designer, permit consultant, internal checklist, municipal contact, or existing software?
4. Did municipality/address-specific information ever change the initial generic answer?

The desired E2 denominator is not `quotes/month`; it is:

`quotes where permit applicability is still unresolved at the insertion point / total relevant quotes in the bounded sample`.

A quote-first partner with >=500 current-family candidate events/month would be high-value only if a material share still needs this decision.