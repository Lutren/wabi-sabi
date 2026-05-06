# Repo Tree Fundamental Cleanup - 2026-05-06

Estado epistemologico: `CERTEZA` para evidencia local medida; `INFERENCIA` para decisiones de limpieza futura.
Regla base: buscar la estructura fundamental, estable y verificable. No borrar por ruido visual. Todo residuo se retira solo con ficha, hash, reemplazo o prueba de regenerabilidad.

## Resumen Operativo

Esta pasada corrigio el problema principal de arbol: el repo Git padre vive en `C:\Users\L-Tyr`, por eso Git estaba mezclando perfil de Windows, descargas, configuraciones privadas y workspace. Se aplico higiene local reversible en `C:\Users\L-Tyr\.git\info\exclude` para que el repo padre deje de tratar el perfil completo como codigo.

No se borraron documentos unicos ni fuentes privadas. La limpieza ejecutada aqui fue de frontera Git, no de contenido canonico.

## Evidencia Medida

| medicion | resultado | estado |
|---|---:|---|
| `pending_review.py --write --quiet` | `active_dedup=449`, `claudio_open=69` | `CERTEZA` |
| Curador status | `current_downloads_files=0` | `CERTEZA` |
| Curador SQLite `files` | `180` | `CERTEZA` |
| Curador SQLite `fichas` | `180` | `CERTEZA` |
| Curador status `ARCHIVO_FRIO` | `161` | `CERTEZA` |
| Curador status `BORRADO_DUPLICADO` | `18` | `CERTEZA` |
| Curador status `BASURA_REGENERABLE_BORRADA` | `1` | `CERTEZA` |
| `Downloads` recursivo | `0` archivos, `0.0 MB` | `CERTEZA` |
| audit repo | `11935` archivos, `1852` directorios | `CERTEZA` |
| status padre tracked-only | `84` lineas | `CERTEZA` |

## Fronteras Canonicas

| unidad | rol | decision |
|---|---|---|
| `C:\Users\L-Tyr` | repo padre / wrapper de control | no usar para `git add .`; staging exacto solamente |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` | portfolio MEDIOEVO actual | canon operativo principal |
| `-=MEDIOEVO=-\-=LIBROS` | repo anidado editorial/canon legacy | `REVIEW`; no mezclar con commits del repo padre |
| `-=MEDIOEVO=-\-=LIBROS\claudio` | repo anidado runtime Claudio | `REVIEW`; sucio y ahead, trabajo concurrente |
| `apps\commercial` | productos comerciales | conservar propietario; publicar solo copy filtrado |
| `packages\open-dev` | open source publico | mantener sanitisable y testeable |
| `docs\canon` y `docs\intake` | atlas, fichas y decisiones | fuente humana del Curador |
| `runtime\curador_seto` | indice operativo SQLite / archivo frio | fuente maquina del Curador |
| `COMMS` | comunicacion de agentes | contrato de handoff, no archivo muerto |
| `E:\MEDIOEVO_ASSETS`, RPG, TCG | frontera privada | `BLOQUEADO` para limpieza publica |

## Hallazgos Fundamentales

1. El ruido mas peligroso no era un duplicado: era una frontera Git mal alineada. Mientras el repo padre veia todo el perfil de Windows, cualquier status o commit podia mezclar fuentes privadas con codigo.
2. `Downloads` ya fue absorbido por el Curador activo en esta medicion: no quedan archivos actuales en `Downloads`, y el indice marca 180 fuentes fichadas.
3. Los duplicados grandes restantes no son candidatos directos a borrar. Muchos son TCG/assets privados, licencias validas por paquete, evidencia de releases o bases de datos runtime.
4. Los archivos grandes activos detectados son memoria/runtime, no basura por defecto:

| path | tamano | decision |
|---|---:|---|
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\cogni_kernel_memory.sqlite3` | `41.82 MB` | `KEEP_REVIEW_RUNTIME_MEMORY` |
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\claudio_bootstrap.db` | `33.39 MB` | `KEEP_REVIEW_RUNTIME_MEMORY` |
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\logs\claudio_api_server.stdout.log` | `28.67 MB` | `CANDIDATE_ROTATE_AFTER_PROCESS_CHECK` |
| `-=MEDIOEVO=-\-=LIBROS\claudio\memory_index.db` | `27.55 MB` | `KEEP_REVIEW_RUNTIME_MEMORY` |

## Decision De Limpieza

| clase | accion ahora | razon |
|---|---|---|
| perfil Windows fuera de workspace | excluido localmente de Git | frontera estable, reversible, sin borrar |
| fuentes unicas absorbidas | conservar en Archivo Frio | el original no se borra si es unico |
| duplicados exactos seguros de Downloads | ya ejecutados por Curador | existe ficha, hash y WitnessLog |
| logs runtime grandes | revisar/rotar despues | puede estar activo; conservar tail y hash antes |
| `.git`, packs, vendors, modelos, assets privados | no tocar | no son basura por nombre |
| `.pytest_cache`, `__pycache__`, builds generados | candidatos | solo con gate y contencion de ruta |

## Protocolo Para Agentes

1. Abrir `docs\intake\CURADOR_MASTER_INDEX.md` para ver estado humano.
2. Consultar `runtime\curador_seto\curador_index.sqlite` para verdad operativa.
3. No usar `git add .` desde `C:\Users\L-Tyr`.
4. No borrar por extension, nombre o intuicion.
5. Todo retiro necesita: `SHA256`, ficha, reemplazo o regenerabilidad, decision de gate y evento WitnessLog.
6. Si un repo esta anidado, trabajar en su root propio y no mezclar commits entre repos.
7. Si un archivo toca RPG/TCG, familia, secretos, publicaciones, modelos pesados o acciones externas, queda `REVIEW` o `BLOQUEADO`.

## Pendientes De Siguiente Cierre

| pendiente | tipo | accion segura |
|---|---|---|
| repo padre aun tiene 84 lineas tracked-only modificadas | coordinacion | separar cambios por modulo y commits exactos |
| Claudio repo anidado esta ahead/dirty | coordinacion | esperar o trabajar solo por contrato de API/docs |
| `claudio_api_server.stdout.log` crecio a 28.67 MB | runtime cleanup | verificar proceso, guardar tail+hash, rotar si gate aprueba |
| assets website vs `E:\MEDIOEVO_ASSETS` | source-of-truth | crear mapa canonico antes de borrar duplicados |
| `publish_staging` contiene multiples repos | publicacion | mantener como staging; no publicar sin gate |
| Atlas actual refleja absorcion de Downloads pero no todos los continentes tienen fuentes | curaduria | ejecutar absorcion por root especifico cuando toque global |

## Resultado

El arbol queda mas estable porque Git ya no confunde el perfil completo con el proyecto. `Downloads` queda medido como vacio y absorbido en Curador. La siguiente limpieza real debe ir por carriles pequenos: logs runtime, caches regenerables, staging publico y source-of-truth de assets, no por borrado masivo.
