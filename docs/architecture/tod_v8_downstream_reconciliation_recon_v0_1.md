# ToD v8 downstream reconciliation — reconnaissance report

**Claude, at Huayin's direction, 2026-09-28.** Answering
`attachments/82a20961_cc_tod_v8_downstream_reconciliation_recon_v0_1.md` against
`attachments/df08b97e_tod_v8_downstream_reconciliation_v0_1.md` (position paper v0.1).

**Governing theory:** *The Theory of Data*, Version 8.0, DOI **10.5281/zenodo.23018979**, published
28 September 2026. **Baseline verified against the published record, not the candidate** — see §0.

**Standing.** Reconnaissance only. **No code. No schema invention. No rename. No compatibility break.**
Nothing in this report is authorized work. Every claim carries `file:line` and was re-verified against the
source after the sweep that produced it; findings marked **VX** were reproduced by executing the code.

---

## 0. Baseline check — the published paper vs the candidate

**CORRECTED 2026-09-28, after Huayin supplied the canonical file.** The attachment
`attachments/1710d7b5_theory_of_data_v8_0_zenodo_23018979.md` is **byte-identical** (md5, 83,539 bytes) to the
copy I fetched from the Zenodo record, so the audited artifact is right. **My characterization of it was
wrong, and the error was methodological.**

**What I did wrong.** I compared the published text to the v0.18 candidate by diffing *headings* and counting
*tokens*. Headings are identical but one; token counts matched. I inferred "structurally identical, one section
added" and "none of the omission-audit findings were incorporated." **A word-level content diff shows 44
changed hunks.** `FIRST` occurs 14 times in both files — while the sentence containing it changed materially.
**Counting occurrences cannot detect a rewritten sentence, and I should not have drawn a negative conclusion
from a null token delta.**

**What is actually true.** The published v8.0 is materially edited, and **four of the sixteen findings in
`tod_v8_v0_18_accidental_omission_audit_v0_1.md` were addressed in publication — including the two I ranked
first and second.**

| audit finding | status in published v8.0 |
|---|---|
| **Ordered-family coherence** (audit §4.12 — *"the largest structural gap the sweep found"*) | **RESOLVED.** §6.2: *"Together with \(\bot\) as identity on known-empty blocks, **the witness carrier forms a commutative monoid on compatible LAST witness states.** Therefore, under the same governed order, participation, coherent-instance, and evidence premises, **staged and direct LAST continuation are path-independent on the witness carrier. The dual result holds for FIRST**."* That is v7.1's Proposition 8.1, restored. §6.4's exclusion sentence remains, but it is now *accurate* rather than an unmet promise — the ordered case is discharged in §6.2. |
| **`FIRST` never specified** (audit §4.13) | **RESOLVED.** §6.1 l.1132: *"FIRST requires the dual condition: a unique least participating point."* |
| **No construction for a complete order on a multi-constituent anchor** (audit §4.1) | **SUBSTANTIALLY ANSWERED.** §6.1 now specifies the *outcome* without needing a construction: *"If two relevant participating points remain incomparable, the corresponding ordered result is not established."* The theory refuses rather than constructs, which is complete. What survives is a usability point, not an insufficiency: an implementer wanting a *usable* `{account, day}` order still has no canonical constructor. |
| **Coarsening-sufficiency ≠ restriction/deletion** (audit §5, and my §D.6 below) | **RESOLVED.** §3.1 l.297: *"Value closure is relative to admitted continuation. **It does not imply recoverability of prior contributions or sufficiency for restriction, deletion, correction, or a changed analytical law.**"* That is v7.1 §10.2/§10.3 in substance. |

**Also added:** §1.1 "Relation to prior work" (Codd, OLAP/summarizability, incomplete information, provenance;
references [1]–[12]); a rewritten abstract and §1 introducing the two forms explicitly; and in §6.2,
*"the witness retains both the selected source point and its value, so later continuation compares governed
source positions rather than only the displayed scalar."* **Slightly trimmed:** the `⊥` passage lost its boxed
inequality and the sentence explaining *why* substituting `⊥` is unsafe; the rule survives as *"The state
\(\bot\) denotes established emptiness only. An unavailable witness has want of state and must not be
represented by \(\bot\)."*

