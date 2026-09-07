# Frame-QL vNext — O2 Reconciliation to Theory of Data v7.1

**T7.1-C — Working Draft 0.1 — 6 September 2026**  
**Status:** Semantic reconciliation note  
**Authority:** ToD v7.1 ordered-family amendment v0.2  
**Purpose:** Reconcile O2 ordered-expression architecture with the corrected Theory of Data family boundary.  
**Not a syntax release. Not an implementation authorization.**

---

## 1. Why O2 must change

O2 originally treated analytical-point-order dependence as a reason to place FIRST, LAST, LAG, RANK, cumulative, and rolling operations in one general ordered-expression layer outside measure families.

ToD v7.1 corrects that boundary.

The decisive distinction is no longer:

`order-independent family` versus `order-dependent expression`.

It is:

```text
ordered analytical operation
    ├── satisfies the measure-family contract
    │       → ordered measure family
    │
    └── does not
            → general ordered expression
```

FIRST and LAST are canonical ordered-family candidates.

Ordinary LAG, LEAD, RANK, ROW_NUMBER, cumulative, and rolling operations remain general ordered expressions under their focal meanings.

TOP-k can be an ordered measure family when defined with exact rich state.

---

## 2. The O2 common-core abstraction was too broad

O2 proposed:

```text
Ordered Expression
    =
Operand
+ Governed Ordered Domain
+ Operator Law
```

with a general peer/sequence/domain structure shared by FIRST/LAST and focal ordered operations.

That overgeneralizes.

FIRST/LAST do not need a generic peer domain when they are understood as ordered family laws.

Their semantics come from:

```text
support anchor S
governed order over the analytical point space of S
current target anchor A
projection S → A
family law
```

The current anchor `A` itself supplies the support fiber:

`S(a) = π_(S→A)^(-1)(a)`.

There is no separate constitutive peer anchor in the foundational family law.

---

## 3. Ordered family branch

An ordered measure family has the semantic form:

`G = L_OS(F)`

where:

- `F` is the operand family;
- `S` is the constitutive support anchor;
- `OS` is the governed ordered support structure on `S`;
- `L` is the ordered family law.

For multidimensional:

`S = A1 × ... × An`,

`OS` includes:

- governed root-dimensional factorization;
- dimension precedence;
- complete point order within every constituent dimension;
- induced complete analytical-point order `≺S`.

For any admitted current anchor `A`, the measure at point `a` is formed from the support fiber `S(a)`.

This branch must satisfy:

- identity completeness;
- projection-fiber locality;
- exact sufficient state;
- enumeration invariance;
- direct/staged path coherence;
- governed materialization/re-entry.

---

## 4. LAST

LAST becomes:

`LAST_OS(F)`.

At current point `a`:

`LAST_OS(F)@a = F @ max_(≺S) S(a)`.

Important consequences:

1. LAST acts on established measures at `S`, not carrier rows.
2. No generic tie selector is part of canonical LAST.
3. If multidimensional order is incomplete, the ordered support is under-specified.
4. Physical row order can never complete the support order.
5. The reusable state retains the winning support point and value.

Legacy:

`FAMILY { last ORDER day }`

is therefore not the semantic model.

At best it is an incomplete historical encoding of part of `OS`.

---

## 5. FIRST

FIRST is symmetric:

`FIRST_OS(F)@a = F @ min_(≺S) S(a)`.

It belongs to the same ordered-family branch.

---

## 6. TOP-k

TOP-k is also admissible in principle as an ordered measure family when:

- support order is governed;
- the exact top-k witness set is sufficient state;
- merge is exact;
- projection-fiber locality holds.

This is useful because it demonstrates that the family branch is not limited to scalar extrema.

---

## 7. General focal ordered-expression branch

The following ordinary operations remain general ordered expressions because their focal value depends on analytical points outside the focal point's own projection fiber:

```text
LAG
LEAD
RANK
DENSE_RANK
ROW_NUMBER
cumulative operations
rolling operations
```

These still need much of O2's domain/context machinery.

Their semantic form may remain close to:

```text
General Ordered Expression
    operand
    focal anchor
    contextual ordered domain
    governed order
    operator-specific neighborhood / relation law
    result-locus law
```

This branch must not be forced into measure-family continuation.

---

## 8. What survives from O2 for general expressions

The following O2 discoveries remain useful:

- order is over analytical points, not rows;
- physical order is never authority;
- query-level output `ORDER BY` is orthogonal to inner ordered meaning;
- order standing must be positively established;
- LAG/ROW_NUMBER need stronger positional determinacy than RANK;
- rolling positional windows and order-range windows are different laws;
- contextual domain must be governed;
- focal operations need a distinct result-locus rule;
- missing/unsupported ordered-domain participation cannot silently disappear.

These belong to the general ordered-expression branch.

---

## 9. What is retired from O2 for FIRST/LAST

The following should no longer be used to define canonical FIRST/LAST:

- generic `peer anchor`;
- `peer domain = output anchor minus order axis`;
- generic tie semantics;
- arbitrary order-key list as the theory;
- SQL-like `PARTITION BY` analogy;
- assumption that FIRST/LAST are forever outside families;
- assumption that order-dependence itself blocks family continuation.

Some of these may remain useful implementation terms for general ordered expressions, but they are not the ToD semantics of ordered families.

---

## 10. Revised 2×2

The implementation/analytical shape remains useful:

