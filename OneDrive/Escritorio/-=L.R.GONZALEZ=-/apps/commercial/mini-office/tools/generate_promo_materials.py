#!/usr/bin/env python
"""
Mini Office - Generador de Materiales Publicitarios
===================================================
Genera todo el contenido publicitario para marketing
"""

import json
from pathlib import Path
from datetime import datetime

# Importar agentes
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.analyst import MarketAnalyst
from agents.creative import CreativeDirector
from agents.copywriter import Copywriter
from agents.designer import Designer


def generate_all_promo_materials():
    """Genera todos los materiales publicitarios"""

    print("\n" + "="*60)
    print("MINI OFFICE - GENERADOR DE MATERIALES PUBLICITARIOS")
    print("="*60)

    # 1. Análisis de mercado
    print("\n[1/4] Ejecutando Market Analyst...")
    analyst = MarketAnalyst()
    market_analysis = analyst.analyze()

    # 2. Concepto creativo
    print("[2/4] Ejecutando Creative Director...")
    creative = CreativeDirector()
    creative_concept = creative.develop_concept()

    # 3. Copywriting
    print("[3/4] Ejecutando Copywriter...")
    copywriter = Copywriter()
    copy_assets = copywriter.write_copy()

    # 4. Diseño
    print("[4/4] Ejecutando Designer...")
    designer = Designer()
    design_system = designer.create_design_system()

    # Guardar resultados
    output_dir = Path(__file__).parent.parent / 'reports'
    output_dir.mkdir(exist_ok=True)

    # Market Analysis report
    with open(output_dir / 'market_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(market_analysis, f, indent=2, ensure_ascii=False)

    # Creative Brief
    with open(output_dir / 'creative_brief.json', 'w', encoding='utf-8') as f:
        json.dump(creative_concept, f, indent=2, ensure_ascii=False)

    # Copy Assets
    with open(output_dir / 'copy_assets.json', 'w', encoding='utf-8') as f:
        json.dump(copy_assets, f, indent=2, ensure_ascii=False)

    # Design System
    with open(output_dir / 'design_system.json', 'w', encoding='utf-8') as f:
        json.dump(design_system, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print("MATERIALES GENERADOS EXITOSAMENTE")
    print("="*60)
    print(f"\nArchitú guardados en: {output_dir}")
    print("  - market_analysis.json")
    print("  - creative_brief.json")
    print("  - copy_assets.json")
    print("  - design_system.json")

    return {
        'market': market_analysis,
        'creative': creative_concept,
        'copy': copy_assets,
        'design': design_system
    }


def generate_social_media_posts():
    """Genera posts para redes sociales"""

    posts = {
        'twitter': [
            "Tu oficina virtual que trabaja 24/7? Ya existe. Se llama Mini Office. #AI #OpenSource #Conway247",
            "Agentes AI autonomos + estetica pixel art = Productividad del futuro. Mini Office esta aqui. #MiniOffice #CLAUDIO",
            "Deja de perder tiempo configurando herramientas. Mini Office se configura solo. #AutoMate #AI",
            "Conway's Game of Life + AI Agents = Mini Office 24/7. Tu oficina nunca duerme. #OpenSource",
            "Pixel art no es solo retro. Es productividad con estilo. #MiniOffice #PixelArt"
        ],
        'linkedin': [
            "Presentamos Mini Office: La primera oficina virtual con agentes AI autonomos y estetica pixel art. Disponible en GitHub.",
            "El futuro del trabajo es automatico. Mini Office te ayuda a gestionar tus agentes AI mientras te concentras en lo importante.",
            "Open Source + AI + Pixel Art = Mini Office. La combinacion que no sabias que necesitabas."
        ],
        'instagram': [
            "Tu oficina nunca se vio tan pixelada. #MiniOffice #PixelArt #AI #OpenSource",
            "Agentes reales. Trabajo real. Estilo real. #Conway247 #CLAUDIO",
            "El futuro es pixelado. #MiniOffice #Cyberpunk #Steampunk"
        ],
        'github': """
# Mini Office - Conway 24/7 Edition

> Tu oficina virtual que trabaja 24/7

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

## Caracteristicas
- 5 Agentes AI trabajando en tiempo real
- 8 Departamentos especializados
- Evolucion automatica (performance >= 0.85)
- Interfaz pixel art personalizable
- 100% offline despues de instalar

## Instalacion rapida
```bash
git clone https://github.com/medioevo/mini-office.git
cd mini-office
pip install -r requirements.txt
python mini_office.py
```

## Hecho con ❤️ por MEDIOEVO
        """
    }

    return posts


def generate_gumroad_description():
    """Genera descripcion para Gumroad"""

    return """
# Mini Office - Conway 24/7 Edition

## Tu oficina virtual que trabaja 24/7

Mini Office es una oficina virtual auto-contenida que monitorea y controla tus agentes AI en tiempo real. Diseñado con estética retro-pixelada para developers que aman el estilo cybersteampunk.

## ¿Qué obtienes?

- **5 Agentes AI reales** trabajando en tiempo real
- **8 Departamentos** especializados (IT, HR, research, QA, Writing, Social, Cleaning, Security)
- **Evolución automatica** cuando el performance >= 0.85
- **Interfaz pixel art** personalizable con CLAUDIO Design System v1.0
- **Auto-ejecutable** - sin instalación compleja
- **100% offline** después de instalar dependencias

## Características principales:

✓ Sistema Conway basado en el Juego de la Vida
✓ Agentes que evolucionan y mejoran automaticamente
✓ Dashboard visual con métricas en tiempo real
✓ Diseño Steampunk + Cyberpunk + Biopunk
✓ Documentación completa incluida
✓ Código abierto (MIT License)

## requisitos:

- Python 3.8+
- Windows, Linux o macOS
- 50MB de espacio en disco

## ¿Cómo funciona?

1. Descargas el archivo ZIP
2. Ejecutas INSTALL_AND_RUN.bat (Windows) o install_and_run.sh (Linux/Mac)
3. El sistema instala dependencias automaticamente
4. Tu navegador se abre en http://localhost:8000
5. ¡Listo! Tu oficina virtual está funcionando

## Soporte:

- Documentación completa incluida
- Issues en GitHub: https://github.com/medioevo/mini-office/issues
- Email: l-tyr-r@outlook.com

## Licencia:

MIT License - Puedes usar, modificar y distribuir libremente.

---

**Precio:** GRATIS (o paga lo que quieras desde $0 USD)

**Garantía:** 100% gratuito y de código abierto. Si te gusta, considera dejar una estrella en GitHub.
"""


def generate_readme_short():
    """Genera reADME corto para publicación"""

    return """
# Mini Office - Conway 24/7

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Tu oficina virtual que trabaja 24/7**
> Agentes AI autónomos con estética pixel art

## Instalación Rápida

```bash
# Windows
INSTALL_AND_RUN.bat

# Linux/Mac
chmod +x install_and_run.sh && ./install_and_run.sh
```

## Características

- 5 Agentes AI en tiempo real
- 8 Departamentos especializados
- Evolución automatica (performance >= 0.85)
- Diseño CLAUDIO v1.0 (Steampunk + Cyberpunk)
- 100% Open Source (MIT)

## Demo

Después de instalar, abre tu navegador en:
http://localhost:8000

## Documentación Completa

Ver [reADME.md](reADME.md) para documentación completa.

## Licencia

MIT License - Ver [LICENSE](LICENSE)
"""


if __name__ == '__main__':
    # Generar todos los materiales
    materials = generate_all_promo_materials()

    # Generar posts para redes
    social_posts = generate_social_media_posts()
    print("\n" + "="*60)
    print("POSTS PARA reDES SOCIALES GENERADOS")
    print("="*60)
    print("\nTwitter (5 posts):")
    for i, post in enumerate(social_posts['twitter'], 1):
        print(f"  {i}. {post[:80]}...")

    print("\nLinkedIn (3 posts):")
    for i, post in enumerate(social_posts['linkedin'], 1):
        print(f"  {i}. {post[:80]}...")

    print("\nInstagram (3 posts):")
    for i, post in enumerate(social_posts['instagram'], 1):
        print(f"  {i}. {post[:80]}...")

    # Guardar posts
    output_dir = Path(__file__).parent.parent / 'reports'
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / 'social_media_posts.json', 'w', encoding='utf-8') as f:
        json.dump(social_posts, f, indent=2, ensure_ascii=False)

    # Gumroad description
    gumroad_desc = generate_gumroad_description()
    with open(output_dir / 'gumroad_description.txt', 'w', encoding='utf-8') as f:
        f.write(gumroad_desc)

    # reADME corto
    readme_short = generate_readme_short()
    with open(output_dir / 'reADME_SHORT.md', 'w', encoding='utf-8') as f:
        f.write(readme_short)

    print("\n" + "="*60)
    print("MATERIALES GUARDADOS EN: reports/")
    print("="*60)
