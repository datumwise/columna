# The Open Planner — kernel and searcher (fork document v0.8)

*datumwise desk artifact, 2026-07-27, v0.8 (round 10 folded; PRIORITY STAKED: the program note is published — DOI 10.5281/zenodo.21632723, 2026-07-27; provisional items upgrade at v1.1 on the execution beat's results).
Status: DESIGN, pre-implementation. This
document is the development brief for the team loop (Huayin ratifies; desk
adjudicates; CC verifies by execution; external searcher searches). External
claims land UNVERIFIED until executed. Origin: Huayin's sufficiency insight,
2026-07-26 evening.*

---

## 1 · The claim (precise form)

Columna's query planner decomposes into two components with different trust
requirements: a **searcher**, which finds candidate plans and may be
probabilistic, external, or adversarial; and a **kernel**, which is small,
deterministic, engine-owned, and adjudicates every candidate before execution.
Nothing executes unvalidated. Therefore an LLM agent (e.g., a NOOA-style
code-acting agent) is *admissible as a planner* — not because it is trusted,
but because the architecture makes trust in the searcher unnecessary.

**The governing doctrine**: probability is admitted to search, never to
adjudication. As testable claims (external reviewer's crystallization,
renamed C1–C4 to avoid the roadmap's P-numbers): **C1 searcher
substitutability** (round-4 rename) — any component receiving the
planning-sufficient public interface can participate as an UNTRUSTED
candidate generator; admissibility as a searcher is distinct from
competence as one; **C2 kernel
completeness** — every servable ask has at least one certifiable Plan IR,
where SERVABLE is defined planner-independently (round-4 circularity fix):
an ask whose FrameQL denotation is defined over the declared Manifold and
for which the model licenses a result under the mood contract;
**C3 dual correctness** — certification establishes Lawful(plan, model) AND
Faithful(plan, ask, model); **C4 planning sufficiency** — the searcher needs
nothing beyond the public planning-sufficient projection.

**The sufficiency theorem (Huayin)**: planning requires no private inputs.
The planner's knowledge divides into (a) the law — transport rules, face
requirements, anchor licensing, summarizability — which is public by
publication (the papers, the manuals, the grammar page), and (b) the meaning
of the specific dataset — which is exactly the `describe` projection, public
by design (§2b insulation: logical names only, licenses included). Everything
needed to PLAN is public; private information (the physical map, credentials)
is needed only to EXECUTE. Hence planners are public buildable software, and the describe boundary is
simultaneously the security boundary and the planning-sufficiency boundary.

Two precisions (v0.2). **Admissibility vs optimality**: the theorem claims
ADMISSIBILITY-sufficiency — describe + ask suffices to construct at least one
certifiable plan. OPTIMALITY-sufficiency is not claimed: cost-based choice
may use private physical statistics, engine-side — the engine (inside the
TCB) may apply meaning-preserving rewrites to any certified plan. The
searcher finds an admissible computation; the engine makes it fast — under
**P-REWRITE**, stated as a conservation law (round 5): Certified(P) ∧
Rewrite(P, P′) ⇒ ⟦P′⟧M = ⟦P⟧M — the trusted engine may transform freely
within denotation preservation. Precision: this is not new risk — today's
co-designed planner+engine already rewrite implicitly inside the trusted
path; the split makes the boundary visible and the obligation nameable. **The
formal object (external reviewer's notation, adopted)**: D = describe(M) is a
PLANNING-SUFFICIENT PROJECTION iff for every servable ask A there exists a
plan P constructible from (D, A) with Kernel(M, P, A) = certified. **The
necessity dual (round-3 question, adopted as central)**: what is the MINIMUM
information that must cross the trust boundary? Predicted three-tier
structure, formalized (round 4): N ⊆ D ⊆ H, where N = information logically
necessary for ANY certifiable plan to exist (semantic sufficiency), D = the
published describe projection, H = information improving a given searcher's
success probability/cost (search sufficiency) — H may contain DERIVED
material (examples, canonical plans, prose), which is what makes
documentation's value measurable without conflating it with necessity —
with the corollary experiment that folklore descriptions, logically
unnecessary, should measurably raise a probabilistic searcher's success
rate. Documentation's role in a certified system becomes measurable.

## 2 · Definitions

- **Plan IR**: a declarative artifact describing a candidate execution —
  transports, anchor spends, face selections, alignment steps, reducers —
  over LOGICAL names only. Today this exists as planner internals;
  formalizing it as a stable, documented, serializable artifact is work item
  one. The IR must be complete for the grammar (every servable ask has an IR)
  and closed (the IR can express nothing the law forbids expressing — where
  impossible, the kernel rejects).
- **Certificate**: the kernel's verdict on a plan: admissible / rejected
  (with the violated law named) — plus the derivation obligations it
  discharged (below).
- **Searcher**: anything that emits Plan IR. The in-engine static planner is
  searcher #0. An agent reading `describe` is searcher #1. A human is a
  legitimate searcher.
- **Kernel**: the deterministic checker; the ONLY component with authority
  to admit a plan. Requirement (round-3 correction): small and auditable
  enough to constitute a CREDIBLE trusted computing base — the
  order-of-magnitude size ratio vs the static planner is an empirical
  target, not a definition. TCB precision: kernel + engine are one trust
  base; the kernel MAY share the engine's code (already trusted) and must
  never share the searcher's. Searcher-exclusion is the property; kernel
  smallness is the marginal audit cost. The honest metric: how much
  machinery must be trusted to believe the answer was not fabricated by the
  searcher.

## 3 · The kernel's two obligations — and the second one is the research

**(A) Lawfulness**: the plan violates no law of the declared model. Concretely,
per the shipped adjudication machinery: every transport step follows a
corroborated hierarchy edge and crosses no blocked edge; every M:N crossing
declares a face and spends it lawfully; anchors are spent within license;
basis semantics respected; alignment steps only where the (0.14) alignment
law licenses them; reducers within family bounds. Lawfulness checking is
near-mechanical — it replays the same rules the static planner obeys
constructively, as checks.

**(B) Faithfulness**: the plan COMPUTES THE ASK. This is the deep obligation,
and the one that distinguishes this design from its ancestors: a lawful plan
answering a *different* question than the one asked would be a new silent
failure mode — the exact disease this house exists to cure, reintroduced one
layer down. Proof-carrying code certifies safety, not intent; we must certify
both. The reason faithfulness is checkable at all: the ask is FrameQL, whose
denotation over a Manifold is small and formal (the papers' semantics). So
the kernel's obligation B is: verify the plan is a correct implementation of
the ask's denotation — plan ⊨ ask — by structural correspondence (each
IR step justified by a semantics rule), not by testing. Working name: **the
faithfulness certificate**. If obligation B cannot be discharged for some
plan the searcher found, the kernel rejects even if the plan is lawful — and
the mood machinery reports it honestly (below).

## 4 · The escalation ladder

1. Ask arrives → **searcher #0** (static planner). Serves the overwhelming
   majority; nothing changes for the served path.
2. Static planner returns a *plannable refusal* — the ask is legal, the
   deterministic search is not implemented for its class (today's recall
   ledger: OF-13 coordinate-WHERE, P1/0.14 alignment compositions,
   crossed-population distinct, face chains) → **searcher #1** (the agent)
   is invoked with `describe` + the ask; it emits Plan IR.
3. Kernel adjudicates: obligations A and B. Admit → execute → the answer
   carries its certificate in disclosures ("plan searched by X, certified by
   kernel vN"). Reject → the mood contract takes over: reject-with-reason,
   or clarify if the searcher surfaced a genuine ambiguity the ask's grammar
   permits.
4. **Cache**: certified plans are cached keyed by ask shape (the
   normalization of the ask modulo literals). The searcher runs once per
   novel shape; every replay executes the pinned canonical plan — which is
   also the determinism OF-23(b) wants, arrived at independently.

## 5 · Authority model

The searcher holds ZERO ambient authority: no connection, no credentials, no
map, no engine handle. Its entire I/O is (describe, ask) → Plan IR. Pass-by-
reference stops at the plan document. A compromised or hallucinating searcher
can waste kernel cycles and nothing else. Kernel and engine remain one
trusted computing base; the searcher is explicitly outside it.

## 6 · Lineage — the adjudicated prior-art sweep (round 6, RG; desk-verified)

**Certified compilation of queries**: Q*cert (SIGMOD 2017,
querycert.github.io) and DBCert — Coq-verified SQL compilation pipelines.
Cover: machine-checked compiler correctness for a query language. Don't
cover: untrusted searchers, per-candidate certification, ask-faithfulness,
public-projection sufficiency. [VERIFIED by desk search: querycert.github.io
live, SIGMOD'17 demo confirmed; DBCert = arXiv:2203.08941, PACMPL 2022,
"first mechanically verified compiler from canonical SQL to imperative
code" — RG's characterizations accurate on every checked citation]

**Translation validation** (Pnueli et al.; Necula; Leroy's validators):
per-run validation of an untrusted transformation's OUTPUT rather than the
transformer — the closest mechanism ancestor to our kernel-checks-each-
candidate posture. Doesn't cover: semantic models adjudicated against data,
or intent (ask) conformance.

**LLM-plan structural validation (the 2026 wave)** — the nearest neighbors,
all verified against the live record: **PlanCompiler** (arXiv:2604.13092):
typed JSON plans over a fixed node registry; a deterministic validator runs
seven STRUCTURAL checks (node existence, edge validity, type compatibility,
acyclicity, orphans, arity, required params) before execution — obligation A
in our vocabulary, and the paper itself concedes structurally valid plans
can survive validation while wrong — obligation B named as absent by the
neighbor's own text. **SPIN** (2605.14051): DAG-contract validation +
repair prompting — structural. **POLARIS** (2601.11816): typed planning,
validator-guarded execution, policy constraints — governance-structural.
**LLM-QO** (VLDB 2025): an LLM writes execution plans directly, replacing
the optimizer's search — the UNGATED searcher; our anti-pattern exhibit.
**Text-to-SQL validators** (constrained decoding, schema linking): safety
and syntax, never denotation. **VeriPlan** (LTL/model-checking for LLM
plans): temporal-logic safety in general planning, not analytical
denotation. **ZKP-SQL** (PoneglyphDB, ZKSQL): proofs of EXECUTION
integrity, not of plan-intent conformance.

**The seam — nearby consistency objects (round 7, RG; anchor desk-verified)**:
industry consistency mechanisms sort into three OBJECT classes, none of
which is the seam. (a) *Plan-tree integrity after rewrite*: Elasticsearch
ESQL's plan-consistency verifier (PR #105371, shipped 8.13.0 —
VERIFIED: a sanity rule asserting node dependencies survive each optimizer
pass; Elastic has since grown a family: expression validation #105477,
layout checks #130855, dependency checker #130409) — obligation-A-shaped,
structural, single-derivation. (b) *Plan identity over time*: Oracle SQL
Plan Management / SAP HANA plan stability — pin a chosen plan against
optimizer drift [training-era, well-established]. (c) *Result equality
across versions/engines*: Materialize's self-correcting materialized views
(output-drift diffs on upgrade) [training-era]; Meta-style engine-migration
replay [plausible-class, unverified]. **Bounded nothing-found**: no system
identifies, exploits, or certifies DERIVATION-vs-DERIVATION agreement of
the same semantic facts by a planner path and an executor path within one
system — the A1 seam. Consequence: CC's seam test has no published
precedent; the test is itself a contribution, and the related-work
paragraph now has its structure (three existing consistency objects; the
fourth is the gap).

**C4 corroborated from the literature's own structure (round 7, RG)**: the
cost-based optimization corpus uniformly treats physical statistics,
histograms, and indexes as OPTIMALITY inputs — absence yields suboptimal
plans, never inadmissible ones; logical correctness is fixed by query +
logical schema. Bounded nothing-found for any planning-decision class
requiring private physical inputs for ADMISSIBILITY. Reading: the field
has held the admissibility/optimality split implicitly since System R and
never isolated it as a theorem, because planners always lived INSIDE the
trust boundary — untrusted searchers make the boundary load-bearing and
public for the first time. (The sufficiency theorem names and formalizes
an assumption forty years of practice already obeyed.)

**P-FAITH ancestors (rounds 8–9, RG; key anchors desk-verified)**:
**Grain Theory** (Karayannidis, arXiv:2601.00995, Jan/May 2026 — VERIFIED):
type-level grain with a bounded lattice (≡g, ≤g, ⟨⟩g), compositional grain
lifts (φ(h₂∘h₁)=φ(h₂)∘φ(h₁)), CalcG deciding pipeline grain-correctness
from schema alone, fan/chasm traps, Lean 4 proofs. THE ADJUDICATED DELTA,
proven at the desk: **Attack B escapes it** — the unfaithful plan's every
intermediate grain is coarser than its input (no refinement, no
duplication), so CalcG passes it clean while the answer runs 1.21×; the
violation lives in the MEASURE ALGEBRA (a reducer's denotation fixes its
input grain), a layer grain theory lacks. We adopt the lift-composition
machinery style for the kernel's grain fragment and show the flagship
attack is invisible to it. **The two-directions completion (round 10,
desk)**: intermediate-grain violations come in two directions, and they
land on OPPOSITE certificates — the REFINEMENT direction (fan trap:
intermediate finer than input, join-fanout duplication) is in Columna an
obligation-A concern, governed by face law (touch double-counts by
declared meaning and discloses; split conserves) and already shipped; the
COARSENING direction (mean-of-sums, Attack B) is grain-clean and
lawful-per-node, catchable only by the denotation — obligation B. The
literature's best formal pathology and our flagship attack split across
the two certificates: structural evidence the dual-certificate thesis
carves at a joint. (Corrects the searcher's round-10 summary, which
conflated the fan trap with Attack B against its own round-9 material —
drift caught by the kernel, logged without penalty.) **Mechanization
leads (round 10)**: the grain-theory Lean artifact (zero-sorry, pinned
toolchain, 36+9 opaque-structure axioms, property-based cross-validation
against PostgreSQL, Agda twin) is adopted as the METHOD TEMPLATE for
mechanizing the kernel — Manifold laws as axiom base, obligation
discharge as theorems, rejection as type error; and the Lean-verified
Datalog certificate checker (checker of proof trees against formalized
semantics) is logged as the closest implementation ancestor for
P-KERNEL's kernel-as-verified-checker route [SEARCH-DERIVED,
unadjudicated]. Further deltas: their incomparability (⟨⟩g) is
an error boundary — our faces turn a governed subset of incomparable pairs
into lawful crossings; their grain is declared-and-typed — ours is TRIED
(edges corroborated on attested data at publish). **Proof-Carrying Plans**
(PADL 2019 / arXiv:2008.04165, resource logic, Curry-Howard — training-era
real): owns the bare phrase; ours becomes "certified analytical plans";
their types encode goal pre/postconditions, ours a denotation over an
adjudicated model — and their plans-inhabit-types construction is a logged
formalization LEAD for obligation B (IR nodes as typed combinators, the
ask's denotation the goal type, faithfulness = inhabitation)
[SEARCH-DERIVED, unadjudicated]. **U-semiring SQL equivalence** (Chu et
al., arXiv:1802.02229 — training-era real): candidate machinery for
P-EQUIV's semantic layer. QED/RuleScript and aggregation-consistency
(arXiv:2307.00417) ride as [plausible, unverified]. **Bounded gap
restated**: no published obligation language walks an analytical Plan IR
node-by-node against an ask denotation; no dual certificate exists; the
M₀→M₁ protocol is unnamed in the corpus.

**NOTHING FOUND — four regions, RG's sweep + the desk's independent
verification search agreeing**: (i) a metadata-sufficiency theorem for
planning; (ii) LCF/PCC-descended kernels applied to analytical planning
over a DATA-ADJUDICATED semantic model; (iii) dual certificates —
lawfulness AND ask-faithfulness; (iv) certified plan-equivalence as a
kernel duty. These four absences are the novelty claims, now citable as
bounded negative results. The deltas this design claims over the lineage:

1. **Adjudicated target**: the kernel checks against a meaning model that was
   itself TRIED against the data at publish (licenses, verdicts) — not
   against type safety or memory safety. The certificate chain runs
   data → adjudicated model → certified plan → served answer.
2. **The sufficiency theorem**: searchers are commodity BY CONSTRUCTION
   because the planning-sufficient projection is public. Stated with
   prior-art discipline (round-3 correction, desk's overclaim struck): we
   have not yet identified a prior system combining planning-sufficiency of
   a public projection with semantic analytical adjudication — the
   literature search establishes whether that holds.
3. **Mood integration**: search failure and certification failure degrade
   into an honest answer vocabulary (clarify/refuse with reasons) rather
   than an error. The certificate system can speak about its own gaps.

## 7 · Open problems (the honest list)

- **P-IR**: formalize the Plan IR. Completeness w.r.t. the grammar;
  canonical serialization (certificates must be over canonical bytes);
  versioning discipline when the law grows. The three-way tension (round-3,
  adopted): too expressive → huge kernel; too restrictive → lost recall;
  target sequenced (round 4): first a MINIMAL-ENOUGH CLOSED IR extracted
  from the current planner's internals (extract → prove closure → prove
  faithfulness → measure kernel), with actual minimality a later
  theorem — premature minimization risks hiding a missing semantic
  operation. Minimality ultimately serves P-EQUIV and the kernel-size
  target.
- **P-FAITH**: the faithfulness proof system. What is the obligation
  language? Structural correspondence rules per IR step; what fragment needs
  more than syntax-directed checking (suspects: alignment compositions,
  face-chain reassociation)? Attack classes (round 4): **A** obvious lawful
  substitution (revenue↔inventory by category) · **B** semantically adjacent
  (avg revenue per customer vs per transaction — note this is the Two
  Anchors' input-grain subject) · **C** observationally-equivalent traps
  (wrong plan, right answer on current data) — C proves output-testing can
  never substitute for plan ⊨ ask. Round-5 upgrade, adopted as the flagship
  exhibit: the M₀→M₁ perturbation protocol — two plans, equal outputs on
  M₀, different denotations; add one chosen row (M₁) and the outputs
  diverge, making same-observation ≠ same-semantics experimentally
  undeniable. **The attack corpus already exists
  (desk, round 4): the Silent Failure Atlas's 67 entries and the benchmark's
  14 defect classes ARE the lawful-but-unfaithful pattern library, with 111
  frozen asks as test vectors — the taxonomy built to grade models grades
  the obligation language one layer down.**
- **P-KERNEL-SIZE**: demonstrate the kernel is genuinely small — target: the
  checker is an order of magnitude less code than the static planner, or the
  trust story weakens.
- **P-EQUIV**: sequenced per round 5 — actual DAG → canonical DAG
  serialization → SEMANTIC equivalence (⟦P₁⟧M = ⟦P₂⟧M); never
  flatten-and-compare, since columns share CARVE/ANCHOR and naive tree
  normalization destroys meaningful sharing. Ask-shape normalization for
  the cache rides the canonical layer.
- **P-RECERT**: Manifold version bump invalidates which certificates?
  (Cheap answer: all; right answer: those whose obligations touched changed
  declarations — needs the obligation-to-declaration dependency recorded in
  the certificate.)
- **P-SUFF**: the sufficiency test as CI — plan the full battery from
  describe-JSON alone; byte-identical certified plans required. Round-3
  upgrade, adopted: three environments (A: describe+map+credentials · B:
  describe only · C: describe + deliberately misleading physical metadata)
  must yield the same certified plan, proving non-reliance; then
  describe-minus-X ablations map the actual sufficiency boundary field by
  field. First known gap candidate: `blocked_edges` may not currently cross
  describe; if so, describe must be extended (safe today — kernel still
  rejects — but recall-lossy for external searchers).
- **P-ADV**: the adversarial searcher suite (round-3, adopted): #0 static
  planner · #1 LLM on (describe, ask) · #2 malicious (attempts: unlicensed
  crossing, double anchor spend, blocked edge, invented dimension, lawful
  plan for the wrong ask, certificate-input manipulation) · #3 random
  structurally-plausible IR. **P-BLIND (round 5)**: submit the SAME IR via
  every generator; the kernel's adjudication must be identical — K(M, P, A)
  depends on nothing else. (Demonstrated accidentally at the meta-layer:
  rounds 1–5 ran with the reviewer's identity misattributed and no
  adjudication changed — searcher substitutability held in practice before
  the test existed.) Success criterion, formalized (round 4): K(M, P, A) depends ONLY on the
  authoritative model, the candidate plan, and the ask — never on planner
  identity, confidence, provenance, token probabilities, search path, or
  attempt count. Same (M, P, A) from human, static planner, LLM, random, or
  adversary yields the identical kernel result.
- **P-ECON**: searcher cost bounding — token budgets per escalation, and the
  cache as the amortizer; what's the SLA story when search is slow?

## 7b · EXECUTED: Attack B, against the shipped Cascadia warehouse

`revenue.mean @ cal.month` — the faithful plan (mean over transaction
atoms, the FrameQL denotation) vs the lawful-but-unfaithful composition
(sum @ store·product·month, then mean of the sums). Both plans use only
lawful nodes. Six months shown; the divergence is 13–17% monthly, 1.21×
overall:

| month | faithful | unfaithful | ratio |
|---|---|---|---|
| 2024-01 | 139.91 | 164.03 | 1.172 |
| 2024-02 | 125.81 | 145.22 | 1.154 |
| 2024-03 | 127.25 | 149.38 | 1.174 |
| 2024-04 | 137.91 | 156.09 | 1.132 |
| 2024-05 | 139.14 | 158.48 | 1.139 |
| 2024-06 | 130.56 | 152.41 | 1.167 |

Node legality → plan legality → plan faithfulness: the three-level
distinction now has a printed receipt. (Desk construction via direct
queries mirroring the two IR compositions; CC's beat re-derives through
the engine path and freezes both IR documents as fixtures.)

## 8 · Task ledger and round-6 tasking

**Reviewer registry (never-silent correction)**: external-reviewer rounds
1–5 were conducted by ChatGPT, misattributed in conversation as Grok;
discovered post-hoc, documents unaffected (all credits read "external
reviewer"). Round 6+ reviewer: Grok ("RG"), onboarded fresh. The
misattribution is logged as accidental evidence for C1. **Rounds 6–10
delivered and adjudicated: five-for-five on delivery; citation accuracy
5/5 on every falsifiable check; one summary regression (fan trap ≠ Attack
B) caught by the kernel and corrected — the adjudication layer doing its
job on a true-citing searcher.** RG stands by — no search regions currently open; the loop
manufactures no make-work. The ball: CC's execution beat.** Misfire ledger, desk entry: the sweep was declared
"empty attachment" three times while its content was present in the
conversation record throughout — the kernel probed its reading view, the
uploads directory, and the transcript, every referent except the record it
was answering from. Clause recorded beside the proverbs: *a reader's view
is not the record; "I cannot see it" must never be spoken as "it does not
exist."*



Rounds 3–5 (predecessor): design critique delivered and folded; zero
artifacts. Round 6 (RG): **the sweep delivered and adjudicated** — §6 is
now the verified lineage, the four nothing-found regions are the citable
novelty claims. Standing: RG on call for verification-shaped tasks; the
gate returns to the desk/CC construction beat (IR closure shim · Attack B
engine-path fixture · Attack C perturbation pair · the seam test ·
P-BLIND). Diagnosis (round 4, mutual): a searcher was tasked with
construction — the architecture's own doctrine violated one meta-level up.
**REASSIGNMENT**: the IR strawman and the Cascadia attack construction move
to the desk + CC (repo access, verification by execution) as the program's
first post-launch beat; the external searcher keeps exactly one task —
the one matching its nature. **THE ARTIFACT GATE (constitution, all
seats)**: no further architecture prose is adjudicated — from any
participant — until the reassigned artifacts land. Round-5 tasking for the
external searcher:

1. **Prior-art sweep** on the precise-form claim of §1: LCF/PCC-descended
   architectures applied to database query planning or semantic layers;
   certified query optimization/compilation (e.g., validated optimizers);
   any system where an LLM proposes plans checked by a deterministic
   SEMANTIC validator (not a syntax/safety validator); any claim resembling
   metadata-sufficiency for planning. Citations, one line each: what it
   covers, what it doesn't.
2. **Attack P-FAITH — now concrete**: Cascadia's model is public in the
   shipped package (`pip install columna`; three universes —
   transaction/inventory/category_profile; faces touch/primary/split on the
   product↔category crossing; anchors per the case study). Construct the
   strongest LAWFUL-but-UNFAITHFUL Plan IR over Cascadia's actual model — a
   real artifact, not a category. The harder the example, the better the
   obligation language must become.
3. **Strawman the Plan IR**: propose a minimal IR (five to ten node types)
   sufficient for: a grain climb, one M:N crossing with a declared face, one
   anchor spend, one alignment step. We will adjudicate it against the real
   planner's internals.
4. **Counterexample the sufficiency theorem**: name any planning decision
   you believe requires information describe does not carry. Each candidate
   either breaks the theorem or hardens the describe contract — both
   outcomes are wins.

*Provenance note: §6's framing and §3(B)'s necessity were sharpened by an
external reviewer's round-2 restatement ("navigate a deterministic semantic
state space without being allowed to redefine it") — credited on
publication. All external contributions in this document are search results;
adjudication remains internal.*
