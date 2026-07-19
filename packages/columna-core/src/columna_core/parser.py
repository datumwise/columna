"""
columna_core.parser — the definition-language parser (ingest-first authoring).

Translates a written MANIFOLD definition (the .cf successor, the corrected grammar)
into the in-memory Manifold object (model.py). This is the AUTHORING entry point: the
planner/engine already run on the object; the parser removes hand-construction so a
written definition is queryable end-to-end.

Grammar (statement-oriented; '#' comments; { } blocks):
    MANIFOLD <name> VERSION <n>
    UNIVERSE <name> = <dim> * <dim> ... [WHERE <predicate>]
    LEVEL <name> = <column> [BASE] [ATTR <name> = <table>.<column> [, ...]]
    HIERARCHY <lineage> { <a> -> <b> VIA <table>(<a_col>, <b_col>) [-> <c> VIA ...] ; <path> ... }
    RELATE <a> <-> <b> VIA <table> [NOTE "<text>"]

    Any declaration may carry (case-demo b/d):
      -- "<text>"                     a DESCRIPTION (folklore) — LOGICAL, flows to describe + the wire
      REJECT <table>.<col> "<reason>" an attested rejected/aside physical incarnation — PHYSICAL,
                                      map-artifact-ONLY, NEVER crosses describe or the wire (§2b)
    MEASURE <name> ON <universe> FROM <table> AS <agg>(<expr>)
    MEASURE <name> ON <universe> FROM <table> VALUE <expr>
        [M_ANCHOR { <col>, ... }]
        [FAMILY { <agg> [: <tier>] [BLOCKED { <lineage>, ... }] ... }]
    DERIVED <name> = <expr>
"""
from __future__ import annotations
import re
from dataclasses import replace
from typing import Optional
from .model import (Manifold, Universe, DimensionLevel, FunctionalEdge,
                    MeasureColumn, FamilyMember, BAnchor, DerivedColumn,
                    Ref, Comparison, Predicate, Assert, Hierarchy,
                    Relate, Face, FACE_SCHEMES, TOUCH)

_KW = ("MANIFOLD", "UNIVERSE", "LEVEL", "RELATE", "MEASURE", "DERIVED",
       "ASSERT", "HIERARCHY", "ATTR")   # EDGE purged (§2a); ATTR = standalone universe row-attributes

# B1 (capture §7): the comparison set an aggregate-invariant ASSERT may use. `==` rides the WP-B
# adjudication tolerance (one tolerance policy, everywhere); v1 excludes `!=`.
ASSERT_OPS = ("==", "<=", ">=", "<", ">")

# B3 (capture §7): the four population bases, each determining what absence MEANS engine-wide.
BASIS_TYPES = frozenset({"events", "spine", "product", "registry"})


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


# ---- DESCRIPTION + REJECT (case-demo b/d) -----------------------------------
# Two annotations any declaration may carry. They are opposite sides of the blast wall:
#   DESCRIPTION  `-- "<text>"`     folklore-into-the-system; LOGICAL — flows to describe + the wire.
#   REJECT       `REJECT <phys> "<reason>"`   the author's attested record of a physical incarnation
#                that was surveyed and NOT chosen (or a caveat on the chosen binding, e.g. the eom
#                fossil). PHYSICAL + map-artifact-only — it NEVER crosses describe or the wire (§2b).
# `--` (double dash + quote) never collides with a formula minus (single `-`) or the `->` hop arrow.
_DESC_RE = re.compile(r'--\s*"([^"]*)"')
_REJECT_RE = re.compile(r'REJECT\s+([\w.]+)\s+"([^"]*)"')


def _pop_rejects(s: str):
    """Strip every REJECT clause off a declaration. Returns (clean_s, rejects) with
    rejects = ((physical, reason), ...) — attested, NOT adjudicated, map-artifact-only."""
    rejects = tuple((p, r) for p, r in _REJECT_RE.findall(s))
    return _REJECT_RE.sub("", s), rejects


def _pop_desc(s: str):
    """Strip the FIRST DESCRIPTION (`-- "text"`) off a line. Returns (clean_s, description)."""
    m = _DESC_RE.search(s)
    if not m:
        return s, ""
    return (s[:m.start()] + s[m.end():]).rstrip(), m.group(1)


