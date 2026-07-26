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

from .model import (License, VERIFIED, CORROBORATED, UNTESTABLE, CONTRADICTED,
                    TOUCH, ASSIGN, ORDER_MIN)
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


# (`AssertContradiction` and `AssertNotWellFormed` stood here — the B1 ASSERT channel's fail-closed
#  siblings. RETIRED with the construct in 0.13.0: the assert provers proved a claim no serving
#  behavior depended on, so they failed the admission test. Ruling 2026-07-26.)


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


# (The B1 ASSERT provers — `_prove_assert`, `_prove_row_assert`, and their serve-at-anchor helpers
#  `_serve_fr` / `_material_codes` / `_cmp` / `_invariant_counterexample` / `_clean_serve_reason` /
#  `_sql_ref` / `_logical_ref` — stood here. RETIRED in 0.13.0 (ruling 2026-07-26). Removed, not
#  mothballed: unreachable machinery is where the next fossil grows.)


# ─────────────────────────────────────────────────────────────────────────────
# The published SCOPE (the scope-edit law): a PURE function of declarations × the CURRENT attestation's
# verdicts. No ratchet — reattest is symmetric (a now-functional hierarchy unblocks its edge); history
# lives in watermarks and the ledger, never in scope-state (Huayin, 2026-07-16).
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PublishedScope:
    """The published manifold's SERVING scope — the scope-edit law made concrete, uniform across its
    degrade targets (each toward correctness in its own kind): licenses degrade to RECOMPUTE (revoked),
    edges degrade to BLOCKED TRANSPORT (transport across them refuses `contradicted_edge`). Everything
    else serves untouched. Recomputed fresh on every publish/attest from that attestation's verdicts
    (pure function; no history — history lives in watermarks and the ledger).

    A THIRD degrade target stood here: asserts degraded to CUT, and a query into a cut region refused
    `conflicting_data`. It retired with ASSERT in 0.13.0 (ruling 2026-07-26) — one construct, one
    degrade target, one refusal reason, all three gone together, because the cut region's sole producer
    was a violated assert. `conflicting_data` is tombstoned in disclosure.REASON_OUTCOME and pinned as
    never-emitted."""
    blocked_edges: frozenset = frozenset()          # (frm, to) whose transport is BLOCKED (refuted hierarchy)
    blocked_by: dict = field(default_factory=dict)  # (frm, to) -> [{lineage, key}]
    licenses: dict = field(default_factory=dict)    # "derived.member" -> verdict (license-state snapshot)


def _revoked_license(fm, why: str) -> License:
    return License(verdict=CONTRADICTED, lineages=frozenset(fm.declared_lineages), basis=why, attestation=None)


def _snapshot_licenses(m) -> dict:
    snap = {}
    for dname, d in m.derived.items():
        for member, fm in d.family.items():
            snap[f"{dname}.{member}"] = fm.license.verdict if fm.license else None
    return snap


def scope_from_report(m, report: dict) -> PublishedScope:
    """Build the PublishedScope from a (degrade-mode) adjudication report — a pure read of the current
    verdicts: the blocked edges (with the refuting key) and the license snapshot."""
    blocked, blocked_by = set(), {}
    for edge, rec in report.get("_blocked", {}).items():
        blocked.add(edge)
        blocked_by.setdefault(edge, []).append(rec)
    return PublishedScope(blocked_edges=frozenset(blocked), blocked_by=blocked_by,
                          licenses=_snapshot_licenses(m))


