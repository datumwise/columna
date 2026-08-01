#!/usr/bin/env python3
"""MAP-2 · D3 — the oracle protocol (the seam-certificate method, generalized).

    python specs/open_planner/map2/oracle_harness.py --selftest

Polars is the PERMANENT REFERENCE ORACLE (charter §4 D3). This module IS the comparison protocol D4's
pilot runs a candidate lowering through; it is importable (`oracle`, `compare`, `Comparison`,
`negative_control`) and self-testing.

THE PROTOCOL, for a candidate lowering L of a Columna plan P:
  1. ORACLE   — execute P natively on the shipped engine (Polars). This is ground truth, by fiat.
  2. CANDIDATE — execute L on the consumer (D4: Acero/DuckDB via Substrait). D3 defines the seam;
                 D4 supplies the consumer. Here the "candidate" is any frame claiming to equal the
                 oracle, so the instruments can be exercised and the negative control proven now.
  3. COMPARE  — under two instruments, tolerance STATED per comparison:
                 • structural-exact — schema (names+dtypes as a set), row count, and the anchor-key
                   set must match EXACTLY. Shapes are never toleranced.
                 • numeric-tolerant — every value cell, joined on the anchor keys, must agree within a
                   STATED absolute tolerance. The digest-of-rounded instrument stays RETIRED (charter).
  4. REQUIRE  — N comparisons, ZERO disagreements, and the PERIMETER (what the certificate covers)
                stated in the result.

THE NEGATIVE CONTROL IS NOT OPTIONAL (charter §4 D3, §5(3)). A harness that has never failed has not
been shown to be able to fail. `negative_control()` takes the oracle, builds ONE deliberately broken
candidate (a dropped row, a perturbed value, a swapped reducer), and asserts the comparison FAILS
loudly — then restores (oracle vs itself) and asserts it PASSES. `control_valid` is
(baseline_pass AND broken_fails AND restored_pass). Until it is True, no positive result counts.
"""
from __future__ import annotations

import dataclasses
import sys
from typing import Optional

import polars as pl


# ---- canonicalization: a frame's identity is its rows-as-a-set at its anchor, order-free ----------

def canonical(df: pl.DataFrame, key_cols: list[str]) -> pl.DataFrame:
    """Sort by the anchor keys and put columns in a stable order, so comparison is order-free."""
    cols = sorted(df.columns)
    return df.select(cols).sort(by=[k for k in sorted(key_cols) if k in cols])


# ---- the comparison result -----------------------------------------------------------------------

@dataclasses.dataclass
class Comparison:
    label: str
    perimeter: str                       # what this certificate covers, in one clause
    tolerance: float                     # the STATED absolute tolerance for the numeric instrument
    n_cells: int = 0                     # value cells compared
    structural_ok: bool = False
    numeric_ok: bool = False
    disagreements: list = dataclasses.field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.structural_ok and self.numeric_ok and not self.disagreements

    def summary(self) -> str:
        v = "PASS" if self.passed else "FAIL"
        return (f"[{v}] {self.label} — structural={self.structural_ok} numeric={self.numeric_ok} "
                f"cells={self.n_cells} tol={self.tolerance:g} disagreements={len(self.disagreements)} "
                f"| perimeter: {self.perimeter}")


# ---- the two instruments -------------------------------------------------------------------------

