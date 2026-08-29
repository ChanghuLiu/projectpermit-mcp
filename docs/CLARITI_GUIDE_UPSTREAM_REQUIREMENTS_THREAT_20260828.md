# Clariti Guide Upstream Requirements Threat — 2026-08-28

## Why this is different from CivCheck

The CivCheck / Clariti score review reduced ProjectPermit defensibility from 2/10 to 1/10 because a reusable commercial platform can maintain and calibrate regulatory/code logic across multiple jurisdictions, achieve independently measured municipal-review accuracy and distribute through established govtech channels.

That review deliberately left 1/10 because CivCheck's public workflow is primarily **downstream**: applicants already know the permit/application type and submit documents for completeness/code-compliance pre-check.

A separate Clariti product, **Clariti Guide** (formerly Camino Development Guide), closes much of that upstream distinction.

Guide is explicitly a **pre-application permitting assistant** rather than a plan-review engine.

## Current product contract

Clariti's current Guide product page says Guide:

- answers permitting questions online before application;
- uses GIS to determine the rules/regulations applying to a project based on **zoning and work planned**;
- supports location-based alerts based on the project's parcel;
- uses an address/project type to determine property-specific conditions;
- calculates fees and expected timelines upfront;
- can operate standalone or integrate with another permitting system;
- lets municipal staff build/edit decision logic with a visual no-code rule builder.

Clariti's current explanatory material describes the applicant flow more explicitly:

1. the applicant answers project questions such as location, submission type and valuation;
2. Guide processes those facts;
3. the applicant receives a personalized summary/instructions;
4. the result includes what permits and supporting documents are needed, how to apply, fees and likely approval timing.

Sources:

- https://www.claritisoftware.com/products/guide
- https://www.claritisoftware.com/blog/the-5-ingredient-recipe-for-plan-review-and-permitting-success
- https://www.claritisoftware.com/blog/how-this-permitting-tool-can-help-you-cut-counter-visits-by-70-percent

That contract is materially closer to ProjectPermit than CivCheck:

`location / parcel + project details -> applicable rules + permits / process / requirements`

It is not identical to ProjectPermit's deterministic output schema, but it occupies the same upstream pre-application decision space.

## Cross-jurisdiction replication is a product feature

Guide's **Community Templates** allow agencies to clone other customers' configurations rather than build every permit path from zero.

Clariti currently describes:

- a shared library of **thousands of permit-type configurations**;
- Clariti-built starter templates;
- cloning another jurisdiction/customer configuration with a click;
- editing the copied configuration to fit the local jurisdiction;
- a visual rules engine requiring no coding;
- implementations where permit types can go live in weeks.

Clariti Launch exposes the same broader Community Templates model across permit types, rules, steps and workflows.

Sources:

- https://www.claritisoftware.com/products/guide
- https://www.claritisoftware.com/products/launch-permitting-software

This is directly relevant to the residual ProjectPermit thesis because cross-jurisdiction requirements knowledge is no longer demonstrated only as handcrafted one-city logic. A commercial permitting vendor has explicitly productized reuse/cloning of local permit configurations.

## Independent government deployment evidence

### McKinney, Texas

The current City of McKinney Development Services website directs users to its **Development Navigation Assistant (DNA)**:

> create an account, answer questions about your project, and receive a custom step-by-step guide to permitting your project.

The City's Home Repairs & Permit Information page directs residents to DNA specifically in the context of knowing which repairs require permits.

McKinney's own archived development-services material says DNA was designed as a question-and-answer resource providing a custom step-by-step guide for residential projects through the permitting process.

Official sources:

- https://www.mckinneytexas.org/3563/Development-Services
- https://www.mckinneytexas.org/3350/Home-Repairs-Permit-Information
- https://www.mckinneytexas.org/Archive.aspx?ADID=2505

Clariti identifies McKinney DNA as a Clariti Guide / former Camino Guide deployment. The City-side evidence above independently verifies that the product is actually present in the current municipal workflow.

### Bainbridge Island, Washington

The current City of Bainbridge Island permitting page tells applicants to use the **Clariti Permit Guide** and says the Guide provides prompts based on **project type and GIS mapping tools**. It is available without an account.

Official source:

- https://www.bainbridgewa.gov/1287/Permitting

These government pages are stronger than vendor-only customer logos: they show live municipal use of a project-specific pre-application guide.

