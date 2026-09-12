"""
test_governed_v2.py — publication format v2, the foundation-law vocabulary, the total `Law(F)` view,
and the K0v2 compile boundary.

The property under test, in one sentence: **the Core family is built from established governed law,
and the private mapping is checked against it rather than read for it.**
"""
from __future__ import annotations

import copy
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fixtures_v2 import lighthouse as lh                                       # noqa: E402

from columna_core.compiler.compile_v2 import K0_LAWS, compile_v2               # noqa: E402
from columna_core.compiler.realization import parse_mapping                    # noqa: E402
from columna_core.compiler.refusals import (                                   # noqa: E402
    ExecutionRepresentationGap, InputIdentityMismatch, LogicalMeaningMissing, MappingIncomplete,
    UnsupportedCoreCapability,
)
from columna_core.governed import foundation as fdn                            # noqa: E402
from columna_core.governed import resolve as R                                 # noqa: E402
from columna_core.governed.publication import (                                # noqa: E402
    PublicationFormatRefusal, parse_publication,
)
from columna_core.operators import REGISTRY                                    # noqa: E402

HERE = pathlib.Path(__file__).parent
FIRSTLIGHT = HERE.parent.parent / "columna-server" / "fixtures" / "firstlight"


def _pub(mutate=None):
    d = copy.deepcopy(lh.publication())
    if mutate:
        mutate(d)
    return parse_publication(d)


def _map(mutate=None):
    d = copy.deepcopy(lh.mapping())
    if mutate:
        mutate(d)
    return parse_mapping(d)


def _family(doc, reference):
    for decl in doc["logical"]["declarations"]:
        if decl["kind"] == "family" and decl["body"]["canonical_reference"] == reference:
            return decl["body"]
    raise KeyError(reference)                                   # pragma: no cover


# ══ the foundation-law vocabulary ════════════════════════════════════════════════════════════════
def test_the_vocabulary_is_structurally_sound():
    assert fdn.selftest() == []


def test_min_and_max_supply_no_empty_fiber_value_and_nobody_is_asked():
    # §5.2 / §6.1.1 / §11.5.1. A theorem of the law, established once, never re-declared per family.
    assert fdn.LAWS["MIN"].empty_fiber == "no_value"
    assert fdn.LAWS["MAX"].empty_fiber == "no_value"
    assert fdn.LAWS["SUM"].empty_fiber == "identity"
    assert "no finite witness" not in fdn.LAWS["SUM"].sufficient_state


def test_count_continues_by_sum_and_may_never_be_cited_as_a_continuation():
    # §5.2: "two retained count states 37 and 12 can combine to 49 under count-state continuation.
    # Counting the two scalar values as new observations gives 2."
    assert fdn.LAWS["COUNT"].entails_continuation == "SUM"
    assert fdn.LAWS["COUNT"].usable_as_continuation is False


def test_mean_is_vocabulary_without_being_servable_and_does_not_continue():
    assert fdn.LAWS["MEAN"].entails_continuation == fdn.NO_CONTINUATION
    assert fdn.LAWS["MEAN"].empty_fiber == "not_applicable"
    assert "MEAN" not in K0_LAWS          # §4.1 — a backend's inability does not remove the law


def test_a_citation_never_falls_back_across_versions():
    with pytest.raises(fdn.UnknownFoundationLaw):
        fdn.resolve(fdn.LawCitation(fdn.VOCABULARY, "99", "SUM"))
    with pytest.raises(fdn.UnknownFoundationLaw):
        fdn.resolve(fdn.LawCitation("somebody.else", fdn.VERSION, "SUM"))
    with pytest.raises(fdn.UnknownFoundationLaw):
        fdn.resolve(fdn.cite("NOT_A_LAW"))


def test_a_bare_law_name_is_not_a_citation():
    with pytest.raises(fdn.UnknownFoundationLaw):
        fdn.LawCitation.from_dict({"law": "SUM"})


def test_the_vocabulary_is_not_the_operator_registry():
    """Re-derived, not promoted. Pinned BOTH ways so neither can drift into the other."""
    for law in fdn.LAWS.values():
        for realization_field in ("deliver_sql", "scan_impl", "in_core", "kind", "witness"):
            assert not hasattr(law, realization_field), (
                f"{law.name} carries {realization_field!r} — realization has entered the vocabulary")


