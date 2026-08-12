"""
test_source_identity.py — the OPTIONAL `SOURCE_MANIFOLD <id> VERSION <semver>` statement
(columna#150, P0(b)).

The ruling (Huayin, 2026-08-10): keep `MANIFOLD ... VERSION <int>` — this engine artifact and its
integer engine/cache revision — UNCHANGED, and add an ADDITIVE source-identity reference to the
PUBLISHED governed Manifold a lowering came from. It is a third, distinct identity dimension: a
stable id AND a semantic version, an atomic pair. Guardrails exercised here:

  1. not derived  — the source id is NOT the MANIFOLD name; retained only when authored.
  2. atomic pair  — id-without-version and version-without-id are ungrammatical (one statement).
  3. legacy loads — a .cml without the statement parses; its retained source identity is None.
  5. exact retain — parse → model keeps id and semver byte-identical (opaque to columna).

(Guardrail 4 — a Studio lowering MUST emit it — lives on the manifold-agent side, not the parser:
the parser accepts a legacy artifact; the lowerer, which knows it is minting a governed artifact,
is the one that fails when the pair is absent.)
"""
import pytest

from columna_core.parser import parse_manifold, ParseError

# A minimal well-formed manifold body the source-identity statement rides on. The MANIFOLD name
# (`retail`) is deliberately DIFFERENT from the source id below, so a "derive id from name" fallback
# would be caught (guardrail 1).
_BODY = """
UNIVERSE u = a
LEVEL a = a_id BASE
MEASURE m ON u FROM t AS sum(t.x)
"""


def _mf(header: str):
    return parse_manifold(header + "\n" + _BODY)


# ---- retention: parse keeps the exact pair, distinct from the integer engine revision --------------

def test_source_identity_retained_verbatim():
    m = _mf("MANIFOLD retail VERSION 17\nSOURCE_MANIFOLD retail-catalog-9f3a VERSION 1.2.0")
    assert m.version == 17                                   # the integer engine/cache revision, untouched
    assert m.source_manifold_id == "retail-catalog-9f3a"     # the stable published id, verbatim
    assert m.source_manifold_version == "1.2.0"              # the SEMANTIC publish version, verbatim


def test_source_id_is_not_derived_from_manifold_name():
    # name `retail` != source id; the parser must not conflate them (guardrail 1).
    m = _mf("MANIFOLD retail VERSION 17\nSOURCE_MANIFOLD some-other-id VERSION 3.0.1")
    assert m.name == "retail"
    assert m.source_manifold_id == "some-other-id"


def test_semver_prerelease_and_build_kept_verbatim():
    m = _mf("MANIFOLD retail VERSION 1\nSOURCE_MANIFOLD id VERSION 2.4.0-rc.1+build.7")
    assert m.source_manifold_version == "2.4.0-rc.1+build.7"


# ---- guardrail 3: a legacy artifact loads with NO retained source identity (not an invented one) ---

def test_legacy_cml_has_no_source_identity():
    m = _mf("MANIFOLD retail VERSION 17")
    assert m.source_manifold_id is None
    assert m.source_manifold_version is None


# ---- guardrail 2: the pair is atomic — the single statement carries both, or it is ungrammatical ---

def test_source_id_without_version_is_rejected():
    with pytest.raises(ParseError, match="SOURCE_MANIFOLD"):
        _mf("MANIFOLD retail VERSION 17\nSOURCE_MANIFOLD lonely-id")


def test_non_semver_source_version_is_rejected():
    # a bare integer is the ENGINE version's shape, not a semantic version — fail closed.
    with pytest.raises(ParseError, match="SOURCE_MANIFOLD"):
        _mf("MANIFOLD retail VERSION 17\nSOURCE_MANIFOLD id VERSION 7")


def test_garbage_source_version_is_rejected():
    with pytest.raises(ParseError, match="SOURCE_MANIFOLD"):
        _mf("MANIFOLD retail VERSION 17\nSOURCE_MANIFOLD id VERSION banana")


def test_duplicate_source_manifold_is_rejected():
    with pytest.raises(ParseError, match="duplicate SOURCE_MANIFOLD"):
        _mf(
            "MANIFOLD retail VERSION 17\n"
            "SOURCE_MANIFOLD first VERSION 1.0.0\n"
            "SOURCE_MANIFOLD second VERSION 2.0.0"
        )


# ---- the existing integer VERSION grammar is untouched (the ruling's central constraint) -----------

def test_manifold_integer_version_unchanged_without_source():
    m = _mf("MANIFOLD retail VERSION 17")
    assert m.version == 17 and isinstance(m.version, int)
