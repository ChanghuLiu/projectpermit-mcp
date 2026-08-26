# ProjectPermit / BuildRequirements

ProjectPermit is an evidence-linked municipal permit preflight engine for construction and renovation projects. **BuildRequirements** is the deterministic rules engine inside it.

## Current jurisdiction coverage

Phase 0 release-readiness is complete for the original proving ground:

- `gatineau_qc`
- `ottawa_on`

Phase 1A added:

- `toronto_on`
- `mississauga_on`

Phase 1B adds conservative deterministic coverage for:

- `laval_qc`
- `longueuil_qc`

The engine covers 8 normalized project families, preserves uncertainty instead of guessing, attaches official-source evidence to every rule result, and exposes the same jurisdiction router through HTTP, standard MCP, and x402-paid MCP.

First-party municipal address/GIS resolution is available for Gatineau, Ottawa, Toronto and Mississauga. Laval and Longueuil currently support rule preflight with `resolve_address=false` while reliable no-cost property adapters are evaluated.

The engine deliberately does **not** call an LLM. A calling agent normalizes natural-language scope into structured facts; BuildRequirements applies deterministic municipal rules.

## Live endpoints

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The HTTP API also exposes free machine-readable capability discovery at `GET /v1/capabilities`.

The paid MCP exposes a free `projectpermit_info` tool and the paid `check_project_requirements` tool. The current **testnet discovery price** is **$0.01 USDC** on Base Sepolia (`eip155:84532`); it is not the intended commercial price.

The result is a preflight information package, **not municipal authorization, legal advice, engineering certification, or building-code design approval**.

## Market thesis

The business target is not a homeowner-only `Do I need a permit?` wizard. ProjectPermit is intended to become a **cross-jurisdiction permit-requirements intelligence layer** for contractor, property-management, construction/design, permitting, and real-estate software Agents.

The Phase 0 payment/discovery plumbing is proven. The next validation risk is whether external B2B workflows generate enough repeated paid calls to justify maintaining more municipal rule adapters.

See `docs/MARKET_VALIDATION.md` for the call-volume model, competitive analysis, pricing thesis, expansion-city scorecard, and demand gates.

## Architecture

All transports now call the same shared address-aware preflight pipeline:

`HTTP / free MCP / x402 paid MCP -> preflight_service -> municipal address/GIS adapters -> jurisdiction router -> deterministic rules`

Resolved non-null municipal property facts can enrich a request before rule evaluation. Unknown overlays remain unknown and never silently overwrite an explicit caller value.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn projectpermit.api:app --host 127.0.0.1 --port 8000
```

For standard MCP support:

```bash
pip install -e '.[mcp]'
projectpermit-mcp
```

`projectpermit-mcp` uses MCP Python SDK v2 Streamable HTTP, JSON responses, and stateless HTTP. It listens on `127.0.0.1:8001` by default. Override with `PROJECTPERMIT_MCP_HOST` and `PROJECTPERMIT_MCP_PORT`.

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## API

`POST /v1/check-project-requirements`

Example:

```json
{
  "jurisdiction": "toronto_on",
  "resolve_address": false,
  "project": {
    "family": "window_door",
    "action": "replace_same_size",
    "single_dwelling_house": true,
    "structural_change": false,
    "new_exit": false
  }
}
```

For an address-aware jurisdiction, set `resolve_address=true` and supply `address`; the same behavior is available through standard MCP and paid MCP.

## Repository map

- `src/projectpermit/engine.py` — original Gatineau/Ottawa deterministic rules
- `src/projectpermit/expansion_rules.py` — Toronto/Mississauga Phase 1A rules
- `src/projectpermit/quebec_expansion_rules.py` — Laval/Longueuil Phase 1B rules
- `src/projectpermit/jurisdiction_router.py` — public jurisdiction dispatcher
- `src/projectpermit/preflight_service.py` — shared address-aware preflight pipeline
- `src/projectpermit/address.py` — Gatineau/Ottawa/Toronto address/GIS adapters
- `src/projectpermit/mississauga_address.py` — Mississauga address/property adapter
- `src/projectpermit/api.py` — HTTP API
- `src/projectpermit/mcp_server.py` — standard MCP v2 server
- `src/projectpermit/paid_mcp_server.py` — x402-native paid MCP v2 server
- `src/projectpermit/mcp_v2_x402_compat.py` — MCP SDK v2 / x402 result compatibility shim
- `data/source_manifest.json` — official source registry/freshness metadata
- `schemas/` — public request/response schemas
- `scripts/paid_mcp_unpaid_smoke.py` — no-cost remote payment-challenge test
- `scripts/paid_mcp_buyer_smoke.py` — real buyer-side testnet paid MCP call
- `scripts/facilitator_capability_probe.py` — no-cost facilitator capability matrix
- `scripts/projectpermit_bazaar_lookup.py` — read-only Bazaar catalog lookup
- `docs/PHASE0_SPEC.md` — original product/engineering scope
- `docs/PHASE0_RELEASE_READINESS.md` — completed Phase 0 release gate
- `docs/MARKET_VALIDATION.md` — market size, monthly-call model, pricing and expansion gates
- `docs/X402_ARCHITECTURE.md` — payment/discovery design

## x402 / Bazaar status

The canonical paid HTTP resource is:

`https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`

It is indexed by the current Bazaar-capable facilitator canary with canonical HTTPS discovery metadata. A real buyer-side HTTP call and a real paid MCP call have both completed successfully with server-side verification and settlement.

The current paid MCP / Bazaar canary facilitator is:

`https://facilitator.goplausible.xyz`

No additional paid smoke calls should be made merely to prove plumbing that has already passed.

## CI / verification

Current CI covers:

- Python 3.11 + 3.13
- deterministic jurisdiction-rule and schema tests
- shared address-aware preflight service regressions
- official source-manifest contracts
- MCP v2 integration
- x402 wire behavior
- MCP v2 settlement-receipt compatibility
- Docker build + live `/health`
- public multi-jurisdiction MCP tool invocation
- public paid-MCP unpaid challenge
- facilitator capability checks
- canonical HTTPS Bazaar catalog state

See `STATUS.md` and `docs/PHASE0_RELEASE_READINESS.md` for release evidence and `docs/MARKET_VALIDATION.md` for the business gates.

## Safety boundary

Determinations intentionally use preflight language such as `REQUIRED`, `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, and `MUNICIPAL_CONFIRMATION_REQUIRED` where uncertainty exists. Ambiguous official thresholds are conservatively routed to confirmation instead of being silently resolved.

The engine should not be presented as a municipality, permit issuer, lawyer, architect, or engineer.