# ══ the v1 break ═════════════════════════════════════════════════════════════════════════════════
def test_a_v1_artifact_is_refused_with_its_reason_and_never_read():
    raw = json.loads((FIRSTLIGHT / "governed-publication.json").read_text())
    with pytest.raises(PublicationFormatRefusal) as exc:
        parse_publication(raw)
    msg = str(exc.value)
    assert "NO automatic v1 read" in msg
    assert "under-determines its own meaning" in msg


@pytest.mark.parametrize("kind", ["measure", "member", "boundary"])
def test_the_retired_kinds_are_refused_by_name(kind):
    def mutate(d):
        d["logical"]["declarations"].append({"kind": kind, "name": "x", "body": {}})
    with pytest.raises(PublicationFormatRefusal, match="retired"):
        _pub(mutate)


# ══ consume-or-refuse ════════════════════════════════════════════════════════════════════════════
def test_an_unrecognised_governed_key_refuses_rather_than_being_ignored():
    def mutate(d):
        _family(d, "revenue")["fill_rule"] = "zero"
    with pytest.raises(PublicationFormatRefusal, match="unrecognised governed key"):
        _pub(mutate)


def test_an_unrecognised_mapping_key_refuses():
    def mutate(d):
        d["realizations"][2]["root_evaluator"] = "sum"
    with pytest.raises(MappingIncomplete, match="unrecognised key"):
        _map(mutate)


def test_identity_is_not_a_label():
    def mutate(d):
        _family(d, "min(revenue@sale_at)")["family_id"] = "lh-revenue"
    with pytest.raises(PublicationFormatRefusal, match="declared twice"):
        _pub(mutate)


def test_two_families_may_not_hide_under_one_reference():
    # §2.2 — "Two distinct active identities cannot be hidden under one ambiguous canonical
    # reference." This is the synonym-operator hole, closed at the identity layer.
    def mutate(d):
        _family(d, "min(revenue@sale_at)")["aliases"] = ["revenue"]
    with pytest.raises(PublicationFormatRefusal, match="two families"):
        _pub(mutate)


def test_authority_may_not_outlive_the_thing_it_attests():
    def mutate(d):
        d["authority"]["family_constitution"]["lh-ghost"] = {
            "established_by": "x", "at": "y", "constitution_fingerprint": "z",
            "fingerprint_scheme": "sigma-f-1"}
    with pytest.raises(PublicationFormatRefusal, match="does not declare"):
        _pub(mutate)


def test_family_constitution_authority_is_a_distinct_record_type_from_elf_1():
    pub = _pub()
    assert set(pub.constitution_authority) == {"lh-revenue", "lh-revcount", "lh-revmin",
                                               "lh-revmax"}
    for rec in pub.constitution_authority.values():
        assert rec.fingerprint_scheme != "elf-1", (
            "family constitution and universe existence law must not share a fingerprint scheme; "
            "they attest different objects and one scheme would compare incomparables")


# ══ the total Law(F) view ════════════════════════════════════════════════════════════════════════
def test_the_resolved_view_is_total_so_silence_is_impossible():
    for view in R.resolve_all(_pub()).values():
        assert set(view.entries) == set(R.RESPONSIBILITIES)
        for r in R.RESPONSIBILITIES:
            assert view.entries[r].standing in (R.ESTABLISHED, R.EXPLICIT_NONE, R.UNESTABLISHED)


def test_every_lighthouse_family_is_valid():
    for view in R.resolve_all(_pub()).values():
        assert view.valid, view.validity_problems


def test_a_constructed_family_entails_its_continuation_result_domain_and_empty_fiber():
    views = R.resolve_all(_pub())
    count = views["lh-revcount"]
    assert count[R.C8_CONTINUATION].provenance == R.ENTAILED
    assert count[R.C8_CONTINUATION].value.name == "SUM"
    assert count[R.C6_SEMANTIC_VALUES].provenance == R.ENTAILED
    assert count[R.C6_SEMANTIC_VALUES].value == "integer"      # not the operand's `decimal`
    assert count[R.C9_EXCEPTIONAL].value["empty_fiber"] == "identity"

    mn = views["lh-revmin"]
    assert mn[R.C9_EXCEPTIONAL].provenance == R.ENTAILED
    assert mn[R.C9_EXCEPTIONAL].value["empty_fiber"] == "no_value"


