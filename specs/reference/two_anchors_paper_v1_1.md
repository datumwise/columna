# The Two Anchors of a Measure: The Input and Output Grains Common Analytics Leaves Uncaptured

**Huayin Wang** · 2026 · License: CC BY 4.0
*Companion to* The Silent Failure Atlas *(Zenodo v1.3, DOI: 10.5281/zenodo.20762839).*

---

## Abstract

A stored analytical measure — an average, a rate, an index, even a minimum — is conventionally
understood to live at one grain: its *output* grain, "for the North region in 2024." We show this is
half the story. A large and common class of measures is governed by **two** grains: the output anchor,
and a usually-unspoken **input anchor** — the grain the measure was reduced over. The input anchor is
substantive (it is why "average order value" has three different values over one small dataset), yet
the field has no systematic way to capture it, reason about it, or use it. We give a criterion for
exactly when it is live, show that the average and the weighted average hide it for two *distinct*
structural reasons, and identify a class of measures — including MIN and MAX — that pass every
additivity check yet remain uninterpretable without it. The only mechanism the field uses today is the
measure's *name*; conventions like ARPU vs ARPPU are the field independently discovering the anchor and
patching it in a medium that can neither record it reliably nor check it. We close by deriving — not
asserting — the properties any structured account of the two anchors must have.

---

## 1. A number that is not one number

Here is a region's sales for a quarter, in full:

| order | customer | lines (each a sale) | order total |
|---|---|---|---|
| O1 | C1 | $100, $20 | $120 |
| O2 | C1 | $10 | $10 |
| O3 | C2 | $40, $40, $40 | $120 |

Total revenue is $250. Now answer one ordinary question: **what is the average order value?**

- Averaged over **orders** (3 of them): $250 / 3 = **$83.33**.
- Averaged over **lines** (6 of them): $250 / 6 = **$41.67**.
- Averaged over **customers** (2 of them): $250 / 2 = **$125.00**.

Three different numbers. Same region, same quarter, same phrase "average order value," same revenue
in the numerator. The only thing that changed is *what we divided by* — the grain of the unit we
averaged over. And note the trap in plain sight: a table stored at the line grain, asked for "average
order value," will silently return $41.67 — the average *line* value — under a column named for
orders.

Nothing in the output records which of the three we computed. If we materialize one of these into a
column called `avg_order_value` at the grain *(region, quarter)*, and discard the rows, the column's
name, its data type, its owner, its refresh schedule, and its lineage to the table it came from are
all preserved — and the one fact that picks $83.33 from $41.67 from $125.00 is gone, because that
fact was never a property of the column. It was a property of the *act of averaging*.

That missing fact is not an oversight; it is a **coordinate** the measure carries and the practice has
no place to put. This paper shows that common analytical measures — average, ratio, index, weighted
average, distinct count, extremum — are governed by **two** grains, not one: the familiar **output
anchor** (the grain the result is reported at) and a second, usually unspoken **input anchor** (the
grain it was reduced over). Both are substantive — they change the value or what it means — and neither
has a systematic home in how we record, reason about, and serve measures. We make the two anchors
precise, give the criterion for when the input anchor is live, show the output anchor is itself only
loosely pinned, and argue the field has been managing both through a single unreliable channel — the
measure's name.

The individual pitfalls below — average-of-averages, mis-weighted means, re-aggregated rates — are
known to every working analyst as review-checklist folklore, and the additive/semi-additive
distinction is textbook dimensional modeling. Our contribution is not to discover them but to show
they are one phenomenon — two coordinates governing the measure — and that there is no systematic,
structured way to **capture** those coordinates, **reason** with them, or **use** them.

## 2. Naming the parts

We now give the small vocabulary the rest of the paper needs. Everything in it was already visible in
§1; we are only labeling it.

**Grain and anchor.** Our example has a stack of grains: a *line* is finer than an *order*, which
(grouped by customer) is finer than a *customer*, which is finer than the whole *(region, quarter)*.
These grains form a lattice ordered by "finer than." A grain, used as the level at which a measure
sits, we call an **anchor**. The coarsest point — the fully collapsed *(region, quarter)* — is the
**output anchor**, written `o`. The grain we average/count/extremize *over* is the **input anchor**,
written `i`. Both are anchors, and the paper's claim is that a measure needs *both* stated — and that
the practice states the output anchor only loosely and the input anchor almost never.

