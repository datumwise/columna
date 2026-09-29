"""
columna_platform.frameql — **real Frame-QL text, served through the v8-native Platform MME.**

    Frame-QL syntax  →  Platform request interpretation  →  family or expression target
                     →  MME adjudication  →  Answer / classified refusal

    syntax    the ONE place Frame-QL syntax enters Platform. Imports `columna_core.envelope` — a
              PROVABLY syntax-only module — and converts to a `PlatformRequest` before returning, so the
              AST never reaches the kernel.
    request   the Platform-native canonical request form: governed tokens and a constituent set.
    serving   resolution BY SORT, MME adjudication, and a total classified `Outcome`.
    exhibit   the runnable demonstration, over real query strings.

**THE BOUNDARY.** `columna_platform.kernel` imports `columna_core` NOWHERE, and three tests hold that.
This package adds exactly ONE Core import, in `syntax.py`, and it is a grammar: `columna_core.envelope`
imports only `re`, `dataclasses` and `typing`, and importing it pulls in two modules — the package's lazy
`__init__` and the parser. No Core analytical semantics, planner law, family/member model,
generated-family doctrine or Operator Registry is reachable from it, and the import CLOSURE is measured by
a test rather than asserted here.
"""
from __future__ import annotations

from .request import PlatformRequest, RequestInterpretationRefusal, RequestedSeries
from .serving import (
    CLASSIFICATIONS,
    Column,
    DISCLOSE,
    Frame,
    FrameQLService,
    Outcome,
    REFUSE,
    SERVE,
    SYNTAX,
    UNRESOLVED,
    UNSUPPORTED,
)
from .syntax import EnvelopeSyntaxError, interpret, parse

__all__ = ["CLASSIFICATIONS", "Column", "DISCLOSE", "EnvelopeSyntaxError", "Frame", "FrameQLService",
           "Outcome", "PlatformRequest", "REFUSE", "RequestInterpretationRefusal", "RequestedSeries",
           "SERVE", "SYNTAX", "UNRESOLVED", "UNSUPPORTED", "interpret", "parse"]
