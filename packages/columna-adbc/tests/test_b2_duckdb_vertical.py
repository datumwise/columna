"""
B-2 · **one real backend, cold to warm.** The vertical integration proof and its boundary controls.

    **Cold Frame-QL request → real DuckDB/ADBC realization → Arrow → independent fidelity adjudication →
    ordinary MME admission → serve; identical warm request → MME serve with zero additional backend work.**
    — Huayin, 2026-09-30 (B-2, the milestone)

The headline proof is §A. Everything after it exists because a real provider is the first thing that could
quietly acquire authority it was never granted, and B-2 is partly a test that **B-1' survives contact with
reality**: the backend gets no privileged path, no trusted-provider flag, and no suppression of a check.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

import b2_exhibit as EX
import b2_revenue_warehouse as W
import pytest

from columna_adbc import DuckDbAdbcSource, DuckDbFamilyProvider, PhysicalFamilyBinding
from columna_platform.kernel.geometry import KernelRefusal
from columna_platform.kernel.realization_manager import RealizationManager

REPO = pathlib.Path(__file__).resolve().parents[3]
ASK = EX.ASK


@pytest.fixture
def warehouse(tmp_path):
    return W.build(tmp_path)


@pytest.fixture
def world(warehouse):
    """The cold world: constituted, empty, and wired to a real DuckDB file."""
    return EX.cold_world(warehouse)


# ══ A · THE HEADLINE PROOF ════════════════════════════════════════════════════════════════════════

def test_cold_frameql_request_reaches_duckdb_and_the_identical_warm_request_does_not(world):
    """**THE MILESTONE, IN ONE TEST.** Frame-QL text in, a database read once, and the second identical
    request answered from held state."""
    mme, service, source, provider, _ = world
    assert source.fetches == [], "the world must be cold before the first request"

    cold = service.serve(ASK)
    assert cold.classification == "serve", cold.render()
    assert len(source.fetches) == 1
    assert len(cold.frame.rows) == len(W.ORDERS)

    warm = service.serve(ASK)
    assert warm.classification == "serve", warm.render()
    assert len(source.fetches) == 1, "the warm request contacted the backend"
    assert warm.frame.rows == cold.frame.rows


def test_the_values_served_are_the_warehouse_values_at_the_governed_root(world):
    _, service, _, _, _ = world
    frame = service.serve(ASK).frame
    order_at = frame.coordinates.index("order")
    served = {row[order_at]: row[-1] for row in frame.rows}
    assert served == {o[2]: o[3] for o in W.ORDERS}


def test_the_exhibit_runs_green(capsys):
    assert EX.main() == 0
    assert "ALL CHECKS PASSED" in capsys.readouterr().out


# ══ B · THE PHYSICAL CROSSING ═════════════════════════════════════════════════════════════════════

def test_the_generated_sql_is_a_bare_projection_and_nothing_more(world):
    _, service, source, _, _ = world
    service.serve(ASK)
    sql = source.fetches[0][3]
    assert sql == ('SELECT "booked_on", "order_ref", "shop_code", "net_amount" '
                   'FROM "sales"."fact_order"')
    for banned in ("GROUP BY", "SUM(", "WHERE", "JOIN", "ORDER BY", "HAVING", "*"):
        assert banned not in sql.upper(), banned


def test_the_unrequested_column_is_never_projected(world):
    """A projection that quietly widens is a projection nobody is governing."""
    _, service, source, _, _ = world
    service.serve(ASK)
    assert W.UNREQUESTED_COLUMN not in source.fetches[0][3]


def test_the_value_column_crosses_as_arrow_and_is_never_converted(world):
    """**§3, as a property of the object rather than a promise in a docstring.**

    The state the provider offers holds a `pyarrow` array. If anything had gone through `to_pylist` and been
    rebuilt, `values` would be a Python list and this would fail."""
    import pyarrow as pa

    mme, service, _, provider, _ = world
    service.serve(ASK)
    held = mme.measure("revenue", mme.family("revenue").root).value
    assert isinstance(held.values, (pa.Array, pa.ChunkedArray))
    assert len(held.values) == len(W.ORDERS)


def test_the_arrow_schema_that_crossed_is_the_one_the_binding_asked_for(warehouse):
    source = DuckDbAdbcSource(path=warehouse, name="commerce-warehouse")
    material = source.fetch(schema=W.SCHEMA, table=W.TABLE,
                            columns=[W.DAY_COLUMN, W.ORDER_COLUMN, W.STORE_COLUMN, W.VALUE_COLUMN])
    assert material.table.schema.names == [W.DAY_COLUMN, W.ORDER_COLUMN, W.STORE_COLUMN, W.VALUE_COLUMN]
    assert str(material.table.schema.field(W.VALUE_COLUMN).type) == "double"
    assert material.table.num_rows == len(W.ORDERS)


# ══ C · THE PROVIDER CLAIMS; IT DOES NOT CERTIFY ══════════════════════════════════════════════════

def test_a_real_offer_cannot_reach_the_cache_door_unadjudicated(world):
    """**B-1', unchanged, against a REAL provider.** The whole point of §6."""
    mme, _, _, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    proposal = next(iter(provider.propose(requirement)))
    offer = provider.realize(proposal)

    with pytest.raises(KernelRefusal) as raised:
        RealizationManager.establish(mme, offer)
    assert raised.value.code == "unadjudicated-offer-at-the-door"


