"""Scene 3 — A column is a function.

Values bloom over every in-universe point at once, as a smooth surface hovering over the region:
a column is a value at every point of its universe. Then a few points stay dark under a small
hollow ring — where the column leaks, the leak has a *declared mechanism* (the M-anchor,
understated).
"""
from __future__ import annotations

import numpy as np
from manim import (
    Scene,
    VGroup,
    Dot,
    Line,
    Circle,
    FadeIn,
    FadeOut,
    Create,
    Write,
    RIGHT,
    UP,
    DOWN,
)

import brand as B
import grid as G

# same universe as Scene 2 (per-store staircase: rows below are outside)
OUTSIDE_ROWS = [3, 2, 2, 1, 1, 1, 0, 0]

# a few in-universe points where the column leaks (no value) — declared by the M-anchor
LEAKS = {(4, 3), (6, 2), (2, 4)}


def _inside(i: int, j: int) -> bool:
    return j >= OUTSIDE_ROWS[i]


def _height(i: int, j: int) -> float:
    """A smooth field over the region (no numerals shown — a column's *shape*, not a claim)."""
    return float(np.exp(-(((i - 3.4) ** 2) * 0.11 + ((j - 3.8) ** 2) * 0.16)))


class Scene3Column(Scene):
    def construct(self):
        inside = [(i, j) for i in range(G.NX) for j in range(G.NY) if _inside(i, j)]
        valued = [p for p in inside if p not in LEAKS]

        # --- re-establish the carved universe (Scene 2's end state) ---
        gridlines = G.gridlines(color=B.GRID_DIM, stroke_width=1.0).set_stroke(opacity=0.28)
        dots = {p: Dot(G.pt(*p), radius=0.045 * 1.25, color=B.COOL) for p in inside}
        self.play(FadeIn(gridlines, run_time=0.6), FadeIn(VGroup(*dots.values()), run_time=0.8))
        self.wait(0.2)

        top = VGroup(
            B.label("column", size=22, color=B.TEXT_SOFT),
            B.label("revenue", size=30, color=B.WARM, mono=True),
        ).arrange(RIGHT, buff=0.22).to_edge(UP, buff=0.7)
        self.play(Write(top, run_time=0.8))

        # --- the mesh surface: warm edges between adjacent valued points ---
        mesh = VGroup()
        vs = set(valued)
        for (i, j) in valued:
            for (di, dj) in ((1, 0), (0, 1)):
                nb = (i + di, j + dj)
                if nb in vs:
                    mesh.add(Line(G.pt(i, j), G.pt(*nb), stroke_width=1.4, color=B.WARM))
        mesh.set_stroke(opacity=0.45)

        # --- bloom: valued points swell warm (sized/brightened by the field); mesh draws in ---
        blooms = []
        for p in valued:
            h = _height(*p)
            d = dots[p]
            blooms.append(
                d.animate.set_color(B.WARM).scale((0.055 + 0.075 * h) / (0.045 * 1.25)).set_opacity(
                    0.55 + 0.45 * h
                )
            )
        self.play(*blooms, Create(mesh, run_time=1.6, lag_ratio=0.01), run_time=1.6)

        cap1 = B.caption("A column: a value at every point of its universe.")
        self.play(Write(cap1, run_time=1.1))
        self.wait(1.3)

        # --- the leak: a few points stay dark under a small hollow ring (M-anchor) ---
        rings = VGroup(
            *[
                Circle(radius=0.15, stroke_color=B.COOL, stroke_width=2.2, fill_opacity=0).move_to(
                    G.pt(*p)
                )
                for p in LEAKS
            ]
        )
        self.play(
            *[dots[p].animate.set_color(B.DOT_DIM).set_opacity(0.5).scale(0.7) for p in LEAKS],
            FadeIn(rings, run_time=1.0),
            run_time=1.0,
        )

        cap2 = B.caption("…and where it leaks, the leak has a declared mechanism.", size=28)
        m_tag = B.label("M-anchor", size=20, color=B.COOL).to_corner(UP + RIGHT, buff=0.7)
        self.play(FadeOut(cap1, run_time=0.4))
        self.play(Write(cap2, run_time=1.0), FadeIn(m_tag, run_time=0.8))
        self.wait(1.8)
