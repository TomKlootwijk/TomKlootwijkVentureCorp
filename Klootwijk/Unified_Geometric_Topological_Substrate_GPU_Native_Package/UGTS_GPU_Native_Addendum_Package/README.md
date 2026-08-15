# UGTS-GN 1.1 - GPU-Native Geometric-Topological Substrate Addendum

This package is the GPU-native and physical-device revision of the unified substrate. It removes Unity/Godot adapters and makes the authoritative target a direct Vulkan/SPIR-V compute path or a measured hardware device.

## What is included

- `report/`: complete synthesis report and report source.
- `spec/`: 197-mechanism knowledge catalog, typed schema, ABI/state layout, metric definitions and claims ledger.
- `gpu/`: four Vulkan compute shaders, compiled SPIR-V modules, direct Vulkan runtime, bootstrap compiler, cache artifacts and scripts.
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

The original portable baseline in `benchmarks/vulkan_native_run/` selected SwiftShader, a CPU/software Vulkan device. A local Windows physical-GPU validation is now recorded in [`benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md`](benchmarks/PHYSICAL_GPU_REPORT_RTX_5070_TI_LAPTOP.md), with raw and aggregate data under `benchmarks/windows_native_run/`, `benchmarks/windows_lut_cache_run/`, and `benchmarks/windows_physical_gpu_aggregate/`.

On Windows with Visual Studio Build Tools, run the device-local Vulkan path directly:

```powershell
& .\gpu\scripts\run_windows_vulkan_benchmarks.ps1
& .\gpu\scripts\run_windows_lut_benchmarks.ps1
```

The benchmark modules use the fixed reference query sheet=1, orientation=0, compatibility-mask bit=2; production modules should parameterize or version this convention.

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
