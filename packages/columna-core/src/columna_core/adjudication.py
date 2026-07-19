"""columna_core.adjudication — the Certificate kernel's adjudicator (WP-B).

Turns a *declared* derived-column fertility (the parser records `declared_lineages`, `license=None`)
into an *adjudicated* `License`, by the constitutional ladder:

    authority is declared; mathematics may verify; data may only refute or corroborate; default closed.

Two channels, tried in order (the first that decides, wins):

  math  — compile-time, NO data. A *homogeneous-linear* formula reduced by an *additive-monoid*
          reducer (`sum`) satisfies reduce-path ≡ recompute-path for ALL data — a symbolic proof from
          the formula tree + operator algebraic properties (`OperatorSig.linear`). Verdict VERIFIED,
          timeless (attestation None).

  data  — publish-time, needs the connector. For each declared lineage, compute reduce-path
          (R-reduce the formula's finer values along an edge of that lineage) vs recompute-path
          (the formula evaluated from components at the coarse anchor) on the *attested data*. A
          mismatch beyond tolerance ⇒ CONTRADICTED: publish FAILS CLOSED with the counterexample
          named. Survived (no counterexample) ⇒ CORROBORATED, watermarked to the attestation
          (re-adjudicated when the attestation changes). No testable edge / no connector ⇒
          UNTESTABLE: recorded, visible in describe, but NEVER exercised (ruling §5) — an asserted
          license changes no served number, so it needs no runtime caveat (CV2-2).

Tolerance (ruling §4): exact for integer/decimal outputs; float uses rtol=1e-9, atol=1e-12; the
policy is recorded in the license basis. The comparison sorts fine rows by (coarse, fine) key before
reducing, so the summation order is deterministic where feasible.

The adjudicator is the SOLE constructor of a `License` (the parser never mints one). It runs at
publish; VERIFIED never touches data, so an unpublished manifold simply forgoes the reduce-path
optimization — never a wrong number (the recompute path is always correct; the license is only the
equality theorem that lets the engine skip it).
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field, replace
from typing import Optional

import polars as pl

from .model import License, VERIFIED, CORROBORATED, UNTESTABLE, CONTRADICTED
from .operators import REGISTRY
from .disclosure_wire import code_for, materiality_for

# float tolerance policy (ruling §4)
_RTOL = 1e-9
_ATOL = 1e-12

# reducer name -> polars aggregation (the reduce-path combine). Reducers we can faithfully replay
# over finer values; a declared member outside this set is not data-testable here -> UNTESTABLE.
_REDUCE = {
    "sum":   lambda c: c.sum(),
    "min":   lambda c: c.min(),
    "max":   lambda c: c.max(),
    "mean":  lambda c: c.mean(),
    "count": lambda c: c.count(),
}


class Contradiction(Exception):
    """A declared capability a counterexample in the attested data refutes. Raised at publish; the
    manifold does NOT publish (fail closed, loudly, with the counterexample named). The fertility case
    is the base; ASSERT and HIERARCHY refutations are siblings (same fail-closed contract), so
    `except Contradiction` catches all three."""

    def __init__(self, derived: str, member: str, lineage: str, counterexample: dict):
        self.derived, self.member, self.lineage = derived, member, lineage
        self.counterexample = counterexample
        c = counterexample
        super().__init__(
            f"CONTRADICTED: derived '{derived}' member '{member}' declared FERTILE along "
            f"'{lineage}', but reduce-path ≠ recompute-path on the attested data. Counterexample "
            f"@ {c['anchor']}={c['key']!r}: reduce={c['reduce']!r} vs recompute={c['recompute']!r} "
            f"(|Δ|={c['abs_diff']!r}, tol={c['tol']}). Publish fails closed."
        )


class AssertContradiction(Contradiction):
    """A declared invariant (ASSERT) the attested data violates at publish. Fails closed. (On
    RE-attestation the same violation becomes a scope CUT, not a publish failure — the
    published-scope/cut-set increment; here, at first publish, it fails closed.)"""

    def __init__(self, name: str, universe: str, claim: str, counterexample: dict):
        self.name, self.universe, self.claim = name, universe, claim
        self.counterexample = counterexample
        Exception.__init__(
            self,
            f"CONTRADICTED: assert '{name}' ON '{universe}' — {claim} — is violated on the attested "
            f"data. Counterexample @ {counterexample.get('anchor')}: "
            f"{counterexample.get('left')!r} vs {counterexample.get('right')!r} "
            f"(op {counterexample.get('op')}, tol {counterexample.get('tol')}). Publish fails closed."
        )


class AssertNotWellFormed(Exception):
    """A declared invariant whose expression does not CLEANLY serve at its anchor — ill-posed
    (clarify/refuse/error) OR served only under a CRITICAL disclosure (e.g. a blocked reduction: the
    number does not reconcile, so it is not a clean quantity to hold an invariant against). You may not
    assert what may not be asked: this is a DECLARATION-time well-formedness failure, DISTINCT from
    UNTESTABLE (which stays reserved for askable-but-unattested). Fails publish closed, naming the
    underlying planner reason."""

    def __init__(self, name: str, universe: str, side: str, expr: str, reason: str):
        self.name, self.universe, self.side, self.expr, self.reason = name, universe, side, expr, reason
        Exception.__init__(
            self,
            f"ASSERT '{name}' ON '{universe}' is not well-formed: its {side} '{expr}' does not serve "
            f"cleanly at the anchor — {reason}. You may not assert what may not be asked; publish fails closed."
        )


class HierarchyContradiction(Contradiction):
    """A declared HIERARCHY step that is NOT functional on the attested data (a key with >1 parent).
    Fails closed."""

    def __init__(self, lineage: str, frm: str, to: str, key, n_parents: int):
        self.lineage, self.frm, self.to, self.key = lineage, frm, to, key
        Exception.__init__(
            self,
            f"CONTRADICTED: hierarchy along '{lineage}' — step {frm}->{to} is not functional on the "
            f"attested data: key {key!r} maps to {n_parents} distinct parents. Publish fails closed."
        )


# ─────────────────────────────────────────────────────────────────────────────
# math channel — a symbolic proof of homogeneous linearity over the formula tree
# ─────────────────────────────────────────────────────────────────────────────
_BINOP = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}


def _atom_refs(node: ast.AST):
    """Every measure/derived atom referenced in the subtree (Name or dotted Attribute head)."""
    for n in ast.walk(node):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
            yield n.value.id
        elif isinstance(n, ast.Name):
            yield n.id


def _is_constant_expr(node: ast.AST) -> bool:
    """A SCALAR operand: a literal/declared constant — an expression with NO atom reference. `100`,
    `-5`, `2*3` are scalars; anything naming a measure is data (a data-constant may corroborate,
    never verify — ruling §3), so it is deliberately NOT a scalar here."""
    return next(_atom_refs(node), None) is None


def _homogeneous_linear(node: ast.AST, m) -> bool:
    """Is `node` a HOMOGENEOUS linear form in its measure atoms — a linear combination with scalar
    coefficients and NO additive constant term? (Additive-monoid `sum` distributes over exactly
    these: sum(a·x ± b·y) = a·sum(x) ± b·sum(y); a bare `+ c` offset breaks it.)"""
    if isinstance(node, ast.Expression):
        return _homogeneous_linear(node.body, m)
    if isinstance(node, ast.Constant):
        return False                      # a bare constant term is an offset — not homogeneous
    if isinstance(node, ast.Name):
        d = m.derived.get(node.id)
        if d is not None:                 # a derived atom: recurse into its own formula (soundness)
            return _homogeneous_linear(ast.parse(d.formula, mode="eval"), m)
        return node.id in m.measures      # a measure atom is a degree-1 term
    if isinstance(node, ast.Attribute):   # dotted family member ref (e.g. level.last) — a data atom
        return isinstance(node.value, ast.Name) and node.value.id in m.measures
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return _homogeneous_linear(node.operand, m)
    if isinstance(node, ast.BinOp):
        op = _BINOP.get(type(node.op))
        L, R = node.left, node.right
        if op in ("+", "-"):
            return _homogeneous_linear(L, m) and _homogeneous_linear(R, m)
        if op == "*":                     # scalar-operand rule: exactly one side linear, the other scalar
            return ((_homogeneous_linear(L, m) and _is_constant_expr(R)) or
                    (_is_constant_expr(L) and _homogeneous_linear(R, m)))
        if op == "/":                     # scalar divisor only: data/scalar is linear; data/data is not
            return _homogeneous_linear(L, m) and _is_constant_expr(R)
    return False


def _prove_math(m, derived, reducer: str) -> Optional[License]:
    """The math channel: VERIFIED iff the member's reducer is an additive monoid (`linear` and
    `is_monoid` — i.e. `sum`) AND the formula is a homogeneous linear form. Else None (undecided —
    hand to the data channel)."""
    op = REGISTRY.get(reducer)
    if op is None or not (op.linear and op.is_monoid):
        return None
    if not _homogeneous_linear(ast.parse(derived.formula, mode="eval"), m):
        return None
    return License(
        verdict=VERIFIED,
        lineages=frozenset(derived.family[reducer].declared_lineages),
        basis=(f"symbolic: '{derived.formula}' is a homogeneous linear form; reducer '{reducer}' is "
               f"an additive monoid ⇒ reduce-path ≡ recompute-path for all data (timeless)."),
        attestation=None,
    )


# ─────────────────────────────────────────────────────────────────────────────
# data channel — reduce-path vs recompute-path on the attested data
# ─────────────────────────────────────────────────────────────────────────────
def _tol_for(dtype) -> tuple:
    """(exact, describe) — integer/decimal compare exactly; float carries rtol/atol (ruling §4)."""
    if dtype.is_integer() or dtype == pl.Decimal or str(dtype).startswith("Decimal"):
        return True, "exact (integer/decimal)"
    return False, f"rtol={_RTOL:g}, atol={_ATOL:g} (float)"


def _serve_data(server, anchor: str, name: str, formula: str):
    """Resolve the derived formula at `anchor` via the planner (the recompute path — the engine's
    default). Returns the (key, value) polars frame, or None if it does not cleanly serve there
    (e.g. a co-anchor clarify) — an anchor we cannot test at."""
    fr = server.frame(anchor).column(name, formula).run()
    if fr.outcome in ("clarify", "refuse", "error") or fr.data is None:
        return None
    return fr.data


def _reduce_path(fine_df: pl.DataFrame, edge, con, fine_lvl: str, coarse_lvl: str,
                 name: str, reducer: str) -> pl.DataFrame:
    """R-reduce the finer derived values along one edge to the coarse grain. Deterministic order:
    sort by (coarse, fine) key before the group-wise reduce."""
    emap = con.deliver_edge(edge.provider_table, edge.frm_col, edge.to_col)   # [_frm, _to]
    fine = (fine_df.rename({name: "_v"})
            .with_columns(pl.col(fine_lvl).cast(pl.Utf8).alias("_k")))
    emap = emap.with_columns(pl.col("_frm").cast(pl.Utf8), pl.col("_to").cast(pl.Utf8))
    j = fine.join(emap, left_on="_k", right_on="_frm", how="inner").sort(["_to", "_k"])
    return (j.group_by("_to", maintain_order=True)
             .agg(_REDUCE[reducer](pl.col("_v")).alias("_reduce"))
             .rename({"_to": coarse_lvl}))


def _find_counterexample(reduce_df, recompute_df, coarse_lvl, name) -> Optional[dict]:
    """First cell where reduce-path ≠ recompute-path beyond tolerance, or None."""
    exact, tol_desc = _tol_for(recompute_df[name].dtype)
    a = reduce_df.with_columns(pl.col(coarse_lvl).cast(pl.Utf8))
    b = recompute_df.rename({name: "_recompute"}).with_columns(pl.col(coarse_lvl).cast(pl.Utf8))
    j = a.join(b, on=coarse_lvl, how="inner").sort(coarse_lvl)
    for row in j.iter_rows(named=True):
        rv, cv = row["_reduce"], row["_recompute"]
        # test CLOSENESS and flag its negation — this catches a plain numeric gap AND the pathological
        # cases (a NaN/inf from a division-by-zero the reduce-path hit but recompute did not, or a hole
        # on exactly one side): `not (nan <= tol)` is True, so a non-finite reduce refutes, as it must.
        if rv is None or cv is None:
            if rv is None and cv is None:
                continue                                   # both empty at this cell — no claim to test
            close, diff = False, float("nan")
        else:
            diff = abs(float(rv) - float(cv))
            close = (rv == cv) if exact else (diff <= _ATOL + _RTOL * abs(float(cv)))
        if not close:
            return {"anchor": coarse_lvl, "key": row[coarse_lvl], "reduce": rv,
                    "recompute": cv, "abs_diff": diff, "tol": tol_desc}
    return None


def _prove_data(server, m, derived, reducer: str, attestation: Optional[str], trace) -> License:
    """The data channel. Raises Contradiction on the first refutation (publish fails closed); else
    CORROBORATED if at least one lineage was testable, else UNTESTABLE."""
    fm = derived.family[reducer]
    con = server.engine.con
    if reducer not in _REDUCE:
        return _untestable(derived, reducer, f"reducer '{reducer}' is not data-replayable in Core")

    tested_any, tol_note = False, ""
    for lineage in sorted(fm.declared_lineages):
        edges = [e for e in m.edges if e.lineage == lineage]
        for e in edges:
            recompute = _serve_data(server, e.to, derived.name, derived.formula)
            fine = _serve_data(server, e.frm, derived.name, derived.formula)
            if recompute is None or fine is None:
                continue                                   # not testable at this edge
            reduce_df = _reduce_path(fine, e, con, e.frm, e.to, derived.name, reducer)
            ce = _find_counterexample(reduce_df, recompute, e.to, derived.name)
            if ce is not None:
                raise Contradiction(derived.name, reducer, lineage, ce)
            tested_any = True
            _, tol_note = _tol_for(recompute[derived.name].dtype)
            if trace is not None:
                trace.append(f"corroborate {derived.name}.{reducer} FERTILE {{{lineage}}} @ "
                             f"{e.frm}→{e.to}: reduce ≡ recompute ({tol_note})")

    if not tested_any:
        return _untestable(derived, reducer, "no edge of the declared lineage(s) was testable on the "
                                             "attested data (no clean fine/coarse pair)")
    return License(
        verdict=CORROBORATED,
        lineages=frozenset(fm.declared_lineages),
        basis=f"data-refutation survived: reduce-path ≡ recompute-path on the attested data; tol {tol_note}.",
        attestation=attestation or _watermark(server, m, derived),
    )


def _untestable(derived, reducer: str, why: str) -> License:
    return License(
        verdict=UNTESTABLE,
        lineages=frozenset(derived.family[reducer].declared_lineages),
        basis=f"asserted on authored authority — {why}. Recorded and visible in describe, never exercised.",
        attestation=None,
    )


def _watermark(server, m, derived) -> str:
    """A stable attestation id from the connector versions of the home tables the formula touches —
    so CORROBORATED re-adjudicates when the data is re-attested (a version change ⇒ a new watermark)."""
    con = server.engine.con
    tables = sorted({m.measures[a].home_table for a in set(_atom_refs(ast.parse(derived.formula, mode="eval")))
                     if a in m.measures})
    try:
        parts = [f"{t}@{con.table_version(t)}" for t in tables]
    except Exception:
        parts = tables
    return "attest:" + ";".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# Track-1 channels (B1 ASSERT, B2 HIERARCHY) — same kernel: mint the UNCHANGED License, fail closed
# on refutation. The `License` constructor and `Contradiction` contract are reused verbatim; these are
# new CUSTOMERS of the kernel, not changes to it (the ADR-034 generality test).
# ─────────────────────────────────────────────────────────────────────────────
def _license(verdict, lineages, basis: str, attestation: Optional[str] = None) -> License:
    """Mint a License — the SAME dataclass the fertility channel mints, byte-identical schema."""
    return License(verdict=verdict, lineages=frozenset(lineages), basis=basis, attestation=attestation)


def _attest_tables(con, tables) -> str:
    """A stable attestation id from the connector versions of the tables a trial touched (so
    CORROBORATED re-adjudicates when the data is re-attested)."""
    ts = sorted(set(tables))
    try:
        return "attest:" + ";".join(f"{t}@{con.table_version(t)}" for t in ts)
    except Exception:
        return "attest:" + ";".join(ts)


def _expr_tables(m, *exprs) -> set:
    tables = set()
    for expr in exprs:
        for tok in re.findall(r"[A-Za-z_]\w*", expr or ""):
            if tok in m.measures:
                tables.add(m.measures[tok].home_table)
    return tables


# ---- B2 HIERARCHY: functional-dependence test on the attested data ----------
def _prove_hierarchy(server, m, h) -> License:
    """Each step of the chain must be a genuine key->key function: every `frm` maps to exactly one
    `to` in the provider table. A key with >1 parent ⇒ HierarchyContradiction (publish fails closed).
    No connector / no deliverable edge ⇒ UNTESTABLE (recorded, describe-visible, never exercised)."""
    con = server.engine.con
    tables = []
    # Every hop of every branch must be a genuine key->key function (§2a: adjudication tests every hop;
    # every hop functional ⇒ every chain composition — day->month->quarter — is functional too).
    for chain in h.paths:
        for i in range(len(chain) - 1):
            frm, to = chain[i], chain[i + 1]
            edge = next((e for e in m.edges if e.frm == frm and e.to == to and e.lineage == h.lineage), None)
            if edge is None:                               # desugared edges should always be present
                return _license(UNTESTABLE, {h.lineage}, f"no edge {frm}->{to} along '{h.lineage}' to test")
            try:
                emap = con.deliver_edge(edge.provider_table, edge.frm_col, edge.to_col)   # [_frm, _to]
            except Exception:
                return _license(UNTESTABLE, {h.lineage},
                                f"edge table '{edge.provider_table}' not deliverable — asserted on authored authority.")
            bad = (emap.group_by("_frm").agg(pl.col("_to").n_unique().alias("_n")).filter(pl.col("_n") > 1))
            if bad.height > 0:
                raise HierarchyContradiction(h.lineage, frm, to, bad["_frm"][0], int(bad["_n"][0]))
            tables.append(edge.provider_table)
    paths_desc = " ; ".join(" -> ".join(c) for c in h.paths)
    return _license(CORROBORATED, {h.lineage},
                    f"functional dependence held on the attested data: every hop maps to one parent "
                    f"across {paths_desc} (every branch, so every composition).",
                    attestation=_attest_tables(con, sorted(set(tables))))


# ---- B1 ASSERT: invariant tested at its anchor on the attested data ----------
def _serve_fr(server, anchor: tuple, colname: str, expr: str):
    """Serve one expression at the anchor via the planner (the recompute path). Returns the whole
    FrameResult (so the caller can read both the data and its disclosures)."""
    return server.frame(*anchor).column(colname, expr).run()


def _material_codes(fr) -> set:
    """The wire codes of the MATERIAL caveats a served frame carries (critical ones are already
    excluded upstream by the askability check). The verdict's trial context — cheap honesty."""
    codes = set()
    for col in fr.columns:
        if col.refusal is None:
            for c in col.disclosure.caveats:
                if materiality_for(c.category, c.rel_error) == "material":
                    codes.add(code_for(c.category))
    return codes


