# V8-1 · durable governed expression — design stop-gate

**Claude, at Huayin's direction, 2026-09-28.** Answers §5 and §6 of
`attachments/d1e2eb0e_cc_immediate_instruction_tod_v8_migration_v0_1.md`.
**Governing theory:** ToD v8.0, DOI 10.5281/zenodo.23018979.

**Standing.** Design report. **No expression schema is implemented.** Prerequisite V8-0 is merged on
`v8-0/contain-basis-mediated-family-standing` (ruff clean; platform 361 passed; core 1887 passed / 50
skipped). Working candidate per Huayin, 2026-09-28: **native v3.1**, not publication v2, and *"add
expression to `ADMITTED_KINDS`" is not sufficient constitution by itself* — §B takes that as binding.

---

## A. Record shape — the minimum sibling to `Family`

`Family` carries fourteen body keys (`publication.py:192-196`). Mapping v8's required carriers against
them shows the sibling is **not** a subset, a superset, or a variant: it overlaps on five, renames
three, needs three genuinely new, and must **refuse** five.

| v8 requirement (§3.5, §5.3, §7.3) | in `Family` today | for `Expression` |
|---|---|---|
| stable expression identity | `family_id`, opaque, never derived from content | **`expression_id`**, same opacity rule |
| canonical reference / aliases | `canonical_reference`, `aliases` | **same, unchanged** |
| universe | `universe` | **same** |
| constructor / operator-law identity | `formation.law` (a law citation) | **`constructor`**, same citation shape |
| operand identities | `formation.operands` — a **bare tuple** | **`operands`**, but see next row |
| **operand roles** | — nothing. Position only | ⚠ **NEW.** v8 §5.3's basis is role-indexed `(G₁…G_m)`; `composite.Component.law` already keys by role at runtime (`composite.py:110`) with no declared counterpart |
| **constitutive inner anchors** | — one `constitutive_anchor`, and it means the family ROOT | ⚠ **NEW.** `mean(Revenue@Order)@Region` has an inner constitutive `Order` and an outer evaluation anchor; §3.6 makes the inner one identity-bearing |
| participation / scope | `participation` (free-form str) | **same shape**; `scope` is new but may ride the same slot pending the C5 unit |
| **sufficient basis where required** | C7 is **entailed** from a law, never declared | ⚠ **NEW as a declared fact.** `sse_contract_v0_1.md:280` already records composite-basis *declaration* as an unbuilt precondition |
| basis compatibility requirements | `StateBasis.requires_common_participation` — on the **law**, not the declaration | **promote to the declaration** (a per-expression fact) |
| identity-bearing parameters | `formation.parameters` | **same** |
| succession | `fcf` fingerprints + `IDENTITY_BEARING` | **own Σ(E)** — §C |

**Five keys the expression record must NOT have**, each because carrying it would assert a family fact:

- `constitutive_anchor` **as a root.** §3.2's `R_F` is the origin of continuation; an expression has no
  continuation to originate. It is *evaluated at* an anchor, which is a property of a request, not of
  the declaration. Reusing the name would make `serving.py:864-867` treat an expression as rooted.
- `continuation` (C8) — the whole point is that there is none.
- `movement` (C3 edge validity) — movement is family continuation under licence.
- `prohibited_constituents` (`P_F`) — a family-domain law.
- `exceptional` / `empty_fiber` (C9) — an expression's empty behaviour comes from its **constructor over
  its basis**, which v8 §4.3 states precisely for the case at hand: the SUM/COUNT basis is established
  as `(0,0)` and *"the expression is undefined on that basis"* at `n=0`. That is a different fact from
  a law having no fold, which is what `no_composition` now names (V8-0).

### Why not `Family(continuation=None)` — the repo answer, not a stylistic one

The instruction forbids it; the repo supplies the reason. `resolve_family` produces a **total** view
over nine responsibilities and would assign, for such a record: C8 `EXPLICIT_NONE`, C7 `ESTABLISHED`
via the formation route, C9 `{"empty_fiber": "no_composition"}`, and C3 domain/movement standings. **Four
of those are family-only facts, and after V8-0 the first two combine to a guaranteed C4 refusal.** So
the shape does not merely misname the object — it routes it into a resolver whose every answer is
about a family, and then correctly refuses it. An expression needs **its own resolve path** producing
its own (smaller) total view: constructor, operands+roles, inner anchors, participation/scope, basis,
basis compatibility, parameters. Six or seven responsibilities, not nine, and none of them C3/C8/C9.

