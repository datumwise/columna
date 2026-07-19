#!/usr/bin/env python3
"""Universe Visual generator — the spec's Figure 1, built by running the SHIPPED package.

GENERATED, NEVER HAND-DRAWN (design brief, ratified 2026-07-19): the SVG is composed at build
time from `describe_manifold` + `describe_measure` ALONE — every element label, verdict, member,
formula, basis and stack is read off the wire, so the figure is auto-true as the manifold evolves
and wall-safe by construction (describe carries no physical identifier). Only the reviewed CAPTIONS
(the prose under/around the figure) are human copy, ratified at the design gate and kept in COPY
below — never element labels.

Emits JSON on stdout: the main figure SVG, the two hover-pair SVGs (the semi-additive burn), and
the ratified captions + a referent registry. Exits non-zero on any unknown declaration kind so the
build FAILS CLOSED (a new describe shape must be taught, never silently dropped).

RELATE (product<->category) is rendered DESCRIBE-TRUE (option A, design gate 2026-07-19): `category`
is a non-base level no functional edge reaches, so it draws as a floating dashed unclimbable block.
The product<->category link + cardinality live only in manifold.non_functional (not the describe
wire); they render only if/when a `relates[]` surface is added to describe (option B, pending).
"""
import html
import json
import sys
from importlib.metadata import version

from columna_server import tools as T
from columna_server.demo import demo_store, DEMO_MANIFOLD_ID as MID

# ── the four-mood palette, bound to the SHIPPED /case tokens (hex — SVG presentation attrs don't
#    resolve CSS var()). serve/corroborated · disclose · clarify/verified · refuse · untestable. ──
SERVE = "#2f6b34"; SERVE_BG = "#e6f2e6"; SERVE_RULE = "#cfe0cf"
DISCLOSE = "#c08a1e"
VERIFIED = "#2456a6"
REFUSE = "#a63030"
UNTEST = "#7a6f4e"; UNTEST_BG = "#f2efe6"
INK = "#1c1a17"; SUB = "#6b675f"; FAINT = "#a49e91"; RULE = "#c9c2b4"; PAPER = "#ffffff"

VERDICT_COLOR = {"corroborated": SERVE, "verified": VERIFIED, "disclose": DISCLOSE,
                 "contradicted": REFUSE, "untestable": UNTEST}
VERDICT_BG = {"corroborated": SERVE_BG, "verified": "#eef1fb", "untestable": UNTEST_BG}

# ── ratified CAPTIONS (Huayin, design gate 2026-07-19). PROSE only — never element labels. ──
COPY = {
    "kicker": "THE UNIVERSE VISUAL · FIGURE 1",
    "title": "Cascadia — two universes",
    "lede": ("Universe-first: each population is a box holding its grain (the floor), its reachable "
             "stacks, and its metric families. Boxes overlap where they share dimensions; the shared "
             "stacks are drawn once. Every badge is pinned to a real verdict. Labels are verbatim "
             "from describe."),
    "overlap_suffix": "— the overlap IS the shared atlas",
    "fork_note": "weeks don't nest — the fork",
    "floor_events": "solid floor = events",
    "floor_spine": "hatched floor = spine (can have gaps)",
    "hover_intro": ("The hover, shown as a static pair (in the shipped visual, hovering a family "
                    "member paints the stacks by traversability — CSS-only, no JS). Here the "
                    "first burn, taught: the same {measure} over the same {stack} stack, two members."),
    "hover_barred": ("barred (✕) — summing a stock across time doesn't reconcile; the "
                     "B-anchor bars {stack}."),
    "hover_travels": ("travels (✓) — the period-end position is a clean read; last takes "
                      "the latest snapshot."),
    "leftout": ("Left out by design (the spec + the map hold the detail): logical attributes, the "
                "map's reject rows, operator properties, provenance. The visual holds the shape; a "
                "caption links the Manifold spec and the physical→logical map."),
    "leftout_spec_route": "/manifold",       # wired to the real Manifold-spec route (design gate)
    "leftout_map_route": "/case#map",         # wired to the real physical->logical map route
    "legend": [("swatch", SERVE, "✓ corroborated hop / travels (serve)"),
               ("box", UNTEST_BG, "untestable basis (honest)"),
               ("dash", REFUSE, "RELATE — non-functional, unclimbable"),
               ("spine", None, "spine floor (gaps possible)")],
}

# describe basis kinds this generator knows how to render. Anything else => fail closed.
KNOWN_BASIS = {"events", "spine"}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


