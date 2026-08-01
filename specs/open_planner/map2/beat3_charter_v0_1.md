# Beat 3 Charter — The Two Seams
### C3, the CROSS-bearing pilot · the DuckDB second-consumer inheritance test

*Charter v0.1 · 2026-08-01 · desk-drafted for ratification · executes under
the Open Planner program (fork doc v0.12 §11 tail) · inherits beat 2's
walls (§7 of its charter) unchanged · founds beat 3.*

---

## 1 · Mandate

Beat 2 proved the method: meaning-plans lower onto container engines under
conservation certificates, per-rule proofs amortize, and the cargo schema
holds its two channels under byte-diff. What it did not test are the two
boundaries the whole architecture stands on. **The vertical seam**: a plan
split between home and substrate — stay-home meaning-work feeding lowered
work, results crossing back — where the pushdown boundary stops being a
table column (S9) and becomes a runtime handoff. **The horizontal seam**: a
rule certificate offered to a *second* engine — where "certify once per
backend type" either transfers or drift refuses it. One beat, two seams;
each seam one experiment; both un-gated (per the corrected BLOCK-1: no
environment dependency exists or ever did).

## 2 · Experiment A — C3, the CROSS-bearing pilot (the vertical seam)

**The plan shape**: an ask whose derivation contains a stay-home CROSS
feeding lowered work — the canonical Cascadia form: revenue crossed
through a declared face (start with `touch`; see A-4), then
transported/reduced at a lowered grain. The exact ask is proposed by CC
from D1's table and adjudicated by the desk before build — attested
syntax, per standing law.

**What A must establish**:
- **A-1 — the mixed execution is conservation-clean end-to-end**: the
  full plan (home CROSS + substrate TRANSPORT/REDUCE) agrees with the
  all-home oracle under the D3 protocol. Acceptance: N ≥ 30, zero
  disagreements, stated tolerance, tamper control re-run with a
  seam-specific break mode — a deliberately corrupted handoff (wrong
  grain or dropped rows at the home→substrate boundary) must FAIL loudly.
- **A-2 — S7 gets its first exhibit**: the face spend recorded in the
  certificate (`{face_id, scheme, conservation_claim}`), shape settled
  against a real crossing; v0.3 of the schema opens on this.
- **A-3 — S9's stay_home boundary is executable truth**: the lowering map
  names which nodes ran where, and the harness *verifies* the split
  (substrate received only the lowered spans; the CROSS never left home —
  checked, not asserted).
- **A-4 — the disclosure chain survives the seam**: the crossing's
  disclosure (multi_counted for touch) reaches the answer intact when
  half the plan ran elsewhere — the custody law's observable half. If
  the touch pilot falls easily, an `alloc` variant with its
  reconciliation badge is the stretch goal: conservation arithmetic
  across the seam is the hardest honest test available. Stretch, not
  gate.

**What A must NOT do**: lower any part of CROSS itself (D1's verdict
stands: arithmetic per-shape at best, disclosure minting never); invent a
new handoff transport (the home→substrate exchange uses the existing
map/connector machinery — if that machinery can't express the handoff,
that is a FINDING and the pilot stops there, rowed).

## 3 · Experiment B — the DuckDB inheritance test (the horizontal seam)

**Setup**: consumer venv pinned `duckdb==1.1.3` + substrait extension
(the throwaway-venv proof, made standing); the engine and oracle stay
put. Same ibis-substrait plans, same D3 harness, consumer swapped.

**What B must establish**:
- **B-1 — the transfer question, answered with receipts, either way**:
  both existing rule certificates (TRANSPORT-shaped-sum, REDUCE-mean) are
  offered to DuckDB. Each either passes the full oracle protocol on the
  new consumer — minting its second rule certificate, same rule identity,
  new backend band — or fails, in which case **V4 executes as written: no
  cover, no lowering, the plan falls home**, and the failure is
  characterized (which function, what divergence, drift or gap). A
  refusal is a *result*: it would be the program's first live drift
  specimen and the empirical justification for per-backend proof.
- **B-2 — band mechanics become real**: the new certificates carry
  DuckDB's band (1.1.x + extension version); the §4b versioning question
  (band width, re-proof triggers) gets its first evidence-based answer,
  filed for schema v0.3.
- **B-3 — inheritance economics measured**: wall-clock and steps to
  certify consumer #2 vs consumer #1, recorded. The amortization claim
  ("a harness run, not a connector project") gets a number.

**What B must NOT do**: relax tolerance to make a transfer pass (the
tolerance policy is beat-1 law; a pass bought by loosened tolerance is a
silent failure of the study itself); ship the 1.1.3 pin anywhere near
production paths (study venv only — the version skew is itself rowed as a
deployment question for MAP-2(a), not solved here).

## 4 · Deliverables and acceptance (falsifiable)

DONE when: (1) **C3's certificate** exists — v0.2-conformant native
emission, A-1 through A-4 satisfied (A-4's alloc variant explicitly
optional), seam break-mode demonstrated; (2) **B's verdict matrix**
exists — 2 rules × DuckDB, each cell PASS-with-new-certificate or
REFUSED-with-characterization, no third state; (3) **schema v0.3 opens**
with S7's settled shape + the band-mechanics evidence (desk cuts it on
these inputs); (4) **D5 rows** filed as found — expected candidates
named now: the handoff-expressibility finding if A stalls, drift
specimens if B refuses, band-width question regardless; (5) the fold
lands in fork doc v0.13. Results that count as success without being
passes: a characterized drift refusal (B); a rowed handoff gap (A). What
counts as failure of the *study*: an uncharacterized refusal, a
tolerance quietly widened, an asserted-not-verified stay-home split.

## 5 · Division of labor and sequencing

**CC**: propose C3's ask (desk adjudicates before build) · build A then
B, or interleave at will — but **report A-3's split verification and
B-1's first cell before completing either experiment** (the two moments
where a surprise reshapes the beat). **Desk**: this charter; C3 ask
adjudication; schema v0.3 on the beat's inputs; the v0.13 fold.
**Ratifier**: this charter's word; A-4's alloc stretch call if it gets
close; acceptance of the beat's closure.

## 6 · Walls (inherited, plus two new)

Beat 2's §7 walls carry forward verbatim (no foreign plans, no
whole-plan delegation, custody absolute, no production wiring, no
completeness claims). New: **the tolerance wall** (§3-B) and **the
handoff wall** (§2 — existing machinery or a rowed finding, never an
improvised transport).

## 7 · Rank

Two experiments, two boundaries, every outcome informative and every
refusal a specimen. The beat asserts nothing in advance except what its
harness can check — and it inherits beat 2's best sentence as its bar:
the schema was accepted by its own native emission; the seams will be
accepted by their own verified splits, or refused with names.

*— the desk, for ratification. On the word, CC proposes C3's ask and
stands up the 1.1.3 consumer; the desk stands adjudication.*
