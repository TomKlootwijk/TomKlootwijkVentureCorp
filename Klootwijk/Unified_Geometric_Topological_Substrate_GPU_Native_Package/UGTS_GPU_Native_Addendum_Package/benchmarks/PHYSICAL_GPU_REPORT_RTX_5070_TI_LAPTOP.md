# UGTS-GN physical GPU validation — RTX 5070 Ti Laptop GPU

Run date: 2026-08-15 (Europe/Amsterdam)  
Status: physical discrete-GPU execution verified; direct hardware performance-counter access unavailable.

## Result

The UGTS compute path ran through the NVIDIA Vulkan driver on the local NVIDIA GeForce RTX 5070 Ti Laptop GPU. Storage buffers were allocated from `VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`; host-visible coherent buffers were used only for explicit upload/readback staging. GPU timestamps surround the compute dispatch, not transfer or CPU-oracle work.

This is the closest native path available in the installed Windows environment: direct Vulkan/SPIR-V with no Unity, Godot, browser, ANGLE, or SwiftShader layer. It is not strict bare-metal execution because Windows WDDM, the vendor driver, dynamic clocks, and the OS scheduler remain active.

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
| OS / CPU | Windows 11 build 26200 / Intel Core Ultra 7 255HX |

Core aggregate: three independent processes (`replicate_2`, `replicate_3`, and `replicate_4`), a minimum 500–750 ms warmup per case, and 100–200 measured dispatches per case. Reported latency and rates are medians of each process's device-timestamp p50; the rate range is the min/max across those processes. The earlier count-only `replicate_1` is retained but excluded because it did not reliably stabilize clocks.

## Core metrics at 4,194,304 candidates

| Profile | Mode | Device p50 | Candidate rate | Cross-run rate range | Verified-event rate | Logical bandwidth |
|---|---|---:|---:|---:|---:|---:|
| G64_E32 | evaluate | 0.824 ms | 5.089 Gcandidate/s | 5.085–6.277 G/s | 249.089 Mevent/s | 488.581 GB/s |
| G64_E32 | evaluate + commit | 0.822 ms | 5.105 Gcandidate/s | 5.085–6.279 G/s | 249.855 Mevent/s | 490.084 GB/s |
| G32_E16 | evaluate | 0.335 ms | 12.513 Gcandidate/s | 10.206–12.569 G/s | 594.209 Mevent/s | 600.616 GB/s |
| G32_E16 | evaluate + commit | 0.412 ms | 10.190 Gcandidate/s | 7.144–10.191 G/s | 483.895 Mevent/s | 489.113 GB/s |

“Logical bandwidth” is declared input-record bytes plus output-record bytes divided by device time. It is not measured DRAM traffic and can include cache reuse. At this batch size the packed G32_E16 path is 2.459× faster than G64_E32 for evaluation and 1.996× faster with atomic commit.

GPU-observed event counts at this size were:

| Profile | Supported | Support + compatible | Verified | Event yield |
|---|---:|---:|---:|---:|
| G64_E32 | 2,213,528 | 368,801 | 205,281 | 4.8943% |
| G32_E16 | 2,085,336 | 346,957 | 199,179 | 4.7487% |

## Inner-working verification

The revised harness reads back and checks every output record. It verifies scalar distance, guard, confidence, event time where present, support/compatibility/verified flags, route, lineage hash, and state flags. For commit variants it independently derives counts from output flags and requires the four GPU atomic counters to match exactly.

Across the three aggregate core runs, 112,529,408 output records passed. Across the two LUT-cache runs, 570,425,344 outputs passed.

The deterministic corpus contains values exactly on `r == radius` and `guard == 0`. NVIDIA and the CPU oracle do not always choose the same side after their different floating-point evaluation paths:

| Profile at N=4,194,304 | CPU/GPU topology divergences | Fraction | Boundary handling |
|---|---:|---:|---|
| G64_E32 | 5,219 | 0.12443% | all inside the explicit `5e-5` predicate-boundary band |
| G32_E16 | 321 | 0.00765% | all inside the explicit `5e-5` predicate-boundary band |

