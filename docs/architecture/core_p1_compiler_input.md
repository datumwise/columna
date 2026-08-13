# Core-P1 — Compiler-input boundary record

**Status:** design checkpoint / pre-implementation (no compiler code yet)
**Date:** 2026-08-13
**Sources traced:**
- `columna` @ `1a7e213` (`columna-core` `0.15.0-core`): `.cml` grammar/model (`parser.py`, `model.py`), demo `benchmark.cml`; old pre-split P1 trace under `specs/open_planner/` (pinned `0.14.0-core` / Substrait 0.46.0) and `specs/columna_manifold_spec_current.md` §8/§10.
- `manifold-agent` @ `d9ea705` (`0.12.0`): authored Manifold + governed publication (`manifold.py`, `validate.py`, `logical.py`, `publication.py`, `mapping.py`).

This is the Core-P1 boundary record; read alongside `f0_reconnaissance.md` and `s2_closure.md`.

---

## Governing invariants (permanent)

> **Meaning must exist before realization. Mapping realizes meaning; it does not create it.**

**Stop rule (verbatim, carried into implementation):**

> If the governed publication does not contain enough meaning to compile, stop. If the private
> mapping does not contain enough realization information to compile, report a mapping gap. In
> neither case may the compiler invent the missing fact.

Three failure modes must stay distinct — collapsing them into "lowering failed" is exactly what
would breach the blast wall:

- **missing logical meaning → authoring/model gap**
- **missing physical realization → mapping gap**
- **unsupported Core capability → Core-compiler coverage gap** (and its sibling, **Core execution
  grammar/runtime gap** — the representation cannot hold the construct)

**Blast wall:** no physical realization detail (table, column, schema, connection, join-key,
grain, provider, credential, path, runtime topology) may leak back into the authored Manifold to
make Core lowering easier. Physical facts live only in the private mapping; proof that a
realization satisfies a law lives only in adjudication/evidence — never substituted into mapping.

`.cml` is a **Core-private execution serialization**, not the shared boundary. The shared boundary
is the `GovernedPublicationArtifact`; `SOURCE_MANIFOLD` inside `.cml` is a realization *claim*
checked against `artifact.ref`.

---

## Gap-class definitions

| class | meaning |
|---|---|
| **L** — authoring/model gap | the authored artifact body lacks meaning the compiler needs |
| **M** — mapping-model gap | no private-mapping structure exists to realize the kind physically |
| **C** — Core-compiler coverage gap | Core cannot faithfully compile a construct/reducer whose meaning + realization are both known |
| **G** — Core execution grammar/runtime gap | the `.cml`/execution image cannot represent the construct (verified by *semantic identity loss*, not mere absence of syntax) |
| **VERIFY** | provisionally flagged; requires a targeted verification pass before a class is assigned |
| **—** | none |

---

## Compiler-input matrix

Q1 governed meaning in artifact · Q2 physical fact required from mapping · Q3 Core construct to
emit · Q4 mapping sufficient? · Q5 `.cml` grammar sufficient? · Q6 gap class.

