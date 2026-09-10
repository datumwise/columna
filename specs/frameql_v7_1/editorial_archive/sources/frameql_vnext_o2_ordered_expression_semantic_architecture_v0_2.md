# Frame-QL vNext — O2 Ordered-Expression Semantic Architecture

**Working Draft 0.2 — 6 September 2026**  
**Status:** Semantic architecture  
**Purpose:** Derive the minimal common structure of ordered analytical expressions independently of legacy FIRST/LAST family-founding behavior.  
**Authority posture:** successor design; legacy bonus behavior is intentionally ignored except in a retirement appendix.  
**Not a syntax release. Not an implementation authorization.**

---

# 0. Position

Theory of Data v7 keeps measure-family continuation order-independent.

Frame-QL therefore needs a separate expression layer for analytics whose result depends on an order over analytical points.

Examples include:

```text
FIRST
LAST
LAG
LEAD
RANK
DENSE_RANK
ROW_NUMBER
cumulative operations
rolling operations
```

The common architecture should not be derived from SQL window syntax, current Core reducer/scan classes, or legacy:

```text
FAMILY { last ORDER ... }
```

Those are implementation/history concerns.

The successor question is:

> **What semantic structure must exist for an order-sensitive analytical result to be determinate?**

The answer developed here is:

```text
ordered analytical expression
    =
operand expression
+ ordered analytical domain
+ operator-specific selection / neighborhood law
+ operator-specific result-locus law
+ operator-specific standing / exceptional-case law
```

The familiar surface fields:

```text
order key
direction
ties
window
offset
```

are possible spellings or decompositions of that deeper structure.

They are not the architecture itself.

---

# 1. The ordered analytical domain

An ordered expression operates over analytical points, not physical rows.

Let:

- \(U\) be the governed universe;
- \(I\) be the **sequence anchor** at which the operand and order expressions participate;
- \(P\) be the **peer anchor**, with:

\[
I \succeq P.
\]

The refinement relation gives a governed projection:

\[
\pi_{I\rightarrow P}: I\rightarrow P.
\]

For each peer point \(p\in P\), the sequence candidates are the \(I\)-points in its fiber:

\[
I(p)=\{i\in I:\pi_{I\rightarrow P}(i)=p\}.
\]

The peer anchor may be the coarsest anchor when all participating points belong to one peer set.

It may also equal the sequence anchor, although many ordered operations become trivial in that case.

This gives the first structural object:

\[
\boxed{
\text{ordered domain}
=
(I,\ P,\ \pi_{I\to P},\ O)
}
\]

where \(O\) is a governed order specification over the participating \(I\)-points inside each peer fiber.

---

# 2. Why sequence anchor and peer anchor are different roles

Consider daily account balances.

The complete sequence points are not merely `day`.

They are:

```text
{account, day}
```

because a balance is a value about one account-day.

So:

```text
sequence anchor I = {account, day}
peer anchor P     = {account}
order             = day chronology within each account
```

Then:

```text
LAST(balance @ {account, day})
```

can select one terminal account-day inside each account peer.

This distinction prevents a common mistake.

`day` is the **order coordinate**.

`{account, day}` is the **analytical point anchor being sequenced**.

`{account}` is the **peer partition**.

Those are different semantic roles even when surface syntax makes them look compact.

---

# 3. The peer domain is governed analytical geometry

The peer domain is not a free `PARTITION BY` list.

For the foundational vNext ordered-expression model, peers are induced by a governed anchor \(P\) that is coarser than or equal to the sequence anchor \(I\).

Thus:

\[
I\succeq P.
\]

This gives every sequence point exactly one peer fiber under governed partition geometry.

If a proposed peer grouping is not a partition—for example overlapping category membership—it cannot silently become an ordered peer domain.

The system first needs lawful structure such as:

```text
single-valued assignment
allocation where analytically appropriate
membership universe
another governed derived anchor
```

This keeps ordered analytics inside the same analytical geometry as the rest of Frame-QL.

No special peer ontology is introduced.

---

# 4. The order is a governed relation over analytical points

The semantic object is not fundamentally:

```text
key = day
direction = ASC
```

It is a governed order relation over participating points.

For each peer fiber \(I(p)\), let:

