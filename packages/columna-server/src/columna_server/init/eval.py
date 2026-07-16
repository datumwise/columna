"""
columna_server.init.eval — the eval suite: run record, scorer, report (CP-2, to the STANDING contract
`specs/wp_cp2_eval_run_record_v0_1.md`).

Golden authoring benchmarks are the ratchet. This module is the MEASUREMENT DEVICE — it scores an init
OUTPUT against a benchmark's adjudicated ground truth, on the ratified axes (closure · grade ·
explicitness · checklist-concentration · convergence), and renders the standing report. It is scorer
logic only: the judgment being scored is the mind's; this compares its result to ratified ground truth,
so the eval is testable hermetically with scripted outputs (validating the instrument, not a mind).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

SCORER_VERSION = "0.3"                    # 0.3 (2026-07-16): 0.2's deterministic normalization + synonym
                                          # maps, PLUS the grade axis reports n/a (None) when no closure
                                          # matched — an axis that passes by never being evaluated is the
                                          # instrument lying politely (Huayin). Old records stay interpretable.
BENCHMARK_LIST_VERSION = "1"             # B1–B11, ratified 2026-07-16


@dataclass(frozen=True)
class Benchmark:
    id: str
    kind: str                            # "◆" oracle-asymmetric | "○" mechanical
    schema: dict                         # {table: (columns, rows)} — the messy schema + sample
    ground_truth: dict                   # {closures, grades, oracle_calls, max_checklist}
    title: str = ""


@dataclass
class BenchmarkResult:
    benchmark_id: str
    kind: str
    closure: bool
    grade: Optional[bool]                # True | False | None (n/a — no graded closure matched; scorer 0.3)
    explicitness: bool
    checklist_concentration: bool
    convergence_cost: int                # iterations RUN
    loop_budget: int
    converged: bool                      # the censoring flag (amendment 3): passed within budget?
    passed: bool
    failure_narrative: str = ""
    retries: int = 0                     # malformed-output retries across this benchmark's iterations (convergence data)
    loop_violation: bool = False         # the mind re-proposed a struck declaration — the harness law fired (DATA)


@dataclass
class RunRecord:
    # provenance — first-class (contract §1, incl. the three amendments)
    model_id: str
    model_version: str
    sampling: dict                       # {temperature, seed, max_tokens}
    harness_config: dict                 # {aperture_cap, loop_iteration_budget}
    kp_version: str
    provider: str                        # "scripted" | "anthropic"
    benchmark_list_version: str = BENCHMARK_LIST_VERSION
    scorer_version: str = SCORER_VERSION
    results: list = field(default_factory=list)     # [BenchmarkResult]
    run_id: Optional[str] = None         # stamped AFTER the run (never inside the harness)
    run_timestamp: Optional[str] = None

    def summary(self) -> dict:
        oracle = [r for r in self.results if r.kind == "◆"]
        conv = [r.convergence_cost for r in self.results if r.converged]
        return {
            "passed": sum(r.passed for r in self.results),
            "total": len(self.results),
            "oracle_explicit": sum(r.explicitness for r in oracle),
            "oracle_total": len(oracle),
            "mean_convergence_converged_only": round(sum(conv) / len(conv), 1) if conv else None,
            "censored": sum(1 for r in self.results if not r.converged),   # capped-without-passing
            "loop_violations": sum(1 for r in self.results if r.loop_violation),
        }


def _canon(s: str) -> str:
    """Canonical identity form (scorer 0.2, deterministic): lowercase, collapse whitespace, normalize
    an edge/relate arrow ('a -> b', 'a to b', 'a<->b' -> 'a->b'). NO semantic judgment."""
    s = " ".join(str(s).strip().lower().split())
    s = s.replace(" -> ", "->").replace("<->", "->").replace(" to ", "->").replace("--", "-")
    return s


def _oracle_key(call: str) -> str:
    """The canonical TAG of an oracle-asymmetric call — the category before the ':' (basis, universe,
    m-leak, fertility, refutation, additivity). Explicitness is checked by this KEY appearing in the
    checklist, not by prose equality (deterministic keyword match, not a mind reading a mind)."""
    return call.split(":", 1)[0].strip().lower()


def score(benchmark: Benchmark, output: dict, loop_budget: int) -> BenchmarkResult:
    """Score one init OUTPUT vs the benchmark's adjudicated ground truth (scorer 0.2 — deterministic
    normalization + keyword ◆-matching). `output` = {proposals: [{kind, target, grade}], checklist:
    [surfaced calls], iterations, retries}. Hard-fail axes: closure, grade, explicitness (a silent ◆
    call fails even when the value is right)."""
    gt = benchmark.ground_truth
    proposals = output.get("proposals", [])
    checklist = list(output.get("checklist", []))
    syn = {(_canon(k.split(":", 1)[1]) if ":" in k else _canon(k)): {_canon(v) for v in vs}
           for k, vs in gt.get("synonyms", {}).items()}
    fails = []

    opened = [p for p in proposals if p.get("opens_fertility")]
    if opened:
        fails.append("proposed a fertility OPENING (polarity violation)")

    def _match(kind, tgt, want_kind, want_tgt):
        if kind != want_kind:
            return False
        ct, cw = _canon(tgt), _canon(want_tgt)
        return ct == cw or ct in syn.get(cw, set())

    want = [tuple(c) for c in gt["closures"]]
    proposed = [(p["kind"], p.get("target", "")) for p in proposals if not p.get("opens_fertility")]
    unmatched = [w for w in want if not any(_match(pk, pt, w[0], w[1]) for pk, pt in proposed)]
    closure_ok = not unmatched and not opened
    if unmatched:
        fails.append(f"missing/mismatched closures: {unmatched}")

    graded_matches, grade_ok = 0, True         # grade is n/a (None) when no GRADED closure matched (scorer 0.3)
    for p in proposals:
        for w in want:
            if _match(p["kind"], p.get("target", ""), w[0], w[1]):
                exp = gt["grades"].get(f"{w[0]}:{w[1]}")
                if exp:
                    graded_matches += 1
                    if p.get("grade") != exp:
                        grade_ok = False
    grade = grade_ok if graded_matches else None
    if grade is False:
        fails.append("a proposal carries the wrong INFERRED_* grade")

    blob = _canon(" ".join(checklist))
    missing_keys = [_oracle_key(c) for c in gt.get("oracle_calls", []) if _oracle_key(c) not in blob]
    explicit_ok = not missing_keys
    if missing_keys:
        fails.append(f"silent on oracle-asymmetric call(s): {sorted(set(missing_keys))}")

    max_cl = gt.get("max_checklist", 10 ** 9)
    concentration_ok = explicit_ok and len(checklist) <= max_cl
    if explicit_ok and not concentration_ok:
        fails.append(f"checklist flooded ({len(checklist)} items > max {max_cl})")

    iterations = int(output.get("iterations", 1))
    passed = closure_ok and (grade is not False) and explicit_ok      # n/a grade doesn't fail; closure gates
    converged = passed and iterations <= loop_budget
    return BenchmarkResult(
        benchmark_id=benchmark.id, kind=benchmark.kind, closure=closure_ok, grade=grade,
        explicitness=explicit_ok, checklist_concentration=concentration_ok,
        convergence_cost=iterations, loop_budget=loop_budget, converged=converged,
        passed=passed, failure_narrative="; ".join(fails), retries=int(output.get("retries", 0)))


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


class _ClaimAperture:
    """A DuckDBConnector whose catalog() ALSO surfaces declared-but-unENFORCED keys (`catalog_claims`).
    This is how B11 is encoded faithfully: a warehouse routinely DECLARES a key the engine does not
    enforce, so the sample can violate it — DuckDB won't let us insert a row violating an enforced FK,
    so the claim rides as catalog metadata over unconstrained data. Everything else delegates."""

    def __init__(self, con, claims: dict):
        self._c = con
        self._claims = claims or {}

    def catalog(self):
        cat = self._c.catalog()
        for t in cat:
            for claim in self._claims.get(t["table"], []):
                t["keys"].append({**claim, "enforced": False, "source": "catalog-declared"})
        return cat

    def __getattr__(self, name):
        return getattr(self._c, name)


def build_aperture(schema: dict):
    """A DuckDBConnector over a benchmark's schema — the two-ends data wall for the run. Schema shape:
        {"tables": {name: {"cols":[(n,type)], "pk":[...], "fk":[(col,reftable,refcol)], "rows":[...]}},
         "catalog_claims": {table: [{"type":"UNIQUE"|"FK", "columns":[...]}]}}      # optional, unenforced
    Real DECLARED keys (pk/fk) land in catalog() via DuckDB's constraints (so a catalog-graded edge has
    real catalog evidence); `catalog_claims` ride unenforced for the refutation case."""
    import duckdb
    from columna_core import DuckDBConnector
    con = duckdb.connect()
    tables = schema["tables"]
    for name, spec in tables.items():
        parts = [f'"{c}" {t}' for c, t in spec["cols"]]
        if spec.get("pk"):
            parts.append(f"PRIMARY KEY ({', '.join(spec['pk'])})")
        for col, rt, rc in spec.get("fk", []):
            parts.append(f"FOREIGN KEY ({col}) REFERENCES {rt}({rc})")
        con.execute(f'CREATE TABLE "{name}" ({", ".join(parts)})')
    for name, spec in tables.items():                    # parents first (dict order) — FK insert order
        for r in spec.get("rows", []):
            con.execute(f'INSERT INTO "{name}" VALUES ({", ".join(_lit(v) for v in r)})')
    dc = DuckDBConnector(con)
    claims = schema.get("catalog_claims")
    return _ClaimAperture(dc, claims) if claims else dc


def benchmark_coherence(benchmark) -> list:
    """The SELF-COHERENCE meta-check (Huayin, ruling 1): every ground-truth CLOSURE must be derivable
    from the schema's OWN evidence — catalog()/profile() must actually emit what the ground truth
    claims. Returns a list of incoherences (empty = coherent). This kills the real-001 failure class
    STRUCTURALLY (a benchmark whose truth its own aperture cannot support fails the test, not a run)."""
    ap = build_aperture(benchmark.schema)
    cat = {t["table"]: t for t in ap.catalog()}
    gt = benchmark.ground_truth
    has_fk = any(str(col.get("type", "")).upper().startswith("FOREIGN") for t in cat for col in cat[t]["keys"])
    _num = lambda ty: any(x in ty.upper() for x in ("INT", "DOUBLE", "DEC", "FLOAT"))
    numeric_cols = any(_num(c["type"]) for t in cat for c in cat[t]["columns"])
    cat_cols = any(not _num(c["type"]) and "DATE" not in c["type"].upper() for t in cat for c in cat[t]["columns"])
    temporal = any("DATE" in c["type"].upper() or "TIME" in c["type"].upper() for t in cat for c in cat[t]["columns"])
    bad = []

    def _fd_holds(frm, to):
        for t in cat:
            names = {c["name"] for c in cat[t]["columns"]}
            if frm in names and to in names:
                n = ap.con.execute(f'SELECT count(*) FROM (SELECT "{frm}" FROM "{t}" GROUP BY "{frm}" '
                                   f'HAVING count(distinct "{to}") > 1)').fetchone()[0]
                return n == 0
        return False

    for kind, target in gt["closures"]:
        if kind == "edge":
            grade = gt["grades"].get(f"edge:{target}")
            if grade == "inferred_catalog" and not has_fk:
                bad.append(f"edge '{target}' is catalog-graded but the schema declares no FK")
            elif grade == "inferred_sample":
                frm, to = target.split("->")
                if not _fd_holds(frm, to):
                    bad.append(f"edge '{target}' is sample-graded but the data shows no functional {frm}->{to}")
        elif kind == "hierarchy":
            if not temporal:
                bad.append(f"hierarchy '{target}' needs a temporal column to detect a calendar")
        elif kind == "measure":
            if not numeric_cols:
                bad.append(f"measure '{target}' has no numeric column to aggregate in the schema")
        elif kind == "level":
            if not cat_cols and not numeric_cols:
                bad.append(f"level '{target}' has no column in the schema to key it")
        elif kind == "derived":
            measure_targets = {t for k, t in gt["closures"] if k == "measure"}
            for need in gt.get("derived_needs", {}).get(target, []):
                if need not in measure_targets:
                    bad.append(f"derived '{target}' needs measure '{need}', absent from this benchmark's "
                               f"measure closures — its ground truth is unformable from the schema")
        elif kind == "relate":
            claims = benchmark.schema.get("catalog_claims", {})
            violated = False
            for tbl, cs in claims.items():
                for claim in cs:
                    col = claim["columns"][0]
                    nd, nt = ap.con.execute(f'SELECT count(distinct "{col}"), count(*) FROM "{tbl}"').fetchone()
                    violated = violated or nd < nt
            if not violated:
                bad.append(f"relate '{target}' claims a refutation but no catalog-declared key is violated by the data")
    return bad


def _review_from_ground_truth(loop, benchmark) -> None:
    """The eval plays the VERIFIER (the human's role in real use is the ground truth here): strike any
    proposal not in the ground-truth closures, so the next revise turn addresses it. This is
    search-with-verifier — the harness thesis's shape, with ratified ground truth as the oracle."""
    from columna_core.draft import ACCEPTED, STRUCK, PROPOSED
    gt = benchmark.ground_truth
    syn = {(_canon(k.split(":", 1)[1]) if ":" in k else _canon(k)): {_canon(v) for v in vs}
           for k, vs in gt.get("synonyms", {}).items()}
    want = [tuple(c) for c in gt["closures"]]

    def _matches(kind, tgt):
        for wk, wt in want:
            if kind == wk and (_canon(tgt) == _canon(wt) or _canon(tgt) in syn.get(_canon(wt), set())):
                return True
        return False

    for p in loop.draft.proposals:
        if p.review != PROPOSED:
            continue
        p.review = ACCEPTED if _matches(p.kind, p.target) else STRUCK    # normalized (scorer 0.2), not exact


def run_benchmark(benchmark: Benchmark, provider, loop_budget: int) -> BenchmarkResult:
    """Drive init over one benchmark to convergence (or the budget), scoring each round against the
    adjudicated ground truth. Convergence cost = iterations run; `converged` is censored at the budget."""
    from .loop import InitLoop, LoopViolation
    loop = InitLoop(build_aperture(benchmark.schema), provider, benchmark.id)
    r0 = getattr(provider, "retries", 0)                     # malformed-output retries are convergence data
    result = None
    for i in range(1, loop_budget + 1):
        try:
            if i == 1:
                loop.generate()
            else:
                _review_from_ground_truth(loop, benchmark)  # the verifier marks; then the mind revises
                loop.revise()
        except LoopViolation as e:
            # SCORE, never crash (Huayin, ruling 2): a protection firing is DATA. The revise raised
            # BEFORE absorbing, so loop.output() is the LAST VALID draft — read the other axes from it
            # (◆-explicitness especially: a re-proposing mind still surfaced or didn't its sharp calls).
            out = loop.output()
            out["retries"] = getattr(provider, "retries", 0) - r0
            result = score(benchmark, out, loop_budget)
            result.loop_violation = True
            result.converged = False                        # censor convergence
            result.passed = False
            if not result.failure_narrative:
                result.failure_narrative = str(e)
            else:
                result.failure_narrative += f"; loop_violation: {e}"
            return result
        out = loop.output()
        out["retries"] = getattr(provider, "retries", 0) - r0
        result = score(benchmark, out, loop_budget)
        if result.passed:
            break
    return result


def render_report(run: RunRecord) -> str:
    """The standing report shape (contract §3) — a readable checkpoint document, not a CI artifact."""
    s = run.summary()
    L = [
        f"EVAL RUN {run.run_id or '<unstamped>'}  ·  {run.run_timestamp or '<unstamped>'}",
        f"provider={run.provider}  model={run.model_id}@{run.model_version}  "
        f"sampling={run.sampling}  harness={run.harness_config}",
        f"kp=v{run.kp_version}  benchmark_list=v{run.benchmark_list_version}  scorer=v{run.scorer_version}",
        "",
        f"SUMMARY   passed {s['passed']}/{s['total']}   "
        f"◆-explicitness {s['oracle_explicit']}/{s['oracle_total']}   "
        f"mean convergence (converged-only) {s['mean_convergence_converged_only']}   "
        f"censored {s['censored']}   loop-violations {s['loop_violations']}",
        "─" * 74,
    ]
    for r in run.results:
        tag = "PASS" if r.passed else "FAIL"
        gmark = "n/a" if r.grade is None else ("✓" if r.grade else "✗")
        axes = (f"closure{'✓' if r.closure else '✗'} grade{gmark} "
                f"explicit{'✓' if r.explicitness else '✗'} concise{'✓' if r.checklist_concentration else '✗'}")
        conv = f"conv {r.convergence_cost}{'' if r.converged else ' (CAPPED)'}"
        rt = f"  retries {r.retries}" if r.retries else ""
        lv = "  LOOP-VIOLATION" if r.loop_violation else ""
        L.append(f"{r.benchmark_id} {r.kind}   {tag}   {axes}   {conv}{rt}{lv}")
        if not r.passed:
            L.append(f"       └ narrative: {r.failure_narrative}")
    L += ["─" * 74,
          "CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.",
          "◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record."]
    return "\n".join(L)