| kind | Q1 artifact meaning | Q2 mapping fact | Q3 Core construct | Q4 | Q5 | Q6 |
|---|---|---|---|---|---|---|
| **measure** | `value_type`, `root_member`; opt `fill_rule`, `default_reduction` (`validate.py:85,110,127`) | `Binding.root_evaluator` = physical reducer `agg(table.col)`, never invented (`mapping.py:42-50`) | `MEASURE`→`MeasureColumn` (`parser.py:419`; `model.py:145`) | ✅ | ✅ | **C** for holistic reducers |
| **member** | `measure`,`anchor`,`universe` (`validate.py:86`) | central `Binding(member,connection,schema,table,column,grain,universe)` (`mapping.py:157-191`) | `FAMILY` member→`FamilyMember` (`parser.py:466`; `model.py:127`) | ✅ | ✅ | **C** for holistic/sketch |
| **anchor** | `components[{name,type}]` (`validate.py:69`; `logical.py:71`) | anchor-grain `Binding` from `unique_at`: `grain=PK`, `column=None` (`mapping.py:154,174`) | no statement; query arg, built from `LEVEL`+`A()` (`A1:45`; `model.py:352`) | ✅ (grain) | ⚠️ | **VERIFY** (see ruling 6) |
| **universe** | `basis`,`anchor`; opt structured `restriction` AST; ratification in `authority.*` not body (`validate.py:83,176`; `publication.py:223`) | none dedicated — `coverage` only stamps `universe` on a member binding; restriction predicate unrealized (`mapping.py:157-165`) | `UNIVERSE`+`WHERE`+`BASIS`→`Universe` (`parser.py:184`; `model.py:44`) | ❌ | ✅ | **M**+**C** (restriction realization + predicate lowering) |
| **relationship** | `from`,`to`,`functionality`,`disposition` (`validate.py:86`) | **none** — `build_mapping` skips; join keys stranded in `evidence.subject` (`mapping.py:161-165`) | `RELATE`+`FACES`→`Relate`/`Face` (`parser.py:332,270`; `model.py:228`) | ❌ | ✅ | **M** (join keys) + **C** (face-law disclosure non-delegable) |
| **boundary** | `measure`,`forbidden`,`across` — additivity law (`validate.py:88`) | none (purely logical) | no `BOUNDARY` kw; candidate realization via family `BLOCKED` anchors (`benchmark.cml:54`; `parser.py:466`) | ✅ n/a | ⚠️ | **VERIFY** (BLOCKED-equivalence, ruling 5) |
| **hierarchy** | `levels`(child,parent),`direction` (`validate.py:87,262`) | **none** — skipped like relationship; level cols in `evidence` only (`mapping.py:161-165`) | `HIERARCHY`→`FunctionalEdge` (`parser.py:500,515`; `model.py:248`) | ❌ | ✅ | **M** (level cols) + **C** (fan-out unless certified edge) |
| **crosswalk** | `from_coords`,`to_coords`,`correspondence`; "format-only, logic later", no synthesis path (`validate.py:89`; `manifold.py:95`) | none | no `CROSSWALK` kw; would be forced into `HIERARCHY` or `RELATE VIA` (`spec:28-32`; `parser.py:344`) | ❌ | ❌ | **L** first → **M/G deferred behind L** (ruling 3) |
| **attribute** | `of`,`value_type`; identity `<of>.<name>`; physical keys forbidden (`validate.py:82,152`) | **none** — no attribute `Binding`; deferred to P1 (`manifold.py:44-50`; spec §10) | inline `LEVEL…ATTR` only; standalone `ATTR ON` **retired** (`parser.py:204,527`; `model.py:77`) | ❌ | ⚠️ | **M** (attribute realization) + **G** for non-level |

### Headline (corrected)

- **Closest to compile-ready:** `measure`, `member` — logical body + concrete `Binding` with
  `column`/`grain`/`root_evaluator`. **Not wholly "done":** reducer coverage remains a Core-compiler
  capability boundary (holistic/sketch reducers do not lower).
- **`anchor`:** logical identity + grain realization largely present, **but preservation of governed
  coordinate identity through Core execution must be verified** (cargo audit) before it is called solved.

### Faithfulness cargo the compiler must carry or fail closed (obligations, not gaps)

The old-P1 D1 loss table attests these are lost in a naive lowering and must ride as explicit cargo
— this is where the blast wall lives at runtime:
- universe **basis + absence-law** — events-**zero** vs spine-**gap** vs align-**miss** are three nulls a Rel renders identically (`D1:56,61,114`);
- hierarchy / functional-crosswalk **certified-edge verdict** — a bare join on a non-functional key silently **fans out** (`D1:58,87`);
- relationship / M:N-crosswalk **face-law disclosure minting** — non-delegable custody law: over-count badge, `memberships_unrepresented` shadow (`D1:59,93`);
- anchor **coordinate-vs-value identity** and `(coords, universe)` binding (`D1:55,68`).

The old **8-node Plan IR** (`open_planner_artifact_A1_v0_3.md`) and **D1 loss table**
(`map2/D1_lowering_table_v0_1.md`) are **evidence/checklist only** — not a settled Core-P1 API
(D1 self-labels its nodes/verdicts "proposed").

---

## Rulings (Huayin, 2026-08-13)

**1. Relationship / hierarchy physical realization belongs in the mapping model.**
Extend the private mapping; do **not** read physical join/level info from `Declaration.evidence.subject`
(evidence supports/adjudicates a declaration; it is not the durable realization contract).
Minimum realization structures (field names NOT frozen yet):
- *relationship realization*: logical relationship ref · from-side physical key(s) · to-side physical key(s) · required physical relation path / source identity.
- *hierarchy realization*: logical hierarchy ref · child-level physical realization · parent-level physical realization · required join / functional path.
Permanent: **if the compiler needs a physical fact repeatedly and deterministically, it belongs in the
private realization model, not evidence.** Preserve the separation: logical functionality/disposition →
artifact; physical keys/path → mapping; proof the realization satisfies the law → adjudication/evidence.
Do not put proof results into mapping as substitutes for logical law.

**2. Attribute realization is a Core-P1 mapping-model deliverable.**
Logical declaration stays `{of, value_type}`; the physical column belongs only in private realization.
Add an attribute realization binding sufficient to answer "logical `<coordinate>.<attribute>` → which
physical value realizes it?" Do **not** add `table`/`column`/`schema`/`connection` to the authored
attribute body. Later explicit check (not measure-reduction semantics): for a coordinate member, does the
realized attribute have at most one governed value where functionality is required?

