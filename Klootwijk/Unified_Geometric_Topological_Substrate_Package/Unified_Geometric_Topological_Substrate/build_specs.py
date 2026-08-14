from __future__ import annotations
import csv, json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPECS = ROOT / 'specs'
SPECS.mkdir(parents=True, exist_ok=True)

sources = [
    dict(id='S1', short='NUM19', filename='numeric-fractal-dialogue.pdf', pages=30, role='Numeric, phonetic, binary, triangle, Pascal/Sierpinski, graphics and topology motif chain.'),
    dict(id='S2', short='AUTHOR_DIALOGUE', filename='author-dialogue-bundle-[identifiers-omitted].pdf', pages=52, role='Extended dialogue bundle; duplicates the D/B/phi-to-R thread and adds AR, cognition, networking, and narrative extrapolations.'),
    dict(id='S3', short='KC_GRAPHICS', filename='kc-vector-graphics.pdf', pages=10, role='Graphics adapter: log-polar mapping, SDF/CSG, phasor-style coverage, 1-bit temporal/spatial modulation, chromatic offsets, prepress.'),
    dict(id='S4', short='BEN_BURGER', filename='ben-burger-zero-index-dialogue.pdf', pages=19, role='Zero-based indexing, split-oval/torque wave motif, overlapping semicircles, shared-domain interpretation.'),
    dict(id='S5', short='WAVEGUIDE', filename='spherical-throughput-waveguide.pdf', pages=12, role='Bounded optofluidic hardware translation, B.C.E. logic, metrics, fabrication and kill criteria.'),
    dict(id='S6', short='CHRONO_SYNTHESIS', filename='chronological-spherical-substrate-synthesis.pdf', pages=12, role='Mature internal synthesis: query-first event calculus, local spherical support, compatibility, lineage, feasibility discipline.'),
    dict(id='S7', short='HOLLOWLAND', filename='hollowland-double-vacuum.pdf', pages=36, role='Double-vacuum, phase sheets, analytic cones, hourglass routing, procedural grammar, kinematic calculus and highly speculative extensions.'),
    dict(id='S8', short='GEORGE_BUNDLE', filename='george-dialogue-bundle.pdf', pages=42, role='Substantially overlapping D/B/phi-to-R dialogue bundle; later pages add perception, storage and related extrapolations.'),
    dict(id='S9', short='D_TO_PH', filename='d-to-ph-glyph-topology.pdf', pages=34, role='Core glyph morph, parity hinge, log-polar/L-system, SDF-global hinge and topology motif thread.'),
]

