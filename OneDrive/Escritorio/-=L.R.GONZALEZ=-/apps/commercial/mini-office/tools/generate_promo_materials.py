#!/usr/bin/env python
"""Generate Mini Office promo materials from product-safe agents."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.analyst import MarketAnalyst
from agents.creative import CreativeDirector
from agents.copywriter import Copywriter
from agents.designer import Designer


def generate_all_promo_materials():
    """Generate all review materials into reports/."""
    output_dir = Path(__file__).parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)

    materials = {
        "market": MarketAnalyst().analyze(),
        "creative": CreativeDirector().develop_concept(),
        "copy": Copywriter().write_copy(),
        "design": Designer().create_design_system(),
    }

    targets = {
        "market": "market_analysis.json",
        "creative": "creative_brief.json",
        "copy": "copy_assets.json",
        "design": "design_system.json",
    }
    for key, filename in targets.items():
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(materials[key], f, indent=2, ensure_ascii=False)

    return materials


def generate_social_media_posts():
    """Generate low-claim social drafts."""
    return {
        "short": [
            "Mini Office organiza roles, tareas y materiales en una app local.",
            "Founder access review: local-first, aprobacion humana y gates comerciales claros.",
        ],
        "linkedin": [
            "Mini Office es una oficina local para revisar flujos de agentes antes de publicar o entregar productos."
        ],
    }


def generate_gumroad_description():
    """Generate a draft Gumroad description for review."""
    return """# Mini Office

App local para revisar flujos, materiales y roles de agentes antes de publicar
o entregar un producto.

Estado: FOUNDER_ACCESS_REVIEW.

No activar checkout publico hasta cerrar licencia, soporte, privacidad,
reembolsos, clean-machine QA, manifest y hash de entrega.
"""


def generate_readme_short():
    """Generate a short README draft."""
    return """# Mini Office

Mini Office es una app local para revisar tareas, materiales y roles de agentes.

```bash
python mini_office.py --status
python mini_office.py --no-browser
```

Ver `COMMERCIAL_LICENSE.md` antes de cualquier entrega externa.
"""


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)

    materials = generate_all_promo_materials()
    with open(output_dir / "social_media_posts.json", "w", encoding="utf-8") as f:
        json.dump(generate_social_media_posts(), f, indent=2, ensure_ascii=False)
    with open(output_dir / "gumroad_description.txt", "w", encoding="utf-8") as f:
        f.write(generate_gumroad_description())
    with open(output_dir / "README_SHORT.md", "w", encoding="utf-8") as f:
        f.write(generate_readme_short())

    print(json.dumps({"generated": sorted(materials.keys())}, indent=2))
