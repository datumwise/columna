# The Theory of Data in One Afternoon

**The rules you already obey, the world they come from, and the query that falls out.**

*datumwise · v0.13 · 24 August 2026 · role: site on-ramp — The Case / Start Here*

---

**What this is.** A walk, in one sitting, from failures you have personally debugged to the theory that explains them — ending at a question you will ask yourself before we ask it for you. It requires no prior reading. The notation is simplified for the page; the executable examples are machine-checked, and the formal objects are defined in the works linked at the end. Inline notation such as `revenue @ {store, month}` is the theory's naming form, used in prose. Every expression presented as Frame-QL on this page is verified against the shipped parser.

**What this is not.** It is not the theory — that is a formal document with proofs and its own DOI. It is not a statistics lesson; the question of what evidence supports is a second afternoon, and we will point at it exactly once. And it is not a product pitch: the discipline described here needs no product. You can practice it tomorrow with a text file and a stubborn temperament.

---

## 1. Four scars

Most experienced data people carry the same scars. They were acquired independently, in different companies, on different stacks, and they healed into the same folk rules. Start by checking your own.

### The average of averages

Two stores. Store A: 100 orders, \$10,000 of revenue — average order value \$100. Store B: 10 orders, \$3,000 — average order value \$300.

What is the average order value across both stores?

One analyst averages the averages: (100 + 300) / 2 = **\$200**. Another divides total revenue by total orders: 13,000 / 110 = **\$118.18**.

Both numbers came from valid queries. Both will render beautifully on a dashboard. One of them is wrong by 69%, and nothing in a typical toolchain will say so.

You know this one. The folk rule is *never average averages*. You may even know the repair: carry the sums and counts, divide at the end. Hold that thought — the repair is more interesting than the rule.

### The drifting denominator

A stakeholder asks: *what was average revenue per open store yesterday?*

The company had 50 stores open yesterday. The sales table contains rows for 47 of them. Of the three others, two genuinely sold nothing — their zeros are real. One had a feed failure — its number exists in the world and is missing from the warehouse.

Observed revenue totals \$940,000. Three answers now circulate in the wild:

- **\$20,000** — total divided by the 47 stores that happen to have rows. The denominator silently became "stores that appear in this table."
- **\$18,800** — total divided by 50, which quietly treats the feed-failure store's unknown revenue as zero.
- **\$19,183.67** — total divided by the 49 stores whose values are actually known (47 observed, 2 true zeros). Honest, if it is labeled as covering 49 of 50. It rarely is.

The question as asked — all 50 open stores — cannot currently be answered exactly, because one store's revenue is unknown. No query errors. Three plausible numbers, each an answer to a *different* question, all wearing the same label. The folk rules here are *know your population* and *never confuse zero with missing*. Notice the scar contains three kinds of absence: a store that sold nothing (zero, a value); a store whose feed failed (missing, a state); and a store closed for renovation, which does not belong in the denominator at all (ineligible: outside the declared population for this question).

### The sum that means nothing

An inventory table: units on hand, per store, per day. A store holds 100 units on Monday, 100 on Tuesday, 100 on Wednesday.

`SUM(on_hand)` across the three days returns 300.

Three hundred what? The same hundred units were counted three times. The sum executes flawlessly and denotes nothing. Across *stores* on one day, the same SUM is perfectly meaningful. The folk rule: *never sum stock across time*. Averaging it is fine (average daily on-hand: 100). Taking the last value is fine (period-end: 100). Summing is fine along one axis and meaningless along another. The database treats all of these identically.

### The join that manufactures money

Orders join to order lines. The shipping fee lives on the order — \$10, once. After the join, the fee appears on every line: an order with four lines now carries \$40 of shipping into any downstream SUM. The folk rule: *watch your grain after joins*. Most analysts learn it by producing, at least once, a revenue number that exceeded reality — confidently, plausibly, and in production.

### Take stock

Four scars, four folk rules, and one observation worth sitting with:

> **Few of us learned these rules as one curriculum. We derived them from incidents — and practitioners everywhere derived the same ones. Fragments exist in the research literature; as working analysts meet them, they arrive as disconnected folk rules, with no single governed account of identity, location, law, and state standing behind them. Rules that everyone independently rediscovers are usually not rules at all. They are symptoms of a law nobody wrote down where the system could read it.**

