# Columna 0.9.0 — release notes (DRAFT, for Huayin's gate)

**From: Claude Code, 2026-07-17. The full span since 0.8.0, in the house register. Drafted for the
release cut so it is ready when Huayin is; to his gate for ratification. On ratification it feeds the
GitHub Release + the `columna-core`/`columna-server` CHANGELOGs. This is a DRAFT (a lock): no PR, no
merge — the words are proposed, not shipped.**

---

## Columna 0.9.0

*A query is a Frame, not an instruction. 0.9.0 is the release where the shipped `@`-fragment gives way
to the language it was always a fragment of — one statement with a visible output grain, many juxtaposed
series, filtering and shaping, macros, and a first-class `EXPLAIN` — and where `@` finally means exactly
one thing.*

### The envelope is the language — `SELECT … AT {…}`, and the Name's Law
FrameQL is now a statement, not a terse pair. The whole form:

```frameql
[EXPLAIN]
[FROM <manifold>]
SELECT <series> [AS <alias>] [, <series> [AS <alias>]]…
AT { <anchor> }
[WHERE   <per-series predicate> [AND …]]
[HAVING  <output-frame predicate> [AND …]]
[ORDER BY <output-frame column> [ASC|DESC] [, …]]
[LIMIT <n> [PER { <anchor coordinates> }]]
```

