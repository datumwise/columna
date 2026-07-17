# WP · FrameQL — the envelope grammar (0.9.0). Deliverable 1: THE GRAMMAR SPEC (proposals-first)

_Status: **PROPOSAL, for Huayin's ratification before any code.** Ruled: "We have to get the Query
Language right — we can't ship in this state. The shipped `@`-fragment is not the language; the
envelope is, and it ships before launch as 0.9.0." This document proposes exact grammar text. Nothing
here is built until it is ruled. Every `[PROPOSE → RULE]` tag marks a point where I have chosen a
default and Huayin rules on sight._

---

## 0 · What ships, and why this comes first

The shipped surface is `name: expr @ anchor` — one output anchor spelled by a trailing `@`, one series
per column, no `WHERE`/`HAVING`/`ORDER BY`/`LIMIT`. That is **a fragment**, not the language. The
envelope is the language: a statement with an explicit **`AT {anchor}`** output frame, multiple
juxtaposed series, filtering and shaping clauses, macro bindings, and a first-class `EXPLAIN`. It
ships as **0.9.0 before launch**. This spec is deliverable 1 because the grammar is the contract every
later increment (parser → planner → sugars → EXPLAIN → surface migration → manuals convergence)
writes against; ruling it wrong once costs all of them.

**The one collision, ruled.** Two things currently spell with `@`:
- the shipped **outer** `@` = the **output** anchor (`aov @ cal.month`);
- the shipped **inner** `@` = the **input** anchor of an inline reduction (`avg(aov@day)`, already
  `ast.MatMult` in the planner — the input-anchor pin).

Huayin ruled the **manual's semantics win**: **`@` is the INPUT-anchor marker, universally.** The
output anchor leaves the trailing `@` and becomes the statement's **`AT {anchor}`** clause. After this
WP there is exactly one meaning for `@` — the grain a series reads its input at — and exactly one place
the output grain is named — `AT`. This is the whole reason the fragment cannot ship as the language:
its two `@`s mean opposite things.

---

## 1 · The statement form

```
[EXPLAIN]
[FROM <manifold>]
SELECT <series> [AS <alias>] [, <series> [AS <alias>]]…
AT { <anchor> }
[WHERE   <per-series predicate> [AND …]]
[HAVING  <output-frame predicate> [AND …]]
[ORDER BY <output-frame column> [ASC|DESC] [, …]]
[LIMIT <n> [PER { <anchor coordinates> }]]
```

- **`ON` is ABSENT** — dead per §2c. A population is never named in a query; universe is resolved
  **structurally** from the series' measures (one-expression-one-universe; a span across universes is a
  `cross_universe` category error on the query-error channel, not a mood). `ON …` is a
  **definition-language** clause only; if it appears in a query it is `frameql_syntax`.
- **`FROM <manifold>` is OPTIONAL.** [PROPOSE → RULE] It **defaults to the bound manifold** (the one the
  session/tool is attached to) and is **required only** when the surface holds more than one manifold
  and the statement must name which. Rationale: the demo, the MCP `query` tool, and the agent are all
  single-manifold-bound; making `FROM` mandatory would put ceremony on every single-manifold ask for a
  case they never hit. The multi-manifold surface (a future catalog) is where `FROM` earns its keep.
  *A statement with no `FROM` against a multi-manifold surface refuses with the manifold list named.*
- **`AT { <anchor> }` is REQUIRED and the sole output-grain declaration.** The braces carry an anchor
  which is a product of levels spelled with `*` (`AT {region*store}` ≡ `AT {region, store}`; the comma
  is accepted on input, `*` is canonical — the standing anchor-spelling law). `AT {}` (the empty
  anchor) is the scalar/grand-total frame. [PROPOSE → RULE] the comma-inside-braces is accepted as a
  synonym for `*` so the worked example below reads naturally; the retirement of the comma is the same
  post-launch hygiene sweep already ruled, not this WP.

**Clause order is fixed** (as written above); clauses are optional but may not be reordered. A
misordered clause is `frameql_syntax` with the expected order named.

---

## 2 · The series — canonical form, and `@` as the input-anchor marker

A **series** is one output column's expression. Canonically:

```
<reduction>( <column-expression> [ @ { <input anchor> } ] )
```

- The **`@ { <input anchor> }`** pins the grain the reduction reads its operand at — the **input**
  anchor. `sum(revenue @ {transaction})` reads `revenue` at transaction grain and sums to the output
  `AT`. `avg(aov @ {day})` reads `aov` at day grain and averages to the output `AT`.
