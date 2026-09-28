# What ToD v8 implies for Frame-QL, MME, and the Columna Platform

**Claude, at Huayin's direction, 2026-09-28.** Doctrine subject:
`attachments/751083b9_theory_of_data_v8_publication_manuscript_v0_18_continuity_completion_candidate.md`
(v0.18; cited as **v8:§/line**). Code subject: this repository at `a667f60`.

**Standing.** Assessment only. **No implementation, no schema change, no ruling.** Every claim below is
quoted at `file:line` and was re-verified against the source after the sweep that produced it.

---

## 1. Verdict

> **Columna has one sort, and it is `family`. v8 has two. Everything else in this note is a consequence of
> that single fact.**
>
> **v8 §7.2 does not merely cover Columna's position — it names it:** *"This is a stricter boundary than
> earlier drafts and **some earlier Manifold design notes, which allowed a derived family to be justified
> either by self-sufficient continuation or by a sufficient-state basis.** Version 8 reserves the family
> category for the former case."*

**The good news is larger than the bad.** v8 closes at least five open ledger rows, settles a doctrine gap
that was explicitly deferred *pending a ruling*, ratifies three of four ruled Cache(r) laws, and **requires no
grammar change at all**. The work is concentrated in one place: resolution and the governed record.

---

## 2. The one finding

`governed/native.py:86` — the complete list of admitted declaration kinds:

```python
ADMITTED_KINDS: frozenset[str] = frozenset({"universe", "family"})
```

`governed/publication.py:18` — *"THE v2 ONTOLOGY. **One family kind** (`family`), covering primitive and
constructed formation and named and query-constructed alike."*

**And v7.1's either/or is not archival — it is executable.** `governed/resolve.py:68-69` carries both
justification routes as siblings of one record:

```python
C7_SUFFICIENT_STATE = "sufficient_state_bases"
C8_CONTINUATION     = "continuation_and_agreement"
```

