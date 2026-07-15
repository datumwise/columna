# Design capture — the Manifold as material artifact: Authoring, Explorer, and the tier-2 WP
**v0.1 · RATIFIED in session (Huayin, 2026-07-15; §7 forks remain open by design for the tier-2 WP's CP-0) ·
supersedes the 2026-07-14 SCAFFOLD · feeds: the on-ramp + Explorer tier-2 WP brief ·
routing: specs/context/ on ratification, alongside the execution-positions capture**

## 1 · The component map (RATIFIED)

The **Manifold spec is the system's one material artifact**: Authoring produces it;
Explorer, Planner, Metric Engine, MCP, and every future surface consume it; no external
surface ever touches the physical layer. The artifact is two layers, today fused in one
file: the **Law** (universes, levels, edges-with-lineages, measures with anchors and
families, derived formulas — pure logic) and the **Map** (Law → physical materialization).
Consumers sort cleanly: **Law-only consumers** (Explorer, MCP, agents, the wire, via
describe) and **Law+Map consumers** (Planner/Metric Engine, via the connector) — the
ADR-031 seam, restated from the artifact side.

**The two-output rule (RATIFIED):** Authoring tools produce two outputs — the manifold
(Law) and the Map. v1 sequencing: `columna init` emits today's fused `.cml` (the Map's v0
form is the inline `FROM`/`VIA` binding fields); the artifact split into separable
Law/Map lands at the Authoring-era WP, which needs the Map as a first-class concept
anyway. Either way, the insulation guarantee holds NOW (§2).

## 2 · The formal representation (RATIFIED) and the insulation guarantee

**Three layers** — the `.cml`'s own organization, ratified as the formalism:
- **Coordinates** — levels plus functional edges, the *shared* coordinate atlas. A rollup
  (`day → cal.month`) and a cross-table relationship (`store → region`) are the same
  declared thing: a functional edge tagged with a lineage. Lineage namespaces (`cal.*`)
  are the dimension families.
- **Populations** — universes as carved products of base levels
  (`transactions = customer × store × product × day`; predicates carve).
- **Functions** — measures anchored on populations; families govern travel (member
  reducers, `BLOCKED` per lineage = B-anchor, `ORDER` for ordered monoids, `M_ANCHOR`
  leak; V rides describe); derived columns close the algebra. Tier
  (additive/sketch/holistic) is operator-level, from the registry — never declared on
  the measure.

**Universe connection — three ways, asymmetric by design:** (1) shared base levels — the
primary mechanism; where co-anchoring, cross-population ratios, `ON UNIVERSE` pins, and
`co_anchor_ambiguous` live; (2) functional edges — universe-agnostic coordinate motion;
(3) `RELATE` — declared M:N, existing so fan-out refusals can name the edge: a connection
declared in order to refuse honestly, never to transport.

## 2a · Anchors and the top of the lattice (RATIFIED 2026-07-15; wire-verified)

**The anchor:** *coordinates are the space; an anchor is an address in it* — the grain at
which a column's values are keyed; a choice of resolution per coordinate. Three roles at
once: the **key** (where the values live), the **input to legality** (transport is motion
between anchors along functional edges, judged per lineage), the **site of combination**
(the denotation rule: formulas evaluate over co-anchored atoms at the anchor). V/M/B are
each measure's **declared physics of motion** in this space: B = barred directions, M =
the measurement's own leak beyond its key, V = validity semantics on describe.

