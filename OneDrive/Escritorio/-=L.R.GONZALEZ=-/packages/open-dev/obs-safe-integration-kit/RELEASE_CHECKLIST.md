# Release Checklist

Status: required before any public push or package upload.

- [x] `python -m pytest -q` passes from this package root.
- [x] Python files compile with `python -m py_compile`.
- [x] CLI/import smoke passes without writing secrets or external state.
- [x] `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, `SECURITY.md` and `LICENSE` are present.
- [x] Secret scan reports `count_reported=0`.
- [x] Path scrub finds no local machine paths, private game paths or account/service names.
- [x] Claims scan reviewed; prohibited categories appear only as negative boundary language.
- [x] No caches, build outputs, virtualenvs, vendor folders or raw intake/source files are included.
- [ ] Destination repo/package name is selected.
- [ ] ActionGate and host gate approve the exact external action.

Current state: local package promotion only. External publication remains blocked until the gate passes for a concrete destination.
