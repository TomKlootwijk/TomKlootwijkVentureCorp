# UGTS yield, compression, and practical limits

Date: 2026-08-15  
Device: NVIDIA GeForce RTX 5070 Ti Laptop GPU  
Execution path: direct Vulkan compute on the physical GPU, using device-local storage buffers and native SPIR-V  
Reported L2 capacity: 36 MiB (37,748,736 bytes), returned by the local CUDA device-properties query

## Plain-language result

For the fixed benchmark corpus, roughly **1 candidate in 21 becomes an event**. The measured G32/G24/G20 path retained 199,179 of 4,194,304 candidates, a **4.7488% event yield**. Compacting to only those events makes the logical event stream **21.058x smaller** than a dense E16 stream.

The practical single-pass implementation reserves room for 1 event per 16 candidates (6.25%). At the largest measured case this is a 4 MiB buffer instead of 64 MiB, a **16x allocation reduction**, with zero overflow and 0.961 MiB left unused.

The best measured total layout is the fixed-query G24 state with E16 bounded output: **100 MiB total allocation** for 4,194,304 candidates, versus 192 MiB for packed G32 plus dense E16 and 384 MiB for authoritative G64 plus dense E32. That is respectively **1.92x** and **3.84x** less memory.

Separating lineage into a cold stream does not reduce total storage: G20 hot state + 4-byte cold lineage is still 24 bytes per candidate. It does reduce the allocation touched by every lane from 100 MiB to 84 MiB at the largest case. Six balanced, sequentially isolated process runs measured a **1.108x append speedup** and **1.110x counted-path speedup** over G24 at 4,194,304 candidates. This is useful, but it is not the theoretical 1.190x maximum because retained lanes still fetch lineage and cache-line amplification is real.

A native `VK_KHR_shader_clock` pointer chase now sharpens the cache boundary. Random dependent-load time is flat through the exact reported 36 MiB L2 size, rises **1.242x at 38 MiB**, and reaches **2.134x at 40 MiB**, **4.714x at 64 MiB**, and **6.295x at 128 MiB**, all relative to 36 MiB. Sequential dependent loads rise only 3.57% from 36 to 128 MiB because adjacent accesses retain spatial locality.

An independent native CUDA `sm_120` control supplies a real cycle-domain comparison. One warp using L1-bypassing `ld.global.cg` measures a cross-size median of **399.57 cycles per hot dependent step** and **1,087.79 cycles after a 256 MiB L2-eviction pass**: the post-eviction path is **2.722x** slower, or about 688 additional exposed cycles per step. CUDA event timing corresponds to approximately **153.4 ns per hot step** and **401.8 ns per post-eviction step** for the complete one-warp kernel. These are warp-exposed values, not the latency of one scalar memory transaction.

A new native CUDA concurrency sweep closes the gap between that one-warp control and the saturated Vulkan result. At 736 independent warps (16 warps per SM), a hot 36 MiB random table sustains **42.863 billion requested `u32` loads/s**, indistinguishable from the 4 MiB control. Expanding the table by only 4 MiB to 40 MiB drops throughput **45.34% to 23.429 Gload/s**. The 64 and 128 MiB cases deliver only 9.318 and 7.506 Gload/s. This directly confirms that packing the hot random-access footprint at or below L2 matters under production-like concurrency; it also shows that scheduler and memory-queue pressure, not just a fixed hit/miss latency, creates the large above-L2 slowdown.

## Yield

The largest deterministic G32-family dispatch produced this funnel:

| Stage | Records | Share of all candidates | Human interpretation |
|---|---:|---:|---|
| Candidates | 4,194,304 | 100.0000% | All inputs examined |
| Supported | 2,085,336 | 49.7183% | About 1 in 2 passes geometric support |
| Supported + compatible | 346,957 | 8.2721% | About 1 in 12 reaches the compatible set |
| Verified events | 199,179 | 4.7488% | About 1 in 21.058 is emitted |
| Rejected/non-event | 3,995,125 | 95.2512% | This is the work removed from the output stream by compaction |

