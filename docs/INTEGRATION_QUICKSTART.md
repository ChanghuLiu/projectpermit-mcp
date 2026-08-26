# ProjectPermit Integration Quickstart

Updated: 2026-08-26

ProjectPermit is a deterministic, evidence-linked municipal permit preflight service. It is **not** a municipality, permit issuer, legal opinion, engineering review or authorization to begin work.

## Live endpoints

- Capabilities / status: `https://projectpermit-api-v2-production.up.railway.app/v1/capabilities`
- Paid HTTP preflight: `https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`
- Standard MCP developer preview: `https://projectpermit-mcp-production.up.railway.app/mcp`
- x402 paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The current x402 price is **$0.01 Base Sepolia test USDC**. It is a testnet discovery price, not commercial pricing.

## 1. Discover capabilities for free

```bash
curl -s https://projectpermit-api-v2-production.up.railway.app/v1/capabilities
```

Use this endpoint before calling a paid transport. It returns the supported jurisdictions, project families and which jurisdictions currently support first-party municipal address resolution.

## 2. Request shape

Minimal example:

```json
{
  "jurisdiction": "ottawa_on",
  "project": {
    "family": "window_door",
    "action": "replace_same_size"
  },
  "property": {
    "heritage": false
  },
  "resolve_address": false
}
```

Address-aware example:

```json
{
  "jurisdiction": "vancouver_bc",
  "address": "<civic address>",
  "resolve_address": true,
  "project": {
    "family": "interior_renovation",
    "action": "painting"
  }
}
```

For developer validation, integrations may include a stable **non-PII** tag:

```json
{
  "context": {
    "client_tag": "your-integration-dev"
  }
}
```

The server hashes `client_tag` before telemetry logging. Do not put a person's name, email, civic address, token, API key or other secret in this field.

## 3. Standard MCP developer preview

The standard MCP endpoint currently exposes `check_project_requirements` without x402 payment so developers can validate workflow fit before commercial packaging is locked.

This is a **temporary developer-validation preview**, not a promise of permanent free production access.

Python MCP client example:

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://projectpermit-mcp-production.up.railway.app/mcp"

async def main():
    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "check_project_requirements",
                {
                    "jurisdiction": "toronto_on",
                    "project": {
                        "family": "window_door",
                        "action": "replace_same_size",
                        "single_dwelling_house": True,
                        "structural_change": False,
                        "new_exit": False
                    },
                    "context": {"client_tag": "your-integration-dev"}
                },
            )
            print(result.structured_content)

asyncio.run(main())
```

## 4. Paid HTTP / x402 behavior

A request without payment receives HTTP `402 Payment Required` plus the x402 v2 `PAYMENT-REQUIRED` challenge. An x402-compatible buyer can sign the authorization, repeat the request with `PAYMENT-SIGNATURE`, and receive the structured result after facilitator verification/settlement.

The canonical resource is:

```text
https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements
```

Current testnet profile:

```text
network=eip155:84532
asset=0x036CbD53842c5426634e7929541eC2318f3dCF7e
price=$0.01 test USDC
```

Never put a wallet private key in application source, Git, issue trackers or chat. Buyer signing material stays on the buyer side.

## 5. x402 paid MCP

The paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid tool

The tool returns a payment challenge through MCP metadata when called without an x402 payment. x402-aware MCP clients can authorize the payment and repeat the tool call automatically.

## 6. Supported jurisdictions

Current rules footprint:

- `gatineau_qc`
- `ottawa_on`
- `toronto_on`
- `mississauga_on`
- `laval_qc`
- `longueuil_qc`
- `vancouver_bc`

Current first-party address/GIS resolution:

- Gatineau
- Ottawa
- Toronto
- Mississauga
- Vancouver

Use `GET /v1/capabilities` rather than hard-coding this list because coverage will change.

## 7. What to integrate first

The highest-value workflow is not a homeowner asking a one-time question. Integrate ProjectPermit at a repeated decision point, for example:

- contractor job intake -> permit preflight before quote/schedule
- property work order/capex project -> preflight before approval/vendor dispatch
- construction estimate/project setup -> preflight before design/submission workflow
- permit-management platform -> upstream routing before full application research

ProjectPermit should answer **whether deeper permit work is likely required and why**, then hand off to a municipal portal, permit-management system or human professional when required.

## 8. Result contract

Typical result fields include:

- `jurisdiction`
- `determination`
- `requirements[]`
- stable `rule_id`
- official-source `evidence[]`
- `confidence`
- `engine_version`
- `address_context` when requested/supported
- safety disclaimer

Expected conservative states include `REQUIRED`, `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, `MUNICIPAL_CONFIRMATION_REQUIRED` and `OUT_OF_SCOPE`.

A confirmation result is intentional. The engine should not silently convert incomplete municipal guidance into a false no-permit answer.

## 9. Developer validation signal

If you are testing workflow fit, the useful feedback is:

- which platform/workflow is calling
- project families you need
- jurisdictions you need
- expected calls/month if integrated
- whether address-aware evidence is worth roughly `$0.20-$0.50` per result or an equivalent monthly plan

The next municipality expansion is intentionally driven by repeated usage/design-partner demand rather than by city count alone.