def _structural(oracle: pl.DataFrame, cand: pl.DataFrame, key_cols: list[str], c: Comparison) -> bool:
    reasons = []
    if set(oracle.columns) != set(cand.columns):
        reasons.append(f"schema names differ: oracle={sorted(oracle.columns)} cand={sorted(cand.columns)}")
    else:
        od = {k: str(v) for k, v in zip(oracle.columns, oracle.dtypes)}
        cd = {k: str(v) for k, v in zip(cand.columns, cand.dtypes)}
        # numeric dtype family is what matters (Int64 vs Float64 across engines is not a shape defect)
        def fam(t): return "num" if any(x in t for x in ("Int", "Float", "Decimal")) else t
        mism = {k: (od[k], cd[k]) for k in od if fam(od[k]) != fam(cd.get(k, ""))}
        if mism:
            reasons.append(f"dtype family differs: {mism}")
    if oracle.height != cand.height:
        reasons.append(f"row count differs: oracle={oracle.height} cand={cand.height}")
    ok_keys = [k for k in key_cols if k in oracle.columns and k in cand.columns]
    if ok_keys:
        okey = set(map(tuple, canonical(oracle, key_cols).select(ok_keys).iter_rows()))
        ckey = set(map(tuple, canonical(cand, key_cols).select(ok_keys).iter_rows()))
        if okey != ckey:
            reasons.append(f"anchor-key sets differ: only-oracle={list(okey-ckey)[:4]} only-cand={list(ckey-okey)[:4]}")
    for r in reasons:
        c.disagreements.append({"instrument": "structural-exact", "detail": r})
    c.structural_ok = not reasons
    return c.structural_ok


def _numeric(oracle: pl.DataFrame, cand: pl.DataFrame, key_cols: list[str], tol: float, c: Comparison) -> bool:
    if not c.structural_ok:               # numeric comparison presupposes aligned shapes
        c.numeric_ok = False
        return False
    keys = [k for k in key_cols if k in oracle.columns]
    val_cols = [col for col in oracle.columns if col not in keys and oracle[col].dtype.is_numeric()]
    o = canonical(oracle, key_cols)
    d = canonical(cand, key_cols)
    worst = 0.0
    for col in val_cols:
        ov, dv = o[col].to_list(), d[col].to_list()
        for i, (a, b) in enumerate(zip(ov, dv)):
            c.n_cells += 1
            if a is None or b is None:
                if a is not b:
                    c.disagreements.append({"instrument": "numeric-tolerant", "col": col, "row": i,
                                            "detail": f"null mismatch oracle={a} cand={b}"})
                continue
            delta = abs(float(a) - float(b))
            worst = max(worst, delta)
            if delta > tol:
                c.disagreements.append({"instrument": "numeric-tolerant", "col": col, "row": i,
                                        "oracle": a, "cand": b, "abs_delta": delta, "tol": tol})
    c.numeric_ok = not any(x["instrument"] == "numeric-tolerant" for x in c.disagreements)
    c._worst_delta = worst               # recorded, not hidden (0.13.1 doctrine)
    return c.numeric_ok


def compare(oracle: pl.DataFrame, cand: pl.DataFrame, key_cols: list[str], *,
            label: str, perimeter: str, tolerance: float) -> Comparison:
    """Run both instruments; tolerance is STATED, not defaulted. Returns a Comparison (never raises on a
    data disagreement — a disagreement is DATA, recorded, per the two-level correctness contract)."""
    c = Comparison(label=label, perimeter=perimeter, tolerance=tolerance)
    _structural(oracle, cand, key_cols, c)
    _numeric(oracle, cand, key_cols, tolerance, c)
    return c


# ---- the oracle ----------------------------------------------------------------------------------

def oracle(store, manifold: str, frameql: str) -> tuple[pl.DataFrame, list[str]]:
    """Execute a Columna ask natively on the shipped engine and return (frame, anchor_key_cols).
    This is the REFERENCE. The frame is the served wire's columns, reassembled as a Polars DataFrame."""
    from columna_server import tools as T
    wire = T.query(store, manifold, frameql)
    if wire.get("outcome") not in ("serve", "disclose"):
        raise RuntimeError(f"oracle ask did not serve ({wire.get('outcome')}): {frameql}")
    cols = wire["columns"]
    anchor_keys = [k for k in cols[0]["values"][0].keys() if k != "value"] if cols and cols[0]["values"] else []
    # reassemble: one row per anchor tuple, one column per series
    rows: dict = {}
    for col in cols:
        for v in col["values"]:
            key = tuple(v[k] for k in anchor_keys)
            rows.setdefault(key, {ak: v[ak] for ak in anchor_keys})
            rows[key][col["name"]] = v["value"]
    frame = pl.DataFrame(list(rows.values())) if rows else pl.DataFrame()
    return frame, anchor_keys


