# V8-1 · the durable governed expression — implementation record

**Claude, at Huayin's direction, 2026-09-28.** Implements the V8-1 design stop-gate
(`v8_1_durable_governed_expression_design_stop_gate_v0_1.md`) under the eight rulings of 2026-09-28.
**Governing theory:** ToD v8.0, published 2026-09-28, cited by version and section throughout — the
publication registry carries no record for v8.0 and `scripts/check_publications.py` fails closed on an
unregistered identifier, so the identifier is registry business (see §H).

**Standing.** Implementation. Prerequisite V8-0 is on `v8-0/exact` (PR #345), and this unit is stacked
on it, not merged into it — the stop-gate boundary is preserved as two branches and two review units.

---

## A. The expression record — `native.Expression`

A **sibling** of `Family`, built as one. Not `Family(continuation=None)`, not routed through
`resolve_family`, and sharing with the family reader only the strictness helpers (`_strict`, `_obj`,
`_req`) — the discipline, not the contract.

### Envelope — `EXPRESSION_KEYS`

| key | required | note |
|---|---|---|
| `kind` | ✓ | `"expression"`, admitted at native v3.1 and at no earlier minor |
| `name` | ✓ | the declaration name |
| `body` | ✓ | below; TOTAL at key granularity |
| `expression_constitution_authority` | ✓ | `ExpressionAuthority`; scheme must be `ecf-1` |
| `universe_authority_binding` | ✓ | **required**, unlike a family's — see §C |

### Body — `EXPRESSION_BODY_KEYS`

| key | required | in Σ(E) | note |
|---|---|---|---|
| `expression_id` | ✓ | — | opaque; identity is not part of its own determinant |
| `canonical_reference` | ✓ | — | a label |
| `aliases` | | — | labels |
| `universe` | ✓ | nominal | the SPELLING leaves the `ecf-1` payload; the world is governed through the binding |
| `constructor` | ✓ | ✓ | a `(vocabulary, version, law)` citation, validated as a citation and **not resolved at read** |
| `operands` | ✓ | ✓ | `[{role, family_id}]` — **role-indexed**, roles distinct, every reference resolving in this publication |
| `inner_anchors` | | nominal | the CONSTITUTIVE INNER anchors (§3.6); resolved into the payload as `_inner_anchors` |
| `participation` | ✓ | ✓ | |
| `scope` | | ✓ | |
| `parameters` | | ✓ | identity-bearing parameters |
| `admitted_bases` | | **✗ — ruled out** | `[{basis_id, components:[{role, family_id}], requires_common_participation}]`; zero, one or several |

### The five family keys that are ABSENT, each with its reason

`constitutive_anchor` (§3.2's `R_F` is the origin of continuation, and an expression has none to
originate; it is EVALUATED at an anchor, which is a property of a request) · `continuation` (C8) ·
`movement` (C3 edge validity) · `prohibited_constituents` (`P_F`, a family-domain law) · `exceptional`
(C9; an expression's empty behaviour comes from its constructor over its basis — §4.3's `(0,0)`).

There is no `anchor_token` on the record either. The **absence of the singular is the point**:
reducing several inner anchors to one would be inventing a root.

**Ruling 4, executable.** `admitted_bases` is a TUPLE and is OUT of Σ(E). *A sufficient basis is an
establishment route; v8 allows more than one for the same expression; expression identity ≠ one
particular sufficient basis used to establish it.* Two consequences the default would have got wrong:
admitting a second lawful route would have minted a successor, and two artifacts admitting different
subsets of the same routes would have been two expressions.

---

## B. Expression resolver responsibilities — `expression.resolve_expression`

A TOTAL view over **seven** responsibilities. None of them is a C3/C8/C9, and the intersection with
`resolve.RESPONSIBILITIES` is empty — asserted by a test.

| | responsibility | in Σ(E) | what it settles |
|---|---|---|---|
| E1 | `constructor` | ✓ | the operator law resolves in the cited vocabulary version; reports whether the constructor's own algebra carries a continuation, and does **not** adjudicate on it (§5.4's moment families are continuation-bearing and lawful) |
| E2 | `operands_and_roles` | ✓ | every operand's governed value domain is admitted by the constructor. **Arity is reported UNCHECKED** — no law in `foundation` states a signature |
| E3 | `constitutive_inner_anchors` | ✓ | DECLARED, or ENTAILED from the operands where they agree; UNESTABLISHED where they disagree, rather than picking one |
| E4 | `participation_and_scope` | ✓ | ONE responsibility. The C5 applicability / participation / support split stays deferred (ruling 9) |
| E5 | `admitted_bases` | ✗ | zero / one / several; coverage, the law's participation requirement, continuation congruence, and declared common participation |
| E6 | `basis_agreement` | ✗ | *alternative lawful bases must agree*; `EXPLICIT_NONE` below two |
| E7 | `identity_bearing_parameters` | ✓ | the constructor's `required_parameters` are supplied; no default is invented |