\[
\preceq_O
\]

denote the order relation required by the expression.

The relation may be established from one or more order expressions evaluated at the sequence points.

Conceptually:

```text
order expressions:
    day
    event_time
    revenue
    (event_time, transaction_id)
```

with governed comparison semantics supplied by their semantic value types and the requested/governed ordering convention.

Direction is therefore best understood as part of the order relation itself.

For example:

```text
chronological(day, ascending)
reverse_chronological(day)
descending(revenue)
lexicographic(event_time ASC, transaction_id ASC)
```

may all establish different relations.

The final surface grammar may decompose those relations into keys plus `ASC` / `DESC`.

The semantic architecture need not.

---

# 5. Order-key standing

Every participating sequence point whose position matters must have enough governed standing to be placed in the required order.

Suppose a transaction is known to exist and is placed at `{account, transaction}`, but its event time is unsupported.

If event time is the required order expression, the system cannot silently remove that transaction from the sequence and call the resulting LAST or LAG complete.

This is not physical sorting failure.

It is an upstream support defect in the ordered analytical domain.

The governing rule is:

> **An eligible sequence point whose required order standing is unsupported may not silently disappear from the ordered domain.**

The outcome may be refusal, disclosure, or another governed partial-result policy depending on the eventual language/profile contract.

The semantic architecture only requires that the loss remain visible.

---

# 6. Peer-placement standing

Likewise, a point may exist at the sequence anchor while its placement under the peer anchor is unsupported.

For:

```text
I = {account, day}
P = {account}
```

if the account coordinate is unsupported for an existing sequence point, the system cannot determine which account sequence contains that point.

This is the ordered-expression analogue of the R4 placement problem.

It must not be repaired by:

```text
dropping the point
placing it into NULL account
putting it into an arbitrary peer
```

The ordered domain depends on positive peer placement.

---

# 7. Candidate points, operand support, and participation are different

An ordered expression has at least three distinct questions about a sequence point \(i\):

1. **Does the analytical point participate in the ordered domain?**
2. **Can its order position be established?**
3. **Is the operand value supported there?**

These must not be collapsed.

Consider:

```text
LAG(balance)
```

at an account-day point whose immediate predecessor exists but has unsupported Balance.

Two possible semantics are:

```text
A. predecessor position exists; returned lag value is unsupported

B. skip unsupported Balance points and use the previous supported Balance
```

Those are different analytical expressions.

Neither may be inferred merely from implementation convenience.

Therefore each ordered operator law needs an explicit **participation / operand-standing rule**.

The architecture does not impose one global "ignore missing" convention.

---

# 8. Common semantic decomposition

An ordered analytical expression can be decomposed into:

\[
\boxed{
\mathcal E
=
\operatorname{OrdExpr}
(E,\ \mathcal D,\ L,\ \theta)
}
\]

where:

- \(E\) is the operand expression;
- \(\mathcal D\) is the ordered analytical domain;
- \(L\) is the operator-specific law;
- \(\theta\) is any meaning-bearing parameter set.

The ordered domain contains:

\[
\mathcal D
=
(I,\ P,\ \pi_{I\to P},\ O,\ R_D).
\]

Here \(R_D\) is the **domain-formation rule** that determines which governed sequence points are candidates for the ordered expression under the request. It is part of semantic meaning; the realized point set is request/data dependent and is not itself part of canonical identity.

The operator law \(L\) determines:

```text
what focal object(s) the expression is evaluated for
which sequence point(s) or neighborhood are selected
what value operation is applied
where the result lives
what order strength is required
how unsupported operand/order standing behaves
what exceptional cases do
```

This is the minimal common structure.

---

# 9. Result locus: peer-collapsing versus focal-preserving

Ordered operations divide naturally by where their result lives.

This is not a new ontology.

It is a property of the operator law.

## 9.1 Peer-collapsing ordered expressions

These produce one result per peer fiber.

Examples:

```text
FIRST
LAST
```

With sequence anchor \(I\) and peer anchor \(P\):

```text
input points       I
peer fibers        P
result location    P
```

The operation selects one point from each peer fiber and returns the operand value associated with that selected point.

This movement from \(I\) to \(P\) is **not a ToD reducer**.

