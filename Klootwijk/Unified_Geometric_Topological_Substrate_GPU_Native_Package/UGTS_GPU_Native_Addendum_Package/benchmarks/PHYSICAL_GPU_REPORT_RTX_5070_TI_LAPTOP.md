# UGTS-GN physical GPU validation - RTX 5070 Ti Laptop GPU

Run date: 2026-08-15 (Europe/Amsterdam)  
Status: physical discrete-GPU execution verified; direct hardware performance-counter access unavailable.

## Result

The UGTS compute path ran through the NVIDIA Vulkan driver on the local NVIDIA GeForce RTX 5070 Ti Laptop GPU. Storage buffers were allocated from `VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`; host-visible coherent buffers were used only for explicit upload/readback staging. GPU timestamps surround the compute dispatch, not transfer or CPU-oracle work.

This is the closest native path available in the installed Windows environment: direct Vulkan/SPIR-V with no Unity, Godot, browser, ANGLE, or SwiftShader layer. It is not strict bare metal because Windows WDDM, the NVIDIA driver, dynamic laptop clocks, and the OS scheduler remain active.

The selected device also exposes `VK_KHR_shader_clock` with device-scope clocks. A four-process, order-balanced 512-step dependent SSBO chase is flat through the exact 36 MiB reported L2 capacity, rises 1.242x at 38 MiB and 2.134x at 40 MiB, then reaches 4.714x at 64 MiB and 6.295x at 128 MiB relative to 36 MiB. These are implementation-defined shader-clock ticks under a saturated workload, not claimed hardware cycles or nanoseconds.

An independent CUDA 12.8 `sm_120` control uses per-SM `clock64()` cycles and L1-bypassing `ld.global.cg` loads. Across 4-128 MiB tables, a one-warp immediate-hot repeat measures 399.57 cycles per dependent step at the median of sizes, while the same chain after a 256 MiB L2-eviction pass measures 1,087.79 cycles: a 2.722x post-eviction penalty. Complete-kernel CUDA-event time corresponds to 153.4 ns and 401.8 ns per step respectively. Native SASS and zero-spill compiler output verify the intended instruction path. This is exposed warp-step latency, not one scalar transaction's latency.

A second native CUDA matrix scales the same dependent `ld.global.cg` path from one warp to 736 warps (16 per SM). At maximum measured concurrency, immediate-hot requested throughput is 42.863 Gload/s for the exact 36 MiB table and 23.429 Gload/s at 40 MiB, a 45.34% loss for 4 MiB of excess allocation. It falls to 9.318 Gload/s at 64 MiB and 7.506 Gload/s at 128 MiB. This reproduces the capacity boundary in native cycle/throughput measurements and quantifies the scheduling and memory-queue amplification hidden by the one-warp control.

The packed G32 kernel was also run end to end with confidence supplied through Vulkan uniform texel-buffer LUTs. Both an 8,196-byte adjacent-sample layout and a 16,384-byte one-fetch interval-pair layout are semantically valid. Neither provides a stable end-to-end advantage over native `exp2` for this kernel on this GPU: LUT lookup is slower while arithmetic latency is exposed and effectively tied once state/output traffic dominates. A byte-identical SSBO control additionally shows that large random texture-buffer and SSBO reads share the same cache-capacity cliff.

Verified-only G32 event compaction is now implemented and measured. A subgroup-ballot/workgroup-reservation path writes only the 4.75% verified events and reduces all four global counters per workgroup. At 4,194,304 candidates it is 1.528x faster than dense evaluation and 1.869x faster than dense evaluation with per-lane global counters across the original balanced job-order set. A second balanced run uses a bounded 6.25%-capacity event FIFO: it retains every event with zero overflow, reduces the actual output allocation from 64 MiB to 4 MiB (16x), and measures 0.219 ms at the four-process median.

An optional pre-threshold profile removes the per-candidate exponential from the verification predicate and computes confidence only for retained events. It improves append-only medians by 1.0-4.5% at smaller/mid sizes, but converges to +0.03% at 4,194,304 and does not materially improve the counted path. It is therefore a declared alternate G32 ABI, not the default.

A fixed-query G24 hot-state profile then removes fields that the benchmark query does not consume and stores a 6-bit log-distance threshold code. With the same 6.25%-capacity output allocation, this reduces resident state-plus-output allocation from 132 MiB to 100 MiB at 4,194,304 candidates. The direct-decoder control measures 0.168 ms, 1.306x faster than G32 append, and 0.168 ms with reduced counters, 1.312x faster than G32. A separate 128-byte, one-fetch texture-LUT decoder is effectively tied with the direct decoder once bandwidth-bound and slower below L2. The measured win therefore comes from the 24-byte record footprint and shifted cache boundary, not from the LUT itself.

A follow-on G20 experiment splits the 4-byte lineage seed from the five-word hot geometry record and reads it only after verification. Total state storage remains 24 bytes per candidate, but the declared always-hot state-plus-output allocation falls from 100 MiB to 84 MiB at 4,194,304 candidates. Six balanced, sequentially isolated processes measure 1.108x higher append throughput and 1.110x higher counted-path throughput than G24 at that size, with identical counts and validated retained payloads. This is a locality win rather than additional storage compression; the dedicated [yield/compression/limits report](YIELD_COMPRESSION_LIMITS_RTX_5070_TI_LAPTOP.md) gives the human-readable accounting and bounds.

## Hardware and run conditions

| Item | Value |
|---|---:|
| GPU | NVIDIA GeForce RTX 5070 Ti Laptop GPU (Blackwell) |
| CUDA compute capability / SMs | 12.0 / 46 |
| VRAM | 12,227 MiB reported by `nvidia-smi` |
| L2 cache | 37,748,736 bytes (36 MiB), CUDA device-properties query |
| Vulkan | 1.4.325, discrete device, vendor `0x10DE`, device `0x2F18` |
| Driver | NVIDIA 591.59, WDDM |
| Timestamp | 1 ns period, 64 valid bits |
| Vulkan subgroup | 32 lanes; compute basic + ballot supported (8 subgroups per 256-thread workgroup) |
| OS / CPU | Windows 11 build 26200 / Intel Core Ultra 7 255HX |

The direct baseline aggregate covers six independent processes: the three stabilized direct-only runs and three new direct-plus-LUT runs. Cases used a 500-750 ms minimum warmup and 100-200 measured dispatches. The original paired direct/LUT comparison uses the three new processes. A second comparison of direct, adjacent-sample LUT and interval-pair LUT uses four independent processes, two in forward and two in reverse mode order. The G24 attribution control uses six independent processes, three in each job order. The primary G20 comparison likewise uses six processes, but they were explicitly run one at a time; the earlier partially concurrent corpus is retained and excluded. The uniform-texel/SSBO control uses four sequentially isolated processes, two in each program order. The Vulkan shader-clock study adds four sequentially isolated processes, two forward and two reverse, with 750 ms minimum warmup and 100 timed submissions per case. The CUDA cycle study adds four isolated processes, two ascending and two descending table orders, with 50 measured cold/hot pairs after five warmup pairs per table. The CUDA concurrency study adds four sequential processes, reverses both table and warp order, and retains 15 cold/hot pairs after three warmups for each of 55 table/warp cases. Reported latency and rates are medians of process-level device-timestamp, shader-clock, or CUDA cycle p50 values; ranges expose cross-process WDDM and clock variation.

Each timed case repeatedly dispatches against the same resident device-local buffers. Values at or below L2 capacity are therefore intentional cache-hot steady-state measurements, not cold one-pass streaming numbers.

## Core metrics at 4,194,304 candidates