`ExpressionView.valid` runs over **Σ(E) only**, so an expression with no admitted basis is VALID and
not EVALUABLE — two questions, deliberately separate, because fusing them is the fusion V8-0 had to
unpick at the C7 seam. `establishable` is the second question.

**What is reused from `resolve`:** the standing VOCABULARY only (`Standing`, and
`established`/`explicit-none`/`unestablished` with their provenances) — sort-agnostic by content.
**What is not:** `LawView` (keyed by `family_id`, validity over Σ(F)), `IDENTITY_BEARING` (which IS
Σ(F) and contains C4/C5/C6/C8), `resolve_family`, and family lineage — an expression's ancestry runs
through its OPERANDS (`Expression.operand_family_ids`), and a basis is a route to a value, not a
parent.

### Two limits named rather than papered over

1. **Continuation congruence cannot distinguish two component laws that entail the same
   continuation.** `SUM` and `COUNT` both entail `SUM`, so a family whose target is a count and one
   whose target is a total are indistinguishable at this check. The missing fact is in the FAMILY
   declaration: a family declares its `target` as prose and its `continuation` as a citation, and
   never names the law its own values are FORMED by. **A repo obligation, reported, not filled.**
2. **Operand arity has nothing to be checked against**, for the same class of reason: the vocabulary
   carries operand DOMAINS, not signatures.

---

## C. `Σ(E)` and `ecf-1`

`Σ(E) = constructor · governed operand identities · operand roles · constitutive inner anchors ·
participation and scope · identity-bearing parameters` — v8 §7.3's own list, and nothing added.

**One scheme, and it starts where `fcf-2` ended.** `fcf` needed two because it acquired the U-authority
binding and resolved anchors after families were already established under a spelling-based digest.
An expression sort minted today has no such era, so `ecf-1` drops the `universe` spelling (governed
through the binding) and resolves the inner anchors from birth. That is also why the binding is
**required** on an expression and optional on a family: without it the world would be in no payload
and under no authority — a hole, not a transition.

**`ecf-1` is TOTAL over its identity keys, and `fcf`'s one hole is deliberately not reproduced.**
`canonical_family_payload` writes a key only `if key in body`, so for a family an absent optional key
and a key declared empty give two digests — two identities for one analytical fact. Here they digest
the same, and a steward cannot change an expression's identity by adding a key that says nothing.

**Operands sort by role, and the role carries the order.** Reordering the serialization is not a
change; swapping which family fills which role is. That is the trade a bare positional tuple cannot
make, and it is why the role is on the record at all.

### Succession — `expression.succession`

Compares Σ(E) PAYLOADS, not declarations, which is what makes the negative cases true by construction:
admitting or withdrawing a basis, adding an alias, or re-spelling the canonical reference cannot reach
the payload. Verdicts are two — `SAME_EXPRESSION` / `SUCCESSOR_REQUIRED` — with no "possibly the
same", because a verdict a consumer has to interpret will be interpreted differently twice.

Both universes are taken, because the payload RESOLVES inner anchors: a change to the world can change
Σ(E) with no expression byte moving, and that is correct.

**Ruling 6 held.** The rule's escape clause — *unless governed equivalence establishes continuity* —
**never fires**, and the module says so in the verdict rather than filing it and forgetting.

---

## D. Version and reader behaviour

**`NATIVE_PUBLICATION_FORMAT_VERSION` 3.0 → 3.1. `SUPPORTED_NATIVE_VERSIONS` `("3.0",)` → `("3.0",
"3.1")`. `ADMITTED_KINDS` becomes minor-relative.**

