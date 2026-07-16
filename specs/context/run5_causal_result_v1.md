# Run 5 — the causal test (KP v0.2 control vs KP v0.3 treatment): RESULT (2026-07-16)
**The first measured KP iteration.** One keyed session, two arms, same model (`claude-opus-4-8`), same
benchmarks (B1–B11 v1), same scorer (**v0.4**), proposal-capture on. The ONLY variable is the prompt:
CONTROL = KP v0.2 (retrieved from git `0b95014`), TREATMENT = KP v0.3 (the live salience block). n=1 per
arm (single sample — see the caveat).

## Headline
| arm | passed | ◆-explicit | loop-viol | censored |
|-----|--------|-----------|-----------|----------|
| CONTROL (v0.2)   | **3/11** | **4/7** | 0 | 8 |
| TREATMENT (v0.3) | **5/11** | **6/7** | 0 | 6 |

**The salience edit moved the needle: ◆-explicitness 4/7 → 6/7, passes 3 → 5.**

## Per-benchmark (closure / explicit / passed), CONTROL → TREATMENT
| B | kind | doctrine | closure | explicit(◆) | passed | note |
|---|------|----------|---------|-------------|--------|------|
| B1  | ◆ | basis (control)      | F→F | T→T | F→F | closure miss both |
| B2  | ◆ | **additivity** (native) | T→T | T→T | **T→T** | surfaced in BOTH arms |
| B3  | ◆ | universe (control)   | **T→F △** | T→T | **T→F △** | control-arm REGRESSION (see caveat) |
| B4  | ◆ | **m-leak** (native)  | T→T | **F→T △** | **F→T △** | THE CRUX — named-in-v0.2-yet-silent → surfaced under trigger |
| B5  | ○ | mechanical           | T→T | T→T | T→T | stable pass |
| B6  | ○ | edge (FD)            | F→F | T→T | F→F | closure miss both |
| B7  | ○ | hierarchy            | F→F | T→T | F→F | closure miss both |
| B8  | ◆ | **fertility** (native) | F→F | **F→F** | F→F | RESISTED — silent in both arms |
| B9  | ○ | level                | T→T | T→T | **F→T △** | non-target improvement (noise) |
| B10 | ◆ | basis/registry (control) | F→F | T→T | F→F | surfaces the ◆ call, misses the universe decomposition |
| B11 | ◆ | **refutation** (native) | T→T | **F→T △** | **F→T △** | surfaced under trigger; checklist FLOODED (5 > max 2) |

## Reading (with discipline — n=1 per arm)
**The salience treatment works on 2 of the 4 native doctrines, cleanly:**
- **m-leak (B4)** silent → surfaced. This is the CRUX result: m-leak was *named* in v0.2 yet silent (run 4),
  and under v0.3's observable trigger it surfaces. **Confirms salience is scaffolding, not naming.**
- **refutation (B11)** silent → surfaced — but the checklist FLOODED (5 items > max 2): the predicted
  salience↔concentration trade appeared exactly here (recall bought at the cost of concentration).
- **additivity (B2)** surfaced in BOTH arms — no lift to measure this run (v0.2 already surfaced it here,
  unlike run 4; run-to-run variance in the control).
- **fertility (B8) RESISTED** — silent in both arms. The salience treatment did NOT surface it. Fertility
  is the holdout: the one native doctrine a prompt-only trigger did not move (the draft's prediction #2
  failure branch — the native doctrines may not all yield to a prompt fix).

**Caveat — this is n=1 per arm, and the control arm is not perfectly still.** B3 (universe, a control)
REGRESSED on closure/passed, and B9 (a non-target) improved — both are single-sample movements that a
stochastic mind produces run-to-run (run 4's 4 loop-violations also vanished to 0 here). So the ◆-recall
lift (4→6) and the m-leak/refutation flips are real and directional, but the clean one-variable isolation
is muddied by control-arm noise. A confident causal claim wants replication (k samples per arm) before
the flooding/fertility findings are acted on.

## RETENTION GAP (owned)
The run harness wrote its full artifacts (per-arm `render_report`, the B10 proposal-vs-GT capture, and the
captured-proposals JSON) to `/tmp`, which a cleanup wiped before they were moved into the repo — a
retention-infrastructure mistake (they should have been written to `specs/`). This file preserves the
scored AXES (above), read from the live run before the wipe. **Lost:** the proposal-level detail (what
each arm actually proposed), per-benchmark grade/concise/conv/retries, and specifically **B10's
proposal-vs-ground-truth capture** that ruling 3's evidence-retention asked for. B10's axes survive (both
arms surface the basis ◆ call, both miss the universe decomposition — consistent with the
over-specification hypothesis), but the exact proposals do not. **Fix:** the harness must write to
`specs/context/` henceforth; B10's proposal detail (and any replication) needs a targeted re-run on a key.

## Queue (unchanged; ruling-driven, one at a time)
Salience measured (this run). Next per the standing order: **flooding/concentration** (B11 gives it a live
handle now), then **revise-discipline** (0 loop-violations here vs 4 in run 4 — the finding itself may need
re-measurement before it's attributed). Nothing moves until Huayin rules on the next single variable.
