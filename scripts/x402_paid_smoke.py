"""Run one real Base Sepolia x402 payment against ProjectPermit.

Security: set EVM_PRIVATE_KEY only in your local shell. Never commit or paste it.
The payer wallet must have Base Sepolia USDC (and a little test ETH if its
wallet/provider needs gas for unrelated wallet operations; x402 exact uses an
EIP-3009 authorization and the facilitator settles it).
"""
from __future__ import annotations

import asyncio
import os

from eth_account import Account
from x402 import x402Client
from x402.http import x402HTTPClient
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

URL = os.getenv(
    "PROJECTPERMIT_URL",
    "https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements",
)

PAYLOAD = {
    "jurisdiction": "ottawa_on",
    "project": {"family": "window_door", "action": "replace_same_size"},
    "property": {"heritage": False},
}


async def main() -> None:
    key = os.getenv("EVM_PRIVATE_KEY")
    if not key:
        raise SystemExit("Set EVM_PRIVATE_KEY in your local shell; never paste it into chat or commit it.")

    account = Account.from_key(key)
    print(f"payer={account.address}")
    print(f"url={URL}")

    client = x402Client()
    register_exact_evm_client(client, EthAccountSigner(account))
    http_client = x402HTTPClient(client)

    async with x402HttpxClient(client) as http:
        response = await http.post(URL, json=PAYLOAD)
        await response.aread()
        print(f"status={response.status_code}")
        print(response.text)
        if response.is_success:
            settlement = http_client.get_payment_settle_response(
                lambda name: response.headers.get(name)
            )
            print(f"settlement={settlement}")
        else:
            print("payment-required=", bool(response.headers.get("payment-required")))
            raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
