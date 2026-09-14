"""OF-57 — the realization axis is the ASSERTION REVISION, faithfully (ruled Huayin, 2026-09-14).

THE TWO LEVELS, AND WHY BOTH CONTROLS MATTER.

    RESPONSIBILITY   publication_ref + kind + subject. Does NOT move when the endpoint, grain,
                     operators or exactness change — those are revisions of one responsibility's
                     claim, not a different claimant.
    REVISION         the complete content asserted. ANY content-bearing change moves it.

THE DEFECT THESE REPLACE. `Standing.realization` was hand-concatenated from five things out of the
claim's six content-bearing facts, so `continuation_operator` sum -> wildly_wrong and
`formation_operator` None -> min both produced a BYTE-IDENTICAL standing and combined. The repair is
not "add the two fields": completeness is now DERIVED from the parsed claim's own dataclass fields,
so a field added later enters the identity without anyone remembering.

WHAT IS DELIBERATELY NOT ASSERTED HERE. Nothing about who asserted the claim (attestation is a
separate open jurisdiction), nothing about whether the claim is still true of the source (currency
likewise), and no cryptographic property. The digest resists ACCIDENT, not a forger.
"""
from __future__ import annotations

import dataclasses
import json

import pytest
from columna_platform import assertion, serving
from columna_platform.refusals import WantOfCompatibility
from columna_platform.state import RetainedStateStore

from conftest import PUBLICATION

REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"


@pytest.fixture(scope="module")
def pub():
    p, _views = serving.open_publication(PUBLICATION)
    return p


@pytest.fixture(scope="module")
def claim(pub):
    return serving.realize(serving.bind(pub, str(_MAPPING)), REVENUE)


_MAPPING = (__import__("pathlib").Path(__file__).parents[1]
            / "fixtures" / "proof_a" / "private-core-mapping-v2.json")


def _rev(pub, claim, **changes):
    return assertion.revision(pub.ref, dataclasses.replace(claim, **changes) if changes else claim)


def _endpoint(pub, claim, **changes):
    return assertion.revision(pub.ref,
                              dataclasses.replace(claim,
                                                  endpoint=dataclasses.replace(claim.endpoint, **changes)))


# ══ completeness is derived, not listed ═══════════════════════════════════════════════════════

def test_every_content_bearing_field_of_the_claim_enters_the_revision(pub, claim):
    """THE PIN THAT MAKES THIS REPAIR DIFFERENT FROM 'ADD THE TWO MISSING FIELDS'.

    Every dataclass field of the parsed claim must be content-bearing here unless deliberately
    named as encoding metadata. A field added to the realization format therefore enters the
    identity automatically — and if someone adds one that should NOT, this test makes them say so
    explicitly rather than silently omitting it."""
    declared = {f.name for f in dataclasses.fields(claim)}
    assert set(assertion.content_fields(claim)) == declared - assertion._NOT_CONTENT
    for omitted in ("formation_operator", "continuation_operator"):
        assert omitted in assertion.content_fields(claim), f"{omitted} is the OF-57 witness"


def test_changing_ANY_content_field_changes_the_revision(pub, claim):
    """THE PIN THAT ACTUALLY BINDS THE COMPUTATION, and it exists because the one above did not.

    A first draft checked only `content_fields()` — the helper. Mutating `revision()` to drop the
    two operators left that check GREEN, because the helper and the computation were two places
    saying the same thing and only one of them was mutated. This test drives the real function over
    every declared content field, so an omission ANYWHERE in the derivation fails here.

    The mutation values are generated from the field, not listed, for the same reason the field set
    is: a hand-written list is the mechanism that produced OF-57."""
    base = assertion.revision(pub.ref, claim)
    for name in assertion.content_fields(claim):
        current = getattr(claim, name)
        if dataclasses.is_dataclass(current):                      # the endpoint
            inner = dataclasses.fields(current)
            for f in inner:
                altered = dataclasses.replace(current, **{f.name: _other(getattr(current, f.name))})
                assert assertion.revision(
                    pub.ref, dataclasses.replace(claim, endpoint=altered)) != base, \
                    f"endpoint.{f.name} does not enter the revision"
            continue
        assert assertion.revision(
            pub.ref, dataclasses.replace(claim, **{name: _other(current)})) != base, \
            f"{name} does not enter the revision"


