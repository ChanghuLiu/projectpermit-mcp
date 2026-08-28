# Quebec Municipal Platform/API Pressure — 2026-08-28

## Purpose

ProjectPermit is already at the **50/100 PAUSE / RE-SCOPE** boundary. This note tests whether the Quebec rescue hypothesis can still rely on `cross-municipality regulatory automation`, `official citations`, or `API integration` as differentiators.

The answer is increasingly **no**.

The remaining rescue thesis must be narrower:

> a contractor/software-facing, upstream `project/address -> permit applicability` machine contract that buyers prefer to purchase externally rather than reproduce inside existing municipal or contractor platforms.

This note records three important supply-side pressures: **Munia**, **PG Solutions / AccèsCité Territoire**, and **Cloudpermit**.

---

## 1. Munia: Quebec municipal regulatory AI is already real, reusable and purchased

### Public product position

Munia / Carange Solutions publicly positions Munia as a Quebec municipal AI platform used by **120+ municipalities, MRCs and public organizations**.

Current public capabilities include municipal/regulatory research, sourced answers, municipality-specific assistants trained on local rules and archives, custom assistants, API/OAuth/custom-schema connectivity, Microsoft 365 integration and automation through external tools.

Sources:

- `https://carangesolutions.com/`
- `https://carangesolutions.com/munia/`
- `https://munia.ai/?r=84569181536`
- `https://munia.ai/application/`

### Independent delivery/adoption evidence

Public municipal council records independently show real Munia licence procurement.

Examples reviewed on 2026-08-28 include McMasterville, Pincourt and Napierville, including municipal licence and training purchases.

Representative sources:

- `https://www.mcmasterville.ca/wp-content/uploads/2025/09/pv-4-aout-2025.pdf`
- `https://villepincourt.qc.ca/uploads/Proces-verbaux/2025/2025-07-08_-_PV_OFFICIEL.pdf`
- `https://www.napierville.ca/fichiersUpload/fichiers/20260217115542-01-301-proces-verbal-2026-01-15.pdf`

Interpretation:

> municipality-specific regulatory AI in Quebec is already a **real purchased capability**, not merely an experimental chatbot category.

### Urbanism / permit relevance

Munia publicly includes an urbanism use case for **preliminary review of permit files** and regulatory research, and supports assistants grounded in a municipality's own regulations and archives.

Source:

- `https://munia.ai/formation-ia-urbanisme-quebec/`

This does **not** prove a standardized external contract such as:

`address + residential scope -> REQUIRED / LIKELY_NOT_REQUIRED / CONFIRMATION_REQUIRED + municipal evidence`

for contractor/proptech products across many Quebec municipalities.

Munia therefore becomes a **high-priority API/buyer-boundary competitor**, not an exact substitute yet.

---

## 2. PG Solutions / AccèsCité Territoire: the strongest Quebec permit-system boundary found so far

### Scale and product position

PG Solutions publicly states that it has served Quebec municipal/MRC software for more than **45 years** and has **1,000+ active clients** across Quebec.

Source:

- `https://pgsolutions.com/`

Its AccèsCité Territoire suite explicitly includes:

- **Permis** — management of permit/certificate requests and issued permits;
- **Urbanisme** — management of urbanism applications, specification grids, usages and standards;
- online permit requests;
- municipal/citizen portal integration through Voilà!;
- automated permit issuance/payment in configured online workflows.

Sources:

- `https://pgsolutions.com/logiciels/`
- `https://pgsolutions.com/2024/02/16/hausse-de-demandes-de-permis-a-prevoir/`

Voilà! is publicly described as allowing citizens to submit municipal permit requests when connected to AccèsCité.

Sources:

- `https://play.google.com/store/apps/details?id=com.pgsolutions.smartcity`
- `https://www.valdavid.com/services-aux-citoyens/voila/`

### Independent deployment evidence

Public municipal procurement records confirm real permit-module deployment. Examples include municipalities/MRCs purchasing AccèsCité Territoire and online-permit modules, including a 2025 MRC contract for the permit/inspection software and multiple municipal renewals/implementations.

Representative sources:

- `https://www.nouvellebeauce.com/wp-content/uploads/2025/09/001-3100-PV-2025-06-18-sans-signature.pdf`
- `https://saintpaul.quebec/storage/app/media/proces-verbaux/pv-2022/pv-2022-02-07-vf.pdf`
- `https://www.veniseenquebec.ca/storage/app/media/municipalite/conseil-municipal/proces-verbaux/2021/2021-04%20%20Proc%C3%A8s%20verbal%20assembl%C3%A9e%20ordinaire%20du%206%20avril%202021.pdf`

### API / interoperability evidence

The reviewed public material shows that PG Solutions permit data/workflows can participate in third-party integrations.

A 2026 GetApp review for eZsign explicitly cites an **API with PG Solutions for permits in AccèsCité Territoire**, and the vendor response acknowledges the permit integration.

Source:

- `https://www.getapp.ca/software/2079711/ezsign`

PG Solutions contract/support materials also reference exports/bridges to external systems and broader modernization with third-party APIs.

Important boundary:

> current public evidence proves **permit-system integration**, not a public upstream applicability/requirements endpoint.

The scan did **not** find public documentation showing that third-party contractor software can call:

`municipality/address + work scope -> whether a permit is required + relevant permit type/rule`

before a permit request/dossier exists.

### Why PG Solutions is especially important

PG Solutions is more strategically relevant than a general municipal AI vendor because it is already a **Quebec permit/urbanism system of record** at substantial scale.

