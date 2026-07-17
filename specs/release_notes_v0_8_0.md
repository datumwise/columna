# Columna 0.8.0 — release notes (DRAFT, to Huayin's gate)
**From: Claude Code, 2026-07-17. The full span since 0.7.8, in the house register. Commissioned for the
launch cut so it is ready when Huayin is; to his gate alongside PR #40 (CP-3). Feeds the GitHub Release +
`columna-core`/`columna-server` CHANGELOGs on ratification.**

---

## Columna 0.8.0

*A number owes you its assumptions. 0.8.0 is the release where the assumptions became first-class — declared,
adjudicated, and legible — and where the meaning gets in through a door you can see.*

### The Certificate customers — ASSERT and HIERARCHY, under the scope-edit law
Declared invariants (`ASSERT`) and functional-dependence chains (`HIERARCHY`) are now adjudicated by the
same Certificate kernel that licenses derived-column fertility — the same `License`, minted the same way,
failing publish **closed** on a contradiction. When re-attested data violates a declaration, the manifold
does not lie and does not silently drop it: the **scope-edit law** cuts exactly the affected scope, uniform
across all three kinds — an ASSERT degrades to a **cut** (`conflicting_data`), a license to a **recompute**,
a hierarchy edge to **blocked transport** (`contradicted_edge`). `reattest` recomputes the serving scope
from the current verdicts — a pure function, symmetric: fix the data and the scope restores. History lives
in watermarks and the ledger, never in the scope.

### §2c — one expression, one universe
Universe resolution is settled. A column expression evaluates in **one** universe and never crosses the
boundary: an expression spanning two populations is a **category error** (`cross_universe`), not a hedged
answer. `ON UNIVERSE` is retired from the query grammar — a population is resolved structurally, and pinned
where it belongs, in **definitions**. Multi-population asks are posed by **juxtaposition** (separate columns,
each over its own universe); a single-universe manifold needs no qualification at all. The old
cross-universe "wedge" is gone — it was never a mood, it was a mistake.

### BASIS and absence semantics — what a missing row means
A universe now declares its **basis** — `events`, `spine`, `product`, or `registry` — and the basis fixes
what absence *means*. In an **events** population, a missing row is a lawful **zero** (immaterial). In a
**spine** or **product**, it is a **gap** — served with an `incomplete_data` caveat, never a silent zero. A
**registry** makes membership a checkable fact. Serving follows the declaration; the record of how well it
was tested rides `describe`.

### The four-mood wire, on one tour
Every answer is one of four moods — **serve · disclose · clarify · refuse** — returned as structured data on
one contract (`contract_version` `"1"`). `columna-server demo --play` walks all four in one flow on
well-posed asks: a clarify (an inline reduction whose input grain is underdetermined), a refuse (an ask
outside the contracted space), a **disclose** (a stock summed across a blocked time axis — served *with* a
material caveat, never a silent wrong total), and a clean serve.

### `columna init` — the authoring on-ramp, meaning-in through a visible door
A new front door: `columna init` recovers meaning from a messy database and proposes a Manifold. It sits at
the **meaning-in seam** between two human-designed walls — a **governed aperture** (catalog, profile-stats,
metered samples; an exfiltrating read is structurally impossible) and a **draft that cannot lie in its
favor** (the two-layer **polarity wall**: it may propose closures freely, and has *no legal way* to express
an inferred opening — data may suggest walls, never doors). It proposes; the human declares.

### The knowledge package — a measured, shipped v0.5
The authoring agent's knowledge package ships at **v0.5**, and it got there by measurement, not assertion.
A pre-registered eval ratchet moved it one variable at a time: **v0.3** made the Columna-native sharp calls
salient (◆-recall 4/7 → 6/7; the crux — m-leak was *named* yet silent, and surfaced only under a trigger);
**v0.4** pruned the checklist (flooding down, but recall bought at a cost — caught by its own do-not-ship
clause and reverted); **v0.5** re-tuned the prune with an evidence-justified floor (flooding halved **and**
recall held). The live KP is always the best-measured KP.

### `describe` — the whole manifold, legible; no physical identifier crosses
`describe` gained License blocks across fertility/hierarchy/assert, basis + absence semantics on universes,
operator properties, and the published-scope/cut state. And it closed a wall: **no structural physical
identifier crosses `describe` or the wire** — no table names, no qualified `table.column`. A standing test
enforces it.

### The Manifold Explorer
A portable Explorer component renders any `describe` — measure-first, searchable — and puts three things one
click from every fact: the **law** that defines it, the **verdict** that tested it, and the **query** that
shows it. The whole manifold, wearing its verdicts.

---

*Upgrade: `pip install --upgrade columna` (or `columna-core columna-server`). The wire contract is unchanged
(`contract_version` "1"); 0.8.0 is additive on the surface and deeper underneath.*

**Status: DRAFT — to Huayin's gate. On ratification: cut the GitHub Release from this, and fold the
per-package lines into the columna-core / columna-server CHANGELOGs.**