**Measure and family.** A named quantity that can appear at several anchors — *revenue* at the line,
order, customer, or region level — is a **measure family**. A family member at a specific anchor is a
**column**, written `m@a`. A bare family name `m` is not a column; revenue "as such" has no value
until you say revenue *at what grain*. The finest anchor at which a family is natively recorded is its
**root** (here, revenue at the line grain).

**Reducer.** Moving a measure from a finer anchor to a coarser one is a **reducer**, written
`ρ(m@i)@o`. Revenue's reducer is SUM; the minimum balance's is MIN. The signature has *two* anchors,
`i` and `o`, and much of the paper is about when the first one matters.

**Path-independence.** Revenue has a convenient property: summing lines to orders and then to the
region gives the same total as summing lines straight to the region. The result at `o` does not depend
on the route — or on the intermediate `i`. Call a reducer with this property **path-independent** (the
term of art is *confluent*; we use the plainer word). When a reducer is path-independent, we may
simply write `revenue@region`, because the input anchor has dropped out: the value is a function of
`o` alone. *This is the entire reason the one-grain picture usually works.*

## 3. When the input anchor survives

The criterion is now a single line.

> **Anchor-arity.** An aggregate's grain-arity is a property of the **(measure, reducer)** pair. If the
> reducer is path-independent for the measure, the input anchor `i` collapses and the result is a
> one-grain quantity `m@o`. If it is *not* path-independent, `i` is a free parameter and the result is
> a genuine two-grain operator `ρ(m@i)@o` whose value depends on both.

One direction is just the definition of path-independence. The other is what §1 showed by example: COUNT
is not path-independent — counting lines and adding up is not the same as counting orders — so any
operator whose value flows through a COUNT inherits a live `i`. The average is exactly such an operator,
which is the subject of §4.

This is a generalization of classical **summarizability** [1,2], which asks whether a *sum* may be
validly rolled up along a dimension. That is the path-independence question for one reducer, SUM. The
input-anchor view asks the more general question for *any* operator — *on which input grain does this
value depend?* — and, crucially, extends past the additive measures the older theory set aside.

## 4. The average and the weighted average: two grains, two reasons

The two most common two-grain measures are two-grain for *different* reasons. Both must be understood;
treating them as one case hides the more dangerous one.

**The average — the count is the culprit.** Write the average of `m`, reported at `o`, taken over units
`i`:

> `avg(m)@o over i  =  ( revenue@o )  /  ( count(*@i)@o )`

In our example the numerator `revenue@o` is $250 *no matter what* — SUM is path-independent, so the
numerator's input grain collapses and it contributes nothing to the ambiguity. The entire two-grain-ness
sits in the denominator: `count(*@i)@o` is "how many `i`-things are in `o`," and that count is 3, 6, or 2
depending on whether `i` is order, line, or customer. So:

> **The average is two-grain because its denominator counts, and counting is not path-independent. Its
> numerator is innocent.** The hidden parameter has a plain-English name: *average over what?*

**The weighted average — the product is the culprit.** Now a different shape. Take two product lines in
an order:

| line | unit price | quantity |
|---|---|---|
| A | $10 | 2 |
| B | $5 | 10 |

The quantity-weighted average price is `sum(price·quantity) / sum(quantity)`, formed at the line grain:
`(10·2 + 5·10)/(2+10) = 70/12 = $5.83`. The cheap line dominates because it sells more, exactly as it should.

Here is the number an analyst actually produces by mistake: the plain average of the two prices,
`(10 + 5)/2 = $7.50`. That is the price averaged over the two *price rows*; the correct $5.83 averages over the
twelve *units sold*. Same measure, same output grain, off by $1.67 — a different input grain, exactly as in §1.

