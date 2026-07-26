# The ASSERT Retirement — ruling document (v0.1)

*Desk artifact, 2026-07-26. Ruled by Huayin: option (c) — ASSERT retires from
the Manifold entirely. This document governs the work package; CC's PROPOSAL.md
is written against it. Strings marked DRAFT await Huayin's ratification and are
placeholders until his word. Verification inputs: the desk's execution checks
(2026-07-26) and CC's (a)–(c) report (PR #99 merge card).*

---

## 1 · The ruling and its doctrine

**ASSERT is retired from the Manifold. Both shipped forms** — row
(`ASSERT <n> [ON <u>] WHERE <pred>`) and aggregate
(`ASSERT <n> [ON <u>] AT <anchor> HOLDS <invariant>`) — **and, by cascade, the
standalone row-attribute form `ATTR <names> ON <universe>`**, whose sole
consumer is the row-form assert (verified: `row_attrs` appears in exactly one
place in the shipped package, the assert purity check). The **inline**
`LEVEL … ATTR` form **stays**: universe predicates load on it.

**The doctrine** (enters the manual's declaration chapter, the grammar page's
frame, and eventually Paper A):

> Everything a Manifold's trial proves is a precondition of something it
> serves. A Manifold does not carry claims for their own sake: seven provers
> shipped, and six prove their own construct's serving preconditions —
> hierarchy functionality licenses climbs, fertility licenses derived
> re-aggregation, basis licenses absence semantics, face laws license
> crossings. The assert provers alone proved a claim no serving behavior
> depended on: load-bearing in form, unloaded in fact. Data contracts belong
> to the attestation layer, not the meaning layer.

**The admission test** (governs every future construct): *a construct is
admitted iff its prover licenses some serving behavior.* Applied twice on day
one: it retired ASSERT and found the standalone-ATTR cascade on its own.

## 2 · What retires, what stays, what is protected

| item | fate |
|---|---|
| `ASSERT` (both forms): parser, `Assert` model, `_prove_row_assert`, `_prove_assert`, serve-at-anchor helpers, `ASSERT_OPS`, describe/documents emission, `Manifold.asserts` | **retire** |
| standalone `ATTR … ON <universe>`: parser path, `Universe.attributes`, `row_attrs` machinery, describe emission | **retire** (remove, not mothball — unreachable machinery is where the next fossil grows) |
| inline `LEVEL … ATTR` (name + binding; predicate vocabulary) | **stays, untouched** |
| `ASSERT`/`ATTR` in `_KW` | `ASSERT` leaves; `ATTR` stays (inline clause) |
| `conflicting_data` REFUSE producer (`planner.py:174`), reason entry (`disclosure.py:188`), degradation path (`adjudication.py:545`) | **tombstone** per the `co_anchor_ambiguous` precedent (`disclosure.py:165`): dated comment + retirement-pin test asserting the reason is never emitted |
| 🔒 reserved caveat code (`disclosure_wire.py:59-65`, "RETAINED, reserved and UNWIRED") | **do not touch** — same string, different referent |
| 🔒 benchmark hazard *category* `conflicting_data` (lives in ground-truth-benchmark) | **out of blast radius** — not this repo, not this concept |
| `/docs/grammar` | self-heals on regeneration; **delete** the now-dead `SUPPLEMENT["ASSERT"]` entry and the generator docstring's superseded "rowed upstream" line |
| describe wire | the `asserts` field is removed; `contract_version` stays "1" pre-broadcast with zero consumers — the release note states the removal explicitly |

