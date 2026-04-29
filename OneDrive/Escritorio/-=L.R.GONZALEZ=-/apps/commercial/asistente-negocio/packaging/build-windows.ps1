Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProductRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProductRoot
try {
  npm install
  npm run check
  npm run build:win
}
finally {
  Pop-Location
}
