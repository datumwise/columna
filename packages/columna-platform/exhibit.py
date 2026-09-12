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
