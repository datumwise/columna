# OF-16 / OF-17 — reference manual correction (desk draft v0.1)

*Desk artifact, 2026-07-26. Row option (a): the desk writes the correction.
Every claim below verified by EXECUTION against the shipped parser
(`columna-core` 0.12.0), not by reading. Two rows close together: OF-16 (§26.6
inverted + wrong signature) and OF-17 (the Chapter 26 preamble keyword set).
Huayin ratifies; CC applies verbatim.*

---

## 1 · What the shipped parser actually accepts (executed, 2026-07-26)

| form | source | result |
|---|---|---|
| `HIERARCHY location store -> region` | §26.6 body, as written today | **REJECTED** — `bad HIERARCHY … (expected 'HIERARCHY <lineage> { … }')` |
| `EDGE store -> region ALONG location VIA stores(store_id, region)` | §26.6 annotation, as written today | **REJECTED** — `EDGE` is not a keyword; the line is swallowed into the preceding statement |
| `HIERARCHY location { store -> region VIA stores(store_id, region) }` | the shipped grammar | **PARSES** |

The parser's own docstring is the authority:

    HIERARCHY <lineage> { <a> -> <b> VIA <table>(<a_col>, <b_col>) [-> <c> VIA ...] ; <path> ... }

and `_KW` carries the comment `# EDGE purged (§2a)`. So §26.6 is wrong in
**both** directions — it marks the purged form SHIPPED and the shipped form
SCHEDULED — and its body signature is a third error independent of the
inversion: no braces, no per-hop `VIA`. A reader following §26.6 today writes
grammar the parser rejects, twice over.

## 2 · The §26.6 replacement (RATIFIABLE COPY — replaces lines 1525–1531)

### Status annotation — replaces the current `> **[single functional edge: SHIPPED …]**` line

> **[`HIERARCHY`: SHIPPED 0.12 — the sole surface for functional roll-up]** ·
> **[refresh-verification of edge functionality (edge functional in the data →
> verdict): SCHEDULED — Certificate-kernel WP]** — `HIERARCHY` declares one or
> more functional hops as a named lineage; a two-node hierarchy *is* the single
> edge (the former `EDGE` short form was purged in the case-demo sweep §2a, and
> the parser no longer carries the keyword). What remains scheduled is not the
> declaration but its *verification*: the refresh-time check that each declared
> hop is in fact functional in the bounded data, entering the certificate with a
> verdict (ADR-034 D1).

### Body — replaces the current `HIERARCHY <name> <child> -> <parent> …` paragraph

`HIERARCHY <lineage> { <child> -> <parent> VIA <table>(<child_col>, <parent_col>)
[-> <grandparent> VIA <table>(…)] [; <second_path> …] }` declares a roll-up
lineage in a dimension family. The braces are required; every hop names the
physical table and the column pair that carries it, and a semicolon separates
additional paths that share the lineage name. Each hop asserts a total
functional dependency over the Manifold's boundaries (Chapter 4.3); chains
commute automatically, and redundantly declared diamonds are checked for
commuting (Chapter 4.4). A hop is *both* an assertion and a navigable
structure: it enters the certificate like any precondition, *and* it licenses
climbs, scan parameters (`reset`/`within`/`step` resolve along it), and
derived-dimension resolution. Promoted values must cascade along every lineage
the dimension participates in (Chapter 5.3); the cascade is declared with the
lineage. Time-varying dependencies are declared in their period-qualified or
split form per Chapter 4.7, not forced into a hop the data will contradict.

*Worked form, from the shipped demo Manifold:*

    HIERARCHY location { store -> region VIA stores(store_id, region) }

*A functional relationship the model asserts but no query should climb is
`ASSERT <child> -> <parent> IS FUNCTIONAL` (§26.8) — assertion without
navigation. A non-functional (many-to-many) relationship is not a hierarchy at
all: it is a `RELATE` with declared faces (Chapter 4.8 / the crossing
increment), because no lineage can be honest about a hop that fans out.*

## 3 · The OF-17 fix — Chapter 26 preamble (line 1476)

Current: *"…the shipped 0.7.8 keyword set is the short forms — `MANIFOLD`,
`UNIVERSE` (with an inline predicate), `LEVEL`, **`EDGE`**, `MEASURE` …"*

RATIFIABLE replacement for that clause:

> the shipped keyword set is the *short* forms — `MANIFOLD`, `UNIVERSE` (with an
> inline predicate), `LEVEL` (with inline `ATTR`), `HIERARCHY`, `RELATE` (with
> declared faces), `MEASURE` (with inline `M_ANCHOR`/`FAMILY`/`BLOCKED`/`ORDER`),
> `DERIVED`, `ASSERT`

*(Derived by execution from the parser's own `_KW` tuple: MANIFOLD, UNIVERSE,
LEVEL, RELATE, MEASURE, DERIVED, ASSERT, HIERARCHY, ATTR — with `EDGE` carrying
the purge comment. Note the version reference: "0.7.8" is stale everywhere it
appears in this preamble; the correction drops the pinned number in favour of
"the shipped keyword set", so the sentence cannot rot again at the next
release.)*

## 4 · Scope discipline — what this correction does NOT touch

- No other §26 subsection is edited. `DIMENSION`, `ALIAS`, `ASSERT`,
  `WITHHOLD`, §26.10 are out of scope even where their status marks may also be
  stale — a status-mark audit of the whole chapter is a separate, larger pass
  and should be rowed rather than smuggled in here.
- The `RELATE`/faces surface is *mentioned* in §26.6's closing note (because a
  reader arriving at hierarchies must be told where many-to-many goes) but is
  not documented here; §26.6 gains no new construct.
- Prose elsewhere in the manual that references edges as an internal concept
  stays: `kind="edge"`, "functional edge", the internal taxonomy — the purge was
  of the *surface keyword*, never of the concept (ratified 2026-07-25).

## 5 · Application notes for CC

1. Apply §2 and §3 verbatim; no other manual edits in the PR.
2. **Verify by execution, not by reading**: parse the worked form in §2 and the
   §26.6 body's signature against the shipped parser; both must succeed.
3. Re-run `scripts/check_purged_grammar.py` — the ROWED exemption keyed to
   OF-16 must now report the file clean; the guard **fails if the row closes
   while the fossil remains**, so a green guard plus a clean grep is the
   closure evidence.
4. Grep the manual for any remaining `EDGE` occurrence and report the list
   before closing; expected after this pass: zero surface-form occurrences.
5. Close **OF-16 and OF-17 together** in `open_forks.md` with the PR link, per
   OF-17's ruled option (a).
6. Row separately, do not fix here: **a status-mark audit of Chapter 26** (are
   any other SHIPPED/SCHEDULED marks stale?) and **the stale "0.7.8" version
   references** elsewhere in the manual.

## 6 · Note on the missing draft

CC's own OF-16 draft (`specs/of16_manual_26_6_correction_draft_v0_1.md`,
referenced by the ledger row) exists on no branch and no ref — the row links to
a file the repo does not contain. This desk draft supersedes it. Two actions:
point the OF-16 row at this artifact when it lands, and treat the dangling link
as a small instance of the referent proverb — a ledger row citing an unpushed
working-tree file is a claim about a path that does not resolve.
