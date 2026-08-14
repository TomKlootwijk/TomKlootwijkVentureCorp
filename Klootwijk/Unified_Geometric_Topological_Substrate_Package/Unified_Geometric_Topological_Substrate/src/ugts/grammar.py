from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Mapping, Sequence

from .geometry import Field2D, UnionField
from .math2d import Vec2


class GrammarError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Production:
    symbol: str
    replacement: tuple[str, ...]


@dataclass(slots=True)
class FiniteGrammar:
    """Finite, budgeted string grammar.

    It intentionally refuses unbounded expansion: max_depth and max_symbols are part of
    the grammar contract and make recursion an inspectable data-generation mechanism.
    """

    axiom: tuple[str, ...]
    productions: dict[str, tuple[str, ...]] = field(default_factory=dict)
    max_depth: int = 8
    max_symbols: int = 100_000

    def __post_init__(self) -> None:
        if self.max_depth < 0:
            raise GrammarError('max_depth must be nonnegative')
        if self.max_symbols < 1:
            raise GrammarError('max_symbols must be positive')

    @classmethod
    def from_productions(
        cls,
        axiom: Sequence[str],
        productions: Iterable[Production],
        *,
        max_depth: int = 8,
        max_symbols: int = 100_000,
    ) -> 'FiniteGrammar':
        table: dict[str, tuple[str, ...]] = {}
        for production in productions:
            if production.symbol in table:
                raise GrammarError(f'duplicate production for {production.symbol!r}')
            table[production.symbol] = production.replacement
        return cls(tuple(axiom), table, max_depth=max_depth, max_symbols=max_symbols)

    def expand(self, depth: int | None = None) -> tuple[str, ...]:
        target_depth = self.max_depth if depth is None else depth
        if target_depth < 0 or target_depth > self.max_depth:
            raise GrammarError(f'depth must be in [0, {self.max_depth}]')
        current = self.axiom
        if len(current) > self.max_symbols:
            raise GrammarError('axiom exceeds max_symbols')
        for _ in range(target_depth):
            next_symbols: list[str] = []
            for symbol in current:
                replacement = self.productions.get(symbol, (symbol,))
                next_symbols.extend(replacement)
                if len(next_symbols) > self.max_symbols:
                    raise GrammarError('grammar expansion exceeded max_symbols')
            current = tuple(next_symbols)
        return current


PrimitiveFactory = Callable[[Vec2, float], Field2D]


@dataclass(slots=True)
class ShapeGrammarCompiler:
    """Compile a finite token stream into an implicit union of placed primitives.

    Tokens `+`, `-`, `[`, and `]` perform simple 2D turtle rotation and stack control.
    Registered primitive tokens emit fields. This is deliberately small enough to audit.
    """

    factories: dict[str, PrimitiveFactory]
    step: float = 1.0
    angle_step: float = 0.5

    def compile(self, symbols: Sequence[str], origin: Vec2 = Vec2(0.0, 0.0)) -> Field2D:
        position = origin
        angle = 0.0
        stack: list[tuple[Vec2, float]] = []
        fields: list[Field2D] = []
        for token in symbols:
            if token == '+':
                angle += self.angle_step
            elif token == '-':
                angle -= self.angle_step
            elif token == '[':
                stack.append((position, angle))
            elif token == ']':
                if not stack:
                    raise GrammarError('unbalanced closing bracket')
                position, angle = stack.pop()
            elif token == 'F':
                position = position + Vec2(self.step, 0.0).rotate(angle)
            elif token in self.factories:
                fields.append(self.factories[token](position, angle))
            # Unknown tokens are inert variables by design.
        if stack:
            raise GrammarError('unbalanced opening bracket')
        if not fields:
            raise GrammarError('grammar emitted no geometry')
        field = fields[0]
        for other in fields[1:]:
            field = UnionField(field, other)
        return field
