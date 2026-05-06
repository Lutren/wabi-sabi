#!/usr/bin/env python
"""Creative director agent for Mini Office."""

import json
from datetime import datetime
from pathlib import Path


class CreativeDirector:
    """Generate product-safe creative direction."""

    def __init__(self):
        self.name = "Creative Director"
        self.specialty = "Visual Concepts & Narrative"

    def develop_concept(self, product_name="Mini Office", theme="medioevo-office"):
        """Return a conservative creative brief."""
        return {
            "product": product_name,
            "theme": theme,
            "timestamp": datetime.now().isoformat(),
            "visual_identity": {
                "colors": {
                    "primary": "#2eccc7",
                    "secondary": "#d98f2b",
                    "accent": "#59cf91",
                    "background": "#0b0b0f",
                },
                "typography": {
                    "display": "Segoe UI, system-ui",
                    "body": "Segoe UI, system-ui",
                },
                "style_keywords": [
                    "local workstation",
                    "pixel-like office grid",
                    "medioevo industrial",
                    "human approval",
                ],
            },
            "narrative": {
                "hook": "Una mini oficina local para revisar flujos antes de publicar.",
                "story": (
                    "Mini Office convierte roles, materiales y tareas en una vista "
                    "local que el operador puede revisar antes de entregar."
                ),
                "taglines": [
                    "Revision local. Entrega mas clara.",
                    "Tu oficina de agentes, con aprobacion humana.",
                    "Ordena, revisa y empaqueta.",
                ],
            },
            "moodboard": [
                "control room",
                "compact office board",
                "MEDIOEVO workshop",
            ],
        }

    def generate_brief(self, output_path="reports/creative_brief.json"):
        """Generate a creative brief."""
        concept = self.develop_concept()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(concept, f, indent=2)
        return concept


if __name__ == "__main__":
    director = CreativeDirector()
    print(json.dumps(director.generate_brief(), indent=2))
