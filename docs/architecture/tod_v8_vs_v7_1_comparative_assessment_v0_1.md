# Comparative assessment — *The Theory of Data* Version 8.0 (v0.14) against Version 7.1

**Claude, at Huayin's direction, 2026-09-28.** Subjects:
`attachments/d777b3f6_the_theory_of_data_v7_1_zenodo_22649945.md` (published, Zenodo 22649945, 1,471 lines /
140,001 bytes) and
`attachments/fe91af9d_theory_of_data_v8_publication_manuscript_v0_14_review_candidate.md` (2,082 lines /
73,087 bytes).

**Standing.** Evaluation of the two theories against each other, read from both source texts rather than from
v8's own §9.2 continuity claims. **No implementation. Neither manuscript is rewritten.** Companion to
`tod_v8_publication_manuscript_referee_report_v0_5.md`, which reviews v0.14 on its own terms.

---

## 1. Verdict

> **v8 is the better theory, and the improvement is explanatory rather than merely editorial: v7.1 tells you
> what you may not do, and v8 tells you what to build. The family/expression split is the right cut, and value
> closure earns its place by explaining a class of prohibitions v7.1 could only enumerate.**
>
> **v8 is 52% of v7.1's length. Most of the difference is prohibition that value closure now entails, which is
> real compression. But some of it is worked counterexamples, and one loss is doctrinal: v7.1 had family
> succession and v8 does not.**

**v8 should supersede v7.1.** Three things should be carried forward before it does.

---

## 2. Where v8 is better

### 2.1 The family/expression split resolves a genuine overload in v7.1

`sufficient-state` appears **40 times** in v7.1, and the phrase *sufficient-state family* does two different
jobs that v7.1 never separates:

- a family whose **value is structured continuation state** — the FIRST/LAST witness family of §8, the retained
  point-value basis of §8.6;
- a **durable quantity justified by a basis** — the derived measures §5 admits, whose displayed value does not
  carry continuation.

v7.1 §5's title — *"Sufficient state remains ordinary analytical data"* — is a defensive claim, and the chapter
is organized around refusing to let sufficient state become a new ontological kind. **v8 keeps the first job in
the family layer and moves the second to the expression layer**, which is why `sufficient-state` drops to 2
occurrences: the term was carrying a distinction that is now structural.

**This is not a renaming.** It changes what can be claimed. In v7.1, a durable derived measure could be a
family on the strength of a sufficient basis, and the consequences of that had to be fenced case by case. In
v8 it cannot, so the fences are unnecessary.

### 2.2 v8 is constructive where v7.1 is prohibitive, and this is measurable

Count v7.1's section titles of the form *X is not Y* or *X does not Z*: §3.6, §3.8, §5.5, §5.8, §6.3, §7.3,
§9.3, §9.4, §9.6, §10.3, §10.4, §10.5, §10.6, §10.7, §11.3. **Fifteen sections whose headline is a
prohibition.** They are all correct. But a theory whose chapter titles are mostly refusals leaves the reader
without a procedure.

**v8 has one place where a prohibition became a recipe, and it matters more than its length suggests.** v7.1
§5 and v8 §5.5 both state that an analytical law cannot use a relationship that was neither retained nor
reconstructed — the weighted-mean \(w_ix_i\) pairing case. v7.1 stops there. **v8 §5.4 makes
\(Count, SumX, SumX^2, SumXY\) value-closed families and statistics expressions over them**, so the pairing is
formed at the root and covariance and correlation *cannot* destroy it. The prohibition is discharged by
construction rather than by vigilance. That is the difference between a theory you must remember to obey and
one whose shape obeys itself.

### 2.3 The family-relative root is a new result, not a compression

v7.1 has no \(R_F\). Its measures are defined on eligible and supported subsets of an anchor, and the question
of where a family's continuation *begins* is not asked — which is why v7.1 can be read as either requiring an
atomic fact table or leaving the base unexplained.

v8 §3.2 answers it: the root is **relative to the family**, need not be the finest governed anchor, and need
not reach the analytical-point level. With §3.2's *"the root must be sufficient for every family relation the
constitution claims from it"* and *"a coarser materialization … cannot simply be renamed as the family root"*,
plus §3.8's four-way separation of continuation, root formation, evidence provenance and physical computation,
**v8 reconciles a genuine base for continuation with the refusal of a primitive point table.** v7.1 had the
refusal (endnote-equivalent material in §2.1) and not the reconciliation.

