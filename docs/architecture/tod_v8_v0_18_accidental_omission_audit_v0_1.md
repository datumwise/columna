# Accidental-omission audit — v7.1 → *The Theory of Data* v8.0, revision v0.18

**Claude, at Huayin's direction, 2026-09-28.** Subjects:
`attachments/751083b9_theory_of_data_v8_publication_manuscript_v0_18_continuity_completion_candidate.md`
(2,216 lines / 82,918 bytes) with `attachments/889cdfe4_tod_v8_v0_18_revision_note.md`, audited against
`attachments/d777b3f6_the_theory_of_data_v7_1_zenodo_22649945.md` (published, Zenodo 22649945, 1,471 lines /
140,001 bytes).

**Question asked.** *What, if anything, remains doctrinally present in v7.1 that v8 has accidentally omitted
rather than intentionally compressed or superseded?*

**Method.** Full sweep of all fourteen v7.1 chapters and four appendices against the whole of v0.18, with
every claim classified **superseded** / **compressed-or-relocated** / **accidentally omitted**. Findings below
were independently re-verified against both source texts before inclusion; several candidates were
reclassified as superseded and are recorded as such in §6.

**Standing.** No implementation. Neither manuscript is rewritten. Supersedes nothing; companion to
`tod_v8_publication_manuscript_referee_report_v0_5.md` and `tod_v8_vs_v7_1_comparative_assessment_v0_1.md`.

---

## 1. Verdict

> **All five v0.18 restorations land, and two of my v0.14 findings were repaired better than I proposed.**
>
> **The answer to the question asked is a pattern rather than a list. v8's compression systematically kept
> the *uses* of v7.1's apparatus and dropped the *definitions*. There are at least five terms that v0.18 now
> relies on — two of them introduced by this very revision — which the manuscript never defines, because the
> defining passage lived in a v7.1 section that was compressed away.**

**No foundational blocker.** **Everything that concentrates is ordered families.** v8's treatment of
FIRST/LAST inherited the *requirements* and shed the *machinery*: v0.18 restored the completeness premise
while v8 had already deleted the only construction that discharges it (§4.1); §6.4 declares ordered families
out of scope of the one family coherence theorem and never supplies the replacement (§4.12); the compression
theorem that licenses root-only materialization for those families is gone (§4.5); and FIRST itself is never
defined (§4.13). **Four of the five v7.1 chapters audited contributed a finding to this one area.**

---

## 2. The restorations, verified

| Claim | Status | Evidence |
|---|---|---|
| Family succession restored | ✅ | §7.3 retitled *"Family and expression identity and succession"*; l.1601–1612 enumerate identity-bearing family constitution and add the v8-specific corollary: *"A root artifact established under the earlier constitution is not automatically established under the successor constitution and cannot be made so by relabeling."* |
| FIRST/LAST order completeness | ✅ | l.1204: *"complete enough on every admitted contributing fiber… every finite nonempty admitted fiber must have a unique greatest participating point… A merely partial order in which two relevant participating points can remain incomparable does not establish a LAST value."* Scoped **per fiber**, which is better than v7.1's global formulation. |
| MEAN collision restored | ✅ | l.550–578, verbatim numbers, correctly scoped to event-constituted participation. |
| `⊥` known-empty only | ✅ | l.1268: *"Substituting \(\bot\) for an unavailable witness can otherwise produce a definite FIRST or LAST result that the evidence does not warrant."* **This is a new soundness result, not a v7.1 carry-forward.** |
| Idempotence note | ✅ | l.459–473, with the right fence: *"Idempotence is a property of the continuation law, not permission to duplicate or discard participation."* |

**Section structure is otherwise identical to v0.14** — the only heading change is §7.3's retitle — and every
sentence this report series has tracked survives. The restorations were made in place, cleanly.

