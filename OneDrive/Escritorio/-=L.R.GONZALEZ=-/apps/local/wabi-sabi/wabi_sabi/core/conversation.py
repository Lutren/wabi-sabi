from __future__ import annotations

from typing import Any


FOLLOWUP_HINTS = {
    "aplicalo",
    "aplícalo",
    "continua",
    "continúa",
    "hazlo",
    "lo anterior",
    "sigamos",
    "sigue",
    "sigue con eso",
    "eso",
}


def local_chat_response(
    prompt: str,
    provider_status: dict[str, Any] | None = None,
    recent_memory: list[dict[str, Any]] | None = None,
) -> str:
    lowered = prompt.lower()
    if is_followup(prompt) and recent_memory:
        topic = recent_topic(recent_memory)
        if topic:
            return (
                f"Sigo con lo anterior: {topic}\n\n"
                "Aplicacion local segura:\n"
                "- No publico ni envio nada afuera desde aqui.\n"
                "- Te dejo una forma public-safe para usar ahora: presentar ActionGate Lite como una compuerta simple para agentes.\n"
                "- Copy: Antes de que un agente actue, debe mostrar evidencia, riesgo y frontera. Si no puede probarlo, no ejecuta: queda en REVIEW o BLOCK.\n"
                "- Siguiente paso local: convertir esto en un post corto o mini demo sintetica sin rutas privadas."
            )
    if any(item in lowered for item in {"contacto directo", "estamos en contacto", "estas ahi", "estás ahi", "hola"}):
        return (
            "Estoy aqui, Tyr. Esta ventana es contacto directo con Wabi-Sabi en modo local privado: "
            "publicacion, push y deploy estan bloqueados. Puedo conversar, revisar proyectos, razonar BRAIN_OS "
            "o preparar cambios de codigo con plan, diff, confirmacion y rollback. "
            "Detecto que quieres probarme como agente real; dime que quieres construir o revisar ahora."
        )
    if any(item in lowered for item in {"nombre", "llamas", "quien eres", "quién eres"}):
        return (
            "Soy Wabi-Sabi, el nodo conversacional local de MEDIOEVO/OSIT. "
            "Mi trabajo es entender la intencion, mantener ActionGate, usar proveedores locales o cloud autorizados "
            "sin imprimir secretos y convertir pedidos de codigo en plan/diff/apply/rollback."
        )
    if "bajo riesgo" in lowered or "qué puedo hacer hoy" in lowered or "que puedo hacer hoy" in lowered:
        return (
            "Hoy lo mas seguro es trabajar local y reversible: revisar live-state, cerrar un pendiente pequeno, "
            "preparar un plan de codigo con diff, o ejecutar un sandbox con rollback. "
            "Mantengo publicacion, push, deploy y secretos bloqueados."
        )
    if "no apliques" in lowered or "no apliques todavia" in lowered or "no apliques todavía" in lowered:
        return (
            "Correcto: no aplico nada. Puedo mostrarte el diff pendiente, explicar riesgos y dejar el plan listo. "
            "La escritura solo ocurre con /apply, /aplicar o una confirmacion clara."
        )
    loaded_count = _blueprint_count(provider_status)
    blueprint_note = f" Tengo {loaded_count} blueprint(s) cargados para guiar rutas y limites." if loaded_count else ""
    return (
        "Te sigo. Respondo en lenguaje natural y mantengo la ejecucion bloqueada hasta que haya plan, evidencia "
        f"y confirmacion cuando toque archivos reales.{blueprint_note} "
        "Si quieres programar, preparo primero un plan y un diff; si quieres solo pensar el sistema, conversamos directo."
    )


def blueprint_release_brief(prompt: str, provider_status: dict[str, Any] | None = None) -> str:
    loaded_count = _blueprint_count(provider_status)
    sources = _blueprint_sources(provider_status)
    source_line = f"Blueprints cargados: {loaded_count}." if loaded_count else "Blueprints cargados: no detectados en esta corrida."
    if sources:
        source_line += f" Base local: {', '.join(sources[:3])}."

    return "\n".join(
        [
            "Respuesta local inmediata:",
            source_line,
            "",
            "Candidato para liberar hoy sin revelar demasiado:",
            "ActionGate Lite para agentes: una mini guia + demo local que obliga a clasificar acciones como APPROVE, REVIEW o BLOCK antes de ejecutar.",
            "",
            "Problema actual que resuelve:",
            "Los agentes con permisos amplios pueden borrar, publicar o tocar datos sensibles demasiado rapido si no existe una compuerta de evidencia previa.",
            "",
            "Que puedes mostrar en redes:",
            "- El problema en 2 lineas.",
            "- Un flujo simple: observar -> adjuntar evidencia -> clasificar riesgo -> ejecutar solo si es reversible/local.",
            "- Un ejemplo sintetico, sin rutas privadas, sin prompts maestros y sin secretos.",
            "",
            "Que debes retener privado:",
            "- Runtime Claudio completo.",
            "- Blueprints internos, cuentas, rutas locales sensibles, libros completos, RPG/TCG y thresholds no revisados.",
            "",
            "Copy corto public-safe:",
            "Estoy separando agentes utiles de agentes peligrosos con una compuerta local: antes de actuar, el agente debe mostrar evidencia, riesgo y frontera. Si no puede probarlo, no ejecuta: queda en REVIEW o BLOCK.",
        ]
    )


def is_followup(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return any(hint in normalized for hint in {_normalize(item) for item in FOLLOWUP_HINTS})


def recent_topic(recent_memory: list[dict[str, Any]]) -> str:
    for item in reversed(recent_memory):
        prompt = str(item.get("prompt") or "")
        output = str(item.get("output") or "")
        combined = f"{prompt}\n{output}".lower()
        if "actiongate lite" in combined:
            return "ActionGate Lite para agentes, una propuesta public-safe para redes sin revelar el runtime privado"
        if "redes" in combined or "liberar" in combined or "public-safe" in combined:
            return "una pieza tech public-safe para redes, reteniendo blueprints internos y material privado"
        if prompt:
            return "el ultimo tema conversacional local"
    return ""


def _blueprint_count(provider_status: dict[str, Any] | None) -> int:
    policy = (provider_status or {}).get("blueprint_policy", {})
    sources = policy.get("sources") if isinstance(policy, dict) else []
    return len(sources) if isinstance(sources, list) else 0


def _blueprint_sources(provider_status: dict[str, Any] | None) -> list[str]:
    policy = (provider_status or {}).get("blueprint_policy", {})
    sources = policy.get("sources") if isinstance(policy, dict) else []
    output: list[str] = []
    if not isinstance(sources, list):
        return output
    for item in sources:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "")
        if path:
            output.append(path.rsplit("/", 1)[-1])
    return output


def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
    )
