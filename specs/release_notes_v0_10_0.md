# Columna 0.10.0 — release notes (DRAFT, for Huayin's gate)

**From: Claude Code, 2026-07-18. The span since 0.9.0, in the house register. Drafted for the release
cut so it is ready when Huayin is; to his gate for ratification. On ratification it feeds the GitHub
Release + the `columna-core`/`columna-server` CHANGELOGs. This is a DRAFT (a lock): no PR, no merge —
the words are proposed, not shipped.**

---

## Columna 0.10.0

*The definition language, taught by a case — and checked, minds included.*

0.10.0 is the release where the Manifold's **definition language** grows up, and where a realistic
**case demo** — Cascadia Retail — proves it end to end: a real warehouse modeled to a spec, every
claim adjudicated against the data, the four moods served live, and the assistant's own transcripts
recorded rather than illustrated. `columna-core` reaches **0.10.0**; `columna-server` reaches **0.4.0**.

### The definition language (`columna-core` 0.10.0)

- **EDGE is purged — `HIERARCHY` is the sole surface for functional paths.** An edge is a two-node
  hierarchy; a lineage is a small branching structure (calendar chains day→month→quarter→year and hangs
  a week branch off day, because ISO weeks don't nest in months). Each hop carries its `VIA`; the block
  desugars to the `FunctionalEdge`s that remain the single internal truth — adjudicator, planner, and
  engine vocabulary untouched.
- **Descriptions are folklore-into-the-system.** Any declaration — and each family member — may carry a
  `-- "one-line description"`; it flows model → describe → the wire. The folklore lives in the
  declarations.
- **Logical attributes (OF-9).** A level declares attributes (`ATTR opened = stores.opened_date`) and a
  universe declares row-attributes (`ATTR units, units_returned ON transaction`). A universe predicate
  reads `day >= store.opened` and renders logically; the physical binding stays on the map, never
  crossing describe or the wire.
- **The two-artifact projection.** One authored graph, two documents: the **Manifold spec** (purely
  logical — what everyone reads) and the **physical→logical map** (many-to-one, resolving each concept to
  one authoritative binding, with the rejected incarnations kept and reasoned). `no_physical_leak` makes
  the blast wall checkable — the logical spec carries none of the map's physical vocabulary.
- **The row-assert data channel.** A row-form `ASSERT … WHERE units_returned <= units` is now probed
  against the attested data — it holds (corroborated) or names a counterexample (fails closed); NULL
  comparands are not violations.

### The case demo, and the agent grows hands (`columna-server` 0.4.0)

- **The demo is Cascadia Retail.** One team, one warehouse, six questions, three chapters — the
  requirement, the design (two artifacts, the many-to-one map), and the Manifold live. `demo --play`
  runs the four-mood wheel over the real Cascadia Manifold.
- **The case rides as an on-demand MCP resource** (`case_chapter` / `case_manifest`) — the WHY behind
  the Manifold, fetched on a triggering pointer, not stuffed into every prompt.
- **The query agent has hands** — native tool-use: within a turn it consults `describe`, checks a plan
  with `explain`, and runs the terminal `query`; bounded cycles, grounding preserved, the MCP boundary
  intact (the agent process never imports the engine).
- **The transcripts are recorded, not illustrated.** Chapter 3's conversations are the actual recording:
  human turns scripted, agent turns live, tool calls visible, every take preserved. Four takes climbed a
  ladder — each surfaced a gap, each gap became a ratified prompt law or a ledgered language fork — and
  the shipped chapter keeps the warts: a guard suppressing a would-be ungrounded answer, a law that is a
  bias on a rented mind and not a guarantee. *Which is precisely why every claim in this system is
  checked rather than trusted, minds included.*

### The honest ledger

Two roads named, not promised: **coordinate-value predicates in `WHERE`** (`region = 'west'`) are the
leading post-launch language increment (the universal SQL reflex; the interim measure is the
anchor-and-read prompt law, which retires when the native filter lands), and the demo's **frozen world
has no clock** (relative-time is a design fork, not a bug). Both on the record.

*The whole case — the warehouse, the map, the spec, and every transcript — ships in the demo.
`pip install columna`, and rerun it yourself.*
