# Ruling 2026-08-22 (CG2) — the lowering receipt, and the milestone hold

**Status:** **restored record.** Documentation only. Authorizes nothing that the ruling itself did not
authorize on the day it was made.
**Ruled:** 2026-08-22 (CG2).
**Restored to the repository:** 2026-08-22, on instruction, after a read-only checkpoint review found
that shipped code cites this ruling by section number while the repository could not show it.
**Governs:** the lowering receipt shipped in `columna-server` 0.9.0, released as `v0.15.2`
(`8c85db3cbc80ae95286afbc7e23f618abe991bb2`; triad `columna` 0.15.2 / `columna-core` 0.15.2 /
`columna-server` 0.9.0).
Reads with `core_p1_compiler_contract.md`, `core_p1_compiler_input.md`,
`core_p05_certification_lifecycle.md`, `core_p05a_closed_by_default_serving.md`.

---

## Why this record exists

`columna_server/lowering_receipt.py` opens by citing "**CG2 ruling, 2026-08-22 §1**", and cites §2 and
§3 further down; `columna_server/tools.py` cites §3; PR #198 records §1, §2, §3 and §5 as the rulings it
honoured. The document those citations point at was never committed. A reader holding the code could
therefore see *that* an authority was invoked but not *what* it said — and the milestone boundary that
holds compiler work behind the Core-P1 checkpoint survived only as prose in a changelog.

That is a record defect, not a semantic one: the implementation is consistent with the ruling. This file
closes the defect by putting the ruling where its citations can resolve.

**This restoration is not a re-ruling.** It states what was decided on 22 August 2026, in the terms it
was decided, and nothing further.

---

## What was ruled

### 1. The receipt establishes an exact publication→execution-image binding, and only that

The lowering receipt establishes:

```
exact governed publication  →  exact compiled Core execution image
```

It answers one question — *was this image compiled from this publication?* — and stays silent on every
other.

### 2. The receipt does not imply certification, evidence, or `PublishedScope`

A receipt is **not** certification, **not** attestation, **not** evidence, and **not** `PublishedScope`
admission. Receipt presence must never be read as current certification. The lifecycle is unchanged, and
the receipt sits at exactly one step of it:

```
publication + mapping
    → compile CLOSED image        ← the receipt records THIS step, and only this step
    → realization/data adjudication
    → certification
    → PublishedScope admission
    → serve
```

### 3. The receipt is meaning-free, and verifiable at runtime without the private mapping

The runtime must be able to verify the binding **without**:

* loading the private mapping;
* reconstructing logical meaning from the `.cml`;
* re-running lowering.

The receipt carries no analytical meaning — no universe, measure, level, predicate or family — so it
cannot become a second, quieter channel for publication meaning. Binding identity is **deterministic**:
two receipts produced from identical inputs bind identically.

### 4. `contract_version = "3"` remains

The receipt's condition vocabulary is an **additive** extension inside `contract_version` `"3"`. The
catalog's shape is unchanged — same rows, same keys, same order — and only the set of values a
`conditions` entry may take grows. This is not a wire break.

### 5. Milestones 1–3 were authorized

Milestones 1–3 were authorized by this ruling. **They are now complete**, shipped in PR #198 and released
as `v0.15.2` / `columna-server` 0.9.0.

### 6. Milestones 4–7 were held, in this order

```
4  PrivateCoreMapping
5  minimal fail-closed compiler + .cml emitter + receipt emitter
6  provisioner
7  first public governed fixture
```

**Mapping precedes compiler.** The order is part of the ruling, not an implementation preference.

### 7. No milestone 4–7 implementation was authorized

This ruling authorized no compiler, no `PrivateCoreMapping`, no provisioner, and no public governed
fixture. That work requires a later checkpoint decision — the Core-P1 checkpoint recorded at the end of
`core_p1_compiler_contract.md` ("No compiler implementation until this lifecycle checkpoint is reviewed
and ruled").

---

## Citation map — where the shipped code invokes this ruling

| § as cited | cited by | clause above |
|---|---|---|
| **§1** | `columna_server/lowering_receipt.py` ("WHAT THIS ESTABLISHES, EXACTLY"); PR #198 ("receipt ≠ certification") | 1 and 2 |
| **§2** | `columna_server/lowering_receipt.py` ("THE RUNTIME MUST BE ABLE TO VERIFY THE BINDING WITHOUT"; "BINDING IDENTITY IS DETERMINISTIC"); PR #198 ("meaning-free, deterministic") | 3 |
| **§3** | `columna_server/lowering_receipt.py` ("FORMAT VOCABULARY … three conditions"); `columna_server/tools.py` (additive vocabulary inside `contract_version "3"`); PR #198 | 4 |
| **§4** | **nothing** — see the gap note below | — |
| **§5** | PR #198 ("**§5 — held.** No compiler, no `PrivateCoreMapping`, no provisioner, no public governed fixture") | 6 and 7 |

**Gap, recorded rather than filled.** No shipped artifact cites **§4**, and its text is not recoverable
from this repository. Clause 5 above (milestones 1–3 authorized) likewise carries no § citation in any
shipped artifact. Neither is reconstructed here. If the original §4 is later recovered and says something
this record does not, the original governs and this file is amended.

---

## What this ruling did not do

It did not certify anything, weaken any legacy semantics, promote any fixture, break the wire, or move
the Core-P1 checkpoint. The blast wall is untouched: `GovernedPublication.logical` still comes only from
the governed publication artifact.
