# The Open Planner: Certified Analytical Plans from Untrusted Searchers
### A research program and preliminary empirical report

**Huayin Wang** · datumwise (independent open-source research project) ·
datumwise.ai · contact@datumwise.ai
Version 1.3 · 2026-07-29 · License: CC-BY 4.0 · DOI: 10.5281/zenodo.21632723 (v1.0 stakes the claims · v1.1 beat-1 evidence + claim discipline · v1.2 re-centered abstract · v1.3 completes the beat: the observational-equivalence pair and provenance-blindness)
*Companion system: Columna (Apache-2.0), pip install columna. Prior deposits by this project: the Silent Failure Atlas; the Ground Truth benchmark; the theory papers linked from datumwise.ai/about.*

## Abstract

Analytical systems can contain implicit trust boundaries their designers
never named. We report one, discovered in a shipped open-source system
(Columna): the planner and the engine independently derive the same
semantic facts — transport edges — agreeing by co-design, certified by
nothing. The Open Planner makes that boundary explicit: it reifies the
computation as a certifiable intermediate object (an eight-node plan IR
extracted from the shipped planner) and separates **probabilistic search**
from **deterministic semantic adjudication** — an untrusted searcher
proposes plans; a small kernel certifies each candidate for **lawfulness**
(no law of the declared, data-adjudicated model is violated) and
**faithfulness** (the plan implements the ask's denotation — plan ⊨ ask)
before execution. An executed, independently verified attack demonstrates
the distinction is not academic: a plan lawful at every node, with
locally coherent grains, diverges from the faithful answer by 13–17%
monthly (1.21× overall) on public demonstration data. The seam now holds
its first certificate (56 comparisons, 0 disagreements, perimeter
stated). We further state a **planning-sufficiency claim** — everything
required to construct a certifiable plan is contained in the model's
public logical projection, making planners public buildable software —
as the enabling condition for the searcher's seat being open. A bounded
prior-art sweep found no published work in four specified regions. The
governing doctrine: **probability is admitted to search, never to
adjudication.**

## 1 · Setting

Columna is an open-source data framework in which meaning is declared (a
Manifold: universes, grains, measures, hierarchies, M:N crossings governed
by declared "faces"), adjudicated against the data at publish (every
declaration is tried and carries a verdict), and served through an engine
whose answers arrive in one of four moods: served, disclosed (with
assumptions), clarified (the question has several legitimate readings), or
refused (with the reason). There is no SQL anywhere in the system; the
engine executes its own plans over the declared model. Agents and humans
read the same wire contract. The `describe` projection exposes the model's
logical content only — names, structure, licenses, verdicts — never
physical bindings (§2b insulation, enforced by test).

## 2 · The claim

Once planning becomes untrusted, semantic agreement that was previously
implicit in a co-designed planner/engine becomes a trust-boundary
obligation that must be represented, certified, and tested explicitly.
The planner decomposes into a searcher and a kernel with different trust
requirements. As testable claims:

- **C1 — searcher substitutability.** Any component receiving the public
  planning interface can participate as an untrusted candidate generator
  (admissibility as a searcher is distinct from competence as one).
- **C2 — kernel completeness.** Every servable ask has at least one
  certifiable plan, where *servable* is defined planner-independently: an
  ask whose denotation is defined over the declared Manifold and for which
  the model licenses a result under the mood contract.
- **C3 — dual correctness.** Certification establishes Lawful(plan,
  model) AND Faithful(plan, ask, model).
- **C4 — planning sufficiency.** The searcher needs nothing beyond the
  public planning-sufficient projection.

**The sufficiency claim** (a formal definition plus a conjecture; the
P-SUFF experiment decides it). Planning requires no private inputs: the law
is public by publication; the meaning of the particular dataset is exactly
the `describe` projection, public by design. D = describe(M) is a
*planning-sufficient projection* iff for every servable ask A there exists
a plan P constructible from (D, A) with Kernel(M, P, A) = certified. Two
precisions: the theorem claims **admissibility**-sufficiency, not
optimality — cost-based choice may use private statistics engine-side,
under the conservation law **P-REWRITE**: Certified(P) ∧ Rewrite(P, P′) ⇒
⟦P′⟧ = ⟦P⟧. And the necessity dual is open — the NECESSITY HYPOTHESIS: N ⊆ D ⊆ H, where N is the
logically necessary core and H includes search-helpful surplus (making
documentation's marginal value experimentally measurable). We note that traditional cost-based optimizers generally treat physical
statistics as inputs to plan selection rather than as prerequisites for
semantic admissibility; the split has been held implicitly because
planners always lived inside the trust boundary. Untrusted searchers make
the boundary load-bearing and public for the first time.

## 3 · The kernel's two obligations

**(A) Lawfulness** is near-mechanical: replay the model's laws as checks —
transports follow corroborated hierarchy edges and cross no blocked edge;
M:N crossings declare and lawfully spend a face; anchors are spent within
license; reducers stay within family bounds.

**(B) Faithfulness** is the research problem. A plan can be lawful at
every node and still compute a different question than the one asked —
the exact silent failure the meaning layer exists to prevent,
reintroduced one level down. Existing proof-carrying and checked-search traditions certify the
properties their certificates encode; none hands us the particular
obligation plan ⊨ ask over a data-adjudicated analytical model. Faithfulness is checkable because the ask's
denotation over a Manifold is small and formal: the obligation is
structural correspondence of each IR step to a semantics rule — never
output testing (§6, Class C, shows why testing cannot suffice).

## 4 · The extracted IR and the seam

From the shipped planner we extracted (not invented) an eight-node IR:
ANCHOR · CARVE · COLUMN · TRANSPORT · CROSS · REDUCE · ALIGN · DERIVE —
a per-column DAG joined at ALIGN. Two findings:

**There is no reified plan object in the shipped system, and the
transports are computed twice** — once planner-side for the
certificate/disclosure surface, once engine-side for execution — agreeing
by co-design, certified by nothing. The architecture therefore does not
add a trust boundary to a clean system; **it exposes and formalizes one
that already implicitly ships.** Closing this seam (a test that
planner-derived edges ≡ engine-mirrored transports) has, per the sweep
below, no published precedent.

**Disclosure is a projection of the plan**: every caveat the system
serves corresponds to an IR node's declared consequence, so the
certificate can *generate* the disclosure — one certified artifact, two
readers (machine execution, human epistemics).

## 5 · Executed evidence [beat-1: independently verified]

**Attack B — lawful-but-unfaithful, executed on the public demonstration
warehouse.** Ask (shipped surface): `SELECT avg(revenue) AT {cal.month}`. Faithful plan: mean over
transaction atoms (the denotation). Unfaithful plan: sum at
store·product·month, then mean of the sums — every node lawful, the
composition a different statistic:

| month | faithful | unfaithful | ratio |
|---|---|---|---|
| 2024-01 | 139.91 | 164.03 | 1.172 |
| 2024-02 | 125.81 | 145.22 | 1.154 |
| 2024-03 | 127.25 | 149.38 | 1.174 |
| 2024-04 | 137.91 | 156.09 | 1.132 |
| 2024-05 | 139.14 | 158.48 | 1.139 |
| 2024-06 | 130.56 | 152.41 | 1.167 |

Overall 1.21×. Node legality → plan legality → plan faithfulness: three
distinct levels, and only the third catches this. *Status at v1.1 — three layers, three ranks: the NUMBERS are VERIFIED
(independent reproduction, exact, 12/12 + ratio, assert-on-divergence
fixtures frozen). The FAITHFUL half is ENGINE-EXECUTED. The UNFAITHFUL
half is NOT EXPRESSIBLE from the ask surface (the build restricts input
anchors to a single level) and was EXECUTED at its native IR layer from
the engine's own primitives, engine unmodified: one primitive pair, one
changed input-grain argument, a 21% different answer. Two findings ride
this: (F1) the shipped mood contract already CLARIFIES the
underdetermined form — the two horns are caught by structure, live — and
the pinned form, once expressible, is a different question faithfully
answered: no ask can be unfaithful to itself; unfaithfulness lives only
in the gap between a plan and an ask, which is why the kernel begins
where the grammar's protection ends — at the searcher's channel. And the
demonstration establishes the NECESSITY of the faithfulness obligation;
whether a kernel CATCHES the attack is exactly the open experiment (no
kernel exists yet — that is the program).* Class A (measure
substitution) is the one-rule base case. Class C — two plans with
different denotations and identical outputs on current data, diverging
after a one-row perturbation (M₀→M₁) — is specified as the flagship
demonstration that no finite set of output observations establishes
faithfulness.

## 5b · Beat-1 results (summary)

The dual-derivation seam now holds its FIRST CERTIFICATE: 56 comparisons
across the battery, 0 disagreements — two structurally separate BFS
traversals over separate edge collections, non-vacuity established before
the claim, a tamper-and-restore negative control baked into the artifact,
and the perimeter stated: the certificate covers the two traversals
including across the projection copy; the upstream declaration parse is
outside it. IR closure over the executable corpora (33 served asks across
four suites, reported separately): zero ninth-node candidates, all eight
nodes observed in the wild — closure is UNFALSIFIED, not proven. Class A
frozen: two lawful served plans differing in exactly one field
(COLUMN.measure_ref); beside it, an out-of-domain refusal exhibit — two
obligations, two different deaths: lawfulness kills one loudly before
faithfulness is consulted; only faithfulness catches the other.
ERRATUM (v1.0 → v1.1): v1.0's phrase "the system's 111-ask battery"
conflated the benchmark's 111 natural-language questions (a separate
public corpus over its own warehouse) with the executable ask corpus;
closure ran on the executable corpora as stated above. v1.3 also
corrects ask notation to the shipped envelope surface (`SELECT … AT
{anchor}`): earlier versions wrote asks in a schematic shorthand using
`@` as an output-anchor mark, but on the shipped surface `@` marks
INPUT anchors — an actively misleading choice in a paper about
input-grain attacks, caught in review.

**Class C — executed (v1.3, the flagship exhibit).** Protocol: find or
mint two plans with different denotations and identical outputs on the
current data (M₀), then perturb by one chosen row (M₁) and watch them
diverge. The natural-coincidence audit of the demonstration model found
exactly one coincidence — and it is ROBUST (a priority-1 assignment
nothing can outrank), yielding a construction lemma: coincidence
FRAGILITY is a requirement of the protocol, not an accident of it.
The minted fixture: M₀ = the multi-membership face and the assignment
face agree on EVERY row; M₁ = M₀ plus one membership row → exactly one
cell diverges, by exactly the perturbing product's revenue (+69,285.46).
Two plans, same outputs, different denotations, one row apart: **no
finite set of output observations establishes semantic faithfulness** —
the kernel must reason over the computation, not its observed results.

**Provenance-blindness — executed, with a finding (v1.3).** The
invariance holds where it must: values and semantic disclosures are
identical across generation paths and call counts. One annotation was
found varying with call count — and root-caused as a channel-taxonomy
defect, not a property failure: a MECHANICAL serving fact ("served from
cache", version-checked, true on every call) riding the semantic
disclosure channel under a semantic name. Every disclosure was true;
the label and the channel were wrong. Consequence, promoted to design
law: the certificate's disclosure projection must carry TWO channels —
semantic (call-invariant; provenance-blindness's true jurisdiction) and
mechanical (legitimately variant) — a split the shipped wire does not
make and the kernel design now mandates. Findings F1–F5 and two
instrument corrections are recorded in the program's beat report;
notably, the beat's verification layer caught two errors inside the
program's own artifacts and refused two findings that were not there
(a one-ULP difference correctly classified as noise; a provenance
effect that was call order in disguise).

## 6 · Related work (bounded sweep)

Verified against the live record: **Q\*cert** (SIGMOD'17) and **DBCert**
(PACMPL'22) mechanize compiler correctness for query languages — no
untrusted searcher, no ask-faithfulness. **Translation validation**
(Pnueli; Necula; Leroy's validators) is the mechanism ancestor — validate
each output, not the transformer — without semantic models adjudicated
against data or intent conformance. The **2026 structural-validation
wave** (PlanCompiler, arXiv:2604.13092; SPIN; POLARIS) checks LLM plans
for node existence, types, acyclicity, arity — obligation A's shape — and
PlanCompiler's own text concedes structurally valid plans can survive
validation while wrong: obligation B named as absent by the nearest
neighbor. **Grain Theory** (arXiv:2601.00995; artifact-verified: the
theory core is 35 Lean modules, zero `sorry`) supplies compositional
grain lifts and schema-only fan-trap detection — and our flagship attack
**escapes it**: the unfaithful plan's every intermediate grain is coarser
than its input, so grain checking passes it clean; the violation lives in
the measure algebra (a reducer's denotation fixes its input grain).
Notably, the two directions of intermediate-grain violation land on
opposite certificates — refinement (fan traps) is lawfulness (face law,
conservation); coarsening (mean-of-sums) is faithfulness — evidence the
dual-certificate distinction carves at a joint. **Proof-Carrying Plans**
(PADL'19) owns the phrase for AI planning (goal pre/postconditions via
Curry-Howard); our certificates target denotations over a
data-adjudicated model. **Our bounded search did not identify published work** in four regions: a
metadata-sufficiency theorem for planning; LCF/PCC-descended kernels over
data-adjudicated semantic models; dual lawfulness+faithfulness
certificates; certified plan-equivalence as a kernel duty.

## 7 · Open problems

**P-IR** (minimal-enough closed IR; canonical DAG serialization) ·
**P-FAITH** (the obligation language; attack classes A/B/C; leads: typed
combinators à la Curry-Howard, grain-lift composition for the grain
fragment, measure-algebra rules for reducer input-grains) ·
**P-KERNEL-SIZE** (a credible TCB; the kernel may share the engine's
code, never the searcher's) · **P-EQUIV** (DAG → canonical → semantic
equivalence; semiring machinery as candidate) · **P-RECERT**
(certificate invalidation under model evolution) · **P-SUFF** (the
three-environment protocol: describe+map, describe-only, describe+
misleading physics must yield the same certified plan; describe-minus-X
ablations map the boundary) · **P-ADV / P-BLIND** (adversarial searcher
suite; K(M, P, A) provably independent of provenance, confidence, and
attempt count) · **P-ECON** (search cost; certified-plan caching, which
also yields deterministic serving).

## 8 · A note on method

This program was developed by a loop that instantiates its own
architecture: probabilistic searchers (external AI reviewers) produced
candidate critique and literature; a deterministic adjudication seat
verified every claim against sources or execution; a build seat executed;
a human ratified. Searcher contributions were treated as unverified until
checked; citation accuracy across all falsifiable checks was 100%; one
searcher substitution occurred mid-program with no adjudication changes —
an accidental demonstration of C1. The rule that governed the loop
governs the architecture: **agreement is search evidence; execution is
evidence.**

## 8b · Claim status

| claim / artifact | evidence at v1.1 | status |
|---|---|---|
| C1 searcher substitutability | informal workflow illustration | OPEN |
| C2 kernel completeness | definition; P-SUFF planned | OPEN |
| C3 lawfulness | shipped adjudication laws | PARTIAL |
| C3 faithfulness | Attack B: necessity shown; no kernel yet | OPEN |
| C4 planning sufficiency | formalized; experiment planned | OPEN |
| Plan IR (8 nodes) | extracted; closure unfalsified (33 asks) | CONSTRUCTED+ |
| The seam | certified, 56/0, perimeter stated | EXECUTED |
| Attack B | 12/12 verified; IR-layer executed | VERIFIED |
| Class C (M₀→M₁) | minted pair; one-row divergence executed | EXECUTED |
| P-BLIND | invariance holds; channel-split finding | EXECUTED+FINDING |
| Prior art | bounded sweep, four regions empty | REPORTED |

## 9 · Status

v1.0 staked the program's claims on 2026-07-27; v1.1 added beat-1
evidence and the claim-discipline pass; v1.2 re-centered the abstract on
the discovered boundary; v1.3 (2026-07-29) completes the first execution
beat: the observational-equivalence pair and the provenance-blindness
runs, with their findings. Next: the kernel prototype (lawfulness
obligation first) and a Substrait mapping study for the plan IR. Correspondence and collaboration: contact@datumwise.ai.

Agreement is search evidence; execution is evidence.
