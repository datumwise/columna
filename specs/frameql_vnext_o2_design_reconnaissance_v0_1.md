# Frame-QL vNext — O2 Ordered-Expression Design Reconnaissance

**Mission:** O2 successor design reconnaissance · **Authority posture:** reconnaissance only
**Repo state:** `datumwise/columna` @ `bfb3cfe` (`main`, clean) · **Date:** 2026-09-06
**Nothing implemented. No parser, planner, registry, spec, profile, schema, wire, doc or test was edited. No PR.**

Six read-only inspectors plus direct probes of the running engine. Every claim is marked **SV** (read at
file:line) or **VX** (reproduced against the running engine, probe and output shown). Paths are relative
to `packages/columna-core/src/columna_core/` unless stated.

---

# 1. Executive conclusion

**The O2 semantic model can be implemented on current architecture, and it needs exactly one new
execution seam, one new static descriptor and one new resolved carrier. It does not need a new core
expression abstraction, and it does not need full R4.**

That is the good news, and it is load-bearing, so here is the reason rather than the assertion.

**The architecture already has the O2 axes. It has them as an accident of three operator kinds, and one
cell of the resulting 2×2 is empty.** `operators.py:11-14` declares `REDUCER, SCAN, MAP`, and the file's
own comments name both axes:

| | anchor-**preserving** | anchor-**changing** |
|---|---|---|
| order-**independent** | `MAP` — *"point-wise, anchor-preserving"* (`operators.py:14`) | `REDUCER` — ToD family continuation |
| order-**dependent** | `SCAN` — *"order-dependent, anchor-preserving"* (`operators.py:186`) | **∅** |

O2's focal-preserving operators (§9.2 — LAG, LEAD, RANK, cumulative, rolling) are `SCAN`. O2's
peer-collapsing operators (§9.1 — FIRST, LAST landing at a coarser peer anchor `P`) belong in the empty
cell. Because that cell does not exist, `first`/`last` are declared `REDUCER` (`operators.py:166-169`),
and that declaration is what hands them family-founding rights through the gate at `parser.py:686-692`:

```python
if op.kind != REDUCER:
    errs.append(f"measure '{meas.name}': operator '{op_name}' is a {op.kind}, not a reducer
                — only reducers found families …")
```

**So legacy family-founding FIRST/LAST is not a feature anyone chose. It is the side effect of a missing
kind.** This reframes the sequencing: the successor does not have to displace the legacy path, it has to
fill the empty cell — after which the legacy path is a classification question rather than a migration.

**And the "no continuation rights" law already exists and is already correct.** `Operator.re_entrant`
(`operators.py:67`, ruled 2026-09-01) is a fail-closed re-entry certification, consulted for real at
`planner.py:1604`, and `last`/`first` are deliberately **not** certified, with the reason recorded at
`operators.py:104`: *"the witness is (value, order_key), not the finalized value."* O2 §21 —
*availability is not continuation permission* — is therefore **half-implemented**: the declaration exists,
it is right, and it is simply not the predicate guarding family founding. That is a much smaller repair
than writing the law from scratch.

## 1.1 What is genuinely missing, in one sentence each

1. **An order-carrying general series reduction.** Two collapse paths exist and each has half of what the
   successor needs: `_SERIES_REDUCE` (`engine.py:784-790`) is general, non-family and order-**blind**
   (it folds one `_v` column); `_combine_exprs` (`engine.py:764-774`) is order-**aware** (it carries
   `(_value, _order)` and selects by `sort_by("_order").last()`) but is reachable only through family
   founding. **The successor needs their union, and nothing else at the execution layer.**
2. **A peer anchor as a value.** It does not exist. The word *"peer"* does not appear in `columna-core`.
   It is computed by set subtraction on the output anchor at `engine.py:296` and discarded.
3. **A resolved carrier for the completed order contract.** Today the entire contract survives, for scans
   only, as one English sentence inside a caveat detail string (`engine.py:306-308`).

## 1.2 Two current correctness defects found en route

Neither is an O2 design gap; both are shipping behaviour, and both bear on the category-B ruling.

- **A tied `LAST` serves a non-deterministic number, undisclosed** — reproduced three ways
  independently (§7.1). The served value changes with physical row insertion order, and the two
  mechanisms that implement it return **different answers for the same tie set in the same build**.
- **R4-C0 withholds the unplaced row but not its contribution on the ordered path** (§7.2). New as of
  today's merge; the eight R4-C0 regressions never ask an ordered question.

---
# 2. Current ordered implementation map

Five hops. **The artifact between hop 2 and hop 3 is not an AST — it is a list of
`(name, verbatim-expression-string)` pairs** (`planner.py:1297-1301`), and every downstream stage
re-derives a CPython AST from that string and throws it away. There is no structured intermediate
representation anywhere between the envelope parser and the engine call. That single fact governs most
of §4 and all of §6.

