# Run 6 — the concentration test (KP v0.3 control vs KP v0.4 treatment), REPLICATED: RESULT (2026-07-16)
**The second measured KP iteration, with replication.** One keyed session, two arms, same model
(`claude-opus-4-8`), same benchmarks (B1–B11, **B8 corrected → ○**), same scorer (**v0.4**), **k=2**
replicates per (arm, benchmark), proposal-capture on. The ONLY variable is the prompt: CONTROL = KP v0.3
(from git `dc83cee`), TREATMENT = KP v0.4 (the prune gate). Durable artifacts: `specs/context/run6/`
(`captured.json`, `b10.json`, `report.md`) — retained under the ruling-3 gate, from birth.

## Headline (means per replicate)
| arm | passed | ◆-explicit | flood | loop-viol (total) |
|-----|--------|-----------|-------|-------------------|
| CONTROL (v0.3)   | 3.5 | **5.0** | **7.5** | 0 |
| TREATMENT (v0.4) | 3.0 | **4.0** | **4.5** | 2 |

**The prune gate did its job on flooding (7.5 → 4.5) — but it cost ◆-recall (5.0 → 4.0).** That is
**prediction-2's failure branch**: concentration bought with recall is not a win.

## Per-benchmark rates (CONTROL → TREATMENT; △ = moved)
| B | kind | doctrine | pass | explicit(◆) | flood | note |
|---|------|----------|------|-------------|-------|------|
| B1  | ◆ | basis      | 0→0 | **1.0→0.5 △** | 1.0→1.0 | basis recall ERODED (1 of 2 reps went silent) |
| B2  | ◆ | additivity | 1→1 | 1.0→1.0 | 0.5→0.0 △ | held; flood cleared |
| B3  | ◆ | universe   | 0→0 | 0.0→0.0 | 1.0→1.0 | silent+flooded both (closure fails both) |
| B4  | ◆ | m-leak     | **1.0→0.5 △** | **1.0→0.5 △** | 0.0→0.5 △ | run-5's CRUX gain ERODED — recall down AND flood up |
| B5  | ○ | mechanical | 1→1 | – | 0.0→0.0 | stable pass |
| B6  | ○ | edge       | 0→0 | – | 1.0→0.5 △ | flood cleared |
| B7  | ○ | hierarchy  | 0→0 | – | 1.0→0.5 △ | flood cleared |
| B8  | ○ | (fertility→advice) | 0→0 | – | **1.0→0.0 △** | flood fully cleared; B8 now ○ (ruling 2) |
| B9  | ○ | level      | 0.5→0.5 | – | 0.5→0.0 △ | flood cleared |
| B10 | ◆ | basis/registry | 0→0 | 1.0→1.0 | 1.0→1.0 | surfaces the call, misses the (over-specified) universe split |
| B11 | ◆ | **refutation** | 0→0 | **1.0→1.0** | 0.5→0.0 △ | **HELD — the watched at-risk call did NOT go silent; flood cleared** |

## Reading (ruling-4 discipline, n=2)
1. **Flooding fell as designed: 7.5 → 4.5 mean** — the prune gate works; B2/B6/B7/B8/B9/B11 all shed
   flood, several to zero. The concentration mechanism is real (not the restated exhortation v0.3 already had).
2. **But ◆-recall fell: 5.0 → 4.0 — PREDICTION-2's DO-NOT-SHIP clause is triggered.** The erosion is on
   **B1 basis (1.0→0.5)** and **B4 m-leak (1.0→0.5)** — NOT on the watched B11 refutation, which **HELD
   (1.0→1.0)**. The m-leak erosion is the sharpest concern: it was run-5's crux gain, and the prune
   partly undid it (recall down, flood up on B4).
3. **The watched call survived; the collateral did not.** Your reading instruction named B11 as most
   at-risk under a strict (a)-reading; B11 held. The gate instead clipped basis and m-leak — genuine,
   material, oracle-asymmetric calls that the prune should have KEPT. So the gate is not mis-reading (a);
   it is slightly over-aggressive on materiality (b), dropping load-bearing calls as if immaterial.
4. **Loop-violations 0 → 2** — the treatment introduced two struck-re-proposals (the revise-discipline
   signal, run-4=4 / run-5=0 / run-6-treatment=2). Still noisy across runs; the variance question is not
   yet settled at this n.
5. **n=2 caveat:** every △ here is a single-replicate flip (1.0→0.5 = one of two reps). The flood
   reduction is corroborated across many benchmarks (robust); the recall erosion rests on 2 single-rep
   flips (B1, B4) — directional, not yet confident. Higher n would firm it.

## Disposition (for Huayin's ruling)
Per the ratified **prediction-2 do-not-ship clause**, ◆-recall dropped → **v0.4 does not ship as-is**.
v0.4 is currently the LIVE KP (ratified→live→measured, in that order), so the clause calls for **reverting
the live KP to v0.3 pending a re-tune** of the gate (less aggressive on materiality — keep basis/m-leak,
cut only true padding). BUT at n=2 the erosion is 2 single-rep flips, so the alternative is **replicate at
higher n before reverting**, to separate a real recall cost from noise. **Which — revert-and-retune, or
replicate-first — is Huayin's call.** Held; nothing reverted unilaterally.

## Standing debts settled this run
- **B10 proposal-vs-truth CAPTURED** (`b10.json`, ruling 3 debt): the mind proposed only `universe budget`
  (not GT's `catalog`+`budget`) while correctly surfacing the basis ◆ call — evidence for the
  over-specification read (the closure✗ penalizes a defensible ◆ decomposition, not a genuine miss).
- **Loop-violations measured across replicates** (0 control / 2 treatment) — the revise-discipline variance
  question is now being measured, not guessed.
- **Retention held:** artifacts durable in-repo from birth; no `/tmp` loss.