- When the input anchor is **omitted** and the reduction's operand has a **unique** natural grain, the
  series is well-posed without it (single-grain sugar, §3). When omission leaves the input grain
  **underdetermined**, the series does not serve — it **clarifies `input_anchor_ambiguous`**, naming the
  candidate input anchors. This is the shipped clarify, unchanged in meaning; §3 states the continuity
  precisely.
- A **bare measure with no reduction** (`revenue`, `aov`) is a series iff its grain matches the output
  `AT` (or reaches it by a verified edge); it carries an implicit identity reduction. A bare measure
  that would require reduction to reach `AT` but names none is `input_anchor_ambiguous` (it must say at
  what grain, and how, it collapses).
- **`@` NEVER spells the output anchor.** The output anchor is `AT`, always. [PROPOSE → RULE] the
  brace form `@ { … }` is canonical for the input anchor to visually rhyme with `AT { … }` (both are
  anchors, both braced); a **bare** `@ day` (no braces, single level) is accepted sugar for `@ {day}`.

**The disposition of the shipped terse `cols @ anchor` form.** [PROPOSE → RULE] **Retire it as a
top-level statement form; do not keep it as a sugar.** Reason: under the ruling, a top-level
`aov @ cal.month` now reads as "`aov` **input**-anchored at `cal.month`, output anchor unstated" — which
is exactly an underdetermined output, i.e. it would have to *clarify for a missing `AT`*. Keeping it as
sugar for `SELECT aov AT {cal.month}` would mean `@` spells the output anchor in one position and the
input anchor in every other — the precise ambiguity this WP exists to kill. Cleaner: **the trailing-`@`
output form is retired**; the envelope's `SELECT … AT {…}` is the only output-grain syntax. Migration
cost is real and enumerated in §6 (demo, llms.txt, the What-is-Columna glossary line `aov @ cal.month`,
the site query strings, every manual example) — all move to `SELECT aov AT {cal.month}`. *If you would
rather keep the terse single-series form alive as a distinct sugar, the alternative is a **different
marker** for the output (e.g. `aov → cal.month`) so `@` stays unambiguously input; I recommend against
adding a second output syntax at all, but flag it as the live alternative.*

---

## 3 · Chapter 3's sugars, and their refusal conditions (the continuity)

Sugars are surface conveniences that **desugar to the canonical form**; each has a **refusal condition**
that is not a new outcome but an existing wire mood. The naming of the continuity is the point: **the
shipped `input_anchor_ambiguous` clarify IS a sugar's refusal condition** — the sugar is "omit the input
anchor," and its refusal is "the omission is underdetermined." Proposed sugar set for 0.9.0:

| Sugar (surface) | Desugars to | Refusal condition (existing mood) |
|---|---|---|
| **Omitted input anchor** `avg(aov)` | `avg(aov @ {g})` for the unique natural grain `g` | `input_anchor_ambiguous` **clarify** when `g` is not unique — names the candidate anchors |
| **Bare `@ level`** `aov @ day` | `aov @ {day}` | — (pure spelling) |
| **Comma anchor** `AT {region, store}` | `AT {region*store}` | — (accepted-on-input spelling) |
| **Bare measure at `AT`** `SELECT revenue AT {region}` | identity reduction at `{region}` if grain reaches it by a verified edge | `input_anchor_ambiguous` if reduction is required but unnamed; `b_anchor_crossing`/`blocked_reduction` **disclose/refuse** if the edge is blocked |
| **Single-universe bare ask** (no universe anywhere) | resolves in the manifold's sole universe | `cross_universe` **error** only if measures actually span universes |

[PROPOSE → RULE] this is the **minimal** sugar set — every entry is a spelling shortcut with a named
desugaring, and its failure is an already-shipped mood. I deliberately do **not** propose
value-filter-in-brackets, scans, or allocation macros as sugars in 0.9.0 (they are grammar the engine
does not have; they stay `[ROADMAP]` in the manual per CP-M1 M1-d). Chapter 3 documents exactly this
table.

---

## 4 · The naming laws (Chapter 1.6, as written)

- **`AS`** is the explicit alias: `SELECT sum(revenue @ {transaction}) AS gross AT {region}`. An alias
  is the column's name on the output frame.
- **Mechanical defaults, only where unambiguous.** An unaliased reduction names itself
  **`<reducer>_<column>`** — `sum(revenue…)` → `sum_revenue`, `avg(aov…)` → `avg_aov`. **The input
  anchor never affects the name** (`avg(aov @ {day})` and `avg(aov @ {week})` both default to `avg_aov`;
  if both appear in one frame that is a collision, refused — see next). A bare measure names itself by
  the measure. Where the default would be ambiguous, no name is invented — it is refused.
