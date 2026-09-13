"""The mapping-format constants may not drift apart.

THIS IS A CODE INVARIANT, NOT A PROSE STAMP, and the distinction is the point (v2 realization freeze
§10). The currency guard renders a template from the shipped state and asserts the literal appears in
a file: it compares PROSE TO SHIPPED STATE. It has no mechanism for comparing two constants to each
other, and giving it one would make it something other than what it is. So the two checks are
separate, and this file is the second one.

Each mapping reader carries a PRODUCER constant and a CONSUMER constant:

    MAPPING_FORMAT_VERSION           the version a producer writes    ("1" / "2")
    SUPPORTED_MAPPING_FORMAT_MAJOR   the major a reader accepts       ( 1  /  2 )

They must agree, and until now nothing compared them. Two constants that must agree with nothing
comparing them is not a hypothetical failure mode — see `test_the_server_publication_major_is_a
_different_dimension` below for a live case of exactly that shape, which this unit deliberately does
NOT fix.
"""
import pytest

from columna_core.compiler import inputs as v1
from columna_core.compiler import realization as v2


@pytest.mark.parametrize("module,name", [(v1, "v1 (inputs)"), (v2, "v2 (realization)")])
def test_the_producer_and_consumer_constants_agree(module, name):
    written = module.MAPPING_FORMAT_VERSION
    accepted = module.SUPPORTED_MAPPING_FORMAT_MAJOR

    assert written.isdigit(), f"{name}: MAPPING_FORMAT_VERSION is a bare major, not {written!r}"
    assert int(written) == accepted, (
        f"{name}: a producer writes mapping_format_version {written!r} and this reader accepts only "
        f"major {accepted}. One of the two moved without the other.")


@pytest.mark.parametrize("module,expected", [(v1, 1), (v2, 2)])
def test_each_reader_accepts_exactly_its_own_major(module, expected):
    """Pinned so a lift is a deliberate edit here, not a silent consequence elsewhere."""
    assert module.SUPPORTED_MAPPING_FORMAT_MAJOR == expected


def test_the_two_readers_are_different_majors():
    """v1 and v2 are distinct formats read by distinct modules; neither may drift onto the other."""
    assert v1.SUPPORTED_MAPPING_FORMAT_MAJOR != v2.SUPPORTED_MAPPING_FORMAT_MAJOR


def test_a_mapping_of_the_other_major_refuses(tmp_path):
    """The constants are not decorative — they are what the reader enforces."""
    from columna_core.compiler.realization import parse_mapping
    from columna_core.compiler.refusals import CompileRefusal

    with pytest.raises(CompileRefusal, match="major"):
        parse_mapping({"mapping_format_version": "1",
                       "publication_ref": {"manifold_id": "m", "version": "1.0.0"},
                       "realizations": []})


# THE ANALOGOUS SERVER CONSTANT IS A DIFFERENT DIMENSION, and its test lives in the SERVER package
# (`test_publication_format_major.py`) rather than here — a columna-core test that imports
# columna_server would make core's suite depend on a package it does not depend on, to assert a fact
# about that package. See there for why it is recorded rather than repaired.