**Still standing from the audit** (content-probed, not token-counted): the name↔identity doctrine
(`namespace`/`alias`/`immutable`/`canonical name` — 0); `formation` undefined; the congruence obligation
defining `governed equivalence` — 0; the target-specification obligation — 0; Proposition 8.2's extraction
homomorphism — 0; the overlapping-relationship/partition boundary — 0.

**Consequence for this reconciliation, and it is good news:** the ordered-witness path is now backed by a
published path-independence result. **My claim that "anything built on ordered continuation is building ahead
of the published theory" is withdrawn** — Columna's `ORDERED_W` is covered. Every other finding in §A below
was derived from repo evidence and is unaffected.

---

## A. Exact repository facts

### A.1 ⛔ The stop-gate has tripped — C4 answerability (brief Q2) — **VX**

The brief: *"Determine whether C4 allows a family member `F@A` to be established from analytical objects
outside family `F`. If yes, stop and characterize the conflict."*

**It does.** Reproduced by executing the resolver, not inferred.

`native_law.py:153-170`, `assert_answerable` — by its own docstring *"The decision, and the whole of it"*:

```python
c7 = view[C7_SUFFICIENT_STATE]
if c7.standing != ESTABLISHED:  raise WantOfLaw(...)
if not moving: return
```

**C8 continuation is never consulted.** Answerability is granted on a sufficient-state basis alone. The
predicate is `answerable(F, moving) ≡ C7 ESTABLISHED ∧ (¬moving ∨ C3_EDGE_VALIDITY positive)`.

**And `resolve.py:361-366` is where the two routes fuse:**

```python
basis_law = cont
basis_provenance = ENTAILED
basis_source = "the continuation law"
if basis_law is None and fam.formation.kind == CONSTRUCTION:
    basis_law = fdn.resolve(fam.formation.law)
    basis_source = "the formation law"
```

Route 1 is family-internal continuation — v8 value closure. Route 2 is basis-mediated reconstruction from
operands — the route v8 §9.2 abolishes. **Both emit `Standing(C7, ESTABLISHED, ENTAILED)`;
`basis_provenance` is set once at `:361` and the fallback never revises it.**

> **The distinction v8 makes constitutive exists in the repo today only as an interpolated substring in a
> prose note** — `"the continuation law"` vs `"the formation law"`. Core tests already string-match it
> (`test_governed_v2.py:282,294`).

The comment three lines above (`resolve.py:356-359`) keeps `cont` and `basis_law` as separate names
*deliberately*, warning that letting one variable mean two things is *"how the two facts this correction
separates would quietly grow back together."* **The instinct was right at the variable level; the provenance
token did not follow.**

**Reproduced:** `mean(revenue@sale_at)` declared `"kind": "family"` → C8 `EXPLICIT_NONE`, C7 `ESTABLISHED`,
**VALID**, answerable at its constitutive anchor. v8 §9.2 names that exact quantity a governed expression.

**Answer to the brief's sub-question:** "basis" in C4 is **AMBIGUOUS / BOTH** — not a wrong meaning, two
meanings under one token.

**Aggravating:** `governed/native.py:86` — `ADMITTED_KINDS = frozenset({"universe","family"})`. There is no
`E` sort to reclassify into. **The repo cannot currently express the correct answer.**

### A.2 The resolved analytical target, and the narrowest seam (Q1)

**23 intrinsically family-only sites** (20 in `columna-platform/src`, 3 in `columna_core/governed`),
11 accidental, 9 already generic. But the number that sizes the change is different:

> **22 of the 23 are downstream of a single dispatch.** The seam is `request.py:97-98` —
> `family = pub.resolve_reference(token)` together with its `if family is None:` arm.

