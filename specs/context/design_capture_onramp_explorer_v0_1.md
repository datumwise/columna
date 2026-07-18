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

## 2b″ · The wall is semantic, not lexical (Huayin, explicit, 2026-07-18)

The insulation principle stated formally: the Manifold is CLOSED UNDER ITS OWN
INTERPRETATION — every expression in it must be interpretable under the Manifold's
grammar alone, and under that interpretation the Manifold is self-sufficient. The
physical→logical map is the interpretation function binding the spec to one
particular warehouse; the spec must be fully readable by someone who never sees the
map. Corollaries: (i) spelling coincidence between a logical name and a physical
column is MEANINGLESS to the wall — `ATTR units = units` is lawful because `units`
in the spec denotes the declared attribute, regardless of the binding's spelling;
(ii) the forbidden thing is exactly an expression with a free variable only the
physical world can bind; (iii) the leak checker's true spec is RESOLUTION, not
string matching — every identifier resolves within the spec's own namespace, and a
name that resolves only via a binding is the leak. Description strings are authored
prose, policed by the folklore rule, not the checker.

## 2b′ · The case is the knowledge (Huayin, 2026-07-18)

The three case-demo chapters (setup · solutioning · live) double as a ONE-SHOT
TRAINING DOCUMENT for minds: every doctrine the KP teaches by rule, the case teaches
by incident attached to an observable — which is the run-5 salience finding (triggers
beat names) in narrative form. A fresh model session is the new hire; the case is
folklore-into-the-system for minds. CLARIFIED (Huayin): "agent" means BOTH minds —
the AUTHORING agent (the chapters as craft: requirement → scoping → many-to-1
resolution → spec, sharp calls attached to incidents) and the END-USER/QUERY agent
(the chapters as context: why the manifold is shaped this way, what the moods are
for — the difference between correct relays and good ones). Consequences, per
surface: (i) the chapters join llms-full at the case-demo build — strangers' agents;
(ii) the QUERY agent's MCP knowledges gain the case — HOW it rides (always-in-prompt
vs on-demand document) is a proposal point for the recapture increment, CC proposes,
Huayin rules; (iii) the ready-made AUTHORING ratchet experiment, post-launch: KP v0.5
+ case-chapters arm vs v0.5 baseline — if the case lifts the Columna-native ◆ calls,
the KP's future format tilts narrative; a query-side effect (relay/explanation
quality) is expected but unmeasured — no serving-side eval exists yet; noted, not
claimed; (iv) all rowed, not run, until Huayin's word.

## 2a · The minimalist scoping doctrine (Huayin, 2026-07-18, case-demo redesign)

