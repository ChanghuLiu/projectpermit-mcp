import unittest
from types import SimpleNamespace

from projectpermit.mcp_v2_x402_compat import to_x402_compatible_result


class MCPV2X402CompatTest(unittest.TestCase):
    def test_preserves_meta_and_structured_content(self):
        raw = SimpleNamespace(
            content=[SimpleNamespace(type="text", text="ok")],
            is_error=False,
            meta={
                "x402/payment-response": {
                    "success": True,
                    "transaction": "0xabc",
                    "network": "eip155:84532",
                }
            },
            structured_content={"determination": "LIKELY_NOT_REQUIRED"},
        )
        bridged = to_x402_compatible_result(raw)
        self.assertFalse(bridged.is_error)
        self.assertEqual(bridged.content, [{"type": "text", "text": "ok"}])
        self.assertEqual(
            bridged._meta["x402/payment-response"]["transaction"], "0xabc"
        )
        self.assertEqual(
            bridged.structuredContent["determination"], "LIKELY_NOT_REQUIRED"
        )


if __name__ == "__main__":
    unittest.main()