class Fail(Exception):
    """A describe shape the generator has not been taught — the build must fail closed."""


# ───────────────────────────── tiny SVG helpers ─────────────────────────────
def _t(x, y, s, size=12, fill=INK, weight=None, anchor="start", cls="", style=""):
    a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<text {" ".join(a)}>{s}</text>'


def _rect(x, y, w, h, rx=0, fill="none", stroke="none", sw=1, opacity=None, dash=None):
    a = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'rx="{rx}"',
         f'fill="{fill}"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    return f'<rect {" ".join(a)}/>'


def _line(x1, y1, x2, y2, stroke=RULE, sw=1, dash=None):
    a = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"', f'stroke="{stroke}"', f'stroke-width="{sw}"']
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    return f'<line {" ".join(a)}/>'


def _check(cx, cy, color=SERVE):
    """A corroborated hop-seam ✓ badge (glyph + color — never color alone)."""
    return (f'<g><circle cx="{cx}" cy="{cy}" r="8" fill="{SERVE_BG}" stroke="{color}" stroke-width="1"/>'
            f'{_t(cx, cy + 3.2, "✓", 10, color, anchor="middle")}</g>')


def _level_block(cx, y, label, w=64, h=26, fill=PAPER, stroke=RULE, text_fill=INK):
    """One level block in a stack, centered on cx."""
    x = cx - w / 2
    return (_rect(x, y, w, h, rx=4, fill=fill, stroke=stroke, sw=1.2)
            + _t(cx, y + h / 2 + 4, esc(label), 12, text_fill, anchor="middle", cls="mono"))


# ───────────────────────────── describe → model ─────────────────────────────
def build_model(dm):
    """Read the describe wire into a layout-neutral model. Fails closed on unknown basis."""
    universes = []
    for u in dm["universes"]:
        if u["basis"] not in KNOWN_BASIS:
            raise Fail(f"universe {u['name']!r} has unknown basis {u['basis']!r} — teach the generator")
        universes.append(u)
    # edges by base level -> the stacks that rise from it (with fork paths)
    hiers = dm["hierarchies"]
    # asserts homed per universe
    asserts = dm.get("asserts", [])
    measures = dm["measures"]
    derived = dm.get("derived", [])
    # RELATE (ruling B, 2026-07-19): declared M:N relationships ride describe as relates[] — drawn as a
    # dashed connector from the base level to a stackless `to` block, the note quoted verbatim. Fail
    # closed if a relate names a `to` level describe never declared (a new declaration kind, untaught).
    # The wedge extended to Figure 1 (ruling (i), 2026-07-19): the relates KEY must be PRESENT — an empty
    # list is a lawful "genuinely no relations", but a MISSING key means the shipped package predates the
    # RELATE wire (columna-server < 0.5.0) and cannot provide Figure 1's declared M:N. The site is
    # structurally incapable of deploying a figure the shipped describe can't fully ground — bump the pin.
    if "relates" not in dm:
        raise Fail("describe_manifold carries no `relates` key — the shipped package predates the RELATE "
                   "wire (columna-server < 0.5.0); Figure 1 cannot ground its declared M:N. Bump the pin.")
    relates = dm["relates"]
    levels = {d["level"] for d in dm["dimensions"]}
    for r in relates:
        if r["to"] not in levels or r["frm"] not in levels:
            raise Fail(f"relate {r['frm']}->{r['to']} names a level absent from describe — teach it")
    return {"universes": universes, "hierarchies": hiers, "asserts": asserts, "measures": measures,
            "derived": derived, "relates": relates, "edges": dm["edges"]}