`AT { <anchor> }` is the **sole** output-grain declaration — a product of levels spelled with `*`
(`AT {region*store}`; the comma is accepted on input, `*` is canonical), `AT {}` the grand-total frame.
Multiple asks over one grain are posed by **juxtaposition** — several series in one `SELECT`, each
carrying its own reduction and its own input anchor. `FROM` is optional and defaults to the bound
manifold (required only where a surface holds more than one). `WHERE` binds per series before assembly;
`HAVING`/`ORDER BY`/`PER` speak of the assembled output frame by its own column names and anchor
coordinates — **no hidden pulls** of a reachable-but-unnamed dimension; the remedy names itself ("add it
to the anchor, or select it as a column"). `WITH <name> = <expression>` is the reuse device —
repeat-the-expression is dead as the idiom. Names follow one law: `AS` is explicit, an unaliased
reduction defaults to `<reducer>_<column>`, and a **collision is refused, never suffixed** — distinctness
or refusal, output columns and anchor coordinates sharing one namespace.

This is the **Name's Law** made operational: *the Frame is the query* — a DataFrame minus its Data is a
Frame, and a column is an expression of what a thing **is**, not an instruction for how to fetch it. The
grammar admits; the four-mood kernel adjudicates. Syntax never pre-judges whether a finer-grain series
may participate in a coarser `AT` — that is settled by a **verified edge** and its verdict, not by a
parse.

### `@` means one thing now — the input anchor
Two things used to spell with `@`: the **outer** `@` named the output anchor (`aov @ cal.month`), the
**inner** `@` named a reduction's input grain (`avg(aov@day)`). They meant opposite things. Huayin ruled
the manual's semantics win: **`@` is the input-anchor marker, universally** — the grain a series reads
its operand at — and the output grain moves to `AT`, always. `@ { <input anchor> }` is canonical (it
rhymes with `AT { … }`; both are braced anchors); bare `@ day` is accepted sugar. After 0.9.0 there is
exactly one meaning for `@` and exactly one place the output grain is named. That collision — a fragment
whose two `@`s mean opposites — is the whole reason it could not ship as the language, and it is closed.

### `EXPLAIN`, first-class beside `query`
`EXPLAIN <statement>` is the same grammar with a prefix, and it **touches zero data** (`executed: false`,
`fetches_delta: 0`). It returns the **canonical desugared form** — the exact artifact the planner
consumed, every sugar expanded, `@`/`AT` explicit, `WITH` substituted, never a reconstruction — the
per-series **atom decomposition** ((measure, member) @ input-anchor), the **dependency cone** with each
edge/derived-column/assert carrying its **current verdict** (verified/corroborated/untestable/
contradicted; cut/blocked scope), and the **would-be annotation**: the mood each series *would* return and
why, computed without a fetch. It is exposed on MCP as a tool beside `query`, and it is the agent's cheap
inner loop — propose a statement, `EXPLAIN` it for free, read the would-be mood, and `query` only when the
annotation says serve or disclose. The payload is additive over the shipped `explain`
(`desugared`/`atoms`/`cone` join the existing `executed`/`fetches_delta`/caveats); a standing test holds
its zero-fetch invariant and asserts its would-be outcome equals the query's actual one.

### Dependent-pair transport — the worked example runs whole
The engine now completes a target anchor where one level is **functionally determined** by another
(region fixed by store). The determined level is **attached 1:1 along the edge** (join-and-group, native
Polars — the planner adjudicates the edge's functionality upstream, Polars executes what it ruled), never
reduced, never inflated. Inline reductions serve at a dependent-pair anchor — the pinned input anchor pins
its lineage, the orthogonal output dimensions join the input grain, then reduce. With this, the spec's
canonical five-liner runs **whole** — two series at different input grains (store, day), a dependent-pair
output `AT {region*store}`, `ORDER BY` with the `PER` key leading, `LIMIT 3 PER {region}` — and serves:

```frameql
FROM retail
WITH line = revenue @ {transaction}
SELECT sum(line)        AS gross,
       avg(aov @ {day}) AS typical
AT { region * store }
ORDER BY region, gross DESC
LIMIT 3 PER { region }
```

The **conjoined `PER` law** holds it together: `PER` keys are anchor coordinates only (an alias is
refused) **and** `PER ⊆ ORDER BY` — `PER` groups, the remaining `ORDER BY` keys rank within, groups
present contiguously. (One honest boundary, reported either way: DG-2's structural serve-with-caveat —
collapsing a base dimension while transporting another across a *blocked* lineage, e.g.
`SELECT level.sum AT {store*cal.month}` — does **not** fall out of this machinery. It stays a distinct
`unsupported` gap owed its own engine increment; the demo's disclose reaches it through the shipped
materiality rule, not through dependent-pair transport.)

### The migration — every speaking surface moved to the envelope
The wire *is* the envelope now. The MCP `query` tool parses statements (`parse_statement` +
`run_statement`); its `universe` argument is **gone** — a population is resolved structurally and is never
named in a query (§2c). The `demo --play` tour, the MCP acceptance suite, and the agent tests all speak
`SELECT … AT {…}`; the four moods walk unchanged. The README's four-mood bullets are re-spelled in the
envelope. The **agent system prompt** is rewritten to teach the envelope — `SELECT`/`AT`, `@` as the
input anchor, `WHERE`/`HAVING`/`ORDER BY`/`LIMIT PER`, `WITH`; because a prompt edit is a knowledge-package
ruling under the copy law, that diff and its four examples are **FLAGGED for Huayin's ratification** with
the exact terse→envelope changes surfaced, not silently adopted. (The remaining surfaces — `llms.txt`, the
site query strings, and the new prose-coherence deploy tripwire from the #45 incident — migrate on the
site branch as its own draft, not in this cut.)

---

## Upgrade — a breaking change, stated plainly

**0.9.0 breaks the query wire.** The terse `cols @ anchor` statement form is **RETIRED** from every
shipped surface (dated tombstone, 2026-07-17). Old terse queries **no longer parse** as a query — under
the ruling a top-level `aov @ cal.month` would now read as "`aov` input-anchored at `cal.month`, output
grain unstated," which is exactly an underdetermined output; keeping it as sugar would resurrect the very
`@` ambiguity this release exists to kill. So it is gone, not softened. `columna_core.frameql.parse_frameql`
survives only as a **tombstone** kept for lineage/interpretability — no shipped surface calls it. The MCP
`query` tool's `universe` argument is removed with it (§2c: universe is never named in a query).

Migrate every query string to `SELECT … AT {…}`:

| Was (terse, retired) | Now (envelope) |
|---|---|
| `aov @ cal.month` | `SELECT aov AT {cal.month}` |
| `inv: level.last @ store` | `SELECT level.last AS inv AT {store}` |
| `avg(aov) @ cal.month` | `SELECT avg(aov) AT {cal.month}` |
| `level.sum @ store*cal.month` | `SELECT level.sum AT {store*cal.month}` |

The **inner** `@` inside a reduction is unchanged in meaning — `avg(aov @ {day})` still pins the input
grain; only the trailing **output** `@` is retired, replaced by `AT`. The wire **contract is unchanged**
(`contract_version` `"1"`): the four moods are the same data, and the `EXPLAIN` payload extends additively.
The break is in the **accepted query grammar**, not the response schema — the numbers you already trust
still arrive shaped the same way; the strings that ask for them change.

*Upgrade: `pip install --upgrade columna` (or `columna-core columna-server`). Re-spell any stored FrameQL
query strings per the table above; an `EXPLAIN` of a migrated statement is a free, zero-data way to
confirm it desugars and would serve before you run it.*

**Status: RATIFIED-PENDING-CEREMONY** (Huayin, 2026-07-17 — pre-screened in full at the design desk;
these gate-stamp in the flip itself). Version scheme **CONFIRMED**: **columna-core 0.9.0**, **columna-server
0.3.0** (its own 0.x track; the wire-INPUT break earns server's minor bump), **columna (meta) 0.9.0** (pins
core>=0.9.0, server>=0.3.0). On the cut: the GitHub Release `v0.9.0` is cut from this; the per-package lines
fold into the CHANGELOGs.

**Both gate items RESOLVED.** (1) The agent system-prompt terse→envelope diff was **RATIFIED on sight at the
#49 checkpoint** — every clause conformant to the ratified grammar (the conjoined PER law included) and the
retirement stated plainly to the agent. (2) **`contract_version` stays `"1"`, confirmed with the reasoning
for the record:** the contract versions the RESPONSE — the four-mood shapes, the caveat schema, the reason
codes — none of which change, and EXPLAIN extends additively; the break lives in the accepted INPUT grammar,
which is carried by the package semver and the dated tombstone (2026-07-17), exactly as this draft argues.

**Rowed, post-flip (its own beat — does NOT reopen #49):** a `frameql` grammar-version field advertised in
`describe`, so any external agent can detect which grammar a server speaks — additive, transition-friendly.

**Flip order (ruled; carried verbatim into the FLIP-READY checklist):** merge **#49 FIRST** (the 0.9.0 cut
needs its code on main) → tag/Release **`v0.9.0`** on main → `publish.yml` fires (OIDC → PyPI) → bump the
website shipped-coherent pin to 0.9.0 → **#46 un-drafts and merges** (the site surfaces + prose-coherence
tripwire go green against the new pin) → the **manuals** merge after Huayin's prose pass → **one deploy**.
