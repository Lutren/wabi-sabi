#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
npm install
npm run check
npm run build:mac