def scope_diff(old: PublishedScope, new: PublishedScope) -> dict:
    """The authoring-event report: what THIS attestation changed vs the previous scope —
    revocations/re-licenses (licenses), blocked/unblocked edges (hierarchies). Never a silent
    mutation — this diff is what summons the author to the three exits. (`cuts`/`restores`/`cut_by`
    stood here; they retired with ASSERT in 0.13.0, ruling 2026-07-26.)"""
    revocations, relicenses = [], []
    for k, v in new.licenses.items():
        ov = old.licenses.get(k)
        if ov in (VERIFIED, CORROBORATED) and v == CONTRADICTED:
            revocations.append(k)
        elif ov == CONTRADICTED and v in (VERIFIED, CORROBORATED):
            relicenses.append(k)
    newly_blocked = sorted(new.blocked_edges - old.blocked_edges)
    return {"revocations": sorted(revocations), "relicenses": sorted(relicenses),
            "blocked_edges": newly_blocked, "unblocked_edges": sorted(old.blocked_edges - new.blocked_edges),
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
class FaceContradiction(Contradiction):
    """A declared crossing FACE whose driver the attested data refutes (a tie at the top for ASSIGN, a
    zero-sum driver for ALLOC, a missing/non-servable driver, or a dependency cycle). Fails publish
    closed, naming the offense — same kernel as the fertility/hierarchy/assert channels."""
    def __init__(self, face_key: str, why: str):
        self.face_key, self.why = face_key, why
        # bypass Contradiction's fertility-shaped __init__ (derived/member/lineage/counterexample); keep the
        # isinstance(., Contradiction) identity so `except Contradiction` catches all four channels.
        Exception.__init__(self, f"CONTRADICTED: face '{face_key}' — {why}; publish fails closed.")


def _face_frontier(m, face, rel) -> str:
    """The frontier grain the driver is served at — the base level of the driver measure's universe.
    Must be one of the RELATE's endpoints (the driver lemma: a spine at the frontier grain)."""
    d = m.measures[face.selection]
    return next(iter(m.universes[d.universe].base_dimensions))


def _prove_face(face, rel, server, m) -> License:
    """A crossing FACE is CLOSED by default (the polarity law); its License is the door — it OPENS the
    trip across the non-functional (M:N) edge. Minted only here, at publish, per scheme:

    · touch  — VERIFIED (timeless, symbolic; touches no data): membership expansion is exact arithmetic.
    · assign — CORROBORATED (touches data): the driver is servable at the frontier grain, present for
               every member, and yields a UNIQUE TOP per member set (no tie-at-top). A tie fails closed.
    · alloc  — CORROBORATED: the driver is non-negative and every member's driver-sum is strictly
               positive (a zero-sum member = undefined split). A violation fails closed.
    The EVENTS-ONLY restriction is a SERVING law (enforced at resolve), not a verdict."""
    key = f"{rel.frm}<->{rel.to}.{face.name}"
    if face.scheme == TOUCH:
        return _license(VERIFIED, set(),
            f"touch crossing '{face.name}': membership expansion is exact arithmetic (the value reaches "
            f"every match; no weights to reconcile). Serving is events-only (spine replication corrupts "
            f"completeness; refused at resolve).")
    # assign / alloc — the driver must be a declared, servable measure at the frontier grain.
    if face.selection not in m.measures:
        raise FaceContradiction(key, f"{face.scheme.upper()} driver '{face.selection}' is not a declared measure")
    d_uni = m.universes[m.measures[face.selection].universe]
    if d_uni.basis is not None and d_uni.basis != "spine":
        # the driver lemma + the acyclicity object (notes §4): a lawful driver is a SPINE at the frontier
        # grain. An events-derived driver ("allocate by last year's revenue share") is lawful ONLY once
        # served and FROZEN as a spine — derived-then-recorded. A raw events measure used as a driver is
        # the un-frozen dependency the acyclicity law forbids; fail closed here where it is concrete.
        raise FaceContradiction(key, f"{face.scheme.upper()} driver '{face.selection}' lives on a "
                                     f"'{d_uni.basis}' universe — a driver must be a SPINE at the frontier "
                                     f"grain. An events-derived driver must first be served and frozen as a "
                                     f"spine (derived-then-recorded); a raw events measure has no single "
                                     f"value per member to rank or weight.")
    frontier = _face_frontier(m, face, rel)
    if frontier not in (rel.frm, rel.to):
        raise FaceContradiction(key, f"driver '{face.selection}' lives at '{frontier}', not a frontier grain "
                                     f"of {rel.frm}<->{rel.to} (the driver lemma: a spine at the frontier)")
    eng = server.engine
    try:
        driver = eng._serve_driver(face, frontier)                     # [frontier, _drv]
    except Exception as e:
        raise FaceContradiction(key, f"driver '{face.selection}' is not servable at '{frontier}': {e}")
    if frontier == rel.to:
        bridge = eng.con.deliver_edge(rel.via_table, rel.via_frm_col, rel.via_to_col)   # _frm=frm, _to=to(frontier)
    else:
        bridge = eng.con.deliver_edge(rel.via_table, rel.via_to_col, rel.via_frm_col)
    b = bridge.join(driver.rename({frontier: "_to"}), on="_to", how="inner")            # _frm, _to, _drv
    member_side = rel.frm if frontier == rel.to else rel.to
    attest = _attest_tables(eng.con, [m.measures[face.selection].home_table, rel.via_table])
    if face.scheme == ASSIGN:
        asc = (face.order == ORDER_MIN)
        top = b.group_by("_frm").agg((pl.col("_drv").min() if asc else pl.col("_drv").max()).alias("_top"))
        tied = (b.join(top, on="_frm").filter(pl.col("_drv") == pl.col("_top"))
                 .group_by("_frm").agg(pl.col("_to"), pl.len().alias("_n")).filter(pl.col("_n") > 1))
        if tied.height:
            ex = tied.head(3).iter_rows(named=True)
            detail = "; ".join(f"{member_side} {r['_frm']}: tied {sorted(r['_to'])}" for r in ex)
            raise FaceContradiction(key, f"ASSIGN ORDER {face.order} on '{face.selection}' has a tie at the top "
                                         f"for {tied.height} {member_side} — no unique designation: {detail}")
        return _license(CORROBORATED, {face.selection}, attestation=attest,
            basis=f"assign crossing '{face.name}': driver '{face.selection}' yields a unique ORDER {face.order} "
                  f"top per {member_side} (single-count preserves mass; the shadow is disclosed).")
    # alloc
    neg = b.filter(pl.col("_drv") < 0)
    if neg.height:
        raise FaceContradiction(key, f"ALLOC driver '{face.selection}' is negative for {neg.height} "
                                     f"membership(s) (e.g. {rel.to} {neg['_to'][0]}) — a weight cannot be negative")
    zero = b.group_by("_frm").agg(pl.col("_drv").sum().alias("_s")).filter(pl.col("_s") <= 0)
    if zero.height:
        raise FaceContradiction(key, f"ALLOC driver '{face.selection}' sums to zero for {zero.height} "
                                     f"{member_side} (e.g. {zero['_frm'][0]}) — an all-zero driver is an "
                                     f"undefined split; declare a positive raw driver")
    return _license(CORROBORATED, {face.selection}, attestation=attest,
        basis=f"alloc crossing '{face.name}': driver '{face.selection}' is non-negative with a strictly "
              f"positive sum per {member_side} (splitting preserves mass; the badge certifies it).")


def _prove_faces_acyclic(server, m) -> None:
    """The acyclicity law (notes §4): the dependency graph {face → its driver measure → that measure's
    universe → any faces serving it would require} must be a DAG. A lawful driver is a spine at the
    frontier grain (native or functionally reachable), so it requires NO crossing — the graph is edgeless
    and trivially acyclic. An edge appears only for an events-derived driver NOT frozen as a spine (it
    could reach the frontier only by crossing a face), which can cycle. Fails publish closed, cycle named."""
    faces = {f"{r.frm}<->{r.to}.{f.name}": (r, f) for r in m.non_functional for f in r.faces if f.selection}
    edges = {k: set() for k in faces}
    for k, (r, f) in faces.items():
        d = m.measures.get(f.selection)
        if d is None:
            continue
        d_base = set(m.universes[d.universe].base_dimensions)
        frontier = _face_frontier(m, f, r)
        # native or functionally reachable ⇒ no crossing ⇒ no edge (the driver lemma, the v1 case).
        if frontier in d_base or m.find_path(d_base, frontier) is not None:
            continue
        # else the driver could only reach the frontier by crossing a face ⇒ edge to every face on a
        # relate touching the frontier (that crossing is REQUIRED to serve this driver).
        for k2, (r2, f2) in faces.items():
            if frontier in (r2.frm, r2.to):
                edges[k].add(k2)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in faces}
    def dfs(u, stack):
        color[u] = GRAY
        for v in edges[u]:
            if color[v] == GRAY:
                return stack[stack.index(v):] + [v]
            if color[v] == WHITE:
                r = dfs(v, stack + [v])
                if r:
                    return r
        color[u] = BLACK
        return None
    for k in faces:
        if color[k] == WHITE:
            cyc = dfs(k, [k])
            if cyc:
                raise FaceContradiction(cyc[0], "the face-driver dependency graph has a CYCLE: "
                                        + " → ".join(cyc) + " (an events-derived driver must first be "
                                        "frozen as a spine at the frontier grain — derived-then-recorded)")


