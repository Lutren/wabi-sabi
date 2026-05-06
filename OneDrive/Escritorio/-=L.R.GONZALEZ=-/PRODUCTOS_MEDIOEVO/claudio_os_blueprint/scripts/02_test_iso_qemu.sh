#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISO="${ROOT}/live-build/live-image-amd64.hybrid.iso"

if [[ ! -f "${ISO}" ]]; then
  echo "ISO not found: ${ISO}" >&2
  exit 1
fi

qemu-system-x86_64 \
  -m 4096 \
  -smp 2 \
  -cdrom "${ISO}" \
  -boot d \
  -enable-kvm \
  -display gtk
