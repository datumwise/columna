# firstlight — provenance

## What this fixture proves, and what it does not

**This fixture ships a governed publication that Columna can serve but cannot make.** The authoring
and ratification machinery that produced it is not part of this release. What is demonstrated here is
consumption of governed authority, not its production.

Columna can compile this publication, bind the image to it, provision a runtime unit, admit it as
governed and serve it — all through the generic shipped machinery, with no branch anywhere that
knows this fixture's name. It cannot author a Manifold, and it cannot ratify an existence law.

## Why this file exists

The governed publication format is **structural authority transfer, not cryptographic authenticity**:
no hash, no signature, and a closed schema of `{publication_format_version, ref, logical, authority}`
carrying no producer version or commit. So the identity of the software that produced this artifact
cannot live inside it, and is recorded here instead. This is a record, not an attestation.

## The publication

| | |
|---|---|
| ref | `firstlight@1.0.0` |
| produced by | **manifold-agent v0.12.0** @ `df794a60f5b234f9bb08d1fc85d9dfb081d10316` |
| driven through | **columna-studio** @ `244fd34b05e4fd6de31d018b90cdc8eb07fefc98` |
| published_at | `2026-08-22T22:33:14.252017+00:00` |
| published_by | Huayin Wang |
| ratification | universe `sales`, `elf-1` fingerprint, ratified by Huayin Wang at 2026-08-22T00:00:00Z |

The pinned manifold-agent commit is the one the `v0.12.0` tag and columna-studio's dependency pin
both point at — not a later local HEAD.

The publication was minted through the real governed-publish path: `ratify_existence_law` (the one
human mint primitive) → `stamp_source_identity` (the P0(c) gate, which refuses an unratified or
stale universe) → `Library.publish`. Nothing was hand-authored; a hand-written
`governed-publication.json` would look identical and prove nothing.

**It is not byte-reproducible, by design.** `published_at` is stamped from the wall clock at
publication, so re-running the producer yields different bytes and a different publication digest.
That is why the artifact was produced once and is thereafter immutable, and why every downstream
guard reads these committed bytes rather than re-minting them.

## The execution image

| | |
|---|---|
| compiled by | `columna_core.compiler.compile_k0` |
| columna | **0.16.1** |
| columna-core | **0.16.1** (code identity `0.16.0-core`) |
| columna-server | **0.10.0** (provisioner) |

Unlike the publication, the image **is** byte-reproducible: recompiling the committed publication
against the committed private mapping reproduces `manifold.cml` byte for byte, and a test asserts it.

## Reproducing

```
# runtime stage — needs only a released columna
python packages/columna-server/fixtures/firstlight/build.py --stage runtime

# producer stage — needs manifold-agent (private) at the pin, and columna-studio
python packages/columna-server/fixtures/firstlight/build.py --stage producer \
    --manifold-agent <checkout at df794a6> --columna-studio <checkout>
```

The producer stage refuses to run against any commit other than the pin.

## The private mapping

`private-core-mapping.json` lives in the repository as a reproduction input. It is **not** shipped in
the wheel and **not** part of the runtime unit: it is not governed publication, not a runtime
authority input, and never consulted by server admission. No secrecy claim is made about it — this is
synthetic fixture data, and the physical facts it names are the fixture's own public parquet columns,
already visible in the shipped `manifold.cml`.
