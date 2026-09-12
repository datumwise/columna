# Sufficient State Engine — minimal contract — **v0.1 CANDIDATE**

**Status:** candidate, prepared 2026-09-12 for review. One page by intent: the smallest contract
that can survive Proofs A, B and C without being rewritten by them.
**Excluded by instruction:** DuckDB, ADBC, adaptive materialization, cross-Manifold sharing,
distributed execution, approximation policy beyond what a landed proof requires.

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

*The public name and exact tuple shape of the standing object are deliberately NOT frozen here.* What
is frozen is that the two questions have two answers and that the six facts above remain reachable.

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

## 4. Invalidation is governed outside the SSE — and mostly comes out free

The SSE may perform invalidation. It may not invent the rule. Keying retained state on
`(family_id, constitution_fingerprint)` makes ToD v7.1 §3.9 **structural rather than policy**:

- an **identity-bearing** change mints a new `family_id`, so prior state is simply *unreachable* —
  no invalidation logic runs;
- a **non-identity** change (a movement established, an alias added) leaves the fingerprint
  unchanged, so valid state **survives** — also with no logic.

That is the §7.1 requirement discharged by construction rather than by a policy that could be got
wrong.

**Adopt the conservative-invalidation polarity both existing mechanisms already share.**
`manifold_agent.family.constitution_status` returns STALE when the *fingerprint scheme version*
changes — an incomparable token reads as stale, not as equal. `Connector.data_identity` namespaces
its token by algorithm and engine version for the same reason, and returns `None` — closing reuse —
when it cannot honestly warrant one. Two repos already agree; the SSE should make it three.

## 5. Currency, and the precedent to copy

Core's existing mechanism is the right shape and should be reused rather than reinvented: an opaque
comparable token per realized table, probed **once per request**, compared **per capability** so a
refresh closes only what its own evidence rested on, and failing **closed** on an unavailable token.
Two currency axes must stay distinct in the SSE:

- **data currency** — has the material state moved?
- **realization currency** — is the realization *assertion* still true? (Open jurisdiction; must not
  be absorbed by admission, which checks the carrier, not the claim.)

## 6. Out of scope for v0.1

Composite sufficient-state *declaration* (the governed model has no state-carrier slot — Proof C
precondition, not SSE work), governed movement enablement (Proof B), approximation composition under
continuation (open until the governing text is re-checked; treat unsupported approximation
continuation as a refusal), eviction policy, and every excluded item named at the head of this
document.
