# The Open Planner — kernel and searcher (fork document v0.12)

*datumwise desk artifact, 2026-07-27, v0.12, 2026-07-31 (BEAT 2 COMPLETE AND CLOSED by ratifier ruling: the outbound turn executed — two pilots, two rule certificates, the cargo schema accepted by its own native emission). v0.11 carried the ruling + the turn; beat 1 and rounds 8–9 at v0.9. Deposit at v1.3; theory published (10.5281/zenodo.21696104 v1.1 + 10.5281/zenodo.21707018). DOI 10.5281/zenodo.21632723.
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

**Ecosystem rounds 8–9 (RG; desk-verified incl. registry-level checks)**:
**Apache Ossie (incubating, née OSI)** — spec 0.1.1; physical source
paths REQUIRED in the model; metrics = per-dialect SQL strings, NO
neutral form (nothing to adjudicate in-format, by construction);
validation = schema conformance only; Query API = working-group vapor;
no product ships native import/export (Jul 2026); custom_extensions =
the verdict slot for our export. **Bounded absence (the importer
wedge's founding sentence)**: nothing verifies an interchanged semantic
model AGAINST DATA — closest is MetricFlow's executability checks
(which do include one true refusal behavior: unsafe re-aggregation at
query time — candor noted). **Arrow**: Flight carries opaque
app_metadata — capability exists, epistemic VOCABULARY does not (the
wire row's founding sentence). **Substrait — complete picture**:
adoption clusters in the composable stack (DataFusion both ways, DuckDB
extension, Acero/Velox consume, Ibis/Isthmus produce, ADBC carries
plans); substrait-validator is STRUCTURAL only — with PlanCompiler and
the ES verifier family, every validation layer found stops at
structure; obligation B is absent across all three wire-format worlds.
**semstrait** (verified by registry probe): the only semantic-model→
Substrait bridge, pre-release — closest architectural neighbor yet
(grain-aware routing, "anchor" BFS joins, I8 "manifest is
planner-complete" = sufficiency-adjacent intuition as unproven
invariant) — and its additivity resolver is a v1 STUB: the reinvention
reached the measure algebra and stopped. Its carrier pattern is OUR
transport answer: semantic cargo as AdvancedExtension under a
namespaced URN, ignorable by foreign engines — certified plans travel
as urn:columna:certificate:v1. Its AggregateRole tags
(SemiAdditiveInner, FanoutDedup) are fragments of family law as
ANNOTATIONS where we have LAWS — the field keeps discovering the wall
and marking it with signs; the signs are not the wall. **The P-IR ×
Substrait mapping study is READY TO DRAFT**: entry mechanism, consumer
targets, validation gap, carrier pattern, and the lowering shape
(meaning-nodes compile to compositions of container-Rels; the
certificate extension carries what the lowering means).

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

## 7b · BEAT 1 — COMPLETE (all six deliverables; branch merged via PR #110)

**The seam — FIRST CERTIFICATE**: 56 comparisons, 0 disagreements; separate
BFS bodies over separate edge collections (non-vacuity established
structurally); tamper-restore negative control baked into the artifact;
perimeter stated: covers the two traversals including across the
projection copy — the upstream parse is outside. No published precedent
(per the sweep). **IR closure**: CLOSED over the executable corpora — 33
served asks across four suites reported separately, zero ninth-node
candidates, all eight nodes observed in the wild; rank: UNFALSIFIED, not
proven. **Attack B**: numbers VERIFIED 12/12 + ratio; faithful half
ENGINE-EXECUTED (aov, coincidence-checked); unfaithful half NOT
EXPRESSIBLE from the ask surface (F1, planner.py:371 single-level input
anchors) and EXECUTED at native IR layer from the engine's own primitives
(engine_modified: false) — one changed input_grain argument, 21% delta.
Doctrine coin: no ask can be unfaithful to itself; unfaithfulness lives
only in the gap between plan and ask — the kernel begins where the
grammar's protection ends, at the searcher's channel. **Class A pair**:
frozen — two lawful served plans, ONE differing field
(COLUMN.measure_ref); the out-of-domain refusal exhibit beside it: two
obligations, two different deaths. **Class C — ESTABLISHED (flagship)**:
natural-coincidence audit first (exactly one: G11 touch≡primary — ROBUST,
hence useless; lemma: coincidence-fragility is a requirement of the
M₀→M₁ protocol, not an accident); minted fixture route: M₀ = touch ≡
primary on EVERY row; M₁ = one added row (P0022→G06) → ONE cell diverges,
+69285.46 — same outputs, different denotations, one row apart.
**P-BLIND**: invariance HOLDS for values and semantic disclosures; F5
found a mechanical cache annotation ("served from cache",
engine.py:131,488, version-checked, every disclosure TRUE) riding the
semantic channel under the semantic name FRESHNESS → reclassified: a
channel-taxonomy defect, rowed OF-24 — and promoted to design law: the
certificate's disclosure projection carries TWO channels (semantic:
call-invariant, P-BLIND's jurisdiction · mechanical: legitimately
variant). **Findings ledger F1–F5** + two instrument corrections on
record (the confound proverb: "the confound wears the hypothesis's
clothes — rotate order before attributing"; digest-of-rounded retired
for structural-exact / numeric-tolerant). The beat's epitaph, CC's line:
*the beat's two best moments were both refusals.*

## 7c · EXECUTED: Attack B, against the shipped Cascadia warehouse

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
misattribution is logged as accidental evidence for C1. ## 9 · THE FORK — the derivational alternative (ratifier's contention, 2026-07-29)

**Status: the program's central open question. Both branches held at claim
rank; no beat proceeds on the contested items until ruled. Origin: the
ratifier's design contention, raised after reading v0.9 end-to-end, and
sharpened rather than weakened by every correction of the day (the
notation catch, WP-GRAIN, WP-NAME — all were the language completing
itself).**

### 9a · The contention, stated precisely

The architecture has TWO gates, not one. **Gate 1 — the grammar**: what
can be UTTERED (the envelope surface; generated from the model; classic
accidents inexpressible; teaching refusals). **Gate 2 — the derivation**:
how an utterance BECOMES a plan. Today the plan is constructed from the
ask's parse, and the positional structure is load-bearing: each
syntactic slot (series, pin, anchor, WHERE) drives exactly one assembly
site, so each parse position is a PRE-DISCHARGED proof obligation.
Faithfulness (plan ⊨ ask) holds BY DERIVATION — the way a compiled
program matches its source — and never needs checking because it is
never at risk.

The Open Planner (as designed v0.1–v0.9) keeps gate 1 fully intact —
every request enters as FrameQL, parses, and escalates only on a
plannable-gap refusal; nothing bypasses the language — **and opens gate
2**: the searcher's plan is not derived from the parse but freely
composed in IR space, merely CLAIMING to implement the ask, with
obligation B posted to verify the claim post-hoc. The contention: this
trades faithfulness-by-derivation (solved, shipped, executed daily) for
faithfulness-by-verification (obligation B — which the program's own
sweep found NO ONE has ever built). Compiler form: not "users submit
machine code with no source," but **"users submit source, and a stranger
hands the loader a binary alleging to be its compilation, with no
compiler in between"** — translation validation's hard case, adopted
voluntarily.

### 9b · The surplus-space argument (the fear, made formal)

Let P = well-formed IR plans, A = legal asks, D(A) ⊆ P = the derived
region. F1 proved the inclusion strict. Partition the surplus P \ D(A):

- **(i) Unlawful plans** — violate model law; obligation A rejects;
  cheap; uncontested.
- **(ii) Lawful plans whose denotation NO ask expresses** — Attack B's
  home (pre-WP-GRAIN). Under the design, B rejects these BY DEFINITION
  (faithful to no ask) — but that guard is exactly the unbuilt object;
  today nothing stands between region (ii) and execution except a
  research program.
- **(iii) Lawful plans denotationally EQUAL to a derived plan but
  operationally different** — alternate transports, spend orders, novel
  strategies for the SAME meaning.

**The value-concentration observation**: the open channel's entire
legitimate payoff lives in region (iii) alone — the surplus is ~all
rejection surface — and region (iii)'s admission check is certified
denotational equivalence, the HARDEST object in the program (and the
fourth nothing-found region of the prior-art sweep). The channel's value
is smallest exactly where its machinery is hardest. F1 re-read under
this lens: not a limitation the IR transcends but THE GATE WORKING.

**Region (ii)'s honest disposition is language growth, not plan
admission**: when a computation out there proves WANTED, grow the
grammar (WP-GRAIN migrates Attack B's arithmetic into D(A),
faithful-by-utterance). The gate grows; the bypass never has to. The
recall ledger is, on this reading, the derivational branch's roadmap.

### 9c · The lineage split (what systems practice chose)

Forty years of untrusted-low-level-code answers: **PCC** (producer ships
the proof — certifies encoded properties, NOT source-faithfulness);
**typed assembly** (the low language carries the types; checking stays
local); or **don't ingest foreign low code — search above the IR**. The
derivational alternative is the third answer in our vocabulary:

- The searcher becomes an **advisor inside the derivation**: it proposes
  CHOICES where derivation has genuine freedom — transport routes,
  face-spend orders, strategy selection — the entire region-(iii) prize,
  each choice a cheap LAWFULNESS check, none denotational (the
  denotation is fixed by the parse before the advisor speaks).
- It proposes **ask-rewrites through the front door** (the clarify
  channel — gate-respecting by construction).
- It proposes **new derivation rules as code**, entering through review
  like all code — probability admitted to search over DERIVATIONS,
  never to adjudication, doctrine intact on both branches.
- The kernel shrinks to obligation A plus rewrite-conservation
  (⟦P′⟧=⟦P⟧ within the TCB) — both tractable; the seam certificate
  already evidences the discipline.

### 9d · What survives either ruling / what is contested

**Fork-neutral (unaffected, banked)**: the seam certificate (certifies
today's dual derivation — MORE valuable under 9c); the extracted IR
(the internal object is real regardless of who may author one); C4 /
describe-sufficiency (advisors need it too); Attack B's verified numbers
(the demonstration of what an open channel WOULD admit — evidence for
both branches); the F-ledger; Class C (output observation cannot
establish faithfulness — true under any architecture); the two-channel
disclosure law; the doctrine sentence itself.

**Contested (paused)**: the open ingestion channel; obligation B as
gatekeeper of foreign plans; Substrait IMPORT (export of certified
plans survives; ingestion inherits the full contention).

### 9e · The decision beat (proposed)

Race the architectures on ONE recall-ledger row, receipts against
receipts: implement the same missing capability twice — (a) as a
derivation-rule extension (branch 9c), (b) as a foreign-plan
certification (branch v0.9) — and measure: implementation cost,
verification surface added to the TCB, failure modes' loudness, and
what each leaves reusable. Let the loop decide with execution what is
currently argued with lineage. Candidate row: coordinate-WHERE (OF-13
class — the Meridian ask). The ruling on which branch the house builds
FIRST is the ratifier's; this section is its decision document.


### 9f · THE RULING (ratifier, 2026-07-29 — same day as the contention)

**Ruled: the derivational branch is adopted. Open ingestion is SHELVED
indefinitely** — not refuted; shelved, its market bounded by the
ratifier's own three-move narrowing (surplus-space → parse-but-don't-
derive band → band contents auditable) and priced against an unbuilt
obligation. The searcher-as-advisor (9c) is retained as derivation's
future accelerator. Obligation B's THEORY is retained in full — see §10:
it re-enters outbound as the conservation obligation of certified
lowering (plan ⊨ ask inward became ⟦lowered⟧ = ⟦P⟧ outward — same
discipline, tractable because it runs per-rule inside the TCB against
our own oracle, not per-plan against strangers).

**Cancellations, recorded** (first-principles audit, ratifier-forced):
the kernel-prototype beat AS SCOPED (obligation A over incoming plans) —
cancelled; its organs (law-replay as checks) rebuild inside
lowering-verification. The §9e race — moot; ruled without it. The
ledger-row audit as fork evidence — cancelled (survives only as roadmap
hygiene). Foreign-plan ingestion in any transport, Substrait included —
shelved with the channel.

**What the fork episode banked**: a research question opened in public
(v1.0), evidenced by execution (beat 1, v1.1–v1.3), narrowed by its own
ratifier's adjudication, and closed by argument in eleven days — the
loop's constitution demonstrated on its own flagship. The contention's
geometry (two gates; the surplus partition; value-concentration) is
retained as standing analysis: it is why the outbound direction is
sound, not merely chosen.

## 10 · THE OUTBOUND TURN (the program's direction from v0.11)

**The vision, ruled**: certified Columna plans lowered onto container
plans (Substrait as the lingua-franca route), executing on any
consuming columnar substrate — DuckDB, DataFusion, Velox, Acero — with
the certificate riding as namespaced cargo (urn:columna:certificate:v1,
the carrier pattern proven by semstrait's annotations) and the judge
never compiling. One sentence: **every Substrait-consuming engine
becomes a Columna SUBSTRATE, never a Columna server** — the plan
language can be given away because verdicts cannot be; annotations
describe a plan, a certificate vouches for one.

**MAP-2 — the virtual-engine track** (deployment form of the turn):
(a) certified pushdown lowerings — per-node, per-backend or
via-Substrait; acceptance = the seam-certificate method generalized;
the Polars engine is the PERMANENT REFERENCE ORACLE every lowering must
match; (b) discovery mode — the adjudicators run in reverse propose
candidate manifolds from a live warehouse; machine proposes, HUMAN
DECLARES, data adjudicates — candidates are never truth; (c) plan-
materialization cache — certified plans as warehouse materializations
keyed by ask shape (P-ECON's home). Custody law, absolute: plans
execute under the wire that certified them; backends serve leaves (and,
when lowered, run OUR instructions inside the TCB); moods and
disclosures mint only at our door; the answer never returns from
anywhere the certificate didn't watch.

**Beat 2 — the mapping study, reframed outbound** (charter to follow as
its own artifact): the eight meaning-nodes → compositions of
container-Rels; which lowerings are per-rule certifiable; what the
certificate cargo carries (two-channel disclosure law included, per
F5); where engine drift (BFT-documented) forces per-backend proof;
Substrait extension profile sketch. Deliverable: the design document
MAP-2(a) builds against.

**What beat 1's assets become under the turn**: the reified IR = the
thing lowered; the seam certificate = the acceptance instrument of
certified lowering; Class C = the standing theorem that output testing
can never replace certifying the computation (the sentence said to
every engineer who proposes diffing results against DuckDB); the
channel-split law = the certificate's disclosure schema; Attack B = the
demonstration of what any uncertified path admits. Nothing banked is
stranded; everything points outward.


## 11 · BEAT 2 — COMPLETE AND CLOSED (the outbound turn, executed)

**Chartered 2026-07-31 (map2_mapping_study_charter v0.1→ratified 1.0);
closed same week by ratifier ruling with all §5 acceptance criteria met.
Governing artifacts: the charter; D2 cargo schema v0.2
(map2_certificate_cargo_schema_v0_2); PRs #126–#128.**

**D1 — the lowering table, COMPLETE.** Left column 100% attested by
execution (observer over Polars' own methods, 9 cold asks + 2 minted
WHERE asks after the CARVE gap was closed at root cause — FrameQL WHERE
is SQL-passthrough; single-quoted literals; DOC-1 manual note shipped).
**Zero ninth-node candidates — IR closure re-confirmed one layer below
beat 1.** Verdicts adjudicated: TRANSPORT and monoidal REDUCE
CERTIFIABLE-PER-RULE (with mean via (sum,count) decomposition —
"fertile/mule/holistic" per the published theory's state
classification); CROSS arithmetic per-shape with **disclosure minting
NOT DELEGABLE** (custody law); sketch-distinct and exact median/mode
NOT-LOWERABLE at v1. The table's thesis exhibit, preserved verbatim: *a
bare JoinRel on a non-functional key silently fans out; the edge's
corroborated-functional verdict is invisible to Substrait and is
exactly the cargo the certificate exists to carry.*

**D2 — the certificate cargo schema, v0.2 ACCEPTED by its own test.**
urn:columna:certificate:v1; two channels under F5's law with the
negative rule normative (nothing call-variant on the semantic channel,
V3 machine-checked by byte-diff of two emissions); S6 edge attestations
MANDATORY per TRANSPORT (V1); §4b defines the RULE CERTIFICATE — the
per-(rule × backend band) object M1 references, content-addressed by
rule identity (rule × band × perimeter), proof-runs as attached
evidence so re-proving never flaps a ref; V4: no cover, no lowering —
the plan falls home, never "lowers with a warning." Acceptance test
passed as stated: C2 emitted conformant NATIVELY; C1 re-emitted to
match.

**D3 — the oracle harness, PERMANENT.** Polars the reference oracle;
beat-1 instruments (structural-exact / numeric-tolerant, tolerance per
comparison); tamper-restore negative control demonstrated in BOTH
pilots (three break modes and a wrong-grain mean, each failing on every
cell). Consumer-agnostic: generalized from bench to Acero unchanged.

**D4 — TWO conservation certificates, the program's first.**
**C1** (TRANSPORT-shaped sum → Substrait 0.46.0 → Acero): N=16,548,
zero disagreements, worst delta 2.6e-10 vs 1e-6 tolerance; Attack B
stress: the unfaithful lowering self-consistent with the unfaithful
oracle AND distinguishable from the faithful one by up to 24.98/month —
*output agreement would not have saved it; only plan ⊨ ask does* (Class
C operating at the lowering layer, as chartered).
**C2** (full spine: WHERE-carve as FilterRel + mean via (sum,count) +
ProjectRel divide): N=509, zero disagreements, worst delta 5.5e-12;
V1/V3/V4/V5/V6 all pass on native emission. **Amortization
DEMONSTRATED LIVE**: C2's M1 references both rule certificates — the
new mean rule plus C1's sum rule inherited for its inner sums (S5
`inherited` obligation). A plan certificate points, never copies.

**Rule certificates minted (first in existence):**
rule_c1_transport_shaped_sum × Acero; rule REDUCE-mean × Acero — both
filed with the published adjudication record; every future M1 points at
these digests.

**D5 — rows, with one correction folded at ratifier word:** BLOCK-1
re-diagnosed — NOT egress (the 403 was a CDN error page misread as
firewall; curl + throwaway venv falsified it): the substrait extension
is unpublished for DuckDB 1.5.5/1.3.2, published for 1.1.3 — resolved
by consumer version pin duckdb==1.1.3 (inside core's <2.0 ceiling),
isolated venv, no environment change ever needed. First live instance
of M2's backend version band. Remaining rows: sketch/median-mode
NOT-LOWERABLE; CROSS mint non-delegability; Substrait 0.46.0 +
producer proto pins.

**BEAT 3 — SCOPED, NOT STARTED (charter to follow from the desk):** one
beat, two seams. (a) **C3, the CROSS-bearing pilot** — a stay-home face
crossing feeding lowered work: S7's first exhibit, S9's stay_home
boundary in a mixed plan, the vertical seam (what may leave home)
tested in practice. (b) **the DuckDB second-consumer inheritance test**
— both rule certificates offered to a second engine under the unchanged
harness: the horizontal seam (what transfers between substrates), V4
answering with receipts. UN-GATED: no environment dependency (per the
BLOCK-1 correction). Custody law and §7 walls of the beat-2 charter
carry forward unchanged.

**Rounds 6–9 (RG)
delivered and adjudicated; citation accuracy 7/7 on falsifiable checks
(incl. Apache-Ossie incubation and the semstrait registry probe — for
tiny artifacts, ask the registry, not the search index). Reviewer
transport: the file channel, fixed. Beat 1: COMPLETE — the artifact gate is SATISFIED. Fork RULED at v0.11. Beat 2 COMPLETE
AND CLOSED at v0.12 (§11) — the outbound turn has receipts: two
conservation certificates, two rule certificates, an accepted cargo
schema, a permanent oracle harness. Beat 3 scoped (§11 tail).** RG stands by — no search regions currently open; the loop
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
