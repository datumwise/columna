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
from dataclasses import replace
from typing import Optional

import polars as pl

from .model import License, VERIFIED, CORROBORATED, UNTESTABLE
from .operators import REGISTRY
from .disclosure_wire import code_for

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
    for i in range(len(h.chain) - 1):
        frm, to = h.chain[i], h.chain[i + 1]
        edge = next((e for e in m.edges if e.frm == frm and e.to == to and e.lineage == h.lineage), None)
        if edge is None:                                   # desugared edges should always be present
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
    return _license(CORROBORATED, {h.lineage},
                    f"functional dependence held on the attested data: every key maps to one parent "
                    f"across {' -> '.join(h.chain)}.", attestation=_attest_tables(con, tables))


# ---- B1 ASSERT: invariant tested at its anchor on the attested data ----------
def _serve_expr(server, anchor: tuple, colname: str, expr: str):
    """Serve one expression at the anchor via the planner (the recompute path). Returns the frame
    (anchor levels + `colname`), or None if it does not cleanly serve there."""
    fr = server.frame(*anchor).column(colname, expr).run()
    if fr.outcome in ("clarify", "refuse", "error") or fr.data is None:
        return None
    return fr.data


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


def _prove_assert(server, m, a) -> License:
    """Invariant-form: (1) ASKABILITY — plan LHS/RHS statically; if either does not serve cleanly the
    assertion is not well-formed → fail publish CLOSED naming the reason (rider 1: you may not assert
    what may not be asked; never UNTESTABLE). (2) ATTESTATION — serve both at the anchor, compare per
    op (== rides the WP-B tolerance); a violation ⇒ AssertContradiction. Askable-but-unattested (no
    clean frame despite a clean plan) ⇒ UNTESTABLE. Row-form: UNTESTABLE, base-row channel ledgered
    (open_forks.md · row-assert-data-channel)."""
    if a.kind == "row":
        return _license(UNTESTABLE, set(),
                        "row-predicate assert recorded on authored authority — its base-row data "
                        "channel is ledgered (open_forks.md · row-assert-data-channel); visible in "
                        "describe, never exercised.")
    con = server.engine.con
    # (1) askability — static, no data; fail publish closed if not cleanly serveable
    for side, expr in (("LHS", a.left), ("RHS", a.right)):
        reason = _clean_serve_reason(server.frame(*a.anchor).column("_p", expr).plan())
        if reason is not None:
            raise AssertNotWellFormed(a.name, a.universe, side, expr, reason)
    # (2) attestation — needs data; a clean plan that yields no frame is askable-but-unattested
    left = _serve_expr(server, a.anchor, "_l", a.left)
    right = _serve_expr(server, a.anchor, "_r", a.right)
    if left is None or right is None:
        return _license(UNTESTABLE, set(),
                        f"assert '{a.name}' is askable but unattested at {a.anchor} (clean plan, no "
                        f"served frame); recorded on authored authority, never exercised.")
    j = left.join(right, on=list(a.anchor), how="inner")
    ce = _invariant_counterexample(j, a.op, "_l", "_r", a.anchor)
    if ce is not None:
        raise AssertContradiction(a.name, a.universe, f"{a.left} {a.op} {a.right}", ce)
    _, tol_note = _tol_for(j["_l"].dtype)
    return _license(CORROBORATED, set(),
                    f"invariant '{a.left} {a.op} {a.right}' held at {a.anchor} on the attested data "
                    f"(tol {tol_note}).", attestation=_attest_tables(con, _expr_tables(m, a.left, a.right)))


# ─────────────────────────────────────────────────────────────────────────────
# entry point
# ─────────────────────────────────────────────────────────────────────────────
def adjudicate(server, *, attestation: Optional[str] = None, trace: Optional[list] = None) -> dict:
    """Adjudicate every declared derived-column fertility on `server.m`, attaching the constructed
    `License` to each member (rebuilding the frozen dataclasses in place). Returns
    {derived_name: {member: verdict}}. Raises Contradiction (publish fails closed) on any refutation.

    Idempotent within an attestation: re-running re-derives the same verdicts. The math channel runs
    first and never touches data; the data channel runs only for members math leaves undecided."""
    m = server.m
    report: dict = {}
    for dname, d in list(m.derived.items()):
        if not d.family:                       # denotation-only: nothing to adjudicate
            continue
        new_family, verdicts = {}, {}
        for member, fm in d.family.items():
            lic = _prove_math(m, d, member) or _prove_data(server, m, d, member, attestation, trace)
            new_family[member] = replace(fm, license=lic)
            verdicts[member] = lic.verdict
        m.derived[dname] = replace(d, family=new_family)
        report[dname] = verdicts

    # ── Track-1 Certificate customers: HIERARCHY (FD) and ASSERT (invariant/row) ──
    # Same kernel: each mints the UNCHANGED License and fails closed via a Contradiction sibling.
    if m.hierarchies:
        new_h, hv = [], {}
        for h in m.hierarchies:
            lic = _prove_hierarchy(server, m, h)
            new_h.append(replace(h, license=lic))
            hv[h.lineage] = lic.verdict
        m.hierarchies = new_h
        report["_hierarchies"] = hv
    if m.asserts:
        new_a, av = [], {}
        for a in m.asserts:
            lic = _prove_assert(server, m, a)
            new_a.append(replace(a, license=lic))
            av[f"{a.universe}.{a.name}"] = lic.verdict     # names are universe-scoped
        m.asserts = new_a
        report["_asserts"] = av
    return report
