"""Restricted Equation World Zero reference prototype.

This code demonstrates the corpus's mature, bounded interpretation:
closed-form state evaluation, analytic event roots for a restricted relation family,
local support, compatibility gating, narrow parity routing, and lineage logging.

It is deliberately not a renderer, general physics engine, topology proof, or
universal constant-time solver.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace, asdict
from hashlib import sha256
from math import atan2, cos, pi, sin, sqrt
from typing import Iterable, Protocol, Sequence
import json

EPS = 1e-10


def _wrap_angle(x: float) -> float:
    """Wrap an angle to (-pi, pi]."""
    while x <= -pi:
        x += 2.0 * pi
    while x > pi:
        x -= 2.0 * pi
    return x


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class Trajectory2D:
    """Constant-velocity trajectory and linear phase schedule."""

    x0: float
    y0: float
    vx: float
    vy: float
    phase0: float = 0.0
    phase_rate: float = 0.0

    def position_at(self, t: float) -> tuple[float, float]:
        return (self.x0 + self.vx * t, self.y0 + self.vy * t)

    def phase_at(self, t: float) -> float:
        return _wrap_angle(self.phase0 + self.phase_rate * t)


@dataclass(frozen=True)
class Entity:
    entity_id: str
    trajectory: Trajectory2D
    sheet: int
    address: str
    branch: str = "root"
    parity: int = 0
    invariant_tags: tuple[str, ...] = ()
    state_variables: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class State:
    entity_id: str
    time: float
    position: tuple[float, float]
    phase: float
    sheet: int
    address: str
    branch: str
    parity: int
    invariant_tags: tuple[str, ...]
    state_variables: dict[str, object]

    @property
    def digest(self) -> str:
        return stable_hash(asdict(self))


@dataclass(frozen=True)
class SupportSector:
    """A 2D local radial-angular support (annular sector)."""

    origin: tuple[float, float] = (0.0, 0.0)
    r_min: float = 0.0
    r_max: float = float("inf")
    theta_center: float = 0.0
    theta_half_width: float = pi
    t_min: float = float("-inf")
    t_max: float = float("inf")

    def contains(self, state: State) -> bool:
        if not (self.t_min - EPS <= state.time <= self.t_max + EPS):
            return False
        dx = state.position[0] - self.origin[0]
        dy = state.position[1] - self.origin[1]
        radius = sqrt(dx * dx + dy * dy)
        if not (self.r_min - EPS <= radius <= self.r_max + EPS):
            return False
        if self.theta_half_width >= pi - EPS:
            return True
        theta = atan2(dy, dx)
        return abs(_wrap_angle(theta - self.theta_center)) <= self.theta_half_width + EPS


@dataclass(frozen=True)
class CompatibilityResult:
    compatible: bool
    reason_codes: tuple[str, ...]
    predicate_version: str = "chi-v0.1"


@dataclass(frozen=True)
class CompatibilityPolicy:
    allowed_sheets: tuple[int, ...] = (0, 1)
    target_phase: float | None = None
    phase_tolerance: float = pi
    required_tags: tuple[str, ...] = ()
    predicate_version: str = "chi-v0.1"

    def evaluate(self, state: State) -> CompatibilityResult:
        reasons: list[str] = []
        if state.sheet not in self.allowed_sheets:
            reasons.append("SHEET_MISMATCH")
        if self.target_phase is not None:
            if abs(_wrap_angle(state.phase - self.target_phase)) > self.phase_tolerance + EPS:
                reasons.append("PHASE_OUTSIDE_TOLERANCE")
        missing = [tag for tag in self.required_tags if tag not in state.invariant_tags]
        if missing:
            reasons.append("REQUIRED_TAG_MISSING")
        return CompatibilityResult(not reasons, tuple(reasons), self.predicate_version)


class Relation(Protocol):
    relation_id: str
    policy: CompatibilityPolicy
    support: SupportSector

    def value_at(self, trajectory: Trajectory2D, t: float) -> float: ...
    def roots_after(self, trajectory: Trajectory2D, t0: float) -> list[float]: ...


@dataclass(frozen=True)
class LineRelation:
    """Implicit line n_x x + n_y y + c = 0."""

    relation_id: str
    nx: float
    ny: float
    c: float
    support: SupportSector = field(default_factory=SupportSector)
    policy: CompatibilityPolicy = field(default_factory=CompatibilityPolicy)

    def value_at(self, trajectory: Trajectory2D, t: float) -> float:
        x, y = trajectory.position_at(t)
        return self.nx * x + self.ny * y + self.c

    def roots_after(self, trajectory: Trajectory2D, t0: float) -> list[float]:
        a = self.nx * trajectory.vx + self.ny * trajectory.vy
        b = self.nx * trajectory.x0 + self.ny * trajectory.y0 + self.c
        if abs(a) <= EPS:
            return []  # coincident and parallel cases are intentionally not silently ordered
        t = -b / a
        return [t] if t >= t0 - EPS else []


@dataclass(frozen=True)
class CircleRelation:
    """Implicit circle (x-cx)^2 + (y-cy)^2 - r^2 = 0."""

    relation_id: str
    cx: float
    cy: float
    radius: float
    support: SupportSector = field(default_factory=SupportSector)
    policy: CompatibilityPolicy = field(default_factory=CompatibilityPolicy)

    def value_at(self, trajectory: Trajectory2D, t: float) -> float:
        x, y = trajectory.position_at(t)
        dx = x - self.cx
        dy = y - self.cy
        return dx * dx + dy * dy - self.radius * self.radius

    def roots_after(self, trajectory: Trajectory2D, t0: float) -> list[float]:
        dx0 = trajectory.x0 - self.cx
        dy0 = trajectory.y0 - self.cy
        a = trajectory.vx * trajectory.vx + trajectory.vy * trajectory.vy
        b = 2.0 * (dx0 * trajectory.vx + dy0 * trajectory.vy)
        c = dx0 * dx0 + dy0 * dy0 - self.radius * self.radius
        if abs(a) <= EPS:
            return []
        disc = b * b - 4.0 * a * c
        if disc < -EPS:
            return []
        if abs(disc) <= EPS:
            roots = [-b / (2.0 * a)]
        else:
            s = sqrt(max(0.0, disc))
            roots = [(-b - s) / (2.0 * a), (-b + s) / (2.0 * a)]
        return sorted(t for t in roots if t >= t0 - EPS)


@dataclass(frozen=True)
class TransitionRule:
    transition_id: str
    target_sheet: int | None = None
    toggle_parity: bool = True
    create_branch: bool = False
    state_updates: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Event:
    event_id: str
    entity_id: str
    relation_id: str
    transition_id: str
    time: float
    support_admitted: bool
    compatible: bool
    compatibility_reasons: tuple[str, ...]
    predicate_version: str
    guard_crossed: bool
    root_multiplicity: int
    confidence: float
    pre_state_hash: str
    post_state_hash: str | None
    lineage_parent: str
    branch_created: str | None
    parity_before: int
    parity_after: int | None
    invariant_report: dict[str, object]


@dataclass
class World:
    relations: list[Relation]
    transitions: dict[str, TransitionRule]
    relation_to_transition: dict[str, str]
    event_log: list[Event] = field(default_factory=list)

    def state_at(self, entity: Entity, t: float) -> State:
        return State(
            entity_id=entity.entity_id,
            time=t,
            position=entity.trajectory.position_at(t),
            phase=entity.trajectory.phase_at(t),
            sheet=entity.sheet,
            address=entity.address,
            branch=entity.branch,
            parity=entity.parity,
            invariant_tags=entity.invariant_tags,
            state_variables=dict(entity.state_variables),
        )

    def next_event(self, entity: Entity, t0: float) -> Event | None:
        candidates: list[tuple[float, Relation, State, CompatibilityResult, int]] = []
        for relation in self.relations:
            roots = relation.roots_after(entity.trajectory, t0)
            for root in roots:
                state = self.state_at(entity, root)
                compatibility = relation.policy.evaluate(state)
                support_ok = relation.support.contains(state)
                guard_ok = abs(relation.value_at(entity.trajectory, root)) <= 1e-7
                if support_ok and compatibility.compatible and guard_ok:
                    multiplicity = 2 if isinstance(relation, CircleRelation) and len(roots) == 1 else 1
                    candidates.append((root, relation, state, compatibility, multiplicity))
        if not candidates:
            return None
        root, relation, state, compatibility, multiplicity = min(candidates, key=lambda item: item[0])
        transition_id = self.relation_to_transition[relation.relation_id]
        rule = self.transitions[transition_id]
        parity_after = 1 - entity.parity if rule.toggle_parity else entity.parity
        branch_created = f"{entity.branch}/{transition_id}@{root:.9g}" if rule.create_branch else None
        event_payload = {
            "entity": entity.entity_id,
            "relation": relation.relation_id,
            "transition": transition_id,
            "time": root,
            "pre": state.digest,
        }
        return Event(
            event_id=stable_hash(event_payload)[:24],
            entity_id=entity.entity_id,
            relation_id=relation.relation_id,
            transition_id=transition_id,
            time=root,
            support_admitted=True,
            compatible=True,
            compatibility_reasons=compatibility.reason_codes,
            predicate_version=compatibility.predicate_version,
            guard_crossed=True,
            root_multiplicity=multiplicity,
            confidence=1.0,
            pre_state_hash=state.digest,
            post_state_hash=None,
            lineage_parent=entity.address,
            branch_created=branch_created,
            parity_before=entity.parity,
            parity_after=parity_after,
            invariant_report={"passed": True, "checked": list(entity.invariant_tags)},
        )

    def apply_transition(self, entity: Entity, event: Event) -> Entity:
        rule = self.transitions[event.transition_id]
        new_sheet = entity.sheet if rule.target_sheet is None else rule.target_sheet
        new_parity = 1 - entity.parity if rule.toggle_parity else entity.parity
        new_branch = event.branch_created or entity.branch
        new_vars = dict(entity.state_variables)
        new_vars.update(rule.state_updates)
        lineage_payload = {
            "parent": entity.address,
            "event": event.event_id,
            "branch": new_branch,
            "sheet": new_sheet,
            "parity": new_parity,
        }
        new_address = stable_hash(lineage_payload)[:32]
        updated = replace(
            entity,
            sheet=new_sheet,
            parity=new_parity,
            branch=new_branch,
            address=new_address,
            state_variables=new_vars,
        )
        post_state = self.state_at(updated, event.time)
        committed = replace(event, post_state_hash=post_state.digest)
        self.event_log.append(committed)
        return updated

    def events_in_support(
        self,
        entities: Iterable[Entity],
        support: SupportSector,
        t0: float,
        t1: float,
    ) -> list[Event]:
        events: list[Event] = []
        for entity in entities:
            event = self.next_event(entity, t0)
            if event is None or event.time > t1 + EPS:
                continue
            state = self.state_at(entity, event.time)
            if support.contains(state):
                events.append(event)
        return sorted(events, key=lambda e: (e.time, e.entity_id, e.relation_id))


def lineage_address(seed: str, grammar_path: Sequence[str], lineage_events: Sequence[str]) -> str:
    return stable_hash({"seed": seed, "grammar_path": list(grammar_path), "events": list(lineage_events)})[:32]