Everything above that line is sort-agnostic; everything below is family-root law without exception
(`constitutive_anchor`, movement, licence). An expression target that branches at the `None` arm and returns
early **never reaches any of the other 22**, and the family success path changes by zero bytes. Downstream
blast radius is two call sites (`serving.py:598`, `:766`), both already inside `_translated`
(`serving.py:682`), the shared refusal→wire table, so a peer inherits the refusal contract rather than
restating it.

**The `None` arm already names the gap in prose:** *"does not evaluate expressions"* (`request.py:104-105`).

**A correction to the brief's own premise.** That arm raises **`WantOfLaw`**, not `UnsupportedByThisProfile`.
So a token naming a durable governed expression returns a **governed verdict** — *"no governed family answers
to the reference"* — rather than a capability limit, **sending a steward to correct a publication that is
correct.** (`UnsupportedByThisProfile` for expressions appears only at `request.py:264-266`, for the `WITH`
clause.)

**Hardest test pin:** `test_of39_constitution_compatibility.py:199-202` asserts
`[f.name for f in dataclasses.fields(AnalyticalIdentity)] == ["family_id","anchor"]`. Its docstring guards
**storage and constitution** leaking into identity, not sort. **A peer target type does not violate it;
widening `AnalyticalIdentity` would.** That is an argument for the peer, from the repo's own test.

**An expression result is already served through a family identity slot.** `serving.py:943-950`:

```python
if st.composite is not None:
    final = _composite.finalize(st.composite)
    return FrameResult(col.frame, Disclosure.clean(), [col], (identity.anchor,))
```

**One `if` statement, not an architecture.**

### A.3 `sufficient_state` and the undiscovered boundary (Q3)

Both v8 objects exist in the runtime today, under one English phrase, **in one dataclass ten lines apart**:

| v8 object | code |
|---|---|
| family **continuation state** (§5.1) | `state.py:70-158` `RetainedState.array`/`.table`; folded by `continuation.py:76 continue_to`; combined by `state.py:222 combine` |
| expression **sufficient basis** (§5.3) | `state.py:151 composite`; `composite.py:100 CompositeState`, role-indexed via `Component.law`; constructor `finalize` `:251` → `Finalized` `:239` |

`state.py:89-90` — `basis: Optional[str]`, a *family* continuation description, **inside** the compatibility
tuple (`state.py:134-135`). `state.py:151` — `composite`, the *actual* expression basis, **outside** it.

And upstream, `C7_SUFFICIENT_STATE` carries sometimes a scalar continuation description and sometimes a
`StateBasis`, so `composite.py:130-134` must branch:

```python
if not isinstance(c7.value, StateBasis):
    raise WantOfLaw("the family's sufficient state is scalar ...; this path constitutes a
                     COMPOSITE basis and will not repackage a scalar as one")
```

> **That `isinstance` check is the family/expression boundary — discovered by implementation, named nowhere.**

### A.4 MEAN (Q4) and Proof C

`foundation.py:281-300` — `MEAN`: `entails_continuation=NO_CONTINUATION`, `usable_as_continuation=False`,
`state_basis=StateBasis(("SUM","COUNT"), requires_common_participation=True)`. Under v8 §9.2 that is the
*definition* of an object that is not a measure family, and `native.py:86` gives it nowhere else to live.

**`composite.py` already satisfies v8 §5.3's five basis obligations** — role-indexing (`Component.law`,
retrieved by role name at `:110`), independent establishment (`constitute` reads the basis from C7 and
refuses to invent it), joint compatibility (`ParticipationWitness.same_participation`, `:59-85`), anchor
locality (one anchor, one pass), constructor φ (`finalize` → `Finalized(is_sufficient_state=False)`).

> **Proof C is already an expression proof. v8 did not ask for new machinery here; it asked for the existing
> machinery to be called what it is.**