| Profile | Mode | Replicates | Device p50 | Candidate rate | Cross-run rate range | Verified-event rate | Logical bandwidth |
|---|---|---:|---:|---:|---:|---:|---:|
| G64_E32 | evaluate | 6 | 0.746 ms | 5.684 Gcandidate/s | 5.085-6.279 G/s | 278.201 Mevent/s | 545.683 GB/s |
| G64_E32 | evaluate + commit | 6 | 0.822 ms | 5.100 Gcandidate/s | 5.085-6.288 G/s | 249.612 Mevent/s | 489.608 GB/s |
| G32_E16 direct | evaluate | 6 | 0.335 ms | 12.519 Gcandidate/s | 10.206-12.569 G/s | 594.522 Mevent/s | 600.932 GB/s |
| G32_E16 direct | evaluate + commit | 6 | 0.411 ms | 10.206 Gcandidate/s | 7.144-10.242 G/s | 484.669 Mevent/s | 489.894 GB/s |
| G32_E16 LUT | evaluate | 3 | 0.335 ms | 12.526 Gcandidate/s | 12.525-12.567 G/s | 594.834 Mevent/s | 601.248 GB/s |
| G32_E16 LUT | evaluate + commit | 3 | 0.411 ms | 10.195 Gcandidate/s | 10.194-10.199 G/s | 484.140 Mevent/s | 489.360 GB/s |

"Logical bandwidth" is declared input-record bytes plus output-record bytes divided by device time. It is not measured DRAM traffic and can include cache reuse. At this batch size the direct packed G32_E16 path is 2.202x faster than G64_E32 for evaluation and 2.001x faster with atomic commit.

GPU-observed event counts at this size were:

| Profile | Supported | Support + compatible | Verified | Event yield |
|---|---:|---:|---:|---:|
| G64_E32 | 2,213,528 | 368,801 | 205,281 | 4.8943% |
| G32_E16 direct and LUT | 2,085,336 | 346,957 | 199,179 | 4.7487% |

## Inner-working verification

The harness reads back and checks every output record. It verifies scalar distance, guard, confidence, event time where present, support/compatibility/verified flags, route, lineage hash, and state flags. For commit variants it independently derives counts from output flags and requires the four GPU atomic counters to match exactly.

The dispatched SPIR-V performs the complete kernel natively: unpack G32 half pairs where applicable; compute radial length and normalized-axis dot product; apply radial/angular support; apply the sheet/orientation/mask compatibility predicate; evaluate sphere SDF and guard; produce confidence; resolve the verified event and route; hash lineage; write E32/E16 output; and, for commit variants, atomically accumulate the four counters.

The LUT variants replace `exp2(-32 * abs(sdf))` only inside `abs(sdf) < 0.125`. The adjacent-sample layout linearly interpolates 4,097 binary16 confidence samples packed two per `R32_UINT` texel. It occupies 8,196 bytes, or 0.0217% of the 36 MiB L2 cache, and evaluates two sample lookups. The interval-pair layout stores both binary16 endpoints of each of 4,096 intervals in one `R32_UINT` texel. It duplicates interior endpoints, occupies 16,384 bytes or 0.0434% of L2, and requires one lookup per interpolated value. Both use binding 3 as a Vulkan `UNIFORM_TEXEL_BUFFER`; values outside the interval use direct `exp2`, preserving the function's domain.

The compiler produces twenty-six named execution variants and twenty-six `spirv-opt -O` counterparts. All 52 bundled SPIR-V artifacts pass `spirv-val --target-env vulkan1.2`; the native harness measurements use the named non-`.opt` files. Disassembly shows two dynamic calls to the adjacent-sample fetch routine in the named module (two static `OpImageFetch` instructions after optimization), one `OpImageFetch` in the interval-pair module, and one in the G24 log-threshold LUT module. The paired cache probe has one `OpImageFetch` on the uniform-texel path and storage-buffer `OpLoad` instructions on its byte-identical SSBO path. Both shader-clock modules contain two device-scope `OpReadClockKHR` operations; only the 512-step module retains the dependent SSBO-load loop. The one-warp CUDA compiler control uses 17 registers; the concurrency probe uses 16. Both report no stack and no spills. Native `sm_120` SASS shows two `CS2R SR_CLOCKLO` reads and an `LDG.E.STRONG.GPU` in each chase, while each zero-step control has no load. The G24 direct and G20 controls have no `OpImageFetch`. Both G24 modules declare a 24-byte state-array stride; G20 declares a 20-byte stride plus storage binding 4 for lineage, and the optimized module loads lineage after the non-verified early return. Representative NVIDIA pipeline evidence comes from integrated `replicate_1`, with interval-pair rows from `lut_pair/f1`, pre-threshold rows from `prethreshold/f1`, G24 rows from `hot_log_control/f1`, and G20 rows from `cold_lineage_isolated/f1`:

| Program | SPIR-V | NVIDIA pipeline cache | Cache-reloaded creation |
|---|---:|---:|---:|
| G64_E32 evaluate | 4,888 B | 10,068 B | 0.046 ms |
| G64_E32 evaluate + commit | 5,508 B | 11,015 B | 0.095 ms |
| G32_E16 direct evaluate | 5,528 B | 10,001 B | 0.054 ms |
| G32_E16 LUT evaluate | 8,068 B | 12,090 B | 0.149 ms |
| G32_E16 interval-pair LUT evaluate | 7,456 B | 11,345 B | 0.063 ms |
| G32_E16 direct evaluate + commit | 6,148 B | 11,009 B | 0.055 ms |
| G32_E16 LUT evaluate + commit | 8,548 B | 13,085 B | 0.085 ms |
| G32_E16 interval-pair LUT evaluate + commit | 7,936 B | 12,458 B | 0.143 ms |
| G32_E16 pre-threshold subgroup append | 8,660 B | 13,984 B | 0.071 ms |
| G32_E16 pre-threshold subgroup append + counts | 10,328 B | 15,991 B | 0.178 ms |
| G24_E16 direct-threshold subgroup append | 8,824 B | 14,579 B | 0.358 ms |
| G24_E16 direct-threshold subgroup append + counts | 10,492 B | 16,514 B | 0.185 ms |
| G24_E16 log-LUT subgroup append | 9,364 B | 15,065 B | 0.098 ms |
| G24_E16 log-LUT subgroup append + counts | 11,032 B | 16,957 B | 0.087 ms |
| G20_E16 cold-lineage subgroup append | 9,028 B | 14,641 B | 0.071 ms |
| G20_E16 cold-lineage subgroup append + counts | 10,696 B | 16,594 B | 0.086 ms |

The six isolated processes also captured driver-native executable statistics. Values were identical across all six captures:

| Program | Subgroup | Registers | Shared memory | Executable binary |
|---|---:|---:|---:|---:|
| G24 direct append | 32 | 22 | 2,052 B | 3,456 B |
| G20 cold-lineage append | 32 | 22 | 2,052 B | 3,456 B |
| G24 direct append + counts | 32 | 40 | 5,124 B | 4,736 B |
| G20 cold-lineage append + counts | 32 | 39 | 5,124 B | 4,864 B |

These are compiler metadata from `VK_KHR_pipeline_executable_properties`, not performance counters. In particular, the append kernels have identical reported compute-resource use, strengthening the attribution to data locality. NVIDIA reports `Local Memory Size = 68,719,476,736` bytes for every executable, an implausible per-thread value that is preserved in the machine-readable output but explicitly excluded from occupancy claims. The driver returned no internal representation or ISA blob.