## 2. The diagnosis

Look at what the four scars have in common.

In every case, the query executed correctly. The engine did exactly what it was told. The failure was in a piece of **meaning the procedure could not see**:

- what law governs combining averages (a state the display threw away);
- what population a denominator refers to (and which absences are zeros, missing, or outside the declared population);
- along which axes a quantity may be summed at all;
- at what grain a value is actually established, versus merely repeated.

Where did that meaning live? Be honest about the inventory: in the analyst's head. In a wiki page nobody reads at query time. In a metric description field that no engine enforces. In tribal knowledge transferred by code review and incident retro. Everywhere, in other words, except the one place the query could consult it.

SQL is not at fault, exactly. SQL is a language about **tables** — rows, columns, joins, groupings. It is superb at describing procedures over stored data. But *store-day*, *population of open stores*, *additivity along the store axis but not the time axis*, *established at order grain* — none of these are things a table can say about itself. The meaning was always one level above the storage, and we have been encoding it *into* procedures, one careful query at a time, and hoping.

That is the diagnosis, and it is short:

> **The dangerous analytical failure is not the error message. It is the plausible answer to the wrong question — and it happens because analytical meaning was never declared anywhere the system could see it.**

The folk rules are what a community develops when the law is real but unwritten. So the next question is not rhetorical: what would it look like to write the law down?

## 3. The world the rules were protecting

Suppose we try, using the retail world from the scars: stores, days, orders, revenue. What would we have to declare so that a machine could catch every failure in section 1 *before* execution?

Work through it. Each declaration will turn one folk rule into a checkable law.

**First: what exists?** Two different answers. *Orders* exist by occurrence — an order is a point in the world because it happened. *Store-days* exist by declaration — the pair (store 12, yesterday) is a legitimate analytical location whether or not anything was sold there, because the calendar and the store roster say so. Call each of these a **universe**: a set of points plus the law that says when a point exists. The drifting-denominator scar was a query answered against the wrong universe — "rows in the sales table" instead of "declared open store-days." And the store that sold nothing is now a first-class citizen: a point that *exists by law with no bytes behind it*. Existence and observation are now separate facts, which is what the zero/missing/ineligible distinction needed: **eligible and observed** (47 stores), **eligible with a true zero** (2), **eligible but unobserved** (the feed failure), **ineligible** (closed for renovation). Four different situations that a bare table renders as, at best, two.

**Second: where do quantities live?** Group the store-day universe by store and month and you get coarser cells; group by region and quarter, coarser still. Each grouping is a partition of the *same points* — a month literally contains its days; nothing is joined, nothing can fan out, the territory is merely re-tiled with fewer cells. Call a governed partition an **anchor**, written as its coordinates: `{store, day}`, `{store, month}`, `{region, quarter}`. Anchors form a lattice ordered by coarseness, and the join-fan-out scar becomes a statement about it: the shipping fee is *established at* `{order}`; repeating it at `{order_line}` — a finer anchor — does not establish it there, and any SUM over the finer copies is adding a value at an address where it doesn't live.

**Third: what is a quantity?** Not a column. *Revenue* is a quantity with an identity and a law: it originates from order events, and it combines by **sum** — which is why revenue at `{store, day}` can be lawfully rolled to `{store, month}` and onward to `{region, quarter}`, along either axis, in any order, and the answers agree. Call the quantity-with-its-law a **measure family**, and a family at a particular anchor a **measure**: `revenue @ {store, month}` is a complete analytical name — the family, at the address. This is the object the whole afternoon has been walking toward, so say it plainly:

> **An analytical number is not a value. It is a value at a declared location, under a declared law, with a declared account of what exists and what was observed. Strip any of that away and the number can no longer be checked.**

**Fourth: the law is what makes the folk rules checkable.** Watch each scar become a clause:

*The average of averages.* A displayed average has thrown away the information needed to combine it further. For an ordinary average, that sufficient information can be carried as `(sum, count)`; for the aov in this world, it lives in the parents — revenue and orders. The displayed average is terminal for this declared aov family: combine or reduce the information that generates it, not the displayed averages themselves. Averaging two displayed averages asks for information the displays no longer contain. Your repair — carry the sums and counts, or equivalently preserve the parent totals — is the law, obeyed by hand.

