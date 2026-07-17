# CP-3 opening proposal — describe + Explorer + the site beat (v0.1, APPROVED 2026-07-17)
**From: Claude Code, 2026-07-16. The last track, launch-critical under Plan B. Proposals-first (CP-2's
rhythm carried in): (a) the code-half increments, (b) the site-beat, (c) the copy skeleton. APPROVED by
Huayin 2026-07-17 with all decisions ruled — see "RULINGS" at the foot. Standing laws restated there.**

## Sourcing note (label reconciliation — so the ground is honest)
- **"Q7 insulation closure"** — there is no `Q7` label in the capture or repo. The ruled content Huayin
  named is capture §2b **"the insulation guarantee (RATIFIED)"**: *no physical identifier ever crosses
  describe or the wire*; two shipped leaks to close (`dimensions[].realized_by` leaves describe; universe
  predicates render logically). I carry it under both names.
- **The demo-BASIS flag** lives in the tier-2 brief (`wp_onramp_explorer_tier2_brief_v0_1.md`, increment-6
  note), not the capture. The absence-semantics LAW it rides on is capture §7 B3.
- **D1** and the **Explorer posture** are ratified in the capture (§7 D1 "closed by assembly"; §6 "Posture
  RULED"). Everything below traces to those.

---

# (a) The code half — increment plan (additive, each tested, contract_version stays "1")

### C-1 · The D1 describe extension (capture §7 D1 — additive to the shipped per-kind shape)
Today `describe_manifold`/`describe_measure` (server `tools.py`) + `describe.py` (`license_to_dict`,
`describe_derived`) emit dimensions/edges/universes/measures/derived. D1 extends this ADDITIVELY:
- **License blocks verbatim across fertility · hierarchy · assert.** `describe_derived` already carries the
  fertility License per member; extend the same `license_to_dict` block to HIERARCHY members and ASSERT
  members (the kernel mints one byte-identical License schema for all three). No new schema — the same block.
- **Signature addressing** — a member's operator signature (kind, is_monoid, arity), **universe-qualified
  where a member name duplicates across universes** (so the address is unambiguous when the same reducer
  name recurs). `describe_measure` already exposes `reducer_kind`/`is_monoid`; add the universe-qualified
  address form.
- **Basis type + absence semantics (B3)** — `describe_manifold`'s universe blocks today carry only
  `base_dimensions` + `predicate`; add **`basis`** (events|spine|product|registry) and its **absence
  meaning** (events→zero-fill+immaterial; spine/product→`incomplete_data` material gap; registry→membership).
- **Published-scope vs cut display (B1)** — surface each member's **scope state**: published vs cut regions
  (from the cut-set / adjudication), so a contradicted edge / cut assert shows as blocked, not absent.
- **Operator properties (registry describe)** — the operator registry's properties (kind, monoid,
  applicable-along) surfaced for each reducer.
- **NO alias block (C1).** Aliases were struck; describe adds none.
- **CV discipline:** additive under the tool-surface discipline; any shape question at CP is a CV-ledger
  line, not a redesign. `contract_version` unchanged.

### C-2 · The insulation closure ("Q7" = §2b insulation guarantee)
*No physical identifier ever crosses describe or the wire.* Close the two shipped leaks + pin the guarantee:
- **`dimensions[].realized_by` leaves describe.** `describe_manifold` currently emits `realized_by` per
  dimension (a physical identifier) — remove it from the describe output.
- **Universe predicates render logically.** `_render_predicate` already renders logically; audit it emits
  no raw `table.column`, close any residual leak.
- **Levels carry a logical dtype** (the Map supplies it today) — describe surfaces the logical dtype, never
  a physical one.
- **The STANDING no-physical-identifier test** — a test that asserts describe (and the wire) output for the
  demo + fixtures contains no physical storage identifier (table/column names, `realized_by`, raw SQL). This
  is the guarantee's enforcement, standing.
- Proposed to land **with C-1** (both edit the describe surface); one increment, "describe v-next."