### 2.4 v8 puts several v7.1 results in better homes

The contraction is not uniform deletion. Two relocations are improvements on the merits:

- **v7.1 §10.6** (lossy state cannot certify the consistency premise — the \((p,10)/(q,20)/(p,11)\)
  conflict-concealment example) sat in the materialization chapter. **v8 keeps it verbatim in substance inside
  §6.2**, next to the witness merge it constrains. It was never a storage fact; it is a fact about the merge.
- **v7.1 §10.1/§10.5's reuse-compatibility obligation** becomes v8 §5.3's *"Required snapshot, population,
  scope, participation, evidence, or other compatibility relations must themselves be established. **If
  compatibility is unresolved, \(E@A\) has want of state even when every operand is individually
  available.**"* That is stronger than v7.1's version — it names the failure mode as want of state rather than
  leaving it as an obligation — and it belongs with sufficient basis.

### 2.5 The vocabulary is cleaner on the standing distinctions

`eligib*` falls from 15 occurrences to **zero**, which looks alarming and is a rename. v7.1 §2.3 carries
\(E_{F,A}\subseteq A\), \(S_{F,A}\subseteq E_{F,A}\) and \(m_{F,A}:S_{F,A}\to V_F\) — eligibility and support
as sets, the measure defined only where evidence reached. v8 uses **applicability** with `NA`, a total map
\(A\to X\cup\{NA\}\), and **want of state** as a separate condition, with §8.3's five-way evidence list
(*"point existence, applicability, participation, support, or compatibility of reused state"*) preserving every
distinction v7.1 drew.

**v8's is easier to read and v7.1's is more precise about one thing**: v7.1's set formulation makes the
difference between *the measure's domain* and *where evidence reached* visible in the notation, where v8 must
carry it in prose. A trade, not a loss — and v8's §4.3 four-case table (`NA` / \(0\) / known-empty fiber /
want of state) is a better teaching device than anything in v7.1 §2.3.

### 2.6 §3.4's type/authority principle is new and fences a real error

> *"Value type determines possible operations; family declaration and law determine which operation has
> analytical authority."*

v7.1 §3.6 forbids operator geometry conferring family authority; v8 extends the same refusal **down to the
value-type layer** — the fact that an operation exists on strings in software does not give it analytical
authority. v7.1 does not fence this, and the String row is the only place in either paper where the theory
declines to supply a law and says why.

---

## 3. What the contraction cost

### 3.1 ⚡ v8 has family lineage but no family succession — and v7.1 had it

**This is the one doctrinal loss, and v8's own architecture makes it more consequential than it was in v7.1.**

v7.1 §3.9 is explicit:

> *"If an identity-bearing definition changes, the result is a **successor family identity**. … Conversely, a
> change of **constitutive order, participation, or formation** cannot be concealed by retaining the old
> label."*
> *"A change of physical representation, retained basis, or execution route is **not** by itself family
> succession. A change to an identity-bearing target, formation, participation, or declared continuation law
> **is**."*

**v8 defines succession only for expressions.** §7.3 is titled *"Expression identity and succession"*; §7.1
gives **family lineage** as *"the constitutive ancestry of measure families"* and stops. There is no family
counterpart to §7.3. `successor` occurs once in v8, in the expression section.

Three places in v8 need it:

1. **§3.1 permits *fixed identity-bearing parameters* and *constitutive order* as family structure.** The word
   *fixed* is doing the work of an unstated succession rule. What happens when a governed order or a law
   parameter changes is exactly v7.1 §3.9's subject, and v8 does not say.
2. **§7.7 makes the root the single canonical authoritative artifact.** A root whose value closure was
   certified under order \(<_1\) is not certified under \(<_2\) — and v7.1 §10.3 said so directly: *"State
   sufficient under one order need not be sufficient to reselect under another. A law-level version change
   cannot be implemented by merely relabeling old winners."* Under v8's root-only materialization this is a
   sharper problem than under v7.1's, because there is one artifact and it is authoritative.
3. **§7.6's agreement obligation** covers \(F@A\) and \(E@A\) under the same identity. Without family
   succession, *the same identity* is undefined across a law change.

