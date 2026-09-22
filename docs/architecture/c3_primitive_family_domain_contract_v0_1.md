# C3 · the primitive-family Case-S domain — implementation contract

**Standing.** A CONTRACT, not an implementation. It states exactly what the next unit may build, what
it must refuse, what it must not touch, and what must be true when it is done. Nothing here is built.

**Authority.** Steward's rulings of 2026-09-22 — the nine of the first set and R1–R12 of the second.
Theory statement: `tod_v7_2_development_addendum_v0_1.md` §A.1–§A.2. Seam analysis and stop-gates:
`c3_family_domain_implementation_plan_v0_1.md` (v0.2). Geometric premise:
`ruling_2026_09_15_universe_constitution.md` §§2–3.

---

## 1 · The scope gate

> **The unit applies to primitive families only.**
>
> ```
> fam.formation.kind == PRIMITIVE
> ```

⟨measured⟩ the gate is **already parsed, already total, already fail-closed**: a `PRIMITIVE` formation
cannot carry operands (`publication.py:163` vs `:176`, `_strict` refuses the key), a `CONSTRUCTION`
must name at least one (`:178-182`), and any third kind refuses (`:188-190`). The gate is a read of an
existing validated field, not a new classification.

⟨measured⟩ **both families of the shipped native fixture are primitive**, so the unit is complete and
fully testable on the artifact the native spine reads. ⟨measured⟩ **no multi-operand construction
exists anywhere in the tree** (3 constructions, all v2, max operand count 1).

**A constructed family reaching the domain decision REFUSES BY NAME** — carrying SG-A as a
`MissingGovernedFact` in the existing C4 idiom, naming the fact, whose it is, and where it would
belong. It does **not** derive, infer, union, or default. (R8.)

---

## 2 · The one declared fact

A new family-body key carrying **the family's prohibited Case-S constituents**, `P_F`.

**Content.** A set of constituent references of the family's own universe. Not anchors, not tokens,
not lineages, not capability names.

**Three states, and they must be three.** This is the load-bearing requirement of the whole unit.

| declaration | `P_F` | standing | `𝒜_F` |
|---|---|---|---|
| key absent | — | `UNESTABLISHED` | `{A_0}` by constitution (R1), **not** by the domain rule |
| explicit-none | — | `EXPLICIT_NONE` | `{A_0}`, positively declared |
| present, **empty** | `∅` | `ESTABLISHED` | every Case-S projection from `A_0` |
| present, non-empty | as declared | `ESTABLISHED` | derived, less the projections that forget into `P_F` |

> **The declared-empty state must be expressible and must not be confusable with absence.** Rows 1
> and 3 differ in what they admit and are the reason the rule does not re-enact the family-admission
> test withdrawn at ToD v7.1 Appendix C.4. A reader that maps an empty collection to "absent" breaks
> the unit's central distinction. **This is the single thing most likely to be got wrong.**

**Validation — fail-closed, on the existing house precedent.** Every reference in `P_F` must
(a) resolve as a constituent of the family's universe, and (b) be a constituent of `A_0`.

Rationale for (b): `Forgotten(A_0 → A) ⊆ A_0`, so a reference outside `A_0` can never be forgotten and
is inert. The house already rules this class of declaration a mistake rather than a harmless no-op —
`parser.py:696-698`: *"a lineage named in a FERTILE (or BLOCKED) block must be carried by a declared
edge — opening (or closing) a door that doesn't exist is a mistake"* — and `:713-718` applied exactly
that rule to `BLOCKED`. **`P_F` adopts it at declaration time.** An inert prohibition is a steward's
error and must be reported as one, not silently carried.

**The reader is a real reader.** Modelled on `continuation` (`publication.py:275`,
`LawCitation.from_dict`), **not** on the identity slot `lambda r: r` (`:276-277`) that `domain` and
`movement` still use.

---

## 3 · What is derived, and never stored

```
A ∈ 𝒜_F   ⟺   A_0 ⪰ A   ∧   Forgotten(A_0 → A) ∩ P_F = ∅        [ESTABLISHED law, Case S]
```

* `A_0` — `universe.denote(family.anchor_token)`, already computed at `native_request.py:153`
* `A_0 ⪰ A` — `Anchor.refines`, set containment, already computed at `native_request.py:183`
* `Forgotten(A_0 → A)` — `Anchor.projection_forgets`, set difference (`native.py:360-375`), already
  pinned at `test_native_c3_identity.py:252`

