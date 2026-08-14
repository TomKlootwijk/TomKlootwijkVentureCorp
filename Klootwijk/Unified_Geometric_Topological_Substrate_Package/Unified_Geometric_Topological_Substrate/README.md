# UGTS-0: Unified Geometric-Topological Substrate

This package is the technical extraction and bounded unification of the nine supplied PDFs. It preserves the corpus's useful geometrical and topological operators while separating them from metaphor, unsupported physics, and totalizing performance claims.

The central architecture is **query-first rather than image-first**:

```text
finite grammar + typed state
        |
        v
local support -> compatibility -> event-surface solve -> transition
        |                                      |
        +---------------- lineage + event log -+
                                               |
                     optional adapters: game / graphics / hardware
```

A state is not only a coordinate. In the reference model it contains:

```text
(position, time, phase, sheet, orientation, lineage, branch, uncertainty)
```

The one-bit motif is retained only as a **schema-bound route/parity/admission flag**. It never replaces continuous values, uncertainty, calibration, or lineage.

## What is included

- `report/Unified_Geometric_Topological_Substrate.pdf` - compiled 45-page unified report.
- `report/` - reproducible XeLaTeX source for the report.
- `specs/` - 69-item concept inventory, claims ledger, source map, JSON schema, and example world.
- `src/ugts/` - dependency-free Python reference implementation.
- `tests/` - executable unit tests.
- `examples/` - runnable demos and generated PBM/PGM/event-log outputs.
- `shaders/` - optional GLSL projection adapter.
- `adapters/` - minimal Unity and Godot integration examples.
- `diagrams/` - report architecture and geometry figures.
- `source_notes/` - per-document extraction notes.

## Quick start

From this directory:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python examples/equation_world_zero.py
PYTHONPATH=src python examples/topology_demo.py
PYTHONPATH=src python examples/graphics_preview.py
PYTHONPATH=src python examples/bce_demo.py
```

Or install locally:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Core API

```python
from ugts import load_world

world = load_world("specs/example_world.json")
state = world.state_at("traveler_A", 1.25)
candidate = world.next_event("traveler_A", 0.0, 5.0)
record = world.process_next_event("traveler_A", 0.0, 5.0)
```

The six minimum substrate queries are:

1. `state_at(entity_id, t)`
2. `next_event(entity_id, t0, t1)`
3. `events_in_support(support, t0, t1)`
4. `can_couple(entity_a, entity_b, t)`
5. `process_next_event(...)` / transition application
6. `reconstruct_identity(entity_id)`

## Technical interpretation of source motifs

| Source motif | Bounded operator in UGTS-0 |
|---|---|
| Binary carry thresholds | Radix scale boundaries and level indices |
| 19 = `10011`, three active bits | Hamming-weight descriptor; optional triangle seed |
| Pascal parity / Sierpinski | Deterministic fractal and test-pattern generator |
| D/B/phi becomes R | Boundary-graph cut plus curve morph |
| Torque / delta-time / phase | Typed kinematic and phase parameters |
| One-bit hinge | Route/parity flag interpreted by a schema |
| `SDF = 0` | Relation/event surface, not an instruction to raymarch forever |
| Cone / sphere / shell | Local radial-angular support and relevance scope |
| Double vacuum | Co-located states that do not couple because phase/sheet/orientation/address differ |
| Hourglass pinch | Explicit four-chamber routing table at an event locus |
| Mobius / Klein bottle | Quotient/gluing maps with orientation/sheet changes |
| Log-polar LUT | Optional local coordinate and compressed 1-bit admission mask |
| Feynman vectors | Normalized as oriented complex-phasor supersampling, not quantum rasterization |
| 1-bit jitter | Optional stochastic spatial or temporal projection adapter |
| Matrix-in-glass | Calibrated transfer matrix in an optofluidic/waveguide endpoint |
| B.C.E. | Bounded Compatibility Event with measured guard crossing |

## Evidence boundary

The documents contain both implementable mechanisms and highly speculative claims. UGTS-0 follows four rules:

1. **Retain the operator, demote the totalizing claim.**
2. **Keep types separate.** Geometry, time, phase, routing bits, optical amplitudes, and identity are different fields.
3. **Bound the solver.** Closed forms are used only for declared surface/trajectory families; generic fields use bracketed numerical roots.
4. **Make projection optional.** Rasterization, raymarching, SDF previews, and display modulation are adapters, not the authoritative world state.

See `specs/claims_ledger.csv` for explicit dispositions. The package rejects universal O(1), zero memory/latency/heat, physical Klein-bottle self-assembly, one-bit-complete-state, and claims that the geometry replaces general AI or all conventional simulation structures.

## Reference implementation map

- `state.py`: typed state, patches, lineage, event records.
- `trajectory.py`: closed-form linear and quadratic motion.
- `support.py`: local radial-angular/time admission.
- `compatibility.py`: phase/sheet/orientation/branch/tag/lineage gating.
- `events.py`: analytic and bracketed event-surface solvers.
- `transition.py`: sheet/orientation/phase/branch/tag/lineage updates.
- `world.py`: query-first runtime and event log.
- `geometry.py`: implicit primitives, CSG, morphing, gradients, overlap lens.
- `topology.py`: Mobius, Klein quotient, portal, and hourglass routing.
- `logpolar.py`: explicit-core log-polar transform and compact bit LUT.
- `numeric.py`: radix thresholds, Hamming weight, Pascal parity, golden-angle samples.
- `glyphs.py`: loop/stem and loop-to-R morph examples.
- `grammar.py`: finite, budgeted grammar and small shape compiler.
- `render.py`: optional CPU projection, 1-bit posterization, and PDM.
- `bce.py`: measured Bounded Compatibility Event controller.
- `io.py`: JSON world loader and event-log serialization.

## Game-engine integration

The authoritative runtime can coexist with a conventional engine:

- ECS components store analytic motion coefficients, sheet/orientation/phase, lineage, and state patches.
- Sensor/FOV systems issue radial-angular support queries.
- Continuous collision systems solve the next valid relation root.
- Portal systems apply explicit coordinate, orientation, and sheet maps.
- Multiplayer systems replicate schema versions and authoritative events; they do not need to replicate every visual frame for closed deterministic motion.
- Rendering remains conventional if desired; the included SDF/log-polar adapter is only one preview path.

Minimal Unity and Godot adapters are under `adapters/`.

## License

The reference implementation is provided under the MIT License. The supplied source PDFs are not redistributed in this package; the report contains extraction notes and page-level traceability only.