def _cmp(l, r, op: str, exact: bool) -> bool:
    l, r = float(l), float(r)
    if op == "==":                                         # only equality rides the tolerance (rider 3)
        return (l == r) if exact else (abs(l - r) <= _ATOL + _RTOL * abs(r))
    if op == "<=":
        return l <= r
    if op == ">=":
        return l >= r
    if op == "<":
        return l < r
    if op == ">":
        return l > r
    return False


def _invariant_counterexample(j, op, lcol, rcol, anchor) -> Optional[dict]:
    exact, tol_desc = _tol_for(j[lcol].dtype)
    for row in j.iter_rows(named=True):
        l, r = row[lcol], row[rcol]
        if l is None or r is None:
            continue                                       # nothing to test at this cell
        if not _cmp(l, r, op, exact):
            return {"anchor": {k: row[k] for k in anchor}, "left": l, "right": r,
                    "op": op, "tol": tol_desc}
    return None


def _clean_serve_reason(fr) -> Optional[str]:
    """Why an invariant expression is NOT cleanly served at its anchor (for assertion), or None if it
    is. Not-clean = the plan is ill-posed (clarify/refuse/error — name the planner reason) OR it serves
    only under a CRITICAL disclosure (name the caveat category). A cleanly-served number is `serve`, or
    `disclose` with no critical caveat."""
    if fr.outcome in ("clarify", "refuse", "error"):
        for col in fr.columns:
            if col.refusal is not None:
                return col.refusal.classified().reason
        return fr.outcome
    for col in fr.columns:
        if col.refusal is None:
            for c in col.disclosure.caveats:
                if c.severity == "critical":
                    return f"critically disclosed ({code_for(c.category)})"   # the wire code (e.g. blocked_reduction)
    return None