# ───────────────────────────── the main figure ─────────────────────────────
def figure_svg(store, model):
    """Compose the two-universe figure from the model. Two-universe horizontal overlap layout."""
    us = model["universes"]
    if len(us) != 2:
        raise Fail(f"the figure layout is taught for exactly two universes; got {len(us)} — teach it")
    # order: the wider-grained universe on the left (more base dims), the other overlapping right
    a, b = sorted(us, key=lambda u: -len(u["base_dimensions"]))
    a_dims, b_dims = list(a["base_dimensions"]), list(b["base_dimensions"])
    shared = [d for d in a_dims if d in b_dims]
    a_only = [d for d in a_dims if d not in shared]
    b_only = [d for d in b_dims if d not in shared]

    W, H = 1060, 600
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="{esc(a["name"])} and {esc(b["name"])} universes, overlapping on '
             f'{esc(" and ".join(shared))}">']
    # defs: spine hatch + dash marker
    parts.append(
        '<defs>'
        '<pattern id="spine" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="8" height="8" fill="{PAPER}"/><line x1="0" y1="0" x2="0" y2="8" stroke="#d9d3c6" stroke-width="1"/>'
        '</pattern>'
        f'<marker id="dash" markerWidth="7" markerHeight="7" refX="4" refY="3.5" orient="auto">'
        f'<path d="M0,0 L6,3.5 L0,7" fill="none" stroke="{REFUSE}" stroke-width="1"/></marker>'
        '</defs>')

    # ── box geometry (2-universe template: A left, B overlapping right) ──
    ax, aw = 34, 620
    bx, bw = 470, 536
    ov_x, ov_w = bx, (ax + aw) - bx     # the overlap = where the two boxes cross
    parts.append(_rect(ax, 70, aw, 486, rx=14, fill=PAPER, stroke=RULE, sw=1.5))
    parts.append(_rect(bx, 118, bw, 438, rx=14, fill=PAPER, stroke=RULE, sw=1.5))
    parts.append(_rect(ov_x, 118, ov_w, 438, fill="#f4f1ea", opacity=".7"))

    # ── box A header ──
    parts.append(_t(52, 98, esc(a["name"]), 18, INK, weight=700))
    parts.append(_t(176, 98, f'BASIS {esc(a["basis"])}', 12.5, SUB, cls="mono"))
    parts.append(_rect(284, 82, 86, 20, rx=10, fill=UNTEST_BG))
    parts.append(_t(327, 96, "untestable", 11, UNTEST, anchor="middle", cls="tag"))
    parts.append(_t(52, 116, esc(_absence_short(a)), 11.5, FAINT))

    # ── box B header (stacked vertically in the clear zone, right of the overlap) ──
    bcx = 852
    parts.append(_rect(bcx - 43, 120, 86, 20, rx=10, fill=UNTEST_BG))
    parts.append(_t(bcx, 134, "untestable", 11, UNTEST, anchor="middle", cls="tag"))
    parts.append(_t(bcx, 166, esc(b["name"]), 18, INK, weight=700, anchor="middle"))
    parts.append(_t(bcx, 186, f'BASIS {esc(b["basis"])}', 12.5, SUB, anchor="middle", cls="mono"))
    parts.append(_t(bcx, 203, esc(_absence_short(b)), 11.5, FAINT, anchor="middle"))

    # ── floor = grain ──
    floor_y = 500
    floor_cx = {}                                          # base level -> its floor block centre
    for i, dim in enumerate(a_only):                       # A-only base blocks (box A lower-left)
        x = 58 + i * 128
        floor_cx[dim] = x + 48
        parts.append(_rect(x, floor_y, 96, 30, rx=5, fill=PAPER, stroke=RULE, sw=1.2))
        parts.append(_t(x + 48, floor_y + 19, esc(dim), 12, INK, anchor="middle", cls="mono"))
    # shared base blocks in the overlap, ordered so the taller/forked stack sits on the RIGHT
    order = sorted(shared, key=lambda d: _stack_height(model["hierarchies"], d))
    sh_slots = {}
    for i, dim in enumerate(order):
        x = 480 + i * 86
        sh_slots[dim] = floor_cx[dim] = x + 36
        parts.append(_rect(x, floor_y, 72, 30, rx=5, fill=PAPER, stroke=INK, sw=1.4))
        parts.append(_t(x + 36, floor_y + 19, esc(dim), 12, INK, anchor="middle", cls="mono"))

    # floor bar + basis textures (A + overlap solid = events; B-only span hatched = spine)
    parts.append(_rect(46, 546, 608, 6, fill=INK, opacity=".5"))
    parts.append(_rect(654, 546, 352, 6, fill="url(#spine)", stroke="#d9d3c6", sw=1))
    parts.append(_t(46, 568, COPY["floor_events"], 10, FAINT))
    parts.append(_t(1006, 568, COPY["floor_spine"], 10, FAINT, anchor="end"))
    if b.get("predicate"):                                 # carve clamp-note on the spine box's floor
        cx = 812
        parts.append(_rect(cx, 484, 182, 30, rx=6, fill=PAPER, stroke=RULE, sw=1))
        parts.append(_t(cx + 91, 498, "carve (spine)", 10.5, SUB, anchor="middle"))
        parts.append(_t(cx + 91, 510, esc(b["predicate"]), 10.5, INK, anchor="middle", cls="mono"))

    # ── the overlap label + the shared stacks (drawn once) ──
    ov_lineages = " · ".join(h["lineage"] for h in model["hierarchies"]
                             if h["chain"] and h["chain"][0] in shared)
    parts.append(_t(480, 222, f'{esc(ov_lineages)} {COPY["overlap_suffix"]}', 11.5, FAINT))
    parts.append(_stacks(model["hierarchies"], sh_slots, floor_y))

    # ── metric families, homed per universe; box A's plaque + RELATE stack below its families ──
    fam_a, end_a = _families(store, a, model, 52, 150)
    parts.append(fam_a)
    fam_b, _ = _families(store, b, model, 724, 246, right=True)
    parts.append(fam_b)

    plaque_bottom = 150
    for asrt in model["asserts"]:                          # asserts plaque(s), homed in box A
        if asrt["universe"] != a["name"]:
            continue
        v = (asrt.get("license") or {}).get("verdict")
        py = end_a + 14
        parts.append(_plaque(52, py, asrt, v))
        plaque_bottom = py + 34

    # ── RELATE (ruling B): a dashed connector from the base level to a stackless `to` block; the NOTE
    #    from describe quoted verbatim (dashed = non-functional = visually unclimbable). ──
    oy = max(plaque_bottom + 20, 430)
    for r in model["relates"]:
        tcx = 314                                          # the `to` (stackless) block, box A lower-mid
        frm_cx = floor_cx.get(r["frm"])                    # dashed connector up from the base block
        if frm_cx is not None:
            parts.append(_line(frm_cx, floor_y, tcx - 30, oy + 28, stroke=REFUSE, sw=1.3, dash="5 4"))
        parts.append(_t(tcx, oy - 6, "RELATE", 8.5, REFUSE, anchor="middle", cls="tag"))
        parts.append(_rect(tcx - 54, oy, 108, 28, rx=4, fill=PAPER, stroke=REFUSE, sw=1, dash="4 3"))
        parts.append(_t(tcx, oy + 18, esc(r["to"]), 11, REFUSE, anchor="middle", cls="mono"))
        parts.append(_t(tcx, oy + 44, esc(r["note"]), 9.5, FAINT, anchor="middle"))
        oy += 64

    parts.append(_legend(28, 588))
    parts.append('</svg>')
    return "".join(parts)


