# Minimal SSE Contract — Proof A/B/C boundary — **PARTIALLY RATIFIED**

**Status:** **§§1, 2, 4, 4.1 and 5 RATIFIED (Huayin, 2026-09-14)**, with the corrections and the one
substantive addition recorded in this revision. §3 is revised to state implementation status and is
**not** ratified as a description of what Platform does today. §6's exclusions stand. The rest of
the document remains candidate.
**Prepared** 2026-09-12 for review; revised 2026-09-12 on instruction; **revised and partially
ratified 2026-09-14** after Proof A, Proof C and the first real material ingress (DuckDB via ADBC)
had exercised it.

**WHAT RATIFICATION MEANS HERE, AND WHAT IT DOES NOT.** The ratified sections are held to have
survived contact: the two-questions split, the compatibility invariant and the six-axis structure
were used to adjudicate a real defect (OF-39) and did not need rewriting to do it — the standing
object's *arity changed under a ruling with no amendment to this contract*, which is the strongest
available evidence that §1 was right to leave the arity unfixed. Ratification does **not** freeze the
standing object's name or arity, does not authorize persistence, and does not convert any §3 row
into a claim about shipped behaviour.
**Scope discipline, not a page count** (clarification, Huayin, 2026-09-12). The governing constraint
is the *smallest contract that can survive Proofs A, B and C without being rewritten by them* — an
admission test for what belongs here, not a length budget. An earlier draft said "one page by
intent", which invited trimming load-bearing material to satisfy a metaphor; the rule is stated as
scope from here on. Nothing is removed to make this shorter.
**Filename retained** as `sse_contract_v0_1.md` so existing citations resolve; the title is the
change.
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

- governing constitution / state-law standing — **both the comparison SCHEME and the ACTUAL
  constitution fingerprint** (ratified 2026-09-14; see §4);
- **participation / eligibility / support regime — ONE axis, not two.** An earlier revision listed
  participation and eligibility-support as separate bullets while §4.1's table carried them as one
  row. §4.1 was right and this list was the anomaly: **the governed model fuses them.** C5 is
  literally named `eligibility_and_participation` (`governed/resolve.py`), so a runtime standing
  that split them would be modelling a distinction the governed layer does not make, and would
  invite two compatibility comparisons where the law supplies one fact. Corrected 2026-09-14;
- sufficient-state basis / representation;
- realization standing;
- currency / validity.

**Additive beyond this list: MOVEMENT STANDING (Proof B).** A state that arrived by a licensed
movement must be able to say so, or the standing it carries forward is a claim about a path nobody
recorded. It is recorded here so its presence in a runtime standing object does not read as
accidental drift — but it is **deliberately not folded into the six-axis table of §4.1**, because it
does not play that table's role: the six axes are the ways retained state ceases to be reusable, and
a movement licence is not a way state goes bad. It is provenance of how the state came to stand
where it does. Whether a *change* to movement standing ever blocks combination is an open question
for Proof B, and until Proof B answers it, movement is carried and not compared.

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

**READ THE STATUS COLUMN BEFORE THE SEMANTICS COLUMN (added 2026-09-14).** This table states what
each operation MEANS. It has been read as a description of what Platform does, which it is not and
never was — so status is now carried per row. **A contract operation appearing in this table does
not imply Platform implements it today.**

| status | meaning |
|---|---|
| **LIVE** | specified here AND called on the successor serving path today |
| **BUILT, UNCALLED** | implemented in `columna-platform` with no caller in any `src/` module — exercised only by direct tests |
| **NOT IMPLEMENTED** | specified here, absent from the code |
| **NOT A STORE OPERATION** | specified here as a semantic requirement, realized by a different mechanism |

