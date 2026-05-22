import json

from wabi_sabi.core.job_queue import JobStore, format_job_result, summarize_jobs


def test_job_store_writes_reads_and_summarizes(tmp_path):
    store = JobStore(tmp_path / "runtime")
    payload = {
        "job_id": "job-test",
        "kind": "codex",
        "status": "done",
        "provider": "codex-cli",
        "prompt": "analiza",
        "output": "respuesta",
        "artifacts": [],
        "error": "",
    }

    path = store.write(payload)

    assert path.exists()
    assert store.read("job-test")["output"] == "respuesta"
    assert store.latest_id() == "job-test"
    assert "job-test" in summarize_jobs(store.list_recent())
    assert "respuesta" in format_job_result(json.loads(path.read_text(encoding="utf-8")))
