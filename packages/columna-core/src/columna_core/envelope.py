"""
columna_core.envelope — the FrameQL ENVELOPE grammar (0.9.0): parser + AST.

The shipped terse `cols @ anchor` form is a *fragment*; the envelope is the language (WP-FrameQL
grammar spec, ratified by Huayin 2026-07-17). This module parses the statement form

    [EXPLAIN] [FROM <manifold>] [WITH <name> = <expr> [, …]]
    SELECT <series> [AS <alias>] [, …]
    AT { <anchor> }
    [WHERE <pred> [AND …]] [HAVING <pred> [AND …]]
    [ORDER BY <col> [ASC|DESC] [, …]] [LIMIT <n> [PER { <dims> }]]

into a `Statement` AST.

Two anchors, one marker each (the ruling that made the fragment un-shippable — its two `@`s meant
opposite things):
  • `@ { <input anchor> }` inside a series — the INPUT anchor (the grain a reduction reads its operand
    at). `@` is the input marker UNIVERSALLY; series-internal expression text (including `@`) is
    captured verbatim and delegated to the expression parser at plan time (ONE expression dialect).
  • `AT { <anchor> }` — the OUTPUT grain, the SOLE output-anchor syntax. The trailing-`@` output form
    is RETIRED.

Scope of THIS increment: PARSE ONLY. It produces the AST and raises `EnvelopeSyntaxError` on a grammar
violation, in the four-mood temperament — the remedy names itself. It enforces NO naming law (§4) and
NO clause-reference law (§5): those are plan-time (the planner owns assembly; the engine stays
envelope-blind). Reserved words (case-insensitive, whole-word): EXPLAIN FROM WITH SELECT AS AT WHERE
HAVING ORDER BY LIMIT PER ASC DESC AND.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INT = re.compile(r"-?\d+")

# structural clause keywords, in canonical statement order (SELECT + AT required; the rest optional)
_CLAUSE_ORDER = ["EXPLAIN", "FROM", "WITH", "SELECT", "AT", "WHERE", "HAVING", "ORDER BY", "LIMIT"]
_SINGLE_KW = {"EXPLAIN", "FROM", "WITH", "SELECT", "AT", "WHERE", "HAVING", "LIMIT"}


class EnvelopeSyntaxError(ValueError):
    """The query does not fit the FrameQL envelope. Rides the existing `frameql_syntax` query-error
    channel (no new wire reason code); its message names the remedy (four-mood temperament)."""


# --- AST -----------------------------------------------------------------------------------------
@dataclass
class Series:
    """One output column. `expr` is verbatim expression text (delegated to the expression parser at
    plan time); `alias` is the explicit `AS` name, or None (a mechanical default is computed at plan
    time — the parser does not invent names)."""
    expr: str
    alias: Optional[str] = None


@dataclass
class Binding:
    """A `WITH name = expr` macro binding — the reuse device; substituted before desugaring (plan
    time). The parser only records the pair."""
    name: str
    expr: str


@dataclass
class OrderKey:
    column: str            # references an output-frame column (alias/default or anchor coordinate) — checked at plan
    descending: bool = False


@dataclass
class Limit:
    n: int
    per: tuple = ()        # anchor coordinates (a `{…}` list), or () — that PER ⊆ ORDER BY is a plan-time law


@dataclass
class Statement:
    series: list                                   # [Series]  (≥1)
    anchor: tuple                                  # levels of AT {…}; () is the grand-total frame
    explain: bool = False
    from_manifold: Optional[str] = None            # None => the bound manifold (required only multi-manifold)
    bindings: list = field(default_factory=list)   # [Binding]
    where: list = field(default_factory=list)      # [str]  per-series predicates
    having: list = field(default_factory=list)     # [str]  output-frame predicates
    order_by: list = field(default_factory=list)   # [OrderKey]
    limit: Optional[Limit] = None

    def render_canonical(self) -> str:
        """Re-emit the statement in normalized canonical spelling (`*` anchors, one clause per line).
        A round-trip witness that the parse captured the structure; also the seed of EXPLAIN's
        `desugared` field in a later increment."""
        out = []
        if self.explain:
            out.append("EXPLAIN")
        if self.from_manifold:
            out.append(f"FROM {self.from_manifold}")
        for b in self.bindings:
            out.append(f"WITH {b.name} = {b.expr}")
        cols = ", ".join(s.expr + (f" AS {s.alias}" if s.alias else "") for s in self.series)
        out.append(f"SELECT {cols}")
        out.append("AT {" + "*".join(self.anchor) + "}")
        if self.where:
            out.append("WHERE " + " AND ".join(self.where))
        if self.having:
            out.append("HAVING " + " AND ".join(self.having))
        if self.order_by:
            out.append("ORDER BY " + ", ".join(k.column + (" DESC" if k.descending else "") for k in self.order_by))
        if self.limit is not None:
            per = (" PER {" + "*".join(self.limit.per) + "}") if self.limit.per else ""
            out.append(f"LIMIT {self.limit.n}{per}")
        return "\n".join(out)


# --- depth-aware scanning helpers ----------------------------------------------------------------
def _check_balance(s: str) -> None:
    depth = 0
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth < 0:
                raise EnvelopeSyntaxError(f"unbalanced brackets — a closing bracket has no opener in {s.strip()!r}")
    if depth != 0:
        raise EnvelopeSyntaxError(f"unbalanced brackets — an opener is never closed in {s.strip()!r}")


def _split_top(s: str, seps: str) -> list:
    """Split on any separator char in `seps` at bracket depth 0 (parens/brackets/braces all count)."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(s):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0 and ch in seps:
            out.append(s[start:i]); start = i + 1
    out.append(s[start:])
    return out


