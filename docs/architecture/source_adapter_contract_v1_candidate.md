# Source-adapter contract — v1 — **CANDIDATE**

**Status:** candidate, 2026-09-14. **Not ratified, and nothing below is implemented.** Prepared on
instruction (Huayin, 2026-09-14) as deliverables **5** (adapter Protocol), **6** (package boundary)
and **7** (first driver) of eight, ahead of any ADBC coding.

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

    #: OPAQUE COMPARABLE DATA-STATE IDENTITY, or None.
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

Approved and recorded:

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

## 8. First driver — **DuckDB-ADBC, confirmed, with one caveat that needs a decision**

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

### 8.3 The caveat, which is a decision and not a blocker

**A vendored, undistributed sub-package has no independent version and no deprecation channel of its
own.** `adbc_driver_duckdb` moves with `duckdb` and cannot be pinned, constrained, or audited
separately. That is a weaker supply-chain guarantee than a real distribution, and it should be
recorded as a known risk rather than discovered later.

Mitigations, in the order they are worth taking:

1. **Pin `duckdb` exactly** in `columna-adbc`, not with a range — the ADBC entrypoint is not part of
   any published compatibility promise we can cite.
2. **Assert at adapter construction** that `adbc_driver_duckdb.driver_path()` resolves, and refuse as a
   capability limit if it does not — so a dependency bump that drops the vendored package is a named
   refusal at startup, not an obscure failure at first fetch.
3. **Keep the fallback known**: `adbc_driver_manager` can load the same `.so` by absolute path (what
   probes 1 and 2 do). It works and is not pinnable, which is why it is a fallback and not the plan.

> **The instruction was:** *"Before implementation, confirm the reproducible DuckDB-ADBC driver
> package/version available to the adapter package. If that cannot be established cleanly, stop rather
> than substitute a different driver silently."* **The judgement offered: it IS established cleanly —
> a pinnable `duckdb==1.5.5` + `adbc-driver-manager==1.12.0`, confirmed running end to end — but the
> "package" is a vendored sub-package rather than a distribution, which is not what "confirm the
> driver package" would normally return.** That difference is surfaced rather than smoothed over,
> because it is the kind of fact that is cheap to accept now and expensive to discover in a year.
> **Not proceeding on it without a ruling.**

---

## 9. Open, for ratification

1. **8.3** — accept DuckDB-ADBC on a vendored, unversioned sub-package with the three mitigations, or
   treat "no independent distribution" as failing *"established cleanly"*?
2. **`Material.data_state`** — define the return slot in v1 while Platform continues to record `None`
   (recommended), or leave `fetch` returning a bare `pa.Table` until currency is ruled?
3. **Does `fetch` refuse, or return short, when a requested column is absent?** Recommendation:
   refuse, as `WantOfState`, naming the object and the columns it does have — matching shipped
   `InMemoryArrowSource` behaviour exactly.
4. **Batching / streaming.** `fetch` returns a materialized `pa.Table`. A `RecordBatchReader` return
   would stream, and `duckdb`'s native `.arrow()` already returns one (study `[E1]`). Recommendation:
   **`pa.Table` in v1** — CAP's coincident-multiplicity check (C5) needs the whole carrier anyway, so
   streaming would buy nothing and would add a consumed-once object to the admission path.
5. **Package naming** — `columna-adbc` is provisional. Confirm as a working name, or park the naming
   question explicitly so it is not settled by inertia.
