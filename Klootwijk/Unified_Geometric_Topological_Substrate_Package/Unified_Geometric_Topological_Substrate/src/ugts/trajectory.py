from __future__ import annotations

from dataclasses import dataclass
from .math2d import Vec2


@dataclass(frozen=True, slots=True)
class LinearTrajectory:
    p0: Vec2
    v0: Vec2
    t0: float = 0.0

    def position_at(self, t: float) -> Vec2:
        dt = t - self.t0
        return self.p0 + self.v0 * dt

    def velocity_at(self, t: float) -> Vec2:
        return self.v0


@dataclass(frozen=True, slots=True)
class QuadraticTrajectory:
    p0: Vec2
    v0: Vec2
    acceleration: Vec2
    t0: float = 0.0

    def position_at(self, t: float) -> Vec2:
        dt = t - self.t0
        return self.p0 + self.v0 * dt + self.acceleration * (0.5 * dt * dt)

    def velocity_at(self, t: float) -> Vec2:
        dt = t - self.t0
        return self.v0 + self.acceleration * dt
