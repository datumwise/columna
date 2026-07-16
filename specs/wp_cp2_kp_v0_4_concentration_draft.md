# CP-2.x — KP v0.4 concentration edit: DRAFT for ratification (the second measured iteration)
**From: Claude Code, 2026-07-16. The single-variable edit Huayin ruling 4 authorized: a CONCENTRATION
treatment for checklist flooding. EXACT prompt text below; nothing goes live until Huayin ratifies (the
KP is frozen under the copy law). Run 6 then measures v0.4 against v0.3, with replication.**

---

## The finding this edit acts on (run 5 evidence)
Salience (v0.3) raised ◆-recall (4/7 → 6/7) — but on **B11 the checklist FLOODED** (5 items > max 2)
when refutation surfaced: recall was bought partly with padding. Run-4 also showed universal flooding.

**The fulcrum (again): exhortation is not a mechanism.** v0.3 ALREADY says "keep the checklist SHORT:
do not flood it" — and it flooded anyway. Just as *naming* m-leak did not make it surface, *telling* the
mind to be short does not make it concentrate. The treatment must give a concrete **discrimination gate**:
a rule for WHICH surfaced calls earn their line, so the checklist prunes to the load-bearing few.

---

## THE EDIT — one paragraph, appended to the sharp-calls block in `system_prompt.md`
**Insert** (exact text) as the final paragraph of the sharp-human-calls section (immediately after the
`refutation` bullet), leaving the four salience triggers and everything else UNCHANGED:

> Then PRUNE to what is load-bearing. A call earns its line only if BOTH (a) it is oracle-asymmetric —
> the machine cannot settle it for the human — AND (b) it is material HERE: naming it would change what
> the human declares. A fact the machine can check for itself (a column type, a declared key, a
> mechanical closure) is NOT a review call — propose it, do not flag it. A trigger that fires on an
> immaterial case is dropped, not surfaced. Surface the one or two calls that actually carry the
> decision and drop the rest; prefer a short, differentiated checklist — even an empty one — to a padded
> list. A long undifferentiated review re-creates the automation bias the whole design exists to kill.

---

## Why this is ONE variable (the discipline)
- **Only concentration moves.** The four salience triggers (additivity · m-leak · fertility · refutation)
  are carried VERBATIM — v0.4 does not touch which doctrines fire, only prunes the surfaced set to the
  load-bearing calls. basis/universe wording, the output contract, grades, polarity, the loop law: all
  untouched.
- **The gate must NOT undo the salience gains.** The prune keeps a call that is oracle-asymmetric AND
  material — which is exactly what the genuine m-leak/refutation/basis/universe calls ARE on the
  benchmarks that hold them. So recall on the RIGHT benchmark should survive; only padding is cut. If
  the prune over-cuts (◆-recall drops back), the run says so — that is the measured risk.

## The falsifiable prediction run 6 tests
1. **Concentration rises** on the ◆ set (B11's flood clears; `concise✓` where it was ✗) **without
   ◆-explicitness falling** from v0.3's 6/7 — the clean win.
2. **Failure branch:** if ◆-recall drops (the prune silenced a genuine call), the gate is too aggressive
   — re-tune, do not ship. Concentration bought with recall is not a win.
3. **Controls unmoved:** closures/grades on the mechanical ○ benchmarks must not shift.

---

## The batched run (ruling 4) — run 6, ONE keyed session
- **A/B with replication, n ≥ 2 per arm.** CONTROL = KP v0.3 (live), TREATMENT = KP v0.4, both scorer 0.4,
  B1–B11 (with B8 corrected), each benchmark run **k ≥ 2 times per arm**; the report aggregates per-arm
  **rates** (pass-rate, ◆-explicit-rate, flood-rate) so the n=1 noise that muddied run 5 (B3 regression,
  B9 lift) is quantified, not guessed.
- **Standing debts folded in (same session):**
  - **B10 proposal-vs-truth capture** written into `specs/context/` (ruling 3 durable), settling the
    run-5 retention gap for ruling 3's B10 evidence.
  - **Loop-violation re-measurement** across the replicates — the revise-discipline variance question
    (run 4 = 4, run 5 = 0) answers itself with n; no separate run needed.
- **Retention is structural now (ruling 3):** the harness writes `{captured, b10, report}` into
  `specs/context/run6/` FROM BIRTH; `render_report` refuses to render until they are durable, and the run
  is not complete until committed. No third loss to `/tmp`.
- **Provenance:** `kp_version` 0.3 (control) / 0.4 (treatment); `scorer_version` 0.4; `harness_config`
  records the replicate count k. run_id/timestamp stamped after.

---
**Status: RATIFIED AS WRITTEN & LIVE (Huayin, 2026-07-16).** The prune gate is now the final paragraph of
the sharp-calls block in `system_prompt.md` (KP v0.4); the four salience triggers and everything else are
unchanged. The exemption rider was considered and REJECTED — measure the trade, don't design it out.
**KP v0.3 archives as the run-6 control** (retrievable at git `dc83cee`, the pre-v0.4 HEAD).

**Reading instruction for run 6 (Huayin):** **refutation (B11) is the most at-risk call** under a strict
(a)-reading of the gate — first place to look. **Prediction 2's do-not-ship clause governs**: if
refutation goes silent, the gate is too aggressive — re-tune, do NOT ship. Concentration bought with
recall is not a win.

Run 6 is AUTHORIZED on the standing clauses: the batched session as drafted (n≥2 per arm, B10's
proposal-vs-truth captured into `specs/context/run6/`, loop-violations counted across replicates, every
artifact durable from birth under the retention gate). It fires on the standing key-and-go. Queue after
v0.4: revise-discipline, which run 6's replicated loop-violation measurement may itself resolve.
