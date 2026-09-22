# C4 · Is the resolved identity lawfully answerable? — implementation record

**2026-09-22.** Unit C4 of the native-consumer sequence. **Construction, not demolition:** nothing
retired, no producer change, no v2 repair, no Platform redesign, and — the standing instruction for
this unit — **no native movement contract invented.** C4 reaches a genuinely missing governed fact
and stops with it characterized.

Suites green — `columna-platform` 326, `columna-core`, `columna-server`. 20 new tests; two C3 tests
rewritten where C4 corrected a layering (§12).

---

## 1 · The exact question C4 must answer

    C3 · WHICH analytical point is being asked for   -> U's constitution + derived geometry
    C4 · MAY that point be answered, and from what   -> Law(F)

Stated as one question: **may `F` lawfully stand at `A`, and is there a governed basis from which a
value of `F` at `A` can be determined?** It decomposes into two, and keeping them apart is the whole
of the unit:

* **sufficiency** — does a governing law establish a sufficient-state basis for `F` at all?
* **admission** — is `A` among the anchors `F` is admitted to stand at? Asked *only* when `A` is not
  the constitutive anchor; at the constitutive anchor the question does not arise, because
  *constitutive* is what it means for the family to be established there.

## 2 · The minimum governed facts required

Two responsibilities of `Law(F)`, and nothing else:

| fact | responsibility | read from |
|---|---|---|
| a sufficient-state basis exists | **C7 · `sufficient_state_bases`** | entailed by the family's continuation law (or its formation law) |
| `F` is positively admitted at a non-constitutive `A` | **C3 · `domain_and_movement`** | the family's own declared movement content |

**Not required:** the universe's constitution, the denotation table, the derived geometry, an anchor
declaration, a basis, a level, a realization mapping, a coordinate type, or any physical fact. The
decision function's signature is `assert_answerable(view, *, moving: bool)` — **there is no anchor in
it**, and a test reads that off the identifiers the function evaluates.

**C7 is asked first, and the reason is the remedy.** Both refusals can be true at once; the ruled
diagnosis order surfaces the one whose remedy is upstream. A family with no governed basis is
unanswerable at *every* anchor, so reporting the movement gap first would send a steward to license
a movement that still could not be answered.

## 3 · Is Law(F) finally required, and which part?

**Yes. C7, and — for a non-constitutive ask — C3.** This is the first unit in the sequence that
needs `Law(F)` at all, and it needs it because the question *is* a question about the family's own
governed law, not because an engine demanded a data structure.

⟨measured⟩ `Law(F)` resolves **totally** for a native family, from the family's own declared clauses:

```
Law(F) — berthings  [fam_Nq4WfR8kPxDvZc2TmLbJhY]
  target_specification           established (declared)
  identity_and_ancestry          established (declared)
  domain_and_movement            unestablished
      · §4.1: 'A geometrically available projection and a computable state operation do not by
        themselves put A in the admitted anchors.' Absence of a prohibition is not permission
  formation                      established (declared)
  eligibility_and_participation  established (declared)
  semantic_values                established (declared)
  sufficient_state_bases         established (entailed)   · entailed by the continuation law SUM
  continuation_and_agreement     established (declared)
  exceptional_cases              established (entailed)
  VALID: yes
```

and the decision, per ask:

```
SELECT berthings AT {berth * day}    at its anchor      ANSWERABLE
SELECT berthings AT {berth}          target=['berth']   WantOfLaw — no positive movement
SELECT berthings AT {}               target=[]          WantOfLaw — no positive movement
```

**Resolving that view consulted no anchor declaration, no `universe.body`, no basis, no level, no
denotation table and no geometry.** That is not a fact about the native reader — it is a fact about
`Law(F)`: **the nine responsibilities are a family's statement about itself.**

## 4 · Do the existing movement licences represent those facts natively?

**Only as a legacy implementation mechanism, and only partially** — and its own module says so:

> *"a RUNTIME PROJECTION — not a governed serialization… The governed v2 artifact carries `movement`
> as an opaque slot with no shape, and Proof B does NOT give it one. The permanent serialization
> question stays open."* — `columna_platform/movement.py`

Split into its two halves, the answer differs:

* **the structural half** — *is this coarsening realizable at all* — is verified by
  `declared_coordinate_names(pub, anchor)`, i.e. by reading an **anchor declaration**. It has no
  native referent, and natively the same question is answered *better*: `Anchor.refines` /
  `projection_forgets` are theorems of the closed individuation rather than reads of a declaration.
