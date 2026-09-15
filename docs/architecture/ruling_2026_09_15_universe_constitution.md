# Ruling — 2026-09-15 — a universe is constituted; Case-S coordinates and anchors are derived from that constitution

**Status:** **DRAFT FOR REVIEW.** Recorded by Claude at Huayin's direction, 2026-09-15; **amended the
same day** to incorporate Rulings 7-10. **Not implemented. No source change is authorized by this
document.**

**Standing of the parts.** The document as a whole is a draft awaiting your ratification. **Rulings
7, 8, 9 and 10 (§§7-10) are decisions you issued on 2026-09-15** and are recorded as ruled, not as
proposed. Rulings 1-6 remain draft.

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

## 7. Ruling 7 — λ_U must be determinate

**Ruled by Huayin, 2026-09-15.**

> **A governed universe constitution must make λ_U determinate and internally resolvable: given the
> universe's root-point individuation and the governed premises referenced by the law, λ_U determines
> whether a candidate root point belongs to `Ω_U`.**
>
> **ToD does not prescribe the representation or grammar of λ_U, and determinacy does NOT mean every
> engine must be able to execute it.**
>
> **A classification of the law's form, a physical source/binding, or explanatory prose MAY ACCOMPANY
> λ_U. None of them SUBSTITUTES for the law itself.**
>
> **`events | spine | product | registry` are recorded as existing compatibility vocabulary whose
> eventual standing remains to be determined. They must NOT be promoted into λ_U merely because they
> exist, and they are NOT retired or redesigned here.**

This completes §1. A constitution that fixed an individuation but left existence to prose would
determine the *shape* of a root point and not its *existence*, and `Ω_U` would be undetermined — which
§1 forbids, since `Ω_U` is fixed by determination.

**Determinacy is a property of the law, not of any engine.** ToD §2.1.1 states `λ_U` by formula and
never lists `Ω_U`; Frame-QL 1.0 §1.3 holds that a Manifold's *"analytical definitions are not physical
database bindings."* A law that no current backend can evaluate is still a law. A law that only a
particular table can be consulted to answer is not one — that is a binding wearing the law's name.

### 7a. What this establishes about the present tree — the consequence is total

The universe contract is written in the validator as
*"U = (A_U, basis, restriction, λ-ratification, description)"* and
*"The executable logical existence law is `anchor + basis + restriction` ONLY"*
(`manifold-agent`, `validate.py:77-82`, `:286-287`). Take that apart under this ruling:

| the tree's law content | standing under Ruling 7 |
|---|---|
| `anchor` | names a **derived** object; no constitutional authority (§2, §3, §12) |
| `basis` | a **classification of the law's form**; may accompany, never substitutes |
| `restriction` | a **modifier** — it narrows a population it presupposes; it does not determine membership outright |
| `law_description` | prose; *"NO executable authority"* by the validator's own words (`validate.py:286-288`) |

**Nothing in the present universe body is λ_U.** The corrected constitution therefore does not *rebase*
an existing field onto the existence law; it introduces a governed object the model has never had.

**The sharpest case is the spine universe, and it is witnessed.** For the shipped spine contract
(`tests/test_validate.py:33-34`) — *"every store-month exists whether or not it traded"* — the entire
ratified law payload is:

```
   'anchor'              : 'store_month'      <- a name for a derived object
   'basis'               : 'spine'            <- a four-way label
   'dependencies'        : {}
   'restriction'         : []
   'fingerprint_version' : 'elf-1'
   law_description in payload?  False
```

A generative law is exactly the case a restriction cannot express, and the interview mints its entire
content as prose (`interview.py:399-403`). So today a spine universe's *"whole intended population
law"* is a name, a label, and two empty containers.

### 7b. What follows for the first migration

Restriction-shaped laws (*"the points of a governed base world satisfying P"*) are within reach of
machinery already judged sound. **Generative laws are not, and Ruling 7 forbids letting `basis`
stand in for one.** The first migration must therefore either carry a λ_U representation able to state
a generative law, or refuse to constitute generative worlds and route them to `Unresolved`. **This
ruling forces the choice; it does not make it.**

---

## 8. Ruling 8 — a constituent rename conservatively stales `elf-2`

**Ruled by Huayin, 2026-09-15.**

> **Do NOT introduce a coordinate/anchor identity token.**
>
> **ToD's statement that a dimension name is conventional does not by itself establish succession
> between `store` and `outlet`. Until governed continuity/equivalence has actually been established, a
> constituent rename changes the resolvable constitution and therefore STALES `elf-2`.**
>
> **This is a conservative RATIFICATION rule, not a claim that the name constitutes the partition.
> Re-ratification CONFIRMS continuity or change; an opaque id would ASSUME it.**

The distinction is exact and is worth holding onto: the name is not identity-bearing *ontologically*;
it is identity-bearing *for the purposes of what a human has ratified*. Those are different claims, and
only the second is made here.

