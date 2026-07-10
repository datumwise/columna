"""Scene 1 — The grid.

An infinite flat Cartesian lattice of dim points fades in — axes `store`, `day`, with a third,
`product`, receding in soft perspective. One point brightens; a real value (58.26) attaches to it
like a tag.  Caption: "Data lives at coordinates."
"""
from __future__ import annotations

import numpy as np
from manim import (
    Scene,
    VGroup,
    Dot,
    Line,
    Text,
    Create,
    FadeIn,
    Write,
    Flash,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    UR,
)

import brand as B
import grid as G
from data import NUM, S1_STORE, S1_PRODUCT, S1_DAY

# grid geometry (shared, so nothing jumps between cuts)
NX, NY = G.NX, G.NY
DX, DY = G.DX, G.DY
BRIGHT_I, BRIGHT_J = 2, 3   # the point that brightens (interior, clearly visible)

# soft-perspective offset for the receding `product` axis
DEPTH = np.array([0.40, 0.30, 0.0])


def _pt(i: int, j: int) -> np.ndarray:
    return G.pt(i, j)


class Scene1Grid(Scene):
    def construct(self):
        # --- receding `product` ghost layers (drawn first, behind) ---
        ghosts = VGroup()
        for depth, op in ((2, 0.11), (1, 0.20)):
            layer = VGroup(
                *[
                    Dot(_pt(i, j) + DEPTH * depth, radius=0.032, color=B.DOT_DIM)
                    for i in range(NX)
                    for j in range(NY)
                ]
            ).set_opacity(op)
            ghosts.add(layer)

        # --- grid lines (thin, luminous, resting) ---
        lines = VGroup()
        for j in range(NY):
            lines.add(Line(_pt(0, j), _pt(NX - 1, j), stroke_width=1.0, color=B.GRID_DIM))
        for i in range(NX):
            lines.add(Line(_pt(i, 0), _pt(i, NY - 1), stroke_width=1.0, color=B.GRID_DIM))

        # --- the lattice of dim coordinates ---
        dots = {
            (i, j): Dot(_pt(i, j), radius=0.045, color=B.DOT_DIM)
            for i in range(NX)
            for j in range(NY)
        }
        lattice = VGroup(*dots.values())

        # --- axis labels ---
        store_lbl = B.label("store", size=26).next_to(
            VGroup(dots[(0, 0)], dots[(NX - 1, 0)]), DOWN, buff=0.45
        )
        day_lbl = B.label("day", size=26).rotate(np.pi / 2).next_to(
            VGroup(dots[(0, 0)], dots[(0, NY - 1)]), LEFT, buff=0.45
        )
        # receding axis: from the front-bottom-right corner into depth (up-right), fully in-frame
        prod_axis = Line(
            _pt(NX - 1, 0),
            _pt(NX - 1, 0) + DEPTH * 2.4,
            stroke_width=1.4,
            color=B.GRID_LIT,
        ).set_opacity(0.65)
        prod_lbl = B.label("product", size=22, color=B.TEXT_SOFT).next_to(
            prod_axis.get_end(), RIGHT, buff=0.12
        ).set_opacity(0.7)

        # --- the caption ---
        cap = B.caption("Data lives at coordinates.")

        # ============ animate ============
        self.play(FadeIn(ghosts, run_time=1.2))
        self.play(Create(lines, run_time=1.6, lag_ratio=0.02))
        self.play(FadeIn(lattice, run_time=1.4, lag_ratio=0.004))
        self.play(
            Write(store_lbl), Write(day_lbl),
            Create(prod_axis), FadeIn(prod_lbl),
            run_time=1.2,
        )
        self.play(Write(cap, run_time=1.0))
        self.wait(0.6)

        # --- one point brightens; a value attaches like a tag ---
        star = dots[(BRIGHT_I, BRIGHT_J)]
        self.play(
            star.animate.set_color(B.WARM).scale(1.9).set_opacity(1.0),
            Flash(star.get_center(), color=B.WARM, line_length=0.18, num_lines=12, flash_radius=0.34),
            run_time=0.9,
        )

        leader = Line(
            star.get_center() + RIGHT * 0.14,
            star.get_center() + RIGHT * 0.9,
            stroke_width=1.4,
            color=B.WARM_SOFT,
        )
        tag = B.value_tag(f"{NUM.s1_amount:.2f}", size=34).next_to(leader, RIGHT, buff=0.14)
        coord = B.label(
            f"{S1_STORE} · {S1_DAY} · {S1_PRODUCT}", size=18, color=B.TEXT_SOFT
        ).next_to(tag, DOWN, buff=0.12, aligned_edge=LEFT)

        self.play(Create(leader), FadeIn(tag, shift=RIGHT * 0.12), run_time=0.7)
        self.play(FadeIn(coord, run_time=0.5))
        self.wait(1.6)
