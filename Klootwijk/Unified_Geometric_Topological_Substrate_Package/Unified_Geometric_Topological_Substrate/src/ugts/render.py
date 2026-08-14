from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from pathlib import Path
import random
from typing import Iterable

from .geometry import Field2D, finite_difference_gradient
from .logpolar import LogPolarLUT, to_log_polar
from .math2d import Vec2, clamp
from .numeric import golden_angle_points


@dataclass(frozen=True, slots=True)
class Bounds2D:
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def __post_init__(self) -> None:
        if self.x_max <= self.x_min or self.y_max <= self.y_min:
            raise ValueError('invalid bounds')


@dataclass(slots=True)
class GrayImage:
    width: int
    height: int
    pixels: list[float]

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError('image dimensions must be positive')
        if len(self.pixels) != self.width * self.height:
            raise ValueError('pixel count does not match dimensions')

    def at(self, x: int, y: int) -> float:
        return self.pixels[y * self.width + x]

    def to_pgm(self, path: str | Path, max_value: int = 255) -> None:
        if not (1 <= max_value <= 65535):
            raise ValueError('max_value must be in [1, 65535]')
        path = Path(path)
        values = [str(round(clamp(v, 0.0, 1.0) * max_value)) for v in self.pixels]
        rows = [' '.join(values[y * self.width:(y + 1) * self.width]) for y in range(self.height)]
        path.write_text(f'P2\n{self.width} {self.height}\n{max_value}\n' + '\n'.join(rows) + '\n', encoding='ascii')

    def to_pbm(self, path: str | Path, threshold: float = 0.5) -> None:
        path = Path(path)
        bits = ['1' if v >= threshold else '0' for v in self.pixels]
        rows = [' '.join(bits[y * self.width:(y + 1) * self.width]) for y in range(self.height)]
        path.write_text(f'P1\n{self.width} {self.height}\n' + '\n'.join(rows) + '\n', encoding='ascii')


def _pixel_center(x: int, y: int, width: int, height: int, bounds: Bounds2D) -> Vec2:
    px = bounds.x_min + (x + 0.5) / width * (bounds.x_max - bounds.x_min)
    py = bounds.y_max - (y + 0.5) / height * (bounds.y_max - bounds.y_min)
    return Vec2(px, py)


def rasterize_field(
    field: Field2D,
    *,
    width: int = 256,
    height: int = 256,
    bounds: Bounds2D = Bounds2D(-1.5, 1.5, -1.5, 1.5),
    samples: int = 8,
    edge_width: float = 0.015,
    logpolar_mask: LogPolarLUT | None = None,
) -> GrayImage:
    """Rasterize an implicit field with deterministic golden-angle supersampling.

    This is the report's technical normalization of the documents' "Feynman vector"
    language: oriented complex phasors are accumulated as a coverage estimator. It is
    a graphics algorithm, not a quantum-mechanical claim.
    """
    if width <= 0 or height <= 0 or samples <= 0 or edge_width <= 0.0:
        raise ValueError('invalid rasterization parameters')
    offsets = golden_angle_points(samples, radius=0.45)
    sx = (bounds.x_max - bounds.x_min) / width
    sy = (bounds.y_max - bounds.y_min) / height
    pixels: list[float] = []
    for y in range(height):
        for x in range(width):
            center = _pixel_center(x, y, width, height, bounds)
            amplitude = 0j
            weight_sum = 0.0
            # One center gradient gives a stable local orientation while keeping the
            # reference rasterizer small and fast enough for tests/examples.
            grad = finite_difference_gradient(field, center)
            base_phase = math.atan2(grad.y, grad.x) if grad.norm2() > 1e-20 else 0.0
            for off in offsets:
                p = Vec2(center.x + off.x * sx, center.y + off.y * sy)
                if logpolar_mask is not None and not logpolar_mask.is_active(to_log_polar(p)):
                    continue
                d = field.value(p)
                # Smooth local coverage around the zero boundary / interior.
                coverage = clamp(0.5 - d / (2.0 * edge_width), 0.0, 1.0)
                if coverage <= 0.0:
                    continue
                phase = base_phase + 0.15 * math.atan2(off.y, off.x)
                amplitude += coverage * cmath.exp(1j * phase)
                weight_sum += coverage
            # Combine ordinary coverage and normalized coherent magnitude. The coverage
            # term avoids cancellation making solid interiors disappear.
            ordinary = weight_sum / samples
            coherent = abs(amplitude) / samples
            pixels.append(clamp(0.75 * ordinary + 0.25 * coherent, 0.0, 1.0))
    return GrayImage(width, height, pixels)


def blue_noise_threshold(width: int, height: int, seed: int = 0) -> list[float]:
    """Small deterministic stochastic threshold field.

    It is not a production blue-noise optimizer; it supplies a reproducible, schema-bound
    jitter adapter for examples and tests.
    """
    if width <= 0 or height <= 0:
        raise ValueError('dimensions must be positive')
    rng = random.Random(seed)
    values = [rng.random() for _ in range(width * height)]
    # Rank ordering makes the histogram uniform and deterministic.
    order = sorted(range(len(values)), key=values.__getitem__)
    ranked = [0.0] * len(values)
    denom = max(1, len(values) - 1)
    for rank, idx in enumerate(order):
        ranked[idx] = rank / denom
    return ranked


def posterize_1bit(image: GrayImage, *, seed: int = 0) -> GrayImage:
    threshold = blue_noise_threshold(image.width, image.height, seed)
    return GrayImage(image.width, image.height, [1.0 if v >= t else 0.0 for v, t in zip(image.pixels, threshold)])


def sigma_delta_bitstream(level: float, length: int) -> tuple[int, ...]:
    """First-order pulse-density/sigma-delta modulation for a level in [0,1]."""
    if length < 0:
        raise ValueError('length must be nonnegative')
    level = clamp(level, 0.0, 1.0)
    error = 0.0
    bits: list[int] = []
    for _ in range(length):
        error += level
        bit = 1 if error >= 0.5 else 0
        error -= bit
        bits.append(bit)
    return tuple(bits)


def chromatic_rho(rho: float, channel_offset: float) -> float:
    """Apply a channel-specific log-radius shift; real-space scale becomes addition."""
    return rho + channel_offset
