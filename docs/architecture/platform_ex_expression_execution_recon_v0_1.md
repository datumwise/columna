# Recon E-X — the expression-execution boundary

**Status:** reconnaissance, recorded. No implementation authorized by this document.
**Commissioned:** Huayin, 2026-09-29, between M-2 and F-1.
**Why then:** M-2 made `ExpressionEvaluator` a real boundary and F-1 was about to make the Fulfillment
Coordinator depend on it. The question was whether the evaluator contract is shaped correctly for heavy
columnar compute *before* the coordinator freezes around it.

> The governing principle: **semantics above; physical columnar execution below.**

---

## A · Current compute-placement inventory

Legend: **(a)** Python per-cell/per-row loop · **(b)** Arrow-native (`pyarrow.compute`) · **(c)** DataFusion
· **(d)** DataSketches/native · **(e)** other (Python scalar / predicate / dispatch).

### The headline placements

| What | Where | Class | Python iterations per call |
|---|---|---|---|
| **AOV division — columnar** | `columnar/provider.py:289-292` | **(b)** `pc.equal` → `pa.nulls` → `pc.if_else` → `pc.cast`×2 → `pc.divide` | **O(1)** for the whole column |
| **AOV division — in-memory** | `kernel/builtins.py:266-275` (`total / n`) driven by `kernel/expression.py:199-204` | **(e)** scalar, driven by **(a)** | **O(cells)** |
| **HLL estimate — columnar** | `columnar/provider.py:293-296` → `estimate_of` at `:111-112` | **(a)** Python comprehension over **(d)** | **O(cells)**, each a full deserialize + `get_estimate` |
| **HLL estimate — in-memory** | `kernel/builtins.py:261-263` | **(d)** | O(1), once per cell from the **(a)** loop |
| **HLL union / structured continuation** | `columnar/provider.py:63-99` UDAF, executed at `:204-206` | **(c)** driving **(a)**+**(d)** | O(rows) inside the accumulator |
| **ADDITION continuation** | `columnar/provider.py:232` → `DF.sum` | **(c)** | fully native |
| **ADDITION continuation — in-memory** | `kernel/builtins.py:279` (`lambda a, b: a + b`) via `kernel/value.py:67-82` | **(e)** driven by **(a)** | O(cells) |
| **LAST / LATEST_BY_ORDER** | **no columnar realization** — `provider.py:236-240` raises `unrealized-composition` | in-memory only, `builtins.py:240-258` **(a)** | — |

### Family continuation, end to end, as actually executed

```
ColumnarMME.measure (columnar/mme.py:495)
  → _continue (:640)
      → _target_index (:657-670)         (a)  O(cells × width) Python set-comprehension
      → _block_of (:672-677)             (a)→(b)  O(cells × width)
      → provider.continue_grouped (:155)
            → pc.filter                  (b)  O(1) Python
            → DataFusion aggregate       (c)  ← the only heavy native step
            → group materialization      (a)  O(groups × width) Python
      → align_onto (:243)                (a)  O(target points) Python reindex, then pa.array (b)
```

**The DataFusion step is bracketed on both sides by Python passes at cell scale.** That is the single most
consequential finding in this inventory and it is about continuation, not expressions.

### Alignment / compatibility work — all Python, one exception

