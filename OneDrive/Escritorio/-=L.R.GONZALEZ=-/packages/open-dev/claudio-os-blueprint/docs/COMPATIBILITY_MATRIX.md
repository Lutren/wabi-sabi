# Compatibility Matrix

Brain OS avoids lock-in by making the core protocol boring and durable:
HTTP, JSON, JSONL, SQLite, Markdown and common media formats.

## Core Formats

| Surface | Format |
| --- | --- |
| Decisions | JSON payloads |
| Witness logs | JSONL |
| Local memory | SQLite |
| Docs and plans | Markdown |
| Audio | WAV, MP3 |
| Video | MP4 |
| Images | PNG, JPG, WebP |
| Captions | SRT, VTT |
| API contracts | OpenAPI / JSON Schema |

## Platform Strategy

| Platform | Role | First path |
| --- | --- | --- |
| Linux | Primary runtime | systemd services, local APIs, CLI |
| Windows | Current work host | bridge CLI, WSL2, local HTTP, files |
| macOS | Portable creator host | bridge CLI, local HTTP, files |
| Android | Companion | capture, chat, approval, assets |
| iOS | Companion | capture, chat, approval, assets |
| PC2 Linux | Server dock | small models, jobs, storage, guardian |

## Compatibility Rules

- Critical workflows must work through files and local HTTP before a native UI
  is required.
- The same decision payload must work from CLI, local API, Windows bridge,
  Linux service and companion clients.
- Browser automation is assisted only: local session, manifest, kill switch,
  witness and approval for external effects.
- APIs for YouTube, TikTok, Meta or other providers stay behind approval gates.
- No workflow depends on hidden credentials embedded in code.
- Local model and agent APIs must bind to loopback by default. On Windows,
  run `scripts/windows_harden_loopback.ps1` to catch drift before connecting
  companions or PC2.

## What This Does Not Promise

- It does not run every Windows or macOS application natively.
- It does not replace Android or iOS.
- It does not bypass platform security, captchas or account restrictions.
- It does not publish automatically without approval.

The durable target is interoperability, not domination of every platform.
