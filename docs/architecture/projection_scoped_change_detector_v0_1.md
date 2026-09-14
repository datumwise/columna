# Projection-scoped change detector — specification — **v0.1 CANDIDATE**

**Status:** candidate, prepared 2026-09-14 on instruction, for review. **Nothing here is
implemented.** `Standing.currency` continues to record `None`, and both adapters continue to return
`data_state=None`, until this specification is ruled.

**Authority:** [`source_adapter_contract_v1_candidate.md`](source_adapter_contract_v1_candidate.md)
§5.1 (RULED 2026-09-14) admits *"a projection-scoped, scan-derived content change detector"* subject
to eight conditions. This document answers the six construction questions that ruling requires to be
settled **before** implementation, and settles them from measurement rather than from Core's
implementation, which it is explicitly forbidden to copy mechanically.

**Naming discipline, restated because it is load-bearing.** This is a **projection-scoped change
detector**. It is not table identity, not snapshot identity, not MVCC identity, not a freshness
token, and not a collision-free content identity. Everything below is written to make that
narrowness true rather than merely declared.

---

## 0. Why the scan and nothing but the scan

The ruling's condition (1) — computed from the same material observation — is not satisfiable on
DuckDB by any catalog surface. Measured, duckdb 1.5.5: inside one transaction and one statement, the
scan returned **2 rows** while `duckdb_tables().estimated_size` returned **3** and
`pragma_storage_info` returned **6**, because another connection had committed in between. Data is
under MVCC; the catalog is not.

A detector composed of window aggregates over the projection has no such gap **by construction**: it
is computed from the same rows that are delivered. Measured under the same concurrency test, the
scan-derived triple was identical before and after another connection's committed insert, and moved
only after the reading transaction committed and re-read.

**Consequence for the adapter: no second query, and no second connection.** The adapter opens one
ADBC connection per `fetch` and closes it; a token requiring a second statement would be a token
from a different moment, and on this adapter also from a different connection.

---

## 1. Which projected columns enter the detector

**All of them, and only them** — the exact column list the realization asked for, which for the
anchored path is the de-duplicated union of the anchor-component columns and the family's value
column.

- **Only them**, because the adapter has no mandate to read unprojected material. `MaterialSource`
  makes a full-object read structurally inexpressible, and widening the detector's input to the
  whole table would reintroduce the full-object read through the back door — buying a stronger
  token by doing the thing the interface exists to forbid.
- **All of them**, because the retained state depends on every projected column: a change to a
  coordinate is as much a change to the state as a change to the value.

**The scope statement this forces, and it must be carried in the token's own name:** the detector
says *"this projection of this object is unchanged"*. It says **nothing** about unprojected columns,
other objects, or the database. A token that moved would mean the state must be re-established; a
token that did not move means only that **the material this state was derived from** is unchanged.

**Open, and deliberately not settled here:** whether two states over *different but overlapping*
projections of one object may compare their tokens at all. The conservative reading is that they may
not — different projections yield different detectors, and comparing them is comparing two different
questions. Recorded so an implementation does not assume otherwise.

## 2. Whether row order is irrelevant

**It must be, and the aggregates measured are.** `count`, `sum` and `bit_xor` over the projection
returned identical values for the same two rows inserted in either order.

This is a **requirement**, not a convenience: CAP v1 carries **no ordering guarantee**, and the
adapter emits no `ORDER BY`. An order-sensitive detector would therefore report spurious change on a
source that re-ordered rows without changing them — turning a lawful reuse into a re-materialization
on the strength of a fact the profile explicitly declines to observe.

**Any order-sensitive construction is therefore excluded**, including running hashes, positional
digests, and hashing the concatenated result in delivery order.

## 3. How NULL participates

**NULL must be distinguishable from every non-NULL value, including from the string `'NULL'`.**

Measured: rendering a row through DuckDB's struct-to-`VARCHAR` cast distinguishes them, because it
quotes strings — `(1, NULL)` renders as `(1, NULL)` and `(1, 'NULL')` renders as `(1, 'NULL')`, and
the two hash differently. An empty string is likewise distinct from NULL.

**This must be asserted by control, not relied upon**, because it is a property of a rendering and
not of the detector's design. The failure it guards against is specific and quiet: a source
replacing a NULL with the literal text `NULL` is a real change to the material, and CAP v1's
absence rule (`want_of_law` on an ungoverned absent observation) turns on exactly that difference.

**Also required:** a row that is entirely NULL must contribute to the detector, not be skipped.
Measured: it does — it produces a non-zero hash and is counted.