| Operation | Status (2026-09-14) | Where |
|---|---|---|
| `insert` | **BUILT, UNCALLED** on the reuse path — called during materialization, never to offer state for a later request | `state.py` |
| `retrieve` | **LIVE** — `decide_result` calls it on every serve | `state.py`, `serving.py` |
| `establish` (re-materialization on a miss) | **LIVE** — the ruled "a retrieval miss is not a refusal" path | `state.py`, `serving.py` |
| `combine` | **BUILT, UNCALLED** — no `src/` caller; a control asserts it acquires none | `state.py` |
| `continue` | **BUILT, UNCALLED** (Proof B/C) | `composite.py`, `continuation.py` |
| `finalize` | **BUILT, UNCALLED** on the serving path | `state.py` |
| `invalidate` | **NOT IMPLEMENTED** | absent |
| `replace` | **NOT IMPLEMENTED** | absent |
| `refuse` | **NOT A STORE OPERATION** — realized by the refusal classes and their wire classification | `refusals.py`, `serving.py` |
| `evict` | **BUILT, UNCALLED**; no eviction POLICY exists (§6) | `state.py` |

**`invalidate`'s absence is benign only because nothing survives a request to be invalidated.** It
becomes mandatory with the first retention mechanism, and it is the operation whose rule §4 says is
governed OUTSIDE the SSE — so its absence today is not merely unbuilt code, it is an unanswered
governed question with no placeholder. Recorded here rather than left to be discovered by the unit
that needs it.

### 3.1 Semantics

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

**THE PARTICIPATION RULE — NORMATIVE, ADDED 2026-09-14 (Huayin).**

> **Every governed axis whose change blocks combination must PARTICIPATE IN THE COMPATIBILITY
> COMPARISON. Merely storing that fact, or making it reachable from the state, is insufficient.**

This is the rule OF-39 demonstrated was missing, and the demonstration is why it is normative rather
than advisory. The earlier wording required the standing facts to be *"reachable where relevant"* —
and every fact **was** reachable. `Standing` carried the constitution fingerprint the whole time.
The comparison simply did not use it: `comparable_to` returned the fingerprint SCHEME and not the
fingerprint, so two states formed under different governed constitutions compared as **compatible**
and could be folded together. Nothing was missing, nothing was unreachable, and the invariant as
then stated was satisfied by an implementation that was wrong.

So reachability is not the requirement; **participation in the comparison is**. An axis that is
stored and not compared is a defect of *this invariant*, not an implementation detail beneath it —
and it is a defect of a particularly quiet kind, because the stored value makes the state look
correctly described while the comparison silently ignores it. OF-39 survived precisely that way: the
wrong value was inert, and inertness reads as absence of a problem.

**Corollary, for reviewers of any future standing object:** it is not enough to check that the
object carries the six axes. Check which of them the comparison consumes, and require a stated
reason for every axis carried but not compared. (Two such reasons exist today and both are sound:
**currency** is not in the comparison because its mechanism is *fail closed* rather than *block
combination* — it is checked by a separate gate raising a different class — and **movement** is not
compared because Proof B has not yet established that a change to it blocks anything. Each is a
decision on the record, which is the standard this corollary sets.)

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
governed movement enablement (Proof B), eviction policy, the shape of the runtime state
specification itself, and every excluded item named at the head of this document.

**Approximation composition under continuation is OPEN and stays open** (standing instruction,
Huayin, 2026-09-12). Until the governing text has been re-checked:

- **treat unsupported approximation continuation as a REFUSAL**, and
- **do not infer composition standing from the implementation.**

Named explicitly, because it is the nearest thing to a temptation: `FoundationLaw.approximation`
exists in `governed/foundation.py` and defaults to `"exact"`. **That field is not the governing
text.** It is one layer's representation of a decision taken elsewhere, and a default is the weakest
possible evidence of a rule — it is what was needed to construct an object, not what was ruled. No
conclusion about approximation-continuation semantics may be drawn from it, from its default, or
from the set of values it currently takes. This document draws none, and a later document that does
should first cite the governing text, not the attribute.

---

## 7. The 2026-09-14 ratification record

### 7.1 What is ratified, and what exercised it