- **Collisions are REFUSED, never suffixed.** Two output columns resolving to the same name do not become
  `avg_aov` / `avg_aov_2`; the frame **refuses** and names the two series, remedy "give one an `AS`."
  This includes a column name colliding with an **anchor-dimension name** in the same frame (a series
  named `region` when `AT {region}` is present is refused — the output frame's columns and its anchor
  coordinates share one namespace). Silence-by-suffix would let two different things wear confusable
  names; the law is distinctness or refusal.
- **Visibility asymmetry.** Aliases are visible to **`HAVING`** and **`ORDER BY`** (clauses that speak of
  the assembled output frame), and **never** to **`WHERE`** or to **sibling series** (which are evaluated
  per-series, before assembly, and cannot reference a column that does not yet exist). A `WHERE` or a
  sibling series that references an alias is `frameql_syntax`, remedy naming the asymmetry.
- **`PER` takes anchor coordinates only, never aliases.** `LIMIT 3 PER {region}` partitions by an anchor
  coordinate of the output frame; `LIMIT 3 PER {gross}` (an alias) is `frameql_syntax`. `PER` shapes the
  frame along its **grain**, not its values.
- **`WITH <name> = <expression>`** is the reuse device — a macro binding, textually substituted into the
  series that reference it before desugaring. `WITH t = revenue @ {transaction} SELECT sum(t) AS gross,
  avg(t) AS typical AT {region}`. **Repeat-the-expression is dead** as the reuse idiom: a shared
  sub-expression is bound once with `WITH` and referenced by name. A `WITH` name colliding with a
  measure/level name is refused (distinctness law again).

---

## 5 · The clause-reference law

**`ORDER BY`, `HAVING`, and `PER` reference the output frame's OWN columns only** — its named series
(aliases/defaults) and its anchor coordinates. There are **no hidden pulls** of a
reachable-but-unnamed dimension: `ORDER BY store_count` when `store_count` is not a column of the frame
does not silently reach into the manifold to compute it. The error path lives in the four-mood
temperament — **the remedy names itself: "add it to the anchor" (or "select it as a column").** A
`HAVING`/`ORDER BY`/`PER` reference to something not on the frame is not a syntax error thrown blank; it
is a refusal that says *what* is unreachable and *how* to make it reachable (put the dimension in `AT`,
or select the series).

**Coarser-grain participation is checked never in syntax but by the declared edge and its adjudicated
verdict.** Whether a series at a finer grain may participate in an output frame at a coarser `AT` is not
a grammar question — the grammar admits it — it is settled by whether a **verified edge** carries the
reduction and whether that edge's **verdict** is clean. A blocked edge yields `b_anchor_crossing` /
`blocked_reduction` (disclose or refuse per materiality); the grammar never pre-judges it. Syntax
admits; the kernel adjudicates.

---

## 6 · `EXPLAIN` as first-class

`EXPLAIN <statement>` is the same grammar with an `EXPLAIN` prefix, and it **touches zero data**. It
returns:

- the **canonical desugared form** (every sugar expanded, `@`/`AT` explicit, `WITH` substituted);
- **atom decomposition** — the (measure, member) @ input-anchor atoms each series resolves to;
- the **dependency cone** — the derived-column/edge/assert lineage each atom pulls in, **with current
  verdicts** (verified/corroborated/untestable/contradicted; cut/blocked scope);
- the **complete would-be annotation** — the mood each series *would* return (serve/disclose/clarify/
  refuse/error) and its reason/caveats, computed by the planner without a fetch;
- **zero data touched** — `executed: false`, `fetches_delta: 0` (the shipped `explain` tool's invariant).

It is exposed on **MCP as a tool beside `query`** (already present as `explain`; this WP extends it to
the envelope and the desugared/atom/cone payload). It is the query agent's **cheap inner loop** — the
agent proposes a statement, `EXPLAIN`s it for free, reads the would-be mood, and only `query`s when the
annotation says serve/disclose. [PROPOSE → RULE] the EXPLAIN payload gains `desugared`,
`atoms`, and `cone` fields (additive; the shipped `executed`/`fetches_delta`/caveats stay).

---

## 7 · The canonical worked example (the spec's proof-of-language)

The **top-3 stores per region by gross, with each region's typical order value**, at `AT {region,
store}` — five lines exercising anchor products, auto-leading dimensions, edge-carried degeneracy, and
`PER ⊆ ORDER BY`:

```frameql
FROM retail
WITH line = revenue @ {transaction}
SELECT sum(line)        AS gross,
       avg(aov @ {day}) AS typical