def _sql_ref(r, binding) -> str:
    """Render a row-predicate Ref to PHYSICAL SQL (for the WHERE probe only — never the license)."""
    if r.is_literal:
        return str(r.value)
    if r.table is None:
        return binding.get(r.column, r.column)     # row-attribute -> its physical column (share spelling ok)
    return f"{r.table}.{r.column}"                  # physical residue table.col


def _logical_ref(r) -> str:
    """Render a row-predicate Ref LOGICALLY (for the license basis + counterexample claim)."""
    if r.is_literal:
        return str(r.value)
    return f"{r.table}.{r.column}" if r.table else r.column


def _prove_row_assert(server, m, a) -> License:
    """The row-assert DATA channel (case-demo, closing open_forks · row-assert-data-channel): a row-form
    predicate is a per-row contract over the population — probe the attested data for ANY violating row.
    A violation ⇒ AssertContradiction (publish fails closed / reattest degrades). None ⇒ CORROBORATED.
    NULL comparands (e.g. untracked returns) make the comparison NULL, so `NOT (pred)` excludes them —
    they are not violations (the folklore: nulls count as no return)."""
    con = server.engine.con
    u = m.universes[a.universe]
    home = next((mc.home_table for mc in m.measures.values() if mc.universe == a.universe), None)
    if home is None:
        return _license(UNTESTABLE, set(),
                        "row-predicate assert: no measure binds this universe to a home table to test "
                        "against; recorded on authored authority, never exercised.")
    binding = {n: (b.split(".", 1)[1] if "." in b else b) for n, b in u.attributes}
    sql = " AND ".join(f"{_sql_ref(c.left, binding)} {c.op} {_sql_ref(c.right, binding)}"
                       for c in a.predicate.comparisons)
    claim = " AND ".join(f"{_logical_ref(c.left)} {c.op} {_logical_ref(c.right)}"
                         for c in a.predicate.comparisons)
    base_phys = [m.levels[d].realized_by for d in sorted(u.base_dimensions) if d in m.levels]
    try:
        rows = con.deliver_base_values(home, base_phys, f"({sql})")   # _value = the row predicate (bool, NULL-safe)
    except ValueError:
        return _license(UNTESTABLE, set(),                            # no attested rows (empty population)
                        f"row predicate '{claim}' is askable but has no attested rows; recorded on "
                        f"authored authority, never exercised.")
    except Exception:
        # the base-row channel probes HOME-TABLE columns and row-attributes; a predicate over a rollup
        # level (needing a broadcast/join) is not probeable here — recorded, never exercised (ledgered).
        return _license(UNTESTABLE, set(),
                        f"row predicate '{claim}' references a term the base-row channel cannot bind "
                        f"directly (a rollup or joined level); recorded on authored authority, never exercised.")
    if rows.height == 0:
        return _license(UNTESTABLE, set(),
                        f"row predicate '{claim}' is askable but has no attested rows; recorded on "
                        f"authored authority, never exercised.")
    bad = rows.filter(pl.col("_value") == False)   # noqa: E712 — null-safe: NULL comparands are not violations
    if bad.height > 0:
        first = bad.row(0, named=True)
        ce = {d: first[m.levels[d].realized_by] for d in sorted(u.base_dimensions)
              if d in m.levels and m.levels[d].realized_by in first}
        raise AssertContradiction(a.name, a.universe, claim, ce)
    return _license(CORROBORATED, set(),
                    f"row predicate '{claim}' held on every attested row of '{a.universe}'.",
                    attestation=_attest_tables(con, {home}))