Validation volume was 112,529,408 dense semantic outputs in the original baseline aggregate, 167,510,016 in the three integrated performance runs, 25,165,824 in the large semantic-hash audit, 570,425,344 outputs in the two dedicated LUT-cache runs, 58,488,372 dense/compact records in the per-lane append sweep, 122,280,144 in the six counterbalanced subgroup runs, 213,909,504 in the four counterbalanced interval-pair LUT runs, 78,075,696 in the four bounded-capacity compaction runs, 27,430,348 retained/dense records in the capacity sweep, 78,075,696 in the four pre-threshold runs, 103,335,456 in the first four G24 log-LUT runs, 161,725,896 in the six direct-versus-LUT G24 controls, 122,192,592 in the four narrow L2-boundary runs, 290,199,888 in the six cold-lineage runs, and 2,281,701,376 in the four texture/SSBO cache-path controls: **4,413,045,560 checked GPU output records** in the reported aggregates. The Vulkan shader-clock study separately validates 12,582,912 invocation payloads representing 3,221,225,472 dependent SSBO loads. The one-warp CUDA cycle study validates another 153,600 payloads representing 52,428,800 dependent loads. The CUDA concurrency matrix validates 42,883,200 payloads representing 14,637,465,600 dependent loads. Compact validation additionally proves that no non-boundary verified source is missing whenever capacity is sufficient.

At 4,194,304 G32 candidates, direct and both LUT layouts, in evaluate and commit modes, all produced the same 64-bit discrete semantic digest, `1284104115210413112`. The digest covers SDF, guard, topology flags, verified/route state, and lineage while deliberately excluding confidence. Confidence is checked numerically instead: direct G32 maximum absolute error was 0.000262 and both LUT layouts measured 0.000479, inside the declared 0.002 G32 tolerance. Mean absolute errors were 0.000122 and 0.000147 respectively.

The deterministic corpus contains values exactly on `r == radius` and `guard == 0`. NVIDIA and the CPU oracle do not always choose the same side after their different floating-point evaluation paths:

| Profile at N=4,194,304 | CPU/GPU topology divergences | Fraction | Boundary handling |
|---|---:|---:|---|
| G64_E32 | 5,219 | 0.12443% | all inside the explicit `5e-5` predicate-boundary band |
| G32_E16 direct and both LUT layouts | 321 | 0.00765% | all inside the explicit `5e-5` predicate-boundary band |

These are not silently treated as exact agreement. Validation requires exact GPU self-consistency and exact atomic-counter agreement; CPU/GPU topology disagreement is accepted only inside the recorded boundary band. Production semantics that require cross-device bit identity must define fixed-point predicates or explicit hysteresis/interval rules instead of comparing floating-point boundary values directly.

## L2 and texture-buffer findings

The core sweep places declared input-plus-output working sets on both sides of the 36 MiB L2 size:

| Profile / mode | Working set | L2 fraction | Median candidate rate | Change past L2 |
|---|---:|---:|---:|---:|
| G64_E32 evaluate | 36 MiB | 1.00x | 14.047 G/s | - |
| G64_E32 evaluate | 48 MiB | 1.33x | 7.541 G/s | -46.3% |
| G32_E16 evaluate | 36 MiB | 1.00x | 35.708 G/s | - |
| G32_E16 evaluate | 48 MiB | 1.33x | 12.876 G/s | -63.9% |

The G32 value at the exact cache-size boundary showed severe run-to-run variation, including WDDM/power-state outliers, so this is evidence of a capacity transition rather than a measured cache hit rate.

The dedicated cache probe stores two unsigned 16-bit log codes per `R32_UINT` texel and reads them through a Vulkan uniform texel buffer. SPIR-V disassembly confirms `OpTypeImage ... Buffer` and `OpImageFetch`, rather than SSBO loads. Two independent runs produced:

| Access | Packed table | L2 fraction | Median lookup rate | Cross-run range |
|---|---:|---:|---:|---:|
| random | 32 MiB | 0.89x | 41.224 Glookup/s | 41.111-41.336 G/s |
| random | 64 MiB | 1.78x | 7.261 Glookup/s | 7.260-7.263 G/s |
| random | 128 MiB | 3.56x | 6.922 Glookup/s | 6.922-6.922 G/s |
| sequential | 32 MiB | 0.89x | 68.103 Glookup/s | 62.482-73.724 G/s |
| sequential | 64 MiB | 1.78x | 74.407 Glookup/s | 74.399-74.415 G/s |
| sequential | 128 MiB | 3.56x | 75.138 Glookup/s | 75.134-75.141 G/s |

Random lookup throughput falls 82.39% (5.677x slower) from 32 MiB to 64 MiB. Sequential/coalesced access does not suffer that capacity cliff. A packed log LUT is therefore viable when its hot random-access footprint remains below roughly 32 MiB on this 36 MiB-L2 GPU, or when accesses are reordered/coalesced. A larger randomly accessed LUT should be tiled, mip-partitioned, or split into a compact hot index plus colder payload.

For an integrated production kernel, a safer hot-LUT target is about 28 MiB (roughly 14.7 million packed 16-bit entries), leaving L2 space for state lines, output writes, descriptors, and other workloads. This is an engineering margin inferred from this device, not a universal cache rule.

The stricter cache-path control uses identical device-local bytes, packed-code math, index hashes and output writes; only the read descriptor/instruction changes between `UNIFORM_TEXEL_BUFFER`/`OpImageFetch` and `STORAGE_BUFFER`/`OpLoad`. Four isolated processes, two in each program order, produced these random-access medians:

| Packed table | L2 fraction | Texture p50 | SSBO p50 | Paired texture/SSBO rate |
|---:|---:|---:|---:|---:|
| 16 MiB | 0.44x | 0.436240 ms | 0.430776 ms | 0.989x |
| 32 MiB | 0.89x | 0.414680 ms | 0.414840 ms | 1.002x |
| 64 MiB | 1.78x | 4.019752 ms | 4.019576 ms | 0.99995x |
| 128 MiB | 3.56x | 9.694880 ms | 9.694648 ms | 0.99998x |

From 32 to 64 MiB, random texture throughput falls 79.368% (4.847x slower) and SSBO throughput falls 79.359% (4.845x slower). The matching latency and cliff show that `texelFetch` does not provide an additional effective capacity tier for this workload. The result is compatible with different front-end paths converging on the same lower cache/memory bottleneck; without counters it does not prove a specific undocumented NVIDIA cache topology. Small/coalesced cases remain clock/order-sensitive, and the texture path does not show a stable advantage there either.

### Device-clock dependent-load sweep

The sharper native probe surrounds 512 strictly dependent `next[index]` SSBO loads with device-scope realtime-clock reads. A zero-step module measures the clock and surrounding instruction overhead. Four sequentially isolated processes use 65,536 invocations per row, two forward and two reverse program/pattern orders:

| Table | L2 fraction | Random net ticks/load | Relative to 36 MiB | Sequential net ticks/load | Random/sequential |
|---:|---:|---:|---:|---:|---:|
| 4 MiB | 0.111x | 1,383.469 | 0.992x | 1,256.000 | 1.101x |
| 32 MiB | 0.889x | 1,393.234 | 0.999x | 1,311.891 | 1.062x |
| 34 MiB | 0.944x | 1,393.656 | 0.999x | 1,305.063 | 1.068x |
| 36 MiB | 1.000x | 1,394.531 | baseline | 1,303.328 | 1.070x |
| 38 MiB | 1.056x | 1,732.516 | 1.242x | 1,319.859 | 1.313x |
| 40 MiB | 1.111x | 2,976.516 | 2.134x | 1,320.781 | 2.254x |
| 48 MiB | 1.333x | 5,230.516 | 3.751x | 1,314.406 | 3.979x |
| 64 MiB | 1.778x | 6,574.063 | 4.714x | 1,347.547 | 4.879x |
| 128 MiB | 3.556x | 8,777.938 | 6.295x | 1,349.828 | 6.503x |

