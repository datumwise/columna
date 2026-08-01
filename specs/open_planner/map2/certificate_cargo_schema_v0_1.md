# D2 — Certificate Cargo Schema v0.1
### urn:columna:certificate:v1 — what rides the wire when a certified plan travels

*Desk draft · 2026-07-31 · Beat 2 deliverable D2 per the ratified charter §4.
Keyed off D1's cargo column; the certified-edge finding is field S6, mandatory.
To be reconciled against the pilot certificate (fixtures/d4_c1_pilot_certificate.json)
by CC — where the pilot's field names differ, the pilot is evidence and this
schema is proposal; reconciliation notes come back for adjudication.*

---

## 1 · Carrier and stance

The certificate rides a Substrait plan as an **AdvancedExtension** under the
URN `urn:columna:certificate:v1`. Foreign consumers ignore it by the
ecosystem's own convention; Columna-aware readers treat it as the plan's
legal record. Stance, restated from the charter: the cargo does not make a
foreign engine lawful — it records that lawfulness was adjudicated upstream
and states exactly what the container-Rels cannot say about themselves.

## 2 · The two channels (F5's law, promoted to schema)

Every field belongs to exactly one channel, declared in the schema itself:

**SEMANTIC channel — call-invariant.** Identical across call counts,
backends, attempts, and serving paths. If two certificates for the same
(model, ask, plan) differ on any semantic field, one of them is wrong.

**MECHANICAL channel — legitimately variant.** Serving and provenance
facts that may differ per execution without any semantic claim changing.

**The negative rule, normative:** nothing that can vary with call count,
backend identity, cache state, or attempt number may appear on the
semantic channel — under any name. (F5's finding was a true mechanical
fact wearing a semantic label; the schema makes that a validation error,
not a judgment call.)

## 3 · Semantic channel fields

- **S1 `schema_version`** — literal `"columna-certificate/1"`.
- **S2 `model`** — Manifold identity: name, version, **adjudication
  digest** (the publish-time verdict set's hash). A certificate without an
  adjudicated model underneath certifies nothing; this field is the chain's
  anchor.
- **S3 `ask`** — the canonical FrameQL text (shipped envelope surface,
  attested syntax only) and its parse digest. The denotation standard the
  plan is faithful to.
- **S4 `plan`** — the IR in canonical serialization: node list, canonical
  digest. The thing the certificate is *about*.
- **S5 `obligations`** — the discharge record, one entry per law with
  jurisdiction: `{law_id, clause, verdict, reason_ref}`. Lawfulness made
  enumerable: family licenses, B-anchor checks, M-anchor obligations,
  universe/population clauses, anchor typing.
- **S6 `edge_attestations`** — **MANDATORY for every TRANSPORT in S4** (the
  pilot's founding finding): `{edge_id, from_level, to_level,
  corroboration_verdict_ref}` for each hierarchy edge the plan traverses. A
  bare JoinRel cannot say it is a corroborated-functional transport; this
  field is where that fact lives. A certificate containing a TRANSPORT
  without its S6 entry is INVALID by schema.
- **S7 `face_spends`** — for every CROSS: `{face_id, scheme
  (touch|assign|alloc), conservation_claim}`. (Per D1, CROSS execution does
  not lower at v1 — but a plan may contain a stay-home CROSS whose result
  feeds lowered work; the spend is still part of the plan's legal record.)
- **S8 `disclosure_projection`** — the semantic disclosures the answer must
  carry (two-stage statistics, crossing caveats, coverage conditions),
  derived from S5/S7, call-invariant by construction.
- **S9 `lowering_map`** — node-span mapping: which IR nodes lowered to
  which Rel spans, and which nodes are STAY-HOME (executed in the metrics
  engine). The pushdown boundary, stated per plan.
- **S10 `perimeter`** — one prose field, mandatory: what this certificate
  covers and what it does not (the seam-certificate discipline, kept).

## 4 · Mechanical channel fields

- **M1 `lowering_attestation`** — producer + versions (ibis-substrait,
  Substrait spec pin e.g. 0.46.0, proto pin), lowering-rule ids applied,
  each with its **rule-certificate ref** (the per-rule oracle proof this
  execution inherits).
- **M2 `backend`** — consumer identity and version (e.g. Acero/pyarrow X,
  DuckDB+extension Y). Per-backend inheritance is checked against M1's
  rule certificates: a rule not certified for this backend ⇒ the plan does
  not lower here (falls home), never "lowers with a warning."
- **M3 `oracle_run`** — for pilot/acceptance certificates: N, tolerance,
  worst delta, tamper-control status, date, harness version.
- **M4 `serving`** — cache/freshness facts (the reformed F5 residents),
  attempt metadata, timestamps.

## 5 · Validation rules (normative, machine-checkable)

V1: every TRANSPORT in S4 has an S6 entry. V2: every CROSS has an S7
entry. V3: no field outside §4 varies across two executions of the same
(S2,S3,S4) — the channel test. V4: every lowering-rule id in M1 resolves
to a rule certificate covering M2's backend. V5: S10 non-empty. V6: S3's
ask text parses on the shipped envelope grammar (attested-syntax rule,
enforced). A certificate failing any V-rule is not a weaker certificate;
it is not a certificate.

## 6 · Open for reconciliation (CC → desk)

Field-name deltas vs the pilot JSON; whether S5 verdict refs point into
the Manifold's published adjudication record or embed; S9 span notation;
canonical digest algorithm choice. Reconciliation notes return with the
next PR; schema v0.2 follows adjudication.

*— the desk. The schema's one-sentence soul: the semantic channel is what
the plan means; the mechanical channel is how this run happened; and the
wall between them is load-bearing.*