| § | ratified | what tested it |
|---|---|---|
| **1** | identity vs compatibility, kept apart — `F @ A` answers *what of*, standing answers *may these combine* | OF-39: the constitution fingerprint joined the comparison **without** joining identity. The two questions stayed two |
| **2** | standing travels WITH state; a retrieved state answers for itself | Proof A's `RetainedState` carries its `Standing`; the wire never reconstructs it from a value buffer |
| **4** | explicit comparability + conservative invalidation, **plus the participation rule added above** | OF-39 is the demonstration, and the reason the addition is normative |
| **4.1** | six axes, four mechanisms | corroborated in code: `comparable_to` carries exactly the *block-combination* axes; currency is checked by a **separate gate raising a different class**, which is row 6 (*fail closed*) correctly kept apart from row 3 (*blocks combination*) |
| **5** | data currency and realization currency stay distinct | both remain unfilled, and the distinction is now load-bearing rather than theoretical: realization currency is one of three open jurisdictions in a RATIFIED freeze, while data currency has a precedent (`Connector.data_identity`) and no implementation |

**The strongest evidence for §1 is negative and worth stating.** Between 2026-09-12 and 2026-09-14
the standing object's arity changed — a four-tuple comparison became a five-tuple — under a ruling,
**with no amendment to this contract**. That is exactly what §1 predicted by declining to fix the
arity, and it is why the decision not to name the object is ratified along with the rest.

### 7.2 What remains deliberately unfrozen

Unchanged by this ratification, and not to be inferred as settled by it:

- **`CompatibilityClass`** as a public, name-bearing object — still not adopted. Naming it would fix
  its arity, and the arity is still being learned;
- **the exact name and arity of the runtime `Standing`** — it has already changed once;
- **persistence backend**, **eviction policy**, **durable state representation** — all out of scope,
  and §6's exclusions stand in full;
- **approximation composition under continuation** — OPEN, per the standing instruction; treat
  unsupported approximation continuation as a refusal and infer nothing from the implementation;
- **the composite side's standing model** — what governed standing must travel with a constituted
  composite basis so that common-pass provenance and cross-basis compatibility stay distinct
  without duplicating or collapsing the model. Rowed as **OF-56**; `pass_id` stays
  observation-local and cross-request equality must never depend on it.

### 7.3 Before state may lawfully survive request N → request N+1

Four things, and **permanent persistence is deliberately NOT among them**. The sequencing rule is
**prove lawful reuse first; make it durable afterward** (Huayin, 2026-09-14).

1. **Warranted data-state identity.** A source must be able to return an opaque comparable token
   under a ruled contract. `None` continues to close reuse, and freshness is never manufactured.
   Both adapters return `None` today, so reuse is closed by construction rather than by omission.
2. **Realization currency.** A separate open jurisdiction, and **data-state equality cannot
   substitute for it**: equal tokens mean *comparable*, not *current*, and the realization question
   is about whether the CLAIM is still true, which admission does not check.
3. **A sound reuse key.** P5-05 reconciled against the now-ratified compatibility rule. Identity and
   every compatibility axis relevant to reuse must be represented correctly — and the realized
   support set must **not** be included where the contract assigns it to attestation rather than to
   identity or keying.
4. **A cross-request retention mechanism**, sufficient for a controlled proof that state established
   by request N can be OFFERED to request N+1. For the first proof this may be an in-memory,
   provider-held store with an explicitly bounded lifetime. Permanent persistence, eviction, process
   restart and durable invalidation remain later work.

**A design note that #316 has already settled, recorded here so a key design does not reopen it:**
a mismatched constitution must be **retrieved and refused as incompatibility**, never hidden by key
construction. Retrieval stays keyed by analytical identity; compatibility is adjudicated explicitly
afterwards. Folding compatibility facts into the lookup key would convert a governed refusal that
names its reason into a silent cache miss that names nothing — and the evidentiary value of refusal
is, per §3, the product's core asset.