def _prove_assert(server, m, a) -> License:
    """Invariant-form: (1) ASKABILITY — plan LHS/RHS statically; if either does not serve cleanly the
    assertion is not well-formed → fail publish CLOSED naming the reason (rider 1: you may not assert
    what may not be asked; never UNTESTABLE). (2) ATTESTATION — serve both at the anchor, compare per
    op (== rides the WP-B tolerance); a violation ⇒ AssertContradiction. Askable-but-unattested (no
    clean frame despite a clean plan) ⇒ UNTESTABLE. Row-form: UNTESTABLE, base-row channel ledgered
    (open_forks.md · row-assert-data-channel)."""
    if a.kind == "row":
        return _prove_row_assert(server, m, a)   # the base-row DATA channel (case-demo) — no longer untestable
    con = server.engine.con
    # (1) askability — static, no data; fail publish closed if not cleanly serveable
    for side, expr in (("LHS", a.left), ("RHS", a.right)):
        reason = _clean_serve_reason(server.frame(*a.anchor).column("_p", expr).plan())
        if reason is not None:
            raise AssertNotWellFormed(a.name, a.universe, side, expr, reason)
    # (2) attestation — needs data; a clean plan that yields no frame is askable-but-unattested
    lfr = _serve_fr(server, a.anchor, "_l", a.left)
    rfr = _serve_fr(server, a.anchor, "_r", a.right)
    if lfr.data is None or rfr.data is None:
        return _license(UNTESTABLE, set(),
                        f"assert '{a.name}' is askable but unattested at {a.anchor} (clean plan, no "
                        f"served frame); recorded on authored authority, never exercised.")
    j = lfr.data.join(rfr.data, on=list(a.anchor), how="inner")
    ce = _invariant_counterexample(j, a.op, "_l", "_r", a.anchor)
    if ce is not None:
        raise AssertContradiction(a.name, a.universe, f"{a.left} {a.op} {a.right}", ce)
    _, tol_note = _tol_for(j["_l"].dtype)
    basis = (f"invariant '{a.left} {a.op} {a.right}' held at {a.anchor} on the attested data "
             f"(tol {tol_note}).")
    trial = sorted(_material_codes(lfr) | _material_codes(rfr))    # verdict's trial context (optional honesty)
    if trial:
        basis += f" Trial values carried material (non-critical) disclosures: {trial}."
    return _license(CORROBORATED, set(), basis,
                    attestation=_attest_tables(con, _expr_tables(m, a.left, a.right)))


