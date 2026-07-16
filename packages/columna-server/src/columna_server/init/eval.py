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

SCORER_VERSION = "0.1"                    # the measurement instrument has versions too (contract §1)
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
    grade: bool
    explicitness: bool
    checklist_concentration: bool
    convergence_cost: int                # iterations RUN
    loop_budget: int
    converged: bool                      # the censoring flag (amendment 3): passed within budget?
    passed: bool
    failure_narrative: str = ""


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
        }


def score(benchmark: Benchmark, output: dict, loop_budget: int) -> BenchmarkResult:
    """Score one init OUTPUT vs the benchmark's adjudicated ground truth.

    `output` = {proposals: [{kind, target, grade, opens_fertility}], checklist: [surfaced ◆ calls],
                iterations: int}. Hard-fail axes: closure, grade, explicitness (a silent ◆ call fails
                even when the value is right)."""
    gt = benchmark.ground_truth
    proposals = output.get("proposals", [])
    checklist = set(output.get("checklist", []))
    fails = []

    opened = [p for p in proposals if p.get("opens_fertility")]
    if opened:
        fails.append("proposed a fertility OPENING (polarity violation)")
    proposed = {(p["kind"], p["target"]) for p in proposals if not p.get("opens_fertility")}
    closure_ok = (proposed == set(map(tuple, gt["closures"]))) and not opened
    if proposed != set(map(tuple, gt["closures"])):
        fails.append("closures do not match ground truth")

    grade_ok = all(p.get("grade") == gt["grades"].get(f"{p['kind']}:{p['target']}")
                   for p in proposals if f"{p['kind']}:{p['target']}" in gt["grades"])
    if not grade_ok:
        fails.append("a proposal carries the wrong INFERRED_* grade")

    oracle_calls = set(gt.get("oracle_calls", []))
    explicit_ok = oracle_calls <= checklist
    if not explicit_ok:
        fails.append(f"silent on oracle-asymmetric call(s): {sorted(oracle_calls - checklist)}")

    max_cl = gt.get("max_checklist", 10 ** 9)
    concentration_ok = explicit_ok and len(checklist) <= max_cl
    if explicit_ok and not concentration_ok:
        fails.append(f"checklist flooded ({len(checklist)} items > max {max_cl})")

    iterations = int(output.get("iterations", 1))
    passed = closure_ok and grade_ok and explicit_ok      # the hard-fail axes
    converged = passed and iterations <= loop_budget
    return BenchmarkResult(
        benchmark_id=benchmark.id, kind=benchmark.kind, closure=closure_ok, grade=grade_ok,
        explicitness=explicit_ok, checklist_concentration=concentration_ok,
        convergence_cost=iterations, loop_budget=loop_budget, converged=converged,
        passed=passed, failure_narrative="; ".join(fails))


def _lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else repr(v)


def build_aperture(schema: dict):
    """A DuckDBConnector over a benchmark's messy schema — the two-ends data wall for the run."""
    import duckdb
    from columna_core import DuckDBConnector
    con = duckdb.connect()
    for name, (cols, rows) in schema.items():
        values = ", ".join("(" + ", ".join(_lit(v) for v in r) + ")" for r in rows)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM (VALUES {values}) AS t({', '.join(cols)})")
    return DuckDBConnector(con)


def _review_from_ground_truth(loop, benchmark) -> None:
    """The eval plays the VERIFIER (the human's role in real use is the ground truth here): strike any
    proposal not in the ground-truth closures, so the next revise turn addresses it. This is
    search-with-verifier — the harness thesis's shape, with ratified ground truth as the oracle."""
    from columna_core.draft import ACCEPTED, STRUCK, PROPOSED
    wanted = set(map(tuple, benchmark.ground_truth["closures"]))
    for p in loop.draft.proposals:
        if p.review != PROPOSED:
            continue
        p.review = ACCEPTED if (p.kind, p.target) in wanted else STRUCK


def run_benchmark(benchmark: Benchmark, provider, loop_budget: int) -> BenchmarkResult:
    """Drive init over one benchmark to convergence (or the budget), scoring each round against the
    adjudicated ground truth. Convergence cost = iterations run; `converged` is censored at the budget."""
    from .loop import InitLoop
    loop = InitLoop(build_aperture(benchmark.schema), provider, benchmark.id)
    result = None
    for i in range(1, loop_budget + 1):
        if i == 1:
            loop.generate()
        else:
            _review_from_ground_truth(loop, benchmark)      # the verifier marks; then the mind revises
            loop.revise()
        result = score(benchmark, loop.output(), loop_budget)
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
        f"kp={run.kp_version}  benchmarks={run.benchmark_list_version}  scorer={run.scorer_version}",
        "",
        f"SUMMARY   passed {s['passed']}/{s['total']}   "
        f"◆-explicitness {s['oracle_explicit']}/{s['oracle_total']}   "
        f"mean convergence (converged-only) {s['mean_convergence_converged_only']}   "
        f"censored {s['censored']}",
        "─" * 74,
    ]
    for r in run.results:
        tag = "PASS" if r.passed else "FAIL"
        axes = (f"closure{'✓' if r.closure else '✗'} grade{'✓' if r.grade else '✗'} "
                f"explicit{'✓' if r.explicitness else '✗'} concise{'✓' if r.checklist_concentration else '✗'}")
        conv = f"conv {r.convergence_cost}{'' if r.converged else ' (CAPPED)'}"
        L.append(f"{r.benchmark_id} {r.kind}   {tag}   {axes}   {conv}")
        if not r.passed:
            L.append(f"       └ narrative: {r.failure_narrative}")
    L += ["─" * 74,
          "CONVERGENCE COST   per-benchmark iters above; converged-only mean + censoring in SUMMARY.",
          "◆-CALL RECORD      each ◆ benchmark's `explicit` flag above is its surfaced/silent record."]
    return "\n".join(L)
