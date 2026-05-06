param(
    [switch]$Apply,
    [switch]$Machine,
    [switch]$RestartOllama
)

$ErrorActionPreference = "Stop"

function Show-Port {
    param([int]$Port)

    $rows = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object LocalAddress, LocalPort, OwningProcess
    if ($rows) {
        $rows | Format-Table -AutoSize
    } else {
        Write-Output "No listener on port $Port"
    }
}

Write-Output "Loopback audit"
Write-Output "User OLLAMA_HOST:    $([Environment]::GetEnvironmentVariable('OLLAMA_HOST','User'))"
Write-Output "Machine OLLAMA_HOST: $([Environment]::GetEnvironmentVariable('OLLAMA_HOST','Machine'))"
Write-Output ""

Write-Output "Claudio API listener:"
Show-Port -Port 47047
Write-Output ""

Write-Output "Ollama listener:"
Show-Port -Port 11434
Write-Output ""

if (-not $Apply) {
    Write-Output "Dry run only. Use -Apply to set User OLLAMA_HOST to 127.0.0.1:11434."
    Write-Output "Use -Apply -Machine from an elevated PowerShell to correct Machine OLLAMA_HOST."
    Write-Output "Use -Apply -RestartOllama only after confirming active jobs can pause."
    exit 0
}

[Environment]::SetEnvironmentVariable('OLLAMA_HOST', '127.0.0.1:11434', 'User')
Write-Output "Set User OLLAMA_HOST to 127.0.0.1:11434"

if ($Machine) {
    try {
        [Environment]::SetEnvironmentVariable('OLLAMA_HOST', '127.0.0.1:11434', 'Machine')
        Write-Output "Set Machine OLLAMA_HOST to 127.0.0.1:11434"
    } catch {
        Write-Output "Could not set Machine OLLAMA_HOST. Run elevated if machine-level value is 0.0.0.0."
        Write-Output $_.Exception.Message
    }
}

if ($RestartOllama) {
    $ollama = Get-Process -Name ollama -ErrorAction SilentlyContinue
    if ($ollama) {
        Write-Output "Stopping Ollama so the new bind address can apply."
        $ollama | Stop-Process
    }
    $path = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
    if (Test-Path $path) {
        Write-Output "Starting Ollama hidden."
        Start-Process -FilePath $path -ArgumentList "serve" -WindowStyle Hidden
    } else {
        Write-Output "Ollama executable not found at expected path: $path"
    }
}
