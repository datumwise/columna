# Frame-QL vNext — R4 Standing Architecture Amendment

**Working Draft 0.2 — 6 September 2026**  
**Status:** Semantic-architecture amendment  
**Purpose:** Refine R4 of *Frame-QL vNext — Semantic Expression Architecture* after the missing-anchor / missing-value / lost-record discussion.  
**Supersedes for R4:** §§6.1–6.8 of the 4 September 2026 semantic-expression architecture working draft.  
**Not a syntax release. Not an implementation authorization.**

---

# 0. Why R4 needs one more layer

The earlier R4 correctly separated:

```text
point existence
measure eligibility
measure support
value
```

and correctly distinguished:

```text
event known not to have occurred
    → point does not exist

event known to have occurred, record lost
    → point exists
    → affected measure values may be unsupported

no record and no governed evidence either way
    → point existence unsupported
```

That model is still correct.

The lost-record discussion exposes one additional standing distinction between **point existence** and **measure standing**:

> A point can be known to exist while the governed system cannot establish where that point belongs under a particular anchor.

Example:

```text
transaction T123 is independently known to have occurred
transaction_date was carried only by the lost record
```

The transaction exists.

But its placement under the `day` anchor may be unsupported.

This is not:

- lawful nonexistence;
- unsupported point existence;
- measure ineligibility;
- an unsupported Revenue value.

It is an upstream failure to establish the point's governed analytical placement.

The working term in this amendment is **anchor-placement standing**.

The term is intentionally provisional. The distinction is semantic; the final public name need not be frozen yet.

---

# 1. No new ToD ontological primitive is required

Let \(U\) be a universe with governed root-point domain:

\[
\Omega_U.
\]

Let \(A\) be a governed anchor, hence a partition of \(\Omega_U\).

For every existing root point \(\omega\in\Omega_U\), partition law determines exactly one block \(a\in A\) such that:

\[
\omega\in a.
\]

Equivalently, the anchor induces a unique projection:

\[
\pi_A:\Omega_U\rightarrow A.
\]

The new issue is **not** whether this projection exists mathematically.

It is whether the governed evidence is sufficient to establish:

\[
\pi_A(\omega)=a.
\]

Therefore anchor-placement standing is best understood as **standing over an already governed projection**, not as a new analytical object beside universe, anchor, measure family, or measure.

This keeps the ToD ontology small.

---

# 2. Revised standing dependency

The semantic dependency is now:

```text
universe existence law
        ↓
point-existence standing
        ↓
anchor-placement standing
        ↓
measure eligibility standing
        ↓
measure support standing
        ↓
semantic value
```

More formally, for a root point \(\omega\), anchor \(A\), family \(F\), and candidate anchor point \(a\):

\[
\lambda_U
\rightarrow
Exist_U(\omega)
\rightarrow
Place_A(\omega)=a
\rightarrow
Eligible_{F,A}(a)
\rightarrow
Supported_{F,A}(a)
\rightarrow
m_{F,A}(a).
\]

The arrows express dependency of establishment, not an execution pipeline.

---


# 2.1 Four different things people may call a "missing anchor"

The phrase **missing anchor** is too ambiguous for canonical use.

At least four different failures can sit behind it.

## A. Required input anchor omitted from the request

Example:

```text
mean(revenue)
```

where `order` versus `customer` would change the family identity.

This is a **request determinacy / identity-completion problem**.

The relevant anchor exists in the governed model; the request failed to state or uniquely determine which one is intended.

This can lead to **Clarify**.

It is not missing data.

## B. The referenced anchor is not governed

Example:

```text
E @ {A}
```

where `{A}` does not resolve to a valid governed anchor in the selected universe.

This is an **anchor-standing / geometry problem**.

There is no valid analytical location under which to interpret the request.

It is not point-existence uncertainty and not measure missingness.

## C. Point existence is unsupported

The system cannot establish whether a candidate point belongs to the universe at all.

This is **unsupported point existence**.

## D. The point exists, but placement under a governed anchor is unsupported

The system knows:

\[
\omega\in\Omega_U
\]

and knows that \(A\) is a valid anchor, but cannot establish:

\[
\pi_A(\omega)=a.
\]

This is **unsupported anchor placement**.

These four cases have different causes, repair paths, and downstream effects.

Canonical diagnostics should preserve the distinctions even if a user colloquially describes all four as "missing an anchor."

---

# 3. Point-existence standing

For a candidate event/root point \(\omega\), governance may establish:

## 3.1 Existent

\[
\omega\in\Omega_U.
\]

The event/root point exists under the universe existence law.

