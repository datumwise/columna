"""columna_core.serving_contract — the SERVING RESULT TYPES, owned by nobody's execution strategy.

WHY THIS MODULE EXISTS. `wire_frame` takes a `FrameResult`, and until 2026-09-12 `FrameResult` and
`ColumnResult` were defined in `planner.py`. Importing the WIRE'S DATA TYPES therefore executed
`projection`, `engine`, `model`, `frameql` and `expr` — the whole legacy execution stack. Proof A
found this the honest way: an execution path that excludes the legacy planner could not reach the
disclosure surface at all, because the surface's vocabulary was trapped behind the planner's imports.

That is a RESPONSIBILITY defect, not a packaging inconvenience. These are plain dataclasses carrying
no planner logic. They describe WHAT A SERVING ANSWER IS — columns, disclosures, anchor, the
four-outcome rollup — which is a contract every execution strategy must satisfy and none of them owns.

WHAT THIS MOVE IS NOT. No field changed, no behaviour changed, no name changed, and NOTHING WAS
COPIED: `planner.py` re-exports these names, so every existing import keeps working and there is
exactly one definition of each. A second enumeration of the wire's types would be strictly worse than
the seam it replaced — two definitions free to drift, with CI checking only one.

The public wire is deliberately untouched. This is an ownership correction, not a redesign.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

import polars as pl

from .disclosure import (CLARIFY, DISCLOSE, ERROR, REFUSE, SERVE, Disclosure, Outcome)


def _fmt_anchor(anchor) -> str:
    """Spell an anchor with the canonical product separator `*` (never a comma). Every surface that
    WRITES an anchor — the EXPLAIN header, error/clarify messages, traces — routes through here so no
    output ever emits a comma anchor (capture §2b RULED (a))."""
    if isinstance(anchor, (tuple, list)):
        return "*".join(str(a) for a in anchor)
    return str(anchor)


@dataclass
class ColumnResult:
    name: str
    expr: str
    frame: Optional[pl.DataFrame]
    disclosure: Disclosure
    refusal: Optional[Outcome] = None
    trace: list = field(default_factory=list)
    universe: Optional[str] = None      # the column's sole universe (§2c)
    fill_rule: Optional[str] = None     # Φ_v resolved from the member contract (columna#143) — drives
                                        # absence semantics. None = undeclared (disclose, never fill).


@dataclass
class FrameResult:
    data: Optional[pl.DataFrame]
    disclosure: Disclosure
    columns: list                 # [ColumnResult]
    anchor: tuple

    # ---- the four-outcome contract, surfaced (ADR-032) --------------------
    # Served columns carry a frame (+ disclosure); a no-result column carries a classified
    # refusal. These expose the planner's verdicts so any surface reads them uniformly.
    @property
    def served(self): return [c for c in self.columns if c.refusal is None]

    @property
    def clarifies(self): return [c for c in self.columns if c.refusal and c.refusal.is_clarify]

    @property
    def refusals(self): return [c for c in self.columns if c.refusal and c.refusal.is_refuse]

    @property
    def errors(self): return [c for c in self.columns if c.refusal and c.refusal.is_error]

    @property
    def outcome(self):
        """Frame-level rollup of the strongest signal: refuse > clarify > error > disclose > serve.
        (A mixed frame still reports its served columns in `data`; this names what needs attention.)"""
        if self.refusals: return REFUSE
        if self.clarifies: return CLARIFY
        if self.errors: return ERROR
        if any(c.disclosure.severity == "critical" for c in self.served): return DISCLOSE
        return SERVE

    def explain(self) -> str:
        lines = [f"EXPLAIN  frame @ {_fmt_anchor(self.anchor)}"]
        for c in self.columns:
            head = f"  • {c.name}" + (f" = {c.expr}" if c.expr != c.name else "")
            lines.append(head)
            for t in c.trace:
                lines.append(f"      ├─ {t}")
            if c.refusal:
                lines.append(f"      └─ {c.refusal}")
            else:
                lines.append(f"      └─ {c.disclosure.render_human()}")
        return "\n".join(lines)
