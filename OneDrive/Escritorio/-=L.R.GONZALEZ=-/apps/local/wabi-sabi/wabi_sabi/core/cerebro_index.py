from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CEREBRO_NAVIGATION_SCHEMA = "wabi.cerebro_navigation.v1"
BIBLIOTECA_REL = Path("-=MEDIOEVO=-") / "-=LIBROS" / "-=CEREBRO=-" / "00_BIBLIOTECA_HUMANA"
CEREBRO_REL = Path("-=MEDIOEVO=-") / "-=LIBROS" / "-=CEREBRO=-"
MASTER_REL = Path("MEDIOEVO_OBSERVACIONISMO_MASTER")
PRODUCTOS_REL = Path("PRODUCTOS_MEDIOEVO")


def build_cerebro_navigation(workspace: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    cerebro = workspace_path / CEREBRO_REL
    master = workspace_path / MASTER_REL
    productos = workspace_path / PRODUCTOS_REL
    biblioteca = workspace_path / BIBLIOTECA_REL
    manifest = _load_master_manifest(master)
    source_count = int(manifest.get("source_count") or 0)
    by_category = manifest.get("by_category") if isinstance(manifest.get("by_category"), dict) else {}
    required_docs = [
        "README.md",
        "RUTA_5_MINUTOS.md",
        "MAPA_POR_SISTEMAS.md",
        "CLAIMS_Y_FALSADORES.md",
        "MODULOS_Y_CODIGO.md",
    ]
    existing_docs = [name for name in required_docs if (biblioteca / name).exists()]
    return {
        "schema": CEREBRO_NAVIGATION_SCHEMA,
        "ok": cerebro.exists() and master.exists(),
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "paths": {
            "cerebro": str(cerebro),
            "biblioteca_humana": str(biblioteca),
            "master": str(master),
            "productos": str(productos),
            "source_manifest": str(master / "SOURCE_MANIFEST.json"),
        },
        "source_summary": {
            "source_count": source_count,
            "by_category": by_category,
        },
        "human_reading_order": [
            {"title": "Orientacion rapida", "path": str(biblioteca / "RUTA_5_MINUTOS.md")},
            {"title": "Mapa por sistemas", "path": str(biblioteca / "MAPA_POR_SISTEMAS.md")},
            {"title": "Claims y falsadores", "path": str(biblioteca / "CLAIMS_Y_FALSADORES.md")},
            {"title": "Modulos y codigo", "path": str(biblioteca / "MODULOS_Y_CODIGO.md")},
            {"title": "Canon compilado", "path": str(master / "00_README_MASTER.md")},
        ],
        "system_map": _system_map(workspace_path),
        "artifact_status": {
            "required_docs": required_docs,
            "existing_docs": existing_docs,
            "missing_docs": [name for name in required_docs if name not in existing_docs],
        },
        "certainty": [
            "CEREBRO is the human entrypoint for canon and maps.",
            "MEDIOEVO_OBSERVACIONISMO_MASTER is the compiled canon layer.",
            "PSI remains the formal theory lane; source folders are not moved by this index.",
        ],
        "inference": [
            "A human-readable system map reduces duplicate truth better than moving source folders now.",
            "Product and publication gates should point to root PRODUCT_MAP, VISIBILITY_MATRIX and RISK_REGISTER.",
        ],
        "unknown": [
            "Heavy PDF/DOCX/ZIP/TAR media may still need per-claim extraction.",
            "Runtime proof for each module is outside this navigation index.",
        ],
        "next_actions": [
            "Write or refresh the human library docs.",
            "Keep source files in place and route new raw material through fichas.",
            "Implement module tests before claiming framework runtime closure.",
        ],
    }


def write_cerebro_navigation_docs(payload: dict[str, Any]) -> list[str]:
    workspace = Path(str(payload["workspace"])).resolve()
    biblioteca = workspace / BIBLIOTECA_REL
    cerebro = workspace / CEREBRO_REL
    productos = workspace / PRODUCTOS_REL
    biblioteca.mkdir(parents=True, exist_ok=True)
    artifacts = [
        _write(biblioteca / "README.md", _readme(payload)),
        _write(biblioteca / "RUTA_5_MINUTOS.md", _ruta_5_minutos(payload)),
        _write(biblioteca / "MAPA_POR_SISTEMAS.md", _mapa_por_sistemas(payload)),
        _write(biblioteca / "CLAIMS_Y_FALSADORES.md", _claims_y_falsadores(payload)),
        _write(biblioteca / "MODULOS_Y_CODIGO.md", _modulos_y_codigo(payload)),
        _write(biblioteca / "CEREBRO_NAVIGATION_MANIFEST.json", json.dumps(payload, indent=2, ensure_ascii=False)),
    ]
    artifacts.append(_update_leer_primero(cerebro))
    artifacts.extend(_write_product_bridges(workspace, productos))
    artifacts.append(_write_agent_manifest(cerebro, payload))
    return [str(path) for path in artifacts]


def _load_master_manifest(master: Path) -> dict[str, Any]:
    path = master / "SOURCE_MANIFEST.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _system_map(workspace: Path) -> list[dict[str, str]]:
    return [
        {
            "system": "Entrada humana / Hipocampo",
            "human_doc": str(workspace / BIBLIOTECA_REL / "README.md"),
            "canon_doc": str(workspace / MASTER_REL / "00_README_MASTER.md"),
            "runtime_or_code": str(workspace / "SOURCE_INTAKE_REGISTER.md"),
            "gate": "APPROVE_LOCAL_DOCS",
        },
        {
            "system": "Sistema cognitivo",
            "human_doc": str(workspace / BIBLIOTECA_REL / "MAPA_POR_SISTEMAS.md"),
            "canon_doc": str(workspace / MASTER_REL / "07_OBSERVACIONISMO.md"),
            "runtime_or_code": str(workspace / "packages" / "open-dev" / "obsai-core"),
            "gate": "PUBLISH_WITH_SCOPE",
        },
        {
            "system": "Sistema inmunologico",
            "human_doc": str(workspace / BIBLIOTECA_REL / "CLAIMS_Y_FALSADORES.md"),
            "canon_doc": str(workspace / MASTER_REL / "18_RIESGOS_CONTRADICCIONES.md"),
            "runtime_or_code": str(workspace / "tools" / "release" / "curador_preflight.py"),
            "gate": "REVIEW_OR_BLOCK_FOR_EXTERNAL_ACTIONS",
        },
        {
            "system": "Sistema nervioso / agentes",
            "human_doc": str(workspace / MASTER_REL / "13_AGENTES.md"),
            "canon_doc": str(workspace / MASTER_REL / "04_TEORIA_IA_AGENTES.md"),
            "runtime_or_code": str(workspace / "apps" / "local" / "wabi-sabi"),
            "gate": "LOCAL_FIRST",
        },
        {
            "system": "Sistema musculoesqueletico / DUAT-GEODIA",
            "human_doc": str(workspace / MASTER_REL / "11_DUAT_GEODIA_HORMIGUERO.md"),
            "canon_doc": str(workspace / CEREBRO_REL / "01_MAPA_SISTEMAS_CEREBRO_DUAT_BRAIN_OS_2026-05-05.md"),
            "runtime_or_code": str(workspace / "PRODUCTOS_MEDIOEVO" / "claudio_os_blueprint"),
            "gate": "READ_ONLY_OR_VM_FIRST",
        },
        {
            "system": "Productos y publicacion",
            "human_doc": str(workspace / PRODUCTOS_REL / "00_LEER_PRIMERO.md"),
            "canon_doc": str(workspace / "PRODUCT_MAP.md"),
            "runtime_or_code": str(workspace / "VISIBILITY_MATRIX.md"),
            "gate": "PUBLICATION_REVIEW_REQUIRED",
        },
    ]


def _readme(payload: dict[str, Any]) -> str:
    return f"""# Biblioteca Humana CEREBRO

Estado: `CANON_HUMANO_DE_NAVEGACION`

Esta carpeta es la puerta de lectura para humanos. No reemplaza las fuentes ni el canon formal: ordena el acceso.

CERTEZA:
- CEREBRO contiene la entrada humana y los mapas.
- `MEDIOEVO_OBSERVACIONISMO_MASTER` contiene la compilacion formal 00-22.
- `-=PSI=-` conserva la teoria formal y fuentes conversacionales.
- Fuentes inventariadas en el ultimo corte: `{payload['source_summary']['source_count']}`.

INFERENCIA:
- La forma mas segura de unificar el marco ahora es una biblioteca navegable, no mover carpetas crudas.

INCOGNITA:
- Los archivos pesados siguen requiriendo ficha individual si se vuelven evidencia de un claim.

ACCION:
- Leer `RUTA_5_MINUTOS.md` primero.
- Usar `MAPA_POR_SISTEMAS.md` para ubicar teoria, codigo, producto y gates.
- Usar `CLAIMS_Y_FALSADORES.md` antes de publicar o afirmar algo fuerte.

ARTEFACTO:
- Biblioteca humana generada por Wabi-Sabi/Codex.
"""


def _ruta_5_minutos(payload: dict[str, Any]) -> str:
    return """# Ruta de 5 Minutos

CERTEZA:
- Si solo puedes leer una ruta, sigue esta lista.

ACCION:
1. `README.md`: que contiene la biblioteca.
2. `MAPA_POR_SISTEMAS.md`: donde vive cada cosa.
3. `CLAIMS_Y_FALSADORES.md`: que se puede decir y que esta bloqueado.
4. `MODULOS_Y_CODIGO.md`: que se puede implementar.
5. `../-=PSI=-/00_README_MASTER.md` o `../../../../MEDIOEVO_OBSERVACIONISMO_MASTER/00_README_MASTER.md`: canon formal.

INFERENCIA:
- Esta ruta reduce R porque evita entrar directo a fuentes crudas, zips o conversaciones largas.

INCOGNITA:
- Si buscas un archivo especifico, usa el manifiesto master o una ficha de fuente.

ARTEFACTO:
- Ruta corta de continuidad humana.
"""


def _mapa_por_sistemas(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {item['system']} | `{item['human_doc']}` | `{item['canon_doc']}` | `{item['runtime_or_code']}` | `{item['gate']}` |"
        for item in payload["system_map"]
    )
    return f"""# Mapa por Sistemas

CERTEZA:
- El marco se lee mejor por sistemas, no por carpetas sueltas.

| Sistema | Lectura humana | Canon | Runtime/codigo | Gate |
|---|---|---|---|---|
{rows}

INFERENCIA:
- CEREBRO funciona como hipocampo/indice; Claudio y Wabi-Sabi ejecutan; PRODUCTOS_MEDIOEVO empaqueta solo despues de gates.

INCOGNITA:
- La equivalencia entre documentos teoricos y codigo necesita tests por modulo.

ACCION:
- Para agregar informacion nueva, primero crear ficha o registro; despues decidir si va a canon, runtime, producto, archivo o privado.

ARTEFACTO:
- Mapa humano de navegacion por sistemas.
"""


def _claims_y_falsadores(payload: dict[str, Any]) -> str:
    return """# Claims y Falsadores

CERTEZA:
- Los claims operativos de Observacionismo se pueden publicar con alcance.
- Los claims fisicos fuertes requieren formalismo, simulacion o falsador numerico.
- Publicacion, venta, push, deploy y acciones externas siguen bajo REVIEW/BLOCK.

| Tipo | Estado | Accion |
|---|---|---|
| Observacionismo como metodo | PUBLISH_ALLOWED_WITH_SCOPE | Usar como framework operativo, no como ciencia total validada |
| Wabi-Sabi/Claudio como nodo operativo | PUBLISH_ALLOWED_AS_MODEL | Presentar como arquitectura local-first |
| OSIT-AG P-01 a P-04 | FORMAL_HYPOTHESIS / algebra local | Reproducir con herramienta simbolica antes de paper fuerte |
| QNM/Hawking/GW/dark energy/inflacion | NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC | Mantener bloqueado hasta computo |
| Sigma clinica/cognitiva | REQUIRES_VALIDATION | Usar lenguaje fenomenologico |
| Matrix/lore | LORE / COMUNICACION | No derivar fisica desde metafora |

INFERENCIA:
- El valor inmediato esta en convertir claims en pruebas, gates y modulos.

INCOGNITA:
- Faltan datasets/preregistros y validacion independiente.

ACCION:
- Antes de publicar, consultar `MEDIOEVO_OBSERVACIONISMO_MASTER/16_CLAIMS_REGISTER.md` y `17_FALSADORES_Y_TESTS.md`.

ARTEFACTO:
- Tabla humana de claims y falsadores.
"""


def _modulos_y_codigo(payload: dict[str, Any]) -> str:
    return """# Modulos y Codigo

CERTEZA:
- Ya existen carriles de codigo para Wabi-Sabi local, obsai-core, curador y ClaudioOS blueprint.
- La informacion absorbida apunta a modulos concretos: gates, memory, curator, router, validator, evidence, claims, simulation.

| Modulo | Ruta inicial | Proposito | Prueba minima |
|---|---|---|---|
| `curator_order_assistant` | `apps/local/wabi-sabi/wabi_sabi/core/curator_assistant.py` | Mantener orden y fichas sin borrar | Report dry-run + witness |
| `cerebro_index` | `apps/local/wabi-sabi/wabi_sabi/core/cerebro_index.py` | Navegacion humana/agente de CEREBRO | JSON + docs generados |
| `ActionGate` | `packages/open-dev/obsai-core/obsai_core/gate.py` | Aprobar/revisar/bloquear | Claims fuertes sin evidencia bloquean |
| `TaskManager` | `packages/open-dev/obsai-core/obsai_core/tasks.py` | Cerrar tareas con evidencia | No cierra sin evidencia |
| `module_manifest_validator` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/contracts` | Contrato minimo de modulos | Manifest sin witness/recovery falla |

INFERENCIA:
- El siguiente paso de codigo debe conectar biblioteca humana, fichas y gates, no crear otro silo.

INCOGNITA:
- Falta runtime completo para algunos modulos del master 00-22.

ACCION:
- Implementar tests de cada modulo antes de afirmar autonomia amplia.

ARTEFACTO:
- Mapa de codigo accionable para agentes.
"""


def _write_product_bridges(workspace: Path, productos: Path) -> list[Path]:
    productos.mkdir(parents=True, exist_ok=True)
    bridges = {
        "PRODUCT_MAP.md": "# PRODUCT_MAP PRODUCTOS_MEDIOEVO\n\nCERTEZA:\n- El mapa canonico de productos vive en `..\\PRODUCT_MAP.md`.\n- Esta carpeta es frente/staging de productos, no fuente unica de verdad.\n\nACCION:\n- Usar este puente para orientar agentes dentro de `PRODUCTOS_MEDIOEVO`.\n- Actualizar el mapa raiz cuando cambie una decision de producto.\n\nARTEFACTO:\n- Puente local hacia el PRODUCT_MAP canonico.\n",
        "VISIBILITY_MATRIX.md": "# VISIBILITY_MATRIX PRODUCTOS_MEDIOEVO\n\nCERTEZA:\n- La matriz canonica vive en `..\\VISIBILITY_MATRIX.md`.\n- Libros, TCG, audiovisual y software comercial no comparten el mismo gate.\n\nACCION:\n- Antes de publicar desde `PRODUCTOS_MEDIOEVO`, verificar allowlist/denylist en la matriz raiz.\n\nARTEFACTO:\n- Puente local hacia la matriz de visibilidad.\n",
        "RISK_REGISTER.md": "# RISK_REGISTER PRODUCTOS_MEDIOEVO\n\nCERTEZA:\n- El registro canonico de riesgos vive en `..\\RISK_REGISTER.md`.\n- Riesgos especificos aqui: mezcla de TCG/privado, betas sin QA, empaques comerciales, claims fuertes y autopublicacion.\n\nACCION:\n- Registrar riesgos nuevos en el archivo raiz, no solo en esta carpeta.\n\nARTEFACTO:\n- Puente local hacia el registro de riesgos.\n",
    }
    return [_write(productos / name, content) for name, content in bridges.items()]


def _write_agent_manifest(cerebro: Path, payload: dict[str, Any]) -> Path:
    path = cerebro / "_MANIFIESTOS" / "AGENTE_ULTIMO_PROCESAMIENTO_CEREBRO.json"
    data = {
        "schema": "medioevo.cerebro.last_processor.v1",
        "last_processor": "agent",
        "agent": "Wabi/Sabi-Codex",
        "processed_at_utc": payload["generated_at_utc"],
        "mode": "human_index_no_source_moves",
        "artifacts": [
            str(cerebro / "00_BIBLIOTECA_HUMANA"),
            str(cerebro / "_MANIFIESTOS" / "AGENTE_ULTIMO_PROCESAMIENTO_CEREBRO.json"),
        ],
        "source_truth": "MEDIOEVO_OBSERVACIONISMO_MASTER and -=PSI=- remain canonical source layers.",
    }
    return _write(path, json.dumps(data, indent=2, ensure_ascii=False))


def _update_leer_primero(cerebro: Path) -> Path:
    path = cerebro / "00_LEER_PRIMERO_HUMANO.md"
    marker = "## Biblioteca humana principal"
    block = """
## Biblioteca humana principal

La entrada recomendada ahora es `00_BIBLIOTECA_HUMANA/`.

- `00_BIBLIOTECA_HUMANA/README.md`: orientacion general.
- `00_BIBLIOTECA_HUMANA/RUTA_5_MINUTOS.md`: lectura minima.
- `00_BIBLIOTECA_HUMANA/MAPA_POR_SISTEMAS.md`: mapa humano por sistemas.
- `00_BIBLIOTECA_HUMANA/CLAIMS_Y_FALSADORES.md`: frontera de claims.
- `00_BIBLIOTECA_HUMANA/MODULOS_Y_CODIGO.md`: puente a runtime y codigo.

Regla: esta biblioteca no reemplaza las fuentes; las hace accesibles.
"""
    existing = path.read_text(encoding="utf-8") if path.exists() else "# CEREBRO MEDIOEVO - LEER PRIMERO HUMANO\n"
    if marker not in existing:
        existing = existing.rstrip() + "\n\n" + block.strip() + "\n"
    return _write(path, existing)


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
