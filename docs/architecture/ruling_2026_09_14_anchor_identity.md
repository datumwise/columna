# Ruling — 2026-09-14 — anchor identity is **universe-relative structural identity**, under **one scheme**

**Status:** **RATIFIED** by Huayin, 2026-09-14. **Not yet implemented.** The defect it corrects is
rowed as **P1-33** (`consolidated_ledger_v0_1.md`, P1, HIGH, OPEN) and stands against live `main`.

**Implementation order (ruled):** these two rulings are recorded **before** any amendment to
[#325](https://github.com/datumwise/columna/pull/325). No source repair is authorized by this
document. A bounded representation reconnaissance runs first; no anchor spelling and no new type are
chosen here.

---

## 1. Ruling 1 — anchor identity is universe-relative structural identity

An anchor is a **governed partition of a universe**. Two equal-looking anchor expressions in
different universes therefore **do not identify one analytical anchor**.

> **Anchor identity is universe-relative structural identity. Within `F @ A`, the family identity
> supplies the universe context. `A` need not duplicate the universe in `AnalyticalIdentity`,
> provided anchor resolution is ALWAYS performed inside the governed universe of `F`.**

**Do not widen `AnalyticalIdentity` to add a universe field**, in this unit or as a reflex. `F`
already determines its governed universe; lawful anchor resolution and lawful movement for that
family occur within it. The universe is a **precondition of resolution**, not a component of the
identity that resolution produces.

**Two consequences that bind immediately.**

1. **The current publication-global, universe-blind anchor matching is NOT AUTHORITATIVE.**
   Resolution must be scoped to the selected family's universe.
2. **"Structural" does not mean a globally interpreted bag of component-name strings.** It means the
   **governed constituent partitions as resolved within that universe**. A component-name set
   compared across universes is not a structural identity; it is a coincidence of spelling, and ToD
   §2.1.3 rules exactly that case: *"Two expressions that happen to group current records identically
   are not thereby analytically equivalent. Equivalence comes from the governing structure, not an
   accident of current data."*

---

## 2. Ruling 2 — one anchor-identification scheme

Declared anchors and lawful projected targets are **not different ontological kinds of location**.

> **Declared anchors and lawful projected targets resolve into the SAME universe-relative structural
> anchor identity. A declaration name may RESOLVE to that identity. A movement licence may AUTHORIZE
> establishment at that identity. NEITHER the declaration name NOR the licence label independently
> CONSTITUTES analytical identity.**

### Consequences, as ruled

- `sale_at` is a **governed publication reference** to an anchor. It is not the identity of the
  partition merely because it is a string.
- `AT {store*day}` and the declaration named `sale_at` **may resolve to the same anchor**, because
  governing structure establishes that equivalence **in the selected family's universe**.
- A lawful projected `{store}` **is an anchor**, whether or not a separate publication declaration
  gives it a name.
- **Movement does not mint `{store}`. It licenses `F` to stand there.**
- The **arrival path remains in `Standing.movement`**, never in `A`.

### Why the two rulings are one ruling

Ruling 2 is what makes Ruling 1 implementable. If declared anchors and projected targets were
identified under two schemes, every site that compares across the two populations would be comparing
values minted under different rules — which is the precise mechanism of P1-33's Witness A, where a
licence label is compared against a declared anchor name at `serving.py:890` and the equality decides
whether a fold happens at all. One scheme is not tidiness; it is the condition under which those
cross-population comparisons mean anything.

---

## 3. What this makes non-authoritative on `main`

| today | status under this ruling |
|---|---|
| `anchors.declared_anchor_names` flattens every declared anchor in the publication into one `{name: frozenset}` map with **no universe key** | **not authoritative** — resolution must be scoped to `F`'s universe |
| `request.py` matches an ask against that flat map | **not authoritative** — same reason |
| `MovementLicence.target_anchor` becomes `AnalyticalIdentity.anchor` (`continuation.py:99`) | **forbidden** — the label does not constitute identity |
| `moving = at_anchor != identity.anchor` (`serving.py:890`) decided by comparing a licence label with a declared name | **forbidden** — movement is determined from resolved analytical locations |
| `FrameResult.anchor` structural from `plan_result`, nominal from `decide_result` | **forbidden** — plan and run must report the same target location |

---

## 4. Implication for #325

**Do not repair #325 by choosing a better `target_anchor` string.** Not the first component name, not
source-anchor-plus-components, not `store`, not `sale_at{store}`. A spelling rule would make the
recorded witnesses stop reproducing while leaving the governed question unanswered, and would bind
the answer to whichever spelling was convenient.

**The identity-bearing use of the free licence label must end.** At minimum, `target_anchor` must no
longer independently decide:

1. `AnalyticalIdentity.anchor`;
2. movement / no-movement;
3. retained-state identity;
4. the public frame location.

Whether the field survives for **descriptive / provenance** purposes is a separate decision and is
not settled here.

### The corrected flow, conceptually

1. select `F`;
2. obtain `F`'s governed universe;
3. resolve the source and requested target anchor expressions **under that universe**, using **one**
   structural identification rule;
4. determine movement **from those resolved analytical locations**;
5. require the movement licence to **authorize** the source → target projection;
6. perform continuation;
7. retain movement provenance **separately**;
8. plan and run report **the same** target location.

Note what step 5 is and is not. The licence answers *may `F` stand here*; it never answers *which
`A`*. That is ToD §4.1's own division of labour: *"A geometrically available projection and a
computable state operation do not by themselves put `A` in `𝒜_F`. The family's definition must
license the quantity being claimed there."* `A` is already a partition before any licence is read.

---

## 5. The doctrine this rests on

| claim | source |
|---|---|
| an anchor **is** a governed partition of `Ω_U` — *"not an arbitrary grouping expression or list of columns"* | ToD v7.1 §2.1.1 |
| a name is a **conventional governed name** given to a partition | ToD v7.1 §2.1.3 |
| expression ≠ partition; *"Equivalence comes from the governing structure, not an accident of current data"* | ToD v7.1 §2.1.3 |
| refinement and projection are defined **only for anchors of the same universe** | ToD v7.1 §2.1.2 |
| labels do not substitute across snapshots, populations or restrictions | ToD v7.1 §2.2 |
| *"Anchors are partitions of their own universes"* | Frame-QL 1.0 §2.7 |
| geometry ≠ admission: an available projection does not put `A` in `𝒜_F` | ToD v7.1 §4.1 |
| `A` is *"a request coordinate, never declared"* | `specs/unit_d_synthesis_v0_4_model_and_publication_design.md` §3 |

The tree already applies the correct rule in one place, for declared anchors only — `request.py`
resolves an ask to a declared anchor by **set equality on declared components**, and its test states
the principle in the ruling's own terms: *"The name `sale_at` is never typed by the requester and
never guessed: it is read off the declaration that carries those components."* These rulings extend
that rule to the projected case and scope both to the family's universe; they do not invent it.

---

## 6. What this ruling does NOT settle

Recorded so that no implementation settles them by choosing a convenient spelling.

- **The representation.** No anchor spelling, no new type, no format. A bounded reconnaissance
  determines the smallest representation compatible with these rulings first.
- **Whether `target_anchor` survives at all**, in a descriptive or provenance role.
- **How the publication establishes which declared anchors belong to which universe.** The `anchor`
  declaration carries **no universe field**; whether the relation is derivable from universe
  declarations plus family constitutive anchors under the present format, or whether the format is
  missing a governed relation, is an open reconnaissance question. **This ruling does not authorize a
  publication-format change.**
- **What `FrameResult.anchor` means uniformly** across plan, execute, and legacy-compatible wire
  surfaces — beyond the requirement in §4 that plan and run agree.
- **OF-58 and OF-56.** Untouched. Neither is settled, advanced, or implicated by this ruling.
