#!/usr/bin/env python
"""Generate Gumroad draft copy for Mini Office founder access."""

import json
from pathlib import Path


def generar_contenido_gumroad():
    """Generate draft Gumroad content without activating checkout claims."""
    return {
        "titulo": "Mini Office",
        "descripcion_corta": "Agente Oficina local para revisar flujos y materiales.",
        "precio": "TBD",
        "categoria": "Software",
        "tags": ["local-first", "agent-workspace", "productivity", "python", "medioevo"],
        "estado": "FOUNDER_ACCESS_REVIEW",
        "descripcion_completa": """
# Mini Office

Mini Office es una app local para revisar tareas, materiales y roles de agentes
antes de publicar o entregar un producto.

## Incluye

- Local runner con `mini_office.py`.
- Interfaz en `http://127.0.0.1:8000`.
- Roles Writer, Debugger, Research, QA y Archive.
- Scripts de instalacion para Windows, Linux y macOS.
- Documentacion y licencia comercial pendiente de revision legal.

## Gate actual

No activar checkout publico hasta cerrar: licencia, soporte, privacidad,
reembolsos, clean-machine QA, manifest y hash de entrega.
""",
        "instrucciones": """
## Windows
Ejecuta `INSTALL_AND_RUN.bat`.

## Linux o macOS
Ejecuta `chmod +x install_and_run.sh` y luego `./install_and_run.sh`.

## Manual
Ejecuta `python mini_office.py --no-browser` y abre
`http://127.0.0.1:8000`.
""",
    }


def generar_posts_redes():
    """Generate low-claim social drafts."""
    return {
        "short": [
            "Mini Office esta en founder access review: oficina local para revisar flujos de agentes antes de publicar.",
            "Local-first, aprobacion humana y paquete comercial con gates claros: ese es el enfoque de Mini Office.",
        ],
        "linkedin": [
            {
                "titulo": "Mini Office: revision local para flujos de agentes",
                "cuerpo": (
                    "Mini Office organiza roles, tareas y materiales en una "
                    "interfaz local. La venta publica queda bloqueada hasta "
                    "cerrar licencia, soporte, privacy, refund y clean-machine QA."
                ),
            }
        ],
    }


def generar_email_marketing():
    """Generate low-claim email draft."""
    return {
        "founder_access": {
            "asunto": "Mini Office founder access",
            "preview": "Revision local de flujos y materiales de agentes",
            "cuerpo": (
                "Mini Office esta en revision founder access. Es una app local "
                "para revisar roles, tareas y materiales antes de publicar o "
                "entregar un producto."
            ),
        }
    }


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)
    payload = {
        "gumroad": generar_contenido_gumroad(),
        "social_posts": generar_posts_redes(),
        "emails": generar_email_marketing(),
    }
    with open(output_dir / "gumroad_content.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Contenido guardado en: {output_dir / 'gumroad_content.json'}")
