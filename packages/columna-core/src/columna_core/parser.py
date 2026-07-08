"""
columna_core.parser — the definition-language parser (ingest-first authoring).

Translates a written MANIFOLD definition (the .cf successor, the corrected grammar)
into the in-memory Manifold object (model.py). This is the AUTHORING entry point: the
planner/engine already run on the object; the parser removes hand-construction so a
written definition is queryable end-to-end.

Grammar (statement-oriented; '#' comments; { } blocks):
    MANIFOLD <name> VERSION <n>
    UNIVERSE <name> = <dim> * <dim> ... [WHERE <predicate>]
    LEVEL <name> = <column> [BASE]
    EDGE <from> -> <to> ALONG <lineage> VIA <table>(<from_col>, <to_col>)
    RELATE <a> <-> <b> VIA <table> [NOTE "<text>"]
    MEASURE <name> ON <universe> FROM <table> AS <agg>(<expr>)
    MEASURE <name> ON <universe> FROM <table> VALUE <expr>
        [M_ANCHOR { <col>, ... }]
        [FAMILY { <agg> [: <tier>] [BLOCKED { <lineage>, ... }] ... }]
    DERIVED <name> = <expr>
"""
from __future__ import annotations
import re
from typing import Optional
from .model import (Manifold, Universe, DimensionLevel, FunctionalEdge,
                    MeasureColumn, FamilyMember, BAnchor, DerivedColumn,
                    Ref, Comparison, Predicate)

_KW = ("MANIFOLD", "UNIVERSE", "LEVEL", "EDGE", "RELATE", "MEASURE", "DERIVED")


class ParseError(Exception):
    pass


# ---- lexing helpers ---------------------------------------------------------
def _strip_comment(line: str) -> str:
    out, inq = [], False
    for ch in line:
        if ch == '"':
            inq = not inq
        if ch == "#" and not inq:
            break
        out.append(ch)
    return "".join(out)


def _statements(text: str):
    cur, depth = [], 0
    for raw in text.splitlines():
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        first = line.strip().split()[0]
        if depth == 0 and first in _KW and cur:
            yield "\n".join(cur); cur = []
        cur.append(line)
        depth += line.count("{") - line.count("}")
    if cur:
        yield "\n".join(cur)


def _block(text: str, kw: str):
    """Return the balanced {...} content following kw, or None."""
    i = text.find(kw)
    if i < 0:
        return None
    j = text.find("{", i)
    if j < 0:
        return None
    depth, k = 0, j
    while k < len(text):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if depth == 0:
                return text[j + 1:k]
        k += 1
    raise ParseError(f"unbalanced braces after {kw}")


# ---- statement parsers ------------------------------------------------------
def _p_manifold(s, M):
    m = re.match(r"MANIFOLD\s+(\w+)\s+VERSION\s+(\d+)", s)
    if not m:
        raise ParseError(f"bad MANIFOLD header: {s!r}")
    M["name"], M["version"] = m.group(1), int(m.group(2))


def _p_universe(s, M):
    m = re.match(r"UNIVERSE\s+(\w+)\s*=\s*(.+?)(?:\s+WHERE\s+(.+))?$", s, re.S)
    if not m:
        raise ParseError(f"bad UNIVERSE: {s!r}")
    name = m.group(1)
    dims = frozenset(d.strip() for d in m.group(2).split("*"))
    pred = parse_predicate(m.group(3).strip()) if m.group(3) else None
    M["universes"][name] = Universe(name, dims, pred)


def _p_level(s, M):
    m = re.match(r"LEVEL\s+([\w.]+)\s*=\s*(\w+)(\s+BASE)?\s*$", s)
    if not m:
        raise ParseError(f"bad LEVEL: {s!r}")
    M["levels"][m.group(1)] = DimensionLevel(m.group(1), m.group(2), bool(m.group(3)))


def _p_edge(s, M):
    m = re.match(r"EDGE\s+([\w.]+)\s*->\s*([\w.]+)\s+ALONG\s+(\w+)\s+VIA\s+(\w+)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", s)
    if not m:
        raise ParseError(f"bad EDGE: {s!r}")
    M["edges"].append(FunctionalEdge(m.group(1), m.group(2), m.group(3),
                                     m.group(4), m.group(5), m.group(6)))


