# UGTS yield, compression, and practical limits

Date: 2026-08-15  
Device: NVIDIA GeForce RTX 5070 Ti Laptop GPU  
Execution path: direct Vulkan compute and native CUDA `sm_120` on the physical GPU, using device-local allocations  
Reported L2 capacity: 36 MiB (37,748,736 bytes), returned by the local CUDA device-properties query

## Plain-language result

For the fixed benchmark corpus, roughly **1 candidate in 21 becomes an event**. The measured G32/G24/G20 path retained 199,179 of 4,194,304 candidates, a **4.7488% event yield**. Compacting to only those events makes the logical event stream **21.058x smaller** than a dense E16 stream.

The practical single-pass implementation reserves room for 1 event per 16 candidates (6.25%). At the largest measured case this is a 4 MiB buffer instead of 64 MiB, a **16x allocation reduction**, with zero overflow and 0.961 MiB left unused.

The best measured total layout is the fixed-query G24 state with E16 bounded output: **100 MiB total allocation** for 4,194,304 candidates, versus 192 MiB for packed G32 plus dense E16 and 384 MiB for authoritative G64 plus dense E32. That is respectively **1.92x** and **3.84x** less memory.

Separating lineage into a cold stream does not reduce total storage: G20 hot state + 4-byte cold lineage is still 24 bytes per candidate. It does reduce the allocation touched by every lane from 100 MiB to 84 MiB at the largest case. Six balanced, sequentially isolated process runs measured a **1.108x append speedup** and **1.110x counted-path speedup** over G24 at 4,194,304 candidates. This is useful, but it is not the theoretical 1.190x maximum because retained lanes still fetch lineage and cache-line amplification is real.

A native `VK_KHR_shader_clock` pointer chase now sharpens the cache boundary. Random dependent-load time is flat through the exact reported 36 MiB L2 size, rises **1.242x at 38 MiB**, and reaches **2.134x at 40 MiB**, **4.714x at 64 MiB**, and **6.295x at 128 MiB**, all relative to 36 MiB. Sequential dependent loads rise only 3.57% from 36 to 128 MiB because adjacent accesses retain spatial locality.

An independent native CUDA `sm_120` control supplies a real cycle-domain comparison. One warp using L1-bypassing `ld.global.cg` measures a cross-size median of **399.57 cycles per hot dependent step** and **1,087.79 cycles after a 256 MiB L2-eviction pass**: the post-eviction path is **2.722x** slower, or about 688 additional exposed cycles per step. CUDA event timing corresponds to approximately **153.4 ns per hot step** and **401.8 ns per post-eviction step** for the complete one-warp kernel. These are warp-exposed values, not the latency of one scalar memory transaction.

A new native CUDA concurrency sweep closes the gap between that one-warp control and the saturated Vulkan result. At the occupancy-query ceiling of 1,104 independent warps (24 warps per SM), a hot 36 MiB random table sustains **43.215 billion requested `u32` loads/s**, indistinguishable from the 4 MiB control. Expanding the table by only 4 MiB to 40 MiB drops throughput **45.20% to 23.683 Gload/s**. The 64 and 128 MiB cases deliver only 9.357 and 7.524 Gload/s. This directly confirms that packing the hot random-access footprint at or below L2 matters under production-like concurrency; it also shows that scheduler and memory-queue pressure, not just a fixed hit/miss latency, creates the large above-L2 slowdown.

The texture-cache hypothesis is now tested through native CUDA instructions as well as Vulkan descriptors. The same bytes and chains compile to `TLD.LZ` through a linear texture object and `LDG.E.STRONG.GPU` through the L2/global path. At full occupancy their median hot-rate ratio across 4-128 MiB is **0.99949x**, and both lose about **45.2% from 36 to 40 MiB**. At one warp, texture is **13.65% slower** and exposes 17.55% more cycles. Texture placement therefore does not create more usable capacity or improve this dependent random LUT on the named GPU; byte packing is the useful lever.

That byte-packing lever is now measured natively rather than left theoretical. Sixteen 6-bit codes occupy three words instead of using two 16-bit slots per word. At full occupancy and the same 36 MiB physical budget, the texture path holds **50,331,648 packed codes at 42.594 billion decoded lookups/s**, versus **18,874,368 slot codes at 43.192 billion/s**. This realizes the full **2.667x capacity for only 1.39% throughput loss**. Packed texture loses 45.05% at the 40 MiB endpoint, proving that packing moves logical capacity without moving the physical cache boundary.

The locality continuum is now measured rather than inferred from only its endpoints. A strictly load-dependent sparse pointer chase scales **4:2:1 at 32/64/128-byte spacing**, with 256-byte spacing following the 128-byte curve. That remains a valid workload-level bound of **128 effective bytes per isolated dependent pointer**, but a new independent random packed-LUT sweep proves it is **not a universal per-code cache charge**.

The new sweep varies useful occupancy from 1 through 170 packed 6-bit codes inside aligned 128-byte regions and tests the exact 42/43, 85/86 and 128/129 code boundaries. At 36 MiB every layout sustains **42.437-43.010 billion texture lookups/s**. At 40 MiB, throughput changes continuously from **42.800 Glookup/s** for one useful code to **23.514 Glookup/s** for 170 useful codes; at 48 MiB the range is **28.104 to 12.628 Glookup/s**. Crossing a 32-byte address boundary with only one additional code causes a small change because that new region is requested on only 1/43, 1/86 or 1/129 lookups. This is direct evidence that neighborhood-use probability matters; neither “0.75 bytes/code” nor “128 bytes/code” alone predicts a random LUT's effective residency.

