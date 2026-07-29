# WP-GRAIN-1 — composite input anchor (`@ {a*b}`)

*proposal · v0.1 · 2026-07-29 · headline of 0.13.4 (CLI-renumbered from a would-be 0.13.4)*

## The one-sentence WP

Lift the **single-level restriction on inline-reduction input anchors** — `@ {a*b}` and `@ {a,b}`
parse wherever `AT {…}` already does; the engine's `REDUCE` receives a composite `input_grain`; the
two-stage-statistic disclosure generalizes across the pin × output-anchor lattice; the ask
`SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}` **serves** with the transport reading
named, instead of failing at the parser.

**Acceptance test:** the F1 exhibit (Attack B unfaithful IR) becomes an ASK-surface transcript that
serves — same numbers as `attack_b_ir.json`, but reached through the shipped grammar rather than
below it.

**Ship as 0.13.4's headline** (`columna` 0.13.4 · `columna-core` 0.13.4 · `columna-server` 0.9.0). The
CLI renumber is the honest read: this changes what a stranger can ASK, which is the surface the
version number measures.

---

## Why this is small code and important doctrine

**The engine is already there.** Beat 1 attested it, in production: `ColumnEngine.resolve` +
`ColumnEngine.reduce_series_to_anchor` (`engine.py:598`) executed the F1 composition through the IR,
engine unmodified. The docstring already reads *"keyed by `input_grain` (a tuple of levels)"*. The
planner already constructs a composite grain internally — `input_grain = (pinned,) + orthogonal`
(`planner.py:1103`) — and joins/reduces across it. F1's "single-level restriction" is **one
parser refusal** at `planner.py:377`:

> `"A braced product @ {a*b} is refused for now — single-level input anchors this build"`

That is the whole barrier at the ask surface. The engine below it is composite-grain-native.

**But the doctrine is not.** F1's ruling (Huayin, 2026-07-27) said the ask surface's job is to make
underdetermined statistics unaskable — *"unfaithfulness lives only in the gap between a plan and an
ask"*. Lifting the restriction opens a two-stage statistic (`sum` then `mean`, at distinct grains)
to the surface as **one atomic ask**. That is correct — an expressible pinned ask is its own
denotation, so it cannot be unfaithful to itself — but it means every combination of
(pinned-input-grain × output-anchor) is now askable, and each one has its own lawful shape and its
own possible refusal. Those laws have to be stated, not discovered case by case.

---

## The pin × output-anchor lattice, level by level

Let `P = (p₁, …, pₙ)` be the pinned input anchor and `A = (a₁, …, aₘ)` the output anchor. Each level
sits in a lattice under **functional reachability** (`find_path`), the same lattice
`_split_dependent_targets` already uses at the output.

For every pair `(p, a) ∈ P × A`, exactly one of five relations holds:

| relation | how it reads at the wire | handling |
|---|---|---|
| **same** `p == a` | *"pin fixes this coordinate, output stands at it"* | present in `input_grain` and `target` — group-by axis (already: `present`/`_transport_attach`) |
| **finer** `p → a` (`p` reaches `a`, `p ≠ a`) | *"resolve at `p`, then reduce along the `p→a` transport"* | reduction axis (already: `reduce_series_to_anchor` transports `src` to `rt`) |
| **coarser** `a → p` (`a` reaches `p`, `p ≠ a`) | ⚠️ **refusable** — a coarser pin cannot reach a finer output | see law 1 below (new reason `pin_coarser_than_output`) |
| **orthogonal** (no path either way) | *"pin's axis is collapsed by the reducer to grand total for that axis while `a` is joined into the frame"* | already handled: `orthogonal = tuple(t ... if find_path({pinned}, t) is None)` — generalizes trivially |
| **face-crossing** `p` and `a` are joined only by a RELATE FACE (touch / primary / split / alloc / assign) | *"the pin's transport crosses a face — the statistic is face-defined"* | see law 3 below |

### Law 1 — no coarser-than-output level in `P` (**refuse**, `pin_coarser_than_output`)

If any `p ∈ P` is functionally REACHED by some `a ∈ A` (i.e. `a → p`), that `p` pins a grain coarser
than what the output asks for; the pinned resolution cannot serve the output without inventing
finer rows. Refuse, name the offending pair, and offer the two lawful edits:

```
Refusal("pin_coarser_than_output",
  f"pin '{p}' is COARSER than output level '{a}' — the pin fixes a grain that cannot resolve "
  f"at the output's grain (a coarser pin cannot serve a finer output, so the reduced value at "
  f"'{a}' would be inventing rows the pin does not distinguish); either replace '{p}' with a "
  f"level finer than or equal to '{a}', or drop it if another pin already reaches '{a}'",
  measure=..., target=_fmt_anchor(A),
  alternatives=(f"replace @ {{...{p}...}} with a level finer than '{a}'",
                f"drop '{p}' from the pin (another pin reaches '{a}')"))
```