Random-chain time is statistically flat from 4 through 36 MiB, rises at 38 MiB, and becomes sharply miss-dominated by 40 MiB. Sequential-chain time rises only 3.57% between 36 and 128 MiB because adjacent cache lines retain spatial locality. This locates the effective saturated random-working-set boundary much more tightly than the earlier 32/64 MiB throughput sweep and aligns with the independent 36 MiB device-property result.

The absolute unit remains deliberately unnamed: `VK_KHR_shader_clock` specifies an implementation-defined clock, and 65,536 in-flight chains expose warp scheduling as well as memory stalls. These are control-subtracted, scheduler-exposed ticks per dependent load, not raw single-load latency, GPU cycles, or nanoseconds. The retained invocation-count control shows that a single repeated warp rapidly makes its small traversed subset hot even when the allocation is larger than L2; it therefore cannot answer the capacity question by itself.

### CUDA `clock64` L2/global-path control

The independent CUDA kernel addresses the unit ambiguity without pretending to replace the capacity sweep. It compiles natively for `sm_120`, uses one warp, bypasses L1 with `ld.global.cg.u32`, and brackets 512 dependent steps with `clock64()`. A 256 MiB L2 eviction kernel precedes the cold chain; the hot chain immediately repeats the exact links and seed.

The timer and cache-path interpretation follows NVIDIA's [CUDA `clock64()` definition](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-support.html#clock-and-clock64) and [PTX cache-operator specification](https://docs.nvidia.com/cuda/parallel-thread-execution/#cache-operators).

| Table | Post-eviction cycles/step | Immediate-hot cycles/step | Post-eviction/hot |
|---:|---:|---:|---:|
| 4 MiB | 1,078.912 | 399.856 | 2.698x |
| 16 MiB | 1,087.917 | 399.741 | 2.721x |
| 32 MiB | 1,088.028 | 399.523 | 2.723x |
| 36 MiB | 1,086.832 | 399.575 | 2.721x |
| 38 MiB | 1,087.941 | 399.415 | 2.724x |
| 40 MiB | 1,087.654 | 399.560 | 2.722x |
| 64 MiB | 1,087.661 | 399.562 | 2.722x |
| 128 MiB | 1,089.004 | 399.577 | 2.725x |

The median of table-size medians is 1,087.789 post-eviction cycles and 399.569 hot cycles per dependent step, a 2.722x ratio and approximately 688 exposed cycles of additional cost. Cross-size hot medians span only 399.415-399.856 cycles; post-eviction medians span 1,078.912-1,089.004. The immediate repeated footprint is deliberately small enough to fit in L2 at every allocation size, explaining why these values do not show the 36-40 MiB capacity cliff.

CUDA-event timing for the complete one-warp kernels gives 153.414 ns per hot step and 401.820 ns per post-eviction step at the median of sizes. These human-time conversions include kernel prologue, result stores, and scheduling; the control-subtracted `clock64()` values are the in-loop cycle metric.

This is a stronger latency control than the Vulkan clock because NVIDIA defines `clock64()` in cycles, but its boundary remains explicit: a warp step may generate up to 32 random sector requests, and elapsed thread time includes scheduling. It is not one scalar cache transaction's latency. The `ld.global.cg` cache operator is also a performance hint, although native SASS confirms `LDG.E.STRONG.GPU` in both the chase and 256 MiB eviction loops.

The CUDA state-forced costs remain flat while the saturated Vulkan chain rises beyond 36 MiB. This is mutually consistent: table size changes the share and concurrency of lower-memory service, not the intrinsic hot/cold step costs. It also rules out a naive two-latency hit-rate inversion. The saturated Vulkan 128/36 MiB ratio is 6.295x, greater than the CUDA post-eviction/hot ratio of 2.722x, so memory queuing and warp scheduling must contribute materially to the saturated result.

### CUDA warp-concurrency and MLP sweep

The second CUDA probe keeps every lane's 512 loads strictly dependent but increases the number of independent one-warp blocks. It tests 1-736 total warps over 4, 36, 40, 64 and 128 MiB allocations. A CUDA occupancy query reports that this 16-register, zero-spill kernel can host at most 24 one-warp blocks per SM; the measurement reaches 16 per SM. Four isolated processes reverse both dimensions, and all 220 rows validate every returned endpoint through an independent CPU affine transform.

| Table | Hot Gload/s at 1 warp | Hot Gload/s at 46 warps | Hot Gload/s at 184 warps | Hot Gload/s at 736 warps | 736-warp exposed cycles/step | 736-warp hot slowdown vs 4 MiB |
|---:|---:|---:|---:|---:|---:|---:|
| 4 MiB | 0.208 | 9.582 | 36.437 | 42.861 | 1,474.8 | baseline |
| 36 MiB | 0.208 | 8.287 | 23.599 | 42.863 | 1,473.3 | 1.000x |
| 40 MiB | 0.208 | 3.943 | 13.839 | 23.429 | 2,703.4 | 1.829x |
| 64 MiB | 0.208 | 3.841 | 8.209 | 9.318 | 6,965.9 | 4.600x |
| 128 MiB | 0.208 | 3.503 | 6.963 | 7.506 | 8,674.1 | 5.710x |

At one warp every hot allocation reports about 400 cycles/step because the repeated path's logical footprint is only about 64 KiB. Increasing independent warps expands coverage and exposes the full allocation: 36 MiB still reaches the 4 MiB saturation rate, but 40 MiB loses 45.34%, 64 MiB loses 78.26%, and 128 MiB loses 82.49%. The result directly joins the two earlier controls: capacity changes service mix, while concurrency turns that mix into queueing and scheduler delay.

At 736 warps the 4 and 36 MiB requested-load rates are about 42.86 billion `u32` loads/s, or 159.7 logical GiB/s. The word "logical" is essential: a random warp instruction can generate many larger cache-sector transactions, so this is neither physical L2 bandwidth nor DRAM bandwidth. Exact sector/DRAM counters remain unavailable. Compute Sanitizer reports zero errors on the instrumented control, whose timings are excluded.

## Integrated direct-versus-LUT result

The following ratios are paired inside each process before taking the median. Positive delta means LUT faster; negative means LUT slower.

| Mode | State + event set | L2 fraction | Direct p50 | LUT p50 | LUT rate delta | Cross-run ratio range |
|---|---:|---:|---:|---:|---:|---:|
| evaluate | 12 MiB | 0.33x | 0.007936 ms | 0.009856 ms | -19.22% | 0.791-0.808x |
| evaluate | 36 MiB | 1.00x | 0.022000 ms | 0.021984 ms | -2.85% | 0.723-1.004x |
| evaluate | 96 MiB | 2.67x | 0.167728 ms | 0.167744 ms | -0.01% | 1.000-1.001x |
| evaluate | 192 MiB | 5.33x | 0.335008 ms | 0.334848 ms | +0.05% | 1.000-1.004x |
| evaluate + commit | 12 MiB | 0.33x | 0.022368 ms | 0.023776 ms | -5.92% | 0.935-0.941x |
| evaluate + commit | 36 MiB | 1.00x | 0.059648 ms | 0.061232 ms | -2.59% | 0.973-0.996x |
| evaluate + commit | 192 MiB | 5.33x | 0.410288 ms | 0.411408 ms | -0.28% | 0.995-0.998x |

The conclusion is critical rather than promotional: for the current confidence function, the table does not improve end-to-end throughput. Native `exp2` wins while the shader is compute-sensitive; once the dense state/output stream becomes the bottleneck, the LUT cost is hidden and both paths converge. The recommended implementation for this exact kernel on this GPU is therefore direct `exp2`.

