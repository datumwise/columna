# MAP-2 · D2 reconciliation notes (v0.1) — full field-by-field
### Reconciling `certificate_cargo_schema_v0_1.md` against the executed C1 pilot certificate

*CC to desk, 2026-08-01. The D2 schema was re-attached and is filed at
`specs/open_planner/map2/certificate_cargo_schema_v0_1.md`. This is the field-by-field pass. **Where
the pilot and schema differ, the pilot is evidence and the schema is proposal;** recommendations are
tagged for adjudication. Schema v0.2 follows. (The earlier blocking note — D2 not received — is
RESOLVED.)*

## 0 · Headline reconciliation finding

The pilot already carries the F5 two-channel split (§2 of D2), and its **V1 and V3 are satisfied in
substance** (edge attestation present; semantic channel byte-stable across two runs). The one
structural correction D2 makes, and it is the right one: **the pilot's semantic channel conflated the
semantic *obligation verdict* with the mechanical *validation run*.** N, tolerance, the tamper status,
and the toolchain versions are *how this run was validated* (mechanical, M1/M2/M3); the semantic claim
is the **conservation obligation discharge** (S5) + the **edge attestation** (S6) + the **perimeter**
(S10). Moving them does not break V3 — they are invariant across runs anyway — but it is the correct
channel assignment, and it is the delta v0.2 should adopt.

## 1 · Semantic channel — S1…S10 vs the pilot

| field | D2 requires | pilot today | verdict / recommendation |
|---|---|---|---|
| **S1** `schema_version` | literal `"columna-certificate/1"` | absent (`certificate` holds a URN) | **ADD S1**; keep the URN as the certificate *instance* id |
| **S2** `model` | Manifold name, version, **adjudication_digest** | absent (Cascadia named only in perimeter prose) | **GAP — the chain anchor.** Add `{name, version, adjudication_digest}`; for the demo, embed with the digest (no published registry yet — §5) |
| **S3** `ask` | canonical FrameQL text + **parse_digest** | ask text present (conservation labels + perimeter); no parse_digest | **PARTIAL** — add `parse_digest` (§5 digest choice) |
| **S4** `plan` | IR node list + **canonical digest** | prose description only | **GAP** — emit the canonical IR node list + digest (the D1 trace already knows the nodes; serialize them) |
| **S5** `obligations` | `[{law_id, clause, verdict, reason_ref}]` | conservation asserted as a `within_tolerance` boolean, not enumerable | **GAP** — the conservation discharge (obligation B, outbound twin) becomes one S5 entry: `{law_id: "conservation", verdict: "discharged", reason_ref: → M3 oracle_run}` |
| **S6** `edge_attestations` | **list**, one per TRANSPORT: `{edge_id, from_level, to_level, corroboration_verdict_ref}` | **present** as a single `edge_attestation` object `{frm,to,via,verdict,evidence}` | **DELTA (content ✓, shape ✗)** — make it a **list**; rename `frm→from_level`, `to→to_level`; add `edge_id`; `verdict`→`corroboration_verdict_ref` (D2 wants a ref, pilot embeds `CONSERVES`+prose — §5 ref-vs-embed). This is D1's founding finding; the pilot has the fact, needs the S6 shape |
| **S7** `face_spends` | per CROSS `{face_id, scheme, conservation_claim}` | none (C1 has no CROSS) | **N/A for C1** — V2 vacuously satisfied; a faced pilot populates it |
| **S8** `disclosure_projection` | semantic disclosures (two-stage stats, crossing caveats, coverage) | absent | **GAP** — Attack B's unfaithful reading *is* a two-stage-statistic disclosure; S8 should carry it, derived from S5 |
| **S9** `lowering_map` | node→Rel span map + STAY-HOME | absent (D1 table has Rel compositions in prose) | **GAP** — emit per §5 span notation; for C1, every node lowered (no stay-home); a sketch/median pilot would carry stay-home entries |
| **S10** `perimeter` | one prose field, mandatory | **present** ✓ | **MATCH** |

## 2 · Mechanical channel — M1…M4 vs the pilot

