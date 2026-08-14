# Chronological Synthesis of the Spherical Substrate Line

## Role in the corpus

This is the most important internal decoder. It changes the reading rule from “an unusual renderer” to “a queryable relation, state and event system.” It explicitly says that rasterization, ray marching, voxel storage and frame loops are downstream projection techniques, while the proposed substrate is built from relations, events, phases, identities and compatibility.

## Recoverable technical core

The document’s strongest formulation is:

- a finite grammar generates a continuous or piecewise-continuous state manifold;
- local spherical/radial-angular supports select relevance;
- relations define implicit event surfaces;
- compatibility gates decide whether co-located sectors may interact;
- transition functions update state at event times;
- lineage and invariants preserve identity across coordinate changes, splits and merges;
- an exogenous log stores novelty that cannot be regenerated from the grammar.

The state-space notation is summarized by `Q = P^n × R_time × S_phase × Z2_sheet × A_address × B_branch`. An entity trajectory is augmented with phase, sheet, lineage address and branch. An event is the earliest root that simultaneously lies inside a support and passes a compatibility predicate.

## Geometric translation

| Corpus image | Technical reading |
|---|---|
| sphere / shell | local support, radial reach, orientation, uncertainty |
| cone | domain of relevance, influence or sensing |
| hourglass | routing partition around a transition locus |
| SDF=0 / B=0 | guard or event surface |
| one-bit | parity, route or validity flag |
| double vacuum | co-location without coupling |
| ontological address | lineage-based identity |

The document repeatedly corrects the “polar-everything” interpretation. Spherical coordinates are a local chart, not a universal remeshing of the world.

## Feasibility boundary

The document narrows the defensible claim to restricted relation families that can answer `state_at(t)` and `next_event` without replaying every frame. It explicitly demotes universal O(1), zero memory and world-equals-general-AI claims to hypotheses. It also identifies algebraic closure, event density, branch explosion, degeneracies, numerical conditioning, exogenous entropy, split/merge identity and semantic grounding as the real bottlenecks.

## Best prototype

“Equation World Zero” is a small hybrid event system with two sheets, one orientation/parity bit, a bounded relation family, simple trajectories, finite grammar depth, lineage and symbolic outputs. The recommended experiment is headless: test state queries, event ordering, compatibility, routing and persistence before building a renderer.

## Files in this package

- `structures/geometry/equation_world_pipeline.svg`
- `structures/geometry/local_spherical_support.svg`
- `structures/geometry/phase_sheet_double_vacuum.svg`
- `structures/geometry/sdf_event_surface.svg`
- `structures/geometry/quad_hourglass.svg`
- `data/equations_and_operators.csv`
- `data/claims_evidence_matrix.csv`

## Page anchors

Executive interpretation: pp. 1-2. Unified concept and equations: pp. 5-7. Complexity and numerical stability: pp. 8-9. Comparison with rendering: pp. 9-10. Risks, experiments and final decision: pp. 11-12.
