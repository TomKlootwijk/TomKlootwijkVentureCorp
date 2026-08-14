from __future__ import annotations

from dataclasses import dataclass
import math

from .geometry import CircleSDF, Field2D, MorphField, SegmentSDF, SmoothUnionField, UnionField
from .math2d import Vec2, clamp


@dataclass(frozen=True, slots=True)
class CubicBezier:
    p0: Vec2
    p1: Vec2
    p2: Vec2
    p3: Vec2

    def point(self, t: float) -> Vec2:
        u = 1.0 - clamp(t, 0.0, 1.0)
        t = 1.0 - u
        return (
            self.p0 * (u * u * u)
            + self.p1 * (3.0 * u * u * t)
            + self.p2 * (3.0 * u * t * t)
            + self.p3 * (t * t * t)
        )


@dataclass(frozen=True, slots=True)
class PolylineField:
    """Distance field to a sampled curve with finite stroke radius."""

    points: tuple[Vec2, ...]
    radius: float = 0.04

    def value(self, p: Vec2) -> float:
        if len(self.points) == 0:
            return math.inf
        if len(self.points) == 1:
            return (p - self.points[0]).norm() - self.radius
        return min(SegmentSDF(a, b, self.radius).value(p) for a, b in zip(self.points, self.points[1:]))


def sample_bezier(curve: CubicBezier, samples: int = 24) -> tuple[Vec2, ...]:
    if samples < 2:
        raise ValueError('samples must be at least 2')
    return tuple(curve.point(i / (samples - 1)) for i in range(samples))


def loop_stem_field(stroke: float = 0.06) -> Field2D:
    """A font-independent loop-plus-stem abstraction used for phi/D/B motifs."""
    loop = CircleSDF(Vec2(0.25, 0.25), 0.55)
    # Ring plus vertical stem. Difference is avoided here to keep the implementation small;
    # a thin circular boundary is represented by abs(distance)-stroke.
    class Ring:
        def value(self, p: Vec2) -> float:
            return abs(loop.value(p)) - stroke
    stem = SegmentSDF(Vec2(-0.30, -0.85), Vec2(-0.30, 0.85), stroke)
    return UnionField(Ring(), stem)


def r_glyph_field(stroke: float = 0.06) -> Field2D:
    """An R-like path built from a stem, upper loop and diagonal leg."""
    stem = SegmentSDF(Vec2(-0.30, -0.85), Vec2(-0.30, 0.85), stroke)
    upper = CubicBezier(
        Vec2(-0.30, 0.80), Vec2(0.75, 0.85), Vec2(0.75, -0.05), Vec2(-0.30, 0.05)
    )
    loop_path = PolylineField(sample_bezier(upper), stroke)
    leg = SegmentSDF(Vec2(-0.05, 0.02), Vec2(0.70, -0.85), stroke)
    return UnionField(UnionField(stem, loop_path), leg)


def loop_to_r_morph(alpha: float, stroke: float = 0.06) -> MorphField:
    """Field morph for the source's cut/unroll loop-to-R trick.

    Intermediate fields are visualization fields and are not guaranteed exact SDFs.
    """
    return MorphField(loop_stem_field(stroke), r_glyph_field(stroke), clamp(alpha, 0.0, 1.0))


def overlapping_semicircle_lens(radius: float = 1.0, separation: float = 1.0) -> tuple[CircleSDF, CircleSDF]:
    if radius <= 0.0:
        raise ValueError('radius must be positive')
    return (
        CircleSDF(Vec2(-0.5 * separation, 0.0), radius),
        CircleSDF(Vec2(0.5 * separation, 0.0), radius),
    )
