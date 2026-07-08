"""
coanchor_demo.py — D5 ratio / rate co-anchoring (ADR-032 D5).

A ratio N / D is a binary derived column whose determinacy is a *co-anchoring* requirement on
its two operand measures: it has a single value only when numerator and denominator resolve
over one shared population. So:

  * same-universe ratio (revenue / orders, both ON transactions) -> SERVE — one population.
  * cross-universe ratio (revenue / level: revenue ON transactions, level ON store_days)
    -> CLARIFY (discriminator=ambiguous): which population is the rate taken over? The engine
    could produce a number per cell, but the *meaning* is ambiguous, so the planner names the
    candidate populations and never guesses.
  * scaling by a constant (revenue / 1000) -> SERVE — not eager; one population.
  * the SAME two measures as two SEPARATE columns -> both SERVED, with a frame-level
    multi-universe coverage caveat, NOT a clarify — proving the clarify is scoped to the ratio
    (a co-anchoring question), distinct from the cross-column population caveat.

This is POPULATION co-anchoring; it is distinct from avg-of-averages, which is a
B-anchor / reaggregability hazard (a served critical caveat), not this.

Run:  python3 coanchor_demo.py
"""
import sys
from columna_core import ManifoldServer, DuckDBConnector, Outcome
from columna_core.disclosure import CLARIFY, AMBIGUOUS, Refusal
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
    print("COLUMNA CORE — D5 ratio/rate co-anchoring (clarify when populations differ)")
    print("=" * 80)
    srv = ManifoldServer(build_manifold(), DuckDBConnector(load()))
    A = ("store", "day")   # both universes (transactions, store_days) are addressable here

    print("\n(A) same-universe ratio serves; cross-universe ratio clarifies")
    same = srv.frame(*A).column("rate", "revenue / orders").run()
    c = col(same, "rate")
    check("revenue / orders (both ON transactions) -> SERVE (one population)",
          c.refusal is None and c.frame is not None and same.outcome != CLARIFY,
          f"outcome={same.outcome}")

    cross = srv.frame(*A).column("rate", "revenue / level.last").run()
    c = col(cross, "rate")
    check("revenue / level.last (transactions vs store_days) -> CLARIFY (ambiguous population)",
          c.refusal is not None and c.refusal.is_clarify and c.refusal.discriminator == AMBIGUOUS,
          f"{c.refusal.kind}/{c.refusal.discriminator}" if c.refusal else "no no-result")
    check("the clarify names BOTH candidate populations (no silent guess)",
          c.refusal is not None
          and any("transactions" in a for a in c.refusal.alternatives)
          and any("store_days" in a for a in c.refusal.alternatives),
          f"alts={list(c.refusal.alternatives)}" if c.refusal else "")
    check("frame-level outcome rolls up to CLARIFY",
          cross.outcome == CLARIFY and len(cross.clarifies) == 1, f"outcome={cross.outcome}")
    check("the clarify is a VALUE (Outcome), not an Exception — a consumer receives data, not a throw",
          isinstance(c.refusal, Outcome) and not isinstance(c.refusal, Exception)
          and not isinstance(c.refusal, Refusal),
          f"type={type(c.refusal).__name__}")
    check("the cross-universe ratio is caught STATICALLY (never reaches the engine)",
          col(srv.frame(*A).column("rate", "revenue / level.last").plan(), "rate").refusal is not None)

    print("\n(B) not eager: a ratio over one population just serves")
    scaled = srv.frame(*A).column("k", "revenue / 1000").run()
    c = col(scaled, "k")
    check("revenue / 1000 -> SERVE (constant denominator, one population)",
          c.refusal is None and c.frame is not None, f"outcome={scaled.outcome}")

    print("\n(C) scoped to the ratio: the same two measures as separate columns SERVE with a caveat")
    twocol = srv.frame(*A).column("rev", "revenue").column("inv", "level.last").run()
    crev, cinv = col(twocol, "rev"), col(twocol, "inv")
    check("revenue and level.last as SEPARATE columns -> both served (no clarify)",
          crev.refusal is None and cinv.refusal is None and not twocol.clarifies,
          f"outcome={twocol.outcome}")
    check("frame carries the multi-universe population caveat (served, not clarified)",
          twocol.disclosure.has("coverage"), twocol.disclosure.render_human())

    print("\n(D) ON UNIVERSE pin — assert the population, resolving the ambiguity (Option A wiring)")
    def pinned(expr, uni, *extra):
        fb = srv.frame(*A).column("c", expr)
        for n, e in extra:
            fb = fb.column(n, e)
        return fb.on_universe(uni).run()

    p = pinned("revenue / orders", "transactions")
    check("pin consistent with both operands -> SERVE (revenue/orders ON transactions)",
          col(p, "c").refusal is None and p.outcome != CLARIFY, f"outcome={p.outcome}")

    p = pinned("revenue / level.last", "transactions")
    check("cross-universe ratio pinned to numerator's universe -> REFUSE (denominator out-of-universe)",
          col(p, "c").refusal is not None and col(p, "c").refusal.is_refuse
          and col(p, "c").refusal.reason == "out_of_universe",
          f"{col(p,'c').refusal.kind}/{col(p,'c').refusal.reason}" if col(p, "c").refusal else "served")
    p = pinned("revenue / level.last", "store_days")
    check("cross-universe ratio pinned to denominator's universe -> REFUSE (numerator out-of-universe)",
          col(p, "c").refusal is not None and col(p, "c").refusal.is_refuse,
          f"{col(p,'c').refusal.reason}" if col(p, "c").refusal else "served")
    check("the SAME ratio WITHOUT a pin still CLARIFIES (D5 unchanged; the pin is what resolves it)",
          col(srv.frame(*A).column("c", "revenue / level.last").run(), "c").refusal.is_clarify)

    p = pinned("level.last", "store_days")
    check("a measure pinned to its own universe -> SERVE (level.last ON store_days)",
          col(p, "c").refusal is None, f"outcome={p.outcome}")
    p = pinned("revenue", "store_days")
    check("a measure pinned to a FOREIGN universe -> REFUSE (out-of-universe for that population)",
          col(p, "c").refusal is not None and col(p, "c").refusal.is_refuse
          and col(p, "c").refusal.reason == "out_of_universe")
    p = pinned("revenue", "no_such_universe")
    check("an unknown pinned universe -> ERROR (not a declared universe)",
          col(p, "c").refusal is not None and col(p, "c").refusal.is_error)

    p = srv.frame(*A).column("rev", "revenue").column("inv", "level.last").on_universe("store_days").run()
    check("two-universe frame pinned -> off-universe column refuses, on-universe serves, caveat resolved",
          len(p.served) == 1 and len(p.refusals) == 1 and not p.disclosure.has("coverage"),
          f"served={len(p.served)} refused={len(p.refusals)} coverage={p.disclosure.has('coverage')}")

    print("\n" + "=" * 80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("=" * 80)
    return 0 if _F == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
