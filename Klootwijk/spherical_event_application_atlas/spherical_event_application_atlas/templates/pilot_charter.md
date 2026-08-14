# Bounded pilot charter

## 1. Question

State the single direct query being tested, such as `state_at(t)`, `next_event`, `events_in_support`, `can_couple`, transition routing, lineage reconstruction, or auditable absence.

## 2. Domain boundary

- Physical model or workflow:
- Authoritative external standard:
- Included relation family:
- Explicit exclusions:

## 3. State and identity

- State schema version:
- Entity identifiers and lineage rules:
- Branch/split/merge policy:
- Exogenous novelty sources:

## 4. Event contract

- Relation/guard:
- Local support:
- Compatibility predicate and version:
- Confidence or certified interval:
- Transition and invariants:

## 5. Negative-event contract

- Expected event:
- Authority creating the expectation:
- Observation-coverage requirement:
- Due interval:
- Valid exception codes:
- Unknown-state policy:

## 6. Baseline

- Matched conventional system:
- Equal task and safety boundary:
- Locked dataset/protocol:

## 7. Metrics

Include task outcome, verified events/s, verified events/J, support and compatibility pruning, miss/false rate, tail latency, drift, calibration, memory, lineage accuracy and human/governance burden.

## 8. Kill criteria

Pre-register the conditions that retain the baseline, narrow the claim, or stop the pilot.
