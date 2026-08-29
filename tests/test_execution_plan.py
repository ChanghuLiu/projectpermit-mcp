import unittest

from projectpermit.execution_plan import (
    BINDING_REQUIRED,
    BLOCKED,
    JOBBER_COMPACT_FIELDS,
    NOOP,
    READY_TO_EXECUTE,
    build_jobber_execution_plan,
    build_servicem8_execution_plan,
)
from projectpermit.preflight_service import run_preflight


class ExecutionPlanTest(unittest.TestCase):
    def _safe_result(self, platform: str, object_type: str, object_id: str):
        return run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "context": {
                    "source_platform": platform,
                    "source_object_type": object_type,
                    "source_object_id": object_id,
                },
                "resolve_address": False,
            }
        )

    def test_servicem8_safe_evidence_route_builds_deterministic_note_upsert(self):
        job_uuid = "123e4567-e89b-12d3-a456-426614174000"
        result = self._safe_result("servicem8", "job", job_uuid)
        plan = build_servicem8_execution_plan(result, job_uuid=job_uuid)

        self.assertEqual(READY_TO_EXECUTE, plan["status"])
        self.assertTrue(plan["executable"])
        self.assertFalse(plan["mutation_performed"])
        self.assertEqual(["read_job_notes", "publish_job_notes"], plan["required_oauth_scopes"])
        self.assertEqual("note", plan["deterministic_record"]["kind"])
        self.assertEqual(3, len(plan["mutation_intents"]))
        self.assertEqual("GET", plan["mutation_intents"][0]["method"])
        self.assertEqual("POST", plan["mutation_intents"][1]["method"])
        self.assertEqual("job", plan["mutation_intents"][1]["body"]["related_object"])
        self.assertEqual(job_uuid, plan["mutation_intents"][1]["body"]["related_object_uuid"])

        second = build_servicem8_execution_plan(result, job_uuid=job_uuid)
        self.assertEqual(
            plan["deterministic_record"]["uuid"],
            second["deterministic_record"]["uuid"],
        )

    def test_servicem8_required_route_builds_task_upsert(self):
        job_uuid = "123e4567-e89b-12d3-a456-426614174001"
        result = run_preflight(
            {
                "jurisdiction": "gatineau_qc",
                "project": {"family": "addition", "floor_area_increase": True},
                "property": {},
                "context": {
                    "source_platform": "servicem8",
                    "source_object_type": "job",
                    "source_object_id": job_uuid,
                },
                "resolve_address": False,
            }
        )
        plan = build_servicem8_execution_plan(result, job_uuid=job_uuid)

        self.assertEqual(READY_TO_EXECUTE, plan["status"])
        self.assertEqual(["read_tasks", "manage_tasks"], plan["required_oauth_scopes"])
        self.assertEqual("task", plan["deterministic_record"]["kind"])
        self.assertEqual("ProjectPermit permit workflow", plan["mutation_intents"][1]["body"]["name"])

    def test_servicem8_target_scope_mismatch_is_blocked(self):
        result = self._safe_result(
            "servicem8",
            "job",
            "123e4567-e89b-12d3-a456-426614174002",
        )
        plan = build_servicem8_execution_plan(
            result,
            job_uuid="123e4567-e89b-12d3-a456-426614174999",
        )
        self.assertEqual(BLOCKED, plan["status"])
        self.assertEqual(["TARGET_SCOPE_MISMATCH"], plan["reason_codes"])
        self.assertEqual([], plan["mutation_intents"])

    def test_servicem8_repeat_unchanged_becomes_execution_noop(self):
        job_uuid = "123e4567-e89b-12d3-a456-426614174003"
        first = self._safe_result("servicem8", "job", job_uuid)
        prior = first["action_bundle"]["identity"]
        repeated = run_preflight(
            {
                "jurisdiction": "ottawa_on",
                "project": {"family": "window_door", "action": "replace_same_size"},
                "property": {"heritage": False},
                "context": {
                    "source_platform": "servicem8",
                    "source_object_type": "job",
                    "source_object_id": job_uuid,
                    "prior_decision_identity": prior,
                },
                "resolve_address": False,
            }
        )
        plan = build_servicem8_execution_plan(repeated, job_uuid=job_uuid)
        self.assertEqual(NOOP, plan["status"])
        self.assertFalse(plan["executable"])
        self.assertEqual(["DUPLICATE_SUPPRESSED"], plan["reason_codes"])
        self.assertEqual([], plan["mutation_intents"])

    def test_jobber_requires_compact_field_and_graphql_binding(self):
        object_id = "Z2lkOi8vSm9iYmVyL1F1b3RlLzEyMw=="
        result = self._safe_result("jobber", "quote", object_id)
        plan = build_jobber_execution_plan(
            result,
            object_type="quote",
            object_id=object_id,
        )

        self.assertEqual(BINDING_REQUIRED, plan["status"])
        self.assertFalse(plan["executable"])
        self.assertEqual(5, len(plan["compact_field_contract"]))
        self.assertEqual(5, len(plan["missing_custom_field_bindings"]))
        self.assertIn("api_version", plan["missing_graphql_bindings"])
        self.assertEqual([], plan["mutation_intents"])
        self.assertEqual(5, len(JOBBER_COMPACT_FIELDS))

    def test_jobber_bound_plan_contains_exactly_five_custom_fields(self):
        object_id = "Z2lkOi8vSm9iYmVyL0pvYi80NTY="
        result = self._safe_result("jobber", "job", object_id)
        bindings = {
            "status": "cfg-status",
            "route": "cfg-route",
            "evidence": "cfg-evidence",
            "freshness": "cfg-freshness",
            "identity": "cfg-identity",
        }
        graphql = {
            "api_version": "TESTED-ACTIVE-VERSION",
            "mutation_name": "BOUND_FROM_GRAPHIQL",
            "id_argument": "BOUND_ID_ARGUMENT",
            "input_argument": "BOUND_INPUT_ARGUMENT",
        }
        plan = build_jobber_execution_plan(
            result,
            object_type="job",
            object_id=object_id,
            custom_field_bindings=bindings,
            graphql_binding=graphql,
        )

        self.assertEqual(READY_TO_EXECUTE, plan["status"])
        self.assertTrue(plan["executable"])
        self.assertFalse(plan["mutation_performed"])
        intent = plan["mutation_intents"][0]
        self.assertEqual("GRAPHQL_POST", intent["transport"])
        self.assertEqual(5, len(intent["custom_fields"]))
        self.assertEqual(
            {"status", "route", "evidence", "freshness", "identity"},
            {item["logical_key"] for item in intent["custom_fields"]},
        )

    def test_jobber_request_is_not_a_supported_custom_field_write_target(self):
        object_id = "Z2lkOi8vSm9iYmVyL1JlcXVlc3QvNzg5"
        result = self._safe_result("jobber", "request", object_id)
        plan = build_jobber_execution_plan(
            result,
            object_type="request",
            object_id=object_id,
        )
        self.assertEqual(BLOCKED, plan["status"])
        self.assertEqual(["UNSUPPORTED_JOBBER_WRITE_TARGET"], plan["reason_codes"])


if __name__ == "__main__":
    unittest.main()