Now the structural twist. *Both* halves of the correct formula are SUMs — both path-independent — so §3 says each
is one-grain, and yet the weighted average is unmistakably two-grain. The reason is the numerator: the product
`price·quantity` must be formed **at the line grain, before the reduction**, because it does not survive being
pushed above it. Given only the reduced factors — the average price $7.50 and the total quantity 12 — *no formula
recovers $5.83*; the per-line products that summed to 70 are gone. So here the input grain survives not through a
non-path-independent *reducer* (as in the average, whose denominator counts) but through a **non-linear operation
performed below the reduction** (the product). Two different measures, two different reasons the input grain lives —
which is why both must be surfaced, not folded into one rule.

**One law for both.** These are two instances of a single statement:

> **Commutation law.** If an operation `g` is applied below a reduction and `g` does not commute with that
> reduction, the pre-reduction grain `i` is a free parameter of the result.

The average is the instance `g = identity`, reducer = COUNT (not path-independent). The weighted average is
`g = product`, reducer = SUM (path-independent reducer, non-linear `g`). Ratios, rates, percentages, shares,
and indices are further instances — each a quotient or non-linear combination of quantities reduced from `i`.
The law thus covers the whole "compute-something-per-row-then-aggregate" family, which is where non-additive
analytics overwhelmingly lives.

A consequence any analyst has met: two correctly computed weighted averages, bearing identical names, types,
definitions, and lineage, can disagree — and no catalogue field explains why, because the discriminating
grain `i` was never recorded. People reach for "there must be a bug." There is no bug. There are two
different `i` wearing one name.

## 5. The fossil that passes every safety check: MIN and MAX

So far the troublemakers were *non-additive*, and a seasoned modeler might reach for the usual reflex —
flag the non-additive measures, trust the rest. That reflex fails, and the cleanest counterexample is the
humble minimum.

Take one customer with two accounts, balances over three days:

| day | account A1 | account A2 | customer total |
|---|---|---|---|
| 1 | $5 | $1000 | $1005 |
| 2 | $800 | $60 | $860 |
| 3 | $400 | $50 | $450 |

**What was this customer's minimum balance this week?**

- Minimum over **account-days** (the finest atoms): the lowest single figure in the grid, **$5**.
- Minimum over **customer-day totals**: the lowest daily total, **$450**.

$5 and $450, same customer, same week, same family "minimum balance," same output grain. And here is the
twist: **MIN is path-independent** — the minimum of per-group minimums is the overall minimum — so it sails
through every additivity/summarizability check. By the §3 criterion its input grain *collapses for
re-aggregation*. Yet the stored number is meaningless without knowing `i`, because "minimum" is a minimum
*of something*, and the something is grained. Re-aggregable, and uninterpretable.

So path-independence is not the whole story. There is a **second, independent property**: whether a stored
value carries its own meaning, or *presupposes* the input grain it ranged over.

- A value is **self-interpreting** if its meaning is fixed by (family, output grain) alone. `revenue@region`
  means "total revenue in the region" — no `i` needed. Additive measures are self-interpreting.
- A value is **grain-presupposing** if its meaning quantifies over `i`-grain *entities*. `min_balance@week`
  means "the smallest of the `{i}`-grain balances," and is incomplete without `i`. Selection (MIN, MAX),
  counting (COUNT), and the order statistics are entity-referential, hence grain-presupposing.

Crossing the two properties gives four cells:

**Figure 1 — The four cells of materialization.** Lossless storage lives in exactly one; current
practice treats all four as if they were that one.

| reducer ＼ value | self-interpreting | grain-presupposing |
|---|---|---|
| **path-independent** | **SUM, additive — lossless ✓** | MIN, MAX, COUNT — *re-aggregable but uninterpretable* |
| **not path-independent** | *(empty — see below)* | AVG, ratio, rate, index, percentile — *neither* |

**Lossless materialization lives in exactly one cell.** Storing a value and discarding its source loses no
analytically relevant information — every coarser view is regenerable from the stored value *and* the value
is interpretable on its own — **iff** the reducer is path-independent **and** the value is self-interpreting:
the SUM cell. Sketch: path-independence lets any coarser view be re-derived from the stored value by applying
the reducer again, so no source is needed; self-interpretation means the value's meaning needs no `i`. Remove
either property and it fails — MIN/MAX/COUNT re-aggregate but cannot be read without `i`; AVG/ratio neither
re-aggregate nor self-interpret. (We claim only losslessness *for coarsening*; no stored aggregate, SUM
included, can be disaggregated to a finer grain.)

