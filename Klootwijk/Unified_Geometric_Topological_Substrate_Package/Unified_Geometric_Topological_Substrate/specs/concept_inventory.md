# Concept inventory

| ID | Category | Concept | Status | Normalized operator | Sources |
|---|---|---|---|---|---|
| N01 | Numeric/fractal | Radix carry threshold | retain | Use radix powers as scale/change boundaries and compact level indices. | S1 pp. 1-4 |
| N02 | Numeric/fractal | Zero-based offset semantics | retain | Keep value, offset and ordinal position as distinct typed quantities. | S4 pp. 1-3 |
| N03 | Numeric/fractal | Active-bit/Hamming-weight filter | translate | Use popcount as a sparse feature count or seed descriptor. | S1 pp. 3-5 |
| N04 | Numeric/fractal | Three-point triangle seed | translate | Map three non-collinear active samples to a simplex/triangle primitive. | S1 pp. 6-7 |
| N05 | Numeric/fractal | Pascal parity to Sierpinski | retain | Use binomial parity as a deterministic fractal/test-pattern generator. | S1 pp. 6-9 |
| N06 | Numeric/fractal | Golden-angle/Fibonacci sampling | translate | Optional quasi-uniform angular sample schedule or dither seed. | S1 pp. 13-15 |
| N07 | Numeric/fractal | Lemniscate/strange-loop recursion | demote | Represent recursion with explicit finite grammar depth and cycle detection. | S1 pp. 18-23 |
| G01 | Glyph/kinematic | Loop-plus-stem decomposition | translate | Represent glyph geometry as a graph of curve segments and junctions. | S9,S2,S8 pp. 1-2 |
| G02 | Glyph/kinematic | Cut-unroll D/B to R | retain | Boundary-graph edit plus continuous curve morph from closed arc to open segment. | S9,S2,S8 pp. 1-4 |
| G03 | Glyph/kinematic | Torque axis T | translate | Use a rotation/warp parameter around a declared pivot axis. | S9,S2,S8 pp. 1-4 |
| G04 | Glyph/kinematic | Delta-time and phase modulation | retain | Store continuous time and phase as separate state coordinates and derivatives. | S1,S7,S9 pp. 10-15;14-18;2-5 |
| G05 | Glyph/kinematic | One-bit parity hinge | retain | Use a schema-bound route/parity flag that selects transition behavior. | S5,S6,S7,S9 pp. 2-8;5-7;14-25;3-8 |
| G06 | Glyph/kinematic | Global hinge field | translate | Model a global morph or transition field evaluated at every query point. | S9,S2,S8 pp. 7-8 |
| G07 | Glyph/kinematic | Chirality/orientation flip | retain | Track an orientation bit and apply a gluing/transition map that may flip it. | S1,S7,S9 pp. 21-29;18-25;4-8 |
| G08 | Glyph/kinematic | Split oval to opposing arches | translate | Use symmetric curve branches around a fixed node for waveform or deformation profiles. | S4 pp. 10-16 |
| G09 | Glyph/kinematic | Overlap lens/shared domain | retain | Use intersection A∩B, lens area, or blend region as explicit shared domain. | S4 pp. 16-19 |
| I01 | Implicit geometry | Signed distance/implicit field | retain | Use implicit scalar fields; reserve exact-distance claims for valid primitives/transforms. | S1,S3,S6,S7,S9 pp. 10-30;1-10;5-10;14-31;7-8 |
| I02 | Implicit geometry | SDF CSG operators | retain | Provide composable implicit-field operators with documented sign convention. | S3 pp. 1-3 |
| I03 | Implicit geometry | Zero surface as event relation | retain | Treat R_j(q)=0 as an event guard and solve crossing time. | S6,S5,S7 pp. 5-7;3-7;14-31 |
| I04 | Implicit geometry | Analytic kinematic sweep | retain | Use closed-form roots for restricted trajectory/surface pairs; certified numerical roots otherwise. | S6,S7 pp. 7-12;14-31 |
| I05 | Implicit geometry | Cone as support/domain | retain | Use analytic radial-angular support predicates for pruning/query scope. | S5,S6,S7 pp. 3-6;5-10;12-25 |
| I06 | Implicit geometry | Spherical/local radial-angular support | retain | Represent local support by radius, angle, orientation, uncertainty and time window. | S5,S6 pp. 3-6;1-10 |
| I07 | Implicit geometry | Nested shells | translate | Use concentric support bands or multiresolution radial intervals. | S6,S7 pp. 1-7;12-25 |
| I08 | Implicit geometry | Hourglass/quad routing | translate | Implement a finite routing partition keyed by sign/sheet/orientation at a transition surface. | S6,S7 pp. 5-7;23-25 |
| I09 | Implicit geometry | Invariant/eigen-axis | retain | Declare invariants and preserved quantities for transitions. | S1,S6,S7 pp. 15-20;5-12;18-25 |
| I10 | Implicit geometry | Projective/homogeneous chart | translate | Optional homogeneous coordinates for intersections and points at infinity. | S6,S7 pp. 5-7;18-25 |
| C01 | Coordinates/sampling | Log-polar transform | retain | Use a local coordinate chart that turns radial scaling into translation in rho. | S1,S3,S7,S9 pp. 10-15;1-10;12-31;5-8 |
| C02 | Coordinates/sampling | One-bit log-polar LUT | retain | Use as a coarse admission/cache mask, never as the whole world state. | S1,S3,S7,S9 pp. 10-15;1-10;12-31;5-8 |
| C03 | Coordinates/sampling | Phasor/Feynman-style edge accumulation | translate | Normalize to complex phasor or oriented coverage accumulation for antialiasing. | S3 pp. 1-8 |
| C04 | Coordinates/sampling | One-bit stochastic jitter | retain | Use deterministic blue-noise/hash dithering with reproducible seeds. | S1,S3 pp. 10-15;7-10 |
| C05 | Coordinates/sampling | Temporal pulse-density modulation | translate | Optional display-output adapter using PDM or delta-sigma modulation. | S3 pp. 4-6 |
| C06 | Coordinates/sampling | Chromatic log-radius offset | retain | Apply channel-specific log-radius shifts before field evaluation, then resample correctly. | S3 pp. 7-8 |
| C07 | Coordinates/sampling | Log-polar prepress screening | translate | Optional print adapter with calibrated halftone, screen angles and dot-gain compensation. | S3 pp. 8-10 |
| T01 | Topology | Phase sheets | retain | Represent state as base position plus sheet, phase, orientation and address. | S6,S7,S9 pp. 5-10;14-25;5-8 |
| T02 | Topology | Double vacuum | retain | Compatibility-gated coupling: same x does not imply same sector. | S5,S6,S7 pp. 2-7;5-10;14-25 |
| T03 | Topology | Mobius gluing | retain | Implement quotient-map boundary wrapping with orientation flip. | S7,S9 pp. 7-12;5-8 |
| T04 | Topology | Klein-bottle gluing | translate | Implement two rectangle-edge identifications, one orientation reversing. | S5,S7,S9 pp. 2,5;7-25;5-10 |
| T05 | Topology | Topological portal/gluing map | retain | Use explicit port, orientation map, coordinate transform and transfer metadata. | S5,S6,S7 pp. 2-5;5-12;14-25 |
| T06 | Topology | Inside/outside sign with schema | retain | Bind every bit to a declared schema/version and keep uncertainty separate. | S3,S5,S7,S9 pp. 1-10;2-7;14-31;3-8 |
| T07 | Topology | Strange loop/self-reference | demote | Use explicit cycles, fixed points and termination/cycle policies in the grammar/event graph. | S1,S7,S9 pp. 18-30;7-25;5-10 |
| A01 | Information architecture | Finite grammar G | retain | Use bounded-depth typed productions that compile to supported relation primitives. | S6,S7,S9 pp. 1-12;26-31;5-8 |
| A02 | Information architecture | State manifold Q | retain | Use a typed immutable state record; optional orientation and uncertainty extensions. | S6 pp. 5-7 |
| A03 | Information architecture | Relation family R_j(q)=0 | retain | Store typed relations with parameters, domains and solver capability metadata. | S6 pp. 5-12 |
| A04 | Information architecture | Support predicate C<=0 | retain | Separate admission/support from geometry and from compatibility. | S5,S6 pp. 3-7;5-12 |
| A05 | Information architecture | Compatibility predicate chi | retain | Compose physical and digital compatibility predicates. | S5,S6 pp. 3-7;5-12 |
| A06 | Information architecture | Event time t* | retain | Compute min valid root after t0 with tolerance and confidence. | S5,S6 pp. 3-7;5-12 |
| A07 | Information architecture | Transition rule T_j | retain | Use pure transition functions producing state patches and event records. | S5,S6 pp. 5-7;5-12 |
| A08 | Information architecture | Lineage address | retain | Use stable entity IDs plus parent/merge ancestry and transition lineage. | S5,S6,S7 pp. 3-12;1-12;26-35 |
| A09 | Information architecture | Irreducible external event log | retain | Event-source only novelty, transitions, confidence and calibration changes. | S5,S6 pp. 7-11;1-12 |
| A10 | Information architecture | Query-first API | retain | Expose direct query methods independent of a frame loop. | S5,S6 pp. 3-12;1-12 |
| A11 | Information architecture | Projection adapter | retain | Place raster/raymarch/SDF preview in a replaceable adapter layer. | S3,S6 pp. 1-10;1-12 |
| A12 | Information architecture | Hybrid layer separation | retain | Use core/query/projection/hardware modules with explicit interfaces. | S5,S6 pp. 2-12;1-12 |
| A13 | Information architecture | Branch and chamber routing | retain | Use finite enums and explicit routing tables. | S6,S7 pp. 5-12;23-31 |
| A14 | Information architecture | Uncertainty/confidence | retain | Attach numeric intervals/confidence and solver status to every event. | S5,S6 pp. 1-12;8-12 |
| A15 | Information architecture | Schema-bound packed data caution | retain | Version all bitfields/LUTs and ship schema with data. | S2,S8,S9,S5 pp. 27-29;26-28;26-28;7 |
| A16 | Information architecture | Agent on shared relation substrate | translate | Keep agent integration minimal: queries and transition choices, not universal AI compression. | S6,S7 pp. 11-12;34-36 |
| K01 | Game technology | Analytic motion component | retain | Entity component stores trajectory coefficients and state patches. | S6,S7,S4 pp. 7-12;26-31;10-16 |
| K02 | Game technology | Continuous collision/event component | retain | Event solver returns ordered crossings with guard semantics. | S6,S7 pp. 7-12;26-31 |
| K03 | Game technology | Sensor cone component | retain | FOV/range query before relation solving. | S5,S6,S7 pp. 3-9;5-12;12-25 |
| K04 | Game technology | Procedural grammar component | retain | Compile grammar tokens to primitives, supports and transitions. | S6,S7,S9 pp. 11-12;26-31;5-8 |
| K05 | Game technology | Topological portal component | retain | Portal has entry surface, exit transform, sheet map and lineage event. | S5,S6,S7,S9 pp. 2-7;5-12;18-25;5-8 |
| K06 | Game technology | Deterministic network/event replication | translate | Replicate authoritative events and schema versions, not every visual frame. | S6 pp. 8-12 |
| K07 | Game technology | Graphics preview component | retain | Optional GPU or CPU preview; no authority over simulation. | S1,S3,S6 pp. 10-15;1-10;9-10 |
| H01 | Hardware endpoint | Bounded Compatibility Event (B.C.E.) | retain | Reuse the core event schema for a measured optofluidic front end. | S5 pp. 1-12 |
| H02 | Hardware endpoint | Local support -> liquid lens -> mode -> guard | retain | Separate optical, fluid, mode and digital-control models. | S5 pp. 3-9 |
| H03 | Hardware endpoint | Matrix-in-glass | retain | Treat as a measured passive/tunable transfer matrix, not stored imagery. | S5 pp. 2-5 |
| H04 | Hardware endpoint | One-bit hardware route flag | retain | Store amplitudes, thresholds, uncertainty and lineage separately. | S5 pp. 2-7 |
| H05 | Hardware endpoint | Spherical throughput metric | retain | Report support, compatibility, miss/false rates, energy, latency and drift. | S5 pp. 3,6,9-12 |
| H06 | Hardware endpoint | Hollowlens-0 demonstrator | retain | Prototype only after guard, compatibility, calibration and baseline are preregistered. | S5 pp. 4,8-10 |
