# CP-3 copy skeleton — every string for ratification, once and whole (v0.1, PRE-SCREEN)
**From: Claude Code, 2026-07-17. Per Huayin's ruling: the full slot inventory with DRAFTS as one
artifact — pre-screen from Huayin's desk, then ratify once and whole (no dribbling). Copy law: every
string below is Huayin's; nothing ships unratified. Drafts are in the site's register (terse, honest —
"a number owes you its assumptions"). Each slot names its home file.**

Legend: `[slot]` id · **home** · DRAFT string. Mark each ✅ ratify / ✏️ revise / ✂️ cut at pre-screen.

---

## A · The four-mood exhibit (`src/data/seeded_queries.json` labels + `ExhibitB.astro`)
The exhibit rebuilds on the ratified wheel exemplars (S-2). Button labels name the ask in plain words.

- **[A1] clarify label** · seeded_queries.json → DRAFT: *"average order value by month — which reading of `aov`?"*
- **[A2] refuse label** · → DRAFT: *"last inventory, by customer — but inventory has no customers"*
- **[A3] disclose label** · → DRAFT: *"stock summed over months, per store"*
- **[A4] serve label** · → DRAFT: *"average order value by month"*
- **[A5] disclose-leg narrative** · ExhibitB caption → DRAFT: reuse the RATIFIED wheel line verbatim —
  *"Summing `level` — a stock — over days into calendar months adds daily snapshots that do not reconcile
  along the blocked day→month axis. Columna serves the per-bucket numbers WITH a material caveat…"*
  (confirm verbatim reuse, or a shorter site cut).
- **[A6] exhibit caption (frame)** · ExhibitB.astro → DRAFT: keep current *"this is the actual wire —
  what an AI agent receives. Every answer is a pair: a result, and its disclosure. The mood is how the
  pair reads."*
- **[A7] fool-it placeholder + help** · RATIFIED (Huayin 2026-07-17): foil = **`profit_margin`** ·
  help: *"a plausible column label no one declared — watch it refuse."* (the purge includes the fool-it box).

## B · verdict badges (S-1 SUPERSEDED — sell_through_rate KILLED, Huayin 2026-07-17)
- **[B1] ~~sell_through_rate describe-card~~ — CUT.** No card for a metric that doesn't exist.
- **[B2] verdict-badge labels — SURVIVES** as the Explorer's GENERAL verdict-badge vocabulary (the badges
  were never sell_through_rate's): `verified` · `corroborated` · `untestable` · `contradicted` (lower-case,
  as-is), badge tooltip = the license basis + attestation. The Explorer badges every real declared object
  (asserts, hierarchies, fertility licenses) — the whole manifold wearing verdicts, not a mascot.

## C · `/explorer` page (`src/pages/explorer.astro`, S-4) + the component microcopy (`src/explorer/manifold-explorer.ts`)
- **[C1] page title + lede** · explorer.astro → DRAFT title: *"Manifold Explorer"* · lede: *"Every measure,
  universe, and edge in the demo Manifold — with the law that defines it, the verdict that tested it, and
  the query that shows it."*
- **[C2] search placeholder** · component `.mx-search` → DRAFT: *"search measures, universes, edges…"* ·
  empty-state DRAFT: *"nothing matches — clear the search to see the whole Manifold."*
- **[C3] triad labels** · component `.mx-law/.mx-trial/.mx-demo` → DRAFT: the triad is presented WITHOUT
  literal "law/trial/demonstration" headers (facts left, badge right, button below) — confirm, or add
  visible labels: *"defined as"* / *"tested"* / *"show me"*.
- **[C4] "copy as query" button + confirmation** · component `.mx-copy` → DRAFT button: *"copy as query"* ·
  confirmation: *"copied"*.
- **[C5] section headings** · component `SECTIONS` → DRAFT: *Measures · Derived · Universes · Asserts ·
  Hierarchies* (title-case, as-is).
- **[C6] scope note** · component `.mx-scope` → DRAFT full: *"full scope published"* · cut: *"cut: {names}"*.
- **[C7] basis / absence rendering** · component `universeCard` → DRAFT: basis shown as its word
  (`events`/`spine`/`product`/`registry`) or *"undeclared"*; absence phrase comes from core describe
  (`absence_semantics`) — confirm those phrases (*"absence is a lawful ZERO…"*, *"absence is a GAP…"*,
  *"membership is a checkable fact…"*, *"undeclared (absence-semantics inert…)"*).

## D · `src/data/wire_strings.json` — governed reason-code strings (copy law)
Friendly communicative strings for the reason codes the new exemplars + §2c surface:
- **[D1] `cross_universe`** · → DRAFT: *"this asks one number of two populations — a category error, not
  a caveat. Ask each population separately, or reconcile them first."*
- **[D2] `b_anchor_crossing` / `blocked_reduction`** · → DRAFT: *"this sums a stock across a blocked axis;
  the per-bucket totals don't reconcile. Served with the caveat, never as a silent total."*
- **[D3] `incomplete_data` / `data_gap`** · **DOES NOT SHIP this beat.** S-5 BASIS landed
  (store_days=spine), but the recapture shows the seeded queries hit NO grid gap → no `incomplete_data`
  surfaces. Per the ruling ("[D3]'s string ships if the grid has gaps"), it's held until a query gaps.
  DRAFT retained for when it does: *"some expected rows are absent — a gap, not a zero. The figure covers
  what's present; the gap is disclosed."* Teaching surface NOT lost meanwhile: C-7's universe cards render
  the declared absence semantics as TEXT ("absence is a GAP…") even while no query fires them.
  **Post-launch candidate (Huayin 2026-07-17, recorded not built):** a deliberately-seeded gap exhibit (a
  store dark for a day) to fire `incomplete_data` live — a launch+ enhancement, not this beat.
- **[D4] `input_anchor_ambiguous`** · (the standing CP-M1 gap) → DRAFT: *"this reduction needs to know
  which input grain to read `aov` at — pick one, and the number is exact."*

## E · Homepage entry point (`src/pages/index.astro`)
- **[E1] `/explorer` entry copy** · index.astro (compact link from the exhibit) → DRAFT: *"Browse the whole
  Manifold → the Explorer"* (links to `/explorer`).

---

## Notes for the pre-screen
- **Reuse vs re-author:** [A5]/[A6]/[B2]/[C5]/[C7] propose REUSE of already-shipped/ratified strings —
  flag any you want re-authored.
- **S-5 dependency:** [D3] ships only if the demo-BASIS add lands (your S-5 YES → it does; confirm the string).
- **The triad labels [C3]** are the one genuine design choice — labelless (cleaner, reference-dense) vs
  labelled (*defined as / tested / show me*). Your call sets the component's final microcopy.
- On ratification I fold the exact strings into `seeded_queries.json`, `wire_strings.json`,
  `manifold-explorer.ts` (replacing the `COPY:` drafts), and the `/explorer` + homepage pages — one pass,
  then the S-3/S-5 recapture returns to you with the seeded-number diff.
