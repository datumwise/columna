"""
columna_server.init.runner — the replicated A/B eval runner (CP-2.x, Huayin ruling 4, 2026-07-16).

A measured KP iteration is an A/B: a CONTROL arm (the prior live KP) vs a TREATMENT arm (the candidate),
same model + scorer + benchmarks, one keyed session, only the prompt varying. Run 5 was n=1 per arm and
its control was not perfectly still; ruling 4 mandates REPLICATION (n≥2 per arm) so the noise is
quantified, not guessed, and folds the standing debts into the same session (B10 proposal-vs-truth
capture; loop-violations counted across replicates).

RETENTION IS STRUCTURE (ruling 3): this runner writes its artifacts — captured proposals, B10 evidence,
the report — into a DURABLE in-repo directory FROM BIRTH, sets them on each RunRecord, and lets
`render_report`'s retention gate refuse to render until they are on disk. An infra/API error ABORTS the
run loudly (never a fake miss). The runner itself is hermetic with a scripted provider factory.
"""
from __future__ import annotations

import json
import os

from .eval import run_benchmark, render_report, RunRecord, BenchmarkResult, SCORER_VERSION
from .benchmarks import BENCHMARKS


class InfraAbort(RuntimeError):
    """A benchmark run blew up on infrastructure (API overload / network) — NOT a mind miss. The run
    aborts rather than recording a fake 0 that would poison the measurement (run-5's overload lesson)."""


def _is_infra(e: BaseException) -> bool:
    """Classify an exception as INFRASTRUCTURE (an API/transport failure — abort the run) vs a
    CONTRACT/harness failure (score it as a benchmark outcome). An empty completion is already handled at
    the parse layer (→ no proposals); a persistent malformed reply is the MIND failing the contract, not
    infra. Anthropic SDK errors (overload/rate/connection/timeout) live in the `anthropic` module tree."""
    mod = type(e).__module__ or ""
    return mod.split(".", 1)[0] == "anthropic" or isinstance(e, (ConnectionError, TimeoutError))


def _rate(vals) -> float:
    vals = list(vals)
    return round(sum(1 for v in vals if v) / len(vals), 3) if vals else 0.0


def run_replicated_ab(*, arms, bids, k, loop_budget, out_dir, provider_for, model_id, stamp):
    """Run a replicated A/B and write durable artifacts.
      arms:  [{"name": str, "kp_version": str}]  — CONTROL first, TREATMENT second (by convention).
      bids:  benchmark ids to run (e.g. sorted(BENCHMARKS)).
      k:     replicates per (arm, benchmark), k≥2 for a measured run.
      provider_for(arm, bid, rep) -> a fresh provider (raise to force an InfraAbort).
      out_dir: a DURABLE in-repo directory (NOT /tmp) — created if absent.
      model_id: provenance label; stamp: {"run_id","run_timestamp"} (stamped by the caller, never here).
    Returns the aggregate dict; writes out_dir/{captured.json,b10.json,report.md}.
    """
    # a REAL measurement must land durably in-repo (ruling 3); a scripted plumbing run may write anywhere.
    if model_id != "scripted" and any(str(out_dir).startswith(t)
                                      for t in ("/tmp", "/var/tmp", "/dev/shm", "/run/")):
        raise ValueError(f"out_dir {out_dir!r} is a temp dir — a real run writes durable evidence only "
                         f"(ruling 3). Point it into the repo tree (specs/).")
    os.makedirs(out_dir, exist_ok=True)
    cap_path = os.path.join(out_dir, "captured.json")
    b10_path = os.path.join(out_dir, "b10.json")
    rep_path = os.path.join(out_dir, "report.md")
    artifacts = {"captured": cap_path, "b10": b10_path, "report": rep_path}

    # 1) run every (arm, benchmark, replicate); abort loud on infra failure
    per_arm = {}                                  # name -> {bid -> [BenchmarkResult]*k}
    captured = {}                                 # name -> [ {bid, rep, ...axes..., proposals, checklist} ]
    for arm in arms:
        per_arm[arm["name"]], captured[arm["name"]] = {}, []
        for bid in bids:
            reps = []
            for rep in range(k):
                try:
                    prov = provider_for(arm, bid, rep)
                    r = run_benchmark(BENCHMARKS[bid], prov, loop_budget)
                except Exception as e:
                    if _is_infra(e):                        # a real API error (overload/rate/connection)
                        raise InfraAbort(f"[{arm['name']}] {bid} rep{rep}: {type(e).__name__}: {e} — "
                                         f"infrastructure, not a mind miss; no report written (ruling 3).") from e
                    # a CONTRACT/harness error that survived the provider's retry is a benchmark outcome,
                    # not infra: SCORE it (protection firing is DATA — never abort a 44-run session on one).
                    r = BenchmarkResult(benchmark_id=bid, kind=BENCHMARKS[bid].kind, closure=False,
                                        grade=None, explicitness=False, checklist_concentration=False,
                                        convergence_cost=loop_budget, loop_budget=loop_budget,
                                        converged=False, passed=False,
                                        failure_narrative=f"CONTRACT/HARNESS: {type(e).__name__}: {e}")
                reps.append(r)
                import sys as _sys                          # per-(arm,bid,rep) progress — closes run-6's
                print(f"  [{arm['name']}] {bid} rep{rep}: "                 # visibility gap (no stream then)
                      f"{'PASS' if r.passed else 'fail'} closure={r.closure} "
                      f"explicit={r.explicitness} flood={not r.checklist_concentration} "
                      f"lv={r.loop_violation}", file=_sys.stderr, flush=True)
                captured[arm["name"]].append({
                    "bid": bid, "rep": rep, "passed": r.passed, "closure": r.closure, "grade": r.grade,
                    "explicit": r.explicitness, "concise": r.checklist_concentration,
                    "conv": r.convergence_cost, "converged": r.converged, "loop_violation": r.loop_violation,
                    "retries": r.retries, "narrative": r.failure_narrative,
                    "proposals": r.scored_proposals, "checklist": r.scored_checklist})
            per_arm[arm["name"]][bid] = reps

    # 2) write the RAW evidence FIRST (durable) — the report is written last, so it summarizes survivors
    with open(cap_path, "w") as f:
        json.dump(captured, f, indent=2, ensure_ascii=False)
    b10 = {"benchmark": "B10", "ground_truth": BENCHMARKS["B10"].ground_truth, "arms": {}}
    for arm in arms:
        b10["arms"][arm["name"]] = [c for c in captured[arm["name"]] if c["bid"] == "B10"]
    with open(b10_path, "w") as f:
        json.dump(b10, f, indent=2, ensure_ascii=False)

    # 3) aggregate per-arm rates + build a gated RunRecord per arm (retention gate fires here)
    agg, records = {}, {}
    for arm in arms:
        name = arm["name"]
        flat = [r for bid in bids for r in per_arm[name][bid]]
        rec = RunRecord(model_id=model_id, model_version=model_id,
                        sampling={"max_tokens": 2048, "temperature": "provider-default"},
                        harness_config={"aperture_cap": 1000, "loop_iteration_budget": loop_budget, "replicates_k": k},
                        kp_version=arm["kp_version"], provider=("scripted" if model_id == "scripted" else "anthropic"),
                        results=flat, run_id=f"{stamp.get('run_id','run')}-{name}",
                        run_timestamp=stamp.get("run_timestamp"), artifacts=artifacts)
        records[name] = rec
        rows = {}
        for bid in bids:
            rs = per_arm[name][bid]
            is_oracle = BENCHMARKS[bid].kind == "◆"
            rows[bid] = {
                "kind": BENCHMARKS[bid].kind,
                "pass_rate": _rate(r.passed for r in rs),
                "closure_rate": _rate(r.closure for r in rs),
                "explicit_rate": (_rate(r.explicitness for r in rs) if is_oracle else None),
                "flood_rate": _rate((not r.checklist_concentration) for r in rs),
                "loop_viol_rate": _rate(r.loop_violation for r in rs),
            }
        agg[name] = {
            "rows": rows,
            "passed_mean": round(sum(r.passed for r in flat) / k, 2),
            "oracle_explicit_mean": round(sum(r.explicitness for r in flat if r.kind == "◆") / k, 2),
            "flood_count_mean": round(sum(1 for r in flat if not r.checklist_concentration) / k, 2),
            "loop_viol_total": sum(1 for r in flat if r.loop_violation),
        }

    # 4) render (gate enforced) + the A/B rates table -> durable report.md
    report = _render_ab(arms, records, agg, bids, k)
    with open(rep_path, "w") as f:
        f.write(report + "\n")
    return {"aggregate": agg, "artifacts": artifacts, "report": report}


