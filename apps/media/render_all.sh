#!/usr/bin/env bash
# Render all six scenes at 1080p and stitch them, in storyboard order, into manifold.mp4.
# Usage:  micromamba run -p ./.env ./render_all.sh   [-ql|-qh]   (default -qh = 1080p)
set -euo pipefail
cd "$(dirname "$0")"

QUALITY="${1:--qh}"

# (class, file) in storyboard order. Scenes are added as they are approved.
SCENES=(
  "Scene1Grid:scene1_grid.py"
  "Scene2Universe:scene2_universe.py"
  "Scene3Column:scene3_column.py"
  "Scene4Anchors:scene4_anchors.py"
  "Scene5Block:scene5_block.py"
  "Scene6Moods:scene6_moods.py"
)

CLIPS=()
for entry in "${SCENES[@]}"; do
  cls="${entry%%:*}"; file="${entry##*:}"
  [ -f "$file" ] || { echo "skip (not yet built): $file"; continue; }
  echo ">>> rendering $cls"
  manim "$QUALITY" "$file" "$cls"
  # locate the produced mp4 (manim nests by quality dir); newest match wins
  clip="$(find out/videos -name "${cls}.mp4" -print0 | xargs -0 ls -t 2>/dev/null | head -1)"
  [ -n "$clip" ] && CLIPS+=("$clip")
done

if [ "${#CLIPS[@]}" -gt 0 ]; then
  echo ">>> stitching ${#CLIPS[@]} clips -> manifold.mp4"
  : > out/_concat.txt
  for c in "${CLIPS[@]}"; do echo "file '$PWD/$c'" >> out/_concat.txt; done
  ffmpeg -y -f concat -safe 0 -i out/_concat.txt -c copy out/manifold.mp4
  echo ">>> done: out/manifold.mp4"
fi
