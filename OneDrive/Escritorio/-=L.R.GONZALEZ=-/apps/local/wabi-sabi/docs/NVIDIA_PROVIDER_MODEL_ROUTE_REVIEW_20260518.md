# NVIDIA Provider Model Route Review 2026-05-18

StateFingerprint: `WABI-CLOUD-PROVIDER-v0-5-20260518`

## Estado

- Provider principal configurado: `nvidia`.
- Modelo primario configurado: `nvidia/llama-3.1-nemotron-ultra-253b-v1`.
- Fallback local: `ollama/qwen2.5:0.5b`.
- Ultimo smoke real v0.4: `SMOKE_FAIL_REDACTED`.
- Error observado: `PROVIDER_OR_MODEL_NOT_FOUND_REDACTED`.
- PublicationGate: `BLOCK`.

No se repitio smoke cloud en v0.5. El diagnostico actual es local y no envia
workspace, rutas, codigo, BRAIN_OS, canon, raw prompts, datasets ni logs
privados.

## Referencias oficiales NVIDIA

- NVIDIA API Reference registra el modelo como `nvidia / llama-3.1-nemotron-ultra-253b-v1`:
  `https://docs.api.nvidia.com/nim/reference/nvidia-llama-3_1-nemotron-ultra-253b-v1`
- La matriz NVIDIA NIM for LLMs lista `Llama 3.1 Nemotron Ultra 253B V1` con
  model id `nvidia/llama-3.1-nemotron-ultra-253b-v1`:
  `https://docs.nvidia.com/nim/large-language-models/1.8.0/models.html`
- La API NVIDIA NIM LLM expone endpoints OpenAI-compatible, incluyendo
  `POST /v1/chat/completions` y `GET /v1/models`:
  `https://docs.nvidia.com/nim/large-language-models/latest/reference/api-reference.html`
- La API de preview documenta `https://integrate.api.nvidia.com/v1/chat/completions`
  como chat completion compatible con OpenAI:
  `https://docs.api.nvidia.com/nim/reference/create_chat_completion_v1_chat_completions_post`

## Hipotesis del 404/provider not-found

1. Endpoint base incorrecto para esa cuenta o producto.
2. Formato de model id incorrecto en el adapter o alias.
3. Cuenta sin entitlement al modelo.
4. Region o API route distinta para el catalogo habilitado.
5. Billing/cuota no activado para ese modelo.
6. SDK adapter usando una ruta legacy.
7. Wrapper OpenAI-compatible requiere otro path o un model id exacto obtenido
   desde View code / API Reference en la cuenta NVIDIA.

## Alias candidatos locales

- `nvidia/llama-3.1-nemotron-ultra-253b-v1`
- `nvidia/llama-3_1-nemotron-ultra-253b-v1`
- `llama-3.1-nemotron-ultra-253b-v1`
- `llama-3_1-nemotron-ultra-253b-v1`

Estos aliases solo quedan registrados para revision. No se ejecutan llamadas
cloud por alias en v0.5.

## Que revisar sin compartir secretos

- Catalogo o dashboard NVIDIA API de la cuenta.
- Endpoint base mostrado por NVIDIA para el modelo.
- Model id exacto desde View code / API Reference.
- Presencia de variable de entorno como booleano redactado, sin imprimir valor.
- Entitlement de cuenta para `Llama-3.1-Nemotron-Ultra-253B-v1`.
- Cuota/billing de la cuenta.
- Si el modo OpenAI-compatible usa `/v1/chat/completions`, `/v1/responses` u
  otro path gestionado por NVIDIA para esa cuenta.
- Si `GET /v1/models` esta disponible como diagnostico seguro; en v0.5 queda
  `REVIEW_MODEL_LIST_API`, no implementado por defecto.

## Que no hacer

- No pegar API keys en chat.
- No commitear `.env`.
- No publicar headers.
- No enviar workspace.
- No enviar BRAIN_OS, Fragmentos, canon completo, libros, RPG/TCG, raw prompts
  ni datasets.
- No repetir llamadas ciegas por alias.
- No declarar `SMOKE_PASS` sin respuesta JSON exacta, parseada y exitosa.

## Siguiente accion segura

Revisar manualmente el dashboard/API Reference de NVIDIA y seleccionar un alias
unico solo despues de confirmar endpoint, entitlement y request shape. La
siguiente llamada, si se habilita, debe ser una unica prueba minima con el
prompt JSON de smoke y sin workspace.