A follow-on stride decomposition now explains that continuum more tightly. Holding allocation and aligned 128-byte-line count at 40 MiB/327,680 while requesting four, two or one 32-byte portions per line produces **23.343, 38.505 and 42.802 Glookup/s**. Holding requested 32-byte span at 12 MiB while increasing containing-line count from 98,304 to 393,216 lowers throughput from **43.214 to 28.119 Glookup/s**. The evidence therefore supports separate resident-data and line-address pressures plus a smaller address-span modifier. These are predictive layout models, not privileged NVIDIA sector/tag measurements.

Extending the same lookup to 4-KiB spacing reveals a second engineering boundary. With useful words and containing test-line count fixed, native throughput remains full at a 252 MiB address span and falls between **252 and 256 MiB**. Exact 512- and 1,024-byte pitches also create a separate texture-path alias: changing pitch by only 32 bytes can restore full rate. At a 7 MiB target, 992/1,024/1,056-byte texture strides deliver **42.802/28.621/43.007 Glookup/s** while the global path stays near 42.8. Sparse LUT layout therefore needs both total-span and stride-index terms; neither is relabeled as a measured TLB or cache-set specification.

A CUDA VMM control now removes the remaining physical-capacity ambiguity. Every virtual slot aliases the same **2 MiB physical allocation**, only one eighteenth of the 36 MiB L2, while virtual reach is swept from 64 to 510 MiB. Full-occupancy global/texture rates remain near 42.9 Glookup/s through 240 MiB, then fall together to **39.523/39.539 at 248 MiB**, **35.663/35.687 at 252 MiB**, and **34.439/34.456 at 256 MiB**. The 252-256 MiB transition therefore survives with constant physical backing and is an address-reach/distribution limit for this workload, not unique-data overflow of L2.

CUDA's hardware-compression hint is also tested rather than inferred. The driver grants and reports effective generic-compressible allocations, but periodic and entropy-dense packed6 LUTs measure generic/non-compressible median ratios of essentially **1.000x** and keep the same 36-40 MiB cliff. Hardware compression therefore provides no usable extra capacity for these information-bearing log-code patterns. Constant-content upper controls are radically different: both all-zero words and independently checked all-one words hold the global path near 38.6 Glookup/s through **240 MiB / 335,544,320 packed codes**, a **6.667x throughput-equivalent allocation-capacity lower bound** relative to 36 MiB. The all-one control reaches 38.611 Glookup/s at 240 MiB versus 7.004 without compression. These are zero-information constant tables, not measured byte-compression ratios, and both lose throughput at the 248 MiB address-reach boundary.

An important texture erratum prevents overclaiming. The spectacular all-zero texture rates were reproduced, but a nonzero constant control then produced **zero valid timed texture payloads**, while the global constant path and periodic/entropy texture paths stayed valid. The zero checker can accept an incorrect zero return. Therefore the all-zero texture curve is a sentinel false positive and is excluded completely from cache-capacity and compression claims; the valid information-bearing texture rows still show no benefit.

### At-a-glance metrics

| Question | Human-readable answer | Status |
|---|---|---|
| How many candidates become events? | 199,179 of 4,194,304: **4.7488%**, or about **1 in 21.058** | Measured and validated |
| How much does exact event compaction save? | 64 MiB dense E16 becomes 3.039 MiB of actual events: **95.2512% fewer bytes / 21.058x smaller** | Corpus-specific exact result |
| What is the practical one-pass output allocation? | 4 MiB at a 6.25% bound: **16x smaller** than dense, 75.98% utilized, zero overflow | Measured implementation |
| What is the best complete tested layout? | G24 + bounded E16 is **100 MiB**, versus 384 MiB for G64 + dense E32: **3.84x smaller** | Fixed-query profile |
| What does 6-bit LUT packing save? | 2.00 to 0.75 byte/code: **62.5% fewer bytes / 2.667x more codes** | Exact encoding and native implementation |
| Does CUDA generic compression add packed-LUT capacity? | **No for periodic or entropy-dense packed6 (about 1.000x).** All-zero and all-one constant controls reach a **6.667x throughput-equivalent allocation bound** through 240 MiB | Constant-content native VMM bound; physical ratio unmeasured |
| How close is block packing to the information floor? | 170 codes use 1,020/1,024 bits: **99.609% bit yield**, 0.752941 byte/code | Practical block ceiling |
| How many dense packed codes fit nominal 36 MiB L2? | **50,331,648** in a continuous stream; **50,135,040** in 170-code blocks | Arithmetic ceiling; 42.592 Glookup/s block result |
| What is the safer dense-LUT target? | **39,146,832 measured codes just below 28 MiB**, reserving 8 MiB of nominal L2 | Engineering target, not theorem |
| Does texture add cache capacity? | No measured gain: valid information-bearing native texture/global median **0.99949x**, with the same roughly 45.2% 36-to-40 MiB loss. The all-zero texture curve is invalidated by a nonzero sentinel | Matched native control plus semantic erratum |
| Is sparse residency always 128 bytes/code? | **No.** That bound applies to the dependent pointer chase; independent packed lookups follow probability-weighted neighborhood use | Corrected by line-occupancy sweep |
| What predicts sparse independent LUT residency? | At least **requested data portions + containing-line count + address span**; none alone fits every curve | Native stride decomposition |
| What limits very sparse page-spaced LUTs? | Full rate through **240 MiB**, measurable loss at **248 MiB**, and a 252-256 MiB transition even with only **2 MiB physical backing**; also avoid exact 512/1,024-byte texture pitches | VMM-isolated device/workload timing bound |
| What is the universal lossless one-pass event bound? | **100% output capacity** unless the application supplies a yield contract | Theoretical worst case |

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

