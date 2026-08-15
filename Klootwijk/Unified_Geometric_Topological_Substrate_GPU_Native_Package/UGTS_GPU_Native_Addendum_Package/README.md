# UGTS-GN 1.1 - GPU-Native Geometric-Topological Substrate Addendum

This package is the GPU-native and physical-device revision of the unified substrate. It removes Unity/Godot adapters and makes the authoritative target a direct Vulkan/SPIR-V compute path or a measured hardware device.

## What is included

- `report/`: complete synthesis report and report source.
- `spec/`: 197-mechanism knowledge catalog, typed schema, ABI/state layout, metric definitions and claims ledger.
- `gpu/`: ten Vulkan compute-shader sources, twenty-two named execution variants plus twenty-two optimized SPIR-V counterparts, direct Vulkan runtime, cache artifacts and scripts.
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

The original portable baseline in `benchmarks/vulkan_native_run/` selected SwiftShader, a CPU/software Vulkan device. A local Windows physical-GPU validation is now recorded in [`benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md`](benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md), with a human-readable [`yield, compression and limits report`](benchmarks/YIELD_COMPRESSION_LIMITS_RTX_5070_TI_LAPTOP.md). Raw and aggregate data is under `benchmarks/windows_native_run/`, `benchmarks/windows_integrated_lut_run/`, `benchmarks/windows_lut_cache_run/`, `benchmarks/lut_pair/`, `benchmarks/sg_compact/`, `benchmarks/bounded_compact/`, `benchmarks/capacity_sweep/`, `benchmarks/prethreshold/`, `benchmarks/hot_log_lut/`, `benchmarks/hot_log_control/`, `benchmarks/l2_boundary_hot/`, `benchmarks/cold_lineage_hot/`, and `benchmarks/windows_physical_gpu_aggregate/`.

On Windows with Visual Studio Build Tools, run the device-local Vulkan path directly:

```powershell
& .\gpu\scripts\run_windows_vulkan_benchmarks.ps1
& .\gpu\scripts\run_windows_lut_benchmarks.ps1
& .\gpu\scripts\run_windows_lut_pair_benchmarks.ps1
& .\gpu\scripts\run_windows_compact_benchmarks.ps1
& .\gpu\scripts\run_windows_prethreshold_benchmarks.ps1
& .\gpu\scripts\run_windows_hot_log_lut_benchmarks.ps1
& .\gpu\scripts\run_windows_cold_lineage_benchmarks.ps1
```

The benchmark modules use the fixed reference query sheet=1, orientation=0, compatibility-mask bit=2; production modules should parameterize or version this convention.

The compact runner accepts `-CapacityRatio 0.0625` for a real one-slot-per-16-candidates output allocation. The GPU append counter records total demand, writes are bounded by the descriptor length, and overflow fails validation unless `-AllowOverflow` is explicitly selected for diagnostics.

The optional pre-threshold compact profile stores `min(guard_epsilon, -log2(confidence_floor)/32)` in the second guard half. It resolves the monotonic confidence predicate with a distance comparison and materializes confidence only for retained events. This changes the G32 field contract and therefore remains a separately named profile.

The G24 fixed-query hot profile goes further: it removes unused time/phase fields, replaces the dynamic compatibility mask with a producer-computed bit, and stores a 6-bit log-distance threshold code. Its direct decoder is the recommended variant on the measured RTX 5070 Ti Laptop GPU. The bundled 128-byte uniform-texel-buffer decoder validates the texture-cache form, but the balanced control shows that the large-case gain comes from the 24-byte state footprint, not the LUT. A four-process narrow sweep independently moves the counted-path cache cliff from the G32 allocation's 0.974-1.003x-L2 interval to the G24 allocation's 0.977-0.998x interval.

The G20 cold-lineage experiment retains the same 24-byte total state storage but splits it into a 20-byte geometry/meta hot stream plus a 4-byte lineage stream loaded only by verified lanes. At 4,194,304 candidates it measures 1.097x higher append throughput and 1.102x higher counted-path throughput than G24. This is a measured locality improvement, not a claim of 20-byte total storage.

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