def _absence_short(u):
    s = u.get("absence", "")
    # "absence is a lawful ZERO (zero-fill; immaterial)" -> the human clause before the paren
    return s.split("(")[0].strip() if s else ""


def _stack_height(hiers, base):
    """The number of rungs the tallest chain rooted at `base` rises (for lane ordering)."""
    best = 0
    for h in hiers:
        if h.get("chain") and h["chain"][0] == base:
            best = max(best, len(h["chain"]) - 1)
    return best


def _stacks(hiers, sh_slots, floor_y):
    out = []
    PITCH, RH, RW = 66, 28, 72
    for h in hiers:
        chain = h.get("chain") or []
        base = chain[0] if chain else None
        if base not in sh_slots:      # only shared-base stacks live in the overlap (drawn once)
            continue
        v = (h.get("license") or {}).get("verdict")
        color = VERDICT_COLOR.get(v, FAINT)
        cx = sh_slots[base]
        # the primary chain rises rung by rung from the base block
        prev_top = floor_y            # the base block's top edge
        for i, lvl in enumerate(chain[1:]):
            by = floor_y - (i + 1) * PITCH
            out.append(_line(cx, prev_top, cx, by + RH, stroke=color, sw=1.4))
            out.append(_level_block(cx, by, lvl, w=RW))
            out.append(_check(cx - 48, (prev_top + by + RH) / 2, color))
            prev_top = by
        # fork paths: any other path sharing the base diverges up-right (weeks don't nest)
        for path in h.get("paths", []):
            if path == chain or len(path) < 2 or path[0] != base:
                continue
            fx = cx + 84
            for j, lvl in enumerate(path[1:]):
                fy = floor_y - (j + 1) * PITCH
                out.append(_line(cx + RW / 2 - 8, floor_y - 6, fx, fy + RH, stroke=color, sw=1.2))
                out.append(_level_block(fx, fy, lvl, w=64))
            out.append(_t(fx, floor_y - PITCH - 10, COPY["fork_note"], 9.5, FAINT, anchor="middle"))
    return "".join(out)


