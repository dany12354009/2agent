from __future__ import annotations

import argparse
from pathlib import Path

from .app.application import create_service
from .decision.styles import STYLE_PROFILES


def main() -> None:
    parser = argparse.ArgumentParser(description="AutoCut AI production CLI")
    parser.add_argument("video", nargs="+", help="Input video path(s)")
    parser.add_argument("--style", default="clean_shorts", choices=sorted(STYLE_PROFILES.keys()))
    parser.add_argument("--out", default="autocut_output", help="Output folder")
    parser.add_argument("--license", default="free", choices=["free", "pro"])
    parser.add_argument("--intensity", type=float, default=0.7)
    args = parser.parse_args()

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