It is order-sensitive point selection.

## 9.2 Focal-preserving ordered expressions

These produce one result for each focal sequence point.

Examples:

```text
LAG
LEAD
RANK
DENSE_RANK
ROW_NUMBER
cumulative operations
rolling operations
```

Their result location remains \(I\).

The peer anchor supplies context.

The focal sequence point supplies the output point.

Thus:

```text
input / focal anchor    I
peer context            P
result location         I
```

The peer anchor is contextual; it is not a second current anchor of the result.

---

# 10. FIRST and LAST

For each peer point \(p\in P\), let:

\[
D_p\subseteq I(p)
\]

be the governed participating sequence points.

FIRST selects a governed minimal point:

\[
s_{\min}(p)\in D_p.
\]

LAST selects a governed maximal point:

\[
s_{\max}(p)\in D_p.
\]

The result value is the operand at that selected point.

Conceptually:

\[
LAST(E;\mathcal D)@p
=
E@s_{\max}(p).
\]

The result lives at the peer anchor \(P\).

## 10.1 Order requirement

FIRST/LAST require a unique selected boundary point or an operator law that governably resolves an otherwise non-unique boundary.

A mere tied order-key value is not enough to choose one physical row.

## 10.2 Missing selected operand

If the selected terminal point exists and its operand value is unsupported, LAST does not silently retreat to an earlier supported value unless the operator law explicitly defines a "last supported" expression.

These are different semantics:

```text
last point's balance

last supported balance
```

The canonical language must not collapse them.

---

# 11. LAG and LEAD

LAG and LEAD are focal-preserving.

For focal point \(i\in D_p\), the operator selects a relative sequence point.

Conceptually:

\[
Lag_k(i)
\]

is the point \(k\) predecessor positions before \(i\) under the governed sequence order.

Likewise:

\[
Lead_k(i)
\]

is the \(k\) successor.

The result remains at \(i\), hence at sequence anchor \(I\).

## 11.1 Stronger order requirement

Positional LAG/LEAD require an order strong enough to determine predecessor/successor positions.

A total preorder with unresolved ties may be sufficient for RANK but insufficient for positional LAG.

Therefore "tie semantics" is not one universal field.

The operator law determines what order structure it requires.

## 11.2 Unsupported predecessor value

If the predecessor point is established but the operand is unsupported there, the lagged result is unsupported under the ordinary positional law.

Skipping to another supported point would define a different operator.

---

# 12. RANK, DENSE_RANK, and ROW_NUMBER

Ranking exposes why ordered operators need different order-strength requirements.

## 12.1 RANK

RANK can operate over equivalence classes induced by tied order keys.

Points with equal order standing can share one rank.

The result remains at each focal sequence point.

## 12.2 DENSE_RANK

DENSE_RANK likewise permits ties but assigns ordinal values to distinct order classes without gaps.

## 12.3 ROW_NUMBER

ROW_NUMBER requires a fully determinate sequence position for each point.

If order keys tie and no governed secondary ordering exists, ROW_NUMBER is underdetermined.

Therefore:

```text
RANK
    can admit tied order classes

ROW_NUMBER
    requires unique position
```

The same order specification can be lawful for one and insufficient for the other.

---

# 13. Cumulative operations

A cumulative operation is focal-preserving.

For focal point \(i\in D_p\), it selects a prefix-like neighborhood:

\[
N(i)\subseteq D_p.
\]

A cumulative sum conceptually applies an order-independent sum law to the values in that order-dependent neighborhood:

\[
CumSum(E)(i)
=
sum\{E@j:j\in N(i)\}.
\]

The inner value combination may use a familiar family-forming law.

The overall expression remains ordered because \(N(i)\) depends on the focal point and the selected order.

This is important:

> **Using SUM inside an ordered neighborhood does not make the cumulative expression a SUM measure family.**

The order-dependent neighborhood is part of the expression's meaning.

---

# 14. Rolling operations

Rolling operations are also focal-preserving.

Their defining feature is an operator-specific neighborhood law:

\[
N_\theta(i).
\]

Different neighborhood laws establish different analytical expressions.

## 14.1 Positional window

Example:

```text
previous 7 sequence points including current
```

The neighborhood depends on sequence position.

