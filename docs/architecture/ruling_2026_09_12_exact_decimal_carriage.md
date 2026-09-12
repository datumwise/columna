# Ruling 2026-09-12 — exact-decimal carriage

**Status:** **ruled and in force.** Documentation of a decision already authorized and already
landed; this file is the record, not a new authority.
**Ruled:** 2026-09-12 (Huayin), confirmed at the merge of PR #274.
**Governs:** the lowering of a governed `decimal` value domain onto a physical carrier — the
`_DOMAIN_TO_DTYPE` mapping in `columna_core.compiler.compile_v2` and every successor profile that
lowers a governed value domain.
**In force since:** `d48c4db` (*governed: carry decimal, refuse silent family loss, freeze
candidates*), merged to `main` as `c98cf53e4073869e1da6ae3fafd77d850c637422` via PR #274.
**Reads with:** `docs/architecture/admission_fidelity_study_v0_1.md` (the measured evidence),
`core_realization_profile_v2_freeze.md` (the realization claim shape — a **different** subject, see
§5), `proof_a_proposal_v0_1.md` (where the refusal half is exercised).

---

## Why this record is separate from the realization freeze

This is a **lowering / type-carriage rule**: it governs what a profile may do when it puts a governed
value domain onto a physical representation. The realization-format freeze governs the **shape of a
realization claim** — what a mapping file may assert, and what it may never assert.

The two touch the same `decimal` in passing and are otherwise unrelated jurisdictions. Filing this
ruling inside the freeze would have made a claim-shape document the authority for a carriage rule,
and a later reader looking for the carriage rule would have to know to look in a format freeze to
find it. Separate subject, separate record (instruction, Huayin, 2026-09-12).

---

## 1. The ruling, verbatim

> A governed exact-decimal domain must be carried exactly where the current substrate can carry it
> exactly; it must not be silently lowered to binary floating point.

Quoted rather than paraphrased, and it is worth saying why: the rule has **two halves that pull in
opposite directions**, and every available paraphrase keeps one and loses the other.

- **Where the substrate can carry exactly — carry exactly.** The lawful case is not "close enough".
  A profile that has an exact carrier available and does not use it has lowered the law, not the
  coverage.
- **Where it cannot — refuse, do not coerce.** The rule forbids the *silent lowering*. It does not
  forbid refusal; refusal is the compliant outcome outside the envelope, and an honest refusal is
  the product's asset.

Neither half licenses anyone to *decide* the envelope. The envelope is **measured** (§3), not chosen.

---

## 2. What was wrong, and why it was unforced

`_DOMAIN_TO_DTYPE["decimal"]` mapped to `Float64` — binary floating point substituted for a governed
exact-decimal domain. This is the type-system instance of **reducing law rather than coverage**.

It was **unforced**, which is what makes it a defect rather than a constraint. `Decimal` was already
in `types.DTYPES` and already in `NUMERIC`, so `sum` admitted it under the existing signature, and
the compile → parse → serve test passed unchanged when the mapping was corrected.

A second consequence, independent of precision: binary floating point breaks the **exact
associativity** that C7 / `has_identity` / `_check_continuation_conformance` assert at token level.
The old mapping therefore asserted a property of a representation that the representation did not
have.

---

## 3. The measured evidence available now

From `admission_fidelity_study_v0_1.md`, on one machine at pyarrow 25.0.1 / polars 1.44.2 /
duckdb 1.5.5. **Observations of specific builds, not contractual guarantees** — the study labels
every row, and this ruling inherits those labels rather than promoting them.

**Exact carriage is available on the incumbent path:**

| case | Arrow | in-process | result |
|---|---|---|---|
| `DECIMAL(18,4)` money | `decimal128(18,4)` | `Decimal(18,4)` | **preserved** — `12345678901234.5678` |
| `DECIMAL(38,9)` | `decimal128(38,9)` | `Decimal(38,9)` | **preserved** |
| `DECIMAL(3,1)`, `0.1+0.2` | `decimal128(4,1)` | `Decimal(4,1)` | **preserved** — `0.3` |
| NULL in a decimal column | `decimal128(18,4)` | `Decimal(18,4)` | preserved, **type survives** |

