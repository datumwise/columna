"""columna_core.frameql — the Frame-QL surface."""
from __future__ import annotations
from typing import Optional
from .model import Manifold
from .projection import PlannerView
from .engine import ColumnEngine
from .planner import Planner, FrameResult


class ManifoldServer:
    def __init__(self, manifold: Manifold, connector):
        self.m = manifold
        self.engine = ColumnEngine(manifold, connector)
        self.planner = Planner(PlannerView(manifold), self.engine)

    def frame(self, *anchor, where: Optional[str] = None) -> "Frame":
        return Frame(self, tuple(anchor), where)

    def publish(self, trace=None) -> int:
        """Materialize the witness store: build and store base-grain sketches for every
        sketch-witness measure, once. Returns the number of witnesses built."""
        return self.engine.publish_witnesses(trace)

    @property
    def witnesses(self): return self.engine.witnesses

    @property
    def stats(self): return self.engine.stats
    @property
    def fetches(self): return self.engine.con.fetch_count


class Frame:
    def __init__(self, server, anchor, where=None):
        self.server = server
        self.anchor = anchor
        self.where = where
        self.cols = []
        self.universe = None

    def column(self, name, expr=None):
        self.cols.append((name, expr if expr is not None else name)); return self

    def on_universe(self, u):           # records the population pin (verified at resolve)
        self.universe = u; return self

    def run(self) -> FrameResult:
        return self.server.planner.run(self.anchor, self.cols, self.where, population=self.universe)

    def plan(self) -> FrameResult:
        """The would-be annotation without executing (zero backend fetches)."""
        return self.server.planner.plan(self.anchor, self.cols, self.where, population=self.universe)

    def explain(self, execute: bool = True) -> str:
        return (self.run() if execute else self.plan()).explain()