def _split_top_word(s: str, keyword: str) -> list:
    """Split on a whole-word case-insensitive KEYWORD at bracket depth 0 (for AND / etc.)."""
    up = keyword.upper()
    parts, depth, start, i, n = [], 0, 0, 0, len(s)
    while i < n:
        ch = s[i]
        if ch in "([{":
            depth += 1; i += 1
        elif ch in ")]}":
            depth -= 1; i += 1
        elif depth == 0 and (m := _WORD.match(s, i)):
            if m.group(0).upper() == up:
                parts.append(s[start:i]); start = m.end()
            i = m.end()
        else:
            i += 1
    parts.append(s[start:])
    return parts


def _skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i].isspace():
        i += 1
    return i


def _clause_spans(text: str):
    """Ordered [(KEYWORD, kw_start, kw_end)] for structural clause keywords at bracket depth 0,
    whole-word case-insensitive. 'ORDER BY' matches the ORDER…BY pair. A non-keyword word is skipped
    whole (so `at_risk_count` never trips `AT`)."""
    spans, depth, i, n = [], 0, 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "([{":
            depth += 1; i += 1; continue
        if ch in ")]}":
            depth -= 1; i += 1; continue
        if depth == 0 and (m := _WORD.match(text, i)):
            up = m.group(0).upper()
            if up == "ORDER":
                j = _skip_ws(text, m.end())
                m2 = _WORD.match(text, j)
                if m2 and m2.group(0).upper() == "BY":
                    spans.append(("ORDER BY", m.start(), m2.end())); i = m2.end(); continue
            if up in _SINGLE_KW:
                spans.append((up, m.start(), m.end())); i = m.end(); continue
            i = m.end(); continue
        i += 1
    return spans


# --- clause-body parsers -------------------------------------------------------------------------
def _parse_ident(s: str, what: str) -> str:
    s = s.strip()
    m = _WORD.fullmatch(s)
    if not m:
        raise EnvelopeSyntaxError(f"expected a single name for {what}, got {s!r}")
    return s


def _parse_anchor_braces(body: str, clause: str) -> tuple:
    """`{ a * b }` -> ('a','b'). `{}` -> (). The braces are required; `*` canonical, `,` accepted."""
    body = body.strip()
    if not (body.startswith("{") and body.endswith("}")):
        raise EnvelopeSyntaxError(
            f"{clause} needs a braced anchor — write {clause} {{ level }} (the braces say the anchor is "
            f"a product of levels), e.g. {clause} {{region*store}}; got {body!r}")
    inner = body[1:-1].strip()
    if not inner:
        return ()                                  # the grand-total frame (AT {})
    levels = tuple(p.strip() for p in _split_top(inner, "*,") if p.strip())
    if not levels:
        raise EnvelopeSyntaxError(f"{clause} {{ … }} is empty of levels — name at least one, or use {{}} for the grand total")
    return levels


