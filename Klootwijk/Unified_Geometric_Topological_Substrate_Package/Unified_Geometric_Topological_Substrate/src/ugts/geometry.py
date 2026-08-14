from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Protocol

from .math2d import Vec2, clamp


class Field2D(Protocol):
    def value(self, p: Vec2) -> float: ...


@dataclass(frozen=True, slots=True)
class CallableField:
    fn: Callable[[Vec2], float]
    name: str = 'callable_field'

    def value(self, p: Vec2) -> float:
        return float(self.fn(p))


@dataclass(frozen=True, slots=True)
class CircleSDF:
    center: Vec2
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0.0:
            raise ValueError('radius must be positive')

    def value(self, p: Vec2) -> float:
        return (p - self.center).norm() - self.radius


@dataclass(frozen=True, slots=True)
class BoxSDF:
    center: Vec2
    half_size: Vec2

    def __post_init__(self) -> None:
        if self.half_size.x <= 0.0 or self.half_size.y <= 0.0:
            raise ValueError('half_size components must be positive')

    def value(self, p: Vec2) -> float:
        qx = abs(p.x - self.center.x) - self.half_size.x
        qy = abs(p.y - self.center.y) - self.half_size.y
        outside = Vec2(max(qx, 0.0), max(qy, 0.0)).norm()
        inside = min(max(qx, qy), 0.0)
        return outside + inside


@dataclass(frozen=True, slots=True)
class SegmentSDF:
    a: Vec2
    b: Vec2
    radius: float = 0.0

    def value(self, p: Vec2) -> float:
        ba = self.b - self.a
        denom = ba.norm2()
        if denom == 0.0:
            return (p - self.a).norm() - self.radius
        h = clamp((p - self.a).dot(ba) / denom, 0.0, 1.0)
        return (p - (self.a + ba * h)).norm() - self.radius


@dataclass(frozen=True, slots=True)
class TriangleSDF:
    a: Vec2
    b: Vec2
    c: Vec2

    def value(self, p: Vec2) -> float:
        # Exact signed distance to a 2D triangle, adapted from standard IQ formulation.
        def edge_distance(pa: Vec2, pb: Vec2) -> tuple[float, float]:
            e = pb - pa
            w = p - pa
            denom = e.norm2()
            t = 0.0 if denom == 0.0 else clamp(w.dot(e) / denom, 0.0, 1.0)
            d = w - e * t
            return d.norm2(), w.cross(e)

        d1, s1 = edge_distance(self.a, self.b)
        d2, s2 = edge_distance(self.b, self.c)
        d3, s3 = edge_distance(self.c, self.a)
        area_sign = math.copysign(1.0, (self.b - self.a).cross(self.c - self.a) or 1.0)
        inside = (s1 * area_sign <= 0.0 and s2 * area_sign <= 0.0 and s3 * area_sign <= 0.0)
        d = math.sqrt(min(d1, d2, d3))
        return -d if inside else d


@dataclass(frozen=True, slots=True)
class ConeSectorField:
    """Implicit field for a finite 2D cone sector with origin, direction and range.

    This is an admission field rather than a guaranteed exact Euclidean SDF at the apex.
    Negative values indicate points inside the angular/radial sector.
    """
    origin: Vec2
    direction: float
    half_angle: float
    radius: float

    def value(self, p: Vec2) -> float:
        d = p - self.origin
        r = d.norm()
        if r == 0.0:
            angular = -self.half_angle
        else:
            theta = math.atan2(d.y, d.x)
            delta = abs((theta - self.direction + math.pi) % (2.0 * math.pi) - math.pi)
            angular = delta - self.half_angle
        radial = r - self.radius
        # max gives an intersection of angular and radial inequalities.
        return max(angular * max(r, 1.0), radial)


@dataclass(frozen=True, slots=True)
class UnionField:
    left: Field2D
    right: Field2D
    def value(self, p: Vec2) -> float:
        return min(self.left.value(p), self.right.value(p))


@dataclass(frozen=True, slots=True)
class IntersectionField:
    left: Field2D
    right: Field2D
    def value(self, p: Vec2) -> float:
        return max(self.left.value(p), self.right.value(p))


@dataclass(frozen=True, slots=True)
class DifferenceField:
    left: Field2D
    right: Field2D
    def value(self, p: Vec2) -> float:
        return max(self.left.value(p), -self.right.value(p))


@dataclass(frozen=True, slots=True)
class SmoothUnionField:
    left: Field2D
    right: Field2D
    k: float

    def value(self, p: Vec2) -> float:
        if self.k <= 0.0:
            return min(self.left.value(p), self.right.value(p))
        a, b = self.left.value(p), self.right.value(p)
        h = clamp(0.5 + 0.5 * (b - a) / self.k, 0.0, 1.0)
        return (1.0 - h) * b + h * a - self.k * h * (1.0 - h)


@dataclass(frozen=True, slots=True)
class MorphField:
    """Linear field blend used as an explicit morph parameter.

    A linear blend is useful for visualization and transition fields, but it does not
    guarantee that intermediate fields remain exact signed-distance functions.
    """
    a: Field2D
    b: Field2D
    alpha: float

    def value(self, p: Vec2) -> float:
        t = clamp(self.alpha, 0.0, 1.0)
        return (1.0 - t) * self.a.value(p) + t * self.b.value(p)


def finite_difference_gradient(field: Field2D, p: Vec2, h: float = 1e-5) -> Vec2:
    if h <= 0.0:
        raise ValueError('h must be positive')
    dx = field.value(Vec2(p.x + h, p.y)) - field.value(Vec2(p.x - h, p.y))
    dy = field.value(Vec2(p.x, p.y + h)) - field.value(Vec2(p.x, p.y - h))
    return Vec2(dx / (2.0 * h), dy / (2.0 * h))


def lens_area_equal_circles(radius: float, center_distance: float) -> float:
    """Area of overlap between two equal circles."""
    if radius <= 0.0:
        raise ValueError('radius must be positive')
    d = abs(center_distance)
    if d >= 2.0 * radius:
        return 0.0
    if d == 0.0:
        return math.pi * radius * radius
    return 2.0 * radius * radius * math.acos(d / (2.0 * radius)) - 0.5 * d * math.sqrt(4.0 * radius * radius - d * d)
