from __future__ import annotations

import argparse
from pathlib import Path

from .app.application import create_service
from .decision.styles import STYLE_PROFILES
from .tui import launch_tui


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AutoCut AI command line")
    sub = parser.add_subparsers(dest="command", required=True)

    batch = sub.add_parser("batch", help="Process one or many videos")
    batch.add_argument("video", nargs="+", help="Input video path(s)")
    batch.add_argument("--style", default="clean_shorts", choices=sorted(STYLE_PROFILES.keys()))
    batch.add_argument("--out", default="autocut_output", help="Output folder")
    batch.add_argument("--license", default="free", choices=["free", "pro"])
    batch.add_argument("--intensity", type=float, default=0.7)

    sub.add_parser("tui", help="Launch terminal UI")
    sub.add_parser("desktop", help="Launch desktop UI")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "tui":
        launch_tui()
        return

    if args.command == "desktop":
        from .ui.app import launch

        launch()
        return

    service = create_service(license_tier=args.license)
    service.config.product.edit_intensity = max(0.1, min(args.intensity, 1.0))

    results = service.batch_process(args.video, args.style)
    root = Path(args.out)
    root.mkdir(parents=True, exist_ok=True)

    for src, result in zip(args.video, results):
        target = root / Path(src).stem
        paths = service.export_all(result, target)
        print(f"[{src}] warnings: {result.warnings}")
        print(paths)


if __name__ == "__main__":
    main()