def test_a_primitive_family_declares_its_continuation_because_nothing_entails_one():
    views = R.resolve_all(_pub())
    assert views["lh-revenue"][R.C8_CONTINUATION].provenance == R.DECLARED


def test_an_undeclared_primitive_continuation_is_unestablished_not_defaulted():
    def mutate(d):
        _family(d, "revenue").pop("continuation")
    view = R.resolve_all(_pub(mutate))["lh-revenue"]
    assert view.standing(R.C8_CONTINUATION) == R.UNESTABLISHED
    assert not view.valid                     # continuation is identity-bearing (§3.9)


def test_movement_is_unestablished_and_that_is_a_visible_state_not_a_silence():
    for view in R.resolve_all(_pub()).values():
        assert view.standing(R.C3_DOMAIN_MOVEMENT) == R.UNESTABLISHED
        assert "not permission" in view[R.C3_DOMAIN_MOVEMENT].note
    # and it does not make the family invalid — a family can exist while a movement has not been
    # established (ruled 2026-09-11)
    assert all(v.valid for v in R.resolve_all(_pub()).values())


def test_explicit_none_is_a_positive_negative_distinct_from_absence():
    def mutate(d):
        _family(d, "revenue")["continuation"] = {"none": "a stock does not compose over time"}
    view = R.resolve_all(_pub(mutate))["lh-revenue"]
    assert view.standing(R.C8_CONTINUATION) == R.EXPLICIT_NONE
    assert view[R.C8_CONTINUATION].settled
    assert view.valid                          # explicitly none IS established
    assert view.standing(R.C7_SUFFICIENT_STATE) == R.EXPLICIT_NONE


def test_a_declared_continuation_that_diverges_from_the_formation_law_refuses():
    def mutate(d):
        _family(d, "count(revenue@sale_at)")["continuation"] = lh._cite("MIN")
    with pytest.raises(R.LawResolutionRefusal, match="different family"):
        R.resolve_all(_pub(mutate))


def test_citing_count_as_a_continuation_refuses():
    def mutate(d):
        _family(d, "revenue")["continuation"] = lh._cite("COUNT")
    with pytest.raises(R.LawResolutionRefusal, match="refuses"):
        R.resolve_all(_pub(mutate))


def test_a_theorem_of_the_cited_law_is_not_re_declarable():
    def mutate(d):
        _family(d, "min(revenue@sale_at)")["exceptional"] = {"empty_fiber": "identity"}
    with pytest.raises(R.LawResolutionRefusal, match="not\n?\\s*re-declarable|re-declarable"):
        R.resolve_all(_pub(mutate))


def test_a_law_that_does_not_admit_the_operand_domain_refuses():
    # the CONSTRUCTION side: SUM over a text operand.
    def construction(d):
        _family(d, "revenue")["value_domain"] = "text"
        _family(d, "min(revenue@sale_at)")["formation"]["law"] = lh._cite("SUM")
    with pytest.raises(R.LawResolutionRefusal, match="does not admit"):
        R.resolve_all(_pub(construction))


def test_a_primitive_may_not_compose_under_a_law_that_rejects_its_own_values():
    # the CONTINUATION side, which has no formation law to catch it first: a `text` quantity
    # declaring an additive continuation.
    def mutate(d):
        _family(d, "revenue")["value_domain"] = "text"
        for ref in ("count(revenue@sale_at)", "min(revenue@sale_at)", "max(revenue@sale_at)"):
            _family(d, ref)["formation"]["law"] = lh._cite("COUNT" if "count" in ref else "MIN")
    with pytest.raises(R.LawResolutionRefusal, match="does not admit values of domain"):
        R.resolve_all(_pub(mutate))


def test_a_constructed_result_domain_is_a_consequence_not_a_choice():
    def mutate(d):
        _family(d, "count(revenue@sale_at)")["value_domain"] = "decimal"
    with pytest.raises(R.LawResolutionRefusal, match="consequence, not a choice"):
        R.resolve_all(_pub(mutate))