```
                     ORDERED REDUCER                          SCAN
                     SELECT level.last AT {store,cal.month}   SELECT cumsum(revenue.sum, by="day") AS c AT {store,day}

1 parse              Statement(series=[Series(expr,alias)], anchor)          same
   envelope.py:78-88 order carried: NOTHING                    order carried: inside the opaque expr string

2 desugar            Planner.desugar  planner.py:846-891       byte-identical Statement
                     a pure TEXT->TEXT transform; adds no      _canon_expr only touches @ {…}
                     resolved fact whatsoever  (VX)

2b render            render_canonical()  envelope.py:90-117    surface `by=` survives only inside expr
                     "SELECT level.last\nAT {store*cal.month}"

3 plan               _engine_columns -> [(name, text)]         _scan_call  planner.py:1865-1929
                     planner.py:1301                            -> transient tuple (op, arg, n, by), DISCARDED
                     FamilyMember.order_by is NEVER read by     plan_order_axis  planner.py:293-367
                     the planner (projection.py:47 strips it)   -> ONE STRING, no direction, no strength
3b law walk          _Travel(op, frm, to, subject, law)         _scan_order_standing calls plan_order_axis
                     planner.py:2091-2095 — frm is the de       AGAIN and throws the axis away, keeping
                     facto sequence anchor, to the de facto     only the refusal (planner.py:1048-1072)
                     result locus. Order key/direction/ties:
                     ABSENT

4 resolved op        engine.resolve cache key =                engine.scan(...) — loose keyword args
                     (measure, member, target, uni, where)     planner.py:2586-2589
                     engine.py:228 — NO ORDER DIMENSION.       There is no object.
                     Two different completed order contracts
                     over one atom alias to ONE memo entry

5 engine             _deliver_and_transport_monoid             ColumnEngine.scan  engine.py:256-310
                     engine.py:311-380                          partition = [d for d in target
                     FIRST AND ONLY appearance of the order                  if d != order_axis]   :296
                     key, at :322-328. arg_max(value,order)     frame.sort(partition+[order_axis]) :297
                     direction decoded from combine=="argmax"   ascending ONLY — no descending scan
                     ties = whatever DuckDB does               scan_impl -> literal 6-entry polars dict
5b combine           _combine_exprs  engine.py:764-774          Caveat(TRANSPORT, "scan cumsum over
                     sort_by("_order").last() — a SECOND,       order 'day' within ['store']")  :306-308
                     different tie mechanism                    <- the ONLY artifact in the whole system
                                                                   that states a completed order contract,
                                                                   and it is a free-text detail string
```

**VX** — the executed wire payload for `level.last` carries `"disclosures": []`. The order key `day` is
named nowhere: not in the trace, not in any disclosure, not in EXPLAIN.

---

# 3. Semantic-field matrix

| O2 semantic field | Current carrier | Reusable? | Gap? | Recommended authority |
|---|---|---|---|---|
| **sequence anchor `I`** | For scans: **≡ output anchor** (`engine.py:256-259`, one anchor parameter). For first/last: **does not exist** — delivery grain derived from the output anchor (`engine.py:313-314`), selection runs over physical **rows** | partial | **YES — the decisive one.** Nearest carrier is `_Travel.frm` (`planner.py:2093`), computed and discarded | resolved ordered expression |
| **peer anchor `P`** | **Nothing.** The word "peer" does not occur in `columna-core`. `partition = [d for d in target if d != order_axis]` (`engine.py:296`), used on 5 lines, never adjudicated, never on the wire except inside English prose | no | **YES** | resolved ordered expression (+ optionally a Manifold declaration — §4.4) |
| **peer projection `π: I→P`** | **Already governed and already exists**: `PlannerView.find_path` over `_out_certified` (`projection.py:214-216, 255-259`), closed by default; lifted to anchor-vs-anchor with refusal codes by `_check_pin_laws` (`planner.py:1499-1546`); an explicit (I, P, π) triple with planner-selected certified routes already runs at `planner.py:2696-2771` → `engine.py:823-874` | **YES — verbatim** | polarity only: `_check_pin_laws` *refuses* the coarser pin a peer would be | existing (no new geometry concept) |
| **order relation** | Three unrelated mechanisms, none of them a relation: scan axis (`plan_order_axis → str`), `FamilyMember.order_by: Optional[str]`, output `OrderKey(column, descending)` | no | **YES** | Manifold declaration **+** CDT comparison **+** request (split forced by code boundaries — §6) |
| **order keys** | A scalar `str` in **both** inner regimes (`planner.py:293`, `model.py:164`) | no | **YES** — no secondary key expressible, so §12.3 ROW_NUMBER is unsatisfiable *by construction* | resolved ordered expression |
| **direction / comparison** | **No field anywhere** on the inner order. Smuggled into operator identity (`combine="argmax"/"argmin"`, `operators.py:166-169`) and into a Polars sort default (`engine.py:297`). Exists only on output `ORDER BY` | no | **YES** — and proven a no-op: on a tie `arg_max` and `arg_min` return the *same row*, so `first` and `last` are the same operation (VX §7.1) | request + resolved expression |
| **order strength / ties** | **Nothing.** `needs_order: bool` is the degenerate form — and it is **inert**, read as a gate by nothing (§7.3) | no | **YES** | operator registry (`OrderedLaw`) for the requirement; resolved artifact for the disclosure |
| **domain-formation rule** | Implicit: WHERE restricts before formation (correct, §19-conformant, VX) plus a **silent** null-operand exclusion spliced into the same SQL WHERE (`engine.py:339-342`) | partial | **YES** — lawful restriction and unlawful shrink arrive on the identical channel and are indistinguishable downstream | resolved ordered expression |
| **operand-standing rule** | **Nothing.** `last` silently *is* `last supported` (§10.2 collapse, VX); `cumsum`/`cummax` implicitly skip an unsupported point and serve the downstream cells as ordinary | no | **YES** | `OrderedLaw` (per operator) |
| **selection / neighbourhood law** | `scan_impl` — a key into a literal 6-entry polars dict (`engine.py:299-301`); `combine` — a key into a 5-way `if` chain (`engine.py:764-774`) | mechanics only | **YES** as a *class* | `OrderedLaw` |
| **result locus** | **Nothing.** `grep -rn locus` over core+server returns zero hits. Locus is positional: `scan` passes `target` through; `resolve` collapses to `target` | no | **YES** | `OrderedLaw` (static per operator) |
| **offset** | `n: int`, default 1 — **the only ordered parameter with a real value shape** (`planner.py:1849-1856` → `engine.py:300-301`) | **YES** | no | operator parameters |
| **window / boundary** | `needs_window: bool` — a *refusal marker*, not bounds. Repo-wide grep for `preceding`/`following`/`ROWS BETWEEN`/`RANGE`: **zero hits** | no | **YES** — there is no ROWS/RANGE distinction to implement against | `OrderedLaw` + request |
| **reset / within** | **No code representation.** Documented as language at `docs/frame_ql_language.md:559-563` | no | **YES** — but O2 §18 is right that peer geometry may absorb it (VX: the MTD reset is reachable today *only* by mutating the output anchor) | peer anchor, per §18 |
| **continuation permission** | **`Operator.re_entrant`** — exists, fail-closed, correctly `False` for first/last, consulted at `planner.py:1604` | **YES — verbatim** | it is simply not the gate at `parser.py:688` | existing |

