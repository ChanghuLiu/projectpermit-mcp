"""Regression smoke for x402 settlement meta across MCP SDK v2 naming."""
from types import SimpleNamespace

from projectpermit.mcp_v2_x402_compat import to_x402_compatible_result
from x402.mcp.utils import convert_mcp_result, extract_payment_response_from_meta

raw = SimpleNamespace(
    content=[SimpleNamespace(type="text", text="ok")],
    is_error=False,
    meta={
        "x402/payment-response": {
            "success": True,
            "transaction": "0xabc",
            "network": "eip155:84532",
            "amount": "10000",
        }
    },
    structured_content={"determination": "LIKELY_NOT_REQUIRED"},
)

converted = convert_mcp_result(to_x402_compatible_result(raw))
receipt = extract_payment_response_from_meta(converted)
assert receipt is not None
assert receipt.success is True
assert receipt.transaction == "0xabc"
assert receipt.network == "eip155:84532"
print("x402_mcp_v2_receipt_smoke=PASS")
