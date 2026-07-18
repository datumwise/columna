"""
test_describe_extension.py — the D1 describe extension serializers (CP-3 C-1) + the §2b insulation
guarantee at the serializer layer (C-2).

Additive to the shipped per-kind shape: License blocks verbatim across fertility/hierarchy/assert, basis
+ absence semantics on universes, operator properties. The §2b guarantee — no physical identifier crosses
describe — is enforced here (the hierarchy's VIA table never appears) and by the standing server test.
"""
from columna_core import (describe_universe, describe_assert, describe_hierarchy, operator_properties,
                          absence_semantics, License, CORROBORATED, UNTESTABLE)
from columna_core.model import Universe, Assert, Hierarchy
from columna_core.projection import OperatorSig


def test_absence_semantics_per_basis():
    assert "ZERO" in absence_semantics("events")            # events: absence = lawful zero
    assert "GAP" in absence_semantics("spine")              # spine: absence = material gap
    assert "GAP" in absence_semantics("product")            # product: absence = gap
    assert "membership" in absence_semantics("registry")    # registry: present vs absent is a fact
    assert "undeclared" in absence_semantics(None)          # None: wiring inert until declared


def test_describe_universe_carries_basis_absence_and_license():
    lic = License(verdict=CORROBORATED, basis="events zero-fill tested", attestation="w1")
    u = Universe(name="sales", base_dimensions=frozenset({"store"}), basis="events", basis_license=lic)
    d = describe_universe(u, "day >= opened_date")          # predicate rendered logically by the caller
    assert d["basis"] == "events" and "ZERO" in d["absence"]
    assert d["basis_license"]["verdict"] == "corroborated"
    assert d["predicate"] == "day >= opened_date" and d["base_dimensions"] == ["store"]


def test_describe_assert_row_and_invariant_forms_carry_the_kernel_license():
    lic = License(verdict=UNTESTABLE, basis="author note")
    row = Assert(name="nonneg", universe="sales", kind="row", license=lic)
    d = describe_assert(row, "region >= 0")
    assert d["form"] == {"kind": "row", "predicate": "region >= 0"}
    assert d["license"]["verdict"] == "untestable"
    inv = Assert(name="recon", universe="sales", kind="invariant", anchor=("store",),
                 left="revenue", op="==", right="gross - discounts", license=lic)
    di = describe_assert(inv)
    assert di["form"]["kind"] == "invariant" and di["form"]["left"] == "revenue" and di["form"]["op"] == "=="
    assert di["form"]["anchor"] == ["store"]


def test_describe_hierarchy_carries_license_and_HIDES_the_physical_via_table():
    lic = License(verdict=CORROBORATED, attestation="w1")
    h = Hierarchy(lineage="calendar", paths=(("day", "week", "month"),), license=lic)
    d = describe_hierarchy(h)
    assert d["lineage"] == "calendar" and d["chain"] == ["day", "week", "month"]
    assert d["license"]["verdict"] == "corroborated"
    # §2b insulation: the VIA table is a physical identifier — it NEVER crosses describe
    assert "via_table" not in d and "caltbl" not in str(d)


def test_operator_properties_surfaces_registry_facts_not_mechanics():
    sig = OperatorSig(name="sum", kind="reducer", accepts=frozenset({"Float64"}), out_rule="same",
                      is_monoid=True, linear=True)
    assert operator_properties(sig) == {"kind": "reducer", "is_monoid": True, "linear": True,
                                        "needs_order": False, "needs_window": False}
    assert operator_properties(None) is None                # unknown reducer
