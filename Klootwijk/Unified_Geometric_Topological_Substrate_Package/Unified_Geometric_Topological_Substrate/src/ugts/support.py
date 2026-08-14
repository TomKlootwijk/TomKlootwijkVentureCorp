from __future__ import annotations

from dataclasses import dataclass
import math

from .math2d import Vec2, angle_distance
from .state import EntityState


@dataclass(frozen=True, slots=True)
class RadialAngularSupport:
    origin: Vec2 = Vec2(0.0, 0.0)
    r_min: float = 0.0
    r_max: float = math.inf
    theta_center: float = 0.0
    theta_half_width: float = math.pi
    time_min: float = -math.inf
    time_max: float = math.inf

    def __post_init__(self) -> None:
        if self.r_min < 0.0 or self.r_max < self.r_min:
            raise ValueError('Invalid radial interval')
        if not (0.0 <= self.theta_half_width <= math.pi):
            raise ValueError('theta_half_width must lie in [0, pi]')
        if self.time_max < self.time_min:
            raise ValueError('Invalid time interval')

    def contains_point(self, point: Vec2, t: float) -> bool:
        if not (self.time_min <= t <= self.time_max):
            return False
        d = point - self.origin
        r = d.norm()
        if not (self.r_min <= r <= self.r_max):
            return False
        if r == 0.0 or self.theta_half_width >= math.pi:
            return True
        theta = math.atan2(d.y, d.x)
        return angle_distance(theta, self.theta_center) <= self.theta_half_width

    def contains(self, state: EntityState) -> bool:
        return self.contains_point(state.position, state.time)
