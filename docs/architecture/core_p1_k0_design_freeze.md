# Core-P1 K0 — final design-freeze note

**Status:** **RATIFIED IN FULL** (CG2, 2026-08-22). Scope and the reducer allow-list were ruled at the
K0 checkpoint (D1 = GO); the four remaining implementation-defining sections — §3 field freeze, §5
compile/emission/receipt contract, §6 location, §7 acceptance-test outline — were ratified on the same
date and are marked individually below. No section of this note is proposed any longer.

> **Core-P1 K0 implementation is authorized once this amendment is merged.** (CG2, 2026-08-22.)
> There is no further architecture checkpoint before K0 code.

**Date:** 2026-08-22 (design freeze) · 2026-08-22 (ratified; implementation authorized)
**Pinned to:** `main` `01cbeab507bd9712ea09b3785c5526dd67819c34`; released triad `columna` 0.15.2 /
`columna-core` 0.15.2 / `columna-server` 0.9.0.
**Dependency (explicit):** `ruling_2026_08_22_lowering_receipt.md`. K0 is milestone **4** complete plus
the first cut of milestone **5**, in the order that ruling fixed — **mapping precedes compiler**.
Reads with `core_p1_compiler_input.md`, `core_p1_compiler_contract.md`,
`core_p05_certification_lifecycle.md`, `core_p05a_closed_by_default_serving.md`.

Permanent invariants, carried unchanged: meaning before realization · mapping realizes meaning, it does
not create it · no physical detail leaks into the authored Manifold · **mapping realizes law, it cannot
certify law; the compiler translates authority, it cannot manufacture authority.**

---

## 1. Scope — RULED

**In K0:**

```
measure · member · anchor
  + the unrestricted UNIVERSE and base LEVEL declarations required for a
    parseable / well-formed Core execution image
```

The universe/level addition is not a scope widening. It is a **well-formedness necessity**: a measure
cannot be emitted without a universe to bind, and a universe cannot be emitted without a `LEVEL` for
every base dimension (`parser.check_wellformed` — `measure … references unknown universe`, `universe …
references unknown base level`). Because `WHERE` and `BASIS` are both optional in the `UNIVERSE`
grammar, an *unrestricted* universe costs no restriction-lowering machinery at all.

**Out of K0** — universe **restrictions**; **hierarchy**. All previously ruled exclusions stand
unchanged: relationship (bare or faced) · attribute (co-located or cross-table) · faces · boundary ·
crosswalk · provisioning · any certification-dependent capability.

**Refusal, never omission.** A governed publication containing an out-of-scope construct must **refuse
with its named category**. An image that silently drops governed law is the one outcome that must be
impossible — it would make the receipt bind a publication to an image that does not carry its meaning.

---

## 2. Reducer allow-list — RULED

**K0 emits exactly four reducers:**

```
sum   count   min   max
```

All four are VALUE-witness monoids (`is_monoid=True`) that Core executes exactly:
`sum`/`count` combine by `sum`; `min` combines by `min`, `max` by `max`. `count` carries the parser's
`pre_expr = "1"` special case; `min`/`max` declare `accepts=ORDERED, out_rule="same"` and neither
carries `in_core=False`.

`min` and `max` were initially held out **for scope minimality alone**. That is not a reason, so the
ruling required verification instead: *include them if the shipped Core parses, validates and executes
them faithfully; otherwise report the exact reason.* It does, and the verification is recorded below.

### Verification of `min` / `max` against shipped Core (2026-08-22)

Run against `columna-core` at this pin, in a K0-shaped world — one unrestricted `UNIVERSE` over a
product of two base `LEVEL`s, no `HIERARCHY`, no `RELATE`, no restriction — with values chosen
non-monotonic so that `min`/`max` cannot coincide with `first`/`last`:

```
store day amount        MEASURE amt ON sales FROM sales_lines VALUE amount
  s1  d1   10.0             FAMILY { sum  count  min  max }
  s1  d2    3.0
  s1  d3    7.0         UNIVERSE sales = store * day       (unrestricted)
  s2  d1    5.0         LEVEL store = store_id BASE
  s2  d2   40.0         LEVEL day   = day      BASE
  s2  d3   20.0
```

| step | result |
|---|---|
| parse | OK — `family = {count, max, min, sum}` |
| `check()` | **CLEAN**, 0 errors |
| `publish()` | OK — the real lifecycle (adjudicate, then witnesses) |
| execute at the leaf grain `{store, day}` | all four `served`; 6 values each; **exact match** to independently computed truth |
| execute at the rolled-up grain `{store}` | all four `served`; **exact match** — `min` → `{s1: 3.0, s2: 5.0}`, `max` → `{s1: 10.0, s2: 40.0}` |

