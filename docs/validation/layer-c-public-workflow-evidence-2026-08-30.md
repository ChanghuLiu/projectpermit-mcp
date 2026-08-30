# Layer C public workflow-fit evidence — 2026-08-30

## Question

Is the proposed Layer C insertion point — before/during estimate or preconstruction scope formation — consistent with how contractors and construction software already work?

This note is **workflow-fit / pain-context evidence only**. It is not direct buyer evidence, does not establish willingness to pay, and does not upgrade E1/E2/E3/E4/E5.

## Evidence

### Jobber: permit cost already belongs inside the construction quote

Jobber's current construction quoting guidance says construction quotes are more complex because of material fluctuation, subcontractor/specialist labour, **permit fees**, and equipment rentals. It recommends including fees such as permits in the total and including a term that allows the quote to be updated when project scope changes.

Source: https://www.getjobber.com/academy/how-to-write-quote-for-job/

Jobber's core product workflow is Request -> Quote -> Job -> Invoice -> Payment, and approved quote line items become the job. That makes quote formation a real operational boundary rather than a marketing abstraction.

Sources:
- https://help.getjobber.com/en/articles/quote-basics/
- https://help.getjobber.com/en/articles/converting-a-quote-to-a-job/

Interpretation: if a regulatory fact changes required scope, professional involvement, permit fee, or sequencing, the useful moment is before the quote hardens into the job.

### Buildertrend: estimate scope/specifications are first-class workflow objects

Buildertrend's Estimate supports detailed scope, cost codes, internal notes, proposals and specifications. Its documentation explicitly says a Specification can be created from an Estimate to document materials, installation details and **additional project requirements**.

Source: https://buildertrend.com/help-article/estimate-overview/

Buildertrend also publicly discusses permit cost codes inside estimating/cost-code practice; one official example notes that some customers create multiple permit cost codes even though Buildertrend recommends simplifying them where possible.

Source: https://buildertrend.com/podcast/the-better-way/s01ep01-cost-codes/

Buildertrend's job record also contains a permit-number field, showing permitting information persists downstream after the estimate stage.

Source: https://buildertrend.com/help-article/job-management/

Interpretation: the target systems already contain the objects a regulatory-obligation result would affect: scope/specification text, cost items, project notes, schedule/job state and permit metadata.

### Municipal responsibility makes the information consequential, not merely informational

The City of Ottawa states that the owner is responsible for ensuring a building permit is obtained and may authorize a contractor/designer to apply; it also states owner and builder/contractor are equally liable under the Ontario Building Code Act. The City explains permits are used to meet building, zoning and related standards.

Source: https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/frequently-asked-questions/building-permits

Interpretation: a permit/regulatory determination can affect real project responsibility and cannot safely be treated as a decorative search result.

### Municipal variation is a recurring real-world property of the workflow

Canadian contractor/renovation guidance repeatedly notes that permit triggers, application documents, inspections and timelines vary by municipality and project scope. Examples:

- Ferguson Brothers (North Vancouver): municipality, scope and specific triggers determine whether a permit is needed; requirements differ across nearby Lower Mainland municipalities.
  - https://fergusonbrothers.ca/articles/renovation-permit-north-vancouver
- Multi Group (Metro Vancouver contractor): supporting-document requirements vary by jurisdiction; contractors integrate application, comment response and inspection coordination into the project workflow.
  - https://multigroup.ca/blog/how-contractors-handle-permits-in-metro-vancouver
- RealCraft's Canadian city guide explicitly warns requirements vary by municipality/project and municipal requirements change over time.
  - https://realcraft.ca/permits/

These are not buyer-volume evidence and include commercial guidance, but they support the basic product premise that one static national checklist is insufficient.

## What this supports

1. **Correct insertion point:** before/during quote and preconstruction scope formation is plausible and aligns with existing software workflow objects.
2. **Useful outputs are not just permit yes/no:** scope implications, permit/approval fees, required documents/professionals, sequencing/inspections and source freshness can affect the quote-to-job handoff.
3. **Integration should be additive:** return structured facts that can populate existing quote/specification/note/job objects rather than trying to replace estimating software.
4. **Platform distribution remains high leverage:** a result that can be inserted into a Jobber/Buildertrend-like quote workflow has a much stronger repeat-call path than a standalone homeowner lookup.

## What this does NOT support

- It does not prove buyers will pay for ProjectPermit.
- It does not establish monthly workflow volume for any specific company/account.
- It does not prove regulatory facts change a material fraction of quotes.
- It does not prove the current 7-city coverage is sufficient.
- It does not justify building Layer C now.

## Falsification question remains unchanged

For a real buyer/software team:

> In a typical month, how many estimates/preconstruction records need current local regulatory requirements before price/scope is finalized, and in how many of those does the answer materially change scope, price, schedule, required professional involvement or handoff?

Until that denominator and consequence are observed from independent buyers/workflows, Layer C remains validation-only.
