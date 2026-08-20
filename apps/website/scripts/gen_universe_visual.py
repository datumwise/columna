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
BASE = "#3f6d8c"; BASE_BG = "#eaf1f6"      # the block's anchor fact — the base line reads as one (v5)

VERDICT_COLOR = {"corroborated": SERVE, "verified": VERIFIED, "disclose": DISCLOSE,
                 "contradicted": REFUSE, "untestable": UNTEST}
VERDICT_BG = {"corroborated": SERVE_BG, "verified": "#eef1fb", "untestable": UNTEST_BG}

# ── ratified CAPTIONS. PROSE only — never element labels. The main caption is the THREE-UNIVERSE
#    redesign (founder's ruling, Huayin 2026-07-24): multi-universe is foundational, so all three
#    universes get identical first-class treatment; the edge grammar (solid = functional M:1, dotted =
#    the product↔category frontier) carries the entire distinction, and the three faces ride ON the
#    dotted edge as the licensed passages that govern it. Caption is RATIFIED (see below). ──
COPY = {
    "kicker": "THE UNIVERSE VISUAL · FIGURE 1",
    "title": "Cascadia — three universes",
    # CAPTION v5 — RATIFIED (Huayin, the five-in-one word, 2026-07-24); supersedes v3.
    # It is also the source of Figure 1's bracketed text equivalent in llms-full (read, never
    # retyped), so edits here change what agent readers get — keep it and the figure in step.
    "caption": ("Cascadia's manifold: three universes. Each block shows its base (colored) and the "
                "grains its solid, functional edges reach; '=' links shared declarations — store, day, "
                "and category — across universes. The dotted product↔category edge inside transaction "
                "is the frontier: an M:N reach, not a functional grain, servable only through its three "
                "declared faces, whose drivers live in category_profile."),
    "identity_note": "one declared level, two presences — the '=' marks the shared-atlas declaration",
    "identity_note_conformance": ("one declared level, two presences — the '=' marks the shared-atlas "
                                   "declaration. Occurrences must conform to members — adjudication dated, rides OF-5."),
    "presence_note": ("category appears here through the M:N bridge — an occurrence presence, not a "
                      "functional grain; servable only through a declared face"),
    "bridge_label": "product_categories(product_id, category_id)",
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
    # `/case#map` never existed: /case carries ch1/ch2/ch3 only, and the physical->logical map is
    # taught inside CHAPTER 2 (verified against the built page). The caption promised an address the
    # site does not have — caught by scripts/check_fragments.mjs, which now fails the build on any
    # unresolvable internal fragment.
    "leftout_map_route": "/case#ch2",         # the chapter that holds the physical->logical map
    # the CLOSED edge grammar (v5, Huayin 2026-07-24): solid = functional hop IN-BOX; dotted = the M:N
    # frontier reach IN-BOX (faces mandatory); "=" = declared identity ACROSS boxes. Cross-box lines are
    # "=" only. (Driver arrows are a separate binding annotation, not a structural edge class.)
    "legend": [("swatch", SERVE, "solid → = functional hop, in a universe (M:1)"),
               ("dash", REFUSE, "· · · the M:N frontier reach, in-box (faces mandatory)"),
               ("eq", VERIFIED, "= declared identity across universes"),
               ("base", BASE, "the block's base (anchor)")],
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
    # ASSERT retired in 0.13 (ruling 2026-07-26); describe no longer emits an `asserts` field.
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
    return {"universes": universes, "hierarchies": hiers, "measures": measures,
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
    # CLOSED EDGE GRAMMAR (Huayin 2026-07-24): every wire edge must classify as exactly one known class —
    # FUNCTIONAL (a hop inside one universe's declared hierarchy), IDENTITY (a base level shared across
    # universes, derived), or FRONTIER (the relate). Any edge the generator can't place in this closed
    # grammar refuses to render (absence of a line must mean absence of a passage). Functional edges are
    # dm['edges']; each must belong to a declared hierarchy lineage — else it is an untaught inter-level
    # class and the figure fails closed rather than drawing a line whose meaning it doesn't know.
    hier_pairs = set()
    for h in model["hierarchies"]:
        for path in [h.get("chain") or []] + h.get("paths", []):
            for a, b in zip(path, path[1:]):
                hier_pairs.add((a, b))
    for e in model.get("edges", []):
        if (e["frm"], e["to"]) not in hier_pairs:
            raise Fail(f"edge {e['frm']}->{e['to']} is not a declared functional hierarchy hop and is "
                       f"neither the frontier nor an identity seam — an unknown edge class the closed "
                       f"grammar refuses to render; teach it")
    return {"home": home, "profile": profile, "third": third, "relate": r,
            "shared_levels": sorted({d for u in us for d in u["base_dimensions"]
                                     if sum(d in v["base_dimensions"] for v in us) > 1})}


# ───────────────────────────── the main figure (three universes, v5) ─────────────────────────────
def figure_svg(store, model, roles):
    """Compose the THREE-UNIVERSE figure (founder's ruling v5, Huayin 2026-07-24, after live review).

    Block order inventory | transaction | category_profile. Each block shows its BASE (colored — the
    block's anchor fact) and the grains its solid functional (M:1) edges reach. The FRONTIER is now
    IN-BOX: inside transaction, `product` reaches a `category` PRESENCE chip by a dotted M:N edge that
    the three declared faces ride (the product_categories bridge labels it); the presence wears distinct
    styling — an occurrence, not a functional grain. The CLOSED edge grammar: solid = functional hop
    in-box; dotted = the M:N frontier reach in-box (faces mandatory); "=" = declared identity ACROSS
    boxes — and cross-box lines are "=" ONLY. store, day, and category are the shared declarations
    (category's "=" links transaction's presence to category_profile's base, carrying the dated
    occurrence-conformance note). Driver arrows (a binding annotation, not a structural edge) run from
    category_profile's measures to the faces. Labels verbatim from describe; caption is ratified prose."""
    home, profile, third = roles["home"], roles["profile"], roles["third"]
    r = roles["relate"]
    faces = r.get("faces", [])
    shared = [lvl for lvl in roles.get("shared_levels", [])]     # store, day

    W, H = 1160, 560
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="Cascadia manifold, three universes {esc(third["name"])}, {esc(home["name"])}, '
             f'{esc(profile["name"])}; store, day and category are shared declarations linked by = identity '
             f'edges; the dotted {esc(r["frm"])} to {esc(r["to"])} M:N frontier lives inside {esc(home["name"])} '
             f'and is crossed only by faces {esc(", ".join(f["name"] for f in faces))}">']
    parts.append(
        '<defs>'
        f'<marker id="dhead" markerWidth="9" markerHeight="9" refX="6.5" refY="4.5" orient="auto">'
        f'<path d="M0,1 L8,4.5 L0,8 Z" fill="{VERIFIED}"/></marker></defs>')

    CARD_Y, CARD_H = 36, 400
    inv_x, inv_w = 32, 232
    txn_x, txn_w = 304, 486
    cp_x, cp_w = 830, 300
    day_y, store_y = 300, 336        # the store/day "=" band
    frontier_y = 402                 # the in-box frontier + the category "=" band

    def _mline(x, yy, m):
        return (_t(x, yy, esc(m["name"]) + " ", 13, INK, cls="mono")
                + _t(x + _tw(m["name"]) + 8, yy, f'[{esc(" · ".join(m["family"]))}]', 13, FAINT, cls="mono"))

    def _header(u, x, w):
        g = [_rect(x, CARD_Y, w, CARD_H, rx=14, fill=PAPER, stroke=RULE, sw=1.7),
             _t(x + 18, CARD_Y + 30, esc(u["name"]), 18, INK, weight=700),
             _t(x + 18, CARD_Y + 48, f'BASIS {esc(u["basis"])}', 12, SUB, cls="mono"),
             _rect(x + w - 90, CARD_Y + 14, 76, 19, rx=10, fill=UNTEST_BG),
             _t(x + w - 52, CARD_Y + 27, "untestable", 10.5, UNTEST, anchor="middle", cls="tag")]
        absc = _absence_short(u)
        hy = CARD_Y + 66
        if absc:
            g.append(_t(x + 18, hy, esc(absc), 11, FAINT)); hy += 16
        if u.get("predicate"):
            g.append(_t(x + 18, hy, "carve " + esc(u["predicate"]), 10.5, SUB, cls="mono")); hy += 16
        # the BASE line — colored, one anchor fact, consistent across all blocks (v5 item 1)
        g.append(_rect(x + 14, hy - 12, _tw("base: " + " · ".join(u["base_dimensions"]), 6.6) + 20, 18,
                       rx=4, fill=BASE_BG))
        g.append(_t(x + 18, hy, "base: ", 11, BASE, weight=700, cls="mono")
                 + _t(x + 18 + _tw("base: ", 6.6), hy, esc(" · ".join(u["base_dimensions"])), 11, BASE, cls="mono"))
        return g, hy + 20

    def _measures(u, x, my, drivers=False):
        ms = [m for m in model["measures"] if m["universe"] == u["name"]]
        g = [_t(x + 18, my, "MEASURE" + ("S" if len(ms) != 1 else ""), 11, SUB, cls="tag")]
        anchors = {}
        yy = my + 22
        for m in ms:
            g.append(_mline(x + 18, yy, m))
            if drivers:
                anchors[m["name"]] = (x + 18 + _tw(m["name"] + " ") + _tw(" · ".join(m["family"])) + 24, yy - 4)
            yy += 22
        return g, anchors, yy

    def _shared_pair(x, side):
        """the day/store GRAINS presences (the "=" anchors) at a box's facing edge."""
        g, anch = [], {}
        cx = (x - 58) if side == "left" else (x + 58)        # x is the facing inner edge
        g.append(_t(cx, min(day_y, store_y) - 27, "GRAINS", 10, SUB, anchor="middle", cls="tag"))
        for lvl, cy in (("day", day_y), ("store", store_y)):
            if lvl not in shared:
                continue
            g.append(f'<g data-ref="grain-{esc(lvl)}"><title>{esc(COPY["identity_note"])}</title>'
                     + _level_block(cx, cy - 15, lvl, w=84, h=30, stroke=INK) + '</g>')
            anch[lvl] = ((cx + 43) if side == "left" else (cx - 43), cy)   # face the gap, not the far edge
        return g, anch

    # ── inventory (left) ──
    gi, hy_i = _header(third, inv_x, inv_w)
    gm_i, _, _ = _measures(third, inv_x, hy_i)
    gs_i, sa_inv = _shared_pair(inv_x + inv_w, "left")        # facing edge = right side of inventory
    gi += gm_i + gs_i
    names = ", ".join(sorted({h["lineage"] for h in model["hierarchies"]
                              if (h.get("chain") or [None])[0] in third["base_dimensions"]}))
    gi.append(_t(inv_x + 18, frontier_y - 6, f"functional grains: {esc(names)} ✓", 9.5, FAINT))
    gi.append(_t(inv_x + 18, frontier_y + 8, f"identical to {esc(home['name'])} — see the = edges", 9.5, FAINT))
    parts += [f'<g data-ref="universe-{esc(third["name"])}">'] + gi + ['</g>']

    # ── transaction (centre) — holds the in-box frontier ──
    gt, hy_t = _header(home, txn_x, txn_w)
    gm_t, _, my_end_t = _measures(home, txn_x, hy_t)
    gs_t, sa_txn = _shared_pair(txn_x, "right")              # facing edge = left side of transaction
    gt += gm_t + gs_t
    # functional-grain breadcrumbs (the reached grains) — beside the measures (upper-right of the block)
    bx0 = txn_x + 180
    gt.append(_t(bx0, hy_t, "functional grains — ▸ = corroborated M:1 hop", 9.5, FAINT))
    hi = 0
    for h in model["hierarchies"]:
        chain = h.get("chain") or []
        if chain[0] not in home["base_dimensions"]:
            continue
        col = VERDICT_COLOR.get((h.get("license") or {}).get("verdict"), SERVE)
        yb = hy_t + 22 + hi * 22
        crumb = " ▸ ".join(chain)
        gt.append(_t(bx0, yb, esc(crumb), 10.5, INK, cls="mono") + _t(bx0 + _tw(crumb, 6.3) + 6, yb, "✓", 10.5, col))
        for pth in h.get("paths", []):
            extra = [lv for lv in (pth or []) if lv not in chain]
            if extra:
                gt.append(_t(bx0 + _tw(crumb, 6.3) + 20, yb, "· " + esc(" ".join(extra)), 9.5, FAINT))
        hi += 1
    # the IN-BOX frontier: product → dotted M:N edge → category PRESENCE, faces riding it
    fx_prod = txn_x + 70
    fx_pres = txn_x + txn_w - 66
    gt.append(_t(fx_prod - 8, frontier_y - 26, "FRONTIER — the M:N reach (in-box)", 9, REFUSE, cls="tag"))
    gt.append(_level_block(fx_prod, frontier_y - 15, r["frm"], w=_tw(r["frm"], 7.4) + 30, h=30, stroke=INK))
    # the presence chip (distinct styling: dashed frontier border + tint) + hover
    presw = _tw(r["to"], 7.4) + 34
    gt.append(f'<g data-ref="presence-{esc(r["to"])}"><title>{esc(COPY["presence_note"])}</title>')
    gt.append(_rect(fx_pres - presw / 2, frontier_y - 15, presw, 30, rx=5, fill="#fbeeee", stroke=REFUSE, sw=1.5, dash="4 3"))
    gt.append(_t(fx_pres, frontier_y + 5, esc(r["to"]), 12.5, REFUSE, anchor="middle", cls="mono"))
    gt.append(_t(fx_pres, frontier_y - 21, "presence", 8.5, REFUSE, anchor="middle", cls="tag"))
    gt.append('</g>')
    # the dotted edge product→presence + the bridge label riding it
    gt.append(_line(fx_prod + _tw(r["frm"], 7.4) / 2 + 18, frontier_y, fx_pres - presw / 2 - 4, frontier_y,
                    stroke=REFUSE, sw=1.7, dash="2 5"))
    gt.append(_t((fx_prod + fx_pres) / 2, frontier_y + 20, COPY["bridge_label"], 9.5, FAINT, anchor="middle", cls="mono"))
    # the three face chips ON the dotted edge
    face_cx = {}
    n = max(len(faces), 1)
    span0, span1 = fx_prod + 66, fx_pres - 70
    for i, f in enumerate(faces):
        fx = span0 + (span1 - span0) * ((i + 0.5) / n)
        face_cx[f["name"]] = fx
        cw = _tw(f["name"], 7.6) + 26
        gt.append(f'<g data-ref="face-{esc(f["name"])}"><title>{esc(f["description"])}</title>')
        gt.append(_rect(fx - cw / 2, frontier_y - 13, cw, 26, rx=13, fill=PAPER, stroke=REFUSE, sw=1.5))
        gt.append(_t(fx, frontier_y + 4, esc(f["name"]), 12.5, REFUSE, anchor="middle", weight=600, cls="mono"))
        gt.append('</g>')
    parts += [f'<g data-ref="universe-{esc(home["name"])}">'] + gt + ['</g>']

    # ── category_profile (right) ──
    gc, hy_c = _header(profile, cp_x, cp_w)
    gm_c, driver_anchor, _ = _measures(profile, cp_x, hy_c, drivers=True)
    gc += gm_c
    # the category BASE chip (its anchor grain), facing transaction for the "=" edge
    cat_cx = cp_x + 62
    gc.append(f'<g data-ref="base-{esc(r["to"])}">'
              + _level_block(cat_cx, frontier_y - 15, r["to"], w=_tw(r["to"], 7.4) + 30, h=30, stroke=INK)
              + _t(cat_cx, frontier_y - 21, "base", 8.5, BASE, anchor="middle", cls="tag") + '</g>')
    parts += [f'<g data-ref="universe-{esc(profile["name"])}">'] + gc + ['</g>']

    # ── the "=" identity edges (the ONLY cross-box lines) ──
    def _eq(x1, x2, y, note, lvl):
        mx = (x1 + x2) / 2
        return (f'<g data-ref="identity-{esc(lvl)}"><title>{esc(note)}</title>'
                + _line(x1, y - 3, x2, y - 3, stroke=VERIFIED, sw=1.5)
                + _line(x1, y + 3, x2, y + 3, stroke=VERIFIED, sw=1.5)
                + _t(mx, y - 8, "=", 15, VERIFIED, anchor="middle", weight=700) + '</g>')
    for lvl in shared:
        if lvl in sa_inv and lvl in sa_txn:
            parts.append(_eq(sa_inv[lvl][0], sa_txn[lvl][0], sa_inv[lvl][1], COPY["identity_note"], lvl))
    # category: transaction's presence = category_profile's base (with the dated conformance note)
    parts.append(_eq(fx_pres + presw / 2 + 3, cat_cx - (_tw(r["to"], 7.4) + 30) / 2 - 3, frontier_y,
                     COPY["identity_note_conformance"], r["to"]))

    # ── driver arrows (binding annotation): profile measures → the faces they power ──
    for f in faces:
        d = f.get("driver")
        if d and d in driver_anchor and f["name"] in face_cx:
            sx, sy = driver_anchor[d]
            fx = face_cx[f["name"]]
            parts.append(f'<g data-ref="driver-{esc(d)}-{esc(f["name"])}"><title>{esc(d)} drives {esc(f["name"])}</title>')
            parts.append(f'<path d="M {sx} {sy} C {sx - 40} {sy + 90}, {fx + 30} {frontier_y - 90}, {fx} {frontier_y - 13}" '
                         f'fill="none" stroke="{VERIFIED}" stroke-width="1.2" marker-end="url(#dhead)" opacity="0.8"/>')
            parts.append('</g>')
    # note the driver descriptions are wire-sourced; empty until the manifold carries them (companion PR)

    parts.append(_legend(28, H - 26))
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
        elif kind == "eq":                         # the "=" identity edge
            out.append(_line(cx, y - 6, cx + 15, y - 6, stroke=color, sw=1.4))
            out.append(_line(cx, y, cx + 15, y, stroke=color, sw=1.4))
        elif kind == "chip":                       # a declared face (pill)
            out.append(_rect(cx, y - 10, 16, 15, rx=7, fill=PAPER, stroke=color, sw=1.3))
        elif kind == "base":                       # the colored base line
            out.append(_t(cx, y, "base:", 11, color, weight=700, cls="mono"))
            cx += _tw("base:", 6.4) - 22
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


# ───────────────────────────── the HERO preset (homepage v2, Group 3) ─────────────────────────────
def hero_svg(model, roles):
    """A simplified, line-art HERO variant of the manifold, from the SAME model as figure_svg — so the
    hero cannot drift from the shipped package (art direction §1). Ink-only, hairline strokes, no fill,
    no colour: three universe blocks (name + basis only — no measure lists, no grain breadcrumbs, no
    caption v5), the `=` identity seams, and the dotted frontier with its face chips. Everything is read
    from the wire; nothing is hard-coded, so a package change redraws the hero.
    """
    home, profile, third = roles["home"], roles["profile"], roles["third"]
    r = roles["relate"]
    faces = [f["name"] for f in r.get("faces", [])]
    shared = roles["shared_levels"]                       # e.g. ['day', 'store'] — the identity seams

    W, H = 640, 440
    p = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="The Cascadia demo manifold: three universes — %s, %s and %s — with = identity '
         'seams on %s and a dotted %s to %s frontier crossed through the %s faces.">'
         % (W, H, home["name"], third["name"], profile["name"], " and ".join(shared),
            r["frm"], r["to"], ", ".join(faces))]

    def block(x, y, w, h, name, basis):
        # hairline outline, no fill; name in ink, basis small and quiet
        p.append(_rect(x, y, w, h, rx=0, fill="none", stroke=INK, sw=1))
        p.append(_t(x + w / 2, y + h / 2 - 2, name, size=15, fill=INK, weight="600", anchor="middle",
                    style="font-family:var(--font-mono, monospace)"))
        p.append(_t(x + w / 2, y + h / 2 + 16, "basis: " + basis, size=11, fill=SUB, anchor="middle"))

    # layout: home left-centre; third top-right (functional/identity); profile bottom-right (frontier).
    # Kept roomy so neither the identity seam nor the frontier chips crowd a block corner.
    hb = (36, 152, 196, 96)      # home
    tb = (444, 34, 168, 88)      # third
    pb = (444, 320, 168, 88)     # profile
    block(*hb, home["name"], home["basis"])
    block(*tb, third["name"], third["basis"])
    block(*pb, profile["name"], profile["basis"])

    # identity seams: home ↔ third, one `=` per shared level, labelled
    hx, hy = hb[0] + hb[2], hb[1] + 24           # right edge of home, upper
    tx, ty = tb[0], tb[1] + tb[3] / 2            # left edge of third
    p.append(_line(hx, hy, tx, ty, stroke=RULE, sw=1))
    mx, my = (hx + tx) / 2, (hy + ty) / 2
    p.append(_t(mx, my - 6, "=", size=17, fill=INK, weight="700", anchor="middle"))
    p.append(_t(mx, my + 13, " · ".join(shared), size=10, fill=FAINT, anchor="middle"))

    # the frontier: home ↔ profile, DOTTED, with face chips
    fx, fy = hb[0] + hb[2], hb[1] + hb[3] - 20    # right edge of home, lower
    px, py = pb[0], pb[1] + pb[3] / 2             # left edge of profile
    p.append(_line(fx, fy, px, py, stroke=INK, sw=1, dash="2 5"))
    # the frontier label sits above the line's midpoint, clear of the home block on its right side
    lmx, lmy = (fx + px) / 2, (fy + py) / 2
    p.append(_t(lmx + 8, lmy - 34, "%s ↔ %s" % (r["frm"], r["to"]),
                size=11, fill=SUB, anchor="middle", style="font-style:italic"))
    # face chips along the frontier, spread across its middle so none sits on a block corner
    n = len(faces)
    for i, name in enumerate(faces):
        t = 0.30 + (0.40 * (i / (n - 1))) if n > 1 else 0.5
        cx = fx + (px - fx) * t
        cy = fy + (py - fy) * t
        wch = _tw(name, per=6.5) + 14
        p.append(_rect(cx - wch / 2, cy - 9, wch, 18, rx=0, fill=PAPER, stroke=RULE, sw=1))
        p.append(_t(cx, cy + 4, name, size=10.5, fill=INK, anchor="middle",
                    style="font-family:var(--font-mono, monospace)"))

    p.append("</svg>")
    return "".join(p)


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
        "hero_svg": hero_svg(model, roles),
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