### C-3 · The Explorer tier-2 component (capture §6 Posture — RULED, working-user-first)
- **A COMPONENT that binds ANY describe artifact, zero site-specific coupling.** It consumes the describe
  dict (C-1's shape) and renders it; the site's `/explorer` is merely its demo-manifold instance.
- **IA: reference-first, measure-first, searchable** — dense, daily-use, one click deep (not narrated).
- **The law/trial/demonstration triad** per fact: **law** = the describe facts (basis, absence, signature,
  scope/cut); **trial** = the adjudicated License verdict (the badge); **demonstration** = **"copy as query"
  primary**, with demo-player wiring ONLY on the site instance.
- **Functional microcopy under the copy law** (not narrative corpus prose).
- **Home question (proposed):** build the component **in `apps/website/` for CP-3** (the site instance),
  authored to bind any describe artifact so the **package-served deployment** (`columna-server` offering the
  Explorer against a live manifold) is a clean near-future lift — recorded, NOT CP-3 scope. *Confirm this
  home, or rule the component belongs in the package now.*
- **Inherited, not re-decided:** §7 B1 (the Explorer shows published-scope vs cut regions) and §7 D1 (the
  describe schema it binds to).

**Proposed code sequence:** C-1 + C-2 together (describe extension + insulation closure, same surface, one
tested increment) → C-3 (the Explorer binds the extended describe). Each is a checkpoint.

---

# (b) The site beat — plan
The live exhibit (`ExhibitB.astro` + `seeded_queries.json` + `gen_transcript.py`) still runs the **old
cross-universe wedge** (`sell_through_rate: revenue / level.last`) for clarify+refuse — which now **errors**
under §2c (the drift-guard is tripping on exactly this). The beat rebuilds it on the shipped law.

### S-1 · Declare `sell_through_rate` properly (capture §6 scope f)
Add it to the demo `manifold.cml` as a real **DERIVED** with its family + **declaration-time population**
(§2c — the pin lives in definitions), retiring tier-1's provenance-labeled inline workaround. It then has a
real **describe object** and a **live adjudicated License verdict** → the **verdict badge** on the demo's
own metric.

### S-2 · Rebuild the four-mood exhibit on the ratified exemplars (mirror the shipped wheel tour)
Replace the erroring seeded queries with the wheel tour: **clarify** `avg(aov) @ cal.month` · **refuse**
`level.last @ customer` · **disclose** `level.sum @ store*cal.month` · **serve** `aov @ cal.month`. The
exhibit mirrors `demo --play` (one source of truth), and the drift-guard tripwire clears.

### S-3 · The seeded recapture (REQUIRED — a checkpoint recapture)
`gen_transcript.py`'s `SEEDED`/`WEDGE`/`SEPARATE`/`SERVE`/`FOOL` re-pointed to the new exemplars →
regenerate `transcript.generated.json`. **This moves seeded numbers** (the drift-guard is the tripwire that
must pass on the new law). Also fix the **dangling `gen:transcript` npm script** (points to a non-existent
`gen_transcript.mjs`; CI calls the `.py` directly — align them).

### S-4 · The `/explorer` page (capture §6 Home — RULED)
A standalone **`/explorer`** page = the Explorer component's demo-manifold instance, bound to the demo's
describe artifact; the homepage exhibit keeps a **compact entry point** linking in.

### S-5 · The demo-BASIS question (increment-6 flag — HUAYIN'S CHECKPOINT DECISION, one recapture)
**Should the demo manifold gain BASIS declarations?** For: the **honest zero in a juxtaposition** (events
absence rendered as 0, alongside a spine gap) is strong exhibit material for the four moods / the Certificate
layer — it would let the disclose leg *show* absence semantics live. Against: it is **one recapture** (adding
BASIS moves seeded numbers; the drift-guard trips until regenerated); absence semantics is shipped and inert
on the basis-less demo today. **Decision yours** — add BASIS (one recapture, richer exhibit) or leave inert.

**Recaptures on the table:** S-3 (required, the exemplar swap) and S-5 (optional, the BASIS add) — both
checkpoint decisions per the standing law; any seeded number that moves comes back to you.

---

# (c) The copy skeleton — every string needing ratification, slotted (so it arrives once and whole)
Copy law: every string is yours. Below is the complete slot inventory with a DRAFT for each (ratify/revise
in one pass); nothing is final until you rule.

**Exhibit (four-mood) — `seeded_queries.json` labels + `ExhibitB.astro`:**
1. clarify button label — DRAFT: *"average order value by month — which input anchor?"*
2. refuse button label — DRAFT: *"last inventory by customer (inventory has no customers)"*
3. disclose button label — DRAFT: *"stock summed over months, per store"*
4. serve button label — DRAFT: *"average order value by month"*
5. disclose-leg narrative (mirror the ratified wheel line) — DRAFT: the wheel's *"Summing `level` — a stock
   — over days into calendar months adds daily snapshots that do not reconcile…"* (already ratified for the
   wheel; confirm verbatim reuse on the site).
