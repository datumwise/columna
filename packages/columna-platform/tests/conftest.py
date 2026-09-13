import copy
import json
from pathlib import Path

import pytest

from columna_core.governed.publication import parse_publication
from columna_core.governed.resolve import resolve_all

from columna_platform import serving

REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"
PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = Path(__file__).resolve().parents[1] / "fixtures" / "proof_a" / "private-core-mapping-v2.json"


@pytest.fixture
def governed():
    """publication + total law views + the bound, hand-written realization claim."""
    pub, views = serving.open_publication(PUBLICATION)
    mapping = serving.bind(pub, MAPPING)
    family = [f for f in pub.families if f.family_id == REVENUE][0]
    return pub, views, mapping, family


@pytest.fixture
def revenue(governed):
    pub, views, mapping, family = governed
    return family, views[REVENUE], serving.realize(mapping, REVENUE)


def no_result(wire: dict) -> dict:
    """The single column's classified no-result, from a real wire payload."""
    return wire["columns"][0]["no_result"]


def reason(wire: dict) -> str:
    return no_result(wire)["reason"]


def alternatives(wire: dict) -> list:
    return [a["token"] for a in no_result(wire)["alternatives"]]


def _publication_with(**family_body):
    """The lighthouse artifact with extra slots on `revenue`. Built in-memory, never written.

    A FIXTURE VARIANT RATHER THAN A SECOND FIXTURE FILE: the fact under test is one slot's presence,
    and a whole committed artifact differing in one key is a thing that drifts from its sibling."""
    doc = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    doc = copy.deepcopy(doc)
    for dec in doc["logical"]["declarations"]:
        if dec.get("body", {}).get("family_id") == REVENUE:
            dec["body"].update(family_body)
    pub = parse_publication(doc)
    return pub, resolve_all(pub)[REVENUE]


@pytest.fixture
def domain_only_view():
    """C3 ESTABLISHED by a DOMAIN alone — movement absent. The hole the corrected guard closes."""
    _pub, view = _publication_with(domain="the trading calendar")
    return view


@pytest.fixture
def declared_no_movement_view():
    """C3 EXPLICIT-NONE: the family has declared that nothing moves."""
    _pub, view = _publication_with(movement={"none": "this family does not move"})
    return view


@pytest.fixture
def anchored(governed):
    """Retained state at `sale_at(store x day)` — admitted, then retained with its coordinates."""
    from columna_platform import admission, carrier
    from columna_platform.state import AnalyticalIdentity, RetainedState, Standing

    pub, views, mapping, family = governed
    view = views[REVENUE]
    real = [r for r in mapping.families if r.family_id == REVENUE][0]
    ac = carrier.exact_money_at_sale_at()

    admitted = admission.admit(view, real, ac.as_carrier())      # the value column, admitted
    st = RetainedState(
        identity=AnalyticalIdentity(REVENUE, family.constitutive_anchor),
        standing=Standing(
            constitution="fcf-1:c176d2a4f35e443c84e03e6cff3c27a1088b390887e15ae59d1312129e3840ce",
            constitution_scheme="fcf-1",
            participation=view["eligibility_and_participation"].value,
            basis=view["sufficient_state_bases"].value,
            realization="warehouse:sales.fact_sale.amount/coincident/exact",
            currency="tok-1"),
        array=admitted.array, governed_domain=admitted.governed_domain,
        carrier_type=admitted.carrier_type,
        table=ac.table, anchor_columns=ac.anchor_columns)
    return pub, view, st


@pytest.fixture
def licence(anchored):
    from columna_platform import movement
    pub, _view, _st = anchored
    return movement.project(pub, source_anchor="sale_at", target_anchor="store",
                            target_components=["store"], law="SUM")


MEAN_ID = "lh-revmean"


def _publication_with_mean():
    """The lighthouse artifact plus a MEAN family over `revenue`. In-memory; fixture untouched."""
    doc = copy.deepcopy(json.loads(PUBLICATION.read_text(encoding="utf-8")))
    doc["logical"]["declarations"].append({"kind": "family", "name": "revenue_mean", "body": {
        "family_id": MEAN_ID,
        "canonical_reference": "mean(revenue@sale_at)",
        "universe": "sales",
        "constitutive_anchor": "sale_at",
        "target": "the arithmetic mean of revenue over participating sale points",
        "formation": {"kind": "construction",
                      "law": {"law": "MEAN", "version": "1", "vocabulary": "datumwise.foundation"},
                      "operands": ["fam_qv8Ky3mR7bTpZa1LwXcNdg"]},
        "participation": "every sale point carrying a recorded amount"}})
    pub = parse_publication(doc)
    return pub, resolve_all(pub)[MEAN_ID]


@pytest.fixture
def mean_view():
    _pub, view = _publication_with_mean()
    return view


@pytest.fixture
def admitted_pair(governed):
    """Two carriers that have genuinely PASSED ADMISSION, chosen so the mean is exact.

        A: 10.0000 + 15.0000 + 5.0000  = 30.0000 over 3
        B:  6.0000                     =  6.0000 over 1
        combined                        = 36.0000 over 4  ->  9.0000  exactly representable

    Routed through `admission.admit` against `revenue`'s law view rather than hand-built: "one
    ADMITTED carrier" is the premise of the whole proof, and a fixture that fabricates the admission
    would let the composite be constituted from something admission would have refused."""
    from decimal import Decimal
    import pyarrow as pa
    from columna_platform import admission, carrier

    _pub, views, mapping, _family = governed
    revenue_view = views[REVENUE]
    realization = [r for r in mapping.families if r.family_id == REVENUE][0]

    def _adm(values):
        c = carrier.Carrier(
            pa.array([Decimal(v) for v in values], type=pa.decimal128(18, 4)),
            "duckdb DECIMAL(18,4) -> arrow decimal128(18,4), preserved")
        return admission.admit(revenue_view, realization, c)

    return _adm(["10.0000", "15.0000", "5.0000"]), _adm(["6.0000"])


def _publication_with_mean_no_participation():
    """A MEAN family that declares NO participation — so C5 is genuinely unestablished."""
    doc = copy.deepcopy(json.loads(PUBLICATION.read_text(encoding="utf-8")))
    doc["logical"]["declarations"].append({"kind": "family", "name": "revenue_mean", "body": {
        "family_id": MEAN_ID,
        "canonical_reference": "mean(revenue@sale_at)",
        "universe": "sales",
        "constitutive_anchor": "sale_at",
        "target": "the arithmetic mean of revenue over participating sale points",
        "formation": {"kind": "construction",
                      "law": {"law": "MEAN", "version": "1", "vocabulary": "datumwise.foundation"},
                      "operands": ["fam_qv8Ky3mR7bTpZa1LwXcNdg"]}}})
    pub = parse_publication(doc)
    return resolve_all(pub)[MEAN_ID]


@pytest.fixture
def mean_view_without_participation():
    return _publication_with_mean_no_participation()
