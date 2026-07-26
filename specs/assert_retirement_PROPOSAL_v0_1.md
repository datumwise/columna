# The ASSERT Retirement — PROPOSAL (v0.1)

*Written against `assert_retirement_ruling_v0_1.md`. **No code written.** Every inventory item below
was checked against the repo, not read off the ruling. Three conformance findings and one structural
surprise are reported in §1 and §2 — the surprise is an off-ramp item under the ruling's §8.*

---

## 1 · Inventory conformance

Everything the ruling names exists where it says, with three corrections.

| ruling says | verified |
|---|---|
| Cascadia `manifold.cml` line 16 (standalone ATTR) and line 73 (the assert) | ✅ exact — line 16 `ATTR units, units_returned ON transaction`, line 73 `ASSERT returns_bounded ON transaction WHERE units_returned <= units` |
| `cascadia_slice.cml` line 54 | ✅ exact — and note it is the **aggregate** form (`AT store HOLDS …`), so both shipped forms have a live fixture |
| `test_cut_set.py:64`, `test_assert_hierarchy.py` | ✅ present |
| core: parser, model, adjudication, `ASSERT_OPS`, documents, `__init__` | ✅ all present |
| server `tools.py` describe block | ✅ present |
| §26.8 | ✅ exists (line 1545) — **and is marked `SCHEDULED — on-ramp WP`, never SHIPPED** |
| `specs/wp2_2_mcp_server_spec.md:128`, FrameQL manual, CHANGELOG | ✅ present |
| site generators `gen_case.py`, `gen_universe_visual.py` | ✅ both reference asserts |
| benchmark kit + demo benchmark manifold ASSERT-free; `eval.py` clean | ✅ confirmed — `conflicting_data` appears in **no** `.json` in this repo |

### Correction 1 — the case chapters are at a different path, and there are **six** files, not two

The ruling cites `case ch2.md:141 + ch3.md:21`. Those live at **`apps/website/src/content/case/`**, not
under `columna-server`. The server carries **separately-named copies**:

| surface | file | hits |
|---|---|---|
| site | `apps/website/src/content/case/ch2.md` | 2 |
| site | `apps/website/src/content/case/ch3.md` | 1 |
| package | `packages/columna-server/src/columna_server/case/ch2_solutioning.md` | 2 |
| package | `packages/columna-server/src/columna_server/case/ch3_live.md` | 1 |

**The three-surface lockstep therefore spans four files, not two** (the third surface, `llms-full`,
composes from the site copies at build). The differing filenames are exactly the shape that defeats a
naive sweep — related to proverb 4. Any plan that edits only `ch2.md`/`ch3.md` leaves the package
copies stale, and `gen_case.py` reads the **package** copies.

### Correction 2 — §26.8's status is `SCHEDULED`, not shipped

§26.8 currently reads **`[ASSERT: SCHEDULED — on-ramp WP]`**. The ruling's §5 replacement text
(`RETIRED — 0.13`) is still right, but the annotation is being changed *from* SCHEDULED, not from
SHIPPED — worth stating because it means **the manual has never documented ASSERT as shipped**, even
while the parser accepted it. That is the same form-primacy defect OF-18 tracks, in a third variant:
here the manual *understated* what ships.

### Correction 3 — `ASSERT` never entered the docstring grammar block

Confirmed again here: the retirement removes `ASSERT` from `_KW` and from the parser, and the
docstring block never listed it. So `/docs/grammar` heals with **no docstring edit at all** — only the
dead `SUPPLEMENT["ASSERT"]` entry and the generator docstring's superseded "rowed upstream" line need
deleting, exactly as the ruling's §2 says.

## 2 · ⚠️ Structural surprise → off-ramp (ruling §8)

**§26.6 now points readers *at* the retiring construct as the recommended alternative — and I put it
there today.**

`docs/columna_reference_manual_5e.md:1537`, landed this morning in the OF-16 correction, reads:

> *A functional relationship the model asserts but no query should climb is
> `ASSERT <child> -> <parent> IS FUNCTIONAL` (§26.8) — assertion without navigation.*

That sentence was correct when written and is falsified by this ruling. Left alone, §26.6 would send a
reader to a RETIRED section for the assertion-without-navigation case, four hours after we corrected
§26.6 precisely so it stopped teaching syntax the parser rejects.

The ruling's §5 anticipates the *content* (the FD form is "retained for the record", its future home
is `blocked_edges`) but does not name **this cross-reference** as a site to edit. It needs desk-drafted
replacement copy, because §26.6 is ratified content and the sentence is load-bearing: it teaches the
assertion-vs-navigation distinction the ruling explicitly says "remains true and now lives with
`HIERARCHY` (§26.6)" — so §26.6 is where that idea lands, and it currently outsources it to §26.8.

**Recommendation:** one desk-drafted sentence replacing line 1537's first clause, shipped in the same
WP as the §5 rewrite — one manual pass, not two, consistent with the ruling's own "one rewrite" rule.
**I am not drafting it**; it is ratified manual content.

## 3 · File-by-file plan

