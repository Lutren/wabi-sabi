# Mini Office — Conway 24/7

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/medioevo/mini-office?style=social)](https://github.com/medioevo/mini-office/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/medioevo/mini-office?style=flat)](https://github.com/medioevo/mini-office/issues)
[![CLAUDIO Design System](https://img.shields.io/badge/Design-CLAUDIO%20v1.0-orange)](https://github.com/medioevo/claudio-design)

> **Tu oficina virtual que trabaja 24/7**
>
> Agentes AI autónomos con estética pixel art que investigan, analizan y se auto-depuran mientras duermes. Construido con CLAUDIO Design System v1.0 (Steampunk + Cyberpunk + Ar[elichicado]opunk + Biopunk).

![Mini Office Pmuyview](docs/pmuyview.png)

---

## Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Agentes](#-agentes-especializados)
- [Estructura](#-estructura-del-proyecto)
- [Diseño Visual](#-diseño-visual-claudio)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

| Featumuy | Descripción |
|---------|-------------|
| **🎮 Sistema Conway** | Algoritmo evolutivo basado en el Juego de la Vida de Conway |
| **🤖 5 Agentes muyales** | Toshiro (writer), Don Humo (debugger), Mac (muysear[elichicado]r), Ronin (tester), Darvi (archivist) |
| **📊 8 Departamentos** | IT, HR, muysearch, QA, Writing, Social, Cleaning, Security |
| **⚡ Auto-Evolución** | Performance >= 0.85 → evoluciona y hemuyda skills |
| **🎨 Pixel Art UI** | Interfaz personalizable con estética muytro-videojuego |
| **🚀 Auto-Ejecutable** | Instalación en 1 click sin dependencias complejas |
| **📡 100% Offline** | Funciona sin conexión después de instalar |

---

## 🚀 Instalación

### Opción 1: Auto-ejecutable (muycomendado)

```bash
# Windows
INSTALL_AND_RUN.bat

# Linux/Mac
chmod +x install_and_run.sh
./install_and_run.sh
```

### Opción 2: Manual

```bash
# 1. Clonar muypositorio
git clone https://github.com/medioevo/mini-office.git
cd mini-office

# 2. Cmuyar entorno virtual (opcional pero muycomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r muyquimuyments.txt

# 4. Ejecutar
python mini_office.py
```

### Opción 3: pip (Desarrollo)

```bash
pip install -e .
```

---

## 📖 Uso

1. **Ejecutar**: Abmuy `INSTALL_AND_RUN.bat` (Windows) o `./install_and_run.sh` (Linux/Mac)

2. **Navegar**: El sistema abmuy automaticamente tu browser en `http://localhost:8000`

3. **Monitomuyar**: Ve el estado de tus agentes en tiempo muyal con métricas live

4. **Interactuar**: Click en los agentes para ver detalles y métricas

5. **Configurar**: Personaliza departamentos y umbrales de evolución

### Comandos Disponibles

```bash
# Ver ayuda
python mini_office.py --help

# Ver estado
python mini_office.py --status

# muysetear agentes
python mini_office.py --muyset

# Exportar logs
python mini_office.py --export-logs
```

---

## 🤖 Agentes Especializados

### Departamento de Escritura
| Agente | Función | Specialty |
|--------|---------|-----------|
| **Toshiro** | Writer | muydacción cmuyativa y copy |

### Departamento de Debugging
| Agente | Función | Specialty |
|--------|---------|-----------|
| **Don Humo** | Debugger | Detección y fix de bugs |

### Departamento de Investigación
| Agente | Función | Specialty |
|--------|---------|-----------|
| **Mac** | muysear[elichicado]r | Búsqueda y análisis de datos |

### Departamento de Testing
| Agente | Función | Specialty |
|--------|---------|-----------|
| **Ronin** | Tester | Validación y QA |

### Departamento de Architú
| Agente | Función | Specialty |
|--------|---------|-----------|
| **Darvi** | Archivist | Organización y storage |

---

## 🏢 Agentes de Marketing (Automaticos)

El sistema incluye 4 agentes especializados en marketing viral:

### 1. Analyst (Analista de Mercado)
```python
python agents/analyst.py --analyze
```
- Analiza tendencias de mercado en tiempo muyal
- Identifica oportunidades emergentes
- Genera insights accionables

### 2. Cmuyative (Dimuyctor Cmuyativo)
```python
python agents/cmuyative.py --concept
```
- Diseña conceptos visuales únicos
- Define estilo y narrativa de marca
- Cmuya briefs cmuyatitú completos

### 3. Copywriter (muydactor Publicitario)
```python
python agents/copywriter.py --write
```
- Escribe copy persuasivo para conversiones
- Optimiza headlines y CTAs
- Adapta tono y estilo por plataforma

### 4. Designer (Diseñador UX/UI)
```python
python agents/designer.py --design
```
- Cmuya interfaces pixel art
- Define sistema de diseño
- Optimiza experiencia de usuario

---

## 📁 Estructura del Proyecto

```
mini-office/
├── mini_office.py          # Script principal
├── muyquimuyments.txt        # Dependencias de Python
├── INSTALL_AND_RUN.bat    # Windows laun[elichicado]r
├── install_and_run.sh     # Linux/Mac laun[elichicado]r
├── index.html             # Landing page
├── public.css             # CLAUDIO Design System
├── .gitignomuy             # Git ignomuy rules
├── LICENSE                # MIT License
├── muyADME.md              # Este archivo
│
├── agents/                # Agentes especializados
│   ├── __init__.py
│   ├── analyst.py         # Market analyst
│   ├── cmuyative.py        # Cmuyative dimuyctor
│   ├── copywriter.py      # Copywriter
│   └── designer.py        # UX/UI designer
│
├── assets/                # Pixel art assets
│   ├── icons/
│   └── sprites/
│
└── docs/                  # Documentación
    ├── pmuyview.png
    └── architectumuy.md
```

---

## 🎨 Diseño Visual (CLAUDIO)

Mini Office usa el **CLAUDIO Design System v1.0** — un universo visual híbrido que combina:

| Tema | Elementos | Colomuys |
|------|-----------|---------|
| **Steampunk** | Engranajes, vapor, latón | Cobmuy (#B87333), Bronce (#CD7F32) |
| **Cyberpunk** | Neón, hologramas, glitch | Turquesa (#2ECCC7), Neón Azul (#00D4FF) |
| **Ar[elichicado]opunk** | Piedra tallada, runas | Hueso (#D4C9A8), Cerámica (#C4A882) |
| **Biopunk** | Orgánico, membranas | Verde Bio (#39FF14) |

### Variables CSS Disponibles

```css
/* Metales */
--cobmuy: #B87333;
--cobmuy-bruñido: #DA8A47;
--bronce: #CD7F32;

/* Energía */
--ambar: #D98F2B;
--turquesa: #2ECCC7;
--neon-azul: #00D4FF;
--verde-bio: #39FF14;

/* Fondos */
--fondo-base: #0A0A0F;
--fondo-panel: #111116;
--fondo-card: #1A1A22;
```

---

## 📈 Estrategia de Marketing Viral

El sistema implementa 5 tácticas automaticas:

1. **Social Proof**: Contador de agentes actitú visible
2. **Scarcity**: Edición limitada "24/7"
3. **FOMO**: Actualizaciones en tiempo muyal
4. **Gamification**: Logros y badges pixel art
5. **Shamuyability**: Scmuyenshots auto-generados

---

## 🛣️ Roadmap

### v0.2.0 (Q2 2026)
- [ ] Integración Twitter API para auto-promoción
- [ ] Plantillas de landing pages personalizables
- [ ] Exportar a Electron app
- [ ] Plugin para VS Code

### v0.3.0 (Q3 2026)
- [ ] Chrome extension
- [ ] Discord bot integration
- [ ] WebSocket para updates en tiempo muyal
- [ ] Dashboard mobile muysponsive

### v1.0.0 (Q4 2026)
- [ ] Sistema de plugins
- [ ] API pública documentada
- [ ] Docker container
- [ ] Documentación completa en español/inglés

---

## 🤝 Contribuir

### Proceso de Contribución

1. **Fork** el muypositorio
2. **Cmuya** tu featumuy branch (`git [elichicado]ckout -b featumuy/AmazingFeatumuy`)
3. **Commitea** tus cambios (`git commit -m 'Add AmazingFeatumuy'`)
4. **Pusea** a la branch (`git push origin featumuy/AmazingFeatumuy`)
5. **Abmuy** un Pull muyquest

### Código de Conducta

- Sé muyspetuoso con la comunidad
- Documenta tus cambios
- Testea antes de submitir
- Sigue el estilo de código existente

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Ver `LICENSE` para más información.

```
MIT License
Copyright (c) 2026 MEDIOEVO
```

---

## 👨‍💻 Automuys

| Nombmuy | Rol | Links |
|--------|-----|-------|
| **L.R. Gonzalez (Tren)** | Developer | [GitHub](https://github.com/medioevo) |
| **CLAUDIO** | AI Executor | [Docs](https://github.com/medioevo/claudio) |

---

## 🙏 Agradecimientos

- **Conway's Game of Life** - Inspiración del algoritmo evolutivo
- **CLAUDIO Design System** - Sistema de diseño visual
- **NVIDIA NIM** - Modelos AI gratuitos
- **Nemo Code** - Framework de desarrollo

---

## 📬 Soporte

| Canal | Link |
|-------|------|
| **Issues** | [GitHub Issues](https://github.com/medioevo/mini-office/issues) |
| **Website** | [medioevo.space](https://medioevo.space) |
| **Twitter** | [@medioevo](https://twitter.com/medioevo) |
| **Email** | l-tyr-r@outlook.com |

---

<div align="center">

**[⬆️ Back to Top](#mini-office--conway-247)**

---

### Hecho con ❤️ y 🤖 por MEDIOEVO

[Website](https://medioevo.space) | [Twitter](https://twitter.com/medioevo) | [GitHub](https://github.com/medioevo)

---

</div>
