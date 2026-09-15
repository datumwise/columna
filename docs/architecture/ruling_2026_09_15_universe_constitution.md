# Ruling — 2026-09-15 — a universe is constituted; Case-S coordinates and anchors are derived from that constitution

**Status:** **DRAFT FOR REVIEW.** Recorded by Claude at Huayin's direction, 2026-09-15. **Not
ratified. Not implemented. No source change is authorized by this document.**

**What it continues.** `ruling_2026_09_14_anchor_identity.md` §6 left one question explicitly open:

> *"What determines that an anchor `A` is a particular governed partition of `U` is therefore an open
> ONTOLOGY question, to be answered from ToD v7.1 and Frame-QL 1.0 before any schema is considered."*

This ruling answers that question. It answers it by **denying the shape the question was asked in**.
There is no relation to be established between an anchor and a universe, because for the ordinary
case there are not two objects to relate.

---

## 0. The correction this ruling records

The reconnaissance that preceded this document proposed an `anchor → universe` relation as the
missing constitutional link. **That proposal was wrong, and it is withdrawn here.**

A relation presupposes two independently existing relata. But a partition is not an object that
exists on its own and is later attached to a set: **a partition is a structure *on* Ω_U, and its
domain *is* Ω_U.** There is no free-floating `store` partition waiting to be related to `sales`.
Asking "which universe does this anchor belong to?" is asking which set a structure-on-a-set is a
structure on — a question that is already answered, or else the structure was never well-formed.

The gap on `main` is therefore **not** a missing edge in the publication graph. It is that **the
universe constitution itself is absent**: the publication never states what makes a root point of
`sales` exist or by what governed primitives one is individuated, so there is no Ω_U for any
partition to be a partition *of*. The dangling anchors are a **symptom**; the absent constitution is
the **defect**.

---

## 1. Ruling 1 — a governed universe constitutes an analytical world

> **A governed universe `U` constitutes an analytical world. Its constitution must make determinate:**
>
> 1. **the identity of the analytical world;**
> 2. **its primitive root-point individuation — the governed primitive coordinates / analytical
>    inputs by which a root point is individuated;**
> 3. **its existence law `λ_U`, which determines which such root points exist.**
>
> **`Ω_U` is determined by that constitution. It is not separately enumerated.**

`Ω_U` is fixed by determination, not by extension. ToD states `Ω_U` by law and never lists it:
*"A universe `U` has a governed root-point domain `Ω_U` under an existence law `λ_U`. The law answers
what makes a root point exist in this analytical world"* (ToD v7.1 §2.1.1). The governing standard
throughout is **explicit and internally resolvable** — a constitution must *determine* its world; it
need not *enumerate* it, and a publication that enumerated it would be recording evidence, not law.

Two consequences bind immediately.

**1a. The root anchor `R_U` and the scalar anchor `{}` are derived, never authored.**
`R_U = {{ω} : ω ∈ Ω_U}` (ToD v7.1 §2.1.1) is a *theorem* of the constitution. `{}` is *"the coarsest
one-point anchor of the selected universe"* (Frame-QL 1.0 §4.5). Neither may be declared, and an
authoring surface that accepts a declaration of either is accepting a statement that cannot be false
and cannot be authoritative.

**1b. Event-like and spine-like universes are not two kinds.** *"Event-like and spine-like domains
are forms of the existence law, not additional top-level ontological kinds"* (ToD v7.1 §2.1.1). The
constitution therefore needs **one** law slot, not a kind discriminator; occurrence-based and
declared/generated laws differ in what `λ_U` says, not in what a universe is.

**1c. The root is world-relative, not physical.** *"The root is relative to the declared analytical
world. It need not be the finest description possible in physical reality… Primitive dimensions and
analytical inputs are governed starting facts in that universe; the theory does not infer them from
physical naming conventions"* (ToD v7.1 §2.1.1). A universe's primitive individuation is therefore an
**act of governance**, and may never be read off a table's grain, a primary key, or a column list.

---

## 2. Ruling 2 — Case S: a primitive coordinate is a governed constituent of the individuation

> **A primitive coordinate such as `store` is a governed constituent of the universe's root-point
> individuation. It must NOT be described as a free-standing partition subsequently related to a
> universe.**
>
> **For a primitive coordinate `c`, its placement on `Ω_U` is the coordinate projection determined by
> the universe's individuation. Its anchor is the fiber partition of that projection.**
>
> **Therefore its totality, single-valuedness, covering and disjointness are CONSEQUENCES of the
> universe constitution, not separately authored anchor claims.**

