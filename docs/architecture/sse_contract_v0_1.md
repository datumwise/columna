# Sufficient State Engine — minimal contract — **v0.1 CANDIDATE**

**Status:** candidate, prepared 2026-09-12 for review. One page by intent: the smallest contract
that can survive Proofs A, B and C without being rewritten by them.
**Excluded by instruction:** DuckDB, ADBC, adaptive materialization, cross-Manifold sharing,
distributed execution, approximation policy beyond what a landed proof requires.

---

## 0. Where the SSE sits in the chain of authority

**Architectural ruling (Huayin, 2026-09-12):**

> An entailed fact does not need to be repeated as constitutive authority. It may be re-derived
> wherever the consumer is itself authorized and equipped to perform that derivation. If a
> downstream component does not own that derivation, the fact must cross the boundary as an
> explicitly derived runtime projection rather than be reinvented there.

The chain this puts the SSE at the end of:

```
constitution  →  entailed law  →  runtime projection  →  material state
  (governed)      (derived by         (derived           (the SSE
   authority)       the layer          EXECUTION          executes it)
                    owning the law)     INPUT)
```

Three consequences that shape everything below.

**The SSE executes sufficient-state law; it does not rediscover why a state is sufficient.** C7's
sufficient-state requirement is entailed by the governed foundation — `foundation.py` carries a
`sufficient_state` per law and `resolve.py` derives C7 from the continuation. The SSE does not own
that derivation and must not re-perform it: it would need the foundation vocabulary, the law
citations, and the version discipline that go with them, and a runtime that can re-derive law can
also re-derive it *differently*. So the owning layer derives a **runtime state specification** and
carries it across. That projection is derived execution input — **not** new constitutive authority,
and **not** realization.

**Absence of an entailed fact from a serialized artifact is not law loss.** The question is never
"was it written down?" but "does the receiving component hold the authoritative premises and the
lawful derivation?" Where it does, re-derivation is lawful. Where it does not, the projection must
be carried. This is the same reasoning that keeps entailed consequences out of the constitution
fingerprint: a fact already determined by what is declared cannot distinguish two families that
declare the same thing.