# ---- statement parsers ------------------------------------------------------
def _p_manifold(s, M):
    m = re.match(r"MANIFOLD\s+(\w+)\s+VERSION\s+(\d+)", s)
    if not m:
        raise ParseError(f"bad MANIFOLD header: {s!r}")
    M["name"], M["version"] = m.group(1), int(m.group(2))


def _p_universe(s, M):
    s, rejects = _pop_rejects(s)          # map-layer incarnations (e.g. inventory's eom fossil note)
    s, description = _pop_desc(s)
    # optional trailing `BASIS <type>` (B3) — stripped first so the WHERE predicate parse is undisturbed.
    basis = None
    bm = re.search(r"\s+BASIS\s+(\w+)\s*$", s)
    if bm:
        basis = bm.group(1)
        if basis not in BASIS_TYPES:
            raise ParseError(f"bad UNIVERSE BASIS '{basis}' (one of {sorted(BASIS_TYPES)})")
        s = s[:bm.start()]
    m = re.match(r"UNIVERSE\s+(\w+)\s*=\s*(.+?)(?:\s+WHERE\s+(.+))?$", s, re.S)
    if not m:
        raise ParseError(f"bad UNIVERSE: {s!r}")
    name = m.group(1)
    dims = frozenset(d.strip() for d in m.group(2).split("*"))
    pred = parse_predicate(m.group(3).strip()) if m.group(3) else None
    M["universes"][name] = Universe(name, dims, pred, basis, description=description, rejects=rejects)


def _parse_attrs(text: str):
    """Parse an ATTR clause `<name> = <table>.<column> [, <name> = ...]` -> ((name, binding), ...).
    A logical attribute OF a level (case-demo c, OF-9): the NAME is logical (referenced as
    `<level>.<name>` in predicates); the `<table>.<column>` binding is physical (map-layer)."""
    attrs = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        am = re.match(r"(\w+)\s*=\s*([\w.]+)\s*$", part)
        if not am:
            raise ParseError(f"bad ATTR clause: {part!r} (expected '<name> = <table>.<column>')")
        attrs.append((am.group(1), am.group(2)))
    return tuple(attrs)


def _p_level(s, M):
    s, rejects = _pop_rejects(s)          # region's two rejects live here (map-layer)
    s, description = _pop_desc(s)
    # optional trailing `ATTR <a> = <table>.<col> [, ...]` (case-demo c) — logical attributes OF the level
    attributes = ()
    am = re.search(r"\s+ATTR\s+(.+)$", s, re.S)
    if am:
        attributes = _parse_attrs(am.group(1))
        s = s[:am.start()]
    m = re.match(r"LEVEL\s+([\w.]+)\s*=\s*(\w+)(\s+BASE)?\s*$", s)
    if not m:
        raise ParseError(f"bad LEVEL: {s!r}")
    name = m.group(1)
    # A level name is declared once. Caught here (before the dict would silently collapse the dupe)
    # so the per-universe leaf-uniqueness check below is SOUND — two identical names share a leaf and
    # would otherwise vanish into one key and escape the check.
    if name in M["levels"]:
        raise ParseError(f"duplicate LEVEL declaration '{name}' — a level name is declared exactly once")
    M["levels"][name] = DimensionLevel(name, m.group(2), bool(m.group(3)),
                                       description=description, rejects=rejects, attributes=attributes)


# EDGE is PURGED (case-demo §2a): an edge is a two-node hierarchy; HIERARCHY is the sole surface for
# functional paths. The desugaring below emits the SAME FunctionalEdges the old EDGE produced — the
# edges stay the single internal truth (adjudicator/planner/engine untouched).
_HOP = re.compile(r"->\s*([\w.]+)\s+VIA\s+(\w+)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)")