If the constitution individuates a root point of `sales` by the tuple `(store, day)`, then the map
`π_store : Ω_U → Dom(store)` exists by construction — every root point has exactly one `store`
because that is what it means for `store` to be a constituent of its individuation. The fibers
`π_store⁻¹(v)` are nonempty blocks that are pairwise disjoint and cover `Ω_U`, which is exactly ToD
§2.1.1's anchor law. **The anchor `{store}` is therefore proved, not claimed.**

This is why the four properties must never again appear as authored assertions. An authoring surface
that asks the author to assert *"store is total over sales"* is asking them to re-state a theorem,
and — worse — creates a surface on which they can state it **falsely**, producing a publication that
is internally inconsistent in a way no gate can adjudicate.

### 2a. The limit clause, stated so it cannot be misread

> **Case S requires no independent constitutive act for the coordinate BEYOND the universe's own
> constitution.**

This ruling deliberately does **not** say "zero facts per coordinate." That phrasing would license a
mechanical promotion of physical fields into coordinates, which ToD §2.1.1 forbids in terms
(*"the theory does not infer them from physical naming conventions"*).

A primitive coordinate **does** carry governed constitutive content — at minimum its governed
name/reference, and whatever value-domain / individuation semantics the world requires. That content
is constitutive. What the ruling denies is that it is **separate**: it is authored **inside the
universe's constitution, as part of the individuation**, and not as an independent object that is
afterwards linked. One act, one place.

---

## 3. Ruling 3 — compound anchors are derived common refinements

> **Given governed constituent partitions of ONE universe, compound anchors are their governed common
> refinements, and are DERIVED.**

ToD v7.1 §2.1.3: *"A compound anchor is a governed common refinement… its points are the nonempty
intersections of their blocks over the declared universe."* Frame-QL 1.0 §4.5: `{customer * cal.month}`
*"does not mean a full Cartesian product. It denotes the governed common refinement of its constituent
partitions over the selected universe. Only analytical points that exist under that universe law
belong to the anchor."*

Hence, **if the root-point individuation of `sales` is exactly `(store, day)`, then**

```
    {store * day}  =  R_sales
```

**and that equality follows from the constitution. It is not established by an anchor declaration,
and no declaration is entitled to assert or to contradict it.** The injection `q : S ↪ ∏Aᵢ` of ToD
§2.1.3 is into, not onto, precisely because `λ_U` — not the product — decides which combinations
exist. Sparsity is thus a consequence of the law, never a defect of the anchor.

---

## 4. Ruling 4 — Case G: where derivation fails, the placement itself is the governed primitive

> **Where a placement is NOT derivable from the primitive individuation, the additional governed
> primitive is the placement / construction ITSELF.**
>
> **If that placement is total and single-valued over `Ω_U`, its fibers determine a Case-G
> partition.**

This is the honest residue. `region` is not a constituent of `(store, day)`; a construction —
whatever governs store-to-region placement — is what must be authored, and the partition follows from
*it* by the same fiber argument as Case S. The object authored is the **placement**, not the anchor;
the anchor remains derived.

**The Appendix-D distinctions are preserved intact and must not be collapsed by any authoring
convenience** (ToD v7.1 §2.1.3, Appendix D):

| construction | what it does | what it is NOT |
|---|---|---|
| **assignment** | may establish a single-valued partition **in the same universe** | not automatic from a relationship |
| **membership-universe construction** | establishes a **different universe**, in which each membership is a distinct point | not a partition of the original `Ω_U` |
| **allocation** | a **contribution law** (conserved) | **not a partition** |
| **full-touch expansion** | a **contribution law** (deliberate repetition) | **not a partition** |

ToD Appendix D: *"An overlapping relationship does not automatically induce a partition… A
relationship's existence alone is not permission to repeat and aggregate contribution."* Allocation
and full-touch therefore may **never** be modelled as anchors, and a Case-G authoring object that
accepted them as partitions would be unsound at the first row.

---

## 5. Ruling 5 — names resolve governed structure; they do not constitute it

> **Coordinate and anchor expressions RESOLVE governed structure. They do not CONSTITUTE it.**
>
> **The same visible `store` in `sales` and in `inventory` resolves against different universe
> constitutions. The resulting partitions are therefore universe-relative. Equality across those
> universes is NOT ordinary anchor equality.**