Of the supported records, 16.6379% are compatible. Of compatible records, 57.4074% verify. G24 and G20 reproduce the G32 compact counts and retained payload semantics exactly under the declared tolerance policy.

G64 has a slightly different 4.8943% yield because G32 is a lossy binary16 performance profile; G32 is not claimed to be bit-identical to G64.

## Compression by representation

| Change | Bytes per record | Reduction | Compression ratio | Scope |
|---|---:|---:|---:|---|
| G64 state -> G32 state | 64 -> 32 | 50.0% | 2.000x | General packed performance profile; lossy binary16 fields |
| G32 state -> G24 state | 32 -> 24 | 25.0% | 1.333x | Fixed-query specialization; omits time/phase and precomputes compatibility |
| G64 state -> G24 state | 64 -> 24 | 62.5% | 2.667x | Fixed-query comparison, not a lossless encoding |
| E32 event -> E16 event | 32 -> 16 | 50.0% | 2.000x | Packed event ABI |
| Dense E16 -> exact compact E16 | 64 MiB -> 3.039 MiB | 95.2512% | 21.058x | Logical output at the observed 4.7488% yield |
| Dense E16 -> bounded E16 allocation | 64 MiB -> 4 MiB | 93.75% | 16.000x | Real single-pass allocation at 6.25% capacity |
| G24 hot -> G20 hot | 24 -> 20 | 16.667% | 1.200x | Hot stream only; a separate 4-byte lineage stream remains allocated |

At 4,194,304 candidates, the complete allocated-memory comparison is:

| Layout | State | Allocated output | Total | Reduction versus G64/E32 dense |
|---|---:|---:|---:|---:|
| G64 state + dense E32 | 256 MiB | 128 MiB | 384 MiB | baseline |
| G32 state + dense E16 | 128 MiB | 64 MiB | 192 MiB | 2.000x smaller |
| G32 state + bounded E16 | 128 MiB | 4 MiB | 132 MiB | 2.909x smaller |
| G24 state + bounded E16 | 96 MiB | 4 MiB | 100 MiB | 3.840x smaller |
| G20 hot + cold lineage + bounded E16 | 80 MiB hot + 16 MiB cold | 4 MiB | 100 MiB | 3.840x smaller total; 84 MiB in the declared always-hot state/output set |

The G20 split is therefore a **locality optimization, not additional storage compression**. Calling it 20-byte total compression would be incorrect.

## Measured processing yield

The six-process cold-lineage comparison used three forward and three reverse job orders, 750 ms minimum warmup, 200 timed dispatches per case, bounded 6.25% output, and twelve sizes from 1,310,720 through 4,194,304 candidates. Processes ran sequentially rather than competing with one another. All 432 benchmark rows passed payload, counter, completeness, overflow, and pipeline-cache reload validation.

At 4,194,304 candidates:

| Path | Append p50 | Candidate throughput | Emitted-event throughput | Paired speedup over G24 |
|---|---:|---:|---:|---:|
| G24 direct append | 0.167560 ms | 25.032 billion candidates/s | 1.189 billion events/s | baseline |
| G20 + cold lineage append | 0.151256 ms | 27.730 billion candidates/s | 1.317 billion events/s | 1.108x |
| G24 direct append + counts | 0.168016 ms | 24.964 billion candidates/s | 1.185 billion events/s | baseline |
| G20 + cold lineage append + counts | 0.151392 ms | 27.705 billion candidates/s | 1.316 billion events/s | 1.110x |

Across all twelve sizes, the median of the per-size paired speedups is 1.118x for append and 1.025x for append + counts. The first five counted sizes range from 0.926x to 0.948x and the 1,507,328-candidate append case is 0.996x, so the split should not be represented as an unconditional win for every dispatch size. One retained process-level G24 counted timing at the largest size is a visible clock-state outlier; the six-process median is reported without deleting it.

These rates are cache-hot steady-state rates from repeated dispatches against resident buffers. They are not cold one-pass DRAM streaming rates.

## Theoretical and practical limits

### Output capacity

