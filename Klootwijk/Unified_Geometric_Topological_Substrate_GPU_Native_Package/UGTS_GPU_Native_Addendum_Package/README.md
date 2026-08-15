# UGTS-GN 1.1 - GPU-Native Geometric-Topological Substrate Addendum

This package is the GPU-native and physical-device revision of the unified substrate. It removes Unity/Godot adapters and makes the authoritative target a direct Vulkan/SPIR-V compute path or a measured hardware device.

## What is included

- `report/`: complete synthesis report and report source.
- `spec/`: 200-mechanism knowledge catalog, typed schema, ABI/state layout, metric definitions and claims ledger.
- `gpu/`: twelve Vulkan compute-shader sources, twenty-six named execution variants plus twenty-six optimized SPIR-V counterparts, the direct Vulkan runtime, and native CUDA `sm_120` L2 cycle/concurrency controls with build/run scripts.
- `reference/`: dependency-free CPU oracle and binary packers.
- `tests/`: executable reference tests.
- `benchmarks/`: raw and derived benchmark data, plots and named metrics.
- `hardware/`: fixed-function device architecture, register map, measurement plan and Q16.16 RTL reference gate.
- `sources/`: privacy-safe source manifest and source-by-source extraction notes.
- `examples/`: exchange-format and custom-encoder examples.

## Quick validation

```bash
python -m unittest discover -s tests -v
bash gpu/scripts/run_all_validation.sh
```

The original portable baseline in `benchmarks/vulkan_native_run/` selected SwiftShader, a CPU/software Vulkan device. A local Windows physical-GPU validation is now recorded in [`benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md`](benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md), with a human-readable [`yield, compression and limits report`](benchmarks/YIELD_COMPRESSION_LIMITS_RTX_5070_TI_LAPTOP.md). Raw and aggregate data is under `benchmarks/windows_native_run/`, `benchmarks/windows_integrated_lut_run/`, `benchmarks/windows_lut_cache_run/`, `benchmarks/lut_path_control/`, `benchmarks/lut_pair/`, `benchmarks/sg_compact/`, `benchmarks/bounded_compact/`, `benchmarks/capacity_sweep/`, `benchmarks/prethreshold/`, `benchmarks/hot_log_lut/`, `benchmarks/hot_log_control/`, `benchmarks/l2_boundary_hot/`, `benchmarks/cold_lineage_isolated/`, `benchmarks/l2_latency_isolated/`, `benchmarks/cuda_l2_clock_isolated/`, `benchmarks/cuda_l2_mlp_isolated/`, and `benchmarks/windows_physical_gpu_aggregate/`.

On Windows with Visual Studio Build Tools, run the device-local Vulkan path directly:

```powershell
& .\gpu\scripts\run_windows_vulkan_benchmarks.ps1
& .\gpu\scripts\run_windows_lut_benchmarks.ps1
& .\gpu\scripts\run_windows_lut_pair_benchmarks.ps1
& .\gpu\scripts\run_windows_compact_benchmarks.ps1
& .\gpu\scripts\run_windows_prethreshold_benchmarks.ps1
& .\gpu\scripts\run_windows_hot_log_lut_benchmarks.ps1
& .\gpu\scripts\run_windows_cold_lineage_benchmarks.ps1
& .\gpu\scripts\run_windows_l2_latency.ps1
& .\gpu\scripts\run_windows_cuda_l2_clock.ps1
```

The benchmark modules use the fixed reference query sheet=1, orientation=0, compatibility-mask bit=2; production modules should parameterize or version this convention.

The compact runner accepts `-CapacityRatio 0.0625` for a real one-slot-per-16-candidates output allocation. The GPU append counter records total demand, writes are bounded by the descriptor length, and overflow fails validation unless `-AllowOverflow` is explicitly selected for diagnostics.