AT { region * store }
ORDER BY region, gross DESC
LIMIT 3 PER { region }
```

_(§7 corrected 2026-07-17, Huayin ruling on flag 3 — FLAGGED: the earlier draft wrote `ORDER BY gross
DESC`, dropping `region`. **PER's law is BOTH constraints conjoined**, not rivals: PER keys are anchor
coordinates only (aliases refused) **AND** `PER ⊆ ORDER BY` — PER groups, the remaining ORDER BY keys
rank within, groups present contiguously. So every PER key must also be an ORDER BY key; `region` is
restored to ORDER BY, matching the original ratified five-liner and the What-is-FrameQL piece.)_

Reading it:
- **`AT { region * store }`** — the output anchor is the **product** of two levels; every row is a
  (region, store) pair. `region` **auto-leads** as the coarser coordinate (the edge region←store carries
  it); it is not selected as a series, it is an anchor coordinate, and `ORDER BY`/`PER` may name it.
- **`WITH line = revenue @ {transaction}`** binds the transaction-grain line once; `sum(line)` reduces it
  to the (region, store) grain — the reduction is **edge-carried** (transaction → store → region), and
  the grammar admits it while the kernel's verdict on those edges decides serve vs disclose.
- **`typical = avg(aov @ {day})`** reads `aov` at **day** grain (its input anchor) and averages to
  (region, store) — a **degeneracy** the edge carries: two different input grains (transaction, day)
  collapsing into one output frame, legal because each series names its own `@`.
- **`ORDER BY region, gross DESC`** references the frame's own columns; `region` (the PER key) leads so
  groups are contiguous, `gross DESC` ranks within each.
- **`LIMIT 3 PER { region }`** keeps the top 3 rows per `region` — **`region` is both an anchor
  coordinate AND an ORDER BY key** (the conjoined PER law), so the per-partition top-N is well-posed.
  `PER {typical}` would be refused (alias, not a coordinate); `PER {store}` would be refused unless
  `store` is added to ORDER BY (PER ⊆ ORDER BY).

This single statement is the acceptance target for the parser+planner increment: parse it, desugar it,
resolve its atoms, admit its edges, and shape it — every clause exercised.

---

## 8 · What this spec does NOT decide (deferred to increments after ratification)

Per the WP sequencing, ratification of §§1–7 gates: parser/AST (four-mood-temperament errors) →
planner assembly (the planner owns the envelope; multi-series = juxtaposition; `WHERE` per-series
reachability bound pre-reduction; `HAVING` by name on the assembled frame; `ORDER BY`; `LIMIT PER` with
`PER ⊆ ORDER BY`) — the engine stays per-column and envelope-blind → sugars → `EXPLAIN` → surface
migration (demo tour, seeded corpus + drift gate, MCP server, agent prompt with KP conformance edits
flagged, llms.txt, site query strings). Checkpoints per house pattern; each increment verified.

**The manuals convergence rides this WP** (ruled): flags 1 & 3 (Chapter 1's `SELECT`/`FROM`/`AT` grammar;
Appendix B keywords) become this WP's **documentation increment** — the Coframe→envelope rewrite,
writing the manual to the envelope **as implemented**, one truth; flag 2 (`inform`→`refuse`) is adopted
manual-wide with a one-line ADR-020 lineage note. The `wp-manuals-alignment` diff holds unmerged and its
(i)–(iv) law-reconciliation carries into the **unified envelope-era diff**; the Chapter-2 rewrite is
reframed (its terse-form framing superseded). Huayin's prose pass happens **once**, on the final unified
diff. The manual's preface gains the origin law as its opening: *"the Frame is the query, not operational
instruction"* (DataFrame minus Data is Frame; columns are expressions of what a thing **is**, not
operational process).

---

## 9 · Points awaiting your ruling (the `[PROPOSE → RULE]` roll-up)

1. **`FROM` optional, defaults to the bound manifold** (§1) — required only multi-manifold.
2. **`AT {}` required; comma accepted inside braces** as a synonym for `*` (§1).
3. **Terse `cols @ anchor` RETIRED**, not kept as sugar (§2) — the alternative is a distinct output
   marker (`→`); I recommend retirement.
4. **Brace input anchor `@ { … }` canonical; bare `@ level` accepted** (§2).
5. **The minimal sugar set** (§3) — omitted-input-anchor, bare `@ level`, comma anchor, bare-measure-at-
   `AT`, single-universe bare ask; nothing else in 0.9.0.
6. **EXPLAIN payload gains `desugared`/`atoms`/`cone`** (§6), additive.
7. **The worked example** (§7) as the parser+planner acceptance target.

Everything in §§4–5 (the naming laws and the clause-reference law) is proposed **as Huayin wrote them** —
transcribed to exact grammar, not reinterpreted; flag if any transcription drifts from intent.
