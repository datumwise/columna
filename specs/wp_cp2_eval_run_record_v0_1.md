# CP-2 — the eval run-record + report contract (v0.1)
**From: Claude Code, 2026-07-16. The measurement contract, defined BEFORE the first data point exists
(rider 1, 2026-07-16). PROPOSED for confirmation; the report shape (§3) becomes the STANDING format
(rider 2). No real-model run happens without Huayin's explicit go (rider 3).**

## 1 · Provenance — first-class fields on every run record (rider 1)
The ratchet's convergence and quality numbers are meaningless unless compared like-with-like. Every run
record carries, as first-class fields (not a footnote):
- `model_id` + `model_version` — the exact rented mind (e.g. `claude-opus-4-8` + the dated version).
- `kp_version` — the knowledge-package version (versioned doctrine; a prompt ruling's effect on scores
  must be measurable across versions).
- `benchmark_list_version` — the ratified benchmark set (B1–B11 = v1).
- `provider` — `scripted` (hermetic) or `anthropic` (real mind); scripted runs are labeled so they
  never contaminate the real-mind trend line.
- `run_id`, `run_timestamp` — stamped after the run (never inside the harness, per the determinism rule).

## 2 · Per-benchmark result — the scored axes (ratified)
For each benchmark (B1–B11), the record holds:
- `benchmark_id`, `kind` (◆ oracle-asymmetric | ○ mechanical).
- `closure` — did it bar/assign/leak/refute right? (per-declaration diff vs adjudicated ground truth).
- `grade` — INFERRED_CATALOG vs INFERRED_SAMPLE (and, for B11, catalog-refuted) correctness.
- `explicitness` — for ◆ benchmarks: was the oracle-asymmetric call SURFACED in the review checklist?
  **Silent = HARD FAIL** even when the value is right.
- `checklist_concentration` — was the checklist kept short and differentiated (◆ calls surfaced AND the
  review not flooded)? Scored, not just ◆ recall.
- `convergence_cost` — loop iterations to a passing draft (RECORDED metric, not pass/fail; the harness
  thesis's open empirical question, measured from the first real-provider run — rider from 2026-07-16).
- `passed` — the boolean roll-up (any hard fail ⇒ not passed).
- `failure_narrative` — when not passed, a short human-readable account of WHAT the draft got wrong
  (the diagnostic the report leads with).

## 3 · The report — a readable checkpoint deliverable, not a CI artifact (rider 2)
The first real-provider report comes to Huayin as a readable document; this shape is the standing format:
```
EVAL RUN <run_id>  ·  <run_timestamp>
provider=<anthropic|scripted>  model=<model_id>@<model_version>
kp=<kp_version>  benchmarks=<benchmark_list_version>

SUMMARY   passed N/11   ◆-explicitness M/<#◆>   mean convergence <k> iters
─────────────────────────────────────────────────────────────────────────
B1 events-vs-spine ◆   PASS   closure✓ grade✓ explicit✓ concise✓   conv 2
B8 polarity trap   ◆   FAIL   explicit✗ — proposed the opening as inferred
       └ narrative: <what went wrong, in one or two sentences>
...
─────────────────────────────────────────────────────────────────────────
CONVERGENCE COST (the empirical question)   per-benchmark iters + the mean trend
◆-CALL RECORD                               each ◆ call: surfaced / silent
```
CI runs the HERMETIC suite (harness behavior — pass/fail, no judgment scoring). The eval suite runs on
demand and produces THIS report; the first real-provider run is a checkpoint to Huayin.

## 4 · What I build next (hermetic; real mind waits for the go)
- The `AnthropicProvider` for init behind the same loop; **scripted stays the default** everywhere.
- The eval harness: benchmark loader (schemas + adjudicated ground truth), the scorer over §2's axes,
  the run record (§1–2), the report renderer (§3) — all runnable and TESTED with a scripted stand-in
  (validating the scorer, not a mind).
- Init's actual inference (generate reading the aperture → proposals per the KP).
- **The first real-model run against B1–B11 waits for Huayin's explicit word** — one message, and the
  first mind walks the corridor the rulings built.

Confirm the run-record fields (§1–2) and the report shape (§3), or revise; then the harness is built to
this contract.
