# UGTS yield, compression, and practical limits

Date: 2026-08-15  
Device: NVIDIA GeForce RTX 5070 Ti Laptop GPU  
Execution path: direct Vulkan compute on the physical GPU, using device-local storage buffers and native SPIR-V  
Measured L2 capacity: 36 MiB (37,748,736 bytes), reported by the local CUDA device-properties query

## Plain-language result

For the fixed benchmark corpus, roughly **1 candidate in 21 becomes an event**. The measured G32/G24/G20 path retained 199,179 of 4,194,304 candidates, a **4.7488% event yield**. Compacting to only those events makes the logical event stream **21.058x smaller** than a dense E16 stream.

The practical single-pass implementation reserves room for 1 event per 16 candidates (6.25%). At the largest measured case this is a 4 MiB buffer instead of 64 MiB, a **16x allocation reduction**, with zero overflow and 0.961 MiB left unused.

The best measured total layout is the fixed-query G24 state with E16 bounded output: **100 MiB total allocation** for 4,194,304 candidates, versus 192 MiB for packed G32 plus dense E16 and 384 MiB for authoritative G64 plus dense E32. That is respectively **1.92x** and **3.84x** less memory.

Separating lineage into a cold stream does not reduce total storage: G20 hot state + 4-byte cold lineage is still 24 bytes per candidate. It does reduce the allocation touched by every lane from 100 MiB to 84 MiB at the largest case. Six balanced process runs measured a **1.097x append speedup** and **1.102x counted-path speedup** over G24 at 4,194,304 candidates. This is useful, but it is not the theoretical 1.190x maximum because retained lanes still fetch lineage and cache-line amplification is real.

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

The six-process cold-lineage comparison used three forward and three reverse job orders, 750 ms minimum warmup, 200 timed dispatches per case, bounded 6.25% output, and twelve sizes from 1,310,720 through 4,194,304 candidates. All 432 benchmark rows passed payload, counter, completeness, overflow, and pipeline-cache reload validation.

At 4,194,304 candidates:

| Path | Append p50 | Candidate throughput | Emitted-event throughput | Paired speedup over G24 |
|---|---:|---:|---:|---:|
| G24 direct append | 0.167304 ms | 25.070 billion candidates/s | 1.191 billion events/s | baseline |
| G20 + cold lineage append | 0.152488 ms | 27.506 billion candidates/s | 1.306 billion events/s | 1.097x |
| G24 direct append + counts | 0.167456 ms | 25.047 billion candidates/s | 1.189 billion events/s | baseline |
| G20 + cold lineage append + counts | 0.152608 ms | 27.484 billion candidates/s | 1.305 billion events/s | 1.102x |

Across all twelve sizes, the median of the per-size paired speedups is 1.089x for append and 1.085x for append + counts. The smallest counted case is the exception (0.986x); the split should not be represented as an unconditional win for every dispatch size.

These rates are cache-hot steady-state rates from repeated dispatches against resident buffers. They are not cold one-pass DRAM streaming rates.

## Theoretical and practical limits

### Output capacity

- **Corpus-specific exact lower bound:** 199,179 E16 records, or 3,186,864 bytes (3.039 MiB). Achieving exactly this allocation without prior knowledge requires a count/scan followed by allocation and write, or an equivalent two-pass scheme.
- **Smallest measured lossless fraction:** 4.7488%. A rounded 4.75% allocation has only 51 event slots of slack in this corpus and is too fragile for production.
- **Current practical bound:** 6.25%, or 262,144 records/4 MiB. It is 75.98% utilized and has 62,965 spare records, equal to 31.61% headroom relative to observed demand.
- **Universal one-pass bound without a distribution contract:** 100% yield. Any candidate can theoretically verify, so a lossless single-pass caller must either reserve dense capacity, accept overflow, or use two passes. The observed 4.7488% is a workload property, not a universal theorem.

### L2-resident candidate limits

With a 6.25%-capacity E16 output, the output allocation costs exactly 1 byte per candidate. Ignoring small counters, code, descriptors, alignment, other GPU users, and cold-stream cache sectors, the nominal 36 MiB limits are:

| Always-hot layout | Nominal bytes/candidate | Theoretical candidates fitting in 36 MiB L2 |
|---|---:|---:|
| G32 + bounded output | 33 | 1,143,901 |
| G24 + bounded output | 25 | 1,509,949 |
| G20 hot + bounded output | 21 | 1,797,558 |

The measured G32 and G24 performance cliffs occur near these crossings, but exact NVIDIA cache-hit/DRAM counters are permission-blocked (`ERR_NVGPUCTRPERM`). These capacities are therefore nominal residency calculations supported by timing cliffs, not measured hit-rate thresholds.

For G20, the ideal traffic model adds only 4 bytes times the 4.7488% event yield, or **0.190 logical cold-lineage bytes per candidate**. The other bound is that sparse accesses pull enough cache sectors to approach the original 4 bytes per candidate. Thus the useful state/output traffic lies between approximately 21.19 and 25 bytes per candidate. The observed 1.097x large-case gain realizes about half of the ideal 19.05% bandwidth-ratio headroom.

### Representation floor

The current G20 hot record is five native 32-bit words: four packed binary16 geometry pairs plus guard/meta. The arbitrary 32-bit lineage value is the sixth word in cold storage. Under the present field precision and arbitrary-lineage contract, **20 hot + 4 cold bytes is the practical native floor demonstrated here**.

A true 20-byte total record is possible only if lineage can be derived from the candidate index, reconstructed from another source, narrowed, or omitted. That is an application contract change, not free compression. More aggressive compression would require additional quantization, constrained coordinate domains, axis reconstruction, or a changed output/identity contract; no honest information-theoretic minimum can be stated without those domain assumptions.

The E16 event is likewise a practical aligned ABI rather than a mathematical lower bound. It carries a 32-bit SDF, two binary16 values, topology flags, and 32-bit lineage. Going below 16 bytes requires changing precision, packing/alignment, identity, or downstream access assumptions.

### LUT ceiling

The G24 log-threshold LUT occupies 128 bytes, only 0.000339% of the 36 MiB L2. Capacity is not its problem. The balanced control shows that direct arithmetic is faster below L2 and effectively tied when bandwidth-bound, so the LUT does not improve this kernel on this GPU. The package therefore recommends the direct decoder despite the LUT's excellent size.

## Validation strength and limits

The new G20/G24 comparison adds 795,082,752 candidate-dispatch records and 290,199,888 checked output records. Combined with the earlier aggregate, the report corpus now contains **2,131,344,184 checked GPU output records**.

All 44 bundled SPIR-V modules pass `spirv-val --target-env vulkan1.2`. G20 disassembly confirms a real `ArrayStride 20`, storage binding 4 for lineage, subgroup ballot operations, four atomic counter sites in the counted variant, and no texture fetch. In the optimized module, the lineage `OpLoad` is located after the non-verified early-return branch, confirming that only retained lanes execute the logical lineage load.

The remaining limit is observability: timings and exact readback validation are native and real, but exact L2 hit rate, cache-sector traffic, and DRAM bytes are not available until NVIDIA performance-counter permission is enabled. Consequently, this report labels logical byte models and nominal L2 residency as theory/inference rather than hardware-counter facts.

Machine-readable paired results are in `windows_physical_gpu_aggregate/cold_lineage_comparison.csv` and `windows_physical_gpu_aggregate/aggregate_metrics.json`. Raw six-process results are under `cold_lineage_hot/`.