## 14.2 Order-value range window

Example:

```text
points whose timestamps lie within the preceding 7 days
```

The neighborhood depends on distance in the order-key value domain.

These are not interchangeable.

A seven-point window is not a seven-day window.

The canonical ordered-expression meaning must preserve which neighborhood law was used.

---

# 15. Selection / neighborhood law is the real common operator axis

FIRST/LAST, LAG/LEAD, cumulative, and rolling operations can now be stated uniformly.

Each operator supplies a law that maps the ordered peer domain to selected point(s) or neighborhoods.

Conceptually:

\[
Selection_L:
(D_p,\ i?)
\rightarrow
\mathcal P(D_p)
\]

where a focal point \(i\) is present for focal-preserving operators.

Examples:

```text
FIRST
    whole peer domain → first boundary singleton

LAST
    whole peer domain → last boundary singleton

LAG k
    focal point → predecessor singleton

LEAD k
    focal point → successor singleton

CUMULATIVE
    focal point → prefix neighborhood

ROLLING
    focal point → governed local neighborhood

RANK
    focal point → ordinal standing derived from order classes
```

RANK does not literally need a selected value subset, so the most general term is **ordered operator law** rather than "window law."

The selection/neighborhood formulation nevertheless explains most of the family.

---

# 16. Tie behavior is operator-relative

The architecture should not freeze a universal field:

```text
ties = ...
```

before the operator laws require one.

The deeper rule is:

> **The governed order must be strong enough for the result the operator claims to establish.**

Examples:

```text
LAST
    needs a unique terminal point or governed selector

LAG
    needs unique relative positions

RANK
    may admit tied equivalence classes

DENSE_RANK
    may admit tied equivalence classes

ROW_NUMBER
    needs unique total positions

RANGE rolling window
    may naturally include every point tied at a boundary value
```

Surface syntax may still expose tie options.

Their semantics come from operator-specific order requirements.

---

# 17. Direction belongs to order meaning

Likewise, the architecture does not require a universal independent `direction` field.

Changing direction changes the order relation.

Therefore direction is meaning-bearing wherever the resulting relation changes.

Conceptually:

```text
day ascending
day descending
```

are different order specifications.

A surface grammar may spell this with:

```text
ASC
DESC
```

The resolved semantic artifact should carry the actual governed order relation or an equivalent canonical specification.

---

# 18. Reset and partition boundaries

Some current systems express concepts such as:

```text
reset at year
partition by account
within region
```

The architecture should not treat all of them as one generic parameter.

The peer anchor already determines one stable partition of the sequence domain.

A "reset" inside a peer may instead define a finer neighborhood boundary or a derived peer anchor.

Example:

```text
YTD cumulative revenue per account
```

could use:

```text
sequence anchor    {account, day}
peer anchor        {account, year}
order              day chronology
neighborhood       prefix within account-year peer
result             {account, day}
```

If `year` is lawfully part of the peer partition, no separate reset primitive is required.

This suggests a design preference:

> **Represent reset as governed peer geometry where possible; introduce a separate reset construct only where real examples cannot be expressed that way.**

Do not invent both prematurely.

---

# 19. WHERE and ordered-domain formation

Frame-QL `WHERE` is request-local analytical restriction applied before affected expressions are formed.

Therefore the ordered domain is built from the restricted eligible analytical points, subject to the operator's own participation law.

This means:

```text
WHERE ...
```

can change:

- which sequence points participate;
- which point becomes FIRST/LAST;
- rank standing;
- cumulative neighborhoods;
- rolling neighborhoods.

That is expected.

`WHERE` does not act as output selection.

`HAVING` and `LIMIT` do not retroactively alter the ordered expression's input domain.

---

# 20. Output ORDER BY remains orthogonal

Query-level:

```text
ORDER BY
```

orders the returned frame.

The ordered analytical domain is established independently.

Even when the same key appears in both places, there is no ambient inheritance.

Thus:

```text
SELECT lag(balance ...)
AT {account, day}
ORDER BY day
```

does not complete the LAG order contract.

The LAG expression must already have one governed order meaning.

---

# 21. Ordered expressions do not gain continuation law by syntax

An ordered expression can produce a lawful analytical result.