**Why the fourth cell is empty.** A non-path-independent operator that is nonetheless self-interpreting would
have to vary with `i` while referring to no `i`-grained entity. But the two sources of non-path-independence
from §4 are each entity-referential: a non-path-independent reducer (count, distinct, order statistic) selects
or counts `i`-entities, and a non-linear sub-reduction operation (the weighted-average product) is formed over
`i`-rows. Either way the result refers to the `i`-grain population — i.e. it is grain-presupposing. So
non-path-independence appears to *entail* grain-presupposition, and the cell is empty by construction, not by
accident. (We state this as an argued conjecture; a proof would need a precise account of "entity-referential.")

The reading for practice: prevailing metadata treats **all four cells as if they were the SUM cell** —
self-describing, recoverable stored numbers. That is true for the additive measures the practice grew up
around, and false for everything else, *including the textbook-simple MIN and MAX.*

## 6. The output anchor is under-determined, too

The input anchor took three sections because it is the neglected, structurally rich one — usually
absent, and live or not depending on the operator. The output anchor is the *other* coordinate, and
its problem is lighter but real: it is not absent, it is **loosely pinned**. Both must be stated to
specify a measure; they are simply not symmetric in how badly the practice mishandles them. Two
reasons the output anchor is looser than it looks, and naming them completes the picture.

**The table grain is only an upper bound.** A column stored in a daily table is not thereby a daily
figure. Broadcast and denormalization routinely repeat a coarser value across finer rows — a
month-to-date total copied onto every day of the month, a customer-level score attached to each
transaction. The host grain tells you the value is *no finer than* the row; it does not tell you it is
*at* the row. So the output anchor is bounded by the table, not fixed by it.

**"Per X" conflates the two anchor roles.** The very phrase the field reaches for to pin a grain is ambiguous
about *which* grain. "Average order value **per customer**" can mean `i = customer` — total ÷ number of
customers, *one number* — or `o = customer` — each customer's own average, *a value apiece*. The same three
words name an input choice or an output breakdown, resolved only by context. The preposition that is supposed
to specify the grain does not say whether it is specifying the input or the output one.

So both coordinates are loose in practice: the input anchor is usually silent, and the output anchor is only
upper-bounded by the table and ambiguously gestured at by language. A *fully specified* measure states both,
unambiguously — and almost none do.

## 7. Capture, process, use — and the limits of the name

State a measure's family, its input anchor, its output anchor, and its reducer, and three things become
possible that are not possible today.

- **Capture.** The measure is recorded unambiguously: `avg(order_value)` over `i = line` at `o = (region,
  quarter)` is a different, distinguishable object from the same family over `i = customer`. The fork that
  produced $41.67 vs $125.00 in §1 is now two named things, not one ambiguous one.