| Site | Class | Cost |
|---|---|---|
| `columnar/index.py:64-78` `CoordinateIndex.identity` | **(e)** Python + `json.dumps` + `sha256` | **O(cells × width) per property ACCESS — not cached** |
| `columnar/expression.py:130` layout check | reads `.identity` twice per role pair | O(#roles × cells) |
| `columnar/index.py:146-149` `aligns_with` | two full digest recomputations | O(cells) ×2 |
| `columnar/index.py:96-100` `columns()` | **(a)** | O(cells × width) |
| `columnar/standing.py:150-156` `take` | **(b)** `Array.take` | O(1) Python — **the only Arrow-native reindex primitive, and `align_onto` does not use it** |

### DataFusion containment — the good news

`datafusion` is imported at exactly **two lines in the whole package**: `columnar/provider.py:47-48`.
Nothing above the provider imports it, constructs a `SessionContext`, or holds a `DataFrame`.

What *does* travel upward is **text**: `provider.py:207` writes `"datafusion: aggregate(...)"` into
`ContinuationResult.route`, `columnar/mme.py:655` copies it onto the served `Answer`, and
`columnar/exhibit.py:397,536` assert on the substring. `provider.py:273` sets
`AlignmentReport.from_identity = "datafusion-group-output"`. The provider **name**
(`"arrow+datafusion"`) also reaches `RealizationStanding` and thence `RetentionKey`.

**Assessment: this is provenance, not leakage.** No engine handle, no concept and no capability crosses
upward — a reader learns which engine folded the value, which is exactly what realization standing is for.
It would become leakage the moment anything *branched* on it; nothing does.

### SQL — none, and already guarded

No `.sql(` call exists in the package. No f-string or concatenation builds a query. The only `SELECT`
tokens are Frame-QL's own DSL (`frameql/syntax.py:29,97`). `columnar/exhibit.py:693-706` already scans
every `.py` in `columnar/` for `.join(` and `.sql(` and asserts the absence at `:556`.

**§3 is currently satisfied and mechanically enforced.** Nothing needs doing.

---

## B · Evaluator boundary assessment

The intended pipeline:

```
governed expression → resolved Arrow operands → physical execution request
                    → DataFusion / Arrow-native provider → Arrow result
```

**The boundary supports this today, with one defect.**

What is already right:

* `columnar/expression.py:170-171` is the *only* arithmetic call in the evaluator —
  `self.families.provider.evaluate_positional({role: states[role].values}, kernel=...)`. Operands cross as
  `pa.Array`, one per role, on one `CoordinateIndex`. That is already "resolved Arrow operands".
* Everything above that line is governed semantics: basis routes (`:86-87`), the seam to family state
  (`:116-117`), layout identity (`:128-138`), instance compatibility (`:139-140`), want-of-state
  (`:155-156`), data-state attribution (`:173-180`), disclosures (`:182-195`). None of it touches a value.
* The evaluator holds **no** DataFusion concept, no `SessionContext`, no SQL.

### The defect: the evaluator names a physical kernel

```python
# columnar/expression.py:169
kernel = "ratio" if law.name == "MEAN" else "hll_estimate"
```

Compare its in-memory twin:

```python
# kernel/expression.py:193
apply = self.families.provider.capability(law.name, "apply")
```

The kernel path dispatches through `ProviderProfile.capability` — a provider-owned table. The columnar
path **hard-codes a string switch on the law name and names the physical kernel upward.** `"ratio"` and
`"hll_estimate"` are execution concepts; the evaluator should be naming a *law* and letting the provider
say how it executes one.

Consequences as it stands:

1. a third expression constructor requires editing the **evaluator**, not the provider;
2. a second columnar provider (DuckDB, native kernels) must adopt the same two magic strings;
3. `ColumnarProvider` has **no `capability()` method at all** (`grep "def capability"` → only
   `kernel/realization.py:113`), so there is nowhere for it to declare what it can execute.

Related dead surface: `Realization.finalize` (`kernel/realization.py:78`) is declared and **never
populated or called** anywhere. HLL finalization is routed through `apply` instead
(`kernel/builtins.py:289`). A finalization slot exists on paper and is not the one in use.

> **RESOLVED — E-3 retired the slot (2026-09-29).** Asked whether it named any legitimate *family-level*
> responsibility under v8, the answer is no, and structurally so: a structured family law names its
> finalizer by governed law name (`HLL_SKETCH.finalized_by == "HLL_ESTIMATE"`), and that named law's own
> realization supplies it through `apply`. A `finalize` on the FAMILY's realization would be a second route
> from family state to a displayed number, owned by a provider and authorised by no law — reachable without
> ever consulting `finalized_by`. It was also strictly weaker than the `apply` it duplicated (one payload,
> no parameters, and sketch parameters are compatibility-bearing). The concept's correct residue is already
> in the code on the columnar half: `ExecutionCapability.finalizes` is **derived** from a value-form
> transition and asserted nowhere. The ruling is recorded in `kernel/realization.py`'s module docstring.

---

## C · Minimum provider contract the evaluator would need

Derived from what the evaluator actually asks for today, and no more:

```
ExpressionExecutionProvider
    name
    realizes_constructor(law_name) -> bool          # capability, asked before execution
    capability(law_name, "apply") -> callable       # the dispatch the kernel path already has
    apply(law_name, operands: Mapping[role, Array], parameters) -> Array
```

Three properties that must hold and do:

* **operands arrive resolved.** The provider never fetches, never measures, never sees a `MeasureFamily`.
* **geometry is preserved.** Expression evaluation is a MAP: one coordinate index in, the same index out.
  The provider needs no `target_index` parameter, which is precisely what distinguishes it from
  continuation.
* **the result is Arrow.** No conversion at the boundary.

The only change from today is that `law_name` replaces `kernel`, and the provider owns the mapping.

---

## D · Shared provider abstraction, or separate?

**The code makes ONE provider object inevitable and TWO capability contracts inevitable.** Both halves of
that matter.

One object, because `ColumnarProvider` already is one: it holds the single `SessionContext`
(`provider.py:152`), the UDAF registration (`:98-99`), the Arrow plumbing, and both verbs. Splitting into
`ColumnarContinuationProvider` and `ExpressionExecutionProvider` as separate classes would duplicate the
session, the sketch helpers and the alignment machinery for no gain.

Two contracts, because the verbs are genuinely different in kind:

| | `continue_grouped` | `evaluate_positional` |
|---|---|---|
| shape | **REDUCER** — changes the anchor | **MAP** — preserves the index |
| needs a target index | **yes** (`target_index=`) | no |
| standing | must propagate participation/support masks and produce a new `ColumnStanding` | derives from the operands; produces a value column |
| result | `ContinuationResult` (index + values + standing + route) | a bare `pa.Array` |
| failure mode | `unrealized-composition` | none today — the string switch cannot fail |

A merged `execute(request)` would have to make `target_index` and `standing` optional, and "optional
because the other shape does not need it" is how a contract stops describing either shape.

**Recommendation: one `ColumnarExecutionProvider` object with a declared capability table keyed by
(shape, law)** — `MAP` / `REDUCER`, and `SCAN` when scans arrive — rather than two classes or one merged
method. Do **not** rename or restructure now; the capability table is the part with present value, because
it is what removes the string switch.

---

## E · Seam correction needed before F-1

**None for the expression-execution boundary.**

F-1's coordinator depends on exactly two things: `evaluator.evaluate(expression, anchor, basis_id=,
data_state=)` returning an `Answer`, and `GovernedExpression.admitted_bases` (a governed declaration, not
evaluator internals). The kernel-name switch lives *inside* `_establish`, below both. **F-1 does not
harden it**, and F-1's suite pins that insulation by swapping in a substitute evaluator the coordinator
cannot distinguish.

So the defect in §B is recorded for the DataFusion unit and deliberately **not** fixed here.

> One correction *was* needed for F-1, in a different seam, and was made: `kernel.MME.measure` took a
> `MeasureFamily` while `ColumnarMME.measure` took a `family_id` string, so no component above both could
> call either without knowing which engine it held. `MME.subject` now normalises either spelling and both
> engines accept both, changing no existing call site. That is the fulfillment seam, not this one.

---

## F · Recommended timing for DataFusion expression execution

Sequenced by dependency, not by appetite. **Steps 1 and 2 are independent of DataFusion entirely** and are
worth more per line than step 3.

1. **Give `ColumnarProvider` a capability table** and delete the string switch at
   `columnar/expression.py:169`. Interface-only, no behaviour change, no new engine. This is the
   prerequisite for every later provider, including a DuckDB one.
2. **Cache `CoordinateIndex.identity`.** It is a frozen dataclass computing a JSON dump + SHA-256 on every
   property access, and it is accessed in the evaluator's hot layout check. A one-line memoisation removes
   an O(cells × width) Python pass per access. Pure win, no design content.
3. **Move `hll_estimate` off the Python comprehension** (`provider.py:293-296`) to a DataFusion UDF or an
   Arrow kernel. This is the one expression path that is O(cells) in Python, and the only one where
   DataFusion buys something today — `ratio` is already fully Arrow-native and would gain nothing.

   > **⚠️ THIS RECOMMENDATION WAS WRONG, AND E-3 REVERSED IT (2026-09-29).** Both named routes fail, and the
   > recon could not see it because — as its own *Bounded claims* section says — **it benchmarked nothing.**
   > E-3 measured, on 2 000 sketches:
   >
   > * the same loop inside a **DataFusion Python UDF costs 1.95 µs/cell against 1.51 in-process — 1.29×
   >   SLOWER.** A Python UDF *is* a per-batch Arrow→Python→Arrow round trip with the same comprehension
   >   inside it. *"A DataFusion UDF that simply contains the same Python per-cell loop is not an
   >   architectural improvement"* (Huayin, 2026-09-29) — and this one is not even a faster one.
   > * DataFusion's only native HLL capability, **`approx_distinct`, is the wrong operation and returns a
   >   confident wrong number** over the governed family value: it counts distinct *blobs* (2 where the
   >   population is 4). Its internal HLL is a vendored redis derivative with no header or version, not
   >   interoperable with DataSketches' `serialize_compact()` at any level.
   > * **there is no Arrow kernel** and could not be: the work is a third-party sketch decode.
   >
   > What E-3 did instead: it **characterized** the boundary and removed the *carriage* around it — one
   > vectorised `to_pylist()` in place of N boxed scalars with two `as_py()` calls each, for 36.8% (uniform
   > 172-byte sketches) to 22.8% (mixed 12–4136-byte sketches) less CPU, leaving a remainder within 8% of
   > the native floor. The loop that stays is one `hll_sketch.deserialize(...).get_estimate()` per sketch,
   > i.e. already native.
   >
   > A genuinely vectorized native form **does** exist — Apache's own Rust crate `datasketches` ≥ 0.5.0
   > reads C++ compact HLL images, DataFusion 54 accepts Rust UDFs in-engine via the `datafusion-ffi`
   > PyCapsule protocol, and `datafusion-comet` PR #4802 is a merged reference. It is deferred **not for
   > want of a library** but because the Rust crate's estimates are not bit-identical to the C++ library's
   > for merged sketches (≈0.7%, inside RSE but not zero): adopting it is **a second `RealizationStanding`,
   > not a faster path to the same value**, and belongs to a provider unit with its own admission evidence.
   > See `packages/columna-platform/tests/test_e3_hll_estimate_execution.py` §C, and the adjudication
   > recorded on `provider.estimates_of`.
   >
   > **Step 4 stands and is now the live recommendation** — the continuation brackets are the larger cost and
   > E-3 measured nothing that changes that.
4. **Then, and only then, consider the continuation brackets** — `_target_index`, the group
   materialization, and `align_onto`. These are the largest Python costs in the system and they belong to
   *continuation*, not expressions, so they are an MME-side unit and should be scoped as one.
5. **Scans and windows: not yet.** No current expression needs them, and a provider contract that declared
   `SCAN` before a caller existed would be designed against a guess.

**Do not start at step 3.** The temptation is to reach for DataFusion because it is the interesting part;
the inventory says the cheapest real wins are a dispatch table and a memoised digest.

---

## Bounded claims

This recon read the code and did not benchmark anything. Every cost above is an **iteration count read off
the source**, not a measurement. Where it says O(cells) it means a Python-level loop over cells exists at
that line; it does not say that loop is the bottleneck in any workload, because no workload has been
profiled. A performance unit should measure before acting on step 4.
