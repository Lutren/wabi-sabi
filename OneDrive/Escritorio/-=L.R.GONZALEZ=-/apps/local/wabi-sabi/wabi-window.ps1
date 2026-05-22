param(
    [switch]$Here
)

$ErrorActionPreference = "Stop"
$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Here) {
    Set-Location -LiteralPath $AppDir
    $env:PYTHONPATH = "$AppDir;$env:PYTHONPATH"
    $PipedInput = @($input)
    if ($PipedInput.Count -gt 0) {
        $TextInput = ($PipedInput -join [Environment]::NewLine) + [Environment]::NewLine
        $TextInput | & python -m wabi_sabi.cli.main hablar --no-cloud
    } else {
        & python -m wabi_sabi.cli.main hablar --no-cloud
    }
    exit $LASTEXITCODE
}

$EscapedAppDir = $AppDir.Replace("'", "''")
$Command = "Set-Location -LiteralPath '$EscapedAppDir'; .\wabi.cmd hablar --no-cloud"

Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
    "-NoExit",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    $Command
)
