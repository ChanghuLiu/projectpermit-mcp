"""Run exactly one real Base Sepolia x402 payment against ProjectPermit's HTTP discovery twin.

Security: set EVM_PRIVATE_KEY only in your local shell. Never commit or paste it.
The payer wallet must have Base Sepolia USDC. One successful invocation makes one
$0.01 test-USDC payment; do not loop or retry automatically.
"""
from __future__ import annotations

import asyncio
import json
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
    "context": {"client_tag": "projectpermit-owner-smoke"},
    "resolve_address": False,
}


async def main() -> None:
    key = os.getenv("EVM_PRIVATE_KEY")
    if not key:
        raise SystemExit("Set EVM_PRIVATE_KEY in your local shell; never paste it into chat or commit it.")

    account = Account.from_key(key)
    print(f"payer={account.address}")
    print(f"paid_http_url={URL}")
    print("max_expected_payment=$0.01 Base Sepolia test USDC")

    client = x402Client()
    register_exact_evm_client(client, EthAccountSigner(account))
    http_client = x402HTTPClient(client)

    async with x402HttpxClient(client) as http:
        response = await http.post(URL, json=PAYLOAD)
        await response.aread()
        print(f"status={response.status_code}")

        if not response.is_success:
            print(f"response={response.text[:1000]}")
            print("payment_required_header_present=", bool(response.headers.get("payment-required")))
            raise SystemExit("HTTP Bazaar paid smoke did not complete successfully")

        try:
            result = response.json()
        except ValueError as exc:
            raise SystemExit("ProjectPermit HTTP result was not JSON") from exc

        print("tool_result=" + json.dumps(result, sort_keys=True))
        if result.get("determination") != "LIKELY_NOT_REQUIRED":
            raise SystemExit(f"Unexpected determination: {result.get('determination')}")

        settlement = http_client.get_payment_settle_response(
            lambda name: response.headers.get(name)
        )
        if settlement is None:
            raise SystemExit("Missing PAYMENT-RESPONSE settlement receipt")

        print(f"settlement_success={settlement.success}")
        print(f"settlement_network={settlement.network}")
        print(f"settlement_transaction={settlement.transaction}")
        print(f"settlement_amount={settlement.amount}")

        if not settlement.success:
            raise SystemExit(f"Settlement failed: {settlement}")
        if str(settlement.network) != "eip155:84532":
            raise SystemExit(f"Unexpected settlement network: {settlement.network}")
        if not settlement.transaction:
            raise SystemExit("Settlement receipt did not contain a transaction id")

        print("http_bazaar_paid_smoke=PASS")


if __name__ == "__main__":
    asyncio.run(main())
