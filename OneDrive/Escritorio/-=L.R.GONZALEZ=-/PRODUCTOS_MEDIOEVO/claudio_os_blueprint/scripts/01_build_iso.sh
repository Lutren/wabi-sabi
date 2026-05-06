#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}/live-build"

lb clean || true
lb config
sudo lb build

echo "ISO should be under ${ROOT}/live-build/live-image-amd64.hybrid.iso"
