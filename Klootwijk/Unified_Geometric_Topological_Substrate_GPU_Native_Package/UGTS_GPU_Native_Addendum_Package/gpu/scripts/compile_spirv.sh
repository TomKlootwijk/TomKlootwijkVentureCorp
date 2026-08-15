#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/build/spirv}"
mkdir -p "$OUT"
: "${GLSLANG_VALIDATOR:=glslangValidator}"
for shader in "$ROOT"/shaders/vulkan/ugts_eval_*.comp; do
  stem="$(basename "$shader" .comp)"
  for counters in 0 1; do
    mode="evaluate"
    [[ "$counters" == 1 ]] && mode="evaluate_commit"
    target="$OUT/${stem}_${mode}.spv"
    "$GLSLANG_VALIDATOR" -V --target-env vulkan1.2 -DENABLE_COUNTERS="$counters" "$shader" -o "$target"
    if command -v spirv-opt >/dev/null 2>&1; then
      spirv-opt -O "$target" -o "$OUT/${stem}_${mode}.opt.spv"
    fi
    if command -v spirv-val >/dev/null 2>&1; then
      spirv-val --target-env vulkan1.2 "$target"
    fi
  done
done
LUT_SHADER="$ROOT/shaders/vulkan/ugts_log_lut_probe.comp"
if [[ -f "$LUT_SHADER" ]]; then
  for random_access in 0 1; do
    access="sequential"
    [[ "$random_access" == 1 ]] && access="random"
    target="$OUT/ugts_log_lut_${access}.spv"
    "$GLSLANG_VALIDATOR" -V --target-env vulkan1.2 -DRANDOM_ACCESS="$random_access" "$LUT_SHADER" -o "$target"
    if command -v spirv-opt >/dev/null 2>&1; then
      spirv-opt -O "$target" -o "$OUT/ugts_log_lut_${access}.opt.spv"
    fi
    if command -v spirv-val >/dev/null 2>&1; then
      spirv-val --target-env vulkan1.2 "$target"
    fi
  done
fi
"$ROOT/tools/inspect_spirv.py" "$OUT"/*.spv -o "$OUT/spirv_manifest.json"
echo "SPIR-V outputs written to $OUT"
