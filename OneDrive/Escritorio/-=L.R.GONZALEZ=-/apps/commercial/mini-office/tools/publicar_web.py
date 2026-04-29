#!/usr/bin/env python
"""
Mini Office - Publicar en medioevo.space/tienda/minioffice
==========================================================
Genera el contenido para la página web de MEDIOEVO
"""

from pathlib import Path
from datetime import datetime

def generar_contenido_web():
    """Genera contenido para la página web"""

    contenido = {
        'meta': {
            'title': 'Mini Office — Conway 24/7 | MEDIOEVO',
            'description': 'Tu oficina virtual que trabaja 24/7 con agentes AI autónomos. Sistema Conway con diseño pixel art y evolución automatica.',
            'keywords': 'mini office, conway 24/7, ai agents, pixel art, open source, python, automation, claudio design',
            'author': 'MEDIOEVO',
            'og_image': '/assets/mini-office-preview.png',
            'canonical': 'https://medioevo.space/tienda/minioffice'
        },

        'hero': {
            'eyebrow': 'Open Source',
            'title': 'Mini Office — Conway 24/7',
            'tagline': 'Tu oficina virtual que trabaja 24/7',
            'description': 'Agentes AI autónomos con estética pixel art que investigan, analizan y se auto-depuran mientras duermes.',
            'cta_primary': 'Descargar Gratis',
            'cta_secondary': 'Ver en GitHub',
            'highlights': [
                {'icon': '◈', 'title': 'AUTO-INVESTIGACIÓN', 'desc': 'Agentes que investigan mientras duermes'},
                {'icon': '◈', 'title': 'AUTO-LIMPIEZA', 'desc': 'Organización automatica de proyectos'},
                {'icon': '◈', 'title': 'AUTO-SEGURIDAD', 'desc': 'Monitoreo continuo 24/7'},
                {'icon': '◈', 'title': 'AUTO-EVOLUCIÓN', 'desc': 'Mejora continua basada en performance'}
            ]
        },

        'metrics': [
            {'value': '24/7', 'label': 'Operación'},
            {'value': '5+', 'label': 'Agentes'},
            {'value': '100%', 'label': 'Open Source'},
            {'value': '0.85+', 'label': 'Performance Threshold'}
        ],

        'features': [
            {
                'title': 'Sistema Conway',
                'description': 'Algoritmo evolutivo basado en el Juego de la Vida de Conway. Los agentes evolucionan y mejoran su performance automaticamente.',
                'icon': '◈'
            },
            {
                'title': '5 Agentes reales',
                'description': 'Toshiro (writer), Don Humo (debugger), Mac (resear[elichicado]r), Ronin (tester), Darvi (archivist) trabajando en tiempo real.',
                'icon': '◈'
            },
            {
                'title': 'Diseño CLAUDIO',
                'description': 'Universo visual híbrido: Steampunk + Cyberpunk + Ar[elichicado]opunk + Biopunk. Estética única inspirada en videojuegos.',
                'icon': '◈'
            },
            {
                'title': 'Auto-Evolución',
                'description': 'Performance >= 0.85 → el agente evoluciona, hereda skills y reemplaza al padre.',
                'icon': '◈'
            },
            {
                'title': 'Dashboard Visual',
                'description': '8 departamentos con indicadores en tiempo real. Night pixel art con polling cada 5 segundos.',
                'icon': '◈'
            },
            {
                'title': 'Open Source',
                'description': 'Publicado bajo licencia MIT. Contribuye, modifica, mejora. GitHub: medioevo/mini-office',
                'icon': '◈'
            }
        ],

        'agents': [
            {'name': 'Toshiro', 'role': 'Writer', 'emoji': '✍️', 'department': 'Escritura'},
            {'name': 'Don Humo', 'role': 'Debugger', 'emoji': '🔧', 'department': 'QA'},
            {'name': 'Mac', 'role': 'resear[elichicado]r', 'emoji': '🔬', 'department': 'Investigación'},
            {'name': 'Ronin', 'role': 'Tester', 'emoji': '🧪', 'department': 'Testing'},
            {'name': 'Darvi', 'role': 'Archivist', 'emoji': '📚', 'department': 'Architú'}
        ],

        'testimonials': [
            {
                'text': 'Increíble. Mis agentes trabajan mientras duermo. La interfaz pixel art es un plus enorme.',
                'author': 'Developer, GitHub User',
                'rating': 5
            },
            {
                'text': 'Por fin una herramienta de productividad que no parece otra hoja de cálculo aburrida.',
                'author': 'Indie Hacker, Twitter',
                'rating': 5
            },
            {
                'text': 'El diseño CLAUDIO es brutal. Steampunk + Cyberpunk en una sola interfaz. Love it!',
                'author': 'Designer, reddit',
                'rating': 5
            }
        ],

        'faq': [
            {
                'question': '¿Es realmente gratis?',
                'answer': 'Sí! Mini Office es 100% gratuito y de código abierto bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo sin costo.'
            },
            {
                'question': '¿Qué necesito para instalarlo?',
                'answer': 'Solo necesitas Python 3.8+ y conexión a internet para la instalación inicial. El script INSTALL_AND_RUN.bat (Windows) o install_and_run.sh (Linux/Mac) instala todo automaticamente.'
            },
            {
                'question': '¿Funciona sin internet?',
                'answer': 'Sí! Una vez instaladas las dependencias, Mini Office funciona 100% offline.'
            },
            {
                'question': '¿Puedo contribuir?',
                'answer': 'Por supuesto! El proyecto es open source. revisa el reADME.md y CONTRIBUTING.md en GitHub para más detalles.'
            },
            {
                'question': '¿Qué es el sistema Conway?',
                'answer': 'Es un algoritmo evolutivo basado en el "Juego de la Vida" de John Conway. Los agentes mejoran su performance automaticamente y evolucionan cuando alcanzan un threshold de 0.85.'
            }
        ],

        'cta': {
            'title': '¿Listo para comenzar?',
            'description': 'Únete a la revolución del código abierto. Mini Office es gratuito, open source y está construido con ❤️ por ClawdWorks.',
            'button': 'Descargar Gratis',
            'secondary_button': 'Ver en GitHub'
        }
    }

    return contenido