If its existing APIs can expose configured permit/urbanism rules or required permit categories before application creation, the Quebec rescue thesis would weaken sharply: the authoritative municipal platform could already supply the same layer directly.

A direct boundary question was sent to `ventes@pgsolutions.com` on 2026-08-28 asking whether current APIs expose pre-application permit applicability/requirements or mainly integrate existing permit dossiers/workflows.

Until that is verified, PG Solutions is classified as:

> **HIGH-PRIORITY QUEBEC EXACT-BOUNDARY TARGET — NOT YET A CONFIRMED UPSTREAM SUBSTITUTE**.

---

## 3. Cloudpermit: mature Canadian permitting software already combines local-code AI, requirements and APIs

Cloudpermit is a mature Canadian local-government permitting platform. Its Building Permitting product publicly supports configurable permit/application requirements, public/contractor portals, AI assistance through NoVa, municipality-specific code content, automatic issuance for eligible routine permit types, GIS/property integration and API access.

Sources:

- `https://cloudpermit.ca/products/building-permitting`
- `https://cloudpermit.ca/products/planning`
- `https://cloudpermit.ca/customers`

Cloudpermit's Land Use Permits product bridges land-use permits and building permits and configures forms/attachments from permit category/work type.

Sources:

- `https://support.cloudpermit.com/support/solutions/articles/67000710781-land-use-permits-description`
- `https://support.cloudpermit.com/support/solutions/articles/67000719157-land-use-permits-product-features`

### API boundary

Cloudpermit's public API one-pager documents these API families:

- Workspaces;
- Attachments;
- Inspections;
- Property;
- Payments.

API service is contract-enabled and supports training/test integration before production.

Sources:

- `https://cloudpermit.ca/hubfs/US%20One-Pagers/What%20Cloudpermits%20API%20Can%20Do%20for%20You.pdf?hsLang=en-ca`
- `https://cloudpermit.ca/products/building-permitting`

The current public documentation does **not** show a pre-workspace `should this project require a permit?` endpoint.

A direct question was sent to a publicly listed Cloudpermit sales contact on 2026-08-28 asking whether configured requirements or NoVa local-code knowledge can be called before an application/workspace exists.

### Quebec-specific boundary

The focused search did not identify a public Quebec municipality customer in Cloudpermit's current customer material. It remains a strong **future/platform substitution pressure**, not a demonstrated Quebec exact competitor.

---

## 4. Citadel is not an exact permit competitor

Citadel is Quebec-developed municipal SaaS with a secure, documented REST API that lets third-party applications interact with municipal data.

Sources:

- `https://www.citadelapp.com/fr/plateforme/connectivite-et-integration`
- `https://www.citadelapp.com/fr/a-propos/securite`

However, the current reviewed product is municipal asset-management / maintenance software, not a demonstrated permit-applicability engine.

Citadel therefore proves that Quebec municipalities already operate open/integrated SaaS ecosystems, but it should **not** be counted as permit competition without stronger evidence.

---

## 5. What this does to the Quebec rescue thesis

The rescue thesis can no longer rely on any of these claims:

- Quebec municipal regulatory AI is undeveloped;
- municipalities cannot maintain local-rule AI;
- source-grounded regulatory answers are scarce;
- API connectivity into municipal software is unusual;
- permit-system interoperability is absent;
- cross-municipality reuse of regulatory-assistant technology is inherently difficult.

The only remaining plausible value proposition is:

> **a reusable external contractor/software API that turns a normalized renovation scope + municipality/address into a conservative permit-applicability decision, with evidence/versioning/unknown-state safety, and that is cheaper or safer for buyers than extending their own existing AI/regulatory stack or integrating directly with municipal systems of record.**

That proposition is still unvalidated.

---

## 6. New rescue falsification questions

### PG Solutions

Can a third-party contractor/proptech product call the configured AccèsCité Permit/Urbanisme logic **before a permit dossier exists** and obtain required permit/approval information?

Negative/kill signal:

- yes, at practical economics/coverage across many Quebec municipalities.

Positive/rescue signal:

- APIs remain record/workflow integrations only, and independent software buyers still identify an upstream decision gap.

### Munia

Can municipality-specific regulatory assistants / permit-related logic be exposed to third-party contractor, marketplace or proptech products rather than municipality-owned workflows?

### Cloudpermit

Can NoVa/local-code configuration or permit-category/requirements logic be called programmatically by external contractor software before an application workspace exists?

---

## Score impact

**No immediate score change.**

ProjectPermit remains **50/100, PAUSE / RE-SCOPE**.

Competitive headroom is already at **0/10**. The evidence does not yet justify another defensibility downgrade because PG Solutions, Munia and Cloudpermit still do not publicly prove the exact third-party upstream deterministic contract.

However, the rescue burden is materially higher:

- source citations are not a moat;
- municipal AI is not a moat;
- API integration is not a moat;
- permit-system interoperability is not a moat;
- reusable local-regulation technology is not a moat.

Only **validated external buyer preference for the narrow upstream contract** can rescue the project.

## Bottom line

Quebec still contains a public-market gap, but it is now extremely specific.

The highest-priority exact competitor check is now **PG Solutions / AccèsCité Territoire**, followed by Munia and Cloudpermit API boundaries.

Do not restart engineering because these products leave a schema-level difference.

The next decisive evidence must be one of:

1. a real multi-customer Quebec software/platform buyer with >=500 qualifying monthly events and explicit external buy preference;
2. a vendor confirmation that an existing platform already exposes the same upstream capability, which would push the rescue toward No-Go;
3. repeated paid/external usage proving buyers actually select ProjectPermit despite the existing municipal/vertical AI stack.
