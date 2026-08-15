[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\..\benchmarks\cuda_vmm_compression_lut_smoke'),
    [string]$SizeMiB = '4,28,32,36,38,40,48,64,96,128',
    [string]$Warps = '184,1104',
    [string]$Patterns = 'zero6,periodic6,entropy6',
    [string]$Paths = 'global_cg,texture_object',
    [int]$EvictionMiB = 256,
    [int]$Warmup = 2,
    [int]$Samples = 10,
    [ValidateSet(0, 1)]
    [int]$Order = 0,
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'
$gpuRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ($SkipBuild) {
    $executable = Join-Path $gpuRoot 'build-windows\ugts_cuda_vmm_compression_lut_bench.exe'
} else {
    $buildOutput = & (Join-Path $PSScriptRoot 'build_windows_cuda_vmm_compression_lut.ps1')
    if ($LASTEXITCODE -ne 0) { throw "Build failed with exit code $LASTEXITCODE" }
    $executable = $buildOutput | Select-Object -Last 1
}
if (-not (Test-Path -LiteralPath $executable)) {
    throw "CUDA VMM compression-LUT benchmark executable not found: $executable"
}
$outputPath = [System.IO.Path]::GetFullPath($OutputDirectory)
& $executable --out-dir $outputPath --size-mib $SizeMiB --warps $Warps --patterns $Patterns `
    --paths $Paths --eviction-mib $EvictionMiB --warmup $Warmup --samples $Samples --order $Order
if ($LASTEXITCODE -ne 0) {
    throw "CUDA VMM compression-LUT benchmark failed with exit code $LASTEXITCODE"
}