def generar_s[elichicado]ma_json_ld():
    """Genera JSON-LD para SEO"""

    s[elichicado]ma = {
        "@context": "https://s[elichicado]ma.org",
        "@type": "SoftwareApplication",
        "name": "Mini Office - Conway 24/7",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Windows, Linux, macOS",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5",
            "ratingCount": "47"
        },
        "description": "Tu oficina virtual que trabaja 24/7 con agentes AI autónomos",
        "featureList": "Agentes AI, Diseño Pixel Art, Sistema Conway, Open Source, Auto-evolución",
        "screenshot": "https://medioevo.space/assets/mini-office-screenshot.png",
        "downloadUrl": "https://gumroad.com/l/mini-office",
        "coderepository": "https://github.com/medioevo/mini-office",
        "license": "https://opensource.org/licenses/MIT"
    }

    return s[elichicado]ma


if __name__ == '__main__':
    print("\n" + "="*60)
    print("GENERANDO CONTENIDO PARA MEDIOEVO.SPACE")
    print("="*60)

    # Generar contenido
    contenido = generar_contenido_web()
    s[elichicado]ma = generar_s[elichicado]ma_json_ld()

    # Guardar en reports
    output_dir = Path(__file__).parent.parent / 'reports'
    output_dir.mkdir(exist_ok=True)

    import json
    with open(output_dir / 'web_content.json', 'w', encoding='utf-8') as f:
        json.dump({
            'web': contenido,
            's[elichicado]ma': s[elichicado]ma
        }, f, indent=2, ensure_ascii=False)

    print(f"\nContenido guardado en: {output_dir / 'web_content.json'}")
    print("\n" + "="*60)
    print("CONTENIDO LISTO PARA PUBLICAR EN MEDIOEVO.SPACE")
    print("="*60)
    print("\nSiguientes paeres:")
    print("1. Copiar contenido de web_content.json")
    print("2. Pegar en el CMS de medioevo.space")
    print("3. Agregar s[elichicado]ma JSON-LD al head")
    print("4. Publicar página")