The integrated table stores decoded binary16 confidence values, not log codes. A true log code would have to be decoded with another exponential before writing the existing E16 confidence field, eliminating the reason to replace `exp2`; alternatively, keeping the code in log form would change the output contract. The separate probe still establishes the cache behavior of the user's proposed two-per-texel log-code layout. A log-domain production design becomes attractive only if downstream stages also consume the log code or compare thresholds in log space without decoding.

### One-fetch interval-pair refinement

The interval-pair experiment tests whether the original LUT's second dynamic texture fetch was masking a useful cache-resident path. Each ratio below is paired within a process before taking the median across two forward-order and two reverse-order processes. Because clock states can differ between modes in the same process, a paired ratio need not equal the ratio of the two cross-process median p50 values.

| Mode | Candidates | Direct p50 | Two-fetch p50 | One-fetch p50 | One-fetch vs direct rate | One-fetch vs two-fetch rate |
|---|---:|---:|---:|---:|---:|---:|
| evaluate | 262,144 | 0.007920 ms | 0.009840 ms | 0.009768 ms | -18.85% | +0.82% |
| evaluate | 524,288 | 0.011944 ms | 0.013576 ms | 0.013056 ms | -8.27% | +4.52% |
| evaluate | 786,432 | 0.018520 ms | 0.022416 ms | 0.021072 ms | -7.10% | +11.40% |
| evaluate | 1,048,576 | 0.079328 ms | 0.072872 ms | 0.074816 ms | -1.63% | -1.34% |
| evaluate | 2,097,152 | 0.167944 ms | 0.167848 ms | 0.167704 ms | +0.13% | +0.09% |
| evaluate | 4,194,304 | 0.334520 ms | 0.334888 ms | 0.410248 ms | -18.20% | -9.25% |
| evaluate + commit | 262,144 | 0.022304 ms | 0.023712 ms | 0.022792 ms | -2.00% | +3.96% |
| evaluate + commit | 524,288 | 0.040680 ms | 0.041024 ms | 0.040928 ms | -0.61% | +0.23% |
| evaluate + commit | 786,432 | 0.060728 ms | 0.061024 ms | 0.060488 ms | +0.56% | +0.82% |
| evaluate + commit | 1,048,576 | 0.088848 ms | 0.092112 ms | 0.085296 ms | +3.07% | +0.94% |
| evaluate + commit | 2,097,152 | 0.205032 ms | 0.248920 ms | 0.226400 ms | -8.76% | -0.67% |
| evaluate + commit | 4,194,304 | 0.409824 ms | 0.409824 ms | 0.409944 ms | -0.03% | -0.07% |

One fetch recovers part of the two-fetch overhead in several small and mid-size cases, but it does not reverse the result against direct `exp2`: evaluate remains 7.10-18.85% slower than direct through 786,432 candidates. At 4,194,304, its evaluate/direct paired-rate range is 0.813-1.000x, exposing the same clock-state split seen elsewhere; evaluate+commit is effectively tied, with 1.000x median against direct and a 1.000-1.006x range. Removing a fetch is real, but the measured benefit is neither monotonic nor robust enough to justify doubling the table. Direct `exp2` remains the recommended path for this exact confidence function on this device.

## Native verified-event compaction

Two G32 compaction implementations were tested:

- Per-lane atomic append: every verified lane reserves one E16 slot with `atomicAdd`; its full-count variant retains per-lane candidate/support/compatibility atomics.
- Subgroup/workgroup append: subgroup ballots produce lane ranks, one invocation reserves a contiguous range for the whole 256-candidate workgroup, and the full-count variant reduces all four counts to at most four global atomics per workgroup.

SPIR-V disassembly confirms `GroupNonUniform` and `GroupNonUniformBallot` capabilities, four ballot/bit-count reductions, workgroup-shared count/offset arrays, and four `OpAtomicIAdd` sites in the full-count variant. It also contains a second `OpArrayLength` for event-buffer capacity and a conditional store, establishing that the append-demand counter advances even when a bounded output descriptor is full. Local `vulkaninfo` reports a fixed 32-lane NVIDIA subgroup with compute basic and ballot operations, so each 256-thread workgroup contains eight subgroups on this device.

Every compact record is read back, matched to a candidate using lineage plus scalar/topology payload, checked for duplicates and unexpected entries, and validated with the same boundary policy as dense output. The verifier also proves that every CPU-verified non-boundary candidate appears in the compact stream. Append counts and full reduced counters match exactly.

Six independent subgroup processes - three forward job order and three reverse - produced:

| Candidates | Dense eval p50 | Subgroup compact p50 | Paired speedup | Dense full-count p50 | Subgroup compact + counts p50 | Paired speedup |
|---:|---:|---:|---:|---:|---:|---:|
| 262,144 | 0.007856 ms | 0.009536 ms | 0.828x | 0.022352 ms | 0.009968 ms | 2.246x |
| 524,288 | 0.011976 ms | 0.012848 ms | 0.950x | 0.040752 ms | 0.013984 ms | 2.921x |
| 786,432 | 0.021768 ms | 0.016528 ms | 1.284x | 0.060304 ms | 0.018160 ms | 3.315x |
| 1,048,576 | 0.064728 ms | 0.020608 ms | 3.126x | 0.088064 ms | 0.022512 ms | 3.930x |
| 2,097,152 | 0.186616 ms | 0.112464 ms | 1.659x | 0.206056 ms | 0.114352 ms | 1.797x |
| 4,194,304 | 0.334464 ms | 0.218888 ms | 1.528x | 0.410344 ms | 0.219424 ms | 1.869x |

At the largest case, the paired subgroup/dense evaluate ratio is tightly grouped at 1.524-1.535x even after reversing job order. The full-count ratio is 1.517-2.753x because first-job clock ramp and one slow dense baseline widen the range; 1.869x is the process-paired median across the balanced order set. The subgroup barriers and scan lose to dense output at small evaluate-only sizes, with the crossover in this corpus between 524,288 and 786,432 candidates. Reducing counters per workgroup wins even at the smallest measured size.

At 4,194,304 candidates, event yield is 4.7488%. Dense E16 output is 64 MiB and the logical compact stream is 3,186,864 bytes (3.04 MiB), a 21.058x output-stream reduction. Including the 128 MiB G32 input state, state plus logical output falls from 192 MiB to 131.04 MiB, a 1.465x reduction.

The original six-process timing set used worst-case `N * 16` output capacity. A second implementation bounds the allocation to one E16 slot per 16 candidates (6.25% capacity) and guards every write against `events.length()`. The append counter remains the total demand, so `max(demand - capacity, 0)` is an exact GPU-visible overflow count. Two forward and two reverse processes produced:

| Candidates | Capacity | Verified | Overflow | Dense eval p50 | Bounded subgroup p50 | Paired speedup | Dense commit p50 | Bounded subgroup + counts p50 | Paired speedup |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 262,144 | 16,384 | 12,454 | 0 | 0.007904 ms | 0.009536 ms | 0.829x | 0.022288 ms | 0.010024 ms | 2.227x |
| 524,288 | 32,768 | 24,905 | 0 | 0.011920 ms | 0.013512 ms | 0.883x | 0.040680 ms | 0.014104 ms | 2.884x |
| 786,432 | 49,152 | 37,350 | 0 | 0.017984 ms | 0.016512 ms | 1.066x | 0.061216 ms | 0.018192 ms | 3.355x |
| 1,048,576 | 65,536 | 49,798 | 0 | 0.071400 ms | 0.020568 ms | 3.477x | 0.092208 ms | 0.022544 ms | 3.891x |
| 2,097,152 | 131,072 | 99,597 | 0 | 0.167744 ms | 0.112432 ms | 1.491x | 0.227352 ms | 0.114136 ms | 2.003x |
| 4,194,304 | 262,144 | 199,179 | 0 | 0.333872 ms | 0.218952 ms | 1.525x | 0.410992 ms | 0.219824 ms | 1.876x |