These are not silently treated as exact agreement. Validation requires exact GPU self-consistency and exact atomic-counter agreement; CPU/GPU topology disagreement is accepted only inside the recorded boundary band. Production semantics that require cross-device bit identity must define fixed-point predicates or explicit hysteresis/interval rules instead of comparing floating-point boundary values directly.

## L2 and buffer-texture LUT findings

The core sweep places declared input-plus-output working sets on both sides of the 36 MiB L2 size:

| Profile / mode | Working set | L2 fraction | Median candidate rate | Change past L2 |
|---|---:|---:|---:|---:|
| G64_E32 evaluate | 36 MiB | 1.00× | 13.948 G/s | — |
| G64_E32 evaluate | 48 MiB | 1.33× | 7.543 G/s | −45.9% |
| G32_E16 evaluate | 36 MiB | 1.00× | 35.669 G/s | — |
| G32_E16 evaluate | 48 MiB | 1.33× | 13.377 G/s | −62.5% |

The G32 value at the exact cache-size boundary showed substantial run-to-run variance, so the table is evidence of a capacity transition, not a direct cache hit-rate measurement.

The dedicated probe stores two unsigned 16-bit log codes per `R32_UINT` texel and reads them through a Vulkan `UNIFORM_TEXEL_BUFFER`. Two independent runs produced:

| Access | Packed table | L2 fraction | Median lookup rate | Cross-run range |
|---|---:|---:|---:|---:|
| random | 32 MiB | 0.89× | 41.224 Glookup/s | 41.111–41.336 G/s |
| random | 64 MiB | 1.78× | 7.261 Glookup/s | 7.260–7.263 G/s |
| random | 128 MiB | 3.56× | 6.922 Glookup/s | 6.922–6.922 G/s |
| sequential | 32 MiB | 0.89× | 68.103 Glookup/s | 62.482–73.724 G/s |
| sequential | 64 MiB | 1.78× | 74.407 Glookup/s | 74.399–74.415 G/s |
| sequential | 128 MiB | 3.56× | 75.138 Glookup/s | 75.134–75.141 G/s |

Random lookup throughput falls 82.39% (5.677× slower) from 32 MiB to 64 MiB. Sequential/coalesced access does not suffer that capacity cliff. A packed log LUT is therefore viable when its hot random-access footprint remains below roughly 32 MiB on this 36 MiB-L2 GPU, or when accesses are reordered/coalesced. A larger randomly accessed LUT should be tiled, mip-partitioned, or split into a compact hot index plus colder payload.

## Profiling boundary

Nsight Systems reported `ERR_NVGPUCTRPERM`: GPU performance-counter sampling requires a privilege not enabled on this machine. An attempted Vulkan trace produced a report file but no Vulkan API rows, so it is not used as evidence. No L2 hit-rate, sector count, or raw DRAM-byte claim is made. The cache conclusion is an inference from a controlled working-set sweep, the independently queried 36 MiB L2 size, and repeatable throughput behavior.

Dynamic laptop clocks and WDDM scheduling remain visible in the cross-process ranges. Device timestamps remove host submission latency from the metric but cannot remove clock/power-state variation.

## Reproduction

```powershell
# Build both direct Vulkan executables with Visual Studio Build Tools.
& .\gpu\scripts\build_windows_vulkan.ps1

# Core physical-GPU sweep.
& .\gpu\scripts\run_windows_vulkan_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\windows_native_run\new_run `
  -Sizes '262144,393216,524288,786432,1048576,2097152,4194304' `
  -Warmup 10 -WarmupMilliseconds 750 -Iterations 200

# Packed log-LUT texture-cache sweep.
& .\gpu\scripts\run_windows_lut_benchmarks.ps1 `
  -OutputDirectory .\benchmarks\windows_lut_cache_run\new_run `
  -Warmup 10 -WarmupMilliseconds 500 -Iterations 100
```

Primary machine-readable results are in `benchmarks/windows_physical_gpu_aggregate/aggregate_metrics.json`, with environment metadata in `environment.json`. Raw run JSON/CSV files remain in `benchmarks/windows_native_run/` and `benchmarks/windows_lut_cache_run/`.