The rolled-up ask is the load-bearing one: asking at a **subset of the product anchor** aggregates
across the dropped component, so it exercises the monoid **combine** step (`min`-of-`min`s,
`max`-of-`max`es) rather than mere delivery — and it does so without any hierarchy, which K0 excludes.
Both are correct against independent truth.

**Conclusion: `min` and `max` parse, validate, execute and combine faithfully. They are in K0.**

### `mean` — OUT of K0. Do not emit.

The shipped Core does not execute the emitted form faithfully. `mean` is registered
`witness=HOLISTIC, is_monoid=False, in_core=False`, and **no sufficient-state (`sum + count`)
composition exists anywhere in Core**. The failure mode is the reason this is called out rather than
merely listed:

* `FAMILY { mean }` **parses clean and `check_wellformed`s clean** — `mean` is in the registry, is a
  `REDUCER`, and passes `signature_ok`.
* It then **refuses at execution**: `in_core` is consulted only on the scan path, never on the reducer
  path, so the request reaches the holistic branch and raises
  `Refusal("unsupported", "holistic operator 'mean' not implemented")`.
* `avg` is an alias that `check_wellformed` never canonicalizes, so `FAMILY { avg }` is a hard parse
  error instead.

The same verification run confirms this empirically as the control. Adding `mean` to the family above
parses and `check()`s **CLEAN, 0 errors**, and then at execution returns:

```
status = 'error'
no_result = { kind: 'error', reason: 'unsupported',
              detail: "holistic operator 'mean' not implemented" }
```

`core_p1_compiler_input.md` ruling 4 permits `mean` to lower through exact sufficient state
"*if semantics are preserved*". **That condition is not satisfied by the shipped Core**, so the
permission does not apply. A compiler that read the conditional as a licence would emit a document
that validates and then fails at query time.

### `median` and `mode` — OUT of K0, classification NOT settled

Out for **scope minimality only**. The prior classification must **not** be carried forward as settled:
`core_p1_compiler_input.md` ruling 4 lists `median` and `mode` among the Core-compiler **coverage (C)**
refusals, and the shipped evidence does not support that reading —

> **Shipped Core executes both.** `_recompute_holistic` delivers raw base rows and aggregates at the
> target grain: `median` via `pl.col("_value").median()`, `mode` via `.mode().first()`. `median`
> accepts `NUMERIC | TEMPORAL`; `mode` accepts `ANY`. Neither approximates.

**Their compiler classification is deferred**, to be decided on its own evidence when K1 scope is set —
not inherited from ruling 4, and not re-affirmed here.

### Everything else — out

`last` · `first` — exactly computable, but they require `ORDER <level>`, and **Core does not validate
that at parse**, so the obligation would fall on the compiler. `distinct` and the `hll_*` family —
sketch witness, and single-target-level only in this build. Every MAP and SCAN operator — Core itself
rejects these as family members.

Unlike `min`/`max`, each of these is held out for a **stated reason**, not for minimality.

---

## 3. `PrivateCoreMapping` — field freeze — RATIFIED

**Freeze the on-disk format, not a Python class.** The `columna` and `manifold-agent` trees are
import-disjoint and the disjointness is test-enforced (`test_server_ingests_the_artifact_without_
importing_manifold_agent` asserts `"manifold_agent" not in sys.modules`), yet `columna-server` already
consumes `GovernedPublicationArtifact` as plain JSON with the stdlib only. That precedent transfers
exactly and inverts no dependency.

**File:** `private-core-mapping.json`. **JSON, not YAML** — the `columna` tree has zero `yaml` imports
and no PyYAML dependency; persisting the mapping as YAML would force one on the consumer for nothing.

```
PrivateCoreMapping
    mapping_format_version   "1"
    publication_ref          { manifold_id: str, version: str }
    realizations             [ ... ]
```

Exactly two realization kinds in K0:

```jsonc
{ "kind": "anchor_component",
  "anchor_ref":     "<anchor declaration name>",
  "component_name": "<authored component name>",
  "endpoint": { "connection": str, "schema": str|null, "table": str, "column": str } }

{ "kind": "member",
  "measure_ref":    "<measure declaration name>",
  "member_ref":     "<member declaration name>",
  "universe_ref":   "<universe declaration name>",
  "anchor_ref":     "<anchor declaration name>",
  "endpoint": { "connection": str, "schema": str|null, "table": str, "column": str|null },
  "root_evaluator": "<agg>" }
```

Deliberately absent: relationship · hierarchy · attribute · bridge/`via` · any restriction-reference
record (A4 was **removed** by ruling — restrictions compose through coordinate/attribute realizations;
they are never a persisted per-universe record).

