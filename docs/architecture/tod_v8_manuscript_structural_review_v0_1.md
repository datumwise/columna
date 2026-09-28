# Structural and adversarial review — ToD v8.0 working manuscript v0.5

**Claude, at Huayin's direction, 2026-09-26.** Target:
`attachments/c394a7e9_theory_of_data_v8_working_manuscript_v0_5.md` — 40 sections, 1,975 lines.
Fourth adversarial pass in this line; the first three
(`tod_v8_synthesis_falsification_v0_1/_v0_2/_v0_3.md`) reviewed the synthesis at v0.3, v0.4.1 and v0.5.

**Standing.** Structural and adversarial review. **No implementation. No changes to schemas, Core, Platform,
Manifold, MEL, Frame-QL or publications. The manuscript is not rewritten.** No architecture is restarted, no
retired machinery reintroduced, no promotion mechanism invented, no establishment state turned into a codomain
value.

---

# A. Executive verdict

> **Structurally ready for revision into publication form, with one foundational blocker.**
>
> **The blocker: \(F@A\) is not indexed by its universe of analysis, and three sections need it to be.**
> §3 makes anchors partitions of \(\Omega_U\) and §30 insists geometry is intra-universe — but §5's family
> definition and §6's \(F@A\) never mention \(U\), §2 licenses free subset-universes with no bridge while §30
> requires one for exactly that act, and §24's coherence obligation is discharged by an undefined term
> (*"the same governed context"*, 3 occurrences, never defined).

