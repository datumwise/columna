"""Proof A, exhibited — run the path and print what it decided, and where it stopped.

    python packages/columna-platform/exhibit.py
"""
from pathlib import Path

from columna_platform import admission, carrier, serving
from columna_platform.refusals import ProofRefusal
from columna_platform.state import AnalyticalIdentity, RetainedStateStore

REVENUE = "fam_qv8Ky3mR7bTpZa1LwXcNdg"
HERE = Path(__file__).resolve().parent
PUBLICATION = HERE.parent / "columna-core" / "tests" / "fixtures_v2" / "lighthouse-v2-publication.json"
MAPPING = HERE / "fixtures" / "proof_a" / "private-core-mapping-v2.json"
CONSTITUTION = "fcf-1:c176d2a4f35e443c84e03e6cff3c27a1088b390887e15ae59d1312129e3840ce"


def rule(t=""):
    print(f"\n── {t} " + "─" * max(0, 76 - len(t)))


def main():
    rule("THE GOVERNED PATH")
    pub, views = serving.open_publication(PUBLICATION)
    print(f"publication        {pub.ref}  (format v{pub.format_version})")
    mapping = serving.bind(pub, MAPPING)
    print(f"mapping            format v{mapping.mapping_format_version} -> {mapping.publication_ref}"
          f"   BINDING CHECKED FIRST")
    family = [f for f in pub.families if f.family_id == REVENUE][0]
    view = views[REVENUE]
    real = serving.realize(mapping, REVENUE)
    print(f"family             {family.canonical_reference}  [{family.family_id}]")
    print(f"  C5 participation {view['eligibility_and_participation'].value}")
    print(f"  C6 value domain  {view['semantic_values'].value}")
    print(f"  C7 basis         {view['sufficient_state_bases'].value}   <- projected in, not re-derived")
    print(f"  C3 movement      {view['domain_and_movement'].standing}")
    print(f"  C9 exceptional   {view['exceptional_cases'].standing}: {view['exceptional_cases'].value}")
    print(f"realization claim  {real.endpoint.connection}:{real.endpoint.schema}."
          f"{real.endpoint.table}.{real.endpoint.column}  grain={real.grain} exactness={real.exactness}")

    rule("POSITIVE CONTROL — identity and standing survive materialization")
    store = RetainedStateStore()
    st = serving.materialize(family, view, real, carrier.exact_money(),
                             basis=view["sufficient_state_bases"].value,
                             constitution=CONSTITUTION, constitution_scheme="fcf-1",
                             currency="tok-1", store=store)
    print(f"carrier            {carrier.describe(carrier.exact_money())}")
    print(f"admitted as        governed domain {st.governed_domain!r}  (carrier {st.carrier_type})")
    print(f"exact value held   {st.array[0].as_py()}")
    w = serving.decide(view, store, AnalyticalIdentity(REVENUE, family.constitutive_anchor))
    print(f"\nWIRE               contract_version={w['contract_version']!r}  outcome={w['outcome'].upper()}")
    print(f"  anchor           {w['frame']['anchor']}   executed={w['executed']}")
    print(f"  column           {w['columns'][0]['name']}  status={w['columns'][0]['status']}")
    print(f"  values           {[v['value'] for v in w['columns'][0]['values']]}")
    print( "  standing, read off the retained state (never recomputed):")
    held = store.retrieve(AnalyticalIdentity(REVENUE, family.constitutive_anchor))[0]
    for k, v in held.standing.__dict__.items():
        print(f"    {k:20} {v}")

    rule("NEGATIVE CONTROLS — each carrier DELIVERS; admission refuses anyway")
    for label, c in (("binary float where decimal is governed", carrier.lossy_float()),
                     ("decimal128(38,0) full width", carrier.over_envelope()),
                     ("exact decimal containing an absence", carrier.with_absence())):
        try:
            admission.admit(view, real, c)
            print(f"  {label:38} ADMITTED  <-- CONTROL FAILED")
        except ProofRefusal as r:
            print(f"  {label:38} {r.condition}  [{r.jurisdiction}]")
            print(f"    remedy: {r.remedy or 'none — re-realization cannot help'}")
            print(f"    {r.detail[:150]}...")

    rule("WANT-OF-LAW, ON THE WIRE")
    law = serving.decide(view, store, AnalyticalIdentity(REVENUE, "sale_at"), at_anchor="month")
    _print_refusal(law)

    rule("WANT-OF-STATE, ON THE WIRE")
    store.evict(AnalyticalIdentity(REVENUE, "sale_at"))
    state = serving.decide(view, store, AnalyticalIdentity(REVENUE, "sale_at"))
    _print_refusal(state)
    print(f"\n  same mood ({law['outcome']}), different reason and jurisdiction — which is the point.")

    rule("A RETRIEVAL MISS IS NOT A REFUSAL")
    store2 = RetainedStateStore()
    store2._rematerializer = lambda _i: serving.materialize(
        family, view, real, carrier.exact_money(), basis=view["sufficient_state_bases"].value,
        constitution=CONSTITUTION, constitution_scheme="fcf-1", currency="tok-2", store=store2)
    w2 = serving.decide(view, store2, AnalyticalIdentity(REVENUE, "sale_at"))
    print(f"  empty store + a re-materialization path -> outcome={w2['outcome'].upper()}"
          f"   (re-materializations: {store2.rematerializations})")
    print("  the caller never learns the cache missed; `want_of_state` is not `evicted`.")

    rule("C3 STANDING IS NOT A MOVEMENT LICENCE")
    import copy, json as _json
    from columna_core.governed.publication import parse_publication
    from columna_core.governed.resolve import resolve_all
    doc = copy.deepcopy(_json.loads(PUBLICATION.read_text(encoding="utf-8")))
    for dec in doc["logical"]["declarations"]:
        if dec.get("body", {}).get("family_id") == REVENUE:
            dec["body"]["domain"] = "the trading calendar"
    trap = resolve_all(parse_publication(doc))[REVENUE]
    print(f"  C3 standing: {trap['domain_and_movement'].standing}   "
          f"value: {trap['domain_and_movement'].value}")
    print(f"  movement_licence(): {serving.movement_licence(trap)}")
    store3 = RetainedStateStore()
    serving.materialize(family, trap, real, carrier.exact_money(),
                        basis=trap["sufficient_state_bases"].value, constitution=CONSTITUTION,
                        constitution_scheme="fcf-1", currency="tok-1", store=store3)
    w3 = serving.decide(trap, store3, AnalyticalIdentity(REVENUE, "sale_at"), at_anchor="store")
    _print_refusal(w3)
    print(f"\n  {serving.RESPONSIBILITY_STANDING_RULE}")

    rule("PROOF B — ONE POSITIVELY LICENSED MOVEMENT")
    from columna_platform import movement, continuation
    from columna_platform.state import RetainedState
    ac = carrier.exact_money_at_sale_at()
    adm = admission.admit(view, real, ac.as_carrier())
    anchored = RetainedState(
        identity=AnalyticalIdentity(REVENUE, family.constitutive_anchor),
        standing=held.standing, array=adm.array, governed_domain=adm.governed_domain,
        carrier_type=adm.carrier_type, table=ac.table, anchor_columns=ac.anchor_columns)
    print("  state @ sale_at(store*day):")
    for row in zip(*[ac.table.to_pydict()[c] for c in ("store", "day", "amount")]):
        print(f"    {row[0]:6} {row[1]}  {row[2]}")
    lic = movement.project(pub, source_anchor="sale_at", target_anchor="store",
                           target_components=["store"], law="SUM")
    print(f"\n  licence          {lic.describe()}")
    print(f"  validated against DECLARED components {list(lic.source_components)}")
    print(f"  C8 continuation  {continuation.established_continuation_law(view)}")
    moved = continuation.continue_to(view, anchored, lic, target_anchor="store")
    print("\n  continued @ store:")
    for row in zip(*[moved.table.to_pydict()[c] for c in ("store", "amount")]):
        print(f"    {row[0]:6} {row[1]}")
    print(f"  same family      {moved.identity.family_id == REVENUE}   anchor now {moved.identity.anchor!r}")
    print(f"  carrier type     {moved.array.type}  (exact, never widened)")
    print(f"  movement on standing: {moved.standing.movement}")
    st_b = RetainedStateStore(); st_b.insert(anchored)
    wb = serving.decide(view, st_b, anchored.identity, at_anchor="store", licence=lic)
    print(f"\n  WIRE             contract_version={wb['contract_version']!r} outcome={wb['outcome'].upper()}"
          f"  anchor={wb['frame']['anchor']}")
    print(f"  values           {[v['value'] for v in wb['columns'][0]['values']]}")

    rule("PROOF B — MECHANICALLY COMBINABLE, NOT LICENSED")
    from columna_core.operators import get_operator
    op = get_operator("sum")
    print(f"  Operator('sum')  is_monoid={op.is_monoid}  combine={op.combine!r}  -> the fold is MECHANICALLY available")
    st_c = RetainedStateStore(); st_c.insert(anchored)
    _print_refusal(serving.decide(view, st_c, anchored.identity, at_anchor="store", licence=None))

    rule("PROOF C — COMPOSITE SUFFICIENT STATE FOR MEAN")
    import copy as _copy, json as _json2
    from decimal import Decimal as _D
    from columna_core.governed.publication import parse_publication as _pp
    from columna_core.governed.resolve import resolve_all as _ra
    from columna_core.governed.foundation import LAWS as _LAWS
    from columna_platform import composite as _comp
    doc = _copy.deepcopy(_json2.loads(PUBLICATION.read_text(encoding="utf-8")))
    doc["logical"]["declarations"].append({"kind": "family", "name": "revenue_mean", "body": {
        "family_id": "lh-revmean", "canonical_reference": "mean(revenue@sale_at)",
        "universe": "sales", "constitutive_anchor": "sale_at",
        "target": "the arithmetic mean of revenue over participating sale points",
        "formation": {"kind": "construction",
                      "law": {"law": "MEAN", "version": "1", "vocabulary": "datumwise.foundation"},
                      "operands": [REVENUE]},
        "participation": "every sale point carrying a recorded amount"}})
    mv = _ra(_pp(doc))["lh-revmean"]
    print(f"  C8 continuation  {mv['continuation_and_agreement'].standing}   (the displayed mean does not compose)")
    b = _comp.declared_basis(mv)
    print(f"  C7 basis         {mv['sufficient_state_bases'].standing}  {b.components}  "
          f"common participation required = {b.requires_common_participation}")
    print(f"  COUNT component continues under {_LAWS['COUNT'].entails_continuation!r} "
          f"(usable_as_continuation={_LAWS['COUNT'].usable_as_continuation})")

    def _adm(vals):
        return admission.admit(view, real, carrier.Carrier(
            __import__("pyarrow").array([_D(v) for v in vals], type=__import__("pyarrow").decimal128(18, 4)),
            "duckdb DECIMAL(18,4) -> arrow decimal128(18,4), preserved"))
    A, B = _adm(["10.0000", "15.0000", "5.0000"]), _adm(["6.0000"])
    s1, s2 = _comp.constitute(mv, A, anchor="sale_at"), _comp.constitute(mv, B, anchor="sale_at")
    print(f"\n  pass 1  SUM={s1.component('SUM').value} COUNT={s1.component('COUNT').value}  pass_id={s1.witness.pass_id[:8]}")
    print(f"  pass 2  SUM={s2.component('SUM').value} COUNT={s2.component('COUNT').value}  pass_id={s2.witness.pass_id[:8]}")
    comb = _comp.continue_composite(s1, s2)
    print(f"  continued  SUM={comb.component('SUM').value} COUNT={comb.component('COUNT').value}")
    fin = _comp.finalize(comb)
    print(f"  FINALIZED  mean = {fin.value}   is_sufficient_state={fin.is_sufficient_state}")
    st_c = RetainedStateStore()
    st_c.insert(RetainedState(identity=AnalyticalIdentity("lh-revmean", "sale_at"),
                              standing=held.standing, array=None, governed_domain="decimal",
                              composite=comb))
    wc = serving.decide(mv, st_c, AnalyticalIdentity("lh-revmean", "sale_at"), column="mean_revenue")
    print(f"  WIRE       contract_version={wc['contract_version']!r} outcome={wc['outcome'].upper()}"
          f"  value={wc['columns'][0].get('value')}")

    rule("PROOF C — THE PAIR NOBODY CONSTITUTED")
    from columna_platform.refusals import ProofRefusal as _PR
    try:
        _comp.pair(s1.component("SUM"), s2.component("COUNT"), family_id="lh-revmean", anchor="sale_at")
        print("  PAIRED  <-- CONTROL FAILED")
    except _PR as r:
        print(f"  same participation rule: {s1.witness.same_participation(s2.witness)}   "
              f"same pass: {s1.witness.matches(s2.witness)}")
        print(f"  {r.condition} [{r.jurisdiction}]  {r.detail[:150]}...")

    rule("EMPTY-FIBER LAW IS NOT ABSENCE LAW")
    from columna_platform.admission import EMPTY_FIBER_RULING
    print(f"  C9 standing: {view['exceptional_cases'].standing}   value: {view['exceptional_cases'].value}")
    print(f"  {EMPTY_FIBER_RULING}")


def _print_refusal(w):
    nr = w["columns"][0]["no_result"]
    from columna_core.disclosure import jurisdiction_for
    print(f"  outcome          {w['outcome'].upper()}")
    print(f"  kind/disc        {nr['kind']} / {nr['discriminator']}")
    print(f"  reason           {nr['reason']}   [jurisdiction: {jurisdiction_for(nr['reason'])}]")
    print(f"  remedy           {[a['token'] for a in nr['alternatives']] or 'none'}")
    print(f"  detail           {nr['detail'][:120]}...")


if __name__ == "__main__":
    main()
