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

# ── ratified CAPTIONS. PROSE only — never element labels. The main caption is the THREE-UNIVERSE
#    redesign (founder's ruling, Huayin 2026-07-24): multi-universe is foundational, so all three
#    universes get identical first-class treatment; the edge grammar (solid = functional M:1, dotted =
#    the product↔category frontier) carries the entire distinction, and the three faces ride ON the
#    dotted edge as the licensed passages that govern it. Caption is DRAFT until Huayin's word. ──
COPY = {
    "kicker": "THE UNIVERSE VISUAL · FIGURE 1",
    "title": "Cascadia — three universes",
    # DRAFT caption (Huayin ratifies with his word) — verbatim from the founder's ruling.
    "caption": ("Cascadia's manifold: three universes — transaction (events), inventory (spine), and "
                "category_profile (spine), whose measures license the category crossing. Solid edges "
                "are functional paths; the dotted edge is the product↔category frontier, crossable "
                "only through its three declared faces."),
    "lede": ("Universe-first, and multi-universe as foundational: each population is a first-class "
             "block holding its basis and its metric families. The edges carry the distinction — solid "
             "hops are functional (many-to-one) paths; the one dotted edge is the product↔category "
             "frontier, crossed only through its three declared faces. Labels are verbatim from describe."),
    "fork_note": "weeks don't nest — the fork",
    "frontier_note": "product ↔ category — the frontier (non-functional; M:N)",
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
    "legend": [("swatch", SERVE, "✓ functional hop (M:1, serve)"),
               ("box", UNTEST_BG, "untestable basis"),
               ("dash", REFUSE, "the product↔category frontier"),
               ("chip", REFUSE, "a declared face + its driver")],
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


def resolve_roles(model):
    """THREE-UNIVERSE redesign (founder's ruling, Huayin 2026-07-24). Identify each universe's role from
    the wire — never by name — so the figure is auto-true, and FAIL CLOSED on anything the layout is not
    taught. The layout is taught for exactly: three universes, one M:N frontier relate, whose `frm` and
    `to` levels are the base of two DISTINCT universes; the third universe is functionally linked (shares
    a base dim) to the frontier's home. Roles:
      • home    — the universe whose base holds the frontier's `frm` (product) level;
      • profile — the universe whose base holds the frontier's `to` (category) level; its measures drive faces;
      • third   — the remaining universe (inventory), functionally sharing base dims with home.
    Every face driver (if present) must be a measure of the profile universe (subfield completeness —
    a driver on the wire the figure can't ground fails the deploy).
    """
    us = model["universes"]
    if len(us) != 3:
        raise Fail(f"the figure is taught for exactly three universes; got {len(us)} — teach the layout")
    relates = model["relates"]
    if len(relates) != 1:
        raise Fail(f"the figure is taught for exactly one frontier relate; got {len(relates)} — teach it")
    r = relates[0]

    def base_of(level):
        found = [u for u in us if level in u["base_dimensions"]]
        return found[0] if len(found) == 1 else None

    home = base_of(r["frm"])
    profile = base_of(r["to"])
    if home is None or profile is None:
        raise Fail(f"frontier {r['frm']}->{r['to']} does not resolve to exactly one home + one profile "
                   f"universe — teach the layout")
    if home is profile:
        raise Fail(f"frontier {r['frm']}->{r['to']} lands both ends in one universe — not a crossing")
    others = [u for u in us if u is not home and u is not profile]
    if len(others) != 1:
        raise Fail("the figure is taught for exactly one third (functional) universe — teach the layout")
    third = others[0]
    if not (set(third["base_dimensions"]) & set(home["base_dimensions"])):
        raise Fail(f"third universe {third['name']!r} shares no base dimension with the home universe — "
                   f"the taught layout expects a functional link; teach it")
    # every declared face driver must be a measure of the profile universe (subfield completeness)
    profile_measures = {m["name"] for m in model["measures"] if m["universe"] == profile["name"]}
    for f in r.get("faces", []):
        d = f.get("driver")
        if d is not None and d not in profile_measures:
            raise Fail(f"face {f['name']!r} names driver {d!r}, not a measure of the profile universe "
                       f"{profile['name']!r} — the figure cannot ground it (subfield-completeness wedge)")
    return {"home": home, "profile": profile, "third": third, "relate": r}


# ───────────────────────────── the main figure (three universes) ─────────────────────────────
def figure_svg(store, model, roles):
    """Compose the THREE-UNIVERSE figure (founder's ruling, Huayin 2026-07-24): multi-universe is
    foundational, so all three universes get identical first-class treatment (solid-bordered cards).
    The EDGE GRAMMAR carries the entire distinction — solid = corroborated functional (M:1) hops; the
    single DOTTED edge = the product<->category frontier, crossed only by its three declared FACES,
    drawn as chips ON the edge. DRIVER ARROWS run from the profile universe's measures into the faces
    they power. Labels verbatim from describe; the caption is ratified prose (rendered by the page)."""
    home, profile, third = roles["home"], roles["profile"], roles["third"]
    r = roles["relate"]
    faces = r.get("faces", [])

    W, H = 1180, 772
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="Cascadia manifold, three first-class universes {esc(home["name"])}, '
             f'{esc(third["name"])}, {esc(profile["name"])}; solid functional edges and the dotted '
             f'{esc(r["frm"])} to {esc(r["to"])} frontier crossed by declared faces '
             f'{esc(", ".join(f["name"] for f in faces))}">']
    parts.append(
        '<defs>'
        f'<marker id="dhead" markerWidth="9" markerHeight="9" refX="6.5" refY="4.5" orient="auto">'
        f'<path d="M0,1 L8,4.5 L0,8 Z" fill="{VERIFIED}"/></marker>'
        '</defs>')

    CARD_Y, CARD_H = 44, 300
    home_x, home_w = 32, 372
    third_x, third_w = 428, 270
    prof_x, prof_w = 740, 300

    def _mline(x, yy, m):
        return (_t(x, yy, esc(m["name"]) + " ", 13, INK, cls="mono")
                + _t(x + _tw(m["name"]) + 8, yy, f'[{esc(" · ".join(m["family"]))}]', 13, FAINT, cls="mono"))

    def _card(u, x, w, drivers=False):
        g = [f'<g data-ref="universe-{esc(u["name"])}">']
        g.append(_rect(x, CARD_Y, w, CARD_H, rx=14, fill=PAPER, stroke=RULE, sw=1.7))   # solid = first-class
        g.append(_t(x + 18, CARD_Y + 30, esc(u["name"]), 18, INK, weight=700))
        g.append(_t(x + 18, CARD_Y + 48, f'BASIS {esc(u["basis"])}', 12, SUB, cls="mono"))
        g.append(_rect(x + w - 90, CARD_Y + 14, 76, 19, rx=10, fill=UNTEST_BG))
        g.append(_t(x + w - 52, CARD_Y + 27, "untestable", 10.5, UNTEST, anchor="middle", cls="tag"))
        absc = _absence_short(u)
        if absc:
            g.append(_t(x + 18, CARD_Y + 66, esc(absc), 11, FAINT))
        g.append(_t(x + 18, CARD_Y + 82, "base " + esc(" · ".join(u["base_dimensions"])), 10.5, FAINT, cls="mono"))
        if u.get("predicate"):
            g.append(_t(x + 18, CARD_Y + 98, "carve " + esc(u["predicate"]), 10.5, SUB, cls="mono"))
        ms = [m for m in model["measures"] if m["universe"] == u["name"]]
        my = CARD_Y + 122
        g.append(_t(x + 18, my, "MEASURE" + ("S" if len(ms) != 1 else ""), 11, SUB, cls="tag"))
        anchors = {}
        my += 24
        for m in ms:
            g.append(_mline(x + 18, my, m))
            if drivers:
                anchors[m["name"]] = (x + 18 + _tw(m["name"] + " ") + _tw(" · ".join(m["family"])) + 30, my - 4)
            my += 24
        if _is_semi_additive(store, u, model):
            g.append(_t(x + 18, my + 4, "semi-additive — sum barred over", 10.5, FAINT))
            g.append(_t(x + 18, my + 17, "calendar; last travels (see below)", 10.5, FAINT))
            my += 30
        # home: the corroborated ASSERT chip, seated at the card foot
        for asrt in model["asserts"]:
            if asrt["universe"] != u["name"]:
                continue
            v = (asrt.get("license") or {}).get("verdict")
            g.append(_plaque(x + 18, CARD_Y + CARD_H - 40, asrt, v))
        g.append('</g>')
        return g, anchors

    g_home, _ = _card(home, home_x, home_w)
    g_third, _ = _card(third, third_x, third_w)
    g_prof, driver_anchor = _card(profile, prof_x, prof_w, drivers=True)
    parts += g_home + g_third + g_prof

    # ── the ATLAS: base levels + solid functional (M:1) stacks + the dotted frontier ──
    FRONTIER_Y = 396
    BASE_Y = 488
    floor_cx = {}

    frm_cx, to_cx = 250, 980
    for lvl, cx in ((r["frm"], frm_cx), (r["to"], to_cx)):
        floor_cx[lvl] = cx
        parts.append(_level_block(cx, FRONTIER_Y - 15, lvl, w=104, h=30, stroke=INK))

    shared_dims = [d for d in home["base_dimensions"]
                   if d in third["base_dimensions"] and d not in (r["frm"], r["to"])]
    own_dims = [d for d in home["base_dimensions"]
                if d not in shared_dims and d not in (r["frm"], r["to"])]
    x = 110
    for d in own_dims:
        floor_cx[d] = x
        parts.append(_level_block(x, BASE_Y, d, w=96, h=30))
        x += 118
    if shared_dims:
        sh_x0 = 392
        parts.append(_t(sh_x0, BASE_Y - 16, "shared · " + esc(home["name"]) + " + " + esc(third["name"]),
                        10, FAINT))
        for i, d in enumerate(shared_dims):
            cx = sh_x0 + 42 + i * 132
            floor_cx[d] = cx
            parts.append(_level_block(cx, BASE_Y, d, w=96, h=30, stroke=INK))

    # solid functional stacks (corroborated ✓) descending from each rooted base level
    PITCH, RH, RW = 68, 28, 90
    for h in model["hierarchies"]:
        chain = h.get("chain") or []
        base = chain[0] if chain else None
        if base not in floor_cx:
            continue
        v = (h.get("license") or {}).get("verdict")
        color = VERDICT_COLOR.get(v, SERVE)
        cx = floor_cx[base]
        prev = BASE_Y + 30
        for i, lvl in enumerate(chain[1:]):
            by = BASE_Y + (i + 1) * PITCH
            parts.append(_line(cx, prev, cx, by, stroke=color, sw=1.6))
            parts.append(_check(cx - 48, (prev + by) / 2, color))
            parts.append(_level_block(cx, by, lvl, w=RW))
            prev = by + RH
        for path in h.get("paths", []):
            if path == chain or len(path) < 2 or path[0] != base:
                continue
            fx = cx - 128
            for j, lvl in enumerate(path[1:]):
                fy = BASE_Y + (j + 1) * PITCH
                parts.append(_line(cx - RW / 2 + 6, BASE_Y + 34, fx + 40, fy + RH / 2, stroke=color, sw=1.3))
                parts.append(_level_block(fx, fy, lvl, w=84))
            parts.append(_t(fx, BASE_Y + PITCH + 46, COPY["fork_note"], 9.5, FAINT, anchor="middle"))

    # ── the DOTTED frontier edge with the FACE chips ON it ──
    fy = FRONTIER_Y
    parts.append(_line(frm_cx + 54, fy, to_cx - 54, fy, stroke=REFUSE, sw=1.7, dash="2 5"))
    note_cx = frm_cx + 110                                    # over the product→touch segment, clear of chips/arrows
    parts.append(_t(note_cx, fy - 44, COPY["frontier_note"], 10.5, REFUSE, anchor="middle"))
    if r.get("note"):
        parts.append(_t(note_cx, fy - 30, esc(r["note"]), 10, FAINT, anchor="middle"))

    n = max(len(faces), 1)
    span0, span1 = frm_cx + 120, to_cx - 120
    for i, f in enumerate(faces):
        cx = span0 + (span1 - span0) * ((i + 0.5) / n)
        name = f["name"]
        cw = _tw(name, 7.6) + 28
        parts.append(f'<g data-ref="face-{esc(name)}"><title>{esc(f["description"])}</title>')
        parts.append(_rect(cx - cw / 2, fy - 14, cw, 28, rx=14, fill=PAPER, stroke=REFUSE, sw=1.5))
        parts.append(_t(cx, fy + 4, esc(name), 13, REFUSE, anchor="middle", weight=600, cls="mono"))
        parts.append('</g>')
        d = f.get("driver")
        if d and d in driver_anchor:
            sx, sy = driver_anchor[d]
            parts.append(f'<g data-ref="driver-{esc(d)}-{esc(name)}"><title>{esc(d)} drives {esc(name)}</title>')
            parts.append(f'<path d="M {sx} {sy} C {sx} {sy + 54}, {cx} {fy - 66}, {cx} {fy - 14}" '
                         f'fill="none" stroke="{VERIFIED}" stroke-width="1.3" marker-end="url(#dhead)"/>')
            parts.append(_t((sx + cx) / 2 + 4, (sy + fy) / 2 - 4, "drives", 9, VERIFIED, cls="tag"))
            parts.append('</g>')

    parts.append(_legend(28, H - 34))
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
            out.append(_check(cx + 6, y - 3, color))
            cx += 6
        elif kind == "box":
            out.append(_rect(cx, y - 9, 13, 13, rx=2, fill=color, stroke=UNTEST, sw=1))
        elif kind == "dash":                       # the dotted frontier edge
            out.append(_line(cx, y - 3, cx + 15, y - 3, stroke=color, sw=1.6, dash="2 4"))
        elif kind == "chip":                       # a declared face (pill)
            out.append(_rect(cx, y - 10, 16, 15, rx=7, fill=PAPER, stroke=color, sw=1.3))
        out.append(_t(cx + 22, y, label, 11, SUB))
        cx += 32 + _tw(label, 6.2)
    out.append('</g>')
    return "".join(out)