concepts = [
# id, category, name, source expression, normalized operator, status, sources, pages, notes
('N01','Numeric/fractal','Radix carry threshold','Digit-count changes at powers of the radix.','Use radix powers as scale/change boundaries and compact level indices.','retain','S1','1-4','Exact for positional number systems.'),
('N02','Numeric/fractal','Zero-based offset semantics','An index of 35 denotes the 36th stored position.','Keep value, offset and ordinal position as distinct typed quantities.','retain','S4','1-3','Prevents off-by-one errors; not altered arithmetic.'),
('N03','Numeric/fractal','Active-bit/Hamming-weight filter','19 = 10011 has three active bits; zeros are treated as inactive.','Use popcount as a sparse feature count or seed descriptor.','translate','S1','3-5','The phonetic syllable link is a mnemonic, not a general encoding law.'),
('N04','Numeric/fractal','Three-point triangle seed','Three active positions are treated as triangle anchors.','Map three non-collinear active samples to a simplex/triangle primitive.','translate','S1','6-7','Any three non-collinear points form a triangle; the mapping is chosen.'),
('N05','Numeric/fractal','Pascal parity to Sierpinski','Odd/even entries in Pascal triangle form a Sierpinski pattern.','Use binomial parity as a deterministic fractal/test-pattern generator.','retain','S1','6-9','Technical correction: rows 2^k-1, not generally 2^k, are all odd when indexed from zero.'),
('N06','Numeric/fractal','Golden-angle/Fibonacci sampling','Phi/Vogel spacing is proposed to avoid visible repetition.','Optional quasi-uniform angular sample schedule or dither seed.','translate','S1','13-15','Useful heuristic; it does not guarantee zero aliasing or zero cost.'),
('N07','Numeric/fractal','Lemniscate/strange-loop recursion','Infinity and Escher loops symbolize self-generation.','Represent recursion with explicit finite grammar depth and cycle detection.','demote','S1','18-23','Keep as a recursion motif, not a proof of self-creating physics.'),

('G01','Glyph/kinematic','Loop-plus-stem decomposition','Chosen phi/D/B glyphs are decomposed into loop(s) plus a stem.','Represent glyph geometry as a graph of curve segments and junctions.','translate','S9,S2,S8','1-2','Glyph form varies by font; the decomposition is a design convention.'),
('G02','Glyph/kinematic','Cut-unroll D/B to R','Break the lower loop and straighten the released arc into a diagonal leg.','Boundary-graph edit plus continuous curve morph from closed arc to open segment.','retain','S9,S2,S8','1-4','Implementable as path topology and control-point interpolation.'),
('G03','Glyph/kinematic','Torque axis T','The stem is an axis; rotation shears/unreels the lower loop.','Use a rotation/warp parameter around a declared pivot axis.','translate','S9,S2,S8','1-4','Torque language is a kinematic metaphor unless a physical model is supplied.'),
('G04','Glyph/kinematic','Delta-time and phase modulation','Delta T and delta phi drive movement and phase change.','Store continuous time and phase as separate state coordinates and derivatives.','retain','S1,S7,S9','10-15;14-18;2-5','Do not overload time, torque and triangle into one untyped symbol.'),
('G05','Glyph/kinematic','One-bit parity hinge','A bit toggles closed/open or route A/B.','Use a schema-bound route/parity flag that selects transition behavior.','retain','S5,S6,S7,S9','2-8;5-7;14-25;3-8','The bit is not the complete state.'),
('G06','Glyph/kinematic','Global hinge field','The hinge is applied everywhere through an SDF sign/state change.','Model a global morph or transition field evaluated at every query point.','translate','S9,S2,S8','7-8','A morph parameter changes the implicit field; topology changes require explicit handling.'),
('G07','Glyph/kinematic','Chirality/orientation flip','R/S or mirrored states are associated with sign/orientation reversal.','Track an orientation bit and apply a gluing/transition map that may flip it.','retain','S1,S7,S9','21-29;18-25;4-8','Orientation is distinct from sheet and phase.'),
('G08','Glyph/kinematic','Split oval to opposing arches','A zero-centered oval is split and torque opens it into positive/negative wave arches.','Use symmetric curve branches around a fixed node for waveform or deformation profiles.','translate','S4','10-16','The exact 1:1 amplitude condition is a chosen symmetric case, not universal warped-disk physics.'),
('G09','Glyph/kinematic','Overlap lens/shared domain','Slightly overlapping semicircles form an interference/tolerance/shared-information zone.','Use intersection A∩B, lens area, or blend region as explicit shared domain.','retain','S4','16-19','Interpretation depends on geometry, mechanics or information semantics.'),

('I01','Implicit geometry','Signed distance/implicit field','Geometry is represented by f(p), with f=0 as the boundary.','Use implicit scalar fields; reserve exact-distance claims for valid primitives/transforms.','retain','S1,S3,S6,S7,S9','10-30;1-10;5-10;14-31;7-8','A generic implicit field need not be an exact SDF.'),
('I02','Implicit geometry','SDF CSG operators','Union=min, intersection=max, subtraction=max(a,-b).','Provide composable implicit-field operators with documented sign convention.','retain','S3','1-3','Smooth variants may be added as optional adapters.'),
('I03','Implicit geometry','Zero surface as event relation','The SDF-zero locus becomes a transition surface, not a place to march through.','Treat R_j(q)=0 as an event guard and solve crossing time.','retain','S6,S5,S7','5-7;3-7;14-31','This is the central correction from rendering to event semantics.'),
('I04','Implicit geometry','Analytic kinematic sweep','A cone/trajectory is solved against an implicit boundary for exact event time.','Use closed-form roots for restricted trajectory/surface pairs; certified numerical roots otherwise.','retain','S6,S7','7-12;14-31','No universal non-iterative solver exists.'),
('I05','Implicit geometry','Cone as support/domain','Cones are directional influence, field-of-view or admissibility domains.','Use analytic radial-angular support predicates for pruning/query scope.','retain','S5,S6,S7','3-6;5-10;12-25','Not necessarily a rendered cone.'),
('I06','Implicit geometry','Spherical/local radial-angular support','Spherical means a local chart around a sensor/coupler, not a global world remesh.','Represent local support by radius, angle, orientation, uncertainty and time window.','retain','S5,S6','3-6;1-10','Core type-safety rule.'),
('I07','Implicit geometry','Nested shells','Shells organize radial reach, scale and relevance.','Use concentric support bands or multiresolution radial intervals.','translate','S6,S7','1-7;12-25','Useful local indexing structure, not required globally.'),
('I08','Implicit geometry','Hourglass/quad routing','Four conical chambers meet at a pinch/event locus.','Implement a finite routing partition keyed by sign/sheet/orientation at a transition surface.','translate','S6,S7','5-7;23-25','The pinch is an event/router, not a literal singularity that destroys data.'),
('I09','Implicit geometry','Invariant/eigen-axis','A central axis or mode persists through transformations.','Declare invariants and preserved quantities for transitions.','retain','S1,S6,S7','15-20;5-12;18-25','Eigenlanguage is only literal when a linear operator is actually defined.'),
('I10','Implicit geometry','Projective/homogeneous chart','Null-cone and projective language compactifies direction/scale.','Optional homogeneous coordinates for intersections and points at infinity.','translate','S6,S7','5-7;18-25','Use only where it improves equations and conditioning.'),

('C01','Coordinates/sampling','Log-polar transform','rho=ln(r), theta=atan2(y,x).','Use a local coordinate chart that turns radial scaling into translation in rho.','retain','S1,S3,S7,S9','10-15;1-10;12-31;5-8','Handle r=0 with an epsilon/core cell.'),
('C02','Coordinates/sampling','One-bit log-polar LUT','A bitmask activates radial-angular sectors.','Use as a coarse admission/cache mask, never as the whole world state.','retain','S1,S3,S7,S9','10-15;1-10;12-31;5-8','Schema and quantization parameters are mandatory.'),
('C03','Coordinates/sampling','Phasor/Feynman-style edge accumulation','Subpixel samples carry magnitude/phase and are accumulated.','Normalize to complex phasor or oriented coverage accumulation for antialiasing.','translate','S3','1-8','Not a literal Feynman path integral unless a physical path-integral model is defined.'),
('C04','Coordinates/sampling','One-bit stochastic jitter','Binary noise shifts samples/thresholds around an edge.','Use deterministic blue-noise/hash dithering with reproducible seeds.','retain','S1,S3','10-15;7-10','Jitter trades structured error for noise; it does not remove error.'),
('C05','Coordinates/sampling','Temporal pulse-density modulation','Brightness/coverage is encoded as density of one-bit pulses.','Optional display-output adapter using PDM or delta-sigma modulation.','translate','S3','4-6','Panel hardware and refresh limits remain.'),
('C06','Coordinates/sampling','Chromatic log-radius offset','Channel scaling becomes additive rho offsets.','Apply channel-specific log-radius shifts before field evaluation, then resample correctly.','retain','S3','7-8','Cheap coordinate arithmetic is not zero-cost end-to-end correction.'),
('C07','Coordinates/sampling','Log-polar prepress screening','Spatial one-bit dots scale with rho and orient with theta.','Optional print adapter with calibrated halftone, screen angles and dot-gain compensation.','translate','S3','8-10','Requires press/paper calibration.'),

('T01','Topology','Phase sheets','Multiple states occupy layered sheets over the same base coordinate.','Represent state as base position plus sheet, phase, orientation and address.','retain','S6,S7,S9','5-10;14-25;5-8','Layer identity must be explicit.'),
('T02','Topology','Double vacuum','Co-located states do not interact when phase/sheet/address are incompatible.','Compatibility-gated coupling: same x does not imply same sector.','retain','S5,S6,S7','2-7;5-10;14-25','One of the strongest corpus concepts.'),
('T03','Topology','Mobius gluing','A boundary identification reverses orientation after one loop.','Implement quotient-map boundary wrapping with orientation flip.','retain','S7,S9','7-12;5-8','Use a chart/gluing abstraction rather than literal 4D geometry.'),
('T04','Topology','Klein-bottle gluing','A closed non-orientable quotient is used for looping routes.','Implement two rectangle-edge identifications, one orientation reversing.','translate','S5,S7,S9','2,5;7-25;5-10','Hardware realization remains frontier; 3D pictures self-intersect.'),
('T05','Topology','Topological portal/gluing map','Crossing a boundary re-enters another chart/sheet, possibly transformed.','Use explicit port, orientation map, coordinate transform and transfer metadata.','retain','S5,S6,S7','2-5;5-12;14-25','This makes topology technically testable.'),
('T06','Topology','Inside/outside sign with schema','Binary sign denotes interior/exterior or route state.','Bind every bit to a declared schema/version and keep uncertainty separate.','retain','S3,S5,S7,S9','1-10;2-7;14-31;3-8','Raw bits without layout/schema are ambiguous.'),
('T07','Topology','Strange loop/self-reference','Escher/Klein motifs suggest systems feeding back into themselves.','Use explicit cycles, fixed points and termination/cycle policies in the grammar/event graph.','demote','S1,S7,S9','18-30;7-25;5-10','Narrative inspiration only unless formally specified.'),

('A01','Information architecture','Finite grammar G','A finite rule set generates relations/structures.','Use bounded-depth typed productions that compile to supported relation primitives.','retain','S6,S7,S9','1-12;26-31;5-8','Enforce symbol and expression caps.'),
('A02','Information architecture','State manifold Q','State includes position, time, phase, sheet, address and branch.','Use a typed immutable state record; optional orientation and uncertainty extensions.','retain','S6','5-7','Core data model.'),
('A03','Information architecture','Relation family R_j(q)=0','World geometry/constraints are equations rather than frame snapshots.','Store typed relations with parameters, domains and solver capability metadata.','retain','S6','5-12','Restrict to relation families with known solvers for the prototype.'),
('A04','Information architecture','Support predicate C<=0','Only relations inside a declared local support are candidates.','Separate admission/support from geometry and from compatibility.','retain','S5,S6','3-7;5-12','Supports analytic pruning.'),
('A05','Information architecture','Compatibility predicate chi','Co-location is insufficient; phase/sheet/mode/time/policy must match.','Compose physical and digital compatibility predicates.','retain','S5,S6','3-7;5-12','Return reason codes, not only a bit.'),
('A06','Information architecture','Event time t*','The next event is the earliest supported compatible relation root.','Compute min valid root after t0 with tolerance and confidence.','retain','S5,S6','3-7;5-12','Multiple roots and tangencies need policy.'),
('A07','Information architecture','Transition rule T_j','Crossing an event surface updates sheet/phase/branch/invariants.','Use pure transition functions producing state patches and event records.','retain','S5,S6','5-7;5-12','Preserve pre/post states and provenance.'),
('A08','Information architecture','Lineage address','Identity persists by generative address and invariant history.','Use stable entity IDs plus parent/merge ancestry and transition lineage.','retain','S5,S6,S7','3-12;1-12;26-35','Coordinates are not identity.'),
('A09','Information architecture','Irreducible external event log','Novel exogenous events must be recorded even when closed dynamics are recomputable.','Event-source only novelty, transitions, confidence and calibration changes.','retain','S5,S6','7-11;1-12','No zero-memory claim.'),
('A10','Information architecture','Query-first API','Ask state_at(t), next_event, events_in_support, coupling and identity.','Expose direct query methods independent of a frame loop.','retain','S5,S6','3-12;1-12','Projection is downstream.'),
('A11','Information architecture','Projection adapter','Images are optional outputs, not the authoritative state.','Place raster/raymarch/SDF preview in a replaceable adapter layer.','retain','S3,S6','1-10;1-12','Do not mistake the projector for the state space.'),
('A12','Information architecture','Hybrid layer separation','Persistent world state, local sensing and display remain distinct.','Use core/query/projection/hardware modules with explicit interfaces.','retain','S5,S6','2-12;1-12','Avoid polar-everything and raster-everything.'),
('A13','Information architecture','Branch and chamber routing','Events route state through branches/sheets/chambers.','Use finite enums and explicit routing tables.','retain','S6,S7','5-12;23-31','Avoid implicit magic routing.'),
('A14','Information architecture','Uncertainty/confidence','Verified outputs include error, confidence and calibration.','Attach numeric intervals/confidence and solver status to every event.','retain','S5,S6','1-12;8-12','Essential for real systems.'),
('A15','Information architecture','Schema-bound packed data caution','Raw packed bits are meaningless without layout metadata.','Version all bitfields/LUTs and ship schema with data.','retain','S2,S8,S9,S5','27-29;26-28;26-28;7','Useful contrast from the COBOL sections.'),
('A16','Information architecture','Agent on shared relation substrate','Perception/action can issue the same support/event queries.','Keep agent integration minimal: queries and transition choices, not universal AI compression.','translate','S6,S7','11-12;34-36','Do not claim an LLM is replaced by the geometry.'),

('K01','Game technology','Analytic motion component','Position/velocity/acceleration are closed-form trajectories.','Entity component stores trajectory coefficients and state patches.','retain','S6,S7,S4','7-12;26-31;10-16','Supports horizon skipping for fixed formulas.'),
('K02','Game technology','Continuous collision/event component','Collisions are relation roots under support/compatibility.','Event solver returns ordered crossings with guard semantics.','retain','S6,S7','7-12;26-31','Fallback numerical solver is allowed.'),
('K03','Game technology','Sensor cone component','Agent/sensor relevance uses local radial-angular supports.','FOV/range query before relation solving.','retain','S5,S6,S7','3-9;5-12;12-25','Useful in Unity/Godot/ECS adapters.'),
('K04','Game technology','Procedural grammar component','L-system/shape grammar generates bounded relation sets.','Compile grammar tokens to primitives, supports and transitions.','retain','S6,S7,S9','11-12;26-31;5-8','Finite depth and normalization required.'),
('K05','Game technology','Topological portal component','Mobius/Klein/hourglass routes connect spaces with orientation/sheet changes.','Portal has entry surface, exit transform, sheet map and lineage event.','retain','S5,S6,S7,S9','2-7;5-12;18-25;5-8','Can be rendered conventionally while simulated symbolically.'),
('K06','Game technology','Deterministic network/event replication','Seed plus event log reconstructs closed dynamics.','Replicate authoritative events and schema versions, not every visual frame.','translate','S6','8-12','Only works where deterministic formulas are stable across platforms.'),
('K07','Game technology','Graphics preview component','SDF/log-polar/jitter projects core state to pixels.','Optional GPU or CPU preview; no authority over simulation.','retain','S1,S3,S6','10-15;1-10;9-10','Provides practical game-engine visualization.'),

('H01','Hardware endpoint','Bounded Compatibility Event (B.C.E.)','A verified event is declared only after support, compatibility and a measured guard crossing.','Reuse the core event schema for a measured optofluidic front end.','retain','S5','1-12','The best-defined physical endpoint in the corpus.'),
('H02','Hardware endpoint','Local support -> liquid lens -> mode -> guard','Radial-angular input is tuned, coupled, interfered and thresholded.','Separate optical, fluid, mode and digital-control models.','retain','S5','3-9','Maxwell, Young-Laplace/coupled-mode theory and control logic stay type-separated.'),
('H03','Hardware endpoint','Matrix-in-glass','A waveguide mesh implements a calibrated transfer function.','Treat as a measured passive/tunable transfer matrix, not stored imagery.','retain','S5','2-5','Requires calibration and drift tracking.'),
('H04','Hardware endpoint','One-bit hardware route flag','Parity denotes admission/route/freshness, not amplitude.','Store amplitudes, thresholds, uncertainty and lineage separately.','retain','S5','2-7','Same type-safety rule as software.'),
('H05','Hardware endpoint','Spherical throughput metric','Count verified events/queries per second at a declared error budget.','Report support, compatibility, miss/false rates, energy, latency and drift.','retain','S5','3,6,9-12','Not photon flux alone.'),
('H06','Hardware endpoint','Hollowlens-0 demonstrator','Scanned input, tunable liquid coupler, 2x2 interferometer, balanced detectors, digital sidecar.','Prototype only after guard, compatibility, calibration and baseline are preregistered.','retain','S5','4,8-10','Can fail usefully.'),
]