*The meaningless sum.* The base inventory family's law is austere: `on_hand` is additive across the store axis and declares **no reduction along time at all**. The quantities you lawfully want across time — average daily on-hand, period-end on-hand — are *different families*, each rooted on the base with its own law and its own state. One everyday phrase, several governed identities: in speech, "on hand" covers a small family of families, and a governed world keeps them distinct because their laws differ. `SUM(on_hand)` across days is an operation that exists in no family at all.

*Derived quantities.* Average order value is a family **derived** from two parents — revenue and orders. This family's declared law says: *re-derive at every anchor*. Under that law there is no edge from `aov @ {store, month}` upward to `aov @ {region, quarter}`; the only route runs through the parents. A different construction is also lawful — a family that carries the pair of parent states and combines those — but that is a different declared law and, in a governed world, a different family. The general lesson is smaller and sharper than *never average averages*: a displayed value carries no general license to combine. It combines only when the family law makes that value sufficient state — a plain sum is the obvious case. Otherwise the carried state combines, as the law says. And which law a family lives under is **declared**, not assumed. In this declared world, the mean-of-means is not a mistake you must remember to avoid. The edge it would need does not exist.

*Rooted families.* One more, because it completes the picture: *maximum monthly revenue* is a family whose root is `revenue @ {store, month}` — it begins mid-lattice. It can be lawfully maxed upward to `{region, quarter}`. It can never be recovered from quarterly revenue totals, because summation destroyed the monthly detail on the way up. Summing past a grain is a one-way door in this sense: the detail discarded by the summarized value cannot be recovered from that value alone. Where a family is rooted determines what remains knowable above it. Any veteran of "just derive it from the rollup" arguments has met this law without its name.

That is the whole apparatus a cold reader needs: universes with existence laws, anchors as partitions in a lattice, measure families with laws and roots, state versus display, absence typed. Not one item is exotic. Every item was already present in your folk rules — as a shadow.

## 4. Read a Manifold

Now write it down. Below is the retail world, declared. The notation is simplified for this page — the real artifact is machine-checked, versioned, and richer — but nothing essential is hidden:

```text
manifold: retail                                 # a declared analytical world

universe order_events:
  point: order                                   # exists by occurrence
universe store_days:
  point: (store, calendar.day)                   # exists by declaration
  eligibility: store_calendar.open               # closed store-days are outside this eligible population

dimension store:  store → region
dimension time:   day → month → quarter          # each level partitions the one below

family revenue:
  root: sum of order.amount, established at {store, day}
  law:  additive; reduces by sum along store and time axes
  state: sum

family orders:
  root: count of order, established at {store, day}
  law:  additive; reduces by count-sum
  state: count

family aov:
  parents: revenue, orders
  law: aov = revenue / orders, re-derived at each anchor    # this family's declared law
       no reduction edges of its own              # combining displayed aov is unwritable
                                                  # (a state-carrying variant would be a
                                                  #  different declared family)

family on_hand:
  root: units at {store, day}
  law: additive across the store axis only
       no reduction along the time axis           # summing stock across days exists nowhere

family avg_daily_on_hand:
  root: on_hand @ {store, day}
  law: reduces by average along time; state (sum, count)

family period_end_on_hand:
  root: on_hand @ {store, day}
  law: reduces by last along time; state (value, day key)

family max_monthly_revenue:
  root: revenue @ {store, month}                  # begins mid-lattice
  law: reduces by max
       not derivable from coarser revenue         # the information is already gone
```

Read it twice. Notice three things.

Every scar from section 1 now has a **declared counterpart**. The drifting denominator is the `store_days` universe with its eligibility law. The average of averages is `aov`'s missing reduction edges. The meaningless sum is `on_hand`'s per-axis law. The manufactured shipping money is `established at` doing its quiet work. What used to live in your head, defended in meetings, and re-litigated at every reorg, is thirty lines that a machine can hold you to.

Second: this file is **generative**. It does not list what has been computed; it declares what lawfully *exists* — every family, at every admissible anchor, whether or not anyone has materialized it yet. `revenue @ {region, quarter}` exists by law in this world the way the quiet store-day exists by law: an address with, so far, no bytes behind it.