def _parse_hier_path(path_str: str, lineage: str):
    """Parse one path `<a> -> <b> VIA t(a,b) [-> <c> VIA t(b,c)] ...` -> (chain, [FunctionalEdge]).
    Per-hop VIA (§2a). A single-hop path is a plain edge; a multi-hop path is a composable chain."""
    mstart = re.match(r"\s*([\w.]+)\s*", path_str)
    if not mstart:
        raise ParseError(f"bad HIERARCHY path (no start level): {path_str!r}")
    cur, rest = mstart.group(1), path_str[mstart.end():]
    chain, edges, pos = [cur], [], 0
    for hm in _HOP.finditer(rest):
        if rest[pos:hm.start()].strip():   # only non-whitespace between hops is malformed (§2a: hops may be spaced)
            raise ParseError(f"bad HIERARCHY hop in {path_str!r} near {rest[pos:hm.start()]!r} "
                             f"(expected '-> <level> VIA <table>(<col>, <col>)')")
        to, table, fcol, tcol = hm.group(1), hm.group(2), hm.group(3), hm.group(4)
        edges.append(FunctionalEdge(cur, to, lineage, table, fcol, tcol))
        chain.append(to); cur = to; pos = hm.end()
    if rest[pos:].strip():
        raise ParseError(f"bad HIERARCHY path tail in {path_str!r}: {rest[pos:].strip()!r}")
    if len(chain) < 2:
        raise ParseError(f"bad HIERARCHY along '{lineage}': a path needs >= 2 levels, got {chain}")
    return tuple(chain), edges


def _p_faces(frm: str, to: str, block: str) -> tuple:
    """Parse a RELATE FACES block — mirror of the derived FERTILE family, same polarity: each member is
    `<name> = <SCHEME> [<selection>] -- "<folklore>"`. The parser RECORDS the declaration only (scheme +
    selection + description; license=None); the adjudicator at publish is the SOLE constructor of a
    License. DESCRIPTION is mandatory (the folklore rule — a face must say what the crossing does).

    v1 EXECUTES `touch` only; `assign`/`alloc` are known schemes but declared-but-deferred — they parse-
    error here so no .cml can silently declare an inert face."""
    faces, seen = [], set()
    for line in block.splitlines():        # one face per line (mirror the measure FAMILY); ';' is legal in folklore
        t = line.strip().rstrip(",")
        if not t:
            continue
        t, desc = _pop_desc(t)            # folklore `-- "..."`
        t = t.strip().rstrip(",")
        fm = re.match(r"(\w+)\s*=\s*(\w+)(?:\s+(.*))?$", t)
        if not fm:
            raise ParseError(f"bad FACE on RELATE {frm}<->{to}: {t!r} "
                             f"(expected '<name> = <SCHEME> [<selection>] -- \"<folklore>\"')")
        name, scheme, selection = fm.group(1), fm.group(2).lower(), (fm.group(3) or "").strip()
        if scheme not in FACE_SCHEMES:
            raise ParseError(f"FACE {name} on RELATE {frm}<->{to}: unknown scheme {fm.group(2)!r} "
                             f"(one of {', '.join(x.upper() for x in FACE_SCHEMES)})")
        if scheme != TOUCH:
            raise ParseError(f"FACE {name}: scheme {scheme!r} is declared-but-deferred — v1 executes TOUCH "
                             f"only (assign/alloc are post-launch ledger items)")
        if not desc:
            raise ParseError(f"FACE {name} on RELATE {frm}<->{to}: a DESCRIPTION (`-- \"...\"`) is required "
                             f"(the folklore rule) — say what the crossing does")
        if name in seen:
            raise ParseError(f"FACE {name}: declared twice on RELATE {frm}<->{to}")
        seen.add(name)
        faces.append(Face(name, scheme, description=desc, selection=selection, license=None))
    return tuple(faces)


def _p_relate(s, M):
    # RELATE <a> <-> <b> VIA <table>[(<frm_col>, <to_col>)] [FACES { <name> = <SCHEME> -- "..." ; ... }] [NOTE "<text>"]
    #
    # The bare `VIA <table>` form (no join columns, no faces) is the SHIPPED grammar — untouched, so
    # existing manifolds (Cascadia declares no faces) parse byte-identically. A declared FACE REQUIRES the
    # bridge join columns `VIA <table>(<frm_col>, <to_col>)` (per-hop VIA, copied from HIERARCHY): the
    # engine needs the bridge keys to join-multiply, so a face without them fails closed at authoring.
    faces_block = _block(s, "FACES")
    note_m = re.search(r'NOTE\s+"(.*)"\s*$', s, re.S)
    note = note_m.group(1) if note_m else ""
    head = s.split("FACES", 1)[0] if faces_block is not None else s
    head = re.sub(r'\s+NOTE\s+".*"\s*$', "", head, flags=re.S).strip()   # peel a trailing NOTE off the head
    hm = re.match(r'RELATE\s+([\w.]+)\s*<->\s*([\w.]+)\s+VIA\s+(\w+)(?:\s*\(\s*(\w+)\s*,\s*(\w+)\s*\))?\s*$', head)
    if not hm:
        raise ParseError(f"bad RELATE: {s!r} (expected 'RELATE <a> <-> <b> VIA <table>[(<frm_col>, "
                         f"<to_col>)] [FACES {{ .. }}] [NOTE \"..\"]')")
    frm, to, table, fcol, tcol = hm.group(1), hm.group(2), hm.group(3), hm.group(4), hm.group(5)
    faces = _p_faces(frm, to, faces_block) if faces_block is not None else ()
    if faces and (fcol is None or tcol is None):
        raise ParseError(f"RELATE {frm}<->{to}: a declared FACE needs the bridge join columns — write "
                         f"'VIA {table}(<{frm}_col>, <{to}_col>)' so the engine can cross the edge")
    M["non_functional"].append(Relate(frm, to, note, faces, table, fcol, tcol))