## 3.2 Nonexistent

\[
\omega\notin\Omega_U.
\]

The event/root point is governed as not having existed.

## 3.3 Unsupported point existence

The available governed evidence is insufficient to establish either judgment.

This must remain distinct from nonexistence.

In an event universe:

```text
no event occurred
    → nonexistent point

event occurrence established
    → existent point

no record and no other governed evidence
    → unsupported point existence
```

A surviving dataset must not silently redefine the event universe merely by omitting events whose existence evidence has been lost.

---

# 4. Anchor-placement standing

Assume point existence has been established:

\[
\omega\in\Omega_U.
\]

For governed anchor \(A\), partition law guarantees one true placement:

\[
\pi_A(\omega)\in A.
\]

Governance may nevertheless lack sufficient evidence to identify which anchor point it is.

We therefore distinguish:

## 4.1 Placement established

\[
Place_A(\omega)=a.
\]

The system can establish the unique \(A\)-point containing \(\omega\).

## 4.2 Placement unsupported

The point exists and \(A\) is a governed anchor, but the available evidence does not establish:

\[
\pi_A(\omega)=a
\]

for a unique \(a\in A\).

This is **not** point nonexistence.

The point exists.

This is **not** an invalid anchor.

The partition law remains governed.

This is **not** a missing measure value.

No measure value need be missing at all.

It is insufficient evidence for the point's placement under this anchor.

---


# 4.3 Root-point standing versus anchor-point standing

The formal account above is intentionally root-point centric.

A root point \(\omega\) has existence standing under the universe law. A governed anchor \(A\) then partitions the established root-point domain.

An **anchor point** \(a\in A\) is a nonempty block of that partition.

Therefore anchor-point existence is not an independent primitive beside root-point existence and anchor geometry.

Its standing is derived from:

```text
root-point existence
+
governed anchor geometry
+
supported placement
```

This matters in occurrence-based universes.

A coordinate-shaped candidate such as:

```text
store = S, day = D
```

does not automatically denote an anchor point merely because those coordinate values can be written.

If no governed root point belongs to that block, the block is absent from the partition.

If relevant root-point existence or placement is unsupported, the system may likewise be unable to establish whether that candidate block is populated.

Frame-QL should therefore avoid treating a coordinate tuple as proof that an analytical point exists.

---

# 5. Placement standing can differ by anchor

Placement support is anchor-relative.

A known transaction may have:

```text
customer placement     established
day placement          unsupported
store placement        established
campaign placement     unsupported
```

Therefore there is no single global state called:

```text
the point has a missing anchor
```

The correct question is:

> **Can the point's placement under this governed anchor be established?**

This is one reason to avoid the phrase **missing anchor**.

It hides the anchor-relative nature of the problem.

---

# 6. Placement failure propagates by dependency, not universally

Unsupported point existence is very broad because the system does not know whether the point belongs to the universe at all.

Unsupported placement under \(A\) is narrower.

It blocks only analytical claims whose establishment depends on that placement.

Conceptually:

\[
\neg SupportPlace_A(\omega)
\Rightarrow
\text{claims requiring }\pi_A(\omega)\text{ cannot be fully established}.
\]

It does **not** imply that every analytical claim involving \(\omega\) is unavailable.

Example:

```text
transaction existence      established
revenue value              supported
day placement              unsupported
```

Then total Revenue over all transactions may still be exactly establishable if the total does not require day placement.

But:

```text
Revenue @ day
```

cannot be fully established because the system cannot determine which day receives that transaction's contribution.

Likewise:

```text
count(all transactions)
```

may remain exact because existence is established, while:

```text
count(transactions) @ day
```

is not fully establishable if the transaction cannot be placed into a day.

This is a central consequence of the amendment:

> **Placement support is a dependency of some anchored claims, not a universal proxy for missingness.**

---

# 7. Lost-record cases

The phrase **lost record** itself carries information.

If it is accepted as true that a record was lost, the loss is evidence that a record—and therefore the event represented by that record—previously existed.

The correct standing depends on what information survived outside the lost record.

## 7.1 Lost value only

```text
event occurrence          established
day coordinate            established elsewhere
customer coordinate       established elsewhere
Revenue value             lost
```

Then:

```text
point existence           established
day placement             established
customer placement        established
Revenue eligibility       governed
Revenue support           unavailable
```

This is ordinary missing/unsupported measure standing.

## 7.2 Lost coordinates and values

```text
event occurrence          established independently
record carrying day,
customer and Revenue      lost
```

Then:

```text
point existence           established
day placement             unsupported
customer placement        unsupported
Revenue support           may also be unsupported
```

