from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

EPS = 1e-9
TAU = 2.0 * math.pi


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vec2':
        return Vec2(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> 'Vec2':
        if abs(scalar) < EPS:
            raise ZeroDivisionError('Vec2 division by a near-zero scalar')
        return Vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: 'Vec2') -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: 'Vec2') -> float:
        return self.x * other.y - self.y * other.x

    def norm2(self) -> float:
        return self.dot(self)

    def norm(self) -> float:
        return math.sqrt(self.norm2())

    def normalized(self) -> 'Vec2':
        n = self.norm()
        if n < EPS:
            raise ValueError('Cannot normalize a near-zero vector')
        return self / n

    def rotate(self, angle: float) -> 'Vec2':
        c, s = math.cos(angle), math.sin(angle)
        return Vec2(c * self.x - s * self.y, s * self.x + c * self.y)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    @classmethod
    def from_iterable(cls, values: Iterable[float]) -> 'Vec2':
        x, y = values
        return cls(float(x), float(y))


def clamp(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value


def wrap_angle(angle: float) -> float:
    """Wrap an angle to [-pi, pi)."""
    return (angle + math.pi) % TAU - math.pi


def angle_distance(a: float, b: float) -> float:
    return abs(wrap_angle(a - b))


def solve_quadratic(a: float, b: float, c: float, *, eps: float = EPS) -> list[float]:
    """Return sorted real roots with near-duplicate roots merged."""
    if abs(a) < eps:
        if abs(b) < eps:
            return []
        return [-c / b]
    disc = b * b - 4.0 * a * c
    if disc < -eps:
        return []
    if abs(disc) <= eps:
        return [-b / (2.0 * a)]
    sqrt_disc = math.sqrt(max(0.0, disc))
    # Stable quadratic evaluation.
    q = -0.5 * (b + math.copysign(sqrt_disc, b))
    if abs(q) < eps:
        roots = [(-b - sqrt_disc) / (2.0 * a), (-b + sqrt_disc) / (2.0 * a)]
    else:
        roots = [q / a, c / q]
    roots.sort()
    if len(roots) == 2 and abs(roots[0] - roots[1]) <= eps:
        return [(roots[0] + roots[1]) * 0.5]
    return roots
