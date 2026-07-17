# Run 7 — the concentration-FLOOR test (KP v0.3 control vs KP v0.5 treatment), n=3: RESULT — v0.5 SHIPS
**The re-tune's verdict, pre-registered.** One keyed session, two arms, same model (`claude-opus-4-8`),
same benchmarks (B1–B11, B8 ○, **B10 GT v2**), same scorer (**v0.4**), **k=3** replicates per (arm,
benchmark). Only the prompt varies: CONTROL = KP v0.3 (git `dc83cee`), TREATMENT = KP v0.5 (the floored
prune). Durable artifacts under the ruling-3 gate: `specs/context/run7/`. (First attempt aborted on
account credit exhaustion mid-control — the runner refused to write a partial report, ruling 3 held; this
is the clean re-run on a fresh key.)

## PRE-REGISTERED SHIP TEST — both pass → **SHIP v0.5**
| criterion | target | v0.5 result | |
|-----------|--------|-------------|--|
| (1) flood(mean) | ≤ 4.5 | **3.33** | **PASS** (below v0.4's 4.5 — the concentration win survived the floor) |
| (2) ◆-recall(mean) | ≥ 5.0 | **5.0** | **PASS** (= v0.3 control — the floor fully protected the sharp calls) |

**VERDICT: SHIP v0.5.** No post-hoc adjustment; the criteria were fixed before the run.

## Headline (means per replicate)
| arm | passed | ◆-explicit | flood | loop-viol (total) |
|-----|--------|-----------|-------|-------------------|
| CONTROL (v0.3)   | 3.67 | **5.0** | **6.67** | 2 |
| TREATMENT (v0.5) | 3.33 | **5.0** | **3.33** | 4 |

**The floor achieved BOTH ends at once: flooding halved (6.67 → 3.33, better than v0.4's 4.5) AND
◆-recall fully held (5.0, = v0.3).** v0.4 could only buy one at the other's expense; the evidence-justified
floor buys both.

## The three watched calls (Huayin's read order) — all clean
- **B11 refutation: HELD, 1.0 → 1.0.** The call your reading instruction named most-at-risk survived, again.
- **B1 basis: RECOVERED, 1.0 → 1.0.** Run-6's erosion (1.0→0.5 under the unfloored prune) is REVERSED.
- **B4 m-leak: RECOVERED, 1.0 → 1.0.** Run-5's crux gain, eroded in run 6 (1.0→0.5), is REVERSED and
  its flood held at 0. The floor precisely undid the collateral damage v0.4 did.

## The concentration win, per benchmark (flood CONTROL → TREATMENT)
B6 0.67→0.0, B7 1.0→0.33, B8 1.0→0.33, B9 0.67→0.0, B10 1.0→0.33 — the prune still hits padding hard on
the mechanical/non-triggered surface; the ◆ benchmarks whose triggers fire (B1/B2/B4/B10/B11) keep their
calls. Exactly the floor's design: prune everything untriggered, never a fired trigger.

## Loop-violations (revise-discipline — PASSIVE, ruling 5)
Control 2 / treatment 4 this run. Across runs: run-4 = 4, run-5 = 0, run-6-treatment = 2, run-7 = 2/4.
Still variance, still accumulating; no iteration until it settles (ruling 5). B1 (0→0.67) and B10 (0.33→0.67)
are the treatment's contributors this run — noted, not acted on.

## Disposition
**v0.5 is confirmed as the live KP** (ratified → live → measured → SHIPPED — no revert). The concentration
iteration closes as a WIN: v0.3 salience (◆-recall 4/7→6/7, run 5) → v0.4 unfloored prune (flood win,
recall cost, banked & reverted, run 6) → v0.5 floored prune (both, run 7). The arc is complete and the
live KP is the best-measured KP at every step.

## Standing debts / notes
- **Retention held** — durable artifacts from birth, committed; the credit-abort wrote nothing (ruling 3).
- **B10 under GT v2** — closure now scores the mind's either-decomposition (B10 pass 0.33 both arms; the ◆
  basis call surfaced 1.0 both).
- **n=3** quieted run-6's single-flip noise inside the comparison that mattered: the recall recovery
  (B1, B4 both to 1.0) is a 3-of-3 result, not a lucky flip.