def _render_ab(arms, records, agg, bids, k) -> str:
    L = []
    for arm in arms:
        L += [f"########## ARM {arm['name']} — KP v{arm['kp_version']} (k={k}) ##########",
              render_report(records[arm["name"]]), ""]           # render_report enforces the retention gate
    c, t = arms[0]["name"], arms[1]["name"]
    L += ["=" * 84, f"A/B RATES — CONTROL {c} vs TREATMENT {t}  (k={k}, scorer v{SCORER_VERSION})", "=" * 84,
          f"{'bench':6} {'kind':4} {'pass':13} {'explicit(◆)':15} {'flood':13} {'loopviol':13}"]
    ca, ta = agg[c]["rows"], agg[t]["rows"]

    def cell(a, b):
        fa = "-" if a is None else f"{a:.2f}"
        fb = "-" if b is None else f"{b:.2f}"
        return f"{fa}→{fb}" + ("  △" if a != b else "")
    for bid in bids:
        L.append(f"{bid:6} {ca[bid]['kind']:4} "
                 f"{cell(ca[bid]['pass_rate'], ta[bid]['pass_rate']):13} "
                 f"{cell(ca[bid]['explicit_rate'], ta[bid]['explicit_rate']):15} "
                 f"{cell(ca[bid]['flood_rate'], ta[bid]['flood_rate']):13} "
                 f"{cell(ca[bid]['loop_viol_rate'], ta[bid]['loop_viol_rate']):13}")
    L += ["-" * 84,
          f"CONTROL {c}:   passed(mean) {agg[c]['passed_mean']}  ◆-explicit(mean) {agg[c]['oracle_explicit_mean']}  "
          f"flood(mean) {agg[c]['flood_count_mean']}  loop-viol(total) {agg[c]['loop_viol_total']}",
          f"TREATMENT {t}: passed(mean) {agg[t]['passed_mean']}  ◆-explicit(mean) {agg[t]['oracle_explicit_mean']}  "
          f"flood(mean) {agg[t]['flood_count_mean']}  loop-viol(total) {agg[t]['loop_viol_total']}",
          "",
          "READING (ruling 4): refutation (B11) is the most at-risk ◆ under the strict prune — if its "
          "explicit_rate falls, the gate is too aggressive (prediction-2 do-not-ship). Concentration bought "
          "with recall is not a win."]
    return "\n".join(L)
