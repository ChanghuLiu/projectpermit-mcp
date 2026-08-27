import json
import unittest

import httpx

from projectpermit.servicem8_client import (
    SERVICEM8_API_BASE,
    ServiceM8ClientError,
    ServiceM8ReadOnlyClient,
)


class ServiceM8ReadOnlyClientTest(unittest.TestCase):
    def test_get_job_uses_api_key_header_and_get_only(self):
        seen = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["api_key"] = request.headers.get("X-API-Key")
            return httpx.Response(
                200,
                json={
                    "uuid": "job-123",
                    "status": "Quote",
                    "job_address": "100 Queen St, Ottawa, ON",
                    "job_description": "Rear deck replacement",
                },
            )

        with ServiceM8ReadOnlyClient(
            "test-key",
            transport=httpx.MockTransport(handler),
        ) as client:
            job = client.get_job("job-123")

        self.assertEqual("GET", seen["method"])
        self.assertEqual(f"{SERVICEM8_API_BASE}/job/job-123.json", seen["url"])
        self.assertEqual("test-key", seen["api_key"])
        self.assertEqual("job-123", job["uuid"])

    def test_list_jobs_preserves_verified_query_params(self):
        seen = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["method"] = request.method
            seen["params"] = dict(request.url.params)
            return httpx.Response(200, json=[{"uuid": "job-1"}, {"uuid": "job-2"}])

        with ServiceM8ReadOnlyClient(
            "test-key",
            transport=httpx.MockTransport(handler),
        ) as client:
            jobs = client.list_jobs(params={"$top": "5"})

        self.assertEqual("GET", seen["method"])
        self.assertEqual("5", seen["params"]["$top"])
        self.assertEqual(2, len(jobs))

    def test_job_uuid_is_path_encoded(self):
        seen = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["url"] = str(request.url)
            return httpx.Response(200, json={"uuid": "odd/id"})

        with ServiceM8ReadOnlyClient(
            "test-key",
            transport=httpx.MockTransport(handler),
        ) as client:
            client.get_job("odd/id")

        self.assertIn("odd%2Fid.json", seen["url"])

    def test_http_error_does_not_echo_api_key_or_body(self):
        secret = "super-secret-servicem8-key"

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, text=f"invalid {secret}; private-account-data")

        with ServiceM8ReadOnlyClient(secret, transport=httpx.MockTransport(handler)) as client:
            with self.assertRaises(ServiceM8ClientError) as caught:
                client.get_job("job-1")

        message = str(caught.exception)
        self.assertIn("status 401", message)
        self.assertNotIn(secret, message)
        self.assertNotIn("private-account-data", message)

    def test_non_json_response_is_rejected(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="not json")

        with ServiceM8ReadOnlyClient("test-key", transport=httpx.MockTransport(handler)) as client:
            with self.assertRaisesRegex(ServiceM8ClientError, "non-JSON"):
                client.get_job("job-1")

    def test_client_has_no_mutation_methods(self):
        client = ServiceM8ReadOnlyClient(
            "test-key",
            transport=httpx.MockTransport(lambda request: httpx.Response(500)),
        )
        try:
            self.assertFalse(hasattr(client, "create_job"))
            self.assertFalse(hasattr(client, "update_job"))
            self.assertFalse(hasattr(client, "delete_job"))
            self.assertFalse(hasattr(client, "post"))
            self.assertFalse(hasattr(client, "delete"))
        finally:
            client.close()


if __name__ == "__main__":
    unittest.main()
