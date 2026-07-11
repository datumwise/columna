"""Visual language for the "What a Manifold Is" animation.

Dark ground, thin luminous grid, restrained palette: one warm accent for *data*, one cool
accent for *grammar*. Serene pacing, no camera gimmicks. A proof unfolding, not a promo.

Everything a scene needs to stay in-brand lives here so the six scenes read as one film.
"""
from __future__ import annotations

from manim import (
    Text,
    VGroup,
    Dot,
    Line,
    config,
)

# ---------------------------------------------------------------- palette
# Two registers from one set of scenes. COLUMNA_PAPER=1 renders the "paper" variant — ink-on-paper,
# background matched to datumwise.ai (#faf8f3) — used as the site's ambient §1 texture.
import os as _os

if _os.environ.get("COLUMNA_PAPER") == "1":
    # MONOCHROME INK. The ambient background is aria-hidden decoration, not a mood-tag surface —
    # so it carries NO saturated colour (that privilege belongs to Exhibit B alone). Data vs
    # grammar are distinguished only by tonal value here, never by hue.
    BG = "#faf8f3"        # paper (matches the site)
    GRID_DIM = "#e6dfcf"  # faint grid, resting
    GRID_LIT = "#b9ab90"  # grid, drawn/active
    DOT_DIM = "#b6ab92"   # a coordinate at rest
    TEXT = "#2b2820"      # captions / labels, ink
    TEXT_SOFT = "#6f695c" # secondary labels
    WARM = "#726851"      # DATA — mid warm-grey ink (lighter value)
    WARM_SOFT = "#cfc6b0"
    COOL = "#4c4636"      # GRAMMAR — dark warm-grey ink (darker value)
    COOL_SOFT = "#b3aa93"
    REFUSE = "#3a352b"    # barrier / refusal — ink, not red
else:
    BG = "#0B0E14"        # dark ground
    GRID_DIM = "#1E2A3A"  # thin luminous grid, resting
    GRID_LIT = "#33506E"  # grid, drawn/active
    DOT_DIM = "#33445C"   # a coordinate at rest
    TEXT = "#D3DCE8"      # captions / labels, soft off-white
    TEXT_SOFT = "#8A97A9" # secondary labels
    WARM = "#F4A94B"      # DATA — values, measures, the served number
    WARM_SOFT = "#7A5B32"
    COOL = "#5CC8E6"      # GRAMMAR — universes, edges, the four moods
    COOL_SOFT = "#2E6579"
    REFUSE = "#E8654F"    # a barrier / refusal (still elegant, not alarming)

GONE = BG             # outside a universe: not gray — *gone* (= the ground)
config.background_color = BG  # follow the palette (overrides manim.cfg once this module imports)

# ---------------------------------------------------------------- type
FONT = "DejaVu Sans"  # clean sans, bundled in the env; deterministic across renders
MONO = "DejaVu Sans Mono"


def caption(text: str, color: str = TEXT, size: int = 30) -> Text:
    """One sentence, clean sans, bottom third. The single voice of each scene.

    A `\\n` in `text` makes a centered two-line caption (used where the brief's line is long).
    """
    t = Text(text, font=FONT, weight="LIGHT", color=color, font_size=size, line_spacing=0.8)
    t.to_edge(edge=(0, -1, 0), buff=0.5)  # bottom third
    return t


def label(text: str, color: str = TEXT_SOFT, size: int = 26, mono: bool = False) -> Text:
    return Text(text, font=(MONO if mono else FONT), color=color, font_size=size)


def value_tag(text: str, color: str = WARM, size: int = 30) -> Text:
    """A data value — always warm, always mono (a number is a fact, rendered as one)."""
    return Text(text, font=MONO, weight="MEDIUM", color=color, font_size=size)


def title(text: str, color: str = TEXT, size: int = 40) -> Text:
    return Text(text, font=FONT, weight="NORMAL", color=color, font_size=size)
