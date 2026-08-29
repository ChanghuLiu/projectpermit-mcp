import io
import json
import unittest

from projectpermit.servicem8_cli import (
    ACCESS_TOKEN_ENV,
    API_KEY_ENV,
    GRANTED_SCOPES_ENV,
    run,
)


READY_PLAN = {
    "platform": "servicem8",
    "status": "READY_TO_EXECUTE",
    "executable": True,
    "requires_explicit_execute_call": True,
    "idempotency_key": "ppidem_cli",
    "bundle_id": "ppb_cli",
}


class ServiceM8CliTest(unittest.TestCase):
    def test_dry_run_needs_no_credentials_and_prints_plan(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        calls = []

        def plan_builder(result, *, job_uuid):
            self.assertEqual({"ok": True}, result)
            self.assertEqual("job-123", job_uuid)
            return dict(READY_PLAN)

        def executor(plan, **kwargs):
            calls.append((plan, kwargs))
            return {
                "status": "DRY_RUN",
                "mutation_performed": False,
                "idempotency_key": plan["idempotency_key"],
            }

        code = run(
            ["--job-uuid", "job-123"],
            environ={},
            stdin=io.StringIO('{"ok": true}'),
            stdout=stdout,
            stderr=stderr,
            plan_builder=plan_builder,
            executor=executor,
        )

        self.assertEqual(0, code)
        self.assertEqual("", stderr.getvalue())
        self.assertEqual(False, calls[0][1]["execute"])
        payload = json.loads(stdout.getvalue())
        self.assertEqual("dry_run", payload["mode"])
        self.assertEqual("READY_TO_EXECUTE", payload["plan"]["status"])
        self.assertEqual(API_KEY_ENV, payload["credential_environment"]["api_key"])
        self.assertEqual(ACCESS_TOKEN_ENV, payload["credential_environment"]["access_token"])

    def test_execute_reads_credentials_from_environment_only(self):
        stdout = io.StringIO()
        captured = {}

        def plan_builder(result, *, job_uuid):
            return dict(READY_PLAN)

        def executor(plan, **kwargs):
            captured.update(kwargs)
            return {
                "status": "EXECUTED_UPDATE",
                "mutation_performed": True,
                "idempotency_key": plan["idempotency_key"],
            }

        env = {
            ACCESS_TOKEN_ENV: "oauth-secret",
            GRANTED_SCOPES_ENV: "read_tasks, manage_tasks",
        }
        code = run(
            ["--job-uuid", "job-123", "--execute"],
            environ=env,
            stdin=io.StringIO('{}'),
            stdout=stdout,
            stderr=io.StringIO(),
            plan_builder=plan_builder,
            executor=executor,
        )

        self.assertEqual(0, code)
        self.assertTrue(captured["execute"])
        self.assertEqual("oauth-secret", captured["access_token"])
        self.assertIsNone(captured["api_key"])
        self.assertEqual(["read_tasks", "manage_tasks"], captured["granted_scopes"])
        self.assertNotIn("oauth-secret", stdout.getvalue())
        payload = json.loads(stdout.getvalue())
        self.assertEqual("execute", payload["mode"])
        self.assertEqual("EXECUTED_UPDATE", payload["execution"]["status"])

    def test_private_api_key_is_read_from_environment(self):
        captured = {}

        def executor(plan, **kwargs):
            captured.update(kwargs)
            return {"status": "NOOP", "mutation_performed": False}

        code = run(
            ["--job-uuid", "job-123", "--execute"],
            environ={API_KEY_ENV: "api-secret"},
            stdin=io.StringIO('{}'),
            stdout=io.StringIO(),
            stderr=io.StringIO(),
            plan_builder=lambda result, job_uuid: dict(READY_PLAN),
            executor=executor,
        )
        self.assertEqual(0, code)
        self.assertEqual("api-secret", captured["api_key"])
        self.assertIsNone(captured["access_token"])

    def test_invalid_json_returns_safe_input_error(self):
        stderr = io.StringIO()
        code = run(
            ["--job-uuid", "job-123"],
            environ={},
            stdin=io.StringIO('{bad json'),
            stdout=io.StringIO(),
            stderr=stderr,
        )
        self.assertEqual(2, code)
        self.assertIn("invalid input", stderr.getvalue())
        self.assertNotIn("{bad json", stderr.getvalue())

    def test_blocked_dry_run_returns_nonzero_without_credentials(self):
        def executor(plan, **kwargs):
            return {"status": "BLOCKED", "mutation_performed": False}

        code = run(
            ["--job-uuid", "job-123"],
            environ={},
            stdin=io.StringIO('{}'),
            stdout=io.StringIO(),
            stderr=io.StringIO(),
            plan_builder=lambda result, job_uuid: {"platform": "servicem8", "status": "BLOCKED"},
            executor=executor,
        )
        self.assertEqual(2, code)

    def test_provider_execution_failure_uses_distinct_exit_code(self):
        def executor(plan, **kwargs):
            return {"status": "EXECUTION_FAILED", "mutation_performed": False}

        code = run(
            ["--job-uuid", "job-123", "--execute"],
            environ={API_KEY_ENV: "api-secret"},
            stdin=io.StringIO('{}'),
            stdout=io.StringIO(),
            stderr=io.StringIO(),
            plan_builder=lambda result, job_uuid: dict(READY_PLAN),
            executor=executor,
        )
        self.assertEqual(3, code)


if __name__ == "__main__":
    unittest.main()
