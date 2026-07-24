"""
columna_core.engine — the column engine (the center of Core).

For a request (measure, family_member) @ target_anchor, the engine:
  1. finds the functional path from the universe's base dims to each target level,
  2. B-anchor-checks every transport edge AND every COLLAPSED dimension (per-lineage),
  3. resolves cheapest faithful (cache vs stored delivery),
  4. TRANSPORTS the delivered measure-column along functional edges (rollup & relationship
     are the same operation) — relating columns IN THE ENGINE, never asking the backend to join,
  5. co-computes the disclosure and caches the result.

A B-anchor crossing is DETECTED here (statically, from the spec) and SERVED with a critical
disclosure naming the alternative reducer — never refused (inform-and-serve, ADR-020). An
absent functional path (fan-out across an M:N edge) is a planner-side clarification, surfaced
as a Refusal carrying the three remedies. (Fan-out / out-of-universe are normally caught
earlier, at the planner; the engine's guard is the backstop.)
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import polars as pl

from .model import Manifold, parse_faced, ASSIGN, ALLOC, ORDER_MIN
from .operators import get_operator, VALUE, ORDERED_W as ORDERED, HOLISTIC as OP_HOLISTIC, SKETCH as OP_SKETCH
from .sketch import (hll_count, hll_merge, hll_estimate, rse, Witness, WitnessStore)
from .disclosure import (Disclosure, Caveat, Refusal, AMBIGUOUS,
                         FRESHNESS, APPROXIMATION, TRANSPORT, UNCONFIRMED, OVER_COUNT, SHADOW, RECONCILIATION)


@dataclass
class CacheEntry:
    frame: pl.DataFrame
    sketches: Optional[dict] = None
    version: str = ""


@dataclass
class EngineStats:
    deliveries: int = 0
    transports: int = 0
    cache_hits: int = 0


class ColumnEngine:
    def __init__(self, manifold: Manifold, connector):
        self.m = manifold
        self.con = connector
        self.cache: dict = {}
        self.witnesses = WitnessStore()      # publish-time materialized sketches (stored, not cached)
        self.stats = EngineStats()

    # ---- public: resolve one canonical atom -------------------------------
    def resolve(self, measure: str, member: str, target: tuple,
                where: Optional[str] = None, trace: Optional[list] = None):
        meas = self.m.measures[measure]
        uni = meas.universe
        base = set(self.m.universes[uni].base_dimensions)
        fam = meas.family[member]
        op = get_operator(fam.agg)              # reaggregability is operator-level (the registry)

        # FACED coordinate — a TOUCH crossing across a non-functional (M:N) edge. The value join-
        # multiplies through the relation's VIA bridge to the faced grain (deliberate multi-count,
        # served DISCLOSE). v1 handles a single faced coordinate (the `revenue AT {category.touch}` case).
        faced = [T for T in target if parse_faced(T, self.m.non_functional) is not None]
        if faced:
            return self._resolve_faced(meas, fam, op, target, faced, where, trace)

        # paths to each target level
        paths = {}
        for T in target:
            p = self.m.find_path(base, T)
            if p is None:
                # No functional path = an aggregate-across a non-traversable (M:N) edge: fan-out.
                # This is a PLANNER clarification (the query is underdetermined), not analytical
                # withholding — transport != join, so the membership number is not expressible
                # without one of the three declared resolutions.
                raise Refusal("non_functional_transport",
                              f"'{measure}' cannot be aggregated across to '{T}': the edge into "
                              f"'{T}' is non-functional (M:N). This aggregate-across is "
                              f"underdetermined without a declared resolution",
                              measure=measure, target=str(target),
                              alternatives=("membership filter (accept the overlap deliberately)",
                                            "primary designation (make the edge functional)",
                                            "WITH allocation (supply a partition-of-unity) [Pro]"))
            paths[T] = p

        # B-anchor crossing DETECTION has moved to the planner (it is structural — shape, not
        # provenance — so it lives in the shape projection, alongside fan-out / out-of-universe).
        # The engine still SERVES the crossing result unchanged; it just no longer detects it.

        self._t(trace, f"resolve {measure}.{member} @ {target}  "
                       f"[{op.name}: {'monoid/' + op.witness if op.is_monoid else 'HOLISTIC (recompute-from-base)'}]")

        # cache (exact). Holistic results are reduction-sterile: memoize exact, never as a seed.
        key = (measure, member, target, uni, where)
        ver = self.con.table_version(meas.home_table)
        if key in self.cache and self.cache[key].version == ver:
            self.stats.cache_hits += 1
            self._t(trace, "  cache-hit")
            disc = self._disc(meas, fam, op, uni).with_caveat(Caveat(FRESHNESS, "served from cache"))
            return self.cache[key].frame, disc

        # deliver + (reduce | recompute), dispatched by the operator's witness
        if op.witness == OP_SKETCH:
            frame, sk = self._resolve_sketch(meas, member, target, paths, where, trace)
            self.cache[key] = CacheEntry(frame, sk, ver)
        elif op.witness == OP_HOLISTIC:
            frame = self._recompute_holistic(meas, fam, op, target, paths, where, trace)
            self.cache[key] = CacheEntry(frame, None, ver)     # exact-memoize only; not a reduction seed
        else:   # VALUE or ORDERED — both reduce in witness-space
            frame = self._deliver_and_transport_monoid(meas, fam, op, target, paths, where, trace)
            self.cache[key] = CacheEntry(frame, None, ver)
        return frame, self._disc(meas, fam, op, uni)

    # ---- public: resolve one SCAN (order-dependent, anchor-preserving) ----
    _TEMPORAL_LINEAGES = {"calendar", "fiscal"}

    def _orderable_levels(self) -> set:
        """Levels that carry a natural order — those on a temporal lineage. The manual's
        'typically a temporal dimension'; Core reads it off the edge lineages."""
        lv = set()
        for e in self.m.edges:
            if e.lineage in self._TEMPORAL_LINEAGES:
                lv.add(e.frm); lv.add(e.to)
        return lv

    def scan(self, measure: str, member: str, target: tuple, scan_op: str,
             n: int = 1, by: Optional[str] = None,
             where: Optional[str] = None, trace: Optional[list] = None):
        """A scan is an order-dependent map: it reduces the measure to `target` (the reducer
        atom — anchor-preserving), derives an order from the anchor (or `by=`), partitions by
        the rest, and walks the order. The planner routes here knowing only the name/kind/
        signature; the order-walking mechanics live here. Order-only scans are Core; windowed
        (rolling_*) scans are Pro."""
        op = get_operator(scan_op)
        if not op.in_core:
            raise Refusal("unsupported",
                f"scan '{scan_op}' needs a window= parameter; windowed scans are Pro in this build",
                measure=measure, target=str(target),
                alternatives=("use an order-only scan (cumsum/cummax/cummin/lag/lead/pct_change)",
                              "windowed scans (rolling_*) [Pro]"))

        # 1) the scan input IS the reducer atom served at the (preserved) anchor — and it carries
        #    its own disclosure (e.g. a B-anchor crossing on the underlying reduction rides through).
        frame, disc = self.resolve(measure, member, target, where, trace)

        # 2) derive the order axis (manual ch.2.8 / 5.5): one orderable anchor level, or by=.
        orderable = self._orderable_levels() & set(target)
        if by is not None:
            order_axis = by
        elif len(orderable) == 1:
            order_axis = next(iter(orderable))
        elif not orderable:
            raise Refusal("unknown",
                f"scan '{scan_op}' @ {target} has no derivable order axis (no temporal level in "
                f"the anchor); name it with by=<level>", measure=measure, target=str(target))
        else:
            raise Refusal("unknown",
                f"scan '{scan_op}' @ {target} order axis is ambiguous ({sorted(orderable)}); "
                f"name it with by=<level>", measure=measure, target=str(target))

        partition = [d for d in target if d != order_axis]
        f = frame.sort(partition + [order_axis]) if partition else frame.sort(order_axis)
        v = pl.col("_value")
        expr = {"cumsum": v.cum_sum(), "cummax": v.cum_max(), "cummin": v.cum_min(),
                "lag": v.shift(n), "lead": v.shift(-n),
                "pct_change": (v / v.shift(n) - 1.0)}[op.scan_impl]
        f = f.with_columns((expr.over(partition) if partition else expr).alias("_value"))
        self._t(trace, f"  scan {scan_op} ordered by '{order_axis}'"
                       + (f", partitioned by {partition}" if partition else "")
                       + " (planner routed; engine walked the order)")
        disc = disc.with_caveat(Caveat(TRANSPORT,
            f"scan {scan_op} over order '{order_axis}'"
            + (f" within {partition}" if partition else "")))
        return f, disc

    # ---- monoid delivery + reduce (VALUE and ORDERED) ---------------------
    def _deliver_and_transport_monoid(self, meas, fam, op, target, paths, where, trace):
        start = {T: paths[T][0] for T in target}
        base_levels = list(dict.fromkeys(start.values()))
        realized = self.con.realize(meas.home_table, meas.pre_expr, meas.logical_type)

        # build the delivery aggregates: one witness column for VALUE, two for ORDERED
        if op.witness == VALUE:
            aggs = [("_value", op.deliver_sql(realized))]
            order_phys = None
        else:  # ORDERED: witness is (value, order_key)
            if fam.order_by is None:
                raise Refusal("unknown", f"{meas.name}.{op.name} needs an ORDER key")
            order_phys = self.m.levels[fam.order_by].realized_by
            argfn = "arg_max" if op.combine == "argmax" else "arg_min"
            ordfn = "max" if op.combine == "argmax" else "min"
            aggs = [("_value", f"{argfn}({realized}, {order_phys})"),
                    ("_order", f"{ordfn}({order_phys})")]

        # universe confinement: augment grain with predicate base levels, deliver, confine,
        # then collapse augmented-only dims via the operator's combine.
        pred = self.m.universes[meas.universe].predicate
        pred_levels = self._predicate_levels(pred) if pred else []
        grain = list(dict.fromkeys(base_levels + [l for l in pred_levels if l not in base_levels]))
        grain_phys = [self.m.levels[b].realized_by for b in grain]

        # ORDERED ops resolve to the last/first ACTUAL observation: exclude null values so
        # argmax lands on the last real snapshot (matches SQL arg_max(value, key) semantics).
        where_eff = where
        if op.witness == ORDERED:
            nn = f"({realized}) IS NOT NULL"
            where_eff = f"({where}) AND {nn}" if where else nn

        frame = self.con.deliver_measure(meas.home_table, grain_phys, aggs, where_eff)
        self.stats.deliveries += 1
        frame = frame.rename({self.m.levels[b].realized_by: b for b in grain})
        wit = "(value,order)" if op.witness == ORDERED else "value"
        self._t(trace, f"  deliver {meas.name}.{op.name} @ base {grain} [witness={wit}] (1-table group-by)")

        if pred is not None:
            before = frame.height
            frame = self._confine(frame, meas, pred, trace)
            self._t(trace, f"  confine to universe '{meas.universe}' [{self._pred_str(pred)}]: "
                           f"{before}->{frame.height} base points")

        if grain != base_levels:
            frame = frame.group_by(base_levels).agg(self._combine_exprs(op))

        # DEPENDENT-PAIR completion: a target level fixed by another target level (S->..->T functional)
        # is an ATTRIBUTE, attached 1:1, never a reduction axis (else it collapses its determiner). The
        # rest reduce as before.
        reduction, dependent = self._split_dependent_targets(target)
        for T in reduction:
            cur, path = start[T], paths[T][1]
            for e in path:
                mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
                frame = self._transport_reduce(frame, cur, e.to, mp, op)
                self.stats.transports += 1
                self._t(trace, f"  transport {cur}->{e.to} along {e.lineage} "
                               f"[combine={op.combine}] (in-engine, no join pushdown)")
                cur = e.to
        for T in dependent:
            cur, path = start[T], paths[T][1]
            for e in path:
                mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
                frame = self._transport_attach(frame, cur, e.to, mp)
                self.stats.transports += 1
                self._t(trace, f"  attach {cur}->{e.to} along {e.lineage} (functional 1:1, no collapse)")
                cur = e.to
        return frame.select(list(target) + ["_value"])     # project the witness to the answer

    # ---- TOUCH: join-multiply across a non-functional (M:N) edge ----------
    def _resolve_faced(self, meas, fam, op, target, faced, where, trace):
        """Dispatch a faced crossing (M:N passage, notes v0.2 §3 P2) by the declared face scheme, after
        the crossing guards that are UNIFORM across all three schemes:
          · G4 the chain guard — a multi-hop face path is not yet licensed (disclosure-stacking undesigned);
          · the events-only serving law — on a spine, replication/routing corrupts the grid's completeness;
          · the ANCHOR LAW (G5, value-traversal) — a face crosses ADDITIVE (monoid VALUE) values only; a
            distinct-class measure's output anchor is SPENT at the frontier grain (its per-member counts
            cannot be summed, weighted, or routed), so it refuses uniformly for all three schemes. The
            message speaks the DECLARATION dialect (distinct(...)), never the engine's sketch representation."""
        # G4 — the chain guard (DRAFT copy; Huayin ratifies at the merge gate).
        if len(faced) != 1 or len(target) != 1:
            raise Refusal("chained_crossing",
                          "this ask would cross two declared faces in sequence; chained crossings are not "
                          "yet licensed — ask at one frontier at a time.",
                          measure=meas.name, target=str(target))
        T = faced[0]
        coord, fname, rel, face = parse_faced(T, self.m.non_functional)
        uni = meas.universe
        basis = self.m.universes[uni].basis
        if basis is not None and basis != "events":
            raise Refusal("unsupported",
                          f"crossing {rel.frm}<->{rel.to} is events-only in v1: universe '{uni}' is "
                          f"'{basis}' basis, where replication corrupts completeness — declare an events "
                          f"population or use a functional designation",
                          measure=meas.name, target=T)
        # ANCHOR LAW (G5). Additive-VALUE passes; distinct-class refuses with the anchor-law message.
        if not (op.is_monoid and op.witness == VALUE):
            if op.witness == OP_SKETCH:   # distinct-class — the spent anchor (DRAFT copy; Huayin's merge batch)
                poss = meas.name + ("'" if meas.name.endswith("s") else "'s")
                raise Refusal("anchor_spent",
                              f"{poss} distinct anchor is spent at {rel.frm} — per-{rel.frm} counts "
                              f"cannot be summed, weighted, or routed. If a weighted composite of "
                              f"per-{rel.frm} counts is what you mean, declare it as a value measure; if "
                              f"distinct {meas.name} per {rel.to} is what you mean, that is a "
                              f"crossed-population count — coming with the crossing increment.",
                              measure=meas.name, target=T)
            raise Refusal("unsupported",
                          f"faces cross additive (monoid VALUE) measures only — '{meas.name}.{op.name}' is "
                          f"not (ordered/holistic crossings are post-launch)",
                          measure=meas.name, target=T)
        if face.scheme == ASSIGN:
            return self._resolve_assign(meas, fam, op, target, T, coord, rel, face, where, trace)
        if face.scheme == ALLOC:
            return self._resolve_alloc(meas, fam, op, target, T, coord, rel, face, where, trace)
        return self._resolve_touch(meas, fam, op, target, faced, where, trace)

    def _serve_driver(self, face, frontier):
        """Serve a face's DRIVER measure at the frontier grain (a single-valued spine read — the driver
        lemma, notes §4). Returns [frontier, '_drv']. The driver-ref is a DECLARED measure (resolved at
        publish), so this is the engine's own serve path, one hop."""
        dmeas = self.m.measures[face.selection]
        dmember = next(iter(dmeas.family))
        dframe, _ = self.resolve(face.selection, dmember, (frontier,), None, None)
        # cast to Float64 — a DECIMAL driver (from the source column) would normalize in decimal space and
        # ROUND (0.667 -> 0.7), corrupting the split; the partition-of-unity must be full-precision.
        return dframe.rename({"_value": "_drv"}).with_columns(pl.col("_drv").cast(pl.Float64))

    def _resolve_assign(self, meas, fam, op, target, T, coord, rel, face, where, trace):
        """ASSIGN: the value goes to exactly ONE member — the top-ranked pair per the declared driver +
        ORDER direction. Restrict the bridge to each measure-side key's single top pick, then join (no
        multiply). Total reconciles to the grand total; the SHADOW (memberships not picked) is the honest
        disclosure. The frontier square commutes in total while redistributing between members (notes §5)."""
        uni = meas.universe
        base = set(self.m.universes[uni].base_dimensions)
        other = rel.to if coord == rel.frm else rel.frm       # the measure-side endpoint (e.g. product)
        frontier = coord                                       # the crossed level (e.g. category)
        p = self.m.find_path(base, other)
        if p is None:
            raise Refusal("non_functional_transport",
                          f"'{meas.name}' cannot reach '{other}' to cross to '{T}'", measure=meas.name, target=T)
        frame = self._deliver_and_transport_monoid(meas, fam, op, (other,), {other: p}, where, trace)
        driver = self._serve_driver(face, frontier)           # [frontier, _drv]
        if other == rel.frm:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_frm_col, rel.via_to_col)   # _frm=other, _to=frontier
        else:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_to_col, rel.via_frm_col)
        b = bridge.join(driver.rename({frontier: "_to"}), on="_to", how="inner")             # _frm, _to, _drv
        n_memberships = b.height
        picked = (b.sort("_drv", descending=(face.order != ORDER_MIN))
                    .group_by("_frm").first().select(["_frm", "_to"]))                        # one pick per measure-side key
        n_assigned = picked.height
        n_shadow = n_memberships - n_assigned
        # coverage (the absence law): a measure-side key in NO membership is dropped from every cell.
        covered = picked.select(pl.col("_frm").alias(other)).unique()
        n_total = frame.height
        uncovered = frame.join(covered, on=other, how="anti")
        assigned = self._transport_reduce(frame, other, T, picked, op)                        # single-count join
        # crossed-grain absence — events basis: complete the domain from the bridge, fill 0.
        domain = bridge.select(pl.col("_to").alias(T)).unique()
        assigned = domain.join(assigned, on=T, how="left").with_columns(pl.col("_value").fill_null(0))
        assigned = assigned.sort(T).select([T, "_value"])
        self.stats.transports += 1
        self._t(trace, f"  assign {other}->{T} via {rel.via_table} ORDER {face.order} on {face.selection} "
                       f"[single-count; shadow {n_shadow}; coverage {n_total - uncovered.height}/{n_total}]")
        disc = self._assign_disc(meas, fam, op, uni, rel, face, n_shadow, n_total, uncovered)
        return assigned, disc

    def _assign_disc(self, meas, fam, op, uni, rel, face, n_shadow, n_total, uncovered):
        base = self._disc(meas, fam, op, uni)
        note = face.description or (f"{meas.name} goes to each {rel.frm}'s top {face.selection} {rel.to}")
        base = base.with_caveat(Caveat(SHADOW,
            f"single-counted to each {rel.frm}'s ORDER {face.order} {face.selection} {rel.to}: "
            f"{n_shadow} memberships unrepresented (the shadow). {note}", severity="caution", shadow=n_shadow))
        if uncovered.height:
            base = base.with_caveat(Caveat(TRANSPORT,
                f"{uncovered.height} of {n_total} {rel.frm} are in no {rel.to} — dropped from every cell; "
                f"coverage {n_total - uncovered.height}/{n_total}", severity="info"))
        return base

    def _resolve_alloc(self, meas, fam, op, target, T, coord, rel, face, where, trace):
        """ALLOC: the value SPLITS across a measure-side key's members by the NORMALIZED driver
        (driverᵢ / Σ per member — the declared law, applied here, never stored). Where the driver covers,
        splitting preserves mass everywhere; the RECONCILIATION badge is the commutation certificate
        (notes §5, alloc COMMUTES)."""
        uni = meas.universe
        base = set(self.m.universes[uni].base_dimensions)
        other = rel.to if coord == rel.frm else rel.frm
        frontier = coord
        p = self.m.find_path(base, other)
        if p is None:
            raise Refusal("non_functional_transport",
                          f"'{meas.name}' cannot reach '{other}' to cross to '{T}'", measure=meas.name, target=T)
        frame = self._deliver_and_transport_monoid(meas, fam, op, (other,), {other: p}, where, trace)
        driver = self._serve_driver(face, frontier)           # [frontier, _drv]
        if other == rel.frm:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_frm_col, rel.via_to_col)
        else:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_to_col, rel.via_frm_col)
        b = bridge.join(driver.rename({frontier: "_to"}), on="_to", how="inner")             # _frm, _to, _drv
        # normalize the driver per measure-side key (partition of unity), then split the value.
        b = b.with_columns((pl.col("_drv") / pl.col("_drv").sum().over("_frm")).alias("_wt"))
        j = b.join(frame.rename({other: "_frm"}), on="_frm", how="inner")                     # _frm, _to, _wt, _value
        j = j.with_columns((pl.col("_value") * pl.col("_wt")).alias("_value"))
        split = j.group_by("_to").agg(pl.col("_value").sum()).rename({"_to": T})
        # reconciliation badge — the commutation certificate.
        base_total = float(frame["_value"].sum())
        crossed_total = float(split["_value"].sum()) if split.height else 0.0
        delta = crossed_total - base_total
        tol = max(1.0, abs(base_total)) * 1e-9
        status = "reconciles" if abs(delta) <= tol else "shortfall"
        # crossed-grain absence — events basis: complete the domain, fill 0.
        domain = bridge.select(pl.col("_to").alias(T)).unique()
        split = domain.join(split, on=T, how="left").with_columns(pl.col("_value").fill_null(0))
        split = split.sort(T).select([T, "_value"])
        self.stats.transports += 1
        self._t(trace, f"  alloc {other}->{T} via {rel.via_table} by norm({face.selection}) "
                       f"[split; reconcile {crossed_total:.2f} vs {base_total:.2f} -> {status}]")
        disc = self._alloc_disc(meas, fam, op, uni, rel, face, crossed_total, base_total, delta, tol, status)
        return split, disc

    def _alloc_disc(self, meas, fam, op, uni, rel, face, crossed_total, base_total, delta, tol, status):
        base = self._disc(meas, fam, op, uni)
        note = face.description or (f"{meas.name} splits across each {rel.frm}'s {rel.to} by "
                                    f"normalized {face.selection}")
        recon = (("crossed_total", crossed_total), ("base_total", base_total), ("delta", delta),
                 ("tolerance", tol), ("status", status))
        return base.with_caveat(Caveat(RECONCILIATION,
            f"allocated by normalized {face.selection}: crossed total {crossed_total:.2f} "
            f"{'reconciles to' if status == 'reconciles' else 'falls short of'} the grand total "
            f"{base_total:.2f} (delta {delta:.4f}). {note}",
            severity="info" if status == "reconciles" else "caution", reconciliation=recon))

    def _resolve_touch(self, meas, fam, op, target, faced, where, trace):
        """Execute a touch-face crossing: `<measure> AT {<coord>.touch}`. The measure is delivered at the
        reachable endpoint grain, then JOIN-MULTIPLIED through the relation's VIA bridge to the faced
        coordinate — a product's value reaches EVERY category it sits in, so the frame is deliberately
        multi-counted (totals exceed the grand total) and served in DISCLOSE. This reuses the shipped
        `_transport_reduce` (the M:N bridge just delivers many-per-key pairs instead of one), so the
        multiply falls out of the same combine the functional path uses."""
        uni = meas.universe
        base = set(self.m.universes[uni].base_dimensions)
        if len(faced) != 1 or len(target) != 1:
            raise Refusal("unsupported",
                          "touch v1 resolves a single faced coordinate anchor "
                          f"(got target {target!r}); mixed/multi-faced anchors are post-launch",
                          measure=meas.name, target=str(target))
        T = faced[0]
        coord, fname, rel, face = parse_faced(T, self.m.non_functional)
        # BASIS gate — v1 is EVENTS ONLY (Huayin): on events the expansion is honest arithmetic; on a
        # spine/product grid, replication would corrupt the grid's own completeness claim. Refuse until
        # that thinking is done. (An UNDECLARED basis keeps today's behavior — the crossing still serves.)
        basis = self.m.universes[uni].basis
        if basis is not None and basis != "events":
            raise Refusal("unsupported",
                          f"touch across {rel.frm}<->{rel.to} is events-only in v1: universe '{uni}' is "
                          f"'{basis}' basis, where replication corrupts completeness — declare an events "
                          f"population or use a functional designation",
                          measure=meas.name, target=T)
        if not op.is_monoid or op.witness not in (VALUE,):
            raise Refusal("unsupported",
                          f"touch crosses additive (monoid VALUE) measures only in v1 — '{meas.name}.{op.name}' "
                          f"is not (ordered/holistic/sketch crossings are post-launch)",
                          measure=meas.name, target=T)

        other = rel.to if coord == rel.frm else rel.frm      # the endpoint the measure reaches
        p = self.m.find_path(base, other)
        if p is None:
            raise Refusal("non_functional_transport",
                          f"'{meas.name}' cannot reach '{other}' to cross to '{T}'",
                          measure=meas.name, target=T)

        # exact cache — the faced token rides `target`, so touched/untouched key DISTINCTLY (no collision).
        key = (meas.name, fam.agg, target, uni, where)
        ver = self.con.table_version(meas.home_table)
        disc = self._touch_disc(meas, fam, op, uni, rel, face)
        if key in self.cache and self.cache[key].version == ver:
            self.stats.cache_hits += 1
            self._t(trace, "  cache-hit (touch)")
            return self.cache[key].frame, disc.with_caveat(Caveat(FRESHNESS, "served from cache"))

        # 1) deliver the measure at the reachable endpoint grain (reuse the monoid delivery).
        frame = self._deliver_and_transport_monoid(meas, fam, op, (other,), {other: p}, where, trace)
        # 2) deliver the bridge so `_frm` is ALWAYS the measure side (swap columns for the reverse edge),
        #    then join-multiply + reduce onto the faced grain T (no dedup — the multiply is the point).
        if other == rel.frm:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_frm_col, rel.via_to_col)
        else:
            bridge = self.con.deliver_edge(rel.via_table, rel.via_to_col, rel.via_frm_col)
        # COVERAGE (the second disclosure of the ratified absence law): a measure-side key in NO bridge
        # membership is excluded from EVERY faced cell — so the touch total can fall SHORT of the grand
        # total, the mirror of the over-count. Report the number either way (Huayin): full coverage is
        # itself the honest statement; a shortfall names the excluded count and the value lost.
        covered = bridge.select(pl.col("_frm").alias(other)).unique()
        n_total = frame.height
        uncovered = frame.join(covered, on=other, how="anti")
        n_uncov = uncovered.height
        if n_uncov:
            lost = uncovered["_value"].sum()
            disc = disc.with_caveat(Caveat(TRANSPORT,
                f"{n_uncov} of {n_total} {other} are in no {T.split('.')[0]} — excluded from every cell; "
                f"the touch total falls short of the grand total by {lost} ({meas.name}). coverage "
                f"{n_total - n_uncov}/{n_total}", severity="info"))
        else:
            disc = disc.with_caveat(Caveat(TRANSPORT,
                f"coverage {n_total}/{n_total}: every {other} carrying {meas.name} is categorized "
                f"(no shortfall; the over-count is the only skew)", severity="info"))
        touched = self._transport_reduce(frame, other, T, bridge, op)
        self.stats.transports += 1
        self._t(trace, f"  touch {other} x {T} via {rel.via_table} [join-multiply, combine={op.combine}] "
                       f"(deliberate over-count; coverage {n_total - n_uncov}/{n_total})")
        # 3) crossed-grain absence — EVENTS basis: a bridge coordinate with no touched value is a lawful
        #    ZERO (Huayin ruling: lawful-zero on events universes only). Complete the domain from the
        #    bridge so every declared category appears; fill 0. Undeclared basis => leave as-is (no domain).
        if basis == "events":
            domain = bridge.select(pl.col("_to").alias(T)).unique()
            before = touched.height
            touched = domain.join(touched, on=T, how="left").with_columns(pl.col("_value").fill_null(0))
            n_zero = touched.height - before
            if n_zero > 0:
                disc = disc.with_caveat(Caveat(TRANSPORT,
                    f"{n_zero} {T} with no touched {meas.name} rendered as 0 per events basis"))
        touched = touched.sort(T).select([T, "_value"])
        self.cache[key] = CacheEntry(touched, None, ver)
        return touched, disc

    def _touch_disc(self, meas, fam, op, uni, rel, face):
        """The touch disclosure — the deliberate over-count as a MATERIAL caveat (drives DISCLOSE), carrying
        the face's declared folklore verbatim so the answer says WHY it multi-counts."""
        base = self._disc(meas, fam, op, uni)
        note = face.description or (f"{meas.name} reaches every {rel.to} a {rel.frm} sits in "
                                    f"({rel.detail})")
        return base.with_caveat(Caveat(OVER_COUNT,
            f"multi-counted by construction across {rel.frm}<->{rel.to}: {note}", severity="caution"))

    def _combine_exprs(self, op):
        if op.combine == "sum": return [pl.col("_value").sum().alias("_value")]
        if op.combine == "min": return [pl.col("_value").min().alias("_value")]
        if op.combine == "max": return [pl.col("_value").max().alias("_value")]
        if op.combine == "argmax":
            return [pl.col("_value").sort_by("_order").last().alias("_value"),
                    pl.col("_order").max().alias("_order")]
        if op.combine == "argmin":
            return [pl.col("_value").sort_by("_order").first().alias("_value"),
                    pl.col("_order").min().alias("_order")]
        raise Refusal("unknown", f"no combine for operator '{op.name}'")

    # ---- resolution-anchor metric reduction (WP-B B-4) ----
    # A DERIVED ... AT <res> metric means "<member> of the <res>-resolved series". When asked at a
    # coarser level the engine evaluates the formula at <res> (the planner does that) and reduces the
    # resulting series here — the SOLE place the manifold's edge provenance (provider/keys) lives.
    # The whole finer series is remapped to the target key first and aggregated ONCE, so `mean` is a
    # true mean of the finer values, never a mean-of-means. This reduction is the metric's DECLARED
    # meaning (ruling 5), applied regardless of license: "infertility bars silent reduction, never
    # reduction that is the declared meaning."
    _SERIES_REDUCE = {
        "sum":   lambda c: c.sum(),
        "mean":  lambda c: c.mean(),
        "min":   lambda c: c.min(),
        "max":   lambda c: c.max(),
        "count": lambda c: c.count(),
    }

    def reduce_series(self, frame, from_level: str, target: str, member: str, trace=None):
        """Reduce a per-`from_level` value series (column `_v`) to a single coarser `target` level by
        `member`, composing the functional edge maps along the path. Raises Refusal if `target` is not
        reachable from `from_level` (the metric is defined AT its resolution anchor; a finer or
        unrelated ask is out of universe) or `member` is not a reducible operator."""
        if member not in self._SERIES_REDUCE:
            raise Refusal("unsupported",
                          f"resolution-anchor metric cannot reduce its series by '{member}'")
        if target == from_level:
            return frame
        path = self.m.find_path({from_level}, target)
        if path is None or path[0] != from_level:
            raise Refusal("out_of_universe",
                          f"'{target}' is not reachable from resolution anchor '{from_level}' — this "
                          f"metric is defined AT '{from_level}' and cannot be served there")
        work = frame.rename({from_level: "_key"})
        for e in path[1]:
            mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)   # [_frm, _to]
            work = (work.with_columns(pl.col("_key").cast(pl.Utf8))
                        .join(mp.with_columns(pl.col("_frm").cast(pl.Utf8)),
                              left_on="_key", right_on="_frm", how="inner")
                        .drop("_key").rename({"_to": "_key"}))
            self._t(trace, f"  reduce series {e.frm}->{e.to} along {e.lineage} (single-pass {member})")
        agg = self._SERIES_REDUCE[member](pl.col("_v")).alias("_v")
        return work.group_by("_key").agg(agg).rename({"_key": target})

    def reduce_series_to_anchor(self, frame, input_grain: tuple, target: tuple, member: str, trace=None):
        """Reduce an in-memory value series (column `_v`) keyed by `input_grain` (a tuple of levels) to
        the multi-level `target` anchor by `member`. Reduction targets reachable from an input level are
        transported (relabel + collapse); orthogonal targets already present are kept; functionally-
        DEPENDENT targets are attached 1:1; the remaining input axes (e.g. the pinned input anchor) are
        collapsed by the reducer. Native Polars; the planner adjudicated the shape upstream (directive 7).
        Generalizes the single-level reduce_series to the dependent-pair era."""
        if member not in self._SERIES_REDUCE:
            raise Refusal("unsupported", f"cannot reduce a series by '{member}'")
        reduction, dependent = self._split_dependent_targets(target)
        work, present = frame, set(input_grain)
        for rt in reduction:                                    # transport each reduction target into place
            if rt in present:
                continue
            src = next((g for g in input_grain if g == rt or self.m.find_path({g}, rt) is not None), None)
            if src is None:
                raise Refusal("out_of_universe",
                              f"'{rt}' is not reachable from the input grain {list(input_grain)}")
            cur = src
            for e in self.m.find_path({src}, rt)[1]:
                mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
                work = work.join(mp, left_on=cur, right_on="_frm", how="inner").drop(cur).rename({"_to": e.to})
                cur = e.to
            present.discard(src); present.add(rt)
        red = self._SERIES_REDUCE[member](pl.col("_v")).alias("_v")
        work = (work.group_by(list(reduction)).agg(red) if reduction
                else work.select(red))                          # empty reduction = grand total
        self._t(trace, f"  reduce series -> {list(reduction)} by {member} (collapse input axes)")
        for T in dependent:                                     # attach functionally-determined levels
            S = next(s for s in reduction if self.m.find_path({s}, T) is not None)
            cur = S
            for e in self.m.find_path({S}, T)[1]:
                mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
                work = self._transport_attach(work, cur, e.to, mp); cur = e.to
        return work.select(list(target) + ["_v"])

    def _transport_reduce(self, frame, from_col, to_col, mapping, op):
        j = frame.join(mapping, left_on=from_col, right_on="_frm", how="inner")
        j = j.drop(from_col).rename({"_to": to_col})
        keys = [c for c in j.columns if c not in ("_value", "_order")]
        return j.group_by(keys).agg(self._combine_exprs(op))

    def _split_dependent_targets(self, target: tuple) -> tuple:
        """Partition a target anchor into independent REDUCTION targets and functionally-DETERMINED
        attribute targets. T is DEPENDENT iff another target level S functionally reaches T (S->..->T):
        T is coarser and fixed by S, so it is attached 1:1, never reduced (reducing it would collapse
        its determiner S). DG-2's family — the coordinate machinery completing dependent pairs. The
        engine stays envelope-blind; this is per-atom transport geometry, decided from the edges."""
        dependent = [T for T in target
                     if any(S != T and self.m.find_path([S], T) is not None for S in target)]
        reduction = tuple(T for T in target if T not in dependent)
        return reduction, tuple(dependent)

    def _transport_attach(self, frame, from_col, to_col, mapping):
        """Attach a functionally-DETERMINED attribute level: 1:1 broadcast `to_col` onto each row along
        the edge, KEEPING `from_col` (no collapse). Every from-key maps to exactly one to-key
        (functional edge), so there is no row inflation — Huayin's join-and-group along the edge, native
        Polars. Polars EXECUTES what the planner adjudicated (directive 7): the edge's functionality was
        settled upstream (its verdict); the left-join here just realizes it, never decides it."""
        return (frame.join(mapping, left_on=from_col, right_on="_frm", how="left")
                     .rename({"_to": to_col}))

    # ---- holistic recompute-from-base (non-monoid: median, mode) ----------
    def _recompute_holistic(self, meas, fam, op, target, paths, where, trace):
        """A non-monoid op cannot reduce. Recompute from base at the target grain:
        deliver raw base rows (one table), broadcast the target coordinate keys onto them
        by transport, then aggregate in-engine. No cached/finer result is a candidate."""
        start = {T: paths[T][0] for T in target}
        base_levels = list(dict.fromkeys(start.values()))
        base_phys = [self.m.levels[b].realized_by for b in base_levels]

        rows = self.con.deliver_base_values(
            meas.home_table, base_phys,
            self.con.realize(meas.home_table, meas.pre_expr, meas.logical_type), where)
        self.stats.deliveries += 1
        rows = rows.rename({self.m.levels[b].realized_by: b for b in base_levels})
        self._t(trace, f"  deliver {meas.name} RAW base rows @ {base_levels} "
                       f"({rows.height} rows, no pre-aggregation)")

        # confinement on raw rows (broadcast attrs, filter)
        pred = self.m.universes[meas.universe].predicate
        if pred is not None:
            rows = self._confine(rows, meas, pred, trace)

        # broadcast each target coordinate onto the raw rows (relabel keys, keep all rows). DEPENDENT
        # target levels (fixed by another target level) are ATTACHED (keep the determiner), independent
        # ones relabel base->target as before — else a dependent pair collapses its determiner.
        reduction, dependent = self._split_dependent_targets(target)
        for T in target:
            cur, path = start[T], paths[T][1]
            for e in path:
                mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
                if T in dependent:
                    rows = self._transport_attach(rows, cur, e.to, mp)
                    self._t(trace, f"  attach {cur}->{e.to} onto raw rows (functional 1:1, no collapse)")
                else:
                    rows = rows.join(mp, left_on=cur, right_on="_frm", how="inner").drop(cur).rename({"_to": e.to})
                    self._t(trace, f"  broadcast {cur}->{e.to} onto raw rows (transport, no reduce)")
                cur = e.to

        # aggregate holistically in-engine at the target grain (recompute, not reduce)
        keys = list(target)
        if op.name == "median":
            out = rows.group_by(keys).agg(pl.col("_value").median().alias("_value"))
        elif op.name == "mode":
            out = rows.group_by(keys).agg(pl.col("_value").mode().first().alias("_value"))
        else:
            raise Refusal("unsupported", f"holistic operator '{op.name}' not implemented")
        self._t(trace, f"  {op.name} recomputed in-engine @ {keys} (NOT reduced from a finer result)")
        return out.select(keys + ["_value"])

    # ---- universe confinement (runtime, at base grain) --------------------
    def _predicate_levels(self, pred):
        """Base-level coordinates the predicate references (must be in the delivery grain). A bare ref
        names a level directly; a LOGICAL attribute `<level>.<attr>` (OF-9) needs its level in the grain
        too, so the broadcast can join the attribute onto it."""
        out = []
        for c in pred.comparisons:
            for r in (c.left, c.right):
                if r.is_literal:
                    continue
                if r.table is None and r.column in self.m.levels:
                    out.append(r.column)
                elif r.table in self.m.levels:               # logical attribute -> its level anchors the broadcast
                    out.append(r.table)
        return out

    def _confine(self, frame, meas, pred, trace):
        """Apply the universe predicate at the base grain: broadcast attribute refs onto
        the frame (transport, never a backend join), coerce the compared sides to a common
        dtype, evaluate the comparison, filter."""
        helper_cols = []
        cond = None
        for comp in pred.comparisons:
            le, frame, h1, lcol = self._ref_expr(comp.left, frame, trace)
            re_, frame, h2, rcol = self._ref_expr(comp.right, frame, trace)
            helper_cols += h1 + h2
            le, re_ = self._coerce(le, lcol, re_, rcol, frame)
            c = {">=": le >= re_, ">": le > re_, "<=": le <= re_, "<": le < re_,
                 "=": le == re_, "!=": le != re_}[comp.op]
            cond = c if cond is None else (cond & c)
        frame = frame.filter(cond)
        if helper_cols:
            frame = frame.drop([c for c in set(helper_cols) if c in frame.columns])
        return frame

    def _coerce(self, le, lcol, re_, rcol, frame):
        """Coerce the two sides of a predicate comparison to a comparable dtype. Predicate
        literals arrive as strings (model.Ref.value: str), so a literal adapts to the column
        it is compared against, and between two columns a Utf8 side adapts to the typed side.
        This makes `day >= '2024-06-01'` work on a Date day and `qty >= 10` on an Int64 qty —
        not only on the string-typed coordinates the benchmark happens to use."""
        ldt = frame.schema.get(lcol) if lcol else None
        rdt = frame.schema.get(rcol) if rcol else None
        if lcol is None and rdt is not None:                    # left literal -> right column's dtype
            return le.cast(rdt), re_
        if rcol is None and ldt is not None:                    # right literal -> left column's dtype
            return le, re_.cast(ldt)
        if ldt is not None and rdt is not None and ldt != rdt:  # two columns, differing dtypes
            if ldt == pl.Utf8 and rdt != pl.Utf8: return le.cast(rdt), re_
            if rdt == pl.Utf8 and ldt != pl.Utf8: return le, re_.cast(ldt)
            return le, re_.cast(ldt)
        return le, re_

    def _ref_expr(self, ref, frame, trace):
        """Resolve a predicate Ref to a Polars expr over `frame`, broadcasting attributes.
        Returns (expr, frame, [helper_cols_added], colname_or_None) — colname is the frame
        column the expr reads (None for a literal), which lets _coerce align dtypes."""
        if ref.is_literal:
            return pl.lit(ref.value), frame, [], None
        # OF-9 (case-demo c): a LOGICAL attribute `<level>.<attr>` resolves to its physical binding
        # (`store.opened` -> `stores.opened_date`) and then rides the existing physical broadcast path.
        if ref.table is not None and ref.table in self.m.levels:
            binding = dict(self.m.levels[ref.table].attributes).get(ref.column)
            if binding and "." in binding:
                from .model import Ref
                pt, pc = binding.split(".", 1)
                ref = Ref(False, table=pt, column=pc)
        if ref.table is None:                      # a coordinate/level already in the frame
            return pl.col(ref.column), frame, [], ref.column
        # an attribute T.col -> deliver at its key anchor and BROADCAST onto the frame
        anchor, key_col = self._attr_anchor(ref.table, available=set(frame.columns))
        attr = self.con.deliver_attribute(ref.table, key_col, ref.column)
        helper = f"{ref.table}.{ref.column}"
        attr = attr.rename({"_attr": helper})
        frame = frame.join(attr.select(["_key", helper]), left_on=anchor, right_on="_key", how="left")
        self._t(trace, f"    broadcast attribute {helper} from anchor '{anchor}' (transport, no join pushdown)")
        return pl.col(helper), frame, [helper], helper

    def _attr_anchor(self, table, available=None):
        """Resolve the (level, key_col) at which `table` is keyed, to deliver+broadcast one of
        its attributes. A table usually provides edges at ONE frm level (its grain) — then the
        answer is unambiguous. But a denormalized table can provide edges at several levels
        (store->region AND region->country from one geo table); the attribute's key level is
        then ambiguous, and we must NOT silently pick the first edge. We pin it to the level
        present in the delivery frame (`available`) if exactly one candidate qualifies — that
        is also the level the broadcast must join on — and otherwise REFUSE, naming the
        candidates: an honest 'declare it' over a silent wrong grain."""
        cands = {(e.frm, e.frm_col) for e in self.m.edges if e.provider_table == table}
        if not cands:
            raise Refusal("unknown", f"cannot resolve key anchor for attribute table '{table}' "
                                     f"(no functional edge provides it)")
        if len({f for f, _ in cands}) == 1:               # one grain — unambiguous
            return next(iter(cands))
        if available is not None:                          # several grains — pin by the delivery frame
            pinned = {(f, c) for (f, c) in cands if f in available}
            if len(pinned) == 1:
                return next(iter(pinned))
        frms = sorted({f for f, _ in cands})
        # Analytical no-result: the grain is genuinely ambiguous under the rules. The engine
        # reports the FACT (discriminator=ambiguous) and the candidate frames; it does NOT decide
        # the outcome — the planner classifies ambiguous -> clarify (ADR-032 D3/D4).
        raise Refusal("ambiguous_grain",
            f"attribute table '{table}' is keyed at multiple levels {frms} — cannot infer which "
            f"level its attribute is a property of"
            + ("; the delivery grain pins none uniquely" if available is not None else "")
            + " — declare the attribute's level explicitly",
            discriminator=AMBIGUOUS,
            alternatives=tuple(f"key at '{f}'" for f in frms))

    def _pred_str(self, pred):
        def rs(r):
            return r.value if r.is_literal else (f"{r.table}.{r.column}" if r.table else r.column)
        return " AND ".join(f"{rs(c.left)} {c.op} {rs(c.right)}" for c in pred.comparisons)

    # ---- sketch (distinct) via the three operators, over the witness store ----
    # `distinct` is composed here from hll_count -> hll_merge -> hll_estimate. Each step's
    # vocabulary (kind, witness, signature) is the registry entry; the mechanics are sketch.py.
    # hll_count LOADS from the witness store when published (no base scan); else builds lazily.
    def _resolve_sketch(self, meas, member, target, paths, where, trace):
        if len(target) != 1:
            raise Refusal("unsupported", "sketch transport supports a single target level in this build")
        T = target[0]
        start, path = paths[T][0], paths[T][1]
        p = meas.sketch_precision
        ver = self.con.table_version(meas.home_table)

        # hll_count: base-grain sketches. STORED witness (eager, at publish) is load-bearing here —
        # if present and fresh we read it with NO backend fetch; otherwise we build lazily (fallback).
        if self.witnesses.fresh(meas.name, member, start, ver) and where is None:
            sk = dict(self.witnesses.get(meas.name, member, start).sketches)
            self._t(trace, f"  hll_count: LOADED {len(sk)} witness sketches @ base '{start}' "
                           f"[HLLSketch({p})] (materialized at publish — no base scan)")
        else:
            sk = self._build_base_sketches(meas, start, p, where)
            why = "filtered query" if where is not None else "no witness"
            self._t(trace, f"  hll_count: built {len(sk)} HLL sketches @ base '{start}' "
                           f"[HLLSketch({p})] ({why}; lazy base scan)")

        # hll_merge: union the carrier up each edge of the path (the monoid that makes distinct fertile)
        for e in path:
            mp = self.con.deliver_edge(e.provider_table, e.frm_col, e.to_col)
            m2 = {r["_frm"]: r["_to"] for r in mp.iter_rows(named=True)}
            buckets: dict = {}
            for fk, s in sk.items():
                tk = m2.get(fk)
                if tk is not None:
                    buckets.setdefault(tk, []).append(s)
            sk = {k: hll_merge(v, p) for k, v in buckets.items()}
            self.stats.transports += 1
            self._t(trace, f"  hll_merge: union {e.frm}->{e.to} along {e.lineage} "
                           f"[monoid over HLLSketch({p}); no scan, no join pushdown]")

        # hll_estimate: project the carrier to the number
        frame = pl.DataFrame([{T: k, "_value": hll_estimate(s)} for k, s in sk.items()])
        self._t(trace, f"  hll_estimate: HLLSketch({p}) -> Int64 distinct estimate @ '{T}'")
        return frame, sk

    def _build_base_sketches(self, meas, base_level, precision, where) -> dict:
        """One base scan -> one HLLSketch per base-level bucket. This is the only sketch step that
        touches base rows; the backend scans, Columna builds the sketches in-engine."""
        base_phys = self.m.levels[base_level].realized_by
        rows = self.con.deliver_base_rows(meas.home_table, [base_phys], meas.distinct_col, where)
        self.stats.deliveries += 1
        rows = rows.rename({base_phys: base_level})
        out = {}
        for r in rows.group_by(base_level).agg(pl.col("_dv")).iter_rows(named=True):
            out[r[base_level]] = hll_count(r["_dv"], precision)
        return out

    def publish_witnesses(self, trace=None) -> int:
        """Build and STORE base-grain sketches for every sketch-witness measure, once, at publish.
        One base scan per (measure, base dimension). Eager and deliberate — a materialization
        decision, not a cache fill. Thereafter every coarser distinct-count is a witness merge."""
        built = 0
        for meas in self.m.measures.values():
            if not meas.family:
                continue
            member = next(iter(meas.family))            # Core: single-family sketch measures
            op = get_operator(meas.family[member].agg)
            if op.witness != OP_SKETCH:
                continue
            p = meas.sketch_precision
            ver = self.con.table_version(meas.home_table)
            base_dims = sorted(self.m.universes[meas.universe].base_dimensions)
            for base in base_dims:
                if base not in self.m.levels:
                    continue
                sketches = self._build_base_sketches(meas, base, p, where=None)
                self.witnesses.put(Witness(meas.name, member, base, p, ver, sketches))
                built += 1
                self._t(trace, f"  publish witness: {meas.name}.{member} @ base '{base}' "
                               f"[HLLSketch({p})] — {len(sketches)} sketches stored (1 base scan)")
        return built

    # ---- disclosure -------------------------------------------------------
    # ---- universe-support consistency (publish-time validation) -----------
    def validate_universe_support(self, coverage_tol: float = 0.02) -> list:
        """A universe is ONE population. Every measure bound to it must, when collapsed to
        the universe's base grain, cover the SAME support (the same set of base points) —
        modulo declared coverage. If measures that claim to share a universe reconcile to
        different supports, they belong to different universes (or one is mis-declared).

        NOTE — this is the COUNT-reducer instance of a more general path-independence check:
        the principled form reduces a measure to the universe singleton along EVERY available
        anchoring and asserts the reduced VALUES agree (revenue.sum via calendar == via
        fiscal == ... , because they reduce over one population). That form needs >=2
        anchorings of an axis to be non-vacuous; with a single anchoring it has nothing to
        reconcile against. The support-count version below is non-vacuous on real data
        because its "paths" are different measures' home tables reaching the same population
        — it is path-independence with the reducer fixed to `count`. Generalize to value
        path-independence once a second coordinatization of an axis exists.

        Implemented as the user proposed: reduce each measure to the universe and compare
        the supports. Support is delivered single-table (count of confined base points);
        a mismatch beyond `coverage_tol`, not explained by a declared coverage caveat,
        is flagged. Returns a list of human-readable findings (empty == consistent)."""
        findings = []
        for U in self.m.universes.values():
            ms = [m for m in self.m.measures.values() if m.universe == U.name]
            if len(ms) < 2:
                continue
            base_levels = sorted(U.base_dimensions)
            base_phys = [self.m.levels[d].realized_by for d in base_levels]
            supports, sources = {}, {}
            for m in ms:
                try:
                    f = self.con.deliver_measure(m.home_table, base_phys, [("_n", "count(*)")])
                    f = f.rename({self.m.levels[d].realized_by: d for d in base_levels})
                    if U.predicate is not None:
                        f = self._confine(f, m, U.predicate, None)
                    supports[m.name] = f.height
                    sources[m.name] = m.home_table
                except Exception as e:
                    findings.append(f"universe '{U.name}': measure '{m.name}' cannot be reduced to "
                                    f"base grain {base_levels} (from '{m.home_table}'): {e}")
            if not supports:
                continue
            ref = max(supports.values())
            for name, s in supports.items():
                if ref > 0 and s < ref * (1 - coverage_tol):
                    has_cov = self.m.measures[name].missingness in ("MAR", "MNAR") \
                              or self.m.measures[name].is_unconfirmed
                    note = "" if has_cov else " (no coverage declared — likely a mis-declared universe)"
                    findings.append(
                        f"universe '{U.name}': '{name}' (from {sources[name]}) covers {s} base points "
                        f"vs {ref} for its siblings — {100*(1-s/ref):.0f}% short{note}")
        return findings

    def _disc(self, meas, fam, op, uni, crossings=()):
        cav = list(crossings)
        if meas.is_unconfirmed:
            cav.append(Caveat(UNCONFIRMED, f"measure '{meas.name}' rests on {meas.evidence}"))
        if meas.missingness == "MNAR":
            cav.append(Caveat(UNCONFIRMED,
                f"'{meas.name}' is MNAR (missingness depends on its own value) — averages are selection-biased"))
        if op.witness == OP_SKETCH:
            cav.append(Caveat(APPROXIMATION,
                f"{meas.name}.{op.name}: HLL distinct estimate [HLLSketch({meas.sketch_precision})]",
                rel_error=rse(meas.sketch_precision)))
        return Disclosure(tuple(cav), population=uni)

    def dry_disclose(self, measure: str, member: str, target: tuple) -> Disclosure:
        """The spec-only would-be provenance disclosure for an atom (unconfirmed / MNAR /
        approximation, population-pinned) — computed from the declaration, touching NO data.
        Used by the planner's plan() for EXPLAIN-without-execution. Crossings are added by the
        planner (they are shape); this supplies only the provenance half."""
        meas = self.m.measures[measure]
        fam = meas.family[member]
        op = get_operator(fam.agg)
        return self._disc(meas, fam, op, meas.universe)

    def _t(self, trace, msg):
        if trace is not None:
            trace.append(msg)
