from __future__ import annotations

import unittest

from projectpermit.public_x402_well_known import (
    API_ORIGIN,
    PAID_BATCH_RESOURCE,
    PAID_SINGLE_RESOURCE,
    x402_well_known,
)


class PublicX402WellKnownTests(unittest.TestCase):
    def test_minimal_x402scan_compatibility_shape(self) -> None:
        self.assertEqual(
            x402_well_known(),
            {
                "version": 1,
                "resources": [PAID_SINGLE_RESOURCE, PAID_BATCH_RESOURCE],
            },
        )

    def test_resources_are_canonical_same_origin_https_urls(self) -> None:
        payload = x402_well_known()
        resources = payload["resources"]
        self.assertEqual(len(resources), 2)
        self.assertEqual(len(set(resources)), 2)
        for resource in resources:
            self.assertTrue(resource.startswith(API_ORIGIN + "/v1/"))
            self.assertTrue(resource.startswith("https://"))

    def test_fallback_contains_only_paid_resources_not_pricing_or_credentials(self) -> None:
        payload = x402_well_known()
        serialized = repr(payload).lower()
        self.assertNotIn("preview", serialized)
        self.assertNotIn("pay_to", serialized)
        self.assertNotIn("facilitator", serialized)
        self.assertNotIn("price", serialized)
        self.assertNotIn("token", serialized)
        self.assertNotIn("secret", serialized)


if __name__ == "__main__":
    unittest.main()