def test_lineage_is_derived_from_formation_and_must_be_well_founded():
    views = R.resolve_all(_pub())
    assert views["lh-revcount"][R.C2_IDENTITY].value["parents"] == ("lh-revenue",)
    assert views["lh-revenue"][R.C2_IDENTITY].value["parents"] == ()

    def mutate(d):
        _family(d, "revenue")["formation"] = {
            "kind": "construction", "law": lh._cite("SUM"), "operands": ["lh-revcount"]}
    with pytest.raises(R.LawResolutionRefusal, match="well-founded"):
        R.resolve_all(_pub(mutate))


def test_a_construction_may_not_cite_a_parent_the_publication_does_not_declare():
    def mutate(d):
        _family(d, "min(revenue@sale_at)")["formation"]["operands"] = ["nowhere"]
    with pytest.raises(R.LawResolutionRefusal, match="does not declare"):
        R.resolve_all(_pub(mutate))


def test_an_unestablished_contribution_structure_is_legitimate_at_parse_and_fatal_at_validity():
    def mutate(d):
        _family(d, "revenue")["formation"] = {"kind": "primitive"}
    view = R.resolve_all(_pub(mutate))["lh-revenue"]
    assert view.standing(R.C4_FORMATION) == R.UNESTABLISHED
    assert not view.valid


# ══ the compile boundary ═════════════════════════════════════════════════════════════════════════
def test_lighthouse_compiles_and_its_family_comes_from_law():
    """The governed `decimal` domain is CARRIED as `Decimal`, not coerced to `Float64`.

    This assertion previously read `TYPE Float64` and PINNED a law-loss path as correct behaviour
    (correction, Huayin, 2026-09-12). The substitution of binary floating point for a governed
    exact-decimal domain was the type-system instance of reducing law rather than coverage — and it
    was unforced: measured through Core's own doorway, `pl.from_arrow(con.execute(q).arrow())`
    carries `duckdb DECIMAL(18,4) -> arrow decimal128(18,4) -> polars Decimal(18,4)` exactly.
    `Decimal` was already in `types.DTYPES` and in `NUMERIC`, so `sum` admitted it all along.

    The test is edited here as part of that explicit architectural correction, and for no other
    reason: a pinning test is the record of what was believed correct, so changing one is a ruling,
    not a repair.
    """
    image = compile_v2(_pub(), _map())
    assert "MEASURE revenue ON sales FROM sales_lines TYPE Decimal VALUE amount" in image.text
    assert "FAMILY {" in image.text
    for member in ("sum", "count", "min", "max"):
        assert f"        {member}" in image.text


def test_no_governed_family_may_silently_disappear_from_the_image():
    """Totality over `publication.families` — measured behaviour before this was SILENCE.

    A family whose operand is itself a construction landed in `by_parent` under a non-primitive key,
    was never visited by the emission loop, and was never refused: the image came out BYTE-IDENTICAL
    to one compiled without it, and no realization was required for it either. An established
    governed family disappeared and nothing said so.

    The check is stated as totality rather than as a special case for nested construction, because
    the defect was not nested construction — it was that lowering had no obligation to account for
    what it was given.
    """
    def add_nested(doc):
        constructed = next(d for d in doc["logical"]["declarations"]
                           if d["kind"] == "family"
                           and d["body"]["formation"]["kind"] == "construction")
        nested = copy.deepcopy(constructed)
        nested["name"] = "nested_min"
        nested["body"].update(family_id="fam-nested-xyz", canonical_reference="nested_min",
                              aliases=[])
        nested["body"]["formation"]["operands"] = [constructed["body"]["family_id"]]
        doc["logical"]["declarations"].append(nested)

    publication = _pub(add_nested)
    assert any(f.family_id == "fam-nested-xyz" for f in publication.families), (
        "the governed layer parses it — the loss was downstream, at lowering")

    with pytest.raises(UnsupportedCoreCapability) as caught:
        compile_v2(publication, _map())
    message = str(caught.value)
    assert "nested_min" in message, "the refusal names the family it could not account for"
    assert "silently omits" in message