def _split_top_at(rest: str):
    """Split `rest` at a TOP-LEVEL (paren-depth 0) ` AT ` into (formula, level|None).
    `AT` is the resolution-anchor keyword only at depth 0 — an expression's own parens are
    transparent — so a dotted family reference (`level.last`) and `AT day` compose unambiguously."""
    depth, at = 0, -1
    for i, c in enumerate(rest):
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif depth == 0 and rest[i:i + 4] == " AT ":
            at = i
    if at < 0:
        return rest.strip(), None
    level = rest[at + 4:].strip()
    if not re.match(r"^[\w.]+$", level):
        raise ParseError(f"bad DERIVED resolution anchor: expected 'AT <level>', got {rest[at:]!r}")
    return rest[:at].strip(), level


def _p_fertility_family(name: str, block: str) -> dict:
    """Parse a derived FAMILY block — mirror of the measure FAMILY, inverted polarity: a member is
    `<member> FERTILE { <lineages> }`. The parser RECORDS the declaration only (declared_lineages +
    license=None); the adjudicator at publish is the sole constructor of a License. Empty
    `FERTILE {}` = a declared member with no travel; no member is ever implied."""
    family = {}
    for line in block.splitlines():
        t = line.strip().rstrip(",")
        if not t:
            continue
        mm = re.match(r"(\w+)\s*FERTILE\s*\{([^}]*)\}\s*$", t)
        if not mm:
            raise ParseError(f"bad derived FAMILY member in {name}: {t!r} "
                             f"(expected '<member> FERTILE {{ <lineages> }}')")
        member = mm.group(1)
        lineages = frozenset(x.strip() for x in re.split(r"[,\s]+", mm.group(2)) if x.strip())
        family[member] = FamilyMember(member, declared_lineages=lineages, license=None)
    return family


def _p_derived(s, M):
    # DERIVED <name> = <formula> [AT <level>] [FAMILY { <member> FERTILE { <lineages> } ... }]
    #
    # Grammar boundary (explicit): the FORMULA is everything after '=' up to a top-level `AT`
    # keyword or the `FAMILY` block or end-of-line. `AT`/`FAMILY` are keywords only at paren-depth 0.
    # Authority chain: declare (here) -> adjudicate (publish) -> License. This parser records
    # declarations; it never fills a verdict, so no .cml can arrive claiming VERIFIED.
    fam_block = _block(s, "FAMILY")
    head = s.split("FAMILY", 1)[0] if fam_block is not None else s
    head, description = _pop_desc(head)     # e.g. return_rate's null-handling folklore
    m = re.match(r"DERIVED\s+(\w+)\s*=\s*(.+)", head, re.S)
    if not m:
        raise ParseError(f"bad DERIVED: {s!r}")
    name, rest = m.group(1), m.group(2).strip()
    formula, res_anchor = _split_top_at(rest)
    family = _p_fertility_family(name, fam_block) if fam_block is not None else {}
    M["derived"][name] = DerivedColumn(name, formula.strip(),
                                       family=family, resolution_anchor=res_anchor,
                                       description=description)




