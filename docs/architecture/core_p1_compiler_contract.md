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

### A3. attribute realization — APPROVED; column alone may be insufficient (attachment VERIFY)

Authored body stays physical-clean `{of, value_type}`. Mapping needs at least:
```
attribute realization
    attribute_ref = <of>.<name>
    physical value endpoint { connection, schema, table, column }
    attachment  ← VERIFY (see below)
```
Open question before freezing: **how does the physical value attach to the coordinate named by `of`?**
If co-located on the coordinate's own level table/key, existing coordinate realization makes attachment
unambiguous. If it lives elsewhere, `table+column` alone does not tell the compiler how to obtain **one
value per governed coordinate** — the design must then reference an already-governed relationship/path to
the owning coordinate, **not** duplicate ad-hoc join keys inside the attribute. Preserved distinction:
*physical mapping says where an attribute value comes from; it does not prove the coordinate
functionally determines one value* — that proof/license is separate.

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
- **Coordinate refs — VERIFY:** today `unique_at` gives `{table, grain=keys, column=None}`
  (`mapping.py:154-156`). If the existing grain/level mapping yields an unambiguous
  `coordinate-name → physical-key-column`, reuse it. If not, add an explicit **anchor-component /
  coordinate realization** to the mapping model — but never solve it with universe-specific A4 entries.
- **Attribute refs:** resolve through A3.

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
| `GovernedAuthorityMissing` (**auth**) | *conditional* — introduced ONLY if the authority verification (below) proves the artifact lacks compiler-required certification. A publication-authority gap, cured **above** Core-P1, never in mapping. |

`InputIdentityMismatch` — mapping ref ≠ artifact ref. (Absent artifact/mapping = invalid invocation.)

### Authority-source verification (BLOCKS relationship/hierarchy "supported" status)

The compiler is forbidden to read `Declaration.evidence`/gate counts. So: does emitting Core `FACES` /
`FunctionalEdge` assert something **stronger** than the published logical fields the artifact carries?
- **Outcome A — logical law sufficient:** `HIERARCHY`/`FACES` translate faithfully+deterministically from
  already-published fields (`functionality, disposition, levels, direction`). Document the proof; no extra
  authority cargo.
- **Outcome B — prior certified verdict required:** emitting the Core construct asserts a data-corroborated
  verdict the artifact does not carry (lives only in gate evidence). Then the shared publication lacks
  compiler-required authority cargo → `GovernedAuthorityMissing`, and the cure (durable governed
  certification in the publication artifact) belongs **above** Core-P1. **Stop** if so.

Language discipline: the compiler must say *"translate an established face license / functional-edge
certification into Core representation,"* never *"mint / originate"* one. It encodes established law; it
may not originate law.

### Per-kind status (after this pass, pending authority verification)

| kind | status |
|---|---|
| measure, member, anchor, universe, attribute | classified per current mapping/capability findings (see per-kind table in `core_p1_compiler_input.md`); attribute pending A3 attachment |
| **relationship** | mapping design understood; **authority/certification source = VERIFY** |
| **hierarchy** | mapping design understood; **authority/certification source = VERIFY** |
| boundary | DEFERRED — **G** gap (no faithful representation of `across`) + enforcement alignment |
| crosswalk | DEFERRED — **L** gap (insufficient shared correspondence semantics) |
| holistic / sketch reducers | explicit **C** refusal (`median`, `mode`, `sketch distinct`) |

---

## Cargo discipline

"Cargo" is acceptable **only** when it becomes structured execution law the Core actually consumes.
Governed facts Core semantics depend on — universe basis, absence/fill law, anchor identity,
functional-edge license, face license — must be consumed by the `.cml`/runtime representation. They may
**not** live only in comments, debug metadata, provenance blobs, or compiler reports. If Core depends on
it and the representation does not consume it, the compiler has reduced law.

---

## Final narrow checkpoint (required before ANY compiler code)

1. **A** — exact mapping schema candidate, including coordinate/attribute **attachment**.
2. **B** — relationship `FACES` authority source (Outcome A or B).
3. **C** — hierarchy `FunctionalEdge` authority source (Outcome A or B).
4. **D** — proof that restriction refs resolve **entirely** through reusable coordinate/attribute mappings.
5. **E** — exact supported/refused Core-P1 set after B/C.

Introduce `GovernedAuthorityMissing` only if B or C proves it necessary. No compiler implementation until
this checkpoint is reviewed.

---

### Governing stop rule (verbatim, unchanged)

> If the governed publication does not contain enough meaning to compile, stop. If the private mapping
> does not contain enough realization information to compile, report a mapping gap. In neither case may
> the compiler invent the missing fact.