The 36 MiB values are arithmetic maxima, not safe production allocations. The 28 MiB column reserves 8 MiB (22.2% of L2) for cache-line amplification, other state, outputs, code and system activity. The measured G32/G24 cliffs occur near the absolute crossings, and the new full-occupancy concurrency probe sustains full hot throughput at 36 MiB but loses 45.20% at 40 MiB. Exact NVIDIA cache-hit/DRAM counters remain permission-blocked (`ERR_NVGPUCTRPERM`), so these are engineering limits supported by timing and throughput cliffs rather than counter-derived hit thresholds.

The stride experiment quantifies the cache-line-amplification warning for a strictly load-dependent pointer chain. A densely used stream can approach its encoded bytes per useful entry; that sparse dependent chain paid an effective 128 bytes for one useful `u32` on this workload. These are endpoint bounds, not a universal conversion from logical bytes to cache bytes:

| Access locality | Effective bytes/useful entry | 36 MiB ceiling | 28 MiB target |
|---|---:|---:|---:|
| Dense packed 6-bit stream | 0.75 average | 50,331,648 | 39,146,837 arithmetic; 39,146,832 measured whole-group endpoint |
| Dense 16-bit slots | 2.00 | 18,874,368 | 14,680,064 |
| Dependent pointer chase, one active `u32` per effective region | 128 workload-level bound | 294,912 | 229,376 |

The independent random packed-LUT sweep resolves the space between those endpoints. It shows that even one useful code per aligned 128-byte region does not behave like a fixed 128-byte throughput charge: it retains 99.02% of its 28 MiB rate at a 40 MiB allocation and 65.02% at 48 MiB. The stride decomposition further shows why: requested subregion data and containing-line count are separate constraints, while doubling address span adds another near-boundary penalty. Real LUTs therefore depend on neighborhood reuse, line distribution, dependency, ordering and address span—not encoded bytes alone.

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

The concurrency control uses the same `sm_120`, `clock64()` and `ld.global.cg.u32` path, but launches one 32-lane warp per block and scales from 1 through 1,104 independent warps. Every lane retains a strictly dependent 512-step chain; only the number of independently schedulable chains changes. CUDA's occupancy query reports a ceiling of 24 such blocks per SM, and the measured range reaches that exact ceiling. Four sequentially isolated processes reverse both table and concurrency order to expose order/clock sensitivity.

| Table | Hot at 1 warp | Hot at 46 warps | Hot at 184 warps | Hot at 1,104 warps | Full-occupancy logical rate | Full-occupancy slowdown vs 4 MiB |
|---:|---:|---:|---:|---:|---:|---:|
| 4 MiB | 0.208 Gload/s | 9.582 Gload/s | 36.472 Gload/s | 43.216 Gload/s | 160.99 GiB/s | baseline |
| 36 MiB | 0.208 Gload/s | 8.291 Gload/s | 23.564 Gload/s | 43.215 Gload/s | 160.99 GiB/s | 1.000x |
| 40 MiB | 0.208 Gload/s | 3.948 Gload/s | 13.826 Gload/s | 23.683 Gload/s | 88.23 GiB/s | 1.825x |
| 64 MiB | 0.208 Gload/s | 3.842 Gload/s | 8.209 Gload/s | 9.357 Gload/s | 34.86 GiB/s | 4.618x |
| 128 MiB | 0.208 Gload/s | 3.499 Gload/s | 6.963 Gload/s | 7.524 Gload/s | 28.03 GiB/s | 5.744x |

`Gload/s` counts requested scalar `u32` loads, and logical GiB/s multiplies those requests by four bytes. Random warp loads can fetch much larger sectors or cache lines, so neither column is physical cache or DRAM bandwidth. The single-warp rows remain flat because one repeated warp touches only about 64 KiB of logical link values. As concurrency grows, paths cover enough of the randomly distributed allocation for capacity to become decisive.

At full occupancy, in-kernel exposure is 2,214.9 cycles/step at 4 MiB and 2,212.2 at 36 MiB, then 4,060.7 at 40 MiB, 10,428.3 at 64 MiB and 12,984.4 at 128 MiB. Throughput rises while the GPU fills, then exposed cycles rise as resident warps compete. This is the missing concurrency model behind the earlier observation: the one-warp 2.722x cold/hot ratio is a controlled service-cost bound, while the 5.744x saturated 128/4 MiB slowdown includes queuing and scheduling.

