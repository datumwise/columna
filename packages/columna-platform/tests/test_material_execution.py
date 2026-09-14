"""THE FIRST MATERIAL EXECUTION — and every neighbouring unlawful case, refusing for the right reason.

THE PROPOSITION, and the only one this slice makes:

    A governed exact SUM family can be resolved from public Frame-QL, bound through the ratified
    realization claim to admitted Arrow material, constituted as sufficient state carrying its
    anchor coordinates, and served through the existing public wire — without `.cml`, the legacy
    planner, or the legacy engine participating in analytical meaning.

WHAT "REFUSE BEFORE MATERIAL ACCESS" IS PROVEN WITH, because the phrase is easy to assert and hard
to mean. The controls that claim it are run against a deployment whose source registry is EMPTY. If
any of them reached material, the refusal would be the binding's ("no material source is bound to
connection 'warehouse'") and the assertion on the expected refusal would fail. The proof is that a
path with no material at all still produces the claim-level refusal.
"""
import json
import sys
from decimal import Decimal
from pathlib import Path

import pyarrow as pa
import pytest

from columna_core.compiler.refusals import InputIdentityMismatch
from columna_core.disclosure_wire import wire_frame
from columna_core.envelope import parse_statement

from columna_platform import serving
from columna_platform.provider import PlatformExecutionProvider
from columna_platform.refusals import UnsupportedByThisProfile, WantOfState
from columna_platform.source import MaterialBinding, SourceBindings, read_anchored

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
sys.path.insert(0, str(FIXTURES))
import lighthouse_material as M                                              # noqa: E402

PUBLICATION = (Path(__file__).resolve().parents[2] / "columna-core" / "tests" / "fixtures_v2"
               / "lighthouse-v2-publication.json")
MAPPING = FIXTURES / "proof_a" / "private-core-mapping-v2.json"
REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"

#: A deployment that has bound NOTHING. Reaching material through it is impossible, which is what
#: makes it the instrument for "this refusal happened before material access".
NO_MATERIAL = SourceBindings({})

ASK = "SELECT revenue AT {store*day}"


def _mapping_file(tmp_path, mutate=None) -> str:
    """The committed claim, optionally mutated, written where a provider can load it."""
    doc = json.loads(MAPPING.read_text(encoding="utf-8"))
    if mutate:
        mutate(doc)
    out = tmp_path / "private-core-mapping-v2.json"
    out.write_text(json.dumps(doc), encoding="utf-8")
    return str(out)


def _provider(tmp_path, *, sources=None, mutate=None) -> PlatformExecutionProvider:
    return PlatformExecutionProvider.from_artifact(
        str(PUBLICATION), manifold_id="lighthouse",
        material=MaterialBinding(mapping_path=_mapping_file(tmp_path, mutate),
                                 sources=M.bindings() if sources is None else sources))


def _run(provider, ask=ASK) -> dict:
    """Execute and WIRE IT — the assertions are against the real contract, never a local shape."""
    return wire_frame(provider.run(parse_statement(ask)), universe=None, executed=True)


def _no_result(wire) -> dict:
    return wire["columns"][0]["no_result"]


# ══ CONTROL 9 · the positive case ═══════════════════════════════════════════════════════════════

def test_a_governed_exact_sum_family_is_served_from_material_through_the_public_wire(tmp_path):
    """THE WHOLE PROPOSITION, as one wire payload."""
    wire = _run(_provider(tmp_path))
    assert wire["contract_version"] == "5"
    assert wire["outcome"] == "serve"
    assert wire["executed"] is True
    assert wire["frame"]["anchor"] == ["sale_at"]
    assert wire["columns"][0]["status"] == "served"
    assert wire["columns"][0]["name"] == "revenue"


def test_the_served_rows_carry_the_governed_anchor_coordinates(tmp_path):
    """P5-03's question at the last inch: does the analytical POINT survive the crossing?

    Four bare numbers under an anchor named `sale_at` would be four values nobody can place. The
    keys are the GOVERNED component names — `store`, `day` — and not the physical `store_code` /
    `sold_on` the material actually carries, which is what says the rename was the realization's
    claim being honoured rather than a coincidence of spelling."""
    rows = _run(_provider(tmp_path))["columns"][0]["values"]
    assert [sorted(r) for r in rows] == [["day", "store", "value"]] * 4
    assert {(r["store"], str(r["day"])) for r in rows} == {
        ("east", "2026-01-01"), ("east", "2026-01-02"),
        ("west", "2026-01-01"), ("west", "2026-01-02")}


