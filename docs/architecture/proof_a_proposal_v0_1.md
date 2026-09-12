# Proof A — identity, standing, admission — **implementation proposal v0.1**

**Status:** proposal for authorization, 2026-09-12. **No implementation has begun.** Merging this
file does not authorize the work it describes.
**Success condition:** a governed family identity and its standing survive the passage into retained
material state and return through serving without the physical representation redefining the
meaning — and each neighbouring unlawful case fails **for the right reason, in the right
jurisdiction**.

---

## 1. Forbidden, per instruction

No `compile_v2`, no `.cml`, no legacy planner or engine, no DuckDB persistence, no ADBC, no
realization generator. The realization artifact is **hand-written and read-only**.

One consequence worth stating before it looks like a bug: because Proof A does not use `compile_v2`,
it does not inherit that profile's value-domain table. Its admission check compares a governed
`decimal` against a carrier `decimal128` directly. That is the intended relationship — admission is
where a concrete precision exists to check, which is exactly why the envelope refusal could not live
in the compiler.

## 2. Reused, unchanged (all present today)

| Module | Used for |
|---|---|
| `columna_core.governed.publication` | `parse_publication` — the v2 artifact reader |
| `columna_core.governed.resolve` | `resolve_all` → the total nine-responsibility `Law(F)` view |
| `columna_core.governed.foundation` | the law vocabulary, `sufficient_state`, `empty_fiber`, `has_identity` |
| `columna_core.compiler.realization` | `parse_mapping` / `load_mapping` — reading the hand-written claim |
| `columna_core.compiler.refusals` | the five-category refusal taxonomy |
| `columna_core.operators` | `combine` / monoid metadata for the state basis |
| `columna_core.disclosure` + `disclosure_wire` | the four moods, closed reason registry, `contract_version "5"` |
| `columna_core.types` | the logical dtype vocabulary (with §6's caveat) |
| `packages/columna-core/tests/fixtures_v2/lighthouse*` | the governed publication under test |

Not reused: `parser.py`, `model.py`, `planner.py`, `engine.py`, `adjudication.py`, `connector.py`.

## 3. Files to add

Placement recommendation: a **new top-level package directory**, `packages/columna-platform/`, with
its own `pyproject.toml` but **not** added to the `release-set` lockstep and **not** published.
Rationale: inside `columna-core` it would inherit the PyPI lockstep gates and the published API
surface; outside the repo it would lose the 35-gate harness and the editable-install ergonomics.
A non-published workspace member gets the harness without the release obligation.

```
packages/columna-platform/
  pyproject.toml                      # workspace member; not in LOCKSTEP; not published
  src/columna_platform/
    __init__.py
    carrier.py        # synthetic Arrow carrier construction + introspection (no source, no driver)
    admission.py      # the admission boundary: two checks, both refusing, neither defaulting
    state.py          # RetainedState: analytical identity + standing; insert/retrieve/finalize
    serving.py        # request -> resolve -> admit -> retain -> wire_frame (serve|refuse)
    refusals.py       # want-of-law vs want-of-state, mapped onto existing jurisdictions
  fixtures/
    proof_a/
      private-core-mapping-v2.json    # HAND-WRITTEN. No generator. Read-only.
      carrier-exact.arrow             # decimal128(18,4) — the lawful carrier
      carrier-lossy.arrow             # float64 in place of decimal — negative control 1
  tests/
    test_proof_a_lawful.py
    test_proof_a_negative_controls.py
    test_proof_a_standing_travels.py
```

`carrier-*.arrow` are Arrow IPC files, committed, byte-deterministic — so the proof is reproducible
without a database and the fixtures double as the first admission regression corpus (§5).

## 4. The path

```
lighthouse v2 publication
  → parse_publication            (governed artifact reader, unchanged)
  → resolve_all                  (total Law(F); C6 value_domain = "decimal", C8 = SUM)
  → load_mapping(fixtures/proof_a/private-core-mapping-v2.json)     [READ ONLY]
  → require_same_publication     (binding, before anything else)
  → carrier.load("carrier-exact.arrow")                             [synthetic; no source]
  → admission.admit(law_view, realization, carrier)
        CHECK 1  governed decimal  ⇔  carrier decimal128(p,s) within the 38-digit envelope
        CHECK 2  carrier null      ≠  analytical absence
  → state.insert(RetainedState(identity=(family_id, anchor), standing=…, basis=<runtime state spec>))
        # `basis` is a RUNTIME PROJECTION derived by the governed layer from C7, carried in as
        # execution input — the SSE executes sufficient-state law, it does not re-derive it.
  → serving.serve(request)  → disclosure_wire.wire_frame(...)  → serve | refuse
```

**Lawful case:** `lh-revenue` — primitive, `SUM`-continuing, `grain: coincident`, exact decimal.
Serves, with standing read off the retained state rather than recomputed.

**On the constitution binding.** Proof A binds retained state to the governing constitution standing
using the **constitution fingerprint** available on the v2 artifact's `constitution_authority`. That
is an implementation choice permitted for this proof, not an elevation of the representation: the
contract's invariant is comparability plus conservative invalidation when the comparison scheme
changes, and Proof A should demonstrate the invariant — including at least one assertion that an
incomparable standing does **not** read as agreement.

## 5. Negative controls — measured, not contrived

The Phase 0 fidelity probe produced real failures; using them makes the controls evidence rather
than illustration.

1. **Admission refuses a successfully delivered carrier.** `carrier-lossy.arrow` presents `float64`
   where the governed domain is `decimal`. Delivery succeeds; admission refuses. This is the
   naturally occurring SQLite `REAL` case, which the probe measured collapsing
   `12345678901234.5678 → 12345678901234.568`.
2. **Want-of-law vs want-of-state, distinguishable.** The same family requested at a coarser anchor
   with **no movement licence** → want-of-law (and note the lighthouse fixture publishes movement as
   `unestablished` on purpose, so this control is available today without changing the fixture).
   Then the same request after eviction → want-of-state, carrying that re-realization would resolve
   it. Both refuse; the reasons and jurisdictions must differ.
3. **A finalized scalar offered back as sufficient state** → refused. (Proof C's control, cheap to
   assert here, and it pins `finalize`'s marking from the start.)

Optional fourth, if it costs nothing: **`decimal128(38,0)` at full width** — the probe measured
Arrow carrying it exactly and Polars silently losing the last digits. Admission should refuse at the
Arrow→in-process conversion boundary, which is the empirical reason §Admission's envelope is
*source → driver/configuration → Arrow → in-process carrier conversion* and not merely driver → Arrow.

## 6. Two things Proof A must not quietly inherit

- **`types.py` is substrate-named** — *"the engine is Polars, so the logical types ARE Polars
  dtypes."* Proof A may use the vocabulary, but its admission check must compare against the
  **governed** domain and the **Arrow** type, never against a Polars dtype as the authority. If this
  turns out to require a substrate-independent value-domain vocabulary, that is a finding to report,
  not to invent.
- **Φ is not `empty_fiber`.** Proof A asserts nothing about `FILL`. Core's fill rule answers *what
  does an eligible point with no observed value denote* — a declaration, *"a choice… never a
  consequence"*. `empty_fiber` answers *what does the fold over an empty fiber denote* — entailed
  from the law's algebra. Check 2 concerns the carrier-null distinction only.
- **Entailed facts are projected in, never re-derived.** Per the 2026-09-12 ruling, anything Proof A
  needs that the governed foundation entails — the sufficient-state basis above all — is derived by
  the layer that owns the law and passed in as execution input. If Proof A finds itself importing
  `governed.foundation` to work out *why* a state is sufficient, that is the signal it has taken on
  authority it does not hold, and is a finding to report rather than a shortcut to take.

## 7. What Proof A deliberately does not prove

Governed movement (Proof B), composite sufficient state (Proof C), participation carriage, C1 target
discrimination, realization assertion/attestation/currency ownership, and any persistence. All
remain in the open register.