Five commits, each independently green, in dependency order.

### Commit 1 — core: remove the construct (~180 LOC net removal)
`parser.py` (`_p_assert`, `_p_attr`, `ASSERT_OPS`, `_KW` entry, the `row_attrs` purity block,
universe-attribute plumbing) · `model.py` (`Assert`, `Manifold.asserts`, `Universe.attributes`) ·
`adjudication.py` (`_prove_assert`, `_prove_row_assert`, the assert branch of the degradation path) ·
`documents.py` (incl. **lines 111 and 156** — the `u.attributes` map-side consumers, added by the desk's execution correction) · `__init__.py`. Removed, not mothballed — per the ruling, unreachable machinery is
where the next fossil grows.

Adds the **teaching refusal** (ruling §3, DRAFT string) for both retired forms.

### Commit 2 — core: the `conflicting_data` tombstone (~25 LOC)
`disclosure.py:188` → dated tombstone on the `co_anchor_ambiguous` pattern at line 165 ·
`planner.py:174` producer removed, comments at 102/300/874 updated · `adjudication.py:545` ·
**retirement-pin test** asserting the reason is never emitted.
🔒 `disclosure_wire.py:59-65` and the benchmark hazard category are **untouched** — same string, two
different referents, which is the proverb this WP tests.

### Commit 3 — fixtures + tests (~60 LOC)
`cascadia_slice.cml:54` · `test_cut_set.py` · `test_assert_hierarchy.py` (retires wholesale) ·
Cascadia `manifold.cml` lines 16 + 73.

### Commit 4 — docs + specs (manual pass; DRAFT strings)
§26.8 RETIRED treatment · **§26.6:1537 cross-reference (§2 above)** · FrameQL manual ·
`specs/wp2_2_mcp_server_spec.md:128` · CHANGELOG 0.13.0 · public ledger note.

### Commit 5 — site (after core 0.13.0 is installable)
`gen_case.py`, `gen_universe_visual.py` · `gen_grammar.py`: delete `SUPPLEMENT["ASSERT"]` + the
superseded docstring line · **all four case-chapter files** (§1 correction 1) · re-record ch3.

**Estimate: ~300 LOC net removal**, ~120 added (refusals, tombstone, pin tests, replacement copy).

## 4 · Test plan — both retirement-pin directions provoked

Per the standing rule that a guard is verified in *both* directions, by provoking the failure:

1. **The teaching refusal FIRES.** Parse `ASSERT n ON u WHERE p`, `ASSERT n ON u AT l HOLDS i`, and
   `ATTR a ON u` → each raises, and the message **names the ruling and the release note**, not just a
   syntax error. Asserted on message content, not merely on the exception type.
2. **The tombstoned reason NEVER emits.** Retirement-pin test over the full reason vocabulary asserting
   `conflicting_data` is unreachable — the `co_anchor_ambiguous` precedent.
3. **Inline `LEVEL … ATTR` still works** — parse *and serve* a universe predicate loading on it
   (`WHERE day >= store.opened`). This is the cascade's boundary and the one thing a careless removal
   would break.
4. **Describe no longer emits `asserts`**, and the insulation test still passes.
5. **Full suite + `regen-check` + `check_manual_frameql` + the grammar page's own three fail-closed
   paths**, which will exercise the `_KW` change automatically.

## 5 · Re-record sequencing

0.13.0 core lands → published → site pin bumps → `gen_case.py` re-records ch3 from the shipped
package → **desk verifies the diff is exactly the expected row + count changes and nothing else** →
Huayin ratifies the re-recorded chapter. The site commit (5) cannot precede the release, because the
shipped-coherent path installs from PyPI.

## 6 · Open questions

1. ~~**The §26.6 cross-reference**~~ — **ANSWERED** (desk-drafted, 2026-07-26): joins the ratification
   batch as its sixth DRAFT string, replacing line 1537's sentence with the "no declared form today"
   framing (a two-node HIERARCHY both asserts functionality and licenses the climb — inseparable as
   shipped; the assert-only need, if it materialises, lands on `blocked_edges`).
2. **`contract_version` stays "1"** with `asserts` removed — ruled, and I agree pre-broadcast with zero
   consumers. Flagging only that this is the first *removal* from the wire under that version; if the
   desk wants a precedent recorded for future removals, this is the moment. **STILL OPEN.**
3. ~~**Does `Universe.attributes` removal touch describe's schema?**~~ — **ANSWERED BY EXECUTION**, and
   it corrects the desk's earlier trace: **it does not.** Independently verified here —
   `documents.py:60` and `server/tools.py:76` emit **level** attributes (`l.attributes` / `lv.attributes`,
   "LOGICAL names only"); universe row-attributes (`u.attributes`) appear **only** at
   `documents.py:111` and `documents.py:156` — the physical_map builder and the no_physical_leak check,
   both map-side artifacts that never reach the wire. **Net: the wire loses only the `asserts` field.**
   Those two lines are added to commit 1's removal sites.

*DRAFT. Nothing built. Awaiting ratification of this plan and the five DRAFT strings.*
