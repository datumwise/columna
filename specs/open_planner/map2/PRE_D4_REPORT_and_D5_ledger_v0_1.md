# MAP-2 · Pre-D4 report + D5 ledger (v0.1)
### "D1 skeleton + D3 harness first, report before D4 commits" — the report

*CC to desk/ratifier, 2026-08-01. The charter's sequence gate: D1 table skeleton and D3 harness are
built and self-verifying; this report lands **before** D4 commits, and flags — per the explicit
instruction — everything the DuckDB substrait extension cannot round-trip in this environment, before I
build around it. Nothing here is a custody or scope ruling; those are the ratifier's.*

---

## 1 · What is done (checkable now)

| deliverable | artifact | state |
|---|---|---|
| **D1 left column** (attested trace) | `trace_nodes.py` → `fixtures/d1_polars_trace.json` | **green** — 9 cold asks cover all 8 nodes + both compositions; **0 ninth-node candidates** (every engine Polars op is accounted for by the eight nodes) |
| **D1 table** | `D1_lowering_table_v0_1.md` | **complete, verdicts PROPOSED** — 8 nodes + TRANSPORT-shaped + full spine; no empty verdict cells; Substrait **0.46.0** pinned in the header |
| **D3 harness** | `oracle_harness.py` (`--selftest`) | **green** — oracle==oracle passes; **negative control VALID**: 3 tamper modes (perturb / drop-row / swap-scale) each FAIL loudly on 2 asks; baseline + restored pass |

Run them:
```
python specs/open_planner/map2/trace_nodes.py    specs/open_planner/map2/fixtures/
python specs/open_planner/map2/oracle_harness.py --selftest
```

## 2 · THE PRE-D4 FLAG — the DuckDB substrait extension does not round-trip here

**Finding (blocking, environmental).** The DuckDB substrait extension — the charter's named *first
consumer* (§4 D3) — **cannot be obtained in this environment**. `INSTALL substrait` / `LOAD substrait`
fail: `extensions.duckdb.org` returns **HTTP 403 Forbidden**, and no substrait extension binary is
present for the installed DuckDB **1.5.5**. There is no pip-installable `duckdb-extension-substrait`
wheel either. So `duckdb.get_substrait` / `from_substrait` do not exist in this sandbox, and a
DuckDB-consumer pilot is **not runnable here as specified**.

**The offline path that DOES work — proposed substitution for the desk.** Producer + consumer are both
available and were exercised **end-to-end** before writing this:

- **Producer**: `ibis-substrait` 4.0.1 (→ `substrait` proto **0.16.0**) compiles an ibis expression to a
  Substrait plan; `plan.version` = **0.46.0**.
- **Consumer**: **`pyarrow.substrait` (Acero)** — pyarrow 25.0.0, 65 supported function URIs — consumes
  and *executes* the plan against Arrow tables. Proven smoke: `sum(v) group by g` produced by
  ibis-substrait, executed by Acero, correct result (`a→3, b→3`).

Acero is the reference C++ Substrait consumer (not a downgrade from DuckDB); it is a legitimate first
consumer and keeps the study fully offline. **But the charter named DuckDB, and the consumer is a
study-shaping choice — so I am flagging, not switching.** Requested ruling: **may D4's first consumer be
Acero (pyarrow.substrait), with DuckDB deferred to whenever the extension is reachable?** The D3 protocol
and instruments are consumer-agnostic; only the "execute the candidate" step changes.

**What Acero may still not round-trip (to be bounded IN D4 before it commits, per §8).** The pilot's
round-trip verification must bound fidelity first for: the **FULL OUTER `JoinRel`** (ALIGN), the
**top-per-member window/filter** (CROSS assign), and any **drift-prone scalar** (DERIVE divide/null).
The C1 pilot target (TRANSPORT-shaped: JoinRel + AggregateRel(sum)) uses only monoid aggregation and an
inner join — the Substrait shapes most likely to round-trip — which is why the charter chose it.

## 3 · D5 ledger — rows as found (dated 2026-08-01)