claims = [
('CL01','Universal O(1) world/event solving','reject','Only fixed closed expressions and restricted fixed-degree root problems may be horizon-independent; candidate count and solver cost remain.'),
('CL02','Zero memory / under-32MB universal worlds','reject','Parameters can compress some closed dynamics, but entities, branches, exogenous events, calibration and uncertainty consume memory.'),
('CL03','No latency, heat or power','reject','All computation, actuation, detection and display/hardware paths have latency and energy costs.'),
('CL04','One bit contains the complete state','reject','One bit is only a schema-bound flag; numeric state, uncertainty, lineage and parameters remain separate.'),
('CL05','Golden ratio eliminates aliasing at zero cost','demote','Golden-angle schedules can reduce regularity but require sampling, reconstruction and error analysis.'),
('CL06','Feynman vectors are a standard quantum rasterizer','translate','Use the phrase only as inspiration; the implementation is complex phasor/oriented supersampling.'),
('CL07','Klein bottle physically self-assembles matter','reject','Use quotient/gluing maps in software; no physical self-assembly claim is supported.'),
('CL08','Möbius strip is simply half a Klein bottle','correct','Certain cuts/decompositions relate them, but the statement is not a general unique identity.'),
('CL09','Rows at powers of two in Pascal are all ones/odd','correct','With zero-based row indexing, rows 2^k-1 are all odd; Pascal parity still yields the Sierpinski pattern.'),
('CL10','C(5,3)=10 proves the decimal threshold relation','demote','It is a valid combination count and an interesting coincidence, not a causal structural proof.'),
('CL11','Log mapping removes the origin singularity','correct','Log mapping relocates/rescales the singular behavior; an epsilon/core chart is still required.'),
('CL12','Analytic SDF intersections are always exact and non-iterative','reject','Only selected field/trajectory pairs have closed-form roots; generic cases need numerical/certified methods.'),
('CL13','All BVH/broad-phase structures become unnecessary','reject','Strong support/compatibility filters may replace or complement broad phase in restricted domains; generic scenes still need indexing.'),
('CL14','The topology solves the Von Neumann bottleneck','reject','Data locality may improve, but instruction/data movement and memory hierarchy remain physical constraints.'),
('CL15','World geometry directly replaces general AI/LLMs','reject','A shared query substrate can host agents, but it does not replace model weights, learning, semantics or inference complexity.'),
('CL16','Biology, dreams, economies and wireless auras instantiate the same exact mechanism','reject','These are narrative analogies in the source bundle, not part of the technical unification.'),
('CL17','Chromatic correction is zero-cost','correct','Log-space offsets are cheap, but channel evaluation, filtering, resampling and calibration still cost resources.'),
('CL18','Rasterization and raymarching are forbidden','correct','They are optional downstream projection tools; they do not define the authoritative substrate.'),
]