ToD v7.1 §3.9 supports the reading and, read carefully, compels the conservative side. It says
*"A mere label change **need not** change identity"* — permission, not establishment — and then
*"a change of constitutive order, participation, or formation cannot be concealed by retaining the old
label."* Its closing rule is *"identity before comparison and **versioned succession before silent
redefinition**."* A stale verdict **is** the demand for a succession act. A token that made the rename
invisible would be the silent redefinition §3.9 names.

**Cost accounting, stated plainly.** This yields a *false stale* whenever a rename really was cosmetic.
That costs one human confirmation. The opposite error — a substitution that does not stale — is a
publication that claims a human ratified a world he never saw. The asymmetry is not close.

---

## 9. Ruling 9 — physical realization may be finer than `R_U`

**Ruled by Huayin, 2026-09-15.**

> **Do NOT require `unique_at(full individuation)` as a universal condition of realizing a universe.**
>
> **A physical carrier MAY contain multiple records contributing to one root analytical point.
> `unique_at(full individuation)` can EVIDENCE a coincident / one-row-per-root-point realization
> WHERE THAT REALIZATION IS CLAIMED — but failure of uniqueness does not by itself contradict the
> universe, `Ω_U`, or `R_U`.**
>
> **Keep realization cardinality separate from analytical point identity.**

This closes §6 at the correct strength and corrects the reconnaissance, which had left open whether
full-tuple uniqueness might be *required* for publication. It may not be. ToD v7.1 §2.2: *"A physical
key may represent the point; it does not define the point's analytical standing merely by being unique
in a table"* — **representation**, which does not entail one record per point.

So the three claims stay separate, and no one of them licenses another:

| claim | what establishes it |
|---|---|
| *these constituents individuate a root point of this world* | the constitution (§1, §2) — a human act |
| *this material represents those root points* | a mapping / realization claim |
| *…with exactly one record each* | `unique_at(full tuple)` — **only where coincidence is claimed** |

**A uniqueness failure is therefore not even a realization defect by default.** It contradicts a
*coincidence claim* if one was made, and says nothing otherwise.

**A vocabulary warning, since a near-match exists in the tree and would be the easy mistake.**
`formation.contribution_structure: "coincident"` (`family.py:163`; the shipped fixture at
`tests/fixtures/lighthouse-v2-publication.json:77`) belongs to **family formation** — how contributions
coincide at an analytical point — and is in a different jurisdiction from realization cardinality.
The words are close and the objects are not. Do not borrow it.

---

## 10. Ruling 10 — no authoritative dual read

**Ruled by Huayin, 2026-09-15.**

> **The new universe constitution and `universe.body.anchor` must NEVER be established as competing
> semantic authorities.**
>
> **`universe.body.anchor` has no established meaning under the corrected constitution. During
> migration it MAY be inspected as legacy migration EVIDENCE; it must NEVER adjudicate, override,
> validate, or contradict the new constitution.**
>
> **Once a universe has an authoritative new constitution, analytical resolution uses THAT
> CONSTITUTION ONLY. If the legacy `body.anchor` remains present, its unresolved legacy standing must
> be explicitly DISPOSED OF before publication.**
>
> **Do NOT compare the two and build a tie-break or a semantic-disagreement rule.**

This withdraws a rule the migration reconnaissance had proposed. That reconnaissance suggested that a
universe carrying both a constitution and a divergent `body.anchor` should **refuse on disagreement**.
**That was wrong for the same reason a tie-break is wrong**: a disagreement rule is still a comparison,
and a comparison grants the legacy field standing to disagree. A field with no established meaning
cannot disagree with anything.

**The correct shape is STATE, not precedence.** A universe is in exactly one of two states —
*legacy* or *constituted* — and resolution reads one source accordingly. `body.anchor` on a constituted
universe is **inert and pending disposal**, never an input. This also settles the `body.anchor`
question the 2026-09-14 ruling and §12 left open on the compatibility side: it survives **as an
undisposed legacy artifact that blocks publication**, and in no other role.

---

## 11. The semantic constitution of `U`, consolidated

The whole of §§1-10, stated once as the object.

### Constituted — the three governed facts, and nothing else