# ─────────────────────────────────────────────────────────────────────────────
# The published SCOPE (B1 scope-edit law): a PURE function of declarations × the CURRENT attestation's
# verdicts. No ratchet — reattest is symmetric (a now-holding assert restores its region); history
# lives in watermarks and the ledger, never in scope-state (Huayin, 2026-07-16).
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PublishedScope:
    """The published manifold's SERVING scope — the scope-edit law made concrete, uniform across THREE
    degrade targets (each toward correctness in its own kind): asserts degrade to CUT (cut declarations
    refuse `conflicting_data`), licenses degrade to RECOMPUTE (revoked), edges degrade to BLOCKED
    TRANSPORT (transport across them refuses `contradicted_edge`). Everything else serves untouched.
    Recomputed fresh on every publish/attest from that attestation's verdicts (pure function; no
    history — history lives in watermarks and the ledger)."""
    cut: frozenset = frozenset()          # declaration names (measures + their derived cone) that are CUT
    cut_by: dict = field(default_factory=dict)      # cut decl -> [{assert, universe, counterexample}]
    blocked_edges: frozenset = frozenset()          # (frm, to) whose transport is BLOCKED (refuted hierarchy)
    blocked_by: dict = field(default_factory=dict)  # (frm, to) -> [{lineage, key}]
    licenses: dict = field(default_factory=dict)    # "derived.member" -> verdict (license-state snapshot)