---
# 4. Recommended successor object model — the smallest clean one

**Three objects, of which two already half-exist. The genuinely new one is a value, not a mechanism.**

The temptation is to build one `OrderedExpression` class mirroring §8. That would be wrong here, because
the evidence shows the fields split cleanly along a boundary the codebase *already enforces*:
`projection.py:56-60` — *"The mechanics (witness/combine/deliver_sql/scan_impl) are resolution and stay
engine-side; the planner never sees them."* Some O2 fields are static per operator (law); some are
resolved per request (domain). Fusing them re-crosses a boundary that took work to draw.

## 4.1 `OrderedLaw` — static, per operator, referenced from `Operator` by ONE field

```
OrderedLaw
   result_locus          peer_collapsing | focal_preserving
   order_strength        total_unique | positional | tie_classes_ok
   selection_class       boundary | relative_offset | prefix | local_window | ordinal
   operand_standing      strict | skip_unsupported          (§7 / §10.2 / §11.2)
   boundary_rule         how the first/last focal point behaves    (§25.2)
```

**Why each field exists — every one replaces a hard-coded branch that exists today:**

| field | what it subsumes | evidence |
|---|---|---|
| `result_locus` | the empty 2×2 cell. `grep -rn locus` over core+server returns **zero hits**; locus is positional today (`scan` passes `target` through, `resolve` collapses to `target`) | §1 |
| `order_strength` | `needs_order: bool` — which is **inert**. It is set on all 8 ordered operators, copied into `OperatorSig` and echoed to the wire, and **read as a gate by nothing** (repo-wide grep). The cost is reproduced: a `FAMILY { last }` with no `ORDER` clause *parses clean, plans clean* (`outcome='serve'`, `refusal=None`) and then **fails at execution** — `ERROR: lv.last needs an ORDER key` (VX). That directly violates the invariant the codebase states at `planner.py:1078-1082`: *"A positive preflight disposition must not be returned when the same build already knows that the admitted request cannot be realized."* | VX |
| `selection_class` | `scan_impl` (a key into a literal 6-entry polars dict, `engine.py:299-301`) and `combine` (a key into a 5-way `if` chain, `engine.py:764-774`) — both implementation tags standing in for a semantic class | SV |
| `operand_standing` | the silent §10.2 collapse. `engine.py:337-342` splices `(<operand>) IS NOT NULL` into the delivery WHERE so `last` *is* `last supported`, with **zero disclosure** (VX). Today "last value" and "last supported value" are the same operator; O2 §10.2 says they must not be | VX |
| `boundary_rule` | the sequence boundary, currently emitted as a **false claim**: `lead`'s final point discloses `('unknown','material')` — *"a value existed but was not recorded"* — in a fully placed, fully supported frame (VX). There is no successor point and no value ever existed | VX |

**Why a separate object rather than five more flat fields on `Operator`:** `Operator` has 13 flat fields
serving three disjoint audiences, and `projection.py:172-174` already copies 10 of them into a parallel
`OperatorSig` via an unreadable positional constructor. An ordered law is **planner-facing law**, so it must
cross the mechanics boundary; adding flat fields forces a matching widening of that constructor.
`ordered: Optional[OrderedLaw]`, copied by reference, adds **one** field to each and keeps the split
intact. It also lets the law be `None` for the operators that have none — a distinction the current scheme
cannot express (today `needs_order=False` on `sum` is indistinguishable from "undeclared").

**Do NOT fold in `re_entrant`, `linear` or `is_monoid`.** `operators.py:70-110` is an explicit ruling that
`re_entrant` is strictly stronger than `is_monoid`, that the default `False` means UNCERTIFIED rather than
false, and that a conditional certification *"must NOT be flattened into True."* A descriptor admitting
partial facets would re-open exactly that. Those three belong to the reduction-algebra axis and have their
own adjudicators. Likewise leave `in_core` out: it is a build fact, not a law.

## 4.2 `OrderedDomain` — resolved, per request. The one genuinely new value

```
OrderedDomain
   I    sequence anchor       tuple of levels
   P    peer anchor           tuple of levels,  I >= P
   pi   peer projection       the planner-selected certified routes I -> P
   O    order specification   ordered list of (order expression, direction), + comparison
   R_D  domain-formation rule what restricted the candidate set (WHERE, exclusions)
```

This is new **as a carrier**, not as a concept. Every ingredient is already governed:

- `I >= P` is `PlannerView.find_path` over `_out_certified` (`projection.py:214-216, 255-259`) —
  closed by default, positively-admitted edges only.
- The anchor-vs-anchor lift already exists with refusal codes: `_check_pin_laws`
  (`planner.py:1499-1546`), Law 1 `pin_coarser_than_output`. **The successor needs the same machinery with
  the polarity inverted** — today it *refuses* the coarser pin that a peer would be.
- `π` as planner-selected certified routes already runs: `planner.py:2740-2748` →
  `engine.py:823-874`, which raises `uncertified_edge` if the planner did not plan a route.

**So `OrderedDomain` introduces no new geometry.** It gives a name and a lifetime to a relation the system
already computes, adjudicates and refuses on — and currently derives positionally and throws away.

## 4.3 `ResolvedOrderedExpression` — the artifact, on the EXPLAIN/resolved path

