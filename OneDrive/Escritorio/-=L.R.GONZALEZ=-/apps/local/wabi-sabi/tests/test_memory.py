from wabi_sabi.cli.main import execute_prompt
from wabi_sabi.core.memory import LocalMemory


def test_memory_appends_events(tmp_path):
    runtime = tmp_path / "runtime"
    execute_prompt("ejecuta diagnostico", workspace=tmp_path, runtime_root=runtime, json_mode=True)

    memory = LocalMemory(runtime)
    events = memory.tail_events()

    assert events
    assert events[-1]["agent"] == "debugger"
    assert events[-1]["ok"] is True


def test_memory_reads_conversation_summary(tmp_path):
    runtime = tmp_path / "runtime"
    memory = LocalMemory(runtime)
    memory.append_memory(
        {
            "channel": "wabi_auto_conversation",
            "prompt": "sacame algo para redes",
            "route": "hybrid_codex_background",
            "output": "ActionGate Lite para agentes",
        }
    )

    assert "ActionGate Lite" in memory.conversation_summary()
    assert memory.tail_memory()[-1]["route"] == "hybrid_codex_background"
