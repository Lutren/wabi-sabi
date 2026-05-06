#!/usr/bin/env python
"""Copywriter agent for conservative Mini Office copy."""

import json
from datetime import datetime
from pathlib import Path


class Copywriter:
    """Generate sales and product copy that matches current evidence."""

    def __init__(self):
        self.name = "Copywriter"
        self.specialty = "Persuasive Copy & Content"

    def write_copy(self, product_name="Mini Office", platform="landing"):
        """Write low-claim copy for a target platform."""
        return {
            "product": product_name,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "landing_page": {
                "headline": "Mini Office",
                "subheadline": "Agente Oficina local para revisar flujos y materiales.",
                "cta_primary": "Solicitar founder access",
                "cta_secondary": "Ver estado tecnico",
                "features": [
                    {"title": "Revision local", "desc": "Sirve la interfaz en localhost."},
                    {"title": "Roles claros", "desc": "Writer, Debugger, Research, QA y Archive."},
                    {"title": "Aprobacion humana", "desc": "Las publicaciones externas quedan fuera del runtime local."},
                    {"title": "Paquete comercial", "desc": "Licencia y entrega pendientes de cierre legal."},
                ],
                "social_proof": "Evidence-backed local QA in progress.",
                "urgency": "Founder access only after delivery gates.",
            },
            "social_media": {
                "short": "Mini Office: oficina local para revisar agentes, tareas y materiales antes de publicar.",
                "linkedin": (
                    "Mini Office esta en revision founder access: local-first, "
                    "con aprobacion humana y gates comerciales claros."
                ),
            },
            "email": {
                "subject": "Mini Office founder access",
                "preview": "Revision local de flujos y materiales de agentes",
                "body": (
                    "Mini Office es una app local para revisar roles, tareas y "
                    "materiales antes de publicar o entregar un producto."
                ),
            },
        }

    def generate_assets(self, output_path="reports/copywriting.json"):
        """Generate copy assets."""
        copy = self.write_copy()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(copy, f, indent=2)
        return copy


if __name__ == "__main__":
    writer = Copywriter()
    print(json.dumps(writer.generate_assets(), indent=2))
