from __future__ import annotations

from dataclasses import dataclass
import math
from typing import FrozenSet

from .math2d import angle_distance
from .state import EntityState


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    accepted: bool
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CompatibilityRule:
    allowed_sheets: FrozenSet[int] | None = None
    allowed_orientations: FrozenSet[int] | None = None
    phase_center: float | None = None
    phase_tolerance: float = math.pi
    allowed_branches: FrozenSet[str] | None = None
    required_tags: FrozenSet[str] = frozenset()
    forbidden_tags: FrozenSet[str] = frozenset()
    lineage_prefix: tuple[str, ...] | None = None

    def evaluate(self, state: EntityState) -> CompatibilityResult:
        reasons: list[str] = []
        if self.allowed_sheets is not None and state.sheet not in self.allowed_sheets:
            reasons.append('sheet_mismatch')
        if self.allowed_orientations is not None and state.orientation not in self.allowed_orientations:
            reasons.append('orientation_mismatch')
        if self.phase_center is not None and angle_distance(state.phase, self.phase_center) > self.phase_tolerance:
            reasons.append('phase_mismatch')
        if self.allowed_branches is not None and state.branch not in self.allowed_branches:
            reasons.append('branch_mismatch')
        if not self.required_tags.issubset(state.tags):
            reasons.append('missing_required_tag')
        if self.forbidden_tags.intersection(state.tags):
            reasons.append('forbidden_tag')
        if self.lineage_prefix is not None:
            n = len(self.lineage_prefix)
            if state.lineage[:n] != self.lineage_prefix:
                reasons.append('lineage_mismatch')
        return CompatibilityResult(accepted=not reasons, reason_codes=tuple(reasons))