This is the 2026-09-14 ruling's universe-relative structural identity, now given its ground: the two
`store`s are different partitions not because they were declared twice, but because they are fibers
of projections of **different individuations of different worlds**. Frame-QL 1.0 §2.7 already
legislates the consequence: the same visible `AT {store * cal.day}` in two universes *"does not claim
that the two `{store * cal.day}` anchors are one ToD anchor. Anchors are partitions of their own
universes,"* and juxtaposition *"aligns analytical results for presentation while preserving each
series' universe."* The union of output coordinate keys is *"a frame-assembly domain, not a new
analytical universe or anchor."*

Cross-universe sameness of `store`, where it holds, is therefore a **separate governed claim about
two worlds** (of the family of Appendix-D universe passage), not an equality of anchors — and this
ruling does not settle its form.

> **Do NOT introduce an anchor identity token merely to implement this ruling.**

Universe-relativity is obtained by **resolving inside the universe**, exactly as the 2026-09-14
ruling directs (*"The universe is a precondition of resolution, not a component of the identity that
resolution produces"*). If a token is ever justified, it must be justified by an independent
authoring-model demonstration, not adopted as this ruling's implementation reflex.

---

## 6. Ruling 6 — evidence realizes; it never constitutes

> **`unique_at` does not establish a general anchor.**
>
> **For a REALIZATION of a Case-S universe, uniqueness over the FULL primitive individuation tuple
> can evidence faithful root-point individuation.**
>
> **Uniqueness over a PROPER SUBSET does not establish that subset as a coarser anchor. It may
> instead show only that, in the observed material, that subset's fibers happen to be singleton.**
>
> **Evidence never constitutes the universe or the coordinate.**

The discipline is ToD v7.1 §9.1's (*definition, evidence, and realization* are distinct) and §2.1.3's
(*"Two expressions that happen to group current records identically are not thereby analytically
equivalent. Equivalence comes from the governing structure, not an accident of current data"*).

The asymmetry is worth stating plainly because it is the one an implementation will get backwards:
uniqueness over the full tuple is **confirmatory of a realization** of an already-constituted world —
it says this material faithfully represents one root point per row. Uniqueness over a subset is
**mute about law**; in a period when every store has exactly one open day, `unique_at(store)` passes
and means nothing about whether `{store}` is `R_U`. Also note that uniqueness failure over the full
tuple is likewise not a refutation of the constitution — it is a failure of *this material* to
realize it faithfully, which is a mapping/realization defect, not an amendment to the world.

---

## 7. Conceptual disposition of the present objects

Recorded **without** changing source or serialization. This table states standing, not a migration.

| object | disposition under this ruling |
|---|---|
| `universe` | **Survives.** Its constitution must be **rebased** onto §1: identity, primitive root-point individuation, existence law. |
| `coordinate` | **Survives, rebased** as a **universe-relative primitive governed constituent** of an individuation — no longer a standalone global object. |
| `anchor` **declaration** | **No longer presumed to be a primitive ontological object.** Case-S anchors are **derived** (§2, §3). Whether any declaring act survives at all is an authoring-model question, not a given. |
| `anchor.components` | Its useful **coordinate-description content may survive**. Its **current container has no constitutional authority** — components of a declaration are not thereby constituents of an individuation. |
| `universe.body.anchor` | **No semantic role has been established under this constitution.** It must **not** be reinterpreted merely to preserve compatibility, and no replacement meaning is invented here. The 2026-09-14 ruling already forbade reading it as every family's constitutive anchor; this ruling removes the last remaining presumption that it means anything at all. |
| `relationship` | **Survives as governed structural input.** It **does not establish a partition** (ToD Appendix D). It may be an input to a Case-G construction; it is never itself one. |
| `hierarchy` | **Does not constitute refinement.** Refinement is derived from governed partitions (ToD §2.1.2 — *"A physical join does not supply a missing partition projection"*). Existing hierarchy evidence may still have another lawful role; **this ruling does not settle what that role is.** |
| `Declaration.identity()` | **The mechanism may survive.** But **physical gate subjects must not define analytical identity** — identity that varies with a table/column binding is a physical key wearing an analytical name (ToD §2.2: *"A physical key may represent the point; it does not define the point's analytical standing merely by being unique in a table"*). |

---

## 8. Recorded witness — the ratified law does not include root-point individuation

Run against the shipped `elf-1` machinery and the shipped universe (`manifold-agent` @ `1b76a8c`,
v0.13.2). Baseline universe fingerprint payload:

```python
{'fingerprint_version': 'elf-1', 'anchor': 'sale_at', 'basis': 'events',
 'restriction': [], 'dependencies': {}}
```

| mutation applied to the anchor named by `universe.body.anchor` | universe fingerprint changed? |
|---|---|
| rename component `store` → `outlet` | **no** |
| retype component `store` `text` → `integer` | **no** |
| **delete** the `day` component outright | **no** |
| *control:* `basis` `events` → `spine` | **yes** |
| *control:* rename the universe's `anchor` **string** `sale_at` → `other_at` | **yes** |

The controls matter as much as the mutations. **Renaming the pointer stales the law; deleting what
the pointer points at does not.** The fingerprint is sensitive to the anchor's *spelling* and blind to
its *structure* — which is the exact inversion of ToD §2.1.3's *"The anchor expression and the
partition it denotes should also remain distinct."*

**This is evidence that the currently ratified law does not constitutionally include root-point
individuation.** Deleting a constituent of what is supposed to be the world's individuation leaves
the universe's ratified fingerprint bit-identical, so ratification today certifies something that is
silent about what the world's points are. Note precisely what the witness does and does not show: it
shows the **fingerprint payload carries a name, not a structure** (`'anchor': 'sale_at'` is a string;
nothing the string refers to enters the digest). It does **not** show that any particular field is the
right place to put individuation — see §9.

**The witness is not an accident of the fixture; it is structural.** `dependencies` is built only from
`_law_reference_paths(universe)`, which walks *"the logical reference paths a universe's restriction
depends on"* — the `restriction` operands and nothing else
(`src/manifold_agent/ratification.py:77-88`, `:90-116`). The anchor's components are never consulted
on any path into the digest. So no anchor mutation whatsoever can stale a universe's law under
`elf-1`, for any universe, by construction — the empirical rows above merely exhibit what the payload
builder already guarantees (`src/manifold_agent/ratification.py:155-161`).

---

## 9. What this ruling does NOT settle

Recorded so that no implementation settles them by convenience.

- **The authoring representation.** No field names, no kinds, no schema, no serialization. The
  smallest authoring model capable of expressing §1–§6 is the subject of the accompanying
  reconnaissance, and that reconnaissance does not itself authorize a change.
- **Whether `universe.body.anchor` survives in any role.** No replacement meaning is invented.
- **Whether an anchor declaration survives** as a naming/description act once it is no longer
  constitutive.
- **Whether universes or anchors require opaque identity tokens.** Not decided here, and not to be
  decided as a side effect of implementing this ruling.
- **The form of cross-universe coordinate sameness** (§5) and of universe passage.
- **The lawful residual role of `hierarchy` evidence** (§7).
- **Publication v2.x / v3.** Untouched.
- **P1-33, P1-34, Proof B, Proof C, OF-56, OF-58, persistence, SSE, reuse.** None is repaired,
  advanced, or implicated.

## 10. Doctrine relied on

| claim | source |
|---|---|
| `Ω_U` is governed under an existence law `λ_U`; `R_U = {{ω}}`; an anchor is a governed partition of `Ω_U` with disjoint covering blocks | ToD v7.1 §2.1.1 |
| event-like / spine-like are **forms of the existence law**, not ontological kinds | ToD v7.1 §2.1.1 |
| the root is world-relative; primitive dimensions are **governed starting facts**, not inferred from physical naming | ToD v7.1 §2.1.1 |
| refinement/projection defined **only for anchors of the same universe**; a physical join supplies no projection | ToD v7.1 §2.1.2 |
| a compound anchor is a **governed common refinement**; the universe law decides which combinations exist | ToD v7.1 §2.1.3 |
| expression ≠ partition; equivalence comes from governing structure, not current data | ToD v7.1 §2.1.3 |
| a physical key does not define analytical standing by being unique in a table | ToD v7.1 §2.2 |
| assignment / allocation / membership universe / full-touch are distinct governed constructions; a relationship is not permission | ToD v7.1 §2.1.3, Appendix D |
| definition, evidence, and realization are distinct | ToD v7.1 §9.1 |
| *"Anchors are partitions of their own universes"*; cross-universe juxtaposition is frame assembly, not a shared universe | Frame-QL 1.0 §2.7 |
| `{A * B}` is governed common refinement, not Cartesian product; `{}` is the coarsest anchor, distinct from `R_U` | Frame-QL 1.0 §4.5 |
| a Manifold supplies a **versioned governed analytical model**; physical bindings do not become authored analytical law | Frame-QL 1.0 §1.3 |
| anchor identity is **universe-relative structural identity**; the universe is a precondition of resolution | `ruling_2026_09_14_anchor_identity.md` §1 |
| `universe.body.anchor` must not be enforced as every family's constitutive anchor | `ruling_2026_09_14_anchor_identity.md` §2b |
