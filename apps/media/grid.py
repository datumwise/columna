"""Shared lattice geometry so every scene sits on the *same* coordinate space.

Scene 1 established these values; scenes 2+ import them so the grid never jumps between cuts.
"""
from __future__ import annotations

import numpy as np
from manim import Dot, Line, VGroup, RIGHT, UP, LEFT, DOWN

import brand as B

NX, NY = 8, 6            # store columns, day rows
DX, DY = 0.92, 0.66
# lowered, leaving a clean top band for the grammar/notation that scenes 2,4,5,6 write above
ORIGIN = LEFT * 3.9 + DOWN * 1.1


def pt(i: int, j: int) -> np.ndarray:
    return ORIGIN + RIGHT * i * DX + UP * j * DY


def gridlines(color: str = B.GRID_DIM, stroke_width: float = 1.0) -> VGroup:
    g = VGroup()
    for j in range(NY):
        g.add(Line(pt(0, j), pt(NX - 1, j), stroke_width=stroke_width, color=color))
    for i in range(NX):
        g.add(Line(pt(i, 0), pt(i, NY - 1), stroke_width=stroke_width, color=color))
    return g


def lattice(radius: float = 0.045, color: str = B.DOT_DIM) -> dict:
    """Map (i, j) -> Dot, so scenes can address individual coordinates."""
    return {
        (i, j): Dot(pt(i, j), radius=radius, color=color)
        for i in range(NX)
        for j in range(NY)
    }


def col_x(i: int) -> float:
    return pt(i, 0)[0]


def row_y(j: int) -> float:
    return pt(0, j)[1]