architecture = {
  'name': 'UGTS-0',
  'title': 'Unified Geometric-Topological Substrate - Equation World Zero',
  'version': '1.0.0',
  'state_space': {
    'position': 'R^2 in reference implementation; extensible to R^n/projective charts',
    'time': 'continuous real scalar',
    'phase': 'angle on S^1',
    'sheet': 'small finite enum / Z2 in prototype',
    'orientation': '+1 or -1',
    'lineage_address': 'stable entity id plus ancestry',
    'branch': 'finite branch/chamber id',
    'uncertainty': 'nonnegative scalar or interval metadata',
  },
  'world': ['finite_grammar', 'relations', 'supports', 'compatibility_rules', 'transitions', 'invariants', 'external_event_log'],
  'queries': ['state_at', 'next_event', 'events_in_support', 'can_couple', 'apply_transition', 'reconstruct_identity'],
  'layers': [
    {'name':'authoritative substrate','contains':['typed state','relations','topology/gluing','lineage','event log']},
    {'name':'query/runtime','contains':['support admission','compatibility','event solving','transition routing']},
    {'name':'adapters','contains':['game/ECS','graphics/SDF/log-polar','hardware/B.C.E.']},
  ],
  'constraints': [
    'one-bit values are schema-bound flags only',
    'local polar/spherical charts do not replace the global world model',
    'closed-form claims are limited to declared solver families',
    'all events carry confidence/status/lineage',
    'projection is optional and non-authoritative',
  ]
}

