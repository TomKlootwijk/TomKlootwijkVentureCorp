from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Iterable

from .math2d import TAU, Vec2, clamp


@dataclass(frozen=True, slots=True)
class LogPolarPoint:
    rho: float
    theta: float
    is_core: bool = False


def to_log_polar(p: Vec2, *, origin: Vec2 = Vec2(0.0, 0.0), r_reference: float = 1.0, epsilon: float = 1e-9) -> LogPolarPoint:
    if r_reference <= 0.0 or epsilon <= 0.0:
        raise ValueError('r_reference and epsilon must be positive')
    d = p - origin
    r = d.norm()
    is_core = r < epsilon
    r_safe = max(r, epsilon)
    return LogPolarPoint(math.log(r_safe / r_reference), math.atan2(d.y, d.x), is_core)


def from_log_polar(lp: LogPolarPoint, *, origin: Vec2 = Vec2(0.0, 0.0), r_reference: float = 1.0) -> Vec2:
    if r_reference <= 0.0:
        raise ValueError('r_reference must be positive')
    r = r_reference * math.exp(lp.rho)
    return origin + Vec2(r * math.cos(lp.theta), r * math.sin(lp.theta))


@dataclass(slots=True)
class LogPolarLUT:
    rho_min: float
    rho_max: float
    rho_bins: int
    theta_bins: int
    bits: bytearray = field(init=False)

    def __post_init__(self) -> None:
        if self.rho_max <= self.rho_min:
            raise ValueError('rho_max must exceed rho_min')
        if self.rho_bins <= 0 or self.theta_bins <= 0:
            raise ValueError('bin counts must be positive')
        self.bits = bytearray((self.rho_bins * self.theta_bins + 7) // 8)

    def _flat_index(self, rho_index: int, theta_index: int) -> int:
        if not (0 <= rho_index < self.rho_bins):
            raise IndexError('rho_index out of range')
        if not (0 <= theta_index < self.theta_bins):
            raise IndexError('theta_index out of range')
        return rho_index * self.theta_bins + theta_index

    def _bit_location(self, flat_index: int) -> tuple[int, int]:
        return flat_index >> 3, flat_index & 7

    def set_bin(self, rho_index: int, theta_index: int, active: bool = True) -> None:
        flat = self._flat_index(rho_index, theta_index)
        byte_i, bit_i = self._bit_location(flat)
        mask = 1 << bit_i
        if active:
            self.bits[byte_i] |= mask
        else:
            self.bits[byte_i] &= ~mask

    def get_bin(self, rho_index: int, theta_index: int) -> bool:
        flat = self._flat_index(rho_index, theta_index)
        byte_i, bit_i = self._bit_location(flat)
        return bool(self.bits[byte_i] & (1 << bit_i))

    def quantize(self, lp: LogPolarPoint) -> tuple[int, int] | None:
        if not (self.rho_min <= lp.rho <= self.rho_max):
            return None
        u = (lp.rho - self.rho_min) / (self.rho_max - self.rho_min)
        rho_i = min(self.rho_bins - 1, int(u * self.rho_bins))
        theta = lp.theta % TAU
        theta_i = min(self.theta_bins - 1, int(theta / TAU * self.theta_bins))
        return rho_i, theta_i

    def set_point(self, lp: LogPolarPoint, active: bool = True) -> bool:
        idx = self.quantize(lp)
        if idx is None:
            return False
        self.set_bin(*idx, active=active)
        return True

    def is_active(self, lp: LogPolarPoint) -> bool:
        idx = self.quantize(lp)
        return False if idx is None else self.get_bin(*idx)

    def active_count(self) -> int:
        return sum(byte.bit_count() for byte in self.bits)

    @property
    def storage_bytes(self) -> int:
        return len(self.bits)

    def fill(self, predicate) -> None:
        """Fill bins whose center satisfies predicate(LogPolarPoint)->bool."""
        for i in range(self.rho_bins):
            rho = self.rho_min + (i + 0.5) / self.rho_bins * (self.rho_max - self.rho_min)
            for j in range(self.theta_bins):
                theta = (j + 0.5) / self.theta_bins * TAU - math.pi
                self.set_bin(i, j, bool(predicate(LogPolarPoint(rho, theta))))
