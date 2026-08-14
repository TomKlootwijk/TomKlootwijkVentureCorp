# Spherical Throughput: Practical Waveguide Liquid-Substrate Lensing

## Role in the corpus

This is the most grounded engineering document. It applies an explicit translation rule: retain implementable operators, translate metaphors, demote frontier topology, rewrite absolute claims and reject zero-latency/zero-heat/zero-memory rhetoric.

## Canonical system

A bounded radial-angular input field is admitted, shaped by a tunable liquid region, coupled into compatible guided modes, and converted into a verified event only when a measured guard crosses. Every result includes error, energy, loss, latency, calibration, uncertainty and lineage.

Signal path:

`local spherical support → liquid coupling → compatible guided mode → B.C.E. guard → verified output`

“Spherical” means local angular support/radial reach. “Liquid-substrate” means a liquid element coupled to a solid photonic platform. “Throughput” means verified events or answered queries per second at a declared error budget.

## Physical embodiments

1. **Liquid overclad:** microfluidic liquid above/beside a solid waveguide; best first prototype.
2. **Liquid core:** mode propagates in a liquid-filled channel; stronger interaction but harder packaging/loss control.
3. **Input liquid lens:** deformable droplet/membrane focuses a free-space field into a conventional circuit.

Recommended Hollowlens-0: fused silica or SiN, 2×2 interferometer, microfluidic chamber over one arm, pressure/electrowetting/thermal actuation, balanced photodiodes and an FPGA/MCU sidecar.

## Governing equations

- Maxwell field equation for the dielectric geometry.
- Coupled-mode ODEs for amplitudes, attenuation, propagation constants and tunable coupling.
- Young-Laplace pressure-curvature relation for the meniscus.
- Effective-index phase shift.
- Navier-Stokes only when transient liquid motion cannot be treated quasi-statically.
- Mode-overlap integral for spherical-to-guided coupling.
- Bounded Compatibility Event guard for output declaration.

The file `data/equations_and_operators.csv` carries the exact formulas.

## Control logic

Compatibility can include wavelength, polarization, mode, phase, time window, permission and provenance. Co-location at a coupler is not enough. The one-bit parity flag has a narrow, schema-dependent role; optical amplitudes, uncertainty, thresholds and lineage remain separate state.

The digital sidecar is mandatory for calibration, actuator state, thresholds, drift, saturation, policy tags and safe fallback.

## Metrics

Primary metric: `Θ_sph=N_verified/Δt`. A verified event must pass support, compatibility, guard crossing and confidence. Additional metrics include route accuracy, events/J, support and compatibility pruning, median/tail latency, missed/false-event probability, insertion loss and drift.

## Fabrication and failure criteria

The document supplies a conventional optofluidic process: select substrate/wavelength, form guides/couplers, open microfluidic cavity, add liquid and actuator, bond/seal, couple light, detect and calibrate.

Kill criteria include excessive optical loss, irreproducible liquid behavior, actuation too slow for the event rate, mode crosstalk, calibration burden, ambiguous/missed events, packaging failure or no full-system advantage over electronics.

## Explicitly excluded claims

No zero latency, zero heat, zero power, universal O(1), zero-memory universe, exact chaos solution, literal double vacuum, physical Klein-bottle proof, general AI compression, medical effect or replacement for all renderers/PDE solvers.

## Files in this package

- `structures/photonics/hollowlens0_architecture.svg`
- `structures/photonics/spherical_throughput_funnel.svg`
- `data/equations_and_operators.csv`
- `data/claims_evidence_matrix.csv`

## Page anchors

Translation rule: p. 2. Definition: p. 3. Embodiments: p. 4. Equations: p. 5. Metrics: p. 6. Control: p. 7. Fabrication: p. 8. Prototype: p. 9. Failure/kill criteria: p. 10. Canonical addition: p. 11. Component evidence boundary: p. 12.