### Representation floor

The current G20 hot record is five native 32-bit words: four packed binary16 geometry pairs plus guard/meta. The arbitrary 32-bit lineage value is the sixth word in cold storage. Under the present field precision and arbitrary-lineage contract, **20 hot + 4 cold bytes is the practical native floor demonstrated here**.

A true 20-byte total record is possible only if lineage can be derived from the candidate index, reconstructed from another source, narrowed, or omitted. That is an application contract change, not free compression. More aggressive compression would require additional quantization, constrained coordinate domains, axis reconstruction, or a changed output/identity contract; no honest information-theoretic minimum can be stated without those domain assumptions.

The E16 event is likewise a practical aligned ABI rather than a mathematical lower bound. It carries a 32-bit SDF, two binary16 values, topology flags, and 32-bit lineage. Going below 16 bytes requires changing precision, packing/alignment, identity, or downstream access assumptions.

### LUT ceiling

The G24 log-threshold LUT occupies 128 bytes, only 0.000339% of the 36 MiB L2. Capacity is not its problem. The balanced control shows that direct arithmetic is faster below L2 and effectively tied when bandwidth-bound, so the LUT does not improve this kernel on this GPU. A separate byte-identical Vulkan control compares `texelFetch` with SSBO loads: their random-throughput ratios are 0.989x, 1.002x, 1.000x and 1.000x at 16, 32, 64 and 128 MiB, and both lose about 79.36% from 32 to 64 MiB. The native CUDA control independently compiles the paths to real `TLD.LZ` and `LDG.E.STRONG.GPU` instructions; at full occupancy its texture/global ratio is 0.99949x across sizes, with matching 45.2% 36-to-40 MiB losses. Putting the table on either texture path therefore does not create extra effective capacity beyond the shared lower cache/memory bottleneck on this GPU. The package recommends the direct decoder despite the LUT's excellent size.

For a larger log LUT, the human-readable capacity ceilings are:

| Encoding | Bytes/code | Codes in 36 MiB absolute ceiling | Codes in 28 MiB conservative target |
|---|---:|---:|---:|
| Current native two-16-bit-codes-per-word layout | 2.00 | 18,874,368 | 14,680,064 |
| Native densely bit-packed 6-bit stream | 0.75 | 50,331,648 | 39,146,837 |

The capacity arithmetic is now backed by a native CUDA implementation. Packed extraction performs one word load for 14/16 offsets and a second predicated load for the two straddling offsets. The 36 MiB endpoint contains exactly 50,331,648 codes. Whole 16-code packing groups put the measured conservative endpoint four bytes below 28 MiB at 39,146,832 codes, only five below the mathematical floor in the table. At full occupancy the texture path preserves 98.61% of slot throughput at 36 MiB and 98.63% at 28 MiB while storing 2.667x as many codes. The recommendation remains to keep the hot LUT plus competing state below roughly 28 MiB, because nominal 36 MiB leaves no useful L2 margin.

The 6-bit information floor for exactly 64 possible codes is 0.75 byte/code. The 170-code-per-128-byte block implementation uses 1,020 of 1,024 bits, or **99.609% packing yield**, and costs 0.752941 byte/code. At 36 MiB it holds 50,135,040 codes, only 196,608 (0.3906%) below a boundary-free packed stream. This is the practical block-aligned ceiling measured by the line-occupancy control; it excludes indices, page tables, descriptors, outputs, and all competing state.

### Packed-LUT neighborhood-use continuum

The line-occupancy control chooses a random aligned 128-byte region and then a uniformly random useful packed slot inside it. Unused words contain mixed nonzero data, so zero-fill or compression cannot make the physical allocation disappear. The table below reports full-occupancy native texture results. “32-byte demand” is exact address arithmetic: each percentage is the probability that one lookup asks for that 32-byte part of its chosen 128-byte region. It is not an NVIDIA performance-counter sector measurement.

| Useful codes / 128 B | Physical bytes / useful code | Per-lookup 32-byte demand | Useful codes at 36 MiB | 36 MiB | 40 MiB | 48 MiB |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 128.000 | 100% | 294,912 | 43.010 G/s | 42.800 G/s | 28.104 G/s |
| 42 | 3.0476 | 100% | 12,386,304 | 43.009 G/s | 42.599 G/s | 28.093 G/s |
| 43 | 2.9767 | 100% + 2.33% | 12,681,216 | 42.491 G/s | 41.978 G/s | 26.491 G/s |
| 64 | 2.0000 | 67.19% + 34.38% | 18,874,368 | 42.590 G/s | 37.848 G/s | 18.385 G/s |
| 85 | 1.5059 | 50.59% + 50.59% | 25,067,520 | 42.677 G/s | 37.366 G/s | 17.900 G/s |
| 86 | 1.4884 | 50.00% + 51.16% + 1.16% | 25,362,432 | 42.437 G/s | 36.139 G/s | 17.583 G/s |
| 128 | 1.0000 | 33.59% + 34.38% + 33.59% | 37,748,736 | 42.591 G/s | 28.645 G/s | 14.399 G/s |
| 129 | 0.9922 | 33.33% + 34.11% + 33.33% + 0.78% | 38,043,648 | 42.588 G/s | 27.939 G/s | 14.237 G/s |
| 170 | 0.7529 | 25.29% + 25.88% + 25.29% + 24.71% | 50,135,040 | 42.592 G/s | 23.514 G/s | 12.628 G/s |

