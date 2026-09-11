"""
columna_server.frameql — a one-name re-export: the language's syntax-error channel.

`FrameQLSyntaxError` is defined in `columna_core.frameql` (ADR-035 D3 moved the query surface into
core, where it lives under core's test regime). This module keeps the historical server-side import
site stable for that error type — the one name it carries that is wholly current: the expression
grammar and the planner raise it, and the server relays it as the `frameql_syntax` query error.

It carried one more name, `parse_frameql`, the parser for the terse `<columns> @ <anchor>` fragment.
That fragment is not part of Frame-QL 1.0 and is not a public language surface (ruled 2026-09-11);
the parser is quarantined in core under a private name and is not re-exported here. The language is
the ENVELOPE — `columna_core.envelope.parse_statement`, `SELECT … AT {…}` — which is what
`columna_server.tools` calls.
"""
from __future__ import annotations

from columna_core.frameql import FrameQLSyntaxError  # noqa: F401  (re-export)

__all__ = ["FrameQLSyntaxError"]