Scoping is a CHARACTERISTIC of Columna, against the enterprise-wide comprehensive-
coverage instinct of semantic-layer technologies. The principles: identify fact sources
minimally; reject layered aggregation tables (performance is the metric engine's cache
job, not a table's); drop stored calculated metrics — compute in Columna in real time;
prefer calculated dimensions to stored ones; deriveds (metrics and dimensions) are
SCOPE REDUCERS. And the load-bearing clause: **the universe definition is the upfront
data-scope contract** — products × predicate × basis declare the population the
Manifold binds to, which is what lets a stable, near-static Manifold stand safely on
dynamic physical tables. Naming corollaries ruled the same day: universes carry
SINGULAR concept names (transaction, inventory) — the universe names a concept, never
describes records or the basis; lineages name meanings (location, calendar), not
mechanisms. **Grammar ruling: EDGE is PURGED — subsumed by HIERARCHY** — an edge is a
two-node hierarchy; `HIERARCHY <lineage> { path; path }` holds branching (weeks don't
nest in months, so calendar is a small DAG), each edge carries its VIA, adjudication
tests every edge and chain, bars address the lineage whole. RELATE stays (non-
functional). Definition-language change: parser + adjudicator + .cml migration = a
ruled increment of the case-demo build WP. HIERARCHY beat DIMENSION (which names the
coordinate family, an orthogonal concept) and FD_PATH (the formal name, kept for the
manual) because it is the analyst's own word — the dual-audience requirement applied
to the grammar.

## 2 · The formal representation (RATIFIED) and the insulation guarantee

**THE NAME'S LAW (Huayin, 2026-07-17, on the origin of FrameQL):** start with DataFrame;
take the Data out and the Frame remains — still everything: a collection of column
expressions on one anchor. In Columna, columns are expressions of WHAT A THING IS, not
operational process. FrameQL says the Frame IS the query — a declared assembly, never an
operational instruction. Corollary, ruled the same day: the shipped single-expression
`@`-form is a fragment, not the language; the envelope (SELECT … AT … with its clauses,
ON dead per §2c) is the language, and it ships before launch. The planner assembles the
frame and owns the envelope's clauses; the engine computes series, envelope-blind.

**PRECISION (CP-3 C-2, 2026-07-16):** the guarantee as SHIPPED: no STRUCTURAL physical
identifier crosses describe/wire — no table names, no qualified `table.column`;
predicate attribute names render as the author wrote them (unqualified). Full
verification — declared logical names for predicate attributes — is OF-9 (a
definition-language extension, not a rendering fix). Signature addressing on the wire
is STRUCTURED, never a dotted string: a flattened address would be indistinguishable
from physicality under the standing no-physical-identifier test. The dotted signature
remains the human query syntax, untouched.

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

- **Signatures and suffix addressing (RULED 2026-07-15; supersedes the global-uniqueness
  form of this bullet).** Full signatures: dimension `universe.family.level`; metric
  family `universe.metric_family` — unique within the manifold. **The legal short forms
  are exactly the suffixes of the full signature** (`family.level`, `level`;
  `metric_family`) — a suffix resolves iff unambiguous, else the parser demands one
  segment more, naming the ambiguity. No non-suffix forms (`universe.level` is dead).
  **Uniqueness is scoped per universe**: leaf names unique within each universe's
  included levels; the same name MAY recur across universes. Metric families likewise
  (sales.revenue and finance.revenue are different metrics). **Addresses vs objects:**
  signatures are addresses; levels are manifold-scope OBJECTS that universes include —
  sharing is by identity, never by name; `transactions.day` and `store_days.day` address
  the same day. Dimension families cover, not partition; membership is edge-derived.
  **Anchoring is family-agnostic; travel is not.** The shadowing ban extends: operator
  overrides never enter the level namespace.
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

## 2c · Universe resolution: one expression, one universe (RULED 2026-07-15; supersedes the combo-law draft)

- **Resolution algorithm (memory-free end to end):** the metric resolves the universe
  (bare when unique in the manifold; `universe.metric` when duplicated); the anchor's
  levels must be included in THAT universe (`m @ a`: m and a in the same universe); the
  metric column `m @ a` is unique in the manifold or written in a longer suffix.
- **The expression law:** a column expression — math over mappers and reducers of metric
  columns — evaluates in ONE universe and never crosses the boundary. An attempted
  cross-universe expression is a language-law violation on the ERROR channel (per the Q1
  precedent: category errors do not ride the four moods), with a remedy naming the two
  legal paths: the juxtaposed form, or a proposed declaration snippet — the error that
  teaches you to legislate.
- **The frame law (juxtaposition):** a Frame-QL query is a list of column expressions,
  each from a single universe, possibly different across columns — legit IFF every
  anchor level is the SAME OBJECT in all participating universes (same-named strangers
  refuse, both named). The juxtaposed output is an alignment view, not a Frame of the
  manifold: each column keeps its own population semantics; missing where a universe has
  no atoms; per-column honesty, no false claim of shared population.
- **`ON UNIVERSE` is DEAD in the query grammar** — the expression law deleted its last
  query-side job. Cross-universe combination is an AUTHORING act: the declared derived
  carries its population choice; population syntax survives only in the definition
  language, REQUIRED on cross-universe deriveds, fail-closed if absent. (The demo's
  wedge, `sell_through_rate`, becomes the exemplar: tier-2 item f declares it properly.)
- **Single-universe sugar:** a one-universe manifold may omit the universe ceremony —
  implicit universe, `ON` clauses optional. Ratified.
- **Implementation routing:** capture-only today. Suffix addressing (universe-prefixed
  forms), per-universe uniqueness beyond the WP's amended item 2, the expression and
  frame laws, and the definition-language population requirement enter tier-2 CP-1 or a
  follow-on mini-WP — explicitly NOT the in-flight anchor WP (whose item 2 was amended
  to per-universe scope by separate instruction).

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

**The frame (RATIFIED 2026-07-15): Authoring IS an AI Agent — and one builds an agent by
building its world.** Semantic reasoning (meaning recovery from messy human artifacts) is
legit and is the entire value; the mind is rented from the frontier model; what we build
is the world: the ARTIFACT (draft format, grades, the Map), the TOOLS (catalog readers,
samplers, the adjudicator — deterministic software), the LAWS (state machine,
publish-as-author's-act, the polarity principle), and the KNOWLEDGE (manuals, captures,
describe — documentation is agent capability). Governing sentence: **agents live at the
seams; the algebra lives in the core** — the query agent at the meaning-out seam, the
authoring agent at the meaning-in seam, one algebra between them that neither can corrupt.
Consequences: A5's never-infer set is enforced as ARTIFACT well-formedness (the draft
format has no legal way to express an inferred opening — schema, not prompt); the agent's
knowledge package is doctrine under the copy law (prompt edits are rulings); testing
splits mind/world — unit tests for tools and laws, EVALS for judgment (golden authoring
benchmarks); the on-ramp WP's deliverables grow by two: the knowledge package and the
eval suite.

