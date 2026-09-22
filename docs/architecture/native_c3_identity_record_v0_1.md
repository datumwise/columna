# C3 · Native resolution and identity — implementation record

**2026-09-22.** Unit C3 of the native-consumer sequence. **Construction, not demolition:** nothing
retired, no producer change, no Platform redesign, no movement implementation, no Law(F) work. The
v2 request path, `serving.plan_result`, `serving.decide_result`, the movement licence machinery and
`columna_platform.anchors` are all byte-unchanged.

Suites green — `columna-platform` 306, `columna-core` 1884 / 50 skipped, `columna-server` 416 / 2
skipped. 20 new tests.

**Stop-gate, as stated:** *"two synonym tokens yield one identity; two universes carrying one token
do not collide; plan and run report the same location."* All three witnessed in
`packages/columna-platform/tests/test_native_c3_identity.py`.

> **Why C3 happens in `columna-platform` at all.** `AnalyticalIdentity` lives there, and so does the
> plan/run pair the stop-gate names. The unit could not be performed anywhere else. What was added
> is one new module and one widened annotation; nothing existing was re-shaped.

---

## 1 · The first operation beyond visibility and availability

**Analytical request resolution:** a public Frame-QL request arrives as syntax, and the native path
must produce `AnalyticalIdentity(F, A)`.

It is first, and not merely next. Visibility answers *does this governed lineage exist here* and
availability answers *can this installation serve it*; the only other thing anyone can do with a
publication is **ask it something**, and every downstream object is keyed by the result —
`AnalyticalIdentity` is the retained-state retrieval key, the fold-eligibility key (`combine`
refuses unequal identities), the eviction key, and the public frame location.

## 2 · The exact semantic inputs it requires

Seven, and no others:

| input | kind |
|---|---|
| the series token | syntax |
| the `AT {…}` coordinate token set | syntax |
| reference → family, by canonical reference or declared alias, uniquely | governed |
| family → universe (`F → U`) | governed |
| the universe's **closed individuation** — to resolve each coordinate | governed |
| the universe's **Case-S denotation table** — to resolve the family's `constitutive_anchor` token | governed |
| refinement (⊇) and projection (set difference) over constituent sets | **derived** |

**Not required, and not consulted:** the `Law(F)` view, the C7 sufficient-state basis, a movement
licence, the realization mapping, a coordinate type, a basis, a level, a hierarchy, or any physical
fact.

## 3 · Can those be obtained directly from the native resolved model?

**Yes — all seven, with no translation.** Two were additions, and neither is one:

* `NativePublication.resolve_reference` — the publication format owning its own reference rule, the
  same discipline `GovernedPublicationV2.resolve_reference` already follows. A `family_id` is
  deliberately *not* a way of asking: identity is not a reference.
* `Anchor.refines` / `Anchor.projection_forgets` — already built in C1 as computed geometry.