def _parse_select(body: str) -> list:
    if not body.strip():
        raise EnvelopeSyntaxError("SELECT names no series — a query is a frame of at least one column, "
                                  "e.g. SELECT revenue AT {region}")
    series = []
    for raw in _split_top(body, ","):
        seg = raw.strip()
        if not seg:
            raise EnvelopeSyntaxError("empty series in SELECT (a dangling comma?) — every column is an expression")
        # trailing `AS <alias>` at depth 0
        parts = _split_top_word(seg, "AS")
        if len(parts) == 1:
            series.append(Series(expr=seg, alias=None))
        elif len(parts) == 2:
            expr, alias = parts[0].strip(), parts[1].strip()
            if not expr:
                raise EnvelopeSyntaxError(f"series has an AS alias but no expression before it: {seg!r}")
            series.append(Series(expr=expr, alias=_parse_ident(alias, "an AS alias")))
        else:
            raise EnvelopeSyntaxError(f"series names AS more than once: {seg!r} — one alias per column")
    return series


def _parse_with(body: str) -> list:
    out = []
    for raw in _split_top(body, ","):
        seg = raw.strip()
        if not seg:
            raise EnvelopeSyntaxError("empty WITH binding (a dangling comma?) — each is `name = expression`")
        eq = _split_top(seg, "=")
        if len(eq) < 2 or not eq[0].strip():
            raise EnvelopeSyntaxError(f"malformed WITH binding {seg!r} — write `name = expression` (the reuse device)")
        name = _parse_ident(eq[0], "a WITH name")
        expr = "=".join(eq[1:]).strip()
        if not expr:
            raise EnvelopeSyntaxError(f"WITH {name} = … has no expression on the right of `=`")
        out.append(Binding(name=name, expr=expr))
    return out


def _parse_order_by(body: str) -> list:
    if not body.strip():
        raise EnvelopeSyntaxError("ORDER BY names no column — name an output-frame column, e.g. ORDER BY gross DESC")
    keys = []
    for raw in _split_top(body, ","):
        seg = raw.strip()
        if not seg:
            raise EnvelopeSyntaxError("empty ORDER BY key (a dangling comma?)")
        toks = seg.split()
        desc = False
        if len(toks) >= 2 and toks[-1].upper() in ("ASC", "DESC"):
            desc = toks[-1].upper() == "DESC"
            col = " ".join(toks[:-1]).strip()
        else:
            col = seg
        keys.append(OrderKey(column=col, descending=desc))
    return keys


def _parse_limit(body: str) -> Limit:
    body = body.strip()
    if not body:
        raise EnvelopeSyntaxError("LIMIT needs a row count — e.g. LIMIT 3, or LIMIT 3 PER {region}")
    # optional trailing `PER { … }` at depth 0 — find the PER keyword (whole word, depth 0)
    per = ()
    pos = None
    depth, i, n = 0, 0, len(body)
    while i < n:
        ch = body[i]
        if ch in "([{":
            depth += 1; i += 1
        elif ch in ")]}":
            depth -= 1; i += 1
        elif depth == 0 and (m := _WORD.match(body, i)):
            if m.group(0).upper() == "PER":
                pos = (m.start(), m.end()); break
            i = m.end()
        else:
            i += 1
    if pos is not None:
        n_part, per_part = body[:pos[0]].strip(), body[pos[1]:].strip()
        per = _parse_anchor_braces(per_part, "PER")
    else:
        n_part = body
    if not _INT.fullmatch(n_part.strip()):
        raise EnvelopeSyntaxError(f"LIMIT wants a whole number, got {n_part.strip()!r} — e.g. LIMIT 3")
    n_val = int(n_part.strip())
    if n_val <= 0:
        raise EnvelopeSyntaxError(f"LIMIT must be a positive count, got {n_val}")
    return Limit(n=n_val, per=per)