The optional pre-threshold compact profile stores `min(guard_epsilon, -log2(confidence_floor)/32)` in the second guard half. It resolves the monotonic confidence predicate with a distance comparison and materializes confidence only for retained events. This changes the G32 field contract and therefore remains a separately named profile.

The G24 fixed-query hot profile goes further: it removes unused time/phase fields, replaces the dynamic compatibility mask with a producer-computed bit, and stores a 6-bit log-distance threshold code. Its direct decoder is the recommended variant on the measured RTX 5070 Ti Laptop GPU. The bundled 128-byte uniform-texel-buffer decoder validates the texture-cache form, but the balanced control shows that the large-case gain comes from the 24-byte state footprint, not the LUT. A four-process narrow sweep independently moves the counted-path cache cliff from the G32 allocation's 0.974-1.003x-L2 interval to the G24 allocation's 0.977-0.998x interval. A second four-process control reads identical packed log-code bytes through `texelFetch` and an SSBO: random-path ratios are 0.989x, 1.002x, 1.000x and 1.000x at 16, 32, 64 and 128 MiB, and both paths share the same 32-to-64 MiB cliff. The texture-buffer path therefore does not provide extra effective cache capacity on this device.

A native `VK_KHR_shader_clock` control plus 512-step dependent SSBO chase samples the L2 boundary in 2 MiB increments. Four isolated, balanced processes are flat through the exact 36 MiB reported capacity, rise 1.242x at 38 MiB and 2.134x at 40 MiB, and reach 4.714x at 64 MiB relative to 36 MiB. The raw unit is deliberately reported as implementation-defined shader-clock ticks under scheduler load, not invented GPU cycles or nanoseconds.

An independent CUDA 12.8 control compiles directly to `sm_120`, bypasses L1 with `ld.global.cg`, and reads the per-SM `clock64()` cycle counter. Four isolated runs measure a cross-size median of 399.57 cycles per immediate-hot dependent warp step and 1,087.79 cycles after a 256 MiB L2-eviction pass, a 2.722x penalty. Complete-kernel CUDA-event timing corresponds to approximately 153.4 ns and 401.8 ns per step. `cuobjdump` confirms `CS2R SR_CLOCKLO` and `LDG.E.STRONG.GPU`; `ptxas` reports 17 registers and zero spills. The metric still includes warp time slicing and up to 32 random sector requests per step, so it is not labelled scalar transaction latency.

A second native CUDA control scales independent one-warp blocks from one warp to 736 warps (16 per SM) while preserving each lane's 512-step dependency chain. Four balanced processes validate 42,883,200 payloads representing 14.64 billion loads. At maximum concurrency, hot requested throughput is 42.863 Gload/s for a 36 MiB table and 23.429 Gload/s at 40 MiB, a 45.34% boundary loss; 64 and 128 MiB reach only 9.318 and 7.506 Gload/s. This confirms that packed random-access state should remain below nominal L2 and quantifies the memory-queue/scheduler amplification behind the saturated cliff.

The G20 cold-lineage experiment retains the same 24-byte total state storage but splits it into a 20-byte geometry/meta hot stream plus a 4-byte lineage stream loaded only by verified lanes. Across six isolated balanced processes, at 4,194,304 candidates it measures 1.108x higher append throughput and 1.110x higher counted-path throughput than G24. Native NVIDIA compiler metadata reports identical register, shared-memory, and binary-size values for the two append kernels, strengthening the locality attribution. This is a measured locality improvement, not a claim of 20-byte total storage.

## Core execution path

```text
finite grammar / typed state
  -> radial-angular support
  -> compatibility
  -> relation guard
  -> verified event
  -> route / lineage / novelty log
```

## Source and engineering boundary

The source corpus is treated as a design record. Exact numeric, geometric and topological operators are retained; ambiguous motifs are translated into typed constructs; unsupported physical or totalizing claims are rejected or demoted. Standard `100%` remains 1. The addendum's `100100_2 = 36_10` is an explicitly versioned glyph encoder, not ordinary percentage arithmetic.
