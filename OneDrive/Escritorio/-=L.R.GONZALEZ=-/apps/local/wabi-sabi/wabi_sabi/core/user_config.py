from __future__ import annotations

from pathlib import Path


CONFIG_DIR = Path.home() / ".medioevo" / "wabi"
CONFIG_PATH = CONFIG_DIR / "config.yaml"
DEFAULT_RUNTIME_DIR = CONFIG_DIR / "runtime"

DEFAULT_CONFIG_TEXT = """default_mode: chat
default_workspace_policy: current_directory_with_confirmation
default_runtime_dir: "%USERPROFILE%\\\\.medioevo\\\\wabi\\\\runtime"
provider_strategy: auto_free_first
preferred_cloud_order:
  - nvidia
  - gemini
  - deepseek
  - qwen
  - openrouter
  - local
chat_order:
  - nvidia
  - gemini
  - deepseek
  - local
  - qwen
  - openrouter
coding_order:
  - nvidia
  - deepseek
  - gemini
  - qwen
  - local
private_order:
  - local
disabled_until_fixed:
  - anthropic
coding:
  require_apply_confirmation: true
  create_rollback: true
  run_tests_when_available: true
  never_touch_private_release_paths: true
models:
  nvidia: "nvidia/nemotron-3-super-120b-a12b"
  qwen: "qwen-plus"
  dashscope_qwen: "qwen-plus"
  deepseek: "deepseek-chat"
  local_ollama: "qwen2.5-coder:3b"
local:
  smoke_model: "qwen2.5:0.5b"
  coding_model: "qwen2.5-coder:3b"
providers:
  deepseek:
    type: openai_compatible
    base_url: "https://api.deepseek.com/v1"
    env_key: "DEEPSEEK_API_KEY"
    default_model: "deepseek-chat"
  qwen:
    type: openai_compatible
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    env_key_candidates:
      - "DASHSCOPE_API_KEY"
      - "QWEN_API_KEY"
    default_model: "qwen-plus"
  openrouter:
    type: openai_compatible
    base_url: "https://openrouter.ai/api/v1"
    env_key: "OPENROUTER_API_KEY"
    default_model: "deepseek/deepseek-chat"
"""


REQUIRED_BLOCKS: dict[str, str] = {
    "default_mode:": 'default_mode: chat\n',
    "default_workspace_policy:": "default_workspace_policy: current_directory_with_confirmation\n",
    "default_runtime_dir:": 'default_runtime_dir: "%USERPROFILE%\\\\.medioevo\\\\wabi\\\\runtime"\n',
    "provider_strategy:": "provider_strategy: auto_free_first\n",
    "preferred_cloud_order:": "preferred_cloud_order:\n  - nvidia\n  - qwen\n  - deepseek\n  - openrouter\n  - local\n",
    "chat_order:": "chat_order:\n  - local\n  - nvidia\n  - qwen\n  - deepseek\n  - openrouter\n",
    "coding_order:": "coding_order:\n  - nvidia\n  - deepseek\n  - qwen\n  - local\n",
    "private_order:": "private_order:\n  - local\n",
    "disabled_until_fixed:": "disabled_until_fixed:\n  - anthropic\n  - gemini\n",
    "coding:": (
        "coding:\n"
        "  require_apply_confirmation: true\n"
        "  create_rollback: true\n"
        "  run_tests_when_available: true\n"
        "  never_touch_private_release_paths: true\n"
    ),
    "models:": (
        "models:\n"
        '  nvidia: "nvidia/nemotron-3-super-120b-a12b"\n'
        '  qwen: "qwen-plus"\n'
        '  dashscope_qwen: "qwen-plus"\n'
        '  deepseek: "deepseek-chat"\n'
        '  local_ollama: "qwen2.5-coder:3b"\n'
    ),
    "local:": 'local:\n  smoke_model: "qwen2.5:0.5b"\n  coding_model: "qwen2.5-coder:3b"\n',
    "providers:": (
        "providers:\n"
        "  deepseek:\n"
        "    type: openai_compatible\n"
        '    base_url: "https://api.deepseek.com/v1"\n'
        '    env_key: "DEEPSEEK_API_KEY"\n'
        '    default_model: "deepseek-chat"\n'
        "  qwen:\n"
        "    type: openai_compatible\n"
        '    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"\n'
        "    env_key_candidates:\n"
        '      - "DASHSCOPE_API_KEY"\n'
        '      - "QWEN_API_KEY"\n'
        '    default_model: "qwen-plus"\n'
        "  openrouter:\n"
        "    type: openai_compatible\n"
        '    base_url: "https://openrouter.ai/api/v1"\n'
        '    env_key: "OPENROUTER_API_KEY"\n'
        '    default_model: "deepseek/deepseek-chat"\n'
    ),
}


def ensure_user_config() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8", newline="\n")
        return CONFIG_PATH

    text = CONFIG_PATH.read_text(encoding="utf-8", errors="replace")
    additions: list[str] = []
    for marker, block in REQUIRED_BLOCKS.items():
        if marker not in text:
            additions.append(block.rstrip())
    if additions:
        suffix = "\n\n# Added by Wabi local repair: required default keys without overwriting existing values.\n"
        suffix += "\n\n".join(additions)
        CONFIG_PATH.write_text(text.rstrip() + suffix + "\n", encoding="utf-8", newline="\n")
    return CONFIG_PATH


def default_runtime_root() -> Path:
    ensure_user_config()
    return DEFAULT_RUNTIME_DIR
