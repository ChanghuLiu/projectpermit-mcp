# ServiceM8 Distribution Wedge

Updated: 2026-08-27

## Decision

ServiceM8 is the current **#2 embedded field-service distribution experiment** after Jobber.

It is not selected because it is proven to have the largest TAM. It is selected because it offers an unusually low-friction technical validation path for a low-cash independent developer while exposing exactly the work-object fields ProjectPermit needs.

## Why ServiceM8 is attractive now

Current official ServiceM8 material establishes:

- a REST API at `https://api.servicem8.com/api_1.0/`;
- **Private Applications** can use an API key to connect to the developer's own ServiceM8 account or one specific customer's account;
- a ServiceM8 Developer account is **not required** to use a private API key;
- API keys are created in ServiceM8 under `Settings -> API Keys`;
- private API requests use the `X-API-Key` header;
- Public Applications use OAuth 2.0 and can later add webhooks, platform UI integration and other capabilities;
- a public application does not have to be listed publicly in the Add-ons Directory;
- ServiceM8 offers a Free plan at `$0/month`, 1 user, up to 30 jobs/month;
- every plan includes core job cards, quotes, invoices and scheduling.

The unresolved detail is whether API-key creation is exposed on the Free plan in the current account UI. Do not assume this until verified in a real account. Even if it is not, the public Developer Partner/OAuth path remains documented.

## Workflow fit

ServiceM8's `Job` object directly exposes:

- `uuid`;
- `status` — `Quote`, `Work Order`, `Unsuccessful`, or `Completed`;
- `job_address`;
- `job_description`;
- auto-geocoded location fields.

The documented `GET /api_1.0/job/{uuid}.json` and `GET /api_1.0/job.json` endpoints require the `read_jobs` OAuth scope for public apps and accept API-key authentication for private integrations.

ServiceM8's REST naming guide also maps quote/invoice line items to `JobMaterial`. `GET /api_1.0/jobmaterial.json` requires `read_job_materials` for OAuth applications.

This creates a natural ProjectPermit flow:

`ServiceM8 Quote/Work Order -> job_address + job_description (+ optional JobMaterial names) -> structured ProjectPermit facts -> deterministic preflight -> proposed routing result`

## Why quote-time is the preferred surface

ServiceM8 uses the same Job record through stages including `Quote` and `Work Order`. That makes quote-time attractive because:

- the civic address already exists;
- scope text already exists;
- permit uncertainty can change price, schedule, fee assumptions or escalation;
- the contractor does not need a second homeowner-facing permit website;
- the same record can later transition into work-order execution.

The first prototype should accept both `Quote` and `Work Order`, but prioritize measuring quote-stage usefulness.

## Read-only privacy boundary

The initial ProjectPermit adapter should extract only:

- source platform;
- job UUID;
- job status;
- civic job address;
- job description;
- optionally scope-relevant JobMaterial names/descriptions when explicitly supplied to the adapter.

It should ignore:

- customer/client identity;
- phone/email;
- billing address;
- invoice/payment data;
- staff/assignee data;
- prices/costs unless a future deterministic permit rule explicitly requires project cost and the user knowingly supplies it.

No ServiceM8 write mutation is needed for technical validation.

## Private vs Public integration path

### Phase S0 — private own-account validation

Preferred cheapest path:

1. create a ServiceM8 account;
2. check whether the current Free plan exposes `Settings -> API Keys`;
3. create a private API key if available;
4. create several synthetic jobs/quotes in the account;
5. use read-only GET requests only;
6. run ProjectPermit against those own-account jobs.

This does not prove market demand. It only validates the live API contract.

### Phase S1 — public Development Partner path

For multi-customer distribution:

1. register as a ServiceM8 Development Partner;
2. create a Public Application / Add-on;
3. implement OAuth 2.0;
4. request the minimum required scopes (`read_jobs`; add `read_job_materials` only if line-item detail materially improves classification);
5. add webhooks/UI integration only after E3/E4 shows real repeated value.

Do not request broad customer/payment scopes merely because they exist.

## Comparison with the other current platform candidates

### Jobber — #1

Advantages:

- strong Canadian/home-service relevance;
- Request/Quote/Job/Property workflow fit;
- current read-only ProjectPermit adapter already implemented;
- larger apparent distribution opportunity.

Constraint:

- Jobber's Marketplace-oriented testing guidance says not to engage existing Jobber customers for testing before coordinating with a Jobber developer representative.

Therefore Jobber remains #1 strategically, but the next live-account step has an external/manual platform gate.

### ServiceM8 — #2

Advantages:

- own-account private API-key path is explicitly documented;
- no Developer account required for that private path;
- free ServiceM8 plan exists;
- Job object exposes address + description + quote/work-order status directly;
- public OAuth path exists for later scale.

Main uncertainty:

- actual ServiceM8 market penetration in ProjectPermit's current Canadian municipalities is not yet established;
- API key availability on the Free-plan UI still needs live verification.

### ServiceTitan — #3 technical/platform opportunity

ServiceTitan provides third-party developer access and a standard-data integration environment once access is granted. Its potential distribution scale is strong, but it requires developer access/approval before the environment can be used. Keep it as a high-leverage later channel rather than the cheapest immediate prototype.

### Housecall Pro

Housecall Pro has a documented API and partner/OAuth route, but the customer-side custom API feature is associated with higher-tier plans and verified Integration Partners require a formal partner path. It is currently less attractive for a zero/low-cash own-account prototype than ServiceM8.

### Workiz

Workiz exposes a public REST API and API token pattern, but current account/add-on availability, Canadian workflow relevance and partner-distribution mechanics need more validation before it outranks ServiceM8.

## Technical validation gates

- [ ] read-only ServiceM8 adapter + tests
- [ ] read-only API-key client + tests
- [ ] synthetic/de-identified integration benchmark
- [ ] real own-account API key and live `GET job` probe
- [ ] verify Free-plan API-key availability in the current UI
- [ ] verify whether `job_description` alone is usually enough or JobMaterial data materially improves scope normalization

The first four are technical gates only. None count as market E3/E4 unless independent real operator data/usage is involved.

## Market validation gates

After technical fit:

- obtain representative historical scopes from independent operators using ServiceM8 or an equivalent field-service workflow;
- measure candidate permit-decision jobs/month, not total ServiceM8 jobs;
- measure whether permit applicability required research/escalation;
- measure whether the determination changed quote, schedule, fees or routing;
- observe repeated external calls;
- do not infer TAM directly from ServiceM8's global job-value marketing numbers.

## Falsification test

ServiceM8 should be downgraded if any of these become true:

- Canadian supported-city usage is too small to create a meaningful distribution path;
- API/private-key access requires material recurring spend before any useful validation;
- job descriptions are systematically too sparse to classify permit scope without high-friction manual input;
- experienced contractors already know applicability with near-zero research effort;
- integration would need broad sensitive customer/billing data to work.

## Official sources reviewed 2026-08-27

- Authentication / Private & Public Applications: https://developer.servicem8.com/docs/authentication
- REST overview: https://developer.servicem8.com/docs/rest-overview
- Add-on types: https://developer.servicem8.com/docs/add-on-types
- List Jobs: https://developer.servicem8.com/reference/listjobs
- Retrieve Job: https://developer.servicem8.com/reference/getjobs
- Job field documentation: https://developer.servicem8.com/reference/createjobs
- List Job Materials: https://developer.servicem8.com/reference/listjobmaterials
- ServiceM8 pricing: https://www.servicem8.com/pricing
