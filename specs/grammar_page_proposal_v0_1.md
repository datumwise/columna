# The shipped grammar reference — proposal (v0.1, for Huayin's ratification)

*Workstream B of the external-AI probe response. **Proposal only — no code written.** The desk's
earlier framing contained one error that must not reach the page; it is corrected in §3 and that
correction is the reason this is proposal-first rather than build-first.*

---

## 1 · The defect this fixes

A model reading the manuals produced a Manifold the **shipped parser rejects** on three construct
types:

| construct | what the model wrote | why the parser rejects it |
|---|---|---|
| `MANIFOLD` | no `VERSION` | `VERSION <n>` is required |
| `LEVEL` | no `= <column>` | the map clause is required by the shipped short form |
| `MEASURE` | no `FROM … AS …` | the map clause is required by the shipped short form |

It got **`HIERARCHY` right** — which is the §26.6 correction working in the wild, five days after
landing. That is the control in this experiment: the one construct we fixed is the one the model
produced correctly.

**Root cause is structural, not typographical** (rowed on OF-18): Chapter 26 presents **long forms as
primary** and the **shipped short forms as parentheticals**, so a careful reader learns the form the
parser does not accept. Better prose cannot fix this; a reader who reads *more* carefully learns the
wrong thing *more* thoroughly.

## 2 · The deliverable

A grammar page **generated from `columna-core`'s own parser**, so it cannot drift from what ships:

- **Every shipped keyword.** Read from the parser's `_KW` tuple, which today is exactly:
  `MANIFOLD · UNIVERSE · LEVEL · RELATE · MEASURE · DERIVED · ASSERT · HIERARCHY · ATTR`.
  Generated, not transcribed — so a keyword added or purged in the package changes the page.
- **Its exact signature**, derived from the parser's own patterns rather than restated by hand.
- **Worked examples that the build verifies parse.** Every example on the page is executed against the
  shipped parser at build time, and **the build FAILS if any example does not parse** — the
  has-to-be-loud principle, applied to documentation. This is the property the manuals lacked: nothing
  in CI ever read Chapter 26's examples.

The generator belongs beside the existing ones (`gen_case.py`, `gen_universe_visual.py`,
`gen_transcript.py`) and rides the **shipped-coherent** deploy path, so the page describes the pinned
released package, never a local checkout.

## 3 · ⚠️ The correction — what the page must NOT say

The desk's earlier framing was that **"physical binding is part of the declaration."** That is
**wrong, and the architecture is the opposite.** It must not reach the page.

**§2b / C-2 insulation, which the code enforces:** `describe` emits **logical names only** — no
`realized_by`, no `VIA` bridge, no `FROM` table, no expression — and a **standing insulation test**
(`packages/columna-server/tests/test_describe_insulation.py`) asserts that physical identifiers never
cross describe or the wire.

So the page teaches **syntax and layering together**. A `.cml` source document **co-locates two
layers**:

| layer | what it is | who sees it |
|---|---|---|
| **Logical declarations** | what the Manifold *is* — universes, levels, measures, hierarchies, relates, asserts | **agents and callers**, over `describe` and the wire |
| **Map clauses** | how it binds to physical storage | **engine only** — never crosses `describe` |

**Every map clause is labelled as such on the page.** The map-side clauses are:

- `= <column>` (on `LEVEL`)
- `FROM <table> AS <agg>(<expr>)` / `FROM <table> VALUE <expr>` (on `MEASURE`)
- `VIA <table>(<col>, <col>)` (per hop, inside `HIERARCHY`)
- `REJECT …`

**§2b is the page's frame, stated up front** — not a footnote. A reader must leave the page knowing
that the file they are writing contains two layers, that only one of them is visible to an agent, and
that this is enforced rather than merely intended. The page is where a reader most likely forms the
wrong mental model, which is why the framing is load-bearing.

## 4 · Route — my recommendation

**`/docs/grammar`**, a sibling of the three existing manuals (`/docs/framework`, `/docs/frameql`,
`/docs/reference`), rather than a section inside the framework manual.

Reasons:
- The manuals are **ratified prose documents**; this page is **generated output**. Filing generated
  content inside a ratified manual muddies which parts are ratifiable and which are recomputed — and
  it would make the manual's own build fail on a package change, which is a surprising coupling.
- It is a **reference lookup**, used differently from a manual read top to bottom.
- It gives the "read this before writing a Manifold" pointer a stable, short, guessable URL.

The reference manual's §26 should then **point at it** as the authority on shipped syntax, keeping
§26 for semantics. (That pointer is a manual edit and therefore rides OF-18's pass, not this page.)

## 5 · Discoverability

`llms.txt` and `llms-full` gain a **Start here** pointer, phrased so a model knows it is the
precedence-setting document:

> Writing a Manifold? Read /docs/grammar first — the shipped keyword set with exact signatures and
> examples verified against the released parser at build time.

## 6 · Open questions for the desk

1. **How much semantics on the page?** My recommendation: the *minimum* that makes a signature
   usable, with everything else linking to the manuals. A generated page that grows prose becomes a
   fourth manual nobody ratified.
2. **Does the page show a full worked Manifold**, or per-construct fragments only? I lean **both** —
   fragments for lookup, one complete parseable document at the end, since the probe's failure was a
   *whole document* that didn't parse, not an isolated clause.
3. **`ATTR` is in `_KW`** but is an inline clause of `LEVEL` rather than a standalone statement.
   Listing it as a peer keyword would be accurate to the parser and misleading to a reader. My
   recommendation: list it under `LEVEL`, with a note that it appears in `_KW`.
4. **OF-21 interacts with this page.** If the map layer later moves to a separate file, the page's
   two-layer framing becomes a two-*file* framing. The proposal is written so that change would be an
   edit to the framing, not a rewrite — but the desk may prefer to settle OF-21 first.

## 7 · What is NOT in this proposal

- No code. No generator, no route, no llms edits for this workstream.
- No manual edits. The §26 pointer and the form-primacy fix ride **OF-18**.
- No change to `describe`, the wire, or the insulation test. This is a documentation surface only —
  and the insulation guarantee it describes is the one already enforced.

*DRAFT for ratification. Nothing here is built.*