# ---- the mandatory negative control --------------------------------------------------------------

def _break(df: pl.DataFrame, key_cols: list[str], mode: str) -> pl.DataFrame:
    """Produce ONE deliberately broken candidate from the oracle, three ways."""
    val_cols = [col for col in df.columns if col not in key_cols and df[col].dtype.is_numeric()]
    if mode == "perturb_value" and val_cols and df.height:
        col = val_cols[0]
        vals = df[col].to_list()
        vals[0] = (vals[0] or 0.0) + 1.0        # a 1.0 shift — far above any sane tolerance
        return df.with_columns(pl.Series(col, vals))
    if mode == "drop_row" and df.height > 1:
        return df.head(df.height - 1)
    if mode == "swap_scale" and val_cols:
        col = val_cols[0]
        return df.with_columns((pl.col(col) * 2.0).alias(col))   # a doubled column — a wrong reducer's shape
    return df


def negative_control(store, manifold: str, frameql: str, tolerance: float) -> dict:
    """REQUIRED (charter §4 D3). Prove the harness can FAIL: oracle vs a broken candidate must FAIL,
    oracle vs itself must PASS. Returns a dict with control_valid."""
    ref, keys = oracle(store, manifold, frameql)
    baseline = compare(ref, ref, keys, label="baseline(oracle vs self)",
                       perimeter=frameql, tolerance=tolerance)
    broken_results = {}
    for mode in ("perturb_value", "drop_row", "swap_scale"):
        broken = _break(ref, keys, mode)
        cmp = compare(ref, broken, keys, label=f"tamper({mode})", perimeter=frameql, tolerance=tolerance)
        broken_results[mode] = cmp
    restored = compare(ref, oracle(store, manifold, frameql)[0], keys,
                       label="restored(oracle vs fresh oracle)", perimeter=frameql, tolerance=tolerance)
    all_broken_fail = all(not c.passed for c in broken_results.values())
    valid = baseline.passed and all_broken_fail and restored.passed
    return {
        "frameql": frameql, "tolerance": tolerance,
        "baseline_passes": baseline.passed,
        "each_tamper_fails": {m: (not c.passed) for m, c in broken_results.items()},
        "restored_passes": restored.passed,
        "control_valid": valid,
        "note": "a broken lowering MUST fail loudly before any positive result counts",
        "_detail": {m: c.summary() for m, c in broken_results.items()},
    }


# ---- self-test -----------------------------------------------------------------------------------

def main(argv):
    if "--selftest" not in argv:
        print(__doc__)
        return 2
    from columna_server.demo import demo_store
    store = demo_store()

    print("=== D3 oracle harness — self-test ===\n")
    # 1) oracle vs oracle passes; the instruments run on a real served ask.
    ref, keys = oracle(store, "cascadia", "SELECT revenue AT {region}")
    print(f"oracle 'SELECT revenue AT {{region}}' -> {ref.height} rows, anchor keys {keys}")
    same = compare(ref, ref, keys, label="oracle==oracle",
                   perimeter="revenue AT {region}", tolerance=1e-9)
    print(" ", same.summary())

    # 2) THE NEGATIVE CONTROL — must be valid or the harness is not testing.
    print("\n--- negative control (must FAIL on a broken candidate) ---")
    for q in ("SELECT revenue AT {region}",
              "SELECT sum(revenue @ {store*product*cal.month}) AT {cal.month}"):
        ctrl = negative_control(store, "cascadia", q, tolerance=1e-6)
        print(f"  {q}")
        print(f"    baseline_passes={ctrl['baseline_passes']} "
              f"each_tamper_fails={ctrl['each_tamper_fails']} restored={ctrl['restored_passes']} "
              f"-> control_valid={ctrl['control_valid']}")

    ok = ctrl["control_valid"] and same.passed
    print("\nSELF-TEST:", "PASS — the oracle agrees with itself and the negative control is valid"
          if ok else "FAIL — the harness cannot be trusted until this is green")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