- **Process.** With the anchors explicit you can *compute over them*: decide realizability (does a path exist
  from `i` to `o`?), check the consistency law (do the family's members agree under the reducer?), and apply
  the §3 criterion to know whether `i` is even live — so the system knows when to bind silently and when to
  ask. None of this is possible without the anchors as first-class data.
- **Use.** At serve time the measure is bound to the intended anchors, and when the input anchor is contested
  (§3–§5 say exactly when), it can be surfaced rather than guessed.

Strip the anchors and all three fail — which is the situation today. The natural objection is to *recover* the
anchors after the fact. For the output anchor you can sometimes refute a too-coarse guess; for the input
anchor you generally cannot, and §4 is the reason: **distinct input anchors produce distinct values under one
name, so the stored value does not determine the anchor that produced it.** The map from anchor to value is
many-to-one; it has no inverse. (A surviving companion — a stored count beside an average — sometimes permits
partial recovery, but unreliably and not in general.) The practical reading is flat: the anchors must be fixed
when the measure is made, because the value does not carry them.

**The one mechanism the field has is the name — and it knows the anchors matter, because it puts them there.**
ARPU vs ARPPU — average revenue *per user* vs *per paying user* — are two standard acronyms differing in
exactly the input anchor's denominator population. Gross vs net, DAU vs MAU, blended vs paid CAC are the same
move. These name-forks exist because a single name with an implicit anchor produced silent disagreements
between teams, and the fix the field reached for was to **fork the name and bake the anchor into the metric's
identity.** That is the field independently discovering that the anchor is real and substantive — and patching
it lexically.

But the name is the wrong medium, and it fails at each of the three verbs:

- *Capture* through the name is partial and unverified. `avg_order_value` asserts `i = order` — over data that,
  in §1, has no order entity at all. The name carries an *intended* anchor; the value carries an *actual* one;
  they can disagree with nothing to flag it.
- *Process* over a name is impossible. You cannot run a realizability or consistency check against a string,
  and "per_X" is itself role-ambiguous (§6). There is no standard, no closed vocabulary, no grammar to compute
  over — only convention, and convention varies by team.
- *Use* inherits both failures. An agent or query that trusts the name binds whatever the name asserted,
  correct or not, with no way to verify.

So the name is **folk-metadata**: the field's correct intuition that the anchors must be recorded, implemented
in the one channel that can neither record them reliably nor check them at all.

## 8. Two ways to hold an anchor

There are two ways to hold a measure's anchors. The incumbent way attaches them to the value as *text* —
names, descriptions, tags — and trusts a reader, human or model, to recover the intent. The alternative makes
them part of the measure's *structure* — declared, typed, computed-with. The contrast is not a matter of
taste; three properties separate the two, and each is *earned* by the sections above, not asserted.

- **Explicit beats implicit — because the value does not determine its own anchors.** §4's non-invertibility
  is the proof: if the value carried the anchor, implicit recording would suffice; it does not, so the anchor
  must be stated, not inferred. This is not a style preference; it is forced by the many-to-one map.
- **Structured beats unstructured-without-even-a-convention — because the medium, not the reader, is the
  defect.** The name channel is unstandardized and role-ambiguous (`per_X`, §6); a perfectly accurate reader
  of a misleading name is confidently wrong. Better readers — better models — do not repair a medium that
  cannot express the distinction. The defect is in what the name *can carry*, not in who reads it.
- **Verifiable beats guessed — because a structured anchor can be checked and a named one cannot.**
  Realizability, the consistency law, and the §3 anchor-arity criterion are all decidable over *declared*
  anchors. A name asserting "per order" against data with no order entity is not checkable at all — it can
  only be believed.

**Scope, stated honestly.** This argues for structured capture *wherever the anchors are substantive* — which
§3–§5 characterize precisely: the non-path-independent and grain-presupposing operators. Where the operator is
additive and self-interpreting (the SUM cell), the anchors are immaterial and the name suffices. The claim is
not that everything must be structured — only that a large, common, *characterized* class must be, and that
this class is exactly the one current practice handles worst.

We name no system here. The contribution is the gap and the properties any adequate filling of it must have:
explicit, structured, verifiable capture of two anchors that common measures carry and current practice records
in a name. Whether those properties are met by a semantic layer, a metric store, or a new kind of object is a
separate question; the necessary conditions are the same.

The same logic extends from how a measure is *defined* to how a system *discloses* the anchor it chose. A
system that must surface its input-anchor choice in prose faces a false binary: stay silent (and risk the
silent error this paper is about) or disclose (and bury the reader in caveats, most of them about anchors that,
being path-independent, do not matter). Prose has no field for "and this is immaterial." A structured
disclosure — the chosen anchors plus a materiality flag derivable from path-independence — dissolves the
binary: the producer can disclose every choice and the consumer can filter to the material ones, retaining the
rest for audit. Completeness becomes filterable rather than punishable, and which disclosures matter becomes a
checkable property rather than a matter of the producer's restraint. The structured-beats-unstructured argument
of this section is thus not only about the metric's definition; it is about every place an anchor choice is
communicated.

## 9. Related work

**Summarizability** [1,2,3,4] formalized when *additive* roll-up is valid along a dimension — the
path-independence question for SUM. The two-anchor view generalizes from validity-of-summation to
grain-dependence-of-any-operator, and adds the orthogonal grain-interpretability axis, which places MIN/MAX
(valid to roll up, yet uninterpretable when stored) outside the older theory's reach.

**Dimensional modeling** [5] gives the additive/semi-additive/non-additive trichotomy — the practitioner form
of path-independence, restricted to SUM and period-end cases. The two-axis taxonomy subsumes it and expresses
what the trichotomy cannot: that MIN and MAX are path-independent yet grain-presupposing.

**Silent-failure taxonomy** [6] catalogues the downstream errors the two anchors produce when left implicit;
the extremum/count grain-presupposition of §5 is filed there as a named mode (F1.11). The question of *when*
an anchor can be reconstructed after materialization — a recovery theory, gestured at by §7's non-invertibility
remark — is left to companion work; this paper needs only that the value does not, in general, carry it.

## 10. Scope, limitations, and companion work

This paper is *operator-level*: what one reduction does to one measure, and what recording it requires. Three
companion claims are held out deliberately. (i) A *schema-level* closure condition — every column either a
path-independent family generator pinned by its root, or a typed expression-graph terminating on such
generators and on declared external atoms — standing to the relational normal forms as a theory of *derivation*
integrity stands to one of *storage* integrity. (ii) A *two-strata* partition of analytical failure into a
certifiable processing-grammar stratum and a disclose-only inference stratum, of which the anchor account is a
grammar-stratum mechanism. (iii) A *recovery theory* and the automated authoring built on it — when the
anchors of an already-materialized measure can be reconstructed from data and metadata, and by what procedure —
for which this paper supplies only the negative premise (the value alone does not determine them). A
higher-risk sub-claim — that temporal patterns (as-of, effective dating, restatement, semi-additivity over
time) are not a separate mechanism but the same anchor account with time as one lattice dimension — is deferred
to the schema work, where its decisive test is whether the temporal failure family *dissolves* into the general
theory rather than surviving as a special case.

Limitations: the lattice idealizes real grain structures that are sometimes not lattices; the lossless-cell
characterization (§5) is a sketch, not a proof; and the emptiness of the fourth cell is argued, not proved.

## References

[1] H.-J. Lenz, A. Shoshani. *Summarizability in OLAP and Statistical Data Bases.* SSDBM, 1997.
[2] J. Horner, I.-Y. Song. *A Taxonomy of Inaccurate Summaries and Their Management in OLAP Systems.* ER, 2005.
[3] J.-N. Mazón, J. Lechtenbörger, J. Trujillo. *A survey on summarizability issues in multidimensional modeling.* DKE 68(12), 2009.
[4] M. Hachicha, J. Darmont. *Summarizability Issues in Multidimensional Models: A Survey.* 2013.
[5] R. Kimball, M. Ross. *The Data Warehouse Toolkit*, 3rd ed. Wiley, 2013.
[6] H. Wang. *The Silent Failure Atlas: A Taxonomy of Silent Analytical Failures in Data Analysis.* Zenodo v1.3, 2026. DOI: 10.5281/zenodo.20762839. (The MIN/MAX result of §5 is filed there as mode F1.11.)

---
*Version 1.1 (adds a structured-disclosure paragraph to §8; otherwise identical to v1.0).*

*Cite as: Huayin Wang (2026). The Two Anchors of a Measure: The Input and Output Grains Common
Analytics Leaves Uncaptured. Companion to* The Silent Failure Atlas *(Zenodo v1.3, DOI:
10.5281/zenodo.20762839). [DOI assigned on publication.]*

*Contributions: (i) the two-anchor account of common measures, with the path-independence criterion for
when the input anchor is live; (ii) the average/weighted-average two-mechanism decomposition and the
commutation law unifying them; (iii) the path-independence × grain-interpretability taxonomy and its
single-lossless-cell characterization (sketch); (iv) the capture/process/use framing and the derived
necessary conditions for any structured account. Prior aggregation hazards are cited as folklore being
unified, not as new discoveries. Open: the lossless-cell characterization and the empty fourth cell are
argued, not proved.*
