from __future__ import annotations

from pathlib import Path

from ugts.numeric import pascal_parity_rows


ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'examples' / 'generated' / 'pascal_sierpinski.pbm'
rows = pascal_parity_rows(128)
width = 255
canvas = [[0] * width for _ in range(128)]
for y, row in enumerate(rows):
    x0 = 127 - y
    for k, bit in enumerate(row):
        canvas[y][x0 + 2 * k] = bit
out.write_text(
    'P1\n255 128\n' + '\n'.join(' '.join(map(str, row)) for row in canvas) + '\n',
    encoding='ascii',
)
print(f'wrote {out}')
