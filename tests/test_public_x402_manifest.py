import os
import unittest

from projectpermit.public_x402_manifest import API_ORIGIN, PAID_ENDPOINT, x402_service_manifest


class PublicX402ManifestTest(unittest.TestCase):
    def test_manifest_matches_commercial_launch_contract(self):
        keys = (
            "PROJECTPERMIT_X402_NETWORK",
            "PROJECTPERMIT_X402_PAY_TO",
            "PROJECTPERMIT_X402_PRICE_USD",
            "PROJECTPERMIT_X402_FACILITATOR_URL",
        )
        previous = {key: os.environ.get(key) for key in keys}
        try:
            os.environ["PROJECTPERMIT_X402_NETWORK"] = "eip155:8453"
            os.environ["PROJECTPERMIT_X402_PAY_TO"] = "0x1111111111111111111111111111111111111111"
            os.environ["PROJECTPERMIT_X402_PRICE_USD"] = "$0.05"
            os.environ["PROJECTPERMIT_X402_FACILITATOR_URL"] = "https://facilitator.payai.network"
            manifest = x402_service_manifest()
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

        self.assertEqual("1.0", manifest["x402"])
        self.assertEqual(PAID_ENDPOINT, manifest["endpoint"])
        self.assertEqual(f"{API_ORIGIN}/openapi.json", manifest["openapi"])
        self.assertEqual(
            {"currency": "USDC", "base": "0.05", "unit": "request"},
            manifest["pricing"],
        )
        self.assertEqual("base", manifest["payment"]["chain"])
        self.assertEqual("eip155:8453", manifest["payment"]["network"])
        self.assertEqual("exact", manifest["payment"]["scheme"])
        self.assertEqual("https://facilitator.payai.network", manifest["payment"]["facilitator"])
        description = manifest["description"].lower()
        for term in ("building permit", "contractors", "ai agents", "official-source evidence"):
            self.assertIn(term, description)

    def test_manifest_requires_base_mainnet_and_pay_to(self):
        previous_network = os.environ.get("PROJECTPERMIT_X402_NETWORK")
        previous_pay_to = os.environ.get("PROJECTPERMIT_X402_PAY_TO")
        try:
            os.environ["PROJECTPERMIT_X402_NETWORK"] = "eip155:84532"
            os.environ["PROJECTPERMIT_X402_PAY_TO"] = "0x1111111111111111111111111111111111111111"
            with self.assertRaisesRegex(RuntimeError, "Base mainnet"):
                x402_service_manifest()

            os.environ["PROJECTPERMIT_X402_NETWORK"] = "eip155:8453"
            os.environ.pop("PROJECTPERMIT_X402_PAY_TO", None)
            with self.assertRaisesRegex(RuntimeError, "PAY_TO"):
                x402_service_manifest()
        finally:
            if previous_network is None:
                os.environ.pop("PROJECTPERMIT_X402_NETWORK", None)
            else:
                os.environ["PROJECTPERMIT_X402_NETWORK"] = previous_network
            if previous_pay_to is None:
                os.environ.pop("PROJECTPERMIT_X402_PAY_TO", None)
            else:
                os.environ["PROJECTPERMIT_X402_PAY_TO"] = previous_pay_to


if __name__ == "__main__":
    unittest.main()