world_schema = {
  '$schema': 'https://json-schema.org/draft/2020-12/schema',
  'title': 'UGTS-0 World Definition',
  'type': 'object',
  'required': ['schema_version','entities','relations'],
  'properties': {
    'schema_version': {'type':'string'},
    'entities': {'type':'array','items':{'$ref':'#/$defs/entity'}},
    'relations': {'type':'array','items':{'$ref':'#/$defs/relation'}},
    'topology': {'type':'array','items':{'type':'object'}},
    'metadata': {'type':'object'},
  },
  '$defs': {
    'vec2': {'type':'array','prefixItems':[{'type':'number'},{'type':'number'}],'minItems':2,'maxItems':2},
    'entity': {
      'type':'object','required':['id','trajectory'],
      'properties': {
        'id':{'type':'string'},
        'trajectory':{'type':'object','required':['type','p0','v0','t0'],'properties':{
          'type':{'enum':['linear','quadratic']},'p0':{'$ref':'#/$defs/vec2'},'v0':{'$ref':'#/$defs/vec2'},
          'a':{'$ref':'#/$defs/vec2'},'t0':{'type':'number'}}},
        'phase':{'type':'number'},'sheet':{'type':'integer'},'orientation':{'enum':[-1,1]},
        'branch':{'type':'string'},'tags':{'type':'array','items':{'type':'string'}},
      }
    },
    'relation': {
      'type':'object','required':['id','surface','transition'],
      'properties': {
        'id':{'type':'string'},
        'surface':{'type':'object'},
        'support':{'type':'object'},
        'compatibility':{'type':'object'},
        'transition':{'type':'object'},
      }
    }
  }
}