At the largest case the bounded output allocation is 4 MiB, a real 16x allocation reduction; state plus allocated output is 132 MiB, 1.455x below the 192 MiB dense layout. The 4 MiB allocation leaves 62,965 unused slots (0.96 MiB) above the observed stream. Relative to the earlier worst-case-capacity medians, large append changes from 0.218888 to 0.218952 ms (+0.03%) and append+counts from 0.219424 to 0.219824 ms (+0.18%); these are separate run sets, so they establish practical parity rather than a causal cost estimate.

A capacity sweep at 4,194,304 candidates isolates the memory/risk trade. Signed headroom is capacity minus the exact 199,179-event GPU demand:

| Capacity ratio | Slots | Allocation | Allocation reduction | Headroom | Overflow | Subgroup append p50 |
|---:|---:|---:|---:|---:|---:|---:|
| 4.00% | 167,773 | 2,684,368 B | 25.000x | -31,406 | 31,406 | 0.218896 ms |
| 4.75% | 199,230 | 3,187,680 B | 21.053x | 51 | 0 | 0.219072 ms |
| 5.00% | 209,716 | 3,355,456 B | 20.000x | 10,537 | 0 | 0.219040 ms |
| 6.25% | 262,144 | 4,194,304 B | 16.000x | 62,965 | 0 | 0.218952 ms (four-run median) |

The 4.75% setting is lossless only by 51 records in this deterministic corpus and is too brittle as a production default. The 5% setting gives 5.29% headroom relative to observed events; 6.25% gives 31.61% event headroom and a power-of-two capacity rule with no measurable large-case throughput cost. The report therefore uses 6.25% as the conservative measured setting, while still requiring callers to size from their own worst-case event distribution.

A deliberate 1% capacity run independently exercised the failure path. At 262,144 candidates all four compact variants reported 12,454 demanded, 2,622 retained and 9,832 overflow events. Every retained payload validated, each demand counter exactly matched the dense GPU result, no out-of-range write occurred, and the harness rejected the run unless `--allow-compact-overflow` was supplied. This validates both safe truncation and fail-closed default behavior. A two-pass count/allocate/write pipeline remains preferable when lossless operation is required but no conservative capacity contract is available.

### Pre-threshold confidence predicate

The benchmark state stores binary16 guard epsilon `0.0100021362` and confidence floor `0.7001953125`. For `confidence = exp2(-32 * distance)`, that floor permits distance through `0.0160678341`; the guard is therefore strictly tighter, and every guard-crossing lane already has confidence at least `0.8010319`. Computing `exp2` before verification is redundant for this corpus.

The optional pre-threshold profile stores `min(guard_epsilon, -log2(confidence_floor)/32)` in the high half of the guard word. The GPU uses that effective distance for verification and materializes confidence only after the non-verified lanes return. SPIR-V disassembly places `Exp2` before the verification branch in the original subgroup module and after the early-return region in the pre-threshold module. Four processes, two in each job order, produced:

| Candidates | Original append p50 | Pre-threshold p50 | Paired rate change | Original + counts p50 | Pre-threshold + counts p50 | Paired rate change |
|---:|---:|---:|---:|---:|---:|---:|
| 262,144 | 0.009624 ms | 0.009488 ms | +1.01% | 0.009920 ms | 0.009944 ms | -0.32% |
| 524,288 | 0.013600 ms | 0.013032 ms | +4.47% | 0.014064 ms | 0.014032 ms | +0.11% |
| 786,432 | 0.017096 ms | 0.016440 ms | +4.14% | 0.018160 ms | 0.018256 ms | -0.57% |
| 1,048,576 | 0.020648 ms | 0.020552 ms | +0.98% | 0.022528 ms | 0.022624 ms | -0.32% |
| 2,097,152 | 0.112464 ms | 0.112480 ms | +0.01% | 0.114224 ms | 0.113464 ms | +0.67% |
| 4,194,304 | 0.219000 ms | 0.218928 ms | +0.03% | 0.220032 ms | 0.219936 ms | +0.04% |

All original/pre-threshold GPU counts match, every retained payload validates, and all runs are complete with zero overflow at 6.25% capacity. The large append ratio range is 1.000-1.234x because one original-path job entered a slow clock state; the balanced median is 1.0003x. The conclusion is narrow: pre-thresholding helps append-only work by roughly 1-4.5% before the stream becomes state-bandwidth dominated, but it does not materially improve the large case or the workgroup-counted path. Unlike a texture LUT it adds no cache footprint, but it changes the G32 field contract and is justified only when the producer can declare and precompute the monotonic threshold.

### G24 fixed-query hot state and 128-byte log-threshold LUT

The G24 profile specializes the declared fixed benchmark query rather than pretending to be a general replacement for G32. Its six 32-bit words retain position, cone threshold, axis, radius, guard epsilon and lineage. Time and phase are dropped, the full compatibility mask is reduced to a producer-computed compatible bit, and sheet/orientation plus a 6-bit confidence-distance code occupy the high 16 bits of the guard word. SPIR-V declares `ArrayStride 24`, so this is a real 24-byte storage-buffer record rather than a host-only packing claim.

The code represents the log-domain threshold `-log2(confidence_floor)/32` over `[0, 0.125]`. The LUT version expands its 64 codes to binary16 distances with one `OpImageFetch` from 32 `R32_UINT` texels: 128 bytes total, or 0.00034% of local L2. The direct control uses the identical G24 layout and subgroup algorithm but decodes `code * (0.125/63)` arithmetically; disassembly contains no image fetch. Both compute confidence with `exp2` only for retained E16 events. Six processes, three in each job order, produced:

| Candidates | G32 append p50 | G24 direct p50 | G24 LUT p50 | Direct/G32 paired rate | LUT/direct paired rate | Direct/G32 + counts | LUT/direct + counts |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 262,144 | 0.009528 ms | 0.008208 ms | 0.009744 ms | 1.163x | 0.841x | 1.003x | 0.991x |
| 524,288 | 0.013536 ms | 0.012064 ms | 0.013808 ms | 1.122x | 0.873x | 1.001x | 0.997x |
| 786,432 | 0.016568 ms | 0.016096 ms | 0.017872 ms | 1.027x | 0.903x | 1.005x | 0.987x |
| 1,048,576 | 0.020592 ms | 0.020112 ms | 0.021856 ms | 1.023x | 0.923x | 1.014x | 0.932x |
| 1,310,720 | 0.071536 ms | 0.024288 ms | 0.025904 ms | 2.947x | 0.937x | 2.792x | 0.929x |
| 1,572,864 | 0.085840 ms | 0.037040 ms | 0.038536 ms | 2.318x | 0.981x | 2.196x | 0.951x |
| 2,097,152 | 0.112464 ms | 0.086792 ms | 0.087808 ms | 1.296x | 0.982x | 1.303x | 0.997x |
| 4,194,304 | 0.218976 ms | 0.167664 ms | 0.187216 ms | 1.306x | 0.995x | 1.312x | 0.999x |

