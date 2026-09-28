# ToD v8.0 development journal

**Candidate material. Not authoritative publication text, not adopted, carrying no authority.** Opened by Claude
at Huayin's direction, 2026-09-25, when the work was designated the candidate architecture for **v8.0** rather
than further amendments to v7.1.

**Predecessor entries carried forward.** A.3, A.6, and **A.9–A.14** were drafted against a v7.2 successor and now
belong here unchanged in content: A.3 family splitting · A.6 continuation is not formation · A.9 R1′ single
authority · A.10 R1″ identity over resolved semantics · A.11 retirement of contribution multiplicity · A.12
governed point selection versus population-changing restriction · A.13 the determination-clause model · A.14
family domain as derived. A.1 and A.2 remain **withdrawn**.

Entries below are new from the reconciliation pass
([`tod_v8_0_candidate_reconciliation_v0_1.md`](./tod_v8_0_candidate_reconciliation_v0_1.md)).

---

## B.1 One family, one universe — an axiom the corpus relies on and never states

`cross-universe` has **zero occurrences** in v7.1; §4's nine-row family-law contract has **no universe row**;
Appendix B.2's family definition omits it. Yet **\(\Sigma(F)\) contains *"the governed universe"***, refinement
is defined only *"for anchors of the same universe"*, and a reducer *"contracts a strictly finer anchor to a
coarser one **within a universe**."*

> **The invariant is presupposed by the machinery and asserted nowhere. v8 should state it.**

It earns its place three times: it makes `F@A` resolvable at all (anchor identity is universe-relative); it lets
a material measure **drop \(U\)** (B.7); and it makes *one expression, one universe* a **consequence** rather
than a second rule (B.5).

## B.2 Event and spine are forms of the existence law — and this is already published twice

ToD §2.1.1: *"**Event-like and spine-like domains are forms of the existence law, not additional top-level
ontological kinds.**"* Statistical Bridge §3.1: *"**But event and spine are existence forms, not the whole
Theory-of-Data universe ontology.**"* The Bridge never uses the term *universe type*.

**A third published paper does type them** — `w-missingness-has-a-universe` §4.3, \(U=(\kappa,A_U,P_U)\) with
\(\kappa\) *"the universe type."* **That is the tension, and it is one of level, not of content.**

And the estate has **already ruled**: the 2026-09-15 universe-constitution ruling §7 holds
`events | spine | product | registry` as *"compatibility vocabulary whose eventual standing remains to be
determined"* and forbids promoting them into \(\lambda_U\).

> **v8 must not ratify a universe-type taxonomy.** The corrected principle: **the form of the existence law is
> irrelevant to a universal analytical law once its premises are established, and essential to establishing them
> and to governed passage** — because it determines what a point's absence means.

## B.3 The eight-state absence account, and the Contract Calculus composition gap

Eight states: nonexistent · unresolved existence · ineligible · unresolved eligibility · non-participating ·
participating-with-zero · participating-but-unsupported · known-empty contributing fiber.

**Contract Calculus \\(G_1\\) has four source-point states, and falls short in two different ways:**

- **no slot** for *unresolved existence* or *unresolved eligibility* — the §15.4 embedding is **total on \(P\)**
  and must know which case holds;
- **one case carries two states** — CC has **no participating domain distinct from eligibility**, so
  \(a\in E\setminus S\) covers both *"the law did not consume this point"* and *"the law consumed it and the
  value is unestablished."* **Under `Complete`, a merely non-participating eligible point is demanded as an
  observation.**

**Characterized, not repaired.** CC's four states are adequate exactly where \(D=E\), which is what its fragments
address and more than it claims (*"the **smallest** population-and-partiality extension"*; a complete partiality
calculus marked **"Not claimed"**). **ToD's \(D\) is the concept CC lacks; ToD's §2.3 is the standing account CC
lacks. Each paper is complete on its own terms; they have not been composed.**

**And the Bridge's §5.1 layering — *occurrence ≠ recording ≠ value observation* — must not be folded in.** It is
three kinds of evidence failure **underneath** state 7, not three more states.

## B.4 `identity_at` withdrawn; analytical lineage does the work

**ToD is explicit that \(A\) is not in \(\Sigma(F)\)** and that constitutive parameters *"remain inside \(F\)…
They do not become additional current anchors of \(F@A\)."* **There is no published measure identity, and v8
should not mint one.**

The distinction needs three terms and the third is published: **family identity** \(\Sigma(F)\) · **the location**
\(A\) · **the resolved determination at \(A\)**, which is what **§3.7's analytical lineage** records. The only
addition v8 makes is that **lineage is per-measure, not per-family** — which §3.7's own *"constitutive ancestry"*
supports, since ancestry at a coarse anchor and at the grounding anchor are not the same ancestry.

**And the theorem needs no new identity object at all**, because §3.9 already supplies the mechanism:

> **Adding an identity-bearing clause yields a successor family identity (§3.9). Existing constructions reference
> the predecessor and are therefore unaffected.** When a namespace version re-points the name at the successor,
> a construction re-resolved through that name denotes the same quantity **iff the successor's determination at
> the bound anchor agrees with the predecessor's.**

**Succession plus name resolution — both published — and the inertness result holds under either reading of the
still-open question whether a purely extension-widening addition is a succession or a refinement.** That
robustness is the point: the theorem does not depend on settling it.

## B.5 The three jurisdictions, and a corpus tension they resolve

**Composition (one universe) · assembly (many universes, one anchor) · passage (between universes).** All three
are already in the estate; what is missing is the sentence that relates them.

- **Composition** — Frame-QL's §2c: *"Every column expression evaluates inside **exactly one** universe… a
  `cross_universe` **category error**, not a hedged answer."* And *"every ascription is implicitly
  `expr @ (a, U)`."*