def _revoked_license(fm, why: str) -> License:
    return License(verdict=CONTRADICTED, lineages=frozenset(fm.declared_lineages), basis=why, attestation=None)


def _assert_reads(m, a) -> set:
    """The measure/derived columns an invariant's expression reads (its cut SEED)."""
    names = set()
    for expr in (a.left, a.right):
        for tok in re.findall(r"[A-Za-z_]\w*", expr or ""):
            if tok in m.measures or tok in m.derived:
                names.add(tok)
    return names


def _declaration_cone(m, seeds) -> frozenset:
    """The declaration cone of `seeds`: the seed columns + every derived that transitively references
    one of them (declaration granularity, B1 v1)."""
    cone = set(seeds)
    changed = True
    while changed:
        changed = False
        for dname, d in m.derived.items():
            if dname in cone:
                continue
            refs = {r.split(".", 1)[0] for r in re.findall(r"[A-Za-z_]\w*(?:\.\w+)*", d.formula)}
            if refs & cone:
                cone.add(dname)
                changed = True
    return frozenset(cone)


def _snapshot_licenses(m) -> dict:
    snap = {}
    for dname, d in m.derived.items():
        for member, fm in d.family.items():
            snap[f"{dname}.{member}"] = fm.license.verdict if fm.license else None
    return snap