def test_the_served_values_are_exact_decimals_and_not_floats(tmp_path):
    """The governed domain is exact decimal, and it is exact ON THE WIRE, not merely in the carrier.

    `1.2345 + 3.7037` is the pair chosen because it is not representable in binary floating point:
    if anything on this path had gone through a float, the total would miss."""
    values = [r["value"] for r in _run(_provider(tmp_path))["columns"][0]["values"]]
    assert all(isinstance(v, Decimal) for v in values), [type(v).__name__ for v in values]
    assert sum(values) == Decimal("34.9382")


def test_the_state_is_constituted_under_the_publications_own_constitution(tmp_path):
    """OF-39's correction, as a control. The fingerprint comes from the artifact, for THIS family.

    It is asserted against the publication rather than against a literal, because a literal is what
    was wrong before: the proofs carried `count(revenue@sale_at)`'s fingerprint for revenue, and no
    test could see it because `comparable_to` does not carry the fingerprint at all."""
    pub, _views = serving.open_publication(str(PUBLICATION))
    fingerprint, scheme = serving.constitution_of(pub, REVENUE)
    assert fingerprint == pub.constitution_authority[REVENUE].constitution_fingerprint
    assert scheme == "fcf-1"
    # and it is NOT the neighbouring family's, which is the defect that was there
    others = {fid: ca.constitution_fingerprint
              for fid, ca in pub.constitution_authority.items() if fid != REVENUE}
    assert fingerprint not in others.values()


def test_realization_currency_is_left_unresolved_and_closes_reuse(tmp_path):
    """An OPEN JURISDICTION, discharged honestly rather than waived.

    `None` closes reuse and never reads as fresh. For a request-local execution that combines
    nothing this costs nothing — which is exactly why it must not be quietly filled in."""
    pub, views = serving.open_publication(str(PUBLICATION))
    mapping = serving.bind(pub, _mapping_file(tmp_path))
    family = [f for f in pub.families if f.family_id == REVENUE][0]
    real = serving.realize(mapping, REVENUE)
    from columna_platform.state import RetainedStateStore
    anchored = read_anchored(
        M.bindings(), real, serving.component_realizations(mapping, family.constitutive_anchor))
    st = serving.materialize_anchored(pub, family, views[REVENUE], real, anchored,
                                      basis=views[REVENUE]["sufficient_state_bases"].value,
                                      store=RetainedStateStore())
    assert st.standing.currency is None
    assert st.standing.constitution == pub.constitution_authority[REVENUE].constitution_fingerprint


# ══ CONTROL 1 · governed decimal presented on a physical float ══════════════════════════════════

def test_a_float_carrier_is_refused_though_the_material_delivered(tmp_path):
    """The source hands back a float64 column. Nothing raises on the way in; admission refuses."""
    floats = pa.array([10.0, 20.0, 1.2345, 3.7037], type=pa.float64())
    wire = _run(_provider(tmp_path, sources=M.bindings(**{M.VALUE_COLUMN: floats})))
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "floating-point" in _no_result(wire)["detail"]


# ══ CONTROL 2 · wrong publication, and a family the publication does not declare ═════════════════

def test_a_mapping_for_another_publication_refuses_at_binding(tmp_path):
    def mutate(doc):
        doc["publication_ref"]["manifold_id"] = "not-lighthouse"
    with pytest.raises(InputIdentityMismatch):
        _provider(tmp_path, sources=NO_MATERIAL, mutate=mutate)


def test_a_realization_naming_an_undeclared_family_refuses_at_binding(tmp_path):
    """§4's "unknown refuses", on the successor path. Binding fails, so nothing can execute."""
    def mutate(doc):
        doc["realizations"].append({
            "kind": "family", "family_id": "fam_nonesuch",
            "endpoint": {"connection": "warehouse", "schema": "sales",
                         "table": "fact_sale", "column": "amount"},
            "grain": "coincident", "formation_operator": "sum", "exactness": "exact"})
    with pytest.raises(WantOfState, match="does not declare"):
        _provider(tmp_path, sources=NO_MATERIAL, mutate=mutate)