def _p_measure(s, M):
    # §2c single-universe sugar: `ON <universe>` is OPTIONAL; a None universe is filled with the sole
    # universe in parse_manifold (or errors if the manifold has more than one).
    s, rejects = _pop_rejects(s)          # rejected physical incarnations (e.g. the stale summary tables)
    fam_block = _block(s, "FAMILY")
    man_block = _block(s, "M_ANCHOR")
    # DESCRIPTION lives on the HEADER, before the FAMILY block; per-member descriptions live inside it.
    head_portion = s.split("FAMILY", 1)[0] if fam_block is not None else s
    head_portion, description = _pop_desc(head_portion)

    head = re.match(r"MEASURE\s+(\w+)(?:\s+ON\s+(\w+))?\s+FROM\s+(\w+)", head_portion)
    if not head:
        raise ParseError(f"bad MEASURE header: {s!r}")
    name, universe, table = head.group(1), head.group(2), head.group(3)

    inline = re.search(r"\bAS\s+(\w+)\s*\((.*?)\)", head_portion)

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
        val = re.search(r"\bVALUE\s+(.+?)(?=\s+M_ANCHOR\b|\s+FAMILY\b|$)", head_portion, re.S)
        pre_expr = val.group(1).strip() if val else ""
        if fam_block is None:
            raise ParseError(f"MEASURE {name}: needs AS <agg>(...) or VALUE + FAMILY block")
        for line in fam_block.splitlines():
            t = line.strip().rstrip(",")
            if not t:
                continue
            t, mem_desc = _pop_desc(t)        # per-member folklore (e.g. stock.sum / stock.last)
            t = t.strip().rstrip(",")
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
            family[agg] = FamilyMember(agg, BAnchor(blocked), order_by, description=mem_desc)

    m_anchor = frozenset()
    if man_block is not None:
        m_anchor = frozenset(x.strip() for x in man_block.split(",") if x.strip())

    # optional logical dtype: "... TYPE Categorical" (default Float64). Vocabulary, not physical.
    tm = re.search(r"\bTYPE\s+(\w+)", head_portion)
    logical_type = tm.group(1) if tm else "Float64"

    M["measures"][name] = MeasureColumn(name, universe, table, pre_expr,
                                        logical_type=logical_type,
                                        family=family, m_anchor=m_anchor,
                                        distinct_col=distinct_col,
                                        description=description, rejects=rejects)


def _split_invariant(inv: str, name: str):
    """Split an aggregate-invariant body at its top-level comparison (paren-transparent). Longer ops
    win at a position (`<=` before `<`), so `a <= b` never reads as `a < =b`."""
    depth = 0
    for i, c in enumerate(inv):
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif depth == 0:
            for op in ASSERT_OPS:
                if inv[i:i + len(op)] == op:
                    left, right = inv[:i].strip(), inv[i + len(op):].strip()
                    if not left or not right:
                        raise ParseError(f"bad ASSERT {name!r} invariant: empty side around {op!r}")
                    return left, op, right
    raise ParseError(f"bad ASSERT {name!r} invariant {inv!r}: expected a comparison "
                     f"(one of {list(ASSERT_OPS)})")


def _p_assert(s, M):
    # ASSERT <name> ON <universe> WHERE <predicate>                 (row-level; universe-carving grammar)
    # ASSERT <name> ON <universe> AT <anchor> HOLDS <invariant>     (aggregate over measures at an anchor)
    # §2c single-universe sugar: `ON <universe>` is OPTIONAL (filled in parse_manifold when sole).
    s, description = _pop_desc(s)          # e.g. returns_bounded's "the team's data contract" folklore
    head = re.match(r"ASSERT\s+(\w+)(?:\s+ON\s+(\w+))?\s+(WHERE\s+.+|AT\s+.+)$", s, re.S)
    if not head:
        raise ParseError(f"bad ASSERT: {s!r} (expected 'ASSERT <name> [ON <universe>] WHERE/AT ...')")
    name, universe, rest = head.group(1), head.group(2), head.group(3).strip()
    wm = re.match(r"WHERE\s+(.+)$", rest, re.S)
    if wm:
        M["asserts"].append(Assert(name, universe, "row",
                                   predicate=parse_predicate(wm.group(1).strip()),
                                   description=description))
        return
    am = re.match(r"AT\s+(.+?)\s+HOLDS\s+(.+)$", rest, re.S)
    if not am:
        raise ParseError(f"bad ASSERT {name!r}: expected 'WHERE <predicate>' or "
                         f"'AT <anchor> HOLDS <invariant>', got {rest!r}")
    anchor = tuple(a.strip() for a in re.split(r"[*,]", am.group(1)) if a.strip())
    left, op, right = _split_invariant(am.group(2).strip(), name)
    M["asserts"].append(Assert(name, universe, "invariant", anchor=anchor,
                               left=left, op=op, right=right, description=description))