- **Corpus-specific exact lower bound:** 199,179 E16 records, or 3,186,864 bytes (3.039 MiB). Achieving exactly this allocation without prior knowledge requires a count/scan followed by allocation and write, or an equivalent two-pass scheme.
- **Smallest measured lossless fraction:** 4.7488%. A rounded 4.75% allocation has only 51 event slots of slack in this corpus and is too fragile for production.
- **Current practical bound:** 6.25%, or 262,144 records/4 MiB. It is 75.98% utilized and has 62,965 spare records, equal to 31.61% headroom relative to observed demand.
- **Universal one-pass bound without a distribution contract:** 100% yield. Any candidate can theoretically verify, so a lossless single-pass caller must either reserve dense capacity, accept overflow, or use two passes. The observed 4.7488% is a workload property, not a universal theorem.

### L2-resident candidate limits

With a 6.25%-capacity E16 output, the output allocation costs exactly 1 byte per candidate. Ignoring small counters, code, descriptors, alignment, other GPU users, and cold-stream cache sectors, the nominal 36 MiB limits are:

| Always-hot layout | Nominal bytes/candidate | Absolute 36 MiB ceiling | Conservative 28 MiB target |
|---|---:|---:|---:|
| G32 + bounded output | 33 | 1,143,901 | 889,700 |
| G24 + bounded output | 25 | 1,509,949 | 1,174,405 |
| G20 hot + bounded output | 21 | 1,797,558 | 1,398,101 |

The 36 MiB values are arithmetic maxima, not safe production allocations. The 28 MiB column reserves 8 MiB (22.2% of L2) for cache-line amplification, other state, outputs, code and system activity. The measured G32/G24 cliffs occur near the absolute crossings, and the new concurrency probe sustains full hot throughput at 36 MiB but loses 45.34% at 40 MiB. Exact NVIDIA cache-hit/DRAM counters remain permission-blocked (`ERR_NVGPUCTRPERM`), so these are engineering limits supported by timing and throughput cliffs rather than counter-derived hit thresholds.

For G20, the ideal traffic model adds only 4 bytes times the 4.7488% event yield, or **0.190 logical cold-lineage bytes per candidate**. The other bound is that sparse accesses pull enough cache sectors to approach the original 4 bytes per candidate. Thus the useful state/output traffic lies between approximately 21.19 and 25 bytes per candidate. The observed 1.108x large-case gain realizes about 57% of the ideal 19.05% bandwidth-ratio headroom.

### Native dependent-load boundary

Four sequentially isolated, order-balanced processes used the device-scope realtime clock around 512 strictly dependent SSBO loads per invocation. Each chase row ran 65,536 invocations, or 33,554,432 dependent loads. A separately compiled zero-step shader supplies the clock/instruction control. All 192 rows and 12,582,912 invocation payloads validate; their validated chain endpoints represent **3,221,225,472 executed dependent loads**.

| Random table | L2 fraction | Median net ticks/load | Relative to 36 MiB | Random/sequential ratio |
|---:|---:|---:|---:|---:|
| 4 MiB | 0.111x | 1,383.469 | 0.992x | 1.101x |
| 32 MiB | 0.889x | 1,393.234 | 0.999x | 1.062x |
| 34 MiB | 0.944x | 1,393.656 | 0.999x | 1.068x |
| 36 MiB | 1.000x | 1,394.531 | baseline | 1.070x |
| 38 MiB | 1.056x | 1,732.516 | 1.242x | 1.313x |
| 40 MiB | 1.111x | 2,976.516 | 2.134x | 2.254x |
| 48 MiB | 1.333x | 5,230.516 | 3.751x | 3.979x |
| 64 MiB | 1.778x | 6,574.063 | 4.714x | 4.879x |
| 128 MiB | 3.556x | 8,777.938 | 6.295x | 6.503x |