**The top (Huayin's unification):** each universe has a terminal level **⊤_U** — the
universe collapsed to one point; every lineage's final edge lands there. ⊤ is
per-universe (⊤_transactions ≠ ⊤_store_days: different populations' grand totals). Each
universe's anchor space is a **bounded lattice** [⊥_U = the atoms, ⊤_U = the grand-total
cell]. **The unification theorem: removing a dimension is not a special operation — it is
ordinary lineage transport, the last edge.** One law of reduction everywhere; "sum over a
dimension" (old lingo) = transport to ⊤ by the family reducer. Corollary: with ⊤_U
terminal, every level has a path to it — *a universe's coordinate graph is connected.*

**Wire-verified (2026-07-15):** the shipped planner already implements the unification —
an absent coordinate is at ⊤, and collapse counts as crossing the lineage:
`level.sum @ region` fires `blocked_reduction` (material, critical) with detail
"collapses dimension 'day' along blocked lineage 'calendar'" and a remedy naming `.last`;
`level.last @ region` and `revenue @ region` serve clean. On record as shipped design: at
the wall, the mood for a monoid reducer is disclose-critical-with-remedy, not refuse
(distinct from the materialized-metric refusal).

**The one gap the formalization exposes:** ⊤ has no syntax — the parser requires ≥1 level
after `@`, so the one-cell grand total is inexpressible today. Grammar-growth candidate
per ADR-035 D1 (enters by ruling; surface spelling is Huayin's ear-call when wanted).

**Terms ledger:** *coordinate = lineage = dimension family* — "lineage" canonical in code
and doctrine; "coordinate" the formal-picture word; "dimension family" the industry-facing
gloss.

## 2b · The anchor expression grammar (RULED 2026-07-15; grammar-growth per ADR-035 D1)

- **Formal names (RULED 2026-07-15): level names are globally unique across dimension
  families.** Rationale (Huayin): same-short-name levels make `revenue @ week` dubious
  but UNDETECTABLE — the naming law forces distinct concepts to distinct names
  (`week` / `fiscal_week`), surfacing ambiguity at authoring as a well-formedness error,
  never at asking. Dimension families **cover, not partition**: a level belongs to one
  or more families (`day` ∈ cal and bus_cal — the same level), and **membership is
  edge-derived** — level ∈ family iff it touches an edge of that lineage; no new
  declaration exists. `family.level` is qualified-and-usable, validated against
  edge-derived membership — chiefly a documentation/pinpointing instrument; the bare
  level name is expected almost everywhere, by its uniqueness. (Contrast: measure
  families partition their members.) **Anchoring is family-agnostic; travel is not** —
  the anchor names a position; fertility and B-anchors are per-lineage. The shadowing
  ban extends: aliases and operator overrides never enter the level namespace.
- **The anchor product:** `*` — the SAME operator as `UNIVERSE ... = a * b * c`.
  General form: `revenue @ region*day`. **RULED (a):** keep-both through launch — `*`
  canonical in all system output, comma accepted on input; the comma retires in the
  post-launch grammar-hygiene sweep.
- **Resolution order (standing rule; CORRECTED 2026-07-15 — no demo fix is owed):**
  a literal level-name match wins (dotted stored names like the demo's `cal.month` are a
  legitimate authoring style); otherwise the token splits and resolves as family.level.
  Well-formedness forbids the one bad state: a single token reaching two levels (fail
  closed, both sites named). The post-launch hygiene sweep is the comma retirement ONLY.
  **Bare family names are definition-language citizens (`ALONG`/`BLOCKED`/`FERTILE`) and
  query-language non-citizens (qualifier prefixes only)** — queries name positions;
  definitions legislate motion. (Cosmetic note, never owed: the demo's `cal.` prefix
  predates the family concept — its lineage is named `calendar`.)
- **The grand total (RULED 2026-07-15): expressible where anchors are data, unspelled
  where they are strings.** The engine already serves the empty-tuple anchor
  (`planner.run((), …)` → serve; wire-verified) — the grand total exists at the
  API/tool/agent layer, where an empty tuple is an honest value. The string grammar
  deliberately does not spell it: `()` WITHDRAWN (a token relating to no family, absurd
  under many-family universes), bare/empty stays rejected (the FOOL-query shape). Closed
  by deferral per ADR-035 D1 — if a string-surface need lands, Huayin's ear rules the
  spelling then, with usage evidence. Partial omission stands as shipped law (absent
  dimensions are at ⊤; §2a).
- **Citizenship, completed (RULED 2026-07-15) — the two sides invert.** Dimension side:
  the LEAF is the query-language citizen (bare `region`, unique); the family is
  prefix-only in queries, full citizen in definitions (`ALONG`/`BLOCKED`/`FERTILE`).
  Measure side: the FAMILY is the query-language citizen — the askable form is
  `family @ anchor` (`revenue @ region`), the default member resolving behind it;
  `family.member` selects a non-default member; bare members never stand alone. Anchors
  name positions, so leaves; asks name quantities, so families. A measure term without
  an anchor (inside a derived formula or expression term) takes its context per the
  denotation rule — the universe implied, atoms co-anchored where evaluation happens; a
  top-level query still requires its `@`.
- **Universe names never appear in anchor position (RULED):** universes and levels live
  in disjoint parser namespaces; a universe name after `@` is rejected with a pointed
  error. Populations ride `ON UNIVERSE`, explicit or implied, and nowhere else.
- **Sequencing (RULED (a), 2026-07-15):** the grammar rulings land as a small parser WP
  BEFORE the manuals merge — Ch. 2 documents the ruled grammar; Ch. 6 regenerates
  against it. Merge order: parser WP → manuals CP-M2 merge.

**The insulation guarantee (RATIFIED, this WP):** *no physical identifier ever crosses
describe or the wire.* Two shipped leaks are closed in this WP: `dimensions[].realized_by`
leaves describe, and universe predicates are rendered logically (no raw `table.column`
references). A standing test enforces the guarantee. Capture item carried with it: levels
need a logical dtype (today the Map supplies it); declared at the Law level when the
artifact splits.

## 3 · The Map doctrine (RATIFIED)

The mapping is **N-to-1**: N physical materializations (table, view, file columns) → 1
logical family member. The Map is therefore a **materialization inventory**, entry schema:
*(family member, anchor, physical object, dtype, attestation ref)*. Consequences:

- **Warehouse rollup tables, Cacher entries, and connector delivery targets are the same
  object** — a materialization of a family at an anchor — governed by the same laws.
- **The materialization admission law (RATIFIED):** serving from a materialization not at
  the atoms is a fertility question. Only the fertile may be served from a pre-reduced
  materialization; an infertile member's rollup serves only identical hits;
  never-substitute applies verbatim. A rollup table is a cache entry somebody else built.
- **Attestation is per-materialization.** Verdicts live on (Law × Map-entry ×
  attestation): a CORROBORATED license watermarked to the fact table says nothing about
  the rollup view until it is attested. The classic "is this aggregate table still right?"
  becomes a per-entry verdict.

## 4 · Operator doctrine (RATIFIED)

The four levels factor into two orthogonal structures:

**The semantic chain** (what an operator *is* and is *called*):
1. **Framework Library** — the standard set, versioned with columna-core, shared by every
   installation; VERIFIED by construction (ships with proofs/tests).
2. **Site Library** — the installation's genuine extensions; enter through the onboarding
   contract with **claimed properties adjudicated by the Certificate kernel** (RATIFIED:
   math verifies compositions of knowns; data corroborates/refutes opaque ones; UNTESTABLE
   stands asserted-and-disclosed; CONTRADICTED fails registry entry closed). The registry
   is the Certificate layer's future customer; build when the first custom operator asks.
3. **Manifold name-overrides** — per-manifold, inheritable, possibly empty; communicative
   metadata only.

**The execution maps** (how a resolved operator runs): per-connector maps standard →
backend expressions for per-column ops (Map-side; certified-delivery parity suite);
Combiner-substrate implementations for all cross-column work (never mapped to backends —
hard-NO pushdown).

**The governing rule** — the decidable test applied to operators: changes legality or
value → Site Library entry, adjudicated; changes only the name → manifold override,
weightless. **Mini-fork A (RULED): the shadowing ban** — overrides may introduce new names
for existing operators; they may NEVER rebind a framework or site name to different
semantics; parser-enforced; same collision law as ALIAS. **Mini-fork B (RULED): resolve at
parse/publish time** — plans, wire, describe, and cache keys carry only resolved standard
identities; the local name rides as communicative provenance. Names cannot fragment the
cache; resolve early, remember the costume, key on the substance.

## 5 · Authoring (RATIFIED doctrine; built later; init is the first slice)

Huayin's workflow maps 1:1 onto the constitutional sentence: agent inference → PROPOSALS
carrying `INFERRED_*` grades (*data may suggest, never grant*); human change/approve →
the DECLARATION act (*authority is declared*); agent verification → the adjudication
channels (*mathematics may verify; data may only refute or corroborate*); publish →
default closed (CONTRADICTED fails). **The durable contract is the artifact state
machine:** `scoped → proposed → declared → attested → published`, grades and verdicts
riding every declaration. The multi-context module architecture (database / code / docs /
semantic-layer adapters; persona: the data engineer) is the later product; **`columna
init` is Authoring's database-context slice** — same state machine, one context, two
outputs per §1, no adapter framework in v1 (YAGNI guard).

## 6 · Explorer tier 2 (RULED)

- **Data path (by shipped precedent):** extend the existing build-time capture pipeline —
  `gen_transcript.py` runs the shipped package, fails the build closed on drift; the
  Explorer is structurally incapable of showing a manifold the package didn't describe.
  Friendly strings only from governed `wire_strings.json`, templated from structural
  fields; the **wire-strings coverage check** ships as a build-time assertion (every
  shipped reason/code has a string; `input_anchor_ambiguous` is the known gap).
- **Scope IN (RULED):** (a) licenses + verdicts on derived members — VERIFIED (timeless) ·
  CORROBORATED (watermark shown) · UNTESTABLE (asserted, says so); (b) fertility made
  visible — per member per lineage, askability vs travel, extending the shipped
  legal-cone display with the license that opens each direction; (c) ALIAS rendering —
  the wardrobe on the one anchored object; (d) resolution anchors on `AT` metrics;
  (e) an Operator Registry panel — kind, monoid, linear: the same facts the adjudicator
  reads (and, per §4, the resolved-name discipline made visible); (f) declare
  `sell_through_rate` as a proper DERIVED in the demo manifold — retiring tier 1's
  provenance-labeled workaround and putting a live verdict badge on the demo's own metric.
- **Scope OUT:** visual anchor-lattice map (tier 3); query playground beyond the seeded
  set (live-compute era); search/filter polish.
- **Home (RULED):** a standalone **`/explorer`** page; the homepage exhibit keeps a
  compact entry point linking in. New page copy is corpus-sourced under the copy law and
  lands before the freeze or explicitly after launch — Huayin's sequencing call at freeze
  time.

## 7 · Forks remaining for CP-0 of the WP (open; positions sketched)

- **A1 · init inference sources** — catalog only vs catalog + sampled data; what each may
  propose (universes/levels from tables+keys; edges from FKs + observed functional
  dependence; measures from numerics; calendar detection).
- **A3 · draft vs publish-attempt** — position: init emits a draft artifact that cannot
  publish until reviewed; publish is an explicit act (degradation toward correctness).
- **A4 · interaction model** — one-shot vs interview vs generate-then-annotate; an agent
  running init is a first-class caller.
- **A5 · the never-infer set** — enumerate explicitly; fertility is on it always; B-anchor
  bars propose-only at strongest grade.
- **B1 · ASSERT semantics** — what is assertable; channel mapping; violated-then-revoked
  disclosure behavior.
- **B3 · UNIVERSE BASIS** — what each basis type licenses/verifies; material disclosures.
- **C1 · ALIAS syntax** — `ALIAS <name> FOR <target>`; target kinds; collision law per
  §4's shadowing ban; chains banned.
- **D1 · describe schema** — extend the shipped per-kind shape additively; License block
  reused verbatim across fertility/hierarchy/assert; versioning posture vs the wire
  contract.
- **CP structure** — proposal: CP-0 (this capture + A/B/C/D rulings) → CP-1 syntax +
  adjudication → CP-2 init slice → CP-3 describe + Explorer → CP-4 full diff. Certificate
  kernel reused unchanged; any License schema change is a named checkpoint fork.
