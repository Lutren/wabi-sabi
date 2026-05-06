#!/usr/bin/env python
"""Generate website copy for Mini Office without unsupported claims."""

import json
from pathlib import Path


def generar_contenido_web():
    """Generate website content that matches current QA status."""
    return {
        "meta": {
            "title": "Mini Office | MEDIOEVO",
            "description": (
                "App local para revisar flujos, materiales y roles de agentes "
                "con aprobacion humana."
            ),
            "keywords": "mini office, local-first, ai agents, medioevo, founder access",
            "author": "MEDIOEVO",
            "canonical": "https://medioevo.space/software.html",
        },
        "hero": {
            "eyebrow": "Founder access review",
            "title": "Mini Office",
            "tagline": "Agente Oficina local",
            "description": (
                "Interfaz local para revisar tareas, materiales y roles antes "
                "de publicar o entregar productos."
            ),
            "cta_primary": "Solicitar acceso",
            "cta_secondary": "Ver ficha tecnica",
            "highlights": [
                {"title": "Revision local", "desc": "Corre en localhost."},
                {"title": "Roles claros", "desc": "Writer, Debugger, Research, QA y Archive."},
                {"title": "Aprobacion humana", "desc": "Sin acciones externas desde esta vista."},
                {"title": "Gates comerciales", "desc": "Licencia y paquete final pendientes."},
            ],
        },
        "metrics": [
            {"value": "Local", "label": "runtime"},
            {"value": "5", "label": "roles"},
            {"value": "Manual", "label": "approval"},
            {"value": "QA", "label": "status"},
        ],
        "features": [
            {
                "title": "Local runner",
                "description": "mini_office.py sirve index.html en 127.0.0.1.",
            },
            {
                "title": "Customer boundary",
                "description": "Venta externa bloqueada hasta legal, soporte y paquete final.",
            },
            {
                "title": "MEDIOEVO visual system",
                "description": "Lenguaje visual industrial con cobre, turquesa y paneles oscuros.",
            },
        ],
        "faq": [
            {
                "question": "Esta listo para venta publica?",
                "answer": "No. Esta en founder access review hasta cerrar los gates.",
            },
            {
                "question": "Funciona sin servicios externos?",
                "answer": "La ruta de smoke local sirve una app estatica en localhost.",
            },
        ],
    }


def generar_schema_json_ld():
    """Generate conservative JSON-LD for SEO drafts."""
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Mini Office",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Windows, Linux, macOS",
        "description": "App local para revisar tareas y roles de agentes.",
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/PreOrder",
            "priceCurrency": "USD",
        },
    }


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)
    payload = {
        "web": generar_contenido_web(),
        "schema": generar_schema_json_ld(),
    }
    with open(output_dir / "web_content.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Contenido guardado en: {output_dir / 'web_content.json'}")