def scope_from_report(m, report: dict) -> PublishedScope:
    """Build the PublishedScope from a (degrade-mode) adjudication report — a pure read of the current
    verdicts: the cut declarations' cones (with coordinates) and the blocked edges (with the refuting
    key)."""
    cut, cut_by = set(), {}
    for rec in report.get("_cuts", {}).values():
        for decl in rec["cone"]:
            cut.add(decl)
            cut_by.setdefault(decl, []).append({"assert": rec["assert"], "universe": rec["universe"],
                                                "counterexample": rec["counterexample"]})
    blocked, blocked_by = set(), {}
    for edge, rec in report.get("_blocked", {}).items():
        blocked.add(edge)
        blocked_by.setdefault(edge, []).append(rec)
    return PublishedScope(cut=frozenset(cut), cut_by=cut_by,
                          blocked_edges=frozenset(blocked), blocked_by=blocked_by,
                          licenses=_snapshot_licenses(m))


def scope_diff(old: PublishedScope, new: PublishedScope) -> dict:
    """The authoring-event report: what THIS attestation changed vs the previous scope — cuts/restores
    (asserts), revocations/re-licenses (licenses), blocked/unblocked edges (hierarchies). Never a silent
    mutation — this diff is what summons the author to the three exits."""
    revocations, relicenses = [], []
    for k, v in new.licenses.items():
        ov = old.licenses.get(k)
        if ov in (VERIFIED, CORROBORATED) and v == CONTRADICTED:
            revocations.append(k)
        elif ov == CONTRADICTED and v in (VERIFIED, CORROBORATED):
            relicenses.append(k)
    cuts = sorted(new.cut - old.cut)
    newly_blocked = sorted(new.blocked_edges - old.blocked_edges)
    return {"cuts": cuts, "restores": sorted(old.cut - new.cut),
            "revocations": sorted(revocations), "relicenses": sorted(relicenses),
            "blocked_edges": newly_blocked, "unblocked_edges": sorted(old.blocked_edges - new.blocked_edges),
            "cut_by": {d: new.cut_by.get(d, []) for d in cuts},
            "blocked_by": {e: new.blocked_by.get(e, []) for e in newly_blocked}}


# ---- B3 BASIS: the testedness record (serving follows the DECLARATION, not this license) ----
def _prove_basis(basis: str) -> License:
    """BASIS is a SEMANTIC DECLARATION, not a shortcut license — absence-semantics serving follows the
    declaration regardless (like a B-anchor bar). This License records only the claim's TESTEDNESS for
    describe/trust. v1: UNTESTABLE per type (the data-refutation channels need a domain source):
      · events   — oracle-asymmetric (a false events claim is unrefutable; absence-as-zero and
                   absence-as-gap look identical), so asserted-and-disclosed.
      · spine/product — internal-contiguity and completeness both need the level's DOMAIN (min/max/
                   distinct on the ordered axis); that connector domain-read IS the spine-grid work
                   (open_forks OF-5), so the refutation channel rides there.
      · registry — membership is checkable against a source; deferred with the grid (OF-5)."""
    why = {
        "events":   "events basis asserted (oracle-asymmetric: a false events claim is unrefutable) — "
                    "absence renders as zero per the declaration; not data-tested.",
        "spine":    "spine basis asserted — internal-contiguity/completeness need the ordered axis's "
                    "domain (the spine-grid, OF-5); serving renders absence as a gap per the declaration.",
        "product":  "product basis asserted — cartesian completeness needs the domain grid (OF-5); "
                    "serving renders absence as a gap per the declaration.",
        "registry": "registry basis asserted — membership is checkable against a source (OF-5); "
                    "serving follows the declaration.",
    }[basis]
    return _license(UNTESTABLE, set(), why)


# ---- RELATE FACES: the crossing-disposition license (polarity law — closed opens) ----
def _prove_face(face) -> License:
    """A crossing FACE is CLOSED by default (the polarity law: `data may suggest walls, never doors`);
    its License is the door — it OPENS the trip across the non-functional (M:N) edge. Minted only here,
    at publish (never on parse), mirroring FamilyMember fertility and _prove_basis.

    v1 mints the TOUCH verdict: membership expansion is EXACT arithmetic — the value reaches every match,
    there is no partition-of-unity to reconcile (unlike `alloc`) and no canonical pick to test (unlike
    `assign`), so it is VERIFIED (timeless, symbolic; touches no data). The EVENTS-ONLY restriction is a
    SERVING law (enforced at resolve, like a basis declaration), not a verdict: on a spine the same
    expansion would corrupt the grid's own completeness claim."""
    return _license(VERIFIED, set(),
        f"touch crossing '{face.name}': membership expansion is exact arithmetic (the value reaches every "
        f"match; no weights to reconcile) — the license opens the trip. Serving is events-only (spine "
        f"replication corrupts completeness; refused at resolve until that thinking lands).")