# ─────────────────────────────────────────────────────────────────────────────
# entry point
# ─────────────────────────────────────────────────────────────────────────────
def adjudicate(server, *, attestation: Optional[str] = None, trace: Optional[list] = None,
               degrade: bool = False) -> dict:
    """Adjudicate every declared capability on `server.m`, attaching the constructed `License` in
    place. Returns {derived_name: {member: verdict}} plus `_hierarchies`/`_basis`/`_faces`.

    `degrade=False` (first PUBLISH): strict — any refutation raises Contradiction (publish fails
    closed). `degrade=True` (RE-ATTEST): a data refutation is a scope EDIT, not a failure — a violated
    fertility license is REVOKED (degrade to recompute), and a refuted HIERARCHY blocks transport
    across its edge (recorded in `_blocked` with the refuting key).

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
                                            "engine recomputes (a license guards a shortcut, so revoking "
                                            "it costs speed, never correctness).")
            new_family[member] = replace(fm, license=lic)
            verdicts[member] = lic.verdict
        m.derived[dname] = replace(d, family=new_family)
        report[dname] = verdicts

    # ── Track-1 Certificate customer: HIERARCHY (FD) ──
    # Same kernel: it mints the UNCHANGED License and fails closed via a Contradiction sibling.
    # Degrade targets are uniform (Huayin, 2026-07-16): licenses→recompute, edges→blocked transport —
    # each toward correctness in its own kind. (asserts→cut left with ASSERT in 0.13.0.)
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
        _prove_faces_acyclic(server, m)          # the DAG law first — a cycle fails before any per-face proof
        fv, new_nf = {}, []
        for r in m.non_functional:
            if r.faces:
                faces = tuple(replace(f, license=_prove_face(f, r, server, m)) for f in r.faces)
                r = replace(r, faces=faces)
                for f in faces:
                    fv[f"{r.frm}<->{r.to}.{f.name}"] = f.license.verdict
            new_nf.append(r)
        m.non_functional = new_nf
        report["_faces"] = fv
    return report