This is not a request to restart the architecture. The architecture is sound and has now survived four passes.
It is a **missing index on the central notation**, and the paper already uses it informally (§15: *"a Balance
family over an Account-by-Day universe"*; §31: *"about the orders in the relevant universe"*). One decision plus
roughly a page of consequential edits.

Everything else below is repairable during editing. Two further class-1 items are a proof-statement defect in
the paper's only numbered proposition (§16) and an unhandled branch in §7's four-question decision procedure.

**On the three prior blockers:** all discharged. The §5.8 sufficiency collision stays withdrawn (§9: *"They do
**not** define analytical sufficiency"*). The totality gap stays closed (§4's semantic map, held faithfully in
every later section — see C2). And **§10.1 answers my v0.5 class-1 directly and correctly**: *"The
sufficient-basis account governs the **law-determined** route to a target. It is not the base case of
grounding."* That was the last thing I had, and it is properly resolved.

---

# B. Class-1 findings

## B1 ⚡ \(F@A\) carries no universe index, and §2 and §30 give incompatible accounts of restriction

**Earliest section: §5–§6** (the family definition and the \(F@A\) notation). **Kind: foundational
contradiction plus a missing premise.**

### The three statements that cannot all stand

**§3** makes the geometry universe-relative: *"An anchor \(A\) is a governed partition of the point domain
\(\Omega_U\)."*

**§2** then licenses restriction as a free act:

> *"A governed subset of analytical points can be constituted as a smaller universe of analysis, **carrying
> forward or restricting whatever geometry and analytical laws remain applicable**."*

**§30** says that crossing universes is not that at all:

> *"Cross-universe passage requires its own governed relationship… Such a passage may be deterministic and
> perfectly lawful. **It is still not an anchor projection.**"*

**A restriction *is* a subset universe.** So §2 says a restriction carries laws forward for free and §30 says
moving between universes needs a governed bridge with a stated conservation and loss account. These are two
accounts of one act. §16 already knows §30 is right — its post-proof remark reads *"It does not say that a
**restriction**, completion, allocation, or change of participation is merely another staging"* — and §34
punts a third time: *"A request-local filter does not silently become a new universe **unless the governing
semantics say that it does**."* Three sections touch it; none rules.

### The forcing case

Let \(U\) be all orders and \(U'\) the January orders, both carrying a Region anchor and a governed Revenue
family. Then \(Revenue@Region = 1000\) in \(U\) and \(300\) in \(U'\).

§24 states the coherence obligation:

> *"If two lawful derivations both claim the same target \(F@A\), **under the same governed context**, then
> they must agree."*

Same \(F\). Same \(A\). Different values. Either

- **the two are not the same target**, in which case \(F@A\) is incomplete notation and the universe is part of
  the target's identity — which §5's definition and §6's notation both deny by omission; or
- **they are the same target**, and the paper's central consistency obligation is violated by an operation §2
  explicitly permits.

The escape is *"under the same governed context."* That phrase occurs **three times** (§5, §22, §24) and is
**never defined anywhere in the manuscript.** As the text stands, the paper's coherence obligation — which §39
and §40 both list as one of ToD's three purposes — rests on an undefined term, and the one substitution that
would make it true is the one §5 and §6 leave out.

### Why this is foundational rather than editorial

It is the formal home of three things the corpus has already settled and v8 currently cannot express:

- **restriction versus carve** — MA §5 / Contract Calculus Theorem G1.6, *"a carve needs a distinct population
  identity."* `carve` has **0 occurrences** in the manuscript, for the fourth version running. If \(F@A\) is
  universe-indexed, carve falls out as a consequence rather than needing its own machinery.
- **the collapsed-population hazard** the Statistical Bridge §9.2 names (*"Observed rows silently become the
  target population"*). §2's *"carrying forward"* is exactly the licence that produces it.
- **`scope`** — half of the frozen `clause = source × scope`. The manuscript uses the word twice (§32, §33)
  without ever defining it (C5). A universe index is where it would attach.

### Two admissible repairs — the paper should choose one, not leave it open

1. **Families are universe-scoped.** Write the mature object as \(F@A\) *within* \(U\), make §2's subset-universe
   a **cross-universe passage under §30**, and let restriction inherit §30's obligations (what corresponds, what
   is conserved, what is lost, what claim it licenses). This is the Contract Calculus-consistent reading and it
   makes the carve rule a theorem rather than an axiom.
2. **Family identity transcends universes; its measures do not.** \(F\) is a durable identity; \(m_A\) is always
   relative to a \(\Omega_U\); *"the same governed context"* is **defined** to include the universe. Restriction
   then preserves identity and changes the measure, which matches §25's list of things that do not create a
   successor family.

Either works. **What cannot stand is §2 and §30 as written.** My own reading is that (2) is closer to what the
manuscript already does — §15 and §31 both speak of a family *over* a universe — but (1) is the one the
published neighbors expect, and the paper should say which and why.

## B2 ⚡ Proposition 16.1 is ill-formed for semigroup laws, and its load-bearing premise is not the one the proof uses

**Earliest section: §16.** **Kind: theorem/proof defect plus a missing premise.**

### (i) The quantifier admits a case the conclusion cannot express

Premise 3 is *"the contributing fibers are **finite**"* — not nonempty — and the conclusion is asserted *"for
every \(a\in A\)."* Take \(a\) with \(D\cap\pi_{I\to A}^{-1}(a)=\varnothing\). Then \(B_D(a)=\varnothing\) by its
own definition, and both sides of the conclusion are an \(\oplus\)-fold over the empty set. For a law with an
identity that is fine. For **ordinary MIN or MAX** — which §8 and §9 both insist have *"no empty identity in the
value domain"* — **both sides are undefined and the stated equality is ill-formed.**

The paragraph after the proof knows this: *"For a semigroup law such as ordinary MIN or MAX without an empty
identity, the same regrouping proof applies to **nonempty** finite contributing fibers."* But that is a remark,
not a premise, and a numbered proposition should not be repaired by the prose beneath it. **Fix: add
nonemptiness to premise 3, or restrict the conclusion to \(a\) with \(D_A(a)\neq\varnothing\) and state the
identity case as a corollary.** One line.

### (ii) The proof proves the easy half; a prose premise carries the hard half

The proof **defines** \(g_B(b)=\bigoplus_{i\in D\cap\pi_{I\to B}^{-1}(b)}g_I(i)\) and then reassociates. That
establishes that **regrouping one continuation is grouping-invariant** — true, and almost immediate from
associativity and commutativity once the partition observation is made. (The partition observation itself is
correct: projection composition puts every contributing \(i\) in exactly one nonempty contributing \(B\)-fiber.)

But **§17 uses the proposition for something stronger**:

> *"Suppose additive Revenue is grounded at Order and can be lawfully continued through Day to Month… Suppose
> direct continuation is also admitted… **If Proposition 16.1 applies, both paths establish the same analytical
> measure.**"*

That requires the **family's admitted measure at Day** to *be* the Order-continuation to Day. Nothing in the
proof establishes that; \(g_B\) is stipulated, not identified with \(Revenue@Day\). The bridge is premise 4
(*"direct and staged paths consume the same governed contributions, with the same multiplicity and formation"*),
which is stated in prose, is **never invoked in the proof**, and is doing all the analytical work. Premise 1
(*"the relevant family movements are admitted"*) is likewise never used.

**This matters because premise 4 is where every interesting failure lives** — a restriction between stages, a
different participation rule at \(B\), an allocation, a completion. The manuscript's own remark lists exactly
those. As drafted, the reader gets a rigorous proof of the trivial half and an informal sentence covering the
half that can actually go wrong.

**Fix, and it strengthens the paper:** state premise 4 formally as an identification —
\(g_B = \) the family's admitted measure at \(B\), *and* the \(B\)-level participating domain is
\(\pi_{I\to B}(D)\) with unchanged formation — then the proof can invoke it and the remark becomes a corollary
rather than a caveat. Alternatively, keep 16.1 as a lemma about regrouping and add a short Proposition 16.2 that
does the family-path step. **The result is right; the statement is weaker than its use.**

## B3 ⚡ §7's four-question decision procedure has an unhandled branch at question 2

**Earliest section: §7, with its root in §4.** **Kind: missing premise / boundary mistake.**

§7 closes with an ordering presented as a decision procedure, and says the law may proceed *"only after those
questions are resolved"*:

1. Does the point exist?
2. **Does the measure apply?**
3. Does the law require this point to participate?
4. Is the required value or state established?

The manuscript handles *unresolved* explicitly at **Q3** (*"participation is **unresolved** rather than silently
inferred from the supported remainder"*) and at **Q4** (want of state). At **Q2** it offers only resolved-yes (a
value) and resolved-no (`NA`, which §4 defines as a positive claim: *"resolved-inapplicable"*).

**There is no branch for unresolved applicability.** `eligib*` occurs **once in 1,975 lines**, and only as a
participation rule. ToD v7.1 §2.3 is explicit that this case exists: *"Eligibility may be **unresolved** rather
than established or denied."*

**Concretely:** an account-day exists in \(\Omega_U\). Whether Balance applies there depends on whether the
account was open that day, and the open/closed evidence is missing. This is **not** `NA` — that would assert
resolved-inapplicability, which is a stronger claim than the evidence supports, and it is exactly the
over-claim §4 built the semantic map to prevent. It is **not** want of state as §4 currently scopes it — *"the
evidence or analytical state required to establish **its value**"*. And it is not unresolved participation.
**It has no home in the theory as written.**

**Fix, and it must not become a codomain value:** extend §4's want-of-state sentence to cover state required to
resolve *applicability*, not only *value* — *"If the measure applies but the required evidence is unavailable,
or if the state required to determine **whether it applies** is unavailable, the attempted establishment has
want of state."* Then §7's Q2 gets the same unresolved branch Q3 and Q4 already have. **One sentence**, no new
machinery, no new codomain inhabitant.

*(§8 is honest here — it says *"at least four"* cases, not four. §7's ordering is the section that claims
completeness.)*

---

# C. The four central distinctions, checked for quiet collapse

## C1 Continuation state vs sufficient basis — **held everywhere except §26**

§9 and §10 draw it cleanly, and §9 carries the refusal I asked for two passes ago in the paper's own voice:
*"These examples… do **not** define analytical sufficiency… Sufficiency is a separate, target-relative
question."* §11 lists the four ideas side by side. §21 keeps constitutive lineage off it.

**§26 collapses them at the one law where collapse is invisible.** The section opens on continuation
(*"does not imply that the continuation state used to produce it is still available"*), closes on the box
*"stored answer \(\not\Rightarrow\) retained continuation capability"* — and its second item is
*"A displayed MEAN does not imply retention of its SUM and COUNT **basis**."*

For MEAN the continuation state is \((s,n)\) and a sufficient basis is \((SUM@A, COUNT@A)\) — §21's own example.
**They carry the same two numbers.** MEAN is therefore the one case where using the wrong word is undetectable,
which makes it the worst place to use it loosely and the best place to nail the distinction.

**Fix:** split §26 into two claims — *stored answer \(\not\Rightarrow\) retained continuation state* and *stored
answer \(\not\Rightarrow\) retained sufficient basis* — and use MEAN deliberately: the same pair \((s,n)\)
answers *"can this combine with another month's state?"* as continuation state and *"can MEAN be established
here?"* as a basis, and those are different questions about one stored object. Synthesis v0.5 had the second
claim (*"a materialized object may or may not retain an admitted sufficient basis for some other target"*) and
**the manuscript dropped it**; restoring it fixes this.

## C2 Semantic measure map vs establishment — **held, cleanly, in every section**

I attacked this hardest because it was v0.4.1's class-1. §4 states it; §8's four-case list keeps want-of-state
outside the codomain; §10.1 restates the trichotomy for the grounded route; §11 produces a want-of-state MEAN;
§26 keeps storage out of it; §32 enforces it against pressure (*"the answer is want of state… it cannot silently
redefine the original quantity around the surviving observations"*); §35 keeps SQL `NULL` out. **No section puts
an establishment state into \(X\cup\{NA\}\).** This distinction is now the most robust thing in the paper.
The only gap is B3, which is a *missing* judgment, not a leaked one.

## C3 Family vs expression — **held**, with one internal inconsistency

§6, §18, §19, §20, §21, §25 and §34 all respect it. §19 explicitly refuses the generic promotion operator and
names the four things that do not suffice (repetition, business naming, physical storage, coherent evaluation).
§20 keeps AOV's ratio out of family lineage while allowing a later constituted AOV family. §34 keeps request
syntax from minting identity.

**But §5 states four family obligations and §19 states seven, with no cross-reference.** §5: members;
law-bearing relations; derivability; coherence. §19: determinate target; identity-bearing formation; admitted
measures; law-bearing relations; derivability; coherence; well-founded ancestry. A reader cannot tell which is
the definition and which is a checklist. **Fix:** §5 should present its four as *what becomes visible with
nested anchors* and forward-reference §19 as the full contract, or §19 should be explicit that it restates §5
plus three conditions earned in §10, §19 and §23.

## C4 Same-family continuation vs cross-law interchange — **held, and it is the cleanest of the four**

I looked specifically for a later section overgeneralizing Proposition 16.1 into arbitrary operator interchange
and **found none**. §15 boxes the prohibition (*"lawfulness of each edge \(\not\Rightarrow\) commutation of
different edges"*). §16's post-proof remarks refuse it by name (*"it does not establish interchange between
different laws, such as SUM and LAST"*). §17 scopes compression to *coherent family staging* and immediately
fences it (*"a family-changing construction, a change of source population, a different participation rule, a
different ordered selection"*). §26 fences reuse the same way. Nothing downstream relaxes it.

*(§15's arithmetic checks out against ToD §11.2: \(SUM\circ LAST=80+40=120\); day totals \(20,40,80\);
\(LAST\circ SUM=80\). The raggedness is in \(\Omega_U\), and §15 says so.)*

## C5–C9 Smaller terminology findings

- **C5 `scope` is used twice and never defined.** §32: *"what source and **scope** determine Revenue"*; §33:
  *"participation and **scope**"*. It is half of the frozen `clause = source × scope`, and §10.1 is where the
  determination pattern *"first becomes visible"* — so either define it there or drop the word. Using an
  undefined term in two boundary sections invites readers to supply the v7-era meaning.
- **C6 "the same governed context" is undefined** (3 uses) and B1 shows it is load-bearing.
- **C7 §8 and §14 appear to disagree about LAST's empty case.** §8: LAST *"has the same shape"* as MIN/MAX — no
  empty identity. §14 gives LAST an explicit \(\bot\) with \(\bot\oplus w=w\), i.e. a **monoid identity**. Both
  are correct; the reconciliation is that \(\bot\) is an identity **in \(K\)**, not a value in \(X\), and
  finalization of \(\bot\) is ungoverned. That sentence is missing, and the asymmetry is unexplained — MIN/MAX
  admit exactly the same \(\bot\) treatment and §9 does not give it to them.
- **C8 §14's witness combination is undefined when \(s=t\).** The case split covers \(s<_S t\) and \(t<_S s\)
  only. Harmless under partition regrouping where each point appears once, but the associativity claim in the
  very next sentence depends on the definition being total, and the displayed formula is the paper's.
- **C9 `incomparab*` = 0.** §3 defines refinement and never says two anchors of one universe may be
  **incomparable**. Week and Month are both partitions of \(\Omega_U\) with neither refining the other — ToD
  §2.1.2's *"a week can cross a month boundary."* One sentence in §3 fixes it, and it protects §11's
  day→month→quarter example from being read as *"any two time anchors compose."*

---

# C. v7.1 reconciliation

**Method.** Both documents read end to end in a parallel full-read sweep, then **every claimed absence
re-verified by me directly in both files**, and the v7.1 quotations re-derived from the publication of record
before endorsement. Deliberate renames (`sufficient state` → `continuation state` + `sufficient basis`) were
treated as preserved throughout. Wording, chapter order and retired ontology are not reported as losses.

| classification | count |
|---|---|
| preserved explicitly in v8 | 24 |
| preserved in a simpler or derived form | 17 |
| intentionally moved outside the foundation | 9 |
| superseded by a stronger/corrected v8 statement | **8** |
| **apparently lost and still needed** | **12** |

**Headline: v8 is a faithful and in several places better reconstruction of the v7.1 core.** The twelve losses
are not scattered — they cluster in four places: **anchor incomparability**, **state-substitution discipline**,
**the refinement direction**, and **the contextual-formation account v7.1 explicitly restored.**

## C.1 The three that should not survive into publication

### C-L1 — Refinement is a *partial* order, and same-family does not imply mutual reachability
**This is my C9, and it is worse than I graded it.** I found the missing sentence in §3; the sweep found the
missing *obligation* in §5. v7.1 §6.3 (line 604):

> *"Family coherence does not erase partition geometry. **Revenue at Week and Revenue at Month may belong to one
> additive family even when neither anchor refines the other.** The family guarantees agreement along admitted
> paths; **it does not manufacture a path between incomparable locations.**"*

Verified: v8 has **0** occurrences of `incomparable`, `partial order`, `reachab*`; `refine` appears 4 times,
always as a two-anchor *B finer than A* relation; §16 assumes \(I\succeq B\succeq A\) throughout.

**What breaks:** §5 defines a family as realized over admitted anchors *"with lawful derivability along its
family structure"* — so a reader concludes any two measures of one family are mutually derivable. §5's *"geometry
alone does not create a family edge"* guards the case where a projection exists but no law does. **Nothing in v8
guards the case where no projection exists at all**, which is the single most common production error (rolling a
weekly materialization up to calendar months). **Upgrade my C9 from one sentence in §3 to: one sentence in §3
plus one obligation in §5.**

### C-L2 — A declared state equivalence must be a congruence — and **this corrects my own stable list**
v7.1 §6.6 requires \(u\equiv u', v\equiv v'\Rightarrow u\oplus v\equiv u'\oplus v'\) and
\(u\equiv u'\Rightarrow\phi(u)=\phi(u')\), with §10.5 (line 926) giving the counterexample I verified verbatim:

> *"MEAN states \((10,1)\) and \((1000,100)\) both display \(10\). Adding the same new state \((20,1)\) gives
> means \(15\) and \(1020/101\). The equal current results did not retain equal continuation information."*

Verified: `congruen*` — **0 occurrences in v8**. And §25 line 1336 lists, among the changes that do *not* create
a successor identity:

> *"— a new carrier encoding of the same continuation state;"*

**with no obligation that the encoding respect \(\oplus\) and \(\phi\).** §36's realization duty is scoped to
*physical* realization, not to a declared analytical equivalence between two continuation states.

**I listed §25 as stable result E14. That was wrong, and I am withdrawing it.** As written, line 1336 is an open
door: any two states that finalize to the same displayed value can be called the same continuation state
re-encoded. This is the *substitution* claim, orthogonal to §26's *retention* claim — §26 says a displayed value
does not imply retained capability; C-L2 says two states that display alike may not be swapped as continuation
inputs. **One clause on line 1336** closes it.

### C-L3 — The contextual-formation account, and the withdrawn impossibility theorem
**The most dangerous of the twelve, because it risks silently reinstating something v7.1 explicitly retracted.**
v7.1 Appendix C.4 (line 1424):

> *"Earlier Version 7.1 working drafts proposed universal projection-fiber locality of formation as a
> family-admission test. **That claim and the categorical contextual-family exclusions derived from it are
> withdrawn.**"*

and §3.4 (line 280): *"No general impossibility theorem for lag-, rank-, cumulative-, or rolling-derived families
follows from it… **Neither automatic promotion nor categorical exclusion is justified by the function name.**"*

Verified: v8 has **0** occurrences of `LAG`, `rolling`, `cumulative`, `rank`, `focal`; `contextual` occurs
**once**, in §34, as something a request language *"may also articulate."*

**The risk is structural, not lexical.** §16 defines continuation entirely over \(g_I(i)\) for
\(i\in D\cap\pi^{-1}(a)\) — **contributions strictly inside the fiber.** That is precisely the projection-fiber
locality shape from which the v7.0 drafts derived the exclusion, and which v7.1 withdrew by name. A careful
reader of v8 alone can re-derive the retracted theorem from §16 and conclude that rolling and rank families are
categorically inadmissible.

§19's seven obligations are the right general contract and I count them as preserving v7.1 line 284's *common
family contract* (*"not a second admission system"*). **What is missing is one paragraph saying the contract
applies to contextually formed inputs, and that §16's in-fiber continuation is not an admission test.**
Given that v7.1 spent an appendix withdrawing this, v8 cannot be silent about it.

## C.2 Four that should be fixed, with one correction to the sweep

- **C-L4 — Conservation of relationships / formation order.** v7.1 §3.5, boxed and verified: *"**An operation
  cannot use a relationship that was neither retained nor reconstructed from governed evidence.**"* with *"A
  weighted mean requires pointwise products at its constitutive anchor **before separate reductions destroy the
  pairing**."* Verified absent: `pairing`, `covarian*`, `correlation`, `conserv*` (1 hit, unrelated) — all 0.
  **Correction to the sweep:** it claims v8's basis adequacy *"is checked role-by-role and passes for
  `SUM(value)` + `SUM(weight)`."* **That is wrong.** §10's adequacy clause is an indiscernibility condition —
  *"Two governed evidence configurations that agree on every required basis input… must determine the same
  target"* — and it correctly rejects that basis: \((10,1),(0,100)\) and \((0,1),(10,100)\) agree on both sums
  and give weighted means \(10/101\) and \(1000/101\). **§10 detects the failure. What it does not do is name
  the remedy.** The real loss is the positive formation rule — *form the pointwise product at the constitutive
  anchor* — which is the only v7.1 rule governing **multi-input formation order**, and which v7.1 §11.6 made the
  contract emphasis for four of eight statistical groups. Recommend one paragraph in §10 or §19.
- **C-L5 — Lossy state cannot certify its own coherent-instance premise** (v7.1 §10.6, §8.2; `lossy` = 0 in v8).
  §14 line 747 *asserts* the premise — *"Within one fixed coherent analytical instance"* — and §26 licenses
  witness reuse *"under the same governed order and compatible participation"* without saying **who establishes
  compatibility, or that the witness cannot**. A planner merging witnesses from two snapshots may read
  successful combination as evidence of coherence. v7.1 §13.2 recorded this as one of four validated adversarial
  checks.
- **C-L6 — The refinement direction is entirely absent.** v7.1 §3.6, verified: *"replication of a coarse value
  for participation in a finer expression does not establish a finer measure of the same family."*
  `replicat*`/`broadcast`/`disaggregat*` = 0. §3's *grouping points ≠ determining a value* is the
  coarsening-direction guard; **v8 has no mirror**, so joining a monthly target onto daily rows and calling the
  result a daily measure is forbidden by nothing in the paper.
- **C-L7 — Internal value structure is not analytical location** (v7.1 §5.7, boxed and verified). §9 says
  continuation state *"is not a new ontological category"* and may be *"tuples, sets, sketches, or point-value
  witnesses"* — the *kind* half. The *location* half is gone, and v8 then introduces \(K=Set(X)\),
  \(K=HLLSketch\) and \(w=(s,x(s))\) as ordinary values. Without the rule, the witness's point coordinate reads
  as a second current anchor of \(F@A\).

## C.3 Five that are editorial or belong to scope

**C-L8 Proposition 6.2** (coherence lifts through a well-founded basis by induction) has no v8 counterpart —
v8 has exactly one proposition. §9's \(K=(s,n)\) brings the common staged case under 16.1, but the **induction**
is what covers composites whose basis roles are themselves composite (variance from moments, correlation from
paired moments). §10's anchor-locality recursion sets it up and never proves coherence lifts through it.
**This is the same defect as B2(ii) from the other side:** the paper can prove coherence for single-\(\oplus\)
families and must assert it everywhere else. Fixing B2 and C-L8 together is one piece of work.
**C-L9** downstream disclosure does not repair an undefined computation (v7.1 §9.4; `disclos*` = 0) — §32 and
§37 cover *silent* restriction only, and the contamination half (late row removal does not undo a consumed
contribution to an order-dependent intermediate) has no substitute.
**C-L10** positive evidence-adequacy criteria for LAST under partial evidence (v7.1 §9.2, §9.6) — v8 keeps the
prohibitions and drops the criteria, leaving no stated way to answer LAST under partial evidence at all.
**C-L11** the multiset counterexample (\(0,0,6\) has mean 2; discarding multiplicity gives 3) and the
multiplicity-preserving family; `multiset`/`quantile` = 0. As with C-L4, §10's adequacy catches it and the paper
never offers the object that fixes it.
**C-L12** what *"must agree"* means for approximate realizations (v7.1 §6.4, §12.1) — §24's agreement obligation
is unqualified, and §36 requires an error contract without saying **how it composes under staging**, which
matters because §16 licenses arbitrary regrouping.

## C.4 Where v8 is stronger than v7.1 — eight supersessions

Worth recording so the revision does not "restore" them: the **positive** SUM/LAST sufficient condition (§15 —
v7.1 had only the counterexample); the corrected remedy for failed interchange (§5, §15 — v7.1 §4.1 leaned
toward auto-splitting the family, v8 rules that the destination is simply not established); **grounding as an
explicit first-class route** (§4, §10.1, §23 — v7.1 had only *"governed primitive inputs"*); the generalized
order requirement (§12 — lexicographic is now *"one valid form"*, not the only one); **fiber-relative LAST**
named as such (§13); Prop 16.1's premises promoted into the statement rather than left in prose after the proof;
the three-way lineage separation (§17); and the four-way semantic codomain with establishment kept outside it
(§4, §8).

## C.5 Two apparatus notes

- **v8 names neither Contract Calculus nor Measure Algebra** (0 occurrences each; v7.1 cites both). The §5.8
  withdrawal I pushed for two passes is complete — but v7.1's *positive* companion sentence went with it
  (*"Compatible earlier work on constitutive anchors, closed law contracts, participation, pairing, and carrier
  adequacy **remains applicable**"*). One sentence should say MA's continuation-class machinery is retained as
  machinery. That is the notification obligation I flagged at v0.5, now with a concrete home.
- **The statistical extension catalog** (v7.1 §11.6, eight groups, supplement S.1–S.8) gets **no disposition in
  v8**. These are deterministic analytical families, so §31's Statistical Bridge is explicitly *not* the right
  destination — v7.1 §12.5 says so. One sentence of disposition. Likewise v7.1's anti-analogy rule (*"TOP-k and
  rank-based correlation acquire no standing merely by analogy"*) has no counterpart: §19 closes the promotion
  routes it enumerates, and analogy is not among them.
- **Publication apparatus** not carried over (not losses in a working draft, but flag for the revision): v7.1
  §13.1's scope limit (*"Family admission is a set of obligations on a construction, not a claim that an
  algorithm can discover every family"*), §13.2's two reference suites and four adversarial checks — **two of
  which are C-L5 and C-L11 above** — and the references section; v8 cites [1]–[14] nowhere.

## C.6 Correction to section E

**E14 (Succession versus realization, §25) is withdrawn from the frozen list** pending C-L2's congruence clause.
Everything else in section E stands. Section F gains C-L1, C-L3 and C-L6 as obligations; **F11 (contextual
expressions) is upgraded from a drafting note to C.1 severity** for the reason in C-L3.

---

# D. Structural revision recommendations, ordered by importance

**D1. Cut one of the four recapitulations.** §6, §28, §39 and §40 each restate the whole development, and §39
reproduces §6's two-sided arrow diagram essentially verbatim. *Problem it solves:* by §39 the reader has been
told the same thing four times and cannot tell which statement is canonical, which makes the architecture look
padded rather than small — the opposite of the paper's thesis. *Recommendation:* keep §6 (earned, in place),
keep §28 as the compact restatement, **cut §39**, keep §40 short and rhetorical.

**D2. Number and prove §15's local coherence theorem.** §15 calls its result *"a **local coherence theorem**"*
and then states it in prose with no number and no proof, while §16 — the less contested result — gets
Proposition 16.1 with a formal proof. *Problem it solves:* the SUM/LAST interchange condition is the paper's
most-cited and most-fought-over result, and it currently has **less formal standing than the regrouping lemma**.
*Recommendation:* Proposition 15.1, with its three premises stated formally (rectangular Account-by-Day region;
Balance applicable and participating throughout; a common governed Day order across account fibers) and a
four-line proof. The counterexample stays as the motivating example.

**D3. Fix the forward references of the two terms the paper insists must not be confused.** *"continuation
state"* is first used in **§5** (line 184) and defined in **§9** (line 400); *"sufficient basis"* is used at the
end of §6 and defined in §10. *Problem it solves:* the reader meets the distinction the paper is most anxious
about before either term exists. *Recommendation:* neutralize the §5 and §6 uses (*"different laws, retained
state, finalization, and analytical claims"*), or move one-line definitions forward.

**D4. Merge the duplicated boundary test.** §29 and §38 state the same test in different words. *Problem:* two
tests read as two criteria. *Recommendation:* state it once in §29; make §38 a list that applies it.

**D5. Tier the back third.** §29–§38 is ten consecutive jurisdiction sections. §30 (cross-universe) and §32
(evidence vs law) are **load-bearing** — B1 shows §30 is doing foundational work — and must stay in main text.
But §33 (Manifold), §34 (Frame-QL / MEL) and §37 (agents) name specific datumwise artifacts, and §36 is a
floating-point note that belongs with §35. *Problem it solves:* a foundational paper that names two product
languages in main text invites the reading that ToD is a product rationale, and it dates the paper against its
own neighbors' version churn. *Recommendation:* an appendix, *"ToD and its neighboring frameworks"*, carrying
§33, §34, §37 and the §36 realization notes; §35 absorbs §36's principle in two sentences.

**D6. Reconcile the two family-obligation lists** (§5's four, §19's seven) — see C3.

**D7. §11 is carrying three jobs.** The COUNT/MEAN four-way separation (*"This example separates four ideas in
one place"*) is one of the strongest passages in the manuscript, and the section then appends the mean-of-mean
warning and a segue to order. *Problem:* the paper's cleanest demonstration ends on a different topic.
*Recommendation:* move the mean-of-mean material to **§18**, which already uses
\(mean(mean(revenue@day)@month)@quarter\) as its expression example — it is an expression point, not a
participation point.

**D8. §17's MAX contrast is garbled.** *"taking MAX at Order and then summing something afterward"* does not
name a second construction precisely enough to contrast with the first. Give it a definite second expression or
cut it; the surrounding claim is right and does not need it.

---

# E. Stable results — treat as frozen unless new evidence appears

These survived direct attack in this pass, several of them having survived earlier passes as well:

1. **\(v@a\) and \(F@A\) as one analytical grammar at two levels of governance** (§1, §6). No theorem was found
   requiring a prior primitive; the nearest candidate (the meaning of absence) still needs \(\lambda_U\) and is
   therefore later, which confirms the ordering.
2. **Grounding versus law-determination as the two establishment routes**, with grounding terminating the
   regress (§4) — **and §10.1's ruling that the sufficient-basis account governs only the law-determined
   route.** This was the blocker two versions running and is now correctly resolved.
3. **The semantic measure map \(A\to X\cup\{NA\}\) with establishment judgments outside the codomain** (§4).
   The most robust result in the paper (C2).
4. **geometry \(\neq\) participation \(\neq\) support** (§7), and **participation is not inferred from support**
   (§11), including the value-dependent-participation guard (§7).
5. **Empty participation as a law case**, with the four distinct states and *"missing evidence does not get to
   impersonate emptiness"* (§8).
6. **continuation state \(\neq\) sufficient basis** (§9, §10), with the five basis obligations. This took three
   versions to get right and is now correct and complete.
7. **Sufficiency is target-relative, not continuation-class-relative** (§9, §10) — ToD v7.1 §5.8 upheld.
8. **Family as intensional durable identity; no generic promotion operator; one reducer \(\neq\) one family**
   (§5, §19) — including the ruling that premise failure prevents establishment rather than splitting Balance.
9. **The Balance SUM/LAST non-commutation**, its ragged-geometry counterexample, and the rectangular sufficient
   condition (§15). Arithmetic verified against ToD §11.2. *(Subject to D2's formalization, not to doubt.)*
10. **Finite family coherence as regrouping only**, with the explicit refusal to generalize to cross-law
    interchange (§16). *(Result right; statement needs B2.)*
11. **family lineage \(\neq\) expression tree \(\neq\) carrier lineage** (§17).
12. **constitutive lineage \(\neq\) sufficient-basis dependency** (§21), and **alternative bases must establish
    the same target; agreement alone is not proof** (§22).
13. **Identity determines required agreement; agreement does not determine identity** (§24).
14. **Succession versus realization** (§25), including the ruling that a different admitted sufficient basis is
    *not* a successor identity.
15. **Approximation is located by whether the semantic claim changes** (§27), with the float and realization
    treatment consistent with it (§36).
16. **Cross-universe passage is not an anchor projection** (§30) — load-bearing, and the anchor for B1's repair.
17. **analytical law \(\neq\) evidence that its premises hold** (§32); **request syntax \(\neq\) authority**
    (§34); **interpretation \(\neq\) adjudication \(\neq\) execution** (§37).

---

# F. Drafting obligations — repairable while editing, no foundation reopened

1. **Unresolved applicability** (B3) — one sentence in §4, one branch in §7.
2. **Define or drop `scope`** (C5). If B1 is resolved by universe-indexing, `scope` has a natural definition and
   the frozen `clause = source × scope` finally connects.
3. **Define "the same governed context"** (C6) — follows from B1's decision.
4. **State that anchors of one universe may be incomparable** (C9) — one sentence in §3.
5. **Reconcile §8 and §14 on LAST's empty case** (C7): \(\bot\) is an identity in \(K\), not a value in \(X\).
   Consider giving MIN/MAX the same treatment for symmetry.
6. **Complete §14's witness combination for \(s=t\)** (C8).
7. **The `participation ≠ support` *permission*** — fourth version running. ToD §11.5.1 admits
   \(count(revenue@order)=97\) *"when the latter's participation law counts those supported observations."*
   `97` has 0 occurrences and the manuscript states only the prohibition. The reconciliation is one line and
   belongs in §11: **a law may take support as its *subject*; it may not take support as its silent
   *population*.** The 97 is lawful precisely because its target *is* the evidence.
8. **The \(v@a\) type-versus-individuation sharpening** — `individuat*` = 0, fourth version. A point's *type* is
   a tuple of coordinate values; its *individuation* is the closed claim that these constituents and no others
   individuate the world, which the 2026-09-15 ruling makes one of the universe's three constituted facts. §1
   needs one clause or the \(a \to \Omega_U\) ordering is arguably circular.
9. **`carve`** = 0, fourth version — but **this is now subsumed by B1.** Resolve the universe index and carve
   follows; do not add separate machinery for it.
10. **A `sufficient-state basis` migration note.** v7.1's published compound term is split in v8 into
    *continuation state* and *sufficient basis*. The split is right, but v7.1 readers need a one-paragraph
    translation rule or half of them will map the old term onto the wrong new one.
11. **Contextual expressions.** `contextual` occurs once, only as a request-language feature (§34). v7.1 treats
    *family constructed from a contextual expression* under the common family contract. §19's seven obligations
    are that contract — the manuscript just never applies them to the contextual case, which is the one readers
    will ask about first.
