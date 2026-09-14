# Source-adapter contract — v1 — **CANDIDATE**

**Status:** **APPROVED** (Huayin, 2026-09-14) with one adjustment and a set of explicit caveats,
amended the same day and returned for final ratification. **Nothing below is implemented**, and
implementation is gated: the pre-ingress conformance repair (continuation-operator checks in K0v2 and
Platform; coordinate type/nullity admission) must be green and merged **before** `columna-adbc` is
written.

**All names in this document are provisional**, per the approval of the conceptual interface.

---

## 1. Three jurisdictions, kept apart

The single most important thing this contract does is refuse to let three different kinds of fact
share one artifact.

| # | jurisdiction | what lives there | who authors it | where it lives |
|---|---|---|---|---|
| 1 | **governed realization facts** | `connection`, `schema`, `table`, `column` | the steward, as a claim about the source | the private realization mapping (v2 shape, frozen) |
| 2 | **adapter interface** | how Platform asks for material and what it gets back | this contract | `columna-platform`, as a `Protocol` |
| 3 | **deployment configuration** | driver, DSN, credentials, pool sizes, TLS, timeouts | the deployment | the deployment's own construction code, injected |

> **DSNs AND CREDENTIALS NEVER ENTER THE GOVERNED REALIZATION ARTIFACT.** The token `"warehouse"`
> means nothing to any package here. It means whatever the deployment bound it to, and a deployment
> that bound nothing has no material for it — which is a refusal, not a default. This is already the
> shipped invariant (`source.py`, ruled 2026-09-14) and the adapter contract inherits it unchanged:
>
> > *changing `connection` alone must change which material source is selected, or cause a refusal.*

---

## 2. The interface

```python
#: Jurisdiction 2. Names provisional. Lives in columna-platform; implemented elsewhere.

@dataclass(frozen=True)
class Material:
    """What one projected fetch returns."""

    #: the projected columns, in Arrow, with the PHYSICAL column names the request asked for
    table: pa.Table

    #: OPAQUE COMPARABLE DATA-STATE IDENTITY, or None. ADDED IN V1 BY RULING (2026-09-14).
    #: WHY IT RIDES ON THE RETURN VALUE AND IS NOT A SECOND CALL: the token belongs to the SAME
    #: material observation as the carrier beside it. A separate `data_state()` call could observe a
    #: DIFFERENT state, and the pair would then describe two moments while looking like one.
    #: None is not "fresh" and not "unknown-but-fine" -- it CLOSES REUSE (see section 6).
    #: Platform never interprets, parses, orders or derives meaning from this value. It compares it
    #: for equality with another token from the same adapter, and does nothing else with it.
    data_state: str | None = None


class MaterialSource(Protocol):
    """One deployment-bound source of Arrow material. ONE METHOD, ON PURPOSE."""

    def fetch(self, *, schema: str | None, table: str,
              columns: Sequence[str]) -> Material:
        """Return exactly `columns` from `(schema, table)`, as Arrow.

        `schema=None` is a POSITIVE claim that no schema qualification applies -- never a dropped
        one. `None` and `"sales"` are different objects and neither answers for the other.

        `columns` is the complete projection: the anchor's component columns and the family's value
        column, in one request. An implementation MUST NOT return columns that were not asked for.

        A MISSING REQUESTED COLUMN OR OBJECT IS A REFUSAL (ruled 2026-09-14). An adapter must NOT
        silently return a shorter projection: a caller that asked for three columns and received two
        would be holding a carrier whose coordinates are quietly incomplete, and CAP's coordinate
        name check would then refuse it for the wrong reason, naming the anchor rather than the
        source.

        `table` IS A FULLY MATERIALIZED `pa.Table`, never a `RecordBatchReader` (ruled 2026-09-14).
        The adapter MAY consume a reader internally -- duckdb's native `.arrow()` returns one, and
        that API hazard is measured (study [E1]: it produced fifteen ERROR rows) -- but it must
        DISCHARGE that hazard before handing material to Platform. A consumed-once object must not
        reach the admission path.
        """


class SourceBindings(Protocol):
    """`connection` token -> source. THE ONLY THING THAT KNOWS WHAT "warehouse" MEANS."""

    def source_for(self, connection: str) -> MaterialSource: ...
```

