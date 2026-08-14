from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from .math2d import TAU, Vec2


def radix_digit_count(value: int, base: int = 2) -> int:
    """Return the number of positional digits required for a nonnegative integer.

    Zero is represented by one digit. This function keeps value, offset and ordinal
    semantics separate; it does not reinterpret arithmetic through zero-based indexing.
    """
    if value < 0:
        raise ValueError('value must be nonnegative')
    if base < 2:
        raise ValueError('base must be at least 2')
    if value == 0:
        return 1
    count = 0
    n = value
    while n:
        n //= base
        count += 1
    return count


def radix_thresholds(base: int, maximum: int) -> list[int]:
    """Return powers of *base* at which a new digit is required, up to maximum."""
    if base < 2:
        raise ValueError('base must be at least 2')
    if maximum < 1:
        return []
    out: list[int] = []
    value = base
    while value <= maximum:
        out.append(value)
        value *= base
    return out


def zero_based_ordinal(index: int) -> int:
    """Translate a zero-based index into the corresponding one-based ordinal."""
    if index < 0:
        raise ValueError('index must be nonnegative')
    return index + 1


def active_bit_positions(value: int) -> tuple[int, ...]:
    """Return set-bit positions, most significant first."""
    if value < 0:
        raise ValueError('value must be nonnegative')
    return tuple(i for i in range(value.bit_length() - 1, -1, -1) if value & (1 << i))


def hamming_weight(value: int) -> int:
    if value < 0:
        raise ValueError('value must be nonnegative')
    return value.bit_count()


def pascal_entry_is_odd(row: int, column: int) -> bool:
    """Lucas-theorem parity test for binomial(row, column)."""
    if row < 0 or column < 0 or column > row:
        return False
    return (column & ~row) == 0


def pascal_parity_rows(rows: int) -> list[list[int]]:
    if rows < 0:
        raise ValueError('rows must be nonnegative')
    return [[1 if pascal_entry_is_odd(n, k) else 0 for k in range(n + 1)] for n in range(rows)]


def sierpinski_bit(x: int, y: int) -> int:
    """Return a deterministic Sierpinski/Pascal-parity sample.

    For a triangular grid, x is the column and y is the zero-based row.
    """
    if x < 0 or y < 0:
        return 0
    return 1 if pascal_entry_is_odd(y, x) else 0


def golden_angle_points(count: int, radius: float = 1.0) -> list[Vec2]:
    """Generate a Vogel/golden-angle disk schedule.

    This is an optional low-regularity sample schedule, not a guarantee of zero aliasing.
    """
    if count < 0:
        raise ValueError('count must be nonnegative')
    if radius < 0.0:
        raise ValueError('radius must be nonnegative')
    if count == 0:
        return []
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    return [
        Vec2(
            radius * math.sqrt((i + 0.5) / count) * math.cos(i * golden_angle),
            radius * math.sqrt((i + 0.5) / count) * math.sin(i * golden_angle),
        )
        for i in range(count)
    ]


@dataclass(frozen=True, slots=True)
class ActiveBitTriangle:
    """A chosen 2D triangle embedding of exactly three active bit positions."""

    bit_positions: tuple[int, int, int]
    points: tuple[Vec2, Vec2, Vec2]


def active_bits_triangle(value: int) -> ActiveBitTriangle:
    positions = active_bit_positions(value)
    if len(positions) != 3:
        raise ValueError('value must have exactly three active bits')
    weights = [float(1 << p) for p in positions]
    wmax = max(weights)
    # Preserve a visible non-collinear simplex while encoding relative bit weight.
    points = (
        Vec2(weights[0] / wmax, 0.0),
        Vec2(0.0, weights[1] / wmax + 0.5),
        Vec2(0.0, -weights[2] / wmax - 0.5),
    )
    return ActiveBitTriangle(
        bit_positions=(positions[0], positions[1], positions[2]),
        points=(points[0], points[1], points[2]),
    )