Layouts with 1-42 useful codes request only the first 32-byte address region and share essentially the same capacity curve. The extra region introduced by code 43 is touched only 2.33% of the time; similarly, codes 86 and 129 introduce new regions at just 1.16% and 0.78% probability. The boundary-pair slowdowns are correspondingly modest: 43 versus 42 is 1.46% slower at 40 MiB, 86 versus 85 is 3.28% slower, and 129 versus 128 is 2.47% slower. As demand becomes balanced across two, three, and four regions, the above-L2 loss grows progressively.

The correct engineering model is therefore probabilistic and workload-specific. Storage capacity still follows the exact byte packing. Effective cache residency depends on which portions of that storage are requested, how often, and whether addresses are dependent or independently schedulable. The native sparse-stride control remains a valid opposite endpoint for its dependent chain: its 32/64/128-byte capacity anchors carry 1,179,648, 589,824 and 294,912 active entries at approximately the same 43.0 Gload/s hot plateau, and 256-byte spacing follows the 128-byte curve. It must not be relabeled as a universal 128-byte physical cache line or per-code cost.

### Sparse-LUT data and line-address decomposition

The follow-on independent-lookup control stores one useful packed6 code in the first word of each region and varies the region stride. Its `target_mib` is the requested 32-byte data span; the physical allocation grows in proportion to stride. This creates matched cases that separate useful data requested from the number and span of containing aligned 128-byte lines.

First, keep physical allocation and containing-line count fixed at 40 MiB and 327,680 lines, while changing how many requested 32-byte portions share each line:

| Region stride | Requested 32-byte span | Requested portions / 128-byte line | Full-occupancy texture rate |
|---:|---:|---:|---:|
| 32 B | 40 MiB | 4 | 23.343 Glookup/s |
| 64 B | 20 MiB | 2 | 38.505 Glookup/s |
| 128 B | 10 MiB | 1 | 42.802 Glookup/s |

Allocation and line count alone therefore cannot predict residency. Conversely, keep requested data fixed at 12 MiB and spread it over more containing lines:

| Region stride | Containing 128-byte lines | Physical allocation | Full-occupancy texture rate |
|---:|---:|---:|---:|
| 32 B | 98,304 | 12 MiB | 43.214 Glookup/s |
| 64 B | 196,608 | 24 MiB | 43.207 Glookup/s |
| 128 B | 393,216 | 48 MiB | 28.119 Glookup/s |
| 256 B | 393,216 | 96 MiB | 24.783 Glookup/s |

Requested byte count alone also fails. The 128-byte-stride one-portion-per-line curve remains hot at 10 MiB requested/40 MiB allocation, slows at 11 MiB/44 MiB, and falls sharply at 12 MiB/48 MiB: 42.802, 38.337 and 28.119 Glookup/s. An exact one-code refinement of the original occupancy kernel places the broader line-address transition between 43 and 44 MiB of line-equivalent allocation: 41.785 versus 38.330 Glookup/s, corresponding to 352,256 versus 360,448 containing lines.

Stride 256 and 128 have the same requested data and containing-line count but different address spans. Their paired texture-rate ratios at 9, 10, 11 and 12 MiB requested are 0.990, 0.945, 0.804 and 0.881. The complete evidence therefore needs at least three terms: **resident requested data, containing-line-address pressure, and an address-span modifier**. This is consistent with independently resident subregions inside a wider line-address grouping, but performance-counter access is unavailable, so it is not labeled as a privileged measurement of NVIDIA sectors, tags, sets, partitions or TLBs.

### Page-spaced address reach and stride aliasing

The page-stride control keeps useful words, requested data and containing 128-byte test-line count fixed at each target, then expands spacing through 4 KiB. At exact 4-KiB spacing the full-occupancy curve is:

| Useful words | Address span | Global | Texture |
|---:|---:|---:|---:|
| 32,768 | 128 MiB | 42.590 Glookup/s | 41.784 Glookup/s |
| 65,536 | 256 MiB | 34.315 Glookup/s | 34.451 Glookup/s |
| 98,304 | 384 MiB | 21.470 Glookup/s | 21.506 Glookup/s |
| 131,072 | 512 MiB | 18.424 Glookup/s | 18.462 Glookup/s |
| 262,144 | 1,024 MiB | 15.166 Glookup/s | 15.139 Glookup/s |

At 65,536 useful words only 256 KiB of distinct `u32` words and 8 MiB of containing test lines are involved, so their L2 data/line footprints remain well below the earlier knees. A padded control tightens the independent span transition: target 4 MiB with 2,016/2,048/2,080-byte pitch spans 252/256/260 MiB and gives 42.178/34.318/32.546 Glookup/s globally, with texture agreeing at 42.194/34.454/32.778. The workload-level full-rate boundary is therefore between **252 and 256 MiB of address span**.