The placement failures and value failure are distinct.

They should not be flattened into one generic "missing record" state.

## 7.3 Value survives, placement does not

```text
event occurrence          established
Revenue amount            preserved in payment system
transaction date          lost
```

Then:

```text
point existence           established
Revenue value             supported at the event/root point
day placement             unsupported
```

Total Revenue may remain establishable.

Revenue by day may not.

This case proves that placement standing is not merely another spelling of measure support.

## 7.4 No record and no evidence of event occurrence

Then:

```text
point existence           unsupported
```

The system must not pretend that the point is nonexistent.

Nor should it invent a candidate point carrying a forest of missing measures.

---

# 8. Measure eligibility standing

Once the relevant analytical point has been established, family-specific eligibility can be evaluated.

For \(F@A\), an established \(a\in A\) may be:

```text
eligible for F
ineligible for F
eligibility unresolved / unsupported
```

The third state deserves explicit recognition even if Frame-QL does not expose a separate public predicate immediately.

Example:

```text
metric applies only to active subscriptions
customer-month exists
active-status evidence is unavailable
```

The system cannot truthfully say either:

```text
ineligible
```

or:

```text
eligible but missing
```

until eligibility itself is established.

Therefore:

> **`missing(E)` is meaningful only after eligibility has been positively established.**

---

# 9. Measure support and missing

For an established analytical point \(a\) and an expression/family \(E\) known to be eligible there:

```text
supported(E)
```

means the governed evidence required to establish its semantic value is available.

```text
missing(E)
```

is reserved for:

\[
\boxed{
Eligible(E)\land \neg Supported(E)
}
\]

at an established and adequately placed analytical point.

It does not mean:

```text
point does not exist
point existence is unsupported
placement under required anchor is unsupported
eligibility is unsupported
measure is ineligible
carrier value is SQL NULL
conversion failed
```

This is the central lexical discipline of R4.

---

# 10. Supported zero

A supported zero remains an ordinary supported semantic value:

\[
Supported(E)\land value(E)=0.
\]

It is not missing.

The existence law and completion/support law determine when an absent observation can lawfully establish zero.

Example in a declared operating-calendar universe:

```text
store-day exists
Revenue eligible
governed no-sales rule establishes Revenue = 0
```

Then Revenue is supported with value zero.

An absent physical sales row is therefore not enough to infer either zero or missingness.

---

# 11. Standing is not carrier nullability

Carrier states such as:

```text
SQL NULL
NaN
missing dataframe cell
absent JSON field
parse failure
```

are realization facts.

They may supply evidence for a standing determination.

They do not define analytical standing.

In particular:

```text
carrier NULL
```

can represent, depending on realization:

- unsupported measure value;
- ineligible measure;
- unknown coordinate;
- conversion failure;
- carrier limitation;
- or another condition.

Frame-QL must not infer one semantic standing merely from carrier representation.

---

# 12. Conceptual introspection layers

The language may eventually expose standing introspection.

The semantic model suggests at least:

## Point existence

Conceptually:

```text
exists(point)
existence_supported(point)
```

## Anchor placement

Conceptually, without freezing spelling:

```text
placed(point, A)
placement_supported(point, A)
```

or another equivalent surface.

## Measure eligibility and support

Conceptually:

```text
eligible(E)
eligibility_supported(E)
supported(E)
missing(E)
```

Exact spellings remain open.

The important point is jurisdiction:

```text
exists / placement
    point and geometry standing

eligible / supported / missing
    measure standing
```

These are not ordinary nullable-value functions.

---

# 13. Frame-level consequence

A Frame-QL request usually asks for a complete result at an output anchor.

Unsupported existence or placement can affect that frame without being representable as missing values in returned rows.

For example, suppose one known transaction has an unknown day.

The system must not silently produce daily Revenue from the remaining transactions and call the frame complete.

Possible governed outcomes include:

```text
Refuse
Clarify
Disclose an explicitly governed partial result
```

depending on the request, profile, and governing policy.

The semantic point is:

> **Unknown placement changes support of the anchored result even when no returned cell corresponds to a "missing transaction row."**

The frame can therefore have a support defect whose cause lies upstream of any displayed cell.

---

# 14. Aggregation and denominator consequence

Known lost records are especially important for counts and averages.

Suppose governance establishes:

```text
100 transactions occurred
99 Revenue values are supported
1 transaction's Revenue value is lost
```

Then the transaction population remains 100.

The system must not silently transform this into:

```text
99 transactions
99 Revenue values
```

