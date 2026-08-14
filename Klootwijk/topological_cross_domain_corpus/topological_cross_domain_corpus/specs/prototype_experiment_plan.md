# Prototype Experiment Plan

## Experiment 1 - Horizon skipping

**Question:** Does `state_at(t)` scale with expression size rather than the number of skipped frames?

**Method:** Compare closed-form trajectory evaluation against a fixed-step reference over increasing time horizons.

**Success:** Query time remains approximately horizon-independent while error stays within the preregistered tolerance.

## Experiment 2 - Co-located phase sheets

**Question:** Is double vacuum a real compatibility sector rather than duplicated coordinates?

**Method:** Place two entities at the same position with incompatible sheet/phase labels. Then change only the compatibility token.

**Success:** No event is emitted before compatibility; the expected event appears after the token change.

## Experiment 3 - Event routing at B=0

**Question:** Do parity and sheet transitions preserve invariants and event order?

**Method:** Drive a constant-velocity trajectory across a line or circle guard with a typed route rule.

**Success:** One event is emitted, parity toggles exactly once, the new sheet is correct, and lineage records both pre- and post-state.

## Experiment 4 - Grammar-depth stress

**Question:** Does rule composition remain bounded or normalizable?

**Method:** Increase finite grammar depth while measuring expression size, solver time, and simplification success.

**Success:** Growth stays within a preregistered bound for the admitted relation family.

## Experiment 5 - Identity split/merge

**Question:** Can lineage remain reconstructable through forks and reconciliations?

**Method:** Split one entity into two branches, transition independently, then merge under explicit reconciliation rules.

**Success:** No lineage collision; all parent and branch events are recoverable.

## Experiment 6 - Minimal agent integration

**Question:** Can perception, memory lookup, and action selection reuse the same relation and transition language?

**Method:** Give a minimal agent one support query, one memory relation, and one action transition.

**Success:** The agent's observation and action are represented by the same event schema as physical transitions.

## Experiment 7 - Projection separation

**Question:** Can multiple views be generated without changing authoritative state?

**Method:** Render the same query result through Cartesian, log-polar, and 1-bit projection adapters.

**Success:** All views differ only in representation; state hashes and event logs remain unchanged.

## Experiment 8 - End-to-end B.C.E. throughput

**Question:** Does support plus compatibility plus event solving outperform a matched materialized baseline at equal error?

**Method:** Count only verified events and report miss/false-event rate, latency, energy, loss, calibration, and uncertainty.

**Success:** The preregistered metric vector beats the baseline. Otherwise the hypothesis fails for that implementation.

Source anchors: S1 pp. 11-12; S6 pp. 6, 9-10.