That general boundary is separate from exact stride aliasing. At target 8 MiB, texture rates for 480/512/544-byte pitch are 42.805/26.494/42.775 Glookup/s. At target 7 MiB, 992/1,024/1,056-byte pitch gives 42.802/28.621/43.007 while global stays near 42.8. Larger padded allocation can therefore outperform the smaller exact power-of-two layout, rejecting a monotonic page-count explanation for this component. The defensible label is native address-index aliasing, not a reverse-engineered texture-cache set/bank count.

The CUDA driver separately reports VMM support, generic-compression capability and a 2 MiB minimum/recommended device-local VMM allocation granularity. The page-stride buffers use ordinary `cudaMalloc`; the 2 MiB property is context only and is not treated as their translation page size, compression state or TLB capacity. Explicit VMM compression is measured in its own control below.

### VMM control: constant physical backing, variable virtual reach

The stronger control allocates one 2 MiB device-local VMM object and maps it into every 2 MiB virtual slot. All aliases therefore resolve to the same physical words. Global and texture paths share the exact mapping and all four primary processes received the same base address. The high-occupancy 2 MiB-pitch sweep is:

| Virtual aliases | Virtual span | Physical backing | Global | Texture |
|---:|---:|---:|---:|---:|
| 32 | 64 MiB | 2 MiB | 42.976 Glookup/s | 42.879 Glookup/s |
| 64 | 128 MiB | 2 MiB | 42.979 Glookup/s | 42.863 Glookup/s |
| 96 | 192 MiB | 2 MiB | 42.973 Glookup/s | 42.870 Glookup/s |
| 120 | 240 MiB | 2 MiB | 42.975 Glookup/s | 42.838 Glookup/s |
| 124 | 248 MiB | 2 MiB | 39.523 Glookup/s | 39.539 Glookup/s |
| 126 | 252 MiB | 2 MiB | 35.663 Glookup/s | 35.687 Glookup/s |
| 128 | 256 MiB | 2 MiB | 34.439 Glookup/s | 34.456 Glookup/s |
| 132 | 264 MiB | 2 MiB | 31.942 Glookup/s | 31.943 Glookup/s |
| 160 | 320 MiB | 2 MiB | 24.901 Glookup/s | 24.913 Glookup/s |
| 192 | 384 MiB | 2 MiB | 21.568 Glookup/s | 21.565 Glookup/s |

The physical payload is 18x smaller than nominal L2 in every row. Holding alias count fixed also reproduces the loss: 32 aliases fall from 42.976 Glookup/s at a 64 MiB span to 33.717 at 250 MiB; 64 aliases fall from 42.979 at 128 MiB to 34.561 at 254 MiB. Virtual reach is therefore causal rather than merely correlated with more useful data. Near-identical `LDG`/`TLD` curves show that texture binding does not bypass this limit. The remaining defensible label is virtual address distribution/reach; hardware page size, TLB structure and page-walk events remain unmeasured.

### Native hardware-compression result

The allocation probe explicitly requests VMM compression enums 0 and 1, then queries each handle. The non-compressible request returns effective 0; the generic-compressible request returns effective 1. Both 2 MiB objects map, accept a full-device fill and verify first/last-word readback. The driver has therefore granted the mode, but this property exposes neither compressed bytes nor a compression ratio.

The performance matrix keeps the packed6 decoder at exactly 0.75 byte/code and compares four content controls with compression modes interleaved on every sample:

| Packed6 content | Information character | Median generic/non global | Median generic/non texture | Capacity conclusion |
|---|---|---:|---:|---|
| Zero | Zero entropy / all codes 0 | content- and size-dependent, up to 5.52x rate at 128 MiB | semantically invalidated by nonzero sentinel | Global hardware-compressible upper control only |
| All one | Zero entropy / all codes 63, packed words `0xFFFFFFFF` | 5.51x rate at 240 MiB | invalid; excluded | Independent nonzero global constant control |
| Periodic | `index mod 64`, 48-byte packed repetition | 0.99999x | 1.00001x | No cache-capacity gain |
| Entropy-dense | Mixed pseudorandom 6-bit codes | 1.00003x | 1.00005x | No cache-capacity gain |

The clean monotonic all-zero global curve is:

| Allocation | Packed codes | Non-compressible | Generic compressible | Generic/non |
|---:|---:|---:|---:|---:|
| 36 MiB | 50,331,648 | 38.498 Glookup/s | 38.645 Glookup/s | 1.004x |
| 40 MiB | 55,924,048 | 20.092 Glookup/s | 38.591 Glookup/s | 1.975x |
| 64 MiB | 89,478,480 | 8.691 Glookup/s | 38.525 Glookup/s | 4.455x |
| 128 MiB | 178,956,960 | 7.006 Glookup/s | 38.507 Glookup/s | 5.522x |
| 192 MiB | 268,435,456 | 7.125 Glookup/s | 38.593 Glookup/s | 5.415x |
| 240 MiB | 335,544,320 | 7.005 Glookup/s | 38.650 Glookup/s | 5.517x |
| 248 MiB | 346,729,120 | 6.990 Glookup/s | 28.823 Glookup/s | 4.124x |
| 256 MiB | 357,913,936 | 6.976 Glookup/s | 28.196 Glookup/s | 4.043x |
| 320 MiB | 447,392,416 | 6.887 Glookup/s | 4.748 Glookup/s | 0.689x |
| 512 MiB | 715,827,872 | 6.770 Glookup/s | 1.386 Glookup/s | 0.205x |

