"""Compatibility helpers between MCP Python SDK v2 and x402 MCP client adapters.

x402's current generic MCP result converter still probes v1-style attributes
(`_meta` and `structuredContent`). MCP Python SDK v2 exposes `meta` and
`structured_content`. This shim preserves settlement metadata until the upstream
converter is fully v2-aware.
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any


def to_x402_compatible_result(result: Any) -> Any:
    """Return a lightweight result object in the shape x402 currently reads."""
    content: list[dict[str, Any]] = []
    for item in getattr(result, "content", []) or []:
        if hasattr(item, "text"):
            content.append({"type": "text", "text": str(item.text)})
        elif isinstance(item, dict):
            content.append(dict(item))
        else:
            content.append(
                {
                    "type": str(getattr(item, "type", "text")),
                    "text": str(item),
                }
            )

    return SimpleNamespace(
        content=content,
        is_error=bool(getattr(result, "is_error", False)),
        _meta=dict(getattr(result, "meta", None) or {}),
        structuredContent=getattr(result, "structured_content", None),
    )
