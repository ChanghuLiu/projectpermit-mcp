# Public workflow frequency + consequence matrix — 2026-08-30

## Purpose

Move Layer-C validation one step closer to a real buyer denominator by separating two questions that were previously mixed together:

1. **Frequency:** how often contractors actually face permit/regulatory work;
2. **Consequence:** whether that work changes quote scope, cost, schedule, professional involvement, documents or inspections.

This note uses public contractor/business/community evidence. It is **not E2** because the observations are not a bounded recent denominator from a ProjectPermit buyer and do not establish willingness to pay for ProjectPermit.

Use it as a denominator proxy and to sharpen the next buyer question.

## Evidence matrix

| Source / persona | Frequency signal | Workflow consequence signal | Evidence class | Key limitation |
|---|---|---|---|---|
| HVAC contractor / small-business discussion | Contractor says company pulls **hundreds of permits/year**; keeps a Dropbox folder per jurisdiction with notes on building-department quirks; 2–3 employees work on permits | Repeated jurisdiction-specific operational knowledge is important enough to maintain a shared internal knowledge base | Strong public frequency proxy | US HVAC; anonymous Reddit; no ProjectPermit WTP |
| California GC / contractor discussion | GC says permits are pulled on **almost everything** | Permit process is part of professional business operating model | Public frequency proxy | US jurisdiction; no bounded monthly job denominator |
| Bay Area contractor | Says permits are pulled **~95% of the time** | Reports one permit fee at 10% of project value, standard bathroom permit ~6 weeks, inspections 3–6 weeks, like-for-like windows ~4 weeks | Strong frequency + cost/schedule consequence proxy | One anonymous contractor; local extreme may not generalize |
| Remodel contractor | Says permits are pulled on **all remodeling projects** but not minor handyman repairs | Permit records/inspections are treated as protection/documentation for larger work | Strong project-family frequency proxy | US; no monthly project count |
| Small residential master plumber/mechanical contractor | Reports **5–10 permits/year** because business is mostly small residential work | Shows low-end denominator for a permit-relevant trade business | Useful lower-bound frequency proxy | Low frequency; anonymous; no consequence amount |
| Coastal SC project manager | Says contractor pulled permits **all the time**, especially due historic-district complications | Permit research/follow-up repeatedly consumed time; commenter claims permit-info gathering could take much of a morning | Frequency + research burden proxy | Later product promotion is self-interested; treat time claim cautiously |
| Toronto/GTA RenoHouse | Says local permit costs differ by municipality and are **factored into every quote** | Jurisdiction-specific permit cost directly enters quote economics | Canadian business workflow evidence | Contractor marketing copy; does not say every job requires a permit |
| GTA HMH Construction | Says engineering, applications and sign-offs are **part of every quote** for its permit-heavy specialty work | Quote includes engineering/permit/inspection scope before work | Canadian high-fit business workflow evidence | Specialty contractor; marketing claim; not general contractor population |
| GTHA TwoBricks | Says every quote itemizes labour, materials, **permits**, HST; permit-first process | Permit cost is a standard quoted cost category and inspections are scheduled before work | Canadian quote-workflow evidence | Marketing copy; permit applicability may vary by project |
| Toronto Smart Renovations | Says every quote includes demolition, **permits**, trades, materials, project management | Warns low quotes often omit permit-related scope; missing permit assumptions create later cost differences | Canadian quote consequence evidence | Marketing content; no observed denominator |
| Calgary OAF Construction | Basement quote guide treats building/electrical/plumbing/HVAC permit costs as essential quote line items | Missing permit line item is presented as a meaningful underquote requiring cost adjustment | Canadian quote consequence evidence | Educational/marketing source; basement-specific |
| GTA structural renovation contractor | Engineering + permit application/fees are included in **every quote** for structural work | Direct professional + permit cost bundled into estimate | Canadian high-consequence specialty evidence | Narrow structural-work segment |
| Toronto contractor quote comparison guidance | Permits/engineering can make quotes diverge materially; missing engineering/permit assumptions can hide **$20K+** | Direct quote scope/cost consequence before contract | Canadian high-consequence proxy | Marketing/educational estimate, not audited transaction data |
| Contractor case anecdote | Signed contract later hit stop order; permit + civil engineer requirements increased expected cost to roughly **4× original amount** | Severe quote/scope/professional consequence | Strong consequence anecdote | One extreme case; no frequency inference |
| Remodel homeowner case | Municipality required HVAC work during remodel, causing roughly **$2,500 change order** | Regulatory requirement created direct scope/cost change | Consequence anecdote | Homeowner report, not contractor denominator |
| Construction discussion | Contractors describe permit lead times as months and some sequence work up to first inspection based on jurisdiction timing | Permit timing changes construction scheduling strategy | Schedule consequence proxy | US; may involve risky practices; no WTP evidence |

## Key source URLs

Community / frequency evidence:

- https://www.reddit.com/r/smallbusiness/comments/x2ehhv/contractor_permitting_requirements_how_do_you/
- https://www.reddit.com/r/Contractor/comments/1nztjm3/as_a_licensed_contractor_do_you_always_pull/
- https://www.reddit.com/r/Contractor/comments/1ch7c4o/what_do_yall_usually_grab_a_permit_for/
- https://www.reddit.com/r/Construction/comments/1j3dz3i/is_it_common_that_a_company_would_do_work_before/

Canadian contractor / quote workflow:

- https://renohouse.ca/faq
- https://hmhconstruction.ca/
- https://twobricks.ca/about/
- https://smartreno4u.ca/kitchen-renovation-toronto/
- https://www.oafconstruction.ca/article/comparing-basement-quotes/
- https://crownstructural.ca/pricing-and-process
- https://maserat.ca/blog/how-to-compare-renovation-quotes-toronto/

