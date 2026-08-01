# Beat 2 Charter — The Outbound Mapping Study
### Certified lowerings of Columna plans onto container plans (MAP-2a foundations)

*Charter v0.1 · 2026-07-31 · desk-drafted for ratification · executes under
the Open Planner program as redirected at fork ruling §9f/§10 (fork doc
v0.11) · supersedes nothing; founds beat 2.*

---

## 1 · Mandate and lineage

The fork ruling adopted the derivational branch and turned the program
outbound: **certified Columna plans, lowered onto container plans, executing
on any consuming columnar substrate — the certificate riding as cargo, the
judge never compiling.** This study is the turn's first artifact. Its job is
not to build the lowering; its job is to determine, with receipts, *what a
certified lowering is* — node by node, rule by rule — so that MAP-2(a)
builds against a ratified design instead of an intuition.

Lineage, so nothing is re-argued: the reified eight-node IR (A1, beat 1);
the seam-certificate method (beat 1's first certificate — the acceptance
instrument this study generalizes); Class C (the standing theorem that
output agreement can never substitute for certifying the computation — the
reason this study exists at all); F5's two-channel disclosure law (the
certificate's schema constraint); the carrier pattern (semantic cargo as a
namespaced Substrait AdvancedExtension, ignorable by foreign consumers —
proven in the wild); the custody law (absolute, restated in §7); and the
vantage findings of rounds 8–9 (substrait-validator is structural-only;
every consumer of consequence is columnar; the composable stack built the
mouth).

## 2 · The objects

**The plan.** Eight meaning-nodes, extracted from the shipped engine:
ANCHOR · CARVE · COLUMN · TRANSPORT · CROSS · REDUCE · ALIGN · DERIVE.

**The target vocabulary.** Substrait's container-Rels (ReadRel, FilterRel,
ProjectRel, AggregateRel, JoinRel, SetRel, SortRel, FetchRel), pinned to
one Substrait version for the study's duration (the pin is part of D1's
header; drift across versions is a finding, not a surprise).

**The lowering.** For a node (or composition) N, a lowering L(N) is a
composition of container-Rels plus cargo such that **⟦L(N)⟧ = ⟦N⟧** on the
declared model — the conservation obligation, obligation B's outbound twin,
checked per-rule inside the TCB against our own oracle, never per-plan
against strangers.

**The certificate.** `urn:columna:certificate:v1`, carried in
AdvancedExtension. The cargo does not make a foreign engine lawful; it
records that lawfulness was already adjudicated upstream, and it carries
what the lowering *means* — so a Columna-aware reader can audit, and a
foreign engine can ignore.

## 3 · The study's questions

**Q1** — For each of the eight nodes: what operations does the shipped
Polars engine actually perform? (Attested by execution — CC's pre-charter
trace is this column; nothing in D1's left column may be written from
memory.)

**Q2** — For each node: what container-Rel composition implements the same
denotation, and what does the composition *lose*? (The loss column is the
study's honest center: a JoinRel does not know it is a corroborated-edge
transport; the certificate must carry exactly what the Rels cannot.)

**Q3** — Which lowerings are certifiable *per-rule* (prove once per
backend, reuse forever), which only *per-plan-shape*, and which nodes are
**not lowerable** — they stay home, and the pushdown boundary lands there?
Expected hard cases, named now so the study cannot quietly skip them:
CROSS (face law and reconciliation arithmetic have no Rel vocabulary),
REDUCE under non-monoidal aggregators (mean's sufficient-statistics
decomposition must lower as (sum, count) — the mean-of-means theorem is a
lowering constraint, not just an attack), and sketch-based distincts
(engine-specific state; likely NOT-LOWERABLE at v1).

**Q4** — What must the certificate carry? Schema draft under the
two-channel law: the semantic channel (call-invariant: model identity and
adjudication digest, the ask, the plan, obligations discharged with the
laws named, the disclosure projection) and the mechanical channel
(legitimately variant: lowering attestation, backend identity, oracle-run
reference).

