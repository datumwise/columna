"""Scene 5 — The block (the B-anchor).

An arrow tries to sum a stock (inventory `level`) across time; a clean barrier stands on the time
axis and the SUM is refused — totalling a stock over calendar is non-reconciling (179,656 means
nothing). A LAST arrow passes through smoothly to the period-end snapshot (6,066). The barrier is
elegant, not alarming: the grammar simply knows which directions are legal.

Caption: "Some directions are blocked. The grammar knows which."
"""
from __future__ import annotations

import math
import numpy as np
from manim import (
    Scene,
    VGroup,
    Polygon,
    Rectangle,
    Line,
    Arrow,
    Dot,
    FadeIn,
    FadeOut,
    Write,
    Create,
    GrowArrow,
    RIGHT,
    LEFT,
    UP,
    DOWN,
)

import brand as B
from data import NUM

Y_AX = 0.35                 # the time axis
X_L, X_R = -5.6, 2.9       # stock series extent (time ->)
WALL_X = 3.25
LO, HI = 5450.0, 6250.0    # a line's y-window (a trajectory, not a magnitude bar — zoom is honest here)


def _y(v):
    return Y_AX + (v - LO) / (HI - LO) * 1.9


class Scene5Block(Scene):
    def construct(self):
        series = NUM.s5_daily_level or tuple(
            5800 + 200 * math.sin(0.5 * i) for i in range(31)  # code-only fallback (no numerals)
        )
        n = len(series)
        xs = [X_L + (X_R - X_L) * (i / (n - 1)) for i in range(n)]
        pts = [np.array([xs[i], _y(series[i]), 0]) for i in range(n)]

        title = VGroup(
            B.label("measure", size=24, color=B.TEXT_SOFT),
            B.label("level", size=24, color=B.WARM, mono=True),
            B.label("— a stock over time", size=24, color=B.TEXT_SOFT),
        ).arrange(RIGHT, buff=0.22).to_edge(UP, buff=0.55)

        axis = Line([X_L - 0.2, Y_AX, 0], [WALL_X + 0.15, Y_AX, 0], stroke_width=1.6, color=B.GRID_LIT)
        axis_lbl = B.label("day →", size=20, color=B.TEXT_SOFT).next_to(axis.get_end(), DOWN, buff=0.12)

        area = Polygon(
            *pts, np.array([xs[-1], Y_AX, 0]), np.array([xs[0], Y_AX, 0]),
            stroke_width=0, fill_color=B.WARM, fill_opacity=0.16,
        )
        line = VGroup(*[Line(pts[i], pts[i + 1], stroke_width=2.4, color=B.WARM) for i in range(n - 1)])
        stock_lbl = B.label("inventory  ·  S001  ·  2024-01", size=19, color=B.TEXT_SOFT).move_to(
            [(X_L + X_R) / 2, _y(HI) + 0.15, 0]
        )

        self.play(Write(title, run_time=0.9))
        self.play(Create(axis, run_time=0.6), FadeIn(axis_lbl))
        self.play(FadeIn(area, run_time=0.8), Create(line, run_time=1.3, lag_ratio=0.03), FadeIn(stock_lbl))
        self.wait(0.3)

        # === SUM tries to travel ALONG time and is walled off ===
        sum_lbl = B.label("SUM", size=26, color=B.WARM, mono=True).move_to([X_L - 0.0, -1.35, 0])
        sum_arrow = Arrow(
            [X_L + 0.55, -1.35, 0], [WALL_X - 0.18, -1.35, 0], buff=0.0,
            stroke_width=4, color=B.WARM, max_tip_length_to_length_ratio=0.05,
        )
        # the barrier: a translucent cool band with a bright edge — elegant, not alarming
        wall = VGroup(
            Rectangle(width=0.22, height=2.0, stroke_width=0, fill_color=B.COOL, fill_opacity=0.16).move_to(
                [WALL_X, -1.0, 0]
            ),
            Line([WALL_X - 0.11, -2.0, 0], [WALL_X - 0.11, 0.0, 0], stroke_width=3.5, color=B.COOL),
        )
        blocked = B.value_tag(f"{NUM.s5_sum:,.0f}", size=34, color=B.TEXT_SOFT).move_to([4.75, -1.35, 0])
        strike = Line(
            blocked.get_left() + LEFT * 0.05, blocked.get_right() + RIGHT * 0.05,
            stroke_width=3, color=B.REFUSE,
        )
        blocked_tag = B.label("sum  ·  BLOCKED over calendar", size=18, color=B.REFUSE).next_to(
            blocked, DOWN, buff=0.16
        )

        self.play(Write(sum_lbl))
        self.play(GrowArrow(sum_arrow, run_time=0.9))
        self.play(FadeIn(wall, run_time=0.5), sum_arrow.animate.set_color(B.WARM_SOFT), run_time=0.5)
        self.play(FadeIn(blocked), Create(strike), FadeIn(blocked_tag), run_time=0.9)
        self.wait(0.3)

        # === LAST picks the endpoint and passes through cleanly ===
        endpoint = Dot(pts[-1], radius=0.08, color=B.WARM)
        served = B.value_tag(f"{NUM.s5_last:,.0f}", size=40, color=B.WARM).move_to([4.75, 1.75, 0])
        last_arrow = Arrow(
            pts[-1] + RIGHT * 0.12 + UP * 0.05, served.get_left() + LEFT * 0.18, buff=0.1,
            stroke_width=4, color=B.COOL, max_tip_length_to_length_ratio=0.06,
        )
        last_lbl = B.label("LAST", size=26, color=B.COOL, mono=True).next_to(last_arrow, UP, buff=0.08)
        served_tag = B.label("period-end snapshot  ✓", size=18, color=B.TEXT_SOFT).next_to(
            served, DOWN, buff=0.16
        )

        self.play(FadeIn(endpoint, scale=1.5))
        self.play(GrowArrow(last_arrow), Write(last_lbl), run_time=0.9)
        self.play(FadeIn(served, shift=RIGHT * 0.1), FadeIn(served_tag), run_time=0.9)

        b_tag = B.label("B-anchor", size=20, color=B.COOL).to_corner(UP + RIGHT, buff=0.6)
        cap = B.caption("Some directions are blocked. The grammar knows which.")
        self.play(FadeIn(b_tag), Write(cap, run_time=1.1))
        self.wait(2.0)
