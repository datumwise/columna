# C1 · The native-v3 reader, and nothing else — implementation record

**2026-09-22.** Unit C1 of the five-unit consumer sequence
(`manifold-agent/docs/native_v3_consumer_recon_v0_1.md` §13). **Reader only: no serving, no
Platform, no engine, no compilation, no producer change.** `columna-server`, `columna-platform` and
every legacy engine surface are byte-unchanged; the full `columna-core` suite is green at 1864
passed / 50 skipped.

**Stop-gate, as stated:** *"the shipped native fixture parses, its geometry is derived, all four
currency claims verify, and a tampered constitution refuses."* All four are witnessed by
`packages/columna-core/tests/test_native_v3_reader.py` (41 tests).

---

## 1 · What was built

`packages/columna-core/src/columna_core/governed/native.py` — a **separate reader with a separate
model**, beside `publication.py` (v2) and never inside it. It yields the §5 resolved model:

| § | object | how it is reached |
|---|---|---|
| N1 | `Universe(constitution, denotations, conformance, attestation)` | read |
| N2 | `Anchor`, `root_anchor`, `scalar_anchor`, `constituent_anchors`, `refines`, `projection_forgets`, `union` | **computed on every access; never read, never stored** |
| N3 | `Anchor(universe, frozenset[constituent])` | `universe.denote(token)`, or `universe.anchor(request_coordinates)` |
| N4 | `NativePublication.resolve(ref) -> Resolution(family, universe, anchor)` | `F → U → A`, in that order, always inside `U` |
| N5 | `NativePublication.currency() -> CurrencyReport` | four claims, all from the bytes |

**The four currency claims, measured against the shipped fixture:**

```
elf-2 attestation    harbour        CURRENT        elf-2 recomputes to f077c0e15f4af4ff…
F4 coverage          harbour        COVERED        6 asserted, 6 raised by this constitution
U-authority binding  berthings      BOUND          cites the attestation carried on 'harbour'
fcf-2 constitution   berthings      CURRENT        recomputes to 38546850c5f83933…
U-authority binding  moorings       UNBOUND        no binding claimed; not BOUND and not equivalent standing
fcf-1 constitution   moorings       CURRENT        recomputes to cecffbe222b7bda6…
```

**The derived geometry, measured:**

```
constituents                 : ['berth', 'day'] | closed: True
R_U   (theorem of closure)   : harbour{berth, day}
{}    (scalar anchor)        : harbour{}
constituent anchors          : {'berth': ['berth'], 'day': ['day']}
refines(berthing_at,by_berth): True
projection forgets           : ['day']
berthing_at == berth_day     : True   synonyms: ['berth_day', 'berthing_at']
```

---

## 2 · What native meaning is now consumed

Everything the v2 path discarded silently. Under `parse_publication` the same bytes report *"a
universe stating no law"* with `{}` authority; under this reader the constitution, its closed
individuation, λ_U's three facts, the premises, the conformance judgment, the `elf-2` attestation,
the Case-S denotation table, the family constitution authorities and the U-authority binding are
all **named, resolved and checked**.

Two consequences beyond mere visibility:

* **Synonyms collapse.** `berthing_at` and `berth_day` are one `Anchor`. The v2 consumer's refusal
  — *"this profile will not choose between two governed anchors"*, marked `# pragma: no cover`
  because the case *"cannot be built from a publication this proof is authorized to write"* — is
  the **ordinary case** in a lawful native artifact, and it does not arise here at all, because
  a request's coordinate set **is** the anchor. Ruling 11 lands on the consumer side as a
  simplification.
* **Universe scoping stopped being a rule.** `Anchor` carries its universe, so comparing two
  across worlds *refuses*, and no publication-global anchor index can be constructed. Ruling 1 is
  satisfied structurally rather than by policy.

## 3 · Which legacy assumptions disappeared

Not deprecated — **unreachable from this model**, because there is nowhere to put them:

