# Regulatory Depth Licensing / Cash-Cost Gate — 2026-08-30

## Decision

Do **not** ingest a general Canadian building-code corpus, do **not** reproduce National/Québec code text in a commercial API, and do **not** buy a commercial code licence yet.

The Layer-C hypothesis (`project facts -> current regulatory obligation bundle + source/freshness/change identity`) remains worth validating with buyers, but current official licensing terms show that substantive building-code depth is not automatically a zero-cost data problem.

This document is a product/cost gate, not legal advice. Written licensing clarification is pending from NRC Codes Canada, Québec copyright administration and Ontario's Building and Development Branch.

## 1. National Building Code / NRC — commercial machine use is not currently a free assumption

Official sources checked 2026-08-30:

- NRC terms and conditions: https://cnrc.canada.ca/en/corporate/transparency/terms-conditions
- NRC Publications Archive copyright terms: https://nrc-publications.canada.ca/eng/copyright/
- NRC Codes Canada publications: https://nrc.canada.ca/en/certifications-evaluations-standards/codes-canada/codes-canada-publications
- ISED/NRC deterministic compliance challenge: https://ised-isde.canada.ca/site/innovative-solutions-canada/en/deterministic-artificial-intelligence-assisted-compliance-checking-building-permit-applications

Observed boundary:

- National Codes are available as free electronic PDFs for access/consultation.
- Free access is **not the same thing as a commercial redistribution licence**.
- NRC's general terms state that commercial reproduction requires prior written permission unless another licence applies.
- The NRC Publications Archive terms prohibit commercial use of archive materials under its default access licence and prohibit systematic downloading.
- Most importantly for ProjectPermit, the current ISED/NRC automated-compliance challenge says NRC is **still updating the licensing and distribution approach for commercial use of machine-readable National Codes**.

### Product implication

Until NRC provides written clarification, ProjectPermit must not assume that it can:

- bulk-ingest NBC 2020/2025 into a commercial rule corpus;
- transform the full Code into a machine-readable commercial database;
- use systematic extraction/AI ingestion of National Code text and redistribute derived code content without a licence;
- make full provision text part of the API payload.

A licensing inquiry was sent to Codes Canada on 2026-08-30 asking specifically about a commercial API that returns short structured requirement facts + provision identifiers + source links, and about internal machine extraction/processing.

## 2. Ontario — legal text is relatively permissive, but the Building Code content has a second licensing layer

Official sources checked 2026-08-30:

- Ontario copyright information: https://www.ontario.ca/page/copyright-information
- Open Government Licence – Ontario: https://www.ontario.ca/page/open-government-licence-ontario
- O. Reg. 163/24: https://www.ontario.ca/laws/regulation/240163
- O. Reg. 242/26: https://www.ontario.ca/laws/regulation/r26242
- 2024 Ontario Building Code information: https://www.ontario.ca/page/2024-ontario-building-code
- Building Code Compendium licensing information: https://www.ontario.ca/page/request-digital-copy-2012-building-code-compendium

### Clearly favourable layer

Ontario's King's Printer states that statutes, regulations and judicial decisions may be reproduced without seeking permission and without charge, subject to accuracy, Crown-copyright acknowledgement and non-official-version requirements where applicable.

This makes e-Laws legislation a much lower licensing-risk input than National Code content.

### Important Building Code boundary

The current Building Code is not a self-contained long regulation on e-Laws. O. Reg. 163/24 adopts:

1. the National Building Code of Canada 2020; and
2. the Ontario Amendments to the National Building Code of Canada 2020.

Ontario's Building Code information explains that the Compendium consolidates those sources. Ontario separately states that commercial reproduction/distribution of its Building Code Compendium requires a ministry licence.

Therefore:

> `Ontario statute/regulation reproduction is permitted` does **not** imply `the full Ontario Building Code corpus is automatically free for commercial ingestion/reproduction`.

A licensing inquiry was sent to `buildingtransformation@ontario.ca` on 2026-08-30 asking whether short derived requirement facts/provision identifiers and internal machine processing of the Ontario Amendment/Compendium material require a commercial licence, and what the fee structure is.

### Freshness evidence

This is also a strong maintenance example. Current O. Reg. 163/24 is consolidated from 2026-07-22 and lists amendments including 110/26, 119/26 and 242/26. O. Reg. 242/26 changed the incorporated Ontario Amendment Document date to **2026-07-17**.

This demonstrates that a useful obligation API cannot treat `Ontario Building Code 2024` as one static document version. Version/effective-date identity is a real product requirement.

## 3. Québec — current official terms create the strongest low-cash constraint

Official sources checked 2026-08-30:

- LégisQuébec copyright: https://www.legisquebec.gouv.qc.ca/fr/contenu/droit_auteur
- Québec copyright / reproduction authorization: https://www.quebec.ca/droit-auteur
- RBQ explanatory guide for CNB 2020 modified Québec: https://www.rbq.gouv.qc.ca/fileadmin/medias/pdf/Publications/francais/cahier-explicatif-changements-cnb-2020.pdf

