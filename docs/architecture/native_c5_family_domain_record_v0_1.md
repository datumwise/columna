# C5 · the primitive-family Case-S domain — unit record

**One governed fact was added to the model and nothing else.** The rest of the rule was already
shipping: the family root, the refinement order, and the set difference that derives what a
projection forgets. This unit declares the fact, derives the domain from it, and stops.

Authorization: steward, 2026-09-22 (R13, corrected R14, R11, R12, and the explicit holds).
Contract: `c3_primitive_family_domain_contract_v0_1.md`. Theory: `tod_v7_2_development_addendum_v0_1.md`
§A.1–§A.2.

---

## 1 · The rule, measured

⟨VX⟩ against the shipped native fixture — universe `harbour` = `{berth, day}`, `berthings` rooted at
`A_0 = {berth, day}`:

```
 P_F               standing        AT {berth * day}          AT {berth}
                                   forgets []                forgets ['day']
 absent            unestablished   ADMIT                     REFUSE
 explicit-none     explicit-none   ADMIT                     REFUSE
 declared []       established     ADMIT                     ADMIT
 declared ['day']  established     ADMIT                     REFUSE
 declared ['berth'] established    ADMIT                     ADMIT
```

**Read the third and fifth rows against the first.** `declared []` and `absent` differ — that is the
whole distinction the responsibility exists to carry, and collapsing them would re-enact the
family-admission test ToD v7.1 Appendix C.4 withdrew. `declared ['berth']` and `declared []` agree —
that is R14: a governed constituent irrelevant to *this* projection is lawful and inert.

**Every row admits the root, and none of them takes an exception to do it.** `Forgotten(A_0 → A_0)`
is empty and the empty set meets no prohibition, so the root passes the ordinary rule — including in
the row that prohibits *both* of the universe's constituents.

The refusal names what exceeded the law:

> `'berthings' may not stand at harbour{berth}: its governed family-domain law prohibits losing
> ['day'], and the projection from its family root harbour{berth, day} forgets ['day']. The family
> is defined at its root and at the locations its own law admits; this is not one of them. No
> movement, licence, re-realization or coarser plan can supply what the family's law withholds`

---

## 1b · Suite standing, measured against a pristine baseline

⟨VX⟩ the branch was compared against an untouched `main` worktree, same interpreter, same run:

| | branch | pristine `main` |
|---|---|---|
| `columna-core` | **1847 passed, 0 failed**, 50 skipped, 38 errors | 1845 passed, **1 failed**, 50 skipped, 38 errors |
| `columna-platform` | **342 passed** | — |
| `columna-adbc` | **68 passed** | — |

**The 38 errors are pre-existing and identical on both sides** (`test_pin_verdict_truthfulness`,
`test_plan_run_standing`); they are not this unit's and are not repaired by it. The baseline's single
failure (`test_fixture_drift::test_import_and_version`) reproduces on `main` and passes on the
branch; it is sensitive to an editable install being present, not to this change. `ruff` is clean
across every changed package.

Two incidental defects were found and deliberately **not repaired**, per the unit's holds: the
`exhibit.py` demo crashes on `main` with `materialize() missing 1 required keyword-only argument:
'publication_ref'` (verified on the pristine baseline — its C3 read, the part this unit touches,
works); and the repository's own test extras omit `pytest-asyncio`, without which the server's MCP
tests cannot run at all.

---

## 2 · What changed

| file | change |
|---|---|
| `governed/publication.py` | `prohibited_constituents` in `_FAMILY_KEYS`; a real reader (`_prohibited_constituents`); `Family.prohibited_constituents` |
| `governed/native.py` | same key in `FAMILY_BODY_KEYS`; **`NON_IDENTITY_KEYS`** (R12); representation + governed-reference validation at the artifact boundary |
| `governed/resolve.py` | **C3 split** into `C3_FAMILY_DOMAIN` and `C3_EDGE_VALIDITY`; the pre-split entry retained, derived, compatibility-only |
| `columna_platform/native_domain.py` | **new** — the predicate, the scope gate, and the characterized constructed-family fact |
| `columna_platform/native_law.py` | reads `C3_EDGE_VALIDITY`; `MOVEMENT_STANDING_UNDECIDED` narrowed to the edge half |
| `columna_platform/serving.py` | **docstring only** — records that the question it left open is now ruled. No behaviour change |