`resolve.py:113-115` makes `EXPLICIT_NONE` a **settled** standing (*"Established or explicitly none — either
way, not silent"*). So at `resolve.py:296-299`, a family citing a law that *"does not compose across
refinement"* resolves `C8_CONTINUATION = EXPLICIT_NONE`; at `resolve.py:385-389` its `C7` is `ESTABLISHED`
from the basis; and `resolve.py:139-144` reports **valid**.

> **A `Family` record with provably zero continuation, justified only by a SUM/COUNT basis, resolves VALID
> today.** `foundation.py:281-300` is the law that does it: `MEAN` with
> `entails_continuation=NO_CONTINUATION`, `state_basis=StateBasis(("SUM","COUNT"), …)`,
> `usable_as_continuation=False`.

That is precisely the category v8 abolishes, **and there is no second record type to move it into.** This is
the smallest change with the largest blast radius, and it should be scoped first. Two independent sweeps
reached these same lines from opposite directions (the Frame-QL spec, and the Core model).

---

## 3. Manifold

**v8 hands Manifold its schema explicitly.** §8.5 is addressed to this layer by name, lists what a governed
representation may declare — *"universes and anchors; measure families **and their roots**; family laws;
**durable governed expressions**; participation and scope; governed order; sufficient bases; family and
expression lineage; evidence references"* — and concludes:

> *"Version 8 therefore gives Manifold **two distinct reusable analytical classes**: measure family and
> governed expression. The second class is not a lesser form of governance. It simply makes no
> family-continuation claim."*

**What must be added:** a sort discriminator; a declaration kind for durable governed expressions; for
families, a declared root `R_F` and the value-closure claim per admitted edge.

### 3.1 ⚡ v8 reverses a frozen decision — and sides with the code

`R_F` **already exists in the implementation**, correctly, as `constitutive_anchor`
(`governed/publication.py:247`, required field; `native.py:1110`), resolved universe-relatively and **not**
required to be the finest anchor — which is v8 §3.2 exactly. Platform already treats it as the root:
`serving.py:864-867` (*"the state has been established at the CONSTITUTIVE ANCHOR"*).

**Both frozen design contracts deleted it:**

- `columna_semantic_contract_v1_0.md:882` — *"### 3.6 Family root as a separate object — **dies**"*
- `manifold_family_declaration_contract_v1_0.md:472` — *"**family root / \(A_0\)** — **eliminated.** Every
  clause carries its own anchor reference; **a family with two grounding clauses has no single root, and
  needs none**"*

v8 makes \(R_F\) constitutive (§3.2), makes \(F@R_F\) the canonical authoritative family state (§7.7), and
warns that *"root anchor ≠ whatever grain happened to be stored first."*

**And v8 answers the contract's stated reason directly.** §7.6: *"A quantity independently grounded at
incomparable anchors with no available governed common refinement cannot share one family root merely because
the sources use the same business name. For example, Headcount grounded by Department from one source and by
Location from another **constitutes distinct family identities** when neither grounding can lawfully derive
the other or a common root."* Two groundings are **two family identities with a declared agreement
obligation**, not one rootless family. **The code was right; the frozen doctrine needs withdrawing.**

---

## 4. Frame-QL

### 4.1 The grammar needs nothing

`:2808-3043` §15 — precedence, `@` binding, braces, named args, dotted-path disambiguation — is entirely
sort-neutral, and `:3045` §15.7's closed list stands. **The v8 change is wholly in resolution, not syntax.**
The `@`/`AT` architecture is already right: `mean(revenue @ {order}) @ {region}` *is* v8's
`mean_revenue_order@Region` with Order as an identity-bearing constitutive inner anchor.

### 4.2 ⚡ The spec already contains v8's proof and draws the opposite conclusion

`:1199`:

> *"The two exact states `(sum=10,count=1)` and `(sum=1000,count=100)` both display 10, but adding `(20,1)`
> produces 15 and `1020/101`. **Current display agreement is not continuation equivalence.**"*

**That is v8 §3.5's continuation collision, verbatim, in the adopted spec** — and the same document classifies
`mean(revenue @ {order})` as **family-forming** (`:629-636` §3.5, `:1030-1038` §6.1) and calls Order *"a
constitutive input anchor of **the mean-family identity**"* (`:824`). The premise was established and the
conclusion was not drawn. **The argument for v8's reclassification is already inside Frame-QL's own text.**

### 4.3 The spec twice declined exactly what v8 now requires

- `:511` — *"These are properties of the expression and its law, **not disjoint ontological kinds**."*
- `:2768` §11.4 — *"This language revision does not add a Manifold kind, a `DERIVED` syntax, a publication
  field, or a witness type."*
- `:2792` §13 — *"distinguish analytical-point-order dependence, family-law admission, **retained value/state
  capability**, and the operation a representation is licensed to perform next. **These distinctions do not
  require four new registry columns.**"*

v8 promotes **retained-state capability to the primary sort discriminant**. §13 is the claim v8 most directly
unseats, and it should be revisited rather than quietly overtaken.

### 4.4 The conditional identity is half-built and wired to the wrong question

v8 §8.6: `Op(F@A)@B` is **first an expression**, and becomes `F@B` only when `Op` is the admitted family
relation — *"`SUM(Revenue@Day)@Month ≡ Revenue@Month` **when that edge is admitted**"* — while
*"`SUM(exact_unique_customer_order@Store)@Region` means the sum of store-level unique counts. **It is not
regional exact unique count**."*

`planner.py:1616-1622` already tests almost exactly v8's condition: *"it licenses the collapse only when the
outer reducer IS the member doing the inner delivery."* But:

- it is consumed only for pin-collapse and clarify-count, **never to establish a family reference**;
- it is keyed on an **unconditional operator flag** (`operators.py:67`; only `sum` is `True`), and
  `operators.py:96-99` *forbids* conditional certification — *"If type, order, support or anchor conditions
  would qualify the certification, the case must NOT be flattened into True"*. **v8 §3.5 admits a case this
  permanently refuses**: MEAN *is* value-closed *"where the averaged population is a declared governed
  geometry with total participation."*
- `_resolve_inline_reduction` (`planner.py:2850-2926`) always reduces to the frame anchor with a `TRANSPORT`
  caveat. There is no branch resolving to `F@B`, and none marking a composed expression with no continuation
  rights.

**The structural point: v8 turns query rewriting from an algebraic question into a declaration lookup.**
Whether a rewrite is legal depends on which **sort** each name resolves to and, for families, whether **that
specific edge** is admitted. Neither is derivable from the operator.

### 4.5 The promotion apparatus is the doctrine, not an accident

ADR-036, `specs/context/adr_036_generated_family_law.md:39` — *"**Family generation creates a new analytical
family.** It does not create a new operator permission."* Shipped into the language
(`docs/frame_ql_language.md:991`), enforced at `planner.py:2008-2015`, and stated in the registry
(`operators.py:143` — *"`mean` … **GENERATES an analytical family**"*). v8 §3.7 denies the premise.

`DERIVED … FAMILY { <member> FERTILE {…} }` (`parser.py:398`, `model.py:204-215`) is a literal `E ⇒ F`
surface. **One nuance worth keeping:** `adjudication.py:_prove_math` demands a homogeneous linear form — that
is a genuine value-closure argument and is v8-defensible. It is `_prove_data`'s `CORROBORATED` path that must
go, against v8 §7.4: *"Agreement between two wrong bases does not establish correctness."*

---

## 5. MME / Cache(r)

No MME has shipped (ledger **P5-01**). The ruled laws fare well, with one correction.

| Ruled law (Huayin, 2026-07-14) | v8 verdict |
|---|---|
| *"a cache hit may never change the quantity asked"* | **Ratified and grounded.** §7.6: *"identity determines required agreement; agreement does not determine identity."* v8 grounds it in **identity**, not in pre-filtering the store — a stronger guarantee that survives the cache holding expression results. |
| *"a cache hit is a theorem application"* | **Ratified, and the theorem is named**: Proposition 6.2 — with six premises the July text does not enumerate, of which 3 and 4 (same root contributions; same participation, formation, multiplicity, scope) are the live ones. |
| *"the fertile is cached as components first"* | **Ratified and sharpened.** *"Cache the sketch, never the estimate"* is v8 §5.1 in caching vocabulary. v8 adds an axis July lacks: **anchor authority** — \(F@R_F\) is canonical; non-root caches must stay derivationally consistent with it. |
| *"only the fertile is cached"* | **Contradicted as a prohibition; intent preserved.** §7.7 permits caching **both** sorts and moves the restriction from **admission** to **entitlement**: store anything, but only a value-closed family measure may *seed further travel*. **The shipped engine already sides with v8 against the July law** — `engine.py:242`: *"Holistic results are reduction-sterile: memoize exact, never as a seed."* |

**What v8 newly requires**, none of which exists today: a **sort tag** on every cached artifact
(`CacheEntry`, `engine.py:60-78`, has none); a **root reference and input anchor** per cached non-root `F@A`
(the cache records only the *output* anchor `target`, so derivational consistency is not merely unchecked, it
is **unstatable**); participation/scope/law parameters in the key; and for ordered families either the witness
in the value or a declined edge (`_order` is dropped at `engine.py:375`).

**One sort error already in a key.** The witness store is keyed `(measure, member, base_level)` where `member`
is the finalizer name `"distinct"` — **family state filed under the identity of the expression it will
become.**

### 5.1 The retraction exposure

**v8 proves combination coherence and nothing about retraction.** Prop 6.2 assumes associativity and
commutativity; there is no inverse, deletion, or maintenance result anywhere in v8 — and v7.1 §10.3's warning
(*"a LAST or MAX witness can forget which point would win after its selected point is removed"*) is one of the
sentences v8 dropped (audit §4.6).

The conflation is stated in-tree: `two_pillars_strategy_note_v0_4.md:166-167` — *"**Sketches are the cache's
algebra**… mergeable partials **ARE the incremental cache**."* `hll_union` has no inverse.

**No live bug.** Shipped code is safe by whole-token invalidation (`engine.py:154-165`) and witness rebuild;
the July design specifies invalidate-and-propagate, not delta maintenance. **The exposure arrives with the
first append/delta optimization or the first shared cache layer** — which is exactly when nobody will be
re-reading this.

---

## 6. What v8 closes

| Open item | What it asked | v8's answer |
|---|---|---|
| **DG-3** (`planner.py:2110-2124`, held whole 2026-08-20) | `FERTILE` is an equality theorem about the reduce-path; an AT-metric's travel is the opposite — `daily_aov AT day` at month is the **mean of daily rates**. *"There is therefore NO declaration an author could write to permit this travel. Two different concepts wear one name; **separating them needs a ruling, not a patch**."* | **§8.6 is the ruling, using the same case**: *"applying MEAN to monthly mean-revenue values produces mean of monthly means; it is not silently rewritten."* The two concepts are **family continuation** and **composed expression**. The declaration an author could not write is: declare it a governed expression. **DG-3 dissolves rather than needing to be built.** |
| **DG-4 / DG-5** (ADR-036) | generated families have no canonical runtime identity object; open-by-default makes silence permission | They are not families. §3.7. |
| **P5-05** | cache/witness keys cannot be keyed by canonical governed identity | §3.1's fourth obligation supplies the required key content; §3.6 supplies it for expressions. |
| **Reusable-state fork** (`family_law_capability_reusable_state_reconciliation_v0_2.md:462-465`) | Form A (enumerated consumers) vs Form B (declared state semantics) | Dissolved: **a family's required state *is* its value** (§5.1). The carrier becomes a family; its consumers become expressions over it. |
| **The FIRST/LAST family-category question** (three superseded rulings in the authority index) | is FIRST/LAST a family? | **Witness = family, scalar = expression**, by value closure. |

---

## 7. What is already right

This is substantial and should be said plainly before any work is scoped.

1. **Root-only materialization is already the Platform's architecture** (`serving.py:743-749`, `:861-870`).
2. **"A displayed value is not sufficient state" is enforced at four independent points** —
   `state.py:200-206`, `state.py:239-241`, `composite.py:206-208`, `composite.py:286-292` (*always* refuses).
   That is v8 §7.7's hardest rule, implemented, with a named refusal.
3. **The HLL three-operator split is already v8-shaped** — `operators.py:161-165`: two REDUCERs
   producing/merging `HLLSketch` and a MAP projecting `HLLSketch → Int64`. Only the `distinct` wrapper and
   `sketch.py:6`'s framing collapse them.
4. **Naming/aliasing/caching does not mint identity** — the largest area of pre-existing agreement, stated at
   seven places in the Frame-QL spec and matched in `envelope.py:108-122`.
5. **Want-of-state vocabulary, empty-fiber entailment, anchor geometry, declared participation, family
   succession** all match v8 already (`refusals.py`, `foundation.py:171-190`, `native.py:353-399`,
   `resolve.py:226-233`, `native.py:119`).
6. **`count(order)=100` vs `count(revenue@{order})=97`** is v8 §4.4 exactly, encoded at
   `foundation.py:234-252` with `usable_as_continuation=False` for v8's own reason.

---

## 8. Sequencing, if it is wanted

Not a plan — a scoping order. **No implementation is authorized by this note.**

1. **Add the sort.** A second declaration kind and a three-valued resolved reference sort. Everything else
   depends on it, and §2 is the reason: the invalid record has nowhere to go until it exists.
2. **Withdraw the \(R_F\) deletion** from both frozen contracts (§3.1). Doctrine-only; the code already
   complies.
3. **Reclassify**: MEAN/AOV/rate/margin/`distinct`/estimate/variance to the expression layer; `HLLSketch`,
   `DistinctSet`, moment state and the ordered witness to the family layer. Retire the `sketch.py:6` framing.
4. **Re-key the resolver** on the declared family edge rather than the unconditional operator flag (§4.4),
   which also admits the geometry-weighted MEAN case v8 allows and Columna currently cannot express.
5. **Expression succession** (§7.3's other half) — an AOV gross→net redefinition is currently untracked.
6. **MME**: sort tag, root reference, input anchor in the key — before any delta/append optimization.

**And one caution carried from the omission audit:** v8 itself still owes a coherence result for ordered
families (§6.4 excludes them from Proposition 6.2 and never supplies the replacement). Anything Columna builds
on ordered-witness continuation is building ahead of the published theory.