| field | D2 requires | pilot today | verdict / recommendation |
|---|---|---|---|
| **M1** `lowering_attestation` | producer + version pins + **lowering-rule ids + rule-certificate refs** | producer + substrait_version present but **on the semantic channel** (`toolchain`, `substrait_version`); no rule-cert refs | **MOVE to M1** (mechanical); **ADD** lowering-rule ids + rule-certificate refs — the C1 conservation *is* the rule proof for the TRANSPORT-shaped rule on Acero; mint it as a referenceable rule certificate (enables V4 / DuckDB inheritance) |
| **M2** `backend` | consumer identity + version; inheritance checked vs M1 rule certs | consumer in `toolchain` (semantic) | **MOVE to M2** (mechanical); the per-backend inheritance check is the DuckDB-second-consumer mechanism (D5 · BLOCK-1) |
| **M3** `oracle_run` | N, tolerance, **worst delta**, tamper status, date, harness version | N/tolerance/tamper on **semantic**; worst_delta already mechanical | **CONSOLIDATE into M3** (mechanical). Note: the pilot emits **no date/timestamp** — deliberately, so the semantic channel stays byte-stable (V3); a date is legitimately mechanical and can be added there |
| **M4** `serving` | cache/freshness, attempt metadata, timestamps | none (a pilot, not a serve) | **N/A for C1** |

## 3 · Validation rules V1…V6 — pilot status

- **V1** (every TRANSPORT has an S6 entry) — **SATISFIED in substance**: the pilot emits the edge
  attestation and its content is complete; needs the S6 list shape (§1).
- **V2** (every CROSS has an S7 entry) — **vacuously satisfied**: C1 has no CROSS.
- **V3** (nothing outside §4 varies across two runs) — **PASSES**: two runs of the semantic channel are
  byte-identical (verified: `diff d4_c1_semantic_channel.json` across runs is empty). Under D2's channel
  reassignment (§1/§2) it *still* passes — the moved fields are invariant anyway.
- **V4** (every M1 lowering-rule id resolves to a rule certificate covering M2's backend) — **NOT YET**:
  M1 has no rule-cert refs. **This is the gap that makes the DuckDB inheritance test executable** — once
  the C1 TRANSPORT-shaped rule is a referenceable rule certificate (Acero-covered), V4 checks whether a
  second backend inherits it. Recommend minting the C1 rule certificate as M1's first entry.
- **V5** (S10 non-empty) — **SATISFIED**: perimeter present.
- **V6** (S3 ask parses on the shipped envelope grammar) — **SATISFIED**: the pilot asks parse (the
  Manual self-check enforces attested syntax); the composite pin + faced coords are all attested.

## 4 · D2 §6 open questions — recommendations

- **S5 verdict refs — ref vs embed.** **Recommend REF** into the Manifold's published adjudication
  record, anchored by S2's `adjudication_digest`; embedding duplicates the record and dissolves the
  chain anchor. **Demo fallback:** where no published adjudication registry exists (Cascadia), embed the
  verdict *together with* the `adjudication_digest` so it stays re-derivable; production resolves the ref.
- **S9 span notation.** **Recommend:** each IR node carries a `node_id` from S4's canonical
  serialization; `lowering_map = {node_id: {kind: "lowered", rel_span: [<RelRoot-relative child-index
  path>]}}` — a Substrait plan is a tree of Rels, so an index path (e.g. `[0,1]` = root→child0→child1)
  locates the subtree realizing a node; STAY-HOME nodes map to `{kind: "stay-home", engine: "metrics"}`.
- **Canonical digest algorithm.** **Recommend SHA-256 over canonical JSON** (UTF-8, `sort_keys=True`, no
  insignificant whitespace). The pilot **already** emits a sort-keyed semantic serialization
  (`d4_c1_semantic_channel.json`) precisely for this — reuse it as the digest input, which makes the
  certificate digest reproducible and V3-aligned (a byte-stable semantic channel → a stable digest).

## 5 · What the C1 certificate needs to become schema-conformant (held for v0.2, per the ruling)

The next pilot emits a schema-conformant certificate (the schema's own acceptance test), and C1 can be
re-emitted once v0.2 settles field names. The delta list, ready to apply:
add **S1, S2, S3.parse_digest, S4, S5, S8, S9**; reshape **S6** to a list; move **version/backend/
N/tolerance/tamper** to **M1/M2/M3**; add **M1 rule-cert refs** (mint the C1 rule certificate → unlocks
**V4** and the DuckDB inheritance test). V1/V3 already hold; S7/M4 stay N/A for the sum shape.

## 6 · Ledger — DOC-1 (done)

FrameQL `WHERE` is SQL-passthrough → double-quoted literals binder-error as identifiers. One-line
quoting note added to the Frame-QL Manual Second Edition §4.1 (single-quote string literals in `WHERE`).
Reason-code upgrade rowed as a future candidate. Manual self-check green (37 examples, 0 FAIL).

*— CC. V1 ✔ V3 ✔ on evidence; the full S1…S10 / M1…M4 / V1…V6 map above is the reconciliation for
adjudication. On v0.2, the second pilot emits the conformant certificate; C1 re-emits to match.*
