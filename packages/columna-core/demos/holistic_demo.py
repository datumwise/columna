"""
holistic_demo.py — reaggregation is operator-level (monoid structure), permission is
column-level (B-anchor), and the two gates are INDEPENDENT.

(A) THE HEADLINE — same column, same target, the two gates disagree:
      level.last @ (store, cal.month)  WORKS   — `last` is an ORDERED monoid: carry the
                                                 day as a witness, reduce by argmax.
      level.sum  @ (store, cal.month)  REFUSED — `sum` is a monoid too, so the OPERATOR gate
                                                 lets it through; the COLUMN gate does not.
                                                 `sum` is declared BLOCKED along `calendar`,
                                                 so this reduction has no lawful reading and
                                                 the ask is refused (`blocked_reduction`),
                                                 with `.last` named as the lawful neighbour.
    Reaggregability (monoid) and permission (B-anchor) are different gates, and a monoid
    passing the first one earns nothing at the second.

    RULED 2026-08-20 (Huayin, the generated-family law), superseding ADR-020's inform-and-serve
    for this case: the blocked crossing used to be SERVED with a CRITICAL disclosure attached to
    the number. It is not any more. Disclose exists INSIDE the lawful region — it may qualify an
    otherwise admissible result, it may not legalize an operation the governed law does not
    possess. A caveat riding a total that should never have been computed was the mechanism by
    which the same non-reconciling number kept being served, so the number is now withheld and
    the reader is handed the lawful alternative instead.

(B) HOLISTIC — `median` is not a monoid (no finite witness closes it), so it is
    reduction-sterile: the engine recomputes it from base at the target grain rather
    than reducing a finer result. A median-of-daily-medians would be wrong.

Run:  python3 holistic_demo.py
"""
import sys
from columna_core import ManifoldServer, DuckDBConnector
from build_benchmark import load, build_manifold

_P, _F = 0, 0
def check(name, cond, detail=""):
    global _P, _F
    ok = bool(cond); _P += ok; _F += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))

def main():
    print("="*80)
    print("COLUMNA CORE — monoid reaggregation (operator-level) vs B-anchor (column-level)")
    print("="*80)
    con = load()
    srv = ManifoldServer(build_manifold(), DuckDBConnector(con))
    srv.publish()

    # ── (A) last: ORDERED monoid (carried witness) — works where sum is blocked ──
    print("\n(A) level.last @ (store, cal.month) — ORDERED monoid: carry day, reduce by argmax")
    res = srv.frame("store", "cal.month").column("snap", "level.last").run()
    got = {(r["store"], r["cal.month"]): r["snap"] for r in res.data.iter_rows(named=True)}
    truth = {(r[0], r[1]): r[2] for r in con.execute(
        "SELECT e.store_id, c.month, arg_max(TRY_CAST(e.level AS DOUBLE), e.day) "
        "FROM eom_inventory e JOIN calendar c USING(day) GROUP BY 1,2").fetchall()}
    check("level.last@(store,cal.month) == arg_max(level, day) per (store,month) [period-end snapshot]",
          got and all(abs(got[k]-truth[k]) < 1e-6 for k in truth),
          f"{len(got)} (store,month) cells match DuckDB arg_max ground truth")

    print("    EXPLAIN (reduces in WITNESS space — note witness=(value,order), combine=argmax):")
    for line in res.explain().splitlines():
        if any(w in line for w in ("level.last", "witness", "combine", "transport", "deliver", "confine")):
            print("      " + line)

    res2 = srv.frame("store", "cal.month").column("tot", "level.sum").run()
    col = res2.columns[0]
    ref = col.refusal
    check("level.sum@(store,cal.month) is REFUSED (blocked_reduction) — no number is produced at all",
          ref is not None and ref.kind == "refuse" and ref.reason == "blocked_reduction"
          and ref.discriminator == "unsupported"
          and col.frame is None and not col.disclosure.caveats,
          "a structurally unlawful reduction returns no numeric result under Disclose")
    check("the refusal names the lawful neighbour ('.last') among its alternatives",
          ref is not None and any(".last" in a for a in ref.alternatives))
    print("    → two gates: last is monoid AND B-anchor-clear (clean serve); sum is monoid but "
          "B-anchor-blocked over calendar (REFUSED — the operator gate is not the permission gate).")
    if ref: print("    refusal:", ref.detail)

    # ── (B) median: HOLISTIC (non-monoid) — recompute-from-base, never reduce ──
    print("\n(B) med_amount.median @ cal.month — HOLISTIC: recomputed from base, not reduced")
    res = srv.frame("cal.month").column("med", "med_amount.median").run()
    got = {r["cal.month"]: r["med"] for r in res.data.iter_rows(named=True)}
    truth = {r[0]: r[1] for r in con.execute(
        "SELECT c.month, median(t.amount) FROM transactions t JOIN calendar c USING(day) "
        "GROUP BY 1").fetchall()}
    check("median@cal.month == true median(amount) per month (recomputed from base)",
          got and all(abs(got[k]-truth[k]) < 1e-6 for k in truth),
          f"{len(got)} months match DuckDB median ground truth")

    # show WHY it must recompute: a median-of-daily-medians is NOT the monthly median
    naive = {r[0]: r[1] for r in con.execute(
        "SELECT month, median(dm) FROM ("
        "  SELECT c.month, t.day, median(t.amount) dm FROM transactions t JOIN calendar c USING(day) "
        "  GROUP BY 1,2) GROUP BY 1").fetchall()}
    disagree = sum(1 for k in truth if abs(naive[k]-truth[k]) > 1e-6)
    check("a median-of-daily-medians DISAGREES with the true monthly median (so reduction is invalid)",
          disagree > 0, f"{disagree}/{len(truth)} months differ — no combine exists, hence holistic")

    print("    EXPLAIN (RAW base rows + in-engine recompute — no finer result is a candidate):")
    for line in res.explain().splitlines():
        if any(w in line for w in ("med_amount", "RAW", "recomputed", "broadcast", "HOLISTIC")):
            print("      " + line)

    print("\n" + "="*80)
    print(f"RESULT: {_P} passed, {_F} failed")
    print("="*80)
    sys.exit(1 if _F else 0)

if __name__ == "__main__":
    main()
