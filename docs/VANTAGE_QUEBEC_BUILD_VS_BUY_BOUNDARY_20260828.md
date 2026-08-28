# Vantage Quebec Build-vs-Buy Boundary — 2026-08-28

## Why Vantage is a stronger rescue comparator than a generic Quebec ERP

Vantage is not currently a municipal permit-applicability product. Its importance is that it already implements one of ProjectPermit's proposed differentiation claims inside a low-cost Quebec contractor SaaS:

> **source-linked regulatory answers that refuse to invent an article when no verified source is found.**

That makes Vantage a particularly strong test of whether ProjectPermit's deterministic/auditable evidence contract is actually scarce enough to support a separate external API purchase.

## Current public product

Vantage is a Quebec construction-management platform covering quoting, CRM, project/work-order operations, invoicing and field workflows.

Its AI product publicly offers:

- AI-generated construction quotes from a natural-language job description;
- an in-app regulatory assistant in French;
- answers on RBQ / CCQ / CNESST rules;
- exact article numbers;
- links to official LégisQuébec source text;
- a rule that it only cites articles it actually retrieved;
- explicit fallback behavior: when no verified reference is found, it names the relevant code generally and stops rather than inventing a citation.

Sources:

- `https://vantagesuite.ca/`
- `https://vantagesuite.ca/ai`
- `https://vantagesuite.ca/features`

The currently indexed legal texts include:

- Loi sur le bâtiment;
- Code de construction;
- Code de sécurité;
- CCQ labor-relations law;
- CNESST construction safety code.

Vantage explicitly states that the NRC National Building Code is not indexed and that its AI output does not replace professional judgment.

## Economics are important

The regulatory assistant is included in Vantage's plans from the free trial onward.

Current public pricing includes approximately:

- Pro: **C$68/month annually** (or C$85 monthly) with AI quote generation and regulatory assistant;
- Company: **C$156/month** with unlimited AI quote generation and fuller assistant features.

Source:

- `https://vantagesuite.ca/pricing`

This means `official-source citation + conservative no-fabricated-article behavior` is already bundled at low visible marginal cost inside a contractor operating product.

Therefore ProjectPermit cannot treat evidence links or cautious AI behavior alone as a monetizable moat in Quebec.

## Exact boundary — what Vantage does not publicly show

The focused current scan did not find Vantage publicly claiming to:

- determine whether a municipal building permit is required from project scope/address;
- maintain local permit bylaws across Quebec municipalities;
- answer zoning/urbanism/permit-applicability questions using municipal sources;
- expose this regulatory assistant as a third-party developer API;
- normalize permit decisions across municipalities.

Current public regulation coverage is provincial/industry-code oriented rather than municipal permitting.

Therefore Vantage is **not an exact ProjectPermit competitor today**.

## Why this still directly pressures the Quebec rescue

ProjectPermit's surviving Quebec thesis is not merely `AI can cite sources`; Vantage already does that.

The surviving differentiation is now limited to:

1. **municipal** source maintenance rather than provincial code texts;
2. **cross-municipality** normalization;
3. explicit permit-applicability decision contract;
4. rule/version history and reproducibility;
5. property/overlay uncertainty handling;
6. external reusable API/MCP delivery.

The core commercial question is whether those additional burdens are difficult enough that Vantage would buy them rather than extend its existing source-grounded assistant.

## Build-vs-buy falsification question

ProjectPermit sent Vantage's public support address a narrow question on 2026-08-28:

> If users repeatedly needed municipality-specific `permit required?` answers before a quote is finalized, would Vantage index and maintain municipal rules internally or call an external API that maintains municipal sources, version history and uncertain cases — and why?

No customer data, volume data or proprietary implementation detail was requested.

### Strong negative for ProjectPermit

A credible internal-build preference would materially weaken the Quebec rescue if Vantage says:

- extending its current retrieval/source-citation stack to municipalities is straightforward;
- municipal sources can be indexed cheaply enough;
- a separate API creates avoidable cost/latency/dependency;
- deterministic/versioned output is not sufficiently valuable to customers;
- the permit-applicability question occurs too rarely to justify external procurement.

### Positive rescue evidence

A credible external-buy preference would be meaningful if Vantage says:

- municipal source fragmentation and change tracking are materially harder than provincial LégisQuébec indexing;
- cross-city maintenance is a distraction from the core ERP;
- reproducibility/version history or conservative unknown-state handling adds real value;
- it would prefer a maintained external service at practical economics;
- it would test or allocate resources to an integration if the workflow is repeated.

## Evidence maturity / scale boundary

Vantage's current public pages clearly demonstrate the product and pricing, but the reviewed pages do not provide a bounded customer-count or Quebec quote-volume denominator.

Therefore Vantage should be used as a **build-vs-buy/evidence-contract comparator**, not as a market-size denominator.

The comparison is valuable even without scale because its product architecture closely mirrors the type of source-grounded vertical AI that can absorb local regulatory functions.

## Score implication

**No immediate score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

The existence of Vantage does not itself prove municipal permit applicability is already solved. But it removes another weak differentiation claim: source-linked cautious regulatory AI can already be bundled cheaply inside Quebec contractor software.

A human build-vs-buy response is now potentially score-moving for the **Quebec rescue hypothesis**, even though it would not automatically change the broad canonical score by itself.

## Bottom line

Vantage turns the Quebec rescue into a much narrower proposition:

> **ProjectPermit must prove that maintaining municipal permit rules across Quebec is materially harder and more valuable than the provincial source-grounded regulatory assistant a vertical SaaS can already build and bundle cheaply.**

If Vantage or comparable Quebec software says it would simply extend its existing stack internally, the case for a standalone Quebec API becomes much weaker.