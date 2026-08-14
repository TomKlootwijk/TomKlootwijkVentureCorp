from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

from .math2d import Vec2


@dataclass(frozen=True, slots=True)
class MappedPoint:
    point: Vec2
    orientation: int
    sheet: int
    wraps: tuple[int, int] = (0, 0)


@dataclass(frozen=True, slots=True)
class MobiusBand:
    """Rectangle quotient (0,y) ~ (width,-y)."""
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0.0 or self.height <= 0.0:
            raise ValueError('width and height must be positive')

    def map(self, p: Vec2, orientation: int = 1, sheet: int = 0) -> MappedPoint:
        turns = math.floor(p.x / self.width)
        x = p.x - turns * self.width
        y = p.y
        if turns % 2:
            y = -y
            orientation = -orientation
        # Keep y in a representable strip without adding a second topological gluing.
        half = 0.5 * self.height
        y = max(-half, min(half, y))
        return MappedPoint(Vec2(x, y), orientation, sheet, (turns, 0))


@dataclass(frozen=True, slots=True)
class KleinBottleQuotient:
    """Rectangle quotient with (0,y)~(width,height-y) and (x,0)~(x,height)."""
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0.0 or self.height <= 0.0:
            raise ValueError('width and height must be positive')

    def map(self, p: Vec2, orientation: int = 1, sheet: int = 0) -> MappedPoint:
        x_turns = math.floor(p.x / self.width)
        x = p.x - x_turns * self.width
        y = p.y
        if x_turns % 2:
            y = self.height - y
            orientation = -orientation
            sheet ^= 1
        y_turns = math.floor(y / self.height)
        y = y - y_turns * self.height
        return MappedPoint(Vec2(x, y), orientation, sheet, (x_turns, y_turns))


@dataclass(frozen=True, slots=True)
class PortalMap:
    """Explicit technical form of a topological gluing/portal."""
    translation: Vec2 = Vec2(0.0, 0.0)
    rotation: float = 0.0
    scale: float = 1.0
    flip_orientation: bool = False
    sheet_delta: int = 0

    def apply(self, p: Vec2, orientation: int = 1, sheet: int = 0) -> MappedPoint:
        if self.scale == 0.0:
            raise ValueError('Portal scale cannot be zero')
        mapped = p.rotate(self.rotation) * self.scale + self.translation
        if self.flip_orientation:
            orientation = -orientation
        return MappedPoint(mapped, orientation, sheet + self.sheet_delta)


@dataclass(frozen=True, slots=True)
class HourglassRouter:
    """Finite four-chamber routing around a pinch/event locus.

    Chambers are selected by signs of two coordinates. The transition table controls
    how a crossing at the pinch routes the state. This is a discrete routing model,
    not a claim that a physical singularity exists.
    """
    transition_table: Mapping[tuple[str, int], str] | None = None
    epsilon: float = 1e-9

    def chamber(self, u: float, v: float) -> str:
        if abs(u) <= self.epsilon and abs(v) <= self.epsilon:
            return 'PINCH'
        if u >= 0.0 and v >= 0.0:
            return 'A'
        if u < 0.0 <= v:
            return 'B'
        if u < 0.0 and v < 0.0:
            return 'C'
        return 'D'

    def route(self, current: str, parity: int) -> str:
        if parity not in (0, 1):
            raise ValueError('parity must be 0 or 1')
        table = self.transition_table or {
            ('A', 0): 'A', ('A', 1): 'C',
            ('B', 0): 'B', ('B', 1): 'D',
            ('C', 0): 'C', ('C', 1): 'A',
            ('D', 0): 'D', ('D', 1): 'B',
            ('PINCH', 0): 'A', ('PINCH', 1): 'C',
        }
        try:
            return table[(current, parity)]
        except KeyError as exc:
            raise KeyError(f'No route for chamber={current!r}, parity={parity}') from exc
