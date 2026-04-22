from orchestrator import orchestrator


def test_recommend_model_prefers_available_strength(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("XAI_API_KEY", raising=False)

    assert orchestrator.recommend_model("revision") == "claude"


def test_run_task_returns_error_when_api_key_is_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = orchestrator.run_task(
        task="keywords",
        text="A science fiction manuscript",
        model_key="gpt",
        context={"lang": "en"},
    )

    assert result["status"] == "error"
    assert "API key not found" in result["result"]


def test_run_task_uses_custom_prompt(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setitem(orchestrator.CALLERS, "openai", lambda prompt, model_id, api_key: prompt)

    result = orchestrator.run_task(
        task="custom",
        text="Sample text",
        model_key="gpt",
        context={"lang": "en"},
        custom_prompt="Summarize this.",
    )

    assert result["status"] == "ok"
    assert "TEXT:\nSample text" in result["result"]