```
ResolvedOrderedExpression = operand + OrderedDomain + OrderedLaw + parameters
```

**Home: a side artifact on the resolved/EXPLAIN path** (`frameql.py:96-108` already builds a per-series
dict with a `cone` sub-object; an additive sibling key is a pure addition). This was assessed against three
alternatives and it is the only one that is additive:

| home | verdict |
|---|---|
| **(b) EXPLAIN side artifact** | **Chosen.** Nothing breaks. `render_canonical` untouched → round-trip untouched. Reaches a consumer today on the zero-fetch path. Nothing pins its absence |
| (a) canonical AST from `desugar` | **There is no AST.** `desugar` returns a `Statement` whose only series slot is `expr: str`; `run_statement:1308` flattens it to `[(name, text)]` one line later |
| (c) `ColumnResult` / `trace` | `trace` is `list[str]` and is never serialized; `ColumnResult` exists only after run/plan branches, so the contract would not exist for `check_frame_query` |
| (d) surface canonical text | **The canonical form would refuse itself.** VX: `within=` → *"unknown parameter 'within' (accepts n=, by=, window=)"*; and reducers accept **no keywords at all**, so `level.last(by="day")` → *"unsupported expression node Call"*. Serializing the contract requires new grammar; there is no incremental version |

**Round-trip precision that matters** (a correction to M2): the parse/render identity law
(`test_envelope_parser.py:132-136`) binds the **parsed**, pre-desugar `Statement`, not the desugared one.
VX: `parse(desugar(...).render_canonical()) == desugared` is **`False`** at HEAD, because `desugar` sets
`alias='level.last'` while `render_canonical` suppresses `X AS X`. The desugared form round-trips only up to
`desugar∘parse` — which is what `test_envelope_sugars.py:46-49` asserts. So a desugar-introduced field is
constrained by the text-fixed-point law and the EXPLAIN-identity law, **not** by object identity.

## 4.4 The one new execution seam: an order-carrying series reduction

This is the smallest missing abstraction, and it is a **merge of two things that both already exist**:

```
engine.py:784-790   _SERIES_REDUCE   general, non-family, ORDER-BLIND     folds one `_v` column
engine.py:764-774   _combine_exprs   ORDER-AWARE, family-only             carries (_value, _order),
                                                                          selects sort_by("_order").last()
```

`reduce_series_to_anchor` (`engine.py:823-874`) is already a **general I→P collapse**: it takes
`input_grain` (I) explicitly, `target` (P), planner-supplied certified routes (π), and — verified directly —
**gates only on `member not in self._SERIES_REDUCE`. It never consults `Operator.kind`, `witness`,
`combine`, or the family.** `parser.py:686-692` is not on this path. VX:
`SELECT max(onhand.sum @ {store, day}) AS L AT {store}` serves an anchor-changing result at P with no
family standing minted.

So the seam is: **extend the resolved-series contract from `(_v)` to `(_v, _order)` and admit a
*selection* vocabulary beside the *fold* vocabulary.** Note `_transport_reduce` (`engine.py:869-873`)
already excludes `("_value","_order")` from its group keys — the `_order` column concept exists, on the
other path.

