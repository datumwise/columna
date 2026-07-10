# apps/media — "What a Manifold Is" (90s, Manim CE)

A deterministic, programmatic explainer of Columna's core idea: a manifold is *data at coordinates*,
carved by a universe, functioned by columns, reduced through two anchors, and disciplined by a
grammar that knows which directions are blocked. Six scenes, ~15s each → `manifold.mp4` (1080p),
plus each scene as a standalone website clip.

This is **code, not AI video** — every frame is deterministic, in-brand for a correctness company.
And the grounding rule applies to marketing too: **every number on screen is real**, recomputed from
the packaged demo warehouse in `data.py` and drift-guarded (a silent change fails the build).

## Scenes

| # | class | file | idea | grounded number(s) |
|---|---|---|---|---|
| 1 | `Scene1Grid` | `scene1_grid.py` | Data lives at coordinates | `58.26` (a txn amount at one store·day·product) |
| 2 | `Scene2Universe` | `scene2_universe.py` | A universe: the points that exist | — |
| 3 | `Scene3Column` | `scene3_column.py` | A column: a value at every point | — |
| 4 | `Scene4Anchors` | `scene4_anchors.py` | Two anchors — change the grain, change the number | `139.91` vs `140.90` (aov @ 2024-01) |
| 5 | `Scene5Block` | `scene5_block.py` | Some directions are blocked | `6066` (LAST) vs `179656` (blocked SUM) |
| 6 | `Scene6Moods` | `scene6_moods.py` | Meaning above, correctness below | — |

## Environment

Manim CE needs cairo/pango/ffmpeg. This repo builds them **rootless** via micromamba (no system
packages). One-time setup:

```bash
# a self-contained env with manim + duckdb (for the grounded numbers)
micromamba create -y -p ./.env -c conda-forge python=3.12 manim duckdb polars
RUN="micromamba run -p ./.env"
```

(If you have manim + a system cairo/pango/ffmpeg already, just use `manim` directly.)

## Render

```bash
cd apps/media

# one scene, high quality (1080p):     -qh = 1080p30 · -ql = 480p15 (fast preview)
$RUN manim -qh scene1_grid.py Scene1Grid

# a single still (last frame) for review:
$RUN manim -qh -s scene1_grid.py Scene1Grid

# all six scenes + stitch into manifold.mp4:
$RUN ./render_all.sh
```

Config (resolution, fps, dark background, output dir) lives in `manim.cfg`. Rendered video lands in
`out/` (gitignored). Small review stills live in `stills/`.

## Verify the numbers are real

```bash
$RUN python3 data.py     # prints each on-screen number + its warehouse provenance
```
