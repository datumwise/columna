# Admission fidelity — first empirical study — v0.1

> ## ⚠ CORRECTED 2026-09-14 — READ §0 FIRST
> This document as first written made claims its own raw runs do not support. **Twelve corrections**
> are recorded in **[§0 Errata](#0-errata--corrections-to-the-claims-2026-09-14)**, and every
> corrected claim below is marked `[E1]`…`[E12]` at the point it appears. The measurements are
> unchanged and the raw runs are untouched; what changed is what this document says about them.
>
> **This study is not an envelope and must not be ratified as one** (Huayin, 2026-09-14). Normative
> admission authority lives in the **Carrier Admission Profile**, whose rules stand on their own
> authority and cite measurement only as supporting evidence.

**Status:** measurement record, 2026-09-12; **claims corrected 2026-09-14** (§0). **Not a contract,
not a ratified envelope, and not the authority for any admission rule.** It records what was
observed, on one machine, at the versions below, so that the admission boundary is *informed by*
measurement rather than by assumption.
**Commissioned as:** the early read-only ADBC/Arrow fidelity reconnaissance of Phase 0 — measurement,
not ingress construction.

---

## 0. Errata — corrections to the CLAIMS, 2026-09-14

**What this revision is.** The measurements below are unchanged and the raw runs are untouched. What
is corrected is what this document *said about* them. The audit that produced these corrections was
commissioned before ratifying an admission envelope, and its result was that **this study must not be
ratified as an envelope** (Huayin, 2026-09-14): *"We will not ratify the existing admission-fidelity
study as an envelope. We will correct it as a measurement record, then ratify a deliberately narrow
Carrier Admission Profile whose rules stand on their own authority."*

**So this document's status is narrower after the correction than before, not wider.** It is a record
of what was observed. It is **not** a contract, **not** a ratified envelope, and **not** the
authority for any admission rule. Normative authority lives in the Carrier Admission Profile.

Every correction below is keyed `[E1]`…`[E12]` and is marked at the point in §1–§8 where the
uncorrected claim appears.

### The corrections

**[E1] The `duckdb-native` crossing produced no usable matrix rows, and the failure was the probe's.**
§2 says three crossings were tested. All **fifteen** `duckdb-native` rows in `run_1_matrix.txt` are
`ERROR` with `<AttributeError>`, for one cause: in duckdb 1.5.5 `con.execute(sql).arrow()` returns a
`pyarrow.lib.RecordBatchReader`, and `probe_1_matrix.py`'s `note()` reads `tbl.schema` /
`tbl.column(0)`. **Nothing was measured about the driver in those fifteen rows** — a probe defect was
recorded fifteen times. The study never printed those rows, which is how a crossing with no matrix
evidence came to read as one of three tested.

**[E2] `duckdb-native` therefore has exactly three measured points, and they are these.**
(i) `DECIMAL(18,4)` preserved, both through the `RecordBatchReader` and through `.read_all()`
(`run_2_followups.txt` §A). (ii) NULL and NaN remain distinguishable in a `double` column,
`null_count = 1` on both sides (`run_2_followups.txt` §F — that section uses the native connection).
(iii) Row order stable across five runs with no `ORDER BY`, which §5 already refuses to treat as a
guarantee (`run_1_matrix.txt`, final row). **There is no `duckdb-native` measurement** for
`DECIMAL(38,9)`, for `HUGEINT`/`decimal128(38,0)`, for any temporal type, for `TIME`, for `DATE`, for
empty-string-vs-null, or for `LIST`/`STRUCT`/`MAP`. The incumbent doorway is the crossing this record
knows **least** about, not most.

**[E3] Precision greater than 38 was never measured.** `run_2_followups.txt` §D is headed
*"decimal wider than 38 digits"* and its two cases are `DECIMAL(38,10)` and `DECIMAL(38,37)` — both
precision **38**. The heading names the intended question; the probe asked a different one (wider
*scale* at the same precision). **No `p > 38` case exists anywhere in the record**, so no claim about
what happens above 38 digits is supported by this study, in either direction.

**[E4] `(38,10)` and `(38,37)` are Arrow-only results and did not cross into Polars.**
`probe_2_followups.py` §D prints `t.schema.field(0).type` and `t.column(0)[0].as_py()` and never calls
`pl.from_arrow`. The claim *"`DECIMAL(38,37)` crosses intact"* is true of **hop three** and says
nothing about hop four — which is the hop this study's own §1 exists to insist on, and the hop inside
Columna.

**[E5] `LIST`'s machine verdict and this document's prose disagree, and both are now shown.** The raw
verdict is `POLARS-LOSS`: the expected string `[1, 2, 3]` did not match what Polars returned (a
`Series`). §3's prose reads *"preserved, representation differs"*, which is an **interpretation** of
that failure — defensible, and it was not labelled as one. Neither is withdrawn here; the
disagreement is made visible so a reader is not left with a resolved-sounding row over an unresolved
measurement.

**[E6] Five `ok` verdicts are VACUOUS — they mean "no expectation was stated", not "the value was
preserved".** In `probe_1_matrix.py`, `expect_str is None` sets `a_ok = p_ok = True` unconditionally,
so `verdict` is `ok` **whatever arrived**. Five cases carry `expect_str=None`: `timestamp ns`,
`timestamptz`, `struct`, `map` (duckdb), and `mixed-type column` (sqlite). For these five, **no value
comparison was performed at all.** In particular §3's `MAP` row reads *"value preserved, map-ness
lost"*: the second half is readable from the dtype; **the first half was never compared** and is
withdrawn as unsupported. The same withdrawal applies to `STRUCT`'s bare *"preserved"*.

**[E7] Sub-microsecond timestamp VALUE preservation is not established by the raw output.** The
`timestamp ns` input is `'2026-09-12 11:59:00.123456789'`. Run 1 shows Arrow's `as_py()` **raising
`ValueError`**, and the Polars value rendered as `2026-09-12 11:59:00.123456` — the trailing `789`
absent, and absent by construction rather than by column width: `df[name][0]` yields a Python
`datetime`, whose resolution is microseconds. What IS established: the Arrow type is `timestamp[ns]`
and the Polars dtype is `Datetime('ns')` — i.e. the **type** survived. What is NOT established: that
the nanosecond **value** did. §3's *"preserved in carrier"* overstates the evidence and is corrected
to *"ns type survives on both sides; the ns value was not observed on either"*.

**[E8] The Arrow IPC fixture claim is unsupported by the tree and is WITHDRAWN.** §8's *"Regression
intent"* states the two decimal carriers were *"committed as Arrow IPC fixtures so the admission
boundary is tested against measured material rather than a contrived example."* There are **no**
`.arrow`, `.ipc` or `.feather` files anywhere in this repository and no use of `pyarrow.ipc` in any
package. What was actually built is `columna-platform/src/columna_platform/carrier.py` — arrays
constructed in-process with `pa.array(...)`, whose own docstring says so (*"NO DATABASE, NO DRIVER,
NO FILE"*) and which records a deliberate one-digit deviation from the measured `HUGEINT` value
because pyarrow refuses to build it. That is a **weaker provenance** than the sentence claimed:
the shapes cite measured rows, they are not the measured bytes. Corrected accordingly; the intent is
recorded as **not carried out in the form stated**.

**[E9] Version stamps in §2 are recorded, not independently reproduced.** Neither probe prints a
version except `duckdb.__version__` (run 2 §A: `duckdb 1.5.5`). python 3.12.14, the platform/glibc
string, pyarrow 25.0.1, polars 1.44.2, adbc-driver-manager 1.12.0, adbc-driver-sqlite 1.12.0 and
SQLite 3.53.1 are **recorded-but-not-independently-reproduced from the committed raw output**. §2 is
labelled accordingly. `probe_3_errata_checks.py` prints the four that matter for the corrected
decimal claims, so those four are reproduced from run 3 onward.

**[E10] `duckdb-adbc` and `duckdb-native` are two crossings and are now kept apart everywhere.**
§1's fourth-hop sentence, §6's collapse point 3 and §7's first corollary each read as though one
DuckDB path were under study. The §3 matrix is **`duckdb-adbc` throughout**. §7's corollary — *"a
governed exact-decimal domain can be carried faithfully end to end on the incumbent path"* — is
supported, but by **one shape** (`DECIMAL(18,4)`, run 2 §A), not by the fifteen-row matrix.

**[E11] The fourth-hop decimal collapse is keyed on the VALUE's digit count, not on the `(38,0)`
type. Re-measured; see `run_3_errata_checks.txt`.** §6's collapse point 3 reads *"`decimal128(38,0)`
at full width loses digits crossing into Polars while Arrow held it exactly."* The row behind it is
`HUGEINT` carrying the int128 maximum — **thirty-nine digits**, a value out of range for the
`decimal128(38, 0)` it is declared as. Run 3 separates the two discriminators: a `HUGEINT` of 38
nines, and a `DECIMAL(38,0)` of 38 nines, both arrive as `decimal128(38, 0)` and both **round-trip
exactly** through `pl.from_arrow`; three distinct **39-digit** values (int128 max, int128 max − 1,
10³⁸) all arrive typed `decimal128(38, 0)` and **all** lose digits at hop four. From the other side,
pyarrow refuses to construct a 39-digit `decimal128(38,0)` in-process at all
(`ArrowInvalid: Decimal type with precision 39 does not fit into precision inferred… 38`). The
corrected claim: **what collapses at hop four is a driver-emitted value out of precision range for
the Arrow type it is declared as** — here, DuckDB's `HUGEINT` → `decimal128(38,0)` mapping — and not
the `(38,0)` shape.
> **CONSEQUENCE FLAGGED, NOT ACTED ON HERE.** `columna-platform`'s admission CHECK 1 refuses
> `decimal128(38,0)` **as a type**, citing this row, and its comment states the reason as *"exact in
> Arrow but not faithfully carried across the in-process conversion"*. Under the corrected reading
> that refusal is keyed on the wrong property: a conforming 38-digit `(38,0)` value is refused though
> it crosses intact, and the real hazard — an out-of-range value — is not what is being tested. This
> is a **live finding about shipped code** and is deliberately left for a ruling rather than repaired
> inside an errata revision. It is moot for CAP v1's narrow envelope, which admits `decimal128(18,4)`
> only, but the stated reason in the code would still be wrong.

**[E12] §4's SQLite `untyped column` row draws its values from run 2, not from the run-1 row it sits
beside.** Run 1's `sqlite-adbc | mixed-type column` case is a different query
(`SELECT 1 UNION ALL SELECT 'two' ORDER BY 1`) returning `string` / `1`. The `1,2,3,'surprise'` values
and the order-independence finding come from `run_2_followups.txt` §E. The finding stands; its
sourcing is corrected so the two runs are not conflated under one crossing label.

### What survives the correction

Stated positively, so the corrections are not read as a retraction of the study:

- The **four-hop framing** (§1) survives intact and is strengthened by [E11] — hop four is still where
  a value exact in Arrow is lost, the cause is just more precisely named.
- **`decimal128(18,4)` carried exactly**, end to end, on `duckdb-adbc` **and** on `duckdb-native`
  (run 1; run 2 §A). This is the single best-evidenced point in the record and is the one CAP v1
  builds its first positive ingress on.
- **SQLite `REAL` loses at rest** (`…5678 → …568`), before any driver runs — the negative control's
  whole warrant, untouched.
- **Carrier-null and NaN remain distinguishable** through both hops (run 1; run 2 §F).
- **Guarantee vs observation** (§5) is unaffected — if anything [E6] and [E9] are further instances of
  the same discipline applied to this document itself.
- **Row order is an observation and never a guarantee** (§5). CAP v1 restates this as an explicit
  non-guarantee rather than inheriting it.


---

## 1. The envelope actually under study

The admission envelope is **not** driver → Arrow. It is:

> **source semantics → driver / configuration → Arrow → any in-process carrier conversion (e.g. Polars)**

That fourth hop is not decoration. Two of the three collapses found below happen at it or at the
configuration boundary, not at the driver, and the fourth hop is the one **inside** Columna today:
`connector.py` does `pl.from_arrow(con.execute(q).arrow())` on every fetch. **`[E10]`** — and that
incumbent doorway is `duckdb-native`, which is a *different crossing* from the `duckdb-adbc` one the
§3 matrix measures; the two are kept apart throughout after the correction. **`[E11]`** — the precise
cause of the hop-four decimal collapse is corrected in §0.

## 2. Environment

**`[E9]` RECORDED, NOT INDEPENDENTLY REPRODUCED.** Neither committed probe prints a version except
`duckdb.__version__`. Every other stamp below is recorded from the environment as it was believed to
be, and is **not** recoverable from `run_1_matrix.txt` or `run_2_followups.txt`. The four that matter
for the corrected decimal claims are printed by `probe_3_errata_checks.py` and are reproduced in
`run_3_errata_checks.txt`.

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

**Crossings ATTEMPTED.** Three. The first is the incumbent Columna doorway, included deliberately so
the comparison is against what ships, not against an idealization. **`[E1]` It produced no usable
matrix rows** — all fifteen `duckdb-native` cases in run 1 are `ERROR`, from a defect in the probe
rather than in the driver — so of the three crossings attempted, **two** yielded a matrix.
**`[E2]`** lists the three points `duckdb-native` *is* evidenced by.

1. `duckdb-native` — `duckdb.execute(sql).arrow()` → pyarrow → `pl.from_arrow`
2. `duckdb-adbc` — ADBC driver manager loading duckdb's `duckdb_adbc_init` entrypoint → `fetch_arrow_table` → `pl.from_arrow`
3. `sqlite-adbc` — `adbc_driver_sqlite` → `fetch_arrow_table` → `pl.from_arrow`

Raw run records and the probe scripts themselves: `admission_fidelity_v0_1/` beside this document
(`run_1_matrix.txt`, `run_2_followups.txt`, and the two scripts that produced them). Reproduced in
§3–§4. The probes are deliberately **not** wired into CI — they need two ADBC drivers that are not
dependencies of any package here, and a measurement exercise must not add one.

---

## 3. Matrix — DuckDB via ADBC

**`[E10]` This matrix is `duckdb-adbc` throughout.** No row here is evidence about `duckdb-native`.

| case | arrow type | arrow value | polars dtype | result | guarantee or observation? |
|---|---|---|---|---|---|
| `DECIMAL(38,9)` exact | `decimal128(38, 9)` | `123456789012345678.123456789` | `Decimal(38, 9)` | **preserved** | observation |
| `DECIMAL(18,4)` money | `decimal128(18, 4)` | `12345678901234.5678` | `Decimal(18, 4)` | **preserved** | observation |
| `DECIMAL(3,1)` 0.1+0.2 | `decimal128(4, 1)` | `0.3` | `Decimal(4, 1)` | **preserved** | observation |
| `HUGEINT` / int128 | `decimal128(38, 0)` | `170141183460469231731687303715884105727` | `Decimal(38, 0)` | **POLARS LOSS** | observation |
| `TIMESTAMP` µs | `timestamp[us]` | `2026-09-12 11:59:00.123456` | `Datetime('us')` | preserved | observation |
| `TIMESTAMP_NS` | `timestamp[ns]` | *`as_py()` raises `ValueError`* | `Datetime('ns')` | **`[E7]` ns TYPE survives on both sides; the ns VALUE was not observed on either.** `as_py()` raised; the Polars rendering is a Python `datetime`, µs-resolution by construction. (*was: "preserved in carrier"*) **`[E6]` verdict vacuous** | observation |
| `TIMESTAMPTZ` `-04:00` | `timestamp[us, tz=Etc/UTC]` | `2026-09-12 15:59:00+00:00` | `Datetime('us', tz)` | instant preserved, **source offset normalized** — **`[E6]` verdict vacuous** (no expected value was stated), though the normalization is readable from the printed type | observation |
| `TIME` | `time64[us]` | `11:59:00.123456` | `Time` | preserved | observation |
| `DATE` | `date32[day]` | `2026-09-12` | `Date` | preserved | observation |
| NULL in decimal column | `decimal128(18, 4)` | `None` | `Decimal(18, 4)` | preserved, **type survives** | observation |
| all-NULL typed column | `timestamp[us, tz=Etc/UTC]` | `None` | `Datetime` | preserved, **type survives** | observation |
| empty string | `string` | `""` | `String` | preserved, distinct from NULL | observation |
| `LIST<INT>` | `list<l: int32>` | `[1, 2, 3]` | `List(Int32)` | **`[E5]` raw verdict `POLARS-LOSS`**; *"preserved, representation differs"* is an interpretation of that failure, now labelled as one. Both stand; neither is withdrawn | observation |
| `STRUCT` | `struct<a: int32, b: string>` | `{'a': 1, 'b': 'x'}` | `Struct` | **`[E6]` "preserved" WITHDRAWN as unsupported** — no expected value was stated, so no comparison ran | observation |
| `MAP` | `map<string, int32>` | `[('k', 1)]` | `List(Struct)` | **`[E6]` "value preserved" WITHDRAWN as unsupported** (never compared); **map-ness lost** stands, being readable from the dtype | observation |

## 4. Matrix — SQLite via ADBC, and the incumbent DuckDB path

**`[E1]`/`[E2]` The two `duckdb-native` rows below are the whole of that crossing's fidelity
evidence**, and they come from run 2 and from run 1's final row — not from the run-1 matrix, which
errored in all fifteen cases.

| crossing | case | arrow type | result |
|---|---|---|---|
| `sqlite-adbc` | decimal stored as `TEXT` | `string` | preserved exactly (`12345678901234.5678`) |
| `sqlite-adbc` | decimal stored as `REAL` | `double` | **SOURCE LOSS** → `12345678901234.568` |
| `sqlite-adbc` | int64 max | `int64` | preserved |
| `sqlite-adbc` | timestamp / tz as `TEXT` | `string` | preserved as text; no temporal type at all |
| `sqlite-adbc` | NULL | `int64` | preserved |
| `sqlite-adbc` | untyped column `1,2,3,'surprise'` | `string` | **TOTAL TYPE COLLAPSE** → `['1','2','3','surprise']`, order-independent — **`[E12]` sourced from run 2 §E**, not from run 1's differently-worded `mixed-type column` row (whose `ok` verdict is vacuous, **`[E6]`**) |
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
- **Decimal ceiling measured — `[E3]`, `[E4]`:** `DECIMAL(38,37)` crosses **hop three** intact;
  `decimal128` carries 38 digits. The probe never called `pl.from_arrow` for this case, so **hop four
  was not measured** for `(38,10)` or `(38,37)`; and despite the run's own heading, **no case above
  precision 38 was ever run** — both cases are precision 38 with a wider scale.
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
3. **Arrow → in-process carrier (Polars).** **`[E11]` CORRECTED.** What loses digits at this hop is a
   **driver-emitted value out of precision range for the Arrow type it is declared as** — DuckDB's
   `HUGEINT` → `decimal128(38,0)` mapping carrying a **39-digit** value — and **not** the `(38,0)`
   shape. Re-measured in `run_3_errata_checks.txt`: 38-digit `(38,0)` values round-trip **exactly**,
   from both `HUGEINT` and `DECIMAL(38,0)`; three distinct 39-digit values all collapse. `MAP` becomes
   a list of structs. **This is the hop inside Columna**, and it remains the reason the envelope is
   four hops and not three — the correction sharpens the cause, it does not remove the hop.

---

## 7. Conclusion, deliberately narrow

> **ADBC and Arrow often preserve the material distinctions Columna needs — when the source provides
> them. Successful transport does not establish admissibility.**

Two corollaries that follow from the measurements and nothing else:

- A governed exact-decimal domain **can** be carried faithfully end to end on the incumbent path.
  That is what made the `decimal → Float64` coercion in `compile_v2` unforced rather than an honest
  representation gap. **`[E10]`/`[E2]` — supported by ONE shape** (`DECIMAL(18,4)`, run 2 §A), not by
  the §3 matrix, which is `duckdb-adbc`. It is nonetheless the best-evidenced point in the record,
  measured on both DuckDB crossings, and is the shape CAP v1's first positive ingress is built on.
- The carrier **can** distinguish carrier-null from a value, so the carrier-null vs
  analytical-absence distinction is supportable at this boundary. What is missing for that
  distinction is governed, not material.

## 8. What this study does not establish

PostgreSQL or any other driver family (not available here). Nested-type fidelity beyond the three
cases shown. Any ordering guarantee. Error bounds or approximation behaviour. Anything about
eligibility, participation or support — those are analytical standing, and no transport measurement
speaks to them.

**`[E3]` Anything above precision 38**, in either direction — the record contains no such case.
**`[E6]` The value fidelity of `MAP`, `STRUCT`, `TIMESTAMPTZ`, `TIMESTAMP_NS` and SQLite's
mixed-type column** — five cases whose `ok` verdicts were produced without any value comparison.

**Regression intent — `[E8]` WITHDRAWN AS STATED.** The two decimal carriers measured here — one
faithful, one lossy — are the intended basis for Proof A's negative control. The sentence originally
said they were *"committed as Arrow IPC fixtures so the admission boundary is tested against measured
material rather than a contrived example."* **That is not what exists.** There are no `.arrow`,
`.ipc` or `.feather` files in this repository and no use of `pyarrow.ipc` anywhere. The controls are
`columna-platform/.../carrier.py` — arrays built in-process with `pa.array(...)` that **cite** the
measured rows, one of them with a recorded one-digit deviation because pyarrow will not construct the
measured width. That is a weaker provenance than the sentence claimed, and it is the provenance that
actually exists.