**Carry forward.** A family counterpart to §7.3 — three or four sentences, drawn from v7.1 §3.9 — stating that
a change to an identity-bearing family parameter, constitutive order, participation or continuation law yields
a successor family, while a change of representation, cache or execution route does not. v8 has the pieces:
§7.8 already rules *"if the semantic claim changes, analytical identity changes"* for approximation, and §3.1
already distinguishes identity-bearing parameters. Only the family case is missing.

### 3.2 The worked counterexamples went, and they were the proofs

v7.1 is 140k bytes substantially because it **works examples**; v8 is 73k substantially because it does not.
Two are load-bearing for v8's *own* thesis:

- **v7.1 §10.5.** *"MEAN states \((10,1)\) and \((1000,100)\) both display \(10\). Adding the same new state
  \((20,1)\) gives means \(15\) and \(1020/101\). The equal current results did not retain equal continuation
  information."* **This is the one-line demonstration that a displayed scalar is not continuation-bearing
  state — v8's central claim.** v8 §3.5 asserts the same thing (*"a scalar mean at one anchor does not
  determine the mean at a coarser anchor"*) without exhibiting two states that agree on display and diverge on
  continuation. `1000` has zero occurrences in v8. **The strongest available argument for the family/expression
  split is sitting in the superseded paper.**
- **v7.1 §10.4.** *"combining summaries over \(\{i_1,i_2\}\) and \(\{i_2,i_3\}\) double-counts \(i_2\) unless
  an admitted correction accounts for that overlap. **Algebraic associativity never authorizes unknown
  multiplicity.**"* v8 keeps *multiplicity* as Proposition 6.2 premise 4 and keeps §5.5's \(\{0,6\}\) multiset
  example, so the doctrine survives; the sentence that tells a reader why the premise is there does not.

**Carry forward.** Both examples, at roughly two sentences each. The MEAN one belongs in §3.5 immediately
after the three per-case reasons; it converts that section from a classification into a demonstration.

### 3.3 The idempotence/overlap discussion was dropped in the revision that added three idempotent laws

v7.1 §10.4's second half:

> *"Witness extrema and set union are **idempotent** on coherent identical contributions. This can support
> stronger reuse in a particular admitted law. **It does not give every family permission to deduplicate, mix
> inconsistent copies, or disregard contribution provenance.**"*

`idempoten*` : v7.1 **3**, v8 **0**. Meanwhile v0.14's new §3.4 table admits **DistinctSet under \(\cup\),
Boolean ANY under \(\lor\), and Boolean ALL under \(\land\)** — three idempotent laws — and lists them beside
additive numeric and Count, which are not overlap-tolerant, with no remark that the rows differ in this
respect.

Formally v8 is safe: Proposition 6.2's proof partitions the contributing root points, so overlap is excluded
by premise. **The exposure is that the table invites a reader to reason about their own law by analogy with a
neighbouring row, and overlap-tolerance is precisely where the rows disagree.** This is the same failure mode
as finding 4.1 of the v0.14 referee report — §3.4 admitted new laws and the surrounding doctrine was not swept
— and the two remedies belong together: **empty-fiber behavior and overlap behavior are the two places where a
law's algebraic character has analytical consequences, and v7.1 discussed the second while v8 discusses
neither.**

### 3.4 The completeness requirement on governed order was dropped while the witness merge still needs it

v7.1 §7.3: *"Two distinct analytical points of \(S\) are distinguished by its **complete** governed order."*
`complete order` : v7.1 present, v8 **zero occurrences**. v8 §6.1 requires instead that the order *"must
compare the participating points of \(S\) **whose relative position matters to the law**."*

But v8 §6.2's witness merge is a three-case split —

\[
(s,x)\oplus(t,y)=
\begin{cases}
(t,y),& s<_St\\
(s,x),& t<_Ss\\
(s,x),& s=t
\end{cases}
\]

— which is **exhaustive only if \(<_S\) is total on the participating points of the fiber.** Two distinct
incomparable points fall through all three cases and \(\oplus\) is undefined; \(\max_{<_S}D_A(a)\) in the LAST
definition need not exist even for a finite nonempty fiber; and the associativity argument
(*"every finite compatible set has the same governed extremal point"*) presupposes a unique extremum.