```
ADMITTED_KINDS_BY_VERSION = {"3.0": {universe, family},
                             "3.1": {universe, family, expression}}
```

That map is the substantive change, and it makes "additive" mean something in **both** directions:

| situation | behaviour |
|---|---|
| a v3.0 artifact, read by this build | **unchanged.** The shipped harbour fixture is byte-identical, both families' `fcf` digests re-derive, all six currency claims verify |
| a v3.0 artifact carrying an `expression` declaration | **REFUSED**, naming the minor that admits the kind and the remedy (*re-declare as v3.1*). A reader that read it anyway would be deciding that the minor an artifact declared was a formality |
| a declaration kind no minor admits (`anchor`) | refused as before, with the original message — two situations, two remedies |
| a v3.1 artifact, read by an OLDER build | **REFUSED** by `read_version`, through the existing explicit-version contract and no new code: *"compatibility must be KNOWN, not presumed… never because it sorts after this one."* Tested by restoring that build's own `SUPPORTED_NATIVE_VERSIONS`, because that is the whole of what an older build differs by |
| a v3.2 artifact | still refused. Adding a minor is exactly the moment the set could quietly become a floor; both directions are re-pinned |
| publication v2 | **untouched.** Not backported, and structurally cannot be: `_major` discards the minor |

**Ordering held (huayin, 2026-09-28).** Body contract → resolver/validation → Σ(E)/succession → tests →
**then** the two lines above. The sort token is cheap and the constitution is not; admitting a kind
before its body contract, resolver and canonicalization exist would be admitting a name.

---

## E. The migrated MEAN exemplar

`packages/columna-core/tests/fixtures_v3/native-v3_1-publication.json` — a NEW artifact, so the v3.0
fixture stays byte-identical and the "unchanged" claim is measured rather than asserted.

* universe `commerce`, ground `customer_order`, constituents `{store, day}`, denotation
  `sale_at → {store, day}`.
* family `revenue` — primitive, SUM, decimal, at `sale_at`.
* family `order_count` — primitive, SUM, integer, at `sale_at`, same declared participation.
* **expression `average_order_value`** (alias `aov`) — constructor MEAN, operand role `operand` →
  `revenue`, inner anchor `sale_at`, one admitted basis `b_sum_count_store_day` filling
  `SUM → revenue` and `COUNT → order_count` with `requires_common_participation: true`.

It resolves **VALID: yes, EVALUABLE: yes** across all seven responsibilities, and its `ecf-1`
authority re-derives.

**Ruling 5 held, at both layers.** A `kind: family` declaration whose formation cites MEAN still
parses in a v3.1 artifact (parsing compatibility), still reaches C7 by `ENTAILED_FROM_FORMATION`,
and is still refused family standing by V8-0's clause 2 — **the existence of the sort did not rescue
it.** It is not reachable as an expression by any door, and asking for it as one names the remedy
(explicit re-authoring by someone with authority) rather than supplying it.

---

## F. What was deliberately NOT done

* **No request serving and no peer Frame-QL target** (ruling 8). `NativePublication.sort_of` exists so
  a future target has a lawful object to point at; **nothing routes on it**, `request.py` is
  unchanged, and a test pins that — including that `request.resolve`'s arm still NAMES the gap in
  prose rather than filling it.
* **No `composite.py` generalization.** The `(SUM, COUNT)` hard-code, `CompositeState.family_id` and
  `declared_basis` are untouched. Proof C now has a lawful object to point at; wiring it is V8-2/3.
* **No Operator Registry reconciliation** (ruling 7). The stranded semantic facts — `re_entrant`,
  `is_monoid`, `linear`, `combine`, the `accepts`/`out_rule` signature overlap — are carried forward
  itemized in the design stop-gate's §6, and `re_entrant`'s inadequacy as a global Boolean goes to the
  family-edge / Frame-QL identity work.
* **No C5 split** (ruling 9). E4 is one responsibility and says why.
* **No applicability model, no `NA`.** V8-0 freed the spelling; nothing takes it here.
* **No publication v2 backport** (ruling 2).

---

## G. Theory errata candidate — `governed equivalence`

**Recorded as an errata candidate, not an implementation blocker** (ruling 6).

