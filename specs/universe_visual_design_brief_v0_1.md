# The Universe Visual — design brief (v0.1, ratified at the desk)

*The spec's Figure 1: a static, generated visual of a manifold's universes. Ruled by
Huayin after the tier-3 cancellation — image OF the understanding, not machinery
beside it. Realistic, simplistic, less dramatic. Details may be left out: the
text-based Manifold spec holds the completeness; the visual holds the intuition.*

## The organizing principle

UNIVERSE-FIRST, not atlas-first. Levels and paths are shared infrastructure; meaning
lives in universes. Each universe is a box containing its bases, its reachable
hierarchies, and its metric families. The atlas appears only as what universes share.

## The elements

1. **Stacks** — each hierarchy is a stack of level blocks, BASE at the bottom.
   Branching hierarchies FORK: calendar renders day → month → quarter → year rising,
   with day → week as a short offshoot sharing the base segment (weeks don't nest —
   the fork is the lesson). Single-level dimensions are one-block stacks.
2. **The floor is the grain** — all base blocks sit on the box's floor, left to
   right: the universe's anchor signature visible before any label is read
   (transaction: customer · store · product · day; inventory: store · day).
3. **Basis as floor texture** — solid floor = `events` (absence is a lawful zero);
   grid-hatched floor = `spine` (a grid that can have holes). The carve
   (`day >= store.opened`) renders as a small clamp-note on the inventory box edge.
4. **Metric families** — listed inside their home box, per-family with members shown
   (stock: sum, last). Deriveds render as GHOST/OUTLINED rows showing the formula as
   the row itself (`aov = revenue / orders`) among solid measure rows.
5. **Hover = the member, not the family** — hovering a family MEMBER highlights its
   anchor (the base blocks) and paints each stack by traversability, in the FOUR-MOOD
   PALETTE the site already speaks (the /case wheel colors):
   - green — travels clean (serve);
   - amber — travels with a material caveat (the spine's gap territory / disclose);
   - red — barred (a B-anchor bar: stock.sum burns calendar red; stock.last turns
     the same stack green — the hover pair IS the first burn, taught).
   Hover is CSS-class-only. No state, no JS framework, no explorer apparatus.
6. **Multi-universe overlap** — boxes overlap PHYSICALLY where they share dimensions;
   shared stacks (store; day+calendar) draw ONCE in the overlap region. Metric
   families NEVER overlap (measures and deriveds are homed in exactly one universe —
   ratified law). The overlap region is where cross-universe juxtaposition lives; the
   Venn geometry is the co-anchoring rule made visible.
7. **RELATE as a dashed link** — product ↔ category as a dashed connector to a
   category block belonging to NO stack. Dashed = non-functional = visually
   unclimbable: the category-clarify's geometry.
8. **Badges pinned to REAL verdict objects only** — the visual never invents claims:
   hop badges on stack seams (corroborated); the basis badge on the box
   (untestable — honest); the assert (`returns_bounded`) as a small plaque inside
   its box. Verdict colors/glyphs identical to the trial table on /case.
9. **Left out, deliberately** — logical attributes, the map's reject rows, operator
   properties, provenance: the spec and the map hold the details; the visual holds
   the shape. A caption under the visual links both.

## The construction law

GENERATED, NEVER HAND-DRAWN: build-time SVG from `describe` output only — auto-true
as the manifold evolves, wall-safe by construction (describe is the sole source; the
standing no-physical-leak discipline covers it). Hover via CSS classes embedded in
the SVG. The generator fails closed on unknown describe content (a new declaration
kind must be taught, not silently dropped).

## Placement

The hero of /explorer: the visual on top, the existing cards-with-descriptions below
(the Option-A beat proceeds unchanged as the page's bottom half), the Manifold spec
and the physical→logical map linked beside the caption.

## The gate

ONE RENDERED MOCKUP of Cascadia's two universes — transaction and inventory, the
overlap, the fork, one hover state shown (stock.sum red / stock.last green as a
side-by-side pair since a static mockup can't hover) — to Huayin's sight before the
generator is built. Copy law on every string in the visual (labels come from
describe verbatim; captions are ratified copy).