### What is deliberately absent, and why

- **There is no method that returns a whole object.** The shipped `InMemoryArrowSource` has
  `object_for(schema, table) -> pa.Table`, and `read_anchored` then calls `column()` once per
  coordinate and once for the value — **N+1 reads of one object**. Free against an in-process table;
  **N+1 round trips** against a driver. Replacing both with a single `fetch` makes
  *"do not establish `SELECT *` / full-object reads as the external execution model"* a property of
  **the shape of the interface** rather than of anyone's discipline. An adapter *cannot* express a
  full-object read through this Protocol.
- **There is no predicate parameter.** No predicate pushdown in v1. Not deferred for effort: a
  predicate is an analytical restriction, and which restrictions are governed — eligibility,
  participation, support — is exactly the jurisdiction no transport rule may speak to.
- **There is no ordering parameter, and no ordering guarantee.** CAP v1 §6.
- **There is no `execute(sql)`.** The adapter is asked for a projection of a named object, not for the
  result of a statement. A SQL seam here would put query construction in the deployment's hands and
  make the governed endpoint advisory.
- **There is no schema-discovery method.** CAP v1 inspects the schema **actually delivered** on the
  `pa.Table` it received. A separate describe call would introduce a second schema that could differ
  from the one the data came with.

---

## 3. Projection — in from v1

**Yes, projection belongs in the contract from v1** (ruled). One projected request per governed-family
execution, carrying the anchor component columns **and** the value column together.

The one-request form is not an optimisation. It is what makes `read_anchored`'s *"the material columns
are not of one length"* refusal meaningful: N separate fetches of one object may see N different
states of it, and the equal-length check would then be comparing columns that were never one
delivery. **One projection is one observation.**

---

## 4. Where it plugs in