def test_the_real_offer_is_adjudicated_by_the_authority_and_only_then_admitted(world):
    mme, _, source, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    offer = provider.realize(next(iter(provider.propose(requirement))))

    adjudicated = mme.realizations.adjudicate(offer)
    assert adjudicated, adjudicated.refusal
    assert adjudicated.credential.offer is offer, "the credential carries the offer WHOLE"

    admission = RealizationManager.establish(mme, adjudicated.credential)
    assert admission, getattr(admission, "detail", "")
    assert len(source.fetches) == 1


def test_a_real_offer_that_misstates_its_witness_is_refused_by_ADMISSION(world):
    """**Wrong build / stale witness stays an ADMISSION question** (§6, and B-1' §6 before it). Being a
    real database does not move the check, and fidelity does not ask it a second time."""
    from dataclasses import replace

    mme, _, _, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    offer = replace(provider.realize(next(iter(provider.propose(requirement)))),
                    witness="cw-1:deadbeefdeadbeef")

    adjudicated = mme.realizations.adjudicate(offer)
    assert adjudicated, "a misstated witness is NOT a fidelity failure — fidelity only requires it stated"
    admission = RealizationManager.establish(mme, adjudicated.credential)
    assert not admission
    assert admission.code == "off-build-material"


def test_duckdb_capability_does_not_authorize_the_analytical_request(world):
    """A provider bound for a family this Manifold does not declare proposes nothing, and the engine will
    not invent the family because a table exists."""
    mme, _, source, provider, coordinator = world
    unknown = PhysicalFamilyBinding(
        family_id="gross_margin", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN, "order": W.ORDER_COLUMN},
        value_column=W.VALUE_COLUMN)
    bound = DuckDbFamilyProvider(source, unknown, name="duckdb-warehouse")
    assert bound.bindings() == ("gross_margin",)

    outcome = coordinator.__class__(mme, realization=RealizationManager(bound)).fulfill(
        "revenue", mme.family("revenue").root)
    assert not outcome.served
    assert outcome.mood == "lawful-but-unavailable"
    assert source.fetches == [], "capability discovery opened nothing"


def test_a_provider_bound_at_the_wrong_grain_proposes_nothing(world):
    """It supplies **independently established root state** and neither aggregates nor continues, so a
    binding that is not at `R_F` declines rather than offering something refused deeper in."""
    mme, _, source, _, _ = world
    coarse = PhysicalFamilyBinding(
        family_id="revenue", schema=W.SCHEMA, table=W.TABLE,
        coordinates={"store": W.STORE_COLUMN, "day": W.DAY_COLUMN}, value_column=W.VALUE_COLUMN)
    provider = DuckDbFamilyProvider(source, coarse)
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    assert list(provider.propose(requirement)) == []
    assert source.fetches == []


def test_a_provider_will_not_execute_a_proposal_it_did_not_make(world):
    """A handle is a provider's PRIVATE object. Executing another provider's would be executing a physical
    plan this one cannot read — and it opens no connection to find that out."""
    from columna_platform.kernel.realization_manager import RealizationProposal

    mme, _, source, provider, _ = world
    root = mme.family("revenue").root
    foreign = RealizationProposal(provider="somebody-else", family_id="revenue", anchor=root,
                                 handle=("a tuple", "not a handle"))
    with pytest.raises(KernelRefusal) as raised:
        provider.realize(foreign)
    assert raised.value.code == "foreign-proposal"
    assert source.fetches == [], "it refused before opening anything"


def test_capability_discovery_opens_no_connection_at_all(world):
    """`propose` *"executes nothing, fetches nothing, opens nothing"* — asserted against a real driver,
    where the difference is observable."""
    mme, _, source, provider, _ = world
    requirement = mme.requirement_for("revenue", mme.family("revenue").root).requirement
    proposals = list(provider.propose(requirement))
    assert len(proposals) == 1
    assert proposals[0].anchor == mme.family("revenue").root
    assert proposals[0].value_form == "scalar"
    assert source.fetches == []


def test_renaming_the_physical_column_changes_nothing_analytical(tmp_path):
    path = W.build(tmp_path, value_column="turnover_amt", filename="renamed.duckdb")
    source = DuckDbAdbcSource(path=path, name="commerce-warehouse")
    provider = DuckDbFamilyProvider(source, W.binding(value_column="turnover_amt"))
    mme, service, _, _, coordinator = EX.cold_world(path)
    coordinator.realization = RealizationManager(provider)
    outcome = service.serve(ASK)
    assert outcome.classification == "serve", outcome.render()
    assert "turnover_amt" in source.fetches[0][3]
    assert len(outcome.frame.rows) == len(W.ORDERS)


# ══ D · WARM SERVING DOES NOT DEPEND ON THE BACKEND ═══════════════════════════════════════════════