merely because only 99 ordinary records remain.

Therefore an observed-row average:

\[
\frac{\sum_{99} Revenue}{99}
\]

does not answer a governed request for mean Revenue over the 100-transaction eligible population unless a separate governed rule says otherwise.

Existence evidence and value support are separate inputs to analytical establishment.

---

# 15. Propagation rules

The following rules summarize the standing dependencies.

## 15.1 Unsupported existence

If existence of \(\omega\) is unsupported, then claims whose population or support depends on whether \(\omega\in\Omega_U\) cannot be fully established.

Do not represent this as a family of invented missing measure values.

## 15.2 Unsupported placement

If \(\omega\) is known to exist but placement under \(A\) is unsupported, then claims requiring:

\[
\pi_A(\omega)
\]

cannot be fully established.

Claims invariant to that placement may remain establishable.

## 15.3 Ineligibility

If an established point is ineligible for \(F\), there is no missing \(F\)-value at that point.

## 15.4 Unsupported eligibility

If eligibility cannot be established, the system may not coerce the case into either ineligible or missing.

## 15.5 Missing measure

Only after point existence, required placement, and eligibility are established may:

\[
missing(E)
\]

mean eligible-but-unsupported measure value.

---

# 16. Acceptance suite for R4

These cases are semantic tests. A future grammar/profile may expose them differently, but no implementation should contradict their expected judgments.

| Case | Expected semantic judgment |
|---|---|
| event known not to have occurred | point nonexistent |
| no record and no governed evidence whether event occurred | point existence unsupported |
| event known to have occurred, Revenue lost, date retained | point exists; placement established; Revenue may be missing |
| event known to have occurred, whole record lost | point exists; any lost coordinates have unsupported placement; affected measures may separately be unsupported |
| event exists, Revenue preserved elsewhere, date lost | Revenue may remain supported; day placement unsupported; total may be establishable while Revenue@day is not |
| operating-calendar store-day exists, no sales row, governed zero rule | point exists; Revenue supported with zero |
| operating-calendar store-day exists, feed failed | point exists; Revenue eligible; Revenue missing/unsupported |
| transaction exists, customer known, day unknown | customer-anchored claims may remain possible; day-dependent claims are blocked |
| point exists, metric not applicable | ineligible; not missing |
| point exists, applicability evidence unavailable | eligibility unsupported; not yet missing |
| carrier SQL NULL | no semantic judgment without governing realization context |
| numeric parse failure | conversion/realization failure; not missing by itself |
| 100 known events, 99 supported Revenue values | population remains 100; do not shrink denominator to 99 |
| one known event has unknown day | daily frame cannot silently omit it and claim complete support |
| point existence unsupported | do not create N measure-level missing flags as its semantic representation |
| `mean(revenue)` with multiple identity-bearing inner anchors | request under-specified / Clarify; not missing data |
| `E @ A` where A is not a governed anchor | invalid/unestablished anchor geometry; do not evaluate placement or missingness |
| coordinate tuple is syntactically nameable but no root point occupies it in an event universe | no anchor point merely from coordinate spelling |

---

# 17. Consequences for the larger vNext architecture

R4 should now be summarized as:

> **Point existence, anchor placement, eligibility, measure support, and semantic value are distinct standing layers. Missing is reserved for eligible-but-unsupported measure standing after the required point and placement have been established.**

The broader vNext expression architecture remains unchanged.

This amendment does **not** require:

- a new ToD ontological primitive;
- final public syntax for placement predicates;
- immediate changes to the current fill-rule representation;
- immediate wire changes;
- implementation authorization.

It does require the canonical language rewrite to stop using a two-layer "point standing versus measure standing" explanation when that phrasing would hide anchor-relative placement support.

---

# 18. Open naming question

The distinction is settled.

The public name is not.

Working candidates include:

```text
anchor-placement standing
placement standing
projection standing
coordinate standing
anchor-membership standing
```

No choice is forced yet.

The formal idea is clearer than the vocabulary:

\[
\boxed{
\text{support for establishing } \pi_A(\omega)
}
\]

Delay naming until the Manual prose makes one term feel inevitable.

---

# 19. Stop-gate

Before profile or implementation reconciliation of missingness/fill behavior, the language-law standing chapter should be rewritten against this acceptance suite.

Do not let the existing carrier/fill enum determine the semantic categories.

The next implementation-facing question is not:

> "Which null enum should represent placement failure?"

It is:

> **Which current authoring, planner, carrier, and wire facts correspond to each of the standing layers above, and where does the current system lack enough information to represent them faithfully?**

That is a later reconciliation task.
