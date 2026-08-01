# MAP-2 · v0.2 conformance — steps 1–3 (rule certs, C1 re-emit, C2 pilot)
### The first rule certificates, and the schema's own acceptance test, passed

*CC to desk, 2026-08-01. Executes the three-step sequence on D2 v0.2
(`certificate_cargo_schema_v0_2.md`). Run:*
```
python specs/open_planner/map2/emit_c1_v0_2.py specs/open_planner/map2/     # steps 1-2
python specs/open_planner/map2/pilot_c2.py     specs/open_planner/map2/     # step 3
```

## Step 1 — the first rule certificate in existence

`adjudication_record/rule_c1_transport_shaped_sum.json` — the **TRANSPORT-shaped-sum rule × Acero**,
minted from the accepted C1 pilot's numbers (§4b shape). Digest
`sha256:02ed755e…` — the content-address of the rule's **identity** (rule_id · statement · backend
band · perimeter), *not* the mechanical proof-run, so re-proof yields the same ref and a plan cert's
ref cannot flap (the digest-basis refinement flagged in the #128 notes, now realized). This digest is
what every future M1 points at; V4 resolves against it.

## Step 2 — C1's plan certificate, re-emitted v0.2-conformant

`fixtures/c1_plan_certificate_v0_2.json` — the staged delta list went live: **S1** schema_version,
**S2** model + adjudication_digest (the chain anchor), **S3** ask + parse_digest, **S4** IR node list +
digest, **S5** obligations (conservation entry `mode: ref` → the rule cert; family/edge entries),
**S6** the edge attestation as a **list**, **S8** the two-stage-statistic disclosure (read from the
wire, not memory), **S9** lowering_map in RelRoot-relative child-index paths (`[]`→REDUCE, `[0]`→REDUCE,
`[0,0]`→TRANSPORT, `[0,0,0]`/`[0,0,1]`→CARVE reads). **Channel test (V3):** two independent emissions of
`c1_semantic_channel_v0_2.json` are **byte-identical** (external diff empty); the mechanical channel
carries N/tolerance/worst_delta/date and may vary. `c1_v0_2_channel_test.txt` records it.

## Step 3 — C2 pilot: the full spine, emitting v0.2-conformant NATIVELY (the acceptance test)

C2 ask: `avg(revenue @ {store*cal.month}) AT {cal.month} WHERE day >= '2024-04-01'` — the full
CARVE→COLUMN→TRANSPORT→REDUCE spine, exercising two things C1 did not:

- **CARVE as a Substrait `FilterRel`** — the newly-attested WHERE predicate, lowered and executed on
  Acero (the pre-D4 flag noted FilterRel was untested; it round-trips).
- **The REDUCE-mean rule** — a mule mean lowered as its **sufficient statistics** (`AggregateRel[sum]`,
  `AggregateRel[count]`) then a `ProjectRel` divide: the mean-of-means theorem as a lowering constraint.

Acceptance (same bar as C1):

| criterion | result |
|---|---|
| N comparisons | **509** (21 at cal.month + 488 sufficient-statistic sums at store·cal.month) |
| conservation | **PASS** — 0 disagreements, worst delta **5.5 × 10⁻¹²** vs stated **1 × 10⁻⁶** |
| tamper control | **VALID** — a wrong-grain mean (mean of raw amounts, Attack B's input-grain subject) fails on all 21 cells; D3 negative control re-run valid |
| perimeter | stated in the certificate |
| **V1/V3/V4/V5/V6** | **all pass** |
| **schema acceptance** | **PASS** — the native v0.2 emission satisfies every validation rule |

**This is the schema's own acceptance test (schema §6), passed:** the second pilot emits a
v0.2-conformant certificate natively (`fixtures/c2_plan_certificate_v0_2.json`), and C1 re-emitted to
match (step 2).

## The second rule certificate, and amortization made visible

`adjudication_record/rule_c2_reduce_mean_decomposition.json` — the **REDUCE-mean rule × Acero**, digest
`sha256:99afe22f…`, minted on C2's pass. And the amortization economics are now concrete: **C2's M1
references *both* rule certificates** — the new mean rule *and* C1's TRANSPORT-shaped-sum rule, reused
for C2's inner (store,cal.month) sums (S5 carries an `inherited` obligation pointing at C1's digest). A
plan cert *points, never copies*; the second time a rule is needed it costs a reference, not a proof.

## What this unlocks

Two rule certificates now live in the published adjudication record. **Step 4 — the DuckDB
second-consumer inheritance test** — is **UN-GATED** (▸ correction 2026-08-01: the earlier "queued on
egress" was wrong — see BLOCK-1; the extension is merely unpublished for DuckDB 1.5.5, resolved by a
consumer pin `duckdb==1.1.3`, no environment change). It asks: does DuckDB mint its *own* backend-band
certificate for these two rules, or does engine drift **refuse** them (V4: no cover, no lowering — falls
home, never "lowers with a warning")? The harness, the oracle, the rule certs, and the two rules under
test are all in place; the consumer is a version pin away.

## Open, carried to v0.3 (per schema §6)

S7's shape awaits a **CROSS-bearing** exhibit (neither C1 nor C2 crosses); **rule-cert versioning
across backend bands** is exactly what the DuckDB run will pressure-test; whether **S8 entries carry
severity grades** (C1/C2 disclosures are all `immaterial` — a material one would test the field).

*— CC. Steps 1–3 executed and verified. On your word: v0.3 (a CROSS pilot for S7) or step 4 (DuckDB
inheritance, un-gated) — whichever you call.*
