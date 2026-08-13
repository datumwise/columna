# Core-P1 — Compiler contract & private-mapping model (design)

**Status:** design checkpoint / pre-implementation. **No compiler code before the final narrow
checkpoint** (see end). Field names are candidates, **not frozen**.
**Date:** 2026-08-13
**Sources:** `columna` @ main (`0.15.0-core`), `manifold-agent` @ `d9ea705` (`0.12.0`).
Reads with `core_p1_compiler_input.md`, `f0_reconnaissance.md`, `s2_closure.md`.

Governing principle of this pass:

> **Realize each logical object once, then let lowering compose through references.**
> Do not create mapping entries for every *use* of a logical object. This keeps the mapping
> model coherent and preserves the blast wall.

Permanent invariants (carried): meaning before realization; mapping realizes meaning, it does not
create it; no physical detail leaks into the authored Manifold; **mapping realizes law, it cannot
certify law; the compiler translates authority, it cannot manufacture authority.**

---

## The compile boundary

```
compile(governed_publication: GovernedPublicationArtifact,
        private_core_mapping: PrivateCoreMapping)
    -> Core-private execution image        # .cml is one serialization of it
```

**Only these two are inputs.** The compiler must NOT consume, or reach into, any of:
Studio session state · `Declaration.evidence` · audit/profile objects · `manifold.columna.yaml` ·
`draft.lower_to_cml` output. It may not repair a missing input from any of them.