def _p_relate(s, M):
    m = re.match(r'RELATE\s+([\w.]+)\s*<->\s*([\w.]+)\s+VIA\s+(\w+)(?:\s+NOTE\s+"(.*)")?', s)
    if not m:
        raise ParseError(f"bad RELATE: {s!r}")
    M["non_functional"].append((m.group(1), m.group(2), m.group(4) or ""))


def _p_derived(s, M):
    m = re.match(r"DERIVED\s+(\w+)\s*=\s*(.+)", s, re.S)
    if not m:
        raise ParseError(f"bad DERIVED: {s!r}")
    M["derived"][m.group(1)] = DerivedColumn(m.group(1), m.group(2).strip())




def _p_measure(s, M):
    head = re.match(r"MEASURE\s+(\w+)\s+ON\s+(\w+)\s+FROM\s+(\w+)", s)
    if not head:
        raise ParseError(f"bad MEASURE header: {s!r}")
    name, universe, table = head.group(1), head.group(2), head.group(3)

    inline = re.search(r"\bAS\s+(\w+)\s*\((.*?)\)", s)
    fam_block = _block(s, "FAMILY")
    man_block = _block(s, "M_ANCHOR")

    distinct_col = None
    family = {}
    pre_expr = ""

    if inline and fam_block is None:
        agg = inline.group(1)
        arg = inline.group(2).strip()
        if agg == "count":
            pre_expr = "1"
        elif agg == "distinct":
            distinct_col = arg
            pre_expr = arg
        else:
            pre_expr = arg
        family = {agg: FamilyMember(agg, BAnchor())}
    else:
        val = re.search(r"\bVALUE\s+(.+?)(?=\s+M_ANCHOR\b|\s+FAMILY\b|$)", s, re.S)
        pre_expr = val.group(1).strip() if val else ""
        if fam_block is None:
            raise ParseError(f"MEASURE {name}: needs AS <agg>(...) or VALUE + FAMILY block")
        for line in fam_block.splitlines():
            t = line.strip().rstrip(",")
            if not t:
                continue
            # <agg> [BLOCKED { lineages }] [ORDER <level>]   (tier is operator-level — the registry)
            mm = re.match(r"(\w+)\s*(?:BLOCKED\s*\{([^}]*)\})?\s*(?:ORDER\s+([\w.]+))?\s*$", t)
            if not mm:
                raise ParseError(f"bad FAMILY member in {name}: {t!r}")
            agg = mm.group(1)
            blocked = frozenset(x.strip() for x in (mm.group(2) or "").split(",") if x.strip())
            order_by = mm.group(3)
            if agg == "distinct":
                distinct_col = pre_expr
            family[agg] = FamilyMember(agg, BAnchor(blocked), order_by)

    m_anchor = frozenset()
    if man_block is not None:
        m_anchor = frozenset(x.strip() for x in man_block.split(",") if x.strip())

    # optional logical dtype: "... TYPE Categorical" (default Float64). Vocabulary, not physical.
    tm = re.search(r"\bTYPE\s+(\w+)", s)
    logical_type = tm.group(1) if tm else "Float64"

    M["measures"][name] = MeasureColumn(name, universe, table, pre_expr,
                                        logical_type=logical_type,
                                        family=family, m_anchor=m_anchor,
                                        distinct_col=distinct_col)


_DISPATCH = {"MANIFOLD": _p_manifold, "UNIVERSE": _p_universe, "LEVEL": _p_level,
             "EDGE": _p_edge, "RELATE": _p_relate, "MEASURE": _p_measure, "DERIVED": _p_derived}


# ---- public -----------------------------------------------------------------
def parse_manifold(text: str) -> Manifold:
    M = {"name": None, "version": 1, "universes": {}, "levels": {}, "edges": [],
         "measures": {}, "derived": {}, "non_functional": []}
    for stmt in _statements(text):
        kw = stmt.strip().split()[0]
        _DISPATCH[kw](stmt, M)
    if M["name"] is None:
        raise ParseError("missing MANIFOLD header")
    manifold = Manifold(M["name"], M["version"], M["universes"], M["levels"],
                        M["edges"], M["measures"], M["derived"], M["non_functional"])
    errs = check_wellformed(manifold)
    if errs:
        raise ParseError("not well-formed:\n  - " + "\n  - ".join(errs))
    return manifold


