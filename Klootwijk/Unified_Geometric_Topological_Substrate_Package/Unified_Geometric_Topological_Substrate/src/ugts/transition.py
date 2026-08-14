from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from .state import EntityState, StatePatch


@dataclass(frozen=True, slots=True)
class TransitionRule:
    toggle_sheet: bool = False
    sheet_modulus: int = 2
    set_sheet: int | None = None
    flip_orientation: bool = False
    phase_delta: float = 0.0
    set_branch: str | None = None
    add_tags: FrozenSet[str] = frozenset()
    remove_tags: FrozenSet[str] = frozenset()
    lineage_label: str | None = None

    def __post_init__(self) -> None:
        if self.sheet_modulus < 1:
            raise ValueError('sheet_modulus must be positive')
        if self.set_sheet is not None and self.set_sheet < 0:
            raise ValueError('set_sheet must be nonnegative')

    def patch_for(self, state: EntityState, effective_time: float, rule_id: str) -> StatePatch:
        if self.set_sheet is not None:
            new_sheet = self.set_sheet
        elif self.toggle_sheet:
            new_sheet = (state.sheet + 1) % self.sheet_modulus
        else:
            new_sheet = None
        new_orientation = -state.orientation if self.flip_orientation else None
        label = self.lineage_label or f'{rule_id}@{effective_time:.9g}'
        return StatePatch(
            effective_time=effective_time,
            sheet=new_sheet,
            orientation=new_orientation,
            phase_delta=self.phase_delta,
            branch=self.set_branch,
            add_tags=self.add_tags,
            remove_tags=self.remove_tags,
            lineage_note=label,
        )