At 1,310,720 candidates, G32 state plus its bounded output allocation is 41.25 MiB (1.146x L2), while G24 is 31.25 MiB (0.868x L2); the sharp 2.947x append gain is therefore aligned with shifting the hot allocation back below the measured 36 MiB cache boundary. At 4,194,304, the corresponding allocations are 132 MiB and 100 MiB, exactly a 1.32x reduction, close to the stable full-counter speedup of 1.312x. This is strong cache-capacity/traffic evidence, but it is not a direct L2-hit or DRAM-transaction measurement because NVIDIA counters remain permission-blocked.

The append-only LUT rows were bimodal at the largest size: job order alternated approximately 0.168 and 0.207 ms states, so the cross-process LUT p50 above is 0.187 ms even though the within-process paired LUT/direct rate median is 0.995x. The counted kernels were stable: direct was 0.168 ms, LUT was 0.168 ms, and LUT/direct was 0.999x. Below L2, the LUT costs 6-16% against the direct decoder in append-only mode. The critical conclusion is therefore unambiguous: use the 24-byte fixed-query layout where its reduced semantics are acceptable, but keep direct threshold decoding for this 64-entry mapping. The texture-cache LUT is validated and essentially free only after state traffic dominates; it is not the source of the speedup.

#### Narrow L2-boundary sweep

Four additional processes, two in each job order, densely sampled the calculated residency crossings using the more stable full-counter subgroup kernels. All output payloads, dense-GPU demand cross-checks, reduced counters, completeness checks and overflow checks passed.

| Candidates | G32 allocation / L2 | G32 + counts p50 | G24 direct allocation / L2 | G24 direct + counts p50 | G24 LUT + counts p50 |
|---:|---:|---:|---:|---:|---:|
| 1,081,344 | 0.9453x | 0.024288 ms | 0.7161x | 0.022288 ms | 0.024304 ms |
| 1,114,112 | 0.9740x | 0.024400 ms | 0.7378x | 0.023760 ms | 0.024264 ms |
| 1,146,880 | 1.0026x | 0.032792 ms | 0.7595x | 0.024296 ms | 0.025312 ms |
| 1,179,648 | 1.0313x | 0.042144 ms | 0.7813x | 0.024256 ms | 0.027488 ms |
| 1,310,720 | 1.1458x | 0.073568 ms | 0.8681x | 0.026352 ms | 0.028256 ms |
| 1,441,792 | 1.2604x | 0.081344 ms | 0.9549x | 0.028448 ms | 0.030552 ms |
| 1,474,560 | 1.2891x | 0.082016 ms | 0.9766x | 0.029504 ms | 0.030624 ms |
| 1,507,328 | 1.3177x | 0.083952 ms | 0.9983x | 0.033928 ms | 0.035792 ms |
| 1,540,096 | 1.3464x | 0.085936 ms | 1.0200x | 0.038736 ms | 0.039152 ms |
| 1,572,864 | 1.3750x | 0.086968 ms | 1.0417x | 0.041216 ms | 0.042600 ms |

G32 candidate rate falls 23.4% on the step from 0.9740x to 1.0026x L2 and another 19.6% at 1.0313x, a cumulative 38.4% across those two steps. G24 remains flat across the same candidate counts because its allocation is only 0.738-0.781x L2. Its own rate falls 11.1% on the step from 0.9766x to 0.9983x and another 10.4% at 1.0200x, a cumulative 20.3%. The first G24 degradation begins with only 64 KiB of nominal L2 headroom, which is consistent with code, descriptors, counters, cache-line granularity and other GPU activity also competing for cache. The two cliffs move by almost exactly the 32/24-byte state-footprint ratio, materially strengthening the L2-capacity attribution while still not constituting a direct hit-rate measurement.

### G20 hot geometry with cold lineage

The next profile splits G24 into a 20-byte geometry/meta storage-buffer record and a separate 4-byte lineage storage buffer. The shader checks support, compatibility and verification from the hot record; non-verified lanes return before the lineage load. The 4.7488% retained lanes fetch lineage, compute the same hash and emit the same E16 contract. This preserves the complete 24-byte state allocation, so the experiment tests locality rather than claiming extra compression.

Six sequentially isolated processes, three in each job order, cover twelve sizes with 750 ms minimum warmup and 200 measured dispatches. All 432 rows have zero overflow and pass payload, count, completeness and pipeline-cache reload checks. Representative paired results are:

| Candidates | G24 append p50 | G20 append p50 | G20/G24 paired append rate | G24 + counts p50 | G20 + counts p50 | G20/G24 paired counted rate |
|---:|---:|---:|---:|---:|---:|---:|
| 1,310,720 | 0.035400 ms | 0.024680 ms | 1.437x | 0.026328 ms | 0.028432 ms | 0.926x |
| 1,507,328 | 0.030440 ms | 0.030720 ms | 0.996x | 0.032024 ms | 0.033720 ms | 0.948x |
| 1,769,472 | 0.073600 ms | 0.067416 ms | 1.092x | 0.075248 ms | 0.067680 ms | 1.112x |
| 2,097,152 | 0.087568 ms | 0.078784 ms | 1.111x | 0.087920 ms | 0.079712 ms | 1.103x |
| 4,194,304 | 0.167560 ms | 0.151256 ms | 1.108x | 0.168016 ms | 0.151392 ms | 1.110x |

The median per-size paired gain across all twelve sizes is 1.118x append and 1.025x append + counts. Small counted cases can regress, so the split is not an unconditional latency win. At 4,194,304 candidates, the declared always-hot state plus bounded output is 84 MiB rather than G24's 100 MiB, but the separately allocated 16 MiB lineage buffer keeps total allocation at 100 MiB. A pure 25/21 byte traffic model would permit at most 1.190x; retained-lane reads and cache-sector amplification narrow the observed gain. Exact sector traffic remains unmeasured because counters are permission-blocked. The full isolation protocol records the retained clock-state outlier and the common executable SHA-256.

The compaction audit exposed a separate identity problem. For the structured benchmark seed `lineage_seed = i * 2654435761`, the pre-mix expression `lineage_seed ^ i` has only 4,146,164 unique values over 4,194,304 candidates: 47,898 collision keys and 48,140 extra candidates. `mix32` is bijective over 32-bit words, so it cannot remove those collisions. The verifier therefore buckets equal lineage values and disambiguates with the rest of the event payload. Production logs that need unique source identity should carry a source index or a wider lineage identifier; the current 32-bit lineage is not a unique key.

## Important implementation boundaries

- G64 remains dense. G32 now has dense, per-lane atomic compact, and subgroup/workgroup compact paths. Compact buffers support either worst-case capacity or an explicit fractional bound with GPU-visible overflow demand; overflow fails validation unless deliberately allowed.
- G24 is a fixed-query compact ABI, not a lossless G32 encoding. It omits time and phase and replaces the compatibility mask with a precomputed bit; callers needing dynamic queries must retain G32 or define another versioned layout.
- G20 is the same fixed-query semantics with lineage split into a separate cold buffer. It is not a 20-byte total state format: total state allocation remains 24 bytes per candidate.
- Query compatibility remains fixed to sheet 1, orientation 0, and mask bit 2 in the benchmark shaders.
- G32 half packing changes numerical predicates and therefore event counts; it is a lossy performance profile, not a bit-identical substitute for G64.
- Subgroup compaction requires Vulkan subgroup basic/ballot support. It is verified on this NVIDIA Vulkan 1.4 device but must be capability-checked before use on another target.

## Profiling boundary

Nsight Systems reported `ERR_NVGPUCTRPERM`: GPU performance-counter sampling requires a privilege not enabled on this machine. An attempted Vulkan trace produced a report file but no Vulkan API rows, so it is not used as evidence. A validated native Vulkan capability probe against the selected NVIDIA device reports `pipeline_executable_capture = true` and `performance_query_extension_present = false`. No L2 hit-rate, sector count, or raw DRAM-byte claim is made. The cache conclusion is an inference from a controlled working-set sweep, the independently queried 36 MiB L2 size, and repeatable throughput behavior. Native driver compiler statistics are available through `VK_KHR_pipeline_executable_properties`; they do not substitute for L2/DRAM counters.