Same geometry as the existing `out_of_universe` refusal in `reduce_series_to_anchor:614` (which
fires when a target is unreachable from the input grain during execution), but a **distinct
dimension**: this one is about the *pin* choosing an ill-fitting grain relative to the *output*,
not about a plan discovering unreachability at run-time. Per OF-1's standing rule (**one reason
per contested dimension**, 2026-07-14), that dimension mints its own reason and its own
pin-specific teaching message. The check runs statically at the planner chokepoint, before
execution.

### Law 2 — no two levels in `P` are cross-comparable (**refuse**, `redundant_pin` sibling to `ambiguous_grain`)

If `p_i → p_j` for some `i ≠ j`, `p_i` functionally determines `p_j`, so `p_j` pins no additional
grain — the reader will read the pair as fixing two axes when it fixes only one. Refuse for clarity,
not for safety (the numbers would agree with just `p_i` alone):

```
Refusal("redundant_pin",
  f"pin includes both '{p_j}' and '{p_i}', but '{p_i}' functionally determines '{p_j}' "
  f"(a finer level fixes a coarser one) — the pair fixes one axis, not two; "
  f"write @ {{{...without p_j...}}} alone",
  discriminator=AMBIGUOUS,
  alternatives=(f"pin @ {{{fine_only}}} (the finer level)",
                f"pin @ {{{coarse_only}}} (the coarser level — a different denotation)"))
```

Rides an existing discriminator (`AMBIGUOUS` → CLARIFY), a new reason `redundant_pin`. It is a
CLARIFY not a REFUSE by the OF-1 rule (*one reason per contested dimension*, minted 2026-07-14) —
the reader is picking between two admissible pins, not being told the pin is impossible.

### Law 3 — face-crossing at the pin propagates the FACE caveat (**serve with disclosure**, not refuse)

If `p` and `a` are connected only through a face edge — `p = product`, `a = category.touch` — the
pin's transport crosses a face. This is a **face-defined statistic**, the same class the existing
`ColumnEngine.serve_touch_crossing` handles at the output side (`engine.py:443`). The reading is
lawful; the caveat is material and CRITICAL — inform-and-serve, never withheld (`Caveat.CRITICAL`,
ADR-020):

```
Caveat(CRITICAL,
  f"'{reading}' crosses face '{face}' on RELATE '{p}<->{a}' at the pin — the sum of the "
  f"reduced values at the output does not equal the grand total; the crossing is denotational",
  source=f"{p}--{face}-->{a}")
```

This uses the existing `TRANSPORT`/`CRITICAL` caveat kinds — nothing new is minted. The doctrine
piece is that **face-crossing propagates to the pin**, not only to the output; F1's threat model is
a searcher assembling composite pins, and the wire has to carry the caveat at whichever end the
crossing occurs.

### Law 4 — the two-stage-statistic disclosure, generalized (**serve with `TRANSPORT`**, always)

The existing pinned-single-level path already emits an immaterial `TRANSPORT` caveat (OF-2's
ruling, 2026-07-14 — "explicit pin is the reader's own; owes only the immaterial provenance note").
It renders the reading as:

```
"'mean of revenue.sum@day' reduced to cal.month — the mean of revenue.sum@day reading
 (input anchor pinned to 'day'), not the pooled value at cal.month"
```

**Generalization: the pin renders as `{a*b}` (or `{a,b}`, matching the input syntax), and the
"pinned to" clause names the composite:**

```
"'mean of revenue.sum@{store*product*cal.month}' reduced to cal.month — the mean of
 revenue.sum@{store*product*cal.month} reading (input anchor pinned to '{store*product*cal.month}'),
 not the pooled value at cal.month"
```

**Rider — when the pin includes an axis PRESENT in the output (`same` case), the note names it as
the fixed axis rather than a collapsed one**, so a reader sees which coordinate the pin is fixing
and which it is reducing over:

```
"'mean of revenue.sum@{store*product*cal.month}' reduced to cal.month — pin fixes cal.month
 (the output's own axis), reduces over store, product"
```

That is one added sentence in `_resolve_inline_reduction`; the semantics are unchanged.

## What the F1 transcript looks like after this ships

```
SELECT avg(revenue @ {store*product*cal.month}) AT {cal.month}
```

serves with:

