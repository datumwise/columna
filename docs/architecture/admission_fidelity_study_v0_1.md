# Admission fidelity — first empirical study — v0.1

**Status:** measurement record, 2026-09-12. **Not a contract and not a ratified envelope.** It
records what was observed, on one machine, at the versions below, so that the admission boundary is
specified against measurement rather than assumption.
**Commissioned as:** the early read-only ADBC/Arrow fidelity reconnaissance of Phase 0 — measurement,
not ingress construction.

---

## 1. The envelope actually under study

The admission envelope is **not** driver → Arrow. It is:

> **source semantics → driver / configuration → Arrow → any in-process carrier conversion (e.g. Polars)**

That fourth hop is not decoration. Two of the three collapses found below happen at it or at the
configuration boundary, not at the driver, and the fourth hop is the one **inside** Columna today:
`connector.py` does `pl.from_arrow(con.execute(q).arrow())` on every fetch.

## 2. Environment

| | |
|---|---|
| python | 3.12.14 |
| platform | Linux-6.12.105-fly-x86_64, glibc 2.41 |
| pyarrow | 25.0.1 |
| polars | 1.44.2 |
| duckdb | 1.5.5 |
| adbc-driver-manager | 1.12.0 |
| adbc-driver-sqlite | 1.12.0 |
| SQLite engine (via ADBC) | 3.53.1 |
| PostgreSQL | **not available** — no server in the environment; the third driver family is **not established** |

**Crossings tested.** Three. The first is the incumbent Columna doorway, included deliberately so the
comparison is against what ships, not against an idealization.

1. `duckdb-native` — `duckdb.execute(sql).arrow()` → pyarrow → `pl.from_arrow`
2. `duckdb-adbc` — ADBC driver manager loading duckdb's `duckdb_adbc_init` entrypoint → `fetch_arrow_table` → `pl.from_arrow`
3. `sqlite-adbc` — `adbc_driver_sqlite` → `fetch_arrow_table` → `pl.from_arrow`

Raw run records and the probe scripts themselves: `admission_fidelity_v0_1/` beside this document
(`run_1_matrix.txt`, `run_2_followups.txt`, and the two scripts that produced them). Reproduced in
§3–§4. The probes are deliberately **not** wired into CI — they need two ADBC drivers that are not
dependencies of any package here, and a measurement exercise must not add one.

---

## 3. Matrix — DuckDB via ADBC

| case | arrow type | arrow value | polars dtype | result | guarantee or observation? |
|---|---|---|---|---|---|
| `DECIMAL(38,9)` exact | `decimal128(38, 9)` | `123456789012345678.123456789` | `Decimal(38, 9)` | **preserved** | observation |
| `DECIMAL(18,4)` money | `decimal128(18, 4)` | `12345678901234.5678` | `Decimal(18, 4)` | **preserved** | observation |
| `DECIMAL(3,1)` 0.1+0.2 | `decimal128(4, 1)` | `0.3` | `Decimal(4, 1)` | **preserved** | observation |
| `HUGEINT` / int128 | `decimal128(38, 0)` | `170141183460469231731687303715884105727` | `Decimal(38, 0)` | **POLARS LOSS** | observation |
| `TIMESTAMP` µs | `timestamp[us]` | `2026-09-12 11:59:00.123456` | `Datetime('us')` | preserved | observation |
| `TIMESTAMP_NS` | `timestamp[ns]` | *`as_py()` raises `ValueError`* | `Datetime('ns')` | preserved in carrier; **unreachable via `as_py()`** | observation |
| `TIMESTAMPTZ` `-04:00` | `timestamp[us, tz=Etc/UTC]` | `2026-09-12 15:59:00+00:00` | `Datetime('us', tz)` | instant preserved, **source offset normalized** | observation |
| `TIME` | `time64[us]` | `11:59:00.123456` | `Time` | preserved | observation |
| `DATE` | `date32[day]` | `2026-09-12` | `Date` | preserved | observation |
| NULL in decimal column | `decimal128(18, 4)` | `None` | `Decimal(18, 4)` | preserved, **type survives** | observation |
| all-NULL typed column | `timestamp[us, tz=Etc/UTC]` | `None` | `Datetime` | preserved, **type survives** | observation |
| empty string | `string` | `""` | `String` | preserved, distinct from NULL | observation |
| `LIST<INT>` | `list<l: int32>` | `[1, 2, 3]` | `List(Int32)` | preserved, representation differs | observation |
| `STRUCT` | `struct<a: int32, b: string>` | `{'a': 1, 'b': 'x'}` | `Struct` | preserved | observation |
| `MAP` | `map<string, int32>` | `[('k', 1)]` | `List(Struct)` | value preserved, **map-ness lost** | observation |

## 4. Matrix — SQLite via ADBC, and the incumbent DuckDB path

