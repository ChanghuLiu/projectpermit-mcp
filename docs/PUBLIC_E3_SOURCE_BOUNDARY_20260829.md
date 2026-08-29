# Public E3 Source Boundary — 2026-08-29

## Purpose

ProjectPermit still needs a representative E3 benchmark containing real chronological project scopes plus the actual `permit required / not required / other approval` outcome that existed in the source workflow.

Public-data research on 2026-08-29 tested whether this benchmark could be constructed without a partner. The answer is currently **no** for the reviewed Canadian public sources.

This boundary exists to prevent issued-permit records, FAQs, selected municipal examples or unrelated 311 cases from being relabeled as representative E3 evidence.

## What E3 would require

A useful public E3 source would need all of the following:

1. a real proposed project/scope, not a synthetic example;
2. a municipality/location;
3. enough facts to map the case conservatively into ProjectPermit's existing families;
4. a final or contemporaneous applicability outcome such as `building permit required`, `building permit not required`, or a clearly identified alternative approval;
5. chronology or a sampling frame that prevents cherry-picking;
6. enough cases to evaluate false-negative patterns rather than one anecdotes.

## Reviewed public routes

### Issued building-permit datasets

Toronto/Vancouver and similar open permit datasets can supply real permit-positive scopes. They are useful technical **positive controls** and ProjectPermit already uses that pattern for safety canaries.

They cannot provide permit-negative cases because the dataset is conditioned on a permit application/issuance event.

Therefore:

> issued permits are not representative E3 applicability samples.

### Toronto 311 service-request open data

Toronto's public 311 customer-initiated service-request dataset publishes request type, status, responsible division and coarse location/status information for participating service divisions.

The reviewed public dataset does not provide a Toronto Building pre-application scope together with a resolved `permit required / not required` determination. A generic `Closed` service-request status means the service request was handled; it is not a permit-applicability outcome.

Therefore 311 rows cannot safely be converted into E3 labels.

### Ottawa Development Information Officer inquiries

Ottawa explicitly provides an upstream Development Information Officer service for users who supply a subject address, proposed use and relevant project information, with a response normally returned by phone/email.

This is strong workflow evidence that real pre-application clarification occurs.

However, no reviewed public open dataset exposes those private inquiries with their project facts and final applicability outcome.

Therefore the DIO workflow is demand/pain evidence, not a public E3 case source.

### Maple Ridge Building Permit Inquiry

The public Maple Ridge `Building Permit Inquiry` service is an application/status lookup for permits already in the permitting system. It supports permit number/address/date/type/status lookups.

It is downstream of the applicability decision and does not expose pre-application `permit required / not required` outcomes.

### Municipal FAQs / `When do I need a permit?` pages

Toronto, Ottawa and other municipalities publish high-quality lists of common required/not-required work.

These are authoritative rule/guidance sources and can support rule implementation or spot checks. They are not historical project observations and have no representative sampling frame.

Therefore they cannot be counted as E3 cases.

### Development inquiry / planning application records

Public development-inquiry or planning-application records tend to describe larger development proposals and application processes. They are not representative of ProjectPermit's current residential renovation families and are generally already within a formal planning/application workflow.

They should not be used to manufacture a residential permit-applicability benchmark.

## Current conclusion

**Public representative E3 route: CLOSED with currently reviewed sources.**

Do not reopen this route merely by finding another issued-permit table, FAQ, 311 status dataset, permit-application tracker, or selected public case study.

Reopen only if a public source appears that exposes actual pre-application project facts plus a resolved applicability outcome with a defensible chronological/sampling frame.

## What still counts as a valid E3 path

The preferred E3 route remains a partner/operator supplying a chronological anonymized sample such as:

- recent renovation quotes/projects;
- the original scope facts available at the decision point;
- municipality;
- actual permit/no-permit/other-approval outcome or staff decision;
- cases supplied in chronological order rather than selected for ProjectPermit.

Contractors and upstream software/platform operators are therefore still the best E3 source.

## Decision impact

**No score change.** Canonical remains **48/100 — PAUSE / RE-SCOPE**.

Closing an invalid evidence route is not negative market evidence. It simply prevents false confidence. Representative E3 remains **0** and must come from a source that actually observes both the project and the decision outcome.