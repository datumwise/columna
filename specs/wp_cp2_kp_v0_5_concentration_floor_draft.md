# CP-2.x — KP v0.5 concentration-with-a-floor: DRAFT for ratification (the re-tune)
**From: Claude Code, 2026-07-16. The re-tuned concentration gate Huayin ruling 2 authorized after run 6
sent v0.4 back under prediction-2's do-not-ship clause. EXACT prompt text below; nothing goes live until
Huayin ratifies. Run 7 then measures v0.5 against v0.3 with PRE-REGISTERED ship criteria (ruling 3).**

---

## What run 6 measured (why v0.5 exists)
v0.4's unfloored prune (a call earns its line only if oracle-asymmetric AND material) **worked on
flooding — 7.5 → 4.5 mean** — but **eroded ◆-recall — 5.0 → 4.0**, silencing genuine **basis (B1)** and
**m-leak (B4)** calls (m-leak was run-5's crux gain). Prediction-2's do-not-ship clause governed; v0.3 is
live again, v0.4 banked as a measured intermediate. The gate wasn't mis-reading oracle-asymmetry — it was
over-aggressive on **materiality (b)**, dropping load-bearing calls as if they were padding.

## The provenance to record (the exemption, rejected then adopted)
The v0.4 draft **considered and REJECTED** an exemption rider — *"the exemption rider was considered and
rejected: measure the trade, don't design it out."* Run 6 measured the trade. **v0.5 ADOPTS that exemption
POST-measurement**, evidence-justified: the trade is now a datum (−3.0 flood for −1.0 recall, with the
recall loss on genuine sharp calls), not a guess. Design-out was wrong before the measurement; it is right
after it. This is the ratchet working exactly as intended.

---

## THE EDIT — replace the v0.4 prune paragraph with a FLOORED prune
**Insert** (exact text) as the final paragraph of the sharp-human-calls block in `system_prompt.md`
(where v0.4's prune paragraph was; the four salience triggers and everything else stay UNCHANGED):

> Then PRUNE — but with a floor. The six sharp calls above (basis, universe, and the four Columna-native:
> additivity, m-leak, fertility, refutation) are the load-bearing ones. When a call's TRIGGER fires on
> evidence you can actually see, it is ALWAYS material — surface it, every time. Never prune a triggered
> sharp call. The prune applies with full force to EVERYTHING ELSE: untriggered speculation (a call whose
> trigger you do not see in the data), a fact the machine can check for itself (a column type, a declared
> key, a mechanical closure — propose it, do not flag it), a repeat, or any padding — drop all of it. The
> checklist is exactly the triggered sharp calls: no fewer (never silence a fired trigger) and no more
> (never pad). A long undifferentiated review re-creates the automation bias the whole design exists to
> kill; a silenced sharp call re-creates the meaning-loss the whole design exists to prevent.

---

## Why this is still ONE variable (the discipline)
- **Only the prune's floor changes** from v0.4. The four salience triggers are carried VERBATIM (as they
  have been since v0.3); basis/universe wording, the output contract, grades, polarity, the loop law:
  untouched. v0.5 = v0.4's prune + the evidence-justified floor. The comparison that matters is v0.3 → v0.5.
- **The floor targets exactly the run-6 failure.** v0.4 silenced triggered basis/m-leak calls; the floor
  makes a triggered sharp call unprunable. The prune still hits padding (v0.4's win on flooding) — it just
  can no longer reach a fired trigger.

## Run 7 — the pre-registered ship test (ruling 3)
- **A/B, n=3 per arm.** CONTROL = KP v0.3 (live), TREATMENT = KP v0.5. Same model + scorer 0.4 +
  benchmarks (B8 ○, **B10 GT v2**). Higher n addresses run-6's single-flip noise inside the comparison
  that matters.
- **SHIP CRITERIA (pre-registered, both required):**
  1. **flood ≤ 4.5** (at or below v0.4's flood result — the concentration win must survive the floor), AND
  2. **◆-recall ≥ 5.0** (at or above v0.3's recall — the floor must fully protect the sharp calls).
  **If either fails, v0.5 does not ship either.** No post-hoc criteria; these are fixed before the run.
- **Standing:** durable artifacts from birth (ruling 3); loop-violations counted across replicates
  (revise-discipline stays passive — 4/0/2 is variance still accumulating, ruling 5); B10 scored under GT v2.

---
**Status: DRAFT — awaiting Huayin's ratification of the exact insert text. Nothing goes live, and run 7
does not fire, until ratification + the standing key-and-go.**
