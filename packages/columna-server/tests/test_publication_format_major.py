"""The server's supported publication major, and why this unit does not lift it.

RECORDED, NOT REPAIRED (Huayin, 2026-09-12), as part of the realization-freeze conformance unit.

`registry.SUPPORTED_PUBLICATION_FORMAT_MAJOR` is 1. The constant its own comment says it matches —
`manifold_agent.publication.PUBLICATION_FORMAT_VERSION` — is "2". So a current publication artifact
would be refused by this server.

WHY IT IS NOT THE SAME DEFECT AS THE MAPPING CONSTANTS, and why the difference puts it out of scope:

  · the mapping constants (`MAPPING_FORMAT_VERSION` / `SUPPORTED_MAPPING_FORMAT_MAJOR`) are a
    producer and a consumer in ONE module. A test compares them directly, and one now does —
    `columna-core/tests/test_mapping_format_constants.py`.

  · this consumer major must agree with a producer in a DIFFERENT, DELIBERATELY IMPORT-DISJOINT tree.
    `columna-server` may not import `manifold_agent`; the disjointness is test-enforced
    (`test_server_ingests_the_artifact_without_importing_manifold_agent`) and the v2 realization
    freeze rests on it. No in-process comparison can exist without breaking an invariant.

So the coherence cannot be asserted the way the mapping constants can, and whether the server SHOULD
accept publication major 2 is a COMPATIBILITY RULING — about which artifacts this build serves — not
a drift test. This file pins the current value so the gap keeps a name and a lift is deliberate.
"""
from columna_server.registry import SUPPORTED_PUBLICATION_FORMAT_MAJOR


def test_the_supported_publication_major_is_pinned():
    assert SUPPORTED_PUBLICATION_FORMAT_MAJOR == 1


def test_the_import_disjointness_that_makes_this_uncheckable_in_process_still_holds():
    """The reason a comparison test cannot be written. If this ever fails, revisit the decision."""
    import sys

    import columna_server.registry                                       # noqa: F401
    assert "manifold_agent" not in sys.modules