def test_the_mapping_cannot_change_which_family_member_exists():
    """The v1 defect, tested as an invariant: editing the realization's operator changes NOTHING
    about the governed family — it refuses, because the law decides and the mapping only claims."""
    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revmin":
                r["formation_operator"] = "max"
    with pytest.raises(MappingIncomplete, match="The law decides"):
        compile_v2(_pub(), _map(mutate))


def test_a_realization_without_a_delivery_claim_refuses():
    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revcount":
                r.pop("formation_operator")
    with pytest.raises(MappingIncomplete, match="delivery claim"):
        compile_v2(_pub(), _map(mutate))


def test_a_grain_claim_that_contradicts_established_formation_refuses():
    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revenue":
                r["grain"] = "finer"
    with pytest.raises(MappingIncomplete, match="FINER"):
        compile_v2(_pub(), _map(mutate))


def test_a_finer_grain_with_no_established_contribution_law_cannot_compile():
    """`firstlight`'s structural question, as an invariant. In v1 the resolution law was supplied
    silently by `root_evaluator`; here its absence stops the compile."""
    def pub_mutate(d):
        _family(d, "revenue")["formation"] = {"kind": "primitive"}

    def map_mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revenue":
                r["grain"] = "finer"
    with pytest.raises(LogicalMeaningMissing, match="identity-bearing constitution is unresolved"):
        compile_v2(_pub(pub_mutate), _map(map_mutate))


def test_an_undisclosed_approximation_is_refused():
    def mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revmin":
                r["exactness"] = "approximate"
    with pytest.raises(UnsupportedCoreCapability, match="exact deliveries only"):
        compile_v2(_pub(), _map(mutate))


def test_a_law_outside_the_profile_refuses_and_does_not_narrow_the_law():
    def mutate(d):
        _family(d, "min(revenue@sale_at)")["formation"]["law"] = lh._cite("MEAN")
    with pytest.raises(UnsupportedCoreCapability, match="not in this profile"):
        compile_v2(_pub(mutate), _map())


def test_two_governed_families_on_one_core_operator_refuse_rather_than_collapse():
    """The governed layer can express a family Core cannot represent. That refuses — §4.1 — and the
    governed law is untouched."""
    def pub_mutate(d):
        _family(d, "max(revenue@sale_at)")["formation"]["law"] = lh._cite("MIN")

    def map_mutate(d):
        for r in d["realizations"]:
            if r.get("family_id") == "lh-revmax":
                r["formation_operator"] = "min"       # an honest claim about a colliding law
    with pytest.raises(ExecutionRepresentationGap, match="cannot hold both"):
        compile_v2(_pub(pub_mutate), _map(map_mutate))


def test_a_mapping_for_another_publication_is_refused_first():
    def mutate(d):
        d["publication_ref"]["version"] = "9.9.9"
    with pytest.raises(InputIdentityMismatch):
        compile_v2(_pub(), _map(mutate))


def test_an_invalid_family_stops_the_compile_with_the_identity_reason():
    def mutate(d):
        _family(d, "revenue").pop("participation")
    with pytest.raises(LogicalMeaningMissing, match="identity-bearing constitution is unresolved"):
        compile_v2(_pub(mutate), _map())


def test_a_v1_mapping_is_refused_by_major_with_root_evaluator_named():
    raw = json.loads((FIRSTLIGHT / "private-core-mapping.json").read_text())
    with pytest.raises(MappingIncomplete, match="root_evaluator"):
        parse_mapping(raw)


def test_the_image_admits_no_movement_which_is_why_unestablished_movement_is_safe_here():
    """Previously true by accident; now a checked constant. When a profile emits edges this flips."""
    from columna_core.compiler.compile_v2 import K0_EMITS_MOVEMENT
    assert K0_EMITS_MOVEMENT is False
    image = compile_v2(_pub(), _map())
    assert "HIERARCHY" not in image.text and "->" not in image.text