A charitable reading recovers what is needed — for fiber-relative LAST, every pair's relative position
arguably *does* matter — so **the theory is recoverable, not broken.** But v7.1 stated the premise and v8
leaves it to be inferred from a definition that depends on it.

**Carry forward.** Restore completeness as a requirement on \(<_S\) over each contributing fiber's
participating points, or state the three-case merge's totality premise where the merge is given. v8 correctly
keeps the rest of §7.3 — *"Physical row order, insertion order, sort stability, or an arbitrary backend
tie-breaker do not acquire analytical authority"* — so only the completeness clause is missing.

### 3.5 Smaller items, defensibly dropped

- **v7.1 §5.8 / §10.5's refusal of the information quotient** (3 → 0). A positioning statement about
  unpublished Measure Algebra drafts. v8 §9.2 handles MA continuity differently and better, by naming the
  rename (*sufficient state* → *continuation state*). No reason to carry this.
- **v7.1 §11.4 general focal expressions** (`focal` 4 → 0) — subsumed by v8's expression layer, which is
  strictly more general.
- **v7.1 §3.3 contextual formation** (7 → 0) — the substance is in v8 §6.3's non-commuting edges and §7.6's
  identity-relative agreement.
- **v7.1 §10.7's three-row materialization record table** (retained content / established claim / supported
  use). v8 §7.7 has no operational record obligation. Arguably *more* relevant under root-only materialization,
  but it is closer to a governance contract than to foundational doctrine, and v8's §1 rule —
  *"keep a distinction in the foundation when it changes analytical identity, derivability, consistency, or the
  validity of those claims; otherwise treat it as a contract"* — licenses moving it out. **Consistent with
  v8's own stated scope discipline.**
- **v7.1 Appendix B's nine-part compact formal summary** → v8 §9.3, about a page. v7.1 was more usable as an
  implementer's reference. This is the clearest case where v8 traded reference value for readability, and it is
  a reasonable trade for a publication.

---

## 4. The compression, assessed

| | v7.1 | v8 (v0.14) |
|---|---|---|
| Bytes | 140,001 | 73,087 (52%) |
| Chapters | 14 + 4 appendices | 9 + endnotes |
| Named propositions | Propositions in §6, §8 (incl. 8.1, 8.2) | 6.1, 6.2, 6.3 |
| Prohibition-titled sections | ~15 | ~3 |
| Constructive recipes | 0 | 1 (§5.4 moment families) |

**The contraction is mostly honest.** v7.1's bulk is concentrated in chapters 5, 8, 10 and 11 — sufficient
state, FIRST/LAST, materialization/reuse, and the law catalog — and v8's family/expression split makes much of
chapters 5 and 10 unnecessary rather than merely shorter: once a displayed scalar *cannot* be a family, the
long list of things a displayed scalar must not be asked to do collapses.

**Where it is not honest is examples.** v8 retains nearly every *rule* and drops most *demonstrations*. For a
publication that is a defensible editorial choice — except for §3.2's two cases, where the demonstration was
the argument for v8's own central claim.

---

## 5. Recommendation

**v8 supersedes v7.1 and should be published as a re-foundation.** It is a better theory by the standard that
matters: it explains a class of failures v7.1 could only prohibit, and its architecture discharges obligations
that v7.1 left to the reader's vigilance.

**Three things to carry forward from v7.1 before it is superseded:**

1. **Family succession** (v7.1 §3.9, and §10.3's order-version corollary). The only doctrinal loss, and v8's
   root-only materialization raises its stakes.
2. **The two worked counterexamples** — MEAN \((10,1)\) vs \((1000,100)\), and the \(\{i_1,i_2\}/\{i_2,i_3\}\)
   overlap double-count. The first is the best available proof of v8's own thesis.
3. **Completeness of the governed order** (v7.1 §7.3), which v8 §6.2's three-case merge silently requires.

The idempotence remark from v7.1 §10.4 should be folded into whatever repair §3.4 receives for the
empty-fiber gap, since both are consequences of admitting laws whose algebraic character the surrounding
chapters were not swept for.

**None of the three is a foundational objection.** All three are v7.1 material that the re-foundation passed
over, and each is a few sentences in a paper that has room for them.
