# The Open Planner — research program artifacts

**Committed on arrival, 2026-07-27** (commit-on-creation). Research instrumentation only: **nothing
in this directory changes any product surface, and no code here ships in a release.**

## The governing artifacts, in governing order

| # | file | what it is |
|---|---|---|
| 1 | `open_planner_fork_v0_8.md` | **the fork document** — the development brief. DESIGN, pre-implementation. Governs. |
| 2 | `open_planner_artifact_A1_v0_1.md` | **Artifact A1** — the eight-node Plan IR extracted (not invented) from the shipped planner, file:line pinned, plus the Cascadia attack set A/B/C. |
| 3 | `open_planner_deposit_v1_0.md` | **the published program note** — v1.0, 2026-07-27, CC-BY 4.0, **DOI [10.5281/zenodo.21632723](https://doi.org/10.5281/zenodo.21632723)**. Source of the deposited PDF. |

Where they disagree, the earlier number wins.

## The program in four lines

The Open Planner splits Columna's planner into an **untrusted searcher** (probabilistic, external,
possibly adversarial) and a small deterministic **kernel** that certifies every candidate plan before
execution. The kernel discharges two independent obligations: **lawfulness** (violates no law of the
declared model) and **faithfulness** (`plan ⊨ ask` — it computes the question actually asked).
Artifact A1 extracted an eight-node IR from the shipped planner and found the **dual-derivation
seam**: transports are computed twice — planner-side for the certificate/disclosure surface
(`planner.py:604`) and engine-side for execution — agreeing **by co-design, certified by nothing**
(`planner.py:689`). The governing doctrine: **probability is admitted to search, never to
adjudication.**

## The eight IR nodes

`ANCHOR` · `CARVE` · `COLUMN` · `TRANSPORT` · `CROSS` · `REDUCE` · `ALIGN` · `DERIVE`

**A ninth node is a FINDING, not a failure.** It gets reported, never absorbed.

## Beat 1 — the execution beat (this directory's work)

The deposit is published with §5 marked **provisional**, pending engine-path reproduction. This
beat's results upgrade the deposit to **v1.1**. Six deliverables, each carrying a status on the
ladder **CONSTRUCTED → EXECUTED → VERIFIED**:

| # | deliverable | status |
|---|---|---|
| 1 | IR closure — shim + 111-ask battery replay; every served ask factors through the eight nodes | see `BEAT_1_REPORT.md` |
| 2 | Attack B, engine path — faithful vs lawful-but-unfaithful, real machinery, frozen fixtures | ″ |
| 3 | The seam test — planner-derived edges ≡ engine-mirrored transports over the full battery | ″ |
| 4 | Class C — data-coincidence pair + the M₀→M₁ one-row perturbation | ″ |
| 5 | P-BLIND — identical `(M, P, A)` via distinct provenance wrappers; adjudication byte-identical | ″ |
| 6 | Beat report — statuses per the ladder, every number from the run | ″ |

Fixtures land under `fixtures/`.

## Standing off-ramps

These outrank the beat. If any fires, work stops and goes to the desk before anything is written:

- **A ninth IR node** → report it as a finding; never absorb it into the eight.
- **Seam disagreement anywhere** (deliverable 3) → that is a **LIVE BUG in shipped code**. It
  outranks this entire beat and off-ramps immediately.
- **Material divergence from the desk's Attack B numbers** (A1 §7b / deposit §5) → itself a finding;
  off-ramp to the desk before anything is written.

## The numbers this beat reproduces against

Desk-executed via direct queries mirroring the two IR compositions (A1 §7b, deposit §5).
**Agreement upgrades the deposit's provisional marker to VERIFIED.**

| month | faithful | unfaithful | ratio |
|---|---|---|---|
| 2024-01 | 139.91 | 164.03 | 1.172 |
| 2024-02 | 125.81 | 145.22 | 1.154 |
| 2024-03 | 127.25 | 149.38 | 1.174 |
| 2024-04 | 137.91 | 156.09 | 1.132 |
| 2024-05 | 139.14 | 158.48 | 1.139 |
| 2024-06 | 130.56 | 152.41 | 1.167 |

Overall **1.21×**.

## Discipline for this beat

Research instrumentation only. Zero product-surface changes beyond the one ratified site touch (the
seventh publications entry). No release. Launch-ready state undisturbed. Verify from the run —
**a green suite is not a green job.**