| crossing | case | arrow type | result |
|---|---|---|---|
| `sqlite-adbc` | decimal stored as `TEXT` | `string` | preserved exactly (`12345678901234.5678`) |
| `sqlite-adbc` | decimal stored as `REAL` | `double` | **SOURCE LOSS** → `12345678901234.568` |
| `sqlite-adbc` | int64 max | `int64` | preserved |
| `sqlite-adbc` | timestamp / tz as `TEXT` | `string` | preserved as text; no temporal type at all |
| `sqlite-adbc` | NULL | `int64` | preserved |
| `sqlite-adbc` | untyped column `1,2,3,'surprise'` | `string` | **TOTAL TYPE COLLAPSE** → `['1','2','3','surprise']`, order-independent |
| `duckdb-native` | `DECIMAL(18,4)` via `.arrow()` | `decimal128(18, 4)` | **preserved**, including through `pl.from_arrow` |
| `duckdb-native` | row order with no `ORDER BY`, 5 runs | — | identical each run — **observation only, not a guarantee** |

Follow-ups worth recording precisely:

- **`.arrow()` now returns a `RecordBatchReader`** in duckdb 1.5.5, not a `Table`. `pl.from_arrow`
  accepts it and preserves `Decimal(18,4)`. Any admission code that assumes a `Table` will break on
  this version.
- **HUGEINT is a real loss, not a display artifact.** Arrow holds
  `Decimal('170141183460469231731687303715884105727')`; Polars yields
  `Decimal('1.7014118346046923173168730371588410573E+38')`. Nothing raises.
- **Timezone type is set by configuration, not by data.** With `SET TimeZone='America/New_York'`,
  the same instant arrives as `timestamp[us, tz=America/New_York]` instead of `tz=Etc/UTC`.
- **Decimal ceiling measured:** `DECIMAL(38,37)` crosses intact; `decimal128` carries 38 digits.
- **NULL and NaN remain distinguishable** in a float column through both Arrow and Polars
  (`null_count = 1`, `nan` present as a value).

---

## 5. Guarantee versus observation

Nothing in §3–§4 is a contractual guarantee. Every row is an **observation at the stated versions**,
and the distinction matters for how admission is written:

- **Observation.** Every type mapping above. Driver type mappings are implementation behaviour of a
  specific driver build; a version bump may change them, which is why admission must **check the
  Arrow schema it actually received** rather than trust a remembered mapping.
- **Observation, explicitly not a guarantee.** Row order without `ORDER BY`. Stability across five
  runs establishes nothing about ordering; no ordering claim may be derived from it.
- **Structural, and therefore stronger than an observation.** Arrow's type system *has* a
  `decimal128(p, s)` and a validity bitmap distinct from values. That a faithful representation
  EXISTS is a property of the format; that a given driver USES it is an observation.
- **Source-determined, not transport-determined.** SQLite has no decimal and no temporal type, so a
  decimal's fidelity there depends on a storage decision (`TEXT` vs `REAL`) invisible to the
  consumer. No transport can restore what the source never held.

---

## 6. The three collapse points

1. **The source type system.** SQLite `REAL` for a decimal: `12345678901234.5678 → …568`, at rest,
   before any driver runs. Admission cannot repair it and must refuse it.
2. **Driver / configuration.** `TIMESTAMPTZ` arrives as `tz=Etc/UTC` or `tz=America/New_York` for
   the *same instant* depending on a session setting. The instant survives; the source zone does
   not. A distinction decided outside the data is a distinction admission must pin explicitly.
   SQLite's whole-column coercion to `string` belongs here too — the driver chose one type for a
   column the source never typed.
3. **Arrow → in-process carrier (Polars).** `decimal128(38,0)` at full width loses digits crossing
   into Polars while Arrow held it exactly, and `MAP` becomes a list of structs. **This is the hop
   inside Columna**, and it is the reason the envelope is four hops and not three.

---

## 7. Conclusion, deliberately narrow

> **ADBC and Arrow often preserve the material distinctions Columna needs — when the source provides
> them. Successful transport does not establish admissibility.**

Two corollaries that follow from the measurements and nothing else:

- A governed exact-decimal domain **can** be carried faithfully end to end on the incumbent path.
  That is what made the `decimal → Float64` coercion in `compile_v2` unforced rather than an honest
  representation gap.
- The carrier **can** distinguish carrier-null from a value, so the carrier-null vs
  analytical-absence distinction is supportable at this boundary. What is missing for that
  distinction is governed, not material.

## 8. What this study does not establish

PostgreSQL or any other driver family (not available here). Nested-type fidelity beyond the three
cases shown. Any ordering guarantee. Error bounds or approximation behaviour. Anything about
eligibility, participation or support — those are analytical standing, and no transport measurement
speaks to them.

**Regression intent.** The two decimal carriers measured here — one faithful, one lossy — are the
intended basis for Proof A's negative control, committed as Arrow IPC fixtures so the admission
boundary is tested against measured material rather than a contrived example.