**`empty_fiber` is settled by this rule and stays settled.** It is an entailment of continuation
algebra — not Φ, and not a family declaration. Core's `FILL` answers a different question about a
different object (*what does an eligible point with no observed value denote* — a declaration, "a
choice… never a consequence"), and the withdrawn `empty_fiber → FILL` mapping stays withdrawn.

---

## 1. Two questions, kept apart

The contract's whole shape follows from refusing to answer these with one key:

| Question | Answered by |
|---|---|
| *What is this state **of**?* | **analytical identity** — `F @ A` |
| *May these two states be **reused or combined**?* | **retained-state standing** |

> **Matching `F @ A` is necessary for reuse. It is not sufficient.**

Numerically identical co-moment states produced under pairwise versus listwise participation are not
interchangeable. Neither are two states of one family whose governing constitution differs, or whose
realization standing differs, or one of which is stale.

`AnalyticalIdentity` is `(family_id, anchor)` and must not be widened to encode storage details.
Retained-state standing must keep available, **where relevant**:

- governing constitution / state law standing (constitution fingerprint);
- participation regime;
- eligibility / support standing;
- sufficient-state basis / representation;
- realization standing;
- currency / validity.

*The public name and the exact tuple shape of the standing object are deliberately NOT frozen here*
(ruling, Huayin, 2026-09-12). In particular **`CompatibilityClass` is not adopted as a term** by this
document — it has been used in discussion, and using it here would establish it. No term is being
established, and the list above is a set of facts that must remain **reachable where relevant**, not
a record layout. A later document may name the object; this one deliberately does not, because
naming it would also fix its arity, and the arity is what is still being learned. What is frozen is only this: the two questions
have two answers, and the second one is not `F @ A`.

## 2. What retained state must be able to answer, after retrieval

Standing travels **with** state; it is never reconstructed from a bare value buffer. At minimum, a
retrieved state answers: what governed identity, at what anchor, under which publication and
constitution standing, through which realization standing, whether it is still current, what
support/eligibility standing accompanies it, and what lawful continuation its representation still
supports.

Precedent, and the reason to state it as a rule: Core's own `CacheEntry` stores the disclosure
alongside the frame because *"STORING THE DISCLOSURE IS THE POINT, not an optimisation."* The SSE is
the same lesson one layer down.

## 3. Operations

| Operation | Precondition | Refusal / note |
|---|---|---|
| `insert` / `replace` | realization standing present; currency token resolved | a `None` currency token permits insert and **closes reuse** — never manufacture freshness |
| `retrieve` | identity match | may return several states of one identity in different standings; **may never merge them** |
| `combine` | equal identity **and** compatible standing; the basis is mergeable under the family's law | want-of-law if the law does not license it; want-of-compatibility if standing differs |
| `continue` | a **positive** movement licence naming source → target anchor | want-of-law. Never "the arrays can be combined, so proceed" |
| `finalize` | — | the result is marked **not sufficient state**; offering a finalized value back as state is refused |
| `invalidate` | the SSE performs it; **it never decides it** | the rule is governed outside the SSE (§4) |
| `refuse` | — | must name **want-of-law** or **want-of-state**; a want-of-state refusal must carry that re-realization would resolve it |
| `evict` | policy only | may never convert a want-of-state into a want-of-law |

The `refuse` row is load-bearing. A refusal that cannot distinguish *this is not establishable* from
*we evicted it* destroys the evidentiary value of refusal, which is the product's core asset.

## 4. Invalidation is governed outside the SSE

The SSE may perform invalidation. It may not invent the rule.

**The invariant, stated semantically — this is the part that is frozen:**

> Retained state must be bound to the governing constitution / state-law standing under which it was
> formed, with **explicit comparability** and **conservative invalidation when the comparison scheme
> itself changes**.

"Explicit comparability" means the binding must be *comparable at all* — two states either agree on
the governing standing, disagree, or are **incomparable**, and incomparable must not read as agree.
"Conservative invalidation" means a change to the comparison scheme invalidates rather than being
assumed benign.

**A constitution fingerprint is a strong implementation candidate** for that binding and may be used
in Proof A. It is not the invariant, and this contract does not elevate it to one: a different
representation that satisfies comparability and conservatism would satisfy the contract.

*If* a fingerprint is the chosen representation, one consequence is worth noting because it is
unusually cheap: keying on `(family_id, <constitution standing>)` discharges ToD v7.1 §3.9 by
construction rather than by policy — an identity-bearing change mints a new `family_id`, so prior
state is simply *unreachable* and no invalidation logic runs; a non-identity change (a movement
established, an alias added) leaves the standing unchanged, so valid state survives, also with no
logic. That is a property of that representation, not a requirement of this contract.

**Adopt the conservative-invalidation polarity both existing mechanisms already share.**
`manifold_agent.family.constitution_status` returns STALE when the *fingerprint scheme version*
changes — an incomparable token reads as stale, not as equal. `Connector.data_identity` namespaces
its token by algorithm and engine version for the same reason, and returns `None` — closing reuse —
when it cannot honestly warrant one. Two repos already agree; the SSE should make it three.

### 4.1 The structural insight — six axes, four mechanisms, not one

The axes on which retained state can cease to be reusable do **not** share a mechanism. Collapsing
them into a single "invalidate" is the error this section exists to prevent: it would convert
want-of-law refusals into want-of-state refusals, which §3's `evict` row already forbids in the
other direction and for the same reason.

| Axis | What a change to it means | Mechanism | Refusal, if any |
|---|---|---|---|
| **`family_id`** | an identity-bearing change — target, formation, participation, declared continuation, value domain (`_FAMILY_KEYS`; ToD v7.1 §3.9) — mints a **new** identity | **unreachable by construction** | none: no logic runs, prior state is simply never retrieved |
| **constitution / state-law standing** | the governing text or the comparison scheme changed *without* minting a new identity | **explicit, conservative invalidation** | want-of-state; an *incomparable* standing must read as stale, never as agreement |
| **participation / support / eligibility regime** | two states of the **same** identity formed under different regimes — the pairwise-vs-listwise co-moment case | **blocks combination; does NOT invalidate** | want-of-compatibility on `combine`. Both states stay valid and individually reusable |
| **sufficient-state basis / representation** | the runtime state specification changed, or the retained basis does not support the continuation now asked of it | **closes reuse for that continuation; retains for retrieval** | **want-of-law** — the state is still what it is; the law does not license this use of it |
| **realization standing** | the realization claim, or its faithfulness, changed | **invalidate** | **want-of-state**, and it MUST carry that re-realization would resolve it |
| **currency** (data and realization, kept distinct) | the token moved, or cannot be honestly warranted | **fail closed** | a `None` token permits insert and closes reuse; never manufacture freshness |

Four distinct mechanisms — *unreachable*, *invalidate*, *block combination*, *close reuse for a
continuation* — and the difference between them is the difference between refusals that carry
different remedies. Re-realization fixes row 5. It does nothing for row 4, where the remedy is a
licence, and nothing for row 3, where there is no defect to fix at all: two valid states that may
not be added together.

The first row is worth stating plainly because it is the cheapest guarantee in the design and is
easy to mistake for an absence of one: **identity-bearing change needs no invalidation logic,
because the old key is never asked for again.** Rows 2–6 are the cases where something must
actually be decided — which is exactly why the rule is governed outside the SSE.

## 5. Currency, and the precedent to copy

Core's existing mechanism is the right shape and should be reused rather than reinvented: an opaque
comparable token per realized table, probed **once per request**, compared **per capability** so a
refresh closes only what its own evidence rested on, and failing **closed** on an unavailable token.
Two currency axes must stay distinct in the SSE:

- **data currency** — has the material state moved?
- **realization currency** — is the realization *assertion* still true? (Open jurisdiction; must not
  be absorbed by admission, which checks the carrier, not the claim.)

## 6. Out of scope for v0.1

Composite sufficient-state *declaration* (the governed model has no state-carrier slot — a Proof C
precondition, and by §0 it is the governed layer's projection to derive, not the SSE's to invent),
governed movement enablement (Proof B), approximation composition under continuation (open until the
governing text is located; **treat unsupported approximation continuation as a refusal** and do not
infer composition standing from the implementation), eviction policy, the shape of the runtime state
specification itself, and every excluded item named at the head of this document.