`governed equivalence` is the escape clause on both of v8's succession rules — §7.3 (twice) and §7.6 —
and v8 never defines it. ToD v7.1 §6.6 did: the equivalence must be a **congruence with respect to
`⊕`** and must **preserve constructor outputs**. That requirement, or its deliberate replacement, is
the missing definition.

It is load-bearing in two places this unit reached, and in both it is reported rather than answered:

1. **Succession.** An identity-bearing change mints a successor. The second clause of §7.3's rule
   never fires, because there is no already-governed explicit equivalence mechanism in this build.
2. **E6 basis agreement.** Two alternative routes filling one role with two DIFFERENT families agree
   on component laws and participation — and whether those two families are interchangeable in that
   role is exactly the undefined question. The resolver establishes the agreement it can check and
   reports the residue verbatim.

Carried in code as `expression.GOVERNED_EQUIVALENCE_ERRATA`, quoted into both sites' notes, so the gap
travels with the verdict rather than sitting in a document.

---

## H. A second finding, outside this unit's scope

**ToD v8.0 is absent from `registry/publications/`.** A grep of `registry/` for its record id returns
nothing, and `records.json` still carries v7.1 as the latest Theory of Data. `check_publications.py`
G7 therefore fails closed twice over on any tracked file typing the identifier — once for the missing
`consumers.json` row, and again on the row itself, because no registered record carries that DOI. **No
row can be written that the gate would accept.**

Registering it needs live Zenodo verification and a dated snapshot, which is a governance act with its
own unit. Until then the governing theory of this entire migration is cited by version and section —
which is what every argument in this line actually rests on — and the identifier stays registry
business. **Reported, not routed around.**

---

## I. Recommendation — the smallest V8-2 peer-target unit

**One seam, one early return, one defect fixed. Nothing downstream.**

`request.resolve` (`request.py:97-98`) already has the arm: `family = pub.resolve_reference(token)` and
`if family is None:`. The design stop-gate §D measured that 22 of the 23 intrinsically family-only
sites are downstream of it and never reached, and that the family success path changes by zero bytes.

The unit is:

1. **Dispatch on `sort_of(token)` at that arm** — `"family"` → the existing path, unchanged;
   `"expression"` → a peer resolved-request type; `None` → the existing refusal.
2. **A peer type, not a widened `AnalyticalIdentity`.**
   `test_analytical_identity_still_carries_exactly_two_fields` guards storage and constitution leaking
   into identity, not sort; a peer does not violate it and widening the dataclass would. `state.py`
   keys retrieval on `==` alone, so the store needs nothing.
3. **Fix the defect at the same seam.** That arm raises `WantOfLaw` — *"no governed family answers to
   the reference"* — where a durable expression name is a **capability limit**. Today it sends a
   steward to correct a publication that is correct. (This is the same class of defect V8-0 found at
   C7 and this unit found at `NativePublication.family`, which now names the sort.)

**Explicitly not in V8-2:** evaluating the expression, generalizing `composite.py`'s `(SUM, COUNT)`
hard-code, `Op(F@A)@B` rewriting (§8.6), and the Operator Registry. V8-2 should end with an expression
reference reaching a peer target that refuses with a *correct* refusal — the smallest thing that makes
the sort visible to a request without making it evaluable. V8-3 takes Proof C's arithmetic onto it.

---

## Test totals

`ruff --select F,E9` clean over both packages' src and tests.

| suite | before V8-1 | after |
|---|---|---|
| platform | 361 passed | **368 passed** (+7, `test_v8_1_expression_sort_does_not_reclassify.py`) |
| core | 1887 passed / 50 skipped | **1959 passed / 50 skipped** (+71 `test_v8_1_governed_expression.py`, +1 the re-pin in `test_native_v3_reader.py`) |

**Exactly one pre-existing test changed meaning, and it is the one that encoded the pre-v3.1 state:**
`test_two_version_mechanisms_two_refusals[3.1-does not explicitly understand]` was the worked example
of an unrecognised MINOR. It is **reclassified, not deleted** — the case moves to `"3.2"`, and a new
test re-pins the property in both directions (`"3.2"` sorts above the understood `"3.1"` and is still
refused; `"3.0"` sorts below the version this build writes and is still read).
