"""
columna_server.frameql — the ENVELOPE grammar for a Frame-QL query string.

WP-2.2 ruling B: the server owns only the *envelope* — column names, the `@` separator, and the
anchor level list. Every column expression is delegated verbatim to columna-core's existing
expression parser (via `Frame.column(name, expr)`), so there is exactly ONE expression dialect and
the server never reinterprets query semantics. Promotion of this parser into columna-core is a v0.8
item.

Grammar:

    <query>   ::= <columns> "@" <anchor>
    <columns> ::= <column> ("," <column>)*
    <column>  ::= <name> ":" <expr>  |  <expr>          # bare expr -> name defaults to the expr text
    <anchor>  ::= <level> ("," <level>)*

Commas inside parentheses (e.g. `lag(revenue.sum, n=1)`) are NOT top-level separators. The server
accepts no SQL: a query that does not fit this envelope (or whose expression columna-core rejects)
is an error, never executed.

Examples:
    "revenue @ region"
    "rate: revenue / level.last @ store, day"
    "rev: revenue, inv: level.last @ store, day"
"""
from __future__ import annotations

_SQL_HINTS = ("select ", "insert ", "update ", "delete ", "drop ", "create ", "with ", ";")


class FrameQLSyntaxError(ValueError):
    """The query does not fit the Frame-QL envelope (never raised for expression-internal errors —
    those come from columna-core when the frame runs)."""


def _split_top(s: str, delim: str) -> list[str]:
    """Split on `delim` only at paren-depth 0 (so commas inside `f(a, b)` are preserved)."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(s):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
            if depth < 0:
                raise FrameQLSyntaxError(f"unbalanced parentheses in {s!r}")
        elif ch == delim and depth == 0:
            out.append(s[start:i])
            start = i + 1
    if depth != 0:
        raise FrameQLSyntaxError(f"unbalanced parentheses in {s!r}")
    out.append(s[start:])
    return out


def parse_frameql(text: str) -> tuple[tuple[str, ...], list[tuple[str, str]]]:
    """Parse a Frame-QL query string into (anchor_levels, [(column_name, column_expr)]).

    Raises FrameQLSyntaxError on an envelope violation. Does NOT validate expressions or levels —
    columna-core does that when the frame runs (one dialect).
    """
    if text is None or not text.strip():
        raise FrameQLSyntaxError("empty query")
    low = text.strip().lower()
    if any(h in low for h in _SQL_HINTS):
        raise FrameQLSyntaxError("this looks like SQL; the server accepts only Frame-QL "
                                 "(<columns> @ <anchor>), never SQL")

    parts = _split_top(text, "@")
    if len(parts) != 2:
        raise FrameQLSyntaxError("a query must have exactly one '@' separating columns from the "
                                 "anchor, e.g. \"revenue @ region\"")
    cols_part, anchor_part = parts

    anchor = tuple(s.strip() for s in _split_top(anchor_part, ",") if s.strip())
    if not anchor:
        raise FrameQLSyntaxError("the anchor (after '@') must name at least one level")

    columns: list[tuple[str, str]] = []
    for spec in _split_top(cols_part, ","):
        spec = spec.strip()
        if not spec:
            continue
        head, sep, tail = _split_first_top(spec, ":")
        if sep:
            name, expr = head.strip(), tail.strip()
            if not name or not expr:
                raise FrameQLSyntaxError(f"malformed column '{spec}' (expected 'name: expr')")
            columns.append((name, expr))
        else:
            columns.append((spec, spec))   # bare expression: the column is named by its text
    if not columns:
        raise FrameQLSyntaxError("a query must have at least one column before '@'")
    return anchor, columns


def _split_first_top(s: str, delim: str) -> tuple[str, str, str]:
    """Partition on the first top-level `delim` (paren-depth 0). Returns (head, delim|'', tail)."""
    depth = 0
    for i, ch in enumerate(s):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == delim and depth == 0:
            return s[:i], delim, s[i + 1:]
    return s, "", ""
