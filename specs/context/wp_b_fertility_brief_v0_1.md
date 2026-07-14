# WP-B — Derivation fertility: declared, adjudicated, closed by default (v0.1)
**From: Huayin (drafted by the design session, 2026-07-14). For: Claude Code.**
**Against `main` (post-`76be279`). Required reading: audit v0.2 (B4, Forks 3/5),
`test_derivation.py` (the Phase-1 pins this WP must keep green or deliberately flip),
`structured_disclosure_capture.md` (the closed caveat vocabulary — see the S1a lesson),
execution-positions capture (v0.8 delta accompanies this brief).**

## Rulings this WP implements (Huayin, 2026-07-14 — record verbatim in the PR and the
## audit report's Fork 3 entry)
1. **Denotation (Fork 3, final):** a derived name at an anchor denotes its formula evaluated
   over co-anchored atoms at that anchor. Deterministic; serve-clean is correct (pinned in
   T1(b)). No engine-side clarify for this family; sentence-level ambiguity belongs to the
   translation layer, armed by describe.
2. **Fork 3(b), RULED — fertility is declared.** Fertility (ratified term): a derivation
   member's reduction along a lineage both commutes (mathematical gate) and is permitted
   (declared gate). Constitutional sentence: *authority is declared; mathematics may verify;
   data may only refute or corroborate; the default is closed.* Infertile by default —
   today's always-recompute behavior IS the default; this WP adds expressiveness, changes no
   shipped semantics.
3. **Adjudication verdicts (Certificate-kernel shape, per reference manual Part VI):**
   a declaration is VERIFIED (symbolic proof from formula tree + operator algebraic
   properties; timeless), else refutation-tested against attested data → CORROBORATED
   (survived; carries an attestation watermark; re-adjudicated on re-attestation) or
   CONTRADICTED (counterexample; **fails closed at publish** — the manifold does not
   publish), else UNTESTABLE (stands on authored authority; disclosed as asserted).
   Build the declare→adjudicate→verdict machinery in the generalizable shape — fertility is
   the Certificate layer's first customer, not a one-off (Fork 5 remains open for the rest).
4. **Family ruling:** a family of one is a family (`med_amount` precedent). On measures,
   family = askability, fertility = travel — deliberately distinct; do not touch measure
   semantics. On derived columns, family members are CREATED only by adjudicated fertility
   declarations, so there the two coincide by construction. Reuse the `FamilyMember` shape
   for derived members rather than inventing a sibling; extend with license metadata.
5. **Declared resolution anchor (separable feature, same WP):** make the alternative
   reading expressible as a DISTINCT metric whose meaning embeds the anchor (e.g. mean of
   daily rates). Infertility bars silent reduction, never reduction that is the declared
   meaning.