That is one column, one vocabulary set, one planner gate (`_inline_reducer`'s allowlist). It does **not**
touch `Operator.kind`, `parser.py:686-692`, the B-anchor crossing gate, or `witness` dispatch — which is
precisely the O2-I7 separation ("anchor-changing is not enough to make an operation a reducer"). And it
fixes a defect on the way: an order column forces the fiber to be a set of **I-points** rather than a set of
**rows**, which is the root of the non-determinism in §7.1.

---

# 5. Operator mapping

| operator | locus | order strength | selection class | representable in the model? | status today |
|---|---|---|---|---|---|
| `FIRST` / `LAST` | peer_collapsing | total_unique | boundary | yes | **exists, mis-kinded as REDUCER**; reachable only as a member spelling |
| `LAG` / `LEAD` | focal_preserving | positional | relative_offset | yes | **exists**, executes; `n:int` is the one real parameter |
| `CUMSUM` (+`cummax`,`cummin`,`pct_change`) | focal_preserving | positional | prefix | yes | **exists**, executes; `n=` silently accepted and **ignored** for cum* (VX) |
| `RANK` / `DENSE_RANK` | focal_preserving | tie_classes_ok | ordinal | yes | **absent from the registry**; canonical noun only |
| `ROW_NUMBER` | focal_preserving | total_unique | ordinal | yes — *and the model explains why it is unsatisfiable today*: no secondary key can be expressed | **absent from the registry** |
| `rolling` positional | focal_preserving | positional | local_window(positional) | yes | **contract only** — REALIZATION refusal |
| `rolling` range | focal_preserving | positional | local_window(range) | yes | **contract only, and unrepresentable**: zero `preceding`/`following`/ROWS/RANGE hits repo-wide; the only spelling that gestures at it, `window=7d`, does not even lex (`ast.parse` → `SyntaxError`) |

**Three-authority disagreement, and the gate cannot see it.** Eight operators — `cumprod`, `ewm_mean`,
`rolling_min`, `rolling_max`, `rolling_count`, `rank`, `dense_rank`, `row_number` — exist in the canonical
capability TOML and in the published Manual's Appendix A, and in **no other layer**: not the runtime
registry, not either profile, not the build. They are **language-only nouns**. And
`capability_authority.py` reports `build deltas: 0` for them, because a capability absent from the registry
measures `none`, a canonical capability with no profile row defaults to `none`, and `none == none` is not a
delta (`capability_authority.py:98-140`). A ratified-in-prose operator that no layer realizes is
structurally invisible to the conformance gate.

---
# 6. Required authority additions — the governed facts that are genuinely missing

Separated as the mission asks. The split is **forced by existing code boundaries**, not chosen by taste.

## 6.1 Manifold logical declaration

**A1 · Order standing that is not a lineage-NAME match.** This is the load-bearing gap.
```python
TEMPORAL_LINEAGES = frozenset({"calendar", "fiscal"})        # projection.py:223
def orderable_levels(self): ...                              # projection.py:225-235
```
**Governed order standing in this system is a hardcoded match on the author's chosen lineage name string.**
A level is orderable iff it happens to sit on a lineage someone spelled `calendar` or `fiscal`. Nothing
about the level's values, type or any declared comparison enters. Rename `HIERARCHY calendar` to
`HIERARCHY cal` and order silently disappears from the entire model.

The build knows this is provisional and says so in-tree (`planner.py:320-327`): *"a temporal level is 'one
common source of governed order, not the definition of order', so that set may later widen. Widening it
means declaring a NEW SOURCE of order standing, which is declaration law and not this repair's to invent."*
That is the ruling this mission surfaces as due. **The answer is not to add lineage names to the set** —
that keeps name-matching as the definition of order, which is what O2 §4 rejects.

Doctrine to retire alongside it: `docs/frame_ql_language.md:977` still teaches *"derived from the input
anchor when the anchor contains an axis with a **natural order** (typically a temporal axis)"* — the exact
inference O2 forbids. It is currently the accurate description of the implementation.

**A2 · Governance parity between the two order regimes.** `FamilyMember.order_by` is validated by
**nothing** and is invisible to the planner: `MeasureShape.family` is *"member NAMES only — no order_by"*
(`projection.py:47`). Reproduced:

```
FAMILY { last ORDER day  }  -> publishes, serves
FAMILY { last ORDER region } -> publishes, serves     <- non-temporal, ZERO governed order standing
FAMILY { last ORDER txid  }  -> publishes, serves     <- ditto
FAMILY { last ORDER stock }  -> publishes, then KeyError-as-"unsupported"
FAMILY { last ORDER zzz   }  -> publishes, then KeyError-as-"unsupported"
```
Meanwhile `cumsum(..., by='region')` is **refused** `order_not_governed`. Two regimes, two governance
standards, opposite verdicts on the same level. The projection must stop stripping the order key before any
other repair here can bind. The K0 compiler already records the same hole from the other side
(`compiler/compile.py:62-65`).

## 6.2 CDT comparison capability

**A3 · A type, and a comparison, on a coordinate.** `DimensionLevel` is
`(name, realized_by, is_base, description, rejects, attributes)` — **levels have no dtype at all**
(`model.py:70-78`), and the `LEVEL` grammar has no type slot (`parser.py:230`). `types.ORDERED`
(`types.py:40`) is an operator *accept-set* over **measure** dtypes with no operations, no direction, no
collation, no `<=` law — and `first`/`last` do not even use it (`accepts=ANY`). A repo-wide search for a
declared comparison capability returns only `model.Comparison`, the universe-predicate WHERE filter.

**Without A3, A1 can only ever be a hand-maintained allow-list — i.e. the current design with a different
literal.** A relation needs a comparison; the type layer is where a comparison lives; it has none, and the
things being ordered are not typed.

The repo already records this gap independently:
`specs/measure_algebra_finding_2_typed_values_and_state_v0_2.md:259` — *"The order key's own type does not
exist: `DimensionLevel` has no dtype field."*

## 6.3 Frame-QL request / resolved expression

**A4 · Direction on the inner order.** Exists only on the output `ORDER BY`
(`OrderKey(column, descending)`). For the inner order it is smuggled into operator identity — and
**proven a no-op**: on a tie, DuckDB's `arg_max` and `arg_min` return the *same row*, so on the delivery
path `first` and `last` are the same operation (VX §7.1). Direction is per-expression (`day ASC` and
`day DESC` over one declared level are both lawful), so it cannot live in the Manifold.

**A5 · Order key as a sequence.** Scalar `str` in both regimes. No secondary key ⇒ §12.3's governed
secondary ordering for `ROW_NUMBER` is unexpressible **by construction**.

**A6 · The peer anchor as a value** (§4.2), and **A7 · a resolved carrier for the completed contract**
(§4.3). Today the whole contract survives, for scans only, as one English sentence in a caveat detail
string; ordered *reducers* emit `"disclosures": []`.

## 6.4 Operator registry (an existing authority)

**A8 · Operator-relative required order strength** — `OrderedLaw.order_strength`, replacing the inert
`needs_order` bool. Prerequisite: the capability TOML deliberately holds `needs_order`/`needs_window` out
*"pending a ruling"* (`specs/frameql_capabilities.toml:41-44`), so that ruling gates this.

**A9 · A tie rule, vocabulary and refusal code.** None exist for ordered expressions — **and the precedent
does, already shipped, in a neighbouring authority.** `FACE ... ASSIGN BY <driver> ORDER MIN|MAX`
(`parser.py:305-318`) makes direction **mandatory with no default**, for a reason recorded in the source:
*"A silent default would be an unrecorded resolution — the precise sin."* And a tie **fails closed at
publish, naming the tied members** (`adjudication.py:700-709`). That is exactly the shape O2 §16/§17 asks
for. It exists, it works, and it has never been pointed at the ordered-expression layer.

**A10 · Window bounds and the ROWS/RANGE distinction.** `needs_window: bool` is a presence marker; the
value is never read (VX: `window=7` and `window='7d'` produce byte-identical refusals). Zero
`preceding`/`following`/`ROWS BETWEEN`/`RANGE` hits anywhere in the tree.

## 6.5 Profile / runtime realization

`rolling_sum`/`rolling_mean` are contract-only at `level="plan"`; `platform_profile.toml` is
`extends="core", adds=[]`, so every profile answer is Core's. `rank`/`dense_rank`/`row_number` are absent
from the registry entirely. Nothing here blocks the design; it is the honest inventory of what a first
slice may not claim.

---

# 7. Standing blockers — what can be built truthfully before full R4

**Almost nothing here is blocked on R4.** O2 §5 requires only that *"the loss remain visible"* — refusal,
disclosure, or a governed partial-result policy. Disclosure-strength satisfies §5, and the build already has
the channels.

**Achievable before R4:** the determinate cases for FIRST/LAST and LAG (VX controls pass today); "terminal
point known, operand unsupported → result unsupported" (the condition is fully observable in the carrier —
`value IS NULL` at `max(order_key)` — and the Φ/`unknown` channel already exists to carry it); "peer
placement unsupported → do not drop silently" (**already met** post-R4-C0 for FIRST/LAST, because there
P coincides with the output anchor); "order key unsupported → do not drop silently" at disclosure strength
(the count is observable at domain formation with one carrier read); the LAG boundary case; the cumulative
prefix's implicit skip.