def _other(value):
    """A value guaranteed to differ from `value`, whatever it is."""
    return "of57-sentinel" if value != "of57-sentinel" else "of57-sentinel-2"


@pytest.mark.parametrize("field,value", [
    ("grain", "not-coincident"),
    ("exactness", "approximate"),
    ("formation_operator", "min"),
    ("continuation_operator", "wildly_wrong"),
])
def test_a_content_bearing_change_produces_a_different_revision(pub, claim, field, value):
    """The two operators are the measured OF-57 witnesses: each of them produced an IDENTICAL
    standing before this repair."""
    assert getattr(claim, field) != value
    assert _rev(pub, claim) != _rev(pub, claim, **{field: value})


@pytest.mark.parametrize("field,value", [
    ("connection", "somewhere-else"),
    ("table", "other_table"),
    ("column", "other_column"),
    ("schema", "other_schema"),
    ("schema", None),
])
def test_an_endpoint_change_produces_a_different_revision(pub, claim, field, value):
    """Including `schema -> None`. A null schema is a POSITIVE ruled claim — "no schema
    qualification applies" — not an absent field, so it must be distinguishable from every name."""
    assert getattr(claim.endpoint, field) != value
    assert _rev(pub, claim) != _endpoint(pub, claim, **{field: value})


def test_a_null_schema_is_not_the_string_null(pub, claim):
    """The specific collision a looser encoding would allow. A schema literally named `null` and a
    schema qualification that does not apply are different claims."""
    assert _endpoint(pub, claim, schema=None) != _endpoint(pub, claim, schema="null")
    assert _endpoint(pub, claim, schema=None) != _endpoint(pub, claim, schema="None")


# ══ canonical: how it was written must not matter ════════════════════════════════════════════

def test_serialization_differences_alone_do_not_change_the_revision(pub, claim):
    """Key order and whitespace in the producer's document are encoding, not content. Two mappings
    that assert the same thing differently spelled must fingerprint identically."""
    doc = json.loads(_MAPPING.read_text(encoding="utf-8"))

    shuffled = {
        "realizations": [{k: r[k] for k in sorted(r, reverse=True)} for r in doc["realizations"]],
        **{k: doc[k] for k in doc if k != "realizations"},
    }
    import tempfile, pathlib
    tmp = pathlib.Path(tempfile.mkdtemp()) / "m.json"
    tmp.write_text(json.dumps(shuffled, indent=7, sort_keys=False), encoding="utf-8")

    other = serving.realize(serving.bind(pub, str(tmp)), REVENUE)
    assert assertion.revision(pub.ref, other) == assertion.revision(pub.ref, claim)


def test_the_revision_is_namespaced_and_incomparable_schemes_do_not_read_as_equal(pub, claim):
    """A fingerprint under another scheme must be a DIFFERENT string, so it can never compare equal
    to one under this scheme. Incomparable reads as changed — never as agreement."""
    got = assertion.revision(pub.ref, claim)
    assert got.startswith(assertion.ASSERTION_SCHEME + ":")
    assert len(got.split(":", 1)[1]) == 32          # blake2b-16, hex


# ══ responsibility vs revision ════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("field,value", [
    ("grain", "not-coincident"), ("exactness", "approximate"),
    ("formation_operator", "min"), ("continuation_operator", "wildly_wrong"),
])
def test_content_changes_do_not_change_the_RESPONSIBILITY(pub, claim, field, value):
    """A revision of one responsibility's claim is not a different claimant."""
    changed = dataclasses.replace(claim, **{field: value})
    assert assertion.responsibility(pub.ref, changed) == assertion.responsibility(pub.ref, claim)


def test_the_subject_changes_the_RESPONSIBILITY_not_merely_the_revision(pub, claim):
    """A different family is a different responsibility, and both levels must say so."""
    other = dataclasses.replace(claim, family_id="fam_Zx4TgM6oBvNqUeS3rKhDyw")
    assert assertion.responsibility(pub.ref, other) != assertion.responsibility(pub.ref, claim)
    assert assertion.revision(pub.ref, other) != assertion.revision(pub.ref, claim)


