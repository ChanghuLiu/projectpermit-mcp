# Quebec Upstream E2 Targets — 2026-08-28

## Why this note exists

The Permitio human reply recorded in `docs/PERMITIO_DOWNSTREAM_INTAKE_BOUNDARY_20260828.md` makes one validation mistake clear:

> once a contractor job is deliberately routed into a permit-filing workflow, permit need/type may already be known.

ProjectPermit therefore needs evidence **one or two steps earlier** — where a homeowner/project scope first enters a quote/referral/estimate workflow.

The best Quebec rescue evidence now comes from platforms that simultaneously have:

1. project/service description before contractor routing;
2. province-wide or multi-contractor aggregation;
3. enough public scale to plausibly produce >=500 qualifying calls/month;
4. a human/operator who can provide a recent bounded denominator and unresolved-permit subset.

This note adds two such targets.

---

## 1. Québec Rénovation

Public site:

- `https://quebecrenovation.com/`
- `https://quebecrenovation.com/contact/`

### Public workflow

The site says the homeowner:

1. selects the service that matches the project;
2. answers several project questions and provides project details;
3. receives estimates from local contractor partners in roughly 24–48 hours.

That means the platform has a structured project record **before contractor estimates are returned**.

### Public scale claim

The current homepage displays:

- **12k demandes/année**;
- **985 partenaires**;
- **100k clients satisfaits**.

Treat these strictly as vendor-provided scale claims, not E2 evidence.

### Current-family relevance

The platform explicitly lists project categories overlapping ProjectPermit's current families or close proxies, including:

- finition/rénovation de sous-sol;
- construction de garage;
- agrandissement / construction;
- balcon, patio et terrasse;
- portes et fenêtres;
- plomberie résidentielle;
- cuisine / salle de bain;
- rénovation générale.

### Why the arithmetic is promising enough to ask

12,000 requests/year is about **1,000 requests/month** across all categories.

To clear ProjectPermit's minimum Quebec rescue threshold of 500 qualifying calls/month, roughly half of total monthly requests would need to both:

- map into relevant current families; and
- still require a permit-applicability decision.

That is a high bar, so the public scale claim **does not itself rescue the product**.

However, the platform is large enough that a bounded answer can efficiently falsify or support the hypothesis.

### Question sent

On 2026-08-28, ProjectPermit emailed `info@quebecrenovation.com` asking for two recent complete-month buckets:

1. current-family-like project requests;
2. how many still required someone to determine municipal permit applicability before routing to contractors.

Requested buckets:

- `<50`
- `50–99`
- `100–249`
- `250–499`
- `500+`

No customer names, addresses or PII were requested.

### Decision rule

Positive/rescue evidence requires a real bounded answer, not confirmation that permits are sometimes confusing.

A strong result would be:

- >=500 qualifying unresolved events/month, or
- a smaller but clearly repeated denominator plus integration/economic evidence and a path to aggregate multiple equivalent networks.

Negative evidence includes:

- permit applicability is not checked at this stage because it does not affect routing/quotes;
- the owner/contractor generally already knows;
- current-family share is low;
- unresolved cases are rare or primarily outside current coverage.

---

## 2. Besoindunentrepreneur.com / Optilog

Public sources:

- `https://www.besoindunentrepreneur.com/`
- `https://besoindunentrepreneur.com/entrepreneurs/`
- `https://besoindunentrepreneur.com/politique-de-confidentialite/`

### Public workflow

The service describes itself as a province-wide bridge between consumer construction/renovation requests and contractors.

A request is routed to registered contractors according to:

- service / contractor type;
- location;
- project need.

The privacy policy confirms collection can include substantial upstream project/property context such as:

- project type;
- budget;
- region;
- property type and characteristics;
- construction date;
- renovation/maintenance history;
- plans/images.

This is structurally favorable for an applicability call because the platform may possess enough context **before contractor routing**.

### Public scale claim

The site states **30,000 entrepreneurs inscrits au Québec**.

This is only a contractor-network denominator. It does not publish a clean recent project-request count, so it cannot be converted into ProjectPermit call volume.

### Question sent

On 2026-08-28, ProjectPermit emailed `info@optilog.com` asking for the same bounded upstream evidence:

1. recent complete-month current-family-like residential requests;
2. how many still required a person to determine permit applicability before contractor routing.

Again, no PII or customer-level data was requested.

### Decision rule

This target upgrades the Quebec rescue only if it provides a bounded workflow claim or representative cases.

A response such as `we have 30,000 contractors` or `permits are important` remains E0/E1 and does not alter the score.

---

## 3. Why these targets rank above more downstream permit vendors

A downstream permit vendor has strong selection bias:

- jobs arrive because someone already decided to start a permit workflow;
- an expediter's volume is therefore mostly permit-positive by construction.

An upstream quote/referral platform is much more diagnostic because it sees both:

- projects that eventually require permits;
- projects that do not;
- potentially uncertain projects before contractor commitment.

That is the denominator ProjectPermit needs.

Therefore future outreach priority should be:

1. province-wide renovation/intake marketplaces;
2. contractor software at quote/proposal stage;
3. multi-account implementers/integrators;
4. neutral representative industry research;
5. only then downstream permit vendors, and mainly for boundary/competitive questions rather than incidence.

---

## Score impact

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

The new targets are evidence routes, not evidence themselves.

The Quebec rescue still requires a bounded chain:

`upstream real workflow -> current-family denominator -> unresolved permit share -> representative cases -> repeat external calls -> economic signal`

Until that chain begins, do not add Montreal, Quebec City, new families or speculative integrations.