def test_once_admitted_the_warm_request_serves_with_the_backend_unreachable(world):
    """**The stronger control** (§10). A fetch counter proves the backend was not asked; a source that
    raises proves it could not have been."""
    mme, service, source, provider, coordinator = world
    assert service.serve(ASK).classification == "serve"

    coordinator.realization = RealizationManager(
        DuckDbFamilyProvider(EX.FailOnCall(source), W.binding(), name=provider.name))
    again = service.serve(ASK)
    assert again.classification == "serve", again.render()
    assert len(source.fetches) == 1


# ══ E · THE LEVELS OF COUNTING STAY APART (§9) ════════════════════════════════════════════════════

def test_user_requests_and_internal_fulfilment_attempts_are_not_one_counter(warehouse):
    from columna_platform.kernel.observation import RecordingObserver

    observer = RecordingObserver()
    mme, service, source, _, _ = EX.cold_world(warehouse, observer=observer)

    service.serve(ASK)                                     # cold: NEED, then the retry that is READY
    service.serve(ASK)                                     # warm: one READY
    dispositions = [r.disposition for r in observer.records]
    assert dispositions == ["need", "ready", "ready"], dispositions
    assert len(source.fetches) == 1, "two user requests, one backend realization"


def test_the_observation_seam_was_not_taught_to_count_backend_work(warehouse):
    """§9: *"Preserve the existing observation seam unchanged."* The cache proof reads the provider's own
    fetch log, and no field was added to an observation to make B-2 easier to assert."""
    from columna_platform.kernel.observation import Fulfillment, RequestObservation

    for added in ("backend_realizations", "fetches", "provider_calls", "backend_fetches"):
        assert added not in RequestObservation.__dataclass_fields__
        assert added not in Fulfillment.__dataclass_fields__


# ══ F · NOTHING PHYSICAL LEAKED UPWARD (§M) ═══════════════════════════════════════════════════════

def test_no_physical_name_or_backend_vocabulary_entered_platform():
    """**THE DIRECTION OF THE ARROW, MEASURED.** Not one of this fixture's physical facts, and not one
    backend word, may appear anywhere in `columna_platform`."""
    src = REPO / "packages/columna-platform/src"
    # **THE DISTINCTIVE NAMES ONLY, AND THAT IS NOT A WEAKENING.** The first draft of this test also
    # banned `sales` and `channel` and failed — on `requirement.py`'s docstring, which says a NEED must
    # never become *"query table sales / group by month"*, and on the word "channel" in ordinary prose.
    # A guard that fires on English is a test about wording, not about leakage; the crossing's own suite
    # makes the same distinction for the same reason (its SQL ban is case-sensitive so that `" from "`
    # stays an English phrase). Every token below is one nothing but this fixture would ever write.
    physical = (W.TABLE, W.STORE_COLUMN, W.DAY_COLUMN, W.ORDER_COLUMN, W.VALUE_COLUMN,
                "commerce.duckdb", f"{W.SCHEMA}.{W.TABLE}")
    backend = ("duckdb", "adbc", "psycopg", "sqlalchemy", "connection_string", "driver_path")
    offenders = []
    for path in sorted(src.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for name in physical:
            if name in text:
                offenders.append(f"{path.name}: physical name {name!r}")
        for word in backend:
            # PROSE IS ALLOWED AND CODE IS NOT. Platform's docstrings legitimately NAME duckdb to say it
            # is banned; what may not exist is an import or an attribute reach.
            for line in text.splitlines():
                stripped = line.strip()
                if word in stripped.lower() and (stripped.startswith("import ")
                                                 or stripped.startswith("from ")):
                    offenders.append(f"{path.name}: {stripped}")
    assert offenders == [], offenders


def test_the_requirement_platform_hands_a_provider_names_no_physical_object():
    """`FamilyRequirement` is the whole of what Platform tells a provider, and §5 forbids putting a table
    in it. Asked of the object rather than of the module text."""
    from columna_platform.kernel.requirement import FamilyRequirement

    for field in FamilyRequirement.__dataclass_fields__:
        assert field not in ("table", "schema", "column", "columns", "sql", "query", "projection",
                             "connection", "predicate", "plan")


def test_platform_still_imports_no_driver_in_a_clean_interpreter():
    """The standing ban, re-run now that a provider exists. **Importing Platform must still load no
    driver**, which is a stronger statement with the driver installed than without it."""
    code = (
        "import sys;"
        "import columna_platform.frameql.serving, columna_platform.columnar.mme,"
        " columna_platform.kernel.fulfillment;"
        "print('DUCKDB', any(m == 'duckdb' or m.startswith('duckdb.') for m in sys.modules));"
        "print('ADBC', any(m.startswith('adbc') for m in sys.modules));"
        "print('COLUMNA_ADBC', any(m.startswith('columna_adbc') for m in sys.modules))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert "DUCKDB False" in out.stdout, out.stdout
    assert "ADBC False" in out.stdout, out.stdout
    assert "COLUMNA_ADBC False" in out.stdout, out.stdout