It does not thereby acquire a ToD measure-family continuation law.

For example:

```text
last(balance ...)
```

may produce one result per account.

That does not mean the resulting values can be further rolled from account to region under a family-preserving LAST law.

Any later analytical operation must be justified independently.

Similarly, a rolling mean series can be materialized physically without acquiring measure-family sufficient-state authority.

> **Availability is not continuation permission.**

---

# 22. Reusable governed ordered expressions

A future Manifold may need to name an ordered expression for reuse.

Examples include conceptually:

```text
closing_balance
previous_balance
seven_day_rolling_revenue
account_ytd_revenue
```

Such an object can have durable governed expression identity without being a ToD measure family.

Its identity would need to preserve the meaning-bearing ordered-expression contract.

The exact Manifold object class and authoring syntax remain open.

This need should be solved directly.

It should not be routed through legacy family-founding FIRST/LAST.

---

# 23. Canonical semantic signature

Without freezing a concrete serialization, a canonical ordered expression must preserve every meaning-bearing component needed to distinguish its result.

At minimum:

```text
operator identity
operand identity
sequence anchor
peer anchor
governed order specification
domain-formation / participation rule
operator-specific operand-standing rule
operator-specific parameters
operator-specific operand-standing law
operator-specific selection / neighborhood law
result-locus rule
```

Where relevant, the canonical meaning must also retain:

```text
secondary order expressions
order-value comparison semantics
window extent
positional versus value-range window kind
boundary inclusion
offset
exceptional-case policy
```

The resolved canonical semantic artifact may carry this information even when surface syntax uses governed shorthand.

---

# 24. Surface syntax remains downstream

No exact syntax is authorized here.

Possible future forms may resemble:

```text
last(balance @ {account, day}; within={account}; by=day ASC)

lag(balance @ {account, day}; within={account}; by=day ASC; offset=1)

rank(revenue @ {region, product}; within={region}; by=revenue DESC)

rolling_mean(
    revenue @ {store, day};
    within={store};
    by=day ASC;
    range=7 days
)
```

These are illustrations only.

The architecture must not be bent to make one of these spellings convenient.

---

# 25. Operator acceptance suite

## 25.1 FIRST / LAST

| Case | Expected judgment |
|---|---|
| one governed peer anchor + unique order | determinate |
| tied terminal order values, no governed selector | underdetermined |
| terminal point known, operand unsupported | selected result unsupported; do not silently choose earlier supported point |
| peer placement unsupported for an eligible point | ordered result incomplete/unestablished; do not drop point silently |
| order key unsupported for an eligible point | ordered result incomplete/unestablished; do not drop point silently |
| peer anchor not coarser than sequence anchor | invalid ordered domain under foundational model |
| output at peer anchor | valid operator-locus rule; does not make FIRST/LAST a reducer |

## 25.2 LAG / LEAD

| Case | Expected judgment |
|---|---|
| unique positional sequence | determinate |
| tied positions, no secondary order | underdetermined |
| predecessor exists, predecessor operand missing | lag result missing/unsupported under ordinary positional law |
| implementation skips missing predecessor | different operator semantics; not canonical LAG unless explicitly governed |
| first point with no predecessor | governed boundary/exceptional case required |
| result location | sequence/focal anchor |

## 25.3 RANK / DENSE_RANK / ROW_NUMBER

| Case | Expected judgment |
|---|---|
| tied order values for RANK | lawful; shared rank according to rank law |
| tied order values for DENSE_RANK | lawful; dense shared rank |
| tied order values for ROW_NUMBER without selector | underdetermined |
| output location | sequence/focal anchor |

## 25.4 Cumulative

| Case | Expected judgment |
|---|---|
| cumulative sum by governed order | lawful ordered expression |
| same points reversed | different expression/result |
| tied boundary with unspecified prefix semantics | operator contract incomplete where result can change |
| result location | sequence/focal anchor |
| use of SUM inside prefix | does not turn whole cumulative expression into SUM family |

## 25.5 Rolling

| Case | Expected judgment |
|---|---|
| 7 preceding points | positional neighborhood |
| preceding 7 days | order-value range neighborhood |
| same data under two window kinds | different ordered expressions |
| boundary inclusion changes result | meaning-bearing parameter |
| result location | sequence/focal anchor |