**But the sharper finding is that Proof C cannot demonstrate the proposition it is named for.** The desired
proof is `continuation-bearing family value ≠ finalized expression result`. **The left-hand side is absent by
construction.** What Proof C retains is not a family *value* — it is a tuple of values of **two different
families** (SUM-of-revenue and COUNT-of-revenue) bound by a participation witness (`composite.py:169-176`).
Three confirmations from the code:

1. `continue_composite` (`:200-235`) continues each component under its own foundation-declared law, and both
   resolve to `"SUM"` (`:229-231` hard-refuses anything else). **The only continuation performed anywhere in
   the proof is SUM continuation.** The "MEAN family" contributes an identity string and a C7 lookup.
2. `offer_as_state` (`:286-292`) **always** refuses. The proposition needs the positive half — *this* value is
   state and continues, *that* one is not. For event-constituted MEAN the positive half is unreachable by
   construction, so **the proof is all-negative on the only axis that matters.**
3. The family record it depends on is the exact artifact v8 abolishes (`conftest.py:112-126`,
   `exhibit.py:163-170`).

What it *does* demonstrate, and demonstrates better than the manuscript states it, is v8 §5.3's **joint
compatibility** obligation — `composite.py:186-194`: *"Equal-looking values do not establish that two
components ranged over the same contributions."* Worth keeping; just not the proposition on the tin.

