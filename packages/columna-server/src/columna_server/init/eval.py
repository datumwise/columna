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

import os
from dataclasses import dataclass, field
from typing import Optional


class RetentionError(RuntimeError):
    """A real-mind run is NOT complete until its artifacts live at a durable, in-repo location (Huayin
    ruling 3, 2026-07-16: two losses to /tmp is two; there is no third). The report refuses to render
    a real run whose captured evidence is missing or parked under a temp dir."""


_TEMP_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm", "/run/")


def _assert_durable(run) -> None:
    """The retention gate (ruling 3): a real-mind run must declare its artifact paths, they must NOT be
    under a temp dir, and the RAW captured evidence must already be written (the report is written last,
    so it summarizes evidence that already survived). Scripted/hermetic runs are instrument tests, not
    measurements to retain, so they render freely."""
    if run.provider != "anthropic":
        return
    if not run.artifacts:
        raise RetentionError("real-mind run carries no artifact paths — declare durable in-repo "
                             "locations for the captured evidence + report BEFORE rendering (ruling 3).")
    for name, path in run.artifacts.items():
        p = str(path)
        if any(p.startswith(t) for t in _TEMP_PREFIXES):
            raise RetentionError(f"artifact '{name}' at {p!r} is under a temp dir — write run evidence "
                                 f"into the repo tree (specs/); /tmp is not durable (ruling 3).")
    for name in ("captured", "b10"):                      # the raw evidence the report summarizes
        path = run.artifacts.get(name)
        if path and not os.path.exists(path):
            raise RetentionError(f"artifact '{name}' declared at {path!r} but not on disk — write the "
                                 f"captured evidence to its durable location before the report (ruling 3).")

SCORER_VERSION = "0.4"                    # 0.4 (2026-07-16, Huayin ruling 2): closure comparison at the
                                          # DESUGARED NORMAL FORM — HIERARCHY desugars to edges by the
                                          # shipped grammar law, so both ground truth and proposal lower
                                          # to the edge/level normal form before matching. A hierarchy and
                                          # its equivalent edges compare EQUAL (B6/B7 was never a miss);
                                          # levels-without-travel stays a genuine miss. Grammar-defined, no
                                          # judgment. Inherits 0.3's n/a-grade + 0.2's normalization/synonyms.
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
    scored_proposals: list = field(default_factory=list)   # the RAW proposals scored (provenance; enables a
    scored_checklist: list = field(default_factory=list)   # deterministic re-render under a NEW scorer with
                                                           # NO re-run — the gap run-4 exposed, closed here.


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
    artifacts: dict = field(default_factory=dict)   # durable in-repo paths of this run's evidence
                                                    # {captured, b10, report} — ruling 3: a real run is
                                                    # not complete until these are written + committed.

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


def _desugar(kind: str, target) -> list:
    """Lower a closure to its edge/level NORMAL FORM (scorer 0.4, Huayin ruling 2, 2026-07-16). The
    grammar's SHIPPED law: `HIERARCHY a->b->c` desugars to the edges a->b, b->c. So a hierarchy and its
    equivalent edges compare EQUAL, while levels-without-travel (no edge declared) does NOT reduce to an
    edge and stays a genuine miss. Returns canonicalized (kind, target) atoms. Deterministic; the scorer
    borrows an equivalence the grammar already defines, not one it invents."""
    t = _canon(target)
    if kind == "hierarchy":
        nodes = [p for p in t.split("->") if p]
        if len(nodes) >= 2:
            return [("edge", f"{a}->{b}") for a, b in zip(nodes, nodes[1:])]
        return [("level", nodes[0])] if nodes else []
    return [(kind, t)]


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

    def _atom_match(pk, pt, wk, wt):           # atoms are already canonical (from _desugar)
        return pk == wk and (pt == wt or pt in syn.get(wt, set()))

    # scorer 0.4 (ruling 2): desugar BOTH sides to the edge/level normal form before matching.
    want_atoms = []                            # [(kind, target, grade_or_None)] — grade rides each atom
    for c in gt["closures"]:
        g = gt["grades"].get(f"{c[0]}:{c[1]}")
        for ak, at in _desugar(c[0], c[1]):
            want_atoms.append((ak, at, g))
    proposed_atoms = []                        # [(kind, target, grade)]
    for p in proposals:
        if p.get("opens_fertility"):
            continue
        for ak, at in _desugar(p["kind"], p.get("target", "")):
            proposed_atoms.append((ak, at, p.get("grade")))

    unmatched = [(wk, wt) for (wk, wt, _wg) in want_atoms
                 if not any(_atom_match(pk, pt, wk, wt) for pk, pt, _pg in proposed_atoms)]
    closure_ok = not unmatched and not opened
    if unmatched:
        fails.append(f"missing/mismatched closures (normal form): {unmatched}")

    graded_matches, grade_ok = 0, True         # grade is n/a (None) when no GRADED closure matched (scorer 0.3)
    for (wk, wt, wg) in want_atoms:
        if not wg:
            continue
        for pk, pt, pg in proposed_atoms:
            if _atom_match(pk, pt, wk, wt):
                graded_matches += 1
                if pg != wg:
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
        passed=passed, failure_narrative="; ".join(fails), retries=int(output.get("retries", 0)),
        scored_proposals=list(proposals), scored_checklist=list(checklist))


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
    # advice channel (ruling 2): a declared adjudicator-advice must be structurally supported world-side.
    for a in benchmark.ground_truth.get("advice", []):
        if not _advice_supported(gt, a):
            bad.append(f"advice {a} declared but not structurally supported — the eval cannot assert the "
                       f"adjudicator's advice would fire from this benchmark's own closures")
    return bad