1. **The identity of the analytical world.** The **subject** of the constitution, not a term in its
   law. Renaming the universe does not change the world (§8's conservative rule is about *constituents*,
   not about the world's own name, and `Declaration.identity()` is already rename-independent).
2. **The primitive root-point individuation.** A **closed** set of governed constituents — *these and
   no others*. Each carries a governed reference and a governed value domain. Constituent **order is
   not identity-bearing** (ToD §2.1.3, Frame-QL §4.6). A constituent **rename stales** (§8).
3. **λ_U.** Determinate and internally resolvable against (2) and the governed premises it references
   (§7). No prescribed grammar. Determinacy ≠ executability. Classification, binding and prose may
   accompany; none substitutes.

### Derived — never authored, never declared, never fingerprinted

`Ω_U` · the root anchor `R_U` · the scalar anchor `{}` · every Case-S coordinate placement and its
fiber partition · every compound anchor, including `{store * day} = R_sales` · the refinement order
among all of them.

### Outside the constitution

Any physical binding · any realization or evidence fact, **including realization cardinality** (§9) ·
any derived anchor, declared or not · any **Case-G placement** — a structure *on* `Ω_U` that does not
change `Ω_U`, and therefore requires its own governed act rather than disturbing this one ·
`universe.body.anchor`, which has no established role and is disposed of, not interpreted (§10).

---

## 12. Conceptual disposition of the present objects

Recorded **without** changing source or serialization. This table states standing, not a migration.

| object | disposition under this ruling |
|---|---|
| `universe` | **Survives.** Its constitution must be **rebased** onto §1: identity, primitive root-point individuation, existence law. |
| `coordinate` | **Survives, rebased** as a **universe-relative primitive governed constituent** of an individuation — no longer a standalone global object. |
| `anchor` **declaration** | **No longer presumed to be a primitive ontological object.** Case-S anchors are **derived** (§2, §3). Whether any declaring act survives at all is an authoring-model question, not a given. |
| `anchor.components` | Its useful **coordinate-description content may survive**. Its **current container has no constitutional authority** — components of a declaration are not thereby constituents of an individuation. |
| `universe.body.anchor` | **No semantic role has been established under this constitution.** It must **not** be reinterpreted merely to preserve compatibility, and no replacement meaning is invented here. The 2026-09-14 ruling already forbade reading it as every family's constitutive anchor; this ruling removes the last remaining presumption that it means anything at all. **Ruling 10 settles its migration treatment**: inert on a constituted universe, inspectable only as legacy evidence, **explicitly disposed of before publication**, and never compared against the constitution. |
| `relationship` | **Survives as governed structural input.** It **does not establish a partition** (ToD Appendix D). It may be an input to a Case-G construction; it is never itself one. |
| `hierarchy` | **Does not constitute refinement.** Refinement is derived from governed partitions (ToD §2.1.2 — *"A physical join does not supply a missing partition projection"*). Existing hierarchy evidence may still have another lawful role; **this ruling does not settle what that role is.** |
| `Declaration.identity()` | **The mechanism may survive.** But **physical gate subjects must not define analytical identity** — identity that varies with a table/column binding is a physical key wearing an analytical name (ToD §2.2: *"A physical key may represent the point; it does not define the point's analytical standing merely by being unique in a table"*). |

---

## 13. Recorded witness — the ratified law does not include root-point individuation

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
right place to put individuation — see §14.

**The witness is not an accident of the fixture; it is structural.** `dependencies` is built only from
`_law_reference_paths(universe)`, which walks *"the logical reference paths a universe's restriction
depends on"* — the `restriction` operands and nothing else
(`src/manifold_agent/ratification.py:77-88`, `:90-116`). The anchor's components are never consulted
on any path into the digest. So no anchor mutation whatsoever can stale a universe's law under
`elf-1`, for any universe, by construction — the empirical rows above merely exhibit what the payload
builder already guarantees (`src/manifold_agent/ratification.py:155-161`).

---

## 14. What this ruling does NOT settle

Revised 2026-09-15 after Rulings 7-10. Recorded so that no implementation settles the
remainder by convenience.

### Settled on 2026-09-15 — moved OUT of this list, recorded so the change is legible

| was open | now ruled |
|---|---|
| whether a prose-only λ_U is a lawful constitution | **no** — λ_U must be determinate (§7) |
| whether `basis` survives, is subsumed, or is retired | **none of these yet** — compatibility vocabulary, standing undetermined, never promoted into λ_U (§7) |
| whether a constituent rename stales | **yes**, conservatively, and **without** an identity token (§8) |
| whether `unique_at(full tuple)` is required or merely admissible | **admissible, never required** (§9) |
| whether constituent order is identity-bearing | **no** — set, not sequence (§11) |
| whether `universe.body.anchor` may adjudicate during migration | **no** — inert, disposed of, never compared (§10) |

### Still open

- **The authoring representation.** No field names, no kinds, no schema, no serialization. The
  smallest authoring model capable of expressing §§1-11 is the subject of the accompanying
  reconnaissance, and that reconnaissance does not itself authorize a change.
- **The representation of λ_U**, and in particular whether the first migration carries a form able to
  state a **generative** law or refuses to constitute generative worlds (§7b). Ruling 7 forces this
  choice and does not make it.
- **The eventual standing of `events | spine | product | registry`** (§7).
- **Whether an anchor declaration survives** as a naming/description act once it is no longer
  constitutive.
- **Whether universes require opaque identity tokens.** Not decided here, not to be decided as a side
  effect of implementation — and Ruling 8 removes the one argument that was pushing toward it.
- **The equality convention on coordinate values** — what makes two values of a constituent the same
  point. Left open; not a prerequisite for the first Case-S migration.
- **Cross-universe coordinate correspondence** (§5) and universe passage. Left open; not a
  prerequisite.
- **Whether a Case-G partition may participate in a compound anchor** with Case-S constituents. Left
  open; not a prerequisite.
- **The lawful residual role of `hierarchy` evidence** (§12).
- **Publication v2.x / v3.** Untouched.
- **P1-33, P1-34, Proof B, Proof C, OF-56, OF-58, persistence, SSE, reuse.** None is repaired,
  advanced, or implicated.

## 15. Doctrine relied on

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
