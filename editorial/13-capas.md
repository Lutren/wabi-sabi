# Sistema de 13 Capas Editoriales

**Framework de control de calidad para ficción larga.**

Desarrollado y probado en la saga MEDIOEVO (Libros I–III, ~70,000 palabras cada uno).

---

## Principio

La revisión editorial tiene dos enemigos: el orden equivocado y la falta de métricas.  
Arreglar la voz antes de arreglar la estructura es trabajo doble.  
Editar sin contar tics produce intuición, no control.

Este sistema resuelve ambos problemas: **orden de ejecución fijo + entregables cuantificables por capa**.

---

## ⚠️ Meta-regla

```
SI LA ESCENA FUNCIONA, LA REGLA PIERDE.
Verificar canon DESPUÉS, no paralizar ANTES.
PERO: "Funciona" requiere justificación técnica, no "me gustó".
```

---

## Las 13 Capas

Tiempo estimado por capa: **2–3 horas por cada ~70,000 palabras**.

---

### CAPA 1: LIMPIEZA TÉCNICA
**Objetivo:** Eliminar ruido que distorsiona el diagnóstico posterior.

- Encoding: `--` → `—`, mojibake, artefactos de Pandoc
- Normalizar títulos y headers para tabla de contenidos
- Eliminar placeholders editoriales visibles (`[COMPLETAR]`, `[VER NOTA]`)
- Fix typos mecánicos: doble espacio, puntuación duplicada, comillas curvas

**Entregable:** Texto limpio sin ruido técnico. Diff antes/después.

---

### CAPA 2: SATURACIÓN DE CÓDIGO (motifs y tics)
**Objetivo:** Detectar y reducir repetición mecánica que el ojo ya no ve.

```bash
# Ejemplo de flujo de trabajo
grep -c "algo que" manuscrito.txt
grep -c "silencio" manuscrito.txt
grep -c "847" manuscrito.txt
```

**Umbrales recomendados** (ajusta según extensión del libro):

| Elemento | Máximo sugerido |
|---|---|
| Número/símbolo recurrente único | 5 por libro |
| Segundo símbolo recurrente | 20 por libro |
| Sinestesia sensorial ("zumbido") | 20 por libro |
| Nombre de personaje central | 60 por libro |
| "algo que" | 70 por libro |
| "como si" abstracto | 15 por libro |
| "el tipo de" | 10 por libro |
| "No era X. Era Y." | 10 por libro |
| "silencio" decorativo | 30 por libro |

**Entregable:** Conteo antes/después de cada motif intervenido.

---

### CAPA 3: ANTI-INSISTENCIA
**Objetivo:** Eliminar frases que nombran lo que la escena ya mostró.

Buscar y cortar:
- "Era evidente que..."
- "No tenía opción."
- "El peso de lo que acababa de pasar..."
- Cualquier frase que explique la emoción que el lector acaba de vivir

**Excepción válida:** Dato frío de personaje analítico que registra hechos como observador externo. ("Tercera vez en doce días." — esto es caracterización, no insistencia.)

**Entregable:** Lista de cortes con cita ≤20 palabras y justificación.

---

### CAPA 4: MOTOR DEL PROTAGONISTA
**Objetivo:** Verificar que el protagonista actúa por deseo propio, no solo reacciona.

Pregunta por capítulo: **¿El protagonista HACE algo o solo RECIBE cosas?**

- Identificar capítulos donde es 100% reactivo
- Insertar al menos una decisión activa por capítulo
- Cada decisión activa debe costar algo irreversible (una relación, una información, una posibilidad)

**Entregable:** Mapa de decisiones activas vs reactivas por capítulo.

---

### CAPA 5: EXPOSICIÓN → ESCENA
**Objetivo:** Convertir bloques informativos en experiencia dramática.

Señales de alerta:
- Párrafos con listas de datos del mundo
- Diálogos que suenan a conferencia
- Cualquier bloque donde el narrador explica el sistema en lugar de mostrar su efecto

**Técnica de conversión:**
1. Efecto humano concreto primero
2. Explicación parcial después (solo lo que el personaje necesitaría saber)
3. El lector reconstruye el sistema. No lo des completo.

**Entregable:** Antes/después de cada bloque convertido.

---

### CAPA 6: ANTI-INVENTARIO + ANTI-BARROCO
**Objetivo:** Cada detalle justificado, no acumulado.

Reglas:
- Máximo 2 detalles por párrafo. El tercero solo si contradice o sorprende.
- Filtro de POV: ¿Este personaje, en este momento, notaría este detalle? Si no, cortar.
- Descripciones de 4+ líneas: condensar a 2.
- Eliminar descripción tipo cámara documental (inventario sin perspectiva)

**Entregable:** Lista de bloques intervenidos.

---

### CAPA 7: IDIOLECTO + ESTRUCTURA
**Objetivo:** Que cada personaje suene diferente. Que la estructura sirva al significado.

Por personaje:
- Identificar 2–3 patrones de habla únicos (vocabulario, longitud de frase, qué evita decir)
- Verificar que en diálogos largos, las voces son distinguibles sin etiquetas

Estructura:
- Revisar spoilers en paratextos (glosarios, epígrafes)
- Identificar escenas débiles de cierre
- Fijar al menos 1 cortocircuito por personaje secundario por libro (gesto no utilitario que revela sin explicar)

**Entregable:** Guía de voz por personaje + lista de fixes estructurales.

---

### CAPA 8: ANTI-ANALOGÍA + ANTI-TELEOLOGÍA
**Objetivo:** Eliminar las dos muletas más comunes de la prosa de género.