example_world = {
  'schema_version':'1.0.0',
  'metadata':{'description':'Minimal double-vacuum and parity-hinge demonstration.'},
  'entities':[
    {'id':'traveler_A','trajectory':{'type':'linear','p0':[-2.0,0.25],'v0':[1.0,0.0],'t0':0.0},'phase':0.0,'sheet':0,'orientation':1,'branch':'A','tags':['player']},
    {'id':'co_located_B','trajectory':{'type':'linear','p0':[0.0,0.25],'v0':[0.0,0.0],'t0':0.0},'phase':3.141592653589793,'sheet':1,'orientation':-1,'branch':'B','tags':['ghost']}
  ],
  'relations':[
    {'id':'x_zero_hinge','surface':{'type':'line','normal':[1.0,0.0],'offset':0.0},
     'support':{'type':'radial_angular','origin':[0.0,0.0],'r_min':0.0,'r_max':3.0,'theta_center':0.0,'theta_half_width':3.141592653589793},
     'compatibility':{'allowed_sheets':[0],'phase_center':0.0,'phase_tolerance':0.2,'required_tags':['player']},
     'transition':{'toggle_sheet':True,'flip_orientation':True,'set_branch':'B','phase_delta':1.5707963267948966}}
  ],
  'topology':[{'type':'mobius_band','width':4.0,'height':2.0}]
}

