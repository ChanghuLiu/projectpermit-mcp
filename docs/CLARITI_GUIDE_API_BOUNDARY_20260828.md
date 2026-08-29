# Clariti Guide External API Boundary — 2026-08-28

## Question

After Clariti Guide reduced ProjectPermit commercial defensibility to 0/10, the remaining commercial distinction is not feature uniqueness. It is delivery shape:

> Does a private software/agent buyer need a lightweight developer-native permit-applicability machine contract, or can existing upstream permitting platforms already expose the same result programmatically?

Clariti/Camino is the highest-value current test because Guide already productizes:

`project details + parcel/location -> permits / rules / supporting requirements`

## Public API infrastructure is real

The legacy/current Camino developer portal is still publicly reachable at:

- https://developer.oncamino.com/

It is an **Azure API Management** developer portal and exposes navigation for APIs and Products.

The portal states that users must be an **organization user with the proper documentation access permissions** to view API documentation.

The unauthenticated `/apis` route does not expose API names or schemas. The public `/products` route could not be reliably retrieved in the current crawl.

Therefore it is safe to say:

- Camino/Clariti has formal API-management infrastructure;
- API documentation is organization-gated;
- the public web does not currently reveal whether Guide decision outputs are among the exposed APIs.

Do **not** infer a Guide API merely because the developer portal exists.

## Integration claims are still not endpoint proof

Clariti's current Guide product page says Guide:

- can be used as a standalone tool;
- can be integrated with any permitting software.

Clariti Enterprise separately advertises flexible APIs for integrating permitting-system data with other software.

Those facts establish that the Clariti product family is integration-capable. They do **not** establish this machine contract:

`third-party software -> project/location facts -> Guide permit/requirements result`

Public sources reviewed do not show:

- a Guide API endpoint name;
- request/response schema;
- a sample external call;
- authentication/pricing for a Guide-decision API;
- a third-party private software company consuming Guide requirements outside a municipality-owned deployment.

## Old Camino product language confirms exact upstream functionality, not API availability

The still-indexed Camino Development Guide product page is highly relevant to product overlap. It explicitly asks:

> `Which permits do I need?`

and describes a flow of:

1. smart project questionnaire;
2. location / parcel-based checks;
3. a unique customized instruction set.

It says Guide helps applicants determine whether a project is allowed and which permits may be required, including permits across multiple departments.

Source:

- https://camino.ai/solutions/development-guide

That strengthens functional overlap but still does not expose a public developer contract.

## Decision boundary

### Current status

**Guide upstream functionality: verified.**

**Formal Camino/Clariti API infrastructure: verified.**

**Externally callable Guide determination API: unverified.**

No additional score reduction is possible because defensibility is already 0/10. The canonical score remains **48/100 (raw 47.5)**.

### Serious No-Go-strengthening evidence

The delivery-preference thesis becomes materially weaker if a future public document, authorized API documentation or substantive Clariti confirmation establishes that ordinary third-party software can:

1. send project type/scope + address/parcel facts;
2. receive required permit(s), applicable rules or Guide instructions programmatically;
3. do so across multiple configured jurisdictions;
4. obtain the service at economics/integration friction reasonable for private software buyers rather than only municipal enterprise implementations.

That would not change defensibility below zero, but it would strengthen the case for moving from `PAUSE / RE-SCOPE` toward `No-Go` because the last meaningful delivery-shape distinction would be occupied.

### Hold condition

Keep the current decision if:

- APIs are only for applications/status/documents/workflow data;
- Guide can integrate only inside municipality-owned systems;
- Guide decision APIs require bespoke municipal implementation and are not a reusable third-party machine contract;
- public API semantics remain permission-gated/unknown.

## Research stop rule

Do not guess hidden endpoints, attempt unauthorized login, infer API semantics from Azure API Management alone, or keep broad-searching Clariti marketing pages.

The remaining question is now narrow enough to resolve only through:

- authorized/public API documentation;
- a legitimate product/business response;
- a public procurement/integration document that names the Guide decision API;
- a verified third-party software integration using Guide requirements output.

Until one of those appears, return effort to buyer preference, E3, E4 and E5 evidence.