* **the authority half** — *may this family be moved* — is identified by a pair of anchor **NAMES**
  plus a `POSITIVE` token and a law. The *fact* is natively expressible; **its representation is
  not**, because natively there are no anchor names.

**The licence already draws C4's own distinction, in the same words:** *"the subset check answers
'could this coarsening be realized at all?' and the licence answers 'may this family be moved?' —
and the first never answers the second."* So the division is not new doctrine; what is new is that
natively the first half is computed from law and the second half has no contract.

## 5 · Does sufficient state or family structure become necessary?

**Sufficient state: yes, as a STANDING — not as state.** C7 is consulted, and nothing is retrieved,
established, folded or materialized. The question is *does a governing law establish a basis*, which
is a fact about `Law(F)`; whether a state exists is the next unit's question and was not asked.

**Family structure: only lineage, and only for constructions.** `resolve_family` asks a publication
for exactly one thing — a parent family by `family_id`, which is §3.7's lineage edge. Witnessed by
handing it a holder whose entire public surface is `family(family_id)`. Both native fixture families
are primitive, so even that is unused there.

## 6 · Derivable from the artifact vs. separately governed

**Derivable from the native artifact, wholly:** every one of the nine responsibilities for both
fixture families, including C7's basis (entailed by the cited continuation law) and C9's empty fiber
(entailed, never re-asked). ⟨measured⟩ `VALID: yes`.

**Separately governed, and genuinely absent:** the content of C3 — see §9.

## 7 · Can one semantic rule operate on both paths without translating either anchor model?

**Yes, and it is witnessed rather than argued.** The convergence question was asked in the only form
that can be answered: write the rule so that an anchor model *cannot* enter it, then run it over both
paths' views and see whether it still says everything it needs to.

```
── the SAME rule over a LEGACY law view, neither anchor model translated ──
  revenue (v2)  moving=False -> ANSWERABLE
  revenue (v2)  moving=True  -> WantOfLaw: 'revenue' establishes no positive movement…
```

Both paths reach the same verdict for the same reason: C7 ESTABLISHED, C3 UNESTABLISHED. **The v2
serving path is untouched** — it still asks its own version of these questions in its own code; this
is the native rule being shown to apply to a legacy `LawView`, not a replacement of anything.

**And the reason it works is worth stating precisely, because it is narrower than "the paths have
converged".** `Law(F)` is anchor-free, so a rule expressed over `Law(F)` is anchor-free. `moving` is
a boolean the CALLER computes from *its own* anchor model — a native caller from constituent-set
containment, a legacy caller from a declaration-name comparison. **The shared rule sits exactly one
level above the disagreement, and the disagreement is still total underneath it.**

## 8 · Where existing execution machinery demanded a legacy-shaped object

**One site, and it turned out not to be legacy-shaped at all.** `resolve_family` consumes a
`governed.publication.Family` — a v2 module's dataclass. ⟨measured⟩ format v3's total family-body key
set and v2's `_FAMILY_KEYS` **are the same set**, key for key, and every clause means the same thing
in both, so a native family body parses through `parse_family_declaration` **verbatim**. `universe`
and `constitutive_anchor` are read there as required strings and consumed by no rule.

So the object is not a v2 object wearing a shared name; **it is the family-clause contract, which
both majors carry unchanged.** It was given a public name (`parse_family_declaration`, an alias of
the existing `_family`) because a second major now consumes it — an addition that renames nothing
and retires nothing.

**One discrepancy, recorded rather than smoothed.** `C2 · identity_and_ancestry` carries `universe`
and `constitutive_anchor` in its **value** — two nominal references native identity has deliberately
left behind (`fcf-2` removed both from the payload). Nothing consumes them, so nothing is wrong
today; a consumer that began reading `C2.value` for meaning would be reading a spelling on the native
path.

## 9 · New governed fact genuinely missing from the v3 artifact

**One, and C4 stops on it.** Characterized, with no candidate encoding:

```
MISSING : which analytical locations of U, other than its own constitutive anchor, a family F is
          ADMITTED to stand at — and under whose authority. Natively the target location is a
          constituent set that geometry can show exists; what no governed fact states is whether
          F may occupy it
WHOSE   : the steward who constitutes F, as a positive declaration about F — §4.1: 'a geometrically
          available projection and a computable state operation do not by themselves put A in the
          admitted anchors'
WHERE   : the family declaration's C3 slot, which both majors already carry as a total key and
          neither has given a content contract
```