> This is the finding that made the `Float64` mapping unforced: *a governed exact-decimal domain can
> be carried faithfully end to end on the path already in use.*

**And the envelope has measured edges:**

| case | what happens |
|---|---|
| `HUGEINT` → `decimal128(38,0)` at full width | Arrow holds `170141183460469231731687303715884105727` **exactly**; Polars yields `1.7014118346046923173168730371588410573E+38`. **Nothing raises.** |
| decimal stored as SQLite `REAL` | **source loss, at rest**: `12345678901234.5678 → 12345678901234.568` |
| decimal stored as SQLite `TEXT` | preserved exactly |
| ceiling | `DECIMAL(38,37)` crosses intact; `decimal128` carries 38 digits |

Two things follow that the ruling depends on. **The loss is silent** — the HUGEINT case raises
nothing, so "it worked" is not evidence that it was carried. And **fidelity is source-determined,
not transport-determined**: SQLite has no decimal type, so the same value's fidelity depends on a
storage decision (`TEXT` vs `REAL`) that is invisible downstream.

---

## 4. Where the refusal lives, and why it cannot live in the compiler

A governed `value_domain` is the bare token `"decimal"` — **no precision, no scale**. At lowering
there is therefore nothing to compare against a substrate envelope.

> Refusing in the compiler would require **inventing a precision**, which is exactly the kind of
> unauthorized decision this ruling exists to forbid.

The measured envelope (`decimal128`, 38 digits) can only be checked where a **concrete physical
precision exists**, which is **admission**. The rule for a profile is therefore:

- **at lowering:** carry the governed domain onto an exact carrier; never substitute binary floating
  point;
- **at admission:** compare the governed domain against the concrete carrier type, and **refuse**
  outside the faithfully supported envelope rather than coercing into it.

The admission envelope is **four hops, not two** — `source semantics → driver/configuration → Arrow →
in-process carrier conversion`. The HUGEINT case is the empirical reason the fourth hop is named: the
loss occurs *after* Arrow, while Arrow held the value exactly.

---

## 5. What is NOT ruled here

**DuckDB, Arrow and Polars are implementation evidence, not authorities.** They are cited above as
measurements of what a substrate can currently do. They do **not** define governed decimal
semantics, and no property of them may be read back as a rule:

- `decimal128`'s 38 digits are **a measured limit of a carrier**, not the governed bound on an exact
  decimal domain. A different carrier does not change the law; it changes what can be carried.
- Polars' silent narrowing is **a defect to refuse at admission**, never a definition of what
  "decimal" means.
- That a driver *delivered* a value successfully establishes nothing about admissibility. The study's
  own conclusion is kept narrow and is inherited verbatim here: **successful transport does not
  establish admissibility.**

Also not ruled: the *identity* of the faithfully supported envelope as a general matter (it is
measured per substrate, and the measurement is dated); any precision/scale vocabulary for governed
value domains — if one turns out to be required, that is a finding to report, not to invent; and
anything about `FILL`, `empty_fiber`, or approximation, none of which this ruling touches.

**Approximation stays open and unforced.** Nothing here is a conclusion about
approximation-continuation semantics, and `FoundationLaw.approximation` is not read as the governing
text on that question.

---

## 6. Accepted consequences

**The image bytes change** for any publication containing a governed `decimal` family. Artifacts
compiled before `d48c4db` and after it are no longer byte-comparable for those families. **Accepted**
(Huayin, 2026-09-12, at the merge of #274).

**Two pinning tests were edited** — they asserted `TYPE Float64` and now assert `TYPE Decimal` — with
the reason recorded in each. This is recorded as a **ruling, not a repair**: a pinning test is the
record of what was believed correct, so changing one is an exercise of authority and is legible here
rather than only in a diff.
