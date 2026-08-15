#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/build/spirv}"
mkdir -p "$OUT"
: "${GLSLANG_VALIDATOR:=glslangValidator}"
for shader in "$ROOT"/shaders/vulkan/*.comp; do
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
"$ROOT/tools/inspect_spirv.py" "$OUT"/*.spv -o "$OUT/spirv_manifest.json"
echo "SPIR-V outputs written to $OUT"