- values = `attack_b_ir.json.unfaithful_ir.values` verbatim (2024-01: 164.0284…, …)
- outcome = `disclose`
- caveat (immaterial `provenance`/`TRANSPORT`):
  *"'mean of revenue.sum@{store\*product\*cal.month}' reduced to cal.month — pin fixes cal.month,
  reduces over store, product"*

The **faithful** ask — `SELECT avg(revenue @ {customer*store*product*day}) AT {cal.month}` — serves
with the same disclosure and the values from `faithful_ir` (2024-01: 139.9143…, …). The **21%
difference** between the two answers is now expressible **as two well-formed asks that disagree**,
where before it was expressible only as an unfaithful plan hiding under a well-formed ask. That is
what F1 ruled the surface owes the reader.

---

## The scope, precisely

| in scope | out of scope |
|---|---|
| lift `_convert_input_anchor`'s multi-level refusal (`planner.py:377`) | changing the engine's transport machinery (already composite-grain-native) |
| generalize `_reduction_call` to return `pinned: tuple` instead of `pinned: str \| None` | UNPINNED inline reduction (still refuses via `_unpinned_reduction_refusal`) |
| generalize `_infer` and `_resolve_inline_reduction` (`planner.py:874, 1095`) to accept the composite pin (both are ~4-line edits — the composite is already assembled internally) | changing the wire schema — `contract_version` STAYS `"1"` (`disclosure_wire.py` untouched) |
| add laws 1–3 as static planner checks — refusals classified at the existing chokepoints | lifting the restriction on SCAN input anchors (`_scan_call` — separate WP if wanted) |
| generalize the TRANSPORT-caveat rendering (law 4) | the composite input × faced output combinatorics beyond the natural extension of `serve_touch_crossing` (rowed as a future finding if a real case arrives) |

**Wire contract:** unchanged. `contract_version = "1"`. Two new reasons —
`pin_coarser_than_output` (Law 1, REFUSE/`out_of_universe`-family) and `redundant_pin` (Law 2,
CLARIFY/`AMBIGUOUS`-family) — sit inside the existing `REASON_OUTCOME` shape and follow the OF-1
pattern (**one reason per contested dimension**). Adding a reason code does not bump
`contract_version`: the envelope shape is unchanged; readers on `"1"` see the new reasons as
opaque strings and route them by outcome as they already do.

---

## Acceptance criteria (a spec is a promise; make it checkable)

1. **F1 ASK-surface transcript serves.** Both queries from `attack_b.py:127-128` return
   `outcome = disclose`, values byte-equal to `attack_b_ir.json` on the corresponding IR row, and
   carry the TRANSPORT caveat rendered per law 4. This is the headline test.
2. **Law 1 test:** `avg(revenue @ {cal.month}) AT {store*day}` refuses with
   `pin_coarser_than_output` naming `cal.month` (coarser than `day`), with the pin-specific
   teaching message and two alternatives (replace `cal.month`, or drop it).
3. **Law 2 test:** `avg(revenue @ {day*cal.month}) AT {cal.month}` clarifies with `redundant_pin`,
   alternatives offering `@{day}` and `@{cal.month}`.
4. **Law 3 test:** `sum(revenue @ {product*category.touch}) AT {category.touch}` serves with the
   face-crossing CRITICAL caveat (`b_anchor_crossing` — existing).
5. **Law 4 rendering test:** a hermetic golden of the generalized `TRANSPORT` caveat text under all
   four surface variants (`{a*b}`, `{a,b}`, single-level `{a}` regression, orthogonal-pin case).
6. **Existing suite passes byte-identical** on the single-level path — no regression on
   `avg(aov@day)` etc., which is a subset of the composite grammar (`n = 1`).
7. **Wire schema unchanged.** `contract_version == "1"`; the JSON envelope diff on the golden
   transcripts is exactly (added caveat text, added values), nothing else.

---

## The recall-ledger interim, until this ships

The current restriction — *"an inline reduction's input anchor pins one level, not a product of
levels"* — is a **published recall gap** while WP-GRAIN-1 is in flight, not an implementation detail.
See the row minted on the site's recall ledger (`apps/website/src/components/PrecisionRecallFigure.astro`)
and OF-25 in `specs/open_forks.md`.

The public form: *"composite input anchor"* — three words, sits between `OF-13` and `P1 alignment` on
the figure. Struck the release after 0.13.4 ships and passes the acceptance criteria above.

## The row, if 0.13.4 is delayed

If WP-GRAIN-1 is not the 0.13.4 headline (queue pressure, a scope question surfacing after review),
the recall-ledger row STAYS and the ledger tells the truth about what does not yet serve. **A recall
gap is not embarrassing; a hidden recall gap is.** The row goes down when the code goes up, and
neither before nor separately.
