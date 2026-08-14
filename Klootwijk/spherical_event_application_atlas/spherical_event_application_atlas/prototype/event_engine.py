"""Restricted reference implementation of a query-first state/event engine.

This is a teaching and benchmarking prototype. It is not a clinical device, safety
controller, medical decision system, or proof of performance. Relations supply their
own root solver, so the engine does not secretly advance a universal frame loop.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import json
import uuid

Number = float
StateFn = Callable[[Number], "State"]
RootSolver = Callable[[Number], Sequence[Number]]
Predicate = Callable[["State", Number, Dict[str, Any]], Tuple[bool, List[str]]]
TransitionFn = Callable[["State", Dict[str, Any]], "State"]


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class State:
    entity_id: str
    t: Number
    position: Tuple[Number, ...] = ()
    phase: Optional[Number] = None
    sheet: str = "0"
    lineage_address: str = "root"
    branch: str = "main"
    parity: int = 0
    attributes: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = "1.0"

    def digest(self) -> str:
        return stable_hash(asdict(self))


@dataclass(frozen=True)
class Relation:
    relation_id: str
    transition_id: str
    roots_after: RootSolver
    guard_value: Callable[[State, Number], Number]
    transition: TransitionFn
    support: Predicate
    compatibility: Predicate
    predicate_version: str = "1.0"


@dataclass(frozen=True)
class VerifiedEvent:
    event_id: str
    entity_id: str
    relation_id: str
    transition_id: str
    t_star: Number
    support_admitted: bool
    compatible: bool
    predicate_version: str
    guard_crossed: bool
    guard_value: Number
    confidence: Dict[str, Any]
    pre_state_hash: str
    post_state_hash: str
    lineage_parent: str
    branch_created: Optional[str]
    parity_before: int
    parity_after: int
    invariant_report: Dict[str, Any]
    reason_codes: List[str]
    schema_version: str = "1.0"


@dataclass
class ExpectedEvent:
    expectation_id: str
    entity_id: str
    relation_id: str
    due_start: Number
    due_end: Number
    predicate_version: str
    authority: Dict[str, Any]
    status: str = "open"
    exception_code: Optional[str] = None


@dataclass(frozen=True)
class CoverageInterval:
    source_id: str
    start: Number
    end: Number
    healthy: bool = True
    reason: str = ""


@dataclass(frozen=True)
class AbsenceEvent:
    absence_event_id: str
    expectation_id: str
    entity_id: str
    relation_id: str
    emitted_at: Number
    due_interval: Tuple[Number, Number]
    coverage_complete: bool
    coverage_evidence: List[Dict[str, Any]]
    support_valid: bool
    compatibility_valid: bool
    matching_event_count: int
    exception_checked: bool
    reason_codes: List[str]
    confidence: Dict[str, Any]
    predicate_version: str
    schema_version: str = "1.0"


@dataclass(frozen=True)
class UnknownOutcome:
    expectation_id: str
    reason_codes: List[str]
    detail: str


class EventEngine:
    def __init__(self) -> None:
        self._models: Dict[str, StateFn] = {}
        self._events: List[VerifiedEvent] = []
        self._expectations: Dict[str, ExpectedEvent] = {}
        self._coverage: Dict[str, List[CoverageInterval]] = {}

    def register_model(self, entity_id: str, state_fn: StateFn) -> None:
        if entity_id in self._models:
            raise ValueError(f"model already registered: {entity_id}")
        self._models[entity_id] = state_fn

    def state_at(self, entity_id: str, t: Number) -> State:
        try:
            return self._models[entity_id](t)
        except KeyError as exc:
            raise KeyError(f"unknown entity: {entity_id}") from exc

    def next_event(
        self,
        entity_id: str,
        relation: Relation,
        t0: Number,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[VerifiedEvent]:
        context = dict(context or {})
        roots = sorted(r for r in relation.roots_after(t0) if r >= t0)
        for t_star in roots:
            pre = self.state_at(entity_id, t_star)
            support_ok, support_reasons = relation.support(pre, t_star, context)
            compatible, compatibility_reasons = relation.compatibility(pre, t_star, context)
            value = relation.guard_value(pre, t_star)
            crossed = abs(value) <= float(context.get("guard_tolerance", 1e-9))
            if not (support_ok and compatible and crossed):
                continue
            post = relation.transition(pre, context)
            invariant_report = {
                "entity_id_preserved": pre.entity_id == post.entity_id,
                "lineage_present": bool(post.lineage_address),
                "branch_present": bool(post.branch),
            }
            if not all(invariant_report.values()):
                raise ValueError(f"transition violates invariants: {invariant_report}")
            event = VerifiedEvent(
                event_id=str(uuid.uuid4()),
                entity_id=entity_id,
                relation_id=relation.relation_id,
                transition_id=relation.transition_id,
                t_star=t_star,
                support_admitted=support_ok,
                compatible=compatible,
                predicate_version=relation.predicate_version,
                guard_crossed=crossed,
                guard_value=value,
                confidence={"value": 1.0, "method": "closed-form root supplied by relation"},
                pre_state_hash=pre.digest(),
                post_state_hash=post.digest(),
                lineage_parent=pre.lineage_address,
                branch_created=post.branch if post.branch != pre.branch else None,
                parity_before=pre.parity,
                parity_after=post.parity,
                invariant_report=invariant_report,
                reason_codes=support_reasons + compatibility_reasons,
            )
            self._events.append(event)
            self._satisfy_matching_expectations(event)
            return event
        return None

    def record_external_event(self, event: VerifiedEvent) -> None:
        if not (event.support_admitted and event.compatible and event.guard_crossed):
            raise ValueError("external event is not verified")
        self._events.append(event)
        self._satisfy_matching_expectations(event)

    def register_expectation(self, expected: ExpectedEvent) -> None:
        if expected.due_end < expected.due_start:
            raise ValueError("due_end must not precede due_start")
        if expected.expectation_id in self._expectations:
            raise ValueError(f"duplicate expectation: {expected.expectation_id}")
        self._expectations[expected.expectation_id] = expected

    def add_coverage(self, entity_id: str, interval: CoverageInterval) -> None:
        if interval.end < interval.start:
            raise ValueError("coverage interval is inverted")
        self._coverage.setdefault(entity_id, []).append(interval)

    def set_exception(self, expectation_id: str, code: str) -> None:
        expected = self._expectations[expectation_id]
        expected.exception_code = code
        expected.status = "excepted"

    def close_expectation(self, expectation_id: str, now: Number):
        expected = self._expectations[expectation_id]
        if expected.status == "satisfied":
            return expected
        if expected.status in {"cancelled", "excepted"}:
            return UnknownOutcome(expectation_id, [expected.status.upper()], "Expectation was not eligible for absence emission.")
        if now < expected.due_end:
            return UnknownOutcome(expectation_id, ["DUE_INTERVAL_OPEN"], "The due interval has not closed.")
        matching = [
            e for e in self._events
            if e.entity_id == expected.entity_id
            and e.relation_id == expected.relation_id
            and expected.due_start <= e.t_star <= expected.due_end
        ]
        if matching:
            expected.status = "satisfied"
            return expected
        intervals = [i for i in self._coverage.get(expected.entity_id, []) if i.healthy]
        complete, evidence = _coverage_complete(intervals, expected.due_start, expected.due_end)
        if not complete:
            expected.status = "unknown"
            return UnknownOutcome(
                expectation_id,
                ["OBSERVATION_COVERAGE_INCOMPLETE"],
                "No absence event emitted: missing telemetry is not evidence of absence.",
            )
        expected.status = "absent"
        return AbsenceEvent(
            absence_event_id=str(uuid.uuid4()),
            expectation_id=expected.expectation_id,
            entity_id=expected.entity_id,
            relation_id=expected.relation_id,
            emitted_at=now,
            due_interval=(expected.due_start, expected.due_end),
            coverage_complete=True,
            coverage_evidence=[asdict(x) for x in evidence],
            support_valid=True,
            compatibility_valid=True,
            matching_event_count=0,
            exception_checked=True,
            reason_codes=["EXPECTED_EVENT_NOT_OBSERVED_WITH_VALID_COVERAGE"],
            confidence={"value": 1.0, "method": "deterministic coverage and event-log check"},
            predicate_version=expected.predicate_version,
        )

    def events(self) -> List[VerifiedEvent]:
        return list(self._events)

    def _satisfy_matching_expectations(self, event: VerifiedEvent) -> None:
        for expected in self._expectations.values():
            if (
                expected.status == "open"
                and expected.entity_id == event.entity_id
                and expected.relation_id == event.relation_id
                and expected.due_start <= event.t_star <= expected.due_end
            ):
                expected.status = "satisfied"


def _coverage_complete(intervals: Iterable[CoverageInterval], start: Number, end: Number):
    relevant = sorted(
        (i for i in intervals if i.end >= start and i.start <= end),
        key=lambda i: (i.start, i.end),
    )
    if not relevant:
        return False, []
    cursor = start
    used: List[CoverageInterval] = []
    for interval in relevant:
        if interval.start > cursor:
            return False, used
        if interval.end > cursor:
            used.append(interval)
            cursor = interval.end
        if cursor >= end:
            return True, used
    return False, used


def linear_threshold_relation(
    relation_id: str,
    transition_id: str,
    value_at_zero: Number,
    slope: Number,
    threshold: Number,
    transition: TransitionFn,
    support: Optional[Predicate] = None,
    compatibility: Optional[Predicate] = None,
) -> Relation:
    if slope == 0:
        roots: Sequence[Number] = [] if value_at_zero != threshold else [0.0]
    else:
        roots = [(threshold - value_at_zero) / slope]

    def roots_after(t0: Number) -> Sequence[Number]:
        return [r for r in roots if r >= t0]

    def guard_value(state: State, t: Number) -> Number:
        return value_at_zero + slope * t - threshold

    allow: Predicate = lambda state, t, ctx: (True, ["ADMITTED"])
    return Relation(
        relation_id=relation_id,
        transition_id=transition_id,
        roots_after=roots_after,
        guard_value=guard_value,
        transition=transition,
        support=support or allow,
        compatibility=compatibility or allow,
    )
