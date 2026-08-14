# Equation World Zero - Restricted Reference Specification

## Purpose

Equation World Zero (EW0) is the minimum headless prototype implied by the mature corpus reading. It is not a renderer, a universal physics engine, a medical system, or a zero-cost computer. It tests whether one bounded family of continuous relations can answer state and event queries without replaying every frame.

Source anchors: S1 pp. 7, 11-12; S6 p. 9.

## State space

A normalized entity state is

\[
q_e(t) = (x_e(t), t, \phi_e(t), \sigma_e(t), a_e, b_e, p_e)
\]

where:

- `x_e(t)` is a 2D homogeneous or Euclidean position for the first prototype;
- `t` is continuous time;
- `phi_e(t)` is a phase coordinate or schedule;
- `sigma_e(t)` is a finite sheet label, initially `0` or `1`;
- `a_e` is a persistent lineage address;
- `b_e` is a branch identifier;
- `p_e` is a narrow parity/routing bit.

The world record is

\[
W = (G, R, T, I, L)
\]

with finite grammar `G`, relation family `R`, transition rules `T`, invariants `I`, and exogenous log `L`.

## Restricted relation family

EW0 permits only relation types with certified, bounded event solvers:

1. line guards intersected by constant-velocity trajectories;
2. circle guards intersected by constant-velocity trajectories;
3. optional quadratic trajectories when a robust polynomial solver and interval checks are present.

No arbitrary implicit field, arbitrary PDE, self-reference, or unconstrained procedural grammar is admitted in version 0.

## Support

A local spherical support is represented in 2D as an annular angular sector:

- origin `o`;
- radial interval `[r_min, r_max]`;
- angular interval or wrapped union;
- optional time interval;
- confidence or uncertainty margin.

The support predicate is `C_alpha(q,t) <= 0`, operationally implemented as radial, angular, and time-window checks. This is a local query chart, not a global world coordinate system.

## Compatibility

A relation may enter the event solver only when `chi(e,j,t)=1`. The prototype predicate can combine:

- allowed sheet pairs;
- phase-distance tolerance;
- address or provenance policy;
- mode/type compatibility;
- permission or scenario tag;
- freshness/time-window condition.

Compatibility must return a Boolean and a reason code. Co-location alone is never sufficient.

## Event

For relation `j`, the next event is

\[
t^* = \min\{t \ge t_0 : R_j(q_e(t))=0,\ C_\alpha(q_e(t),t)\le 0,\ \chi(e,j,t)=1\}.
\]

The event solver returns an interval or certified root when exact arithmetic is unavailable. Tangencies and multiple roots are represented explicitly rather than silently ordered.

## Transition

At an admitted event:

\[
q_e(t^{*+}) = T_j(q_e(t^{*-}), context).
\]

A transition may:

- toggle the parity bit;
- route to another sheet;
- create a new branch;
- append a lineage event;
- update typed state variables;
- reject the transition if an invariant would fail.

The one-bit field never replaces the rest of the state.

## Identity and memory

The lineage address is normalized as a stable provenance key:

\[
a_e = H(seed_e, grammar\_path_e, lineage\_events_e).
\]

Closed state is regenerated from seed and grammar. Only exogenous novelty, necessary branch history, and audit metadata are stored. The prototype must measure both storage saved and recomputation cost.

## Required queries

1. `state_at(entity, t)`
2. `next_event(entity, t0, relation_family)`
3. `events_in_support(support, t0, t1)`
4. `can_couple(entity_a, entity_b, context)`
5. `transition(event, state, context)`
6. `reconstruct_identity(seed, grammar_path, log, branch)`

A renderer or vector output is optional and must consume query results as a downstream materialized view.

## Exit criteria

EW0 succeeds only if all of the following hold for the preregistered relation family:

- `state_at(t)` cost tracks expression complexity, not skipped frame count;
- event order matches a high-resolution reference implementation;
- co-located incompatible sheets do not couple;
- parity and routing transitions preserve invariants;
- lineage remains reconstructable after split and merge tests;
- grammar depth remains bounded or normalizable;
- memory plus query cost beats the matched materialized baseline at the same error boundary.

## Explicit exclusions

EW0 does not claim universal O(1), zero memory, zero heat, zero latency, exact chaos, literal non-orientable hardware, general AI compression, medical action, biological control, or replacement of every renderer and PDE solver.
