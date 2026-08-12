# The Columna Manifold — current implemented spec

**As-built reference for `columna-core` `0.15.0-core` (wire `contract_version` `"2"`).**
Generated from the code, not from prophecy: every construct below is what the parser
(`columna_core.parser`) accepts and the object model (`columna_core.model`) holds *today*.
Where a construct was retired, that is stated. A short **§9 Not yet implemented** marks the
proposed-but-absent work (notably P0(c)) so this document is never read as promising more than
the engine does.

> **Constitutional sentence.** *Data is property at a point. The anchor names the coordinates;
> the universe defines the points.* Addressing is the anchor's job; existence is the universe's.
> Authority is declared; mathematics may verify; data may only refute or corroborate; the default
> is closed.

---

## 1. What a Manifold is

A **Manifold** is a governed semantic definition that makes a warehouse queryable end-to-end
without hand-construction. It has two layers:

- **Layer 1 — population** (`Universe`): *which observations exist* — a bundle of base dimensions,
  optionally carved by a predicate, grounded in a declared basis.
- **Layer 2 — coordinate** (`DimensionLevel` + `FunctionalEdge`): *how points are addressed* — the
  named grains and the functional (N:1 / 1:1) maps the engine transports along.

The central unification: a **rollup** (`day → month`) and a **cross-table relationship**
(`store → region`) are the *same thing* — a `FunctionalEdge` tagged with a lineage. The backend
never joins; it delivers a measure (single-table group-by) and an edge's key→key mapping
(single-table distinct). A **RELATE** is the anti-edge: an M:N relationship for which no lawful
rollup exists.

The written form is the **`.cml`** definition language (the `.cf` successor). `parse_manifold(text)`
turns it into the in-memory `Manifold`; the planner and engine run on the object.

---

## 2. The `.cml` definition language (grammar, as implemented)

Statement-oriented. `#` line comments. `{ }` blocks. A statement starts at a line whose first token
is a keyword; continuation lines belong to it. Two cross-cutting clauses may ride most declarations:

- **Folklore** — `-- "<text>"` — a **DESCRIPTION**. *Logical*: flows to `describe` and the wire.
- **REJECT** — `REJECT <table>.<col> "<reason>"` — an attested rejected physical incarnation.
  *Physical, map-layer only.* A **blast wall**: never crosses `describe` or the wire (§6).

### 2.1 Header

```
MANIFOLD <name> VERSION <int>
```

`VERSION` is an **integer** — *this engine artifact's* engine/cache revision. It is deliberately
**not** a semantic version (that widening was refused). Required; a document without it is rejected.

```
SOURCE_MANIFOLD <id> VERSION <semver>          # OPTIONAL (columna#150 P0(b))
```

The **source-identity reference**: the published governed Manifold this artifact was lowered from —
a *stable published id* **and** a *semantic publish version* (`major.minor.patch`, optional
`-prerelease` / `+build`), retained verbatim and opaquely. A third, distinct identity dimension,
never derived from the `MANIFOLD` name/version. **Atomic** — the one statement carries both, or it
is ungrammatical; a duplicate is refused. Absent ⇒ *no retained source identity* (a legacy artifact),
never an invented one. (See §5, §7.)

### 2.2 UNIVERSE (Layer 1)

```
UNIVERSE <name> = <dim> * <dim> * ...  [WHERE <predicate>]  [BASIS <kind>]
```

- **`<dim> * <dim>`** — the base dimensions bundled into the population.
- **`WHERE <predicate>`** — the **restriction**: AND-ed comparisons (`>= > <= < = !=`) over
  dimensions/attributes, **never measures**. Carves the valid points.
- **`BASIS <kind>`** — the population's grounding, one of **`events | spine | product | registry`**.
  **Optional; `None` = undeclared** (a legitimate state today). Basis **no longer drives absence
  semantics** (that keyed default was retired in columna#143 — it was a silent wrong zero for
  state-valued measures); it remains a declared property for `describe`/trust and broadcast-safety
  (replication over a non-events population corrupts completeness).

### 2.3 LEVEL (Layer 2)

```
LEVEL <name> = <column> [BASE] [ATTR <name> = <table>.<column> [, ...]]  [-- "<desc>"]  [REJECT ...]
```

- **`BASE`** — this level is a base dimension.
- **`ATTR`** (the *inline* form) — logical attributes **of** a level; the name is logical
  (`<level>.<attr>` is legal in a universe predicate), the `<table>.<column>` binding is physical.
- Forked levels carry a qualified name (`cal.month`, `fisc.month`).

### 2.4 HIERARCHY (functional lineages, B2)

```
HIERARCHY <lineage> { <a> -> <b> VIA <table>(<a_col>, <b_col>) [-> <c> VIA ...] ; <path> ; ... }
```