# ─────────────────────────────────────────────────────────────────────────────
# entry point
# ─────────────────────────────────────────────────────────────────────────────
def adjudicate(server, *, attestation: Optional[str] = None, trace: Optional[list] = None,
               degrade: bool = False) -> dict:
    """Adjudicate every declared capability on `server.m`, attaching the constructed `License` in
    place. Returns {derived_name: {member: verdict}} plus `_hierarchies`/`_asserts`/`_cuts`.

    `degrade=False` (first PUBLISH): strict — any refutation raises Contradiction (publish fails
    closed). `degrade=True` (RE-ATTEST): a data refutation is a scope EDIT, not a failure — a violated
    fertility license is REVOKED (degrade to recompute), a violated ASSERT CUTS its declaration cone
    (recorded in `_cuts` with counterexample coordinates). HIERARCHY stays strict in both modes: a
    non-functional coordinate structure is a geometry failure, not a scoped data conflict.

    Idempotent within an attestation. The math channel runs first (no data); the data channel only for
    members math leaves undecided."""
    m = server.m
    report: dict = {}
    for dname, d in list(m.derived.items()):
        if not d.family:                       # denotation-only: nothing to adjudicate
            continue
        new_family, verdicts = {}, {}
        for member, fm in d.family.items():
            try:
                lic = _prove_math(m, d, member) or _prove_data(server, m, d, member, attestation, trace)
            except Contradiction:              # fertility refutation
                if not degrade:
                    raise                      # first publish: fail closed
                lic = _revoked_license(fm, "fertility refuted on re-attestation — license revoked; the "
                                            "engine recomputes (asserts guard truth costs territory; "
                                            "licenses guard shortcuts costs speed).")
            new_family[member] = replace(fm, license=lic)
            verdicts[member] = lic.verdict
        m.derived[dname] = replace(d, family=new_family)
        report[dname] = verdicts

    # ── Track-1 Certificate customers: HIERARCHY (FD) and ASSERT (invariant/row) ──
    # Same kernel: each mints the UNCHANGED License and fails closed via a Contradiction sibling.
    # Degrade targets are uniform (Huayin, 2026-07-16): asserts→cut, licenses→recompute, edges→blocked
    # transport — each toward correctness in its own kind.
    if m.hierarchies:
        new_h, hv, blocked = [], {}, {}
        for h in m.hierarchies:
            try:
                lic = _prove_hierarchy(server, m, h)
            except HierarchyContradiction as e:    # a step is non-functional on re-attestation
                if not degrade:
                    raise                          # first publish: fail closed (geometry, not a scope edit)
                lic = _license(CONTRADICTED, {h.lineage},
                    f"hierarchy step {e.frm}->{e.to} non-functional on re-attestation — edge BLOCKED; "
                    f"transport along it refuses (edges degrade to blocked transport).")
                blocked[(e.frm, e.to)] = {"lineage": e.lineage, "key": e.key}
            new_h.append(replace(h, license=lic))
            hv[h.lineage] = lic.verdict
        m.hierarchies = new_h
        report["_hierarchies"] = hv
        if degrade:
            report["_blocked"] = blocked
    if m.asserts:
        new_a, av, cuts = [], {}, {}
        for a in m.asserts:
            try:
                lic = _prove_assert(server, m, a)
            except AssertContradiction as e:   # invariant violated by the attested data
                if not degrade:
                    raise                      # first publish: fail closed
                lic = _license(CONTRADICTED, set(),
                               f"invariant '{a.left} {a.op} {a.right}' violated on re-attestation — "
                               f"region CUT until fixed/amended/accepted.")
                cuts[(a.universe, a.name)] = {"assert": a.name, "universe": a.universe,
                    "counterexample": e.counterexample, "cone": _declaration_cone(m, _assert_reads(m, a))}
            new_a.append(replace(a, license=lic))
            av[f"{a.universe}.{a.name}"] = lic.verdict     # names are universe-scoped
        m.asserts = new_a
        report["_asserts"] = av
        if degrade:
            report["_cuts"] = cuts

    # ── B3 BASIS: mint the testedness record per declared basis (serving is independent — §2c/B3) ──
    declared_basis = {n: u for n, u in m.universes.items() if u.basis is not None}
    if declared_basis:
        bv = {}
        for uname, u in declared_basis.items():
            lic = _prove_basis(u.basis)
            m.universes[uname] = replace(u, basis_license=lic)
            bv[uname] = lic.verdict
        report["_basis"] = bv

    # ── RELATE FACES: mint each declared crossing face's license (polarity law; closed opens the trip) ──
    # The parser records faces with license=None; the adjudicator is the sole constructor (kernel reuse,
    # same as fertility/basis). Ship-dark: a manifold declaring no faces (Cascadia) adds nothing.
    if any(r.faces for r in m.non_functional):
        fv, new_nf = {}, []
        for r in m.non_functional:
            if r.faces:
                faces = tuple(replace(f, license=_prove_face(f)) for f in r.faces)
                r = replace(r, faces=faces)
                for f in faces:
                    fv[f"{r.frm}<->{r.to}.{f.name}"] = f.license.verdict
            new_nf.append(r)
        m.non_functional = new_nf
        report["_faces"] = fv
    return report
