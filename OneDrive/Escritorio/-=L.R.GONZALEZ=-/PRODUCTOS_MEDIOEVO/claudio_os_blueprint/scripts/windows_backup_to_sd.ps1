param(
  [Parameter(Mandatory=$true)][string]$Destination
)

$source = "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$target = Join-Path $Destination "claudio_backup_$stamp"

New-Item -ItemType Directory -Force -Path $target | Out-Null
robocopy $source $target /MIR /XD "__pycache__" ".pytest_cache" ".venv" "node_modules" /XF "*.tmp" "*.log"

Write-Host "Backup completed: $target"
