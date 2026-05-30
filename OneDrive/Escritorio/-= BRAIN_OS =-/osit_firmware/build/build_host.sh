#!/usr/bin/env bash
# Reproducible host build + smoke for the OSIT firmware C layer.
#
# Compiles the UEFI C sources (no .asm, no EDK2) with the system C compiler and
# runs the three host tests:
#   t_vsa     - VSA bind/similarity + action_gate(phi>=0.60)        (tests/test_vsa_primitives.c)
#   t_regime  - canon regime ladder + estimate_R + ghost gate        (tests/test_regime.c)
#   t_handoff - handoff fingerprint, validates SHA3-256("") KAT       (tests/test_handoff.c)
#
# KAT: SHA3-256("") = a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
# (t_handoff checks the first four bytes a7 ff c6 f8 and fails BLOQUEADO otherwise).
#
# Runs anywhere a C11 compiler exists (Linux, WSL2, or MinGW on Windows). The asm
# kernels (asm/*.asm) and the UEFI/QEMU path are NOT exercised here; see build_uefi.sh
# and test_qemu.sh for that (Linux/WSL2 with EDK2 + OVMF + qemu-system-x86_64).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/out/host"
CC="${CC:-gcc}"
CFLAGS="${CFLAGS:--std=c11 -O2 -Wall -Wextra}"
SRC=("$ROOT/uefi/osit_gates.c" "$ROOT/uefi/osit_vsa.c" "$ROOT/uefi/osit_handoff.c")

echo "ESTADO: INFERENCIA"
if ! command -v "$CC" >/dev/null 2>&1; then
  echo "BLOQUEADO: C compiler '$CC' not found in PATH"
  echo "ACCIÓN: instala gcc/clang (Linux, WSL2 o MinGW) o exporta CC=<compilador>"
  exit 2
fi

EXE=""
case "$(uname -s 2>/dev/null || echo unknown)" in
  *MINGW*|*MSYS*|*CYGWIN*) EXE=".exe" ;;
esac

mkdir -p "$OUT"
echo "CERTEZA: $($CC --version | head -1)"

build_and_run() {
  local name="$1"; local test_src="$2"
  echo "---- $name ----"
  "$CC" $CFLAGS "$ROOT/tests/$test_src" "${SRC[@]}" -o "$OUT/$name$EXE"
  "$OUT/$name$EXE"
}

build_and_run t_vsa     test_vsa_primitives.c
build_and_run t_regime  test_regime.c
build_and_run t_handoff test_handoff.c

echo "CERTEZA: host smoke complete -> $OUT (t_vsa, t_regime, t_handoff)"