## 4. How coordinate and value types participate

**The value aggregate ALONE is not sufficient, and this is the sharpest finding in this document.**

Measured: `DECIMAL(18,4)`, `DECIMAL(10,4)` and `DECIMAL(38,4)` each holding `10.0000` render
identically and **hash identically**. Precision and scale do not survive the rendering. So a source
whose value column changed from `decimal128(18,4)` to `decimal128(10,4)` — a change CAP v1's value
envelope **would refuse** on the next read — would leave the value aggregate completely unmoved.

**Therefore the detector must carry a separate SCHEMA DIGEST over the ordered
`(column_name, delivered_type)` pairs of the projection**, and it must be over the **delivered
Arrow types**, not the source's declared SQL types — because the delivered schema is what admission
inspects, and it is the only schema the adapter is entitled to claim it observed.

Types that *do* differ in rendering (`DECIMAL(18,4)` vs `DOUBLE` vs `DECIMAL(9,2)`) were measured to
hash differently, but that is incidental and must not be relied on: the schema digest is the
mechanism, and the value aggregate's type-sensitivity is a coincidence of formatting.

## 5. Whether duplicate rows affect it correctly

**Not under `bit_xor` alone — and the measurement is the reason the detector is a triple, not a
digest.**

Measured: `bit_xor(hash(row))` **cancels to `0`** for two identical rows, and again for four. Any
even number of identical duplicate rows contributes nothing. Used alone it would be blind to a
source that duplicated every row.

`count(*)` and `sum(hash(row))` both move on that change (`1 → 2 → 4`, and the sum scales), so **the
triple detects it**. The specification requirement is therefore:

> **All three aggregates are load-bearing and none may be dropped as redundant.** `count` sees
> cardinality; `sum` sees multiplicity; `bit_xor` sees content permutation that preserves both. Each
> covers a class the others miss, and `bit_xor`'s cancellation is the concrete proof that "the hash
> already covers it" is false.

**A control must assert the cancellation directly**, so that a future simplification to a single
aggregate fails loudly rather than silently weakening the detector.

Note this interacts with admission but does not duplicate it: CAP v1's CHECK 5 refuses a carrier
with repeated coordinate tuples, so duplicated rows would be refused at the next read anyway. The
detector's job is different — it must **move**, so the state is re-established and admission gets
the chance to refuse.

## 6. How the detector is encoded

**An opaque string, namespaced on both axes the ruling requires**, of the shape:

```
<detector-algo-version>/duckdb-<engine-version>:<count>:<sum>:<bit_xor>:<schema-digest>
```

Rules the encoding must satisfy:

- **Opaque to Platform.** Platform may compare two tokens for equality **from the same adapter** and
  do nothing else with them — never parse, order, range-check, or derive meaning from a component.
  The internal structure exists for the adapter's own conservatism, not as a public field set.
- **Namespaced by detector/algorithm version.** Bumped whenever the composition changes. Two tokens
  with different algorithm tags are **incomparable, which must read as changed** — never as equal,
  and never as an error.
- **Namespaced by DuckDB engine version.** `hash()` is documented by DuckDB as free to change
  between releases. An engine change must therefore read as **conservative invalidation**, not as an
  ambiguous comparison between two digests that were never comparable.
- **Incomparable reads as stale.** This is the polarity two mechanisms in this house already share
  (`constitution_status` returns STALE when the fingerprint scheme changes; `Connector.data_identity`
  returns `None` rather than an unwarrantable token). The detector makes it three.

### What must yield `None`

- the detector cannot be computed in the same statement as the projection;
- any error establishing it;
- the projection is empty of columns, or the delivered schema cannot be read;
- the adapter cannot warrant **both** halves of the guarantee — moves-on-change *and*
  stable-when-unchanged — for this source.

`None` is not a failure to serve. It is a failure to **reuse**, and "unknown" must never be read as
"unchanged".

---

## 7. What this specification deliberately does not settle

- **Whether Platform consumes the token at all.** `read_anchored` does not read `Material.data_state`
  today and `materialize_anchored` writes `currency=None` by rule. Wiring it is a separate unit.
- **Realization currency.** A data-state token answers *did the material observation change*. It
  does not answer *is the realization assertion still the correct assertion about this source*, and
  it must not be used as though it did. That jurisdiction stays open.
- **Cross-adapter comparison.** Tokens are comparable only within one adapter. Nothing here defines
  comparison across sources, and the conservative reading is that it is meaningless.
- **Collision bounds.** This is a change detector. It is not collision-free and must never be
  documented as if it were, no matter how wide the hash.
