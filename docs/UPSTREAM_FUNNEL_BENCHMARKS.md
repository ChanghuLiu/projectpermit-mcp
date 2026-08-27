# Upstream funnel benchmark limits

Updated: 2026-08-27

Purpose: constrain how public quote/job conversion data may be used when estimating ProjectPermit candidate-call volume.

The goal is to avoid taking an industry quote-conversion statistic and silently turning it into a Toronto/GTA permit-preflight forecast.

## Public observations

### Buildxact historical residential activity

Buildxact's 2020 residential construction activity reports, based on thousands of Australian builders using its estimating/job-management software, reported quote-to-job win rates around **15%–18%** during the observed COVID-era quarters and an average quote-to-win time around **50 days**.

At a 17% win rate, the arithmetic relationship is roughly:

`1 won job <- 5.9 quotes`

This is old Australian platform data and must not be treated as current Canadian/GTA conversion.

### Buildxact 2026 State of the Customer signal

Buildxact's March/April 2026 public State of the Customer material says estimates sent to clients within two days showed a **32% win rate**.

At 32%, the arithmetic relationship is roughly:

`1 won job <- 3.1 fast-sent estimates`

This is a timing-conditioned Buildxact cohort, not an all-customer Canadian base rate.

### Jobber 2026 home-service survey

Jobber's 2026 Home Service Trends Report says **69% of surveyed pros reported a quote win rate above 50%**, and more than one third reported closing over 70% of quotes. Plumbing, roofing and electrical respondents reported among the highest close rates.

The survey covered 1,050 home-service business owners in the **United States** in December 2025, supplemented by anonymized Jobber platform benchmarks.

A 50%–70% win-rate range corresponds arithmetically to only about:

`1.4–2.0 quotes per won job`

Again, this is not a Canadian permit-sensitive cohort.

## What the range means

Observed public quote funnels span roughly:

- ~1.4 quotes per won job at a 70% close rate;
- 2.0 at 50%;
- ~3.1 at 32%;
- ~5.9 at 17%.

That spread is too wide to justify choosing a single generic `quote -> job` multiplier for ProjectPermit.

Trade urgency, project size, builder type, customer acquisition channel, geography, business maturity and quote response time all materially affect the funnel.

## What this does **not** tell us

None of the observations above directly measures:

- candidate permit-applicability decisions per quote;
- permit-sensitive share of quotes;
- ProjectPermit-covered geography share;
- issued permits per won job;
- multiple sub-trade permits per construction project;
- address-aware share;
- paid conversion.

Therefore do **not** calculate:

`Toronto issued permits × generic quote multiplier = ProjectPermit SAM`

and present it as observed demand.

## Correct use

Use public win-rate data only as a **sensitivity bracket** demonstrating why direct partner measurement is necessary.

The decision-useful E2 metric remains:

> In one recent complete month, in a stated covered geography, how many Requests / Estimates / Quotes / Jobs entered the workflow **before permit applicability was already known**?

Prefer the partner's own aggregate count.

If a partner can only supply quotes and won jobs, record both and calculate its own observed conversion rate for that bounded cohort.

## Relation to Toronto trade-permit evidence

Toronto shows approximately **1.67k–1.73k Mechanical + Plumbing + Drain/Site issued permit revisions/month** across 2023–2025.

That proves persistent downstream trade workflow volume. It does not reveal the upstream quote funnel because:

- one project can carry multiple permit revisions/types;
- some jobs never reach permit issuance;
- some quotes are for scopes requiring no permit;
- some contractors know permit applicability before quoting;
- some projects require permit research before a final quote.

The next evidence step therefore remains an actual Toronto/GTA platform or multi-account operator with a bounded upstream denominator.

## Current decision rule

Do not change the 500 / 2,000 / 10,000 monthly integration gates based on generic quote-conversion reports.

Use those reports only to reinforce why a partner-specific E2 denominator is mandatory before expanding municipalities or building more adapters.