def parse_file(path: str) -> Manifold:
    with open(path) as f:
        return parse_manifold(f.read())


# ---- predicate parsing (universe domain) ------------------------------------
def _ref(tok: str) -> Ref:
    tok = tok.strip()
    if tok and (tok[0] in "'\"" or tok.replace(".", "", 1).lstrip("-").isdigit()):
        return Ref(True, value=tok.strip("'\""))
    if "." in tok:                       # table.column -> attribute (cross-table)
        t, c = tok.split(".", 1)
        return Ref(False, table=t, column=c)
    return Ref(False, column=tok)        # bare -> a coordinate/level reference

def parse_predicate(s: Optional[str]) -> Optional[Predicate]:
    """Parse a universe predicate string into identified column references.
    Supports comparisons joined by AND. Each ref is a coordinate (level), an
    attribute (table.column, broadcast in-engine), or a literal."""
    if not s:
        return None
    comps = []
    for clause in re.split(r"\bAND\b", s):
        m = re.match(r"\s*(\S+)\s*(>=|<=|!=|=|>|<)\s*(\S+)\s*$", clause)
        if not m:
            raise ParseError(f"bad predicate clause: {clause!r}")
        comps.append(Comparison(_ref(m.group(1)), m.group(2), _ref(m.group(3))))
    return Predicate(tuple(comps))


# ---- well-formedness (publish-time, object-model §5) ------------------------
def check_wellformed(m: Manifold) -> list:
    errs = []
    # closure: edges/levels/measures/derived reference known names
    for e in m.edges:
        for lv in (e.frm, e.to):
            if lv not in m.levels:
                errs.append(f"edge references unknown level '{lv}'")
    for meas in m.measures.values():
        if meas.universe not in m.universes:
            errs.append(f"measure '{meas.name}' binds unknown universe '{meas.universe}'")
        # universe base dimensions must be declared levels
    for u in m.universes.values():
        for d in u.base_dimensions:
            if d not in m.levels:
                errs.append(f"universe '{u.name}' references unknown base level '{d}'")
    # predicate purity: a universe predicate must not reference a measure (over dims/attrs only)
    for u in m.universes.values():
        if u.predicate:
            for comp in u.predicate.comparisons:
                for ref in (comp.left, comp.right):
                    if not ref.is_literal and ref.table is None and ref.column in m.measures:
                        errs.append(f"universe '{u.name}' predicate references measure '{ref.column}' (impure)")
    # derived closure: formula names resolve to measures/derived
    known = set(m.measures) | set(m.derived)
    for d in m.derived.values():
        for tok in re.findall(r"[A-Za-z_]\w*", d.formula):
            if tok not in known:
                errs.append(f"derived '{d.name}' references unknown column '{tok}'")
    # operator vocabulary + type signatures (compile-time, not a data fact):
    # each family member's operator must exist in the registry, be a REDUCER (only reducers
    # found families — manual Appendix A), and accept the column's dtype.
    from .operators import REGISTRY, signature_ok, REDUCER
    for meas in m.measures.values():
        for op_name in meas.family:
            if op_name not in REGISTRY:
                errs.append(f"measure '{meas.name}': operator '{op_name}' is not in the registry "
                            f"(available: {sorted(REGISTRY)})")
                continue
            op = REGISTRY[op_name]
            if op.kind != REDUCER:
                errs.append(f"measure '{meas.name}': operator '{op_name}' is a {op.kind}, not a reducer "
                            f"— only reducers found families (scans are applied in queries, "
                            f"e.g. {op_name}({meas.name}.<reducer>))")
                continue
            if not signature_ok(op, meas.logical_type):
                errs.append(f"measure '{meas.name}': operator '{op_name}' does not accept logical type "
                            f"'{meas.logical_type}' (accepts {sorted(op.accepts)})")
    return errs