def _families(store, u, model, x, y, right=False):
    """Render a universe's metric families from x,y. Returns (svg, end_y)."""
    out = []
    ms = [m for m in model["measures"] if m["universe"] == u["name"]]
    ds = [d for d in model["derived"] if _derived_universe(store, d, model) == u["name"]]
    out.append(_t(x, y, "MEASURE" + ("S" if len(ms) != 1 else ""), 11, SUB, cls="tag"))
    yy = y + 24
    for m in ms:
        fam = " · ".join(m["family"])
        out.append(_t(x, yy, esc(m["name"]) + " ", 13, INK, cls="mono")
                   + _t(x + _tw(m["name"]) + 10, yy, f'[{esc(fam)}]', 13, FAINT, cls="mono"))
        yy += 24
    # semi-additive note for a family carrying a barred member (describe-derived; ratified copy)
    if right and _is_semi_additive(store, u, model):
        out.append(_t(x, yy + 4, "semi-additive — sum is barred over", 10.5, FAINT))
        out.append(_t(x, yy + 17, "calendar; last travels (see below)", 10.5, FAINT))
        yy += 34
    if ds:
        yy += 8
        out.append(_t(x, yy, "DERIVED", 11, SUB, cls="tag"))
        yy += 22
        for d in ds:
            out.append(_t(x, yy, f'{esc(d["name"])} = {esc(d["formula"])}', 12.5, SUB,
                          cls="mono", style="font-style:italic"))
            yy += 22
    return "".join(out), yy


def _plaque(x, y, asrt, verdict):
    color = VERDICT_COLOR.get(verdict, FAINT)
    bg = VERDICT_BG.get(verdict, UNTEST_BG)
    pred = (asrt.get("form") or {}).get("predicate", "")
    return (_rect(x, y, 300, 34, rx=6, fill=bg, stroke=SERVE_RULE, sw=1)
            + _t(x + 10, y + 15, f'ASSERT · {esc((verdict or "").upper())}', 10.5, color, cls="tag")
            + _t(x + 10, y + 29, f'{esc(asrt["name"])}: {esc(pred)}', 11.5, "#33502f", cls="mono"))


def _legend(x, y):
    out = ['<g>']
    cx = x
    for kind, color, label in COPY["legend"]:
        if kind == "swatch":
            out.append(_rect(cx, y - 9, 12, 12, rx=2, fill=color))
        elif kind == "box":
            out.append(_rect(cx, y - 9, 12, 12, rx=2, fill=color, stroke=UNTEST, sw=1))
        elif kind == "dash":
            out.append(_rect(cx, y - 9, 12, 12, rx=2, fill=PAPER, stroke=color, sw=1, dash="3 2"))
        elif kind == "spine":
            out.append(_rect(cx, y - 9, 12, 12, rx=2, fill="url(#spine)", stroke="#d9d3c6", sw=1))
        out.append(_t(cx + 18, y, label, 11, SUB))
        cx += 26 + _tw(label, 6.2)
    out.append('</g>')
    return "".join(out)


# ───────────────────────── describe-derived predicates ─────────────────────────
def _tw(s, per=7.4):
    return len(str(s)) * per


def _derived_universe(store, d, model):
    """A derived's home universe = the universe of the measures it references (describe-true)."""
    formula = d.get("formula", "")
    for m in model["measures"]:
        if m["name"] in formula:
            return m["universe"]
    return None


def _is_semi_additive(store, u, model):
    for m in model["measures"]:
        if m["universe"] != u["name"]:
            continue
        dm = T.describe_measure(store, MID, m["name"])
        for anc in dm["member_anchors"].values():
            if anc.get("blocked_lineages"):
                return True
    return False