**Anti-analogía:**
- Eliminar: "como si" + concepto abstracto/filosófico
- Conservar: "como si" + imagen física concreta
- Reemplazar siempre con descripción física directa

**Anti-teleología:**
- Eliminar: "No sabía que sería la última vez..."
- Eliminar: "Pronto entendería que..."
- Eliminar: cualquier frase que revela que el narrador sabe el futuro

**Entregable:** Antes/después por instancia identificada.

---

### CAPA 9: CIERRE DE CAPÍTULOS + ANTI-SOLEMNIDAD
**Objetivo:** Capítulos que terminan en acción, imagen o silencio. No en resumen.

- Verificar que ningún capítulo termina con reflexión del protagonista sobre lo que acaba de pasar
- Si hay 3+ páginas de solemnidad consecutiva sin alivio: insertar humor, absurdo, o lo mundano interrumpiendo lo grave

**Tipos de humor que no rompen el tono:**
1. Burocracia con lógica perfecta → resultado ridículo
2. Lo mundano interrumpiendo lo grave (alguien tiene hambre durante la revelación cósmica)
3. El personaje haciendo algo absurdo sin saber que es gracioso

**Entregable:** Lista de finales de capítulo corregidos + momentos de alivio insertados.

---

### CAPA 10: BLOQUES ENCICLOPÉDICOS
**Objetivo:** Condensar lo que queda de exposición después de la Capa 5.

- Inventario de estaciones/locaciones/sistemas: cortar a mínimo funcional
- Verificar que toda regla del mundo mostrada tiene consecuencia mostrada
- Eliminar enumeraciones de futuro con nombres propios ("En el año X, Y haría Z")

**Entregable:** Bloques condensados con conteo de palabras antes/después.

---

### CAPA 11: EMOCIONES + RECONCILIACIONES
**Objetivo:** Que los motivos sean mezcla, no pureza. Que los cierres emocionales cuesten.

- Eliminar reconciliaciones limpias (el conflicto debe dejar rastro)
- Verificar que ningún abrazo o reencuentro funciona como recompensa sin costo
- Cortar "el tipo de" decorativos ("era el tipo de persona que...")
- Cortar "algo que" vagos ("había algo que no podía nombrar")
- Verificar que ninguna emoción se llama por su nombre si ya se mostró físicamente

**Entregable:** Métricas de tics intervenidos + lista de correcciones emocionales.

---

### CAPA 12: LIMPIEZA FINAL
**Objetivo:** Diagnóstico de longitud y coherencia global.

- Repetición mecánica residual: "No era X. Era Y." decorativos
- Verbos débiles en bloques explicativos (ser/estar/haber donde debería haber acción)
- Verificar entropía vs propósito: ¿cada escena cambia algo de forma irreversible?
- Conteo final de palabras por capítulo y verificar que la longitud refleja la tensión

**Entregable:** Métricas finales + diagnóstico de longitud por capítulo.

---

### CAPA 13: PRODUCCIÓN
**Objetivo:** Paquete completo de publicación.

- Generar EPUB (metadata, CSS, TOC)
- Generar PDF Paperback (6×9", márgenes KDP)
- Generar PDF Hardcover (6.14×9.21")
- Generar DOCX editorial
- Marketing: sinopsis corta/larga, keywords, BISAC, prompts de portada

**Entregable:** Paquete completo listo para subir a KDP.

---

## Orden de ejecución

```
Capas 1–3:   Mecánicas (rápidas, se pueden hacer en una sesión)
Capas 4–6:   Estructurales (requieren decisiones del autor)
Capas 7–8:   Voz y estilo (más tiempo por capa)
Capas 9–11:  Revisión fina de tono y emoción
Capa 12:     Diagnóstico final
Capa 13:     Producción
```

---

## Checklist unificado

```
CAPA 1:  [ ] Encoding limpio  [ ] Headers normalizados  [ ] Sin placeholders
CAPA 2:  [ ] Tics contados  [ ] Umbrales respetados  [ ] Conteo antes/después
CAPA 3:  [ ] Sin explicaciones post-escena  [ ] Sin "era evidente"
CAPA 4:  [ ] Protagonista activo  [ ] Decisiones con costo
CAPA 5:  [ ] Sin bloques informativos puros  [ ] Efecto humano primero
CAPA 6:  [ ] Máx 2 detalles/párrafo  [ ] Filtro POV aplicado
CAPA 7:  [ ] Voces distinguibles  [ ] Cortocircuito por secundario
CAPA 8:  [ ] Sin "como si" abstractos  [ ] Sin teleología
CAPA 9:  [ ] Cierres en acción/imagen/silencio  [ ] Humor insertado donde necesario
CAPA 10: [ ] Sin inventarios  [ ] Cada regla tiene consecuencia
CAPA 11: [ ] Motivos mixtos  [ ] Sin reconciliaciones limpias
CAPA 12: [ ] Longitud calibrada  [ ] Entropía verificada
CAPA 13: [ ] EPUB  [ ] PDF Paperback  [ ] PDF Hardcover  [ ] Marketing
```

---

## Sobre los umbrales

Los umbrales de la Capa 2 son sugerencias calibradas para libros de ~70,000 palabras. Escalan linealmente. Para un libro de 35,000 palabras, divide los umbrales a la mitad.

Lo importante no es el número exacto: es el hábito de **contar antes de editar**.

---

*Desarrollado en producción — no en teoría. Probado en Libros I, II y III de MEDIOEVO.*  
*Licencia MIT.*
