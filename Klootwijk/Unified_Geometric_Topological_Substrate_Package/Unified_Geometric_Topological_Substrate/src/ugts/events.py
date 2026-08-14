from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Callable, Protocol, Sequence

from .compatibility import CompatibilityRule, CompatibilityResult
from .geometry import Field2D
from .math2d import EPS, Vec2, solve_quadratic
from .state import Entity, EntityState
from .support import RadialAngularSupport
from .trajectory import LinearTrajectory, QuadraticTrajectory
from .transition import TransitionRule


class EventSurface(Protocol):
    name: str
    solver_name: str
    def value_at(self, entity: Entity, t: float) -> float: ...
    def candidate_times(self, entity: Entity, t0: float, t1: float) -> list[float]: ...


@dataclass(frozen=True, slots=True)
class LineSurface:
    normal: Vec2
    offset: float = 0.0
    name: str = 'line'
    solver_name: str = 'analytic_quadratic'

    def __post_init__(self) -> None:
        if self.normal.norm2() < EPS:
            raise ValueError('Line normal must be nonzero')

    def value_at(self, entity: Entity, t: float) -> float:
        return self.normal.dot(entity.trajectory.position_at(t)) - self.offset

    def candidate_times(self, entity: Entity, t0: float, t1: float) -> list[float]:
        tr = entity.trajectory
        if isinstance(tr, LinearTrajectory):
            a = 0.0
            b = self.normal.dot(tr.v0)
            c = self.normal.dot(tr.p0) - self.offset
        elif isinstance(tr, QuadraticTrajectory):
            a = 0.5 * self.normal.dot(tr.acceleration)
            b = self.normal.dot(tr.v0)
            c = self.normal.dot(tr.p0) - self.offset
        else:
            raise TypeError('LineSurface supports LinearTrajectory or QuadraticTrajectory')
        roots_dt = solve_quadratic(a, b, c)
        roots = [tr.t0 + dt for dt in roots_dt]
        return [t for t in roots if t0 - EPS <= t <= t1 + EPS]


@dataclass(frozen=True, slots=True)
class CircleSurface:
    center: Vec2
    radius: float
    name: str = 'circle'
    solver_name: str = 'analytic_quadratic_linear_trajectory'

    def __post_init__(self) -> None:
        if self.radius <= 0.0:
            raise ValueError('radius must be positive')

    def value_at(self, entity: Entity, t: float) -> float:
        d = entity.trajectory.position_at(t) - self.center
        return d.norm2() - self.radius * self.radius

    def candidate_times(self, entity: Entity, t0: float, t1: float) -> list[float]:
        tr = entity.trajectory
        if not isinstance(tr, LinearTrajectory):
            raise TypeError('CircleSurface analytic roots currently require LinearTrajectory')
        q = tr.p0 - self.center
        a = tr.v0.norm2()
        b = 2.0 * q.dot(tr.v0)
        c = q.norm2() - self.radius * self.radius
        roots = [tr.t0 + dt for dt in solve_quadratic(a, b, c)]
        return [t for t in roots if t0 - EPS <= t <= t1 + EPS]