**Nothing above is added speculatively.** Every new field has either a v8 section requiring it or a
live repo consumer that fakes it today (`composite.Component.law` for roles; `declared_basis` for the
declared basis; `serving.py:943-950` for the evaluation anchor).

---

## B. Publication break — how the sort enters

**Native v3.1, additive, and no second major.** `native.py:72-80` was built for exactly this:

> *"The COMPLETE version strings this build explicitly understands. **A SET** … compatibility must be
> **KNOWN, not presumed**. Adding `"3.1"` is a deliberate act stating this reader understands that
> contract — never inferred from `3.1 > 3.0`."*

| question | answer |
|---|---|
| new top-level kind, or another representation? | **New kind.** `ADMITTED_KINDS` is documented as *"**Positively admitted** … A kind is admitted because something **licenses** it"* — and v8 §8.5 is the licence, naming *"two distinct reusable analytical classes"*. Hiding an expression inside a family body would be the promotion §3.7 forbids, spelled as a schema. |
| how `ADMITTED_KINDS` changes | `{"universe", "family"}` → `{"universe", "family", "expression"}`, **plus** `EXPRESSION_KEYS`, a body parser, a resolve path and Σ(E). Per Huayin: the set entry alone is **not** constitution — it admits a *token*; the contract is the body plus its obligations. |
| do existing family bytes change? | **No. Byte-identical.** v3.0 artifacts carry no expression declarations, and a v3.1 reader reads them unchanged. |
| what do old readers do with v3.1? | **Refuse**, by the contract's own design (`native.py:907-913`). That is the stated intent, not a break in it. |
| publication v2 | **Not backported** (Huayin). v2 also *cannot* do this: `_major` discards the minor — a hole `native.py:78` explicitly declines to reproduce. |
| which fixtures move | **In-tree: only test scaffolding.** `conftest._publication_with_mean` (`:112-126`), `test_governed_v2._with_mean` (`:261-269`), `exhibit.py:163-170`. **No `.cml` declares a mean/avg measure**, and every AOV in every fixture is already `DERIVED aov = revenue / orders` — a post-aggregation expression over two families, already v8-conformant. |
| migration / refusal behaviour | `migrate.py:90-91`'s `_SUGGESTS {"mean":"MEAN","avg":"MEAN"}` must propose an **expression**, not a family formation law. A v3.0 artifact declaring a basis-mediated family should migrate *by proposal to a human* (the existing v1→v2 posture), not silently: the sort change is a succession, not a re-spelling. |

**No shim.** The current format state does not force one: the additive route means old bytes keep
working and new bytes are refused by old readers, which is the contract's normal behaviour.

---

## C. Identity and succession

**Σ(E), from v8 §7.3's own list:** constructor · operand identities · operand roles · constitutive
inner anchors · participation and scope · identity-bearing parameters. A change to any yields a
**successor expression** unless governed equivalence establishes continuity.

**Reusable as-is:** the `fcf` constitution-fingerprint *mechanism* (`native.py:296-320`) — it hashes a
declared body and is sort-agnostic; the `CURRENT / STALE / SCHEME_MISMATCH` triad (`native.py:174-180`);
and the `Standing` / `LawView` totality discipline, which is the best thing in the governed layer and
should be copied in shape.

**Must NOT be reused — each would assert a family fact:**

- `IDENTITY_BEARING` itself. It is Σ(F): it contains C4 formation, C5 participation, C6 semantic values
  and C8 continuation. An expression has no C8, and its C6 is derived from its constructor.
- `resolve_family`, for the reason in §A.
- `constitutive_anchor` as an identity field, for the reason in §A.
- Family lineage. §7.1 keeps **family / expression / carrier** lineage apart; an expression's ancestry
  runs through its operands, which are families, so the edge is *expression → family* and must not be
  recorded as a family→family constitutive edge (`Family.parents` derives exactly that today).

**One gap v8 leaves and the repo will hit:** `governed equivalence` is the escape clause on both
succession rules (§7.3 ×2, §7.6) and v8 never defines it. v7.1 §6.6 did — the equivalence must be a
**congruence** with respect to `⊕` and must preserve constructor outputs. That is an errata candidate,
recorded in `tod_v8_v0_18_accidental_omission_audit_v0_1.md`, and V8-1 should not invent a local
answer.