This is strong native evidence that the effective random-access transition is immediately above the reported 36 MiB capacity for this saturated workload. It is not a direct hit-rate measurement. Vulkan deliberately leaves shader-clock units implementation-defined, and 65,536 in-flight chains expose warp scheduling as well as memory stalls; consequently the table reports ticks and relative ratios, not invented cycles or nanoseconds. An invocation-count control demonstrates that a repeated single-warp path rapidly becomes hot regardless of total allocation and therefore cannot establish table-capacity behavior.

### Native CUDA cycle-domain L2 control

The CUDA control compiles specifically for this GPU's `sm_120` target. One warp performs 512 dependent random loads using `ld.global.cg.u32`, which bypasses L1 and uses the global/L2 cache path. A 256 MiB eviction kernel runs before the cold measurement; the hot measurement immediately repeats the identical path. Four sequentially isolated processes use two ascending and two descending table orders, five discarded warmup pairs, and 50 measured pairs per table.

The semantics follow NVIDIA's [CUDA `clock64()` definition](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cpp-language-support.html#clock-and-clock64) and [PTX cache-operator specification](https://docs.nvidia.com/cuda/parallel-thread-execution/#cache-operators).

| Table | Post-eviction cycles/step | Immediate hot cycles/step | Cold/hot ratio |
|---:|---:|---:|---:|
| 4 MiB | 1,078.912 | 399.856 | 2.698x |
| 16 MiB | 1,087.917 | 399.741 | 2.721x |
| 32 MiB | 1,088.028 | 399.523 | 2.723x |
| 36 MiB | 1,086.832 | 399.575 | 2.721x |
| 38 MiB | 1,087.941 | 399.415 | 2.724x |
| 40 MiB | 1,087.654 | 399.560 | 2.722x |
| 64 MiB | 1,087.661 | 399.562 | 2.722x |
| 128 MiB | 1,089.004 | 399.577 | 2.725x |

Across table sizes, the median post-eviction result ranges only from 1,078.912 to 1,089.004 cycles/step; the immediate-hot result ranges from 399.415 to 399.856. That flatness is expected: the one-warp repeat touches only about 16,384 link visits, so its active subset fits in L2 regardless of the allocation's total size. This experiment measures the hot-L2 versus post-eviction global-path cost; the saturated Vulkan experiment above measures whole-working-set capacity.

The median CUDA-event duration divided by 512 steps is 153.414 ns hot and 401.820 ns post-eviction. Those nanosecond figures include the complete one-warp kernel's prologue, final stores, and any scheduling; the `clock64()` cycle values remain the cleaner in-loop comparison.

The compiler reports 17 registers and zero spills for both the chase and clock-only control. Native `sm_120` SASS contains two `CS2R ..., SR_CLOCKLO` reads and one static `LDG.E.STRONG.GPU` in the chase loop; the control contains the two clock reads and no load. `clock64()` includes thread time slicing, and a warp instruction may request up to 32 random cache sectors. The result is therefore reported as cycles per exposed dependent warp step, not an undocumented scalar L2-hit or DRAM-transaction latency.

Taken together, the experiments say something more useful than either alone: the controlled hot and post-eviction step costs are nearly constant across allocation sizes, while the saturated working-set time rises sharply only after 36 MiB. The capacity cliff therefore reflects a changing mix of cache service, memory queuing and warp scheduling, not a change in the intrinsic cost of an L2 hit. A two-state hit/miss formula cannot be inverted honestly here: the Vulkan 128/36 MiB ratio is 6.295x, already above the CUDA post-eviction/hot ratio of 2.722x, proving that saturated queuing/scheduling contributes materially.

### Native CUDA concurrency and memory-level parallelism

The concurrency control uses the same `sm_120`, `clock64()` and `ld.global.cg.u32` path, but launches one 32-lane warp per block and scales from 1 through 736 independent warps. Every lane retains a strictly dependent 512-step chain; only the number of independently schedulable chains changes. CUDA's occupancy query reports a ceiling of 24 such blocks per SM, while the measured range stops at 16 warps per SM. Four sequentially isolated processes reverse both table and concurrency order to expose order/clock sensitivity.

