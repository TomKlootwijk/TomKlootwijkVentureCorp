# Computational Architecture Decode

## State instead of image

The mature proposal treats a world as directly queryable relations rather than a sequence of pictures. Rendering remains possible but downstream.

## Hybrid event system

The closest established computer-science category is a hybrid dynamical system with:

- continuous state trajectories;
- implicit guard surfaces;
- discrete modes/sheets;
- compatibility predicates;
- transition/reset maps;
- invariants;
- event and novelty logs.

## Direct queries

`state_at(t)` can skip replay for closed-form or compiled trajectories. `next_event` solves for the earliest supported compatible crossing. Neither query is universally constant-time.

## Identity and lineage

A generative address and parent/transition history can preserve identity across coordinate changes. The corpus’s 64-bit UUID claim is too absolute; real systems need collision policy, namespaces and split/merge semantics.

## Memory

Seed + grammar + exogenous log can reduce snapshot storage. Memory remains necessary for coefficients, branch history, external events, calibration and numerical state.

## Acceleration structures

BVHs, octrees and raster grids are not “wrong.” They are conventional candidate-pruning/materialization methods. Analytic support and compatibility are alternatives. Only workload-specific benchmarks can decide which wins.

## Signal/display bridge

KC Vector Art proposes log-polar SDF geometry followed by one-bit pulse density or spatial dithering. This can be a downstream output stage without making pixels the underlying ontology.

## Undefined element

“Feynman vectors” need a formal state/measure/accumulation definition before they can be considered an algorithm.