# Write files
with open(SPECS/'sources.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=sources[0].keys()); w.writeheader(); w.writerows(sources)
with open(SPECS/'concept_inventory.csv','w',newline='',encoding='utf-8') as f:
    fields=['id','category','name','source_expression','normalized_operator','status','sources','pages','notes']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for row in concepts:
        w.writerow(dict(zip(fields,row)))
with open(SPECS/'claims_ledger.csv','w',newline='',encoding='utf-8') as f:
    fields=['id','source_claim','disposition','technical_reason']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for row in claims: w.writerow(dict(zip(fields,row)))
(SPECS/'architecture.json').write_text(json.dumps(architecture,indent=2,ensure_ascii=False),encoding='utf-8')
(SPECS/'world_schema.json').write_text(json.dumps(world_schema,indent=2,ensure_ascii=False),encoding='utf-8')
(SPECS/'example_world.json').write_text(json.dumps(example_world,indent=2,ensure_ascii=False),encoding='utf-8')

# Also produce compact markdown inventories.
md=['# Concept inventory','', '| ID | Category | Concept | Status | Normalized operator | Sources |', '|---|---|---|---|---|---|']
for row in concepts:
    cid,cat,name,src,norm,status,sources_ref,pages,notes=row
    md.append(f'| {cid} | {cat} | {name} | {status} | {norm.replace("|","/")} | {sources_ref} pp. {pages} |')
(SPECS/'concept_inventory.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

print(f'Wrote {len(concepts)} concepts and {len(claims)} claims.')
