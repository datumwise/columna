# Editorial follow-up — link and provenance edits

**Applied 7 September 2026, after the J1/J2 staging at `9fce95f`.**

Kept deliberately separate from [`REVISION_METADATA.md`](REVISION_METADATA.md), which records the
**original J1/J2 replay evidence** and is preserved exactly as first written. The hashes recorded there
are the hashes of the J1/J2-corrected files *at that point*; this file records what happened to them
afterwards, so neither record has to be re-stated to stay true.

## What changed, and why

1. **Adopted reading paths.** The J1/J2 copies carried same-directory links to documents that live in
   `../reviewed_sources/`, so those links did not resolve from this directory. Every local link in an
   adopted copy is now repointed by one rule: **a target that has an adopted copy stays
   same-directory; a target this pass does not change points to `../reviewed_sources/`.** No archived
   file was edited to achieve this.
2. **Corrected source selection.** Three further documents were brought in as adopted copies because
   they needed adoption-facing edits: the Introduction v2.4, the Primer v2.3, and the authority index.
   The archived index selects the *uncorrected* baselines; the adopted one selects the corrected copies
   and says so in a header.
3. **Provenance.** The Introduction and Primer mastheads, and §4 of the adopted index, now separate
   three facts that were previously run together: what the original editorial pass had available; what
   was verified later against the deposited Markdown; and the exact transcription differences and
   successor edits. Evidence: [`PROVENANCE_EVIDENCE.md`](PROVENANCE_EVIDENCE.md).

## Hash trail

| file | starting point | before | after |
|---|---|---|---|
| `a_primer_on_frameql_v2_3_working_draft_v0_1.md` | reviewed baseline | `68c5d0dfa936728a5d277153918015c070d2b311683315b39d64dd60ccc7de1f` | `0cc40ae0ff6b77830e92c9ac3af339a1a0acbe8f683257a2d0131acf9d6adbdb` |
| `columna_o3_governed_analytical_order_v0_2.md` | J1/J2 copy at 9fce95f | `ae55b0bd4dd1b65feb41fc3db9f7a4d650e6654c53bbd60500fc8d3497dcb707` | `e3d38e0ac0e0f6ea51ea4f66134d6f7d87773c1a62208b986ecf33eb363d55a8` |
| `frameql_an_introduction_v2_4_working_draft_v0_1.md` | reviewed baseline | `efe432d2e95458a4924bf07a95c3089674ff8610a6a731ddbd113e61033a0e25` | `02b3a05300312227134943da9a850437bde81f7001d0519bcb2ba44f91e1fa2b` |
| `frameql_language_vnext_working_draft_v0_4.md` | J1/J2 copy at 9fce95f | `78e84a60ed825c4fdffe7beecc26099d34faaa3b15299536b65179389e5873ab` | `ef5e74980dc48b8337259a155a92843e9156645fdbce11a9dff80805c6be5df5` |
| `frameql_v7_1_authority_and_supersession_index_v0_1.md` | reviewed baseline | `d5eddcefe6adfdd79e0a5b2ef003158d8cc15cba597a8a2ec2c6ae97905252f4` | `2dc6b97a9378777774e952615cb17042e11d38f8174cf5312dafff88148a7818` |

The two files whose "before" is the J1/J2 copy are unchanged **in their J1/J2 content**: this pass
touched only link targets in them. The J1 and J2 replacement texts themselves are byte-identical to
what `REVISION_METADATA.md` records, and the archived reviewed sources they were derived from are
untouched.

## What was deliberately not done

No archived file was edited: `../reviewed_sources/`, `../historical_provenance/` and
`../editorial_archive/` are byte-identical to the packages they came from. No revision number or
edition was assigned to any document — that remains an adoption act. The ingest pipeline was not run
and `services/ask/deposits/manifest.json` was not edited. The two inherited Introduction paragraph
splits were **retained**; no rebuild was performed to undo them.