**The shift, in one line: the request's coordinate set IS the anchor.** `AT {berth * day}` *is*
`A = {berth, day}`, resolved inside `U`. Nothing is looked up, so nothing can be ambiguous — which
dissolves a live v2 refusal rather than porting it. `request.resolve` refuses when two declared
anchors carry one component set (*"this profile will not choose between two governed anchors"*,
marked `# pragma: no cover` because *"the case cannot be built from a publication this proof is
authorized to write"*). **In the native fixture that is the ordinary case** — `berthing_at` and
`berth_day` both denote `{berth, day}` — and a consumer that kept name-matching would refuse a
lawful publication on its first request.

## 4 · Where existing execution infrastructure demanded a legacy-shaped representation

**Exactly one site: `AnalyticalIdentity.anchor: str`.** And the demand turned out to be made by the
*annotation*, not by the machinery. `AnalyticalIdentity` is a frozen two-field key used for equality,
hashing and dict lookup; both readings of `A` are hashable value types, so nothing had to change
except telling the truth about what the field now holds:

```python
AnchorOf = Union[str, NativeAnchor]     # v1/v2: a declaration NAME.  v3: a universe-relative set.
```

The two-field shape survives (the 2026-09-14 ruling is not reopened) and **no universe field is
added** — `F` fixes `U`, and the native `Anchor` carries its universe and refuses a cross-world
comparison, so the guarantee is structural at both levels rather than argued at either.

**Two things that looked like they would demand one and did not:**

* **The request-clause completeness surface** (`request.require_supported_clauses`) is reused
  **unchanged**. It classifies the fields of `Statement` as consumed / consumed-upstream /
  unsupported and fails closed on an unknown one. That is a fact about the request LANGUAGE, not
  about publication meaning — so it is genuine convergence, and the reuse is deliberate.
* **The movement licence machinery** (`MovementLicence.source_anchor` / `target_anchor`,
  `serving._licence_for_request`) *is* legacy-shaped and *would* demand a name. **C3 did not touch
  it and did not port it** — which is exactly why the movement boundary below is a refusal and not
  a code path.

## 5 · Is Law(F) encountered?

**No — and this negative is sharper than C2's.** C2 never reached an operation. C3 reached the first
real one and **completed it** without Law(F): request resolution is answered by the constitution,
the denotation table and set algebra, none of which is a §4 responsibility.

**A structural observation that bears on the question.** Resolution is *upstream* of Law(F) **in
both paths**: `serving.plan_result` calls `request.resolve` first and only then indexes `views` to
ask whether C7 sufficient-state is established. Law(F) enters at the step that asks whether the ask
can be **answered**, never at the step that establishes **what is being asked**. So the boundary the
sequence is probing lies below request resolution in the legacy path too — which is information
about where to look next, and **not** evidence that Law(F) is the convergence boundary. Nothing here
is designed toward it.

## 6 · Convergence or inherited implementation dependency?

No encounter, so the question is not yet answerable on its own terms. What C3 *does* show is one
meeting point, and its character:

> Both paths key state by `(family, location)` and **disagree completely about what a location is.**
> `AnalyticalIdentity` is a CONTAINER they share, not a semantics.

That is C2's finding one level down — *identity and availability converge; meaning does not* — and
it is worth naming as the pattern rather than as two coincidences. A shared container is not a
shared model, and a shared container is not evidence of convergence below it.

## 7 · Native facts discarded, weakened, synthesized or translated

**None.** The one that deserves examination:

* **The `constitutive_anchor` token does not enter the identity.** The spelling is used to resolve
  and then dropped. That is not loss: every governed token denoting an anchor is recoverable from
  the anchor (`Universe.synonyms_of`), and *keeping* it would be the defect — Ruling 11's *"names
  are conventions, the anchor is a theorem"*, and the measured consequence of the other choice is
  §1's split identity.
* **The universe is not copied into the identity**, per the standing ruling, and is recoverable
  through `F`.
* Nothing is synthesized: no anchor name is minted, no declaration is fabricated, no coordinate type
  is inferred, no location is invented for a coarser ask.

## 8 · New governed facts genuinely missing from the artifact

**None — but one undecided contract is now reachable by an ordinary request, and that is worth
stating precisely.**

A coarser ask (`SELECT berthings AT {berth}`, or the grand total `AT {}`) is the first thing a user
will type that the native model cannot yet answer. It is **not** a missing fact in the artifact: the
artifact carries no movement object because **no native movement contract has been decided**, and
ruling 3 holds that the contract is derived later from the native model rather than migrated from
the current implementation. C3 therefore refuses, and the refusal is shaped by §4's division and
nothing else:

```
WantOfLaw [fam_Nq4WfR8kPxDvZc2TmLbJhY]: 'berthings' is constituted at harbour{berth, day}, and this
ask stands at harbour{berth}. The target analytical location EXISTS — it is the projection that
forgets ['day'] — and that is a fact of GEOMETRY. Whether this family may stand there is a question
of governed MOVEMENT STANDING, which is a different fact and one the native model does not yet
state. A location existing is not a licence to occupy it, and this path will not infer one from the
geometry that shows it is reachable.
```

**A location existing is not a licence to occupy it.** Geometry is answered exactly; standing is
named as absent, not inferred, not defaulted, and not borrowed from the v2 licence machinery.

A *finer or disjoint* ask is refused differently and deliberately: a coarser location is reached by
forgetting, never by acquiring, so there is nothing for a licence to license and calling it
"unlicensed movement" would name the wrong remedy.

## 9 · Old assumptions that became unreachable

* *"an anchor has a NAME that can be reported"* — the location is a set. There is no name to report,
  and two governed tokens compete for the role.
* *"resolution matches an ask against the declared anchors"* — there are no declarations to match;
  the ask IS the anchor.
* *"two anchors over one component set is an ambiguity to refuse"* — natively that is the lawful
  ordinary case, and nothing has to be chosen between.
* *"a coordinate token is globally meaningful"* — resolution is universe-scoped, and comparing two
  worlds' anchors refuses rather than guessing.
* *"the frame location can be reported two ways"* — see §10.

## 10 · The plan/run divergence — settled by becoming unstatable

The recon requires this settled **before** a native anchor representation is chosen, *"or the choice
will bake it in."* It was measured first, not quoted:

```
── the v2 plan/run divergence, MEASURED (control; untouched) ──
  identity               : AnalyticalIdentity(family_id='fam_qv8Ky3mR7bTpZa1LwXcNdg', anchor='sale_at')
  plan_result   location : ('store', 'day')     <- the structural request
  decide_result location : ('sale_at',)         <- the nominal label
  same location?         : False
```

One lawful request, two answers to *where does this value stand*. **Nothing in C3 repairs it** — the
v2 path is untouched — and the measurement exists so the native claim is a comparison rather than an
assertion.

Natively the divergence is not fixed; **it cannot be stated.** The two candidate representations are
not two representations of one location: the request's coordinate set IS the location, and the
anchor's name does not exist. So `NativeResolvedRequest.location` is *defined as* `identity.anchor`,
`frame_location` is the one site that renders it, and a future caller cannot reintroduce the
divergence by reaching for the other expression, because there is no other one to reach for.

```
SELECT berthings AT {berth * day}
    identity : (fam_Nq4WfR8kPx…, harbour{berth, day})
    location : ('berth', 'day')   (plan side == run side: True)
SELECT moorings  AT {day * berth}
    identity : (fam_Td6JhV2yQn…, harbour{berth, day})
    location : ('berth', 'day')   (plan side == run side: True)
```

And the shape choice, witnessed rather than argued:

```
berthing_at -> harbour{berth, day}
berth_day   -> harbour{berth, day}      one anchor? True
identity with A as the SET     : equal? True
identity with A as a raw STRING: equal? False   <- today's shape splits one identity in two
```

---

## 11 · Notes

* **The two-universe collision fixture is DERIVED and its digests are minted with the consumer's own
  derivation** — stated plainly in the test. It witnesses **universe scoping**, and it cannot witness
  canonicalization agreement with the producer; only the producer-shipped artifact does that
  (**OF-59**, untouched here, as ruled).
* **`columna-core`'s test count rose by 20 without a new core test.** `test_expression_grammar.py`
  is parametrized over an expression corpus harvested from the tree, and it picked up the four new
  Frame-QL strings (×5 checks). The drift guard doing its job; all pass.
* **F-3 fixture debt** untouched, as ruled. The platform suite reads both fixtures from
  `columna-core/tests/`, taking no new copy.
