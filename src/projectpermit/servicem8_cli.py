"""Customer-local ServiceM8 writeback CLI.

The CLI intentionally keeps ServiceM8 credentials outside hosted ProjectPermit.
It consumes a ProjectPermit preflight result, rebuilds the target-bound Layer 6
execution plan locally, defaults to dry-run, and only calls the Layer 7 executor
when --execute is explicitly supplied.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Callable, Mapping, TextIO

from .execution_plan import build_servicem8_execution_plan
from .external_executor import (
    BLOCKED,
    DRY_RUN,
    EXECUTED_CREATE,
    EXECUTED_UPDATE,
    EXECUTION_FAILED,
    NOOP,
    execute_servicem8_plan,
)

API_KEY_ENV = "PROJECTPERMIT_SERVICEM8_API_KEY"
ACCESS_TOKEN_ENV = "PROJECTPERMIT_SERVICEM8_ACCESS_TOKEN"
GRANTED_SCOPES_ENV = "PROJECTPERMIT_SERVICEM8_GRANTED_SCOPES"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="projectpermit-servicem8-exec",
        description=(
            "Build and optionally execute a target-bound ServiceM8 ProjectPermit writeback. "
            "Credentials are read only from environment variables, never command-line flags."
        ),
    )
    parser.add_argument(
        "--result",
        default="-",
        help="ProjectPermit preflight result JSON file, or '-' for stdin (default).",
    )
    parser.add_argument("--job-uuid", required=True, help="ServiceM8 Job UUID selected for writeback.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform the provider write. Without this flag the command is network-free dry-run.",
    )
    return parser


def _load_result(path: str, stdin: TextIO) -> Mapping[str, Any]:
    if path == "-":
        payload = json.load(stdin)
    else:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    if not isinstance(payload, Mapping):
        raise ValueError("ProjectPermit result JSON must be an object")
    return payload


def _scopes(value: str | None) -> list[str]:
    rendered = str(value or "").replace(",", " ")
    return [item for item in rendered.split() if item]


def _write_json(stream: TextIO, payload: Mapping[str, Any]) -> None:
    stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    stream.flush()


def _exit_code(status: str) -> int:
    if status in {DRY_RUN, NOOP, EXECUTED_CREATE, EXECUTED_UPDATE}:
        return 0
    if status == EXECUTION_FAILED:
        return 3
    return 2


def run(
    argv: list[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    plan_builder: Callable[..., dict[str, Any]] = build_servicem8_execution_plan,
    executor: Callable[..., dict[str, Any]] = execute_servicem8_plan,
) -> int:
    """Run the CLI and return a process-style exit code.

    Credential values are never accepted as argv and never rendered to stdout/stderr.
    Injection points exist for deterministic unit tests; production entry points use
    the real plan builder and executor.
    """
    env = environ if environ is not None else os.environ
    input_stream = stdin if stdin is not None else sys.stdin
    output_stream = stdout if stdout is not None else sys.stdout
    error_stream = stderr if stderr is not None else sys.stderr

    args = _parser().parse_args(argv)
    try:
        result = _load_result(args.result, input_stream)
        plan = plan_builder(result, job_uuid=args.job_uuid)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        error_stream.write(f"projectpermit-servicem8-exec: invalid input ({type(exc).__name__})\n")
        error_stream.flush()
        return 2

    if not args.execute:
        execution = executor(plan, execute=False)
        _write_json(
            output_stream,
            {
                "mode": "dry_run",
                "plan": plan,
                "execution": execution,
                "credential_environment": {
                    "api_key": API_KEY_ENV,
                    "access_token": ACCESS_TOKEN_ENV,
                    "granted_scopes": GRANTED_SCOPES_ENV,
                },
            },
        )
        return _exit_code(str(execution.get("status") or BLOCKED))

    execution = executor(
        plan,
        execute=True,
        api_key=env.get(API_KEY_ENV),
        access_token=env.get(ACCESS_TOKEN_ENV),
        granted_scopes=_scopes(env.get(GRANTED_SCOPES_ENV)),
    )
    _write_json(output_stream, {"mode": "execute", "execution": execution})
    return _exit_code(str(execution.get("status") or BLOCKED))


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