# ───────────────────────── describe-derived predicates ─────────────────────────
def _tw(s, per=7.4):
    return len(str(s)) * per


def _wrap(s, width):
    """Greedy word-wrap into lines of at most `width` chars (SVG <text> does not wrap). Used for the
    describe-verbatim face description caption — kept whole, only line-broken."""
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


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


def _referents(model, roles):
    us = sorted(model["universes"], key=lambda u: -len(u["base_dimensions"]))
    ents = [{"id": f"universe-{u['name']}", "name": f"{u['name']} universe",
             "aliases": [u["name"]], "anchor": f"[data-ref='universe-{u['name']}']"} for u in us]
    r = roles["relate"]
    ents.append({"id": "frontier", "name": f"the {r['frm']}↔{r['to']} frontier (dotted edge)",
                 "aliases": ["the frontier", "the dotted edge", "the crossing",
                             f"{r['frm']} to {r['to']}"], "anchor": "[data-ref='face-touch']"})
    for f in r.get("faces", []):
        aliases = [f["name"], f"the {f['name']} face"]
        if f.get("driver"):
            aliases.append(f"{f['name']} (driven by {f['driver']})")
        ents.append({"id": f"face-{f['name']}", "name": f"the {f['name']} face",
                     "aliases": aliases, "anchor": f"[data-ref='face-{f['name']}']"})
    ents.append({"id": "hover-pair", "name": "the semi-additive burn (hover pair)",
                 "aliases": ["hover", "the burn", "stock.sum vs stock.last"], "anchor": "[data-ref='hover-pair']"})
    return {"artifact": "universe-visual", "kind": "web", "entries": ents}