**Two v0.14 findings resolved, one better than proposed.** My empty-fiber finding asked that an assertive
monoid identity be admitted per family. §3.4 l.443 does something sharper: it identifies the real defect as
**the identity also being reachable from a nonempty fiber** — *"`true` for ALL, `false` for ANY, \(0\) for SUM,
\(1\) for PRODUCT, or \(\varnothing\) for set union"* — and makes recoverability of the distinction a **value
closure** obligation rather than a side rule. The observation that **Count is the exception** (l.447: a
nonempty participating fiber has positive count, so \(0\) is already unambiguous) is a piece of reasoning I did
not supply. PRODUCT's undefined *"domain and identity conditions"* is now two named conditions (l.455).

---

## 3. The pattern: v8 kept the uses and dropped the definitions

This is the substantive answer. Five terms are load-bearing in v0.18 and undefined in it, each because the
defining passage sat in a compressed v7.1 section. **Two of the five were made load-bearing by this
revision's own restorations**, which is why the pattern is worth naming rather than patching case by case.

| Term used in v0.18 | Where it carries weight | v7.1 definition, now absent |
|---|---|---|
| **formation** | Prop 6.2 premise 4 (l.1427); **§7.3 identity-bearing family constitution (l.1607) — new in v0.18**; §3.8 *root formation* (l.670) | §3.1: *"The formation contract identifies the operand, its constitutive anchor, eligibility, participation, type, and any context that affects its meaning."* `formation contract` 0 |
| **governed equivalence** | **§7.3 l.1610 and l.1623 — new in v0.18**, the escape clause on both succession rules; §7.6 l.1689 | §6.6: the equivalence *"must be a congruence"* \(u\equiv v,\ u'\equiv v'\Rightarrow u\oplus u'\equiv v\oplus v'\), **and** must preserve constructor outputs \(\phi(u)=\phi(u')\). `congruen` 2→0, `state equivalence` 5→0 |
| **the independently specified expression target** | §5.3 Adequacy (l.1079), the obligation the whole basis apparatus is checked against | §5.3/§4: the target is fixed *"through either an independent semantic specification… or a nominated defining construction"*, and *"**the specification must not rely on the assertion that a candidate basis is sufficient**."* `specification` **17→0** |
| **constitutive order** / \(\mathcal O_S\) | §3.1 permitted fixed structure; **§7.3 identity-bearing (l.1604) — new in v0.18**; §6.1–§6.2 | §7.1: constituent orders plus a **precedence permutation**, lexicographic by first differing coordinate, *proved* total. `precedence` **14→0**, `lexicograph` 5→0 |
| **canonical name / reference** | §8.6's resolver trichotomy (l.1979–1985); §7.3's *"cannot be concealed by retaining the old label"* | §2.2: *"A canonical name resolves to one family identity within a governed namespace and version… a resolved analytical reference must be unambiguous."* Boxed \(family\_id\ne canonical\_name\). `namespace` 3→0, `alias` 3→0, `immutable` 5→0 |

**Each is a few sentences of v7.1 text.** None requires reopening v8's architecture.

---

## 4. Accidentally omitted — strong

### 4.1 ⚡ The multidimensional order construction — v0.18 restored the premise and v8 had deleted the discharge

`precedence` **14 → 0**. `lexicograph` **5 → 0**. `constituent order` 3 → 0.

v7.1 §7.1 is a complete formal construction: governance identifies constituent dimensions \(A_1,\dots,A_n\) of
the constitutive anchor \(S\), establishes a complete point order \(<_i\) in each, and a **precedence
permutation** among them; \(<_S\) compares by first differing coordinate; totality and transitivity are
*proved*; and the scope is fenced — *"It is not a mathematical assertion that every possible order on a product
must be lexicographic. No additional order constructors are admitted here."*

**v0.18 §6.1 now states the obligation this construction exists to discharge** — every finite nonempty
admitted fiber must have a unique greatest participating point — **and supplies no way to meet it.** For a
one-dimensional anchor the requirement is trivial. For `{account, day}`, which is v8's own running anchor, it
is exactly the precedence question, and v8 is silent. v7.1 even warned about this case by name: *"Day
chronology within separately governed fixed-Customer contexts does not silently establish Customer priority
across those contexts."*

**Two things raise this above a missing construction.**

- **It is what v7.1 was for.** v7.1 §C.3: *"Version 7.0 categorically placed analytical-point-order-dependent
  operations outside family continuation… **That exclusion is the intentional revision made here.** The
  complete constituent orders and their precedence supply the particular multidimensional order construction
  admitted by this manuscript."* v8 keeps the permission v7.1 won and drops the machinery that earned it.
- **The restoration created the gap.** At v0.14 there was no completeness premise, so nothing was unmet.
  v0.18 states the obligation and leaves it undischarged.

Lost with it: \(\mathcal O_S\) — *"An ordered family **fixes \(\mathcal O_S\) as constitutive law**"* — which is
the object that §7.3's newly identity-bearing *"constitutive order"* refers to; and v7.1 §11.2's precedence-swap
example (Customer-then-Day → 40, Day-then-Customer → 80), **while v8 §6.3 reuses the same three data points**
for the unrelated SUM/LAST non-commutation result. The data survived; the doctrine it illustrated did not.

**Repair.** Restore v7.1 §7.1's construction, or state explicitly that v8 admits any governed order meeting
§6.1's completeness condition and supplies no canonical constructor — in which case say so, because a reader
of §7.3 needs to know what object *"constitutive order"* names.

### 4.2 ⚡ The name ↔ identity doctrine is gone entirely

`namespace` 3→0 · `alias` 3→0 · `immutable` 5→0 · `canonical name` 3→0 · `canonical reference` 2→0 ·
`unambiguous` 1→0 · `\Sigma(F)` 3→0 · `signature` 3→0.

v7.1 §2.2 and Appendix B.2:

> *"A canonical name resolves to one family identity within a governed namespace and version. The immutable
> family identity is not the same object as its human-readable name. A family may have aliases, but a resolved
> analytical reference must be unambiguous. **Two distinct active identities cannot be hidden under one
> ambiguous canonical reference.**"* — with the boxed \(family\_id \ne canonical\_name\).

**All ~14 uses of "name" in v0.18 are negative** — naming confers no standing, an operator name is not an
identity, a function name is not permission to aggregate. **There is no positive doctrine of what a name does.**

**v8 needs this more than v7.1 did, in two distinct ways.**

- **§8.6 requires a resolver to distinguish three reference sorts** (family reference, governed-expression
  reference, composed expression) and warns *"an expression name can be as durable and convenient as a family
  name. The semantic sort, not the surface convenience, determines what continuation and materialization
  rights follow."* v7.1 had **one** sort and a full resolution doctrine; v8 has **two sorts sharing a
  namespace** and none.
- **v0.18's restored succession rule presupposes it.** §7.3's *"cannot be concealed by retaining the old
  label"* — *label* and *conceal* only mean anything if a name can outlive an identity. v7.1 §3.9 supplied the
  missing half in its next sentence: *"A later namespace version may retain a familiar local name while
  preserving the distinction between the old and new immutable identities. **A mere label change need not
  change identity.**"* The restoration carried the prohibition and left the mechanism behind.

Also gone: the single-valued **default completion** rule (*"`revenue` can resolve to an explicit sum-family
construction only where identity and participation agree"*), which is the only thing in either paper governing
short-form references.

### 4.3 ⚡ The congruence obligation on declared state equivalence — and `governed equivalence` is undefined

`congruen` 2 → 0 · `state equivalence` 5 → 0.

v7.1 §6.6 states an obligation it explicitly marks as a **surviving Version 6.1 requirement**: where two
representations are declared semantically equivalent as continuation inputs, the equivalence must be a
**congruence** with respect to \(\oplus\), and must **preserve the outputs of the constructors that rely on
it** \((\phi(u)=\phi(u'))\). *"Literal semantic equality is sufficient; alternative encodings need an
established equality interpretation or admitted conversion."*

**This bites harder in v8 than in v7.1.** v8 §3.3 explicitly permits *"a tuple, set, multiset, sketch, vector,
matrix, or witness"* as one family value, and §3.4's table offers alternative representational forms for the
same continuation law. **And v0.18 made the term load-bearing:** both succession rules now turn on *"unless
**governed equivalence** establishes continuity"* (l.1610, l.1623), and §7.6 l.1689 requires *"a declared
governed equivalence at that coarsening."* The term appears three times as an escape hatch from identity
change and is defined nowhere. The only nearby sentence, l.2045, merely **denies** that a numerical tolerance
is an equivalence relation; it never supplies the standard.

### 4.4 ⚡ The target-specification obligation — v8's adequacy rests on an undefined and unobliged term

`specification` **17 → 0** (the whole word does not occur in v0.18) · `defining construction` 4→0 ·
`nominated` 3→0.

v8 §5.3's Adequacy obligation reads, in full: *"The basis must actually determine **the independently
specified expression target**."* **Nothing in v8 obliges anyone to supply that specification, states the
admitted routes for supplying it, or constrains its form.**

v7.1 §5.3 did all three, and the third is the one that matters:

> *"Every family law must fix that target throughout its declared analytical domain through either an
> independent semantic specification over its governed analytical inputs and participating contributions or a
> **nominated defining construction**… **The specification must not rely on the assertion that a candidate
> basis is sufficient.** A nominated defining construction supplies the reference meaning; alternative
> constructions must establish equivalence to it."*

**v8 closes the basis-side circularity and leaves the target-side circularity open.** *Independent
establishment* constrains the **inputs** (*"established without assuming the target"*); *Well-foundedness*
constrains the **construction** (*"a circular declaration is not a construction proof"*). Neither forbids
**defining the target as whatever the admitted basis computes** — which satisfies every obligation v8 states
and is exactly what v7.1 §5.3 ruled out. The accompanying v7.1 permission — that one construction may both
define the quantity and serve as a basis, provided it is specified without assuming the target — is also gone,
so v8 does not even offer the safe version.

### 4.5 Proposition 8.2 — the extraction homomorphism that licenses v8's own materialization doctrine

v7.1 §8.6 / Appendix B.6:

> **Proposition 8.2 — Witness extraction preserves compatible union.** For finite sets \(X,Y\) of point-value
> pairs from the same coherent instance, under the same complete governed order,
> \(h(X\cup Y)=h(X)\oplus h(Y)\), with \(h(\varnothing)=\bot\).

`homomorph` 0 · `extract` 0 · `point-value` 0 in v0.18, which has Propositions 6.1, 6.2 and 6.3 only.

v8 §6.2 **asserts the construction** — *"At the family root, a witness can be formed from each materialized
root anchor point and its value"* — without the result that the formation commutes with union. **Under v8's
root-only materialization this matters more than it did in v7.1**: §7.7 persists only \(F@R_F\) and derives
admitted non-root measures, and for an ordered family that derivation *is* the extract-then-merge path.
Proposition 8.2 is precisely the theorem that extracting before merging agrees with merging before extracting.
Both objects remain value-closed families under v8, so **the result is still statable in v8's own vocabulary —
it simply is not stated.** §9.2 claims to preserve *"two identity results"*; this is a third that was not
considered.

### 4.6 Mergeability is not deletion-maintainability

`deletion` 3→0 · `invers` 1→0 · `maintain` 1→0 · `retract` 0 · `incremental` 0.

v7.1 §10.3: *"Combining additional compatible contributions is not the same operation as deleting or
correcting a previous winner. **A LAST or MAX witness can forget which point would win after its selected point
is removed.**"*

**More live in v8 than in v7.1.** §7.7 newly sanctions caching non-root \(F@A\) that *"must remain
derivationally consistent with the root"*, and Proposition 6.2 proves only **combination** coherence under
associativity and commutativity. Nothing in v8 tells a reader that an associative-commutative or
witness-extremal law confers **no retraction capability** — which is exactly the assumption an implementer
makes when incrementally maintaining that cache against deletions and corrections. v8's only inversion
statement (l.224) concerns broadcasting a coarse value downward, a different operation.

### 4.7 The overlapping-relationship / partition boundary (v7.1 §2.1.3 and Appendix D)

`overlapping relationship` 3→0 · `full-touch` 3→0 · `membership universe` 3→0 · `assignment` 4→0 ·
`contribution rule` 2→0 · `repeated contribution` 1→0.

> *"An overlapping relationship does not automatically induce a partition. A product belonging to several
> categories may require an explicit assignment, allocation, membership universe, full-touch expansion under a
> declared contribution rule, or another lawful construction… Conserved allocation and deliberate full-touch
> contribution are different laws. **A relationship's existence alone is not permission to repeat and aggregate
> contribution.**"*

v8 defines anchors as governed partitions and covers only the **execution-grouping** half (*"a `GROUP BY` does
not create a family edge"*, endnote 2 on dimension columns). The **relationship** half — the commonest real
case, and the whole catalogue of lawful structural constructions with their differing contribution semantics —
has no counterpart. This is anchor geometry and is orthogonal to the value-closure narrowing, so nothing in
v8's architecture makes it moot. v0.18's new idempotence note covers a neighbouring point (*"not permission to
duplicate or discard participation"*) but not the structural-construction question.

### 4.8 The corrected locality statement — v7.1's own headline correction over v7.0

`contextual` 17 → 1 · `lag` 4→0 · `rolling` 3→0 · `rank` 4→0 · `window` 1→0 · `impossibility` 1→0 ·
`focal` 4→0.

v7.1 §3.4 exists to stop the fiber-local continuation law from being over-read:

> *"This continuation property does not prohibit context in the formation of those states. **No general
> impossibility theorem for lag-, rank-, cumulative-, or rolling-derived families follows from it.**"*
> *"Neither automatic promotion nor categorical exclusion is justified by the function name."*

**v8 §5.2 states exactly the fiber-local composition law that §3.4 guards, keeps the no-automatic-promotion
half (§3.7, §7.2), and drops the anti-exclusion half** — so the manuscript as written invites precisely the
false inference v7.1 was published to correct. Also gone: *"An implementation may faithfully recompute the
original constitutive values from adequate governed evidence. **The restriction is on changing their analytical
formation or context, not on computing them again**"* — which matters more under v8, where root-only
materialization makes *derive again* the normal path and the recompute/re-form distinction decides whether
that is safe for a contextually formed family.

### 4.9 The statistical convention obligations

`supplement` **12 → 0** · `interpolat` 1→0 · `degenerate` 1→0 · `skew` 1→0 · `kurtosis` 1→0. v8's reference
list omits v7.1's statistical extension supplement, and §9.2 never mentions the catalog.

v8 §5.4 correctly rehomes variance, standard deviation, covariance, correlation, regression summaries and
quantiles as expressions over moment families. **What went with the catalog are the per-group contract
obligations**: the variance denominator convention, the quantile interpolation convention, nondegenerate
domains for skewness and kurtosis, admitted square-root and value domains. **These are identity-bearing
parameters** — the category §3.1 admits as fixed family structure and §7.3 now makes a succession trigger — so
v8 requires identity-bearing parameters to be declared while dropping the only place that said which ones the
canonical statistics have. v7.1's *catalog-membership ≠ admission-for-realization* distinction also has no
counterpart; §3.4's *"not a closed catalog"* is a different claim.

### 4.10 A point's placement under an anchor can be unsupported — with a vestigial term left behind

`placement` 0 in v0.18. v7.1 §2.3: *"Evidence about existence can itself be insufficient. **An existing root
point's placement under a particular anchor can also be unsupported.**"* — with the worked case of a lost
transaction record establishing that the transaction occurred while failing to establish its Revenue or Day
coordinate, and the converse: *"no record and no evidence of occurrence does not by itself establish that an
event did not occur."*

v8 §4.2's ordered establishment questions admit *unresolved* for applicability and participation but never for
existence or placement. **Yet v8 §8.3 still refers to *"an inadmissible or unplaceable contribution"*** — a term
whose only grounding in either paper is the sentence that was dropped.

### 4.11 Why the lossy-merge conclusion is unavoidable

v8 relocated v7.1 §10.6's \((p,10)/(q,20)/(p,11)\) conflict-concealment counterexample into §6.2 and kept the
conclusion *"Compatibility must be established outside the lossy combination."* It dropped the reason:

> *"A local equal-point check is not enough… Comparing the two \(p\)-witnesses first finds a conflict;
> comparing one of them with \(q\) first can discard it and conceal the conflict. **An error-reporting rule
> added to lossy merge is therefore not an associative global validator over arbitrary conflicting
> evidence.**"*

Detection is **grouping-dependent**, which is why the fix cannot be pushed into the merge operator. It is
missing exactly where v8 defines the merge's \(s=t\) case as one that *"assumes compatible evidence for the
same source point and value"* — the spot an implementer would bolt on a check.

### 4.12 ⚡ v8 declares ordered families out of scope of its one family coherence theorem and never supplies the replacement

**This is the largest structural gap the sweep found, and v8 says so itself.**

Chapter 6 is titled *"Coherence, order, and **path independence**."* It proves path independence twice:
**Proposition 6.2** for commutative monoid and semigroup **families**, and **Proposition 6.3** for
**expressions** over a sufficient basis. §6.4's scope note then explicitly removes ordered families from the
first:

> *"This proposition establishes the canonical algebraic region of value closure. It does not define every
> family law. **Ordered families, relation-sensitive families, or other stateful laws require their own
> coherence premises.**"*

**Those premises are never supplied.** §6.2 gives the *ingredient* —

> *"The operation is associative and commutative over compatible witness states because every finite
> compatible set has the same governed extremal point regardless of grouping or physical enumeration."*

— and then immediately fences it: *"This does not make LAST a commutative-monoid law on scalar values."*
**The coherence conclusion is never drawn.** `path-independen` occurs four times in v0.18: the chapter
heading, and three times inside Propositions 6.2 and 6.3. Not once for the ordered witness law.

v7.1 drew it, as a numbered result:

> **Proposition 8.1 — Ordered witness families satisfy finite family coherence.** *"Under §8.2,
> \((\mathsf V_{W,f},\oplus,\bot)\) is a commutative monoid. Its admitted finite continuation satisfies
> Proposition 6.1."*

The move v7.1 makes is the one v8 needs: the witness family is a commutative monoid **on its own carrier**
\(\mathsf V_{W,f}\), which is exactly why the general theorem applies to it even though LAST is not a monoid
law on scalars. v8 states both halves of that argument in §6.2 and never joins them.

**So for FIRST and LAST — the law where staged-versus-direct evaluation is most dangerous, and the one this
revision spent a restoration on — v8 has no path-independence result at all.** It is a self-acknowledged gap:
§6.4 promises that these laws need their own premises and the paper never returns.

**Repair.** Restore Proposition 8.1, or state in §6.2 that the witness carrier \((\mathsf V_{W,f},\oplus,\bot)\)
is a commutative monoid and therefore falls under Proposition 6.2 — two sentences, using material already
present in §6.2. This also supplies the missing half of §4.5: with 8.1 giving coherence and 8.2 giving the
compression, the ordered-family story is closed.

### 4.13 v0.18 never defines FIRST

The restored completeness premise is stated for LAST only:

> l.1204 — *"**For FIRST or LAST**, the governed order must be complete enough on every admitted contributing
> fiber to determine the selected extremum. **For LAST**, every finite nonempty admitted fiber must have a
> unique **greatest** participating point…"*

There is no dual clause requiring a unique **least** participating point, and §6.2's merge defines only the
later-wins case \((s<_St\Rightarrow(t,y))\). **FIRST is named four times in v0.18 and specified zero times**
— §3.4's table row (*"FIRST/LAST-like results"*), §6.1's premise, §6.2's `⊥` warning, and §9.2's continuity
recap. v7.1 supplied the dual in one clause each: *"FIRST uses the earlier witness instead"* and *"FIRST is
symmetric."*

**This one is introduced by v0.18**, since the premise it is missing from is new in this revision.

### 4.14 What the witness compression costs — the bound on what "sufficient" buys

v7.1 §8.6 closes the compression result with its price:

> *"Its loss of nonwinning values does not invalidate that adequacy, but **it can prevent later restrictions,
> deletions, or a change of order from being answered**."*

`restriction` 0 · `deletion` 0 · `reorder` 0 in v0.18. This is the general statement of which §4.6
(deletion-maintainability) and the coarsening/restriction item in §5 are the two special cases: **a lawfully
compressed family value is adequate for the continuation it was certified for and for nothing else.** v8 has
edge-relative value closure (l.302) and *"changed constitutive order ⇒ successor identity"* (l.1612), but
never states that a compression lawful under the current law cannot answer a restricted, deleted, or
re-ordered version of the same question.

### 4.15 The two named non-repairs for a collapsing order representation

v7.1 §7.3 names two ways an implementation fakes a complete order, and v8 keeps neither:

> *"Several carrier records contributing to one \(S\)-point are **not several tied analytical points**. They
> first require a lawful, coherent account of the operand at that point."*
> *"If a physical priority value or truncated label maps distinct points to the same comparison
> representation, **that representation has not realized the declared complete point order. Appending a
> storage identifier or relying on sort stability is not a repair of analytical law.**"*

`tied` 0 · `truncat` 0 · `storage identifier` 0. v8 retains only the fragments *"an arbitrary backend
tie-breaker"* (l.1190) and *"a stable sort does not supply governed anchor-point order"* (l.2015).

**This is the companion failure mode to §4.1, and together they bracket the restored premise.** v0.18 l.1204
covers *too little order* — a partial order leaving relevant points incomparable. v7.1 §7.3 covers *false
order* — a representation that looks total because it collapses distinct points. **v8 now states the
requirement, supplies no construction for meeting it (§4.1), and names no test for when a representation only
appears to meet it.**

### 4.16 Intermediate anchors need no new point order

v7.1 §8.4: *"For \(S\succeq B\succeq A\), the witness at \(B\) still identifies the winning **\(S\)-point**.
The next combination uses \(\mathcal O_S\), **not a freshly invented order on \(B\)-point labels**."*

v8's formalism implies this — its witness is a *source* witness and \(\oplus\) compares under \(<_S\) — but
the prohibition is never stated, and it is a live anti-pattern (ordering Week labels rather than the source
Days). Note that the rule is phrased in terms of \(\mathcal O_S\), the object dropped with §4.1.


---

## 5. Accidentally omitted — secondary

- **The converse realization clause.** v7.1 §4.1: *"**Conversely, a backend's inability to realize an admitted
  movement does not remove that movement from analytical law.**"* v8 runs the argument only in the
  execution-confers-no-standing direction (§8.7). `inability` 0, `unable` 0.
- **Coarsening-sufficiency ≠ restriction-sufficiency.** v7.1 §10.2 and B.8: *"Sufficiency for coarsening does
  not imply sufficiency for a later value filter, population restriction, or redefinition of formation."*
  `filter` 0, `restriction` 0, `predicate` 0. Partly covered by value closure being per-edge, but restriction
  is an operation v8 never names.
- **Numerical-realization prohibitions.** *"Deterministic computation alone is not exactness"*; *"Numerical
  stabilization alone does not turn an inexact operation into an exact associative one"*; no *"execution flag
  to replace the statistical meaning of an approximation."* `stabiliz` 0, `flag` 0.
- **Structural conformance is not institutional authority**, and *"query execution must not silently become a
  second, competing declaration validator"* with the stale-assurance prohibition. `conform` 0, `planner` 0,
  `validator` 0. v8 §8.5 states only the converse.
- **Chapter 13's validation-scope disclaimers.** *"not proof-assistant verification, an implementation audit,
  or independently verified peer review… No assertion that all possible defects have been excluded is made
  here"*, and *"the mathematical results do not establish the conformance of a particular type specification or
  analytical engine."* `peer review` 0, `defect` 0, `conform` 0. The specific reference-check counts should
  **not** carry over — v8 needs its own — but the disclaimer package is publication hygiene and its absence is
  conspicuous in a paper that otherwise fences its claims carefully.
- **Explanation/execution fidelity** (v7.1 §12.4) and the **statistical-independence disclaimer** on compound
  anchors (v7.1 §2.1.3). Both small; both have no counterpart.

---

## 6. Judged superseded, not accidentally omitted

Recorded so the question is answered completely, and because each was a plausible candidate.

| v7.1 item | Why it is superseded |
|---|---|
| **The four governance locations** (§1.5: family identity / edge validity / certificate-materialization / metadata) | v8 §1's editorial rule — *"keep a distinction in the foundation when it changes analytical identity, derivability, consistency, or the validity of those claims; otherwise treat it as a contract, consequence, or neighboring responsibility"* — is a deliberate replacement with a simpler cut. Judgment call; flag if you disagree. |
| **The information-quotient refusal** (§5.8, §10.5) | Positioning against unpublished Measure Algebra drafts. v8's normative criterion is value closure, and §9.2 handles MA continuity better by naming the rename. |
| **Universe root anchor \(R_U=\{\{\omega\}\}\)** | §2.1 and endnote 1 explicitly decline to require the singleton partition; \(R_F\) replaces it. Deliberate. |
| **Self-materializable vs materializable-for-a-target** (§10.8) | §7.2 and §9.2 name and retire exactly this dual justification. Deliberate. |
| **TOP-k exclusions, mapper/reducer typing, the graft, \(\Gamma_F\) edge contracts, `R/W/L` symbols** | Operator- and notation-level constructs replaced by the four obligations plus value closure. |
| **\(E_{F,A}\), \(S_{F,A}\), eligibility as sets** | Renamed to applicability / `NA` / support / want of state, with §8.3's five-way evidence list preserving every distinction. |
| **v7.1 §10.7's three-row materialization table** | Rights now follow the semantic sort (§7.7, §8.6). The **justification limb** — that a materialization must carry or reference the establishment record for the claim it embodies — is the part with no counterpart, and is worth one sentence. |

---

## 7. Recommendation

**v0.18 is close.** The restorations are correct, the empty-fiber repair improves on what was asked, and no
tracked sentence regressed.

**Fix the pattern, not the instances.** Five terms — `formation`, `governed equivalence`, *the independently
specified target*, `constitutive order`/\(\mathcal O_S\), and *canonical name* — are used as though defined and
are not. **Two of them were made load-bearing by this revision.** Each definition is a few sentences of
existing v7.1 text and none reopens v8's architecture.

**In priority order:**

**The ordered-family cluster first — it is one repair, not four.** §§4.1, 4.5, 4.12, 4.13, 4.15 and 4.16 all
concern FIRST/LAST, and restoring v7.1 §§7.1–7.3 and 8.1–8.6 closes every one of them:

1. **Propositions 8.1 and 8.2** (§4.12, §4.5) — coherence and compression for the ordered witness law. §6.4
   already promises these premises; the argument for 8.1 is two sentences using material in §6.2.
2. **The multidimensional order construction** (§4.1) — v0.18 states the requirement and deleted the
   discharge; with §4.15, v8 currently gives no construction *and* no falsity test.
3. **Define FIRST** (§4.13) — one clause, in the premise this revision added.
4. **§4.14 and §4.16**, a sentence each.

**Then the four undefined terms:**

5. **Name ↔ identity resolution** (§4.2) — presupposed by the restored succession rule, and needed more by
   v8's two-sort architecture than by v7.1's one.
6. **The congruence obligation** (§4.3) — defines the `governed equivalence` both succession rules now invoke.
7. **The target-specification obligation** (§4.4) — closes the target-side circularity v8 leaves open.
8. **`formation`** (§3) — a Proposition 6.2 premise and, now, a succession trigger.

**Then §§4.6–4.11**, each a sentence or two.

**Everything else in v7.1 is either preserved, relocated to a better home, or genuinely made moot by the
family/expression split.** The sweep found no case where v8 contradicts a v7.1 result.