Unchanged seam. `MaterialBinding(mapping_path, sources)` already carries `SourceBindings` and is
already injected at provider construction; the deployment constructs the adapter and hands it in.
`read_anchored` changes from N+1 `column()` calls to one `fetch()`, keeps the physical→governed
rename (which is the anchor-component realization's whole job), and keeps the
same-`(connection, schema, table)` check **before** the fetch.

**A provider with no binding PLANS and does not EXECUTE**, and says so as a capability limit rather
than as a governed refusal. Unchanged.

---

## 5. Currency

**Ruled 2026-09-14: add the optional `data_state` slot now.** Semantics deliberately minimal:

- **no token → `Standing.currency = None`, and reuse is closed.** Already the shipped behaviour and
  already tested.
- **an opaque token may travel verbatim** as a comparable data-state identity, later.
- **equality does not mean "fresh."** Two states carrying equal tokens are *comparable*; whether
  either is current is a different question.
- **freshness / currency interpretation remains an unresolved jurisdiction.** Admission checks the
  carrier, not the claim.
- **no persistent reuse yet.**

`Standing.currency` already exists with exactly these semantics (*"opaque comparable currency token.
`None` closes reuse; it never means 'fresh'"*). **The adapter's `data_state` is the thing that would
eventually fill it, and v1 does not fill it** — v1 defines the return slot so that an adapter has
somewhere lawful to put a token, and Platform continues to record `None`.

### 5.1 What may fill it, for DuckDB/ADBC — **RULED 2026-09-14 (Huayin)**

> **A projection-scoped, scan-derived content CHANGE DETECTOR is an admissible data-state token for
> retained state derived from exactly that projection.**

Admissible only when **all** of these hold:

1. computed from **the same material observation** that constituted the retained state;
2. scoped to **the exact projected material** that state depends on;
3. **stable** while that projected material is unchanged;
4. **changes** when that projected material changes, to the strength the detector warrants;
5. its representation is **namespaced** by detector/algorithm version **and** DuckDB engine version;
6. failure to establish it yields **`None`**;
7. **`None` closes reuse**;
8. equality means only that two tokens are **comparable and equal under that detector** — never
   "fresh", never "current", never "the source is globally unchanged".

**Call it what it is: a *projection-scoped change detector*.** It must not be called table identity,
snapshot identity, MVCC identity, a freshness token, or a collision-free content identity. Naming it
any of those would assert a guarantee it does not carry, and the whole reason this class is
admissible is that its guarantee is narrow and stated.

**The token belongs to the material observation that produced the retained state** — not to the
table, and not to the source. A second observation of the same table is a different observation.

### 5.2 DuckDB sources that are NOT admissible — and the measurement that disqualifies them

**Not admissible:** `table_oid`; `estimated_size`; row count alone; ADBC `get_statistics`;
transaction ids; transaction timestamps; `pragma database_size`; file mtime/size; any value from
`duckdb_tables()` or `pragma_storage_info()`.

**The disqualifying property is one measured fact, and it disqualifies the whole catalog class at
once: DuckDB's catalog and storage surfaces can describe a LATER MOMENT than the scan returned
beside them, inside one statement and one transaction.** Measured on duckdb 1.5.5, two cursors on
one database — connection A inside a transaction reads 2 rows; connection B inserts a third and
commits; A then runs a SINGLE statement selecting both the scan and the catalog:

```
rows_seen = 2        catalog estimated_size = 3        storage_info count = 6
```

Data is under MVCC; the catalog is not. **So the race the adapter's docstring names — "a second
query would describe a different moment while looking like the same one" — is NOT avoided by
putting the probe in the same query.** That is why condition (1) above cannot be satisfied by any
catalog surface, regardless of its other properties.

Those other properties are independently disqualifying and were also measured: `table_oid` did not
move across `UPDATE`, `INSERT` or `DELETE` (it moved only on `CREATE OR REPLACE`); `estimated_size`
did not move on a same-cardinality `UPDATE` **and did not move on a `DELETE`**; `txid_current()`
advanced across three consecutive read-only statements with nothing mutated, failing the stability
half of the guarantee. `Connector.data_identity`'s standing rule — *"ROW COUNT ALONE IS NEVER A
VALID IMPLEMENTATION"* — independently excludes `estimated_size` and the ADBC statistics row count.

**The construction that satisfies (1) is the one computed from the scan itself**, because it is made
of the delivered rows. Its specification is
[`projection_scoped_change_detector_v0_1.md`](projection_scoped_change_detector_v0_1.md); nothing is
implemented, and `Standing.currency` continues to record `None` until that specification is ruled.


### 5.3 Realization currency for the first Platform profile — **RULED 2026-09-14 (Huayin)**

> **Realization currency is `None` unless an INDEPENDENT WARRANTED MECHANISM can establish that the
> specific realization assertion revision remains true of the source.**
>
> **For DuckDB-ADBC v1, no such mechanism exists. Realization currency therefore remains `None`, and
> `None` closes cross-request reuse.**

**The reason is structural, not a gap in the implementation.** Classifying every realization claim
fact by what could establish its truth (reconnaissance, 2026-09-14):

| fact | establishable from |
|---|---|
| connection binding still exists | **deployment binding alone** — a local lookup, no source contact |
| schema/table object still resolves | **only by performing the material read** — the contract has no schema-discovery call, by ruling |
| projected columns still resolve | **only by performing the material read** — the short-projection check runs after `fetch` |
| delivered types still satisfy CAP / the claim | **the delivered Arrow schema — which arrives WITH the material** |
| grain / coincident claim still holds | **only by performing the material read** — CHECK 5 tests the delivered rows |
| exactness claim remains supportable | **not a currency question** — checked before any material is read, claim against law |
| formation / continuation operator agreement | **not a currency question** — *"the realization CLAIMS an operator; the law DECIDES"* |

So every fact that is genuinely *about the source* requires the read, and the two cheap facts are
cheap precisely because they are **claim-vs-law conformance**, already checked on every execution
from law and claim alone. **Establishing realization currency would require performing the read that
reuse exists to avoid.**

**Explicitly insufficient, so the requirement is not weakened by degrees:**

- **connection-binding existence alone** is not realization currency — it says a deployment still
  binds a name, not that the assertion is true of what that name reaches;
- **claim-vs-law checks** (exactness, operator agreement) are not realization currency — they are
  conformance of a claim to governed law and touch no source;
- **equality of assertion revision** is not realization currency — it establishes that THE CLAIM did
  not change, which is a different proposition from the claim still being true;
- **equality of the projection-scoped data-state detector** is not realization currency — see §5.4.

**The requirement must not be weakened merely to enable reuse.** A profile that relaxed it would be
reporting a warrant nobody issued, which is the failure every other mechanism in this contract
fails closed to avoid.

### 5.4 What the projection-scoped detector is FOR — **RULED 2026-09-14 (Huayin)**

A consequence of §5.1 that is easy to misread, so it is recorded:

> **The detector is produced from the SAME SCAN that produces the material. It identifies the
> material state FROM WHICH a retained state was established. It does NOT provide an independently
> obtainable current-state check for a LATER request.**

**It may support:** observation provenance; comparison between two states when **both** observations
have already occurred; and future sources whose current token can be warranted independently.

**It may not be interpreted as:** freshness; proof that the source is still unchanged at request
N+1; or authorization to reuse without observing the source again.

The asymmetry is worth naming because it decides what the detector is worth: **it rides free on a
read you are already performing, and there is no carrier for it on a read you are trying not to
perform.** That is exactly why it cannot answer the request-N+1 question, and why implementing it to
claim cross-request reuse would be implementing it to assert something it does not establish.

---

## 6. OF-42 / joins — one execution, one object

For ADBC profile v1:

> **One governed-family execution must be satisfiable from one material object after realization
> binding.** The value column and **every** anchor component must resolve to the same
> `connection` / `schema` / `table`. Otherwise: **capability `unsupported`.**

No join. No inner/outer join policy. No accidental entry into P1-31.

This is already the shipped behaviour and already carries the right jurisdiction —
`UnsupportedByThisProfile`, explicitly *not* a governed verdict, because refusing it as a want-of-state
would tell an operator to go and re-materialize against a capability that does not exist. The contract
restates it because it is now a property of **the adapter interface** too: `fetch` takes one
`(schema, table)` and cannot express a two-object read.

---

## 7. Package boundary — `packages/columna-adbc` (provisional)

**The name is provisional and is not a public-product naming decision.**

```
columna-adbc  ──depends on──▶  columna-platform  ──depends on──▶  columna-core
      │
      └─ depends on: adbc-driver-manager, and one concrete driver package
```

Rules:

1. **`columna-platform` must never import ADBC or any concrete driver.** The existing import-ban tests
   in `columna-platform` (`test_proof_a_findings.py` — the static name scan and the clean-interpreter
   subprocess check, whose forbidden set includes `duckdb` and `adbc_driver_manager`) **stay exactly as
   they are.** They are the standing proof of the direction of the arrow.
2. **The deployment constructs the adapter and injects it** through the existing material-binding seam.
   Nothing in `columna-platform` names a driver, a DSN, or a package.
3. **No driver code in `columna-server`.** The server is a wire surface.
4. `columna-adbc` implements `MaterialSource` / `SourceBindings` and imports from `columna-platform`;
   `columna-platform` imports nothing from it, statically or at runtime.

### Two consequences worth naming before the package exists

- **The import ban's meaning changes scope and should be restated.** Once `columna-adbc` depends on a
  driver, `duckdb` is a dependency **of this repository**. The ban was, and must remain, *"**Platform**
  must not import duckdb"* — not *"this repository must not depend on duckdb."* The clean-interpreter
  test proves the former and is unaffected by the latter; but the sentence in `source.py` that says
  *"DuckDB and ADBC are not merely unused here"* will need a clause so a future reader does not read a
  repository-wide claim into a package-scoped one.
- **`columna-adbc` needs its own ban, in the other direction.** It must not reach into
  `columna_core.planner` / `.engine` / `.model` / `.compiler.compile_v2` — the same forbidden set
  Platform carries — or the adapter becomes a second execution path. Recommend the same two-test
  pattern, copied deliberately rather than shared, for the reason CAP §2 gives about shared tables.

---

## 8. First driver — **DuckDB-ADBC, ACCEPTED for the first bounded ingress slice, with caveats**

### 8.1 Why not SQLite-ADBC, though it is better measured

For the **exact-decimal positive path**, SQLite offers only:

- **`TEXT`** — exact characters, but **the wrong governed carrier type**. Admitting it would require
  CAP to parse a decimal out of a string, which is the profile deciding a governed meaning (CAP §3).
- **`REAL`** — **already lossy at rest**, before any driver runs (`…5678 → …568`).

Neither can establish the positive exact-decimal proposition. **SQLite-ADBC is valuable later as a
negative / source-loss case**, which is the role it should be kept for.

### 8.2 The driver package, established

**This is the deliverable-7 finding, and it is not what one would expect.**

| question | answer |
|---|---|
| Is there an `adbc-driver-duckdb` distribution? | **No.** `pip install adbc-driver-duckdb` → *"No matching distribution found"*; `importlib.metadata.version("adbc-driver-duckdb")` → `PackageNotFoundError`. |
| Then what provides `adbc_driver_duckdb`? | **The `duckdb` wheel vendors it.** `duckdb-1.5.5.dist-info/RECORD` lists four entries under `adbc_driver_duckdb/`. The package has **no dist-info of its own**. |
| How does it find the driver? | `adbc_driver_duckdb.driver_path()` → `importlib.util.find_spec("_duckdb").origin`, connected with entrypoint `duckdb_adbc_init`. |
| Is it the same binary the study's `DUCK_LIB` pointed at? | **Yes, verbatim** — `driver_path()` returns exactly the absolute path probes 1 and 2 hard-coded. |

> **So `duckdb-adbc` and `duckdb-native` are the same shared object reached through two different
> APIs.** They are **distinct crossings with distinct fidelity records** — which is why the errata
> insists on keeping them apart — and they are **not distinct dependencies**. Both statements need to
> be true at once, and conflating them in either direction would be a mistake.

**The pinnable specification, confirmed working:**

```
duckdb==1.5.5
adbc-driver-manager==1.12.0
pyarrow==25.0.1
```

Confirmed by `cap_v1_evidence/run_cap_v1_ingress.txt`: `adbc_driver_duckdb.dbapi.connect()` →
`cursor.execute(...)` → `fetch_arrow_table()` returns a `pa.Table` carrying `decimal128(18, 4)`,
`string` and `date32[day]`, all three **exact across all four hops** including `pl.from_arrow`. The
same run confirms every shape CAP v1 refuses is **actually emitted by this driver**, so the refusals
are load-bearing rather than decorative.

### 8.3 The caveat, recorded — it is a known risk, not a blocker

**A vendored, undistributed sub-package has no independent version and no deprecation channel of its
own.** `adbc_driver_duckdb` moves with `duckdb` and cannot be pinned, constrained, or audited
separately. That is a weaker supply-chain guarantee than a real distribution, and it should be
recorded as a known risk rather than discovered later.

Mitigations — all three are ruled into §8.4's binding requirements:

1. **Pin `duckdb` exactly** in `columna-adbc`, not with a range — the ADBC entrypoint is not part of
   any published compatibility promise we can cite.
2. **Assert at adapter construction** that `adbc_driver_duckdb.driver_path()` resolves, and refuse as a
   capability limit if it does not — so a dependency bump that drops the vendored package is a named
   refusal at startup, not an obscure failure at first fetch.
3. **Never restate the risk as an absolute path.** `adbc_driver_manager` *can* load the same `.so`
   directly, and that is what probes 1 and 2 do — but **the adapter must not**, and §8.4 makes that
   binding. A hard-coded `.so` path trades a versioning risk for a silent portability failure and
   removes the very signal mitigation 2 exists to raise: a missing vendored package would stop being
   detectable at all. Recorded here as the road **not** taken, so nobody takes it later reasoning that
   it "worked in the probe".

### 8.4 RULED 2026-09-14 — accepted, and the record that must be stated accurately

**Accept the vendored DuckDB ADBC surface for the first bounded ingress slice, with explicit
caveats.** The record, stated as ruled:

- **there is no independent `adbc-driver-duckdb` distribution;**
- **the `duckdb==1.5.5` wheel vendors `adbc_driver_duckdb`;**
- **the ADBC surface resolves to the DuckDB shared library;**
- **therefore its version is governed by the pinned DuckDB package, not by an independently versioned
  driver package;**
- **`adbc-driver-manager==1.12.0` is separately pinned.**

**Why this is acceptable for a first ingress:** *the crossing under test is **ADBC API → Arrow**, even
though the underlying engine library is the same DuckDB binary used by the native API.* So
`duckdb-native` and `duckdb-adbc` stay distinct **as crossings, not as binaries** — which is exactly
the pair of statements §8.2 insists must both be true.

**Binding requirements on the adapter:**

| | requirement |
|---|---|
| **fail closed** | if the expected vendored ADBC surface or driver path is unavailable, the adapter **refuses at construction** as a capability limit. A dependency bump that drops the vendored package becomes a named refusal at startup, not an obscure failure at first fetch. |
| **no absolute path** | **do not hard-code an absolute `.so` path.** Resolution goes through `adbc_driver_duckdb.driver_path()` / `importlib.util.find_spec`, never through a `DUCK_LIB`-style constant. This is the one thing probes 1 and 2 did that must not be carried into the adapter. |
| **no false version claim** | **do not claim an independent DuckDB-ADBC driver version.** Anything that reports a driver version must report it as *"the ADBC surface vendored by `duckdb==<pin>`"*. |
| **exact pin** | `duckdb` pinned exactly, not as a range — the ADBC entrypoint is not part of any published compatibility promise we can cite. |

**SQLite-ADBC remains useful later as a source-loss negative control**, and is not a candidate for the
positive path (§8.1).

---

## 9. Ruled, 2026-09-14

| | ruling |
|---|---|
| **Return shape** | `fetch(...)` returns a small **material envelope**, not a naked table: `Material{table: pa.Table, data_state: str \| None}`. The token belongs to the **same material observation** as the carrier — a separate `data_state()` call could observe a different state. Exact class/name provisional. (§2) |
| **No whole-object read** | Confirmed — there is no such method. (§2) |
| **Missing column / object** | **Refuse.** Do not silently return a shorter projection. (§2) |
| **Materialization** | `pa.Table`, **not** a `RecordBatchReader`. The adapter may consume a reader internally but must **discharge that API hazard** before handing material to Platform. (§2) |
| **Currency** | Add the `data_state` slot now. `None` → `Standing.currency = None`, reuse closed; an opaque token travels verbatim for future equality comparison; **token equality does not mean current/fresh**; freshness remains an unresolved jurisdiction. **Do not persist or reuse state yet.** (§5) |
| **OF-42 boundary** | One governed-family execution must be satisfiable from **one material object** after realization binding; coordinates and value resolve to the same `connection`/`schema`/`table`; otherwise capability `unsupported`. **No joins.** (§6) |
| **Package placement** | Separate package, working name `packages/columna-adbc`, **provisional and not a product naming decision**. `columna-adbc → columna-platform`, never the reverse. Platform's existing DuckDB/ADBC import-ban tests stay **unchanged**. The deployment constructs the adapter and injects it through the material-binding seam. **No driver code in `columna-server`.** (§7) |
| **First driver** | Vendored DuckDB ADBC surface **accepted** for the first bounded ingress slice, with the record stated accurately and four binding requirements on the adapter. (§8.4) |

### Implementation gate

**No `columna-adbc` code until the pre-ingress conformance repair is green and merged:**
continuation-operator checks in K0v2 **and** Platform, and coordinate type/nullity admission.
