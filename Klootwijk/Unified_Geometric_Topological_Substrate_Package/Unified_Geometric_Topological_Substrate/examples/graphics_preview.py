from __future__ import annotations

from pathlib import Path

from ugts.geometry import CircleSDF
from ugts.glyphs import loop_to_r_morph
from ugts.math2d import Vec2
from ugts.render import Bounds2D, posterize_1bit, rasterize_field


ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'examples' / 'generated'
out.mkdir(parents=True, exist_ok=True)

for frame, alpha in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
    field = loop_to_r_morph(alpha)
    image = rasterize_field(
        field,
        width=72,
        height=72,
        bounds=Bounds2D(-1.2, 1.2, -1.2, 1.2),
        samples=4,
        edge_width=0.025,
    )
    image.to_pgm(out / f'glyph_morph_{frame:02d}.pgm')
    posterize_1bit(image, seed=100 + frame).to_pbm(out / f'glyph_morph_{frame:02d}_1bit.pbm')

print(f'wrote glyph morph previews to {out}')