The independently validated all-one global control reproduces the same boundary:

| Allocation | Non-compressible | Generic compressible | Generic/non |
|---:|---:|---:|---:|
| 36 MiB | 38.492 Glookup/s | 38.652 Glookup/s | 1.003x |
| 40 MiB | 23.492 Glookup/s | 38.603 Glookup/s | 1.641x |
| 64 MiB | 9.312 Glookup/s | 38.635 Glookup/s | 4.149x |
| 128 MiB | 7.482 Glookup/s | 38.645 Glookup/s | 5.165x |
| 192 MiB | 7.126 Glookup/s | 38.651 Glookup/s | 5.424x |
| 240 MiB | 7.004 Glookup/s | 38.611 Glookup/s | 5.512x |
| 248 MiB | 6.991 Glookup/s | 28.834 Glookup/s | 4.125x |
| 320 MiB | 6.891 Glookup/s | 5.961 Glookup/s | 0.865x |

Full constant-table rate through 240 MiB is a **6.667x throughput-equivalent allocation-capacity lower bound** relative to 36 MiB. It is not proof that the compressor represents arbitrary data at 6.667x, nor a direct measurement that either constant allocation consumes exactly 36 MiB internally. Both constant tables have zero payload entropy before metadata. They bracket a supported constant-pattern class, while the periodic and entropy rows are the relevant result for actual packed log codes.

The 248 MiB loss despite constant compressible content independently confirms that byte compression does not remove virtual-address reach. At 320 MiB generic-compressed constant data becomes slower than its non-compressible control. The engineering rule is therefore: count the deterministic **2.667x software packing** for any 6-bit LUT, assume **no hardware-compression gain** for ordinary information-bearing codes unless their real distribution is separately profiled, and keep virtual reach below the measured 240-248 MiB transition.

The all-zero texture rates are now rejected as semantic evidence. A 174-210 MiB fine sweep found an exact three-MiB resonance and a one-group trim changed rate by up to 19.2x, but an all-one control produced zero valid timed texture payloads. The mismatch-total probe records 35,893,872 wrong codes out of 36,175,872 at 4 MiB and 22,609,920 out of 36,175,872 at 192 MiB for both compression modes. The zero checker can mask that failure. Periodic and entropy texture rows remain mismatch-free and show no generic-compression benefit, preserving the valid conclusion that a texture object is not an automatic extra-capacity or arbitrary-compression tier.

## Validation strength and limits

The G20/G24 comparison adds 795,082,752 candidate-dispatch records and 290,199,888 checked output records. The four texture/SSBO path-control processes add 2,281,701,376 checked outputs, bringing the main physical-GPU output corpus to **4,413,045,560 checked GPU output records**. The Vulkan shader-clock study separately adds 12,582,912 checked invocation payloads whose validated chain endpoints represent 3,221,225,472 executed dependent loads. The one-warp CUDA cycle control adds another 153,600 checked payloads whose endpoints represent 52,428,800 dependent loads. The full-occupancy CUDA concurrency matrix adds **74,678,400 checked payloads representing 25,490,227,200 dependent loads** across 240 valid raw rows. The matched CUDA texture/global matrix adds **98,426,880 checked payloads representing 33,596,375,040 dependent loads** across 256 valid raw rows. The packed-log matrix adds **270,673,920 checked payloads**, including 180,449,280 timed lookup payloads representing **92,390,031,360 individually checked decoded codes**, across 704 valid raw rows. The sparse-stride matrix adds **3,336,192 CPU-validated payloads** across 1,448 valid raw rows; 2,224,128 replayed timed endpoints cover 1,138,753,536 links, while the complete measured kernels execute **366,678,638,592 dependent GPU loads**. The packed-LUT line-occupancy matrix adds **2,064,384 CPU-validated payloads** across 1,792 valid raw rows; 1,376,256 replayed endpoints cover **704,643,072 CPU-replayed code checks**, while the complete timed kernels execute **453,790,138,368 GPU code lookups**. The sparse-address decomposition adds **1,622,016 CPU-validated payloads** across 1,408 valid raw rows; 1,081,344 replayed endpoints cover **553,648,128 CPU code checks**, while the timed kernels execute **356,549,394,432 GPU code lookups**. The one-code refinement separately adds 165,888 CPU payloads, 56,623,104 CPU checks and 36,465,278,976 GPU lookups across 144 valid rows. The page-span, 4-KiB-stride and stride-skew controls add **2,985,984 CPU-validated payloads**, **1,019,215,872 CPU code checks** and **656,375,021,568 timed GPU lookups** across 2,592 valid raw rows. The VMM physical-backing control adds **353,280 CPU-replayed payloads**, **227,512,320 complete zero-mismatch GPU payloads**, and **77,657,538,560 timed lookups** across 368 valid raw rows. The original VMM compression primary/zero-span checker accepts **830,914,560 payloads** and measures **283,618,836,480 timed lookups** across 1,184 rows; its zero-texture subset is now semantically excluded. The independent all-one global corpus adds **101,744,640 validated payloads** and **34,728,837,120 timed lookups** across 96 fully valid rows.

