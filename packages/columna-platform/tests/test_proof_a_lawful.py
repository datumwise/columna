"""THE POSITIVE CONTROL.

A governed identity and its standing survive materialization and are served WITHOUT THE PHYSICAL
CARRIER REDEFINING THEM.
"""
from decimal import Decimal

from columna_platform import assertion, carrier, serving
from columna_platform.state import AnalyticalIdentity, RetainedStateStore

from conftest import PUBLICATION


def _publication():
    """The publication object, read once per call. Cheap, and the alternative — caching it in a
    module global — would make two tests share a frame of reference they did not each establish."""
    pub, _views = serving.open_publication(PUBLICATION)
    return pub


def _constitution():
    """READ FROM THE PUBLICATION (OF-39). The literal that stood here was the COUNT family's."""
    return serving.constitution_of(_publication(), "fam_qv8Ky3mR7bTpZa1LwXcNdg")


def _materialize(family, view, real, store, **kw):
    return serving.materialize(
        family, view, real, kw.pop("carrier_obj", carrier.exact_money()),
        basis=view["sufficient_state_bases"].value,      # DERIVED BY THE GOVERNED LAYER, passed in
        constitution=kw.pop("constitution", _constitution()[0]),
        constitution_scheme=kw.pop("scheme", _constitution()[1]),
        currency=kw.pop("currency", "tok-1"),
        store=store,
        publication_ref=kw.pop("publication_ref", _publication().ref),
    )


def test_the_lawful_case_serves_through_the_real_wire(revenue):
    """THE ACCEPTANCE CRITERION: out through `disclosure_wire`, not a Proof-A-shaped imitation."""
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, family.constitutive_anchor))

    assert w["contract_version"] == "5"          # the REAL contract, unmodified
    assert w["outcome"] == "serve"
    assert w["frame"]["anchor"] == ["sale_at"]
    assert w["executed"] is True
    assert w["columns"][0]["status"] == "served"
    assert len(w["columns"][0]["values"]) == 3


def test_the_governed_decimal_reaches_the_wire_unfloated(revenue):
    """The ruling's first half, all the way out: no binary float anywhere on the path."""
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    w = serving.decide(view, store, AnalyticalIdentity(family.family_id, family.constitutive_anchor))

    values = [v["value"] for v in w["columns"][0]["values"]]
    assert str(values[0]) == "12345678901234.5678"
    assert not any(isinstance(v, float) for v in values)


def test_the_governed_domain_is_carried_exactly_not_lowered(revenue):
    """The ruling's first half: where the substrate CAN carry exactly, it must."""
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)

    assert st.governed_domain == "decimal"
    assert st.carrier_type == "decimal128(18, 4)"
    # the exact value survives; this is the number the SQLite REAL path loses
    assert st.array[0].as_py() == Decimal("12345678901234.5678")


def test_standing_is_read_off_the_state_not_recomputed(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    held = store.retrieve(AnalyticalIdentity(family.family_id, family.constitutive_anchor))[0]

    assert held.standing.constitution == _constitution()[0]
    assert held.standing.constitution_scheme == "fcf-1"
    assert held.standing.participation == "every sale point carrying a recorded amount"
    assert held.standing.basis == "the running total"          # C7, projected in
    # OF-57: the realization axis is now the ASSERTION REVISION identity, not a hand-built prose
    # string. The test's point is unchanged — the standing is READ OFF THE STATE — so it is asserted
    # against a freshly computed revision for the same claim rather than against a literal, which
    # would just re-encode the composition in a second place.
    assert held.standing.realization.startswith(assertion.ASSERTION_SCHEME + ":")
    assert held.standing.realization == assertion.revision(_publication().ref, real)
    assert held.standing.currency == "tok-1"


def test_the_carrier_never_becomes_the_meaning(revenue):
    """`carrier_type` is disclosure. The governed domain is what the state IS."""
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)

    assert st.governed_domain == view["semantic_values"].value == "decimal"
    # the physical description is present but is not the domain, and never substitutes for it
    assert st.carrier_type != st.governed_domain
