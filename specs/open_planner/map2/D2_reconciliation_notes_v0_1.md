# MAP-2 · D2 reconciliation notes (v0.1) — pilot-side evidence
### Reconciling the certificate cargo schema against the executed C1 pilot certificate

*CC to desk, 2026-08-01. Task: reconcile `map2_certificate_cargo_schema_v0_1.md` (D2, desk-drafted)
against the pilot's certificate; where they differ, **the pilot is evidence, the schema is proposal**
(charter). Notes returned for adjudication; D2 v0.2 follows.*

## 0 · Blocking note — the D2 schema file did not reach this environment

`map2_certificate_cargo_schema_v0_1.md` is **not present** in my working tree. I checked: the
`attachments/` directory (holds the charter, not the schema), a repo-wide filename search, and a
content grep for `S6 edge attestation` / `channel test` / `certificate_cargo` — no hit. The message
announcing D2 carried **no `[Attached file: …]` line** (the charter message did), so the upload appears
not to have synced. Per the desk's own misfire clause — *a reader's view is not the record; "I cannot
see it" must never be spoken as "it does not exist"* — I am **not** declaring the schema nonexistent,
and I am **not** reconciling against invented field names (S5/S6/S9 definitions, the digest algorithm),
which would be exactly the write-from-memory the program forbids. **Please re-attach D2** and I will
complete the field-by-field pass (§3 below is the list held for it).

What I *can* deliver without the schema text — because they rest on the pilot's own evidence and on laws
the charter already cites — are the two normative checks you flagged to run hard, **V1** and **V3**.
Both are done, with the pilot extended to satisfy them.

## 1 · V1 — every TRANSPORT carries its edge attestation ✔ (implemented from the founding finding)

**Check:** does the pilot certificate carry, for its TRANSPORT node, the edge attestation that D1's
honest center made load-bearing (a bare `JoinRel` on a non-functional key fans out; the edge's
functional/conserving verdict is the cargo)?

**Before:** no — the v0.1 certificate had no edge/transport field (top-level keys were perimeter,
versions, tolerance, N, conservation, tamper, attack_b, ACCEPTED).

**Now:** the pilot emits `semantic.edge_attestation` for its day→cal.month climb (the calendar
`JoinRel`):
```json
{"node": "TRANSPORT", "frm": "day", "to": "cal.month", "via": "calendar",
 "kind": "functional_climb (INNER join on the from-key; no fan-out)", "verdict": "CONSERVES",
 "evidence": "conservation PASS at both grains within tolerance AND the fan-out tamper (double-count)
              is distinguishable — a bare JoinRel on a non-functional key would double-count and the
              harness kills it",
 "law": "V1 — every TRANSPORT carries its edge attestation (D1's founding finding as schema law)"}
```
**Reconciliation ask:** adopt V1 as schema law; reconcile these field names with D2's **S6** edge-
attestation section (I used `frm/to/via/kind/verdict/evidence` provisionally — rename to S6's names in
v0.2). The *content* is what the pilot has evidence for; the *names* are the schema's to fix.

## 2 · V3 — the channel test: nothing semantic may vary ✔ (caught a real flap; fixed by the F5 split)

**Check:** run the pilot twice, diff the certificates, nothing semantic may vary.

**Finding (v0.1 certificate FAILED it):** two independent runs differed — `max_faithful_vs_unfaithful_gap`
flapped `24.978107366980623 → …723`, and `conservation_worst_delta` flapped `1.6e-10 → 2.47e-10`. Root
cause: **float summation ORDER** across Acero and Polars (the 0.13.1 flap class). These are raw
*measurements*, not claims — and a raw measurement on the semantic channel is exactly the false
precision V3 exists to catch.

**Fix (the F5 two-channel law the charter already cites):** the certificate is now split —
- `semantic` — call-invariant facts only (perimeter, substrait_version, tolerance, N, the `passed` /
  `within_tolerance` / `distinguishable` / `ACCEPTED` booleans, the edge attestation). The semantic
  claim about conservation is **`within_tolerance: true`**, never a raw delta.
- `mechanical` — the legitimately-varying diagnostics (`conservation_worst_delta_observed`,
  `attack_b_max_gap_observed`), explicitly labelled "MAY vary run-to-run; not on the semantic channel."

**Result — V3 PASSES:** the pilot writes `d4_c1_semantic_channel.json`; two runs of it are
**byte-identical** (verified), while the mechanical channel differs (as it should). Verify:
```
python pilot_c1.py /tmp/a && python pilot_c1.py /tmp/b
diff /tmp/a/d4_c1_semantic_channel.json /tmp/b/d4_c1_semantic_channel.json   # empty
```
**Reconciliation ask:** D2's channel split is the normative one; adopt the pilot's semantic/mechanical
partition as evidence that the split is *sufficient* here, and reconcile which specific fields D2 places
on each channel. The one firm claim from the evidence: **raw float measurements (worst_delta, gap) must
be mechanical; the semantic conservation claim is a within-tolerance boolean.**

## 3 · Held for the D2 text (field-by-field — pending re-attachment)

These need the schema's actual wording and cannot be reconciled from the pilot alone:
- **S5 — reference-vs-embed.** Does the certificate *embed* the plan/model/ask or carry a *reference*
  (digest/URN)? The pilot currently embeds a prose `perimeter` and inline booleans; it references
  nothing by digest. Reconcile against S5's rule.
- **S6 — edge attestation structure.** §1 gives the pilot's provisional shape; map to S6's fields.
- **S9 — span notation.** The pilot states its perimeter in prose, not a span notation; adopt S9's form.
- **digest algorithm.** The pilot computes no digest yet (V3 is checked by byte-diff of the semantic
  JSON). If D2 mandates a semantic-channel digest, I will add it over the *sort-keyed* semantic block
  (already emitted deterministically for exactly this).

## 4 · Ledger row (from the CARVE root-cause, per your instruction)

- **DOC-1 (docs/teaching, not urgent).** FrameQL `WHERE` is SQL-passthrough to the connector, so a
  double-quoted literal binder-errors as an identifier; single-quoted literals serve. **Action taken:**
  a one-line quoting note added to the Frame-QL Manual Second Edition at §4.1 (WHERE). **Candidate,
  ledgered:** a reason-code upgrade so the raw binder error becomes a named clarify if it proves
  confusing in the wild — not built, rowed for when a real case arrives.

*— CC. V1 and V3 landed on evidence; the field-by-field pass is one re-attachment away.*
