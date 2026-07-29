# The Open Planner: Certified Analytical Plans from Untrusted Searchers
### A research program note

**Huayin Wang** · datumwise (independent open-source research project) ·
datumwise.ai · contact@datumwise.ai
Version 1.0 · 2026-07-27 · License: CC-BY 4.0 · DOI: 10.5281/zenodo.21632723
*Companion system: Columna (Apache-2.0), pip install columna. Prior deposits
by this project: the Silent Failure Atlas; the Ground Truth benchmark; the
theory papers linked from datumwise.ai/about.*

## Abstract

We propose an architecture in which the query planner of an analytical
system is split into an **untrusted searcher** — probabilistic, external,
possibly adversarial — and a small deterministic **kernel** that certifies
every candidate plan before execution. The kernel discharges two
independent obligations: **lawfulness** (the plan violates no law of the
declared, data-adjudicated semantic model) and **faithfulness** (the plan
implements the ask's denotation — plan ⊨ ask). We state a
**planning-sufficiency theorem**: everything required to construct a
certifiable plan is contained in the model's public logical projection, so
planners are public buildable software and the projection boundary is
simultaneously the security boundary. We report an extracted eight-node
plan IR from a shipped system; the discovery that the shipped system
already contains an uncertified dual-derivation seam the architecture
would close; and an executed attack demonstrating a lawful-per-node plan
that diverges from the faithful answer by 13–17% monthly (1.21× overall)
on public demonstration data. A verified prior-art sweep bounds four
regions where no published work was found. The governing doctrine:
**probability is admitted to search, never to adjudication.**

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

**The sufficiency theorem.** Planning requires no private inputs: the law
is public by publication; the meaning of the particular dataset is exactly
the `describe` projection, public by design. D = describe(M) is a
*planning-sufficient projection* iff for every servable ask A there exists
a plan P constructible from (D, A) with Kernel(M, P, A) = certified. Two
precisions: the theorem claims **admissibility**-sufficiency, not
optimality — cost-based choice may use private statistics engine-side,
under the conservation law **P-REWRITE**: Certified(P) ∧ Rewrite(P, P′) ⇒
⟦P′⟧ = ⟦P⟧. And the necessity dual is open: N ⊆ D ⊆ H, where N is the
logically necessary core and H includes search-helpful surplus (making
documentation's marginal value experimentally measurable). We note the
cost-based optimization literature has held the admissibility/optimality
split implicitly since System R — physical inputs affect plan *quality*,
never plan *existence* — without isolating it as a theorem, because
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
reintroduced one level down. Proof-carrying code certifies safety, never
intent; we must certify both. Faithfulness is checkable because the ask's
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

## 5 · Executed evidence [provisional]

**Attack B — lawful-but-unfaithful, executed on the public demonstration
warehouse.** Ask: `revenue.mean @ month`. Faithful plan: mean over
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
distinct levels, and only the third catches this. *Status: desk-executed
via direct queries mirroring the two IR compositions; engine-path
reproduction and frozen fixtures forthcoming (v1.1).* Class A (measure
substitution) is the one-rule base case. Class C — two plans with
different denotations and identical outputs on current data, diverging
after a one-row perturbation (M₀→M₁) — is specified as the flagship
demonstration that no finite set of output observations establishes
faithfulness.

## 6 · Related work (verified sweep, bounded)

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
data-adjudicated model. **Nothing found** in four regions: a
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

## 9 · Status

This note stakes the program's claims and evidence as of 2026-07-27.
Provisional items are marked; v1.1 will add the engine-path reproduction,
the IR-closure result over the system's 111-ask battery, the seam test,
the Class C pair, and provenance-blindness runs. Correspondence and
collaboration: contact@datumwise.ai.
