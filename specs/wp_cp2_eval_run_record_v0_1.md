# CP-2 — the eval run-record + report contract (v0.1, STANDING)
**From: Claude Code, 2026-07-16. The measurement contract, defined BEFORE the first data point exists
(rider 1). CONFIRMED by Huayin 2026-07-16 with three provenance amendments (sampling + harness_config;
scorer_version; the convergence censoring flag) — folded in. §1–3 are now the STANDING contract; the
report shape (§3) is the standing format. No real-model run happens without Huayin's explicit go (rider 3).**

## 1 · Provenance — first-class fields on every run record (rider 1 + amendments)
The ratchet's convergence and quality numbers are meaningless unless compared like-with-like. Every run
record carries, as first-class fields (not a footnote):
- `model_id` + `model_version` — the exact rented mind (e.g. `claude-opus-4-8` + the dated version).
- `sampling` — temperature, seed (where applicable), token limits. **Two runs on the same model+KP at
  different temperatures are NOT like-with-like** (amendment 1).
- `harness_config` — the **aperture cap** (`APERTURE_SAMPLE_CAP`) and the **loop-iteration budget**. The
  cap silently rescales benchmark difficulty if it ever moves, so it is provenance (amendment 1).
- `kp_version` — the knowledge-package version (versioned doctrine; a prompt ruling's effect on scores
  must be measurable across versions).
- `benchmark_list_version` — the ratified benchmark set (B1–B11 = v1).
- `scorer_version` — the measurement INSTRUMENT has versions too; the ratchet must tell instrument
  drift from subject change (amendment 2).
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
- `convergence_cost` — loop iterations run (RECORDED metric, not pass/fail; the harness thesis's open
  empirical question, measured from the first real-provider run). **Censoring flag (amendment 3):**
  record `loop_budget` and a `converged` boolean per benchmark — "cost 6, converged" and "cost 6, capped
  without passing" are different facts; a mean over censored values misleads exactly at the boundary the
  metric exists to watch. Aggregates report converged-only means AND the censoring rate.
- `passed` — the boolean roll-up (any hard fail ⇒ not passed).
- `failure_narrative` — when not passed, a short human-readable account of WHAT the draft got wrong
  (the diagnostic the report leads with).

## 2a · Amendments 4–5 (Huayin rulings, 2026-07-16, post-baseline)
- **Scorer 0.4 — closure at the DESUGARED NORMAL FORM (ruling 2).** The closure axis lowers BOTH ground
  truth and proposal to the edge/level normal form before matching: `HIERARCHY a->b->c` desugars to the
  edges a->b, b->c by the SHIPPED grammar law, so a hierarchy and its equivalent edges compare EQUAL
  (B6/B7's cross-kind "miss" was an instrument artifact), while levels-without-travel stays a genuine
  miss. Grammar-defined, deterministic, no judgment. The grade rides each desugared atom.
- **Captured output — every result carries its scored proposals + checklist (re-render enablement).** A
  `BenchmarkResult` now stores `scored_proposals`/`scored_checklist`, so a scorer bump re-renders a prior
  run LIKE-WITH-LIKE via `rescore_run(run, benchmarks)` with **no re-run and no key**. A pre-capture
  record (run-4's shape) or a censored loop-violation passes through UNCHANGED and flagged — the
  re-render never fabricates a closure verdict it cannot derive. **Run-4 gap on record:** its report
  stored only the scored axes, so run-4 cannot be re-rendered under 0.4 from stored data; a clean run-4
  baseline under scorer 0.4 requires a re-run (KP v0.2 held), foldable into the run-5 keyed session so
  run-5-vs-baseline stays like-with-like.

## 2b · Amendments 6–7 (Huayin rulings 2–3, 2026-07-16, post-run-5)
- **Retention becomes structure (ruling 3).** The harness writes run artifacts into the REPO TREE from
  birth; a run is not complete until they are written AND committed. Enforced in code: `RunRecord.artifacts`
  carries the durable in-repo paths `{captured, b10, report}`, and `render_report` **refuses to render a
  real-mind run** (`RetentionError`) unless its captured evidence is present and NOT under a temp dir
  (`_assert_durable`). Scripted/hermetic runs render freely (instrument tests, not measurements). Two
  losses to `/tmp` is two; there is no third.
- **The advice channel — fertility is world-side, not an agent ◆ (ruling 2, per A5).** Fertility is the
  ADJUDICATOR'S advice, never the agent's inference, so it is NOT scored as a call the agent must surface
  (the agent's silence on it is constitutional obedience). A benchmark declares `advice`
  (`[{channel, member}]`); the eval checks the advice FIRES deterministically world-side
  (`benchmark_advice_fires` / folded into `benchmark_coherence`) — fertility fires for a formable derived
  RATIO of additive measures. **B8 is corrected**: it exits the ◆ set → ○, drops its agent-fertility
  oracle call, and carries `advice: [{fertility, aov}]`. The remaining agent test on B8 is the mechanical
  closures + the polarity wall (never proposing an opening, structurally enforced).

## 2c · The first measured iteration is recorded (ruling 5)
Run 5 (`specs/context/run5_causal_result_v1.md`) is the harness thesis's first measured confirmation:
KP v0.2 control vs KP v0.3 treatment, one keyed session, scorer 0.4, only the prompt varying —
**◆-explicitness 4/7 → 6/7, passes 3 → 5**, directional at n=1, m-leak crux confirmed. KP v0.3 is the
live KP; v0.2 archives as control. **Next measured variable: FLOODING (KP v0.4, concentration), with
replication n≥2 per arm** batched into ONE keyed session that also (a) captures B10's proposal-vs-truth
detail into specs (the standing ruling-3 debt) and (b) passively re-measures loop-violations across the
replicates (the revise-discipline variance question answers itself with n). v0.4's exact text goes to
Huayin for ratification first.

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