**3. Crosswalk is deferred from Core-P1 compilation.**
`crosswalk` → **unsupported logical construct for Core-P1** → **fail closed with an explicit coverage
reason**. Do not silently treat it as sugar over HIERARCHY or RELATE; the declaration lacks the law to
choose faithfully. The refusal means *Core-P1 lacks sufficient shared law + realization model + execution
representation*, **not** that the crosswalk declaration is invalid. Want hierarchy semantics → author a
hierarchy; want relationship semantics → author a relationship. **L gap first; M/G work deferred behind L.**
Do not design physical crosswalk mapping yet (may record requirements for later only).

**4. Holistic / unsupported reducers refuse closed.**
The compiler may lower a reducer only when Core preserves its governed meaning. `mean` may lower through
exact sufficient state (`sum + count`) *if semantics are preserved*; `median`, `mode`, unsupported
`sketch distinct` → do **not** approximate silently. Failure class = **Core-compiler coverage gap** (not
L, not M). Eventual report shape: "measure X is governed, its physical realization is known, but Core
cannot faithfully compile reducer Y." Approximation is allowed only when approximation is itself an
explicit governed contract — Core-P1 does not invent one.

**5. Verify BOUNDARY → BLOCKED equivalence before deciding representation.**
Targeted verification pass before boundary compiler design. Question: does today's `BLOCKED`
representation preserve the complete authored boundary `{measure, forbidden, across}` law for every
currently valid boundary declaration? Prove both directions (authored boundary → emitted BLOCKED loses
nothing; runtime BLOCKED → enforces exactly the intended prohibition). Check: multiple forbidden anchors;
multiple `across` contexts; nested/product anchors; interaction with family/member reduction; whether
BLOCKED attaches at the right semantic object; whether any ordering/direction info is lost.
- If fully equivalent → boundary: mapping none, grammar none, **compiler coverage: implement translation**.
- If not → **Core execution grammar/runtime gap**. Do not distort the authored boundary to fit BLOCKED.

**6. Anchor does not need a new first-class `.cml` statement in Core-P1.**
Keep anchor as governed identity carried into Core execution structures rather than adding an `ANCHOR`
grammar construct now. Strengthened requirement: **anchor may be implicit in syntax; it may not be
semantically lost.** The compiler must preserve explicit internal cargo distinguishing: coordinate
identity · coordinate type · product composition · universe association where required · grain realization.
A raw list of physical group-by columns is insufficient if it loses the governed logical identity of the
coordinates. Classification revised **G → VERIFY**: absence of first-class syntax is not itself a gap;
*semantic identity loss* is the gap criterion. If the only info `.cml` discards is already retained
authoritatively by the bound GovernedPublication and never needed by Core execution, that is acceptable;
if Core execution/planning needs the lost identity to preserve law, it becomes a **G-gap**.

---

## Core-P1 scope (after these rulings)

The first compiler targets only constructs whose meaning + physical realization can be made explicit
without inventing law. (In-scope ≠ one PR; it means they belong to Core-P1 rather than needing new
shared-theory design first.)

```
IN SCOPE FOR FIRST COMPILER
  measure
  member
  anchor         — subject to cargo verification (ruling 6)
  universe       — after restriction realization is added
  relationship   — after mapping extension (ruling 1)
  hierarchy      — after mapping extension (ruling 1)
  attribute      — after mapping extension (ruling 2)
  boundary       — after BLOCKED-equivalence verification (ruling 5)
DEFERRED
  crosswalk      — until its logical correspondence semantics are sufficient (ruling 3)
```

---

## Next checkpoint (design only, before any compiler code)

Two artifacts, plus two verification passes:
- **A. Proposed private mapping extensions** for attribute, relationship, hierarchy, universe-restriction
  references — per field: what logical object it realizes · why the compiler needs it · why it is physical
  not semantic · whether author-supplied or derivable. (Do not add a field merely because old-P1 proposed one.)
- **B. Compiler contract / refusal taxonomy** — `compile(governed_publication, private_mapping) → Core
  execution image`, else fail with distinct categories (names may change, categories stay separate):
  `LogicalMeaningMissing` · `MappingIncomplete` · `UnsupportedCoreCapability` · `ExecutionRepresentationGap`
  · `IdentityMismatch`/invalid input authority. Plus a per-kind lowering table: logical kind · artifact
  input · mapping input · Core output · proof/check required · failure category.
- **Verifications:** BOUNDARY→BLOCKED equivalence (ruling 5) and anchor-cargo (ruling 6).

Old 8-node Plan IR + D1 loss table = evidence/checklist only; do not adopt the IR automatically.