# ───────────────────────────── the hover pair ─────────────────────────────
def hover_pair(store, model):
    """The first burn, taught as a static pair: the semi-additive measure's barred member vs its
    travelling member over the SAME stack. Derived from describe_measure blocked_lineages."""
    pick = None
    for m in model["measures"]:
        dm = T.describe_measure(store, MID, m["name"])
        barred_member = travel_member = None
        blocked_lineage = None
        for member, anc in dm["member_anchors"].items():
            bl = anc.get("blocked_lineages") or []
            if bl and barred_member is None:
                barred_member, blocked_lineage = member, bl[0]
            elif not bl and travel_member is None:
                travel_member = member
        if barred_member and travel_member and blocked_lineage:
            pick = (m["name"], barred_member, travel_member, blocked_lineage)
            break
    if not pick:
        return None
    measure, barred, travels, lineage = pick
    # the stack that is barred (the blocked lineage's chain, minus the base)
    chain = None
    for h in model["hierarchies"]:
        if h["lineage"] == lineage:
            chain = [lvl for lvl in h["chain"]]
            break
    if not chain:
        return None
    rungs = list(reversed(chain[1:]))    # top → bottom (e.g. cal.quarter, cal.month, day)

    def _panel(member, barred_state):
        color = REFUSE if barred_state else SERVE
        bg = "#fbece9" if barred_state else SERVE_BG
        glyph = "✕" if barred_state else "✓"
        word = "BARRED" if barred_state else "TRAVELS"
        w, h = 480, 430
        p = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" '
             f'aria-label="{esc(measure)}.{esc(member)} at {esc(lineage)} — {word.lower()}">']
        p.append(_t(24, 52, f'{esc(measure)}.{esc(member)} ', 26, INK, weight=700, cls="mono")
                 + _t(24 + _tw(f"{measure}.{member} ", 15.6), 52, f'@ {esc(lineage)}', 26, color,
                      weight=700, cls="mono"))
        bx0, bw0, bh0, gap0 = 100, 170, 60, 52
        y0 = 120
        for i, lvl in enumerate(rungs):
            yy = y0 + i * (bh0 + gap0)
            if i > 0:
                p.append(_line(bx0 + bw0 / 2, yy - gap0 + 6, bx0 + bw0 / 2, yy, stroke=color, sw=2))
            p.append(_rect(bx0, yy, bw0, bh0, rx=8, fill=bg, stroke=color, sw=2))
            p.append(_t(bx0 + bw0 / 2, yy + bh0 / 2 + 7, esc(lvl), 20, INK, anchor="middle", cls="mono"))
        # verdict glyph beside the stack
        gy = y0 + bh0 / 2
        p.append(f'<circle cx="360" cy="{gy}" r="34" fill="none" stroke="{color}" stroke-width="2.5"/>')
        p.append(_t(360, gy + 12, glyph, 34, color, anchor="middle"))
        p.append(_t(360, gy + 70, word, 20, color, anchor="middle", weight=600))
        p.append('</svg>')
        return "".join(p)

    return {
        "measure": measure, "stack": lineage, "barred_member": barred, "travels_member": travels,
        "barred_svg": _panel(barred, True),
        "travels_svg": _panel(travels, False),
    }


def _referents(model):
    us = sorted(model["universes"], key=lambda u: -len(u["base_dimensions"]))
    ents = [{"id": f"universe-{u['name']}", "name": f"{u['name']} universe",
             "aliases": [u["name"]], "anchor": f"[data-ref='universe-{u['name']}']"} for u in us]
    ents.append({"id": "overlap", "name": "the shared atlas (overlap)", "aliases": ["overlap", "shared stacks"],
                 "anchor": "[data-ref='overlap']"})
    ents.append({"id": "hover-pair", "name": "the semi-additive burn (hover pair)",
                 "aliases": ["hover", "the burn", "stock.sum vs stock.last"], "anchor": "[data-ref='hover-pair']"})
    return {"artifact": "universe-visual", "kind": "web", "entries": ents}


def main() -> int:
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    try:
        model = build_model(dm)
        fig = figure_svg(store, model)
        hover = hover_pair(store, model)
    except Fail as e:
        print(f"universe-visual generation FAILED (fail-closed): {e}", file=sys.stderr)
        return 1
    if hover is None:
        print("universe-visual generation FAILED — no semi-additive burn found to teach the hover",
              file=sys.stderr)
        return 1
    a = sorted(model["universes"], key=lambda u: -len(u["base_dimensions"]))[0]
    hover_intro = COPY["hover_intro"].format(measure=hover["measure"], stack=hover["stack"])
    out = {
        "generated_by": f"columna-core {version('columna-core')} / columna-server {version('columna-server')}",
        "manifold": MID,
        "figure_svg": fig,
        "hover": {**hover, "intro": hover_intro,
                  "barred_caption": COPY["hover_barred"].format(stack=hover["stack"]),
                  "travels_caption": COPY["hover_travels"]},
        "copy": {"kicker": COPY["kicker"], "title": COPY["title"], "lede": COPY["lede"],
                 "leftout": COPY["leftout"], "leftout_spec_route": COPY["leftout_spec_route"],
                 "leftout_map_route": COPY["leftout_map_route"]},
        "referents": _referents(model),
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