**Blocked on R4:** exactly one thing — the *positive* judgment *"this point participates in the ordered
domain, its position is unestablished, therefore the result is unestablished"*, as distinct from *"N points
were withheld, count disclosed."* There is no per-point standing carrier anywhere, and R4-C0 explicitly
declined to build one.

**Blocked on something that is not R4** (do not mistake these for standing gaps): the invalid-peer-anchor
case cannot be *stated*, so it cannot be judged; the tie cases need A4/A5/A9; direction needs A4;
`RANK`/`ROW_NUMBER` are simply absent.

## 7.1 Defect — a tied LAST serves a non-deterministic number, undisclosed

Reproduced three times independently, on three different fixtures.

```
### physical row order: as-authored          ### physical row order: REVERSED
  AT {day}          stock.last  -> [10.0]      AT {day}          stock.last  -> [77.0]
  AT {region, day}  stock.last  -> [77.0]      AT {region, day}  stock.last  -> [77.0]
  AT {day}          stock.sum   -> [107.0]     AT {day}          stock.sum   -> [107.0]   <- control, stable
  disclosures = 0                              disclosures = 0
```
`region` has one value, so `AT {day}` and `AT {region, day}` denote **the same tie set** — and return 10.0
and 77.0 in the same build on the same data. Two mechanisms: DuckDB `arg_max` at delivery
(`engine.py:325-328`) and Polars `sort_by("_order").last()` at combine (`engine.py:768-770`). On a tie the
delivery path makes `first` and `last` **the same operation**. `sum`/`max` controls are invariant under
every reordering, so this is specific to the ordered witness.

**Root cause, and why it is the same finding as §4.4:** LAST selects a *row*, not a governed analytical
point, because there is no sequence anchor to select within. The order-carrying series reduction fixes the
class, not just the symptom.

## 7.2 Defect — R4-C0 withholds the unplaced row but not its contribution, on the ordered path

New as of today's merge, reproduced independently by two inspectors on different fixtures.

```
carrier: one record with day = NULL, amount 70;  three placed days 10 / 20 / 30
                            honest        served
cumsum(revenue.sum)         10/30/60      80/100/130
cummax(revenue.sum)         10/20/30      70/70/70      <- every served cell is the withheld value
lag(revenue.sum)            null/10/20    70/10/20      <- a fabricated predecessor at the sequence start
frame disclosure            incomplete_data / material  (the row IS reported withheld)
```
Polars sorts nulls first ascending, so the unplaced record acts as the earliest point of the walk. R4-C0
runs at frame assembly (`planner.py:626-676`), strictly **after** every engine call, and filters only
output-anchor key columns. The frame caveat is true — *"1 row(s) WITHHELD … not a complete account"* — and
insufficient here: the reader is told a row is missing, not that the numbers they *were* served contain it.

**No widening of R4-C0 reaches this** (consistent with the instruction not to widen it): for
peer-collapsing operators the order key is definitionally outside the output anchor; for focal-preserving
operators it is inside but the containment arrives after the walk. The fix belongs at ordered-domain
formation. Stated as a location fact, not a proposal.

## 7.3 Smaller defects surfaced, for the ledger

1. **`needs_order` is a dead flag.** Set on 8 operators, gates nothing. Cost reproduced: `FAMILY { last }`
   with no `ORDER` clause plans `serve` and then errors at execution — violating `planner.py:1078-1082`.
2. **`rolling_*` with `window=` escapes as an uncaught Python exception out of the MCP tool** (VX), because
   `_realization_standing` calls `_scan_call` unguarded before the guarded per-column loop. The
   window-*less* spelling refuses correctly on the wire. **There is zero test coverage of `rolling_*`
   anywhere**; the only exercise uses the covered spelling. `rank(...)` escapes the same way.
3. **The atom cache key has no order dimension** (`engine.py:228`): two different completed order contracts
   over one atom alias to one memo entry.
4. **EXPLAIN under-reports the scan's order contract**: `would_be.disclosures == []` while the executed
   query carries the `transport` caveat naming axis and partition.
5. **`_atoms` erases the ordered operator** (`planner.py:1943-1946`): EXPLAIN's cone reports
   `(revenue, sum)` for a `cumsum`.
6. **`lag`/`lead` sequence boundary is a false claim**: `('unknown','material')` — *"a value existed but was
   not recorded"* — in a fully supported frame.
7. **A SCAN operator can found a DERIVED family and serve** (VX): `FamilyMember("cumsum", …)` on a DERIVED
   publishes with a License and serves at `{cal.month}`. The "only reducers found families" rule iterates
   `m.measures` only (`parser.py:682-691`); the derived-family check never inspects `op.kind`.
8. **`n=` is silently accepted and ignored** by `cumsum`/`cummax`/`cummin` (VX).

---
# 8. Legacy retirement evidence — FIRST/LAST family founding

## Classification: **real compatibility obligation** — but narrowly, and not where it was assumed

