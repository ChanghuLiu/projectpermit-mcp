import os
import unittest
from unittest.mock import patch

from projectpermit.public_agent_manifest import BASE_USDC_CONTRACT, agent_manifest


class PublicAgentManifestTest(unittest.TestCase):
    def _manifest(self):
        env = {
            "PROJECTPERMIT_X402_PRICE_USD": "$0.05",
            "PROJECTPERMIT_X402_BATCH_PRICE_USD": "$2.00",
            "PROJECTPERMIT_X402_NETWORK": "eip155:8453",
            "PROJECTPERMIT_X402_PAY_TO": "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A",
            "PROJECTPERMIT_X402_FACILITATOR_URL": "https://facilitator.payai.network",
        }
        with patch.dict(os.environ, env, clear=False):
            return agent_manifest()

    def test_manifest_is_tier2_post_x402_discovery(self):
        manifest = self._manifest()
        self.assertEqual("1.3", manifest["version"])
        self.assertEqual(
            "projectpermit-api-v2-production.up.railway.app",
            manifest["origin"],
        )
        self.assertEqual(
            "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A",
            manifest["payout_address"],
        )

        network = manifest["payments"]["x402"]["networks"][0]
        self.assertEqual("base", network["network"])
        self.assertEqual("USDC", network["asset"])
        self.assertEqual(BASE_USDC_CONTRACT, network["contract"])
        self.assertEqual("https://facilitator.payai.network", network["facilitator"])

        intents = {intent["name"]: intent for intent in manifest["intents"]}
        single = intents["check_building_permit_requirements"]
        batch = intents["check_building_permit_requirements_batch"]
        self.assertEqual("POST", single["method"])
        self.assertEqual("/v1/check-project-requirements", single["endpoint"])
        self.assertEqual(0.05, single["price"]["amount"])
        self.assertEqual("POST", batch["method"])
        self.assertEqual("/v1/check-project-requirements-batch", batch["endpoint"])
        self.assertEqual(2.0, batch["price"]["amount"])

    def test_manifest_reuses_public_seller_discovery_links(self):
        manifest = self._manifest()
        ext = manifest["extensions"]["projectpermit"]
        self.assertTrue(ext["openapi"].endswith("/openapi.json"))
        self.assertTrue(ext["x402_manifest"].endswith("/.well-known/x402-service.json"))
        self.assertEqual(7, ext["jurisdictions"])

    def test_manifest_rejects_non_base_commercial_network(self):
        env = {
            "PROJECTPERMIT_X402_NETWORK": "eip155:84532",
            "PROJECTPERMIT_X402_PAY_TO": "0xDAAef0FD525278aAD0bA11066A96c338642A3d1A",
        }
        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(RuntimeError, "Base mainnet"):
                agent_manifest()


if __name__ == "__main__":
    unittest.main()
