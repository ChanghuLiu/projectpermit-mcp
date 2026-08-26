"""Run one real x402 payment through ProjectPermit's public paid MCP tool.

Security: set EVM_PRIVATE_KEY only in your local shell. Never commit it or paste it
into chat. The payer needs Base Sepolia test USDC.
"""
from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from eth_account import Account
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from x402 import x402ClientSync
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mcp import x402MCPClient

from projectpermit.mcp_v2_x402_compat import to_x402_compatible_result

URL = os.getenv(
    "PROJECTPERMIT_PAID_MCP_URL",
    "https://projectpermit-x402-mcp-production.up.railway.app/mcp",
)

ARGS = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
    "context": {"client_tag": "projectpermit-owner-smoke"},
}


class MCPClientAdapter:
    """Adapter from MCP SDK v2 ClientSession to x402MCPClient."""

    def __init__(self, session: ClientSession):
        self._session = session

    async def connect(self, transport: Any) -> None:
        pass

    async def close(self) -> None:
        pass

    async def call_tool(self, params: dict[str, Any], **kwargs: Any) -> Any:
        result = await self._session.call_tool(
            name=params.get("name", ""),
            arguments=params.get("arguments", {}) or {},
            meta=params.get("_meta"),
        )
        return to_x402_compatible_result(result)

    async def list_tools(self) -> Any:
        return await self._session.list_tools()


async def main() -> None:
    key = os.getenv("EVM_PRIVATE_KEY")
    if not key:
        raise SystemExit("Set EVM_PRIVATE_KEY locally; never paste it into chat or commit it.")

    account = Account.from_key(key)
    print(f"payer={account.address}")
    print(f"paid_mcp_url={URL}")

    payment_client = x402ClientSync()
    register_exact_evm_client(payment_client, EthAccountSigner(account))

    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            adapter = MCPClientAdapter(session)

            def on_payment_requested(payment_context: Any) -> bool:
                option = payment_context.payment_required.accepts[0]
                print(
                    "payment_required="
                    f"amount={option.amount} asset={option.asset} network={option.network} "
                    f"pay_to={option.pay_to}"
                )
                print("payment_approved=true")
                return True

            paid_client = x402MCPClient(
                adapter,
                payment_client,
                auto_payment=True,
                on_payment_requested=on_payment_requested,
            )

            result = await paid_client.call_tool("check_project_requirements", ARGS)
            print(f"payment_made={result.payment_made}")
            print(f"is_error={result.is_error}")

            response_text = "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in result.content
            )
            print(f"tool_result={response_text}")

            if result.payment_response:
                receipt = result.payment_response
                print(f"settlement_success={receipt.success}")
                print(f"settlement_network={receipt.network}")
                print(f"settlement_transaction={receipt.transaction}")
            else:
                print("settlement_receipt=missing")

            if result.is_error or not result.payment_made:
                raise SystemExit("Paid MCP call did not complete successfully")

            try:
                parsed = json.loads(response_text)
            except json.JSONDecodeError as exc:
                raise SystemExit("ProjectPermit tool result was not JSON") from exc
            if parsed.get("determination") != "LIKELY_NOT_REQUIRED":
                raise SystemExit(f"Unexpected determination: {parsed.get('determination')}")

            print("paid_mcp_buyer_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