@dataclass(frozen=True, slots=True)
class GenericFieldSurface:
    field: Field2D
    name: str = 'generic_field'
    samples: int = 256
    tolerance: float = 1e-8
    max_iterations: int = 80
    solver_name: str = 'sampled_bracket_bisection'

    def value_at(self, entity: Entity, t: float) -> float:
        return self.field.value(entity.trajectory.position_at(t))

    def _bisect(self, entity: Entity, a: float, b: float, fa: float, fb: float) -> float:
        if abs(fa) <= self.tolerance:
            return a
        if abs(fb) <= self.tolerance:
            return b
        if fa * fb > 0.0:
            raise ValueError('Bisection requires a sign-changing bracket')
        lo, hi = a, b
        flo, fhi = fa, fb
        for _ in range(self.max_iterations):
            mid = 0.5 * (lo + hi)
            fm = self.value_at(entity, mid)
            if abs(fm) <= self.tolerance or abs(hi - lo) <= self.tolerance:
                return mid
            if flo * fm <= 0.0:
                hi, fhi = mid, fm
            else:
                lo, flo = mid, fm
        return 0.5 * (lo + hi)

    def candidate_times(self, entity: Entity, t0: float, t1: float) -> list[float]:
        if self.samples < 2:
            raise ValueError('samples must be at least 2')
        if t1 <= t0:
            return []
        roots: list[float] = []
        dt = (t1 - t0) / self.samples
        ta = t0
        fa = self.value_at(entity, ta)
        for i in range(1, self.samples + 1):
            tb = t0 + i * dt
            fb = self.value_at(entity, tb)
            if abs(fa) <= self.tolerance:
                roots.append(ta)
            if fa * fb < 0.0:
                roots.append(self._bisect(entity, ta, tb, fa, fb))
            ta, fa = tb, fb
        if abs(fa) <= self.tolerance:
            roots.append(t1)
        roots.sort()
        deduped: list[float] = []
        for root in roots:
            if not deduped or abs(root - deduped[-1]) > max(self.tolerance * 10.0, EPS):
                deduped.append(root)
        return deduped


Guard = Callable[[EntityState], bool]


@dataclass(frozen=True, slots=True)
class EventRule:
    rule_id: str
    surface: EventSurface
    support: RadialAngularSupport | None = None
    compatibility: CompatibilityRule = CompatibilityRule()
    transition: TransitionRule = TransitionRule()
    guard: Guard | None = None
    enabled: bool = True
    confidence: float = 1.0
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EventCandidate:
    rule: EventRule
    time: float
    state: EntityState
    relation_value: float
    crossing_direction: int
    compatibility: CompatibilityResult


class EventSolver:
    def __init__(self, *, time_epsilon: float = 1e-8, probe_dt: float = 1e-6) -> None:
        if time_epsilon <= 0.0 or probe_dt <= 0.0:
            raise ValueError('time_epsilon and probe_dt must be positive')
        self.time_epsilon = time_epsilon
        self.probe_dt = probe_dt

    def _direction(self, entity: Entity, surface: EventSurface, t: float) -> int:
        before_t = max(entity.trajectory.t0, t - self.probe_dt)
        after_t = t + self.probe_dt
        vb = surface.value_at(entity, before_t)
        va = surface.value_at(entity, after_t)
        delta = va - vb
        return 1 if delta > 0.0 else -1 if delta < 0.0 else 0

    def candidates(self, entity: Entity, rules: Sequence[EventRule], t0: float, t1: float) -> list[EventCandidate]:
        if t1 < t0:
            raise ValueError('t1 must be >= t0')
        out: list[EventCandidate] = []
        lower = t0 + self.time_epsilon
        for rule in rules:
            if not rule.enabled:
                continue
            for t in rule.surface.candidate_times(entity, lower, t1):
                if t < lower or t > t1 + self.time_epsilon:
                    continue
                state = entity.state_at(t)
                if rule.support is not None and not rule.support.contains(state):
                    continue
                comp = rule.compatibility.evaluate(state)
                if not comp.accepted:
                    continue
                if rule.guard is not None and not rule.guard(state):
                    continue
                out.append(EventCandidate(
                    rule=rule,
                    time=t,
                    state=state,
                    relation_value=rule.surface.value_at(entity, t),
                    crossing_direction=self._direction(entity, rule.surface, t),
                    compatibility=comp,
                ))
        out.sort(key=lambda c: (c.time, c.rule.rule_id))
        return out

    def next_event(self, entity: Entity, rules: Sequence[EventRule], t0: float, t1: float) -> EventCandidate | None:
        candidates = self.candidates(entity, rules, t0, t1)
        return candidates[0] if candidates else None