## Canadian delivery boundary

Clariti is a Canadian-headquartered company and has current Canadian permitting deployments/selections, including:

- Municipality of Colchester, Nova Scotia — Clariti Launch is the municipality's online permit system;
- Municipality of the County of Kings, Nova Scotia — public procurement selected Clariti Launch for a system whose requested capabilities included helping residents/developers gather requirements related to a project;
- Revelstoke, British Columbia — Clariti publicly announced selection of Launch + Guide for community-development workflows.

Sources:

- https://colchester.ca/permits
- Municipality of the County of Kings 2025 permitting-software award report
- https://www.claritisoftware.com/blog/revelstoke-bc-selects-clariti-launch

Evidence strength must remain separated:

- Colchester and Kings are independently published municipal/procurement evidence for Clariti permitting presence in Canada;
- the current Revelstoke Launch + Guide evidence located in this review is a Clariti vendor announcement quoting the City's development-services manager, not an independently crawled City implementation page.

Therefore do not claim that the exact Guide upstream workflow has already been independently verified in a Canadian municipality. What is verified is that the same vendor/platform family is commercially present in Canada and that Guide's upstream workflow is independently used by North American municipalities.

## Why this removes the final defensibility point

After the CivCheck downgrade, ProjectPermit's remaining 1/10 defensibility was framed around its exact upstream contract shape:

- scope/project facts before application;
- municipality/property specificity;
- maintained rules;
- deterministic/evidence-versioned/fail-safe output;
- low-cost developer-native machine delivery.

Clariti Guide now demonstrates that the **upstream pre-application requirements layer itself** is already productized across jurisdictions:

- project questions before formal application;
- parcel/GIS context;
- tailored applicable rules;
- permit/supporting-document requirements;
- cloneable permit configurations across agencies;
- no-code local rule maintenance;
- real municipal deployments.

What remains different about ProjectPermit is mostly contract implementation:

- deterministic rule IDs/version metadata;
- fail-safe unknown states;
- developer API/MCP/x402 instead of a government-facing Guide product;
- proposed very low per-call economics.

None of those differences currently has E2/E4/E5 evidence showing that a buyer treats it as a moat or would choose/pay for ProjectPermit because of it.

Commercial defensibility should therefore not receive a positive point merely because the exact JSON/API shape differs from a delivered upstream product.

## Canonical score impact

**Defensibility: 1/10 -> 0/10.**

Weighted contribution:

- before: 1.0 / 10;
- after: 0.0 / 10.

Total raw score:

- before: **48.5 / 100**;
- after: **47.5 / 100**.

Displayed score:

> **48 / 100**

Decision remains:

> **PAUSE / RE-SCOPE — NO FURTHER PRODUCT INVESTMENT; RESCUE / FALSIFICATION ONLY**

This still does not create an irreversible No-Go by itself. The user/buyer question remains unresolved: a private software buyer may value a lightweight external developer-native machine contract differently from a municipality buying/configuring Clariti Guide.

But that preference must now be proven externally. It cannot be counted as existing defensibility.

## Why this is not double-counting CivCheck

CivCheck and Guide attack different parts of the residual thesis:

- **CivCheck:** proves reusable cross-jurisdiction regulatory maintenance, calibration, municipal accuracy evidence and govtech distribution can be productized;
- **Clariti Guide:** proves the upstream pre-application project/location-to-permit-requirements guidance layer can also be productized and reused across jurisdictions.

The CivCheck deduction intentionally stopped at 1/10 because CivCheck was downstream. Guide is the evidence that removes that remaining upstream assumption.

## What could still rescue the project commercially

With defensibility at 0/10, rescue cannot come from feature uniqueness. It must come from evidence that a specific buyer/channel values ProjectPermit's delivery contract enough to create a business despite available alternatives, for example:

- a software buyer explicitly prefers an external API/MCP over municipal/Clariti-style tools for a concrete integration/maintenance reason;
- an E5 buyer commits money or integration resources at useful economics;
- repeated E4 usage shows independent software/agent demand for the developer-native contract;
- representative E3 cases demonstrate an accuracy/safety advantage buyers actually care about;
- meaningful covered-geography call volume exists where current external/first-party alternatives do not fit.

Without that evidence, deterministic rule IDs, MCP/x402 and low per-call pricing are implementation differences, not a demonstrated moat.