def test_the_responsibility_is_readable_and_names_its_publication(pub, claim):
    """An address, not a digest: an operator reading a refusal should see whose claim is at issue
    without a lookup table."""
    got = assertion.responsibility(pub.ref, claim)
    assert got == f"{pub.ref.manifold_id}@{pub.ref.version}/family/{REVENUE}"


def test_a_different_publication_is_a_different_responsibility_and_revision(pub, claim):
    """The claim is ABOUT a publication; the same content under another frame of reference is not
    the same assertion."""
    other_ref = dataclasses.replace(pub.ref, version="9.9.9")
    assert assertion.responsibility(other_ref, claim) != assertion.responsibility(pub.ref, claim)
    assert assertion.revision(other_ref, claim) != assertion.revision(pub.ref, claim)


# ══ authorless, and provenance-free ═══════════════════════════════════════════════════════════

def test_the_revision_is_authorless(pub, claim):
    """Assertion identity says WHAT was claimed, never WHO claimed it. Attestation is a separate
    open jurisdiction and must not be acquired here by accident — so no author-bearing input
    exists to change the answer, and this control records that as a property rather than a hope."""
    import inspect
    src = inspect.getsource(assertion)
    for forbidden in ("author", "signer", "signature", "asserted_by", "established_by",
                      "certificate", "ratified_by"):
        assert f"{forbidden}=" not in src and f'"{forbidden}"' not in src, forbidden


def test_provenance_and_timestamps_cannot_enter_the_revision(pub, claim):
    """`mapping_provenance` is opaque, non-binding and never consulted; a revision that moved with
    it would make it load-bearing by the back door."""
    assert "mapping_provenance" not in assertion.content_fields(claim)
    assert "established_at" not in assertion.content_fields(claim)


# ══ the standing, and what it does and does not change ════════════════════════════════════════

def test_analytical_identity_is_unchanged_when_only_the_revision_changes(revenue, pub):
    """IDENTITY vs COMPATIBILITY, again — the same distinction #316 pinned for the constitution.
    A different realization revision is still a state OF the same analytical thing."""
    family, view, real = revenue
    store = RetainedStateStore()
    from test_proof_a_lawful import _materialize
    # NOTE the realization is passed POSITIONALLY. An earlier draft passed `realization=...` as a
    # keyword, which `_materialize` swallows into **kw and ignores — the test then compared a state
    # against itself and passed for the wrong reason. Left recorded because it is the exact shape
    # of mistake these controls exist to catch.
    a = _materialize(family, view, real, store)
    b = _materialize(family, view, dataclasses.replace(real, continuation_operator="wildly_wrong"),
                     store)
    assert a.identity == b.identity


def test_compatibility_detects_a_different_realization_revision(revenue, pub):
    """THE MEASURED WITNESS, NOW A CONTROL. Before the repair these two combined."""
    family, view, real = revenue
    store = RetainedStateStore()
    from test_proof_a_lawful import _materialize
    a = _materialize(family, view, real, store)
    b = _materialize(family, view, dataclasses.replace(real, continuation_operator="wildly_wrong"),
                     store)

    assert a.standing.realization != b.standing.realization
    assert a.standing.comparable_to != b.standing.comparable_to
    with pytest.raises(WantOfCompatibility):
        store.combine(a, b)


def test_two_states_of_the_same_revision_still_combine(revenue):
    """The positive, asserted so the repair is not simply refusing everything."""
    family, view, real = revenue
    store = RetainedStateStore()
    from test_proof_a_lawful import _materialize
    a, b = _materialize(family, view, real, store), _materialize(family, view, real, store)
    assert a.standing.comparable_to == b.standing.comparable_to
    assert store.combine(a, b).identity == a.identity


def test_combine_is_still_unreachable_from_the_serving_path():
    """Unchanged by this repair, and asserted so it stays that way."""
    import pathlib
    root = pathlib.Path(serving.__file__).resolve().parents[3]
    callers = [p for p in root.rglob("src/**/*.py")
               if ".combine(" in p.read_text(encoding="utf-8")
               and p.name not in ("state.py", "planner.py")]
    assert callers == []
