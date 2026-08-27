# Jobber Operator Validation Cohort

Updated: 2026-08-27

Status: **research/preparation only — no Canadian operator cold email sent**

Purpose: validate the actual contractor workflow behind the Jobber distribution wedge. Platform/API fit alone is insufficient; this cohort is intended to generate E3 historical benchmark evidence and eventually E4 observed use.

Canadian cold commercial outreach is blocked until `docs/CANADA_OUTREACH_COMPLIANCE.md` is satisfied. Do not use the contacts below as a mass-mail list.

## Priority operator candidates inside current ProjectPermit coverage

### 1. Guest Plumbing & HVAC — Toronto / Mississauga

Why especially strong:

- Jobber's own customer story identifies Guest Plumbing as a real Jobber user and describes its Jobber-based scheduling, client files, job forms, rough-in and finishing checklists.
- Jobber's case study lists 16 employees, providing a more substantial workflow than a one-person contractor.
- Guest's current first-party site says it serves Toronto and Mississauga, both inside ProjectPermit's current rules/address footprint.
- Work includes plumbing, HVAC, replacements, repairs and renovations — several scopes adjacent to existing project families.

Public first-party contact observed: `info@guestplumbing.com`; phone `905-745-1963`. Toronto office: `24E Jutland Road, Toronto`.

Best E3 question: take 20 recent Toronto/Mississauga jobs or quotes that were not routine service-only calls, sample them chronologically rather than choosing interesting examples, and compare whether permit applicability was known immediately or required research/escalation.

Sources:
- https://www.getjobber.com/academy/plumbing/guest-plumbing/
- https://guestplumbing.com/toronto-hvac-plumbing-services/
- https://guestplumbing.com/contact-us/

### 2. GRAVITY HOME SERVICES — Ottawa

Why strong:

- Current Jobber-hosted website directly establishes a Jobber web presence.
- First-party site says it serves Greater Ottawa and advertises heating/cooling, water heaters, boilers, heat pumps, gas lines and installations.
- Current site claims 5,750+ installations and 11,000+ customers. Treat these as vendor marketing claims, not API-call counts, but they indicate enough historical work to draw a meaningful sample.
- Ottawa is fully supported by ProjectPermit's rule and address path.

Public contact: `team@gravityhomeservices.ca`; `613-702-6262`.

Best E3 question: 20 recent installation/replacement quotes, excluding simple repair/maintenance. Ask which required permit confirmation, who made the decision, and whether the answer changed price/schedule/dispatch.

Sources:
- https://gravityhomeservices.jobbersites.com/
- https://gravityhomeservices.ca/

### 3. Trademark Plumbing & Heating Ltd. — Toronto / Mississauga

Why strong:

- Current Jobber-hosted website directly establishes a Jobber web presence.
- Serves Toronto and Mississauga along with the GTA.
- 30+ years of experience creates a useful falsification test: if a highly experienced plumbing operator already knows permit applicability essentially for free, our contractor-side wedge may be weak.

Public contact: `services@trademarkplumbing.ca`; `416-258-8231`.

Best E3 question: 20 recent non-emergency project quotes in Toronto/Mississauga, with an explicit field for `permit answer known from experience vs researched/confirmed`.

Source:
- https://trademark.jobbersites.com/

### 4. Direct Plumbing Limited — Toronto / Mississauga

Why strong:

- Current Jobber-hosted website establishes Jobber usage/web presence.
- Serves Toronto, Vaughan, Markham and Mississauga.
- Licensed plumbing, gas and backflow work creates multiple permit-sensitive categories while retaining a large volume of routine work that should correctly remain `LIKELY_NOT_REQUIRED`/out-of-scope.

Public contact: `info@directplumbing.ca`; `416-450-9886`.

Best E3 question: sample 20 recent estimates spanning repairs, installations, gas/backflow and renovation-related work; do not cherry-pick only projects known to need a permit.

Source:
- https://directplumbinglimited.jobbersites.com/

### 5. 23 Degrees Mechanical Inc. — Toronto / Mississauga

Why strong:

- Current Jobber-hosted website establishes Jobber presence.
- Serves Toronto and Mississauga.
- Services include furnace/AC, water heaters, gas lines, heat pumps, fireplaces and pool heaters — a useful boundary test for what ProjectPermit can and cannot answer today.

Public contact: `info@23degrees.ca`; `437-333-4732`.

Best E3 question: 20 recent installation quotes and classify not only ProjectPermit agreement but also `unsupported trade/permit family`, preventing false success from forcing every job into current building-permit families.

Source:
- https://23degrees.jobbersites.com/

### 6. Invirotech Mechanical Services Inc. — Toronto area

Why useful:

- Current Jobber-hosted site establishes Jobber presence.
- Serves Toronto plus Markham/Vaughan/Richmond Hill/Scarborough/Ajax/Pickering/Whitby.
- Only Toronto is currently in ProjectPermit's supported footprint, making this an excellent geography-boundary experiment.

Public contact: `raffy@invirotechmechanical.com`; `416-676-2062`.

Best E3 question: separate recent Toronto cases from unsupported municipalities. This lets us measure actual Toronto call share before considering any adjacent-city expansion.

Source:
- https://invirotechmechanicalservicesinc.jobbersites.com/

## Benchmark protocol

Do not ask operators to choose “cases where permits were difficult.” That would bias the benchmark upward. Preferred sampling method:

1. choose a recent time window (e.g. last 30 or 60 days);
2. filter to project/installation/renovation quotes rather than maintenance-only visits;
3. take the first 20 chronological records or a reproducible random sample;
4. anonymize customer identity and exact address if the partner cannot share it; municipality + scope is enough for non-address tests;
5. separately mark cases where property-specific/address context was actually needed;
6. record the historical permit decision source: experience, office staff research, city call/site, permit service, customer assumption, unknown;
7. run ProjectPermit without seeing the historical answer;
8. compare after the result is frozen.

## E3 scorecard

For each 20-case cohort capture:

- `usable_case`: enough scope to classify;
- `projectpermit_result`;
- `historical_result` if known;
- `agreement`;
- `material_disagreement`;
- `false_likely_not_required` — highest-severity error;
- `confirm_was_appropriate`;
- `address_resolution_needed`;
- `manual_research_minutes` if known;
- `quote_or_schedule_changed`;
- `unsupported_family`;
- `unsupported_jurisdiction`.

A partner saying “20/20 looks good” without the underlying case structure is not E3.

## Decision tests

The contractor-side wedge becomes materially stronger when at least two independent operators show all of the following:

- representative historical samples, not hand-picked cases;
- a repeated point where permit applicability is not already obvious;
- ProjectPermit has no serious false `LIKELY_NOT_REQUIRED` result in the benchmark;
- the permit decision changes quote, schedule, routing, fee, or escalation behavior;
- a plausible ongoing frequency of at least 20 relevant decisions/month/operator or a clear platform aggregation path.

The wedge becomes weaker if experienced operators consistently say—and historical samples confirm—that permit applicability is obvious from trade/scope, with manual research required only for rare edge cases.

## Next technical bridge

The highest-value prototype is not a full Jobber Marketplace app yet. It is a read-only adapter for a Jobber developer/test account:

`Jobber Quote/Job ID -> property + title/line items -> normalized ProjectPermit request -> result + proposed custom-field write-back`

Keep mutation disabled until the read-only mapping is benchmarked. See `docs/JOBBER_DISTRIBUTION_WEDGE.md`.