---

## 3 · Three findings

### F-1 · The comment had stated the ruling all along

`resolve.py`'s own comment above the C3 block read *"Two POSITIVE declarations are required for
admission (§4.1): the anchor must be in the declared domain **AND** the movement licensed"* — while
the code one line below tested a **disjunction**. The conflation was not a considered design; it was
a comment and an implementation that had disagreed since they were written. The split is a repair.

### F-2 · Representation validation had to move to the artifact boundary

The first implementation validated `P_F`'s shape in the family-clause reader — which is reached only
when a consumer later resolves the law. ⟨measured⟩ a malformed clause then **published cleanly and
failed at use**. The check now runs in the native reader, where every other governed clause is
checked, so the artifact refuses at its boundary. Found by a test that expected a refusal and got
none; recorded because the same trap exists for any future governed clause added to the body.

### F-3 · The legacy path was preserved by NOT repointing it

`serving.py` distinguishes three no-licence cases, and the third — *"C3 is established by its DOMAIN
alone"* — exists **only** because of the conflation. Repointing it to `C3_EDGE_VALIDITY` would have
deleted a legacy diagnostic. The authorization is to preserve legacy behaviour and report the
collision rather than force convergence, so the pre-split entry is retained, derived from the two new
ones, and read only by v2. The native path never reads it. **There is no second source of truth.**

---

## 4 · What was preserved, and what was withdrawn

**Preserved.** `Law(F)` resolution consults no anchor model; `assert_answerable` keeps its exact
anchor-free signature and its AST test passes unchanged; `_ParentLookup`'s surface stays `{"family"}`;
C7 is still asked first; geometry refusals stay geometry refusals; the explicit-none path keeps its
own words; ⟨measured⟩ **nothing on the wire moves** — the native spine still has no production
callers and the v2 serving path is untouched.

**Withdrawn.** C4's stronger claim that the *complete* answerability decision can remain anchor-free.
Resolving the family law is anchor-free; **applying its domain condition to a requested `A` is a
relation to a location and necessarily consumes geometry.** The rule was not bent to preserve the
claim — the predicate moved one layer up, to where the law and the resolved geometry are both
legitimately in hand. A new test pins the narrowing so the withdrawn claim cannot be silently
re-adopted.

---

## 5 · Where this unit stopped

**Constructed families.** The scope gate is `formation.kind == PRIMITIVE`, read from a field the
reader already validates strictly. A construction reaching the domain question raises
`CONSTRUCTED_DOMAIN_UNDECIDED` — the fact, whose it is, and where it would belong — and supplies no
derivation, no propagation, no union and no default. ⟨measured⟩ **no multi-operand construction
exists anywhere in the tree**, and the native fixture has none at all.

**The wire distinction.** Four outcomes are now mechanically distinguishable — non-existent geometry,
no domain law, outside the domain naming the constituent, and constructed-and-undecided. **All four
still surface as `want_of_law`.** The closed registry has no member whose governed subject is the
requested output location's admission; minting one is a separate ruling. `anchor_spent` was NOT
reused — it is an aperture-spending reason with a different governed subject. **This is the boundary
this unit stopped at, as instructed, rather than letting wire vocabulary decide analytical semantics.**

Also held and untouched: `Γ_F(B→A)` content, coverage `γ`, participation and support, evidence,
commutation, Case G, relationship expansion, cross-universe movement, any general movement calculus,
`MovementLicence`, P1-36 repair, and Frame-QL syntax.