**Rules frozen with the shape.**

* `private_mapping.publication_ref == governed_publication.ref` is checked **first**, before any
  lowering. Mismatch is `InputIdentityMismatch`; a wholly absent input is an invalid invocation.
* Every authored anchor component maps to **exactly one** realization. Missing, duplicate and unknown
  components all refuse. **No tuple-position inference** — the historic anchor binding carried
  `grain=tuple(keys)` with no named coordinate→column association, which is precisely the gap A-coord
  exists to close.
* Endpoints are **fully resolved** in the mapping as stored. "Derivable" means derivable while
  *constructing* the mapping, never by the compiler at compile time.
* Serialization is deterministic (sorted keys, stable separators), mirroring the publication artifact.

**Naming hazard, recorded.** `manifold_agent.mapping` already defines `MAPPING_VERSION = "0.1"` and a
`mapping_version` field on a *different* object. `mapping_format_version` is deliberately a distinct
name, and its value follows `PUBLICATION_FORMAT_VERSION = "1"` — a bare major that a loader keys on —
**not** the `"0.1"` style. The two must never be conflated.

---

## 4. K0 lowering / proof table — DELIVERED

The per-kind table `core_p1_compiler_input.md` asked for, including the **proof/check required** column
that had never been authored.

| logical kind | artifact input | mapping input | Core output | proof / check required | failure category |
|---|---|---|---|---|---|
| **anchor** | `components[{name,type}]` | `anchor_component` × n | `LEVEL <name> = <column> [BASE]` | every component realized exactly once; no duplicate/unknown; per-universe leaf-name uniqueness | **M** / **L** |
| **universe** (unrestricted only) | `basis`, `anchor`; **no** `restriction` | — (composes) | `UNIVERSE <n> = <dim>[ * <dim>]` | every base dim has a `LEVEL`; **refuse if a restriction is present** | **C** |
| **measure** | `value_type`, `root_member` | `member.endpoint`, `root_evaluator` | `MEASURE <n> ON <u> FROM <t> AS <agg>(<expr>)` | `FROM` taken from the mapping only, never invented; `root_evaluator` ∈ allow-list | **M** / **C** |
| **member** | `measure`, `anchor`, `universe` | `member` realization | `FAMILY { <agg> }` | present in `REGISTRY`, `kind == REDUCER`, `signature_ok` against the declared `logical_type` | **C** |
| **identity** | `ref` | `publication_ref` | `SOURCE_MANIFOLD <id> VERSION <semver>` | emitted ref **==** `artifact.ref`, exact string equality on both fields | `InputIdentityMismatch` |
| relationship · hierarchy · attribute | present | — | **none** | must **refuse**; never silently omitted | **C** (scope) |
| boundary | present | — | **none** | `across` has no representation | **G** |
| crosswalk | present | — | **none** | insufficient shared law | **L** |

`ON <universe>` is emitted on **every** measure. The single-universe sugar is never relied on: its
behaviour changes the moment a second universe appears.

---

## 5. Compile / emission / receipt contract — RATIFIED

```
compile(publication: GovernedPublicationArtifact,
        mapping:     PrivateCoreMapping)   ->   CLOSED execution image
```

**`GovernedCertificationMissing` does not fire from `compile()`.** Compilation answers "can governed law
be faithfully translated into the Core execution representation?"; certification answers "is this path
licensed on this realization and data state?" P0.5a already shipped the adjudicate-and-serve half of
that split, and the receipt module's own lifecycle places `compile CLOSED image` before adjudication.
Compile-time categories stay distinct and are never collapsed into a generic lowering error, with
`InputIdentityMismatch` seated ahead of the four gap categories.

**Determinism is a hard requirement.** The receipt binds **byte digests of the files as shipped, with no
canonicalization**, so identical inputs must produce a byte-identical `.cml`. Therefore: no timestamp
and no ordering nondeterminism may enter the image, and `MANIFOLD <name> VERSION <int>` — the integer
engine revision, a different identity from the source semver — must be derived deterministically
(K0: constant `1`) rather than minted per run.

**Receipt emission is fixed by the shipped verifier, not proposed here.** Required keys:

```jsonc
{ "receipt_format_version": "1.0",            // major must be 1
  "publication_ref": { "manifold_id": ..., "version": ... },
  "publication_digest": "sha256:<64 lowercase hex>",
  "image_digest":       "sha256:<64 lowercase hex>",
  "compiler": { "name": <non-empty str>, "version": <non-empty str> },
  "mapping_provenance": <optional, opaque>,
  "established_at":     <optional str> }
```

