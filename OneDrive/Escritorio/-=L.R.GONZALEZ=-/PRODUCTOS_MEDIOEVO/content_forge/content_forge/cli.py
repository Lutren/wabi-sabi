from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core.engine import ContentForgeEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="content_forge", description="Content Forge Observacionista v1")
    parser.add_argument("--output-root", default="", help="Runtime output root override")
    sub = parser.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="Render a short video")
    add_common_job_args(render)
    render.add_argument("--video", default="", help="Optional input video")
    render.add_argument("--start", type=float, default=0.0)
    render.add_argument("--cut-silence", action="store_true")
    render.add_argument("--transcribe", action="store_true")

    carousel = sub.add_parser("carousel", help="Render a carousel video from images")
    add_common_job_args(carousel)
    carousel.add_argument("--duration-per-slide", type=float, default=2.0)

    status = sub.add_parser("status", help="Read job status")
    status.add_argument("--job-id", default="")
    status.add_argument("--limit", type=int, default=20)

    catalog = sub.add_parser("catalog", help="Build the curated public-safe asset catalog")
    catalog.add_argument("--max-items", type=int, default=500)

    sub.add_parser("health", help="Health check")
    sub.add_parser("simulate-stall", help="Create a stall simulation job")
    return parser


def add_common_job_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", default="MEDIOEVO")
    parser.add_argument("--title", default="")
    parser.add_argument("--format", default="shorts", choices=["tiktok", "shorts", "reel", "youtube"])
    parser.add_argument("--duration", type=float, default=8.0)
    parser.add_argument("--asset", "--assets", dest="assets", action="append", default=[])
    parser.add_argument("--music", default="")
    parser.add_argument("--transcript", default="")
    parser.add_argument("--platform", "--platforms", dest="platforms", action="append", default=[])
    parser.add_argument("--burn-subtitles", action="store_true")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_root = Path(args.output_root) if getattr(args, "output_root", "") else None
    engine = ContentForgeEngine(output_root=output_root)
    if args.command == "health":
        result = engine.health()
    elif args.command == "catalog":
        result = engine.asset_catalog(max_items=args.max_items)
    elif args.command == "status":
        result = engine.status(job_id=args.job_id or None, limit=args.limit)
    elif args.command == "simulate-stall":
        result = engine.simulate_stall()
    elif args.command == "render":
        result = engine.render(args_to_request(args))
    elif args.command == "carousel":
        request = args_to_request(args)
        request["duration_per_slide"] = args.duration_per_slide
        result = engine.carousel(request)
    else:
        raise ValueError(f"Unsupported command: {args.command}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok", False) or args.command in {"status", "health", "simulate-stall"} else 1


def args_to_request(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "prompt": args.prompt,
        "title": args.title,
        "format": args.format,
        "duration": args.duration,
        "assets": args.assets,
        "music": args.music,
        "transcript": args.transcript,
        "platforms": flatten_platforms(args.platforms),
        "burn_subtitles": bool(args.burn_subtitles),
        "video": getattr(args, "video", ""),
        "start": getattr(args, "start", 0.0),
        "cut_silence": bool(getattr(args, "cut_silence", False)),
        "transcribe": bool(getattr(args, "transcribe", False)),
    }


def flatten_platforms(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        out.extend([part.strip() for part in str(value).split(",") if part.strip()])
    return out


if __name__ == "__main__":
    raise SystemExit(main())
