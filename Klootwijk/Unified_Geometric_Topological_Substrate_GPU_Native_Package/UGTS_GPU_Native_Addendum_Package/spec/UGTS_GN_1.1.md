# UGTS-GN 1.1 — GPU-Native Geometric–Topological Substrate

## 1. Scope

UGTS-GN 1.1 is the GPU-native and physical-device addendum to the unified geometric–topological substrate. It deliberately removes game-engine adapters from the target architecture. The authoritative interfaces are:

1. a typed state and event ABI;
2. SPIR-V compute modules and a direct Vulkan runtime;
3. a fixed-function hardware mapping for FPGA/ASIC implementations; and
4. a bounded optofluidic/waveguide endpoint using the same support–compatibility–guard–commit semantics.

The substrate is query-first. It evaluates local support, compatibility and relation guards, commits verified transitions, and retains lineage plus irreducible novelty. Rendering, display and print remain optional downstream projections.

## 2. Corpus normalization rule

A source motif enters the technical core only when it can be expressed as one of:

- a typed field or unit;
- a coordinate/chart transform;
- a support predicate;
- a relation or event surface;
- a compatibility predicate;
- a transition/routing map;
- a lineage/invariant rule;
- a calibrated physical transfer function; or
- a measurable performance, error, energy or memory quantity.

Metaphors that cannot be typed or measured are kept in the claims ledger as hypotheses, analogies or rejected claims.

## 3. Canonical state

A conceptual state is

```text
q = (x, t, phase, sheet, orientation, address, branch, policy, uncertainty)
```

The bundled compute profile implements the hot subset needed for a spherical-support event query:

```text
position xyz
query time t
support axis xyz
radial reach R
angular threshold cos(alpha)
phase
relation guard epsilon
confidence floor
sheet
orientation
compatibility mask
lineage seed
```

### 3.1 G64 authoritative record

`G64State` is 64 bytes and preserves float32 geometric fields.

| Offset | Bytes | Field | Meaning |
|---:|---:|---|---|
| 0 | 16 | `position_time` | x, y, z, t |
| 16 | 16 | `axis_radius` | axis x, y, z, radial reach |
| 32 | 16 | `phase_guard` | cone cosine, phase, guard epsilon, confidence floor |
| 48 | 16 | `meta` | sheet, orientation, compatibility mask, lineage seed |

### 3.2 G32 packed record

`G32State` is 32 bytes. Six pairs of float values are stored as IEEE binary16; topology fields are packed into one word. This profile halves dense state-plus-event traffic but requires a quantization contract. It must not be used where the guard band is smaller than the accumulated coordinate/normal/radius error.

### 3.3 Event records

`E32Event` is a 32-byte diagnostic event. `E16Event` is a 16-byte compact event. Both carry a verified bit, route, lineage hash and state flags. E16 packs guard and confidence as binary16.

A lineage hash is a compact checksum, not a cryptographic identity. Durable identity requires the full generative address and ordered event record.

## 4. Reference query

For candidate `i`:

```text
r              = length(position)
cos_to_axis    = dot(position/r, normalize(axis))
in_support     = (r <= R) and (cos_to_axis >= cone_cos)
compatible     = mode_bit and sheet==target_sheet and orientation==target_orientation
sdf            = r - R
guard           = abs(sdf) - epsilon
confidence      = 2^(-32*abs(sdf))
verified        = in_support and compatible and guard<=0 and confidence>=floor
route           = orientation xor verified
lineage_hash    = mix32(lineage_seed xor candidate_index)
```

The confidence law is a reproducible synthetic benchmark function, not a universal statistical model.

## 5. Native compiler pipeline

```text
finite grammar / typed query
        ↓
UGTS hot-state ABI (G64 or G32)
        ↓
GLSL 450 compute source
        ↓
SPIR-V 1.4 module
        ↓
Vulkan shader module + pipeline layout
        ↓
compute pipeline + vendor pipeline cache
        ↓
GPU dispatch → E32/E16 results → optional verified-event compaction
```

The package contains four SPIR-V modules:

- G64 evaluate;
- G64 evaluate plus atomic commit counters;
- G32 evaluate; and
- G32 evaluate plus atomic commit counters.

The runtime descriptor layout reserves set 0, bindings 0-2: state, event and counters. Evaluate-only modules may optimize the unused counter binding out of the final SPIR-V interface; evaluate+commit modules expose all three bindings. The local workgroup is 256x1x1. `gpu/spirv/spirv_manifest.json` records hashes, instruction counts, entry points, local size and descriptor decorations.

The direct runtime is `ugts_vulkan_bench`. ANGLE/SwiftShader appears only as a reproducible bootstrap compiler in this container; it is not the target runtime. Production targets compile the Vulkan GLSL with glslang/DXC or another conformant tool and execute the SPIR-V through the vendor Vulkan driver.

### 5.1 Reference query convention

The bundled benchmark modules use a fixed query convention: target sheet 1, target orientation 0, and compatibility-mask bit 2. The portable JSON schema and CPU oracle support explicit query values. A production native module should expose those values through specialization constants, push constants or a query buffer, or compile a versioned fixed-query variant.

## 6. Compute/commit split

### Evaluate

Every invocation independently writes an event record. No global atomics are required. This is the maximum-throughput diagnostic path.

### Evaluate + commit

