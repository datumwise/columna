# Attack B — frozen fixtures (deliverable 2)

**Frozen 2026-07-27.** Regenerate with:

```bash
python specs/open_planner/attack_b.py specs/open_planner/fixtures/
```

Exit 0 iff every path agrees with the desk's published numbers. **A green suite is not a green job:**
the script asserts agreement and returns non-zero on divergence, so this fixture set cannot be
refreshed into quiet disagreement.

## Status, per the ladder — three facts of different epistemic rank

| fact | status |
|---|---|
| **Attack B numbers** | **VERIFIED** — independent reproduction, exact, 12/12 months + the overall ratio |
| **Faithful half** | **ENGINE-EXECUTED** — via `aov`, coincidence-checked (below) |
| **Unfaithful half** | **NOT EXPRESSIBLE FROM THE ASK SURFACE** — *finding **F1***, `planner.py:371` — and **EXECUTED at its native IR layer** below that surface, with **no engine modification** |

## The numbers, three independent paths

| month | desk | direct | IR | ask (`aov`) | desk unf. | direct unf. | IR unf. |
|---|---|---|---|---|---|---|---|
| 2024-01 | 139.91 | 139.91 | 139.91 | 139.91 | 164.03 | 164.03 | 164.03 |
| 2024-02 | 125.81 | 125.81 | 125.81 | 125.81 | 145.22 | 145.22 | 145.22 |
| 2024-03 | 127.25 | 127.25 | 127.25 | 127.25 | 149.38 | 149.38 | 149.38 |
| 2024-04 | 137.91 | 137.91 | 137.91 | 137.91 | 156.09 | 156.09 | 156.09 |
| 2024-05 | 139.14 | 139.14 | 139.14 | 139.14 | 158.48 | 158.48 | 158.48 |
| 2024-06 | 130.56 | 130.56 | 130.56 | 130.56 | 152.41 | 152.41 | 152.41 |

**Overall ratio — desk 1.21 · direct 1.2100 · IR 1.2100.**

## The coincidence check — why `aov` is allowed to stand in for the atom-mean

`aov = revenue / orders` equals the mean over transaction atoms **only if** transaction rows are 1:1
with `customer·store·product·day` atoms. **They are not quite.** The shipped warehouse has **19995
transaction rows and 19994 distinct atoms — exactly one collision.** That collision falls **outside**
the published 2024-01…06 window, which is why `aov` reproduces the desk's faithful column there
exactly.

**Asserting the equality globally would be wrong**, and the fixture records the counts so a later
reader can re-check rather than inherit the assumption. Verify from the run.

## Finding F1 — a RECALL row, not a safety bug (ruled Huayin, 2026-07-27)

The unfaithful plan requires a **multi-level input anchor**. This build refuses one by name:

> `planner.py:371` — *"A braced product `@ {a*b}` is refused for now — single-level input anchors this build."*

At runtime: `avg(revenue @ {store*product*cal.month})` → `frameql_syntax`, *"multi-level input anchor
… is not supported in this build."* So **the attack is not utterable from the ask surface.**

That is **the grammar working, not the kernel working.** Multi-level input anchors are a legitimate
future ask-surface feature, and **when they ship they will not open the attack** — for the reason
below.

## The doctrine this exhibit mints (Huayin, 2026-07-27 — verbatim, for v1.1)

> An expressible pinned ask is its own denotation — `avg(revenue @ {store*product*month})`, once
> askable, is a different question, faithfully answered. **No ask can be unfaithful to itself;
> unfaithfulness lives only in the gap between a plan and an ask** — which is why obligation B has no
> ask-surface analogue, why the shipped mood contract already CLARIFIES on the underdetermined form,
> and why the kernel begins exactly where the grammar's protection ends: **at the searcher's channel.**

**The accidental safety is the grammar working; the kernel exists because searchers don't speak
grammar, they speak plans.**

## The CLARIFY exhibit — Two Anchors doctrine running on the wire, today

`SELECT avg(revenue) AT {cal.month}` → **clarify**, not a silent choice between the two horns:

> *"inline reduction `mean(revenue)` does not pin its input anchor — the grain to resolve `revenue`
> at before reducing to `cal.month` is underdetermined"*, offering `pin the input anchor to 'day'`.

Recorded in `attack_b_ask.json` because it is the live proof that the two horns are caught **by
structure**, on the shipped wire, before any kernel exists.

## The IR path — the attack's native layer

`attack_b_ir.json`. Both plans composed from the engine's **own** primitives, called exactly as the
planner calls them:

- `ColumnEngine.resolve` (`engine.py:84`) — IR node 1, `COLUMN(revenue, sum) @ input_grain`
- `ColumnEngine.reduce_series_to_anchor` (`engine.py:598`) — IR node 2, `REDUCE(mean @ target)`

`"engine_modified": false`. The faithful plan pins `input_grain` to the transaction universe's own
grain `customer·store·product·day`; the unfaithful plan pins it to `store·product·cal.month` — the
intermediate collapse. **One primitive pair, one changed argument, a 21% different answer.**

This is the threat model made concrete: **a searcher emitting IR reaches a composition the grammar
refuses to utter.**

## Files

| file | contents |
|---|---|
| `attack_b_direct.json` | duckdb-over-parquet reproduction + the atom-coincidence counts |
| `attack_b_ask.json` | the served faithful ask, the CLARIFY exhibit, and F1's two refusals verbatim |
| `attack_b_ir.json` | both IR compositions, their node lists, values, and `engine_modified: false` |
| `attack_b_agreement.json` | the per-month cross-path agreement matrix and the overall ratios |
