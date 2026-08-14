from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from typing import Iterable

from .compatibility import CompatibilityRule, CompatibilityResult
from .events import EventCandidate, EventRule, EventSolver
from .state import Entity, EntityState, EventRecord
from .support import RadialAngularSupport


@dataclass(slots=True)
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    rules: list[EventRule] = field(default_factory=list)
    solver: EventSolver = field(default_factory=EventSolver)
    event_log: list[EventRecord] = field(default_factory=list)
    schema_version: str = '1.0.0'

    def add_entity(self, entity: Entity) -> None:
        if entity.entity_id in self.entities:
            raise KeyError(f'Duplicate entity id: {entity.entity_id}')
        self.entities[entity.entity_id] = entity

    def add_rule(self, rule: EventRule) -> None:
        if any(r.rule_id == rule.rule_id for r in self.rules):
            raise KeyError(f'Duplicate rule id: {rule.rule_id}')
        self.rules.append(rule)

    def state_at(self, entity_id: str, t: float) -> EntityState:
        return self.entities[entity_id].state_at(t)

    def next_event(self, entity_id: str, t0: float, t1: float) -> EventCandidate | None:
        return self.solver.next_event(self.entities[entity_id], self.rules, t0, t1)

    def process_next_event(self, entity_id: str, t0: float, t1: float) -> EventRecord | None:
        entity = self.entities[entity_id]
        candidate = self.solver.next_event(entity, self.rules, t0, t1)
        if candidate is None:
            return None
        before = candidate.state
        patch = candidate.rule.transition.patch_for(before, candidate.time, candidate.rule.rule_id)
        entity.add_patch(patch)
        after = entity.state_at(candidate.time)
        serial = len(self.event_log)
        digest = hashlib.sha256(
            f'{self.schema_version}|{entity_id}|{candidate.rule.rule_id}|{candidate.time:.17g}|{serial}'.encode('utf-8')
        ).hexdigest()[:16]
        record = EventRecord(
            event_id=f'evt_{digest}',
            entity_id=entity_id,
            rule_id=candidate.rule.rule_id,
            time=candidate.time,
            state_before=before,
            state_after=after,
            relation_value=candidate.relation_value,
            crossing_direction=candidate.crossing_direction,
            confidence=candidate.rule.confidence,
            solver=candidate.rule.surface.solver_name,
            lineage=after.lineage,
            reason_codes=candidate.compatibility.reason_codes,
            metadata=candidate.rule.metadata,
        )
        self.event_log.append(record)
        return record

    def events_in_support(self, support: RadialAngularSupport, t0: float, t1: float) -> list[EventCandidate]:
        out: list[EventCandidate] = []
        for entity in self.entities.values():
            for candidate in self.solver.candidates(entity, self.rules, t0, t1):
                if support.contains(candidate.state):
                    out.append(candidate)
        out.sort(key=lambda c: (c.time, c.state.entity_id, c.rule.rule_id))
        return out

    def can_couple(
        self,
        entity_a: str,
        entity_b: str,
        t: float,
        *,
        max_distance: float = 1e-6,
        phase_tolerance: float = 1e-6,
        require_same_sheet: bool = True,
        require_same_orientation: bool = False,
    ) -> CompatibilityResult:
        a = self.state_at(entity_a, t)
        b = self.state_at(entity_b, t)
        reasons: list[str] = []
        if (a.position - b.position).norm() > max_distance:
            reasons.append('not_co_located')
        if require_same_sheet and a.sheet != b.sheet:
            reasons.append('sheet_mismatch')
        if require_same_orientation and a.orientation != b.orientation:
            reasons.append('orientation_mismatch')
        # Circular phase difference without importing a second rule object.
        from .math2d import angle_distance
        if angle_distance(a.phase, b.phase) > phase_tolerance:
            reasons.append('phase_mismatch')
        return CompatibilityResult(not reasons, tuple(reasons))

    def reconstruct_identity(self, entity_id: str) -> tuple[str, ...]:
        entity = self.entities[entity_id]
        if self.event_log:
            latest_t = max((e.time for e in self.event_log if e.entity_id == entity_id), default=entity.trajectory.t0)
        else:
            latest_t = entity.trajectory.t0
        return entity.state_at(latest_t).lineage