def _p_hierarchy(s, M):
    # HIERARCHY <lineage> { <a> -> <b> VIA t(a,b) [-> <c> VIA t(b,c)] [; <path2>] }   (§2a)
    # Branching allowed (a small DAG — calendar is chain + week branch). Each hop carries its VIA.
    # Desugars to plain FunctionalEdges (the single internal truth) + a provenance record holding paths.
    s, description = _pop_desc(s)          # lineage folklore (names a MEANING — location, calendar)
    m = re.match(r"HIERARCHY\s+(\w+)\s*\{(.*)\}\s*$", s, re.S)
    if not m:
        raise ParseError(f"bad HIERARCHY: {s!r} (expected 'HIERARCHY <lineage> {{ <a> -> <b> "
                         f"VIA <table>(<col>, <col>) [-> ...] [; <path>] }}')")
    lineage, body = m.group(1), m.group(2)
    paths = []
    for path_str in re.split(r"[;\n]", body):
        if not path_str.strip():
            continue
        chain, edges = _parse_hier_path(path_str.strip(), lineage)
        M["edges"].extend(edges)        # the edges remain the single truth (indistinguishable from old EDGEs)
        paths.append(chain)
    if not paths:
        raise ParseError(f"bad HIERARCHY '{lineage}': no paths in the block")
    M["hierarchies"].append(Hierarchy(lineage, tuple(paths), description=description))   # provenance + FD handle


def _p_attr(s, M):
    # ATTR <name>[= <table>.<col>][, ...] ON <universe>  — logical ROW-attributes of a universe
    # (case-demo c extended). Legal in a ROW-form ASSERT's predicate; a row-attribute may SHARE its
    # physical spelling (no `= binding` -> the name is its own binding, resolved against the home table).
    m = re.match(r"ATTR\s+(.+?)\s+ON\s+(\w+)\s*$", s, re.S)
    if not m:
        raise ParseError(f"bad ATTR: {s!r} (expected 'ATTR <name>[= <table>.<col>][, ...] ON <universe>')")
    attrs = []
    for part in m.group(1).split(","):
        part = part.strip()
        if not part:
            continue
        pm = re.match(r"(\w+)(?:\s*=\s*([\w.]+))?\s*$", part)
        if not pm:
            raise ParseError(f"bad ATTR entry: {part!r} (expected '<name>' or '<name> = <table>.<col>')")
        attrs.append((pm.group(1), pm.group(2) or pm.group(1)))   # share spelling when no binding given
    M["universe_attrs"].append((m.group(2), tuple(attrs)))


_DISPATCH = {"MANIFOLD": _p_manifold, "UNIVERSE": _p_universe, "LEVEL": _p_level,
             "RELATE": _p_relate, "MEASURE": _p_measure, "DERIVED": _p_derived,
             "ASSERT": _p_assert, "HIERARCHY": _p_hierarchy, "ATTR": _p_attr}


