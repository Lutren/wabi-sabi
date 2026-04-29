#!/usr/bin/env python
"""
Designer Agent
==============
Diseñador UX/UI para interfaces pixel art
"""

import json
from datetime import datetime

class Designer:
    """Diseñador UX/UI automatizado"""

    def __init__(self):
        self.name = "Designer"
        self.specialty = "Pixel Art UI/UX Design"

    def create_design_system(self, product_name="Mini Office"):
        """Crea sistema de diseño"""
        design = {
            "product": product_name,
            "timestamp": datetime.now().isoformat(),
            "colors": {
                "background": {"primary": "#081018", "secondary": "#101820", "tertiary": "#182030"},
                "foreground": {"primary": "#37d3d0", "secondary": "#e2a760", "accent": "#59cf91"},
                "status": {"success": "#59cf91", "warning": "#f0c27b", "error": "#ff6a66"},
            },
            "typography": {
                "font_main": "Courier New, monospace",
                "font_display": "Consolas, monospace",
                "sizes": {"xs": "12px", "sm": "14px", "md": "16px", "lg": "24px", "xl": "32px"}
            },
            "components": {
                "button": {
                    "padding": "12px 24px",
                    "border_radius": "0",  # Pixelado = sin border-radius
                    "border_width": "4px",
                    "hover_effect": "transform: scale(1.05)",
                },
                "card": {
                    "padding": "20px",
                    "border_width": "2px",
                    "shadow": "0 0 15px rgba(55, 211, 208, 0.3)",
                },
                "agent": {
                    "size": "80x80",
                    "animation": "pulse 2s infinite",
                }
            },
            "animations": {
                "pulse": "keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }",
                "scanline": "keyframes scanline { 0% { transform: translateY(0); } 100% { transform: translateY(1080px); } }",
            },
            "assets": {
                "icons": ["agent", "department", "metric", "status"],
                "sprites": ["idle", "working", "success", "error"],
            }
        }
        return design

    def generate_system(self, output_path="reports/design_system.json"):
        """Genera sistema de diseño"""
        design = self.create_design_system()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(design, f, indent=2)
        return design

if __name__ == "__main__":
    designer = Designer()
    system = designer.generate_system()
    print(json.dumps(system, indent=2))
