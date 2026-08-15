[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path $PSScriptRoot '..\..\benchmarks\windows_physical_gpu_aggregate\environment.json'),
    [string]$CapabilityProbePath = (Join-Path $PSScriptRoot '..\..\benchmarks\native_capability_probe\vulkan_benchmark_results.json'),
    [string]$LatencyProbePath = (Join-Path $PSScriptRoot '..\..\benchmarks\l2_latency_isolated\aggregate\l2_latency_aggregate.json'),
    [string]$CudaClockProbePath = (Join-Path $PSScriptRoot '..\..\benchmarks\cuda_l2_clock_isolated\aggregate\cuda_l2_clock_aggregate.json')
)

$ErrorActionPreference = 'Stop'
$output = [System.IO.Path]::GetFullPath($OutputPath)
$parent = Split-Path -Parent $output
New-Item -ItemType Directory -Force -Path $parent | Out-Null

$torchJson = python -c @'
import json
import torch
p = torch.cuda.get_device_properties(0)
print(json.dumps({
    'torch_version': torch.__version__,
    'cuda_available': torch.cuda.is_available(),
    'name': p.name,
    'compute_capability': f'{p.major}.{p.minor}',
    'multiprocessor_count': p.multi_processor_count,
    'total_memory_bytes': p.total_memory,
    'l2_cache_bytes': p.L2_cache_size,
    'uuid': str(p.uuid),
}))
'@
if ($LASTEXITCODE -ne 0 -or -not $torchJson) {
    throw 'CUDA device-properties query failed.'
}
$cuda = $torchJson | ConvertFrom-Json
$capabilityProbe = $null
if (Test-Path -LiteralPath $CapabilityProbePath) {
    $capabilityProbe = Get-Content -Raw -LiteralPath $CapabilityProbePath | ConvertFrom-Json
}
$latencyProbe = $null
if (Test-Path -LiteralPath $LatencyProbePath) {
    $latencyProbe = Get-Content -Raw -LiteralPath $LatencyProbePath | ConvertFrom-Json
}
$cudaClockProbe = $null
if (Test-Path -LiteralPath $CudaClockProbePath) {
    $cudaClockProbe = Get-Content -Raw -LiteralPath $CudaClockProbePath | ConvertFrom-Json
}

$query = nvidia-smi --query-gpu=name,pci.bus_id,driver_version,memory.total,pstate,clocks.current.graphics,clocks.current.memory,power.draw,power.limit,temperature.gpu --format=csv,noheader,nounits
$gpuFields = $query -split ',\s*'
function Convert-GpuNumber([string]$Value) {
    $parsed = 0.0
    if ([double]::TryParse($Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$parsed)) {
        return $parsed
    }
    return $null
}
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$counterAccess = 'blocked: insufficient NVIDIA GPU performance-counter privilege'
if ($capabilityProbe -and -not $capabilityProbe.device.performance_query_extension_present) {
    $counterAccess += '; selected Vulkan device also does not expose VK_KHR_performance_query'
}

$document = [ordered]@{
    schema = 'UGTS-WINDOWS-GPU-ENVIRONMENT-1.4'
    captured_utc = [DateTime]::UtcNow.ToString('o')
    os = [ordered]@{
        caption = $os.Caption
        version = $os.Version
        build_number = $os.BuildNumber
    }
    cpu = [ordered]@{
        name = $cpu.Name.Trim()
        physical_cores = $cpu.NumberOfCores
        logical_processors = $cpu.NumberOfLogicalProcessors
    }
    gpu = [ordered]@{
        name = $gpuFields[0]
        pci_bus_id = $gpuFields[1]
        driver_version = $gpuFields[2]
        memory_total_mib = [int](Convert-GpuNumber $gpuFields[3])
        observed_pstate = $gpuFields[4]
        observed_graphics_clock_mhz = [int](Convert-GpuNumber $gpuFields[5])
        observed_memory_clock_mhz = [int](Convert-GpuNumber $gpuFields[6])
        observed_power_w = Convert-GpuNumber $gpuFields[7]
        power_limit_w = Convert-GpuNumber $gpuFields[8]
        observed_temperature_c = [int](Convert-GpuNumber $gpuFields[9])
        cuda = $cuda
        vulkan_api = '1.4.325'
        vulkan_device_type = 'discrete'
        vulkan_vendor_id = 4318
        vulkan_device_id = 12056
        vulkan_timestamp_period_ns = 1.0
        vulkan_timestamp_valid_bits = 64
        vulkan_pipeline_executable_properties = if ($capabilityProbe) { [bool]$capabilityProbe.device.pipeline_executable_capture } else { $null }
        vulkan_performance_query = if ($capabilityProbe) { [bool]$capabilityProbe.device.performance_query_extension_present } else { $null }
        vulkan_capability_probe = if ($capabilityProbe) { [System.IO.Path]::GetFullPath($CapabilityProbePath) } else { $null }
        vulkan_shader_clock = [ordered]@{
            extension = 'VK_KHR_shader_clock'
            device_clock_enabled = if ($latencyProbe) { [bool]$latencyProbe.device.shader_device_clock } else { $null }
            source = if ($latencyProbe) { [System.IO.Path]::GetFullPath($LatencyProbePath) } else { $null }
        }
        vulkan_subgroup = [ordered]@{
            size = 32
            min_size = 32
            max_size = 32
            compute_stage_supported = $true
            basic_supported = $true
            ballot_supported = $true
            source = 'local vulkaninfo device-properties query'
        }
        cuda_l2_clock_probe = [ordered]@{
            enabled = if ($cudaClockProbe) { [bool]$cudaClockProbe.validation.all_rows_valid } else { $null }
            target = 'sm_120'
            compiler = 'CUDA 12.8.61'
            load_instruction = 'LDG.E.STRONG.GPU generated from ld.global.cg.u32'
            source = if ($cudaClockProbe) { [System.IO.Path]::GetFullPath($CudaClockProbePath) } else { $null }
        }
    }
    execution = [ordered]@{
        driver_model = 'WDDM'
        storage_memory = 'VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT'
        transfer_memory = 'VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT'
        gpu_timestamp_scope = 'compute dispatch only'
        performance_counter_access = $counterAccess
        pipeline_executable_metadata = if ($capabilityProbe -and $capabilityProbe.device.pipeline_executable_capture) { 'available through VK_KHR_pipeline_executable_properties' } else { 'not captured' }
        shader_clock_scope = if ($latencyProbe) { 'device-scope realtime clock; implementation-defined units' } else { 'not captured' }
        cuda_clock_scope = if ($cudaClockProbe) { 'per-SM clock64 cycle counter; elapsed thread time includes time slicing' } else { 'not captured' }
    }
}

$document | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $output -Encoding utf8
Write-Output $output
