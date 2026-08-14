from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, FrozenSet, Mapping, Protocol, Sequence

from .math2d import Vec2


class Trajectory(Protocol):
    t0: float
    def position_at(self, t: float) -> Vec2: ...
    def velocity_at(self, t: float) -> Vec2: ...


@dataclass(frozen=True, slots=True)
class StatePatch:
    effective_time: float
    sheet: int | None = None
    orientation: int | None = None
    phase_delta: float = 0.0
    branch: str | None = None
    add_tags: FrozenSet[str] = frozenset()
    remove_tags: FrozenSet[str] = frozenset()
    lineage_note: str | None = None


@dataclass(frozen=True, slots=True)
class EntityState:
    entity_id: str
    time: float
    position: Vec2
    velocity: Vec2
    phase: float
    sheet: int
    orientation: int
    branch: str
    lineage: tuple[str, ...]
    tags: FrozenSet[str] = frozenset()
    uncertainty: float = 0.0
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def with_updates(self, **kwargs: Any) -> 'EntityState':
        return replace(self, **kwargs)


@dataclass(slots=True)
class Entity:
    entity_id: str
    trajectory: Trajectory
    phase0: float = 0.0
    phase_rate: float = 0.0
    sheet0: int = 0
    orientation0: int = 1
    branch0: str = 'A'
    lineage0: tuple[str, ...] = ()
    tags0: FrozenSet[str] = frozenset()
    uncertainty: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    patches: list[StatePatch] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.orientation0 not in (-1, 1):
            raise ValueError('orientation0 must be -1 or 1')
        if self.sheet0 < 0:
            raise ValueError('sheet0 must be nonnegative')
        if not self.lineage0:
            self.lineage0 = (self.entity_id,)

    def add_patch(self, patch: StatePatch) -> None:
        self.patches.append(patch)
        self.patches.sort(key=lambda p: p.effective_time)

    def state_at(self, t: float) -> EntityState:
        if t < self.trajectory.t0:
            raise ValueError(f't={t} precedes trajectory start t0={self.trajectory.t0}')
        phase = self.phase0 + self.phase_rate * (t - self.trajectory.t0)
        sheet = self.sheet0
        orientation = self.orientation0
        branch = self.branch0
        lineage = list(self.lineage0)
        tags = set(self.tags0)
        for patch in self.patches:
            if patch.effective_time > t:
                break
            if patch.sheet is not None:
                sheet = patch.sheet
            if patch.orientation is not None:
                orientation = patch.orientation
            phase += patch.phase_delta
            if patch.branch is not None:
                branch = patch.branch
            tags.update(patch.add_tags)
            tags.difference_update(patch.remove_tags)
            if patch.lineage_note:
                lineage.append(patch.lineage_note)
        return EntityState(
            entity_id=self.entity_id,
            time=t,
            position=self.trajectory.position_at(t),
            velocity=self.trajectory.velocity_at(t),
            phase=phase,
            sheet=sheet,
            orientation=orientation,
            branch=branch,
            lineage=tuple(lineage),
            tags=frozenset(tags),
            uncertainty=self.uncertainty,
            metadata=self.metadata,
        )


@dataclass(frozen=True, slots=True)
class EventRecord:
    event_id: str
    entity_id: str
    rule_id: str
    time: float
    state_before: EntityState
    state_after: EntityState | None
    relation_value: float
    crossing_direction: int
    confidence: float
    solver: str
    lineage: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
