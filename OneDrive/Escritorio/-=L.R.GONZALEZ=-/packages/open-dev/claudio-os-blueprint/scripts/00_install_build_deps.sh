#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  live-build \
  qemu-system-x86 \
  xorriso \
  squashfs-tools \
  python3 \
  python3-yaml \
  curl \
  jq

echo "Build dependencies installed."

