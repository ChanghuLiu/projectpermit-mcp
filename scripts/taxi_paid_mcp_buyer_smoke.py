"""Run exactly one real Base Sepolia x402 payment against UK Taxi/PHV MCP.

Uses the same local EVM_PRIVATE_KEY convention as ProjectPermit buyer smoke.
Never commit or paste the private key. One invocation authorizes at most the
advertised $0.02 Base Sepolia test-USDC preflight and does not retry.
"""
from __future__ import annotations

import asyncio
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

URL = "https://uk-taxi-phv-mcp-production-6ef3.up.railway.app/mcp"
PAY_TO = "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A"
ARGS = {
    "payload": {
        "authority": "City of Bradford Metropolitan District Council",
        "age": 30,
        "driving_licence_years": 4,
        "has_pass_plus_certificate": True,
    }
}


class Adapter:
    def __init__(self, session: ClientSession):
        self._session = session

    async def connect(self, transport: Any) -> None:
        pass

    async def close(self) -> None:
        pass

    async def list_tools(self) -> Any:
        return await self._session.list_tools()

    async def call_tool(self, params: dict[str, Any], **kwargs: Any) -> Any:
        result = await self._session.call_tool(
            name=params.get("name", ""),
            arguments=params.get("arguments", {}) or {},
            meta=params.get("_meta"),
        )
        return to_x402_compatible_result(result)


async def main() -> None:
    key = os.getenv("EVM_PRIVATE_KEY")
    if not key:
        raise SystemExit("EVM_PRIVATE_KEY is not set in this local shell.")

    account = Account.from_key(key)
    print(f"payer={account.address}")
    print(f"paid_mcp_url={URL}")
    print("max_expected_payment=$0.02 Base Sepolia test USDC")

    payment_client = x402ClientSync()
    register_exact_evm_client(payment_client, EthAccountSigner(account))

    async with streamable_http_client(URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"server={init.server_info.name}")

            def approve(ctx: Any) -> bool:
                option = ctx.payment_required.accepts[0]
                print(
                    "payment_required="
                    f"amount={option.amount} asset={option.asset} network={option.network} "
                    f"pay_to={option.pay_to}"
                )
                if str(option.network) != "eip155:84532":
                    raise RuntimeError(f"Unexpected network: {option.network}")
                if str(option.amount) != "20000":
                    raise RuntimeError(f"Unexpected amount: {option.amount}")
                if str(option.pay_to).lower() != PAY_TO.lower():
                    raise RuntimeError(f"Unexpected payee: {option.pay_to}")
                print("payment_approved=true")
                return True

            paid = x402MCPClient(
                Adapter(session),
                payment_client,
                auto_payment=True,
                on_payment_requested=approve,
            )
            result = await paid.call_tool("taxi_licence_preflight", ARGS)
            print(f"payment_made={result.payment_made}")
            print(f"is_error={result.is_error}")

            text = "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in result.content
            )
            if result.payment_response:
                receipt = result.payment_response
                print(f"settlement_success={receipt.success}")
                print(f"settlement_network={receipt.network}")
                print(f"settlement_transaction={receipt.transaction}")
            else:
                raise SystemExit("Settlement receipt missing")

            if result.is_error or not result.payment_made:
                raise SystemExit("Paid MCP call did not complete successfully")
            if not result.payment_response.success:
                raise SystemExit("Settlement failed")
            if str(result.payment_response.network) != "eip155:84532":
                raise SystemExit("Unexpected settlement network")
            if not result.payment_response.transaction:
                raise SystemExit("Settlement transaction id missing")
            if "City of Bradford Metropolitan District Council" not in text:
                raise SystemExit("Bradford result missing")
            if "VERIFIED" not in text:
                raise SystemExit("Expected VERIFIED decision missing")

            print("UK_TAXI_X402_REAL_PAID_BUYER_SMOKE=PASS")


if __name__ == "__main__":
    asyncio.run(main())