---

# 26. Cross-case invariants

The stress tests support the following general rules.

## O2-I1 — analytical points, not rows

Order is over governed analytical points at the sequence anchor.

## O2-I2 — peer geometry is explicit

Peer fibers come from governed anchor geometry, not arbitrary physical partitions.

## O2-I3 — order is a relation

Keys and direction are surface/representation ingredients for a governed order relation.

## O2-I4 — order strength is operator-relative

Different operators require different degrees of positional uniqueness.

## O2-I5 — participation is governed

Unsupported order keys or peer placement may not silently remove candidate points. Operand support is governed separately by the operator-specific operand-standing rule; skipping unsupported operand values is never implicit.

## O2-I6 — result locus belongs to the operator law

Some ordered expressions collapse a peer fiber to the peer anchor; others preserve the focal sequence anchor.

## O2-I7 — anchor-changing is not enough to make an operation a reducer

FIRST/LAST can land at a coarser peer anchor while remaining ordered expressions outside ToD family continuation.

## O2-I8 — window semantics are neighborhood semantics

Positional and order-value windows are distinct.

## O2-I9 — output ordering is separate

Query `ORDER BY` never supplies inner order meaning.

## O2-I10 — no automatic family standing

Ordered expressions do not gain measure-family identity or continuation law merely by returning governed values.

---

# 27. What this architecture deliberately does not introduce

This design does **not** introduce:

```text
a new ToD ordered-measure ontology
a third primary ToD value operator
a special "three-anchor measure"
a universal tie-policy primitive
a universal reset primitive
a SQL-window clone as Frame-QL semantics
automatic chronology from time dimensions
continuation rights for ordered results
legacy FIRST/LAST family compatibility machinery
```

Each omission is deliberate.

---

# 28. Open questions now narrow enough for implementation evidence

The semantic structure is stable enough that the remaining questions are implementation/product questions rather than foundational gaps.

## O2-Q1 — canonical order representation

What is the smallest resolved representation that can carry:

```text
order expressions
comparison/direction
secondary keys
operator-required uniqueness/tie standing
```

without forcing premature surface syntax?

## O2-Q2 — peer-anchor surface

Can the existing Frame-QL anchor structure express the peer anchor cleanly, or does ordered-expression syntax need an explicit `within`-like construct?

## O2-Q3 — operator descriptors

Should each operator carry one semantic descriptor that declares:

```text
peer-collapsing or focal-preserving
required order strength
selection/neighborhood class
boundary/exception behavior
```

rather than hard-coded planner branches?

## O2-Q4 — standing propagation

How much of order-key / peer-placement support can current Core observe, and where does full R4 standing remain necessary before exact ordered semantics can be claimed?

## O2-Q5 — reusable named ordered expressions

Which current Manifold layer, if any, is the right future authority for a durable governed non-family expression?

These are appropriate questions for CC reconnaissance.

---

# 29. Legacy bonus-feature boundary

Legacy family-founding FIRST/LAST is intentionally outside this design.

After the successor ordered-expression model is implemented and governed, existing bonus behavior can be classified:

```text
unused historical path
    → retire

used only by old fixtures/demos
    → migrate fixture/demo, retire

genuine external compatibility obligation
    → decide whether normalization onto the successor is worth preserving
```

The successor architecture does not pay compatibility rent in advance.

---

# 30. O2 conclusion

The minimal common semantic structure is:

\[
\boxed{
\text{Ordered Expression}
=
\text{Operand}
+
\text{Governed Ordered Domain}
+
\text{Operator Law}
}
\]

with:

\[
\boxed{
\text{Ordered Domain}
=
\text{Sequence Anchor}
+
\text{Peer Anchor}
+
\text{Peer Projection}
+
\text{Governed Order}
+
\text{Domain-Formation Rule}
}
\]

and the operator law determining:

```text
selection / neighborhood semantics
required order strength
result locus
operand-standing behavior
boundary / exceptional cases
meaning-bearing parameters
```

This structure accommodates FIRST, LAST, LAG, LEAD, ranking, cumulative, and rolling operations without turning ordered analytics into measure-family continuation and without importing the legacy Core implementation model into the successor design.
