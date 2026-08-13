# S2 — Closure checkpoint (2026-08-13)

Dated architectural state at the close of S2. This is a record of *what is settled*, not
implementation guidance; it complements `f0_reconnaissance.md`.

## Status

| Item | State |
|---|---|
| **S2.2b** | **CLOSED** |
| **S2** | **CLOSED** |
| main CI | GREEN |
| release coherence | **BLOCKED pending `columna` 0.15.0 publication** — pre-existing release-state condition, **not an S2 defect** |

Closed on merge of **PR #165** (`S2.2b-2: list_manifolds → governed-publication lineage
catalog`, contract v3), merge commit `d10830e`. Full core + server suite at close: 613 passed,
23 skipped.

## Release-coherence condition (tracked separately, does not reopen S2)

```
main source:   columna-core 0.15.0
PyPI release:  columna-core 0.14.0
site deploy:   "site build + deploy (shipped-coherent)" fail-closes on the mismatch
```

The `shipped-coherent` deploy wedge installs the **released** package from PyPI pinned to the
**current source** version and refuses to build the site against a version PyPI does not yet
have. `0.15.0` has never been published (Publish is release-tag-triggered; no `0.15.0` tag), so
the wedge fail-closes. This is **the wedge working as designed** — it reports that main is ahead
of the shipped package. It failed identically on the two prior merges (#164, #163).

Rulings (Huayin, 2026-08-13):
- The wedge is **not weakened or bypassed**; it stays visible until the next release.
- A later **`0.15.0` release discharges this condition independently**; it does not gate S2 closure.

## The S2 boundary that carries forward into Core-P1

Established and in force:

```
A. Semantic / physical lowering
     GovernedPublicationArtifact  (shared authority)
         + private Core realization / mapping
             → Core compiler
             → Core-private execution image
             → .cml serialization

B. Deployment / installation
     governed-publication.json + manifold.cml + operator deployment configuration
         → provisioner
         → runnable Core deployment unit
```

Governing invariants (permanent):
- **Meaning must exist before realization.** Mapping realizes meaning; it does not create it.
  Lowering translates established meaning; it does not recover or invent missing law.
- **No physical realization detail (table, column, schema, connection, join-key, provider,
  credential, path, runtime topology) may leak back into the authored Manifold** to make Core
  lowering easier.
- `.cml` is a **Core-private execution serialization**, not the shared boundary. The shared
  boundary is the `GovernedPublicationArtifact`. `SOURCE_MANIFOLD` inside `.cml` is a
  realization *claim*, checked against `artifact.ref`.

See `f0_reconnaissance.md` for the full evidence map and the Core-P1 boundary rulings.
