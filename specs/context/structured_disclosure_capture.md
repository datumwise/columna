# Structured disclosure — design capture

A disclosure should be a **structured record**, not a blob of prose. The Haiku baseline-vs-framework
comparison made the case concrete: free-text disclosure forces a false binary and penalizes honesty.
This note fixes the contract, names the load-bearing field, and records how it changes the benchmark,
the detector, and the paper's thesis.

## The insight (why prose disclosure is the defect)

In the Haiku run, the two-anchors framework cut silent failures nearly in half but *lowered* trust,
because on clean additive questions the model added an "input anchor" disclosure and was charged a
false alarm. But the disclosures were not noise — on a transaction count the model wrote
*"Input anchor is 'transaction' (path-independent)."* It surfaced its assumption **and correctly
declared it immaterial.** The penalty fell on the **medium**: prose has no field for "and this doesn't
matter," so the grader could not tell a model documenting a correctly-judged-immaterial assumption from
a model cluttering. Free text forces: disclose (eat the clutter penalty) or stay silent (risk the
silent failure). There is no way, in prose, to file an assumption *and* mark it benign. This is the
paper's own thesis one level up: the medium, not the reader, is the defect — *disclosing in prose is
disclosing un-filterable noise.*

## The contract

A disclosure is a record with a small, fixed set of fields:

```
{
  "code":        "INPUT_ANCHOR_CHOICE",     // controlled vocabulary (closed list)
  "materiality": "immaterial",              // material | immaterial | unknown   ← load-bearing
  "reason":      "assumption",              // ambiguity | assumption | data_defect
  "assumptions": {                          // structured processing state
      "input_anchor":     "transaction",
      "output_anchor":    ["year"],
      "reducer":          "sum",
      "path_independent": true
  },
  "detail": "free text, for the human only"  // never parsed for scoring
}
```

Four required fields (`code`, `materiality`, `reason`, `assumptions`) plus a human-only `detail`. The
addition that does the work is **`materiality`** — derivable from `assumptions.path_independent`, but
named explicitly so a consumer can act on it without re-deriving.

## Why materiality changes everything

**1. It dissolves the false binary.** With a materiality field, a model can surface *everything* and let
the consumer filter. The layer / UI / agent shows `material` disclosures to the human and files
`immaterial` ones for audit. Completeness is no longer punished, because structure makes it filterable.

**2. It makes "good disclosure" a clean, materiality-aware scoring rule** (replaces the prose-matching
detector for the structured case):

| situation | outcome |
|---|---|
| material disclosure on a path-dependent measure | **SURFACED** (correct) |
| no disclosure on a path-dependent measure | **SILENT** (the real failure) |
| immaterial-flagged disclosure on a path-independent measure | **BENIGN** — filtered, audited, *not* a false alarm |
| material-flagged disclosure on a path-independent measure | **MATERIALITY-MISJUDGMENT** — a new, gradeable error |

The fourth row is the prize: the competence the two-anchor theory actually cares about — *surface the
anchor only when path-dependence makes it live* — becomes a directly measurable field
(`materiality` declared vs. true), not an inference from whether prose happened to appear.

**3. It nearly removes the judge.** benchmark_v2's detector does fuzzy key-term matching + a judge for
adequacy *because it reads prose.* With structured disclosure, "did it surface the anchor" is a field
read (`assumptions.input_anchor` vs. the key) and "was it adequate" is `materiality` + the declared
anchor against the contested dimension. The κ-calibrated judge step shrinks to near-zero.

## Forks

**Fork A — who sets materiality. [DECIDED: both; the gap is itself scored.]**
*Model-declared* (`materiality`/`path_independent` asserted by the model) is what makes it a competence
test. *Scorer-verified* (the framework knows the reducer and checks) is what makes it trustworthy. Use
both: the model declares, the scorer checks, and a **mismatch is a scored outcome**
(MATERIALITY-MISJUDGMENT). This is also the honest division of labor from the paper — the model
proposes, the verifiable layer checks.

**Fork B — the code vocabulary must be closed. [DECIDED: small controlled list.]**
`code` is a fixed enumeration (the contested dimensions: input-anchor choice, denominator population,
stock reading, distinct grain, weighting grain, extremum grain; plus data-quality codes: incomplete,
conflicting, unattested). An open string field reintroduces the unstandardized-name problem one level
up — the exact thing the paper indicts. Free expression lives only in `detail`, which is never scored.

**Fork C — disclosure vs. clarify.** A disclosure with `materiality: material` and a *served* value is
"served-and-disclosed"; the same contested dimension with no served value is a clarify. The contract
above covers served disclosures; clarify remains a separate answer kind that names the same `code`.

## What this touches

- **Benchmark answer contract.** The single-shot contract's `annotations: []` (free strings) becomes
  `disclosures: [<structured record>]`. Test-takers emit structure, not prose.
- **The detector (`benchmark_v2/detector.py`).** For structured answers, disclosure detection becomes a
  field read; the prose matcher stays only as a fallback for models that emit free text. The
  adequacy-judge queue shrinks to materiality-mismatch review.
- **The scorer.** Gains the four-way materiality-aware rule; "false alarm" is recharacterized — an
  immaterial-flagged disclosure is benign, a *mis-flagged* one is the real error.
- **The paper.** This is the operational form of §8's "structured beats unstructured": the disclosure
  itself, not just the metric definition, must be structured to be filterable and checkable. Candidate
  one-paragraph addition or a short companion note ("structured disclosure"): the consumer filters by
  materiality for display while retaining all of it for provenance; the model is no longer punished for
  completeness.

## The validation already in hand

The Haiku comparison is the demonstration: under the materiality-aware rule, its 30 "false alarms" on
path-independent measures are mostly **benign** (it flagged them immaterial / path-independent), so the
−0.055 trust penalty the prose grader manufactured largely disappears and the run reads as what it was —
**silent failures halved, no real over-disclosure.** Re-grade (next) quantifies the flip on data we
already have.