def main() -> int:
    store = demo_store()
    dm = T.describe_manifold(store, MID)
    try:
        model = build_model(dm)
        roles = resolve_roles(model)                    # three-universe layout; fails closed on any other shape
        fig = figure_svg(store, model, roles)
        # FAIL-CLOSED SUBFIELD COMPLETENESS (post-flip defect, 2026-07-19). The wedge's LETTER checked the
        # relates KEY was present (build_model); its SPIRIT — "every declared crossing is ON the figure" —
        # was unenforced, so faces[] shipped to the describe wire and never reached the SVG (the defect this
        # PR fixes). Extend the wedge one field deeper: every faces[] entry on the wire (name + verbatim
        # description) must appear in the generated figure, or the deploy fails closed.
        for r in model["relates"]:
            for f in r.get("faces", []):
                if f["name"] not in fig or esc(f["description"]) not in fig:
                    raise Fail(f"relate {r['frm']}->{r['to']} face '{f['name']}' is on the describe wire but "
                               f"absent from the figure — the construction law must render every declared "
                               f"crossing (subfield-completeness wedge)")
        hover = hover_pair(store, model)
    except Fail as e:
        print(f"universe-visual generation FAILED (fail-closed): {e}", file=sys.stderr)
        return 1
    if hover is None:
        print("universe-visual generation FAILED — no semi-additive burn found to teach the hover",
              file=sys.stderr)
        return 1
    hover_intro = COPY["hover_intro"].format(measure=hover["measure"], stack=hover["stack"])
    copy = {"kicker": COPY["kicker"], "title": COPY["title"], "caption": COPY["caption"],
            "lede": COPY["lede"], "leftout": COPY["leftout"],
            "leftout_spec_route": COPY["leftout_spec_route"],
            "leftout_map_route": COPY["leftout_map_route"]}
    out = {
        "generated_by": f"columna-core {version('columna-core')} / columna-server {version('columna-server')}",
        "manifold": MID,
        "figure_svg": fig,
        "hover": {**hover, "intro": hover_intro,
                  "barred_caption": COPY["hover_barred"].format(stack=hover["stack"]),
                  "travels_caption": COPY["hover_travels"]},
        "copy": copy,
        "referents": _referents(model, roles),
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
