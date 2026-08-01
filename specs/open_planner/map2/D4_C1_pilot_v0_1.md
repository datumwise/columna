# MAP-2 · D4 — the C1 pilot: a certified lowering (v0.1)
### The first conservation certificate of the outbound turn

*Deliverable D4 of the Beat-2 charter, executed after the pre-D4 ruling (2026-07-31): Acero is C1's
first consumer; DuckDB is deferred-not-dropped. Run it:*
```
python specs/open_planner/map2/pilot_c1.py specs/open_planner/map2/fixtures/
```
*Evidence: `fixtures/d4_c1_pilot_certificate.json` — `ACCEPTED: true`.*

## What was lowered

The **TRANSPORT-shaped composition** (D1 row C1):
`sum(revenue @ {store*product*cal.month}) AT {cal.month}` — a `JoinRel` (transactions ⋈ calendar on
`day`) + `AggregateRel`(sum → store·product·month) + `AggregateRel`(sum → month), the join-and-regroup
the charter chose because it uses only monoid aggregation and an inner join — the Substrait shapes most
likely to round-trip. Produced with `ibis-substrait` (Substrait **0.46.0**), executed on **Acero**
(`pyarrow.substrait`), oracle-compared against the shipped Polars engine through the D3 harness.

## Acceptance — every criterion, checkable

| criterion (charter §5(4)) | required | result |
|---|---|---|
| **N comparisons** | ≥ 30 | **16 548** (16 524 at store·product·month + 24 at month) |
| **conservation** | zero disagreements within stated tolerance | **PASS** — 0 disagreements; **worst delta 2.6 × 10⁻¹⁰** vs a **stated absolute tolerance of 1 × 10⁻⁶** |
| **tamper control (re-run in the pilot)** | a broken lowering must FAIL loudly | **VALID** — a double-count lowering (the exact bare-`JoinRel` fan-out D1 warns about, simulated by a ×2 `ProjectRel`) fails on all 16 524 cells; the D3 oracle-side negative control is also re-run and valid |
| **Attack B stress (Class C)** | faithful agrees; unfaithful **distinguishable** | **OK** — the faithful mean lowering agrees with the faithful oracle; the unfaithful lowering is self-consistent with the *unfaithful* oracle **and** differs from the faithful oracle by up to **24.98** per month — distinguishable, exactly Class C |
| **perimeter stated** | in the certificate | **yes** — see below |
| **ACCEPTED** | all of the above | **true** |

## The Attack B stress, in one line

The pilot lowered **both** halves of Attack B. The faithful plan (mean over transaction atoms → lowered
as the REDUCE mule decomposition, mean-of-atoms) agrees with the oracle. The unfaithful plan (mean of
store·product·month sums) is a *lawful* Rel composition that **faithfully computes its own plan** (it
matches the unfaithful oracle) yet denotes a different statistic — and the harness **distinguishes it
from the faithful answer**. This is the charter's thesis made executable: *we certify the computation,
never the coincidence of its outputs.* Output agreement between the faithful and unfaithful plans would
not have saved the unfaithful one; only `plan ⊨ ask` separates them, and only a certificate — not a
diff against DuckDB — carries that.

## The perimeter (stated, as the certificate requires)

> Cascadia warehouse · transaction universe · `revenue = sum(amount)` joined to calendar on `day` · the
> TRANSPORT-shaped sum at `(store, product, cal.month)` and its roll-up to `cal.month` · lowered to
> Substrait **0.46.0** via ibis-substrait 4.0.1, executed on **Acero** (pyarrow 25.0.0) · oracle =
> columna-core **0.14.0** on Polars **1.43.1** · absolute tolerance **1 × 10⁻⁶**.

The certificate covers **exactly** this. It does **not** claim: any other node's lowering (D1's proposed
verdicts stand as proposed until each is piloted), any DuckDB result (deferred), or any face/CROSS or
sketch/holistic REDUCE (D5: NOT-LOWERABLE v1). The conservation obligation was checked **per-rule inside
the TCB against our own oracle**, never per-plan against a stranger (custody law, charter §7).

## What the pilot confirms for the study

- **The TRANSPORT-shaped lowering is CERTIFIABLE-PER-RULE in practice**, not just on paper — the D1
  verdict for C1 is now backed by an executed conservation certificate, not a proposal.
- **The oracle protocol (D3) generalizes to a real consumer** unchanged: the same instruments and the
  same negative control certified an Acero-executed Substrait plan. When DuckDB's extension becomes
  reachable (D5 · BLOCK-1), it enters as the **second consumer under this identical harness** — making
  this pilot the study's first **cross-consumer inheritance test** (the ruling's framing).
- **The fan-out hazard is real and catchable.** The double-count tamper — a lawful Rel composition — is
  exactly what an uncertified `JoinRel` on a non-functional key would produce, and the harness kills it.

## D2 reconciliation outcome (V1, V3 — checked hard; detail in `D2_reconciliation_notes_v0_1.md`)

- **V1 — every TRANSPORT carries its edge attestation:** the certificate now emits
  `semantic.edge_attestation` for its day→cal.month climb (D1's founding finding as a first-class
  field: the calendar `JoinRel` conserves — attested by the conservation PASS *and* the fan-out tamper
  being distinguishable).
- **V3 — the channel test caught a real flap and now passes:** two runs of the v0.1 flat certificate
  differed (raw `worst_delta` / `max_gap` flap by float summation order). The certificate is now split
  into a **semantic** channel (call-invariant facts; the conservation claim is `within_tolerance: true`,
  never a raw delta) and a **mechanical** channel (the varying measurements, labelled as such). Two runs
  of `d4_c1_semantic_channel.json` are **byte-identical**; the mechanical channel varies, as the F5 law
  allows. (The D2 schema file did not reach this environment — the field-by-field pass is held for
  its re-attachment; see the reconciliation notes §0.)

## Ledger deltas (feed D5)

- **BLOCK-1 → status update.** DuckDB is the second consumer under the C1 harness — the cross-consumer
  inheritance test. *(▸ correction 2026-08-01: the earlier "unreachable / egress" framing was wrong; the
  extension is merely unpublished for DuckDB 1.5.5, resolved by a consumer pin `duckdb==1.1.3`, no
  environment change — the test is **un-gated**. See BLOCK-1.)*
- **No new NOT-LOWERABLE found in C1** (expected — C1 is the friendly shape). The NL rows (sketch-distinct,
  exact median/mode) and the CROSS disclosure-mint non-delegability await their own pilots.

*— CC, D4 v0.1. The certificate is executed and committed; D4 acceptance is the ratifier's to confirm.*