This overturns the provisional category-B classification, which is why the evidence is laid out in full
rather than summarised. **Internal tests and fixtures are excluded by the bar and are kept separate below.**

**The decisive coupling (VX):** the declaration idiom and the query idiom are not separable.
```
level.last @ {store}  with FAMILY { … last ORDER day }     -> serve
                      with `last ORDER day` REMOVED        -> error: "'level' has no family member 'last'"
FAMILY { last } with the ORDER clause removed              -> error: "level.last needs an ORDER key"
```
`FAMILY { last ORDER <level> }` is the **sole enabling mechanism** for `<measure>.last`.

**Occurrence inventory — 33 declaration-side occurrences across 5 repos, and ~240 query-side:**

| bucket | count | counts as compat evidence? |
|---|---|---|
| internal tests / fixtures | 12 | **no** (excluded by the bar) |
| demos / internal harness | 12 | no — *except* `docs/tools/manual_fixtures/finance_manifold.cml`, which is the fixture the **published manual's examples are verified against** |
| **shipped docs / live public surfaces** | 4 | **yes** — `dist/case/index.html:246`; `dist/llms-full.txt:1963`; `services/ask/index/chunks.json:654` (the **live** /ask retrieval corpus, teaching the full `FAMILY { … last ORDER day }` block verbatim); `docs/columna_reference_manual_5e.md:1519`, published at `/docs/reference` |
| **shipped to users inside the wheel** | 5 | **yes** — `columna_server/demo/benchmark/manifold.cml:56`, `columna_server/demo/cascadia/manifold.cml:59,60,65`, `columna_server/case/ch2_solutioning.md:147`. Per `pyproject.toml:60-65` these ship automatically and `columna-server demo` runs them from a clean-venv install with no path args |
| **external contract / wire** | — | **yes, strongest** — `.last` is **hardcoded as advertised remedy text** in `no_result.alternatives` (`planner.py:1802-1803` et al.) and fires even when `last` is not in the family; `describe_measure.member_anchors[m].order_by` crosses the wire; `recapture.py` is the **ratified** drift-gate exemplar corpus containing `SELECT stock.last AT {store*cal.month} -> serve`; the shipped LLM system prompt teaches `stock.last`; `standing = "ratified"` is published in a table stating *"ratified means the construct is part of Frame-QL"* |
| **PyPI front pages** | — | **yes** — `columna_core` METADATA:96 calls `level.last@(store, cal.month)` **"The headline"** |

## The distinction that matters for the ruling

**The obligation attaches to the query spelling `<measure>.last` and to the published word "ratified".
It attaches only thinly to the declaration mechanism `FAMILY { last ORDER <level> }`.**

- The `.cml` declaration syntax appears in **zero** of the three published repo-root manuals' bodies
  (`frame_ql_language.md` has no `FAMILY` block and no `last ORDER` at all — it teaches only the query
  side), and the published grammar page's `FAMILY` signature **omits the `ORDER` clause entirely**.
- **The governed authoring path cannot produce the idiom and never could.** `K0_REDUCERS = {sum, count,
  min, max}` (`compiler/compile.py:48`), and `_WHY_NOT` names `first`/`last` explicitly: *"requires
  `ORDER <level>`, which Core does not validate at parse — the obligation would fall on the compiler, and
  K0 does not carry it."* `emit.measure_block` emits bare member names with no ORDER clause. Corroborated:
  the one governed manifold in the wheel declares `FAMILY { count max min sum }`.
  **No user who went through governed authoring can ever have created a `FAMILY { last ORDER … }`.**
  The idiom is reachable only by hand-authoring a `.cml` — which the fixtures themselves label a legacy path.
- **No backward-compatibility promise exists** for the `.cml` grammar or the language surface (searched
  docs and all CHANGELOGs). There *is* clean-retirement precedent: the 0.13.0 ASSERT retirement, the terse
  form's dated tombstone, ADR-036's producer-tombstone for `b_anchor_crossing`. This house retires
  deliberately, with tombstones.

**So the useful formulation for a later ruling:** the obligation is to keep **`<measure>.last` meaning what
the PyPI headline and the published manual say it means** — not to keep `FAMILY { last ORDER day }` as the
mechanism that supplies it. That is precisely what the successor can satisfy: fill the empty 2×2 cell, keep
the spelling, retire the mechanism.

**Where the evidence is thin, stated rather than rounded up:** no external user can be *proven* to have
authored one. There is no customer manifold in-repo and no telemetry. That bucket rests on the documented
durable store layout plus the shipped demos modelling the idiom — a real but inferential exposure.

---

# 9. Named reusable ordered expressions (§22) — the home

**`DERIVED` is the only layer where the runtime already works, and the blocker is a tokenizer bug rather
than a semantic rule.**

VX: `DERIVED d = cumsum(revenue, by='day')` fails to publish —
*"references unknown column 'cumsum' / 'by' / 'day'"*. The gate is `parser.py:672-676`, a naive
`re.findall` over the formula that demands every identifier — call heads, keyword-argument names, string
literal contents — be a measure. It never invokes the expression parser. The same block records having been
narrowed once already for exactly this class of false positive.

Bypass only that gate and the whole stack works (VX): a Python-built `DerivedColumn("cum_rev",
"cumsum(revenue, by='day')")` publishes and serves at `{day}`, and correctly refuses `order_not_governed`
at `{cal.month}`.

| candidate | verdict |
|---|---|
| **`DERIVED`** | **Recommended for the name and the reuse.** Runtime proven; polarity already correct — *"DERIVED FERTILE — POSITIVE. Closed by default … No declaration ⇒ no permission"* (`planner.py:1983-1984`); and the wire **already publishes** `"denotation_only": not d.family` — the §21 availability-vs-continuation distinction, already in the artifact |
| governed logical declarations (`manifold-agent`) | **Excluded for reuse of `member`**: `REQUIRED_KEYS["member"] = ("measure","anchor","universe")` makes a member a measure-family member *by definition*, so anything placed there acquires continuation standing structurally. A **new disjoint kind** would not — and one is eventually needed, because a named ordered expression cannot be *published* today at all (the nine declaration kinds have no slot for it) |
| publication artifact / K0 | **Excluded** — a faithful carrier, not an authority; and K0 emits no DERIVED at all |
| `WITH` / `AS` / draft | not durable |