- **Assembly** — *"the frame **juxtaposes** them — separate series, each evaluating in its own universe, standing
  together at a shared anchor"*; vNext §2.2: *"Co-location in one frame does not collapse those identities."*
- **Passage** — Bridge §4.4: *"establishing a measure on an independently existing spine is a **cross-universe
  attribution or construction. That crossing must state its own contract.**"*

> ⚠ **The tension they resolve.** Reference/framework manuals §9.5 call combining different universes *"a
> **legitimate** combination, served with its permanent asymmetry disclosed"*; the Frame-QL Manual §2.4–2.5 calls
> it a **hard error**. **Both are right — §9.5 describes assembly, §2.5 prohibits composition — and no document
> says so.** v8 should supply that sentence.

**Also recorded:** a Frame-QL query is scoped to **one Manifold**, never one universe; **there is no way to name a
universe in a query**; and the v7.1 acceptance suite and joint-consistency ledger contain **zero occurrences of
"universe"** — whatever v8 says here will be the first time the question is tested.

## B.6 Cross-universe passage is a v7.1 regression

v6.1 carried the requirement in full — *"Cross-universe analysis therefore requires an explicit governed
relation, reconciliation, or transfer law… identify the source and target universes, state how analytical points
correspond… and specify which measure identity and contribution contracts survive the transfer."* **v7.1 has zero
occurrences of `cross-universe` and one clause on `universe passage`, deferred to neighbouring work.** The
2026-09-15 ruling independently lists universe passage as **still open**. **v8 should restore it.**

## B.7 The material-measure boundary

**\((U,A,V)\) is one field too large.** A material measure is a materialization of \(F@A\); with \(F\) as the
object's identity, **\(U\) is derivable from \(F\)** by B.1. **The carried content is \((A,V)\)** — and if a
material measure genuinely needed \(U\) independently, B.1 would be false.

**`NA` has a published home**: it is Contract Calculus §15.4's third embedding case \(a\in P\setminus E\),
materialized — contributing nothing **and not counted**. A reducer meeting `NA` must read it as a **domain fact,
not a value**.

> ⚠ **`NA` is sound only where eligibility is *resolved and negative*.** It is a **positive analytical claim**;
> writing it where eligibility is merely *unresolved* manufactures a positive fact from silence — **the same
> error pattern as structural zero**, which is already drifting in the implementation corpus.

**Unresolved existence and unresolved eligibility are not representable in \((A, V\in X\cup\{\mathsf{NA}\})\) —
and need not be, because both are *standing* facts** and belong outside with support. **Nothing is irreducibly
missing from the value representation.**

**And the materialization criterion is sharper than composite/non-composite.** ToD §5.2 — MEAN's scalar *"loses
the weight required for exact continuation"*; ToD §11.3 — *"Displayed LAST values need not determine
continuation."* **LAST is not a composite and fails the same test.**

> **A family may be materialized as a scalar exactly where its displayed value is a sufficient basis for its own
> admitted continuations.** SUM, COUNT, MIN, MAX yes; **MEAN and LAST no.** A scalar may still be stored as an
> **answer**; what it may not be is a **basis** — ToD §10.7: *"A stored answer and retained sufficient state are
> different claims."*

## B.8 Interval, range, point-in-time and membership are not kinds of anything

`interval`, `duration`, `point-in-time`, `range` — **zero occurrences each in ToD v7.1.** They are **not**
universe types and **not** geometric structures. **Interval and duration are semantic value types** (§5.7:
*"Internal value structure is not analytical location"*); **point-in-time is the absence of a time-crossing
clause**; **membership is a governed structural construction** that may *produce* a universe instance (Appendix
D) — never a type.

**This is the largest single reduction in independent assumptions the candidate achieves.**

## B.9 Determination closure

> **Family determination may close under composition only where universal analytical law establishes the required
> composition/interchange premises.**

ToD §11.2 states the negative — *"an interchange law would need its own premises"* — with a worked counterexample.
**The positive rule is unstated and v8 must add it**, together with the distinction between **clause-level
incoherence** (a declaration defect) and **path-level disagreement** (silence), without which closure breaks
Balance in any ragged ledger.

**Rectangularity is derived, not declared.** Its two inputs are **universe geometry** — ToD §2.1.3's *"its image
need not be the full Cartesian product"* — and **the participating domain**, which comes from the resolved source.
**No third input; no family field.** And since \(D\) is selected by the law **and the resolved request**,
**rectangularity can be request-dependent**, so an interchange licence must be checked against the resolved \(D\).

> ⚡ Worth recording: *the image need not fill the product* is **the same fact** that makes a spine sparse and
> that blocks SUM/LAST interchange. **One geometric fact, two consequences.**

## B.10 Open, and deliberately not settled here

1. Whether a purely **extension-widening clause addition** is a §3.9 succession or a refinement. **B.4 shows the
   inertness theorem holds either way**, which lowers the urgency without closing it.
2. The **three LAST/SUM decisions**: composition closure; the incoherence/disagreement distinction; whether
   rectangularity is universe-declarable (now with B.9's request-dependence refinement).
3. **Universe passage's contract** — restored as a requirement (B.6), not designed.
4. The **law of a non-catalogued construction** — the declaration language has no production for defining a law,
   which is the correct place for it to stop.
5. The **\(\kappa\)-versus-existence-form** level tension with `w-missingness-has-a-universe` (B.2).
6. The **CC/ToD composition gap** (B.3) — characterized, not repaired.
7. Two **documentation defects independent of v8**: Reference Manual 5e §9.4's stale query-level `ON`, and the
   §9.5-versus-§2.5 tension (B.5).