## 1. The market is not one frequency bucket

The public evidence rules out a useful but false simplification:

> `one contractor = one expected permit/regulatory check rate`

Observed archetypes span at least three practical bands.

### Low-frequency trade / small residential

Example signal:

- 5–10 permits/year.

Order of magnitude:

- less than one permit/month on average.

A pure high-price per-call API is unlikely to create meaningful direct revenue from this user unless the consequence per event is high.

A low monthly add-on could still work if the value includes convenience/risk reduction, but that requires WTP evidence.

### Permit-relevant remodel / structural / addition contractor

Signals:

- all remodeling projects;
- ~95% of projects;
- engineering/permit/sign-offs included in every quote for specialty contractors;
- permit costs considered during every quote even though not every project ultimately requires a permit.

Likely commercial unit is better modeled around **estimates/projects screened** than permits actually filed.

That distinction matters: ProjectPermit can provide value by returning `LIKELY_NOT_REQUIRED` / missing facts as well as by identifying required permits.

### High-volume multi-jurisdiction contractor/trade company

Signal:

- hundreds of permits/year;
- several employees sharing jurisdiction-specific permit knowledge.

This is the strongest public evidence for a maintained external decision/data layer because the buyer already bears an internal knowledge-maintenance cost.

But it is also the archetype with the strongest internal-build economics.

The product must replace more than a yes/no rule; it must reduce maintained cross-jurisdiction research, freshness and workflow burden.

## 2. The denominator should be `candidate checks`, not `permits issued`

For ProjectPermit, the commercially meaningful workflow starts earlier:

`estimate/job arrives -> contractor must determine whether/what regulation applies -> quote/scope/schedule decision`

Therefore the denominator question should not be:

> How many permits do you pull?

It should be:

> How many estimates/projects make you verify whether a permit, engineer/designer, drawing, inspection or other local requirement applies before you can confidently price or schedule the work?

A project that ends with `no permit required` still consumed the decision workflow.

This matches the public evidence:

- kitchen/remodel contractors sometimes do mostly work that does not require permits but still must know the boundary;
- Canadian quote workflows routinely price permit/engineering assumptions before construction;
- contractors report jurisdiction-specific rules/quirks as a maintained internal knowledge problem.

## 3. Material consequence taxonomy is now well supported

Public evidence independently supports all major Layer-C consequence categories.

### Quote / price

Examples:

- permits and local fees explicitly included in Canadian quotes;
- engineering/permit exclusions can create major apparent quote differences;
- permit/engineering discovery after contract can multiply project cost in extreme cases;
- municipal requirements can create later change orders.

### Scope / professional involvement

Examples:

- structural engineer / civil engineer requirements;
- HVAC/plumbing/electrical requirements;
- drawings and sign-offs;
- professional design responsibilities.

### Schedule

Examples:

- permit processing measured in weeks/months;
- inspection slots measured in weeks;
- contractors actively sequence construction around expected permit/inspection timing.

### Documents / inspections

Examples:

- permit-ready drawings;
- municipality-specific application requirements;
- staged inspections/sign-offs;
- jurisdiction-specific permit-office process quirks.

Therefore the `material consequence` hypothesis is no longer speculative in the abstract.

What remains unproven is **how often these consequences occur inside one buyer's recent bounded workflow**.

## 4. Stronger buyer denominator question

The next buyer question should use a bounded recent sample rather than an abstract monthly estimate.

Preferred wording:

> **Think about your last 20 renovation/construction estimates. For how many did you need to verify a permit, code, engineer/designer, drawing/document, inspection, or other municipality-specific requirement before you could confidently price or schedule the job? Of those, in how many did the answer actually change the quote, scope, schedule, professional involvement, or client handoff?**

Then ask the externalization question:

> **For those checks, do you usually rely on staff knowledge/notes, city websites/calls, a permit specialist, or software? If a maintained API/add-on returned the current requirement with the official source and uncertainty flags, would you rather buy that layer or maintain it internally?**

This yields four numbers/signals from one buyer:

1. bounded candidate denominator out of 20;
2. material-consequence numerator;
3. current replacement behavior/cost;
4. buy-vs-build preference.

That is materially stronger than asking `Would this be useful?`

## 5. Proposed E2 interpretation rule

Do not promote one enthusiastic answer automatically.

A strong E2 candidate should have:

- a bounded recent denominator (e.g. last 20 estimates, last 30 days, or a real monthly range);
- at least several candidate checks, not one freak case;
- at least one recurring material consequence category;
- a current repeated research/maintenance step that can plausibly be replaced;
- preference for external maintained data/software or a clear condition under which they would buy instead of build.

A useful internal heuristic for a contractor account:

- **weak:** <2/20 candidate checks and no material quote/schedule consequence;
- **interesting:** 3–5/20 candidate checks with repeated consequence;
- **strong:** 6+/20 candidate checks or a lower-frequency but very high-cost/risk consequence, plus explicit externalization preference.

These are validation heuristics, not market statistics.

## 6. What this evidence does NOT prove

It does not prove:

- a Canadian average check frequency;
- that public contractor marketing statements equal observed job records;
- that Reddit anecdotes generalize;
- willingness to pay for ProjectPermit;
- a monthly subscription price;
- that Jobber/Buildxact/ServiceM8 users have the same frequency;
- E2, E3, E4 or E5.

## Current decision

This evidence is strong enough to sharpen the buyer gate but not to cross it.

The main uncertainty is no longer:

> Can permit/regulatory requirements ever affect contractor economics?

Public evidence clearly says yes.

The remaining decisive uncertainty is:

> **Within a real buyer's recent estimates, how often does that happen, and will the buyer externalize the maintained jurisdiction decision instead of continuing manual/internal research?**

No E-level change.