The same event evaluation additionally increments four global counters: candidates, support survivors, compatibility survivors and verified events. Atomic contention makes this path slower. A production system should use subgroup/local reductions or verified-event compaction when global counts are required at scale.

## 7. Event compaction

The benchmark deliberately writes dense output so every invocation can be validated. A production novelty log should retain only verified events:

```text
predicate → subgroup ballot → block prefix → global block offsets → compact E16/E32 append
```

The package reports an Event Compaction Ratio derived from observed event yield. That ratio is a memory model, not a measured compaction-kernel speed.

## 8. Native performance vocabulary

| Symbol | Name | Definition |
|---|---|---|
| CER | Candidate Evaluation Rate | candidates evaluated / device time |
| SET | Spherical Event Throughput | verified events / device time |
| ESB | Effective Substrate Bandwidth | logical state+event bytes / device time; not external DRAM bandwidth |
| SRG | Support Rejection Gain | candidates / supported |
| CRG | Compatibility Rejection Gain | supported / compatible |
| EY | Event Yield | verified / candidates |
| CPC | Cold Pipeline Compilation | first `vkCreateComputePipelines` latency |
| CPH | Cache-Seeded Pipeline Hydration | pipeline creation with persisted cache data |
| NPF | Native Program Footprint | SPIR-V bytes and driver cache/binary bytes |
| SCR | State Compression Ratio | G64/E32 dense bytes / G32/E16 dense bytes |
| ECR | Event Compaction Ratio | dense output bytes / verified-only output bytes |
| SNC | State-plus-Novelty Compression | G64/E32 dense / (G32 state + compact E16 events) |
| CCF | Commit Cost Factor | evaluate+commit p50 / evaluate p50 |
| PCP | Packed Compute Penalty | G32 evaluate p50 / G64 evaluate p50 on a named target |

All metrics are meaningful only when device, batch size, record profile, mode, precision, error budget and timing method are reported.

## 9. Memory formulas

For `N` candidates and `V` verified events:

```text
G64/E32 dense             = N × 96 bytes
G32/E16 dense             = N × 48 bytes
G32 + compact E16 novelty = N × 32 + V × 16 bytes
compact E16 log only      = V × 16 bytes
```

The last configuration is valid only when authoritative state is retained elsewhere or reconstructible from seed, grammar, invariants and event log.

A one-bit support mask is `ceil(N/8)` bytes, but it is only a predicate cache. It is not a replacement for state.

## 10. Physical fixed-function mapping

```text
state SRAM / input stream
   ↓
position norm + support-axis dot product
   ↓
radial and angular comparators
   ↓
sheet/orientation/mode compatibility mask
   ↓
relation function + guard/hysteresis
   ↓
confidence/SNR threshold
   ↓
route + lineage update
   ↓
verified-event FIFO / DMA / actuator command
```

An FPGA/ASIC implementation may use fixed point, block floating point or FP16. The numeric contract must declare range, quantization error and guard margin. The Vulkan ABI supplies the reference behavior and golden vectors.

## 11. Optofluidic/waveguide mapping

```text
bounded radial-angular input
   ↓
liquid lens / overclad tuning
   ↓
mode-overlap coupling
   ↓
waveguide phase/interference
   ↓
mode + policy compatibility
   ↓
balanced detector guard crossing
   ↓
digital B.C.E. commit, confidence, lineage and log
```

Maxwell, coupled-mode theory and fluid mechanics remain authoritative for the physical transfer. The event substrate does not replace those equations. A Klein or Möbius label is permitted only when ports, orientation and transfer matrix are explicitly specified.

## 12. Pythagorean-cup addendum

The source’s trident and Pythagorean-cup imagery is retained as a useful 3-to-1 threshold/reset pattern:

- three channels converge;
- an accumulator rises;
- crossing a crest latches an event;
- a reset path drains or clears the accumulator; and
- hysteresis prevents chatter.

It is not an absolute vacuum, a free-energy device or a topological energy recycler.

## 13. Numeric and physical corrections

- Standard `100%` is 1. The value 36 is produced only by a versioned custom glyph encoder.
- The corpus contains both `100101₂=37` and a later `100100₂=36`. UGTS-GN labels them as encoder variants and makes the latter canonical for this addendum.
- Multiplication by 1.5 is not an integer bit shift. In log-base-2 coordinates its displacement is `log2(1.5) ≈ 0.5849625`.
- Information in bits is not energy in joules without a physical process. At 298.15 K, erasing 0.680 bits has a Landauer lower bound of approximately `1.94×10^-21 J`; actual devices consume more. The source’s 202.74 J figure is rejected.
- Topological closure does not eliminate loss, latency, memory, heat, calibration or noise.

## 14. Reproducibility and acceptance

A run is accepted only when:

1. all SPIR-V modules parse and expose the declared entry point, local size and bindings;
2. native pipeline creation and cache reload succeed;
3. counter totals equal the CPU oracle;
4. at least the first 4096 output records match the CPU oracle;
5. p50/p95/p99 device and host latency are recorded;
6. device name/type/API and timestamp period are recorded; and
7. `physical_gpu_claim` is false when the selected device is software or CPU.

## 15. Kill criteria

Stop or redesign when compatibility pruning is weak, event/branch density explodes, FP16 error exceeds guard margin, atomic commit dominates, calibration cost erases hardware advantage, physical false-event/miss targets fail, or the digital sidecar performs nearly all useful work.