The **sole** surface for functional paths after the EDGE purge (§2a). Branching allowed — a lineage
may be a small DAG (calendar's `day→month→quarter→year` **plus** the `day→week` branch). **Sugar**:
it desugars to plain `FunctionalEdge`s indistinguishable from the old hand-declared edges; the record
is communicative provenance plus the handle for the publish-time FD test (every hop a genuine key→key
function; every chain composition holds; a violation ⇒ `CONTRADICTED`, **fails closed**).

### 2.5 RELATE (the anti-edge: M:N) + crossing FACES

```
RELATE <a> <-> <b> [VIA <table>(<frm_col>, <to_col>)] [NOTE "<text>"]
       [FACES { <name> = <SCHEME> [BY <measure-ref> [ORDER MIN|MAX]] -- "<folklore>" ; ... }]
```

- **`VIA`** bridge (table + join columns) is **map-layer**: engine-visible (join-multiply needs it),
  describe-invisible — never on the wire (§6).
- **FACES** — declared crossing dispositions (how an additive value behaves on the trip). Schemes
  (all three execute as of 0.12):
  - **`TOUCH`** — value reaches **every** match (join-multiply; deliberate multi-count; served
    `DISCLOSE`). No driver.
  - **`ASSIGN BY <measure-ref> ORDER MIN|MAX`** — goes to exactly one; the **ORDER direction is
    mandatory** (no default — "top" is ambiguous across driver kinds).
  - **`ALLOC BY <measure-ref>`** — splits across, by the normalized driver.
  - `<measure-ref>` is a **declared-measure** reference (resolved at publish), never a physical column.
  - Folklore is **mandatory** on a face (a face must say what the crossing does). A face is
    **closed-by-default**; its `License` is minted **only** by the adjudicator at publish.

### 2.6 MEASURE

```
MEASURE <name> ON <universe> FROM <table> AS <agg>(<expr>)          # aggregate form
MEASURE <name> ON <universe> FROM <table> VALUE <expr>             # per-row value form
    [TYPE <logical>]
    [FILL zero|unknown|undefined]
    [M_ANCHOR { <col>, ... }]
    [FAMILY { <agg> [: <tier>] [BLOCKED { <lineage>, ... }] ; ... }]
    [-- "<desc>"]
```

- **`AS <agg>(<expr>)`** vs **`VALUE <expr>`** — the aggregate form names an operator inline;
  the value form gives a per-row expression and takes its operators from the `FAMILY` block.
  `AS distinct(<col>)` (and a `distinct` family member) mark a distinct/sketch measure
  (`sketch_precision` = HLL lg_k).
- **`TYPE <logical>`** — the declared **logical** dtype (default `Float64`, e.g. `TYPE Categorical`).
  Vocabulary, not physical: the connector realizes logical → physical.

- **`ON <universe>`** — the population. *Optional sugar*: omit it iff the Manifold has exactly one
  universe (otherwise `ON` is **required** — the ambiguity is named, fail-closed).
- **`FILL <rule>`** — **Φ_v**, the per-measure fill rule (columna#143): what an eligible point with
  **no observed value** denotes — **`zero`** (existed, nil), **`unknown`** (a value existed,
  unrecorded — state-valued), or **`undefined`** (outside the member's population). **Absent =
  undeclared, and undeclared is legitimate**: the engine **discloses**, it does not fill. (Never keyed
  on universe basis — that default is retired.)
- **`M_ANCHOR { ... }`** — the missingness structure. Empty ⇒ **MCAR**; a set not containing the
  measure ⇒ **MAR**; containing itself ⇒ **MNAR**.
- **`FAMILY { ... }`** — reaggregation members. Each names an operator (reaggregability comes from the
  operator **registry** — operator-level) plus a **B-anchor** `BLOCKED { <lineage> }` (which lineages
  reduction is *permitted* along — column-level). The two gates compose: reduce iff *monoid* (possible)
  **and** *B-anchor-clear* (permitted). Measures are **open-by-default** (the B-anchor closes);
  `license` is `None` on a measure member.

### 2.7 DERIVED

```
DERIVED <name> = <expr>  [AT <level>]  [FAMILY { <member> FERTILE { <lineage>, ... } }]
```

- A column generated from stored columns through a formula (post-agg over measure/derived names,
  e.g. `revenue / orders`).
- **Closed-by-default over travel**: a bare formula is **denotation-only** — recomputed from
  components at the anchor, never reduced from cached finer values without a license.
- **`FAMILY { <member> FERTILE { ... } }`** — fertility is *added* by declaring members; each carries
  a `License` **constructed only by the adjudicator at publish** (the parser records the declared
  lineages; it never mints a License).
- **`AT <level>`** (`resolution_anchor`) — makes the alternative reading a **distinct metric** whose
  meaning embeds the anchor (e.g. the mean of daily rates).

### 2.8 Retired statements (still recognized, to teach)

Held in the dispatch **only** so a document written against the old grammar splits at the retired line
and meets a **teaching refusal** there (naming the ruling, not just erroring):

- **`ASSERT`** — retired 0.13.0. A data contract licenses no serving behavior; contracts belong to the
  attestation layer, upstream of the Manifold. (Its cascade also retired the **row-form `ATTR ... ON
  <universe>`** — the inline LEVEL `ATTR` is unaffected.)
- **`EDGE`** — purged (§2a); functional paths are declared via `HIERARCHY`.

---

## 3. The object model (`columna_core.model`)

Every dataclass is `@dataclass` (the `Manifold` container) or `@dataclass(frozen=True)` (the parts).

### Layer 1 — population
- **`Ref`** — a reference inside a predicate: `is_literal`, `value`, `table` (set ⇒ an attribute;
  cross-table ⇒ broadcast), `column` (the coordinate/level name).
- **`Comparison`** — `left: Ref`, `op` (`>= > <= < = !=`), `right: Ref`.
- **`Predicate`** — `comparisons: tuple` (AND-ed).
- **`Universe`** — `name`, `base_dimensions: frozenset`, `predicate?`, `basis?`
  (`events|spine|product|registry`, `None`=undeclared), `basis_license?` (a testedness record minted
  at publish; serving follows the *declaration*, not the license), `description`, `rejects` (map-layer).

### Layer 2 — coordinate
- **`DimensionLevel`** — `name`, `realized_by` (base column key), `is_base`, `description`, `rejects`,
  `attributes` (`((name, physical_binding), ...)`).
- **`FunctionalEdge`** — `frm` (finer), `to` (coarser), `lineage`, `provider_table`, `frm_col`,
  `to_col`, `evidence`. Unifies rollup and relationship; the B-anchor blocks transport per-lineage.

### Measures & derivations
- **`BAnchor`** — `blocked_lineages: frozenset`.
- **`FamilyMember`** — `agg`, `b_anchor`, `order_by?` (ordered ops), `description`,
  `declared_lineages` (derived: recorded, never a License), `license?` (derived fertility; adjudicator-
  only at publish; `None` on measure members).
- **`MeasureColumn`** — `name`, `universe`, `home_table`, `pre_expr` (per-row pre-agg over raw base
  columns; no casts — the connector realizes logical→physical), `logical_type` (`Float64` default),
  `family: dict`, `fill_rule?` (Φ_v), `m_anchor: frozenset` (MCAR/MAR/MNAR), `distinct_col?`,
  `sketch_precision` (HLL lg_k), `evidence`, `description`, `rejects`.
- **`DerivedColumn`** — `name`, `formula`, `family: dict` (empty ⇒ denotation-only, no travel),
  `resolution_anchor?` (`AT <level>`), `description`.

### Relationships & lineages
- **`Face`** — `name`, `scheme` (`touch|assign|alloc`), `description` (mandatory folklore),
  `selection` (driver measure-ref for assign/alloc), `order` (assign only: `min|max`), `license?`
  (adjudicator-only; closed-by-default).
- **`Relate`** — `frm`, `to`, `detail` (NOTE folklore), `faces: tuple`; map-layer `via_table?`,
  `via_frm_col?`, `via_to_col?` (engine-visible, never on the wire).
- **`Hierarchy`** — `lineage`, `paths: tuple` (branches, each a chain of levels), `license?` (minted
  at publish), `description`. Desugars to `FunctionalEdge`s.

### Adjudication
- **`License`** — the adjudicated authority for a declared capability. `verdict`
  (`VERIFIED | CORROBORATED | UNTESTABLE`), `lineages`, `basis` (proof note / attestation ref / author
  note), `attestation?` (the data watermark for `CORROBORATED`). **`CONTRADICTED` never persists past
  publish** — a contradicted declaration fails closed (the Manifold does not publish).

### The container
- **`Manifold`** — `name`, `version` (int), `universes`, `levels`, `edges`, `measures`, `derived`,
  `non_functional` (`[Relate]`), `hierarchies`, and the P0(b) source identity:
  **`source_manifold_id?`**, **`source_manifold_version?`** (both `None` until published; see §7).

---

## 4. Semantics that matter

- **Basis (four-way).** `events | spine | product | registry`. A *semantic declaration*, not a
  shortcut. It does **not** drive absence semantics (retired); it informs `describe`/trust and
  broadcast-safety. The per-basis testedness `License` (`_prove_basis`) is for describe/trust only —
  **serving follows the declaration**, not the license.
- **Fill rule Φ_v.** Per-measure. `zero | unknown | undefined`, or **undeclared** (disclose, never
  fill). Absence is disclosed structurally, never silently zeroed.
- **Missingness.** `M_ANCHOR` ⇒ MCAR / MAR / MNAR.
- **Adjudication (Certificate kernel).** Verdicts `VERIFIED` (symbolic, timeless), `CORROBORATED`
  (refutation-tested against attested data, watermarked, may flip on re-attestation), `UNTESTABLE`
  (authored authority; recorded, never exercised — an asserted license never changes a served number),
  `CONTRADICTED` (**publish fails closed**, loudly, with the counterexample named). Customers:
  derived-column fertility, HIERARCHY FD test, RELATE-face crossing, BASIS testedness.
- **Faces (crossing polarity).** Closed opens: a face's `License` **opens** the crossing.
- **The map-layer blast wall.** `rejects` (physical incarnations) and RELATE `VIA` bridges are
  engine-visible but **never** cross `describe` or the wire. The projection strips them; an insulation
  test asserts it.
- **Three distinct identities** (never derived from one another): the Manifold `VERSION` (integer
  engine/cache revision), the `.cml`/schema **format** version, and the **source identity** pair
  (`source_manifold_id`, `source_manifold_version` — the published governed Manifold, semver).

---

## 5. Lowering & serialization

Two serializations exist, for two audiences:

1. **The `.cml` text** (this document's grammar). Parsed by `columna_core.parser`; the hand-authored
   / engine-ingest form. Round-trips the source identity via `SOURCE_MANIFOLD` (§7).
2. **The engine YAML** (`manifold.columna.yaml`), produced by the Studio side
   (`manifold_agent.Manifold.to_engine_dict/to_engine_yaml`) — the Columna-readable downgrade:
   declaration bodies by section, no evidence/provenance, lossless for everything the engine reads.
   It carries the source-identity pair as `source_manifold_id` / `source_manifold_version` keys.

**Governed lowering (fail-closed).** At **publish**, Studio stamps the source identity onto both the
engine artifact and the retained superset and **requires** it: the governed lowerer
(`columna_studio.apply.stamp_source_identity`) raises rather than emit an artifact with no reference to
the Manifold it came from. The columna **parser stays permissive** (a legacy artifact with no
`SOURCE_MANIFOLD` parses, both fields `None`); the **lowerer is strict** — the same parser-permissive /
lowerer-strict split the system uses elsewhere.

**Wire.** The four moods (serve · disclose · clarify · refuse) travel as data over one contract,
`contract_version` `"2"`.

---

## 6. Fail-closed disciplines already in force

- **Publish adjudication.** A `CONTRADICTED` verdict (FD violation, hierarchy fan-out, data
  refutation beyond tolerance) refuses the publish, naming the counterexample.
- **Governed lowering.** A missing source identity refuses (P0(b)).
- **Single-universe `ON` sugar.** Omitting `ON` with >1 universe is refused, naming the ambiguity.
- **Retired syntax.** `ASSERT` / `EDGE` / row-form `ATTR` meet a teaching refusal that names the ruling.
- **The lowering invariant the system keeps.** *Lowering may reduce coverage; it must never reduce
  law* — "no cover, no lowering; the plan falls home, never lowers with a warning."

---

## 7. Source identity (columna#150 P0(b)) — the identity path in place

```
Studio publish identity  →  persisted Manifold  →  .cml SOURCE_MANIFOLD reference  →  columna runtime retention
```

At publish, Studio mints the semantic version (`bump_version`, `major.minor.patch` from the diff) and
stamps `(source_manifold_id, source_manifold_version)` onto the Manifold; the pair is carried through
the superset and the engine downgrade; the `.cml` grammar retains it on load. Three identity dimensions
stay separate even when values coincide.

---

## 8. Version & compatibility

- `columna_core.__version__` = **`0.15.0-core`**. Wire `contract_version` = **`"2"`**.
- `0.15.0` added the additive `SOURCE_MANIFOLD` statement (no wire change).
- `0.14.0` made an unaliased column's key its **canonical expression** (wire `"1"` → `"2"`).
- `0.13.0` retired `ASSERT` (and the row-form `ATTR`).

---

## 9. Not yet implemented (proposed, **not** current)

Flagged so this document is never over-read:

- **P0(c) — structured universe existence law + explicit completeness.** Today a universe can carry
  `basis = None` (undeclared) and still lower, and the Studio-side existence law (`λ_U`) is a
  **free-text** `law` field with no structured restriction and no completeness state. The proposed
  fail-closed rule — *a universe may lower only when it has a declared basis and its structured
  existence law is explicitly established as complete* — is **under design, not built**. When it lands,
  completeness will be **authored-Manifold state that licenses lowering**, not a new runtime `.cml`
  law (the `.cml` continues to carry only `BASIS` + `WHERE`).
- **Two-format note.** The `.cml` text and the engine YAML are distinct serializations; unifying /
  formally reconciling them is not done here.