**Full inventory beyond the table** (from the desk's blast-radius run): core
`__init__`, fixtures (`cascadia_slice.cml` line 54, `test_cut_set.py:64`,
`test_assert_hierarchy.py`), server `tools.py` describe block, Cascadia
`manifold.cml` lines 16 (standalone ATTR) and 73 (the assert), case chapters
(§4 below), `docs/columna_reference_manual_5e.md` §26.8, FrameQL manual,
`specs/wp2_2_mcp_server_spec.md:128`, both site generators (`gen_case.py`,
`gen_universe_visual.py`), CHANGELOG. Verified unaffected: the public
benchmark kit and demo benchmark manifold (ASSERT-free), `eval.py`.

## 3 · The teaching refusal (DRAFT — Huayin ratifies)

The parser's rejection of retired syntax names the ruling, not just the error:

> `ASSERT was retired in 0.13 — everything a Manifold's trial proves is a
> precondition of something it serves, and a data contract licenses no serving
> behavior. Contracts belong to the attestation layer, upstream of the
> Manifold. (Ruling 2026-07-26; see the 0.13.0 release note.)`

Standalone `ATTR … ON` gets the short form of the same refusal, citing the
cascade.

## 4 · The case chapters (ratified content; three-surface lockstep; ch3 is a recorded exhibit)

**ch2.md:141** — the manifold excerpt drops the `ATTR units, units_returned ON
transaction` and `ASSERT returns_bounded …` lines. The teaching moment they
carried ("checked, not hoped") is real and must not silently vanish; DRAFT
replacement passage, placed where the excerpt's walkthrough discussed the
contract:

> One thing this Manifold deliberately does not carry: the team's data
> contract — "you can't return more than you bought." An early draft declared
> it here, adjudicated like everything else. It was retired by a ruling worth
> stating, because it is the document's admission test: everything a
> Manifold's trial proves is a precondition of something it serves. The
> contract is true of this warehouse — but nothing served depends on proving
> it, so it is not meaning; it is attestation, and it lives upstream. What
> remains in the Manifold is exactly the set of claims the answers stand on.

**ch3.md:21** — the adjudication table loses the `ASSERT returns_bounded`
row; any claim-count prose in the chapter adjusts. **Re-recording plan**: ch3
is a recorded exhibit — after 0.13.0 core lands, the standing seed/gen_case
pipeline re-records it; the desk verifies the diff is exactly the expected
row and count changes and nothing else; Huayin's ratification covers the
re-recorded chapter as with every recorded exhibit.

## 5 · §26.8 — the RETIRED treatment (one rewrite, not two; DRAFT)

The status annotation and body are replaced with:

> **[`ASSERT`: RETIRED — 0.13, ruling 2026-07-26]** — the Manifold's admission
> test: everything its trial proves is a precondition of something it serves.
> The shipped assert proved claims no serving behavior depended on; data
> contracts belong to the attestation layer. Retained for the record: the
> FD form this section once proposed (`ASSERT <child> -> <parent> IS
> FUNCTIONAL` — functionality proven for validity analysis, without licensing
> climbs) is a genuine grammar-level need with no demonstrated use case; if
> one appears, its home is a declarable block on a hierarchy edge (the
> planner's `blocked_edges` machinery, today refutation-only), not a revived
> assert. The assertion-versus-navigation distinction this section taught —
> an assertion enters the certificate; a hierarchy edge is an assertion plus
> a navigable structure — remains true and now lives with `HIERARCHY` (§26.6).

## 6 · Version, sequencing, ledger (ruled)

- **0.13.0, alone, before broadcast.** Removing grammar is breaking; pre-1.0
  minor bump. Retirement is the release's only cargo.
- **P1 alignment renumbers to 0.14.** DRAFT public ledger note: *"2026-07:
  0.13.0 is the ASSERT retirement — ruled, not drifted: the admission test
  (everything a trial proves is a precondition of something served) removed
  the one construct that failed it, plus its cascade. Multi-universe
  alignment (P1), previously 0.13, renumbers to 0.14 unchanged in scope."*
- **DRAFT release note (CHANGELOG 0.13.0)**: BREAKING — `ASSERT` (both forms)
  and standalone `ATTR … ON <universe>` are removed from the definition
  language; migration: delete those lines from your `.cml` (the parser's
  refusal names this note); the describe wire no longer emits `asserts`;
  `conflicting_data` refusals can no longer occur and the reason code is
  tombstoned; rationale: the admission test, stated in one line, with a link
  to the doctrine.

## 7 · Rows minted alongside (recorded, not built)

1. **The FD door**: author-declarable `blocked_edges` — deferred with reasons
   (no demonstrated use case; a construct kept for a use nobody has is how
   ASSERT happened). Lives in `doctrine_gaps.md`.
2. **The licensing test** as standing doctrine for invariant-like proposals.
3. **Universe `WHERE` validation gap** (found by CC's (b) check): the parser
   validates no references in a universe predicate — an undeclared column
   parses. Adjacent defect, out of this WP's scope, rowed with CC's evidence.
4. **Contracts' landing zone**, stated honestly: upstream/external tooling
   today; an attestation WP if demand appears. Cascadia's warehouse keeps the
   invariant true by construction — the data loses nothing.

## 8 · Discipline

Proposal-first: CC's PROPOSAL.md against this document — inventory
conformance, file-by-file plan, LOC estimate, test plan (including provoking
both retirement-pin directions: the teaching refusal fires; the tombstoned
reason never emits), the re-record sequencing, and any structural surprise →
off-ramp to the desk before code. The five DRAFT strings (§3 refusal, §4
passage, §5 annotation, §6 ledger note + release note) ship only on Huayin's
ratification. Standing rules apply: three-surface lockstep for case content;
recorded exhibits change only by re-recording; probe the exact referent —
the two protected `conflicting_data` referents are the test of that proverb.