| Table | Hot at 1 warp | Hot at 46 warps | Hot at 184 warps | Hot at 736 warps | 736-warp logical rate | Slowdown vs 4 MiB at 736 warps |
|---:|---:|---:|---:|---:|---:|---:|
| 4 MiB | 0.208 Gload/s | 9.582 Gload/s | 36.437 Gload/s | 42.861 Gload/s | 159.67 GiB/s | baseline |
| 36 MiB | 0.208 Gload/s | 8.287 Gload/s | 23.599 Gload/s | 42.863 Gload/s | 159.68 GiB/s | 1.000x |
| 40 MiB | 0.208 Gload/s | 3.943 Gload/s | 13.839 Gload/s | 23.429 Gload/s | 87.28 GiB/s | 1.829x |
| 64 MiB | 0.208 Gload/s | 3.841 Gload/s | 8.209 Gload/s | 9.318 Gload/s | 34.71 GiB/s | 4.600x |
| 128 MiB | 0.208 Gload/s | 3.503 Gload/s | 6.963 Gload/s | 7.506 Gload/s | 27.96 GiB/s | 5.710x |

`Gload/s` counts requested scalar `u32` loads, and logical GiB/s multiplies those requests by four bytes. Random warp loads can fetch much larger sectors or cache lines, so neither column is physical cache or DRAM bandwidth. The single-warp rows remain flat because one repeated warp touches only about 64 KiB of logical link values. As concurrency grows, paths cover enough of the randomly distributed allocation for capacity to become decisive.

The 736-warp in-kernel exposure is 1,474.8 cycles/step at 4 MiB and 1,473.3 at 36 MiB, then 2,703.4 at 40 MiB, 6,965.9 at 64 MiB and 8,674.1 at 128 MiB. Throughput rises while the GPU fills, then exposed cycles rise as resident warps compete. This is the missing concurrency model behind the earlier observation: the one-warp 2.722x cold/hot ratio is a controlled service-cost bound, while the 5.710x saturated 128/4 MiB slowdown includes queuing and scheduling.

### Representation floor

The current G20 hot record is five native 32-bit words: four packed binary16 geometry pairs plus guard/meta. The arbitrary 32-bit lineage value is the sixth word in cold storage. Under the present field precision and arbitrary-lineage contract, **20 hot + 4 cold bytes is the practical native floor demonstrated here**.

A true 20-byte total record is possible only if lineage can be derived from the candidate index, reconstructed from another source, narrowed, or omitted. That is an application contract change, not free compression. More aggressive compression would require additional quantization, constrained coordinate domains, axis reconstruction, or a changed output/identity contract; no honest information-theoretic minimum can be stated without those domain assumptions.

The E16 event is likewise a practical aligned ABI rather than a mathematical lower bound. It carries a 32-bit SDF, two binary16 values, topology flags, and 32-bit lineage. Going below 16 bytes requires changing precision, packing/alignment, identity, or downstream access assumptions.

### LUT ceiling

The G24 log-threshold LUT occupies 128 bytes, only 0.000339% of the 36 MiB L2. Capacity is not its problem. The balanced control shows that direct arithmetic is faster below L2 and effectively tied when bandwidth-bound, so the LUT does not improve this kernel on this GPU. A separate byte-identical packed-table control compares `texelFetch` with SSBO loads: their random-throughput ratios are 0.989x, 1.002x, 1.000x and 1.000x at 16, 32, 64 and 128 MiB, and both lose about 79.36% from 32 to 64 MiB. Putting the table on the texture-buffer path therefore does not create extra effective capacity beyond the shared cache/memory bottleneck on this GPU. The package recommends the direct decoder despite the LUT's excellent size.

For a larger log LUT, the human-readable capacity ceilings are:

| Encoding | Bytes/code | Codes in 36 MiB absolute ceiling | Codes in 28 MiB conservative target |
|---|---:|---:|---:|
| Current native two-16-bit-codes-per-word layout | 2.00 | 18,874,368 | 14,680,064 |
| Ideal densely bit-packed 6-bit stream | 0.75 | 50,331,648 | 39,146,837 |

