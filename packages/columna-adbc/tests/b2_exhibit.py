"""
B-2 · **cold to warm, through a real database.** The vertical integration proof, as a runnable narrative.

    **Cold Frame-QL request → real DuckDB/ADBC realization → Arrow → independent fidelity adjudication →
    ordinary MME admission → serve; identical warm request → MME serve with zero additional backend work.**
    — Huayin, 2026-09-30 (B-2, the milestone)

Everything above the crossing already existed and was proved in isolation: F-1 built the serving loop, R-1
built the estate seam, B-0b split authorization from cache adjudication, B-1' built the fidelity boundary.
What had never happened is all of it composing over a real backend, driven by real Frame-QL text. This file
is that, and it is deliberately one family, one anchor, one backend and one request pair.

WHAT IS *NOT* PROVED HERE, ON PURPOSE. No continuation (the target IS the root), no expression, no second
family, no second provider, no persistence, no cache policy. B-2 proves a materialization CAN be retained
and reused, not when it SHOULD be.
"""
from __future__ import annotations

import tempfile

import b2_revenue_warehouse as W

from columna_adbc import DuckDbAdbcSource, DuckDbFamilyProvider
from columna_platform.columnar import exhibit as CEX
from columna_platform.columnar.mme import ColumnarMME
from columna_platform.frameql import FrameQLService
from columna_platform.kernel import IN_MEMORY, MME, REGISTRY, FulfillmentCoordinator
from columna_platform.kernel.observation import RecordingObserver
from columna_platform.kernel.realization_manager import RealizationManager

MANIFOLD = "andfam.commerce"
#: The request, in Frame-QL, at `revenue`'s own root. **One string, issued twice.**
ASK = "SELECT revenue AT {store, day, order}"


class FailOnCall:
    """A source that refuses to be read. **The stronger warm control** (§10): once the materialization is
    admitted, serving must not depend on the backend being reachable at all."""

    name = "commerce-warehouse-offline"

    def __init__(self, real):
        self.real, self.fetches = real, real.fetches

    def fetch(self, **kwargs):
        raise AssertionError("the backend was contacted for a request the MME should have served")

    def versions(self):
        return self.real.versions()


def cold_world(path: str, *, observer=None, provider_name: str = "duckdb-warehouse"):
    """A **constituted and empty** columnar MME, plus the estate that can fill it.

    Constituted means: the Manifold declares `revenue`, its law, its root and its witness. Empty means: no
    value of it is held anywhere. That is the state in which `measure` says *"lawful, and I do not hold
    it"* — the `NEED` that R-1 introduced a second actor for and that nothing could act on until now.

    **NO ROOT IS ESTABLISHED HERE.** Every other exhibit in this repository seals its roots in `build()`
    and is therefore always warm; the cold request in this one has to reach the warehouse or fail."""
    authority = MME(CEX.COMMERCE, REGISTRY, IN_MEMORY, manifold=MANIFOLD)
    authority.register_family(CEX._families(MANIFOLD)[0])          # revenue, and nothing else
    # **THE OBSERVER GOES ON THE ENGINE THAT SERVES, WHICH IS THE COLUMNAR ONE.** The two engines keep
    # their own workload logs because they hold different material; the authority above them is asked
    # constitutional questions and does not serve, so a request never appears in its log.
    mme = ColumnarMME(authority, observer=observer if observer is not None else RecordingObserver())

    source = DuckDbAdbcSource(path=path, name="commerce-warehouse")
    provider = DuckDbFamilyProvider(source, W.binding(), name=provider_name)
    coordinator = FulfillmentCoordinator(mme, realization=RealizationManager(provider), rounds=1)
    service = FrameQLService(mme, coordinator=coordinator)
    return mme, service, source, provider, coordinator


def _rule(title: str) -> None:
    print(f"\n{'─' * 100}\n{title}\n{'─' * 100}")


