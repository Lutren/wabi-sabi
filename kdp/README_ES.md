# Pipeline KDP

**Generación automática de EPUB, PDF y DOCX desde Markdown para Amazon KDP.**

Soporte nativo para lenguas indígenas (náhuatl incluido).  
Probado con manuscritos de hasta 180 páginas. Soluciona los errores de validación más comunes de KDP.

---

## Características

- **Entrada:** Markdown estándar (un archivo por libro o uno por capítulo)
- **Salida:** EPUB, PDF Paperback (6×9"), PDF Hardcover (6.14×9.21"), DOCX
- **Traducción:** Integración con DeepL API
- **Lenguas:** Soporte para caracteres especiales de náhuatl y otras lenguas indígenas
- **Fix automático:** Corrige MediaBox con origen negativo (error común en KDP)
- **Metadata:** Generación de metadata completa (título, autor, ISBN, idioma, BISAC)

---

## Requisitos

```bash
pip install -r requirements.txt
```

- Python 3.10+
- Pandoc (`apt install pandoc` / `brew install pandoc`)
- Ghostscript (`apt install ghostscript` / `brew install ghostscript`)
- Cuenta DeepL API (para traducción; la versión gratuita funciona para volúmenes bajos)

---

## Uso rápido

### Generar todos los formatos

```bash
python publisher.py --input libro.md --title "Mi Libro" --author "Autor" --lang es
```

### Solo EPUB

```bash
python publisher.py --input libro.md --format epub --lang nah
```

### Traducir y generar

```bash
python translator.py --input libro_es.md --target en --output libro_en.md
python publisher.py --input libro_en.md --lang en
```

### Fix de PDF con MediaBox negativo (error KDP)

```bash
python publisher.py --input libro.md --fix-mediabox
```

---

## Configuración de metadata

Crea un archivo `metadata.yaml` junto a tu manuscrito:

```yaml
title: "Título del Libro"
author: "Nombre Autor"
language: "es"          # es, en, nah (náhuatl), o cualquier BCP-47
isbn: "978-XXXXXXXXXX"  # opcional
publisher: "Editorial o nombre propio"
description: |
  Sinopsis de hasta 4,000 caracteres para KDP.
bisac:
  - "FIC028000"  # Science Fiction / General
  - "FIC028010"  # Science Fiction / Adventure
keywords:
  - "ciencia ficción en español"
  - "saga de ciencia ficción"
series:
  name: "Nombre de la Saga"
  number: 1
```

---

## Soporte para lenguas indígenas

El pipeline usa fuentes con cobertura completa de caracteres para:

- **Náhuatl clásico y moderno:** saltillo (ꞌ), vocales largas, etc.
- **Mixteco, Zapoteco, Maya:** caracteres tonales
- **Cualquier lengua con soporte Unicode**

Para náhuatl, usar `--lang nah` activa la fuente correcta y los atributos de idioma en el EPUB.

Si tu lengua no está en la lista, abre un Issue con el código BCP-47 y lo añadimos.

---

## Solución de errores comunes de KDP

### Error: "PDF has a negative MediaBox origin"

```bash
python publisher.py --input libro.md --fix-mediabox
```

Usa Ghostscript para corregir el origen y recomprimir. Probado con páginas de código monoespaciado.

### Error: "Text overflow on page X"

Reducir el tamaño de fuente base en `config.yaml` o aumentar márgenes:

```yaml
font_size: 11      # default: 12
margin_inner: 1.0  # pulgadas
margin_outer: 0.75
```

### Error: "EPUB validation failed"

```bash
python publisher.py --input libro.md --validate-epub
```

Ejecuta epubcheck y reporta los errores con sugerencia de fix.

---

## Estructura del proyecto

```
kdp/
├── publisher.py       # Generador principal
├── translator.py      # Integración DeepL
├── config.yaml        # Configuración global
├── templates/
│   ├── epub.css       # Estilos EPUB KDP
│   ├── paperback.tex  # Template LaTeX 6×9"
│   └── hardcover.tex  # Template LaTeX 6.14×9.21"
└── fonts/
    └── [fuentes con soporte de lenguas indígenas]
```

---

## Flujo de trabajo recomendado para autores de saga

```bash
# Por libro:
python publisher.py --input libro_01.md --metadata libro_01.yaml --all-formats
python translator.py --input libro_01.md --target en
python publisher.py --input libro_01_en.md --metadata libro_01_en.yaml --all-formats

# Output en /output/libro_01/
#   libro_01_es.epub
#   libro_01_es_paperback.pdf
#   libro_01_es_hardcover.pdf
#   libro_01_es.docx
#   libro_01_en.epub
#   ...
```

---

*Licencia MIT.*
