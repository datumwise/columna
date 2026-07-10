"""Scene 6 — The blast wall / the four moods (finale).

Split screen: above, a soft multilingual cloud of meaning (names, phrasings, a question
"average order value?"); below, the rigid luminous lattice. A thin bright line divides them. The
question descends, strikes the line, and returns as four glyphs in sequence —
serve · disclose · clarify · refuse. Then: Columna + pip install columna-core.

Caption: "Meaning above, correctness below. The model proposes; the grammar disposes."
"""
from __future__ import annotations

import numpy as np
from manim import (
    Scene,
    VGroup,
    Text,
    Dot,
    Line,
    Circle,
    Annulus,
    RoundedRectangle,
    Flash,
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

DIV_Y = 0.4  # the dividing line: meaning above, correctness below

# real translations of "average order value" (Latin / Cyrillic / Greek — no CJK in the render font)
CLOUD = [
    ("average order value?", 30, [-3.1, 3.35, 0]),
    ("AOV", 30, [5.1, 3.2, 0]),
    ("valore medio dell'ordine", 21, [2.4, 3.4, 0]),
    ("средний чек", 26, [-5.2, 2.5, 0]),
    ("valeur moyenne de commande", 23, [3.0, 2.55, 0]),
    ("μέση αξία παραγγελίας", 22, [-2.3, 2.45, 0]),
    ("durchschnittlicher Bestellwert", 21, [-4.4, 1.6, 0]),
    ("valor medio del pedido", 23, [3.7, 1.5, 0]),
    ("revenue ÷ orders?", 22, [0.7, 1.85, 0]),
    ("avg basket size", 22, [-1.7, 1.25, 0]),
]


def _mood(name: str, color: str, icon) -> VGroup:
    lbl = B.label(name, size=27, color=color, mono=True)
    icon.next_to(lbl, UP, buff=0.22)
    return VGroup(icon, lbl)


class Scene6Moods(Scene):
    def construct(self):
        # === the divider, and the two realms ===
        divider = Line([-7.0, DIV_Y, 0], [7.0, DIV_Y, 0], stroke_width=2.5, color=B.COOL)
        meaning_lbl = B.label("meaning", size=20, color=B.TEXT_SOFT).to_corner(UP + LEFT, buff=0.5)
        correct_lbl = B.label("correctness", size=20, color=B.COOL).move_to([-6.05, DIV_Y - 0.4, 0])

        # lower realm: a rigid luminous lattice
        lat = VGroup()
        nx, ny = 11, 4
        x0, y0, dx, dy = -6.0, -3.2, 1.2, 0.72
        for i in range(nx):
            for j in range(ny):
                lat.add(Dot([x0 + i * dx, y0 + j * dy, 0], radius=0.035, color=B.COOL).set_opacity(0.5))
        grid = VGroup()
        for j in range(ny):
            grid.add(Line([x0, y0 + j * dy, 0], [x0 + (nx - 1) * dx, y0 + j * dy, 0], stroke_width=0.8, color=B.GRID_LIT))
        for i in range(nx):
            grid.add(Line([x0 + i * dx, y0, 0], [x0 + i * dx, y0 + (ny - 1) * dy, 0], stroke_width=0.8, color=B.GRID_LIT))
        grid.set_stroke(opacity=0.5)

        self.play(Create(divider, run_time=1.0), FadeIn(meaning_lbl), FadeIn(correct_lbl))
        self.play(FadeIn(grid, run_time=0.8), FadeIn(lat, run_time=1.0, lag_ratio=0.01))

        # upper realm: the soft, drifting cloud of meaning
        cloud = VGroup(
            *[Text(t, font=B.FONT, color=B.TEXT_SOFT, font_size=s).move_to(p).set_opacity(0.45) for t, s, p in CLOUD]
        )
        self.play(FadeIn(cloud, run_time=1.6, lag_ratio=0.12))
        self.wait(0.4)

        # === the question descends and strikes the line ===
        q = B.label("average order value?", size=28, color=B.TEXT)
        bubble = RoundedRectangle(
            corner_radius=0.18, width=q.width + 0.6, height=q.height + 0.45,
            stroke_color=B.TEXT_SOFT, stroke_width=1.6, fill_color=B.BG, fill_opacity=0.9,
        )
        chat = VGroup(bubble, q).move_to([0, 3.0, 0])
        self.play(FadeIn(chat, run_time=0.7))
        self.play(chat.animate.move_to([0, DIV_Y + 0.55, 0]), run_time=1.1)
        self.play(
            Flash([0, DIV_Y, 0], color=B.COOL, line_length=0.35, num_lines=20, flash_radius=0.6),
            FadeOut(chat),
            run_time=0.7,
        )
        self.remove(chat)  # ensure the question is gone once it has struck the line

        # === returns as four glyphs, in sequence, below the line ===
        serve = _mood("serve", B.WARM, Dot(radius=0.13, color=B.WARM))
        disclose = _mood("disclose", B.WARM, VGroup(
            Dot(radius=0.13, color=B.WARM), Annulus(inner_radius=0.17, outer_radius=0.21, color=B.COOL),
        ))
        clarify = _mood("clarify", B.COOL, Text("?", font=B.MONO, color=B.COOL, font_size=34))
        refuse = _mood("refuse", B.REFUSE, VGroup(
            Circle(radius=0.15, stroke_color=B.REFUSE, stroke_width=3),
            Line([-0.11, 0.11, 0], [0.11, -0.11, 0], stroke_width=3, color=B.REFUSE),
        ))
        moods = VGroup(serve, disclose, clarify, refuse).arrange(RIGHT, buff=1.15).move_to([0, -1.3, 0])
        seps = VGroup(*[
            B.label("·", size=30, color=B.TEXT_SOFT).move_to(
                (moods[k].get_right() + moods[k + 1].get_left()) / 2 + UP * 0.18
            )
            for k in range(3)
        ])
        for k, mo in enumerate(moods):
            self.play(FadeIn(mo, shift=UP * 0.15, run_time=0.5))
            if k < 3:
                self.play(FadeIn(seps[k], run_time=0.15))

        cap = B.caption("Meaning above, correctness below.\nThe model proposes; the grammar disposes.", size=28)
        self.play(Write(cap, run_time=1.3))
        self.wait(1.8)

        # === resolve to the wordmark ===
        end_moods = moods.copy()
        self.play(
            FadeOut(cloud), FadeOut(chat), FadeOut(grid), FadeOut(lat), FadeOut(divider),
            FadeOut(meaning_lbl), FadeOut(correct_lbl), FadeOut(cap), FadeOut(seps),
            FadeOut(moods), run_time=1.0,
        )
        end_moods.generate_target()
        end_moods.target.scale(0.72).move_to([0, 1.4, 0])
        wordmark = Text("Columna", font=B.FONT, weight="SEMIBOLD", color=B.TEXT, font_size=68).move_to([0, -0.2, 0])
        tagline = B.label("an honest metrics engine", size=24, color=B.TEXT_SOFT).next_to(wordmark, DOWN, buff=0.3)
        pip = B.value_tag("pip install columna-core", size=28, color=B.COOL).next_to(tagline, DOWN, buff=0.5)
        from manim import MoveToTarget
        self.play(MoveToTarget(end_moods), FadeIn(wordmark, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(tagline), FadeIn(pip), run_time=0.9)
        self.wait(2.2)
