# MAP-2 · Beat 3 — the two seams (report v0.1)
### C3, the vertical seam · the DuckDB inheritance, the horizontal seam

*CC to desk/ratifier, 2026-08-01. Executes the beat-3 charter (`map2_beat3_charter_v0_1.md`). Both
experiments complete; one surprise, characterized (not a drift specimen). Run:*
```
python specs/open_planner/map2/pilot_c3.py     specs/open_planner/map2/          # Experiment A
DUCKDB_CONSUMER_PYTHON=<ddb113>/bin/python \
  python specs/open_planner/map2/emit_b_duckdb.py specs/open_planner/map2/       # Experiment B
```

## Experiment A — C3, the CROSS-bearing pilot (the vertical seam) · ACCEPTED

**Ask (desk-approved):** `SELECT revenue AT {category.touch}`. The plan splits:
- **Home (stay-home CROSS):** revenue delivered to product, join-multiplied through the
  `product_categories` bridge (touch — multi-counted), the `multi_counted` disclosure minted. This is
  the crossed intermediate — the home→substrate handoff.
- **Substrate (lowered REDUCE):** an `AggregateRel[sum]` over the handoff → category, executed on Acero.

| criterion | result |
|---|---|
| **A-1** conservation-clean end to end | **PASS** — final 12/12 vs the all-home oracle **and** handoff 870/870 vs an independent reconstruction; **N = 882** |
| **A-1** two seam break modes (each MUST fail) | **VALID** — (i) wrong-grain intermediate and (ii) dropped-rows-pre-sum each fail on every cell |
| **A-3** split *verified*, not asserted | **TRUE** — the substrate Substrait plan is `['aggregate','read']` only: **0 JoinRel, 1 ReadRel** — the bridge never left home (check attached in the cert's `M4.a3_split_verification`) |
| **A-4** disclosure survives the seam | **TRUE** — `multi_counted` minted at home reaches the final answer though the sum ran on Acero |
| **A-2** S7's first exhibit | **filed** — `face_spends: [{face_id: product<->category:touch, scheme: touch, conservation_claim: multi_counted…}]` |
| certificate | `fixtures/c3_plan_certificate_v0_2.json` — v0.2-conformant, V3 semantic channel byte-identical, S9 tags the CROSS `stay_home` |

**A-4 stretch (optional, attempted — PASSES):** `SELECT revenue AT {category.split}` (the alloc face). The
reconciliation badge **survives the seam**: the substrate's crossed total reconciles to the base total,
`delta 2.3e-9` (2,212,391.86 either way), and matches the engine oracle 12/12. Conservation arithmetic
across the home/substrate boundary — the hardest honest test — holds. (`fixtures/c3_split_stretch.json`.)

**The measured boundary (filed on OF-26).** The vertical seam is necessarily minimal, and this is a
finding, not a limitation of the pilot: **a single faced coordinate is the maximal expressible CROSS
seam at v1.** Every richer shape refuses `chained_crossing` (G4) — a second anchor dimension beside a
faced coord *and* a composite input pin under a faced output. So the lowered half is the sum around the
home CROSS; a lowered *transport* can't ride with a cross until chained-crossing licensing ships (future
WP; the handoff wall forbids an improvised transport). Filed as OF-26's measured edge.

## Experiment B — the DuckDB second-consumer inheritance (the horizontal seam) · 2/2 TRANSFER

Consumer venv `duckdb==1.1.3` + substrait extension `be71387` (the BLOCK-1-correction proof made
standing, `duckdb_consumer.py`; study venv only). Same ibis-substrait plans, same D3 harness, consumer
swapped.

**B-1 — the verdict matrix (2 rules × DuckDB), no third state:**

| rule | verdict | DuckDB worst \|Δ\| | new backend-band cert |
|---|---|---|---|
| `c1-transport-shaped-sum` | **PASS-with-new-certificate** | 4.4e-11 | `rule_c1_…__duckdb.json` |
| `c2-reduce-mean-decomposition` | **PASS-with-new-certificate** | 9.1e-13 | `rule_c2_…__duckdb.json` |

