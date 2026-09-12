"""THE POSITIVE CONTROL.

A governed identity and its standing survive materialization and are served WITHOUT THE PHYSICAL
CARRIER REDEFINING THEM.
"""
from decimal import Decimal

from columna_platform import carrier, serving
from columna_platform.state import AnalyticalIdentity, RetainedStateStore

CONSTITUTION = "fcf-1:c176d2a4f35e443c84e03e6cff3c27a1088b390887e15ae59d1312129e3840ce"


def _materialize(family, view, real, store, **kw):
    return serving.materialize(
        family, view, real, kw.pop("carrier_obj", carrier.exact_money()),
        basis=view["sufficient_state_bases"].value,      # DERIVED BY THE GOVERNED LAYER, passed in
        constitution=kw.pop("constitution", CONSTITUTION),
        constitution_scheme=kw.pop("scheme", "fcf-1"),
        currency=kw.pop("currency", "tok-1"),
        store=store,
    )


def test_the_lawful_case_serves(revenue):
    family, view, real = revenue
    store = RetainedStateStore()
    _materialize(family, view, real, store)

    out = serving.decide(view, store, AnalyticalIdentity(family.family_id, family.constitutive_anchor))

    assert out.mood == "serve"
    assert out.identity.family_id == family.family_id
    assert out.identity.anchor == "sale_at"
    assert out.row_count == 3


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

    out = serving.decide(view, store, AnalyticalIdentity(family.family_id, family.constitutive_anchor))

    assert out.standing.constitution == CONSTITUTION
    assert out.standing.constitution_scheme == "fcf-1"
    assert out.standing.participation == "every sale point carrying a recorded amount"
    assert out.standing.basis == "the running total"          # C7, projected in
    assert out.standing.realization.startswith("warehouse:sales.fact_sale.amount/coincident/exact")
    assert out.standing.currency == "tok-1"


def test_the_carrier_never_becomes_the_meaning(revenue):
    """`carrier_type` is disclosure. The governed domain is what the state IS."""
    family, view, real = revenue
    store = RetainedStateStore()
    st = _materialize(family, view, real, store)

    assert st.governed_domain == view["semantic_values"].value == "decimal"
    # the physical description is present but is not the domain, and never substitutes for it
    assert st.carrier_type != st.governed_domain