A study that finds nothing unliftable has not looked. Rows below are **findings**, not misses.

| id | kind | row | reason / disposition |
|---|---|---|---|
| **NL-1** | NOT-LOWERABLE (v1) | REDUCE · `approx_distinct` (sketch distinct) | engine-specific HLL/witness state; no Substrait `AggregateRel` function carries a mergeable sketch → stays home; pushdown boundary at the reducer |
| **NL-2** | NOT-LOWERABLE (v1) | REDUCE · exact `median` / `mode` | holistic, no fertile carrier; recompute-from-base only → stays home |
| **DEFER-1** | not delegable (custody) | CROSS · disclosure minting | the over_count / `memberships_unrepresented` shadow / reconciliation badge mint **at our door**, never on the substrate; CROSS arithmetic lowers per-shape but the disclosure obligation stays home |
| **DEFER-2** | verify-in-D4 | CROSS · `assign` top-per-member | may need a window Substrait 0.46.0 expresses awkwardly; bound the Acero round-trip before relying on it |
| **DEFER-3** | inherited refusal | composite-pin × faced-output | already a shipped `chained_crossing` refuse (OF-26); the lowering inherits the refusal — nothing to lower |
| **GAP-1** | attestation gap | CARVE · WHERE→`FilterRel` | the `_confine` filter path is under-exercised by the Cascadia serving corpus (every WHERE tried hit a region binder error or `filter_unreachable`); need a fixture with a reachable predicate before CARVE's FilterRel lowering is certified |
| **VER-1** | version-pin risk | Substrait **0.46.0** | pinned via the producer; Rel/function vocabulary is version-scoped; drift across versions is a finding, not a surprise (charter §8) |
| **VER-2** | pin-fragility | producer proto pin | `substrait` 0.30.0 (current default) breaks `ibis-substrait` 4.0.1 (`__substrait_version__`); pinned `substrait==0.16.0` to resolve — record so the toolchain is reproducible |
| **BLOCK-1** | environmental blocker | DuckDB substrait extension | HTTP 403 on `extensions.duckdb.org` for DuckDB 1.5.5; consumer substitution to Acero proposed (§2) — **awaiting ruling** |

## 4 · Findings from D1 worth the desk's eye (detail in `D1_lowering_table_v0_1.md` §Findings)

- **F-a — node boundaries are LOGICAL, not physical.** `_deliver_and_transport_monoid` fuses
  COLUMN+TRANSPORT+REDUCE into one method issuing `join`+`group_by`+`agg`; a lowering must *split* that
  into `JoinRel` (TRANSPORT) + `AggregateRel` (REDUCE) with a **certified seam** between — the node seam
  is a lowering obligation the engine currently discharges implicitly.
- **F-b — CARVE's base scan is below Polars** (a duckdb read → `pl.from_arrow`); it lowers to `ReadRel`
  cleanly, but its attestation lives in the connector, not the Polars op-log.
- **The honest center holds (Q2).** The load-bearing loss is **TRANSPORT**: a bare `JoinRel` on a
  non-functional key silently fans out — the *whole* faithfulness of a transport is the edge's
  corroborated-functional verdict, which Substrait cannot see and the certificate must carry. Every
  "faithful" lowering of TRANSPORT is faithful *only under the certified-edge precondition*.

## 5 · Proposed next step (on the ruling)

On a **go** for Acero as D4's first consumer: I build the C1 pilot (TRANSPORT-shaped
`sum(revenue @ {store*product*cal.month}) AT {cal.month}`) — lower → Substrait 0.46.0 → Acero →
oracle-compare through D3 — to the charter's acceptance (N ≥ 30 comparisons, zero disagreements within a
stated tolerance, perimeter in the certificate, Attack B's fixture as the stress case: faithful agrees,
a lowered *unfaithful* variant is distinguishable). I do **not** commit D4 until this report is ruled on.

*— CC. D1 + D3 are on the branch; D2 (cargo schema) is the desk's; the verdict column and the consumer
substitution are yours.*