Identity flow (the compiler **emits** `SOURCE_MANIFOLD`; it does not compare an existing output's):
```
GovernedPublicationArtifact.ref  ==  PrivateCoreMapping.publication_ref
        ↓ compiler
   SOURCE_MANIFOLD emitted == artifact.ref  (exactly)
```

---

## A. Private-mapping model

### A0. Mapping is bound to one immutable publication (REQUIRED, checked first)

```
PrivateCoreMapping
    mapping_format_version
    publication_ref { manifold_id, version }
    realizations[...]
```
**Precondition, before any compilation:** `private_mapping.publication_ref == governed_publication.ref`.
Without this, a valid mapping for `retail@1.2.0` could be combined with `retail@1.3.0` and the compiler
would manufacture a valid-looking `.cml` for the wrong governed meaning. A mismatch is
`InputIdentityMismatch`; a wholly absent artifact/mapping is an *invalid invocation*, a distinct
condition (see refusal taxonomy).

### Final mapping must contain COMPLETE resolved physical facts

"Derivable" means **derivable while constructing the mapping**, never derivable later by the compiler.
Mapping construction may consult gate/profile/audit to resolve endpoints; the **compiler consumes the
mapping only**. The final mapping stores fully-resolved `{connection, schema, table, column/keys}` — the
compiler never re-inspects evidence/profile to recover a missing schema/connection.

### A1. relationship realization — APPROVED (with a boundary)

```
relationship realization
    relationship_ref                       # logical relationship decl
    from endpoint { connection, schema, table, keys[] }
    to   endpoint { connection, schema, table, keys[] }
    bridge realization (optional, M:N)     # PROVISIONAL — trace exact RELATE…VIA needs first
```
- Require **join-key arity to match explicitly** (`len(from.keys) == len(to.keys)`).
- Endpoints are **derivable during construction** from the `referential`/`referential_xbackend`/`fanout`
  gate subjects (`gates.py:725,461,808`); schema/same-backend connection from profile — but the *final*
  mapping stores them resolved.
- Do **not** copy cardinality counts (proof) or the functionality label (logical) into mapping.
- `bridge`/`via` stays provisional; do not let `many_side` (physical gate evidence) become a new logical
  law.

### A2. hierarchy realization — APPROVED in principle; generic `path` NOT frozen

```
hierarchy realization
    hierarchy_ref
    edges[ { logical_child, logical_parent,
             child_endpoint  { connection, schema, table, column },
             parent_endpoint { connection, schema, table, column } } ]
```
- Represent **each adjacent logical hierarchy edge explicitly**; for 3+ levels every adjacent pair has a
  realization. Same-table hierarchies may share endpoint table/connection/schema. (Derivable from the
  `functional` gate subject `gates.py:657`.)
- **Do NOT add a generic `path: [...]`** physical escape hatch. If a cross-table hierarchy needs
  transport, first determine whether it can be expressed by referencing an already-governed
  relationship / existing Core transport. If not, **cross-table hierarchy stays unsupported** until a
  typed realization is designed. The mapping must never hold an arbitrary join path whose meaning exists
  nowhere in the logical Manifold.

### A3. attribute realization — APPROVED; attachment resolved → co-located vs cross-table SPLIT

Authored body stays physical-clean `{of, value_type}`. Mapping needs at least:
```
attribute realization
    attribute_ref = <of>.<name>
    physical value endpoint { connection, schema, table, column }
    attachment  → co-located | governed-path
```
**Verified (2026-08-13):** an attribute may legally be **cross-table** — the inline `ATTR` form accepts any
`table.column` and reaches it by broadcast (`parser.py:205,582,589`); the stored form carries no join key
back to the coordinate (`model.py:77`). So `{table,column}` alone cannot guarantee one value per
coordinate. Resulting **split**:
- **co-located attribute** — physically available on the coordinate's own realized level/key relation,
  requiring no independent transport → **Core-P1 candidate**. Support condition is not merely
  `attr.table == coord.table`; the compiler must know the value is keyed at the coordinate's governed
  key/grain.
- **cross-table attribute** — needs a governed attachment route (an existing governed relationship /
  functional path) to the owning coordinate; **not** ad-hoc join keys inside the attribute. That route is
  itself a `FunctionalEdge`/relate → so it inherits the **certification** question below and stays blocked
  until that path can be governed and licensed.
Preserved distinction: *physical mapping says where an attribute value comes from; it does not prove the
coordinate functionally determines one value* — that proof/license is separate.

### A-coord. anchor-component realization — APPROVED (new; required for composite anchors)

The anchor binding today is `{table, grain=tuple(keys), column=None}` (`mapping.py:154-156,174`) with **no**
named `coordinate → physical-key-column` association; for a composite grain it is simply absent (only
incidentally 1:1 for a single key, by position). columna-core proves the concept one layer down
(`DimensionLevel.realized_by`, `model.py:70`). Add:
```
anchor component realization
    anchor_ref
    component_name
    physical endpoint { connection, schema, table, column }
```
Do not rely on tuple position. Require completeness — every authored anchor component maps to exactly one
realization; reject missing / duplicate / unknown components. The mapping realizes coordinate identity; it
does not redefine the anchor.

### A4. restriction reference realization — REMOVED (do not persist)

A universe restriction already contains logical refs. **Restriction lowering is a compiler composition
over coordinate/attribute realizations**, not a new per-universe physical record:
```
restriction AST → logical ref resolution → coordinate|attribute object
               → that object's private realization → Core WHERE operand
```
Duplicating a column into a `universe_ref/ref_path/column` record would create two mapping truths for the
same object and force a precedence rule. The mapping realizes **logical objects**, not every place they
are referenced.
- **Coordinate refs — RESOLVED:** every restriction ref bottoms out in exactly a coordinate or a
  `coordinate.attribute` (no third target, no physical fallback — `validate.py:133-136,328-349`;
  `ratification.py:106-115`). Lowering = `compose(realization(coord|attr))`. Coordinate refs resolve
  through **A-coord** (added above); attribute refs through **A3**. No per-universe record.

---

## B. Compiler contract & refusal taxonomy

`InputIdentityMismatch` sits **before** the four gap categories (it is an input-authority condition, not a
lowering outcome). The four gap categories stay distinct — never collapse into a generic `LoweringError`:

| category | question it answers |
|---|---|
| `LogicalMeaningMissing` (**L**) | do we know what this means? |
| `MappingIncomplete` (**M**) | do we know how that meaning maps to physical data? |
| `UnsupportedCoreCapability` (**C**) | can the existing Core compiler/runtime perform the required operation faithfully? |
| `ExecutionRepresentationGap` (**G**) | can the Core execution image represent the required law at all? |
| `GovernedCertificationMissing` (**cert**, prov.; a.k.a. `GovernedAuthorityMissing`) | **confirmed real** by the B/C verification — meaning + realization + Core capability all present, but the governed verdict required to *license* execution is not established/carried. **Belongs to the admission/adjudication phase, not assumed to fire from `compile()`** (see phase split below). Cured **above** Core-P1; never in mapping. |

`InputIdentityMismatch` — mapping ref ≠ artifact ref. (Absent artifact/mapping = invalid invocation.)

### Authority-source verification → Outcome B confirmed; but immutable-artifact home NOT assumed

Verified (2026-08-13), both Outcome B:
- **Relationship `FACES {assign|alloc}`** asserts a data-corroborated face **License** minted at publish by
  `columna_core.adjudication._prove_face` (`adjudication.py:457-528`: assign = unique-top/no-tie
  single-count; alloc = non-negative partition-of-unity). A `Face` is closed-by-default; the license opens
  the crossing (`model.py:218-225`). The artifact carries only `{from,to,functionality,disposition}` + per-
  **universe** ratifications — no face license. (`touch` is data-free/VERIFIED but its face + folklore
  aren't carried either — a lesser carriage gap.)
- **Hierarchy `FunctionalEdge`** asserts a truly-functional child→parent map; the planner assumes it
  (`find_path` is a bare BFS, `model.py:302-319`) and the only guard is the adjudication FD verdict applied
  at runtime (`_prove_hierarchy`, `adjudication.py:314-341`; `blocked_edges`, `planner.py:110`). The
  artifact carries `{levels,direction}` + universe ratifications only — no FD verdict.

> **Outcome B confirmed: faced relationships and hierarchy transport require governed certification not
> presently carried across the shared/Core boundary. The correct lifecycle and durable carrier remain
> UNRESOLVED; because these verdicts are data/realization-dependent, the immutable
> `GovernedPublicationArtifact` is NOT assumed to be their home.**

The trace proved certification is *required*; it did **not** prove certification is part of immutable
publication identity. These verdicts (FD holds? order-top unique? weights non-negative & positive-sum?)
depend on physical realization + attested data + sometimes driver values, and can change while the logical
publication is unchanged. So `retail@1.3.0` realized against environment A (FD holds) vs B (FD
contradicted) has one publication meaning but two certification results — storing a `CORROBORATED` verdict
in the immutable artifact would turn a realization/data fact into a publication fact. **Do not do that.**

Two DIFFERENT gaps for faces, kept separate:
- **A — logical-publication carriage gap:** the face *declaration itself* (name/scheme/driver/order/
  folklore) is not carried in `GovernedPublicationArtifact.logical`. The compiler cannot even know which
  face law was declared. Fix above Core-P1 in the shared **logical** publication (not by putting Core
  `License` into `authority`, not by pretending `disposition` prose defines a face).
- **B — certification:** for `assign`/`alloc` the adjudicator establishes whether the declared face is
  currently licensed on the realization. This is the certification-lifecycle question below.

### Refusal taxonomy split by PHASE (candidate shape)

A compiler answers "can I faithfully translate governed law into the Core execution representation?";
adjudication answers "is this execution path licensed on this realization/data state?" — different
questions. Candidate split (names not frozen):
```
COMPILATION                      GOVERNED ADMISSION / ADJUDICATION
  InputIdentityMismatch            GovernedCertificationMissing        (a.k.a. GovernedAuthorityMissing)
  LogicalMeaningMissing            GovernedCertificationContradicted
  MappingIncomplete                GovernedCertificationUntestable
  UnsupportedCoreCapability
  ExecutionRepresentationGap
```
`GovernedCertificationMissing` is a **real** category — meaning exists, realization exists, Core can
represent the op, but the governed verdict required to *license* execution is not established/carried at the
boundary where it is needed. **It is NOT yet ruled to fire from `compile()`** — whether certification is
required *before compilation* or *after compilation, before governed serving* is exactly what the next
workstream settles. Likely two-phase lifecycle to test against the existing Core:
```
compile(publication, mapping) → CLOSED execution image
adjudicate(image, provider/data) → governed certification (data-bound licenses)
serve() → requires the applicable license
```
The face trace already hints this is real (parse → `license=None` closed-by-default → adjudicator sole
License constructor → planner crosses only when licensed). If consistently enforced, a face License does
NOT belong in the compiler input: the **compiler** needs the logical face declaration; the **adjudicator**
needs the physical realization + data.

Language discipline: the compiler *"translates an established face license / functional-edge certification
into Core representation"* — it never *"mints / originates"* one. **Mapping realizes law; it cannot certify
law. The compiler translates authority; it cannot manufacture authority.**

### Per-kind status (after this pass)

| kind | status |
|---|---|
| measure, member, anchor, universe | authority-independent kernel (below); measure/member C-refuse holistic/sketch |
| **attribute** | **co-located** = kernel candidate; **cross-table** = blocked behind governed attachment path + certification |
| **relationship** | **bare M:N `RELATE`** = kernel candidate (must stay non-functional transport); **faced assign/alloc** = certification gap (+ face carriage gap A); `touch` = carriage gap |
| **hierarchy** | declared `{levels,direction}` may suffice to emit a CLOSED edge **iff** the runtime is closed-by-default; certification required before serving — **VERIFY lifecycle** (next workstream) |
| boundary | DEFERRED — **G** gap (`across`) + enforcement alignment |
| crosswalk | DEFERRED — **L** gap |
| holistic / sketch reducers | explicit **C** refusal (`median`, `mode`, `sketch distinct`) |

### Authority-independent compiler kernel (persist; NOT an implementation GO)

```
KERNEL (translatable without the unresolved certification layer)
  measure · member · anchor · universe · bare relationship · co-located attribute
```
Mapping extensions the kernel needs: `A0 publication_ref`, `A1` (relationship join/bridge), `A3`
(co-located attribute), `A-coord` (anchor components). This is what can be translated *without* the
certification layer — it is **not** a green light to write compiler code, because the certification
lifecycle may change the contract from `compile → fully-licensed image` to `compile → closed image;
adjudicate → governed state`. Settle that first.

---

## Cargo discipline

"Cargo" is acceptable **only** when it becomes structured execution law the Core actually consumes.
Governed facts Core semantics depend on — universe basis, absence/fill law, anchor identity,
functional-edge license, face license — must be consumed by the `.cml`/runtime representation. They may
**not** live only in comments, debug metadata, provenance blobs, or compiler reports. If Core depends on
it and the representation does not consume it, the compiler has reduced law.

---

## Next workstream: governed-certification lifecycle (pre-Core-P1)

The A–E checkpoint is resolved (B/C = Outcome B; D = compositional YES; A refined with A-coord + attribute
split). The blocking question is no longer a compiler-schema question — it is the **certification
lifecycle**. Scope this next; do not park it (it gates hierarchy, faced relationships, cross-table
attributes, *and* the compiler/adjudication boundary). Working label: **Core-P0.5 — governed certification
lifecycle**. Design only — no implementation, no provisioning, no promotion of gate evidence, no
Core-specific `License` in the shared artifact.

Checkpoint questions to answer:
1. What is immutable publication law vs realization-bound certification?
2. Exactly where are face declarations authored today? If nowhere in the shared logical model, what
   logical extension is required (carriage gap A)?
3. Can Core compile faces **closed** and adjudicate them later?
4. Can Core compile hierarchy edges **closed** and adjudicate them later? (Decisive sub-question: can a
   parsed-but-uncorroborated `FunctionalEdge` ever become an addressable transport path? If yes → fail-open
   defect to fix; if no → compile-closed is faithful.)
5. Per-verdict behavior today for VERIFIED / CORROBORATED / CONTRADICTED / UNTESTABLE / no-adjudication —
   for both faces and hierarchy.
6. What identity/watermark must bind a data-derived certificate so it cannot transfer across realization or
   data state? (Investigate binding to: `publication_ref` · realization identity / mapping fingerprint ·
   attestation watermark · certification subject · claim · verdict · established_at. **Invariant:** a
   certificate proven against realization A must never silently license realization B; one proven at a data
   attestation must not claim timeless validity unless its law is genuinely timeless — `touch` may be
   timeless, `assign`/`alloc` are not.)
7. Does a new shared certification artifact/state need to exist, or can existing runtime adjudication state
   be the correct carrier?
8. Only in shared/theory terms — never expose `columna_core.model.License` / `blocked_edges` / Core parser
   objects as the shared representation. Core derives its runtime `License` from a shared governed
   certification. **Two physical runtimes are acceptable; two meanings of certification are not.**
9. After those answers: the real production compiler API and first supported set.

No compiler implementation until this lifecycle checkpoint is reviewed and ruled.

---

### Governing stop rule (verbatim, unchanged)

> If the governed publication does not contain enough meaning to compile, stop. If the private mapping
> does not contain enough realization information to compile, report a mapping gap. In neither case may
> the compiler invent the missing fact.