`anchor` declarations · the publication-global anchor-name map · `universe.body.anchor` · `basis` ·
`LEVEL` / `HIERARCHY` · the global coordinate namespace · `logical` as an envelope · the top-level
`authority` section with its two identity spaces · name-matching as the anchor-resolution mechanism
· physical grain, mappings and `unique_at` evidence as inputs to `A`.

**Nothing legacy was removed, renamed or repaired** (ruling 8): `compile_v2`, the v2 reader's
silent acceptance (P2-01, ruling 6), movement licences and publication-global anchors are all
untouched and still ship. No demolition during construction.

## 4 · Rulings honoured, explicitly

1. **No `compile_v3`.** Nothing in C1 compiles, emits `.cml`, or synthesizes a basis, a
   `universe.body.anchor`, an anchor declaration, a LEVEL or a HIERARCHY. Nothing needed one.
2. **P1-34** — not touched, not revived in native form.
3. **P1-33** — held. The geometric half of its distinction is implemented and named
   (`projection_forgets` answers *does the target location exist*); the **governed movement
   standing half is deliberately absent**, and the docstring says so at the site.
4. **Law(F) as candidate boundary** — C1 does not reach it and asserts nothing about it. §5 below
   records what C1 observed that bears on it.
5. **v3 read as v3.** The reader refuses `"2.x"` with a v2-specific reason, refuses a bare major,
   and refuses an unrecognised minor. A v2-shaped artifact wearing a `"3.0"` label is refused on
   its **shape**. Nothing relabels, wraps or downgrades.
6. **P2-01 not repaired.** The v2 reader is unchanged. What C1 does is *not reproduce* the defect:
   `_strict` is applied at the declaration **envelope**, which is the one site v2 omits.
7. **No carrier/type information** anywhere in this module. §5 records the one place the question
   will next present itself.
8. **No cleanup.** Nothing obsolete was deleted.
9. **No producer change.** `manifold-agent` is byte-unchanged. No missing governed fact was found.
10. **Holds preserved.** Universe identity/equality, Case G, carve, membership universes and
    cross-universe correspondence are untouched; comparing anchors across universes refuses rather
    than guessing.

---

## 5 · Findings to carry into C2

**F-1 · The consumer is a SECOND implementation of the canonicalization contract, and that is
structural.** `elf-2`, `fcf-1` and `fcf-2` are recomputed here from the governed facts, because the
consumer may not import the producer (disjointness is test-enforced) and the recon's load-bearing
fact is that the artifact is sufficient on its own. Both derivations reproduce all three shipped
digests exactly. **The standing obligation:** the shipped fixture is the only witness that the two
implementations agree, so a producer-side canonicalization change that does not also update the
fixture would be caught late. Recorded, not repaired — the alternative (a shared published
canonicalization spec, or a conformance-vector file the producer emits) is a decision, not an
implementation detail.

**F-2 · The consumer checks one thing the producer's READER does not.** `parse_native_publication`
on the producer side validates the universe attestation and the binding, but not the family
constitution fingerprint; the producer's **builder** enforces it before publishing. C1 checks it at
read, as N5's fourth claim. A conforming artifact satisfies it; a hand-edited one does not.

**F-3 · Fixture debt, deliberately incurred.** `packages/columna-core/tests/fixtures_v3/native-v3-publication.json`
is a byte copy of the producer's shipped fixture, following the existing
`fixtures_v2/lighthouse-v2-publication.json` precedent. There is no drift guard across the two
repositories. Same class as the recorded Lighthouse debt; it did not obstruct any fact here.

**F-4 · Nothing below the reader was consulted, and nothing asked to be.** No legacy anchor
declaration, global coordinate namespace, `basis` or `universe.body.anchor` was needed to produce
the resolved model — which is the first, weakest piece of evidence bearing on ruling 4. It is
evidence about the READER only; the convergence question is C2/C3's to answer.

**F-5 · The coordinate-type question did not arise, as predicted.** Nothing in reading, resolving
or checking the artifact needed a carrier type. It will next present itself at C4's realization
boundary, not before.
