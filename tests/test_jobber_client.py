import json
import unittest

import httpx

from projectpermit.jobber_client import (
    JOBBER_API_VERSION,
    JOBBER_GRAPHQL_ENDPOINT,
    JobberClientError,
    JobberReadOnlyClient,
)


class JobberReadOnlyClientTest(unittest.TestCase):
    def test_account_query_uses_required_jobber_headers(self):
        seen = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["method"] = request.method
            seen["url"] = str(request.url)
            seen["authorization"] = request.headers.get("Authorization")
            seen["version"] = request.headers.get("X-JOBBER-GRAPHQL-VERSION")
            seen["body"] = json.loads(request.content.decode("utf-8"))
            return httpx.Response(
                200,
                json={
                    "data": {"account": {"id": "QWNjb3VudC0x", "name": "ProjectPermit Test"}},
                    "extensions": {"cost": {"requestedQueryCost": 2}},
                },
            )

        with JobberReadOnlyClient(
            "test-token",
            transport=httpx.MockTransport(handler),
        ) as client:
            account = client.get_account()

        self.assertEqual("POST", seen["method"])
        self.assertEqual(JOBBER_GRAPHQL_ENDPOINT, seen["url"])
        self.assertEqual("Bearer test-token", seen["authorization"])
        self.assertEqual(JOBBER_API_VERSION, seen["version"])
        self.assertIn("query GetAccount", seen["body"]["query"])
        self.assertEqual("ProjectPermit Test", account["name"])

    def test_mutation_is_rejected_before_network_io(self):
        calls = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return httpx.Response(500)

        with JobberReadOnlyClient(
            "test-token",
            transport=httpx.MockTransport(handler),
        ) as client:
            with self.assertRaisesRegex(JobberClientError, "mutations are disabled"):
                client.execute("mutation UpdateJob { jobEdit(input: {}) { userErrors { message } } }")

        self.assertEqual([], calls)

    def test_graphql_errors_raise_without_echoing_token(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"data": None, "errors": [{"message": "Missing scope"}]})

        secret = "super-secret-token"
        with JobberReadOnlyClient(secret, transport=httpx.MockTransport(handler)) as client:
            with self.assertRaises(JobberClientError) as caught:
                client.execute("query GetJobs { jobs(first: 1) { nodes { id } } }")

        self.assertIn("Missing scope", str(caught.exception))
        self.assertNotIn(secret, str(caught.exception))

    def test_http_error_does_not_echo_token_or_body(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, text="Invalid Token Error: do-not-copy-this-body")

        secret = "another-secret-token"
        with JobberReadOnlyClient(secret, transport=httpx.MockTransport(handler)) as client:
            with self.assertRaises(JobberClientError) as caught:
                client.execute("query GetAccount { account { id name } }")

        message = str(caught.exception)
        self.assertIn("status 401", message)
        self.assertNotIn(secret, message)
        self.assertNotIn("do-not-copy-this-body", message)


if __name__ == "__main__":
    unittest.main()