# ══ conformance: governed law vs this engine ═════════════════════════════════════════════════════
@pytest.mark.parametrize("law_name,operator", sorted(K0_LAWS.items()))
def test_core_combines_the_way_the_governed_continuation_law_says(law_name, operator):
    """Cross-check, not a re-derivation. The vocabulary says which law continues values formed by
    this law; the engine says how it merges partial results. They must agree."""
    governed_continuation = fdn.LAWS[law_name].entails_continuation
    assert REGISTRY[operator].combine == K0_LAWS[governed_continuation], (
        f"{law_name}: governed continuation {governed_continuation} vs engine combine "
        f"{REGISTRY[operator].combine!r}")


@pytest.mark.parametrize("law_name,operator", sorted(K0_LAWS.items()))
def test_the_governed_value_domains_agree_with_the_engine_signature(law_name, operator):
    from columna_core.compiler.compile_v2 import _DOMAIN_TO_DTYPE
    law, op = fdn.LAWS[law_name], REGISTRY[operator]
    for domain in sorted(law.operand_domains):
        dtype = _DOMAIN_TO_DTYPE[domain]
        from columna_core.operators import signature_ok
        assert signature_ok(op, dtype), (
            f"{law_name} admits governed domain {domain!r} -> {dtype}, which Core's {operator!r} "
            f"does not accept")


# ══ migration: a proposal, never a publication ═══════════════════════════════════════════════════
def test_the_migration_tool_produces_a_proposal_and_cannot_produce_a_publication():
    from columna_core.governed import migrate
    pub = json.loads((FIRSTLIGHT / "governed-publication.json").read_text())
    mp = json.loads((FIRSTLIGHT / "private-core-mapping.json").read_text())
    proposal = migrate.propose(pub, mp)
    d = proposal.to_dict()
    assert d["status"].startswith("PROPOSAL")
    assert "publication_format_version" not in json.dumps(d)
    assert not hasattr(migrate, "migrate")          # no code path emits a v2 artifact
    assert not any(n.startswith("write") or n.startswith("emit") for n in dir(migrate))


def test_the_proposal_surfaces_the_count_target_and_does_not_choose_one():
    from columna_core.governed import migrate
    pub = json.loads((FIRSTLIGHT / "governed-publication.json").read_text())
    mp = json.loads((FIRSTLIGHT / "private-core-mapping.json").read_text())
    text = migrate.render(migrate.propose(pub, mp))
    assert "WHICH count?" in text
    assert "distinct targets" in text


def test_the_proposal_does_not_assume_the_legacy_sum_member_is_a_family():
    from columna_core.governed import migrate
    pub = json.loads((FIRSTLIGHT / "governed-publication.json").read_text())
    mp = json.loads((FIRSTLIGHT / "private-core-mapping.json").read_text())
    proposal = migrate.propose(pub, mp)
    sums = [c for c in proposal.candidates if c.proposed_reference == "revenue_sum"]
    assert sums and sums[0].classification == migrate.UNDECIDED
    assert any("CONTINUED under another name" in u.question for u in sums[0].unresolved)


def test_the_proposal_records_that_the_legacy_member_bodies_were_byte_identical():
    from columna_core.governed import migrate
    pub = json.loads((FIRSTLIGHT / "governed-publication.json").read_text())
    mp = json.loads((FIRSTLIGHT / "private-core-mapping.json").read_text())
    assert migrate.propose(pub, mp).evidence["member_bodies_byte_identical"] is True


# ══ end to end: law -> image -> served numbers ═══════════════════════════════════════════════════
def _warehouse(tmp_path):
    import duckdb
    con = duckdb.connect(str(tmp_path / "lighthouse.duckdb"))
    con.execute("CREATE SCHEMA IF NOT EXISTS main")
    con.execute("CREATE TABLE main.sales_lines (store_id VARCHAR, sale_date DATE, amount DOUBLE)")
    con.executemany("INSERT INTO main.sales_lines VALUES (?, ?, ?)", lh.ROWS)
    return con