**Two changes required before DERIVED can host it truthfully, and one guard:**
- **Parse, don't tokenize** (`parser.py:672-676`) — resolve call heads against the registry. Without it the
  object is unauthorable in `.cml` although it runs.
- **`DerivedColumn` needs a slot for the resolved ordered domain.** Today the order contract lives in the
  formula string and is re-adjudicated at every ask *against the asked anchor* (VX). The name is therefore
  not durable in the §22 sense: it means different things, or refuses, at different output anchors. **This
  is the one place the O2 target cannot be met by reuse alone** — and it is the same object as §4.2.
- **Guard:** close the continuation leak first. A SCAN operator can found a DERIVED family and serve today
  (VX, §7.3 item 7).

---

# 10. Suggested first implementation slice — not started

**Slice: give the ordered domain a name and a lifetime, for `LAST` only, at disclosure strength.**

1. `OrderedLaw` on the two ordered reducers plus the six executable scans, with `result_locus` and
   `order_strength` **consulted** — which closes the plan-says-serve/run-says-error defect (§7.3 item 1)
   using a field that already exists and is already correct.
2. `OrderedDomain` constructed at ordered-domain formation, with `I ⪰ P` adjudicated by the **existing**
   `_check_pin_laws` machinery at inverted polarity.
3. Emit it on the EXPLAIN/resolved path (§4.3) — additive, no grammar, no round-trip risk.
4. Disclose, at domain formation, any candidate point excluded for unresolved **order-key** standing — the
   count is one carrier read, and it closes the silent-shrink half of O2-I5 without R4 and without
   widening R4-C0.

**Why this slice:** it proves the new abstraction end-to-end, requires no new grammar, no wire bump, no
legacy migration and no R4; and it is the smallest change that makes §7.1's non-determinism *visible*
rather than leaving it silent. It deliberately does **not** include the order-carrying series reduction
(§4.4) — that is slice two, and it is the one that actually retires the mis-kinding.

---

# 11. Questions that need a ruling — code evidence cannot settle them

**Q1 · What confers governed order standing, if not a lineage name?**
*Evidence:* `TEMPORAL_LINEAGES = {"calendar","fiscal"}` is the entire definition (`projection.py:223`); the
code itself defers the question as *"declaration law and not this repair's to invent"*
(`planner.py:320-327`); levels have no type at all (`model.py:70-78`).
*Choices:* (a) a declared per-level orderability + comparison, resting on a new CDT capability;
(b) widen the lineage set — preserves name-matching, which O2 §4 rejects; (c) declare order standing on the
edge/hierarchy rather than the level.
*Recommendation:* **(a)**, and it is a prerequisite for almost everything else in §6. It also needs the CDT
comparison capability to exist, so the two rulings are coupled.

**Q2 · Does the peer anchor get a surface, or stay implicit?**
*Evidence:* `@ {…}` is structurally unavailable — on a scan operand `_check_map_operand_pin` requires
`pinned == anchor` exactly, and on an inline reduction `_check_pin_laws` **refuses** the coarser pin a peer
would be. Overloading `@` would put two opposite polarities on one marker, in a codebase whose stated
doctrine (`envelope.py:15`) is that this exact overload is what made the terse fragment unshippable.
*Choices:* (a) a dedicated braced peer clause — one new marker, adjudicable by existing machinery at
inverted polarity, `render_canonical` gains one line; (b) peer declared at authoring time beside
`FamilyMember.order_by` — zero grammar change, zero round-trip risk, but one measure cannot then serve both
a `{account}`-peer and an `{account, year}`-peer reading without two declarations.
*Recommendation:* **(a)**, because O2 §18 wants reset expressed as peer geometry, and (b) makes the common
YTD case an authoring act. But this is genuinely a trade-off and it is yours.

**Q3 · Is `first`/`last` moving out of `REDUCER` a declaration-model change you want to make?**
*Evidence:* `parser.py:688` makes `kind == REDUCER` the admission rule for family declaration. Changing the
kind removes `first`/`last` from every declared `.cml` family, including the shipped `benchmark.cml` and
`cascadia/manifold.cml` in the wheel. §8 says the compatibility obligation attaches to the **query
spelling**, not the declaration mechanism — so this is survivable, but it is a break with a blast radius
and it wants a dated tombstone rather than a quiet edit.
*Choices:* (a) new kind now, tombstone the declaration form; (b) keep the kind, add `OrderedLaw`, and let
the law rather than the kind gate family founding — smaller, reversible, and leaves the mis-kinding in
place; (c) defer until slice two.
*Recommendation:* **(b) then (a)** — make `re_entrant`/`OrderedLaw` the gate first (it is already correct
for `first`/`last`), and only then change the kind, so the two changes are independently revertible.

**Q4 · §7's participation question, which the architecture cannot currently even ask.**
*Evidence:* `LAG` at a point whose predecessor exists but whose operand is unsupported — current behaviour
is **already** O2-conformant (null propagates positionally, the one correct cell in the whole matrix), while
`cumsum` **implicitly skips** and serves the downstream cells as ordinary. These are two different operator
laws and today they are two different accidents.
*Choices:* per-operator `operand_standing`, defaulting `strict`; or a global convention.
*Recommendation:* per-operator and `strict` by default, which is what §7 requires — but the ruling is which
of the two existing behaviours is the intended one for cumulative, because changing it changes served
numbers.
