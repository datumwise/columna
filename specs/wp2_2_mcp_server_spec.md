# WP-2.2 spec — the Columna MCP server (v1)

**Goal.** Expose a library of Manifolds to AI agents through MCP, with **one contract** (ADR-032
D8): every tool returns the same outcome/disclosure structure the Python API returns — the four
moods as data. This is the wedge product: the first metrics MCP server that can say "it depends."

**Context files (read before coding).**
- `adr_032_columna_engine.md` — D7 (server topology), D8 (three surfaces, one contract, NL agent
  as MCP client). This spec implements D8's MCP surface.
- `columna_core/frameql.py` (`ManifoldServer`, `Frame.run/plan/explain`, `on_universe`),
  `planner.py` (`FrameResult.outcome/.served/.clarifies/.refusals/.errors`),
  `disclosure.py` (`Caveat{category, detail, rel_error, source, severity, remedy}`,
  `Disclosure{caveats, population}`, `Outcome{kind, discriminator, reason, alternatives}`,
  categories: approximation/freshness/coverage/unconfirmed_assumption/transport/b_anchor_crossing).
- `structured_disclosure_capture.md` — the `{code, materiality, ...}` schema this server puts on
  the wire.
- `benchmark.cml` + the WP-0 fixture warehouse — the demo Manifold.
- Depends on: WP-2.1 (Manifold store; may be stubbed as "directory of `.cml` + data-path config"),
  WP-1.3 (disclosure adapter — the mapping table below IS that adapter's spec; if WP-1.3 is not
  merged first, implement the adapter inside this WP in `columna_core.disclosure_wire` and WP-1.3
  collapses into it).

## Tools (five, read-only)

1. `list_manifolds() -> [{manifold_id, name, description, n_measures, universes: [name]}]`
2. `describe_manifold(manifold_id)` → dimensions + levels, functional edges (with lineage tags),
   universes (name + predicate rendered), measure index (name + family).
3. `describe_measure(manifold_id, measure)` → the **family triple** — `family_root`,
   `member_anchors` (the member-anchor set), `family_reducer` — plus `dtype`, `v_anchor`,
   `m_anchor` (mechanism if declared), `b_anchor` (`blocked_lineages`), `universe`,
   `is_monoid`/fertility, and per-property provenance where the Manifold records it
   (`inferred | declared | data_attested`). This tool discharges the pending "MCP measure-family
   descriptor" item.
4. `query(manifold_id, frameql, universe?)` → executes; `universe` maps to `Frame.on_universe`.
5. `explain(manifold_id, frameql, universe?)` → `Frame.plan()` / `explain(execute=False)`:
   the would-be outcome + disclosures with **zero backend fetches**.

`frameql` is the textual form already parsed by the library (anchor spec + column exprs). The
server NEVER accepts SQL and has no write surface of any kind.

## Wire contract (the heart of the WP)

```jsonc
{
  "outcome": "serve | disclose | clarify | refuse | error",   // DERIVED — see "Outcome derivation"
  "frame": {
    "anchor": [...],
    "universe": "U1 | null",
    "rollup_severity": "none|info|caution|critical",
    "disclosures": [ { /* FRAME-scoped wire caveats — see below */ } ]
  },
  "columns": [
    {
      "name": "aov",
      "status": "served | clarify | refuse | error",
      "value":  ...,              // scalar, or omitted
      "values": [...],            // vector rows {group..., value}, or omitted
      "population": "U1",         // Disclosure.population
      "disclosures": [ { /* COLUMN-scoped wire caveat, below */ } ],
      "no_result": {              // present iff status != served; = Outcome as data
        "kind": "clarify | refuse | error",
        "discriminator": "ambiguous | unsupported | null",
        "reason": "co_anchor_ambiguous",
        "detail": "which population is the rate over?",
        "alternatives": [ {"token": "on_universe('customers')", "description": "per customer", "apply": {"universe": "customers"}},
                          {"token": "on_universe('orders')",    "description": "per order",    "apply": {"universe": "orders"}} ]
      }
    }
  ]
}
```

**Outcome derivation (normative).** `outcome` is not a raw copy of `FrameResult.outcome`; it is
derived once, in `disclosure_wire`, so every surface agrees. A no-result mood dominates and is taken
from the engine's rollup (`refuse` > `clarify` > `error`). Otherwise the frame is served, and
**materiality — not severity — decides** `serve` vs `disclose`: the outcome is `disclose` iff at
least one disclosure is `material` (frame- **or** column-scoped), else `serve`. So an
immaterial-only served frame (e.g. a lone `freshness`/`provenance` caveat) reads `serve`, while a
served frame carrying any `material` caveat (a B-anchor crossing, a coverage/`denominator_population`
caveat) reads `disclose`. `rollup_severity` remains the independent severity roll-up and is not the
serve/disclose discriminant.

