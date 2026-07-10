"""Scene 4 — The two anchors.

The surface reduces: fine day-columns (the *real* per-day aov series for 2024-01) collapse into a
month bar; the notation rho( aov @ grain ) @ month stands above. A second collapse from transaction
grain lands on a *different* number. Both side by side: 140.90 (@day) vs 139.91 (@transaction) —
same measure, same month, two input anchors, two numbers.

Caption: "Every reduction has two anchors. Change the input grain, change the number."
"""
from __future__ import annotations

import math
from manim import (
    Scene,
    VGroup,
    Rectangle,
    FadeIn,
    FadeOut,
    Write,
    GrowFromEdge,
    Transform,
    RIGHT,
    LEFT,
    UP,
    DOWN,
)

import brand as B
from data import NUM

Y0 = -1.7                    # baseline the result bars grow from
K = 2.3 / 140.0             # value -> bar height (a ~140 month value stands 2.3 tall)
CK = 0.9 / 220.0            # compressed scale for the fine origin columns (kept low, out of the way)
AX, BX = -3.3, 3.3         # the two result columns, pushed to the sides (empty centre for the Δ)


def _bar(x, value, width, color, opacity, scale):
    h = max(value * scale, 0.02)
    r = Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity)
    r.move_to([x, Y0 + h / 2.0, 0])
    return r


class Scene4Anchors(Scene):
    def construct(self):
        # notation template on top (one form; the two instantiations are tagged under each bar)
        note = VGroup(
            B.label("ρ( ", size=30, color=B.COOL, mono=True),
            B.label("aov", size=30, color=B.WARM, mono=True),
            B.label(" @ ", size=30, color=B.COOL, mono=True),
            B.label("grain", size=30, color=B.COOL, mono=True),
            B.label(" ) @ month", size=30, color=B.COOL, mono=True),
        ).arrange(RIGHT, buff=0.06).to_edge(UP, buff=0.65)
        self.play(Write(note, run_time=1.2))

        # === Panel A — day grain: the real per-day aov series collapses to a month bar ===
        series = NUM.s4_daily_aov or tuple(140 + 45 * math.sin(0.7 * i) for i in range(31))
        n = len(series)
        span, x0 = 2.1, -6.5
        w = span / n * 0.7
        day_cols = VGroup(
            *[_bar(x0 + span * (i / (n - 1)), v, w, B.WARM, 0.7, CK) for i, v in enumerate(series)]
        )
        day_lbl = B.label("aov by day (2024-01)", size=19, color=B.TEXT_SOFT).next_to(day_cols, UP, buff=0.18)
        self.play(GrowFromEdge(day_cols, DOWN, run_time=1.2, lag_ratio=0.03), FadeIn(day_lbl))
        self.wait(0.2)

        bar_a = _bar(AX, NUM.s4_daygrain, 1.0, B.WARM, 1.0, K)
        self.play(Transform(day_cols, bar_a, run_time=1.1), FadeOut(day_lbl, run_time=0.6))
        num_a = B.value_tag(f"{NUM.s4_daygrain:.2f}", size=42).next_to(bar_a, UP, buff=0.25)
        tag_a = B.label("@ day", size=24, color=B.COOL, mono=True).next_to(bar_a, DOWN, buff=0.22)
        self.play(FadeIn(num_a, shift=UP * 0.1), FadeIn(tag_a), run_time=0.9)
        self.wait(0.3)

        # === Panel B — transaction grain: a finer origin, a different number ===
        span_b, xb0, m = 2.1, 4.4, 70
        txn_cols = VGroup(
            *[
                _bar(
                    xb0 + span_b * (i / (m - 1)),
                    120 + 80 * abs(math.sin(1.9 * i + 0.6)),  # texture only (no numerals shown)
                    span_b / m * 0.6, B.WARM, 0.45, CK,
                )
                for i in range(m)
            ]
        )
        txn_lbl = B.label("aov by transaction", size=19, color=B.TEXT_SOFT).next_to(txn_cols, UP, buff=0.18)
        self.play(GrowFromEdge(txn_cols, DOWN, run_time=1.0, lag_ratio=0.01), FadeIn(txn_lbl))

        bar_b = _bar(BX, NUM.s4_pooled, 1.0, B.WARM, 1.0, K)
        self.play(Transform(txn_cols, bar_b, run_time=1.0), FadeOut(txn_lbl, run_time=0.6))
        num_b = B.value_tag(f"{NUM.s4_pooled:.2f}", size=42).next_to(bar_b, UP, buff=0.25)
        tag_b = B.label("@ transaction", size=24, color=B.COOL, mono=True).next_to(bar_b, DOWN, buff=0.22)
        self.play(FadeIn(num_b, shift=UP * 0.1), FadeIn(tag_b), run_time=0.9)
        self.wait(0.3)

        # === the difference is real — a quiet centre callout in the empty gap ===
        neq = B.value_tag("≠", size=48, color=B.TEXT).move_to([0, 0.5, 0])
        dlt = B.label(f"Δ {NUM.s4_daygrain - NUM.s4_pooled:.2f}", size=26, color=B.TEXT_SOFT).next_to(neq, DOWN, buff=0.2)
        self.play(FadeIn(neq), FadeIn(dlt), run_time=0.8)

        cap = B.caption(
            "Every reduction has two anchors.\nChange the input grain, change the number.", size=28
        )
        self.play(Write(cap, run_time=1.2))
        self.wait(2.0)