**The one genuine defect is `continue_composite` (`composite.py:200`)** — it folds two `CompositeState`s
componentwise and returns a `CompositeState` under **one `family_id`**, i.e. continues a *basis* as though it
were family continuation state. Arithmetically correct (each component continues under its own
`entails_continuation`, read from the foundation rather than from the component's name — good code).
Ontologically v8 forbids it: SUM and COUNT continue independently, after which the expression is
**re-evaluated** at the target. The numbers agree; the sort does not.

**Do not delete Proof C.** It is the repo's only working demonstration of `finalized ≠ state`, enforced at
four points (`state.py:200-206`, `:239-241`, `composite.py:206-208`, `:286-292`) — v8 §7.7's hardest rule,
implemented, with a named refusal. **Reclassify it as the first expression proof**, and add a Proof C′ on a
genuinely value-closed structured value.

**Closest existing asset for C′ — `HLLSketch`, unambiguously**, and the reason is decisive:

> **HLL exhibits the inequality in one pair of calls, with both sides present.** `hll_merge(s1, s2)` **succeeds**
> as continuation of a family value; `hll_estimate(…)` yields a finalized result that `offer_as_state` must
> **refuse**. MEAN can never produce the left side.

`operators.py:161-165` already registers the three roles correctly — `hll_count` (→ `HLLSketch`), `hll_merge`
(union monoid, the continuation law), `hll_estimate` (MAP `HLLSketch → Int64`, the finalizer). It is the only
place in the tree where a family's value is a **governed typed value** rather than a scalar, it is
**value-closed literally** (merge takes and returns the same type), and **precision is type identity**
(`sketch.py:15-18`) — so the family value carries its own compatibility constraint *in its type*, exactly what
`requires_common_participation` must assert externally in the MEAN case. It is also v8's own worked example
twice (§3.5 and §5.3).

Three defects to clear first, all already named in-tree: the `distinct` wrapper fusing deliver+combine+project
(`operators.py:159`); the witness store keyed `(measure, member, base_level)` with `member == "distinct"` —
**family state filed under the identity of the expression it will become** (`sketch.py:21,104`); and
`sketch.py:6-7`'s framing.

**Moment/co-moment state is not implemented anywhere** — design prose only. v8 §5.4 names it as the right
*second* customer, but it is greenfield and not a position to prove a principle from.

**Scope-limiting good news.** **No `.cml` in the tree declares a `mean` or `avg` measure.** Every AOV in every
fixture is `DERIVED aov = revenue / orders` — a post-aggregation expression over two families, **already
v8-conformant**. MEAN reaches family standing only via (a) inline generation, (b) `FAMILY { mean FERTILE {…} }`
on a `DERIVED`, and (c) the platform/core **publication fixtures**. The exposure is in test scaffolding and
promotion surfaces, not in authored manifolds.

**One arity blocker to record:** `composite.py:143-145` hard-codes `basis.components != ("SUM","COUNT")`. v8
§5.3's basis is role-indexed `(G₁,…,G_m)` and §5.4 needs `(Count, SumX, SumX², SumXY)` — a two-component
hard-code cannot host variance, covariance or correlation.

### A.5 Standing distinctions (Q6)

**`eligibility_and_participation` (C5) is fused SEMANTICS, not a fused label.** `participation` is a
free-form `Optional[str]` (`publication.py:251`) read **raw** at `:302-304` — unlike `continuation`,
`domain`, `movement` and `prohibited_constituents`, which go through `_slot` at `:310-315` and therefore
have an `ExplicitNone`. **Consequence: denied participation is unrepresentable; denied ≡ unresolved.**
The repo's own frozen contract already says the slot is two facts
(`columna_semantic_contract_v1_0.md:1013,1025,1083,1173`).

**Two of v8's named errors are live:**

1. **COUNT is constituted from delivered carrier rows.** `composite.py:160-167` — `n += 1` per admitted array
   element; `c5.value` is stamped into a `ParticipationWitness` at `:153-155` and **never consulted for the
   count**. v8 §4.4 names this: a governed COUNT *"does not silently replace that population with nonzero
   values, supported values, or surviving physical rows."*
2. **The contributing fiber is inferred from surviving rows.** `formation.py:151-162` — the answered
   population *is* the delivered population. v8 §4.1: *"participation cannot be inferred from whichever rows
   survived execution."*

In fairness the successor path **refuses rather than interprets** wherever it can: a null reaching
constitution raises `WantOfState` (*"a fold that silently skips a null has decided what absence means"*),
`admission.py:181-195` refuses carriers with ungoverned absence semantics, `:290-309` refuses null anchor
coordinates. The defect is that **"complete as delivered" is not "the participating population"** — nothing
checks that every participating point arrived.

**v8 §4.4's worked case cannot be expressed.** Three orders participate, one Revenue unsupported,
`OrderCount@A = 3`: support is carrier-wide (`carrier.null_count`, `carrier.py:39-40`), so *"this point
participates and its value is unsupported"* has no representation.

**⚠ Token collision, to be resolved before `NA` is introduced anywhere.** `foundation.py:168` returns
`"not_applicable"` meaning *"the family does not compose, so there is no fold to take"*. v8's `NA` means
*"the location exists, but the measure does not apply."* **Different facts, same token**, and it flows into
C9 and into `admission.py:63`'s `_ENTAILED_NOT_ABSENCE`. It is live on the MEAN path specifically: MEAN is
`NO_CONTINUATION`, so its `empty_fiber` is `"not_applicable"`, where v8 §4.3 says the answer is *the basis is
established as `(0,0)` and the expression is undefined at `n=0`*.

**Out of blast radius, recorded for completeness:** the physical-null-decides-meaning violations
(`planner.py:705` join-artifact nulls; `:722` null→`0`; `:730-732` null→`NA`) are all on the **legacy Core Φ
path**, not the successor path.

**Worked precedent for the repair:** C3 was already split into `C3_FAMILY_DOMAIN` / `C3_EDGE_VALIDITY`, with
`C3_DOMAIN_MOVEMENT` retained as a derived compatibility-only entry excluded from `RESPONSIBILITIES`
(`resolve.py:51-64`, `:433-450`). **That is the sanctioned pattern for a C5 split, mechanism included.**

### A.6 The phase plan (Q8)

**The phase plan is not in the repository.** It is `attachments/d0385442_columna_current_state_and_future_
plan_2026-09-12_FINAL.md` §19, lines 1290-1613. Grep for `"Phase 6"`, `"Phase 10"`, `"Phase 11"` over the
whole tree returns **zero hits**; the repo tracks the same work as **Proof A/B/C**, **Units B/C/D**, **P0-P5**
ledger rows and **OF-nn** forks.

> **No in-tree artifact can be checked against the phase plan by name.** That is a governance finding
> independent of v8.

### A.7 The SSE name

The expansion *"Sufficient State Engine"* appears **nowhere in the repo** — only in the plan. But v8 §9.2
records the rename (*"What that paper called sufficient state is called continuation state here"*), and under
v8 **"sufficient" belongs to the expression side and "state" to the family side**. The name fuses exactly the
two words v8 pulled apart, and attaches them to a component that demonstrably handles both (§A.3).

**`MME` is the wrong replacement, for a repo-specific reason.** *Measure Materialization Engine / Cache(r)*
is an existing, designed, unshipped component with two Huayin-ruled laws from 2026-07-14
(`specs/context/design_capture_execution_positions_v0_8.md:249-284`), rowed as **P5-01**
(`consolidated_ledger_v0_1.md:3176`) and named in the topology record's list of claims it does *not* make
(`topology_core_platform_delivery_v0_1.md:493`). **Renaming SSE → MME would silently merge two components the
architecture deliberately keeps apart, and orphan two standing rulings.** If MME is wanted, it must be ruled
on as a **merge**, not adopted as a **rename**.

**One concrete cost, already being paid.** **OF-58** (`specs/open_forks.md:84`) is filed as *"two state
mechanisms disagree about whether currency gates combination."* Under v8 there is no disagreement:
`state.py combine` gates **continuation-state reuse**, `composite.py continue_composite` composes a
**sufficient basis** — different objects, different currency obligations. **The fork exists because one word
covered both.**

---

## B. v8 impact table

| # | Finding | Class |
|---|---|---|
| 1 | C4 grants family standing on a sufficient-state basis alone (`native_law.py:163-170`) | **IMPLEMENTATION CHANGE** |
| 2 | Two C7 routes emit one provenance token (`resolve.py:361-366`) | **IMPLEMENTATION CHANGE** |
| 3 | No `E` sort exists (`native.py:86`) | **IMPLEMENTATION CHANGE** |
| 4 | Resolution target is family-only; seam at `request.py:97-98` | **IMPLEMENTATION CHANGE** |
| 5 | Durable-`E` token returns `WantOfLaw`, not a capability limit (`request.py:103`) | **IMPLEMENTATION CHANGE** |
| 6 | Expression result served through a family identity slot (`serving.py:943-950`) | **IMPLEMENTATION CHANGE** |
| 7 | `composite.py` already meets v8 §5.3's five obligations | **REINTERPRET** (relabel, don't rebuild) |
| 8 | `continue_composite` continues a basis as family state (`composite.py:200`) | **IMPLEMENTATION CHANGE** |
| 9 | Proof C cannot exhibit its own proposition — left-hand side absent by construction | **REINTERPRET** — reclassify as the §5.3 expression-basis proof; **move the headline to HLL**, which shows both sides in one pair of calls |
| 9b | `composite.py:143-145` hard-codes a 2-component basis | **IMPLEMENTATION CHANGE** — blocks §5.4 moment families |
| 9c | No authored `.cml` declares mean/avg; every AOV is `DERIVED a/b` | **UNCHANGED** — exposure is fixtures and promotion surfaces, not manifolds |
| 10 | Four refusal points enforcing `finalized ≠ state` | **UNCHANGED** — v8 §7.7's hardest rule, already implemented |
| 11 | Root-only materialization (`serving.py:743-749`, `:861-870`) | **UNCHANGED** |
| 12 | `R_F` present as `constitutive_anchor`, not required to be finest | **UNCHANGED** (but see §D.4) |
| 13 | C5 fused semantics; denied participation unrepresentable | **IMPLEMENTATION CHANGE**, gated by **UNRESOLVED** §D.5 |
| 14 | COUNT counted from delivered rows (`composite.py:160-167`) | **IMPLEMENTATION CHANGE** |
| 15 | Contributing fiber inferred from surviving rows (`formation.py:151-162`) | **IMPLEMENTATION CHANGE** |
| 16 | `"not_applicable"` token collision (`foundation.py:168`) | **IMPLEMENTATION CHANGE** — sequence before any `NA` work |
| 17 | Per-point support unrepresentable; §4.4's `10, ?, 20` case | **UNRESOLVED** |
| 18 | `SSE` name fuses the two objects v8 separated | **REINTERPRET** — contract terminology now; name later |
| 19 | `MME` already names a different component | **UNRESOLVED** — needs a merge ruling, not a rename |
| 20 | OF-58 dissolves under the two-sort reading | **REINTERPRET** |
| 21 | Frame-QL **grammar** | **UNCHANGED** — the change is wholly in resolution |
| 22 | Phase plan not in-tree; no name correspondence | **UNRESOLVED** (governance, not v8) |
| 23 | Phases 4, 5, 9, 11 | **UNCHANGED** — Phase 5 blocked by P1-33/34 anchor identity, not by v8 |
| 24 | Phases 0, 3 baselined on v7.1 | **REINTERPRET** |
| 25 | Phase 2 realization resolved by `family_id` only (`serving.py:806`) | **UNRESOLVED** for expression caches |

