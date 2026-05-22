from __future__ import annotations

import os
import subprocess
from typing import Any


def hidden_subprocess_kwargs() -> dict[str, Any]:
    """Return Windows kwargs that prevent transient console windows."""
    if os.name != "nt":
        return {}

    kwargs: dict[str, Any] = {}
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    if creationflags:
        kwargs["creationflags"] = creationflags

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= getattr(subprocess, "STARTF_USESHOWWINDOW", 1)
    startupinfo.wShowWindow = 0
    kwargs["startupinfo"] = startupinfo
    return kwargs


def run_hidden(*popenargs: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    for key, value in hidden_subprocess_kwargs().items():
        kwargs.setdefault(key, value)
    return subprocess.run(*popenargs, **kwargs)
