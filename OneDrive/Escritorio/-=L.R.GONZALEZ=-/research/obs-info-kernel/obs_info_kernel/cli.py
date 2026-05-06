from __future__ import annotations

import argparse
from pathlib import Path

from .orchestrator import ObservacionismoResearchKernel


def main() -> None:
    parser = argparse.ArgumentParser(description="Kernel Observacionista: anti-informacion + informacion oscura")
    parser.add_argument("--corpus", required=True, help="Directorio con .md/.txt/.json")
    parser.add_argument("--query", required=True, help="Tema o pregunta de investigacion")
    parser.add_argument("--out-dir", default="obs_out", help="Directorio de salida")
    parser.add_argument("--min-coverage", type=float, default=0.55, help="Cobertura minima para nucleo calibrado")
    args = parser.parse_args()

    kernel = ObservacionismoResearchKernel(out_dir=args.out_dir)
    sources = kernel.load_sources_from_dir(args.corpus)
    report = kernel.analyze(args.query, sources, min_coverage=args.min_coverage)

    print("=== OBSERVACIONISMO RESEARCH KERNEL ===")
    print(f"Fuentes: {len(sources)}")
    psi = report["estado_psi"]
    print(f"R={psi['R']} Phi_eff={psi['Phi_eff']} Regimen={psi['regimen']}")
    print(f"Reporte MD: {report['artifacts']['markdown_report']}")
    print(f"Reporte JSON: {report['artifacts']['json_report']}")
    print(f"Fingerprint: {report['artifacts']['fingerprint']}")


if __name__ == "__main__":
    main()
