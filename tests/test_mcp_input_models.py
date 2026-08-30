from __future__ import annotations

import unittest

from pydantic import ValidationError

from projectpermit.mcp_input_models import (
    BatchItemFacts,
    ProjectFacts,
    SinglePreflightArguments,
    batch_items_to_mappings,
    model_or_mapping,
    paid_mcp_input_schema,
)


def _resolve(schema: dict, node: dict) -> dict:
    ref = node.get("$ref") if isinstance(node, dict) else None
    if isinstance(ref, str) and ref.startswith("#/$defs/"):
        return (schema.get("$defs") or {}).get(ref.rsplit("/", 1)[-1], {})
    for key in ("anyOf", "oneOf"):
        values = node.get(key) if isinstance(node, dict) else None
        if isinstance(values, list):
            for candidate in values:
                if isinstance(candidate, dict) and candidate.get("type") != "null":
                    return _resolve(schema, candidate)
    return node


class McpInputModelTests(unittest.TestCase):
    def test_project_schema_exposes_first_call_fields_but_allows_future_facts(self) -> None:
        schema = ProjectFacts.model_json_schema()
        properties = schema.get("properties") or {}
        self.assertIn("family", properties)
        self.assertIn("action", properties)
        self.assertIn("structural_change", properties)
        self.assertIn("deck_height_mm", properties)
        self.assertIn("accessory_area_m2", properties)
        self.assertIs(schema.get("additionalProperties"), True)

        model = ProjectFacts(
            family="window_door",
            action="replace_same_size",
            future_municipal_fact="kept",
        )
        dumped = model_or_mapping(model)
        self.assertEqual(dumped["future_municipal_fact"], "kept")
        self.assertEqual(dumped["family"], "window_door")

    def test_batch_item_keeps_per_item_error_isolation_contract(self) -> None:
        malformed = BatchItemFacts(client_ref="missing-project", jurisdiction="ottawa_on")
        [dumped] = batch_items_to_mappings([malformed])
        self.assertEqual(dumped["client_ref"], "missing-project")
        self.assertEqual(dumped["jurisdiction"], "ottawa_on")
        self.assertNotIn("project", dumped)

    def test_paid_discovery_schema_uses_same_structured_project_contract(self) -> None:
        schema = paid_mcp_input_schema()
        self.assertIs(schema.get("additionalProperties"), False)
        properties = schema.get("properties") or {}
        self.assertEqual(set(schema.get("required") or []), {"jurisdiction", "project"})
        project = _resolve(schema, properties["project"])
        project_properties = project.get("properties") or {}
        self.assertIn("family", project_properties)
        self.assertIn("action", project_properties)
        self.assertIs(project.get("additionalProperties"), True)

    def test_paid_top_level_stays_closed_while_nested_facts_are_extensible(self) -> None:
        parsed = SinglePreflightArguments(
            jurisdiction="ottawa_on",
            project={
                "family": "window_door",
                "action": "replace_same_size",
                "future_rule_fact": 7,
            },
        )
        self.assertEqual(parsed.project.model_dump()["future_rule_fact"], 7)
        with self.assertRaises(ValidationError):
            SinglePreflightArguments(
                jurisdiction="ottawa_on",
                project={"family": "window_door"},
                unknown_top_level="no",
            )


if __name__ == "__main__":
    unittest.main()
