# Lobby de Alejandria - Reglas Operativas

Generated UTC: `2026-05-06T06:30:32Z`

Estado: `INBOX_DOCUMENTAL_ACTIVO`

## Movimiento ejecutado

- Estado actual: `C:\Users\L-Tyr\OneDrive\Escritorio\promts`
- Accion ejecutada: renombrar a `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria`
- Motivo: convertir la carpeta de prompts/documentos en lobby de absorcion, no en archivo permanente.
- Reversibilidad: alta; el cambio es un rename de carpeta y queda registrado aqui.
- Archivos iniciales detectados: `14`
- Archivo de reglas creado: `README_LOBBY_DE_ALEJANDRIA.md`
- SHA256 README: `9E18FC3530731CF0AF711986A05C37BEF986CAE77E3289D872D13EDEBB5FDEFE`

## Contrato

El Lobby no es canon final. Es una zona de llegada para fuentes que deben ser procesadas.

Flujo obligatorio:

1. Registrar ruta, tipo, tamano, fecha y SHA256 cuando sea viable.
2. Clasificar amenaza si viene de internet o de una descarga reciente.
3. Crear ficha por archivo o ficha de lote.
4. Extraer insight, tarea, claim, tecnica, riesgo y sinapsis.
5. Conectar al Atlas: PSI, Claudio/Wabi-Sabi, DUAT/GEODIA, Seguridad, Publicacion, Producto, Privado/Bloqueado o Curaduria.
6. Retirar del Lobby solo despues de absorcion:
   - duplicado exacto seguro -> cuarentena/borrado seguro con hash;
   - fuente unica -> archivo frio canonico;
   - riesgo o duda -> `REVIEW` o `BLOQUEADO`.

## Limpieza diaria

La limpieza diaria debe correr sobre:

- `Downloads`: primero amenaza, despues ficha y absorcion.
- `Lobby de Alejandria`: ficha, absorcion y retiro seguro.

No se ejecutan archivos del Lobby. No se publican fuentes del Lobby. No se borran fuentes unicas sin ficha y sinapsis.
