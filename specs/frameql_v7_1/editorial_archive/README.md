# Editorial archive — provenance for the reviewed successor set

**Staged 7 September 2026 as evidence. Nothing in this directory is an instruction.**

The staged working set and the joint review's own index repeatedly say that superseded inputs "remain
intact in the editorial archive" — J2's added note says it of O3 v0.1, and the authority index says it
of thirteen further files. This directory is that archive, so those references resolve inside the
repository instead of pointing at something absent.

## Status — read this before reading anything here

Every file under `sources/` is **historical evidence at its own snapshot.** None of it is current
design authority, and none of it authorizes work. In particular the withdrawn categorical
FIRST/LAST-family exclusion, the universal formation-locality veto, and the older compulsory-migration
recommendations appear here in their original form **because they were withdrawn**, and must not be
reactivated by citation. `FRAMEQL_VNEXT_M2_CC_RECONNAISSANCE.md` and
`FRAMEQL_VNEXT_O2_CC_DESIGN_RECONNAISSANCE.md` are historical mission texts; they are not reusable
authorizations.

Superseding a recommendation does not rewrite an observed historical implementation fact. Where these
reports recorded reproduced behaviour, that behaviour remains reported.

## The provenance chain, verified

`output/` here is the editorial build's own product. All **twelve** markdown documents in it are
**byte-identical** to `../reviewed_sources/`, which is in turn byte-identical to the joint review
package. So the chain editorial build → joint review → repository staging is unbroken and checkable
by hash at every link.

## Predecessor-source finding (the §4 question)

The two transcriptions under `sources/` were compared against the repository's predecessor sources,
which were themselves verified today against the Zenodo deposit bytes.

| document | transcription vs deposit-verified source |
|---|---|
| *A Primer on Frame-QL* v2.2 | **byte-identical** — sha256 `5555940b…`, 9,295 bytes, 250 lines, both sides |
| *Frame-QL: An Introduction* v2.3 | **content-identical, structurally divergent**: 3,988 word tokens on both sides with **not one word changed**, all 16 fenced blocks byte-identical — but three long paragraphs are split in two, giving +3 paragraph blocks, +6 lines, +3 bytes |

Two of those three splits propagated into the proposed Introduction v2.4 successor; the third fell in
a paragraph the successor revises anyway. The divergence is editorial, not semantic, and it is
recorded here rather than silently normalised away.

The archive's own note calls this "blank-line and paragraph whitespace normalized". That is accurate
for the Primer and slightly generous for the Introduction: introducing a paragraph break is a
structural edit rather than a normalisation, even when no word moves.

## What was omitted from this staging, and why

The editorial package's three PNG render previews (`audit/*.png`, ~445 KB) are not staged. They are
rendering artifacts of the build, carry no textual provenance, and nothing cites them. Every other
file from the package is present, including the build scripts, so the generation record is intact.