`compiler` is required and well-shaped but never interpreted; `mapping_provenance` and `established_at`
are excluded from the binding and are never runtime admission dependencies. Unknown keys are ignored
rather than mapped, so no publication meaning can reach the runtime through the receipt.
`established_at` may therefore be stamped — but nothing time-varying may enter the `.cml` itself.

---

## 6. `PrivateCoreMapping` location — RATIFIED

**The format is specified in the `columna` tree, and its reader lives there too — stdlib-only, mirroring
`PublicationArtifactData`. K0 freezes no producer-side type.**

Constraints that drive it: the trees are import-disjoint and test-enforced; `f0_reconnaissance.md`'s
ownership map already labels `manifold_agent.mapping.Binding` **CORE** (private realization), unlike the
SHARED logical modules beside it; f0 ruling 2 places the compiler "likely a separate compiler module in
the `columna` codebase, **not literally `columna_core.lower`**"; and `columna-server` must never load the
mapping at all — its receipt verification is defined as proceeding *without* it.

**Ruled location: `columna_core`.** The reader and the compiler module live inside the existing
`columna-core` distribution — **not** a new `columna-compiler` package, which is what this note proposed
before ratification and which is hereby superseded. Two reasons the ruled placement is the better one:

* **No new distribution.** A separate package would need its own PyPI Trusted Publisher registration,
  its own version lockstep decision, and its own dependency caps — release-set surface bought for
  nothing, on a repository whose release-coherence guards already fail closed on exactly that class of
  mismatch.
* **It does not contradict f0 ruling 2.** That ruling barred `columna_core.lower` *literally* while
  placing the compiler in "a separate compiler module in the `columna` codebase". A distinct module
  inside `columna_core` satisfies both halves.

Unchanged by the ruling: the compiler parses and `check()`s its own output (self-verification, not a
second grammar); `columna-server` never imports it and never loads the mapping; and Studio and
manifold-agent can produce the JSON later without either tree importing the other.

---

## 7. K0 acceptance-test outline — RATIFIED

**No image to reproduce.** Every `.cml` in the repository contains `HIERARCHY` and/or `RELATE`; there is
no measure/member/anchor-only fixture anywhere. K0 **authors the first one**, and proving it clean is
the deliverable.

Following the testing doctrine ratified at P0.5a closure — **pin the reason for refusal, not merely that
something refused**:

1. **Identity precondition** — `mapping.publication_ref != artifact.ref` raises `InputIdentityMismatch`
   *before* any lowering runs.
2. **Determinism** — compiling twice yields byte-identical output and an identical `image_digest`.
3. **Round-trip** — the emitted `.cml` parses and `check()`s clean through `columna_core`.
4. **Identity emission** — `SOURCE_MANIFOLD` equals `artifact.ref` exactly, both fields (the comparison
   is exact string equality; there is no semver range logic).
5. **Refusal taxonomy** — one test per category, each asserting the *named* category: measure with no
   member (**L**); anchor component missing / duplicated / unknown (**M**); reducer outside the allow-list,
   and universe carrying a restriction (**C**); boundary declaration (**G**); ref mismatch (identity).
6. **Scope refusals are refusals** — a publication containing a hierarchy, relationship or attribute
   **refuses**; it never compiles to an image that silently omits the construct.
7. **End-to-end governed admission** — compile, write the four-file runtime folder, load through
   `columna-server`: `ENTRY_GOVERNED` with zero conditions. This converts the receipt's test-constructed
   fixtures into the end-to-end governed-producer proof that 0.15.2 explicitly does not yet have.
8. **Negative admission** — mutating one byte of the emitted `.cml` yields `lowering_receipt_mismatch`
   and not governed standing.
9. **Blast wall** — no physical identifier appears in the artifact, and the compiler opens nothing but
   its two inputs.
10. **A receipt implies no admission** — the governed runtime answers a kernel measure query while
    `certified_edges` / `certified_faces` remain empty.

---

## 8. Closed and deferred at ratification

**Closed for this unit:**

* **D4 — `bridge` / `via` (M:N): OUT OF K0.** Closed for this unit, not merely moot. Reopens only if a
  later unit brings relationship into scope.

**Deferred, and explicitly NOT K0 blockers:**

* **`median` / `mode` compiler classification** — still deferred (§2). It does not block K0.
* The **`mean` late-refusal hole** (§2) — a property of shipped Core independent of K0: a defect that
  parses and validates at publish time and only refuses at query time. **Not a K0 blocker.** Recorded
  here; not repaired here.

---

### Governing stop rule (verbatim, unchanged)

> If the governed publication does not contain enough meaning to compile, stop. If the private mapping
> does not contain enough realization information to compile, report a mapping gap. In neither case may
> the compiler invent the missing fact.