**It is not an absent key.** `movement` is in the total family-body key set of *both* majors; what has
never been decided is what goes in it. v2's reader accepts arbitrary content for it
(`_slot(…, lambda r: r)`), and the only thing in this tree that builds a movement is a runtime
projection its own module declines to call a serialization.

Consequently C4 refuses in **three distinguishable ways**, and the distinctions are the deliverable:

| situation | verdict |
|---|---|
| C3 UNESTABLISHED, or ESTABLISHED with a domain and no movement | *establishes no positive movement* — absence is never permission, and **the standing is not the test**: C3 is `domain AND movement`, and testing `standing == ESTABLISHED` would serve a coarser anchor for a domain-only family with no licence at all |
| C3 EXPLICIT_NONE | *the family has DECLARED that nothing moves* — a positive negative, said in its own words |
| C3 carries POSITIVE movement content | **STOP.** *"this path has no governed reading of it. The content is preserved, not rejected"* — what a native movement declaration means is undecided, and a profile that guessed would be authoring the contract rather than consuming it |

The third row is where the unit ends. Reaching it is the result; filling it is not C4's to do.

## 10 · Legacy assumptions that became unreachable

* *"deciding answerability requires an anchor model"* — the rule's parameter list has no anchor in
  it, and a test reads that off the identifiers it evaluates.
* *"the structural half of a movement is read from an anchor declaration"* — natively it is a
  theorem of the closed individuation, computed before any standing is asked about.
* *"a movement is identified by a pair of anchor names"* — there are no anchor names.
* *"C3 ESTABLISHED means a movement is licensed"* — already known false in the v2 serving path, and
  natively it cannot even be reached by accident: the content is inspected, never the standing.
* *"resolution decides whether the ask is permitted"* — C4 moved that out (§12).

## 11 · Does the evidence now establish a convergence boundary?

**No — one more layer remains, and C4 has narrowed where it can be.**

What C4 establishes is real and bounded: **a rule expressed purely over `Law(F)` runs on both paths
and translates neither anchor model.** That is the strongest convergence evidence in the sequence so
far, and it is *not* the claim that Law(F) is the convergence boundary. Three reasons to withhold it:

1. **The rule converges because `Law(F)` is anchor-free — and the anchor disagreement is still total
   one level below it.** `moving` is computed by the caller from its own model. A boundary that holds
   only because the contested object was passed as a boolean has not resolved the contest; it has
   located it.
2. **The decision was reached, and nothing was answered.** Everything below — retrieving or
   establishing state, admission against a realization, folding, serving a frame — is untouched, and
   §12.6's semantic-type question and the `(universe_ref, constituent)` realization addressing are
   exactly where a legacy-shaped demand would next appear. The recon's own C4 (*the realization
   boundary*) is that layer and has not been done.
3. **The movement branch is unfinished by ruling.** The one fact C4 needed and could not get is
   undecided, so the decision rule has been exercised on its established path and *stopped* on its
   other one. A boundary claimed from a rule half of whose branches are unreachable would be claimed
   too early.

> **The sequence's running finding, one level further down:** identity and availability converge
> (C2); analytical identity converges structurally and not semantically (C3); and now **the
> answerability RULE converges while the anchor model beneath it does not.** Each layer has
> converged on a form that is silent about anchors — which is evidence about where the boundary is
> *not*, and is accumulating toward, but does not yet establish, where it is.

## 12 · A layering C4 corrected

C3 refused a coarser ask **during resolution**. The refusal said the right thing in the wrong place:
resolution answers *what is being asked for*, and standing is decided against `Law(F)`, which the
resolver may not see — and refusing there left the standing question **unreachable**, so nothing
could ever be asked to license it. (The v2 resolver had already drawn this line for its own reasons
and states it in nearly the same words; the agreement is reported, not treated as a template.)

So `native_request.resolve` now concludes only what geometry establishes — a coarser ask resolves and
`target` carries it — and a **non-projectable** ask still refuses *at resolution*, because that is a
fact about geometry and not about standing: if the target cannot be obtained by lawful universe
geometry, the problem is not a missing licence. Two C3 tests were rewritten to witness the corrected
layering; nothing else in C3 moved.

---

## 13 · Carried forward

* **OF-59** untouched, as ruled. C4 made no canonicalization claim; its fixture variants are minted
  with the consumer's own derivation and witness the *shape* of a family's declared law, not
  agreement with the producer.
* **F-3** fixture debt untouched; no new copies taken.
* **The C2 value discrepancy** (§8) is new and small, and is recorded here rather than rowed: it has
  no consumer today.