**Disclosure scoping (normative).** Disclosures appear at two scopes, and the same wire-caveat shape
is used at both:
- **column-scoped** (`columns[].disclosures`) — caveats a single column's resolution produced (a
  B-anchor crossing on that column, its approximation error, its coverage).
- **frame-scoped** (`frame.disclosures`) — caveats that belong to the frame as a whole and are not
  attributable to any one column, e.g. the multi-universe **coverage** caveat a side-by-side of
  columns over different populations raises. A frame-scoped caveat is never duplicated into a
  column's array. Both scopes feed the outcome-derivation materiality test above.

**`alternatives[].apply`.** When an alternative names a universe pin, it carries a derived
`apply: {"universe": U}` beside the human `token`/`description` — a faithful re-encoding (never a
synthesized alternative) that a caller applies via the `query`/`explain` `universe` arg.

**Wire caveat (the disclosure adapter).** Each engine `Caveat` maps to:

```jsonc
{ "code": "...", "materiality": "material | immaterial", "severity": "info|caution|critical",
  "category": "<engine category, preserved>", "detail": "...", "remedy": "... | null",
  "source": "... | null", "rel_error": 0.012 | null }
```

Category → (code, default materiality) table — one closed vocabulary merging the benchmark codes
with engine-native ones; this table is normative and lives in code as a single dict:

| engine category | wire code | default materiality |
|---|---|---|
| b_anchor_crossing | `blocked_reduction` | **material** |
| coverage | `denominator_population` | **material** |
| unconfirmed_assumption | `input_anchor` | **material** |
| approximation | `approximation` | material iff `rel_error` ≥ 0.01, else immaterial |
| freshness | `freshness` | immaterial |
| transport | `provenance` | **immaterial** (faithful-step record) |

Reserved codes for authoring-era disclosures (emit-capable now, produced later): `stock_reading`,
`distinct_grain`, `weighting_grain`, `extremum_grain`, `incomplete_data`, `conflicting_data`,
`other`. The wire schema is the benchmark schema — one vocabulary end to end.

**Clarify round-trip requirement.** `alternatives[].token` MUST be mechanically substitutable: a
calling agent that picks alternative *k* re-issues `query` with the token applied (as the
`universe` arg or an amended expression) and MUST get a non-clarify outcome for at least the demo
cases. This is tested, not aspirational (acceptance #4).

## Transport & operation

- Python `mcp` SDK. `stdio` transport is canonical (Claude Desktop / local agents);
  `streamable-http` behind `--http :PORT`, gated by `COLUMNA_MCP_TOKEN` if set.
- Entry point: `columna-server mcp --manifolds <dir>` (package `columna-server`, first real code
  in it). Manifold dir layout (stub for WP-2.1): `<dir>/<id>/manifold.cml` + `data.toml`
  (connector type + path).
- Startup parses all manifolds once; `list/describe` never touch data; `explain` must not
  increment `connector.fetch_count` (assert in tests via `ManifoldServer.fetches`).
- Every tool result also includes `"contract_version": "1"`.

## Acceptance (pytest, MCP client harness over stdio)

1. `list_manifolds`/`describe_manifold` round-trip against the fixture Manifold.
2. `describe_measure` on the AOV-relevant family returns the triple (root, member-anchor set,
   reducer) + `blocked_lineages`.
3. **The wedge case:** `query` for the demo ratio/AOV ambiguity returns `outcome: clarify` with ≥2
   structured alternatives (mirrors `coanchor_demo` §D).
4. Substituting an alternative's token and re-querying returns `serve` or `disclose` — the
   round-trip demo, scripted.
5. B-anchor crossing case returns `serve`d value **with** a `blocked_reduction / material /
   critical` wire caveat (inform-and-serve preserved on the wire).
6. Out-of-universe returns `refuse` with `discriminator: unsupported`; unknown operator returns
   `error` — the two are distinguishable on the wire.
7. `explain` on case 5: identical disclosure payload, `fetches` delta = 0.
8. Demo artifact: `demos/mcp_claude_desktop.md` — config snippet + a transcript of the
   AOV clarify→answer→re-query flow.

## Out of scope

Query agent (WP-2.4), auth/multi-tenant, write surfaces, Option B cross-universe confinement,
OSI/dbt import, the website widget (site v1 consumes this server unchanged — that's the point).
