"""columna_core.frameql — the Frame-QL surface."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from .model import Manifold
from .projection import PlannerView
from .engine import ColumnEngine

if TYPE_CHECKING:                     # annotation-only; never imported at runtime
    from .planner import FrameResult

# `Planner` is imported LAZILY, inside `ManifoldServer.__init__`, and that is structural rather than
# stylistic. Since the Frame-QL 1.0 migration the planner imports `columna_core.expr` at module
# scope, `expr` raises this module's `FrameQLSyntaxError`, and a module-scope `from .planner import
# Planner` here would close the loop planner -> expr -> frameql -> planner. The language's error
# channel must sit ABOVE its parser in the import order; the surface that uses the planner can
# perfectly well reach for it when it builds one. `FrameResult` is referenced only in annotations,
# which `from __future__ import annotations` leaves as strings, so it rides the TYPE_CHECKING block.


class ManifoldServer:
    def __init__(self, manifold: Manifold, connector):
        from .planner import Planner                  # lazy: see the import note at the top of the file
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
        """Publish the manifold: ADJUDICATE every declared capability (attaching the constructed License
        — the sole place a License is minted), then materialize the witness store. A CONTRADICTED
        declaration fails closed here: `adjudicate` raises and the manifold does not publish (no
        witnesses built). Returns the number of witnesses built. This is the FIRST-birth act — strict.

        Adjudication is a no-op for a manifold with no declared capability (unchanged behavior)."""
        from .adjudication import adjudicate
        # strict; fails closed. adjudicate establishes the positive PublishedScope (certified edges/faces)
        # as its final atomic step and installs it on the planner — the single governed-serve-ready step.
        self.adjudication = adjudicate(self, attestation=attestation, trace=trace)
        return self.engine.publish_witnesses(trace)

    def _install_closed_scope(self) -> None:
        """P0.5a fail-closed: install an empty PublishedScope (no capability admitted). Used when
        re-attestation cannot produce a coherent result — a stale/ambiguous certification must never
        remain live; governed transport/crossing serving becomes unavailable until a clean adjudication."""
        from .adjudication import PublishedScope
        closed = PublishedScope()
        self.published_scope = closed
        self.planner.install_scope(closed)

    def reattest(self, attestation: Optional[str] = None, trace=None) -> dict:
        """RE-ATTEST an already-published manifold against fresh data — a constitutionally DIFFERENT
        act from `publish` (Huayin, 2026-07-16): a data refutation here EDITS THE PUBLISHED SCOPE
        (degrade), it does not fail closed. Re-adjudicates in degrade mode, recomputes the scope as a
        PURE function of the new verdicts (symmetric — a now-functional hierarchy UNBLOCKS its edge),
        and RETURNS the authoring-event report (the scope diff: revocations, re-licenses, blocked and
        unblocked edges, refuting keys) that summons the author to the three exits. Never mutates
        silently."""
        from .adjudication import adjudicate, scope_diff, PublishedScope
        old = getattr(self, "published_scope", None) or PublishedScope()
        self.engine.cache.clear()          # re-attestation is fresh data — the version-gated cache is stale
        # P0.5a COMPUTE-THEN-SWAP: do NOT clear the live scope before recomputing (the old bug: a
        # clear-before-recompute plus an uncaught face contradiction resurrected blocked edges into
        # serving). adjudicate computes the COMPLETE new verdicts — faces and edges degrade CLOSED, never
        # throw — and installs the coherent new scope atomically at its end. If re-attestation cannot
        # produce a coherent result at all, FAIL CLOSED: a stale/ambiguous certification must never remain
        # live. The adjudicator's own proof-serves use engine/model ops, so the still-live old scope never
        # blocks them.
        try:
            adjudicate(self, attestation=attestation, trace=trace, degrade=True)
        except Exception:
            self._install_closed_scope()
            raise
        new = self.published_scope                          # installed by adjudicate (atomic swap)
        diff = scope_diff(old, new)
        self.engine.publish_witnesses(trace)                # rebuild witnesses for the served regions
        return diff

    def explain_statement(self, stmt) -> dict:
        """EXPLAIN <envelope statement>: the canonical DESUGARED form (the exact artifact the planner
        consumed — desugar()'s output, never a reconstruction) + per-series atom decomposition + the
        dependency cone WITH CURRENT VERDICTS + the would-be annotation, touching ZERO data. The
        planner supplies the shape (provenance-free); the SERVER enriches with verdicts read off this
        Manifold's licenses. The agent's cheap inner loop — exposed on MCP as a tool beside query."""
        from .disclosure_wire import wire_frame
        from .describe import license_to_dict, describe_derived
        p = self.planner
        before = self.engine.con.fetch_count
        d = p.desugar(stmt)                                       # rider 1: the consumed artifact
        fr = p.plan_statement(stmt)                              # would-be annotation (zero fetch)
        would_be = wire_frame(fr, executed=False, fetches_delta=self.engine.con.fetch_count - before)

        def _lic(meas, member):
            mc = self.m.measures.get(meas)
            fm = mc.family.get(member) if (mc and hasattr(mc.family, "get")) else None
            return license_to_dict(fm.license) if (fm and getattr(fm, "license", None)) else None

        series = []
        for s, wcol in zip(d.series, would_be["columns"]):
            atoms, derived_names, edges = p.cone_atoms_and_edges(s.expr, d.anchor)
            for a in atoms:
                a["license"] = _lic(a["measure"], a["member"])   # verdict enrichment (Manifold-side)
            cone = {
                "atoms": atoms,
                "derived": [describe_derived(self.m, n) for n in derived_names],
                "edges": edges,
                # (`cut`/`in_cut_region` stood here — they retired with ASSERT in 0.13.0, ruling
                #  2026-07-26: with no construct able to cut, the fields could only ever be null/false.)
                "scope": {"crosses_blocked_edge": any(e["blocked"] for e in edges)},
            }
            series.append({"name": s.alias, "expr": s.expr, "cone": cone,
                           "would_be": {"status": wcol["status"], "no_result": wcol.get("no_result"),
                                        "disclosures": wcol.get("disclosures", [])}})
        return {"contract_version": would_be["contract_version"], "executed": False,
                "fetches_delta": would_be.get("fetches_delta", 0), "desugared": d.render_canonical(),
                "outcome": would_be["outcome"], "anchor": list(d.anchor), "series": series}

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


# ── the language's syntax-error channel ──────────────────────────────────────────────────────────
# This is the only current surface below this line. Everything after it is quarantined lineage.


class FrameQLSyntaxError(ValueError):
    """A Frame-QL utterance is not readable as Frame-QL.

    The language's OWN error channel, and the whole of it: the expression grammar
    (`columna_core.expr`) raises it on every rejection with a source offset, the planner raises it
    where a statement parses but is not a valid request, and the server relays it as the
    `frameql_syntax` query error. It lives in this module rather than beside the parser because the
    error channel must sit ABOVE the parsers in the import order — see the note at the top of the
    file. No Python-level exception is ever allowed out in its place (P1-26)."""


# ═════════════════════════════════════════════════════════════════════════════════════════════════
#  QUARANTINE — the retired terse `@`-fragment. Read the tombstone on `_parse_retired_fragment`
#  before touching anything below this line. Nothing here is a language surface.
# ═════════════════════════════════════════════════════════════════════════════════════════════════
_SQL_HINTS = ("select ", "insert ", "update ", "delete ", "drop ", "create ", "with ", ";")


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


def _parse_retired_fragment(text: str) -> tuple:
    """Read the RETIRED terse fragment `<columns> @ <anchor>` into (anchor_levels,
    [(column_name, column_expr)]). PRIVATE, and it stays private.

    Fragment grammar, recorded here because nothing else records it any more:

        <query>   ::= <columns> "@" <anchor>
        <columns> ::= <column> ("," <column>)*
        <column>  ::= <name> ":" <expr>  |  <expr>       # bare expr -> the column was named by its text
        <anchor>  ::= <level> (("*" | ",") <level>)*

    ── TOMBSTONE (raised 2026-07-17, WP-FrameQL 0.9.0; quarantined 2026-09-11) ─────────────────────

    THE FRAGMENT IS NOT PART OF FRAME-QL 1.0 AND IS NOT A PUBLIC LANGUAGE SURFACE (ruled 2026-09-11).
    The language is the ENVELOPE — `SELECT <series [AS alias]>,… AT {anchor}`,
    `columna_core.envelope.parse_statement` — in which `@ {…}` is the INPUT-anchor marker universally
    and `AT {…}` is the sole output grain. The fragment spelled both with `@`: the outer one meant the
    output anchor, the inner one the input anchor, and that collision is precisely why it could not
    ship as the language (language reference, Appendix D).

    This is not deprecated public API, because it is not public. It left `columna_core.__all__` and
    the `columna_server.frameql` re-export on 2026-09-11, and the last caller — the docs regeneration
    harness — moved to `parse_statement` in the same change.

    Nor is its `:` the language's `:`. The fragment's colon was a COLUMN LABEL, in the position `AS`
    occupies today; that role was declined and is still declined. Frame-QL 1.0's colon marks a NAMED
    ARGUMENT inside a call (`lag(revenue, n: 1)`), a job the fragment had no surface to spell. One
    character, two roles — the declined one was never adopted (Appendix D).

    WHAT IT IS KEPT FOR. The fragment has an archived body of text behind it — recorded transcripts,
    corpus pages, site query strings, early manual drafts — and this function is the executable
    definition of what those strings meant. A prose description of a retired grammar cannot be run
    against the material written in it; this can. That is the whole warrant, and it is a lineage
    warrant, not a compatibility one.

    IT MUST NOT ACQUIRE NEW CALLERS. A caller here is a caller of a retired grammar; anything that
    needs to read a query reaches for `parse_statement`. Kept rather than deleted because
    vocabularies grow by rule and shrink by tombstone, never silently.

    Raises FrameQLSyntaxError on a fragment violation. Recovers the SHAPE a fragment string carried
    and nothing more — it validates neither expressions nor levels, and never did.
    """
    if text is None or not text.strip():
        raise FrameQLSyntaxError("empty query")
    low = text.strip().lower()
    if any(h in low for h in _SQL_HINTS):
        raise FrameQLSyntaxError("this looks like SQL; the retired fragment read "
                                 "'<columns> @ <anchor>', never SQL")

    parts = _split_top(text, "@")
    if len(parts) != 2:
        raise FrameQLSyntaxError("the fragment form has exactly one '@' separating columns from "
                                 "the anchor, e.g. \"revenue @ region\"")
    cols_part, anchor_part = parts

    # the anchor product: `*` was the fragment's canonical separator (the SAME operator as
    # UNIVERSE a * b * c) and the comma a tolerated input spelling. Both are read here because both
    # were written; archived text does not get to be re-spelled after the fact.
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
        raise FrameQLSyntaxError("the fragment form has at least one column before '@'")
    return anchor, columns
