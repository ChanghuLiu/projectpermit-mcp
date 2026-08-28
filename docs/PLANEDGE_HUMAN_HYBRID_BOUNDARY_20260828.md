# PlanEdge Human-Hybrid Delivery Boundary — 2026-08-28

## Why this addendum exists

`docs/PLANEDGE_API_REQUIREMENT_BOUNDARY_20260828.md` records a strong near-exact overlap: PlanEdge publicly says its workflow automatically determines required permits from project type, municipality and scope, and it separately advertises an Open REST API.

A deeper review of the same current public site adds an important counterweight: PlanEdge also describes a materially human-supported permit-management service.

This addendum prevents the scorecard from treating automation language as proof of a pure externally callable requirement engine.

## Current public human-service signals

PlanEdge's main workflow describes **Requirements Research** as a Day 1–2 stage in which `we identify` the exact permit type, fees, schedules and supplementary municipal requirements.

Its current sales material also says:

- a **dedicated permit specialist** is assigned to an account from day one;
- PlanEdge handles AHJ communication on the client's behalf;
- project-based pricing is quoted before work begins;
- enterprise customers can use monthly-retainer arrangements;
- property owners receive a free permit assessment in which PlanEdge assesses the project and identifies the required permits.

The current Terms describe the company as providing **permit management software and services** that assist clients in preparing, submitting and tracking applications.

Source:

- https://www.planedgepermits.com/

## Why this matters

The same public surface therefore supports two facts at once:

1. an automated workflow engine exists and can auto-populate requirement checklists;
2. a dedicated human permit-specialist / managed-service layer is explicitly part of current delivery.

Those facts are compatible. They do **not** prove that the automated requirement layer is an ordinary self-serve machine contract available directly to third-party software.

A plausible current architecture is hybrid:

`software intake / automation + human permit specialist + municipal workflow management`

That architecture is commercially competitive with ProjectPermit at the full-workflow level, but it is not yet evidence that the narrower ProjectPermit contract already exists externally:

`third-party software -> municipality + scope (+ address) -> programmatic permit-requirements determination`

## Scale claims remain vendor claims

The public site continues to claim 444+ municipalities, thousands of permit applications, historical analytics and coast-to-coast delivery. No independent named customer deployment or public API response was found in the current review that verifies the requirement engine itself at that scale.

Anonymous/semi-anonymous testimonials and vendor-written chronology must not be converted into independent production evidence.

## Decision effect

**No score change.**

The correct status remains:

> PlanEdge is a high-threat near-exact competitor with strong public functional claims, but its external requirement-engine machine contract and independent production scale remain unverified.

The canonical kill condition is unchanged: only direct API documentation, a working public machine contract, a substantive PlanEdge confirmation, or independent production evidence should trigger the mandatory score review.

No further broad PlanEdge website research is useful after this addendum. The remaining uncertainty is semantic and delivery-specific, not feature-discovery-specific.
