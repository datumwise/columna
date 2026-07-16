"""
coanchor_demo.py — the §2c expression law + frame law (2026-07-16).

A column expression evaluates in ONE universe and never crosses the boundary. So:

  * same-universe ratio (revenue / orders, both ON transactions) -> SERVE — one population.
  * cross-universe ratio (revenue / level.last: revenue ON transactions, level ON store_days)
    -> ERROR (`cross_universe`): a language-law category error, NOT a clarify — combining them
    would assert a single population that does not exist. The error names both universes and the
    two legal paths: JUXTAPOSE (ask each as its own column) or DECLARE (a DERIVED carrying its
    population). Caught statically (never reaches the engine); a VALUE, not a throw.
  * scaling by a constant (revenue / 1000) -> SERVE — one population.
  * the two measures as SEPARATE columns -> the FRAME LAW: both served, an alignment view on the
    shared anchor, NO frame-level population caveat (the old multi-universe `coverage` caveat is
    retired — per-column honesty replaces it). This is the juxtapose path, made legal.

`ON UNIVERSE` is dead in the query grammar (§2c): the expression law deleted its last query-side
job, so the demo no longer pins populations at query time.

Run:  python3 coanchor_demo.py
"""
import sys
from columna_core import ManifoldServer, DuckDBConnector, Outcome
from columna_core.disclosure import ERROR, Refusal
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def col(fr, name):
    return next(c for c in fr.columns if c.name == name)

def main():
    print("=" * 80)
    print("COLUMNA CORE — §2c expression law (one universe per column) + frame law (juxtaposition)")
    print("=" * 80)
    srv = ManifoldServer(build_manifold(), DuckDBConnector(load()))
    A = ("store", "day")   # both universes (transactions, store_days) are addressable here

    print("\n(A) same-universe ratio serves; cross-universe ratio is a category ERROR")
    same = srv.frame(*A).column("rate", "revenue / orders").run()
    check("revenue / orders (both ON transactions) -> SERVE (one population)",
          col(same, "rate").refusal is None and col(same, "rate").frame is not None,
          f"outcome={same.outcome}")

    cross = srv.frame(*A).column("rate", "revenue / level.last").run()
    c = col(cross, "rate")
    check("revenue / level.last (transactions vs store_days) -> ERROR (cross_universe), not clarify",
          c.refusal is not None and c.refusal.is_error and c.refusal.reason == "cross_universe",
          f"{c.refusal.kind}/{c.refusal.reason}" if c.refusal else "no no-result")
    check("the error names BOTH universes (no silent guess)",
          c.refusal is not None and "transactions" in c.refusal.detail and "store_days" in c.refusal.detail)
    check("the error offers the TWO legal paths (juxtapose, declare)",
          c.refusal is not None
          and any("juxtapose" in a for a in c.refusal.alternatives)
          and any("declare" in a for a in c.refusal.alternatives),
          f"alts={list(c.refusal.alternatives)}" if c.refusal else "")
    check("frame-level outcome rolls up to ERROR",
          cross.outcome == ERROR and len(cross.errors) == 1, f"outcome={cross.outcome}")
    check("the error is a VALUE (Outcome), not an Exception — a consumer receives data, not a throw",
          isinstance(c.refusal, Outcome) and not isinstance(c.refusal, Exception)
          and not isinstance(c.refusal, Refusal),
          f"type={type(c.refusal).__name__}")
    check("the cross-universe expression is caught STATICALLY (never reaches the engine)",
          col(srv.frame(*A).column("rate", "revenue / level.last").plan(), "rate").refusal is not None)

    print("\n(B) not eager: a ratio over one population just serves")
    scaled = srv.frame(*A).column("k", "revenue / 1000").run()
    check("revenue / 1000 -> SERVE (constant denominator, one population)",
          col(scaled, "k").refusal is None and col(scaled, "k").frame is not None,
          f"outcome={scaled.outcome}")

    print("\n(C) the FRAME LAW: the two measures as separate columns juxtapose (no caveat)")
    twocol = srv.frame(*A).column("rev", "revenue").column("inv", "level.last").run()
    crev, cinv = col(twocol, "rev"), col(twocol, "inv")
    check("revenue and level.last as SEPARATE columns -> both served (juxtaposition, no error)",
          crev.refusal is None and cinv.refusal is None and not twocol.errors,
          f"outcome={twocol.outcome}")
    check("the juxtaposed frame carries NO multi-universe coverage caveat (retired §2c)",
          not twocol.disclosure.has("coverage"), twocol.disclosure.render_human())
    check("the juxtaposition is an alignment view — outcome is serve/disclose, never clarify/error",
          twocol.outcome in ("serve", "disclose"), f"outcome={twocol.outcome}")

    print("\n(D) the DECLARE path: a same-universe declared derived serves (aov = revenue / orders)")
    dec = srv.frame(*A).column("aov", "aov").run()
    check("the declared derived `aov` (ON transactions) -> SERVE — declaration is the other legal path",
          col(dec, "aov").refusal is None and col(dec, "aov").frame is not None, f"outcome={dec.outcome}")

    print("\n" + "=" * 80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("=" * 80)
    return 0 if _F == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