def _advice_supported(gt: dict, advice: dict) -> bool:
    """Is an adjudicator-advice entry structurally supported by the benchmark's OWN closures? (ruling 2,
    deterministic — no mind involved). Fertility fires for a member that is a formable DERIVED RATIO of
    additive MEASURES: aov = revenue/orders is theorem-provably fertile (recomputes along lineages), so
    the adjudicator advises it. We check the member is a derived closure whose derived_needs are all
    measure closures — the grammar-grounded proxy for 'the advice fires'."""
    member = advice.get("member")
    if advice.get("channel") != "fertility":
        return False                                          # only the fertility advice channel is defined here
    is_derived = any(k == "derived" and t == member for k, t in gt.get("closures", []))
    measures = {t for k, t in gt.get("closures", []) if k == "measure"}
    needs = gt.get("derived_needs", {}).get(member, [])
    return is_derived and bool(needs) and all(n in measures for n in needs)


def benchmark_advice_fires(benchmark) -> bool:
    """Deterministic world-side check (ruling 2): every advice entry a benchmark declares would actually
    FIRE from the adjudicator (structurally grounded in the benchmark's own closures). True = the advice
    channel is coherent for this benchmark. This is what replaces the mis-specified agent-fertility ◆:
    fertility is the adjudicator's advice, and the eval checks IT, not the mind's silence."""
    advice = benchmark.ground_truth.get("advice", [])
    return bool(advice) and all(_advice_supported(benchmark.ground_truth, a) for a in advice)


def _review_from_ground_truth(loop, benchmark) -> None:
    """The eval plays the VERIFIER (the human's role in real use is the ground truth here): strike any
    proposal not in the ground-truth closures, so the next revise turn addresses it. This is
    search-with-verifier — the harness thesis's shape, with ratified ground truth as the oracle."""
    from columna_core.draft import ACCEPTED, STRUCK, PROPOSED
    gt = benchmark.ground_truth
    syn = {(_canon(k.split(":", 1)[1]) if ":" in k else _canon(k)): {_canon(v) for v in vs}
           for k, vs in gt.get("synonyms", {}).items()}
    want_atoms = [atom for c in gt["closures"] for atom in _desugar(c[0], c[1])]   # normal form (scorer 0.4)

    def _atom_in_want(pk, pt):
        return any(pk == wk and (pt == wt or pt in syn.get(wt, set())) for wk, wt in want_atoms)

    def _matches(kind, tgt):
        # a proposal is correct iff ALL its desugared atoms are in the ground truth's normal form — so a
        # hierarchy and its equivalent edges each ACCEPT, but levels-without-travel does not (ruling 2).
        atoms = _desugar(kind, tgt)
        return bool(atoms) and all(_atom_in_want(pk, pt) for pk, pt in atoms)

    for p in loop.draft.proposals:
        if p.review != PROPOSED:
            continue
        p.review = ACCEPTED if _matches(p.kind, p.target) else STRUCK    # normal-form match (scorer 0.4)


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


def rescore_run(run: RunRecord, benchmarks: dict) -> RunRecord:
    """Re-render a prior run under the CURRENT scorer from its CAPTURED outputs — no re-run, no key
    (Huayin, ruling 5, 2026-07-16: keep run-N vs run-N+1 like-with-like when the scorer version moves).
    Requires each result to carry `scored_proposals`/`scored_checklist` (added this cycle). A result with
    no captured output (e.g. a loop-violation censored before a score, or a pre-capture record like run-4)
    is passed through UNCHANGED and flagged, so the re-render never silently fabricates a closure verdict."""
    fresh = []
    for r in run.results:
        b = benchmarks.get(r.benchmark_id)
        if b is None or (not r.scored_proposals and not r.scored_checklist):
            fresh.append(r)                                  # cannot re-render — pass through (honest gap)
            continue
        out = {"proposals": r.scored_proposals, "checklist": r.scored_checklist,
               "iterations": r.convergence_cost, "retries": r.retries}
        nr = score(b, out, r.loop_budget)
        nr.loop_violation = r.loop_violation                # loop-violation is a harness event, not a score
        if r.loop_violation:
            nr.converged = False
            nr.passed = False
        fresh.append(nr)
    return RunRecord(
        model_id=run.model_id, model_version=run.model_version, sampling=run.sampling,
        harness_config=run.harness_config, kp_version=run.kp_version, provider=run.provider,
        benchmark_list_version=run.benchmark_list_version, scorer_version=SCORER_VERSION,
        results=fresh, run_id=(run.run_id or "") + f"~rescored@{SCORER_VERSION}",
        run_timestamp=run.run_timestamp)


def render_report(run: RunRecord) -> str:
    """The standing report shape (contract §3) — a readable checkpoint document, not a CI artifact.
    RETENTION GATE (ruling 3): a real-mind run refuses to render unless its captured evidence is already
    durably in the repo tree — no report can be produced from data that lives only in /tmp."""
    _assert_durable(run)
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
