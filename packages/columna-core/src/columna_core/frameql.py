"""columna_core.frameql — the Frame-QL surface."""
from __future__ import annotations
from typing import Optional
from .model import Manifold
from .projection import PlannerView
from .engine import ColumnEngine
from .planner import Planner, FrameResult


class ManifoldServer:
    def __init__(self, manifold: Manifold, connector):
        self.m = manifold
        self.engine = ColumnEngine(manifold, connector)
        self.planner = Planner(PlannerView(manifold), self.engine)

    def frame(self, *anchor, where: Optional[str] = None) -> "Frame":
        # Manifold-aware anchor resolution (capture §2b) runs HERE, at frame-build — the string parser
        # stays manifold-blind. A rejection (universe name in anchor; bad family.level qualification)
        # raises FrameQLSyntaxError so it rides the EXISTING query-error channel (server -> the
        # `frameql_syntax` wire error) with no new wire reason code and a byte-identical four-mood wire.
        return Frame(self, self.planner.resolve_anchor(tuple(anchor)), where)

    def publish(self, trace=None, attestation: Optional[str] = None) -> int:
        """Publish the manifold: ADJUDICATE every declared derived-column fertility (attaching the
        constructed License to each member — the sole place a License is minted), then materialize
        the witness store. A CONTRADICTED declaration fails closed here: `adjudicate` raises and the
        manifold does not publish (no witnesses built). Returns the number of witnesses built.

        Adjudication is a no-op for a manifold with no declared fertility (unchanged behavior)."""
        from .adjudication import adjudicate
        self.adjudication = adjudicate(self, attestation=attestation, trace=trace)
        return self.engine.publish_witnesses(trace)

    @property
    def witnesses(self): return self.engine.witnesses

    @property
    def stats(self): return self.engine.stats
    @property
    def fetches(self): return self.engine.con.fetch_count


class Frame:
    def __init__(self, server, anchor, where=None):
        self.server = server
        self.anchor = anchor
        self.where = where
        self.cols = []
        self.universe = None

    def column(self, name, expr=None):
        self.cols.append((name, expr if expr is not None else name)); return self

    def on_universe(self, u):           # records the population pin (verified at resolve)
        self.universe = u; return self

    def run(self) -> FrameResult:
        return self.server.planner.run(self.anchor, self.cols, self.where, population=self.universe)

    def plan(self) -> FrameResult:
        """The would-be annotation without executing (zero backend fetches)."""
        return self.server.planner.plan(self.anchor, self.cols, self.where, population=self.universe)

    def explain(self, execute: bool = True) -> str:
        return (self.run() if execute else self.plan()).explain()


# ── the ENVELOPE grammar for a Frame-QL query string (promoted from columna-server, ADR-035 D3) ──
# The query surface is canonical (ADR-035 D1); it lives under core's test regime because Explorer
# tier 2 and the on-ramp both build against it. MOVED, not changed — the grammar is untouched; the
# server keeps a thin re-export shim. The envelope owns only column names, the `@` separator, and the
# anchor level list; every column expression is delegated verbatim to core's expression parser (via
# `Frame.column(name, expr)`), so there is exactly ONE expression dialect.
#
# Grammar:
#     <query>   ::= <columns> "@" <anchor>
#     <columns> ::= <column> ("," <column>)*
#     <column>  ::= <name> ":" <expr>  |  <expr>          # bare expr -> name defaults to the expr text
#     <anchor>  ::= <level> (("*" | ",") <level>)*      # `*` canonical (the anchor product); `,` accepted
# Commas inside parentheses (e.g. `lag(revenue.sum, n=1)`) are NOT top-level separators. No SQL: a
# query that does not fit this envelope (or whose expression core rejects) is an error, never executed.
_SQL_HINTS = ("select ", "insert ", "update ", "delete ", "drop ", "create ", "with ", ";")


class FrameQLSyntaxError(ValueError):
    """The query does not fit the Frame-QL envelope (never raised for expression-internal errors —
    those come from the planner when the frame runs)."""


def _split_top(s: str, delims: str) -> list:
    """Split on any character in `delims` at paren-depth 0 (so separators inside `f(a, b)` are
    preserved). One char or several — the anchor accepts both `,` and `*` (the anchor product);
    the column list accepts `,` alone."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(s):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
            if depth < 0:
                raise FrameQLSyntaxError(f"unbalanced parentheses in {s!r}")
        elif ch in delims and depth == 0:
            out.append(s[start:i])
            start = i + 1
    if depth != 0:
        raise FrameQLSyntaxError(f"unbalanced parentheses in {s!r}")
    out.append(s[start:])
    return out


def _split_first_top(s: str, delim: str) -> tuple:
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


def parse_frameql(text: str) -> tuple:
    """Parse a Frame-QL query string into (anchor_levels, [(column_name, column_expr)]).

    Raises FrameQLSyntaxError on an envelope violation. Does NOT validate expressions or levels —
    the planner does that when the frame runs (one dialect).
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

    # the anchor product: `*` is the canonical separator (the SAME operator as UNIVERSE a * b * c);
    # comma is accepted on input through launch (RULED), retiring only in the post-launch hygiene sweep.
    anchor = tuple(s.strip() for s in _split_top(anchor_part, ",*") if s.strip())
    if not anchor:
        raise FrameQLSyntaxError("the anchor (after '@') must name at least one level")

    columns = []
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