**Q5** — Where does engine drift force per-backend proof? (BFT exists
because function semantics diverge across engines; the study identifies
which of our lowerings touch drift-prone functions and therefore cannot
inherit a sibling backend's certificate.)

## 4 · Method

**D1 — the lowering table**, one row per node (plus rows for the two
attested compositions: the TRANSPORT-shaped join-and-regroup and the full
CARVE→COLUMN→TRANSPORT→REDUCE spine). Columns: *node* · *Polars operations
(attested, from the trace)* · *proposed Rel composition* · *what the Rels
lose* · *cargo required* · *certifiability verdict* — one of
CERTIFIABLE-PER-RULE / CERTIFIABLE-PER-SHAPE / NOT-LOWERABLE(stays home),
each verdict with its reason in one sentence. An empty cell is a finding;
a guessed cell is a violation.

**D2 — certificate cargo schema v0.1** (`urn:columna:certificate:v1`),
drafted to Q4's split, with one negative rule stated in the schema itself:
nothing rides the semantic channel that can vary with call count, backend,
or attempt — F5's lesson, promoted to schema law.

**D3 — the oracle protocol**: the seam-certificate method generalized.
Polars is the PERMANENT REFERENCE ORACLE. For a candidate lowering:
execute the plan natively; execute the lowered form on the consumer
(DuckDB via the substrait extension is the study's first consumer, per the
round-trip verification); compare under the beat-1 instruments
(structural-exact for shapes, numeric-tolerant for values, tolerance
stated per comparison — the digest-of-rounded instrument stays retired);
require **N comparisons, zero disagreements**, with a tamper-restore
negative control baked in (one deliberately broken lowering must FAIL, or
the harness is not testing); state the perimeter of what the certificate
covers in the certificate itself.

**D4 — the pilot, the beat's execution evidence**: one lowered plan — the
TRANSPORT-shaped composition at minimum, the full spine if it falls
cheaply — round-tripped through Substrait, executed on DuckDB, and
oracle-compared under D3's protocol, producing the study's first
conservation certificate. Attack B's fixture is the pilot's stress case:
the lowered faithful plan must agree with the oracle to tolerance, and a
lowered *unfaithful* variant must be distinguishable — Class C's lesson
applied to lowerings: we certify the computation, never the coincidence of
its outputs.

**D5 — the ledger rows**: every NOT-LOWERABLE verdict, every deferred
corner, every version-pin risk becomes a dated row. A study that finds
nothing unliftable has not looked.

## 5 · Deliverables and acceptance (falsifiable)

The beat is DONE when: (1) D1 is complete — all eight nodes plus the two
compositions classified, no empty verdicts, left column 100% attested by
the trace; (2) D2 exists and passes the F5 test (no variant fact on the
semantic channel, demonstrated by inspection against the pilot's two
runs); (3) D3 is written and its negative control demonstrated (the broken
lowering fails loudly); (4) D4's pilot certificate exists: N ≥ 30
comparisons, zero disagreements within stated tolerance, DuckDB consumer,
perimeter stated; (5) D5's rows are filed. Failure modes that count as
*results, not misses*: a node proven NOT-LOWERABLE with its reason; a
drift case forcing per-backend proof; a Substrait expressiveness gap
requiring cargo that was expected to be structural.

## 6 · Division of labor

**Desk**: this charter; D2's schema draft; adjudication of D1's verdicts;
the fold into fork doc v0.12. **CC**: D1's left column (the trace —
already tasked, pre-charter), D1's Rel compositions proposed for desk
adjudication, D3's harness, D4's pilot end-to-end, D5's rows as found.
**Ratifier**: this charter's word; the verdicts that change custody or
scope; D4's acceptance.

## 7 · Scope walls (what this study is not)

**No foreign-plan ingestion** — ruled and shelved; nothing in this study
reads a plan we did not derive. **No whole-plan answer delegation** — the
custody law is absolute: lowered work executes as our instructions inside
the TCB; leaves and certified subtrees may run on the substrate; moods and
disclosures mint only at our door; no answer returns from anywhere the
certificate did not watch. **No discovery mode** (MAP-2(b), later). **No
production wiring** — this is a study with one pilot; releases come after
ratified verdicts, through proposal-first, as always. **No new claims of
completeness** — the normal-form conjecture stays a research target; this
study classifies, it does not prove.

## 8 · Risks, named

Substrait version churn (mitigated: pin + finding-not-surprise); the
DuckDB extension's fidelity limits (the round-trip verification bounds
this before D4 commits); tolerance policy disputes (settled by beat-1
instruments, stated per comparison); scope creep toward building MAP-2(a)
inside the study (the walls in §7 exist to be cited).

## 9 · Rank

This charter asserts nothing about the world. It defines a bounded study
whose every deliverable is checkable, whose pilot is executed or absent,
and whose verdicts arrive with reasons attached. The one standing claim it
inherits rather than makes: *an annotation describes a plan; a certificate
vouches for one* — and by this beat's end, the project will know exactly
what vouching costs, node by node.

*— the desk, for ratification. On the word, CC takes D1 and D4; the desk
takes D2 and stands adjudication.*