**Both rules transfer.** No drift specimen — both live in territory the engines agree on (monoid sum,
the (sum,count) mean decomposition are core relational algebra); drift risk concentrates where D1's
NOT-LOWERABLE verdicts already sit (sketch-distinct, exact median/mode), untested here by construction.

**B-2 — band mechanics (first evidence).** Each new cert carries DuckDB's band `>=1.1,<1.2 + ext be71387`
and is **identity-addressed by (rule × band × perimeter)** — so the DuckDB cert has the *same rule_id* as
the Acero cert but a **different digest** (`02ed755e…`→`9e0f68d1…` for sum; `99afe22f…`→`51d92995…` for
mean). Band width is the schema-v0.3 question: each band currently carries exactly one tested version;
widening is unproven, and a re-proof trigger is a tested_version outside the band.

**B-3 — inheritance economics (the amortization's first datum).** Consumer #2 certified in **~0.2 s of
wall-clock per rule** over the SAME plans and the SAME harness — a harness run, not a connector project.
Steps: pin the venv · register 2 base views · `from_substrait(plan)` per rule · oracle-compare · mint the
band cert. Consumer #1 (Acero) was the pilot *build*; consumer #2 reused all of it.

## The surprise, characterized (charter §5 — no uncharacterized refusals)

B-1's mean cell first came back REFUSED — and it was **not a drift specimen.** The plan bytes are
identical to a smoke that passed, and re-execution is clean 4/4 (21 rows, worst 1.8e-12). Root cause: a
**transient DuckDB substrait-extension flake** (`call stack is not deep enough`, from the extension's use
of `inspect.currentframe`) that surfaces intermittently under subprocess invocation on the mean plan; the
same bytes execute cleanly on retry. Handled with a bounded retry in `duckdb_consumer.py` — a harness
robustness fix, **not** a tolerance relaxation and **not** masking a drift (a wrong number or unsupported
function is deterministic and survives every retry). Rowed in D5.

## D5 rows (beat 3, dated 2026-08-01)

| id | kind | row |
|---|---|---|
| **B3-1** | measured boundary (→ OF-26) | a single faced coordinate is the maximal expressible CROSS seam at v1; richer shapes refuse `chained_crossing` (G4). A lowered transport under a cross needs chained-crossing licensing (future WP) |
| **B3-2** | harness flake (fixed) | DuckDB substrait ext `be71387` transient `call stack is not deep enough` (`inspect.currentframe`) on the mean plan under subprocess; deterministic-clean on retry; bounded retry added. Not drift |
| **B3-3** | deployment question (rowed) | the `duckdb==1.1.3` consumer pin is a STUDY venv only; the version skew vs the image's 1.5.5 is a MAP-2(a) deployment question, not solved here |
| **B3-4** | band width (→ schema v0.3) | rule-cert bands each carry one tested version; band width + re-proof triggers are unproven — first evidence filed for schema v0.3 |
| **B3-5** | no-drift-specimen (information) | both rules transferred; drift risk concentrates at D1's NOT-LOWERABLE verdicts, not the monoid/decomposable core |

## Acceptance (charter §4)

1. **C3's certificate** exists, v0.2-conformant native emission; A-1..A-4 satisfied; the alloc stretch
   passed too. ✔
2. **B's verdict matrix** exists — 2 rules × DuckDB, both PASS-with-new-certificate, no third state. ✔
3. **Schema v0.3 inputs** ready: S7's settled shape (touch face_spend exhibit) + band-mechanics evidence
   (the desk cuts v0.3 on these). ✔ (inputs; the cut is the desk's)
4. **D5 rows** filed (above). ✔
5. **Fold to fork doc v0.13** — the desk's. (pending)

Results that count as success without being passes: the measured G4 boundary (A); the characterized flake
(B) — neither an uncharacterized refusal, a widened tolerance, nor an asserted-not-verified split occurred.

*— CC. Both seams accepted by their own verified splits. Over to the desk for schema v0.3 and the v0.13
fold; ratifier for beat-3 closure and the alloc-stretch acknowledgment.*
