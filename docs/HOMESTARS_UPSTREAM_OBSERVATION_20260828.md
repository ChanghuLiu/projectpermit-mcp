# HomeStars Upstream Permit Observation — 2026-08-28

## Purpose

Test whether a large Canadian home-improvement lead marketplace exposes permit-sensitive project scope **before contractor quote/selection**, and whether permit certainty appears to be a consistently structured part of that upstream posting object.

This is **public observational workflow evidence only**. It is not E2, E3, E4 or E5.

## Current workflow evidence

HomeStars currently describes its homeowner workflow as:

1. **Post your job** — homeowner describes the work;
2. **Pros respond** — the posted job is sent to suitable pros;
3. **Shortlist and get in touch** — homeowner chooses who receives contact details and then discusses/collects quotes.

Current public services include many ProjectPermit-relevant categories, including:

- build or renovate basement;
- build or replace decking;
- build shed / shelter / outbuilding;
- build garage;
- build porch;
- build sunroom;
- kitchen renovation;
- bathroom renovation;
- window work;
- general contracting;
- renovation/construction scopes.

HomeStars currently lists service coverage including Toronto, Ottawa, Mississauga and Vancouver, all inside ProjectPermit's present footprint.

Sources:

- https://www.homestars.com/services
- https://www.homestars.com/pro/register
- https://www.homestars.com/blog/become-a-partner

## Public lead examples observed

The current public pro-registration pages expose sample/live lead snippets. Several are clearly close to ProjectPermit's existing eight families.

### 1. Large skylight / roof opening

Public window-contractor lead asks to create a **large skylight covering much of a flat-roof master-bedroom ceiling**, with a pyramid shape and added height.

ProjectPermit overlap:

- `window_door`;
- likely opening/structural facts matter.

Permit-status observation:

- the public lead text does **not** state that permit applicability is already known.

Source:

- https://www.homestars.com/pro/register/window-contractor

### 2. Interior wall plus new sinks

Public general-contractor lead asks to build a wall beside a countertop/sink, replace the existing sink, add a two-compartment sink and install a separate hand-washing sink.

ProjectPermit overlap:

- `interior_renovation`;
- `kitchen_bath_plumbing`;
- wall/plumbing-change facts are material.

Permit-status observation:

- the public lead text does **not** state that permit applicability is already known.

Source:

- https://www.homestars.com/pro/register/general-contractor

### 3. Shed relocation / re-roofing

Public lead asks to move an existing residential shed, re-roof it, respect a stated one-foot fence distance and account for an easement/backyard context.

ProjectPermit overlap:

- `accessory_structure`;
- property/location facts could matter.

Permit-status observation:

- the public lead text does **not** state that permit applicability is already known.

Source:

- https://www.homestars.com/pro/register/interior-designer

### 4. Garage conversion to livable daycare space

Public lead asks to convert a garage that already has an electrical panel into a **livable space for a home daycare**, adding heat, water, sewer, walls, floors and windows.

ProjectPermit overlap:

- `dwelling_change` / `interior_renovation` / `window_door` / plumbing facts;
- this is a strong example of a project where use/occupancy and municipal review can become material.

Permit-status observation:

- the public lead text does **not** state that permit applicability is already known.

Source:

- https://www.homestars.com/pro/register/interior-designer

### 5. Detached garage exterior package — downstream counterexample

A Toronto-area public carpenter lead asks for siding/aluminum/roofing quotes for a detached garage and explicitly says an **approved floor plan/elevation drawing** is attached.

This is useful negative-channel evidence: at least some HomeStars work enters the marketplace after permit/design approval is already substantially resolved.

Source:

- https://www.homestars.com/pro/register/carpenter

### 6. Major pool renovation

A public lead describes a substantial existing-pool renovation including stairs, equipment replacement and wider concrete surround.

This is outside ProjectPermit's current normalized family set, so it must **not** be counted as current-family SAM. It is included only to demonstrate that HomeStars receives substantial regulatory-sensitive project descriptions before contractor selection.

Source:

- https://www.homestars.com/pro/register/mason

## Direct public user uncertainty signal

A HomeStars question published in June 2026 asks how much time and money are needed to obtain a permit for widening front windows/removing masonry and enlarging a basement egress window in Aurora, Ontario.

This is a current public example of a homeowner entering a project workflow while still seeking permit certainty.

Source:

- https://www.homestars.com/questions/v/577/how-much-time-and-money-need-to-acquire-permit-for-expand-windows-in-aurora

This is anecdotal evidence only, not a denominator.

## HomeStars' own permit guidance confirms the workflow position

HomeStars' current renovation guidance tells homeowners to ask a renovation contractor whether they are familiar with local building-code and permit requirements and says permit need depends on project type and municipality.

That wording places permit certainty close to contractor selection/quote discussion rather than proving it is universally resolved before posting.

Source:

- https://www.homestars.com/home-constructions-renovations/renovation-company-pros

## What the observation supports

It supports a specific integration hypothesis:

> A marketplace that already captures project description before pros quote could compute or request a normalized permit-applicability signal before the lead is distributed, rather than asking every homeowner/contractor to independently interpret municipal rules.

The most interesting potential output is not a consumer permit report. It is structured lead metadata such as:

- `permit_preflight_status`;
- `municipality`;
- `rule_ids` / evidence links;
- `needs_confirmation`;
- missing scope facts needed before a safe decision.

## What the observation does NOT prove

The public snippets do **not** prove that:

- the homeowner actually does not know the permit answer;
- HomeStars does not maintain an internal non-public permit field;
- contractors would pay for the signal;
- permit applicability changes lead routing often enough to matter;
- HomeStars would integrate a third-party capability;
- the visible leads are representative of all postings;
- any particular current-month denominator exists.

Absence of permit text in a public snippet is not equivalent to observed uncertainty.

## E2 request sent

On 2026-08-28, ProjectPermit emailed HomeStars at the public professional-support address `service@homestars.com` and asked for two aggregate ranges for one recent complete month across Toronto + Ottawa + Mississauga + Vancouver:

1. number of residential project postings in renovation/building categories where permit applicability could plausibly matter;
2. share arriving before permit applicability had already been established.

No homeowner names, addresses, records or confidential data were requested.

Evidence state: **awaiting qualifying aggregate reply; E2 remains 0 from this target until then.**

## Decision implication

HomeStars is now a higher-value upstream funnel target than another generic contractor email because:

- scope arrives before quote/contractor selection;
- one platform aggregates many pros and projects;
- current geography overlaps ProjectPermit;
- current-family project types visibly occur in the lead stream.

Do not build a HomeStars adapter until HomeStars or another equivalent platform establishes a bounded >=500/month current-family candidate path or explicitly requests a pilot.