| | anchor-preserving | anchor-changing |
|---|---|---|
| analytical-point-order independent | pointwise/map-like | ordinary reduction |
| analytical-point-order dependent | focal ordered operation | ordered reduction |

But the table does **not** decide family standing.

Instead:

```text
ordered reduction
    + family-law contract satisfied
        → ordered measure family

ordered reduction
    + family-law contract not satisfied
        → non-family ordered operation
```

FIRST/LAST are canonical examples of the first case.

Execution shape must never itself grant family-founding rights.

---

## 11. Consequence for the current FIRST/LAST defect

The earlier O2 diagnosis:

> tied LAST lacks governed tie semantics

should be retired for the canonical family case.

The corrected diagnosis is:

> **the engine can apply LAST to carrier rows before it has established the measure at the governed ordered support anchor.**

If several carrier rows lie beneath one support point, physical row multiplicity can leak into argmax/argmin selection.

That is an ordered-support formation defect.

If distinct support points exist in a multidimensional support, the complete analytical order must already be induced from:

- dimension precedence; and
- complete within-dimension orders.

No backend tie behavior is analytical authority.

---

## 12. Consequence for R4-C0 ordered-path contamination

The R4-C0 ordered-path hole remains real.

If evidence cannot be positively placed in the ordered support point space required by an ordered family or focal ordered expression, it may not contribute to that ordered computation before later frame containment.

The corrected invariant is:

> **An ordered computation may consume only support points whose required analytical placement in its governed ordered domain has been established.**

This applies to both ordered families and general ordered expressions.

It does not require full R4 standing to state the containment obligation.

---

## 13. Ordered support is a Manifold-level governed object

Frame-QL should consume a resolved governed order; it should not invent one from syntax.

For support:

`S = A1 × ... × An`,

the language/runtime eventually needs access to:

```text
support anchor S
root-dimensional factorization
dimension precedence
complete point order within each Ai
induced support-point order
```

The Manifold/CDT boundary must determine how those facts are authored and typed.

Frame-QL may allow explicit selection among already-governed orders, but query syntax should not create analytical order by merely listing sort keys.

---

## 14. Surface compatibility

Public query spelling such as:

`stock.last`

is a genuine compatibility obligation.

The legacy declaration mechanism:

`FAMILY { last ORDER day }`

need not remain the semantic mechanism.

The successor should preserve the public analytical capability by resolving `stock.last` to the appropriate governed ordered family law.

Only after the successor exists should legacy declarations be normalized or retired deliberately.

---

## 15. Named reusable general ordered expressions

This remains separate.

A durable named LAG, rolling, or cumulative expression may eventually use the DERIVED/named-expression layer.

That does not affect ordered-family identity.

Do not use the needs of named focal expressions to shape the ordered-family object prematurely.

---

## 16. Revised semantic taxonomy

The vNext taxonomy should distinguish:

```text
family reference
measure expression
general anchorable expression
tuple expression
family-forming analytical expression
ordered family-forming analytical expression
general focal ordered expression
predicate / standing expression
```

This is a semantic classification, not necessarily a surface grammar taxonomy.

The important new distinction is:

```text
ordered family-forming expression
    ≠
general focal ordered expression
```

---

## 17. Capability-registry consequence

The future canonical semantic classification should not force FIRST/LAST into the same class as LAG/RANK merely because all require analytical order.

Possible semantic distinctions may eventually include:

```text
family_forming
ordered_family_forming
ordered_focal
predicate
structural
```

Exact names are not frozen here.

The governing rule is:

> operator classification must reflect analytical law, while family authority is independently checked by the family-law contract.

Do not immediately alter runtime `Operator.kind` or the capability registry from this note alone.

---

## 18. Required next theory/design unit

Before implementation, the next architecture problem is the governed order itself.

Questions:

1. How does a Manifold declare complete order within one root anchor dimension?
2. How is dimension precedence declared for a multidimensional support anchor?
3. How does CDT provide comparison/order capability for analytical point values?
4. How are hierarchical anchor levels related to root-dimension order?
5. How is ordered support identity canonicalized?
6. Can multiple governed orders coexist on the same support anchor?
7. How does a family select which governed order constitutes it?
8. How does the resolved artifact expose ordered support without making query syntax authoritative?

This is T7.1-D / O3.

---

## 19. Reconciled program

```text
DONE
    T7.1-A v0.2 ordered-family theory
    T7.1-B stress test
    T7.1-C O2 reconciliation

NEXT
    O3 governed analytical-order architecture
        root-dimension point order
        dimension precedence
        CDT comparison capability
        ordered-support identity

THEN
    reframe current correctness containment under O3
    implement bounded containment
    implement successor ordered-family path
    implement successor focal ordered-expression path
    normalize public .last compatibility
    retire legacy family declaration mechanism
```

---

## 20. Conclusion

O2 remains valuable, but it now divides into two semantic architectures.

**Ordered measure families** operate over a governed ordered support anchor and remain projection-fiber local, compositional, enumeration-invariant, and path-coherent.

**General focal ordered expressions** use governed order and contextual analytical domains but may depend on neighboring or comparison points outside the focal projection fiber.

FIRST/LAST belong naturally to the first branch.

LAG/RANK/cumulative/rolling belong naturally to the second under their ordinary meanings.

This reconciliation removes SQL/window artifacts from the theory of LAST while preserving the O2 machinery where it is actually needed.
