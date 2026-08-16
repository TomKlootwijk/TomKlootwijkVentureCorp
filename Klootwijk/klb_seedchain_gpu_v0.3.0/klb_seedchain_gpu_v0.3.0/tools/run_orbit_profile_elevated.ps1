$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location -LiteralPath $Root

$Log = Join-Path $Root "profile_orbit_elevated_console.txt"
$ExitFile = Join-Path $Root "profile_orbit_elevated_exit_code.txt"

& powershell -ExecutionPolicy Bypass -File .\scripts\profile_orbit_windows.ps1 `
    -BuildDir build-cuda128-vs -Configuration Release 2>&1 |
    Tee-Object -FilePath $Log

$Code = $LASTEXITCODE
Set-Content -LiteralPath $ExitFile -Value $Code -Encoding ASCII
Write-Host "ELEVATED_PROFILE_EXIT_CODE=$Code"
exit $Code
