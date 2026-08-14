# Prototype Blueprints

## Digital-first Equation World Zero

### Minimum relation family

- 2D or 3D position plus continuous time;
- two sheet labels;
- one route/parity bit;
- analytic trajectories from a restricted family;
- one or two implicit relations;
- local cone support;
- compatibility predicate;
- lineage identifier and append-only event log.

### Required queries

1. `state_at(t)`
2. `next_event(t0)`
3. `events_in_support`
4. `phase_coupling`
5. `transition_route`
6. `reconstruct_identity`

### Success criteria

- correct event ordering;
- no missed crossings within declared tolerance;
- expression growth bounded or normalizable;
- query cost tied to expression complexity rather than skipped frames;
- stable split/merge lineage;
- interval or uncertainty output near degeneracy.

## Hollowlens-0

### Minimum hardware

- one angularly scanned source;
- one tunable liquid coupler;
- one 2×2 interferometric waveguide;
- two balanced detectors;
- one FPGA/MCU sidecar.

### Pre-registration

Fix wavelength, optical power, support sector, compatible modes, thresholds, uncertainty, error targets, energy boundary, calibration interval and electronic baseline before viewing results.

### Kill criteria

Stop or redesign if optical loss, liquid instability, crosstalk, drift, actuation speed, event ambiguity, packaging or digital-sidecar overhead erase the claimed advantage.