Third — and this is where the afternoon has been heading — you have just read a **Manifold**: a declared analytical world, containing its own account of existence, location, law, and identity. A Manifold is a **declaration, not merely a description** — the world's constitution, not its inventory. And its declarations stand trial: they must hold against current realization and support before anything may be served, as section 6 shows. Which raises a question you are now equipped to feel the full weight of:

## 5. How do you query *this*?

Try your reflexes. `SELECT ... FROM` — from *what*? There are no tables here. There are universes, anchors, and families. You could of course go find the physical tables underneath and write the joins and group-bys yourself — but then you are back in section 1, hand-encoding the law into a procedure and hoping, with the Manifold reduced to documentation. The entire point was to make the law *binding*.

So sit with the question honestly for a moment: in a world where meaning is declared, what is a query?

Look at the Manifold again. Every legitimate analytical object in this world already has a **name**: a family, at an anchor. `revenue @ {store, month}`. The thing you want *is already individuated by the declarations*. You do not need to describe how to manufacture it. You need only to *ask for it by name*:

```frameql
SELECT revenue AT {store, month}
```

That is a complete query in **Frame-QL**. Notice what it does not contain. It is not an abbreviation of a SQL statement. It has no joins: the Manifold declares the analytical geometry, and the system combines that declared meaning with its private realization to choose a lawful physical plan. No GROUP BY clause: the anchor names the requested grouping; planning determines how that grouping is physically realized. No physical recipe: the family's law determines what computation is lawful; planning determines how to realize it. The request names a governed object; the system, which knows the law, determines whether and how the object can be manufactured. **The result is the query.**

One more, to see the address system flex:

```frameql
SELECT avg(revenue @ {order}) AT {region, quarter}
```

Average *order-level* revenue, presented at region-quarter. The expression names its own source grain — `revenue @ {order}` — inside the request. Try to say that in SQL and you will produce a subquery whose correctness depends entirely on invisible grain knowledge; here the grain is part of the *name*. Two orders-of-averaging that a dashboard tool renders identically are, in this language, two different addresses — which is the average-of-averages scar, made unwritable.

## 6. Ask, and watch the world answer

Once an analytical world is declared, a governed system can **adjudicate** a request before executing it. The four cases below illustrate the four serving moods used here: Serve, Disclose, Clarify, and Refuse. A production serving system also establishes current support, certification, and authorization before anything is served; Analytical Governance, linked at the end, governs that larger passage, and defines a fifth outcome, **Escalate**, for cases that require new governance authority, evidence, definition, or qualified review beyond what the requester can settle within the governed alternatives already available. Ask the retail Manifold four questions and watch:

**Ask:** `SELECT revenue AT {region, quarter}` → **Serve.** The family reduces by sum; `{store, day}` refines `{region, quarter}` through the declared hierarchies; every input is admitted. The number returns — and it returns *entitled*, because every step from root to result was lawful and checked.

**Ask:** `SELECT max(revenue) AT {region, month}` → **Clarify.** Three governed meanings remain: maximum revenue resolved by *day*, by *store*, or by *order* within each region-month. They are different analytical quantities with different values. The system does not pick one on the requester's behalf. It returns the distinction and waits — because choosing among unresolved lawful meanings is precisely the failure this whole apparatus exists to prevent.

**Ask:** `SELECT sum(on_hand) AT {store, month}` → **Refuse** — with a reason: *the on_hand family declares no reduction along the time axis; governed neighbors that answer lawfully: `avg_daily_on_hand @ {store, month}`, `period_end_on_hand @ {store, month}`.* The query that returned a meaningless 300 in section 1 does not return a wrong number here. It returns the law it broke and the questions that are well-posed nearby. Read that mood carefully: it is a verdict most conventional stacks do not express as governed refusal.

> **Refusal is not a failure state. A system that can refuse is a system whose answers mean something — because you finally know what it would *not* have told you.**

**Ask:** *average revenue per open store, yesterday* → the exact request, over all 50 declared open store-days, is **not currently servable**: forty-nine points are supported; one is eligible but unobserved — the feed failure — and the system will not pretend otherwise. It reports that finding, and it identifies the *separately governed* supported-population measure as a lawful neighbor. Select that alternative — or let policy pre-establish it for exactly this situation — and the verdict is **Disclose**: served, with conditions attached: *\$19,183.67 over 49 of 50 eligible store-days; one store-day unobserved.* Nothing was silently substituted; the request changed hands in the open, and the number travels with its own coverage. The three anonymous figures from section 1, each quietly answering a different question, are replaced by one number that says exactly which question it answers — and one honest statement about the question it cannot yet answer.

