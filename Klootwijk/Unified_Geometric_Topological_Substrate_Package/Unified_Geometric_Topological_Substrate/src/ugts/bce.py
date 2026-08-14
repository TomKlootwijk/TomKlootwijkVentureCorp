from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Mapping


class BCEStage(Enum):
    IDLE = auto()
    ADMIT_SUPPORT = auto()
    TUNE = auto()
    MATCH_MODE = auto()
    CROSS_GUARD = auto()
    LATCHED = auto()
    REJECTED = auto()


@dataclass(frozen=True, slots=True)
class BCEMeasurement:
    time: float
    detector_value: float
    in_support: bool
    mode_ok: bool
    phase_ok: bool
    time_ok: bool = True
    policy_ok: bool = True
    confidence: float = 1.0
    uncertainty: float = 0.0
    lineage: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BCEDecision:
    accepted: bool
    stage: BCEStage
    parity: int
    reason_codes: tuple[str, ...]
    measurement: BCEMeasurement


@dataclass(slots=True)
class BCEController:
    """Bounded Compatibility Event controller.

    The parity bit is a narrow route/latch flag. Detector amplitude, uncertainty,
    confidence and lineage remain separate state.
    """

    threshold: float
    rising: bool = True
    minimum_confidence: float = 0.0
    parity: int = 0
    previous_value: float | None = None

    def __post_init__(self) -> None:
        if self.parity not in (0, 1):
            raise ValueError('parity must be 0 or 1')
        if not (0.0 <= self.minimum_confidence <= 1.0):
            raise ValueError('minimum_confidence must be in [0,1]')

    def _guard_crossed(self, current: float) -> bool:
        if self.previous_value is None:
            return False
        if self.rising:
            return self.previous_value < self.threshold <= current
        return self.previous_value > self.threshold >= current

    def evaluate(self, measurement: BCEMeasurement) -> BCEDecision:
        reasons: list[str] = []
        if not measurement.in_support:
            reasons.append('outside_support')
        if not measurement.mode_ok:
            reasons.append('mode_mismatch')
        if not measurement.phase_ok:
            reasons.append('phase_mismatch')
        if not measurement.time_ok:
            reasons.append('outside_time_window')
        if not measurement.policy_ok:
            reasons.append('policy_rejected')
        if measurement.confidence < self.minimum_confidence:
            reasons.append('confidence_below_minimum')

        guard = self._guard_crossed(measurement.detector_value)
        self.previous_value = measurement.detector_value
        if reasons:
            return BCEDecision(False, BCEStage.REJECTED, self.parity, tuple(reasons), measurement)
        if not guard:
            return BCEDecision(False, BCEStage.CROSS_GUARD, self.parity, ('guard_not_crossed',), measurement)
        self.parity ^= 1
        return BCEDecision(True, BCEStage.LATCHED, self.parity, (), measurement)
