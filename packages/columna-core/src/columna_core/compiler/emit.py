"""
columna_core.compiler.emit — governed declarations -> a CLOSED Core execution image (`.cml` text).

The image is CLOSED by construction: nothing this module emits carries, implies, or anticipates a
certification. A face licence, a functional-edge verdict and a `PublishedScope` admission are all
downstream of adjudication, and K0 emits no construct that could depend on one.

DETERMINISM IS A CORRECTNESS PROPERTY HERE, not tidiness. The lowering receipt binds the image by a
byte digest over the file AS SHIPPED, with no canonicalization, so identical inputs must produce
identical bytes. Therefore: no timestamp, no `Math.random`-shaped anything, no dict-iteration order
dependence, and a fixed integer `MANIFOLD ... VERSION`. Statements are emitted in a fixed kind order
and sorted by name inside each block, so the output does not depend on authored ordering either.

K0 EMITS EXACTLY: SOURCE_MANIFOLD, UNIVERSE (unrestricted), LEVEL (base), MEASURE (+ FAMILY).
Everything else refuses in `compile.py` with a named category before this module is reached.
"""
from __future__ import annotations

import re

from .refusals import ExecutionRepresentationGap, UnsupportedCoreCapability

#: `MANIFOLD <name>` accepts `\w+` only. The governed manifold_id is carried faithfully by
#: SOURCE_MANIFOLD (whose grammar is wider); this is the Core-local artifact label.
_CML_NAME = re.compile(r"^\w+$")

#: `LEVEL <name>` accepts `[\w.]+`; the realized column must be a bare `\w+`.
_LEVEL_NAME = re.compile(r"^[\w.]+$")
_COLUMN = re.compile(r"^\w+$")

#: `SOURCE_MANIFOLD <id> VERSION <semver>` — the id charset and the semver shape the parser requires.
_SOURCE_ID = re.compile(r"^[\w.:@/-]+$")
_SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

#: The four population bases Core recognises. A declared basis outside this set cannot be carried.
_BASIS_TYPES = frozenset({"events", "spine", "product", "registry"})

#: The integer engine revision K0 stamps. Fixed, because it must be reproducible: a per-run value
#: would change the image digest and break the receipt binding for identical inputs.
K0_ENGINE_VERSION = 1


def _require(pattern: re.Pattern, value: str, what: str, subject: str) -> str:
    if not pattern.match(value or ""):
        raise ExecutionRepresentationGap(
            f"{what} {value!r} cannot be represented in the Core execution grammar "
            f"(expected {pattern.pattern})", subject=subject)
    return value


def source_manifold_line(manifold_id: str, version: str) -> str:
    """The realization CLAIM, emitted to equal `artifact.ref` exactly.

    The compiler EMITS this; it never compares an existing image's claim to decide what to build.
    The server does the comparing, and a receipt is what turns the claim into evidence."""
    _require(_SOURCE_ID, manifold_id, "SOURCE_MANIFOLD id", "identity")
    _require(_SEMVER, version, "SOURCE_MANIFOLD version", "identity")
    return f"SOURCE_MANIFOLD {manifold_id} VERSION {version}"


def manifold_header(manifold_id: str) -> str:
    _require(_CML_NAME, manifold_id, "MANIFOLD name", "identity")
    return f"MANIFOLD {manifold_id} VERSION {K0_ENGINE_VERSION}"


def universe_line(name: str, components: tuple, basis: str = None) -> str:
    """`UNIVERSE <name> = <dim> [* <dim>] [BASIS <b>]` — UNRESTRICTED only.

    No WHERE clause is ever emitted by K0. A governed universe carrying a restriction refuses
    upstream: restriction lowering is compiler composition over coordinate realizations, and that
    composition is not in this unit."""
    _require(_CML_NAME, name, "UNIVERSE name", f"universe {name}")
    if not components:
        raise ExecutionRepresentationGap(
            "a universe must bundle at least one base dimension", subject=f"universe {name}")
    for c in components:
        _require(_LEVEL_NAME, c, "universe base dimension", f"universe {name}")
    line = f"UNIVERSE {name} = " + " * ".join(components)
    if basis is not None:
        if basis not in _BASIS_TYPES:
            raise UnsupportedCoreCapability(
                f"declared basis {basis!r} is not one of Core's population bases "
                f"{sorted(_BASIS_TYPES)}; it cannot be carried without changing its meaning",
                subject=f"universe {name}")
        line += f"   BASIS {basis}"
    return line


def level_line(name: str, column: str) -> str:
    """`LEVEL <name> = <column> BASE` — the anchor component, named, never positional.

    BASE is emitted because K0 realizes only base coordinates: every level it emits is a dimension a
    universe bundles directly, never one reached by a functional edge (K0 emits no edges at all)."""
    _require(_LEVEL_NAME, name, "LEVEL name", f"level {name}")
    _require(_COLUMN, column, "LEVEL realized column", f"level {name}")
    return f"LEVEL {name} = {column} BASE"


def measure_block(name: str, universe: str, table: str, column: str,
                  members: tuple, logical_type: str) -> str:
    """`MEASURE <n> ON <u> FROM <t> VALUE <col> TYPE <dtype> FAMILY { ... }`.

    ALWAYS `ON <universe>`, never the single-universe sugar: the sugar's behaviour changes the
    moment a second universe appears, and an image whose meaning depends on how many siblings it
    has is not one a compiler should produce.

    ALWAYS `VALUE ... + FAMILY { ... }`, never the inline `AS agg(...)` form, so one measure with
    one member and one measure with four are emitted by the same rule.

    ALWAYS an explicit `TYPE`, never Core's `Float64` default: the governed `value_type` is meaning,
    and defaulting would silently substitute the compiler's guess for the author's declaration.

    CLAUSE ORDER IS LOAD-BEARING: `TYPE` must precede `VALUE`. The parser reads `VALUE` with a
    lazy match that stops only at `M_ANCHOR`, `FAMILY` or end-of-statement — it does NOT stop at
    `TYPE` — so `VALUE amount TYPE Float64` yields the pre-expression `amount TYPE Float64`, which
    parses clean, passes `check()` clean, and then emits `sum(amount TYPE Float64)` at the
    connector. The document is well-formed and the SQL is not. Emit `TYPE` first."""
    _require(_CML_NAME, name, "MEASURE name", f"measure {name}")
    _require(_CML_NAME, universe, "MEASURE universe", f"measure {name}")
    _require(_CML_NAME, table, "MEASURE table", f"measure {name}")
    _require(_COLUMN, column, "MEASURE value column", f"measure {name}")
    if not members:
        raise UnsupportedCoreCapability(
            "a measure needs at least one family member to be servable", subject=f"measure {name}")
    head = (f"MEASURE {name} ON {universe} FROM {table} "
            f"TYPE {logical_type} VALUE {column}")
    body = "\n".join(f"        {agg}" for agg in members)
    return f"{head}\n    FAMILY {{\n{body}\n    }}"


def render(manifold_id: str, source_version: str, universes: tuple, levels: tuple,
           measures: tuple) -> str:
    """Assemble the image. One trailing newline; no other trailing whitespace anywhere.

    Callers pass ALREADY-SORTED sequences — sorting is the compiler's job, not the renderer's, so
    that determinism is decided in one place and testable there."""
    parts = [manifold_header(manifold_id), source_manifold_line(manifold_id, source_version), ""]
    parts += list(universes) + [""]
    parts += list(levels) + [""]
    for i, block in enumerate(measures):
        parts.append(block)
        if i != len(measures) - 1:
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"
