#!/usr/bin/env python
"""
Mini Office - Publicar en Gumroad
==================================
Script para generar los assets y contenido para Gumroad
"""

import json
from pathlib import Path
from datetime import datetime

def generar_contenido_gumroad():
    """Genera todo el contenido necesario para publicar en Gumroad"""

    contenido = {
        'titulo': 'Mini Office - Conway 24/7 Edition',
        'descripcion_corta': 'Tu oficina virtual que trabaja 24/7 con agentes AI autónomos',
        'precio': '0+',  # Gratis o paga lo que quieras
        'categoria': 'Software',
        'tags': ['ai', 'open-source', 'productivity', 'python', 'pixel-art', 'conway', 'automation'],

        # Descripción completa para Gumroad
        'descripcion_completa': '''
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
''',

        # Instrucciones de instalación
        'instrucciones': '''
# Instalación Rápida

## Windows
1. Descarga el archivo ZIP
2. Extrae en una carpeta
3. Ejecuta `INSTALL_AND_RUN.bat`
4. El sistema instalará dependencias automaticamente
5. Tu navegador se abrirá en http://localhost:8000

## Linux/Mac
1. Descarga el archivo ZIP
2. Extrae en una carpeta
3. Abre terchical en la carpeta
4. Ejecuta `chmod +x install_and_run.sh`
5. Ejecuta `./install_and_run.sh`
6. Tu navegador se abrirá en http://localhost:8000

## Manual (cualquier sistema)
```bash
pip install -r requirements.txt
python mini_office.py
```
''',
    }

    return contenido


def generar_posts_redes():
    """Genera posts para redes sociales"""

    posts = {
        'twitter': [
            {
                'texto': 'Tu oficina virtual que trabaja 24/7? Ya existe. Se llama Mini Office. #AI #OpenSource #Conway247',
                'imagen': 'screenshot_dashboard.png',
                'hora_publicacion': '9:00 AM'
            },
            {
                'texto': 'Agentes AI autonomos + estetica pixel art = Productividad del futuro. Mini Office esta aqui. #MiniOffice #CLAUDIO',
                'imagen': 'screenshot_agents.png',
                'hora_publicacion': '2:00 PM'
            },
            {
                'texto': 'Deja de perder tiempo configurando herramientas. Mini Office se configura solo. #AutoMate #AI',
                'imagen': 'screenshot_install.png',
                'hora_publicacion': '6:00 PM'
            }
        ],
        'linkedin': [
            {
                'titulo': 'Presentamos Mini Office: La primera oficina virtual con agentes AI autónomos y estética pixel art',
                'cuerpo': '''
Estamos emocionados de anunciar el lanzamiento de Mini Office - Conway 24/7 Edition.

Mini Office es una oficina virtual auto-contenida que monitorea y controla tus agentes AI en tiempo real. Diseñado con estética retro-pixelada para developers que aman el estilo cybersteampunk.

Características principales:
- 5 Agentes AI trabajando en tiempo real
- 8 Departamentos especializados
- Evolución automatica (performance >= 0.85)
- Interfaz pixel art personalizable
- 100% Open Source (MIT License)

Disponible gratis en Gumroad y GitHub.

#AI #OpenSource #Productivity #Python #PixelArt
''',
                'hora_publicacion': '10:00 AM'
            }
        ],
        'instagram': [
            {
                'texto': 'Tu oficina nunca se vio tan pixelada. #MiniOffice #PixelArt #AI #OpenSource',
                'tipo': 'imagen_dashboard'
            },
            {
                'texto': 'Agentes reales. Trabajo real. Estilo real. #Conway247 #CLAUDIO',
                'tipo': 'carousel_agentes'
            },
            {
                'texto': 'El futuro es pixelado. #MiniOffice #Cyberpunk #Steampunk',
                'tipo': 'reel_instalacion'
            }
        ]
    }

    return posts


def generar_email_marketing():
    """Genera emails para marketing"""

    emails = {
        'anuncio_lanzamiento': {
            'asunto': 'Mini Office - Tu oficina virtual 24/7 ya está aquí',
            'preview': 'Agentes AI + Pixel Art = Productividad del futuro',
            'cuerpo': '''
Hola!

Hoy es un día especial. Después de mucho trabajo, estamos emocionados de presentarte:

# Mini Office - Conway 24/7 Edition

Imagina una oficina virtual donde:
- Tus agentes AI investigan mientras duermes
- El análisis de mercado es automatico
- La evolución es constante (performance >= 0.85)
- Todo tiene estética de videojuego pixel art

Suena como el futuro, verdad?

Pues el futuro llegó. Y es 100% gratuito.

Mini Office es open source (MIT License), lo que significa que puedes:
✓ Usarlo gratis
✓ Modificarlo para tus necesidades
✓ Contribuir con mejoras
✓ Aprender de cómo funciona

¿Lo mejor? La instalación es en 1 click.

[Botón: Descargar Gratis]

Tu oficina virtual te está esperando.

Saludos,
El equipo de MEDIOEVO

---
P.D.: También revisa el código en GitHub. Las contribuciones son bienvenidas!
'''
        },
        'seguimiento': {
            'asunto': '¿Viste esto? Mini Office te está esperando',
            'preview': 'Únete a la revolución open source',
            'cuerpo': '''
Hola de nuevo!

Solo pasando para recordarte que Mini Office - Conway 24/7 está disponible:

- 5 Agentes AI en tiempo real
- 8 Departamentos especializados
- Diseño CLAUDIO v1.0 (Steampunk + Cyberpunk)
- 100% Open Source

¿Lo mejor? Es completamente gratis.

[Botón: Ver en GitHub]

Nos vemos en el código!

El equipo de MEDIOEVO
'''
        }
    }

    return emails


if __name__ == '__main__':
    print("\n" + "="*60)
    print("GENERANDO CONTENIDO PARA GUMROAD")
    print("="*60)

    # Generar contenido
    contenido = generar_contenido_gumroad()
    posts = generar_posts_redes()
    emails = generar_email_marketing()

    # Guardar en reports
    output_dir = Path(__file__).parent.parent / 'reports'
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / 'gumroad_content.json', 'w', encoding='utf-8') as f:
        json.dump({
            'gumroad': contenido,
            'social_posts': posts,
            'emails': emails
        }, f, indent=2, ensure_ascii=False)

    print(f"\nContenido guardado en: {output_dir / 'gumroad_content.json'}")
    print("\n" + "="*60)
    print("CONTENIDO LISTO PARA PUBLICAR")
    print("="*60)
    print("\nSiguientes paeres:")
    print("1. Ir a gumroad.com")
    print("2. Crear nuevo producto")
    print("3. Copiar/pegar contenido de gumroad_content.json")
    print("4. Subir archivo ZIP del proyecto")
    print("5. Publicar")
