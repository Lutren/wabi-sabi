# Content Forge Observacionista v1

Content Forge is a local-first rendering engine for MEDIOEVO campaigns. It
creates short videos, carousels, captions, previews, thumbnails and a
publish-ready package without posting automatically.

The engine writes each job under:

`runtime/content_forge/jobs/<job_id>/`

Job states:

`observando`, `planificando`, `renderizando`, `qa`, `esperando`,
`atascado`, `requiere_aprobacion`, `listo`, `fallido`.

## CLI

```powershell
python -m content_forge.cli render --prompt "Promo MEDIOEVO" --format shorts --duration 6 --burn-subtitles
python -m content_forge.cli carousel --prompt "Carrusel MEDIOEVO" --format reel --duration-per-slide 2
python -m content_forge.cli status --job-id <job_id>
python -m content_forge.cli catalog
```

Supported presets: `tiktok`, `shorts`, `reel`, `youtube`.

Voice cloning is disabled by default. STT uses local Whisper-compatible
libraries when present and falls back to prompt-based captions.

Durability controls:

- Assets come from public-safe roots by default; personal/artist folders are
  excluded unless a human passes explicit paths.
- If no public asset exists, Content Forge generates a local placeholder and
  records that fact in `warnings`.
- Every rendered video gets ffprobe QA, visual nonblank/contrast QA and stage
  timing metrics for learned observacionista thresholds.
