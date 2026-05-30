# OSIT firmware — build & smoke

Rutas de build, de menor a mayor requisito de entorno. Calibración: **DEMO_ONLY**.
Ninguna toca el BIOS/UEFI físico de la placa — todo es reproducible y reversible.

## 1. Capa host C (corre en cualquier sitio con gcc/clang) — `build_host.sh`

```bash
bash build/build_host.sh           # usa gcc por defecto; CC=clang u otro para cambiar
```

Compila las fuentes C de `uefi/*.c` (sin `.asm`, sin EDK2) y corre tres smokes:

| binario | test | qué valida |
|---|---|---|
| `t_vsa` | `tests/test_vsa_primitives.c` | bind/similarity VSA + `action_gate(phi>=0.60)` |
| `t_regime` | `tests/test_regime.c` | escalera canónica `osit_regime_from_R` + `estimate_R` + ghost gate |
| `t_handoff` | `tests/test_handoff.c` | huella de handoff + **KAT SHA3-256("") = `a7ffc6f8…`** |

Salida en `out/host/`. **Verificado 2026-05-29** (MinGW-W64 gcc 15.1.0, Windows): los tres pasan
`CERTEZA`. Es la única capa que corre en esta máquina Windows.

## 2. Aplicación UEFI X64 (requiere EDK2) — `build_uefi.sh`

```bash
source edksetup.sh            # define WORKSPACE y el comando `build`
export WORKSPACE=/ruta/edk2
bash build/build_uefi.sh      # produce out/uefi/OsitKernel.efi
```

Toolchain exacto: **EDK2** (MdePkg) + **GCC5** + arquitectura **X64**, `BUILD_TARGETS=DEBUG`.
No hay red; el `.dsc` se genera localmente. Esta máquina Windows **no** tiene EDK2 → correr en
**Linux o WSL2**.

## 3. Smoke en QEMU/OVMF (requiere qemu + OVMF) — `test_qemu.sh`

```bash
OVMF_CODE=/usr/share/OVMF/OVMF_CODE.fd bash build/test_qemu.sh out/uefi/OsitKernel.efi
```

Toolchain exacto: **qemu-system-x86_64** + firmware **OVMF** (`OVMF_CODE.fd`). Copia el `.efi`
a un ESP FAT (`out/qemu/esp/EFI/BOOT/BOOTX64.EFI`) y lo arranca con `-serial stdio`, `-net none`,
`-display none` (VM aislada, sin red). Esta máquina Windows **no** tiene qemu/OVMF → correr en
**Linux o WSL2**.

## Otros scripts
- `build_asm.sh` / `build_mcu.sh`: ensamblan los kernels AVX2 (`asm/*.asm`) y compilan la capa MCU
  edge (`mcu/*.c`). Las funciones AVX2 tienen equivalente en C en `uefi/*.c`, que es lo que usa la
  capa host (1).

## Límite de seguridad
No se reflashea el firmware/BIOS físico (irreversible, requiere herramientas del fabricante +
acceso físico). El intent "desde el arranque" se honra de forma segura con: (a) esta capa host +
sandbox UEFI/QEMU y (b) el servicio OSIT al inicio de Windows (`tools/osit_boot/`, árbol L.R.GONZALEZ).
