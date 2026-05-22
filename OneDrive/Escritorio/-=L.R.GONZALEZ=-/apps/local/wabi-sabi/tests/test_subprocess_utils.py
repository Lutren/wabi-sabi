from __future__ import annotations

import os
import subprocess

from wabi_sabi.core.subprocess_utils import hidden_subprocess_kwargs


def test_hidden_subprocess_kwargs_match_platform():
    kwargs = hidden_subprocess_kwargs()
    if os.name == "nt":
        assert kwargs.get("creationflags") == subprocess.CREATE_NO_WINDOW
        assert "startupinfo" in kwargs
    else:
        assert kwargs == {}