The same selected device reports `shaderDeviceClock = true` through `VK_KHR_shader_clock`, allowing the dependent-chain intervals above to be measured inside native GPU execution. This closes the host-timestamp-only observability gap but still does not expose cache hit classifications or define the clock unit.

CUDA `clock64()` provides a per-SM cycle counter and the `ld.global.cg` controls bypass L1, but neither substitutes for privileged cache-sector and DRAM-transaction counters. The hot/post-eviction labels are controlled cache-state interpretations, not direct hardware hit/miss classifications. The concurrency sweep adds a measured queue/scheduler response and logical requested-load throughput; it still cannot label physical transactions or exact hits.

Device timestamps remove host submission latency from the metric but cannot remove dynamic-clock, power-state, or WDDM scheduling variation.

A separate 100 ms `nvidia-smi` telemetry run sampled 212 complete rows while the six large G32 modes ran with 2,000 ms warmup and 400 dispatches each. P-state occupancy was P0/P2/P4/P5/P8 = 80/4/107/9/12 samples. Across 109 samples with nonzero GPU utilization, graphics clock ranged from 630 to 2,782 MHz (2,060 MHz mean), memory clock from 9,001 to 14,001 MHz, power from 12.99 to 118.32 W, and temperature from 54 to 65 C. Dense evaluation landed in its slower 0.532 ms state while subgroup append remained 0.219 ms. Because sampling is asynchronous and not phase-labelled, this run is causal context for the observed clock hysteresis, not part of the performance aggregate.

## Reproduction

```powershell
# Build the direct Vulkan executables with Visual Studio Build Tools.
& .\gpu\scripts\build_windows_vulkan.ps1

# Semantic core plus integrated G32 texture-LUT sweep.
& .\gpu\scripts\run_windows_vulkan_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\windows_integrated_lut_run\new_run `
  -Sizes '262144,393216,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200

# Packed log-code texture-cache sweep.
# The current harness also runs a byte-identical SSBO control; repeat with
# -ReverseOrder for a counterbalanced process.
& .\gpu\scripts\run_windows_lut_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\windows_lut_cache_run\new_run `
  -Warmup 10 -WarmupMilliseconds 500 -Iterations 100

# Direct versus two-fetch and one-fetch confidence-LUT sweep.
# Repeat with -ReverseOrder for a counterbalanced process.
& .\gpu\scripts\run_windows_lut_pair_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\lut_pair\new_run `
  -Sizes '262144,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200

# Dense, per-lane atomic, and subgroup/workgroup compact G32 sweep.
& .\gpu\scripts\run_windows_compact_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\sg_compact\new_run `
  -Sizes '262144,393216,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200

# Same kernel with a real 6.25%-capacity output allocation.
& .\gpu\scripts\run_windows_compact_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\bounded_compact\new_run `
  -Sizes '262144,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200 `
  -CapacityRatio 0.0625

# Original versus pre-threshold subgroup predicate, same bounded allocation.
& .\gpu\scripts\run_windows_prethreshold_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\prethreshold\new_run `
  -Sizes '262144,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200 `
  -CapacityRatio 0.0625

# G32 versus G24 direct and one-fetch log-threshold LUT controls.
# Repeat with -ReverseOrder for a counterbalanced process.
& .\gpu\scripts\run_windows_hot_log_lut_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\hot_log_control\new_run `
  -Sizes '262144,524288,786432,1048576,1310720,1572864,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200 `
  -CapacityRatio 0.0625

# Narrow G32/G24 state-plus-output residency crossings.
& .\gpu\scripts\run_windows_hot_log_lut_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\l2_boundary_hot\new_run `
  -Sizes '1081344,1114112,1146880,1179648,1310720,1441792,1474560,1507328,1540096,1572864' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200 `
  -CapacityRatio 0.0625

# G24 versus 20-byte hot geometry plus a separate cold-lineage stream.
# Repeat with -ReverseOrder for a counterbalanced process.
& .\gpu\scripts\run_windows_cold_lineage_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\cold_lineage_isolated\new_run `
  -Sizes '1310720,1441792,1474560,1507328,1540096,1572864,1638400,1703936,1769472,1835008,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200 `
  -CapacityRatio 0.0625

# Device-clock control plus saturated 512-step dependent SSBO chase.
# Repeat twice normally and twice with -ReverseOrder.
& .\gpu\scripts\run_windows_l2_latency.ps1 `
  -OutputDirectory .\benchmarks\l2_latency_isolated\new_run `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 100

# Native sm_120 one-warp cold/hot cycle control. Repeat in ascending and
# descending table orders in separate processes.
& .\gpu\scripts\run_windows_cuda_l2_clock.ps1 `
  -OutputDirectory .\benchmarks\cuda_l2_clock_isolated\new_run `
  -TableMiB '4,16,32,36,38,40,64,128' `
  -EvictionMiB 256 -Warmup 5 -Samples 50

# Native sm_120 concurrency/MLP sweep. Repeat twice in this order and twice
# with both -TableMiB and -Warps lists reversed in separate processes.
& .\gpu\scripts\run_windows_cuda_l2_mlp.ps1 `
  -OutputDirectory .\benchmarks\cuda_l2_mlp_isolated\new_run `
  -TableMiB '4,36,40,64,128' `
  -Warps '1,2,4,8,16,32,46,92,184,368,736' `
  -EvictionMiB 256 -Warmup 3 -Samples 15
```

Primary machine-readable results are in `benchmarks/windows_physical_gpu_aggregate/aggregate_metrics.json`, with paired values in `integrated_lut_comparison.csv`, `paired_lut_comparison.csv`, `lut_path_comparison.csv`, `l2_latency_comparison.csv`, `cuda_l2_clock_comparison.csv`, `cuda_l2_mlp_comparison.csv`, `prethreshold_comparison.csv`, `hot_log_lut_comparison.csv`, `hot_log_control_comparison.csv`, `l2_boundary_comparison.csv`, and `cold_lineage_comparison.csv`; native compiler metadata in `pipeline_executable_statistics.csv`; compaction values in `compaction_metrics.csv`, `bounded_compaction_metrics.csv`, and `capacity_sweep_metrics.csv`; and environment metadata in `environment.json`. Vulkan shader-clock raw data is in `benchmarks/l2_latency_isolated/`; CUDA cycle/concurrency data and SASS protocols are in `benchmarks/cuda_l2_clock_isolated/` and `benchmarks/cuda_l2_mlp_isolated/`. Raw JSON/CSV remains in `benchmarks/windows_native_run/`, `benchmarks/windows_integrated_lut_run/`, `benchmarks/windows_lut_cache_run/`, `benchmarks/lut_path_control/`, `benchmarks/hashcheck/`, `benchmarks/lut_pair/`, `benchmarks/sg_compact/`, `benchmarks/bounded_compact/`, `benchmarks/capacity_sweep/`, `benchmarks/prethreshold/`, `benchmarks/hot_log_lut/`, `benchmarks/hot_log_control/`, `benchmarks/l2_boundary_hot/`, the primary `benchmarks/cold_lineage_isolated/`, `benchmarks/l2_latency_isolated/`, `benchmarks/cuda_l2_clock_isolated/`, and `benchmarks/cuda_l2_mlp_isolated/` corpora, and `benchmarks/native_capability_probe/`. The older `benchmarks/cold_lineage_hot/` corpus is retained but excluded because four processes overlapped.
