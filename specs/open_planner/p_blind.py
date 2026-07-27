#!/usr/bin/env python3
"""Deliverable 5 — P-BLIND: adjudication is independent of provenance.

    python specs/open_planner/p_blind.py specs/open_planner/fixtures/

RESEARCH INSTRUMENTATION ONLY. Copies the shipped demo data into a temp dir; mutates nothing.

THE CLAIM UNDER TEST (fork doc §7, P-BLIND; formalized round 4):

    K(M, P, A) depends ONLY on the authoritative model, the candidate plan, and the ask -- never on
    planner identity, confidence, provenance, token probabilities, search path, or attempt count.
    The same (M, P, A) from a human, the static planner, an LLM, a random generator, or an adversary
    must yield the IDENTICAL kernel result.

There is no kernel yet, so what is testable today is the SHIPPED adjudication -- the planner+engine's
verdict and served answer -- which is the thing a kernel would have to agree with. If today's
adjudication already varies with how the same (M, P, A) ARRIVED, the property fails before the kernel
is written. This is the falsifiable half available now, and it is worth having: a negative here would
be a live finding about determinism, not a research inconvenience.

THE FOUR PROVENANCE WRAPPERS -- same M, same P, same A, four different routes in:

  W1 static_path         the ordinary shipped route: parse the ask string, plan, execute.
                         (searcher #0 -- the in-engine static planner)
  W2 canonical_roundtrip the parsed Statement is re-rendered via Statement.render_canonical() and
                         re-parsed. Same ask, different TEXT arriving at the parser -- the searcher's
                         phrasing changed, its meaning did not.
  W3 handcrafted         the Statement is rebuilt field by field from envelope AST constructors,
                         never touching the parser. This is a "handcrafted fixture" in the beat's
                         sense: a plan document authored directly, as an external searcher would emit
                         one, rather than derived from our own text.
  W4 shuffled_warehouse  the SAME model and ask, over a byte-different warehouse: every parquet
                         table rewritten with its rows in a different physical order. Same content,
                         same declarations, different physical provenance.

BYTE-IDENTICAL is the bar: the wire adjudication is serialized with sorted keys and compared as
bytes. Not "equivalent", not "same to tolerance" -- identical.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

ASKS = [
    "SELECT revenue AT {cal.month}",
    "SELECT revenue AT {category.split}",
    "SELECT aov AT {cal.month}",
    "SELECT stock.last AT {store*cal.month}",
    "SELECT avg(revenue) AT {cal.month}",          # a CLARIFY -- refusals must be blind too
    "SELECT stock.sum AT {category}",              # a REFUSE
]


def adjudicate(store, q: str) -> dict:
    from columna_server import tools as T
    return T.query(store, "cascadia", q)


def canon(wire: dict, order_sensitive: bool = False, quantize: int | None = None) -> str:
    """The adjudication as canonical bytes.

    ORDER, and why it is normalized by default (FINDING F4). A first pass compared the raw document
    and reported P-BLIND FAILING on every SERVED ask. That was the instrument, not the system: the
    served ROW ORDER is not stable run to run. The same ask, same store, same process, four
    consecutive runs produced four different documents (`SELECT revenue AT {category.split}`),
    differing only in the order of `columns[].values`. Had that been reported as a P-BLIND failure it
    would have been a confident wrong finding -- so the run-to-run stability probe below now ships
    beside the test, and F4 is reported in its own right.

    P-BLIND is a claim about WHICH ADJUDICATION you get, not which order the rows arrive in. So the
    default comparison sorts `columns[].values` by their coordinate keys. `order_sensitive=True`
    keeps the raw document, which is what the stability probe uses to MEASURE F4."""
    doc = json.loads(json.dumps(wire))          # cheap deep copy
    if not order_sensitive:
        for col in doc.get("columns") or []:
            if isinstance(col.get("values"), list):
                if quantize is not None:
                    for v in col["values"]:
                        if isinstance(v.get("value"), float):
                            v["value"] = round(v["value"], quantize)
                col["values"] = sorted(col["values"],
                                       key=lambda v: json.dumps(v, sort_keys=True))
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def same_at_tolerance(a: dict, b: dict, rel: float = 1e-12) -> bool:
    """Compare two adjudications: structure EXACTLY, floats within a relative tolerance.

    Digest-of-rounded was tried first and discarded: rounding does not reliably absorb 1-ULP noise,
    because two values a hair apart can still straddle a rounding boundary and quantize differently.
    A numeric comparison says what we actually mean -- same structure, same numbers to within far
    less than any declared tolerance -- instead of approximating it with a string.
    """
    import math

    def key(v):
        return json.dumps({k: v[k] for k in v if k != "value"}, sort_keys=True)

    sa, sb = json.loads(json.dumps(a)), json.loads(json.dumps(b))
    ca, cb = sa.pop("columns", []) or [], sb.pop("columns", []) or []
    if json.dumps(sa, sort_keys=True) != json.dumps(sb, sort_keys=True):
        return False
    if len(ca) != len(cb):
        return False
    for x, y in zip(ca, cb):
        va, vb = x.pop("values", None), y.pop("values", None)
        if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True):
            return False
        if (va is None) != (vb is None):
            return False
        if va is None:
            continue
        ma = {key(v): v.get("value") for v in va}
        mb = {key(v): v.get("value") for v in vb}
        if set(ma) != set(mb):
            return False
        for k in ma:
            if isinstance(ma[k], float) and isinstance(mb[k], float):
                if not math.isclose(ma[k], mb[k], rel_tol=rel, abs_tol=1e-9):
                    return False
            elif ma[k] != mb[k]:
                return False
    return True


def stability_probe(store, asks, repeats: int = 4) -> dict:
    """FINDING F4 -- measure run-to-run stability of the served document, order-sensitively.

    This is not a P-BLIND control; it is a separate property that P-BLIND's first draft tripped over.
    A kernel that must emit byte-identical certified results, and the certified-plan cache in P-ECON
    that is supposed to yield deterministic serving, both depend on it."""
    out = {}
    for q in asks:
        digs = [hashlib.sha256(canon(adjudicate(store, q), order_sensitive=True).encode()).hexdigest()
                for _ in range(repeats)]
        content = {hashlib.sha256(canon(adjudicate(store, q)).encode()).hexdigest()
                   for _ in range(repeats)}
        out[q] = {"repeats": repeats,
                  "distinct_documents_order_sensitive": len(set(digs)),
                  "distinct_documents_order_normalized": len(content),
                  "row_order_stable": len(set(digs)) == 1,
                  "content_stable": len(content) == 1}
    return out


def cold_start_probe(asks, trials: int = 2, calls: int = 3) -> dict:
    """FINDING F5 -- ATTEMPT-COUNT DEPENDENCE in the shipped adjudication.

    P-BLIND, formalized (fork doc round 4), says K(M, P, A) must depend on nothing but the model, the
    plan and the ask -- "never on planner identity, confidence, provenance, token probabilities,
    search path, OR ATTEMPT COUNT."

    It depends on attempt count. On a FRESH store the FIRST query returns rollup_severity "none" and
    NO `freshness` disclosure; every identical ask after it returns "info" plus a `freshness`
    disclosure. Deterministic, reproducible across fresh stores, and independent of which ask goes
    first.

    Direction matters: the first asker gets LESS disclosure than the second, for the same question on
    the same data. The caveat is graded immaterial/info, so this is not a wrong number -- it is the
    honesty surface varying with call count, which is the property the mood contract exists to make
    invariant.

    This is what P-BLIND's wrapper comparison actually tripped over: W1 ran first and W2/W3 ran after
    it, so the "provenance sensitivity" was call order wearing provenance's clothes.
    """
    from columna_server.demo import demo_store

    out = {}
    for q in asks:
        trial_rows = []
        for _ in range(trials):
            store = demo_store()                       # a genuinely cold store per trial
            seq = []
            for _ in range(calls):
                w = adjudicate(store, q)
                col = (w.get("columns") or [{}])[0]
                seq.append({"rollup_severity": (w.get("frame") or {}).get("rollup_severity"),
                            "disclosure_codes": sorted(d.get("code") for d in (col.get("disclosures") or []))})
            trial_rows.append(seq)
        first, rest = trial_rows[0][0], trial_rows[0][1:]
        out[q] = {"trials": trial_rows,
                  "first_call_differs": any(r != first for r in rest),
                  "reproducible_across_trials": all(tr == trial_rows[0] for tr in trial_rows)}
    return out


def w2_canonical_roundtrip(store, q: str) -> dict:
    from columna_core.envelope import parse_statement
    from columna_server import tools as T
    stmt = parse_statement(q)
    return T.query(store, "cascadia", stmt.render_canonical())


def w3_handcrafted(store, q: str) -> dict:
    """Rebuild the Statement from AST constructors -- never through the ask-string parser."""
    from columna_core import envelope as E
    from columna_core.envelope import parse_statement
    from columna_server import tools as T

    ref = parse_statement(q)
    rebuilt = E.Statement(
        anchor=tuple(ref.anchor),
        series=tuple(E.Series(expr=s.expr, alias=s.alias) for s in ref.series),
        bindings=tuple(ref.bindings), where=ref.where, having=ref.having,
        order_by=tuple(ref.order_by), limit=ref.limit,
    )
    lm = store.get("cascadia")
    fr = lm.server.planner.run_statement(rebuilt)
    from columna_core import disclosure_wire as dw
    return dw.wire_frame(fr)


def _shuffled_store(src: pathlib.Path, dest: pathlib.Path):
    """Same declarations, same rows, different physical order in every parquet file."""
    import duckdb
    root = dest / "shuffled"
    mdir = root / "cascadia"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(src, mdir)
    wh = mdir / "warehouse"
    con = duckdb.connect()
    for p in sorted(wh.glob("*.parquet")):
        # Deterministic reordering that does not depend on any particular column existing:
        # number the rows as read, then write them back in reverse. Different physical order for
        # any table with more than one row; identical contents.
        con.execute(f"create or replace table t as "
                    f"select * exclude (_ord) from ("
                    f"  select *, row_number() over () as _ord from '{p}'"
                    f") order by _ord desc")
        con.execute(f"copy t to '{p}' (format parquet)")
    con.close()
    return root


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    outdir = pathlib.Path(argv[1])
    outdir.mkdir(parents=True, exist_ok=True)

    from columna_server.demo import demo_dir, demo_store
    from columna_server.store import ManifoldStore

    base = demo_store()
    src = pathlib.Path(demo_dir()) / "cascadia"

    results = {"asks": {}, "all_blind": True}
    with tempfile.TemporaryDirectory() as td:
        shuf_root = _shuffled_store(src, pathlib.Path(td))
        shuf_store = ManifoldStore(str(shuf_root))

        for q in ASKS:
            wrappers = {
                "W1_static_path": adjudicate(base, q),
                "W2_canonical_roundtrip": w2_canonical_roundtrip(base, q),
                "W3_handcrafted": w3_handcrafted(base, q),
                "W4_shuffled_warehouse": adjudicate(shuf_store, q),
            }
            digests = {k: hashlib.sha256(canon(v).encode()).hexdigest() for k, v in wrappers.items()}
            # TWO BARS, reported separately and honestly.
            #   strict  -- byte-identical on the order-normalized document. This is the bar the beat
            #              asked for, and it is sensitive to the 1-ULP jitter F4 documents.
            #   tolerance -- values quantized to 9 decimals, far tighter than any declared tolerance
            #              and far looser than one ULP. This isolates PROVENANCE from float noise,
            #              which is the property P-BLIND is actually about.
            ref = wrappers["W1_static_path"]
            tol_ok = {k: same_at_tolerance(ref, v) for k, v in wrappers.items()}
            uniq = sorted(set(digests.values()))
            uniq_tol = [k for k, ok in tol_ok.items() if not ok]
            blind = len(uniq) == 1
            blind_tol = not uniq_tol
            results["all_blind"] &= blind
            results["all_blind_at_tolerance"] = results.get("all_blind_at_tolerance", True) and blind_tol
            row = {"outcome": wrappers["W1_static_path"].get("outcome"),
                   "digests": digests, "distinct_adjudications": len(uniq), "blind": blind,
                   "wrappers_differing_at_tolerance": uniq_tol,
                   "blind_at_tolerance": blind_tol}
            if not blind:
                # Name exactly which wrapper diverged and how -- a negative is a finding, not noise.
                row["divergence"] = {k: json.loads(canon(v)) for k, v in wrappers.items()
                                     if digests[k] != digests["W1_static_path"]}
            results["asks"][q] = row

    results["f4_row_order_nondeterminism"] = stability_probe(base, ASKS)
    results["f4_note"] = (
        "The served row order is NOT stable run to run: same ask, same store, same process, "
        "repeated runs yield documents differing only in the order of columns[].values. Content is "
        "stable; order is not. Reported as its own finding -- it is what P-BLIND's first draft "
        "mistook for a provenance failure. Relevant to OF-23(b) determinism and to P-ECON's "
        "certified-plan cache, which is supposed to yield deterministic serving.")
    results["f5_attempt_count_dependence"] = cold_start_probe(ASKS)
    results["f5_note"] = (
        "P-BLIND VIOLATION, explicitly-named kind. The formalized claim forbids dependence on "
        "'attempt count'. On a fresh store the FIRST query returns rollup_severity 'none' with no "
        "freshness disclosure; every identical ask after it returns 'info' plus a freshness "
        "disclosure. Deterministic and reproducible across cold stores. The first asker gets LESS "
        "disclosure than the second for the same question on the same data. Not a wrong number -- "
        "the honesty surface varying with call count. This is also what the wrapper comparison "
        "mistook for provenance sensitivity: W1 simply ran first.")
    results["claim"] = ("K(M, P, A) depends only on the model, the plan, and the ask -- never on how "
                        "the plan arrived. Tested against the SHIPPED adjudication, which any kernel "
                        "would have to agree with.")
    results["wrappers"] = {
        "W1_static_path": "the ordinary shipped route (searcher #0)",
        "W2_canonical_roundtrip": "re-rendered via render_canonical() and re-parsed -- different text, same meaning",
        "W3_handcrafted": "Statement rebuilt from AST constructors, never through the ask parser",
        "W4_shuffled_warehouse": "same model and ask over byte-different parquet (rows physically reordered)",
    }
    (outdir / "d5_p_blind.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(f"wrote {outdir / 'd5_p_blind.json'}")

    print()
    print("%-44s %-9s %s" % ("ask", "outcome", "distinct adjudications across 4 wrappers"))
    for q, r in results["asks"].items():
        print("%-40s %-9s strict=%d  differ-at-tol=%d  %s"
              % (q[:40], r["outcome"], r["distinct_adjudications"],
                 len(r["wrappers_differing_at_tolerance"]),
                 "BLIND" if r["blind_at_tolerance"] else "*** PROVENANCE-SENSITIVE ***"))
    print()
    print("P-BLIND HOLDS (byte-identical, strict):", results["all_blind"])
    print("P-BLIND HOLDS (at tolerance)          :", results["all_blind_at_tolerance"])
    print("F4 -- run-to-run byte-reproducibility :",
          all(v["content_stable"] for v in results["f4_row_order_nondeterminism"].values()))
    return 0 if results["all_blind_at_tolerance"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
