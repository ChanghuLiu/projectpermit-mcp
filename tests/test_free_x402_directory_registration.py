import unittest
from unittest.mock import Mock

from scripts import register_free_x402_directories as registration


class FreeX402DirectoryRegistrationTest(unittest.TestCase):
    def _manifest(self):
        return {
            "x402": "1.0",
            "description": "Building permit requirements API for contractors and AI agents.",
            "pricing": {"currency": "USDC", "base": "0.20", "unit": "request"},
            "payment": {
                "address": "0x1111111111111111111111111111111111111111",
                "chain": "base",
                "network": "eip155:8453",
                "facilitator": "https://facilitator.payai.network",
                "scheme": "exact",
            },
            "endpoint": registration.CANONICAL_PAID_ENDPOINT,
        }

    def test_manifest_gate_accepts_approved_launch_contract(self):
        registration._validate_manifest(self._manifest())

    def test_manifest_gate_rejects_price_or_network_drift(self):
        manifest = self._manifest()
        manifest["pricing"] = {"currency": "USDC", "base": "0.05", "unit": "request"}
        with self.assertRaisesRegex(RuntimeError, "launch pricing"):
            registration._validate_manifest(manifest)

        manifest = self._manifest()
        manifest["payment"]["network"] = "eip155:84532"
        with self.assertRaisesRegex(RuntimeError, "payment network"):
            registration._validate_manifest(manifest)

    def test_registration_refuses_directory_payment_request(self):
        response = Mock()
        response.status_code = 402
        response.text = "payment required"
        client = Mock()
        client.post.return_value = response
        with self.assertRaisesRegex(RuntimeError, "requested payment"):
            registration._register(client, "directory", "https://example.invalid/register", {})

    def test_registration_accepts_success_and_idempotent_conflict(self):
        for status in (200, 201, 202, 409):
            response = Mock()
            response.status_code = status
            response.text = "ok"
            client = Mock()
            client.post.return_value = response
            self.assertEqual(
                "accepted",
                registration._register(client, "directory", "https://example.invalid/register", {}),
            )

    def test_registration_treats_rate_limit_as_transient(self):
        response = Mock()
        response.status_code = 429
        response.text = "too many registrations"
        client = Mock()
        client.post.return_value = response
        self.assertEqual(
            "transient_failure",
            registration._register(client, "directory", "https://example.invalid/register", {}),
        )

    def test_agent402_public_find_detects_indexed_seller_hint(self):
        response = Mock()
        response.status_code = 200
        response.text = '{"relatedSellers":[{"origin":"https://projectpermit-api-v2-production.up.railway.app"}]}'
        response.json.return_value = {"relatedSellers": [{"origin": registration.ORIGIN}]}
        client = Mock()
        client.get.return_value = response
        self.assertTrue(registration._observe_agent402_public_find(client))
        client.get.assert_called_once_with(
            registration.AGENT402_FIND_BASE_URL,
            params={"q": "ProjectPermit"},
        )

    def test_agent402_external_route_detects_projectpermit_for_task(self):
        response = Mock()
        response.status_code = 200
        response.text = '{"results":[{"seller":"https://projectpermit-api-v2-production.up.railway.app"}]}'
        response.json.return_value = {
            "query": "building permit",
            "include": "external",
            "results": [{"seller": registration.ORIGIN, "name": "ProjectPermit"}],
        }
        client = Mock()
        client.post.return_value = response
        self.assertTrue(registration._observe_agent402_external_route(client, "building permit"))
        client.post.assert_called_once_with(
            registration.AGENT402_ROUTE_URL,
            json={"query": "building permit", "top": 10, "include": "external"},
        )

    def test_agent402_external_route_allows_no_match(self):
        response = Mock()
        response.status_code = 200
        response.text = '{"results":[]}'
        response.json.return_value = {"results": []}
        client = Mock()
        client.post.return_value = response
        self.assertFalse(registration._observe_agent402_external_route(client, "renovation permit"))

    def test_agent402_discovery_refuses_unexpected_payment(self):
        response = Mock()
        response.status_code = 402
        response.text = "payment required"
        client = Mock()
        client.get.return_value = response
        with self.assertRaisesRegex(RuntimeError, "unexpectedly requested payment"):
            registration._observe_agent402_public_find(client)

        client = Mock()
        client.post.return_value = response
        with self.assertRaisesRegex(RuntimeError, "unexpectedly requested payment"):
            registration._observe_agent402_external_route(client, "building permit")

    def test_agent402_task_queries_are_buyer_intent_not_brand_search(self):
        self.assertEqual(
            ("building permit", "renovation permit"),
            registration.AGENT402_TASK_QUERIES,
        )


if __name__ == "__main__":
    unittest.main()
