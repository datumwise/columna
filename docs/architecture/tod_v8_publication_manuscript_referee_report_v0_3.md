# Referee report — *The Theory of Data*, Version 8.0 publication manuscript, revision v0.9

**Claude, at Huayin's direction, 2026-09-28.** Subject:
`attachments/175a8ab0_theory_of_data_v8_publication_manuscript_v0_9_full.md` (2,131 lines) with
`attachments/cff7c7b4_tod_v8_v0_9_revision_note.md`. Supersedes
`tod_v8_publication_manuscript_referee_report_v0_2.md`.

**Standing.** Adversarial read of the revision. **No implementation. No changes to schemas, Core, Platform,
Manifold, MEL, Frame-QL or publications. The manuscript is not rewritten.**

---

## 1. Verdict

> **Both prior findings are resolved, the references section is added, and the revision goes much further: it
> introduces a value-closed core with family roots and a separate expression layer. The architecture is right,
> and it makes the theory constructive where it was previously only prohibitive.**
>
> **One regression: a published non-minimality result was dropped in the §5.3 rewrite, and a minimality claim
> about the root was added in §7.8. Those move in opposite directions and both need attention.**

**No foundational blocker.** Three findings, all repairable in a sentence or two.

---

## 2. The two prior findings, and how they were resolved

I recommended naming **governed assignment** as a third establishment form to house the governed constant, and
asked what establishes the analytical-point-level predicate. **The revision does something better than either.**

§3.6 stops treating root establishment as a *kind* of formation and makes it **a separate question from
continuation**:

> *"Family continuation begins from an established \(F@R_F\). It does not, by itself, explain how that root
> measure was established."*

And grounding becomes a special case rather than a gate: *"If \(R_F\) reaches the analytical-point level… a root
value can be **grounded**: observed, given, **assigned**, or otherwise established directly… **But \(R_F\) need
not reach that level.** A family can begin at a coarser constitutive anchor… provided the root measure has a
governed, non-circular establishment and adequate evidence."*

**This disposes of both findings at once.**

- **The governed constant has a home.** A governed rate or threshold is a family whose root is a coarse anchor,
  established by governed declaration. The word *assigned* is back, and it no longer needs the anchor to be
  point-level. No third form of establishment was needed — the dichotomy that created the gap was dissolved
  instead.
- **The point-level predicate is no longer load-bearing.** It now determines only whether the word *grounded*
  applies, not whether establishment is possible. Nothing turns on a cardinality fact about an unexposed ground.

The boxed four-way separation is the result, and it is the cleanest statement of the point in any draft:

> \(\text{family continuation}\neq\text{root formation}\neq\text{evidence provenance}\neq\text{physical
> computation}\)

with the two errors it forecloses named: *"ToD does not require a primitive fact table beneath every family root.
It also does not allow an arbitrary reported aggregate to bypass the analytical constitution of the family
merely because somebody supplied the number."*

**The references section is added** — v7.1, Measure Algebra v1.0, the Statistical Bridge v3.0 and Frame-QL v2.4,
with DOIs. And endnote 1 was rewritten to carry the root/point-level relationship, which is where it belonged.

---

## 3. What the revision achieves

This is the largest architectural change since the working manuscripts, and it should be reviewed on its merits.

**Value closure as a representational criterion, not a fifth axiom.** §3.2 keeps the four family obligations as
the definition of family *structure* and adds value closure as the criterion for *which object represents the
family*: \(F@R_F\) plus the governed family law and geometry must establish every admitted \(F@A\). The
motivating sentence is the right one: *"If a displayed scalar cannot carry the family's lawful continuation from
the root, the theory does not hide extra state behind that scalar and still call the scalar the family value."*
That is a real diagnosis of a real failure mode, and it explains — rather than stipulates — why some familiar
quantities are not families.

**The family-relative root.** §3.2's \(R_F\) is *"not the root of the universe, need not be the finest governed
anchor of the universe, and need not reach the analytical-point level."* The Balance illustration earns it:
Account-Day points can be *"the indivisible source locations of Balance continuation even when the universe
itself has finer underlying analytical points."* This is what lets the theory keep both the no-atomic-fact-table
commitment and a genuine base for continuation.

