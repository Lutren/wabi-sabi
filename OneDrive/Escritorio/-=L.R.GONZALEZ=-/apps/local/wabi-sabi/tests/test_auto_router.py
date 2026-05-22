from wabi_sabi.cli.parser import parse_command
from wabi_sabi.core.auto_router import decide_auto_route


def test_auto_routes_simple_diagnostic_to_local_agent():
    parsed = parse_command("ejecuta diagnostico")
    decision = decide_auto_route(
        "ejecuta diagnostico",
        parsed,
        {"auto_provider": "codex-cli"},
    )

    assert decision.route == "local_agent"
    assert decision.gate == "APPROVE"


def test_auto_routes_broad_decision_to_codex_when_available():
    prompt = "analiza el repo y decide que es mejor usar"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "codex-cli"})

    assert decision.route == "codex"
    assert "provider:codex-cli" in decision.reasons


def test_auto_routes_codex_mentions_to_codex_even_if_parser_sees_code():
    prompt = "responde como Codex y decide siguiente paso"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "codex-cli"})

    assert decision.route == "codex"


def test_auto_degrades_broad_decision_to_dry_run_without_provider():
    prompt = "analiza el repo y decide que es mejor usar"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "dry-run"})

    assert decision.route == "codex_dry_run"
    assert "no_model_provider_available" in decision.reasons


def test_auto_blocks_external_actions_before_provider_choice():
    prompt = "publica esto en github"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "codex-cli"})

    assert decision.route == "blocked"
    assert decision.gate == "BLOCK"


def test_auto_supports_operator_directives():
    decision = decide_auto_route("/local analiza esto", parse_command("analiza esto"), {"auto_provider": "codex-cli"})
    assert decision.route == "local_agent"
    assert decision.forced is True

    dry = decide_auto_route("/dry analiza esto", parse_command("analiza esto"), {"auto_provider": "codex-cli"})
    assert dry.route == "codex_dry_run"
    assert dry.forced is True


def test_auto_blocks_empty_forced_directives():
    decision = decide_auto_route("/codex", parse_command("/codex"), {"auto_provider": "codex-cli"})

    assert decision.route == "blocked"
    assert decision.gate == "BLOCK"
    assert "empty_prompt" in decision.reasons


def test_auto_keeps_casual_function_testing_local_chat():
    prompt = "hola, estoy probando las funciones"
    parsed = parse_command(prompt)
    decision = decide_auto_route(prompt, parsed, {"auto_provider": "codex-cli"})

    assert parsed.intent == "general"
    assert decision.route == "local_chat"
    assert "local_conversation" in decision.reasons


def test_auto_answers_identity_locally():
    prompt = "hola estoy haciendo pruebas, dime tu nombre"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "codex-cli"})

    assert decision.route == "local_chat"


def test_auto_routes_public_safe_release_ask_to_hybrid_blueprint_brief():
    prompt = "sacame algo de tech que pueda liberar hoy por redes y que sea solucion a algun problema actual"
    decision = decide_auto_route(prompt, parse_command(prompt), {"auto_provider": "codex-cli"})

    assert decision.route == "hybrid_codex"
    assert "local_blueprint_brief" in decision.reasons
