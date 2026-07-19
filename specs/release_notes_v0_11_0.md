# Columna 0.11.0 — release notes (DRAFT — to Huayin's gate)

**From: Claude Code, 2026-07-19. The span since 0.10.0, in the house register. NOT YET RATIFIED — this
draft awaits Huayin's gate; on ratification it becomes the body of the GitHub Release and the source of
the `columna-core` 0.11.0 / `columna-server` 0.6.0 CHANGELOG entries.**

---

## Columna 0.11.0

*The many-to-many crossing executes — the overlap counted, and stated.*

0.11.0 is the release where the **RELATE** — the anti-edge, the relationship that declares "connected,
and no lawful rollup exists" — stops merely *refusing* a category rollup and starts *answering* one,
lawfully. A relationship may now declare **faces**: named crossing dispositions. The first,
`touch`, executes. `columna-core` reaches **0.11.0**; `columna-server` reaches **0.6.0**.

### The crossing executes (`columna-core` 0.11.0)

- **`RELATE` declares FACES.** `RELATE a <-> b VIA t(fcol, tcol) FACES { touch = TOUCH -- "folklore" }`.
  A face names the value's **disposition on the trip** across a non-functional (M:N) edge — the
  self-teaching verb triad **`touch`** (the value reaches every match), **`assign`** (it goes to exactly
  one), **`alloc`** (it splits across) — never the selection criterion, which lives in the declaration.
  The bare `VIA <table>` form is unchanged, so existing manifolds parse byte-identically.
- **`touch` executes; `assign`/`alloc` are declared-but-deferred.** `SELECT revenue AT {category.touch}`
  join-multiplies the measure through the relationship's bridge to the crossed grain: the value reaches
  every category a product sits in, deliberately multi-counted, served in **disclose** with the
  over-count as a material caveat. `assign`/`alloc` parse to an honest, fail-closed refusal — v1 executes
  `touch` only. The bare `{category}` stays barred and now clarifies with the **face menu**.
- **The two skews of a crossing, both disclosed.** Over-count (per-bucket totals overlap; the sum
  *exceeds* the grand total) and its mirror, coverage/shortfall (a fine entity in no bucket is excluded
  from every cell, so the total can fall *short*). The crossing reports its coverage either way.
- **Crossed-grain absence is a lawful zero — events basis only.** On an events population the expansion
  is honest arithmetic; on a spine/grid, replication would corrupt the grid's own completeness claim, so
  the crossing is refused there until that thinking lands.
- **Adjudicated at publish, under the polarity law.** A face is closed by default; its license *opens*
  the crossing, minted only by the adjudicator (never on parse). `touch` = VERIFIED — membership
  expansion is exact arithmetic, no partition-of-unity to reconcile.
- **The `VIA` bridge is map-layer.** Engine-visible (the join-multiply needs it), describe-invisible — it
  never rides `relates[]` or any wire; the insulation test asserts it. `contract_version` stays `"1"`.

### The crossing goes visible (`columna-server` 0.6.0)

- **`describe_manifold`'s `relates[]` gains `faces[]`** — each declared disposition rides describe as
  data (`{name, scheme, description}`), so a consulting agent and the clarify-menu see it from the source
  of truth. Additive; `contract_version` stays `"1"`.
- **Cascadia declares `FACE touch`.** The demo *shows* the crossing: `SELECT revenue AT {category}`
  clarifies with the face menu; `SELECT revenue AT {category.touch}` executes — **12 categories, touch
  total $3,182,555.97 vs. grand total $2,212,391.86** (the ~$970K overlap stated), 600/600 coverage.
- **The recapture corpus grows to ten (E1–E10).** E6 records the face menu (the ask, with its reason and
  the way forward); E10 mints the executed crossing (the answer — disclose, over_count, coverage). Zero
  drift flags.

### The honest ledger

`assign` and `alloc` are on the record as the next faces — the crown is `alloc` (the partition-of-unity
that makes per-bucket totals *reconcile*), and the shipped `WITH allocation` grammar is its parameter.
The spine-basis crossing (replication on a grid) waits on the spine-grid domain source (OF-5). Both
named, neither promised.

*The whole crossing — the declaration, the menu, the executed answer with its overlap stated — ships in
the Cascadia demo. `pip install columna`, and ask for revenue by category yourself.*