The current LégisQuébec copyright page is unusually explicit:

- reproduction, downloading, storage, adaptation and publication require prior authorization from Publications du Québec and associated royalties may apply;
- publishers, associations and organizations, whether for-profit or not, must obtain authorization before reproducing LégisQuébec information;
- downloading LégisQuébec information for processing by an AI tool or to feed an AI tool also requires prior authorization;
- linking to a law/regulation/page does not require reproduction authorization.

### Product implication

For the current low-cash stage, do **not** build a Québec Layer-C corpus by bulk downloading, storing or AI-processing LégisQuébec content unless written authorization is obtained.

A licensing inquiry was sent to `droitdauteur@mcc.gouv.qc.ca` on 2026-08-30 asking specifically about:

- short structured derived requirement facts;
- provision identifiers and links rather than full text;
- internal script/AI-assisted processing;
- licence type and approximate royalties/fees.

### Freshness / effective-date complexity

RBQ states that Québec Chapter I Building is based on NBC 2020 with Québec modifications, effective **2025-04-17**, but the prior provisions may still be applied where qualifying work begins before **2026-10-17**.

That transition is exactly the type of effective-date state a maintained obligation service would need to model if buyer demand is proven.

It is maintenance/value evidence, not buyer-demand evidence.

## 4. Low-cash architecture boundary

If Layer C eventually passes buyer gates, the data architecture should separate sources by rights/cost rather than create one undifferentiated regulatory corpus.

### Class L1 — clearly reusable legal/open information

Examples:

- Ontario statutes/regulations where the King's Printer reproduction conditions are met;
- government datasets explicitly offered under an applicable open licence;
- municipal first-party facts where reuse terms have been verified.

Potential treatment:

- store normalized facts;
- preserve official source/version identity;
- comply with required attribution/non-official notices;
- monitor freshness.

### Class L2 — reference-only until rights clarified

Examples now include:

- National Building Code commercial/machine-readable content;
- Ontario Building Code Compendium / Ontario Amendment material where the intended commercial machine use has not yet been licensed/clarified;
- Québec LégisQuébec-derived content where reproduction/AI-processing authorization has not been obtained.

Potential treatment during validation:

- do not bulk ingest;
- do not redistribute full text;
- retain links/source identifiers only where linking is permitted;
- do not claim that a derived commercial rule database is legally cleared merely because source documents can be viewed for free.

### Class L3 — paid/licensed content

Only create this class after:

1. buyer E2 volume exists;
2. buyer operational consequence is demonstrated;
3. representative E3 cases show the content materially improves the workflow;
4. expected revenue comfortably exceeds licence + maintenance cost;
5. written licence terms support the intended extraction, storage, transformation and API distribution model.

## 5. Pre-build cash gate

Do not spend money on code-data licensing until both market and economics gates pass.

### Market gate

At minimum:

- one credible software/platform buyer provides a bounded monthly denominator;
- one buyer shows a concrete estimate/scope/schedule/professional-involvement consequence;
- evidence suggests the deeper regulatory layer is preferred externally rather than maintained internally.

### Economic gate

Before any licence purchase, estimate:

`expected monthly gross margin from licensed obligation calls`

against:

`licence/royalty + developer maintenance + source review + compliance overhead`.

A licence that is cheap in absolute dollars can still be a bad choice if the workflow denominator is small.

### Current decision

**$0 committed to new regulatory-content licensing.**

Continue validating Layer C with existing/open/clearly permitted sources and buyer interviews. Treat National/Québec/Compendium content as a licensing dependency, not as a free corpus.

## 6. Current evidence status

| Evidence | Classification | Product effect |
|---|---|---|
| Ontario legal-material reproduction permission | data-cost feasibility | favourable for e-Laws legal layer |
| NRC commercial/machine-readable licensing still unresolved | data-cost risk | block corpus ingestion |
| Québec LégisQuébec AI/reproduction authorization requirement | data-cost risk | block Québec legal corpus ingestion |
| Ontario Building Code incorporates NBC + Ontario Amendments | architecture/licensing boundary | separate legal text from code corpus |
| Ontario 2026 amendment churn | maintenance/freshness evidence | supports version-aware architecture |
| Québec 2025-2026 transition | maintenance/effective-date evidence | supports version-aware architecture |
| SubmitX Layer-C interest | E1 | no score change |
| Contrax Layer-C interest | E1 | no score change |
| External repeated use | E4 = 0 | no score change |
| Payment | E5 = 0 | no score change |

## Bottom line

The source-observability work shows that freshness can be maintained cheaply for much of the municipal layer. The licensing review shows that **deeper building-code content introduces a different cost/rights problem**.

That is useful, not fatal: it gives ProjectPermit a clean sequencing rule.

> **Prove repeated buyer demand first → clarify rights → model licence economics → only then ingest deeper code content.**

Do not reverse that sequence.