---

## C. Smallest next implementation unit

**The brief offered a hypothesis — a semantic-target widening around C3/C4 — and asked me to test it rather
than adopt it. Tested: it is the right region and the wrong size, and the ordering is the point.**

You cannot widen the target to admit `E@A` until the system can **tell which objects are `E`**. Today that
discriminator is a prose substring (§A.1). So the target widening is unit **two**, not unit one.

### Unit 1 — make the family/expression boundary machine-readable

Two edits, both at the seam, neither minting a sort:

1. **`resolve.py:361-366`** — give the formation-law route a provenance token distinct from `ENTAILED`.
   Nothing else reads `basis_provenance`; the string `basis_source` already carries the fact in prose.
2. **`native_law.py:163`** — add one premise before the existing C7 clause: C4 refuses family standing where
   C7 is established **only** via a basis the family's own value does not carry. The machine-readable test
   already exists and is already trusted for exactly this discrimination at `composite.py:130`.

**Why this is the right first unit.** It is ~3 lines of semantics. It converts the abolished doctrine from
*silently valid* to *named and refused*. It requires **no new sort, no format change, no grammar change, and
no public-vocabulary change** — so it does not touch the pending format-v2 break (PR #272), and it violates
nothing on the position paper's §9 do-not-change list. And it is a **strict prerequisite** to everything else:
until the two routes are distinguishable, a peer `E@A` target has no criterion for deciding what to accept.

**What it must produce, not just refuse.** Record the missing sort as a `MissingGovernedFact` — the
`MOVEMENT_STANDING_UNDECIDED` pattern already in `native_law.py:118-150` — rather than inventing an `E@A`
kind. That module already declines to make exactly this error.

**What must not be done:** do **not** repair by deleting `resolve.py:364-366`. C7's independence from C8 is a
correct ruling (2026-09-12) and a basis-mediated MEAN is a real governed object. What is wrong is **C4
treating that basis as conferring family standing**, not the basis existing.

### Unit 2 — the peer target at `request.py:97-98`

Only after unit 1. Attach a peer lookup at the `if family is None:` arm; return early. Family path unchanged
byte-for-byte; two downstream call sites; the store needs nothing (`state.py:216-221` keys on `==`, and
`state.py:39-43` already rules that a field's *annotation* may widen per-path without the dataclass changing —
precedent `AnchorOf = Union[str, NativeAnchor]` at `state.py:44`).

### Explicitly deferred

**C5** — correctly, per the brief's warning not to assume it. It is gated on an **UNRESOLVED ruling** (§D.5),
it is identity-bearing (`resolve.py:86-87`) so a declared split is a family succession under §7.3, and the
`NA` work it enables must wait on the token collision (§A.5). The C3 precedent means it is a *known* refactor,
not an urgent one.

**Tests that change meaning under unit 1** — `test_governed_v2.py::test_control_2_mean_has_no_direct_
continuation_and_still_has_a_basis`, `::test_c7_no_longer_follows_c8` (its assertion
`(EXPLICIT_NONE, ESTABLISHED) in pairs` is the exact pair v8 says cannot be a family), and the two `_with_mean`
fixtures declaring `"kind": "family"`. **Proof C's proposition survives verbatim; only the sort of the object
it proves it about changes.**

---

## D. Theory stress

Reported to the standard the brief set: *implementation inconvenience is not a theory defect.* Items 1–3 are
carried from `tod_v8_v0_18_accidental_omission_audit_v0_1.md` and are now **live against the published DOI**.

**D.1 / D.2 / D.3 — WITHDRAWN. Resolved in publication.** These were my first, second and third stress items
against the v0.18 candidate; the published text supplies the ordered-witness path-independence result, the
`FIRST` dual condition, and a refusal rule for incomparable points. See §0. **The ordered-family blocker on
Columna's `ORDERED_W` path does not exist.**

**D.4 — v8 makes `R_F` constitutive; two frozen in-repo contracts eliminated it.**
`manifold_family_declaration_contract_v1_0.md:472` (*"family root / A₀ — **eliminated**"*) and
`columna_semantic_contract_v1_0.md:882` (*"Family root as a separate object — **dies**"*). **Not theory
stress** — v8 §7.6 refutes the argument used to kill it (two incomparable groundings are *distinct family
identities* with an agreement obligation, not one rootless family), and the **code already complies**
(`publication.py:247`). Recorded because the doctrine, not the code, needs withdrawing.

**D.5 — ⚠ v8 requires a distinction this repo ratified as non-existent. This is the live one.**
`sse_contract_v0_1.md:93-96`, ratified 2026-09-14: *"**participation / eligibility / support regime — ONE axis,
not two** … C5 is literally named `eligibility_and_participation`, so a runtime standing that split them would
be modelling a distinction the governed layer does not make."*

**The ratification's premise was that the governed layer does not make the distinction — and its evidence was
C5's name.** v8 §4.1–§4.3 makes applicability, participation and support three separate states. **Not a theory
defect; a ratified decision resting on a v7.1 premise that v8 overturns.** It is a genuine **UNRESOLVED**
requiring Huayin: splitting C5 reverses a ratified §1 axis and widens `Standing.comparable_to`
(`state.py:134-135`) from a 5- to a 6-tuple, which per the OF-39 reasoning must read as STALE rather than
equal — i.e. it needs a scheme bump.

**D.6 — REVISED, and it is now a repo gap rather than theory stress.** I claimed v8 contained no retraction
disclaimer. **It does:** §3.1 l.297 — *"Value closure … does not imply recoverability of prior contributions
or sufficiency for restriction, deletion, correction, or a changed analytical law."* So the theory correctly
**disclaims** sufficiency for deletion without **proving** a retraction law, which is the right posture.

What remains is entirely on the repo side: `invalidate` is listed **NOT IMPLEMENTED** in the SSE contract,
flagged as *"an unanswered governed question with no placeholder"*, and **it is the first operation whose rule
differs by which of the three objects it acts on** — family continuation state, expression sufficient basis,
expression result cache. v8 supplies the sort distinction and the disclaimer; the repo must supply the rule.
`two_pillars_strategy_note_v0_4.md:166-167` (*"mergeable partials **ARE the incremental cache**"*) is the
sentence to revisit first, and `hll_union` has no inverse.

**No remaining item in this section is a defect in ToD v8.0.**

---

## Stop condition

**Stopped at the report, per the brief.** No code, no schema, no rename, no compatibility break. Unit 1 above
is a recommendation, not authorized work.