# ---- public -----------------------------------------------------------------
def parse_manifold(text: str) -> Manifold:
    M = {"name": None, "version": 1, "universes": {}, "levels": {}, "edges": [],
         "measures": {}, "derived": {}, "non_functional": [], "asserts": [], "hierarchies": [],
         "universe_attrs": []}
    for stmt in _statements(text):
        kw = stmt.strip().split()[0]
        _DISPATCH[kw](stmt, M)
    if M["name"] is None:
        raise ParseError("missing MANIFOLD header")
    # merge standalone universe ROW-attributes onto their (frozen) Universe (declared in any order)
    for uname, attrs in M["universe_attrs"]:
        if uname not in M["universes"]:
            raise ParseError(f"ATTR references unknown universe '{uname}'")
        u = M["universes"][uname]
        M["universes"][uname] = replace(u, attributes=u.attributes + attrs)
    # §2c single-universe sugar: a MEASURE/ASSERT that omitted `ON <universe>` takes the sole universe;
    # with more than one universe, `ON` is REQUIRED (fail closed, naming the ambiguity).
    _unis = list(M["universes"])
    for nm, meas in list(M["measures"].items()):
        if meas.universe is None:
            if len(_unis) != 1:
                raise ParseError(f"MEASURE {nm}: 'ON <universe>' is required — the manifold has "
                                 f"{len(_unis)} universes {sorted(_unis)}, so the population is not implicit")
            M["measures"][nm] = replace(meas, universe=_unis[0])
    for i, a in enumerate(M["asserts"]):
        if a.universe is None:
            if len(_unis) != 1:
                raise ParseError(f"ASSERT {a.name}: 'ON <universe>' is required — the manifold has "
                                 f"{len(_unis)} universes {sorted(_unis)}, so the population is not implicit")
            M["asserts"][i] = replace(a, universe=_unis[0])
    manifold = Manifold(M["name"], M["version"], M["universes"], M["levels"],
                        M["edges"], M["measures"], M["derived"], M["non_functional"],
                        M["asserts"], M["hierarchies"])
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
                    if ref.is_literal:
                        continue
                    if ref.table is None and ref.column in m.measures:
                        errs.append(f"universe '{u.name}' predicate references measure '{ref.column}' (impure)")
                    # attribute ref (case-demo c): when the head is a DECLARED level, `<level>.<attr>`
                    # must resolve to a DECLARED logical attribute — `day >= store.opened` needs `store`
                    # to carry `opened`. A dotted head that is NOT a level is an un-migrated PHYSICAL
                    # residue (`stores.opened_date`) — allowed for back-compat, not an attribute claim.
                    if ref.table is not None and ref.table in m.levels:
                        lvl = m.levels[ref.table]
                        if ref.column not in {a for a, _ in lvl.attributes}:
                            errs.append(f"universe '{u.name}' predicate references undeclared attribute "
                                        f"'{ref.table}.{ref.column}'")
    # RELATE well-formedness (fail-closed): endpoints must be declared levels, and a relate carrying a
    # FACE must carry the bridge join columns (the engine needs them to cross). Face schemes/descriptions
    # are already enforced at parse; here we guard the structure the planner/engine will resolve against.
    for rel in m.non_functional:
        for lv in (rel.frm, rel.to):
            if lv not in m.levels:
                errs.append(f"RELATE {rel.frm}<->{rel.to} references unknown level '{lv}'")
        if rel.faces and (rel.via_frm_col is None or rel.via_to_col is None):
            errs.append(f"RELATE {rel.frm}<->{rel.to} declares a FACE but has no bridge join columns "
                        f"(write 'VIA <table>(<frm_col>, <to_col>)')")
    # derived closure: formula names resolve to measures/derived.
    # Scope the well-formedness check to the dotted-HEAD name: a reference like `level.last` names
    # the column `level` with a family-member selector `.last` — only the head is a column name, and
    # member validity is the planner's job (its expression parser handles the same dotted ref, both
    # inline and for a Python-built DerivedColumn). The old naive tokenizer split `level.last` into
    # `level` + `last` and rejected `last`, making any authored DERIVED over a multi-member family
    # inexpressible though the object model supports it. (audit v0.2, B4 parser finding)
    known = set(m.measures) | set(m.derived)
    for d in m.derived.values():
        for ref in re.findall(r"[A-Za-z_]\w*(?:\.\w+)*", d.formula):
            head = ref.split(".", 1)[0]
            if head not in known:
                errs.append(f"derived '{d.name}' references unknown column '{head}'")
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

    # lineage / level well-formedness (WP-B, fail-closed): a lineage named in a FERTILE (or BLOCKED)
    # block must be carried by a declared edge — opening (or closing) a door that doesn't exist is a
    # mistake. A resolution anchor must name a declared level; reachability from the components'
    # universes is the adjudicator's job, not the parser's.
    edge_lineages = {e.lineage for e in m.edges}
    for d in m.derived.values():
        if d.resolution_anchor is not None and d.resolution_anchor not in m.levels:
            errs.append(f"derived '{d.name}': resolution anchor 'AT {d.resolution_anchor}' names an "
                        f"unknown level (have {sorted(m.levels)})")
        for member, fm in d.family.items():
            for lin in fm.declared_lineages:
                if lin not in edge_lineages:
                    errs.append(f"derived '{d.name}' member '{member}': FERTILE lineage '{lin}' is not "
                                f"carried by any declared edge (have {sorted(edge_lineages)})")
    # align the measure BLOCKED validation to the same fail-closed rule (previously unchecked —
    # closing a nonexistent door is harmless, but the asymmetry is worth erasing; see PR note)
    for meas in m.measures.values():
        for agg, fm in meas.family.items():
            for lin in fm.b_anchor.blocked_lineages:
                if lin not in edge_lineages:
                    errs.append(f"measure '{meas.name}' member '{agg}': BLOCKED lineage '{lin}' is not "
                                f"carried by any declared edge (have {sorted(edge_lineages)})")

    # ── anchor-grammar naming laws (capture §2b, fail closed) ───────────────────────────────────
    def _leaf(name: str) -> str:
        return name.rsplit(".", 1)[-1]

    def _families_of(level: str) -> set:
        # edge-derived membership: the lineages of the edges a level touches
        return {e.lineage for e in m.edges if level in (e.frm, e.to)}

    # (item 2) leaf-name uniqueness scoped PER UNIVERSE: within each universe's included levels (base
    # dimensions + everything functionally reachable from them), two DISTINCT levels may not share a
    # leaf (short) name. The same leaf MAY recur across different universes as distinct levels — the
    # ambiguity `revenue @ week` guards against is only ever asked inside one population. Both
    # declaration sites are named. Rationale: distinct concepts get distinct names (`week`/`fiscal_week`),
    # surfacing ambiguity at authoring, never at asking.
    for uname in m.universes:
        by_leaf: dict = {}
        for lv in m.levels:
            if m.level_universe_member(lv, uname):
                by_leaf.setdefault(_leaf(lv), []).append(lv)
        for leaf, lvls in by_leaf.items():
            if len(lvls) > 1:
                errs.append(f"universe '{uname}': levels {sorted(lvls)} share the leaf name '{leaf}' — "
                            f"leaf names must be unique within a universe; rename one so distinct "
                            f"concepts carry distinct names")

    # (item 3b) the one bad state — a single anchor token reaching two levels. A literal dotted level
    # `A.B` whose split (family `A`, level `B`) ALSO resolves — `B` is a declared level that belongs to
    # family `A` (edge-derived) — is ambiguous under the standing resolution order (literal wins, then
    # family.level). Fail closed, both sites named.
    for lv in m.levels:
        if "." in lv:
            fam, rest = lv.split(".", 1)
            if rest in m.levels and fam in _families_of(rest):
                errs.append(f"level '{lv}' collides with level '{rest}' in family '{fam}': the anchor "
                            f"token '{lv}' would reach both (a literal level and the family.level split) "
                            f"— rename one")

    # ── ASSERT well-formedness (B1, fail closed): universe/uniqueness/row-purity here; the invariant
    #    expression + anchor are the adjudicator's (planner's) authority at publish (rider 1).
    seen_assert = set()
    for a in m.asserts:
        if a.universe not in m.universes:
            errs.append(f"assert '{a.name}' binds unknown universe '{a.universe}'")
            continue
        if (a.universe, a.name) in seen_assert:      # names are unique PER UNIVERSE (rider 4)
            errs.append(f"duplicate ASSERT '{a.name}' in universe '{a.universe}' "
                        f"(assert names are unique per universe)")
        seen_assert.add((a.universe, a.name))
        if a.kind == "row":
            # purity: a row predicate is over dims/attrs, never a measure (universe-carving grammar, rider 1).
            # A declared ROW-ATTRIBUTE wins over a same-named MEASURE (case-demo c): the assert names the
            # per-row attribute `units_returned`, a DIFFERENT object from the measure `units_returned` — the
            # spec must not blur them (Huayin's ruling), so the attribute declaration disambiguates here.
            if a.predicate:
                uni = m.universes.get(a.universe)
                row_attrs = {n for n, _ in uni.attributes} if uni else set()
                for comp in a.predicate.comparisons:
                    for ref in (comp.left, comp.right):
                        if (not ref.is_literal and ref.table is None
                                and ref.column in m.measures and ref.column not in row_attrs):
                            errs.append(f"assert '{a.name}' row predicate references measure "
                                        f"'{ref.column}' (row asserts are over dims/attrs only)")
        # invariant-form: the expression + anchor are validated by the ADJUDICATOR at publish, not here
        # — the planner is the one authority on askability (rider 1). An invariant that does not serve
        # cleanly (unknown name, blocked reduction, unpinned inline reduction, bad anchor) fails publish
        # closed via AssertNotWellFormed, naming the planner's reason. Invariants legitimately use inline
        # reductions (`mean(revenue)`), so a parse-time column-head check would wrongly reject operators.
    return errs