6. exhibit caption — keep current *"this is the actual wire…"* or revise.
7. fool-it placeholder/help — updated for the new exemplars.

**`sell_through_rate` — describe card + badge (`ExhibitB` / Explorer):**
8. verdict-badge label copy (per verdict: verified / corroborated / untestable / contradicted).
9. the describe-card one-liner for the metric.

**`/explorer` page — `explorer.astro` + component microcopy:**
10. page title + lede.
11. measure-first search placeholder + empty-state.
12. the law / trial / demonstration triad labels.
13. "copy as query" button label + copied-confirmation.
14. section headings (measures · universes · edges · derived).

**`wire_strings.json` — governed communicative strings (copy law) for reason codes newly surfaced:**
15. `cross_universe` friendly string (the retired wedge now lands here).
16. `b_anchor_crossing` / `blocked_reduction` friendly string (the disclose leg's caveat).
17. `incomplete_data` / `data_gap` friendly string (if S-5 BASIS lands).
18. `input_anchor_ambiguous` (the standing coverage-gap string, still unfilled per CP-M1).

**Homepage:**
19. the compact `/explorer` entry-point copy (links from the exhibit).

---

## Standing laws (all live at this checkpoint)
- **Copy law** on every string above — none ships unratified.
- **Nothing merges to `apps/website/**` without Huayin's explicit go.**
- **Deploy sequencing** (the `/explorer` page + the exhibit rebuild: before-freeze or after-launch) is
  **Huayin's call at this checkpoint.**
- **Recaptures are checkpoint decisions** — S-3 (required) and S-5 (optional) both return to you; any seeded
  number that moves is surfaced, the drift-guard is the tripwire.

## RULINGS — APPROVED (Huayin, 2026-07-17)
1. **Code sequence.** **C-1 + C-2 land as ONE increment** — same describe surface, and the standing
   no-physical-identifier test is **born watching the extended describe, not retrofitted**. **C-3 follows.**
   Sourcing accepted: **"Q7" was the desk's label; the real source is §2b's insulation guarantee** — carry
   it as §2b in all artifacts (the trace-to-source was correct conduct).
2. **Explorer's home: `apps/website/` now, PORTABLE BY CONSTRUCTION** — a cleanly separated directory whose
   ROOT states the portability law (binds any describe JSON, **zero site imports, zero site coupling**).
   Package-serving is an **OF row** (recorded near-future path). **Ruled clarification (load-bearing):** the
   **Explorer does NO insulation work.** Insulation is the Manifold's own property, delivered **wholly at the
   describe layer** — **C-2 owns the wall.** Build C-3 with **no scrubbing, no filtering, no defensive
   rendering**: if anything physical ever appears in an Explorer, that is a **describe bug caught by C-2's
   standing test**, never an Explorer bug (the Explorer cannot leak what its only input never carries).
   **OF row (row it, don't design it):** an AUTHOR-facing provenance surface (FROM/VIA visible to the humans
   who declared them) is a conceivable future Explorer layer — its data could **never** come from describe and
   would need its **own governed source**.
3. **Site beat: S-1…S-4 approved as scoped; S-5 is YES.** demo-BASIS goes in, **riding S-3's already-required
   recapture** (one recapture, both changes — later would cost a second checkpoint) — and it ensures **C-1's
   new universe blocks render POPULATED** in the flagship instance (the Explorer's first impression carries no
   empty fields). The combined recapture returns to Huayin as the checkpoint decision it is, **with the
   seeded-number diff**.
4. **Copy: post the full 19-slot skeleton with drafts as ONE artifact** — it gets a pre-screen from Huayin's
   desk, then he ratifies **once and whole**.
5. **Deploy sequencing — the site flips TOGETHER with a release cut** (adds a step to Plan B). The live site
   is coherent with PyPI 0.7.8; everything since lives only on `main`. **Sequence:** CP-3 code + site beat
   ready → **cut and publish 0.8.0** (§2c, the four-mood tour, the Certificate customers, init, the shipped
   KP — **release notes to Huayin's gate**) → deploy the site → **acceptance walk on the coherent pair** →
   freeze → launch. **One flip, one acceptance surface; the wedge holds until everything moves at once.**

**Proceed (ruled):** branch `wp-cp3` → this proposal as the first specs commit → **C-1 + C-2**. Copy skeleton
and the S-beat/recapture follow; the release cut + deploy are the closing sequence, each at Huayin's gate.