def test_an_established_law_compiles_parses_checks_and_serves(tmp_path):
    """The whole path, on real data: governed law -> a Core image -> a served number.

    The numbers are asserted against the fixture ROWS rather than against the engine, so this fails
    if the family the law established is not the family that got served."""
    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_manifold

    image = compile_v2(_pub(), _map())
    manifold = parse_manifold(image.text)
    problems = manifold.check() if hasattr(manifold, "check") else []
    assert not problems, problems

    con = _warehouse(tmp_path)
    srv = ManifoldServer(manifold, DuckDBConnector(con))
    srv.publish()

    fr = (srv.frame("store")
          .column("total", "revenue.sum")
          .column("n", "revenue.count")
          .column("lo", "revenue.min")
          .column("hi", "revenue.max")
          .run())
    got = {r["store"]: r for r in fr.data.sort("store").iter_rows(named=True)}

    expected = {}
    for store, _day, amount in lh.ROWS:
        e = expected.setdefault(store, {"total": 0.0, "n": 0, "lo": amount, "hi": amount})
        e["total"] += amount
        e["n"] += 1
        e["lo"] = min(e["lo"], amount)
        e["hi"] = max(e["hi"], amount)

    assert set(got) == set(expected)
    for store, e in expected.items():
        assert got[store]["total"] == pytest.approx(e["total"]), store
        assert got[store]["n"] == e["n"], store
        assert got[store]["lo"] == pytest.approx(e["lo"]), store
        assert got[store]["hi"] == pytest.approx(e["hi"]), store


def test_the_served_count_is_the_target_the_family_declared(tmp_path):
    """§11.5.1's distinction, made observable. `lighthouse` declares `count(x@I)` — SUPPORTED
    observations — so a row whose amount is absent must not be counted. In v1 this was the P1-10
    seam: `count` delivered `count(*)` and counted the point instead."""
    import duckdb
    from columna_core import DuckDBConnector, ManifoldServer
    from columna_core.parser import parse_manifold

    con = duckdb.connect(str(tmp_path / "gap.duckdb"))
    con.execute("CREATE SCHEMA IF NOT EXISTS main")
    con.execute("CREATE TABLE main.sales_lines (store_id VARCHAR, sale_date DATE, amount DOUBLE)")
    con.executemany("INSERT INTO main.sales_lines VALUES (?, ?, ?)",
                    lh.ROWS + [("s1", "2026-08-04", None)])

    srv = ManifoldServer(parse_manifold(compile_v2(_pub(), _map()).text), DuckDBConnector(con))
    srv.publish()
    fr = srv.frame("store").column("n", "revenue.count").run()
    got = {r["store"]: r["n"] for r in fr.data.iter_rows(named=True)}
    assert got["s1"] == 3, (
        "the family declared count(x@I) — supported revenue observations — and a point with no "
        "recorded amount is not one of them")


# ══ the frozen v1 path ═══════════════════════════════════════════════════════════════════════════
def test_the_v1_compiler_carries_its_tombstone_and_names_its_successor():
    from columna_core.compiler import compile as v1
    doc = v1.__doc__ or ""
    assert "TOMBSTONE" in doc and "FROZEN" in doc
    assert "compile_v2" in doc


def test_the_v1_compiler_has_not_acquired_a_new_caller():
    """A frozen producer that quietly gains callers is not frozen.

    The pinned set is: the `firstlight` fixture's runtime stage (which rebuilds an image already
    published under v1), and the tests that cover it. Anything else reaching for `compile_k0` is a
    new v1 publication path, which the hard break forbids."""
    root = pathlib.Path(__file__).resolve().parents[3]
    allowed = {
        "packages/columna-server/fixtures/firstlight/build.py",
        "packages/columna-core/tests/test_k0_compiler.py",
        "packages/columna-core/tests/test_governed_v2.py",
        "packages/columna-server/tests/test_k0_governed_producer.py",
        "packages/columna-server/tests/test_lowering_receipt.py",
        "packages/columna-server/tests/test_provisioner.py",
        "packages/columna-server/tests/test_firstlight_governed_fixture.py",
        "packages/columna-core/src/columna_core/compiler/__init__.py",
        "packages/columna-core/src/columna_core/compiler/compile.py",
    }
    callers = set()
    for path in root.glob("packages/**/*.py"):
        rel = path.relative_to(root).as_posix()
        if "compile_k0" in path.read_text(encoding="utf-8"):
            callers.add(rel)
    unexpected = sorted(callers - allowed)
    assert not unexpected, (
        f"new caller(s) of the FROZEN v1 compiler: {unexpected}. Publication v2 is a hard break; a "
        f"v1 artifact migrates through proposal-and-establishment, not through this path.")