# --- the statement parser ------------------------------------------------------------------------
def parse_statement(text: str) -> Statement:
    """Parse a FrameQL envelope statement into a `Statement` AST. Raises `EnvelopeSyntaxError` (with a
    remedy named) on a grammar violation. Does NOT resolve anchors, expressions, names, or edges — the
    planner does that (one dialect; envelope-blind engine)."""
    if text is None or not text.strip():
        raise EnvelopeSyntaxError("empty query — a statement is at least `SELECT <series> AT {<anchor>}`")
    text = text.strip()
    _check_balance(text)

    spans = _clause_spans(text)
    kws = [k for (k, _, _) in spans]

    # EXPLAIN only as a leading prefix
    if "EXPLAIN" in kws and kws[0] != "EXPLAIN":
        raise EnvelopeSyntaxError("EXPLAIN is a leading prefix — write it first: EXPLAIN SELECT … AT {…}")
    if kws.count("EXPLAIN") > 1:
        raise EnvelopeSyntaxError("EXPLAIN appears more than once")

    # required clauses
    if "SELECT" not in kws:
        raise EnvelopeSyntaxError("a query must SELECT at least one series — e.g. SELECT revenue AT {region}")
    if "AT" not in kws:
        raise EnvelopeSyntaxError("a query must declare its output grain with AT { … } — name the levels the "
                                  "frame stands at, e.g. SELECT revenue AT {region} (AT {} is the grand total)")

    # each structural clause at most once; canonical order
    seen = {}
    for (k, s, e) in spans:
        if k in seen:
            raise EnvelopeSyntaxError(f"{k} appears more than once — each clause is written once")
        seen[k] = (s, e)
    order_index = {k: idx for idx, k in enumerate(_CLAUSE_ORDER)}
    present = [k for k in kws]
    positions_in_canon = [order_index[k] for k in present]
    if positions_in_canon != sorted(positions_in_canon):
        raise EnvelopeSyntaxError(
            "clauses are out of order — the canonical order is "
            "[EXPLAIN] [FROM] [WITH] SELECT AT [WHERE] [HAVING] [ORDER BY] [LIMIT]; "
            f"got {' '.join(present)}")

    # slice each clause body: from the end of its keyword to the start of the next keyword
    bounds = {}
    for idx, (k, ks, ke) in enumerate(spans):
        nxt = spans[idx + 1][1] if idx + 1 < len(spans) else len(text)
        bounds[k] = text[ke:nxt]

    explain = "EXPLAIN" in seen
    if explain and bounds.get("EXPLAIN", "").strip():
        raise EnvelopeSyntaxError("EXPLAIN takes no argument — it prefixes the whole statement")

    from_manifold = None
    if "FROM" in seen:
        from_manifold = _parse_ident(bounds["FROM"], "the FROM manifold (one name; FROM is optional and "
                                                     "defaults to the bound manifold)")

    bindings = _parse_with(bounds["WITH"]) if "WITH" in seen else []
    series = _parse_select(bounds["SELECT"])
    anchor = _parse_anchor_braces(bounds["AT"], "AT")
    where = [p.strip() for p in _split_top_word(bounds["WHERE"], "AND") if p.strip()] if "WHERE" in seen else []
    having = [p.strip() for p in _split_top_word(bounds["HAVING"], "AND") if p.strip()] if "HAVING" in seen else []
    order_by = _parse_order_by(bounds["ORDER BY"]) if "ORDER BY" in seen else []
    limit = _parse_limit(bounds["LIMIT"]) if "LIMIT" in seen else None

    if "WHERE" in seen and not where:
        raise EnvelopeSyntaxError("WHERE names no predicate — filter the input, e.g. WHERE region = 'west'")
    if "HAVING" in seen and not having:
        raise EnvelopeSyntaxError("HAVING names no predicate — filter the output frame by a column, e.g. HAVING gross > 1000")

    return Statement(series=series, anchor=anchor, explain=explain, from_manifold=from_manifold,
                     bindings=bindings, where=where, having=having, order_by=order_by, limit=limit)