**The harness thesis (RATIFIED 2026-07-15):** the harnessed agent faces a
search-with-verifier problem, not a generation problem — the Certificate kernel is a
partial ORACLE (edges testable, completeness refutable, properties provable/corroborable,
well-formedness errors as machine-parseable training signal), and the loop converges
against verdicts. Three learning channels, no weights: within-session (the A4 loop),
across versions (the knowledge package under the copy law — authoring failures become
ledgered textbook edits), across time (the eval suite as ratchet; published manifolds as
worked examples). The mind stays rented; the WORLD learns. Oracle coverage map: verifiable
claims are largely the load-bearing ones; the unverifiable residue is largely
communicative (weightless by design); the honest crack — a few meaning-calls are
load-bearing AND oracle-asymmetric (basis type is the sharp case: a false spine claim is
refutable, a false events claim is not — absence-as-zero and absence-as-gap look
identical), plus universe assignment and M-leaks. The harness's deliverable is therefore
to SHRINK review to a short checklist of exactly these human calls — which also dissolves
most automation-bias risk (rubber-stamping is a disease of long undifferentiated reviews).
Strategic corollary: the harness is the compounding proprietary asset — model gains lift
all competitors equally; world gains accrue only here and improve WITH the rented mind.
**FIRST CAUSAL CONFIRMATION (run 5, 2026-07-16):** two arms, one variable (KP v0.2 vs
v0.3 salience edit), same model/scorer/benchmarks — ◆-explicitness 4/7 → 6/7, and the
crux: m-leak was NAMED in v0.2 yet silent, TRIGGERED in v0.3 and surfaced. Salience is
scaffolding, not naming. The canonical finding stands measured: the mind surfaces what
pretraining taught and stays silent on what only the KP teaches — until the world
teaches it with observable triggers.
**THE FIRST COMPLETE RATCHET CYCLE (runs 5–7, 2026-07-16, SHIPPED):** v0.3 salience
(◆ 4/7→6/7, crux confirmed) → v0.4 unfloored prune (flood win, recall cost — caught by
its own pre-registered do-not-ship clause, banked and REVERTED) → v0.5 floored prune
(n=3, pre-registered criteria both cleared: flood halved 6.67→3.33 AND recall held at
5.0; the floor precisely undid v0.4's collateral damage). Ratified → live → measured →
shipped, one honest revert in the middle. The checklist law, now doctrine (from KP v0.5
verbatim): **a long undifferentiated review re-creates the automation bias the whole
design exists to kill; a silenced sharp call re-creates the meaning-loss the whole
design exists to prevent.** The checklist is exactly the triggered sharp calls — no
fewer, no more.

**The two-ends principle (RATIFIED 2026-07-15, Huayin's generalization):** the industry's
principle is human-IN-THE-MIDDLE; Columna's is **human in the middle AND at the two
ends** — the agent operates inside a corridor whose both walls are human-designed, with
the middle reserved for contested judgment. Query agent: data end sealed by the Manifold
(the model perceives only describe metadata and lawful reduced frames — zero raw rows,
ever); action end sealed by intent-under-user's-control; the middle is CLARIFY —
human-in-the-middle machinery invoked exactly where intent is contested. Authoring agent:
data end is the connector's narrow typed API surface (deliver_*-class calls + catalog,
NOT general SQL — an exfiltrating query is structurally uncomposable); artifact end is
the draft spec whose schema cannot express an inferred opening; the middle is
declare-and-publish, the author's acts. **Precision that makes the principle honest: the
ends are GOVERNED APERTURES, not absolute walls** — the authoring aperture includes
metered samples (A1), so the claim is never "the model touches no data" but "every
boundary has a declared shape": bounded rows, profile-stats-first, and a connector-level
sampling policy w/ column masking (KNOB TO BUILD — ledgered for the enterprise era).
General form: an agent is never "connected to" anything — it perceives through declared
apertures, produces into checkable artifacts, and the judgments between belong to humans.
Positioning corollary (stance-contrast from public materials only): the neighboring bet
optimizes how fast raw data reaches the model; ours makes sure it never has to.

Huayin's workflow maps 1:1 onto the constitutional sentence: agent inference → PROPOSALS
carrying `INFERRED_*` grades (*data may suggest, never grant*); human change/approve →
the DECLARATION act (*authority is declared*); agent verification → the adjudication
channels (*mathematics may verify; data may only refute or corroborate*); publish →
default closed (CONTRADICTED fails). **The durable contract is the artifact state
machine:** `scoped → proposed → declared → attested → published`, grades and verdicts
riding every declaration. **The alternating handshake (Huayin's observation, RATIFIED
2026-07-15):** the machine is a strict human–agent alternation — human bounds
(jurisdiction), agent explores (suggestion, graded), human commits (authority), agent
tests (trial, verdicts), human publishes (commitment). Every agent turn is sandwiched
between human acts: the two-ends principle applied FRACTALLY, recurring at every step.
This is the answer to "where is the human in your authoring loop": not somewhere in it —
at every other step, by construction. The multi-context module architecture (database / code / docs /
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
  legal-cone display with the license that opens each direction; (c) STRUCK 2026-07-15 — ALIAS cut per §7 C1; (d) resolution anchors on `AT` metrics;
  (e) an Operator Registry panel — kind, monoid, linear: the same facts the adjudicator
  reads (and, per §4, the resolved-name discipline made visible); (f) declare
  `sell_through_rate` as a proper DERIVED in the demo manifold — retiring tier 1's
  provenance-labeled workaround and putting a live verdict badge on the demo's own metric.
- **Scope OUT:** visual anchor-lattice map (tier 3); query playground beyond the seeded
  set (live-compute era); search/filter polish.
- **Posture (RULED 2026-07-15): working-user-first, not a demo replacement.** The design
  goal is the working user; the launch visitor's teaching stays with the demo and the
  Ladder. Consequence — **the Explorer is a COMPONENT of the product; the site's
  `/explorer` is its demo-manifold instance.** Design constraint: the component binds to
  any describe artifact, zero site-specific coupling; the package-served deployment
  (columna-server offering the Explorer against a live manifold) is the recorded
  near-future path. IA: reference-first — dense, searchable, measure-first entry; the
  law/trial/demonstration triad tuned for daily use (one click deep, not narrated);
  demonstration leg = "copy as query" primary, demo-player wiring only on the site
  instance. Copy: functional microcopy under the copy law (not narrative corpus prose).
  Parked thought (Huayin): the Explorer-as-component may eventually influence the demo's
  future — a file note, not this WP.
- **Home (RULED):** a standalone **`/explorer`** page; the homepage exhibit keeps a
  compact entry point linking in. Page copy under the copy law lands before the freeze
  or explicitly after launch — Huayin's sequencing call at CP-3.

## 7 · Forks remaining for CP-0 of the WP (open; positions sketched)

- **A1 (RULED 2026-07-15):** catalog + scoping, with sampled data attempted — proposals
  carry the grade their evidence earns (INFERRED_CATALOG vs INFERRED_SAMPLE). Output is a
  DRAFT.
- **A3 (RULED 2026-07-15):** no publish until reviewed — the draft artifact cannot
  publish; publish is an explicit act.
- **A4 (RULED 2026-07-15):** iterate — generate, review, revise, in a loop; **publish is
  never an automatic decision: it is an author's act.** An agent running init is a
  first-class caller of the loop, but the publish act belongs to the author.
- **A5 · the never-infer set** — enumerate explicitly; fertility is on it always; B-anchor
  bars propose-only at strongest grade.
- **B1 (RULED 2026-07-15).** Assertable v1: row-level predicates on a universe +
  aggregate invariants at an anchor (cross-measure reconciliation); functional facts are
  HIERARCHY's, no overlap. Data channel only; UNTESTABLE stands asserted-and-disclosed;
  CONTRADICTED fails publish closed. **A violation on re-attestation is an AUTHORING
  EVENT, not a runtime state: it edits the published scope** — the affected region is
  CUT (queries there refuse; everything else serves untouched). Coverage v1: declaration
  granularity — the measures the assert's expression reads + their derived cone; the
  designed refinement is REGION cuts (the adjudicator's counterexamples carry
  coordinates; recording their extent enables March-refuses-February-serves), deferred
  until wanted. Wire: the refusal likely fills the RESERVED `conflicting_data` slot —
  table-check at CP, Huayin confirms the fit (S1a discipline; no minting). The author is
  summoned with three exits: fix data + re-attest · amend the assert · accept the
  reduced scope — all authoring acts in the state machine; the Explorer shows published
  scope vs cut regions (tier-2/3 display consequence, inherited not rediscovered).
  **General law (COMPLETED 2026-07-16, uniform across all three declaration kinds):
  adjudication events edit the published scope; serving never outruns the verdicts.**
  ASSERT guards truth → degrades to CUT (costs territory; `conflicting_data`) · license
  guards shortcut → degrades to RECOMPUTE (costs speed) · HIERARCHY edge guards geometry
  → degrades to BLOCKED TRANSPORT (costs the lineage's motion; `contradicted_edge`).
  First publish stays strict for all three. `reattest` is the distinct verb (Huayin,
  2026-07-16): pure recomputation of the scope from the current attestation's verdicts —
  no ratchet, symmetric (fixing the data restores/unblocks/re-licenses) — returning the
  authoring-event diff that summons the author; history lives in watermarks and the
  ledger, never in scope-state.
- **B3 (RULED 2026-07-15): basis-as-absence-semantics is LAW.** The basis type
  determines what absence means, engine-wide: **events** → absence is ZERO (counts/sums
  zero-fill lawfully); **spine** → absence is a GAP (`incomplete_data` material caveat;
  window edge semantics inherit); **product** → cartesian completeness, absence always a
  gap; **registry** → membership checkable, unknown entities are refutations.
  Adjudication per type: spine completeness refutable (found gap → CONTRADICTED);
  registry corroborates against source; an events claim is oracle-asymmetric (the
  harness thesis's sharp human call) — which is WHY its consequences are maximal law
  rather than annotation: the unaided call must at least do something the machine
  enforces everywhere. The honest zero becomes structural. Engine wiring lands with the
  on-ramp WP's B3 build; the semantics are ruled now.
- **C1 (RULED 2026-07-15): ALIAS is CUT — Huayin's razor.** SUPERSEDES ADR-034 D2 (record
  the amendment there). Rationale: (i) manifold granularity IS the vocabulary mechanism —
  manifolds built as small as the need (department/team/project) put each audience's
  vocabulary at the DECLARATION level of its own manifold, and the hundred-names promise
  is delivered ACROSS manifolds by layered-cache semantic identity ("names cannot
  fragment the cache"), not within one by alias; (ii) session/individual naming (a
  client-language deliverable) is the consumption side of the button — the agent+user's
  jurisdiction per the two-ends principle; the parser/planner never sees it; (iii) no
  saved-query→delivery provenance chain exists for an alias to durably serve. REVISIT
  TRIGGER (ledgered): if a saved-query surface ever ships, rename-compatibility re-opens
  by ruling. **The reconciling asymmetry with operator overrides (which stand): you
  rename what you didn't name — framework operator vocabulary is imported; levels and
  measures are the author's own words, and what you named needs one name.**
- **D1 (CLOSED BY ASSEMBLY 2026-07-15)** — the schema is now determined by the rulings
  above: the shipped per-kind shape extended ADDITIVELY with License blocks verbatim
  (fertility/hierarchy/assert), signature addressing (universe-qualified where
  duplication exists), basis type + its absence semantics (B3), published-scope vs cut
  display (B1), and operator properties (registry describe). No alias block (C1).
  Versioning: additive under the tool-surface discipline; any shape question at CP is a
  CV-ledger line, not a redesign.
- **CP structure** — proposal: CP-0 (this capture + A/B/C/D rulings) → CP-1 syntax +
  adjudication → CP-2 init slice → CP-3 describe + Explorer → CP-4 full diff. Certificate
  kernel reused unchanged; any License schema change is a named checkpoint fork.
