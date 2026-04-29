#!/usr/bin/env python
"""
Copywriter Agent
================
redactor publicitario para copy persuasivo
"""

import json
from datetime import datetime

class Copywriter:
    """redactor publicitario automatizado"""

    def __init__(self):
        self.name = "Copywriter"
        self.specialty = "Persuasive Copy & Content"

    def write_copy(self, product_name="Mini Office", platform="landing"):
        """Escribe copy para plataforma"""
        copy = {
            "product": product_name,
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "landing_page": {
                "headline": "Tu Oficina Virtual que Trabaja 24/7",
                "subheadline": "Agentes AI autonomos con estilo pixel art",
                "cta_primary": "Comenzar Gratis",
                "cta_secondary": "Ver Demo",
                "features": [
                    {"title": "Auto-Investigacion", "desc": "Agentes que investigan mientras duermes"},
                    {"title": "Auto-Limpieza", "desc": "Organizacion automatica de proyectos"},
                    {"title": "Auto-Seguridad", "desc": "Monitoreo continuo 24/7"},
                    {"title": "Auto-Evolucion", "desc": "Mejora continua basada en performance"},
                ],
                "social_proof": "+1000 developers confian en Mini Office",
                "urgency": "Edicion limitada - Open Source",
            },
            "social_media": {
                "twitter": "Tu oficina virtual que trabaja 24/7? Ya existe. Se llama Mini Office. #AI #OpenSource",
                "linkedin": "Presentamos Mini Office: La primera oficina virtual con agentes AI autonomos y estetica pixel art.",
                "instagram": "Tu oficina nunca se veia tan pixelada. #MiniOffice #PixelArt #AI",
            },
            "email": {
                "subject": "Tu nueva oficina virtual esta aqui",
                "preview": "Agentes AI + Pixel Art = Productividad 24/7",
                "body": "Hola! Tu oficina virtual que trabaja 24/7 te esta esperando. Sin suscripciones. Sin complicaciones. Solo productividad pixelada."
            }
        }
        return copy

    def generate_assets(self, output_path="reports/copywriting.json"):
        """Genera assets de copy"""
        copy = self.write_copy()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(copy, f, indent=2)
        return copy

if __name__ == "__main__":
    writer = Copywriter()
    assets = writer.generate_assets()
    print(json.dumps(assets, indent=2))