**`𝒜_F` is never materialized, enumerated, cached, or serialized.** Only the membership predicate
exists. (ToD §4.1: *"notation for its defined analytical domain, not a proposed registry or new
object"*; ruling 6.)

**`A_0 ∈ 𝒜_F` must be a DERIVED result, not an early return.** Under an established law, reflexivity
of `⊇` gives `A_0 ⪰ A_0` and `Forgotten(A_0→A_0) = ∅`, so membership follows. The current bare
`if not moving: return` (`native_law.py:164-165`) must not be what answers it. Where **no** law is
established, the root's standing is governed separately and the theorem may not be detached from its
condition. (R1.)

---

## 4 · Where the decision lives

| layer | keeps | changes |
|---|---|---|
| `Law(F)` resolution | **anchor-model-free** — the proved C4 result, preserved intact | nothing |
| `assert_answerable(view, *, moving)` | **anchor-model-free** | its positive-content branch (`native_law.py:182-190`) narrows to `Γ_F`/γ |
| resolved-geometry layer (`native_request`) | already holds `A_0`, `A`, and the difference | **gains the domain adjudication** |

**`Anchor`, `constituents`, `refines` and `projection_forgets` may not enter `assert_answerable`.**
(R6, option (a).) The narrowing is of the *claim*, not of the proof: what is withdrawn is only that
answerability **as a whole** can be anchor-free. Domain membership is inherently a relation between
`F` and a resolved location.

**No native `MovementLicence` is created**, and no native anchor is translated into one to regain
convergence. (Ruling 6, R6.)

---

## 5 · Identity and succession

| change | consequence | mechanism |
|---|---|---|
| `A_0` changes **structurally** | family succession | `_anchor = sorted(constituents)` is in the `fcf-2` payload |
| `A_0` **renamed**, same structure | **no** succession | the spelling is in `NOMINAL_KEYS`, outside the `fcf-2` payload |
| `P_F` changes | governed law revision, **no** succession | the new key goes in `NON_IDENTITY_KEYS` |
| `𝒜_F` changes via universe geometry | **not decided** — held | — |

**`P_F` must be added to `NON_IDENTITY_KEYS` explicitly.** `native.py:101-104` states the default:
*"Everything else is IN **by derivation** — a body key added later is inside the fingerprint by
default, and taking one out is a decision someone has to write down."* **R12 is that decision, and
this line of the contract is where it is written down.** Omitting the exclusion silently makes every
domain-law revision a family succession — the exact outcome R12 forbids.

**Not identity-bearing is not unversioned.** ⟨measured⟩ the carrier already exists: the native
publication root carries `ref: {manifold_id, version}` and `published: {at, by}`. Two publications may
establish different domains for the same immutable `family_id` and be distinguished and audited by
that. **No new versioning machinery is in scope**, and none is needed.

---

## 6 · What must refuse, and how

Four outcomes must be **mechanically distinguishable** at the end of this unit. That distinguishability
is the unit's deliverable to ruling 9, which defers the reason-code decision until it exists.

| condition | refusal must say |
|---|---|
| target not geometrically reachable | there is no such location for this family — a fact of **geometry**, not a licence question |
| no domain law established | the family establishes no domain law; **absence is not permission** |
| law established, `A ∉ 𝒜_F` | **name the constituent** whose loss the family's law prohibits |
| constructed family, `P_F` not self-declared | the missing governed fact, characterized — **whose** and **where** (R8) |

**No new wire reason code is minted in this unit.** ⟨measured⟩ `REASON_OUTCOME` (`disclosure.py:227`)
is closed and fail-closed; Frame-QL 1.0 §12 forbids the mint in that document. Do **not** reuse
`anchor_spent` — it is an *aperture*-spending reason (`engine.py:528`). All four continue to surface
as `want_of_law` on the wire, distinguished by subject, until ruled. (Ruling 9, SG-C.)

---

## 7 · Conformance obligations

The unit is not done until each of these exists and passes.

1. **The split changes no verdict.** Step 1 (splitting the standing) must leave every existing
   verdict in the tree identical. This is its test, and it is the reason the split goes first.
2. **Declared-empty ≠ absent.** Two families differing only in that one omits `P_F` and one declares
   it empty must yield **different** domains.
3. **`A_0 ∈ 𝒜_F` is derived.** Asserted through the predicate, not through a non-moving early return.
4. **An inert prohibition refuses** at declaration time, naming the reference and why it can never be
   forgotten.
5. **A prohibited projection refuses and names the constituent.**
6. **A permitted projection is admitted** and is *not* thereby claimed lawful — the edge/realization
   layers are untouched and still have their say.
7. **A constructed family refuses by name**, carrying the characterized fact and no candidate encoding.
8. **`P_F` revision does not change the family fingerprint**; a structural `A_0` change does.
9. **`FAMILY_BODY_KEYS == _FAMILY_KEYS`** still holds (`test_native_c4_answerability.py:68-73`).
10. **The fingerprint helpers move with the key** — `_refingerprint_fcf2` / `_refingerprint_family`
    (`:264-278`). ⚠️ **The only seam in this unit that fails silently**; everything else fails loudly.

---

## 8 · Invariants that must not change

These are shipped results. A change to any of them is a defect of the unit, not a consequence of it.

* `test_resolution_consults_no_anchor_model` (`:85-94`) — `native_law.py` imports no anchor model.
* `test_law_resolution_asks_a_publication_for_exactly_one_thing` (`:97-103`) — `_ParentLookup`'s
  public surface stays exactly `{"family"}`.
* C7-is-asked-first and its reason (`:120-130`, `:133-143`), including that `"movement"` does not
  appear in the C7 refusal (`:142`).
* `test_a_NON_PROJECTABLE_ask_still_refuses_at_RESOLUTION` (`:160-167`) and
  `test_a_FINER_ask_is_not_a_movement_awaiting_a_licence` (`test_native_c3_identity.py:261-270`,
  `match="reached by FORGETTING"`) — **geometry refusals must stay geometry refusals** and must not
  become domain refusals.
* `test_an_explicit_none_movement_says_so_in_its_own_words` (`:191-196`) — the explicit-none path
  keeps its own words.
* The two-worlds control (`test_native_c3_identity.py:155-160`) — cross-world anchors cannot be
  compared.
* ⟨measured⟩ **nothing on the wire moves**: `assert_answerable` and `native_request.resolve` have
  zero production callers, and the v2 serving path (`serving.py:388-442`) is untouched.

---

## 9 · Out of contract

Held, and not to be filled opportunistically: constructed-family propagation (SG-A); `Γ_F(B→A)`;
coverage permission `γ`; participation and support; evidence; Case G and relationship expansion;
non-commutative and ordered continuation; any allow-list of anchors or edges; any native
`MovementLicence`; the output-anchor reason code (SG-C); lineage granularity (SG-D); Frame-QL syntax;
the legacy declaration surface and DG-4; P1-36 repair; `planner.py`'s existing `crossed & t.law`;
`domain` being write-only in v2; the `ExplicitNone`-domain conflation beyond the split itself.

---

## 10 · One finding that R11 creates, and a question it raises

⟨measured, this session⟩ **R11's synonym-invariance holds under `fcf-2` and fails under `fcf-1`** —
witnessed in the shipped fixture, which carries one family under each scheme.

`berthings` is `fcf-2` (it has a U-authority binding); `moorings` is `fcf-1` (it has none). Both
declare `constitutive_anchor: "berthing_at"`, and the universe's Case-S denotations make `berth_day`
an **exact synonym** — both resolve to `{berth, day}`. Rewriting only that token, per family:

```
berthings  (fcf-2):  PARSES, fingerprint UNCHANGED        -> R11 satisfied
moorings   (fcf-1):  REFUSES AT PARSE                     -> R11 not available
             "family 'moorings': its authority cites 'fcf-1:cecffbe…', and the identity-bearing
              constitution carried beside it derives 'fcf-1:fe408f30…' under 'fcf-1'."
```

Under `fcf-1`, `constitutive_anchor` is inside `IDENTITY_KEYS` (`native.py:105-107`), so **the
spelling is identity-bearing** — which is precisely what R11 rules it must not be. `fcf-2` removes it
(`NOMINAL_KEYS`) and substitutes the resolved `_anchor`, which is precisely what R11 rules it must be.

**This is not a correctness hole and it does not block this unit.** The behaviour is fail-closed —
the artifact refuses rather than silently minting a successor — and the domain rule is indifferent to
which scheme governs. It is a **capability gap with governed standing**: R11's invariance is simply
unavailable to an unbound family.

> **Question for the steward.** Is R11 (a) a rule about the `fcf-2` identity model, with `fcf-1`
> understood as a known-weaker predecessor that cannot express it; or (b) a rule the identity model
> must satisfy generally, making an unbound family's inability to rename its own anchor a defect worth
> rowing? The 2026-09-21 ruling that *"an UNBOUND `fcf-1` family may exist in a native-v3 artifact"*
> points toward (a). **Not rowed pending that call.**
