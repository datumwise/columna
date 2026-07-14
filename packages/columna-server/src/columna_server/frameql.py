"""
columna_server.frameql — thin re-export shim.

The Frame-QL envelope grammar was promoted into columna-core (ADR-035 D3: the query surface is
canonical and must live under core's test regime, since Explorer tier 2 and the on-ramp build against
it). The parser moved unchanged; the parser's tests moved with it. This shim keeps
`columna_server.frameql` a stable import site so existing callers (and any downstream) are undisturbed.
"""
from __future__ import annotations

from columna_core.frameql import (  # noqa: F401  (re-export)
    FrameQLSyntaxError,
    parse_frameql,
)

__all__ = ["FrameQLSyntaxError", "parse_frameql"]