def main() -> int:                                              # noqa: C901 - an exhibit is a narrative
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        print(f"    {'✓' if condition else '✗'} {label}")
        if not condition:
            failures.append(label)

    observer = RecordingObserver()
    warehouse = W.build(tempfile.mkdtemp())
    mme, service, source, provider, coordinator = cold_world(warehouse, observer=observer)

    print("═" * 100)
    print("  COLUMNA PLATFORM · B-2 · one real backend, cold to warm")
    print(f"  manifold {MANIFOLD!r}   engine {type(mme).__name__}   provider {provider.name!r}")
    print(f"  warehouse {warehouse}")
    print(f"  driver    {provider.versions()}")
    print(f"  binding   {W.binding()}")
    print("  the MME is CONSTITUTED AND EMPTY: no root is established before the first request")
    print("═" * 100)

    # ══ 1 · THE COLD REQUEST. Frame-QL text in; a database is read; a value is served. ════════════
    _rule("PROOF 1 · the COLD Frame-QL request drives the whole loop")
    print(f"  $ {ASK}")
    cold = service.serve(ASK)
    print()
    print("\n".join("  " + line for line in cold.render().splitlines()))
    print()
    check("the cold request SERVES", cold.classification == "serve")
    check("the backend was read exactly once", len(source.fetches) == 1)
    print(f"      backend fetch attempts = {len(source.fetches)}")
    print(f"      SQL                    = {source.fetches[0][3]}")
    check("the projection is BARE — no aggregate, no predicate, no join, no GROUP BY",
          all(token not in source.fetches[0][3].upper()
              for token in ("GROUP BY", "SUM(", "WHERE", "JOIN", "ORDER BY", "*")))
    check(f"the unrequested {W.UNREQUESTED_COLUMN!r} column was never projected",
          W.UNREQUESTED_COLUMN not in source.fetches[0][3])
    check("six governed root points came back", len(cold.frame.rows) == len(W.ORDERS))

    # ══ 2 · WHAT THE ESTATE ACTUALLY DID, AS THE COORDINATOR REPORTS IT ═══════════════════════════
    _rule("PROOF 2 · one realization, adjudicated and admitted through the ordinary door")
    outcome = coordinator.fulfill("revenue", mme.family("revenue").root)
    for route in outcome.realized:
        print(f"      realized {route}")
    print("      rounds used on the cold request = 1; backend realizations = 1")
    check("the second fulfilment needed no realization at all", not outcome.realized)
    check("and it still served", outcome.served)
    check("the backend was STILL read only once", len(source.fetches) == 1)

    # ══ 3 · THE WARM REQUEST. The same text, and the database is not touched. ══════════════════════
    _rule("PROOF 3 · the identical WARM request serves with zero additional backend work")
    before = len(source.fetches)
    warm = service.serve(ASK)
    print("\n".join("  " + line for line in warm.render().splitlines()))
    print()
    check("the warm request SERVES", warm.classification == "serve")
    check("backend fetch attempts are UNCHANGED", len(source.fetches) == before == 1)
    print(f"      backend fetch attempts before = {before}, after = {len(source.fetches)}")
    check("and it served the same values", warm.frame.rows == cold.frame.rows)

    # ══ 4 · THE STRONGER CONTROL. Warm serving does not depend on the backend existing. ════════════
    _rule("PROOF 4 · the backend is taken offline and the warm request still serves")
    coordinator.realization = RealizationManager(
        DuckDbFamilyProvider(FailOnCall(source), W.binding(), name=provider.name))
    offline = service.serve(ASK)
    check("the request serves from the MME with a provider that raises on contact",
          offline.classification == "serve")
    check("and the values are unchanged", offline.frame.rows == cold.frame.rows)
    check("fetch attempts never moved", len(source.fetches) == 1)

    # ══ 5 · TWO USER REQUESTS, ONE BACKEND REALIZATION — AND THE LEVELS ARE KEPT APART ════════════
    _rule("PROOF 5 · user demand and fulfilment attempts are two counters, not one")
    records = observer.records
    print("  Ruled (Huayin, 2026-09-30, §9): *\"do not force `request frequency = 2` from the internal")
    print("  coordinator retry… do not casually call those two internal MME observations two user")
    print("  requests.\"* So the three levels are printed as three, and the exhibit asserts on the one")
    print("  that answers the cache question — the BACKEND counter.")
    print()
    print("      Frame-QL requests issued by the user      = 3   (cold · warm · offline)")
    print("      + one diagnostic coordinator.fulfill      = 1   (PROOF 2 — NOT a user request)")
    print(f"      MME request observations                  = {len(records)}   (the cold one is TWO: "
          f"its NEED and its retry)")
    for record in records:
        print(f"        {record.seq}  {record.request.family_id}@{record.request.target} "
              f"→ {record.disposition}/{record.route}")
    print(f"      backend fetch attempts                    = {len(source.fetches)}")
    check("the cold request produced TWO MME observations — the NEED and the retry that was READY",
          [r.disposition for r in records[:2]] == ["need", "ready"])
    check("every later request produced exactly one READY",
          all(r.disposition == "ready" for r in records[2:]))
    check("and only ONE of them cost a backend read", len(source.fetches) == 1)
    check("the observation seam is UNCHANGED — nothing was added to it to make this countable",
          not hasattr(records[0], "backend_realizations"))
    print("      NOTE the seam counts REQUESTS and was not taught to count backend work. The cache")
    print("      proof reads the provider's own fetch log, which is where physical work is visible.")

    print("\n" + "═" * 100)
    if failures:
        print(f"  {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"    ✗ {f}")
        return 1
    print("  ALL CHECKS PASSED")
    print("  B-2: cold Frame-QL → DuckDB/ADBC → Arrow → fidelity → ordinary admission → serve;")
    print("       identical warm request → MME serve, backend untouched.")
    print("═" * 100)
    return 0


if __name__ == "__main__":                                      # pragma: no cover - manual invocation
    raise SystemExit(main())
