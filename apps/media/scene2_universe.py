"""Scene 2 — The universe.

A predicate is written above (`day >= opened_date`, the real store_days predicate); a boundary
sweeps across the lattice and carves a region. Points inside glow; points outside dissolve to
nothing — not gray, *gone*. Caption: "A universe: the points that exist. Outside it, values
aren't missing - they're not defined."
"""
from __future__ import annotations

import numpy as np
from manim import (
    Scene,
    VGroup,
    VMobject,
    Line,
    FadeIn,
    FadeOut,
    Create,
    Write,
    RIGHT,
    LEFT,
    UP,
    DOWN,
)

import brand as B
import grid as G

# per-store staircase: how many early-day rows fall *outside* (day < opened_date) for each column.
# store_days' predicate is per-store (each store opened on a different date), so the frontier is a
# staircase, not a straight line — the truthful shape of `day >= opened_date`.
OUTSIDE_ROWS = [3, 2, 2, 1, 1, 1, 0, 0]


def _inside(i: int, j: int) -> bool:
    return j >= OUTSIDE_ROWS[i]


class Scene2Universe(Scene):
    def construct(self):
        gridlines = G.gridlines(color=B.GRID_DIM, stroke_width=1.0)
        dots = G.lattice()
        lattice = VGroup(*dots.values())

        # --- establish the coordinate space (continuity with Scene 1) ---
        self.play(FadeIn(gridlines, run_time=0.8), FadeIn(lattice, run_time=0.9, lag_ratio=0.004))
        self.wait(0.2)

        # --- the predicate, written above ---
        uni = B.label("universe  store_days", size=20, color=B.TEXT_SOFT)
        pred = B.label("day ≥ opened_date", size=34, color=B.COOL, mono=True)
        header = VGroup(uni, pred).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.6)
        self.play(Write(uni, run_time=0.6))
        self.play(Write(pred, run_time=0.9))
        self.wait(0.3)

        # --- the frontier: a staircase just below the lowest in-universe row of each column ---
        corners = []
        for i in range(G.NX):
            y = G.row_y(OUTSIDE_ROWS[i]) - G.DY / 2.0
            xl = G.col_x(i) - G.DX / 2.0
            xr = G.col_x(i) + G.DX / 2.0
            corners.append(np.array([xl, y, 0.0]))
            corners.append(np.array([xr, y, 0.0]))
        frontier = VMobject(stroke_color=B.COOL, stroke_width=3.0)
        frontier.set_points_as_corners(corners)

        # sweep the boundary across the grid (left -> right)
        self.play(Create(frontier, run_time=1.6))

        # --- carve: outside dissolves to nothing; inside glows; scaffolding recedes ---
        inside = [dots[(i, j)] for i in range(G.NX) for j in range(G.NY) if _inside(i, j)]
        outside = [dots[(i, j)] for i in range(G.NX) for j in range(G.NY) if not _inside(i, j)]

        self.play(
            gridlines.animate.set_stroke(opacity=0.28),
            *[d.animate.set_color(B.COOL).scale(1.25).set_opacity(1.0) for d in inside],
            *[d.animate.scale(0.1).set_opacity(0.0) for d in outside],
            run_time=1.6,
        )
        self.wait(0.3)

        cap = B.caption(
            "A universe: the points that exist.\nOutside it, values aren't missing - they're not defined.",
            size=27,
        )
        self.play(Write(cap, run_time=1.2))
        self.wait(1.8)