Serve. Clarify. Refuse. Disclose. In these four cases, the distinctions follow from the declared meaning, current support, and the requests themselves — not from an analyst guessing what the requester probably meant. The division of powers stands: the Manifold supplies the declared meaning; current support and governance determine what may be served now. **Declaration is not certification** — the constitution says what would count as lawful; the world's present condition decides what presently qualifies. This is the sentence the whole afternoon compresses into:

> **A computable answer is not automatically an answer entitled to be served. Computation was never the hard part. Entitlement was — and entitlement requires declared meaning.**

## 7. Two readers, and what changes

**For the humans.** Arguments end differently in a declared world. "Which denominator?" stops being a meeting and becomes a line in the Manifold — visible, versioned, and changeable by a governed edit rather than by whoever wrote the last query. The folk rules no longer have to be remembered at query time: the world you work in has no edge where the mean-of-means can stand. The discipline needs no software to begin: declare your populations, write down your families' laws, name your anchors, refuse out loud what your data cannot answer. A text file and a stubborn temperament. Everything else is enforcement.

**For the machines.** Reread the Manifold one last time, and now imagine the reader is not you but an AI agent your company has pointed at its data. Against a raw warehouse, that agent reads `information_schema`, learns *structure*, and guesses *meaning* — it is a section-1 analyst with perfect syntax, infinite confidence, and no scars. Against a Manifold, it reads the **governed analytical question space**: what exists, what every name means, and which operations are lawful. Current adjudication still determines which lawful requests may be served now. It can propose requests in the language of governed objects, and the world can still tell it *no*. Interpretation stays useful; interpretation never becomes authority. When the consumer of your numbers is increasingly a machine that acts on them, that boundary is the difference between an agent with a map and an agent with credentials.

**What this afternoon did not cover — deliberately.** Everything above governs the *data* question: what exists, what is lawful, what a number is. It says nothing about the *evidence* question: when does a lawful number support a claim about the world beyond the data — a forecast, a comparison, a cause? That crossing has its own laws, its own failure catalog, and its own afternoon; the framework is called the **Statistical Bridge**, and the honest summary is that everything here is its prerequisite and none of it is a substitute. One discipline at a time.

## Where to go from here

**Read** — the corpus is small and each piece knows its job:

- *A Primer on the Theory of Data Applied* — three familiar rules, decomposed. The scars-first companion to this walk. (DOI: 10.5281/zenodo.21960380)
- *A Primer on the Theory of Data* — the vocabulary, carefully, in dependency order. (DOI: 10.5281/zenodo.22018549)
- *The Theory of Data* — the foundation itself, with the proofs. (DOI: 10.5281/zenodo.22013410)
- *Analytical Governance* — from a human question to an answer entitled to be served: the architecture around everything above. (DOI: 10.5281/zenodo.22046037)
- *The Statistical Bridge* — the second afternoon: from governed data to licensed claims. (DOI: 10.5281/zenodo.21979821)

**Run** — Columna is the open-source system where this afternoon executes: real Manifolds, real Frame-QL, and the four verdicts returned by a machine rather than illustrated on a page. The theory does not depend on it; it exists to prove the theory runs.

**Challenge** — take a familiar folk rule about analytical data: grain, aggregation, population, derivation, absence, identity, or state. If it cannot be explained through governed existence, location, law, state, or lineage, you may have found a boundary of the theory. We keep a list.

**Build** — the declarations, the language, and the engine are open. The world described here gets built the way it gets queried: one declared meaning at a time.

---

You already knew the rules. Now you have seen the world they were protecting — and the question it leaves you with is the one this page cannot answer for you: *what does your world look like, written down?*
---

## Revision note

**Version 0.13 — 24 August 2026.** Current-pointer maintenance revision of the canonical v0.12 teaching artifact. The Analytical Governance reading pointer is advanced from Version 1.0 to the current Version 1.1 (DOI 10.5281/zenodo.22046037). No teaching prose, examples, Frame-QL expressions, analytical claims, or worked results are changed.