---

## D. Resolution seam — confirmed

**`request.py:97-98`**, the `family = pub.resolve_reference(token)` call and its `if family is None:`
arm. Attach the peer lookup there and return early.

- **Everything above is sort-agnostic**; everything below is family-root law without exception.
- **22 of the 23 intrinsically family-only sites are downstream of it** and are never reached.
- The family success path changes **by zero bytes**; downstream blast radius is two call sites
  (`serving.py:598`, `:766`), both already inside `_translated` (`serving.py:682`), so a peer inherits
  the refusal→wire contract rather than restating it.
- The arm **already names the gap in prose**: *"does not evaluate expressions."*

**Peer target, not a widened `AnalyticalIdentity` — and the repo's own test argues for it.**
`test_analytical_identity_still_carries_exactly_two_fields` guards **storage and constitution** leaking
into identity, not *sort*; a peer type does not violate it, widening the dataclass would. And
`state.py:39-44` already rules that a field's *annotation* may widen per-path without the dataclass
changing (`AnchorOf = Union[str, NativeAnchor]`), which is the precedent for a second inhabitant —
while `state.py:216-221` keys retrieval on `==` alone, so the store needs nothing.

**One defect to fix at the same seam.** That arm raises **`WantOfLaw`** — a governed verdict, *"no
governed family answers to the reference"* — where a durable expression name should be a **capability
limit**. Today it sends a steward to correct a publication that is correct.

Target dispatch, matching the instruction's four cases: family name → existing path; durable expression
name → peer path; unknown name → unresolved/refusal; request-local composed expression → expression
path; and `Op(F@A)@B` rewritten to `F@B` **only** where the bound family law licenses that edge (§8.6).

---

## E. Proof C migration

`composite.py` already satisfies **all five** of v8 §5.3's obligations (V8-0 report §A.4). It survives
as the expression-basis implementation, with the sort corrected around it.

| current | becomes | note |
|---|---|---|
| `declared_basis` (`:123-135`) reading C7 off a **family** `law_view` | **sufficient-basis declaration**, read off the expression record | the one deep change; nothing else can land first |
| `ParticipationWitness` (`:58-84`), `pair` (`:179-197`) | **participation compatibility** | survives verbatim; states §5.3's joint-compatibility obligation better than the manuscript does |
| `Component.continues_under` read from `LAWS`, never from the name (`:91-96`) | **role alignment** | survives verbatim |
| one anchor, one pass, one `pass_id` (`:138-176`) | **anchor locality** | survives |
| `finalize` (`:251-283`), standing checked **before** the division | **finalization** | survives |
| `Finalized(is_sufficient_state=False)` (`:239-247`) + the four refusal points | **expression result** | survives — v8 §7.7's hardest rule, already implemented |
| `continue_composite` (`:200-235`) returning a `CompositeState` under **one `family_id`** | **re-describe**: the basis *families* continue under their own laws; the expression is **re-evaluated** at the target | arithmetically already correct — it reads each component's law from the foundation — but the return type asserts family continuation |
| `basis.components != ("SUM","COUNT")` hard-code (`:143-145`) | **generalize to role-indexed `(G₁…G_m)`** | a 2-component hard-code cannot host §5.4's `(Count, SumX, SumX², SumXY)` |

**Family-only artifacts that should retire:** the MEAN family declarations in
`conftest.py:112-126`, `test_governed_v2.py:261-269` and `exhibit.py:163-170`; `CompositeState.family_id`
as a name; `migrate.py:90-91`'s law suggestion. **Roughly 70% of `composite.py` survives unchanged.**

**Dissolved as a side effect:** **OF-58** — filed as *"two state mechanisms disagree about whether
currency gates combination."* Under the two sorts there is no disagreement: `state.combine` gates
**continuation-state reuse**, `composite.continue_composite` composes a **sufficient basis**. Different
objects, different currency obligations. The fork exists because one word covered both.

---

## F. Format timing — recommendation

