# The Manifold Explorer — a portable component (CP-3 C-3)

**The portability law (RATIFIED, Huayin 2026-07-17).** This directory is the Explorer *component* — a
COMPONENT of the product, not a site feature. Its one law:

> **It binds any `describe` JSON. Zero site imports. Zero site coupling.**

- **Input:** exactly one thing — the JSON that `columna-server`'s `describe_manifold` tool returns (the
  CP-3 C-1 shape: `dimensions · edges · universes · asserts · hierarchies · measures · derived ·
  published_scope`). Nothing else. It reads no site data, no `wire_strings.json`, no globals.
- **No site imports.** Files in this directory import NOTHING from `../` (no layouts, no site scripts, no
  site data). If you need a site thing here, you are doing it wrong — pass it as an argument.
- **The site's `/explorer` is merely an INSTANCE** of this component bound to the demo manifold's
  describe. The package-served deployment (`columna-server` offering the Explorer against a live manifold)
  is the recorded near-future path — **OF-7** — a clean lift precisely because this directory has no
  coupling to remove.

**It does NO insulation work (Huayin 2026-07-17).** Insulation is the Manifold's own property, delivered
wholly at the describe layer — **C-2 owns the wall**. This component performs **no scrubbing, no
filtering, no defensive rendering**: it renders what describe hands it, verbatim. If anything physical
ever appears in the Explorer, that is a **describe bug** caught by C-2's standing no-physical-identifier
test — never an Explorer bug. The component cannot leak what its only input never carries.

**IA (RULED):** reference-first, **measure-first** entry, searchable; every fact carries its
**law / trial / demonstration** triad one click deep — *law* = the describe facts, *trial* = the
adjudicated License verdict, *demonstration* = **"copy as query"** (the demo-player wiring lives only on
the site instance, never here).

**Copy:** functional microcopy under the copy law. The strings in `manifold-explorer.ts` are DRAFTS
pending Huayin's ratification via the CP-3 copy skeleton — they are marked, not final.