The ideal 6-bit row is an information-capacity calculation, not a measured texture format. Native texture-buffer formats do not expose 6-bit elements directly; random extraction may straddle words and add instructions. It offers a theoretical 2.667x code-density gain over the current 16-bit slots only if decoding and access granularity do not erase the benefit. The measured recommendation is therefore to keep the hot LUT plus competing state below roughly 28 MiB, not to assume that a nominal 36 MiB table leaves useful L2 space for anything else.

## Validation strength and limits

The G20/G24 comparison adds 795,082,752 candidate-dispatch records and 290,199,888 checked output records. The four texture/SSBO path-control processes add 2,281,701,376 checked outputs, bringing the main physical-GPU output corpus to **4,413,045,560 checked GPU output records**. The Vulkan shader-clock study separately adds 12,582,912 checked invocation payloads whose validated chain endpoints represent 3,221,225,472 executed dependent loads. The one-warp CUDA cycle control adds another 153,600 checked payloads whose endpoints represent 52,428,800 dependent loads. The CUDA concurrency matrix adds **42,883,200 checked payloads representing 14,637,465,600 dependent loads** across 220 valid raw rows.

All 52 bundled SPIR-V modules pass `spirv-val --target-env vulkan1.2`. The paired cache control disassembles to `OpImageFetch` for the uniform-texel path and storage-buffer `OpLoad` for the SSBO path. The latency control and chase modules each contain two device-scope `OpReadClockKHR` instructions, while only the chase module retains the dependent-load loop. Both independently compiled CUDA probes contain native `sm_120` clock-register reads and L2/global-load SASS with no spills; Compute Sanitizer reports zero errors for the concurrency control. G20 disassembly confirms a real `ArrayStride 20`, storage binding 4 for lineage, subgroup ballot operations, four atomic counter sites in the counted variant, and no texture fetch. In the optimized module, the lineage `OpLoad` is located after the non-verified early-return branch, confirming that only retained lanes execute the logical lineage load.

Native NVIDIA compiler metadata was captured through `VK_KHR_pipeline_executable_properties` in all six isolated processes. G24 and G20 append both report 22 registers, 2,052 bytes shared memory, and a 3,456-byte executable, so the append gain cannot honestly be attributed to fewer registers or a smaller kernel. The counted variants report 40 versus 39 registers, equal 5,124-byte shared memory, and 4,736 versus 4,864-byte executables. The driver also returns an implausible 64 GiB per-thread `Local Memory Size` for every executable; that value is preserved, flagged, and excluded from occupancy reasoning.

The remaining limit is observability: timestamps, Vulkan shader-clock intervals, CUDA cycle intervals and exact readback validation are native and real, but exact L2 hit rate, cache-sector traffic, and DRAM bytes are not available until NVIDIA performance-counter permission is enabled. A native schema-1.8 probe additionally confirms that the selected NVIDIA Vulkan device exposes pipeline-executable metadata but not `VK_KHR_performance_query`. Consequently, this report labels logical byte models and nominal L2 residency as theory/inference rather than hardware-counter facts.

Machine-readable paired results are in `windows_physical_gpu_aggregate/cold_lineage_comparison.csv`, `windows_physical_gpu_aggregate/lut_path_comparison.csv`, `windows_physical_gpu_aggregate/l2_latency_comparison.csv`, `windows_physical_gpu_aggregate/cuda_l2_clock_comparison.csv`, and `windows_physical_gpu_aggregate/cuda_l2_mlp_comparison.csv`; compiler metadata is in `windows_physical_gpu_aggregate/pipeline_executable_statistics.csv`, and the full aggregate is `windows_physical_gpu_aggregate/aggregate_metrics.json`. Vulkan shader-clock raw data is under `l2_latency_isolated/`; CUDA cycle and concurrency data are under `cuda_l2_clock_isolated/` and `cuda_l2_mlp_isolated/`; cache-path controls are under `lut_path_control/`; cold-lineage primary results are under `cold_lineage_isolated/`; `native_capability_probe/` records the selected-device extension evidence. The earlier overlapping-process `cold_lineage_hot/` corpus is retained but excluded from primary claims.
