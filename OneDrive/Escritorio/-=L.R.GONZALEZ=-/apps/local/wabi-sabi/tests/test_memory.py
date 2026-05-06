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