**The expression layer, with the canonical cases.** §3.5 puts MEAN, exact unique count and HLL estimation in the
expression layer over SUM/COUNT, DistinctSet and HLLSketch respectively, each with the reason stated rather than
asserted: the scalar mean is not continuation-complete, the cardinality does not retain overlap, the estimate does
not retain merge capability. And the generic-promotion refusal is sharpened — a family may be constituted *"only
if its chosen value-bearing object satisfies the family obligations **and value closure**."*

**§5.4 is the revision's best new section, and it is the first constructive result in the paper.** Making
\(Count, SumX, SumX^2, SumXY\) value-closed families and statistics expressions over them **answers the
pairing-conservation rule of §5.5 rather than merely restating it.** The prohibition (*"An analytical law cannot
use a relationship that was neither retained nor reconstructed from governed evidence"*) has always been correct
and has never had a recipe. \(SumXY\) as a family *is* the recipe: the pairing is formed at the root, so
covariance and correlation become expressions that cannot destroy it. Every prior draft could say what not to do;
this one says what to do.

**§7.8 draws the materialization consequence without overclaiming.** The two rules (persist only value-closed
family measures; persist each family only at its root) yield a precisely scoped conclusion:
*"**Intra-family** stale-derived-value inconsistency is eliminated by construction. Root freshness, evidence
validity, and cross-family snapshot compatibility remain separate obligations."* Plus *"This does not mean every
possible request is backend-independent"* and *"This is an implementation consequence of the theory, not a
requirement that every implementation adopt one storage architecture."* Correctly hedged throughout.

**Nothing load-bearing was lost in the rewrite, and I checked specifically.** The semigroup branch of
Proposition 6.2 survives (*"in the semigroup case without an identity, staged and direct continuation agree on
every finite nonempty contributing fiber"*), and **MIN/MAX are kept inside the family layer** —
*"MIN and MAX can be value-closed on nonempty domains under a commutative semigroup law"* — rather than exiled
to expressions, which would have been the easy mistake. \(\bot\in K,\ \bot\notin X_F\) survives in §6.2.
Proposition 6.3 is correctly retargeted to \(E@A\), keeps the determinism premise, and gains a stronger fence:
*"It does not promote \(E\) to a family, establish a family edge for the displayed result, or prove equivalence
with a different expression identity."* §7.6's agreement obligation explicitly covers **both** \(F@A\) and
\(E@A\), so moving MEAN between layers did not drop it out of the consistency regime. And §3.1 now **defines**
identity-bearing law parameters, which earlier drafts used undefined.

---

## 4. Findings

### 4.1 ⚡ The non-minimality result was dropped, and a minimality claim was added

**Dropped.** The previous draft's §5.3 contained:

> *"A sufficient basis need not be minimal, necessary, recoverable from every other basis, or materially
> available whenever another lawful route establishes the target."*

**In this revision that sentence has no counterpart.** `minimal` and `need not be necessary` have zero
occurrences; the two surviving hits on *recoverable* and *necessary* are unrelated (witness recoverability in
§6.2, evidence arguments in §8.4). The sentence lived in the section that was rewritten from *"Sufficient
basis"* into *"Sufficient basis for an expression"*, and it went with the retitling.

This is a **published result**, not a stylistic flourish: Version 7.1 states that sufficiency is
*"target- and use-relative, not a necessity or universal recoverability statement."* Without it, a reader
reasonably infers that a sufficient basis must be minimal or must be recoverable from any other basis — and §7.4
still admits **alternative** bases for one target, which only makes sense if neither is canonical.

**Added, in the opposite direction.** §7.8 now says of the root materialization:

> *"It is the **smallest** authoritative family state from which the family claims its admitted continuation."*

Minimality is asserted and not established, and **it is not obviously true**. A DistinctSet root retains the full
participating subset, which is more than some admitted coarsenings require; a moment-family root may carry
\(SumX^2\) that a given admitted anchor's expressions never consult. The root is *canonical* and *authoritative*
— that is what §7.8 actually needs, and it is what the two persistence rules deliver. Minimality is a stronger
claim that buys nothing here.

**Repair.** Restore the non-minimality sentence in §5.3, and change §7.8's *"smallest"* to *"canonical"* — or
state what minimality means and prove it. As it stands the paper drops a disclaimer in one chapter and asserts
its converse in another.

### 4.2 The value-closure definition and its own elaboration disagree about what may sit outside the root

The boxed definition in §3.2 is careful and tight:

> *"…the materialized measure \(F@R_F\)—its governed anchor points and family values, **together with the
> governed family law and geometry**—is sufficient to establish every admitted \(F@A\) without requiring
> analytical state external to the family."*

Four paragraphs later the same section widens it:

> *"A family law may depend on governed order, structured values, or **other family-specific state** so long as
> that information is present in or reconstructible from the materialized root measure and **governed family
> context**."*

**"Governed family context" is undefined and strictly broader than "the governed family law and geometry."** So
is *"other family-specific state."* Under the loose reading, **a MEAN family could be declared value-closed by
calling the counts family-specific state reconstructible from context** — which is precisely the move §3.5 exists
to forbid, and the whole reorganization turns on forbidding it.

The tight reading is clearly intended, and the line that distinguishes them is available: the permitted extras
are **fixed family structure** — governed law parameters, geometry, and constitutive order — whereas the counts
are **per-anchor-point analytical values**, which is exactly what must live in the root measure. Note that §6.2
already reasons the right way for LAST, asking *"whether the witness needed for any admitted continuation is
recoverable from the materialized family"* — recoverable from the **measure**, not from context.

**Repair.** Align the elaboration to the definition: say that the admissible context is governed law, geometry
and order, and that per-anchor-point analytical values are not context. One sentence, and it closes the only
loophole I could find in the new core.

### 4.3 The manuscript never says that MEAN satisfies the four obligations and fails only value closure

This is the sentence that would make the reorganization land, and it is missing.

A reader meeting §3.5 can conclude that MEAN is an expression because it *fails to be a family* — that it does
not meet the four obligations. **That is false, and it makes the argument weaker than it is.** One could declare a
MEAN family with admitted measures at Day and Month, law-bearing relations (weighted recombination), derivability
where the premises hold, and coherence of alternative paths. **All four obligations can be met.** What MEAN fails
is **value closure**: the scalar cannot carry continuation from the root.

That is a far more interesting claim, and it is the one that justifies separating *structure* from
*representation* in the first place. §3.2 gestures at it (*"the continuation-bearing object is the better family
candidate"*) but frames it as a representational preference rather than as the precise point of failure.

**Repair.** One sentence in §3.5: MEAN can satisfy the four family obligations and still fails value closure,
which is why it belongs in the expression layer and why value closure is a criterion the four obligations do not
already entail. This also answers the question a careful reader will ask — *what is value closure adding?* —
which the manuscript currently leaves to inference.

---

## 5. Theorem audit

**Proposition 6.1** unchanged; five premises, each used, conclusion scoped to the region.
**Proposition 6.2** retitled *"in the monoidal region"* but **both branches survive in the statement**, so the
no-identity laws are still covered and MIN/MAX have a theorem. The constitutive anchor \(I\) is not required to
be point-level, so the root doctrine does not disturb it.
**Proposition 6.3** retargeted to \(E@A\), determinism premised, fenced against promotion.

**No proposition is invoked more broadly than it is proved.** §9.1 continues to say so in the paper's own voice.

---

## 6. Additions to the frozen list

- **Value closure as a representational criterion** distinct from the four family obligations, with the
  family-relative root \(R_F\) that need not be the universe's point level.
- **The expression layer \(E@A\)** with its three canonical cases and the reason given in each.
- **§3.6's four-way separation** of family continuation, root formation, evidence provenance, and physical
  computation. This supersedes and improves the formation/evidence separation I froze last time.
- **§5.4's moment families** as the constructive answer to relationship conservation.

---

## 7. Editorial

- Chapter 3 now defines the **family** (§3.1) before the **measure's semantic map** (§3.3), so *measure* is used
  in the family definition before its form is given. Defensible for a foundation that leads with identity, but
  chapter 2 ends by saying values *"must be established separately"* and a reader arriving at §3.1 has not yet
  been shown what a measure is. A one-line forward pointer in §3.1 would settle it.
- The references section resolves the outstanding apparatus gap. §9.2 now names the Measure Algebra relationship
  with a citation behind it.

---

## 8. Summary

Both prior findings are resolved by a better route than the one I proposed, and the revision's new architecture
is correct: value closure explains rather than stipulates why MEAN, exact distinct count and HLL estimation are
not families, the family-relative root reconciles a genuine base for continuation with the refusal of an atomic
fact table, and §5.4 finally turns the pairing prohibition into a recipe.

**Restore the non-minimality sentence and drop *"smallest"* from §7.8.** **Tighten value closure's elaboration
to match its definition.** **Say that MEAN meets the four obligations and fails value closure.**

Nothing else stands between this manuscript and publication revision.