6. **Cache law (recorded now, consumed later):** only the fertile is cached; the fertile is
   cached as components first (policy). This WP exposes the license/verdict interface the
   Cacher will consume as its admission oracle; the Cacher itself is out of scope.
   "Fertile Cacher" as a name: REJECTED (Fork 1 blast radius; the law is the columns',
   not the component's).

## Scope

**B-1. Model (`model.py`).**
- `DerivedColumn` gains `family: dict` (member-name → `FamilyMember`-shaped entry) and an
  optional resolution-anchor field for ruling 5.
- A `License` record on derived family members: verdict (VERIFIED | CORROBORATED |
  UNTESTABLE — CONTRADICTED never persists past publish), basis (what proved/tested it),
  attestation watermark (None for VERIFIED), declared lineages. Shape it so a future
  `HIERARCHY`/`ASSERT` precondition could carry the same record — that is the
  Certificate-kernel requirement.
- Mirror symmetry to preserve: measures are open-by-default and `BLOCKED { lineage }`
  closes; derivations are closed-by-default and the fertility declaration opens.

**B-2. Parser (`parser.py`).** Two extensions, syntax mirroring what exists
(FAMILY/BLOCKED/ORDER). Proposal to bring to CP-B1 (do not finalize silently):
```
DERIVED net_revenue = revenue - refunds
    FAMILY { sum FERTILE { calendar store_geo } }

DERIVED daily_aov = revenue / orders AT day
    FAMILY { mean FERTILE { } }        # explicit: no travel; asked-at anchors reduce the
                                        # day-resolved series by the declared member
```
Exact keywords, whether `AT` rides the formula line, and the empty-FERTILE convention are
CP-B1 forks — propose, show alternatives, Huayin rules.

**B-3. Adjudication (publish time, in/beside `check_wellformed` + attestation).**
- *Math channel:* linearity/commutation detection over the formula AST + operator algebraic
  properties. The registry likely needs an algebraic-properties field per operator (linear,
  monoid-preserving, etc.) — an operator-registry extension; keep it signature-side
  (`OperatorSig`) so the two-projection split holds. Surface the exact property set at CP-B1.
- *Data channel:* refutation test at attestation — compute reduce-path vs recompute-path on
  attested data; any mismatch beyond tolerance ⇒ CONTRADICTED. Tolerance handling
  (exact for integer/decimal, epsilon for float?) is a CP-B1 fork.
- CONTRADICTED ⇒ publish fails with the counterexample named. Fail closed, loudly.

**B-4. Engine/planner query-time behavior per grade.**
- VERIFIED-fertile: reduction path licensed; serve clean.
- CORROBORATED-fertile: licensed; serve with the basis available in provenance.
- UNTESTABLE-declared: licensed; served with a disclosure that the license is asserted.
- Undeclared (default): recompute from components at target anchor — unchanged shipped
  behavior; T1(b) stays green.
- **Disclosure codes: do NOT mint.** Check `CATEGORY_TABLE`/`RESERVED_CODES` and propose the
  mapping at CP-B1 (candidate: `provenance` for the corroborated basis; the
  untestable-asserted case may fit an existing reserved code — report what fits, and if
  nothing does, that is a finding for Huayin, not a new code).
- Resolution-anchor metrics (`AT day`): evaluate the formula at the resolution anchor, then
  reduce by the declared member to the asked anchor. A distinct metric; no interaction with
  the pooled sibling.
- **The resolution ladder (capture amendment 4) governs serving:** lookup at A → recompute
  from components at A (the default; unchanged) → licensed reduction of finer values
  (optimization only; the license IS the equality theorem). Infertility deletes the third
  path and never creates a refusal paths 1–2 could serve. Materialized metrics (no formula)
  refuse via family/B-anchor when travel is unlicensed — the existing measure path; do not
  duplicate it.
- **Never substitute (capture amendment 5):** no code path may serve the pooled value for a
  requested mean-of-finer or vice versa. Add a test that attempts exactly this via the cache
  and asserts it cannot happen.
- **CP-B1 fork (new):** is inline reduction of a derivation (`avg(aov@day) @ month`) legal
  expression-language without a declaration? Once pinned it is fully determined; design
  lean: legal, with a communicative disclosure naming the reading — vs. declared-metrics-
  only. Unpinned (`avg(aov) @ month`) the input anchor is underdetermined in structure ⇒
  engine clarify enumerating candidate input anchors; include this clarify in the test set
  either way the fork is ruled.

**B-5. Describe surface (feeds Explorer tier 2 — the earlier tier-2 ruling: NAMED derived
metrics get describe objects).** Derived describe objects carry: formula; resolution anchor
if any; members with their licenses (verdict, basis, watermark, lineages). The license
interface here is the same one the Cacher will consume — build once.

**B-6. Tests (extend `test_derivation.py`; the audit's must-exist-first spirit).**
- Phase-1 pins stay green: hazard inheritance, serve-clean default (T1(b) — now cites
  ruling 1), dotted-member parse.
- New: declared linear combo → VERIFIED, reduce-path ≡ recompute-path on the fixture;
  declared ratio along sum → CONTRADICTED at publish, counterexample named, publish fails;
  a corroborated case (constructed data with no counterexample) → licensed + watermarked,
  then flipped to CONTRADICTED by a re-attestation with a counterexample row, license
  revoked, behavior degrades to recompute; `AT day` metric ≠ pooled sibling on the fixture
  (the two readings finally both expressible and distinct); measure families untouched
  (family-of-one `med_amount` regression pin); describe objects expose licenses.

## Out of scope, explicitly
Cacher build · Certificate generalization beyond the kernel (ASSERT/HIERARCHY/governance —
Fork 5 open) · any Fork 1 rename · measure-family semantics · any deploy.

## Checkpoints
- **CP-B1 (design, before construction):** syntax proposals, License shape, operator
  algebraic-property set, tolerance policy, disclosure-code mapping, wire/describe schema.
  Rendered, with alternatives, forks named.
- **CP-B2 (pre-merge):** full diff + test counts; both suites green per-package; PR cites
  this brief and records the rulings.
Estimated 3–5 days per the audit. Merge-first; the exception ledger file (`specs/
deploy_exceptions.md`) should land before or with this if not already done.
