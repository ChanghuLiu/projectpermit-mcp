import unittest

from projectpermit.external_executor import (
    BLOCKED,
    DRY_RUN,
    EXECUTED_CREATE,
    EXECUTED_UPDATE,
    EXECUTION_FAILED,
    NOOP,
    execute_servicem8_plan,
)


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class FakeClient:
    def __init__(self, statuses):
        self.statuses = list(statuses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if not self.statuses:
            raise AssertionError("unexpected request")
        status = self.statuses.pop(0)
        if isinstance(status, Exception):
            raise status
        return FakeResponse(status)


def ready_plan(kind="note"):
    record_uuid = "11111111-2222-5333-8444-555555555555"
    job_uuid = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
    if kind == "note":
        lookup = f"/api_1.0/dbonote/{record_uuid}.json"
        create_path = "/api_1.0/note.json"
        update_path = lookup
        body = {
            "uuid": record_uuid,
            "related_object": "job",
            "related_object_uuid": job_uuid,
            "note": "ProjectPermit evidence",
            "action_required": "0",
        }
        scopes = ["read_job_notes", "publish_job_notes"]
    else:
        lookup = f"/api_1.0/task/{record_uuid}.json"
        create_path = "/api_1.0/task.json"
        update_path = lookup
        body = {
            "uuid": record_uuid,
            "name": "ProjectPermit permit workflow",
            "task_details": "ProjectPermit task",
            "related_object": "job",
            "related_object_uuid": job_uuid,
            "task_complete": "0",
        }
        scopes = ["read_tasks", "manage_tasks"]
    return {
        "execution_plan_version": "2026-08-29.1",
        "platform": "servicem8",
        "mutation_performed": False,
        "requires_explicit_execute_call": True,
        "gate_state": "READY_FOR_EXPLICIT_WRITE",
        "idempotency_key": "ppidem_test",
        "scope_fingerprint": "pps_test",
        "bundle_id": "ppb_test",
        "change_classification": "FIRST_OBSERVATION",
        "status": "READY_TO_EXECUTE",
        "executable": True,
        "required_oauth_scopes": scopes,
        "target": {"object_type": "job", "object_id": job_uuid},
        "deterministic_record": {"kind": kind, "uuid": record_uuid},
        "mutation_intents": [
            {"step": "LOOKUP", "method": "GET", "path": lookup},
            {
                "step": "CREATE_IF_MISSING",
                "method": "POST",
                "path": create_path,
                "body": dict(body),
            },
            {
                "step": "UPDATE_IF_EXISTS",
                "method": "POST",
                "path": update_path,
                "body": dict(body),
            },
        ],
    }


class ExternalExecutorTest(unittest.TestCase):
    def test_default_is_network_free_dry_run(self):
        client = FakeClient([])
        result = execute_servicem8_plan(ready_plan(), client=client)
        self.assertEqual(DRY_RUN, result["status"])
        self.assertFalse(result["mutation_performed"])
        self.assertEqual([], client.calls)

    def test_noop_never_calls_provider_even_when_execute_true(self):
        plan = ready_plan()
        plan["status"] = "NOOP"
        plan["executable"] = False
        plan["mutation_intents"] = []
        client = FakeClient([])
        result = execute_servicem8_plan(plan, execute=True, access_token="secret", client=client)
        self.assertEqual(NOOP, result["status"])
        self.assertEqual([], client.calls)
        self.assertNotIn("secret", repr(result))

    def test_oauth_requires_declared_scopes_before_network(self):
        client = FakeClient([])
        result = execute_servicem8_plan(
            ready_plan(),
            execute=True,
            access_token="secret-token",
            granted_scopes=["read_job_notes"],
            client=client,
        )
        self.assertEqual(BLOCKED, result["status"])
        self.assertEqual(["publish_job_notes"], result["missing_scopes"])
        self.assertEqual([], client.calls)
        self.assertNotIn("secret-token", repr(result))

    def test_oauth_missing_record_creates_deterministic_record(self):
        client = FakeClient([404, 200])
        result = execute_servicem8_plan(
            ready_plan("note"),
            execute=True,
            access_token="secret-token",
            granted_scopes=["read_job_notes", "publish_job_notes"],
            client=client,
        )
        self.assertEqual(EXECUTED_CREATE, result["status"])
        self.assertTrue(result["mutation_performed"])
        self.assertEqual("create", result["operation"])
        self.assertEqual(2, len(client.calls))
        self.assertEqual("GET", client.calls[0][0])
        self.assertEqual("POST", client.calls[1][0])
        self.assertEqual("Bearer secret-token", client.calls[0][2]["headers"]["Authorization"])
        self.assertNotIn("secret-token", repr(result))

    def test_api_key_existing_record_updates(self):
        client = FakeClient([200, 204])
        result = execute_servicem8_plan(
            ready_plan("task"),
            execute=True,
            api_key="private-key",
            client=client,
        )
        self.assertEqual(EXECUTED_UPDATE, result["status"])
        self.assertTrue(result["mutation_performed"])
        self.assertEqual("api_key", result["credential_mode"])
        self.assertEqual("private-key", client.calls[0][2]["headers"]["X-API-Key"])
        self.assertNotIn("private-key", repr(result))

    def test_tampered_path_is_blocked_before_credentials_are_sent(self):
        plan = ready_plan()
        plan["mutation_intents"][0]["path"] = "https://evil.example/steal"
        client = FakeClient([])
        result = execute_servicem8_plan(
            plan,
            execute=True,
            access_token="secret-token",
            granted_scopes=["read_job_notes", "publish_job_notes"],
            client=client,
        )
        self.assertEqual(BLOCKED, result["status"])
        self.assertEqual(["LOOKUP_PATH_MISMATCH"], result["reason_codes"])
        self.assertEqual([], client.calls)

    def test_unexpected_lookup_status_stops_without_mutation(self):
        client = FakeClient([500])
        result = execute_servicem8_plan(
            ready_plan(),
            execute=True,
            api_key="private-key",
            client=client,
        )
        self.assertEqual(EXECUTION_FAILED, result["status"])
        self.assertFalse(result["mutation_performed"])
        self.assertEqual(1, len(client.calls))
        self.assertEqual(500, result["provider_status_code"])

    def test_exactly_one_credential_mode_is_required(self):
        client = FakeClient([])
        result = execute_servicem8_plan(
            ready_plan(),
            execute=True,
            access_token="a",
            api_key="b",
            granted_scopes=["read_job_notes", "publish_job_notes"],
            client=client,
        )
        self.assertEqual(BLOCKED, result["status"])
        self.assertEqual([], client.calls)


if __name__ == "__main__":
    unittest.main()