def test_a_family_with_no_realization_refuses_before_material(tmp_path):
    def mutate(doc):
        doc["realizations"] = [r for r in doc["realizations"]
                               if r.get("family_id") != REVENUE]
    wire = _run(_provider(tmp_path, sources=NO_MATERIAL, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "no realization claim" in _no_result(wire)["detail"]


# ══ CONTROL 6 · an approximate claim for an exact family ════════════════════════════════════════

def test_an_approximate_realization_claim_refuses_before_material_access(tmp_path):
    """Freeze §8 on THIS path. The deployment binds no material at all, so reaching this refusal
    proves the claim was checked before anything was read."""
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("family_id") == REVENUE:
                r["exactness"] = "approximate"
    wire = _run(_provider(tmp_path, sources=NO_MATERIAL, mutate=mutate))
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "approximate" in _no_result(wire)["detail"]
    assert "no material source is bound" not in _no_result(wire)["detail"]


def test_the_exactness_check_is_not_satisfied_by_the_carrier_being_exact(tmp_path):
    """The CLAIM is checked, not the bytes. Material that is exact does not rescue an approximate
    claim — which is the whole distinction between checking a carrier and checking an assertion."""
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("family_id") == REVENUE:
                r["exactness"] = "approximate"
    wire = _run(_provider(tmp_path, mutate=mutate))           # real, exact material bound
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "approximate" in _no_result(wire)["detail"]


# ══ CONTROL 3 · grain, and coordinates ══════════════════════════════════════════════════════════

def test_a_finer_grain_claim_against_coincident_formation_refuses(tmp_path):
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("family_id") == REVENUE:
                r["grain"] = "finer"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "grain 'finer'" in _no_result(wire)["detail"]


def test_a_carrier_missing_a_declared_coordinate_refuses(tmp_path):
    """Drop `day`'s realization: the carrier then carries `store` alone.

    Serving it would retain revenue at a point COARSER than the anchor it was constituted at, which
    is movement — and movement needs a positive licence this family does not carry."""
    def mutate(doc):
        doc["realizations"] = [r for r in doc["realizations"]
                               if not (r.get("kind") == "anchor_component"
                                       and r.get("component_name") == "day")]
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "missing ['day']" in _no_result(wire)["detail"]


def test_a_carrier_with_an_undeclared_coordinate_refuses(tmp_path):
    """The other direction, and it must refuse too: a coordinate the anchor does not declare would
    retain the value at a point finer than the publication names."""
    def mutate(doc):
        doc["realizations"].append({
            "kind": "anchor_component", "anchor_ref": "sale_at", "component_name": "till",
            "endpoint": {"connection": "warehouse", "schema": "sales",
                         "table": "fact_sale", "column": "store_code"}})
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert _no_result(wire)["reason"] == "want_of_state"
    assert "not declared: ['till']" in _no_result(wire)["detail"]


# ══ CONTROL 4 · a physical null where no governed absence law exists ════════════════════════════

def test_a_null_in_the_material_refuses_rather_than_being_read_as_absence(tmp_path):
    """The carrier reports THAT a value is absent. What it DENOTES is governed, and lighthouse's C9
    answers a different question — what an empty fiber denotes, not what an absent observation
    does. This is a want of LAW: re-realizing the same source cannot supply the missing rule."""
    with_null = pa.array([Decimal("10.0000"), None, Decimal("1.2345"), Decimal("3.7037")],
                         type=pa.decimal128(18, 4))
    wire = _run(_provider(tmp_path, sources=M.bindings(**{M.VALUE_COLUMN: with_null})))
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_law"
    assert "ABSENT OBSERVATION" in _no_result(wire)["detail"]


# ══ the source binding · R1's invariant ═════════════════════════════════════════════════════════

def test_changing_the_connection_alone_changes_which_source_is_selected(tmp_path):
    """R1, DISCHARGED BY CONSUMPTION AND NOT MERELY BY A CHECK. The claim still says `warehouse`;
    the deployment binds the same bytes under a different name. Nothing else differs, and the
    request stops serving — which is the faithful-consumption test, applied to `connection`."""
    ok = _run(_provider(tmp_path, sources=M.bindings(connection="warehouse")))
    moved = _run(_provider(tmp_path, sources=M.bindings(connection="elsewhere")))
    assert ok["outcome"] == "serve"
    assert moved["outcome"] == "refuse"
    assert _no_result(moved)["reason"] == "want_of_state"
    assert "no material source is bound to connection 'warehouse'" in _no_result(moved)["detail"]


def test_schema_participates_in_selecting_the_material_object(tmp_path):
    """R2, DISCHARGED BY CONSUMPTION HERE (K0v2 refuses a non-null schema instead; both are lawful).

    `sales.fact_sale` and `staging.fact_sale` are different material. Changing only the claimed
    schema must stop the request, or the qualification was decorative."""
    def mutate(doc):
        for r in doc["realizations"]:
            r["endpoint"]["schema"] = "staging"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "refuse"
    assert "holds no object staging.fact_sale" in _no_result(wire)["detail"]


def test_the_table_also_participates(tmp_path):
    def mutate(doc):
        for r in doc["realizations"]:
            r["endpoint"]["table"] = "fact_sale_v2"
    assert _run(_provider(tmp_path, mutate=mutate))["outcome"] == "refuse"


def test_the_column_also_participates(tmp_path):
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("family_id") == REVENUE:
                r["endpoint"]["column"] = "net_amount"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "refuse"
    # WORDING MOVED 2026-09-14 with the projected fetch: the source is now asked for the whole
    # projection in one request, so it reports the missing column(s) as a set. The FACT under test is
    # unchanged -- the endpoint's `column` participates in selection, and naming one the object does
    # not have refuses instead of serving something else.
    assert "'net_amount'" in _no_result(wire)["detail"]
    assert "has no column" in _no_result(wire)["detail"]


def test_material_in_two_objects_is_a_capability_limit_and_not_a_governed_refusal(tmp_path):
    """A join, which this profile does not implement. NOT a want-of-state: re-realizing cannot
    supply a capability, and telling an operator to go and re-materialize would waste their day."""
    def mutate(doc):
        for r in doc["realizations"]:
            if r.get("component_name") == "store":
                r["endpoint"]["table"] = "dim_store"
    wire = _run(_provider(tmp_path, mutate=mutate))
    assert wire["outcome"] == "error"
    assert _no_result(wire)["reason"] == "unsupported"
    assert "join" in _no_result(wire)["detail"]


# ══ CONTROL 5 · capability limits, on the wire, never as a governed verdict ═════════════════════

def test_a_deployment_with_no_material_binding_reports_a_capability_limit(tmp_path):
    """PLANS, does not execute — and says so as `unsupported`, not as a governed refusal."""
    p = PlatformExecutionProvider.from_artifact(str(PUBLICATION), manifold_id="lighthouse")
    wire = _run(p)
    assert wire["outcome"] == "error"
    assert _no_result(wire)["reason"] == "unsupported"
    assert _no_result(wire)["alternatives"] == []


def test_a_multi_series_request_is_a_capability_limit_not_an_unlawful_one(tmp_path):
    wire = _run(_provider(tmp_path), ask="SELECT revenue, revenue AT {store*day}")
    assert wire["outcome"] == "error"
    assert _no_result(wire)["reason"] == "unsupported"


def test_a_coarser_anchor_is_a_GOVERNED_refusal_and_not_a_capability_limit(tmp_path):
    """THE PAIR THAT MAKES CONTROL 5 MEAN SOMETHING. Moving revenue off its constitutive anchor is
    refused by LAW — no positive movement licence — and must not be dressed as "unimplemented",
    which would tell an operator to wait for a feature that was never the obstacle."""
    wire = _run(_provider(tmp_path), ask="SELECT revenue AT {store}")
    assert wire["outcome"] == "refuse"
    assert _no_result(wire)["reason"] == "want_of_law"


def test_an_unknown_reference_is_a_GOVERNED_refusal(tmp_path):
    wire = _run(_provider(tmp_path), ask="SELECT nonesuch AT {store*day}")
    assert _no_result(wire)["reason"] == "want_of_law"


def test_the_three_public_outcomes_are_distinguishable_from_one_another(tmp_path):
    """serve · governed refuse · capability error — one deployment, three asks, three answers."""
    p = _provider(tmp_path)
    seen = {
        _run(p, ASK)["outcome"],
        _run(p, "SELECT revenue AT {store}")["outcome"],
        _run(p, "SELECT revenue, revenue AT {store*day}")["outcome"],
    }
    assert seen == {"serve", "refuse", "error"}


def test_a_capability_limit_never_borrows_a_governed_reason_and_the_reverse(tmp_path):
    """The narrowed prohibition, as an assertion over every outcome this module produces."""
    p = _provider(tmp_path)
    governed = {"want_of_law", "want_of_state"}
    for ask in ("SELECT revenue, revenue AT {store*day}",):
        assert _no_result(_run(p, ask))["reason"] not in governed
    for ask in ("SELECT revenue AT {store}", "SELECT nonesuch AT {store*day}"):
        assert _no_result(_run(p, ask))["reason"] != "unsupported"


def test_the_capability_exception_is_still_not_a_proof_refusal():
    """It is translated at the boundary and nowhere earlier. If it became a `ProofRefusal`, the
    governed handler would catch it and give a capability gap a jurisdiction."""
    from columna_platform.refusals import ProofRefusal
    assert not issubclass(UnsupportedByThisProfile, ProofRefusal)


# ══ CONTROL 7 and 8 · no `.cml`, no legacy stack ════════════════════════════════════════════════

def test_material_execution_consults_no_cml(tmp_path, monkeypatch):
    """Run the whole path from a working directory that contains no `.cml` anywhere beneath it."""
    monkeypatch.chdir(tmp_path)
    assert not list(Path(tmp_path).glob("**/*.cml"))
    assert _run(_provider(tmp_path))["outcome"] == "serve"


def test_material_execution_loads_no_legacy_execution_module():
    """The runtime complement, in a CLEAN interpreter: the path EXECUTES and the stack stays out."""
    import subprocess
    prog = (
        "import sys\n"
        f"sys.path.insert(0, {str(FIXTURES)!r})\n"
        "import lighthouse_material as M\n"
        "from columna_core.envelope import parse_statement\n"
        "from columna_platform.provider import PlatformExecutionProvider\n"
        "from columna_platform.source import MaterialBinding\n"
        f"p = PlatformExecutionProvider.from_artifact({str(PUBLICATION)!r},\n"
        f"    material=MaterialBinding(mapping_path={str(MAPPING)!r}, sources=M.bindings()))\n"
        "fr = p.run(parse_statement('SELECT revenue AT {store*day}'))\n"
        "assert fr.columns[0].frame is not None, 'the run did not serve'\n"
        "banned = {'planner','engine','model','adjudication','parser','projection','frameql',"
        "'expr','connector'}\n"
        "loaded = {m.rsplit('.',1)[-1] for m in sys.modules if m.startswith('columna_core.')}\n"
        "print('LOADED[' + ','.join(sorted(loaded & banned)) + ']')\n"
    )
    out = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "LOADED[]" in out.stdout, out.stdout


def test_the_material_modules_name_no_forbidden_import():
    """The static complement, extended to the modules this slice added."""
    import ast
    forbidden = {"columna_core.planner", "columna_core.engine", "columna_core.model",
                 "columna_core.adjudication", "columna_core.connector", "columna_core.parser",
                 "columna_core.compiler.compile_v2", "duckdb", "adbc_driver_manager"}
    here = Path(serving.__file__).parent
    reached = set()
    for f in sorted(here.glob("*.py")):
        for n in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
            if isinstance(n, ast.Import):
                reached.update(a.name for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                reached.add(n.module)
    assert not (reached & forbidden), sorted(reached & forbidden)


# ══ state lifecycle ═════════════════════════════════════════════════════════════════════════════

def test_the_provider_holds_no_state_between_requests(tmp_path):
    """REQUEST-LOCAL, and asserted rather than assumed: the provider has no store attribute at all,
    so there is nothing that could outlive a request or be served stale."""
    p = _provider(tmp_path)
    assert not any("store" in a.lower() for a in vars(p)), sorted(vars(p))
    first = _run(p)
    second = _run(p)
    assert first == second


def test_nothing_is_finalized_for_a_sum_at_coincident_grain(tmp_path):
    """C7's basis for SUM is "the running total", and at coincident grain the material already IS
    it. No finalization step was invented to have one; the served values are the state."""
    pub, views = serving.open_publication(str(PUBLICATION))
    assert views[REVENUE]["sufficient_state_bases"].value == "the running total"
    rows = _run(_provider(tmp_path))["columns"][0]["values"]
    assert [r["value"] for r in rows] == [amount for _store, _day, amount in M.ROWS]