All 52 bundled SPIR-V modules pass `spirv-val --target-env vulkan1.2`. The paired cache control disassembles to `OpImageFetch` for the uniform-texel path and storage-buffer `OpLoad` for the SSBO path. The latency control and chase modules each contain two device-scope `OpReadClockKHR` instructions, while only the chase module retains the dependent-load loop. The independently compiled CUDA probes contain native `sm_120` clock-register reads and no spills; the texture control additionally proves distinct `TLD.LZ` and `LDG.E.STRONG.GPU` chase instructions. Packed-code SASS contains one slot load and a predicated second packed load through each native path; all four packing kernels retain 24-blocks/SM occupancy with 14-21 registers and zero spills. The sparse-stride SASS contains one `LDG.E.STRONG.GPU`, two clock reads and no timed-control load; it uses 16 registers, zero spills and the same 24-blocks/SM occupancy. The line-occupancy timed kernels compile to native `sm_120` with 26 registers for global and 22 for texture, zero spills, and 24 blocks/SM; SASS contains one unconditional plus one predicated `LDG.E.STRONG.GPU` or `TLD.LZ`, while the matched 18-register timing controls contain no table load. The sparse-address/page/alias timed global and texture kernels both use 22 registers, zero stack/spills and 24 blocks/SM; SASS has exactly one timed `LDG.E.STRONG.GPU` or `TLD.LZ` plus two clock reads, while the 18-register control has no table load. The VMM-alias kernels use 18 registers, zero stack/local memory/spills and 24 blocks/SM; their loop bodies contain exactly one native `LDG.E.STRONG.GPU` or `TLD.LZ` and two `SR_CLOCKLO` reads. The VMM compression packed6 kernels use 22 global or 19 texture registers, zero stack/local memory/spills and 24 blocks/SM; each active branch retains the unconditional plus predicated straddle loads and two clock reads. Compute Sanitizer reports zero errors through 4-KiB stride, a 1-GiB ordinary allocation, paired VMM aliases through 510 MiB, and compressed/non-compressed packed6 mappings through 512 MiB; instrumented timings are excluded. G20 disassembly confirms a real `ArrayStride 20`, storage binding 4 for lineage, subgroup ballot operations, four atomic counter sites in the counted variant, and no texture fetch. In the optimized module, the lineage `OpLoad` is located after the non-verified early-return branch, confirming that only retained lanes execute the logical lineage load.

Native NVIDIA compiler metadata was captured through `VK_KHR_pipeline_executable_properties` in all six isolated processes. G24 and G20 append both report 22 registers, 2,052 bytes shared memory, and a 3,456-byte executable, so the append gain cannot honestly be attributed to fewer registers or a smaller kernel. The counted variants report 40 versus 39 registers, equal 5,124-byte shared memory, and 4,736 versus 4,864-byte executables. The driver also returns an implausible 64 GiB per-thread `Local Memory Size` for every executable; that value is preserved, flagged, and excluded from occupancy reasoning.

The remaining limit is observability: timestamps, Vulkan shader-clock intervals, CUDA cycle intervals and exact readback validation are native and real, but exact L2 hit rate, cache-sector traffic, and DRAM bytes are not available until NVIDIA performance-counter permission is enabled. A native schema-1.8 probe additionally confirms that the selected NVIDIA Vulkan device exposes pipeline-executable metadata but not `VK_KHR_performance_query`. Consequently, this report labels logical byte models and nominal L2 residency as theory/inference rather than hardware-counter facts.

Machine-readable paired results are in `windows_physical_gpu_aggregate/cold_lineage_comparison.csv`, `windows_physical_gpu_aggregate/lut_path_comparison.csv`, `windows_physical_gpu_aggregate/l2_latency_comparison.csv`, `windows_physical_gpu_aggregate/cuda_l2_clock_comparison.csv`, `windows_physical_gpu_aggregate/cuda_l2_mlp_comparison.csv`, `windows_physical_gpu_aggregate/cuda_texture_lut_comparison.csv`, `windows_physical_gpu_aggregate/cuda_l2_stride_comparison.csv`, and the `cuda_packed_log_lut_*.csv` tables. The line-occupancy, sparse-address, page-span, page-stride, stride-skew, VMM-alias, VMM-compression, zero-compression-span and all-one global aggregates are under their correspondingly named `benchmarks/*_isolated/aggregate/` directories; the one-code transition refinement is under `cuda_lut_line_occupancy_k1_refinement/aggregate/`. Compiler metadata is in `windows_physical_gpu_aggregate/pipeline_executable_statistics.csv`, and the earlier combined aggregate is `windows_physical_gpu_aggregate/aggregate_metrics.json`. VMM capability/allocation-property results are under `cuda_vmm_granularity_probe/` and `cuda_vmm_compression_probe/`; compression semantics and the texture-zero erratum are under `cuda_vmm_compression_ones_global_isolated/` and `cuda_vmm_compression_zero_texture_alignment_isolated/`. Vulkan shader-clock raw data is under `l2_latency_isolated/`; cache-path controls are under `lut_path_control/`; cold-lineage primary results are under `cold_lineage_isolated/`; `native_capability_probe/` records the selected-device extension evidence. The earlier overlapping-process `cold_lineage_hot/` corpus is retained but excluded from primary claims.