**The question as posed is moot: the hard one-sort break is already merged** (PR #272, 2026-09-11; head
`78f25ed` an ancestor of `main`; `SUPPORTED_PUBLICATION_FORMAT_MAJOR = 2`, v1 retired;
`NATIVE_PUBLICATION_FORMAT_VERSION = "3.0"`). No open PR carries a format break. The ledger heading at
`consolidated_ledger_v0_1.md:3558` still reads *"landed — pending review, not merged"* and is stale;
**it should be corrected, because it is load-bearing prose that has already misled one analysis (mine).**

**Recommendation: land the expression sort as native v3.1, additively, and do not wait for anything.**
The "two consecutive majors" concern that motivated the hold does not arise — a v3 minor is the
contract's own designed mechanism, existing family bytes are untouched, and old readers refuse new
bytes by intent. **The sequencing constraint is not the format; it is §A's resolve path.** The sort
token is cheap and the constitution is not, so the order is: body contract + resolve path + Σ(E)
first, `ADMITTED_KINDS` and `SUPPORTED_NATIVE_VERSIONS` last, as the act that *admits* what is by then
already defined.

---

## §6. Operator registry — reconnaissance addendum, no implementation

**The division today is nearly the ruled one already.** `foundation.FoundationLaw` says of itself
*"Semantic content only"* and holds: `target_form`, `operand_domains`, `result_domain`,
`entails_continuation`, `sufficient_state`, `approximation`, `state_basis`, `required_parameters`,
`usable_as_continuation`, `composition`, `has_identity`. **That is a semantic authority in shape and in
discipline** — including its refusal to add a "positively denies any basis" field until a law needs it.

`operators.Operator` is a realization registry — `deliver_sql` (a SQL lambda), `scan_impl`, `in_core`,
`needs_window`, `kind` dispatch — **with four semantic facts stranded in it**:

| stranded fact | why it is semantic | already on the law side? |
|---|---|---|
| `re_entrant` | certifies `ρ((+)ᵢ η(ρ(sᵢ))) == ρ((+)ᵢ sᵢ)`; its own comment calls it *"strictly stronger than monoidality"* | no — and it is the v8-critical one, see below |
| `is_monoid` | an algebraic theorem | yes, as `has_identity` + `entails_continuation` |
| `linear` | a symbolic/algebraic property (the WP-B gate) | no |
| `combine` | *"how witnesses merge"* — v8 would call this the continuation law | yes, as `composition` |

And one **duplicated axis**: `accepts` / `out_rule` versus `operand_domains` / `result_domain`.

**Recommendation: `foundation` becomes the single semantic authority; `operators` becomes a provider
realization profile over it.** Do not create a second catalog — and note that `operators` does not
disappear, because `deliver_sql`, `scan_impl` and `in_core` are genuinely per-provider facts that v8
§8.7 places in a different jurisdiction. The four stranded facts migrate, or remain as **derived
projections** of the law; the duplicated signature axis collapses onto the law.

**One semantic responsibility that genuinely cannot fit as currently written, and must change rather
than move.** `operators.py:96-99` *forbids* conditional certification: *"If type, order, support or
anchor conditions would qualify the certification, the case must NOT be flattened into True; it stays
uncertified."* That is sound engineering against a **boolean** flag — and v8 §3.5 requires exactly the
conditional case it refuses: a mean is value-closed *"where the averaged population is a declared
governed geometry with total participation."* So re-entry cannot migrate as a `bool`; it must become
**edge- and condition-relative**, which is also what v8 §3.1 means by value closure holding *"only for
the continuation region over which this condition holds."* **This is the one place where the registry
consolidation is blocked by a semantic change rather than by a refactor**, and it is the same change
V8-1's declared-basis work needs anyway.

---

## Theory stress

**None.** Every difficulty above is stale doctrine, missing repo representation, or implementation
work. The one item in the earlier recon that reached past the published theory — `invalidate` having no
retraction law — is confirmed **not** a v8 defect: §3.1 disclaims it explicitly (*"Value closure … does
not imply recoverability of prior contributions or sufficiency for restriction, deletion, correction,
or a changed analytical law"*). What the repo still owes is a rule that differs by sort, which is a
repo obligation v8 correctly declines to pre-empt.

One **errata candidate** bearing on §C, not a contradiction: `governed equivalence` is load-bearing in
§7.3 and §7.6 and is never defined; v7.1 §6.6's congruence obligation is the missing definition.
